# Directory Explorer

Directory Explorer, dizin yapılarını görselleştirmek, analiz etmek ve dışa aktarmak için esnek bir Python aracıdır. 

Dizinleri özyinelemeli olarak tarar, klasör ve dosya boyutlarını hesaplar.

Sonuçları hem JSON hem de TXT formatında dışa aktarır. 

Komut satırından kolayca kullanılabilir ve farklı analiz ihtiyaçları için özelleştirilebilir.

> *last_modify: 2025-07-20*

<br>


## Özellikler
- Dizin yapılarını özyinelemeli olarak tarar ve analiz eder
- Klasör ve dosya boyutlarını hesaplar
- Sonuçları JSON ve TXT dosyası olarak dışa aktarır
- Özelleştirilebilir çıktı ve kolay komut satırı kullanımı
- Harici bağımlılık yoktur (sadece Python standart kütüphanesini kullanır)


<br>


## Gereksinimler
- Python 3.7 veya üzeri
- Sadece standart kütüphane modülleri: `os`, `json`, `datetime`, `pathlib`, `typing`, `argparse`, `dataclasses`, `re`, `time`


<br>


## Kurulum
1. Scripti `directory_explorer.py` olarak kaydedin.
2. Ekstra bağımlılık gerekmez (sadece standart kütüphane kullanılır).
3. Gerekirse `if __name__ == "__main__":` bloğunu düzenleyin.
4. Terminalde çalıştırın:
   ```sh
   python directory_explorer.py [path] [--no-print] [--no-json] [--no-txt]
   ```


<br>


## Kullanım
1. Ana dizini ve çıktı dizinini belirtin (varsayılan: Desktop).
2. İsteğe bağlı olarak hariç tutulacak dizin ve dosya adlarını girin.
3. Scripti çalıştırın:
   ```sh
   python directory_explorer.py [path] [--no-print] [--no-json] [--no-txt]
   ```
4. Argümanlar:
   - `path`: Taranacak kök dizin (varsayılan: geçerli çalışma dizini)
   - `--no-print`: Dizin verisini ekrana yazdırmaz
   - `--no-json`: Dizin verisini JSON dosyasına aktarmayı kapatır
   - `--no-txt`: Dizin verisini TXT dosyasına aktarmayı kapatır
5. Sonuçlar belirtilen dizinde JSON ve/veya TXT dosyası olarak kaydedilecektir.


<br><br>


## Örnek (python)
```python
from pathlib import Path
explorer = DirectoryExplorer(Path.home() / "Desktop")
# Geçerli çalışma dizinini kullanmak için
# explorer = DirectoryExplorer(os.getcwd()) 
explorer.run(print_data=True, exportJson=True, exportTxt=True)
```

### Örnek (komut satırı)
```sh
python directory_explorer.py 

python directory_explorer.py [path] [--no-print] [--no-json] [--no-txt]

python directory_explorer.py [path] [--no-print] [--no-json] 
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
Bu yazılım, herhangi bir garanti olmaksızın "olduğu gibi" sağlanmaktadır. Kullanım riski kullanıcıya aittir. Tam yasal uyarı için script dosyasına bakınız.



<br><br><hr>

>    Connected : 
><br> - [website/projects](https://mefamex.com/projects)
><br> - [Github/Mefamex/python-code-snippets](https://github.com/Mefamex/python-code-snippets)
