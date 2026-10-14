"""Scan orchestration: discovery loop + parallel port scanning.

Two engines are supported:
  * nmap engine (if nmap is installed and enabled) - one nmap process per host,
  * pure-Python engine - one thread task per port.

The discovery loop runs continuously; it repeats until `Ctrl+C` (SIGINT) and
starts scanning the ports of every newly found host concurrently.
"""

from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional

import host_discovery
import mac_vendor
import network_info
import nmap_engine
import port_scan
import services
from config import Settings
from helpers import clock, parse_port_list
from models import HostInfo, PortInfo
from report import Report


class Scanner:
    """Main class managing discovery + port scanning."""

    def __init__(self, settings: Settings, report: Report):
        self.settings = settings
        self.report = report
        self.hosts: Dict[str, HostInfo] = {}
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

        self.ports = parse_port_list(settings.ports.list)

        # Engine selection: use nmap if present and enabled.
        self.nmap_path = nmap_engine.nmap_path() if settings.nmap.enabled else None
        self.nmap_active = bool(self.nmap_path)

        # Per-port pool for the pure-Python port scan.
        self.pool = ThreadPoolExecutor(
            max_workers=max(1, settings.ports.concurrency), thread_name_prefix="port"
        )
        # Per-host pool for nmap (nmap processes can be heavy).
        self.nmap_pool = ThreadPoolExecutor(
            max_workers=max(1, settings.nmap.concurrency), thread_name_prefix="nmap"
        )

        self.network: Optional[network_info.NetworkInfo] = None
        self.last_scan: Dict[str, float] = {}

    # -- external control --------------------------------------------------
    def stop(self, *_):
        """Raise the stop flag (Ctrl+C / SIGTERM)."""
        self.stop_event.set()

    def engine_name(self) -> str:
        if self.nmap_active:
            kind = "privileged" if nmap_engine.is_privileged() else "unprivileged"
            return f"nmap ({kind})"
        return "pure Python"

    # -- main loop ---------------------------------------------------------
    def run(self) -> None:
        try:
            self.network = network_info.get_network_info(
                self.settings.network, self.settings
            )
        except ValueError as error:
            self.report.error(str(error))
            return

        self.report.start(self.network, len(self.ports), self.engine_name())
        try:
            while not self.stop_event.is_set():
                self._one_pass()
                if self.settings.single_pass:
                    break
                self.stop_event.wait(self.settings.discovery.interval)
        finally:
            self.pool.shutdown(wait=True)
            self.nmap_pool.shutdown(wait=True)
            self.report.finish(self._current_hosts())

    def _current_hosts(self) -> Dict[str, HostInfo]:
        with self.lock:
            return dict(self.hosts)

    # -- discovery pass ----------------------------------------------------
    def _one_pass(self) -> None:
        """One discovery round: update seen hosts, scan new ones, mark lost ones."""
        found = self._discover()
        now = time.time()
        new_hosts: List[HostInfo] = []
        back_online: List[HostInfo] = []
        went_offline: List[HostInfo] = []

        with self.lock:
            # 1) Seen this round: add if new, refresh if present, flag if returned.
            for ip, data in found.items():
                host = self.hosts.get(ip)
                if host is None:
                    host = HostInfo(ip=ip, first_seen=clock(), last_seen=clock())
                    self.hosts[ip] = host
                    new_hosts.append(host)
                elif not host.online:
                    back_online.append(host)

                host.online = True
                host.missed_rounds = 0
                host.last_seen = clock()

                if data.get("ttl") is not None:
                    host.ttl = data["ttl"]
                    host.os_guess = services.ttl_to_os_guess(host.ttl)
                if data.get("rtt_ms") is not None:
                    host.rtt_ms = data["rtt_ms"]
                if host.method == "?":
                    host.method = data.get("method", "?")
                mac = data.get("mac")
                if mac:
                    host.mac = mac
                    host.vendor = data.get("vendor") or mac_vendor.find_vendor(mac)

            # 2) Online hosts not seen this round: counter grows; offline at threshold.
            threshold = max(1, self.settings.discovery.offline_threshold)
            for ip, host in self.hosts.items():
                if ip in found or not host.online:
                    continue
                host.missed_rounds += 1
                if host.missed_rounds >= threshold:
                    host.online = False
                    went_offline.append(host)

        # New hosts: announce + start the port scan (scope expands).
        for host in new_hosts:
            self.report.host_found(host)
            self._start_scan(host)

        # Returning hosts: announce + re-scan their ports.
        for host in back_online:
            self.report.host_back_online(host)
            self._start_scan(host)

        # Lost hosts: stay in the list, only flagged.
        for host in went_offline:
            self.report.host_offline(host)

        # Optional: re-scan known online hosts at a fixed interval.
        if self.settings.ports.rescan_interval > 0:
            with self.lock:
                again = [
                    h
                    for h in self.hosts.values()
                    if h.online
                    and h.scan_done
                    and (now - self.last_scan.get(h.ip, 0))
                    >= self.settings.ports.rescan_interval
                ]
            for host in again:
                self._start_scan(host)

    def _discover(self) -> Dict[str, dict]:
        """Find live hosts with the selected engine."""
        if self.nmap_active and self.settings.nmap.discovery:
            raw = nmap_engine.discover(
                self.network.cidr, self.settings.nmap.extra_options
            )
            for data in raw.values():
                data.setdefault("ttl", None)
                data.setdefault("rtt_ms", None)
                data.setdefault("method", "nmap")
            # nmap scans the whole CIDR; drop our own IP unless requested
            # (the pure-Python path already excludes it from the target list).
            if not self.settings.include_self:
                raw.pop(self.network.local_ip, None)
            return raw
        return host_discovery.find_hosts(self.network.target_ips, self.settings)

    # -- port scanning -----------------------------------------------------
    def _start_scan(self, host: HostInfo) -> None:
        with self.lock:
            host.scan_done = False
            host.pending_ports = 0 if self.nmap_active else len(self.ports)
            host.ports.clear()
            self.last_scan[host.ip] = time.time()

        if self.nmap_active:
            # One nmap process per host.
            self.nmap_pool.submit(self._nmap_host_task, host)
        else:
            # One task per port.
            for port in self.ports:
                self.pool.submit(self._port_task, host, port)

    def _nmap_host_task(self, host: HostInfo) -> None:
        info = nmap_engine.scan_ports(host.ip, self.ports, self.settings.nmap)
        with self.lock:
            host.ports = info
            host.scan_done = True
            host.pending_ports = 0
        for port in sorted(info):
            if info[port].state == "open":
                self.report.port_found(host.ip, info[port])
        self.report.host_scan_done(host)

    def _port_task(self, host: HostInfo, port: int) -> None:
        state, banner = port_scan.scan_port(
            host.ip, port, self.settings.ports.timeout, self.settings.ports.banner
        )
        done = False
        with self.lock:
            pb = PortInfo(
                port=port,
                state=state,
                service=services.port_service_name(port),
                banner=banner,
            )
            host.ports[port] = pb
            host.pending_ports -= 1
            if host.pending_ports <= 0:
                host.scan_done = True
                done = True
        if state == "open":
            self.report.port_found(host.ip, pb)
        if done:
            self.report.host_scan_done(host)
