# Check File Dependencies

Check File Dependencies, Python projelerinde modül bağımlılıklarını otomatik olarak kontrol eden, yükleyen ve güncelleyen güçlü bir araçtır.

Tek veya çoklu modüllerin yüklü olup olmadığını kontrol eder, eksik olanları otomatik yükler ve sürüm uyumluluğunu doğrular.

Proje geliştirme sürecinde bağımlılık yönetimini otomatikleştirmek için tasarlanmıştır.

> *last_modify: 2025-07-20*

<br>



## Özellikler
- Tek veya çoklu modül bağımlılık kontrolü
- Eksik modüllerin otomatik yüklenmesi
- Sürüm uyumluluğu kontrolü (>=, <=, ==, !=, >, <, ~=)
- Otomatik modül güncelleme özelliği
- Detaylı hata yönetimi ve özel exception sınıfları
- Verbose mod ile detaylı çıktı kontrolü
- Timeout yönetimi


<br>


## Gereksinimler
- Python 3.6 veya üzeri
- pip package manager
- İnternet bağlantısı (modül yükleme için)
- Sadart kütüphane modülleri: `subprocess`, `sys`, `importlib`, `re`, `warnings`, `typing`


<br>


## Kurulum
1. Dosyayı `check_file_dependencies.py` olarak kaydedin.
2. Ekstra bağımlılık gerekmez (sadece standart kütüphane kullanılır).
3. Import ederek kullanın:
   ```python
   from check_file_dependencies import CheckFileDependencies
   ```


<br>


## Kullanım
1. Modülleri import edin ve CheckFileDependencies sınıfını kullanın.
2. Kontrol edilecek modül(ler)i belirtin (sürüm gereksinimleri opsiyonel).
3. Tek modül: `CheckFileDependencies.ensure_module("numpy>=1.20.0")`
4. Çoklu modül: `CheckFileDependencies.check_multiple_modules(["requests", "pandas>=1.3.0"])`
5. Sonuç olarak modüller otomatik yüklenecek/güncellenecek ve kontrol edilecektir.


<br>


## Örnek (Tek Modül)
```python
from check_file_dependencies import CheckFileDependencies

# Basit kontrol
CheckFileDependencies.ensure_module("requests")

# Sürüm belirterek kontrol
CheckFileDependencies.ensure_module("numpy>=1.20.0")
CheckFileDependencies.ensure_module("pandas==1.3.5")
```

## Örnek (Çoklu Modül)
```python
from check_file_dependencies import CheckFileDependencies

# Çoklu modül kontrolü
modules = ["requests", "numpy>=1.20.0", "matplotlib", "pandas>=1.3.0"]
results = CheckFileDependencies.check_multiple_modules(modules)

# Sonuçları kontrol et
failed = [module for module, success in results.items() if not success]
if failed:
    print(f"Eksik modüller: {', '.join(failed)}")
else:
    print("Tüm bağımlılıklar hazır!")
```

## Örnek (Konfigürasyon)
```python
from check_file_dependencies import CheckFileDependencies

# Ayarları değiştir
CheckFileDependencies.AUTO_UPDATE = False  # Otomatik güncelleme kapalı
CheckFileDependencies.VERBOSE = True       # Detaylı çıktı açık
CheckFileDependencies.TIMEOUT = 120        # 2 dakika timeout

# Kontrol et
CheckFileDependencies.ensure_module("tensorflow>=2.0.0")
```


<br>


## Desteklenen Sürüm Operatörleri
- `>=`: Büyük eşit (örn: `numpy>=1.20.0`)
- `<=`: Küçük eşit (örn: `pandas<=1.5.0`)
- `==`: Eşit (örn: `requests==2.25.0`)
- `!=`: Eşit değil (örn: `matplotlib!=3.0.0`)
- `>`: Büyük (örn: `scipy>1.0.0`)
- `<`: Küçük (örn: `flask<2.0.0`)
- `~=`: Uyumlu sürüm (örn: `django~=4.0.0`)


<br>


## Hata Yönetimi
```python
from check_file_dependencies import CheckFileDependencies, DependencyError

try:
    CheckFileDependencies.ensure_module("tensorflow>=2.0.0")
    print("TensorFlow hazır!")
except DependencyError as e:
    print(f"Bağımlılık hatası: {e}")
```


<br>


## Örnek Çıktı
```
[MODULE] Starting dependency check for 3 modules...
============================================================
[MODULE] ✅ ready to use: requests (v2.28.1)
[MODULE] ❓ not exist   : numpy
[MODULE] 📥 downloading : numpy>=1.20.0
[MODULE] ✅ installed   : numpy
[MODULE] 🔄 updating    : matplotlib
[MODULE] ✅ updated     : matplotlib
============================================================
[MODULE] Summary: 3/3 successful
```


<br>


## API Referansı

### CheckFileDependencies.ensure_module()
```python
ensure_module(module_name: str, auto_update: bool = None, verbose: bool = None) -> bool
```
Tek bir modülü kontrol eder ve gerekirse yükler.

### CheckFileDependencies.check_multiple_modules()
```python
check_multiple_modules(modules_list: List[str], auto_update: bool = None, verbose: bool = None) -> Dict[str, bool]
```
Birden fazla modülü kontrol eder ve sonuçları dict olarak döner.

### CheckFileDependencies.get_installed_version()
```python
get_installed_version(module_name: str) -> Optional[str]
```
Yüklü modülün sürümünü döner.

### CheckFileDependencies.compare_versions()
```python
compare_versions(current_version: str, required_version: str) -> bool
```
İki sürümü karşılaştırır.


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
><br> - [website/projects](https://mefamex.com/projects)
><br> - [Github/Mefamex/python-code-snippets](https://github.com/Mefamex/python-code-snippets)
