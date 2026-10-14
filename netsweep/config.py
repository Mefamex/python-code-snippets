"""Default values, `config.yaml` loading and the `Settings` configuration object.

Settings are read from the `config.yaml` file in this folder. The CLI (main.py)
overrides only the explicitly given options; everything else comes from the
file.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, List, Optional

try:  # PyYAML
    import yaml

    HAS_YAML = True
except Exception:  # pragma: no cover
    HAS_YAML = False


# Project root directory (the folder containing this file).
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")

# Default port list: common/service ports.
DEFAULT_PORT_STRING = (
    "20,21,22,23,25,53,69,80,88,110,111,123,135,137,138,139,143,161,"
    "389,443,445,465,514,515,548,587,631,636,873,902,993,995,1080,1194,"
    "1433,1521,1723,1883,2049,2082,2083,2181,2375,2376,3000,3128,3260,3306,"
    "3389,3478,5000,5060,5432,5672,5900,5985,5986,6000,6379,6443,7000,8000,"
    "8008,8080,8081,8088,8090,8123,8443,8888,9000,9090,9100,9200,9300,10000,"
    "11211,27017"
)

# Very common ports used by the --quick option.
QUICK_PORTS = [
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    135,
    139,
    143,
    443,
    445,
    993,
    995,
    1433,
    3306,
    3389,
    5900,
    8080,
    8443,
]

# Probe ports tried to catch hosts that do not answer ping.
DEFAULT_PROBE_PORTS = [22, 80, 135, 139, 443, 445, 3389, 5900, 8080]


@dataclass
class DiscoverySettings:
    """Live host discovery parameters."""

    interval: float = 5.0
    offline_threshold: int = 2
    ping_timeout: float = 1.0
    concurrency: int = 128
    tcp_probe: bool = True
    probe_ports: List[int] = field(default_factory=lambda: list(DEFAULT_PROBE_PORTS))


@dataclass
class PortSettings:
    """Parameters for the pure-Python port scanner."""

    list: str = DEFAULT_PORT_STRING
    timeout: float = 0.7
    concurrency: int = 200
    banner: bool = True
    rescan_interval: float = 0.0


@dataclass
class NmapSettings:
    """Parameters for the nmap engine."""

    enabled: bool = True
    discovery: bool = True
    version_detection: bool = True
    concurrency: int = 16
    timeout: int = 300
    extra_options: List[str] = field(default_factory=list)


@dataclass
class OutputSettings:
    """Saving/output parameters."""

    directory: str = "output"
    json: bool = True
    csv: bool = True


@dataclass
class Settings:
    """Top-level object holding the whole configuration."""

    network: Optional[str] = None
    include_self: bool = False
    max_hosts: int = 4096
    single_pass: bool = False
    color: bool = True
    discovery: DiscoverySettings = field(default_factory=DiscoverySettings)
    ports: PortSettings = field(default_factory=PortSettings)
    nmap: NmapSettings = field(default_factory=NmapSettings)
    output: OutputSettings = field(default_factory=OutputSettings)


def _fill(obj: Any, data: Any) -> Any:
    """Fill a dataclass object from a dict; unknown keys are ignored."""
    if not isinstance(data, dict):
        return obj
    for name, value in data.items():
        if hasattr(obj, name):
            setattr(obj, name, value)
    return obj


def _list_to_text(value: Any) -> str:
    """Turn a YAML list into '80,443' form."""
    if isinstance(value, (list, tuple)):
        return ",".join(str(x) for x in value)
    return str(value)


def load_settings(path: Optional[str] = None) -> Settings:
    """Read config.yaml and fill missing fields with defaults."""
    path = path or DEFAULT_CONFIG_PATH
    data: dict = {}

    if os.path.exists(path):
        if not HAS_YAML:
            raise RuntimeError("PyYAML not found. Install: pip install pyyaml")
        with open(path, encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
    elif path == DEFAULT_CONFIG_PATH and HAS_YAML:
        # Create an example config on first run.
        write_default_config(path)

    s = Settings()
    if "network" in data:
        s.network = data.get("network")
    s.include_self = bool(data.get("include_self", s.include_self))
    s.max_hosts = int(data.get("max_hosts", s.max_hosts))
    s.single_pass = bool(data.get("single_pass", s.single_pass))
    s.color = bool(data.get("color", s.color))

    s.discovery = _fill(DiscoverySettings(), data.get("discovery"))
    s.ports = _fill(PortSettings(), data.get("ports"))
    s.ports.list = _list_to_text(s.ports.list)
    s.nmap = _fill(NmapSettings(), data.get("nmap"))
    s.output = _fill(OutputSettings(), data.get("output"))
    return s


def output_abs_path(s: Settings) -> str:
    """Absolute path of the output directory."""
    folder = s.output.directory
    return folder if os.path.isabs(folder) else os.path.join(ROOT_DIR, folder)


# ---------------------------------------------------------------------------
# Default config.yaml text
# ---------------------------------------------------------------------------
DEFAULT_CONFIG_TEXT = """\
# =====================================================================
#  netsweep configuration
#  Changes take effect on the next run.
#  CLI options override the values in this file.
# =====================================================================

# Network to scan. null => auto-detect from the connected interface.
# Example: "10.31.85.0/24"
network: null

# Include your own IP in the scan.
include_self: false

# Safety limit: automatic scanning stops for networks larger than this.
max_hosts: 4096

# true => do a single pass and exit (instead of a continuous loop).
single_pass: false

# Colored output.
color: true

# ----- Discovery (finding live IPs) -----
discovery:
  interval: 5.0            # seconds between discovery passes (re-check every few seconds)
  offline_threshold: 2     # consecutive missed rounds before a host is "offline"
  ping_timeout: 1.0        # single ping wait time (seconds)
  concurrency: 128         # concurrent ping workers
  tcp_probe: true          # probe hosts that don't answer ping over TCP
  probe_ports: [22, 80, 135, 139, 443, 445, 3389, 5900, 8080]

# ----- Port scan (pure-Python engine) -----
ports:
  list: "20,21,22,23,25,53,69,80,88,110,111,123,135,137,138,139,143,161,389,443,445,465,514,515,548,587,631,636,873,902,993,995,1080,1194,1433,1521,1723,1883,2049,2082,2083,2181,2375,2376,3000,3128,3260,3306,3389,3478,5000,5060,5432,5672,5900,5985,5986,6000,6379,6443,7000,8000,8008,8080,8081,8088,8090,8123,8443,8888,9000,9090,9100,9200,9300,10000,11211,27017"
  timeout: 0.7             # port connect timeout (seconds)
  concurrency: 200         # concurrent port workers
  banner: true             # grab banner/header from open ports
  rescan_interval: 0.0     # re-scan hosts every N seconds (0 = once)

# ----- nmap engine (if installed; more accurate) -----
nmap:
  enabled: true            # false => pure-Python engine
  discovery: true          # find live hosts with nmap
  version_detection: true  # -sV service/version detection
  concurrency: 16          # how many nmap processes at once
  timeout: 300             # nmap timeout per host (seconds)
  extra_options: []        # e.g. ["--script", "http-title"]

# ----- Output -----
output:
  directory: output
  json: true
  csv: true
"""


def write_default_config(path: Optional[str] = None) -> str:
    """Write the example config.yaml to disk and return its path."""
    path = path or DEFAULT_CONFIG_PATH
    with open(path, "w", encoding="utf-8") as file:
        file.write(DEFAULT_CONFIG_TEXT)
    return path
