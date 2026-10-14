"""Pure-Python port scanner: TCP connect attempt + banner grabbing.

A connection is made with `socket.connect_ex`; the result is one of three
states:
  "open"     — connection accepted,
  "closed"   — connection refused (RST) or no address,
  "filtered" — timeout (a firewall may be dropping the packets).

Banner grabbing depends on the port type: a TLS handshake on TLS ports, a HEAD
request on HTTP ports, and a raw read elsewhere.
"""

from __future__ import annotations

import errno
import socket
import ssl
from typing import Optional, Tuple

import services

# Error codes used to report 'closed' instead of 'filtered'.
REFUSED_ERRNOS = {errno.ECONNREFUSED}


def scan_port(
    ip: str, port: int, timeout: float = 0.7, banner: bool = True
) -> Tuple[str, Optional[str]]:
    """Scan a single port. Return (state, banner)."""
    family = socket.AF_INET6 if ":" in ip else socket.AF_INET
    try:
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            code = sock.connect_ex((ip, port))
            if code != 0:
                return ("closed" if code in REFUSED_ERRNOS else "filtered", None)
            if not banner:
                return ("open", None)
            return ("open", _grab_banner(sock, ip, port))
    except socket.timeout:
        return ("filtered", None)
    except OSError:
        return ("closed", None)


def _grab_banner(sock: socket.socket, ip: str, port: int) -> Optional[str]:
    """Try to grab a short banner from an open port."""
    try:
        if port in services.TLS_PORTS:
            return _tls_banner(sock, ip)
        if port in services.HTTP_PORTS:
            return _http_banner(sock, ip)
        sock.settimeout(1.0)
        return _clean(sock.recv(512))
    except Exception:
        return None


def _tls_banner(sock: socket.socket, ip: str) -> Optional[str]:
    """Do a TLS handshake and return the protocol version and cipher suite."""
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with context.wrap_socket(sock, server_hostname=ip) as tls_sock:
            version = tls_sock.version()
            cipher = tls_sock.cipher()
        suite = cipher[0] if cipher else ""
        return f"TLS {version} {suite}".strip()
    except Exception:
        return None


def _http_banner(sock: socket.socket, ip: str) -> Optional[str]:
    """Send an HTTP HEAD request and return the 'Server:' header or status line."""
    request = (
        f"HEAD / HTTP/1.0\r\nHost: {ip}\r\n"
        "User-Agent: netsweep\r\nConnection: close\r\n\r\n"
    )
    try:
        sock.sendall(request.encode("ascii", "ignore"))
        sock.settimeout(1.5)
        chunks = []
        total = 0
        while total < 1024:
            chunk = sock.recv(512)
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
    except Exception:
        chunks = []

    text = b"".join(chunks).decode("utf-8", "replace")
    for line in text.splitlines():
        if line.strip().lower().startswith("server:"):
            return line.strip()[:200]
    first = text.splitlines()[0].strip() if text.strip() else ""
    return first[:200] or None


def _clean(data: bytes) -> Optional[str]:
    """Reduce raw bytes to the first meaningful line."""
    if not data:
        return None
    text = data.decode("utf-8", "replace").strip()
    if not text:
        return None
    return text.splitlines()[0][:200]
