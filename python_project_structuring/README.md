# Python Proje Yapılandırıcı

Modern Python projeleri için gerekli klasör ve dosya yapısını otomatik oluşturan araçlar: hızlı bir **temel** şablon (proje dizini + `.venv` + `main.py`) ve kurumsal düzeyde bir **gelişmiş** şablon (src-layout, testler, CI, Docker, dokümantasyon).

> *last_modify: 2026-10-14*

<br>


## Özellikler
- **Temel yapı:** proje dizini + `.venv` + `main.py` + `README.md` iskeletini tek `.bat` ile oluşturur
- **Gelişmiş yapı:** src-layout, katmanlı mimari (core/api/data/external), test piramidi, GitHub Actions, Docker, Sphinx, pre-commit
- **Otomatik içerik:** şablon dosyalar boş değil, hazır içerikle üretilir
- **Harici bağımlılık yok:** yalnızca Python standart kütüphanesi


<br>


## Gereksinimler
| Bileşen    | Gereksinim              |
| ---------- | ----------------------- |
| Python     | 3.8+                    |
| OS         | Windows / Linux / macOS |
| Bağımlılık | Yok                     |

> `basic_structure_create.bat` Windows içindir; `basic_structure.md` içindeki komutları Linux/macOS'ta elle uygulayabilirsiniz.


<br>


## Kurulum

Bu snippet, [`python-code-snippets`](https://github.com/Mefamex/python-code-snippets) reposunun içindedir. Tüm repoyu indirmeden **sadece bu klasörü** çekebilirsiniz:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/Mefamex/python-code-snippets.git
cd python-code-snippets
git sparse-checkout set python_project_structuring
```

> Klasörü GitHub'dan indirip `python_project_structuring` içine koymanız da yeterlidir.
>
> Ayrıntılar (arşivle indirme, `sparse-checkout add/list/disable`, alias) için:
> [Git ile Sadece Belirli Alt Klasörleri Klonlama](https://www.mefamex.com/blog/git-sparse-checkout-klonlama/)


<br>


## Kullanım

### Temel yapı (hızlı başlangıç)
Rehber: [`basic_structure.md`](basic_structure.md) — adımların otomatik hâli:

```bat
basic_structure_create.bat
```

> Çalıştırmadan önce dosya içindeki `[project_name]` yerine kendi proje adınızı yazın.

### Gelişmiş yapı (profesyonel proje)
Rehber: [`advanced_structure.md`](advanced_structure.md) — otomatik oluşturucu:

```bash
python advanced_structure_create.py
```

> Script proje adını interaktif olarak sorar; onayladıktan sonra tüm dosya ve klasörleri oluşturur.


<br>


## Dosyalar
| Dosya | Açıklama |
| ----- | -------- |
| `basic_structure_create.bat` | Temel proje iskeletini oluşturan Windows betiği. |
| `basic_structure.md` | Temel yapının adım adım komut rehberi. |
| `advanced_structure_create.py` | Gelişmiş proje yapısını interaktif oluşturan script. |
| `advanced_structure.md` | Gelişmiş yapının ve dosya içeriklerinin rehberi. |


<br>


### Proje Bağlantıları
- [MEFAMEX | Python Code Snippets](https://github.com/Mefamex/python-code-snippets)
- [Mefamex.com/projects](https://mefamex.com/projects/)
