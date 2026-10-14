"""Local network info: interface, network/broadcast address, gateway, own
IP/MAC and the list of target IPs to scan.

Platform-dependent parts (interface/prefix/gateway/MAC lookup) are delegated to
the `platform_info` layer, so this module works the same on Linux and Windows.
If no network is given, it auto-detects from the default-route interface.
No extra dependency or root privilege is required.
"""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from typing import List, Optional

import platform_info
from config import Settings


@dataclass
class NetworkInfo:
    """Network definition of a scan target."""

    interface: str
    cidr: str
    network_address: str
    broadcast: str
    gateway: Optional[str]
    local_ip: str
    local_mac: Optional[str]
    target_ips: List[str] = field(default_factory=list)


def _target_list(
    net: ipaddress._BaseNetwork,
    local_ip: Optional[str],
    include_self: bool,
    max_hosts: int,
) -> List[str]:
    """Produce the IPs to scan in the network (excluding network/broadcast)."""
    if net.num_addresses > max_hosts:
        raise ValueError(
            f"Network too large: {net.num_addresses} addresses (limit {max_hosts}). "
            "Increase 'max_hosts' in config.yaml or give a narrower network."
        )
    if net.num_addresses <= 2:
        targets = [str(a) for a in net]
    else:
        targets = [str(a) for a in net.hosts()]
    if not include_self and local_ip:
        targets = [ip for ip in targets if ip != local_ip]
    return targets


def get_network_info(network_text: Optional[str], settings: Settings) -> NetworkInfo:
    """Resolve the network info. On error, raise a clear `ValueError`."""
    interface, local_ip, prefix = platform_info.interface_ip_prefix()

    if network_text:
        try:
            net = ipaddress.ip_network(network_text, strict=False)
        except ValueError as error:
            raise ValueError(f"Invalid network '{network_text}': {error}") from error
    else:
        if not local_ip or prefix is None:
            raise ValueError(
                "Network could not be auto-detected; specify it with --network "
                "(e.g. 192.168.1.0/24)."
            )
        net = ipaddress.ip_network(f"{local_ip}/{prefix}", strict=False)

    targets = _target_list(net, local_ip, settings.include_self, settings.max_hosts)

    return NetworkInfo(
        interface=interface or "?",
        cidr=str(net),
        network_address=str(net.network_address),
        broadcast=str(net.broadcast_address),
        gateway=platform_info.find_gateway(),
        local_ip=local_ip or "-",
        local_mac=platform_info.local_mac(interface),
        target_ips=targets,
    )
