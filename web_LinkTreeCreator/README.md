# LinkTreeCreator

LinkTreeCreator, web sitesi link navigasyonu için belirtilen dizindeki tüm .html dosyalarını tarayarak kolay gezinme ve erişim için bir link ağacı (link tree) oluşturan Python aracıdır.

Dizin ve dosya yapısını JSON formatında dışa aktarır, her dosya için URL, tarih, göreli yol ve tam URL bilgilerini toplar.

Web sitesi link navigasyonu ve HTML dosya indeksleme amacıyla optimize edilmiş link ağacı oluşturmak için tasarlanmıştır.

> *last_modify: 2025-07-20*

<br>


## Özellikler
- **Özyinelemeli HTML Tarama:** Belirtilen kök dizinden başlayarak tüm alt dizinlerdeki .html dosyalarını tarar
- **Kapsamlı Bilgi Toplama:** Dosya/klasör adı, yol, URL, tarih ve göreli yol bilgilerini toplar
- **JSON Çıktısı:** Dizin yapısını ağaç şeklinde JSON formatında dışa aktarır
- **Akıllı Filtreleme:** Hariç tutulacak klasör ve dosyaları filtreleyebilir
- **URL Oluşturma:** Her dosya ve klasör için otomatik tam URL oluşturur
- **Özelleştirilebilir Çıktı:** Çıktı JSON dosyasını belirtilen dizine kaydeder
- **Web Optimizasyonu:** Web sitesi link navigasyonu için optimize edilmiş yapı
- **Harici Bağımlılık Yok:** Sadece Python standart kütüphanesini kullanır


<br>

## Gereksinimler
- Python 3.8 veya üzeri
- Sadece standart kütüphane modülleri: `os`, `json`, `datetime`, `pathlib`, `typing`


<br>

## Kurulum
1. Scripti `LinkTreeCreator.py` olarak kaydedin.
2. Ekstra bağımlılık gerekmez (sadece standart kütüphane kullanılır).
3. Import ederek kullanın:
   ```python
   from LinkTreeCreator import LinkTreeCreator
   ```


<br>

## Kullanım

### Temel Kullanım
```python
import os
from pathlib import Path
from LinkTreeCreator import LinkTreeCreator

# Temel parametrelerle kullanım
base_dir = Path(os.getcwd())
output_dir = Path(os.path.join(base_dir, "output"))
output_file = Path("link_tree.json")

# LinkTreeCreator'ı çalıştır
creator = LinkTreeCreator(
    base_dir=base_dir,
    output_dir=output_dir,
    output_file=output_file
)
```

### Filtreleme ile Kullanım
```python
from pathlib import Path
from LinkTreeCreator import LinkTreeCreator

# Belirli klasör ve dosyaları hariç tutarak kullanım
base_dir = Path("/path/to/your/website")
passDirs = ["admin", "temp", "logs", "cache"]
passFiles = ["test_", "backup_", "draft_"]
output_dir = Path("./output")
output_file = Path("website_tree.json")

creator = LinkTreeCreator(
    base_dir=base_dir,
    output_dir=output_dir,
    output_file=output_file,
    passDirs=passDirs,
    passFiles=passFiles
)
```

### Özelleştirilmiş Kullanım
```python
import os
from pathlib import Path
from LinkTreeCreator import LinkTreeCreator

# Proje için özelleştirilmiş kullanım
project_root = Path(os.getcwd())
exclude_dirs = ["admin", "logs", "cache", "temp"]
exclude_files = ["test_", "backup_", "draft_"]
output_location = Path(project_root / "docs" / "navigation")
output_filename = Path("link_structure.json")

# Link ağacını oluştur
LinkTreeCreator(
    base_dir=project_root,
    output_dir=output_location,
    output_file=output_filename,
    passDirs=exclude_dirs,
    passFiles=exclude_files
)

print(f"Link ağacı başarıyla oluşturuldu: {output_location / output_filename}")
```


<br>

## API Referansı

### LinkTreeCreator(base_dir, output_dir, output_file, passDirs=[], passFiles=[])
Ana LinkTreeCreator sınıfı constructor'ı.

**Parametreler:**
- `base_dir` (Path): Taranacak kök dizin
- `output_dir` (Path): Çıktı JSON dosyasının kaydedileceği dizin
- `output_file` (Path): Çıktı JSON dosyasının adı
- `passDirs` (list, optional): Hariç tutulacak klasör adları (varsayılan: [])
- `passFiles` (list, optional): Hariç tutulacak dosya adları (varsayılan: [])

### Walker_link
Tek bir HTML dosyasının bilgilerini tutar.

**Özellikler:**
- `name`: Dosya adı
- `path`: Dosya yolu
- `url`: Dosya URL'i
- `date`: Dosya tarihi (YYYY-MM-DD)
- `relative_path`: Göreli dosya yolu
- `full_url`: Tam URL

### Walker_path
Bir dizinin bilgilerini tutar.

**Özellikler:**
- `name`: Klasör adı
- `path`: Klasör yolu
- `url`: Klasör URL'i
- `date`: Klasör tarihi
- `relative_path`: Göreli klasör yolu
- `full_url`: Tam URL
- `dirs`: Alt klasörler listesi
- `files`: İçindeki dosyalar listesi


<br>

## Çıktı Formatı

### JSON Yapısı
```json
{
  "name": "root_folder",
  "url": "root",
  "date": "2025-07-20",
  "relative_path": "",
  "full_url": "https://mefamex.com/root",
  "dirs": [
    {
      "name": "subfolder",
      "url": "subfolder",
      "date": "2025-07-20",
      "relative_path": "subfolder",
      "full_url": "https://mefamex.com/subfolder",
      "dirs": [],
      "files": [
        {
          "name": "page.html",
          "url": "subfolder/page.html",
          "date": "2025-07-20",
          "relative_path": "subfolder/page.html",
          "full_url": "https://mefamex.com/subfolder/page.html"
        }
      ]
    }
  ],
  "files": []
}
```


<br>

## Konfigürasyon

### BASE_URL Ayarlama
```python
# LinkTreeCreator.py dosyasında BASE_URL değişkenini düzenleyin
BASE_URL = "https://yourdomain.com"
```

### Filtreleme Örnekleri
```python
# Yaygın hariç tutma örnekleri
exclude_dirs = [
    "admin",            # Yönetim paneli
    "logs",             # Log dosyaları
    "cache",            # Cache dizini
    "temp",             # Geçici dosyalar
    "backup"            # Yedek dosyalar
]

exclude_files = [
    "test_",            # Test dosyaları
    "backup_",          # Yedek dosyalar
    "draft_",           # Taslak dosyalar
    "temp_"             # Geçici dosyalar
]
```


<br>

## Performans Notları
- **Büyük Dizinler:** Çok büyük dizin yapıları için işlem süresi uzayabilir
- **Filtreleme:** Gereksiz dosya/klasörleri filtrelemek performansı artırır
- **JSON Boyutu:** Çok fazla HTML dosyası içeren projeler büyük JSON dosyaları oluşturabilir
- **Bellek Kullanımı:** Tüm dosya bilgileri bellekte tutulur, RAM kullanımına dikkat edin


<br>

## Örnek Kullanım Senaryoları

### Web Sitesi Link Navigasyonu
```python
# Web sitesi link yapısını dokümante etmek için
website_creator = LinkTreeCreator(
    base_dir=Path("/var/www/html"),
    output_dir=Path("./docs"),
    output_file=Path("website_links.json"),
    passDirs=["admin", "logs", "cache"],
    passFiles=["test_", "temp_"]
)
```

### Blog Sitesi Analizi
```python
# Blog link analizi için
blog_analyzer = LinkTreeCreator(
    base_dir=Path("./blog_site"),
    output_dir=Path("./analysis"),
    output_file=Path("blog_tree.json"),
    passDirs=["admin", "logs", "temp"],
    passFiles=["draft_", "backup_"]
)
```


<br>

## Lisans
MIT Lisansı (https://opensource.org/licenses/MIT)


<br>

## Yazar
- @mefamex (info@mefamex.com)
    - GitHub: [github.com/Mefamex](https://github.com/Mefamex)
    - www: [mefamex.com](https://mefamex.com)


<br>

## Yasal Uyarı
Bu yazılım, herhangi bir garanti olmaksızın "olduğu gibi" sağlanmaktadır. Kullanım riski kullanıcıya aittir. Production ortamlarında kullanımdan önce test edilmesi önerilir.



<br><br><hr>

>    Connected : 
><br> - [website/py](https://mefamex.com/py)
><br> - [Github/Mefamex/python-code-snippets](https://github.com/Mefamex/python-code-snippets)
