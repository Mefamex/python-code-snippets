"""Console output, coloring and saving results (JSON/CSV)."""

from __future__ import annotations

import csv
import json
import os
import time
from typing import Dict, List

from config import Settings, output_abs_path
from helpers import Color, clock, format_duration
from models import HostInfo, PortInfo


class Report:
    """Class that writes to the screen and saves results to disk."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.started_at = time.time()
        self.host_count = 0
        self.open_port_count = 0

    # -- basic writing -----------------------------------------------------
    def _print(
        self, text: str = "", *extra, color: str | None = None, end: str = "\n"
    ) -> None:
        full = text + "".join(str(e) for e in extra)
        if color and self.settings.color:
            full = f"{color}{full}{Color.RESET}"
        print(full, end=end, flush=True)

    def info(self, message: str) -> None:
        self._print(f"[*] {message}")

    def error(self, message: str) -> None:
        self._print(f"[!] {message}", color=Color.RED)

    # -- header / closing --------------------------------------------------
    def start(self, network, port_count: int, engine: str) -> None:
        self._print()
        self._print("═" * 62, color=Color.CYAN)
        self._print(
            "  LAN DISCOVERY + PARALLEL PORT SCAN", color=Color.BOLD + Color.CYAN
        )
        self._print("═" * 62, color=Color.CYAN)
        self._print(f"  Interface     : {network.interface}")
        self._print(f"  Network (CIDR): {network.cidr}")
        self._print(
            f"  Network addr  : {network.network_address}   "
            f"Broadcast: {network.broadcast}"
        )
        self._print(f"  Gateway       : {network.gateway}")
        self._print(f"  Own IP/MAC    : {network.local_ip} / {network.local_mac}")
        self._print(f"  Target hosts  : {len(network.target_ips)}")
        self._print(f"  Ports to scan : {port_count}")
        self._print(f"  Engine        : {engine}")
        self._print(f"  Output folder : {output_abs_path(self.settings)}")
        self._print("  To stop       : Ctrl+C")
        self._print("═" * 62, color=Color.CYAN)
        self._print()

    def host_found(self, host: HostInfo) -> None:
        self.host_count += 1
        label = f"{Color.GREEN}[+]{Color.RESET}" if self.settings.color else "[+]"
        extras = ""
        if host.mac:
            extras += f"  MAC={host.mac}"
        if host.vendor and host.vendor != "Unknown vendor":
            extras += f"  ({host.vendor})"
        if host.ttl:
            extras += f"  TTL={host.ttl}"
        if host.rtt_ms is not None:
            extras += f"  RTT={host.rtt_ms}ms"
        self._print(
            f"{clock()} {label} New host: {host.ip}{extras}  method={host.method}"
        )

    def port_found(self, ip: str, pb: PortInfo) -> None:
        self.open_port_count += 1
        line = f"{clock()}     {ip}:{pb.port} OPEN ({pb.service})"
        if pb.banner:
            line += f"  ->  {pb.banner}"
        self._print(line, color=Color.GREEN)

    def host_scan_done(self, host: HostInfo) -> None:
        open_ports = host.open_ports()
        extra = f": {', '.join(map(str, open_ports))}" if open_ports else ""
        self._print(
            f"{clock()}     {host.ip} scan done - {len(open_ports)} open ports{extra}",
            color=Color.DIM,
        )

    def host_offline(self, host: HostInfo) -> None:
        """Host no longer responds (stays in the list)."""
        self._print(
            f"{clock()} [-] Offline: {host.ip}  (last seen {host.last_seen})",
            color=Color.YELLOW,
        )

    def host_back_online(self, host: HostInfo) -> None:
        """A lost host reappeared; its ports will be re-scanned."""
        self._print(
            f"{clock()} [~] Back online: {host.ip} - rescanning its ports",
            color=Color.CYAN,
        )

    def finish(self, hosts: Dict[str, HostInfo]) -> None:
        duration = format_duration(time.time() - self.started_at)
        online = sum(1 for h in hosts.values() if h.online)
        offline = len(hosts) - online
        self._print()
        self._print("─" * 62, color=Color.CYAN)
        self._print(
            f"  Done. {len(hosts)} hosts ({online} online / {offline} offline), "
            f"{self.open_port_count} open ports, duration {duration}",
            color=Color.BOLD,
        )
        self._print("─" * 62, color=Color.CYAN)

        saved: List[str] = []
        if self.settings.output.json:
            path = self._save_json(hosts)
            if path:
                saved.append(path)
        if self.settings.output.csv:
            path = self._save_csv(hosts)
            if path:
                saved.append(path)
        for path in saved:
            self._print(f"  Saved: {path}", color=Color.CYAN)

    # -- saving ------------------------------------------------------------
    def _dir(self) -> str:
        path = output_abs_path(self.settings)
        os.makedirs(path, exist_ok=True)
        return path

    def _save_json(self, hosts: Dict[str, HostInfo]) -> str:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._dir(), f"scan_{stamp}.json")
        data = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "host_count": len(hosts),
            "hosts": [h.to_dict() for h in sorted(hosts.values(), key=lambda x: x.ip)],
        }
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return path
        except OSError:
            return ""

    def _save_csv(self, hosts: Dict[str, HostInfo]) -> str:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self._dir(), f"scan_{stamp}.csv")
        try:
            with open(path, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "ip",
                        "mac",
                        "vendor",
                        "ttl",
                        "os_guess",
                        "method",
                        "rtt_ms",
                        "open_ports",
                        "first_seen",
                        "last_seen",
                        "online",
                    ]
                )
                for h in sorted(hosts.values(), key=lambda x: x.ip):
                    writer.writerow(
                        [
                            h.ip,
                            h.mac or "",
                            h.vendor or "",
                            h.ttl or "",
                            h.os_guess or "",
                            h.method,
                            h.rtt_ms if h.rtt_ms is not None else "",
                            ";".join(map(str, h.open_ports())),
                            h.first_seen,
                            h.last_seen,
                            "1" if h.online else "0",
                        ]
                    )
            return path
        except OSError:
            return ""
