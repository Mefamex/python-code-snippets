# LocalHost Server – Port Taramalı Yerel HTTP Sunucusu

Yerel (localhost / LAN) üzerinde seçilen dizini hızlıca HTTP üzerinden servis eden, bir port aralığını tarayıp ilk boş portu seçebilen, yalnızca Python standart kütüphanesi kullanan hafif araç.

> last_modify: 2025-08-13



<br><br>



## 🚀 Özellikler
* Port tarama (varsayılan aralık: 8000–8100)
* Doğrudan port seçimi (-p / --port)
* Tek port veya aralık (-r 9000-9050 ya da -r 8080)
* Yerel IP (LAN) tespiti (fallback 127.0.0.1)
* Windows netstat entegrasyonu ile dolu port listesi
* Harici bağımlılık yok (sadece standart lib)
* Basit, okunabilir kod – kolay genişletme



<br><br>



## � Gereksinimler
| Bileşen    | Gereksinim              |
| ---------- | ----------------------- |
| Python     | 3.8+                    |
| OS         | Windows / Linux / macOS |
| Bağımlılık | Yok                     |

Not: netstat parçası Windows odaklıdır; Linux/macOS için `ss` veya `lsof` adaptasyonu ekleyebilirsiniz.


<br><br>


## 🔧 Kurulum
Klonlayın veya dosyayı indirin, ardından:
```bash
python main.py
```

Opsiyonel EXE (PyInstaller):
```bash
pip install pyinstaller
pyinstaller --onefile --console main.py
```


<br><br>


## 🎯 Kullanım
```bash
# Varsayılan aralıkta port ara
python main.py

# Belirli port
python main.py -p 8080

# Özel aralık
python main.py -r 9000-9050

# Tek port dene (aralık gibi yazmadan)
python main.py -r 8081
```

Tarayıcı erişimi:
```
http://localhost:<port>
http://<LAN_IP>:<port>
```

<br><br>


## 🧭 Argümanlar
| Argüman      | Açıklama             | Örnek                  |
| ------------ | -------------------- | ---------------------- |
| -p / --port  | Kesin port           | -p 8005                |
| -r / --range | Aralık veya tek port | -r 8100-8200 / -r 8101 |

Öncelik: `--port` verilirse aralık yok sayılır.


<br><br>


## 🧪 Örnek Çıktı
```
============================== Scanning Ports ==============================
Aralık: 8000-8100
Checking ports : 8000 - 8100
...
Seçilen boş port: 8001
============================== Starting HTTP Server ==============================
İstenen port: 8001
Çalışma dizini  : D:\\localHost-server
Erişim adresleri:
  http://localhost:8001  |  http://192.168.1.34:8001
(Ctrl+C ile durdur)
```


<br><br>


## 🛡️ Güvenlik Notları
* Kimlik doğrulama yok; aynı ağdaki herkes dosyaları görebilir.
* Hassas dizinlerde çalıştırmayın (örn. bütün C:\ kökü).
* İnternete port yönlendirmesi (NAT) yapmayın.



<br><br>


## ⚙️ İç Yapı
| İşlev               | Amaç                                    |
| ------------------- | --------------------------------------- |
| find_available_port | Aralıkta bind denemesi ile ilk boş port |
| is_port_in_use      | bind başarısız ise port dolu varsayımı  |
| get_local_ip        | Routing tablosu + hostname fallback     |
| run_server          | socketserver.TCPServer ile servis       |


<br><br>


## ❗ Yaygın Sorunlar
| Belirti             | Neden                          | Çözüm                                       |
| ------------------- | ------------------------------ | ------------------------------------------- |
| getaddrinfo failed  | Hatalı host tuple              | Host boş string olsun: ("", port)           |
| Port dolu gözüküyor | Firewall / başka servis / izin | Farklı aralık, yönetici mod veya izin ayarı |
| LAN IP 127.0.0.1    | Yönlendirme yok                | Aynı makine için sorun değil                |


<br><br>


## 🔍 Genişletme Fikirleri
* IPv6 / ThreadingTCPServer
* Çoklu sürücü map (C, D) -> özel handler
* Basit Basic-Auth ekleme
* Renkli terminal (colorama) desteği




<br><br>




### Proje Bağlantıları
- [MEFAMEX | Python Code Snippets ](https://github.com/Mefamex/python-code-snippets)
- [Mefamex.com/projects](https://mefamex.com/projects/)


<br><br><hr>
