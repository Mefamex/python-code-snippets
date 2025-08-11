# FileTreeCreator - Web Sitesi Dosya Ağacı Oluşturucu

FileTreeCreator, web sitesi veya dosya sistemi dokümantasyonu için belirtilen dizinden başlayarak tüm alt dizin ve dosyaları özyinelemeli olarak tarayan Python aracıdır.

Dosya ve klasör yapısını JSON formatında dışa aktarır, her dosya için boyut, tarih, göreli yol ve tam URL bilgilerini toplar.

Web sitesi dokümantasyonu ve otomasyonu amacıyla eksiksiz dosya ağacı oluşturmak için tasarlanmıştır.

> *last_modify: 2025-07-20*

<br>


## Özellikler
- **Özyinelemeli Tarama:** Belirtilen kök dizinden başlayarak tüm alt dizin ve dosyaları tarar
- **Kapsamlı Bilgi Toplama:** Dosya/klasör adı, yol, URL, boyut, tarih ve göreli yol bilgilerini toplar
- **JSON Çıktısı:** Dizin yapısını ağaç şeklinde JSON formatında dışa aktarır
- **Akıllı Filtreleme:** Hariç tutulacak klasör ve dosyaları filtreleyebilir
- **URL Oluşturma:** Her dosya ve klasör için otomatik tam URL oluşturur
- **Özelleştirilebilir Çıktı:** Çıktı JSON dosyasını belirtilen dizine kaydeder
- **Web Optimizasyonu:** Web sitesi dokümantasyonu için optimize edilmiş yapı
- **Harici Bağımlılık Yok:** Sadece Python standart kütüphanesini kullanır


<br>


## Gereksinimler
- Python 3.8 veya üzeri
- Sadece standart kütüphane modülleri: `os`, `json`, `datetime`, `pathlib`, `typing`


<br>


## Kurulum
1. Scripti `FileTreeCreator.py` olarak kaydedin.
2. Ekstra bağımlılık gerekmez (sadece standart kütüphane kullanılır).
3. Import ederek kullanın:
   ```python
   from FileTreeCreator import FileTreeCreator
   ```


<br>


## Kullanım

### Temel Kullanım
```python
import os
from pathlib import Path
from FileTreeCreator import FileTreeCreator

# Temel parametrelerle kullanım
base_dir = Path(os.getcwd())
output_dir = Path(os.path.join(base_dir, "output"))
output_file = Path("file_tree.json")

# FileTreeCreator'ı çalıştır
creator = FileTreeCreator(
    base_dir=base_dir,
    output_dir=output_dir,
    output_file=output_file
)
```

### Filtreleme ile Kullanım
```python
from pathlib import Path
from FileTreeCreator import FileTreeCreator

# Belirli klasör ve dosyaları hariç tutarak kullanım
base_dir = Path("/path/to/your/website")
passDirs = ["node_modules", ".git", "__pycache__", "venv"]
passFiles = [".DS_Store", "*.log", "*.tmp"]
output_dir = Path("./output")
output_file = Path("website_tree.json")

creator = FileTreeCreator(
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
from FileTreeCreator import FileTreeCreator

# Proje için özelleştirilmiş kullanım
project_root = Path(os.getcwd())
exclude_dirs = ["dist", "build", "node_modules", ".git"]
exclude_files = ["*.pyc", "*.log", ".env"]
output_location = Path(project_root / "docs" / "file_structure")
output_filename = Path("project_structure.json")

# Dosya ağacını oluştur
FileTreeCreator(
    base_dir=project_root,
    output_dir=output_location,
    output_file=output_filename,
    passDirs=exclude_dirs,
    passFiles=exclude_files
)

print(f"Dosya ağacı başarıyla oluşturuldu: {output_location / output_filename}")
```


<br>


## API Referansı

### FileTreeCreator(base_dir, output_dir, output_file, passDirs=[], passFiles=[])
Ana FileTreeCreator sınıfı constructor'ı.

**Parametreler:**
- `base_dir` (Path): Taranacak kök dizin
- `output_dir` (Path): Çıktı JSON dosyasının kaydedileceği dizin
- `output_file` (Path): Çıktı JSON dosyasının adı
- `passDirs` (list, optional): Hariç tutulacak klasör adları (varsayılan: [])
- `passFiles` (list, optional): Hariç tutulacak dosya adları (varsayılan: [])

### Walker_file
Tek bir dosyanın bilgilerini tutar.

**Özellikler:**
- `name`: Dosya adı
- `path`: Dosya yolu
- `url`: Dosya URL'i
- `size`: Dosya boyutu (byte)
- `date`: Dosya tarihi (YYYY-MM-DD)
- `relative_path`: Göreli dosya yolu
- `full_url`: Tam URL

### Walker_path
Bir dizinin bilgilerini tutar.

**Özellikler:**
- `name`: Klasör adı
- `path`: Klasör yolu
- `url`: Klasör URL'i
- `size`: Klasör boyutu
- `date`: Klasör tarihi
- `relative_path`: Göreli klasör yolu
- `full_url`: Tam URL
- `folder`: Alt klasörler listesi
- `files`: İçindeki dosyalar listesi


<br>


## Çıktı Formatı

### JSON Yapısı
```json
{
  "name": "root_folder",
  "url": "root",
  "size": 0,
  "date": "2025-07-20",
  "relative_path": "",
  "full_url": "https://example.com/root",
  "folder": [
    {
      "name": "subfolder",
      "url": "subfolder",
      "size": 0,
      "date": "2025-07-20",
      "relative_path": "subfolder",
      "full_url": "https://example.com/subfolder",
      "folder": [...],
      "files": [
        {
          "name": "example.txt",
          "url": "subfolder/example.txt",
          "size": 1024,
          "date": "2025-07-20",
          "relative_path": "subfolder/example.txt",
          "full_url": "https://example.com/subfolder/example.txt"
        }
      ]
    }
  ],
  "files": [...]
}
```


<br>


## Konfigürasyon

### BASE_URL Ayarlama
```python
# FileTreeCreator.py dosyasında BASE_URL değişkenini düzenleyin
BASE_URL = "https://yourdomain.com"
```

### Filtreleme Örnekleri
```python
# Yaygın hariç tutma örnekleri
exclude_dirs = [
    "node_modules",     # Node.js bağımlılıkları
    ".git",             # Git repository
    "__pycache__",      # Python cache
    ".vscode",          # VS Code ayarları
    "dist",             # Build çıktıları
    "build"             # Build dizini
]

exclude_files = [
    ".DS_Store",        # macOS sistem dosyası
    "*.log",            # Log dosyaları
    "*.tmp",            # Geçici dosyalar
    ".env",             # Environment değişkenleri
    "*.pyc"             # Python compiled dosyalar
]
```


<br>


## Performans Notları
- **Büyük Dizinler:** Çok büyük dizin yapıları için işlem süresi uzayabilir
- **Filtreleme:** Gereksiz dosya/klasörleri filtrelemek performansı artırır
- **JSON Boyutu:** Çok fazla dosya içeren projeler büyük JSON dosyaları oluşturabilir
- **Bellek Kullanımı:** Tüm dosya bilgileri bellekte tutulur, RAM kullanımına dikkat edin


<br>


## Örnek Kullanım Senaryoları

### Web Sitesi Dokümantasyonu
```python
# Web sitesi dosya yapısını dokümante etmek için
website_creator = FileTreeCreator(
    base_dir=Path("/var/www/html"),
    output_dir=Path("./docs"),
    output_file=Path("website_structure.json"),
    passDirs=["logs", "cache", "tmp"],
    passFiles=["*.log", "*.cache"]
)
```

### Proje Analizi
```python
# Kod projesi analizi için
project_analyzer = FileTreeCreator(
    base_dir=Path("./my_project"),
    output_dir=Path("./analysis"),
    output_file=Path("project_tree.json"),
    passDirs=[".git", "node_modules", "__pycache__"],
    passFiles=["*.pyc", "*.log", ".env"]
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
