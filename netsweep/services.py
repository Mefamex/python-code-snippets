"""Port -> service name mapping, OS guess from TTL and the port sets used
while grabbing banners.

This is not a complete Nmap database; it labels common ports in a
human-readable way.
"""

from __future__ import annotations

from typing import Optional

# Well-known service names for common ports.
SERVICE_NAMES = {
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    67: "dhcp",
    68: "dhcp",
    69: "tftp",
    80: "http",
    88: "kerberos",
    110: "pop3",
    111: "rpcbind",
    123: "ntp",
    135: "msrpc",
    137: "netbios-ns",
    138: "netbios-dgm",
    139: "netbios-ssn",
    143: "imap",
    161: "snmp",
    162: "snmptrap",
    389: "ldap",
    443: "https",
    445: "smb",
    464: "kpasswd",
    465: "smtps",
    514: "syslog",
    515: "lpd",
    548: "afp",
    587: "submission",
    623: "ipmi",
    631: "ipp",
    636: "ldaps",
    873: "rsync",
    902: "vmware",
    993: "imaps",
    995: "pop3s",
    1080: "socks",
    1194: "openvpn",
    1433: "mssql",
    1521: "oracle",
    1723: "pptp",
    1883: "mqtt",
    2049: "nfs",
    2082: "cpanel",
    2083: "cpanel-ssl",
    2181: "zookeeper",
    2375: "docker",
    2376: "docker-tls",
    3000: "grafana/node",
    3128: "squid",
    3260: "iscsi",
    3306: "mysql",
    3389: "rdp",
    3478: "stun",
    4000: "icq",
    4444: "metasploit",
    5000: "upnp/flask",
    5060: "sip",
    5432: "postgresql",
    5672: "amqp",
    5900: "vnc",
    5985: "winrm",
    5986: "winrm-ssl",
    6000: "x11",
    6379: "redis",
    6443: "k8s-api",
    7000: "cassandra",
    8000: "http-alt",
    8008: "http-alt",
    8080: "http-proxy",
    8081: "http-alt",
    8088: "http-alt",
    8090: "http-alt",
    8123: "home-assistant",
    8443: "https-alt",
    8888: "http-alt",
    9000: "http-alt",
    9090: "prometheus/cockpit",
    9100: "printer",
    9200: "elasticsearch",
    9300: "elasticsearch",
    10000: "webmin",
    11211: "memcached",
    27017: "mongodb",
}

# Ports where a TLS handshake is attempted for the banner.
TLS_PORTS = {443, 465, 636, 993, 995, 2083, 2376, 5986, 6443, 8443, 8883}

# Ports where an HTTP HEAD request is sent for the banner.
HTTP_PORTS = {
    80,
    81,
    591,
    2082,
    3000,
    3128,
    5000,
    8000,
    8008,
    8080,
    8081,
    8088,
    8090,
    8123,
    8888,
    9000,
    9090,
    10000,
}


def port_service_name(port: int) -> str:
    """Common service name for a port number ('?' if unknown)."""
    return SERVICE_NAMES.get(port, "?")


def ttl_to_os_guess(ttl: Optional[int]) -> Optional[str]:
    """Rough OS guess from an observed TTL value.

    Initial TTLs are usually: 64 (Linux/Unix), 128 (Windows), 255 (network
    device). The observed value decreases by 1 per hop; we map to the smallest
    standard value it fits.
    """
    if ttl is None:
        return None
    if ttl <= 64:
        return "Linux/Unix/macOS (guess)"
    if ttl <= 128:
        return "Windows (guess)"
    if ttl <= 255:
        return "Router/network device (guess)"
    return "Unknown"
