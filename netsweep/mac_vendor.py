"""Vendor guess from the first 3 bytes (OUI) of a MAC address.

A small, offline, hand-maintained table; the goal is not an exact inventory
but a "what could this device be?" hint. Prefixes not in the table are marked
as 'Unknown vendor'.
"""

from __future__ import annotations

from typing import Optional

# Key: first 6 uppercase hex characters of the MAC (OUI).
VENDOR_TABLE = {
    # Virtualization / hypervisor
    "000C29": "VMware",
    "005056": "VMware",
    "080027": "VirtualBox",
    "525400": "QEMU/KVM",
    "00155D": "Microsoft Hyper-V",
    "001C42": "Parallels",
    # Microsoft
    "000D3A": "Microsoft",
    "001DD8": "Microsoft",
    "0050F2": "Microsoft",
    # Single-board computers
    "B827EB": "Raspberry Pi Foundation",
    "DCA632": "Raspberry Pi Trading",
    "E45F01": "Raspberry Pi Trading",
    # Embedded / IoT
    "7CDFA1": "Espressif (ESP)",
    "240AC4": "Espressif (ESP)",
    "18FE34": "Espressif (ESP)",
    # Network vendors
    "001E58": "D-Link",
    "00248C": "ASUSTek",
    "001B0C": "Cisco",
    "00E04C": "Realtek",
    "0018F8": "Zyxel",
    # Mobile / consumer
    "001A11": "Google",
    "3C5A37": "Samsung",
    "F0189E": "Apple",
    "88E9FE": "Apple",
    "44650D": "Amazon Technologies",
    "F0B429": "Xiaomi",
}


def find_vendor(mac: Optional[str]) -> Optional[str]:
    """Guess the vendor from a MAC; 'Unknown vendor' if not found."""
    if not mac:
        return None
    clean = mac.replace(":", "").replace("-", "").upper()
    if len(clean) < 6:
        return None
    return VENDOR_TABLE.get(clean[:6], "Unknown vendor")
