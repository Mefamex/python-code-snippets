# pip Güncelleme ve Kurulum Araçları

Kurulu tüm pip paketlerini tek seferde güncelleyen, seçili paket listelerini (`.txt`) işleyen ve kurulu paket envanterini metin dosyasına yedekleyen pratik araçlar.

> *last_modify: 2026-10-14*

<br>


## Özellikler
- **Toplu güncelleme:** kurulu tüm paketleri tek komutla günceller
- **Listeden güncelleme:** seçtiğiniz `.txt` paket listesini baştan sona günceller
- **Toplu kurulum:** birden fazla `requ*.txt` dosyasını birleştirip paralel kurar/günceller
- **Yedekleme:** kurulu paket listesini metin dosyasına aktarır
- **Harici bağımlılık yok:** yalnızca Python standart kütüphanesi


<br>


## Gereksinimler
| Bileşen    | Gereksinim              |
| ---------- | ----------------------- |
| Python     | 3.8+                    |
| OS         | Windows / Linux / macOS |
| Bağımlılık | Yok (yalnızca `pip`)    |


<br>


## Kurulum

Bu snippet, [`python-code-snippets`](https://github.com/Mefamex/python-code-snippets) reposunun içindedir. Tüm repoyu indirmeden **sadece bu klasörü** çekebilirsiniz:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/Mefamex/python-code-snippets.git
cd python-code-snippets
git sparse-checkout set pip_update_install_necessary
```

> Klasörü GitHub'dan indirip `pip_update_install_necessary` içine koymanız da yeterlidir.
>
> Ayrıntılar (arşivle indirme, `sparse-checkout add/list/disable`, alias) için:
> [Git ile Sadece Belirli Alt Klasörleri Klonlama](https://www.mefamex.com/blog/git-sparse-checkout-klonlama/)


<br>


## Kullanım

### 1. Kurulu tüm paketleri güncelle — `pyAllUpdate.py`
Çalışınca önce kurulu tüm paketleri günceller, ardından klasördeki `.txt` listelerinden hangisini kullanacağınızı sorar:

```bash
cd pip_update_install_necessary
python pyAllUpdate.py
```

### 2. `requ*.txt` listelerinden kurulum — `pipInstall_requ.py`
`requ_necessary.txt`, `requ_necessary-2.txt` ve `requ_extra.txt` dosyalarını birleştirip içindeki paketleri paralel (thread pool ile) kurar/günceller:

```bash
cd pip_update_install_necessary
python pipInstall_requ.py
```

> Script çalıştığı dizindeki `requ_necessary.txt`, `requ_necessary-2.txt` ve `requ_extra.txt` dosyalarını okur; hepsi klasörde hazır gelir.

### 3. Tek satırlık komutlar — `all-update-with-cmd.md`
Terminal ile tek komutta tüm paketleri güncellemek için (Linux/macOS ve Windows/PowerShell): [`all-update-with-cmd.md`](all-update-with-cmd.md)


<br>


## Dosyalar
| Dosya | Açıklama |
| ----- | -------- |
| `pyAllUpdate.py` | Kurulu tüm paketleri + seçilen `.txt` listesini günceller, paket envanterini yedekler. |
| `pipInstall_requ.py` | `requ_*.txt` listelerini birleştirip paralel pip kurulumu/güncellemesi yapar. |
| `all-update-with-cmd.md` | Terminal tek satırlık toplu güncelleme komutları. |
| `requ.txt`, `requ_necessary.txt`, `requ_necessary-2.txt`, `requ_extra.txt`, `requ_HARD.txt` | Örnek paket listeleri. |
| `installed_packages.txt` | Kurulu paket listesi (yedek). |


<br>


### Proje Bağlantıları
- [MEFAMEX | Python Code Snippets](https://github.com/Mefamex/python-code-snippets)
- [Mefamex.com/projects](https://mefamex.com/projects/)
