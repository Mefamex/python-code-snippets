"""Platform layer: all OS-dependent work is collected in this single file.

Linux and native Windows are supported. Other modules never call system
commands directly; ping, ARP table, interface/prefix/gateway and MAC
information all come from here. This keeps portability managed in one place.

The parsing functions are **pure functions**: they take text and return data;
they never run commands. This makes the Windows outputs testable on Linux too.
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
from typing import Dict, Optional, Tuple

WINDOWS = os.name == "nt"

# Common install paths tried when nmap is not on PATH (Windows).
NMAP_WINDOWS_PATHS = [
    r"C:\Program Files (x86)\Nmap\nmap.exe",
    r"C:\Program Files\Nmap\nmap.exe",
]

# Color (ANSI) support is determined during startup preparation.
_COLOR_SUPPORT = True

# One-shot cache for the Windows network info.
# Order: (interface, ip, prefix, gateway)
_NETWORK_CACHE: Optional[
    Tuple[Optional[str], Optional[str], Optional[int], Optional[str]]
] = None

# Turns Get-NetIPConfiguration output into JSON (property names are
# language-independent).
_POWERSHELL_COMMAND = [
    "powershell",
    "-NoProfile",
    "-NonInteractive",
    "-Command",
    "Get-NetIPConfiguration | Where-Object { $_.IPv4DefaultGateway -ne $null } | "
    "Select-Object -First 1 -Property InterfaceAlias,"
    "@{n='IPv4';e={$_.IPv4Address[0].IPAddress}},"
    "@{n='Prefix';e={$_.IPv4Address[0].PrefixLength}},"
    "@{n='Gateway';e={$_.IPv4DefaultGateway[0].NextHop}} | ConvertTo-Json",
]


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------
def is_windows() -> bool:
    """Is the process running on Windows?"""
    return WINDOWS


def _run_full(command: list, timeout: float) -> Tuple[Optional[int], str]:
    """Run a command; return (returncode, output). On error (None, "").

    Output is captured as bytes first and then decoded as UTF-8 with
    `replace`, so the ASCII tokens are correct regardless of the local code
    page.
    """
    try:
        result = subprocess.run(command, capture_output=True, timeout=timeout)
    except Exception:
        return None, ""
    raw = result.stdout or b""
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="replace")
    return result.returncode, raw


def _run(command: list, timeout: float = 5.0) -> str:
    """Run a command; return only the output (" " on error)."""
    return _run_full(command, timeout)[1]


# ---------------------------------------------------------------------------
# Ping
# ---------------------------------------------------------------------------
def parse_linux_ping(
    output: str, returncode: Optional[int]
) -> Tuple[bool, Optional[int], Optional[float]]:
    """Interpret Linux/BSD `ping` output. Return (alive, ttl, rtt_ms)."""
    text = output or ""
    if returncode != 0 and "ttl=" not in text.lower():
        return (False, None, None)

    ttl = None
    m = re.search(r"ttl=(\d+)", text, re.I)
    if m:
        ttl = int(m.group(1))

    rtt = None
    m = re.search(r"time=([\d.]+)\s*ms", text, re.I)
    if m:
        rtt = float(m.group(1))

    return (True, ttl, rtt)


def parse_windows_ping(
    output: str, returncode: Optional[int]
) -> Tuple[bool, Optional[int], Optional[float]]:
    """Interpret Windows `ping` output. Return (alive, ttl, rtt_ms).

    On a localized Windows the "time" label may be translated; therefore only
    the `<number> ms` form is matched for RTT. `TTL=` is stable in every
    language.
    """
    text = output or ""
    lower = text.lower()
    # No reply (localized "request timed out" text) => no TTL.
    if "ttl" not in lower:
        return (False, None, None)

    ttl = None
    m = re.search(r"ttl[=:](\d+)", text, re.I)
    if m:
        ttl = int(m.group(1))

    rtt = None
    if re.search(r"<\s*[\d.]+\s*ms", text):
        rtt = 0.5  # round-trip too short to measure (e.g. "<1ms")
    else:
        m = re.search(r"([\d.]+)\s*ms", text)
        if m:
            rtt = float(m.group(1))

    return (True, ttl, rtt)


def ping_once(
    ip: str, timeout: float = 1.0
) -> Tuple[bool, Optional[int], Optional[float]]:
    """Ping a single address. Return (alive, ttl, rtt_ms)."""
    if WINDOWS:
        ms = max(1, int(round(timeout * 1000)))
        code, output = _run_full(
            ["ping", "-n", "1", "-w", str(ms), ip], max(2.0, timeout + 3.0)
        )
        return parse_windows_ping(output, code)

    wait = max(1, int(round(timeout)))
    code, output = _run_full(["ping", "-c", "1", "-W", str(wait), "-n", ip], wait + 2)
    return parse_linux_ping(output, code)


# ---------------------------------------------------------------------------
# ARP table (IP -> MAC)
# ---------------------------------------------------------------------------
def parse_linux_arp(text: str) -> Dict[str, str]:
    """Turn `/proc/net/arp` content into an IP -> MAC dict."""
    table: Dict[str, str] = {}
    for line in (text or "").splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 4 and parts[3] != "00:00:00:00:00:00":
            table[parts[0]] = parts[3].upper()
    return table


def parse_windows_arp(text: str) -> Dict[str, str]:
    """Turn Windows `arp -a` output into an IP -> MAC dict.

    Headers/labels may be localized; therefore only the "IP MAC" form
    (numeric IP + hyphenated MAC) is matched. Multicast/broadcast entries are
    filtered out.
    """
    table: Dict[str, str] = {}
    pattern = re.compile(
        r"(\d{1,3}(?:\.\d{1,3}){3})\s+([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})"
    )
    for line in (text or "").splitlines():
        m = pattern.search(line)
        if not m:
            continue
        ip = m.group(1)
        if ip.startswith(("224.", "239.", "255.")) or ip == "0.0.0.0":
            continue  # multicast / broadcast / invalid
        mac = m.group(2).replace("-", ":").upper()
        if mac != "00:00:00:00:00:00":
            table[ip] = mac
    return table


def read_arp_table() -> Dict[str, str]:
    """Return the IP -> MAC mapping for the current platform."""
    if WINDOWS:
        return parse_windows_arp(_run(["arp", "-a"], 10))
    try:
        with open("/proc/net/arp", encoding="utf-8") as file:
            return parse_linux_arp(file.read())
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Interface / prefix / gateway
# ---------------------------------------------------------------------------
def local_ip_udp() -> Optional[str]:
    """Find the local IP via a UDP socket (no command, works on all platforms)."""
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))  # no packet is sent, only the route is chosen
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        if s is not None:
            try:
                s.close()
            except Exception:
                pass


def _linux_default_interface() -> Tuple[Optional[str], Optional[str]]:
    """(interface, ip) from the default route; else the first IPv4 interface."""
    output = _run(["ip", "-o", "route", "get", "1.1.1.1"])
    interface = ip = None
    m = re.search(r"\bdev\s+(\S+)", output)
    if m:
        interface = m.group(1)
    m = re.search(r"\bsrc\s+(\d+\.\d+\.\d+\.\d+)", output)
    if m:
        ip = m.group(1)
    if interface and ip:
        return interface, ip

    for line in _run(["ip", "-o", "-4", "addr", "show"]).splitlines():
        m = re.search(r"\d+:\s+(\S+)\s+inet\s+(\d+\.\d+\.\d+\.\d+)/\d+", line)
        if m and m.group(1) != "lo":
            return m.group(1), m.group(2)
    return None, None


def _linux_prefix_length(interface: str, ip: str) -> Optional[int]:
    """Prefix length for the given IP on the interface (e.g. /24 -> 24)."""
    for line in _run(["ip", "-o", "-4", "addr", "show", "dev", interface]).splitlines():
        m = re.search(r"inet\s+" + re.escape(ip) + r"/(\d+)", line)
        if m:
            return int(m.group(1))
    return None


def _linux_gateway() -> Optional[str]:
    """Default gateway (Linux)."""
    m = re.search(r"default\s+via\s+(\S+)", _run(["ip", "route", "show", "default"]))
    return m.group(1) if m else None


def parse_windows_powershell_network(
    json_text: str,
) -> Tuple[Optional[str], Optional[str], Optional[int], Optional[str]]:
    """Parse `Get-NetIPConfiguration | ConvertTo-Json` output.

    Return (interface, ip, prefix, gateway). It may be an object or a
    single-element list.
    """
    data = json.loads(json_text)
    if isinstance(data, list):
        data = data[0] if data else {}
    if not isinstance(data, dict):
        return None, None, None, None

    def _first(value):
        return value[0] if isinstance(value, list) and value else value

    interface = _first(data.get("InterfaceAlias"))
    ip = _first(data.get("IPv4"))
    gateway = _first(data.get("Gateway"))

    prefix = _first(data.get("Prefix"))
    if prefix is not None:
        try:
            prefix = int(prefix)
        except (TypeError, ValueError):
            prefix = None
    return interface, ip, prefix, gateway


def _windows_network_raw() -> Tuple[
    Optional[str], Optional[str], Optional[int], Optional[str]
]:
    """Get the Windows network info (once): (interface, ip, prefix, gateway)."""
    global _NETWORK_CACHE
    if _NETWORK_CACHE is not None:
        return _NETWORK_CACHE

    interface = ip = gateway = None
    prefix: Optional[int] = None

    output = _run(_POWERSHELL_COMMAND, 15)
    if output.strip():
        try:
            interface, ip, prefix, gateway = parse_windows_powershell_network(output)
        except Exception:
            interface = ip = gateway = None
            prefix = None

    if not ip:
        ip = local_ip_udp()
        if ip and prefix is None:
            prefix = 24
            print(
                "[!] Network prefix could not be detected; assuming /24.",
                file=sys.stderr,
            )

    _NETWORK_CACHE = (interface, ip, prefix, gateway)
    return _NETWORK_CACHE


def interface_ip_prefix() -> Tuple[Optional[str], Optional[str], Optional[int]]:
    """Active interface name, own IP and prefix length."""
    if WINDOWS:
        interface, ip, prefix, _gw = _windows_network_raw()
        return interface, ip, prefix

    interface, ip = _linux_default_interface()
    prefix = _linux_prefix_length(interface, ip) if (interface and ip) else None
    return interface, ip, prefix


def find_gateway() -> Optional[str]:
    """Default gateway address."""
    if WINDOWS:
        return _windows_network_raw()[3]
    return _linux_gateway()


# ---------------------------------------------------------------------------
# MAC address
# ---------------------------------------------------------------------------
def _uuid_mac() -> Optional[str]:
    """Last resort: machine MAC via `uuid.getnode()` (avoids random)."""
    try:
        import uuid

        node = uuid.getnode()
        if (node >> 40) & 0x01:  # multicast bit => randomly generated
            return None
        return ":".join(f"{(node >> i) & 0xFF:02X}" for i in range(40, -1, -8))
    except Exception:
        return None


def parse_windows_getmac(text: str, interface: Optional[str] = None) -> Optional[str]:
    """Pick a MAC from `getmac /v /fo csv` output.

    If `interface` (connection name) is given, the matching row wins;
    otherwise the first valid MAC is returned.
    """
    candidates = []
    matcher = re.compile(r"([0-9A-Fa-f]{2}(?:-[0-9A-Fa-f]{2}){5})")
    for line in (text or "").splitlines():
        m = matcher.search(line)
        if not m:
            continue
        mac = m.group(1).replace("-", ":").upper()
        if mac == "00:00:00:00:00:00":
            continue
        fields = [f.strip().strip('"') for f in line.split(",")]
        name = fields[0] if fields else ""
        candidates.append((name, mac))

    if interface:
        for name, mac in candidates:
            if name.lower() == interface.lower():
                return mac
    return candidates[0][1] if candidates else None


def local_mac(interface: Optional[str]) -> Optional[str]:
    """MAC address of the active interface."""
    if WINDOWS:
        mac = parse_windows_getmac(
            _run(["getmac", "/v", "/fo", "csv", "/nh"], 10), interface
        )
        return mac or _uuid_mac()

    if interface:
        try:
            with open(f"/sys/class/net/{interface}/address", encoding="utf-8") as file:
                return file.read().strip().upper()
        except Exception:
            pass
    return _uuid_mac()


# ---------------------------------------------------------------------------
# Privilege (for nmap SYN scans)
# ---------------------------------------------------------------------------
def is_admin() -> bool:
    """Is the process running as administrator/root?"""
    if WINDOWS:
        try:
            import ctypes

            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False


def has_npcap() -> bool:
    """On Windows, is Npcap (raw packet driver for SYN scans) installed?"""
    if not WINDOWS:
        return False
    system_root = os.environ.get("SystemRoot", r"C:\Windows")
    candidates = [
        os.path.join(system_root, "System32", "Npcap", "wpcap.dll"),
        os.path.join(system_root, "System32", "wpcap.dll"),
    ]
    return any(os.path.exists(path) for path in candidates)


# ---------------------------------------------------------------------------
# Startup preparation (encoding + color)
# ---------------------------------------------------------------------------
def _enable_windows_ansi() -> bool:
    """Enable ANSI (VT) color codes in the Windows console."""
    try:
        import ctypes
        from ctypes import wintypes

        kernel = ctypes.windll.kernel32
        # STD_OUTPUT_HANDLE = -11
        handle = kernel.GetStdHandle(-11)
        mode = wintypes.DWORD()
        if not kernel.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        if not kernel.SetConsoleMode(
            handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
        ):
            return False
        return True
    except Exception:
        return False


def startup_prepare() -> bool:
    """Startup settings: stdout/stderr as UTF-8; ANSI on Windows.

    Return whether colors are usable (False => plain output).
    """
    global _COLOR_SUPPORT
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:
            pass

    _COLOR_SUPPORT = _enable_windows_ansi() if WINDOWS else True
    return _COLOR_SUPPORT


def color_support() -> bool:
    """Color (ANSI) support state (set by startup_prepare)."""
    return _COLOR_SUPPORT
