"""Live host discovery: ping sweep, ARP table and TCP probing (pure Python).

OS-dependent work (ping command, ARP table) is delegated to the
`platform_info` layer, so this module works the same on Linux and Windows.

If nmap is installed and enabled in the settings, `nmap_engine` gives more
accurate results; this module always remains the fallback engine.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

import platform_info
import port_scan
from config import Settings


def ping_once(
    ip: str, timeout: float = 1.0
) -> tuple[bool, Optional[int], Optional[float]]:
    """Ping a single address. Return (alive, ttl, rtt_ms).

    The command and output parsing are done in `platform_info` per OS.
    """
    return platform_info.ping_once(ip, timeout)


def ping_sweep(ip_list: List[str], timeout: float, concurrency: int) -> Dict[str, dict]:
    """Ping all IPs in parallel; return only the live ones."""
    found: Dict[str, dict] = {}
    with ThreadPoolExecutor(
        max_workers=max(1, concurrency), thread_name_prefix="ping"
    ) as pool:
        futures = {pool.submit(ping_once, ip, timeout): ip for ip in ip_list}
        for future in as_completed(futures):
            ip = futures[future]
            try:
                alive, ttl, rtt = future.result()
            except Exception:
                alive = False
            if alive:
                found[ip] = {"ttl": ttl, "rtt_ms": rtt, "method": "ping"}
    return found


def read_arp_table() -> Dict[str, str]:
    """IP -> MAC mapping (Linux: /proc/net/arp, Windows: `arp -a`)."""
    return platform_info.read_arp_table()


def tcp_alive(ip: str, ports, timeout: float) -> bool:
    """Determine if a host is up via a TCP connect attempt.

    Even 'closed' (connection refused) shows the host is alive.
    """
    for port in ports:
        state, _ = port_scan.scan_port(ip, port, timeout, banner=False)
        if state in ("open", "closed"):
            return True
    return False


def find_hosts(ip_list: List[str], settings: Settings) -> Dict[str, dict]:
    """Find live hosts with the pure-Python engine.

    Return {ip: {ttl, rtt_ms, method, mac}}.
    """
    found = ping_sweep(
        ip_list, settings.discovery.ping_timeout, settings.discovery.concurrency
    )
    macs = read_arp_table()

    # Hosts in the ARP table (recently talked) count as alive.
    for ip in ip_list:
        if ip not in found and ip in macs:
            found[ip] = {"ttl": None, "rtt_ms": None, "method": "arp"}

    # TCP probe for those that don't answer ping.
    if settings.discovery.tcp_probe:
        missing = [ip for ip in ip_list if ip not in found]
        if missing:
            with ThreadPoolExecutor(
                max_workers=max(1, settings.discovery.concurrency),
                thread_name_prefix="tcp-discovery",
            ) as pool:
                futures = {
                    pool.submit(
                        tcp_alive,
                        ip,
                        settings.discovery.probe_ports,
                        settings.ports.timeout,
                    ): ip
                    for ip in missing
                }
                for future in as_completed(futures):
                    ip = futures[future]
                    try:
                        if future.result():
                            found[ip] = {"ttl": None, "rtt_ms": None, "method": "tcp"}
                    except Exception:
                        pass

    for ip in found:
        found[ip]["mac"] = macs.get(ip)
    return found
