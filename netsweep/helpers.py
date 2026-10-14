"""Small utilities: ANSI colors, IP math, port list parsing, thread-safe
printing and duration formatting.

This module does not depend on any other project module; other modules take
helpers from here. This keeps the dependency direction always "towards the
leaves".
"""

from __future__ import annotations

import ipaddress
import threading
import time
from typing import List, Sequence, Union


class Color:
    """ANSI escape sequences (terminal colors)."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GRAY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


# Single global lock so multiple threads never write to the console at once.
PRINT_LOCK = threading.Lock()


def write(
    *parts,
    lock: "threading.Lock | None" = None,
    color: "str | None" = None,
    end: str = "\n",
    colored: bool = True,
) -> None:
    """Thread-safe console write."""
    lock = lock or PRINT_LOCK
    text = "".join(str(p) for p in parts)
    if color and colored:
        text = f"{color}{text}{Color.RESET}"
    with lock:
        print(text, end=end, flush=True)


def ip_to_int(ip: str) -> int:
    """'192.168.0.1' -> integer."""
    return int(ipaddress.ip_address(ip))


def int_to_ip(value: int) -> str:
    """Integer -> '192.168.0.1'."""
    return str(ipaddress.ip_address(value))


def parse_port_list(spec: Union[str, Sequence[int]]) -> List[int]:
    """Turn '80,443,1-1024' or [80, 443] into a sorted, unique port list."""
    ports: List[int] = []

    if isinstance(spec, str):
        for part in spec.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                first, last = part.split("-", 1)
                first_i, last_i = int(first), int(last)
                if first_i > last_i:
                    first_i, last_i = last_i, first_i
                ports.extend(range(first_i, last_i + 1))
            else:
                ports.append(int(part))
    else:
        ports = [int(p) for p in spec]

    return sorted({p for p in ports if 0 < p < 65536})


def timestamp() -> str:
    """'2026-10-14 18:30:00'."""
    return time.strftime("%Y-%m-%d %H:%M:%S")


def clock() -> str:
    """'18:30:00'."""
    return time.strftime("%H:%M:%S")


def format_duration(seconds: float) -> str:
    """Format seconds as '1h 2m 3s'."""
    seconds = int(max(0, seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"
