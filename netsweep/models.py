"""Data models: objects produced during discovery and scanning.

`HostInfo` represents one IP, `PortInfo` the result for a single port.
The reporting and persistence layer uses these objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PortInfo:
    """Scan result for a single port."""

    port: int
    state: str  # "open" | "closed" | "filtered"
    service: str = "?"
    banner: Optional[str] = None


@dataclass
class HostInfo:
    """A discovered host and (if any) its port scan results."""

    ip: str
    mac: Optional[str] = None
    vendor: Optional[str] = None
    ttl: Optional[int] = None
    os_guess: Optional[str] = None
    method: str = "?"  # how the host was found: ping | arp | tcp | nmap
    rtt_ms: Optional[float] = None
    first_seen: str = ""
    last_seen: str = ""
    ports: Dict[int, PortInfo] = field(default_factory=dict)
    scan_done: bool = False
    pending_ports: int = 0
    online: bool = True  # seen in recent rounds?
    missed_rounds: int = 0  # consecutive discovery rounds without a sighting

    def open_ports(self) -> List[int]:
        """Sorted list of ports whose state is 'open'."""
        return sorted(p for p, b in self.ports.items() if b.state == "open")

    def to_dict(self) -> dict:
        """Dictionary representation for JSON/CSV output."""
        return {
            "ip": self.ip,
            "mac": self.mac,
            "vendor": self.vendor,
            "ttl": self.ttl,
            "os_guess": self.os_guess,
            "method": self.method,
            "rtt_ms": self.rtt_ms,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "online": self.online,
            "open_ports": self.open_ports(),
            "ports": {
                str(p): {"state": b.state, "service": b.service, "banner": b.banner}
                for p, b in sorted(self.ports.items())
            },
        }
