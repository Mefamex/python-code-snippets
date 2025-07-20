# POOL Thread Pool - Python Çoklu İş Parçacığı Kütüphanesi

Python'da verimli ve kolay paralel görev yürütümü için profesyonel bir thread pool (iş parçacığı havuzu) implementasyonu.

Görevleri çoklu iş parçacığı ile aynı anda çalıştırır, thread-safe görev yönetimi sağlar ve performans metrikleri sunar.

I/O yoğun işlemler için optimize edilmiş, basit API ile kolay kullanım imkanı sunmaktadır.

> *last_modify: 2025-07-20*

<br>


## Özellikler
- **Verimli Paralel Çalışma:** Görevleri çoklu iş parçacığı ile aynı anda çalıştırır
- **Dinamik Havuz Yönetimi:** Maksimum iş parçacığı sayısını belirleyebilirsiniz
- **Thread-Safe Tasarım:** Güvenli görev ekleme ve sonuç toplama
- **Esnek Sonuç Yönetimi:** Sonuçları saklayabilir veya anında yazdırabilirsiniz
- **Performans Ölçümü:** Otomatik süre hesaplama ve performans metrikleri
- **Basit API:** Kolay kullanım için sezgisel metot isimleri
- **Harici Bağımlılık Yok:** Sadece Python standart kütüphanesini kullanır


<br>


## Gereksinimler
- Python 3.6 veya üzeri
- Sadece standart kütüphane modülleri: `threading`, `queue`, `time`, `random`


<br>


## Kurulum
1. Scripti `threadpool.py` olarak kaydedin.
2. Ekstra bağımlılık gerekmez (sadece standart kütüphane kullanılır).
3. Projenizde import ederek kullanın:
   ```python
   from threadpool import POOL
   ```


<br>


## Kullanım

### Temel Kullanım
```python
from threadpool import POOL
from time import sleep

def kare_al(x):
    sleep(0.1)  # Simülasyon için gecikme
    return x * x

# Thread pool oluştur
pool = POOL(max_threads=4, logFuture=True, ResultwhenDone=False)

# Görevleri ekle
for i in range(10):
    pool.submit(kare_al, i)

# Tüm görevlerin tamamlanmasını bekle ve sonuçları al
sonuclar, gecen_sure, toplam_is_suresi = pool.join()

print("Sonuçlar:", sonuclar)
print(f"Toplam geçen süre: {gecen_sure:.2f} saniye")
print(f"Kurtarılan süre: {toplam_is_suresi-gecen_sure:.2f} saniye")
```

### Farklı Parametrelerle Kullanım
```python
from threadpool import POOL

def topla(x, y):
    return x + y

def carp(x, y, carpan=1):
    return (x * y) * carpan

# Sonuçları anında yazdıran pool
pool = POOL(max_threads=2, logFuture=True, ResultwhenDone=True)

# Farklı fonksiyonlar ve parametrelerle görev ekleme
pool.submit(topla, 5, 3)
pool.submit(carp, 4, 2, carpan=3)
pool.submit(lambda x: x**2, 6)

# Sonuçları bekle
sonuclar, gecen_sure, toplam_sure = pool.join()
```

### I/O Yoğun İşlemler İçin
```python
import requests
from threadpool import POOL

def url_kontrol(url):
    try:
        response = requests.get(url, timeout=5)
        return f"{url}: {response.status_code}"
    except:
        return f"{url}: Hata"

urls = [
    "https://google.com",
    "https://github.com",
    "https://stackoverflow.com"
]

pool = POOL(max_threads=3, logFuture=True)
for url in urls:
    pool.submit(url_kontrol, url)

sonuclar, _, _ = pool.join()
for sonuc in sonuclar:
    print(sonuc)
```


<br>


## API Referansı

### POOL(max_threads=10, logFuture=True, ResultwhenDone=False)
Thread pool sınıfı ana constructor'ı.

**Parametreler:**
- `max_threads` (int): Havuzdaki maksimum iş parçacığı sayısı (varsayılan: 10)
- `logFuture` (bool): Görev sonuçlarını bir listede saklar (varsayılan: True)
- `ResultwhenDone` (bool): Görev tamamlanınca anında yazdırır (varsayılan: False)

### submit(func, *args, **kwargs)
Yeni bir görevi thread pool'a ekler.

**Parametreler:**
- `func`: Çalıştırılacak fonksiyon
- `*args`: Fonksiyona geçilecek pozisyonel argümanlar
- `**kwargs`: Fonksiyona geçilecek anahtar kelime argümanları

### join()
Tüm görevlerin tamamlanmasını bekler ve sonuçları döner.

**Returns:**
- `tuple`: (sonuç_listesi, geçen_süre, toplam_görev_süresi)


<br>


## Performans Notları
- **I/O Yoğun İşlemler:** Bu thread pool I/O yoğun işlemler için idealdir
- **CPU Yoğun İşlemler:** CPU yoğun işlemler için multiprocessing modülü tercih edilmelidir
- **Optimal Thread Sayısı:** Genellikle CPU çekirdek sayısının 2-4 katı optimal sonuç verir
- **Bellek Kullanımı:** Thread havuzu bellek kullanımını optimize eder
- **GIL Etkisi:** Python'un GIL (Global Interpreter Lock) kısıtlaması nedeniyle CPU-bound işlerde performans artışı sınırlıdır


<br>


## Örnek Çıktı
```
Sonuçlar: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
Toplam geçen süre: 0.34 saniye
 kurtarılan :0.66
```


<br>


## Hata Yönetimi
```python
from threadpool import POOL

def riskli_islem(x):
    if x == 5:
        raise ValueError("5 değeri desteklenmiyor!")
    return x * 2

pool = POOL(max_threads=3, logFuture=True, ResultwhenDone=True)

try:
    for i in range(10):
        pool.submit(riskli_islem, i)
    
    sonuclar, gecen_sure, toplam_sure = pool.join()
    print("İşlem tamamlandı!")
except Exception as e:
    print(f"Hata oluştu: {e}")
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
><br> - [website/projects](https://mefamex.com/projects)
><br> - [Github/Mefamex/python-code-snippets](https://github.com/Mefamex/python-code-snippets)
