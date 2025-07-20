# Python Code Snippets

> *author*: [Mefamex](https://github.com/Mefamex) <br>
> *last_modify: 2025-07-20*


Geliştirme sürecinde ihtiyaç duyduğum Python araçlarını ve kod parçalarını bir arada tutmak için oluşturduğum koleksiyon. Bu repository büyük bir framework değil, pratik çözümler sunan bağımsız araçların derlemesidir.

Her araç kendi başına çalışır ve farklı geliştirme ihtiyaçlarına yanıt verir.


- **Bağımsız Araçlar:** Her proje tek başına çalışabilir, birbirine bağımlı değil
- **Standart Kütüphane:** Harici bağımlılık yok, sadece Python built-in modülleri kullanılır  
- **Detaylı Dokümantasyon:** Her araç için ayrı README ve kullanım örnekleri
- **Versiyon Geçmişi:** Her projenin versions klasöründe eski sürümleri mevcut
- **Kolay Entegrasyon:** Projelere doğrudan kopyalayıp kullanabilirsiniz



<br>

## İçindekiler

- [check_file_dependencies](check_file_dependencies/)
  - [`check_file_dependencies.py`](check_file_dependencies/check_file_dependencies.py)
  - [`README.md`](check_file_dependencies/README.md)

- [directory_explorer](directory_explorer/)
  - [`directory_explorer.py`](directory_explorer/directory_explorer.py)
  - [`README.md`](directory_explorer/README.md)

- [multiThread](multiThread/)
  - [`threadpool.py`](multiThread/threadpool.py)
  - [`README.md`](multiThread/README.md)

- [web_FileTreeCreator](web_FileTreeCreator/)
  - [`FileTreeCreator.py`](web_FileTreeCreator/FileTreeCreator.py)
  - [`README.md`](web_FileTreeCreator/README.md)

- [web_LinkTreeCreator](web_LinkTreeCreator/)
  - [`LinkTreeCreator.py`](web_LinkTreeCreator/LinkTreeCreator.py)
  - [`README.md`](web_LinkTreeCreator/README.md)


<br>


## Projeler

**check_file_dependencies:** Python projelerinde modül bağımlılıklarını otomatik kontrol eden, eksik olanları yükleyen araç . [incele](check_file_dependencies/README.md)

**directory_explorer:** Dizin yapısını özyinelemeli olarak tarayan, boyutları hesaplayan ve JSON/TXT formatında dışa aktaran araç . [incele](directory_explorer/README.md)

**multiThread:** Paralel görev yürütümü için thread pool implementasyonu . [incele](multiThread/README.md)

**web_FileTreeCreator:** Web sitesi dosya ağacı oluşturmak için dizinleri tarayan ve JSON çıktısı üreten araç . [incele](web_FileTreeCreator/README.md)

**web_LinkTreeCreator:** Web sitesi navigasyonu için HTML dosyalarını tarayarak link ağacı oluşturan araç . [incele](web_LinkTreeCreator/README.md)
