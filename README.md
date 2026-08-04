# Python Code Snippets

> *author*: [Mefamex](https://github.com/Mefamex) <br>
> *last_modify: 2026-08-04*

Geliştirme sırasında sık ihtiyaç duyduğum Python araçlarını ve küçük ama işe yarar kod parçalarını tek yerde topladığım koleksiyon. Bu depo bir framework değil; her klasör kendi başına çalışabilen, pratik bir araç ya da örnek içerir.

Projede ağırlıkla standart kütüphane kullanılır. Ancak medya işleme, EXIF düzenleme veya video dönüştürme gibi bazı araçlar kendi README dosyalarında belirtildiği üzere ek bağımlılıklar ya da harici araçlar isteyebilir.

## Genel Özellikler
- Her araç bağımsız çalışır ve gerektiğinde doğrudan kopyalanabilir.
- Her projenin kendi kullanım notu ve örnekleri vardır.
- Dizin analizi, dosya ağacı üretimi, medya dönüştürme ve bakım otomasyonu için küçük yardımcılar içerir.
- Bazı araçların eski sürümleri `release` klasörlerinde saklanır.

## Proje Haritası

### Dizin, proje ve bakım araçları
- [file_analyzer.py](file_analyzer.py) - Dizinleri tarayıp dosya türlerine göre karakter sayımı yapan ve sonucu `_folder_analysis_results.txt` olarak kaydeden analiz aracı.
- [directory_explorer](directory_explorer/README.md) - Dizinleri özyinelemeli tarayan, boyut hesaplayan ve JSON/TXT çıktısı üreten araç.
- [python_project_structuring](python_project_structuring/README.md) - Modern Python proje iskeleti oluşturan yapı üretici.
- [check_file_dependencies](check_file_dependencies/README.md) - Modül bağımlılıklarını denetleyen ve eksik paketleri yükleyebilen araç.
- [multiThread](multiThread/README.md) - Basit bir thread pool ile paralel görev yürütme aracı.
- [pip_update_install_necessary](pip_update_install_necessary/pipInstall_requ.py) - Gereken paketleri topluca kurup güncellemek için bakım betiği.

### Medya araçları
- [convert_to_wav/convert_to_wav.py](convert_to_wav/convert_to_wav.py) - Ses dosyalarını ffmpeg ile WAV formatına dönüştüren araç.
- [image_metadata_modify](image_metadata_modify/README.md) - Görsellerin EXIF/meta verilerini okuma ve silme araçları.
- [image-converter](image-converter/README.md) - Instagram odaklı görsel dönüştürme ve optimize etme aracı.
- [m3u8_video_downloader](m3u8_video_downloader/m3u8_video_downloader.py) - M3U8/HLS akışlarını mp4 benzeri çıktılara indirmek için kullanılan basit indirme betiği.

### Web ve yerel servis araçları
- [localHost-server](localHost-server/README.md) - Seçilen port aralığında ilk uygun portu bulup statik dosya sunan yerel HTTP sunucusu.
- [web_FileTreeCreator](web_FileTreeCreator/README.md) - Web sitesi ya da dosya sistemi için JSON tabanlı dosya ağacı oluşturan araç.
- [web_LinkTreeCreator](web_LinkTreeCreator/README.md) - HTML dosyalarından link ağacı oluşturan web navigasyon yardımcısı.

### Dokümantasyon ve örnekler
- [PYTHON_DOCSTRING_example.md](PYTHON_DOCSTRING_example.md) - Python fonksiyon, sınıf ve modülleri için docstring şablonu.

## Kısa Notlar
- Her klasördeki README, o aracın ayrıntılı kullanımını içerir.
- Medya araçları için sistem bağımlılıkları veya pip paketleri gerekebilir.
- Bazı araçlar daha çok günlük kullanım için yazılmıştır; üretim ortamına taşımadan önce test edilmelidir.

<br><hr><br>



