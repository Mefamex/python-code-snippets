# netsweep

Finds the **live IPs on the local network you're connected to** and scans the
**ports of the machines it finds in parallel**. It runs continuously; stop it
with `Ctrl+C`.

Built modularly: each job lives in its own file. No external Python package is
**required** (standard library only). If `nmap` is installed, it can be used
too.

This snippet is part of the
[python-code-snippets](https://github.com/Mefamex/python-code-snippets)
collection.

---

## Download

The snippet lives inside the `python-code-snippets` repository. You do **not**
need to download the whole repository: Git **sparse checkout** + **partial
clone** pulls only the `netsweep/` folder.

### Option A — Clone only this folder (recommended, keeps Git history)

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/Mefamex/python-code-snippets.git
cd python-code-snippets
git sparse-checkout set netsweep
```

What the parameters do:

| Parameter | Purpose |
| --- | --- |
| `--depth 1` | Shallow clone: fetch only the latest commit, not the whole history. |
| `--filter=blob:none` | Blobless clone: download only the folder tree; file contents are fetched only when you ask for this folder. |
| `--sparse` | Start in sparse-checkout mode (no subfolders are extracted at first). |
| `git sparse-checkout set netsweep` | Fetch and reveal the contents of the `netsweep` folder. |

With the default **Cone Mode** (Git 2.37+), the top-level files of the
repository (root `README.md`, `.gitignore`, ...) are also downloaded; other
subfolders are not.

Later, inside the repository:

```bash
git sparse-checkout add some_other_folder   # add another snippet next to netsweep
git sparse-checkout list                    # show which folders are checked out
git sparse-checkout disable                 # turn the filter off and get everything
```

### Option B — Download the folder without Git

If you only want to run the tool (no commits/pulls), extract just this folder:

```bash
curl -sL https://github.com/Mefamex/python-code-snippets/archive/refs/heads/main.tar.gz | tar -xz --strip-components=2 python-code-snippets-main/netsweep
```

### Handy alias

Add a reusable `git clone-sparse` command to `~/.gitconfig`:

```bash
git config --global alias.clone-sparse '!f() { repo="$1"; shift; git clone --depth 1 --filter=blob:none --sparse "$repo" && cd "$(basename "$repo" .git)" && git sparse-checkout set "$@"; }; f'
```

```bash
git clone-sparse https://github.com/Mefamex/python-code-snippets.git netsweep
```

---

## Setup / running

After downloading, run it from the `netsweep` folder (e.g.
`python-code-snippets/netsweep`):

**Linux/macOS:**

```bash
cd python-code-snippets/netsweep
./run.sh                      # default: continuous scan using config.yaml
# or
python3 main.py
```

**Windows (native):**

```bat
cd python-code-snippets\netsweep
run.bat                       REM default: continuous scan using config.yaml
REM or
python main.py
```

Press **Ctrl+C** to stop.

### Requirements

- Python 3.11+ (this machine has 3.14). On Windows, check **"Add python.exe to
  PATH"** during install.
- `nmap` (optional but recommended):
  - Linux (Arch): `sudo pacman -S nmap`
  - Windows: `winget install Insecure.Nmap` (or the official installer)
- `PyYAML` (for config.yaml):
  - Linux (Arch): `sudo pacman -S python-yaml`
  - Windows: `pip install pyyaml`

### Windows notes

- **Native:** Python 3 + (optional) nmap for Windows is enough; WSL is not
  required.
- **Network info:** your own IP via pure Python (UDP socket);
  interface/prefix/gateway via PowerShell (`Get-NetIPConfiguration`). If
  PowerShell is missing, `/24` is assumed (with a warning). This avoids parsing
  the localized `ipconfig` output on non-English Windows.
- **Privileges:** a SYN scan (`-sS`) needs **Administrator + Npcap**; otherwise
  the tool automatically falls back to `-sT` (no privilege required).
- **Color:** ANSI is enabled automatically on the Windows 10+ console; if that
  fails, it falls back to plain output. `run.bat` sets the UTF-8 code page
  (`chcp 65001`).

---

## Settings: `config.yaml`

All settings live in this file. Changes take effect on the next run. Options
given on the command line **override** only the relevant value.

```yaml
network: null               # null => auto-detect; or "10.31.85.0/24"
include_self: false         # also scan your own IP
max_hosts: 4096             # safety limit (prevents accidental /8 scans)
single_pass: false          # true => single pass and exit
color: true

discovery:                  # finding live hosts
  interval: 5.0             # seconds between passes (re-check every few seconds)
  offline_threshold: 2      # consecutive missed rounds before "offline"
  ping_timeout: 1.0
  concurrency: 128
  tcp_probe: true           # probe hosts that don't answer ping over TCP
  probe_ports: [22, 80, 135, 139, 443, 445, 3389, 5900, 8080]

ports:                      # pure-Python port scanner
  list: "80,443,1-1024"     # or list: [80, 443]
  timeout: 0.7
  concurrency: 200
  banner: true
  rescan_interval: 0.0      # 0 => each host is scanned once

nmap:                       # if installed; more accurate
  enabled: true
  discovery: true           # find live hosts with nmap
  version_detection: true   # -sV
  concurrency: 16
  timeout: 300
  extra_options: []

output:
  directory: output
  json: true
  csv: true
```

To regenerate the example config: `python3 main.py --create-config`

---

## Common commands

```bash
python3 main.py --quick --once             # quick (~20 ports), single pass
python3 main.py --network 10.31.85.0/24    # specify the network manually
python3 main.py -p 1-65535 --once          # all ports
python3 main.py --no-nmap                  # disable nmap, pure Python
python3 main.py --no-nmap-version          # disable version detection (faster)
python3 main.py --no-color --output /tmp/net   # no color + different output folder
```

All options: `python3 main.py --help`

> **Note:** running nmap with `sudo` enables a SYN scan (`-sS`) and ARP-based
> discovery; results get faster and more accurate. It also works without root
> (TCP connect scan).

---

## Modules (what each file does)

| File | Responsibility |
|------|----------------|
| `main.py` | Entry point; merges `config.yaml` + CLI options. |
| `config.yaml` | All settings (network, ports, timeouts, nmap, output). |
| `config.py` | YAML loading, defaults, the `Settings` object. |
| `platform_info.py` | Platform layer: ping, ARP table, interface/gateway/MAC, privileges, ANSI (Linux + Windows). |
| `network_info.py` | Interface/network/broadcast address, gateway, own IP/MAC, target list. |
| `scanner.py` | Orchestration: discovery loop + port scanning (nmap or pure Python). |
| `host_discovery.py` | Pure-Python live host discovery: ping + ARP table + TCP probing. |
| `port_scan.py` | Pure-Python port scanner: `connect_ex` + banner grabbing. |
| `nmap_engine.py` | nmap wrapper: parses the XML (`-oX -`) output. |
| `services.py` | Port->service name table, OS guess from TTL, TLS/HTTP port sets. |
| `mac_vendor.py` | MAC (OUI) -> vendor guess. |
| `models.py` | `HostInfo` and `PortInfo` data models. |
| `report.py` | Console output, coloring, JSON/CSV saving. |
| `helpers.py` | ANSI colors, IP math, port list parsing, print lock. |

---

## How it works

1. **Discovery (continuous):** every 5 seconds (by default) all IPs in the
   target range are probed **in parallel**. Ping is sent, the ARP table is
   read, and non-responders are tried over TCP (if nmap is enabled,
   `nmap -sn`).
2. **Expanding scope:** for every new host, a port scan **starts immediately
   and in parallel**. The list grows over time.
   - pure Python: one thread per port (`ThreadPoolExecutor`),
   - nmap: one nmap process per host (`-sT`/`-sS`, optional `-sV`).
3. **Refreshing the list:** the current list is refreshed every round.
   - New IP -> added and scanned.
   - Seen host -> `last_seen`/RTT updated.
   - A host not seen for `offline_threshold` consecutive rounds is marked
     **offline** (stays in the list, not deleted). If it reappears it is set
     **online** and its ports are re-scanned.
4. **Reporting:** open ports and online/offline transitions are printed;
   results are saved under `output/` as timestamped `.json` and `.csv`
   (including an `online` field per host).

## Privilege note

- Root/administrator is **not required**. Without root some ICMP/ARP probing is
  restricted, so TCP probing kicks in for hosts that don't answer ping.
- Run with root (`sudo`) / on Windows with **Administrator + Npcap** and nmap
  uses a SYN scan and ARP discovery.

## Legal notice

Use this tool only on networks you **own or have explicit permission** to scan.
Unauthorized scanning is a crime in most countries.
