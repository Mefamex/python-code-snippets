# -*- coding: utf-8 -*- 

"""
===============================================================================
                            LOCALHOST SERVER
===============================================================================
Basit, bağımsız bir yerel HTTP statik dosya sunucusu.

AMAÇ
    Belirli bir portu veya verilen aralıktaki ilk uygun portu seçerek bulunduğunuz
    dizini (veya seçtiğiniz dizini) hızlıca yerel ağda yayınlamak.

ÖZELLİKLER
    * Port tarama: Belirli aralıkta ilk boş portu bulur (varsayılan 8000-8100).
    * Doğrudan port: -p / --port ile doğrudan port seçebilme.
    * Aralık desteği: -r 9000-9050 gibi özel aralık verebilme ya da tek port.
    * Yerel IP tespiti: LAN IP (fallback ile 127.0.0.1) gösterimi.
    * Basit kullanım: Python standart kütüphanesi dışında bağımlılık yok.
    * Netstat entegrasyonu (Windows): Seçilen aralıktaki dolu portları gösterme.

KISA KULLANIM
    python main.py                  # Varsayılan aralıkta port ara ve çalıştır
    python main.py -p 8080          # 8080 portunda direkt sunucu başlat
    python main.py -r 9000-9050     # 9000-9050 aralığında ilk boş portu bul
    python main.py -r 8080          # Sadece 8080 portunu dene (tek değer)

ARGÜMANLAR
    -p, --port     : Kullanılacak kesin port.
    -r, --range    : Port aralığı (örn: 8000-8100) veya tek port (örn: 8080).

GÜVENLİK UYARILARI
    * Bu araç kimlik doğrulama yapmaz. Aynı yerel ağdaki herkes dosyaları
        okuyabilir. Hassas dizinlerde çalıştırmayın.
    * İnternete port yönlendirmesi yapmayın (NAT / router port forward).
    * Yalnızca okunabilirlik sağlar; yazma (upload) yoktur.

LİSANS
    MIT

DEĞİŞİKLİKLER
    1.0.0 (2025-08-13): İlk sürüm - port tarama + basit sunucu.

YAZAR
    Mefamex (info@mefamex.com)  https://mefamex.com

===============================================================================
"""

__version__ = "1.0.0"
__author__ = "mefamex"
__email__ = "info@mefamex.com"
__license__ = "MIT"
__status__ = "DEVELOPMENT"

__project_name__ = "LocalHost Server"
__url__ = "https://mefamex.com"
__url_github__ = "https://github.com/Mefamex/python-code-snippets"
__copyright__ = "2025 Mefamex"
__description__ = "Basit port taramalı yerel HTTP statik dosya sunucusu"
__date__ = "2025-08-13"
__date_modify__ = "2025-08-13"
__python_version__ = ">=3.6"
__dependencies__ = {
    "external": [],  # pip ile kurulması gereken yok
    "standard_lib": ["os", "socket", "http.server", "socketserver", "argparse", "time"],
}

#================================================================================


import os, sys, platform, socket, http.server, socketserver, argparse
from time import sleep


#================================================================================


DEF_PORT_START: int = 8000
DEF_PORT_END: int = 8100


def get_local_ip() -> str:
    """Yerel LAN IPv4 adresini döndür; hata durumunda 127.0.0.1.

    Birkaç fallback ile getaddrinfo (errno 11001) hatasını tolere eder.
    """
    for target in ("1.1.1.1", "8.8.8.8"):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect((target, 80))
                return s.getsockname()[0]
        except Exception: pass
    try: # gethostbyname_ex daha çok adres döndürebilir
        _host, _alias, addrs = socket.gethostbyname_ex(socket.gethostname())
        for ip in addrs:
            print(f"IP: {ip}")
            if ip and not ip.startswith("127."): return ip
    except Exception:  pass
    return "127.0.0.1"


def is_port_in_use(port: int) -> bool:
    """Port kullanımda mı? Bağlanmak yerine bind ile test.

    bind başarısız olursa port doludur. 0.0.0.0 kullanarak tüm arayüzleri kapsar.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try: s.bind(("0.0.0.0", port))
        except OSError: return True
    return False



# netstat -ano | findstr :8000
def check_port_usage(port: int) -> None:
    """Belirtilen portun kullanım durumunu kontrol eder."""
    # # netstat -ano | findstr :8000
    os.system(f"netstat -ano | findstr :{port}") 


def find_available_port(start_port, end_port) -> int:
    """Belirtilen aralıkta uygun bir port bulur."""
    print(f"Checking ports : {start_port} - {end_port}\n")
    first_safe_port : int = 0
    # check ports -> DEF_PORT_START to DEF_PORT_END
    used_ports = []
    for port in range(0, 65535):
        try:
            if is_port_in_use(port): used_ports.append(port)
            elif DEF_PORT_START <= port and first_safe_port == 0 : first_safe_port = port
        except Exception as e: print(f"Error checking port {port}: {e}")
    if used_ports: 
        pids={}
        for q in used_ports: 
            if DEF_PORT_START <= q <= DEF_PORT_END:check_port_usage(q)
        print(f"\n--------\nThe following ports are in use and were skipped: \n{' '.join([str(q).rjust(5)+f"{"\n" if used_ports.index(q)%12==11 else "" }" for q in used_ports])}")
    sleep(0.5)
    print("---------")
    # print if any port is used
    if first_safe_port == 0:  print("No ports were skipped, all are available.")
    return first_safe_port



def run_server(port: int) -> None:
    """HTTP sunucusunu belirtilen portta başlat."""
    handler = http.server.SimpleHTTPRequestHandler
    try: httpd = socketserver.TCPServer(("", port), handler)  # Tüm arayüzler
    except OSError as e:
        print(f"Sunucu başlatılamadı (port {port}): {e}")
        return
    local_ip = get_local_ip()
    print(f"\nÇalışma dizini  : {os.getcwd()}")
    sleep(0.5)
    print("Erişim adresleri:\n")
    sleep(0.5)
    print(f"     http://localhost:{port}", end="")
    sleep(0.5)
    if local_ip not in ("127.0.0.1", ""): print(f"  |  http://{local_ip}:{port}")
    sleep(0.5)
    print("\n(Ctrl+C ile durdur)\n-------------------\n")
    sleep(0.5)
    httpd.serve_forever()


def main(port: int | None = None, start: int | None = None, end: int | None = None):
    # Kullanıcı parametre verdiyse onları kullan; aksi halde varsayılan
    start = start if start is not None else DEF_PORT_START
    end   = end   if end   is not None else DEF_PORT_END
    try: 
        if port is not None and port != 0:  # Belirli port istenmiş
            print(f"\n============================== Starting HTTP Server ==============================\nİstenen port: {port}")
            run_server(port)
            return
    except Exception as e: print(f"\nSunucu başlatılamadı (port {port}): {e}\n")
    try:
        print(f"\n============================== Scanning Ports ==============================\nAralık: {start}-{end}")
        sleep(1)
        found = find_available_port(start, end)
        sleep(1)
        if found == 0:  print(f"\nUygun port bulunamadı (aranan: {start}-{end}).")
        main(port=found, start=start, end=end)
    except Exception as e: print( f"\nPort tarama hatası: {e}\n" )


def _parse_args():
    EXAMPLES = """
ÖRNEKLER:
    python main.py               -> 8000 - 8000 arasında 
    python main.py -p 8080       -> Doğrudan 8080 portunda çalıştır.
    python main.py -r 8080       -> Sadece 8080 portunu dene (doluysa hata verir).
    python main.py -r 9000-9050  -> 9000-9050 aralığında ilk boş portu seç.
    """
    p = argparse.ArgumentParser( description="Basit yerel HTTP statik dosya sunucusu (port tarama destekli).", epilog=EXAMPLES, formatter_class=argparse.RawTextHelpFormatter, add_help=False )
    p.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}", help="Sürüm bilgisini gösterir.")
    p.add_argument("-p", "--port", type=int, help="Doğrudan bu portu kullan (örn: 8080).")
    p.add_argument("-r", "--range", help="Port aralığı (örn: 8000-8100) veya tek port (örn: 8080). -p verilirse yok sayılır.")
    p.add_argument("-h", "-?", "--help", action="help", help="Yardım mesajını gösterir.")
    p.add_argument("--doc", action="store_true", help="Dokümantasyon mesajını gösterir.")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    rng_start = rng_end = None
    if args.range:
        try:
            if "-" in args.range:
                a, b = args.range.split("-", 1)
                rng_start, rng_end = int(a), int(b)
                if rng_start > rng_end: rng_start, rng_end = rng_end, rng_start
            else:
                # Tek port girişi
                single_port = int(args.range)
                rng_start = rng_end = single_port
        except Exception:
            print("Geçersiz aralık formatı. Örn: 8000-8100 veya 8080")
            raise SystemExit(1)
        
    for _line in str(__doc__ or "").splitlines():
        print(_line)
        sleep(0.02)
    try: 
        main( port=args.port, start=rng_start, end=rng_end )
    except KeyboardInterrupt:
        print("\nSunucu durduruluyor...")
        raise SystemExit(0)
    except Exception as e:
        print(f"\nHata: {e}")
        raise SystemExit(1)