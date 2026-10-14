#!/usr/bin/env python3
"""LAN discovery + parallel port scanning - entry point (CLI).

Settings are read from `config.yaml`; options given on the command line
override only the relevant values.
"""

from __future__ import annotations

import argparse
import os
import signal
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import platform_info
from config import (
    DEFAULT_CONFIG_PATH,
    QUICK_PORTS,
    Settings,
    load_settings,
    write_default_config,
)
from report import Report
from scanner import Scanner


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Find live IPs on your network and scan their ports in parallel.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "-c", "--config", default=DEFAULT_CONFIG_PATH, help="Settings file (YAML)."
    )
    p.add_argument(
        "--create-config",
        action="store_true",
        help="Write the example config.yaml and exit.",
    )

    p.add_argument(
        "-a", "--network", default=None, help="Network to scan (e.g. 192.168.1.0/24)."
    )
    p.add_argument("-p", "--ports", default=None, help="Port list: '80,443,1-1024'.")
    p.add_argument(
        "--quick", action="store_true", help="Scan only the ~20 common ports."
    )
    p.add_argument(
        "-i",
        "--interval",
        type=float,
        default=None,
        help="Seconds between discovery passes.",
    )
    p.add_argument("--once", action="store_true", help="Do a single pass and exit.")
    p.add_argument(
        "--concurrency",
        type=int,
        default=None,
        help="Concurrent port workers (pure Python).",
    )
    p.add_argument(
        "--discovery-concurrency",
        type=int,
        default=None,
        help="Concurrent ping workers.",
    )
    p.add_argument(
        "--timeout", type=float, default=None, help="Port connect timeout (seconds)."
    )

    p.add_argument(
        "--banner",
        dest="banner",
        action="store_true",
        default=None,
        help="Collect banners.",
    )
    p.add_argument(
        "--no-banner",
        dest="banner",
        action="store_false",
        help="Disable banner collection.",
    )
    p.add_argument(
        "--no-tcp-probe",
        dest="tcp_probe",
        action="store_false",
        default=None,
        help="Disable TCP probing for hosts that don't answer ping.",
    )

    p.add_argument(
        "--nmap",
        dest="nmap",
        action="store_true",
        default=None,
        help="Enable the nmap engine.",
    )
    p.add_argument(
        "--no-nmap", dest="nmap", action="store_false", help="Disable the nmap engine."
    )
    p.add_argument(
        "--nmap-discovery",
        dest="nmap_discovery",
        action="store_true",
        default=None,
        help="Use nmap for discovery.",
    )
    p.add_argument(
        "--no-nmap-discovery",
        dest="nmap_discovery",
        action="store_false",
        help="Don't use nmap for discovery (pure Python).",
    )
    p.add_argument(
        "--nmap-version",
        dest="nmap_version",
        action="store_true",
        default=None,
        help="Enable nmap -sV (service/version detection).",
    )
    p.add_argument(
        "--no-nmap-version",
        dest="nmap_version",
        action="store_false",
        help="Disable nmap -sV.",
    )
    p.add_argument(
        "--nmap-concurrency",
        type=int,
        default=None,
        help="How many nmap processes at once.",
    )

    p.add_argument(
        "--rescan",
        type=float,
        default=None,
        help="Re-scan hosts every N seconds (0 = once).",
    )
    p.add_argument("--include-self", action="store_true", help="Also scan your own IP.")
    p.add_argument("--output", default=None, help="Output folder.")
    p.add_argument(
        "--no-json",
        dest="json_save",
        action="store_false",
        default=None,
        help="Don't save JSON.",
    )
    p.add_argument(
        "--no-csv",
        dest="csv_save",
        action="store_false",
        default=None,
        help="Don't save CSV.",
    )
    p.add_argument(
        "--no-color",
        dest="color",
        action="store_false",
        default=None,
        help="Disable colors.",
    )
    return p.parse_args()


def _apply_cli(settings: Settings, a: argparse.Namespace) -> None:
    """Write only the explicitly given CLI options into settings."""
    if a.network is not None:
        settings.network = a.network
    if a.ports is not None:
        settings.ports.list = a.ports
    if a.quick:
        settings.ports.list = ",".join(str(p) for p in QUICK_PORTS)
    if a.interval is not None:
        settings.discovery.interval = a.interval
    if a.once:
        settings.single_pass = True
    if a.concurrency is not None:
        settings.ports.concurrency = a.concurrency
    if a.discovery_concurrency is not None:
        settings.discovery.concurrency = a.discovery_concurrency
    if a.timeout is not None:
        settings.ports.timeout = a.timeout
    if a.banner is not None:
        settings.ports.banner = a.banner
    if a.tcp_probe is not None:
        settings.discovery.tcp_probe = a.tcp_probe
    if a.nmap is not None:
        settings.nmap.enabled = a.nmap
    if a.nmap_discovery is not None:
        settings.nmap.discovery = a.nmap_discovery
    if a.nmap_version is not None:
        settings.nmap.version_detection = a.nmap_version
    if a.nmap_concurrency is not None:
        settings.nmap.concurrency = a.nmap_concurrency
    if a.rescan is not None:
        settings.ports.rescan_interval = a.rescan
    if a.include_self:
        settings.include_self = True
    if a.output is not None:
        settings.output.directory = a.output
    if a.json_save is not None:
        settings.output.json = a.json_save
    if a.csv_save is not None:
        settings.output.csv = a.csv_save
    if a.color is not None:
        settings.color = a.color


def main() -> int:
    color_ok = platform_info.startup_prepare()  # UTF-8 output + (on Windows) ANSI
    args = parse_args()

    if args.create_config:
        path = write_default_config(DEFAULT_CONFIG_PATH)
        print(f"Example config written: {path}")
        return 0

    try:
        settings = load_settings(args.config)
    except Exception as error:
        print(f"[!] Could not load settings: {error}")
        return 1

    _apply_cli(settings, args)

    # If colors aren't supported (e.g. an old Windows console), fall back to plain output.
    if settings.color and not color_ok:
        settings.color = False
        print("[*] This terminal does not support colors; using plain output.")

    report = Report(settings)
    scanner = Scanner(settings, report)

    def _stop(_signum, _frame):
        report.info("Stopping... (in-flight scans will complete)")
        scanner.stop()

    signal.signal(signal.SIGINT, _stop)
    try:
        signal.signal(signal.SIGTERM, _stop)  # not delivered on Windows; harmless
    except (ValueError, OSError, AttributeError):
        pass

    try:
        scanner.run()
    except KeyboardInterrupt:
        scanner.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
