# netsweep – Ağ Keşfi ve Paralel Port Tarayıcı

Bağlı olduğunuz yerel ağdaki **canlı IP'leri bulur** ve bulduğu makinelerin
**portlarını paralel olarak tarar**. Sürekli çalışır; `Ctrl+C` ile durdurulur.

Modüler yazıldı: her iş kendi dosyasında. Ek Python paketi **gerekmez** (sadece
standart kütüphane). `nmap` kuruluysa onu da kullanabilir.

> *last_modify: 2026-10-14*

<br>


## Özellikler
- **Sürekli keşif:** ağdaki canlı IP'leri belirli aralıkla tekrar tarar, listeyi günceller
- **Paralel port tarama:** saf Python motoru veya nmap motoru
- **Dinamik liste:** çevrimdışı düşen host listeden silinmez, geri geldiğinde yeniden taranır
- **Platform:** Linux ve Windows (native, WSL gerekmez)
- **Çıktı:** sonuçları zaman damgalı JSON/CSV olarak kaydeder
- **Harici bağımlılık yok:** isteğe bağlı `nmap` + `PyYAML`


<br>


## Gereksinimler
| Bileşen    | Gereksinim                  |
| ---------- | --------------------------- |
| Python     | 3.11+ (bu makinede 3.14)    |
| OS         | Windows / Linux / macOS     |
| Bağımlılık | Yok (isteğe bağlı: `nmap`)  |

- `nmap` (opsiyonel, önerilir): Linux `sudo pacman -S nmap`, Windows `winget install Insecure.Nmap`
- `PyYAML` (`config.yaml` için): Linux `sudo pacman -S python-yaml`, Windows `pip install pyyaml`


<br>


## Kurulum

Bu snippet, [`python-code-snippets`](https://github.com/Mefamex/python-code-snippets)
reposunun içindedir. Tüm repoyu indirmeden **sadece bu klasörü** çekebilirsiniz:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/Mefamex/python-code-snippets.git
cd python-code-snippets
git sparse-checkout set netsweep
```

> Klasörü GitHub'dan indirip `python-code-snippets/netsweep` içine koymanız da
> yeterlidir.
>
> Yöntemlerin ayrıntısı (arşivle indirme, `sparse-checkout add/list/disable`,
> `clone-sparse` alias) için:
> [Git ile Sadece Belirli Alt Klasörleri Klonlama](https://www.mefamex.com/blog/git-sparse-checkout-klonlama/)


<br>


## Çalıştırma

İndirdikten sonra `netsweep` klasöründen çalıştırın:

**Linux / macOS:**
```bash
cd python-code-snippets/netsweep
./run.sh          # varsayılan: config.yaml ile sürekli tarama
# veya
python3 main.py
```

**Windows:**
```bat
cd python-code-snippets\netsweep
run.bat           REM varsayılan: config.yaml ile sürekli tarama
REM veya
python main.py
```

Durdurmak için **Ctrl+C**.

### Windows notları
- **Native:** Python 3 + (opsiyonel) nmap yeterli; WSL gerekmez.
- **Ağ bilgisi:** kendi IP saf Python ile (UDP), arayüz/prefix/gateway PowerShell
  (`Get-NetIPConfiguration`) ile alınır. PowerShell yoksa `/24` varsayılır
  (uyarı verir) — böylece yerelleştirilmiş `ipconfig` çıktısı ayrıştırılmaz.
- **Yetki:** SYN taraması (`-sS`) için **Yönetici + Npcap** gerekir; yoksa
  otomatik olarak `-sT`'ye (yetkisiz) düşer.
- **Renk:** Windows 10+ konsolunda ANSI otomatik açılır; olmazsa düz çıktı.
  `run.bat` UTF-8 kod sayfasını (`chcp 65001`) ayarlar.


<br>


## Ayarlar (`config.yaml`)

Tüm ayarlar bu dosyadadır; değişiklikler bir sonraki çalıştırmada etkili olur.
Komut satırı bayrakları yalnızca verilen değeri geçersiz kılar.

```yaml
network: null               # null => otomatik algıla; veya "10.31.85.0/24"
include_self: false         # kendi IP'nizi de tarayın
max_hosts: 4096             # güvenlik sınırı (yanlışlıkla /8 taramasını önler)
single_pass: false          # true => tek geçiş yap ve çık
color: true

discovery:                  # canlı host keşfi
  interval: 5.0             # turlar arası saniye (birkaç saniyede bir yeniden kontrol)
  offline_threshold: 2      # "çevrimdışı" demeden önce art arda kaçırma sayısı
  ping_timeout: 1.0
  concurrency: 128
  tcp_probe: true           # ping'e cevap vermeyenleri TCP ile yokla
  probe_ports: [22, 80, 135, 139, 443, 445, 3389, 5900, 8080]

ports:                      # saf Python port tarayıcı
  list: "80,443,1-1024"     # veya list: [80, 443]
  timeout: 0.7
  concurrency: 200
  banner: true
  rescan_interval: 0.0      # 0 => her host bir kez taranır

nmap:                       # kuruluysa; daha doğru
  enabled: true
  discovery: true           # canlı host'ları nmap ile bul
  version_detection: true   # -sV
  concurrency: 16
  timeout: 300
  extra_options: []

output:
  directory: output
  json: true
  csv: true
```

Örnek config'i yeniden üretmek için: `python3 main.py --create-config`

### Örnek komutlar
```bash
python3 main.py --quick --once             # hızlı (~20 port), tek geçiş
python3 main.py --network 10.31.85.0/24    # ağı elle belirt
python3 main.py -p 1-65535 --once          # tüm portlar
python3 main.py --no-nmap                  # nmap kapalı, saf Python
python3 main.py --no-color --output /tmp/net
```

Tüm bayraklar: `python3 main.py --help`

> **Not:** nmap'i `sudo` ile çalıştırmak SYN taraması (`-sS`) ve ARP tabanlı
> keşfi açar; sonuçlar daha hızlı ve doğru olur. Root olmadan da çalışır
> (TCP connect taraması).


<br>


## Modüller
| Dosya | Görevi |
| ----- | ------ |
| `main.py` | Giriş noktası; `config.yaml` + komut satırı seçeneklerini birleştirir. |
| `config.yaml` | Tüm ayarlar (ağ, portlar, zaman aşımları, nmap, çıktı). |
| `config.py` | YAML yükleme, varsayılanlar, `Settings` nesnesi. |
| `platform_info.py` | Platform katmanı: ping, ARP tablosu, arayüz/gateway/MAC, yetki, ANSI (Linux + Windows). |
| `network_info.py` | Arayüz/ağ/broadcast adresi, gateway, kendi IP/MAC, hedef liste. |
| `scanner.py` | Orkestrasyon: keşif döngüsü + port tarama (nmap veya saf Python). |
| `host_discovery.py` | Saf Python canlı host keşfi: ping + ARP tablosu + TCP yoklama. |
| `port_scan.py` | Saf Python port tarayıcı: `connect_ex` + banner toplama. |
| `nmap_engine.py` | nmap sarmalayıcı: `-oX -` XML çıktısını ayrıştırır. |
| `services.py` | Port→servis adı tablosu, TTL'den OS tahmini, TLS/HTTP port kümeleri. |
| `mac_vendor.py` | MAC (OUI) → üretici tahmini. |
| `models.py` | `HostInfo` ve `PortInfo` veri modelleri. |
| `report.py` | Konsol çıktısı, renklendirme, JSON/CSV kaydetme. |
| `helpers.py` | ANSI renkleri, IP matematiği, port listesi ayrıştırma, yazdırma kilidi. |


<br>


## Nasıl çalışır
1. **Keşif (sürekli):** varsayılan olarak her 5 saniyede bir, hedef aralıktaki
   tüm IP'ler **paralel** yoklanır. Ping atılır, ARP tablosu okunur ve cevap
   vermeyenler TCP ile denenir (nmap açıksa `nmap -sn`).
2. **Genişleyen kapsam:** bulunan her yeni host için port taraması **anında ve
   paralel** başlar. Liste zamanla büyür.
   - saf Python: port başına bir thread (`ThreadPoolExecutor`),
   - nmap: host başına bir nmap süreci (`-sT`/`-sS`, opsiyonel `-sV`).
3. **Listeyi tazeleme:** mevcut liste her turda güncellenir.
   - Yeni IP → listeye eklenir ve taranır.
   - Görülen host → `last_seen`/RTT güncellenir.
   - `offline_threshold` tur boyunca görülmeyen host **çevrimdışı** işaretlenir
     (listede kalır, silinmez). Geri gelirse **çevrimiçi** yapılır ve portları
     yeniden taranır.
4. **Raporlama:** açık portlar ile çevrimiçi/çevrimdışı geçişleri ekrana
   yazılır; sonuçlar `output/` altına zaman damgalı `.json` ve `.csv` olarak
   kaydedilir (host başına `online` alanı dahil).


<br>


## Yetki notu
- Root/yönetici **gerekmez**. Root olmadan bazı ICMP/ARP yoklamaları kısıtlıdır;
  bu yüzden ping'e cevap vermeyen host'lar için TCP yoklama devreye girer.
- Root (`sudo`) / Windows'ta **Yönetici + Npcap** ile çalıştırıldığında nmap
  SYN taraması ve ARP keşfi kullanır.


<br>


## Yasal uyarı
Bu aracı yalnızca **sahibi olduğunuz veya tarama izni verilmiş** ağlarda
kullanın. İzinsiz tarama çoğu ülkede suçtur.
