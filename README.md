# PYTHON CODE SNIPPETS

> |               |                                       |
> | ------------- | ------------------------------------- |
> | *author*      | [Mefamex](https://github.com/Mefamex) |
> | *created*     | 2025-08-10                            |
> | *last modify* | 2026-08-11 | Update: Readme |

<br><br>

Sistem yönetimi, otomasyon ve geliştirme süreçlerinde ihtiyaç duyduğum Python araçlarını ve betiklerini bir arada tutmak için oluşturduğum koleksiyon. <br>
Bu repository büyük bir framework değil, pratik çözümler sunan bağımsız araçların derlemesidir.

Her araç (script) kendi başına çalışır ve farklı sistem veya proje ihtiyaçlarına yanıt verir.

- **Bağımsız Araçlar:** Her betik tek başına çalışabilir, dışa bağımlılıkları minimumda tutulmuştur
- **Standart Kütüphaneler:** Mümkün olduğunca Python standart kütüphaneleri kullanılmış, harici bağımlılık gerektirenler kendi içinde belirtilmiştir
- **Pratik Çözümler:** İşletim sistemi otomasyonu, dosya/dizin yönetimi, veri işleme ve sunucu süreçlerini hızlandırır
- **Kolay Entegrasyon:** Doğrudan projenize, sunucunuza veya yerel ortamınıza kopyalayıp çalıştırabilirsiniz

<br><br>

<h2 align="center" id="İçindekiler">İÇİNDEKİLER</h2>

### [check_file_dependencies](check_file_dependencies/)
- Python modüllerinin bağımlılıklarını otomatik olarak kontrol eden, eksik olanları tespit edip yükleyen ve sürüm uyumluluğunu yöneten yardımcı sınıf.

### [convert_to_wav](convert_to_wav/)
- Belirtilen dizindeki tüm ses dosyalarını `ffmpeg` aracılığıyla toplu olarak standart (44100Hz, 16-bit, Mono) WAV formatına dönüştüren otomasyon aracı.

### [directory_explorer](directory_explorer/)
- Dizin yapılarını esnek bir şekilde görselleştiren, özyinelemeli tarama ile boyut hesaplamaları yapan ve sonuçları JSON ile TXT formatında dışa aktaran araç.

### [file_analyzer.py](file_analyzer.py)
- Bir dizin yolundaki dosya ve dizinleri detaylıca analiz eden, dosya boyutları, oluşturulma tarihleri ve hiyerarşi gibi bilgileri raporlayan kapsamlı dizin görselleştiricisi.

### [image-converter](image-converter/)
- Görselleri Instagram boyut ve kalite standartlarına uygun hale getirmek üzere optimize eden (dönüştürme, sıkıştırma) görsel işleme betiği.

### [image_metadata_modify](image_metadata_modify/)
- Fotoğraf ve görsellerin EXIF/metadata verilerini okumak, düzenlemek ve raporlamak için geliştirilmiş veri aracı.

### [localHost-server](localHost-server/)
- Belirli bir portu veya ilk boş portu otomatik bularak bulunulan dizini hızlıca yerel ağda yayınlayan, bağımsız ve pratik bir HTTP statik dosya sunucusu.

### [m3u8_video_downloader](m3u8_video_downloader/)
- `ffmpeg` altyapısını kullanarak `.m3u8` uzantılı yayın veya video bağlantılarını indirip doğrudan `.mp4` video formatına dönüştüren indirme betiği.

### [multiThread](multiThread/)
- Verimli paralel görev yürütümü sağlamak amacıyla oluşturulmuş, thread-safe (iş parçacığı güvenli) profesyonel iş parçacığı havuzu (thread pool) implementasyonu.

### [netsweep](netsweep/)
- Yerel ağdaki canlı IP'leri sürekli keşfedip güncelleyen ve bulduğu makinelerin portlarını paralel olarak tarayan, kendi kendine yeten (standart kütüphane) ağ tarama aracı; Linux ve Windows'ta çalışır, isteğe bağlı nmap motoru destekler.

### [pip_update_install_necessary](pip_update_install_necessary/)
- Kurulu olan tüm pip paketlerini tek seferde güncelleyen ve kurulu paket listelerini bir metin dosyasına (TXT) yedekleyen pratik güncelleme aracı.

### [python_project_structuring/](python_project_structuring/)
- Modern Python uygulamaları için gerekli olan gelişmiş klasör ve dosya yapısını otomatik olarak inşa ederek projeyi daha iyi organize etmenizi sağlayan yapılandırıcı.

### [web_FileTreeCreator](web_FileTreeCreator/)
- Web sitesi veya dosya sistemi dokümantasyonu için alt dizin ve dosyaları tarayarak boyut, tarih, tam URL gibi verilerle birlikte JSON ağacı (file tree) oluşturan araç.

### [web_LinkTreeCreator](web_LinkTreeCreator/)
- Web sitesi gezintisini kolaylaştırmak amacıyla `.html` dosyalarını tarayıp dizin hiyerarşisini analiz ederek bir JSON link ağacı (link tree) inşa eden gezinti aracı.

<br><hr><br>