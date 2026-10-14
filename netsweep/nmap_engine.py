"""nmap engine: uses nmap for more accurate discovery/port scanning when it
is installed.

Output is taken as XML (`-oX -`) and parsed with `xml.etree`. If nmap is
missing or disabled in the settings, the caller falls back to the pure-Python
engine (`host_discovery` + `port_scan`).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

import platform_info
import services
from models import PortInfo

# Map nmap state names to our state names.
STATE_MAP = {
    "open": "open",
    "closed": "closed",
    "filtered": "filtered",
    "unfiltered": "open",
    "open|filtered": "filtered",
    "closed|filtered": "closed",
}


def nmap_path() -> Optional[str]:
    """Path to the nmap executable (None if missing)."""
    path = shutil.which("nmap")
    if path:
        return path
    if platform_info.is_windows():
        for candidate in platform_info.NMAP_WINDOWS_PATHS:
            if os.path.exists(candidate):
                return candidate
    return None


def is_root() -> bool:
    """Is the process running as administrator/root? (needed for SYN scan.)"""
    return platform_info.is_admin()


def privilege_flag() -> str:
    """Flag that tells nmap the privilege state explicitly.

    Arch's nmap is built without libcap, so it cannot detect its own file
    capability; therefore `--privileged`/`--unprivileged` is passed by hand.
    """
    return "--privileged" if is_privileged() else "--unprivileged"


def is_privileged() -> bool:
    """Can a privileged (SYN/OS/ARP) scan be performed?

    Linux  : True if root, or if the nmap binary has `cap_net_raw`.
             e.g. sudo setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip /usr/bin/nmap
    Windows: True if administrator AND Npcap is installed; otherwise a `-sT`
             (no-privilege) scan is used.
    """
    admin = is_root()
    if platform_info.is_windows():
        return admin and platform_info.has_npcap()
    if admin:
        return True
    path = nmap_path()
    if not path:
        return False
    try:
        result = subprocess.run(
            ["getcap", path], capture_output=True, text=True, timeout=5
        )
        return "cap_net_raw" in (result.stdout or "")
    except Exception:
        return False


def _run(command: List[str], timeout: float) -> str:
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout or ""
    except Exception:
        return ""


def _root(xml_text: str):
    try:
        return ET.fromstring(xml_text)
    except ET.ParseError:
        return None


def discover(cidr: str, extra_options: Optional[List[str]] = None) -> Dict[str, dict]:
    """Find live hosts with `nmap -sn`.

    Returned dict: {ip: {"method": "nmap", "mac": ..., "vendor": ...}}
    """
    command = ["nmap", "-sn", privilege_flag(), "-n", "-oX", "-"]
    if extra_options:
        command[1:1] = list(extra_options)
    command.append(cidr)

    root = _root(_run(command, 600))
    if root is None:
        return {}

    result: Dict[str, dict] = {}
    for host in root.findall("host"):
        status = host.find("status")
        if status is None or status.get("state") != "up":
            continue
        ip = mac = vendor = None
        for address in host.findall("address"):
            addrtype = address.get("addrtype")
            if addrtype in ("ipv4", "ipv6"):
                ip = address.get("addr")
            elif addrtype == "mac":
                mac = (address.get("addr") or "").upper()
                vendor = address.get("vendor")
        if ip:
            result[ip] = {
                "method": "nmap",
                "mac": mac,
                "vendor": vendor,
                "rtt_ms": _rtt_ms(host),
            }
    return result


def _rtt_ms(host_element) -> Optional[float]:
    """Round-trip time (seconds) from the `<times srtt="..."/>` field in nmap XML."""
    times = host_element.find("times")
    if times is None or not times.get("srtt"):
        return None
    try:
        return round(int(times.get("srtt")) / 1000.0, 3)
    except ValueError:
        return None


def scan_ports(
    ip: str, ports: List[int], nmap_settings, extra_options: Optional[List[str]] = None
) -> Dict[int, PortInfo]:
    """nmap port scan for a single host. Return {port: PortInfo}."""
    scan_type = "-sS" if is_privileged() else "-sT"
    command = [
        "nmap",
        scan_type,
        privilege_flag(),
        "-Pn",
        "-n",
        "-T4",
        "-p",
        ",".join(str(p) for p in ports),
        "-oX",
        "-",
    ]
    if getattr(nmap_settings, "version_detection", False):
        command.append("-sV")

    options = (
        extra_options
        if extra_options is not None
        else getattr(nmap_settings, "extra_options", [])
    )
    if options:
        command.extend(list(options))
    command.append(ip)

    root = _root(_run(command, getattr(nmap_settings, "timeout", 300)))
    if root is None:
        return {}

    result: Dict[int, PortInfo] = {}
    for host in root.findall("host"):
        for port in host.findall("./ports/port"):
            try:
                pid = int(port.get("portid"))
            except (TypeError, ValueError):
                continue
            state_e = port.find("state")
            state = STATE_MAP.get(
                state_e.get("state") if state_e is not None else "", "closed"
            )

            service = port.find("service")
            # Both engines use the same dictionary, so we check our own table first.
            name = services.port_service_name(pid)
            banner = None
            if service is not None:
                if name == "?":
                    name = service.get("name") or "?"
                parts = [
                    service.get("product"),
                    service.get("version"),
                    service.get("extrainfo"),
                ]
                banner = " ".join(p for p in parts if p) or None

            result[pid] = PortInfo(port=pid, state=state, service=name, banner=banner)
    return result
