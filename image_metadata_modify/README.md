# Image Meta Dataset

## Proje Hakkında
 
**Image Metadata Dataset**, görüntü dosyalarının meta verilerini okuma, silme ve yönetme işlemlerini kolaylaştıran bir Python projesidir. Bu proje, Pillow ve Piexif kütüphanelerini kullanarak görüntü dosyalarının EXIF verilerini işler. Proje, kullanıcıların görüntü dosyalarının meta verilerini kolayca görüntülemesine ve düzenlemesine olanak tanır.

## Özellikler

- **Meta Veri Görüntüleme**: Görüntü dosyalarının mevcut meta verilerini görüntüler.
- **Meta Veri Silme**: Görüntü dosyalarından meta verileri siler ve yeni bir dosya olarak kaydeder.
- **Kullanıcı Dostu Arayüz**: Kullanıcıların işlemleri kolayca gerçekleştirmesine olanak tanır.
- **Desteklenen Formatlar**: JPEG, PNG gibi yaygın görüntü formatlarını destekler.

## UV Entegrasyonu

**UV**, Rust ile yazılmış, son derece hızlı bir Python paket ve proje yöneticisidir. [Ziyaret et](https://docs.astral.sh/uv/).

## Kurulum

Projeyi kullanmak için aşağıdaki adımları izleyin:

1. **Python Kurulumu**: Projeyi çalıştırmak için Python 3.x gereklidir.

2. **Gerekli Kütüphanelerin Kurulumu**:
   ```bash
   pip install pillow piexif
   ```

3. Projeyi Klonlama:
    ```bash
    git clone https://github.com/Mefamex/image-meta-dataset.git
    cd image-meta-dataset
    ```

## Kullanım

Projeyi kullanmak için aşağıdaki adımları izleyin:

1. Meta Veri Görüntüleme:
    ```python
    from metadata_manager import display_metadata
    display_metadata("path/to/your/image.jpg")
    ```

2. Meta Veri Silme:
    ```python
    from metadata_manager import delete_image_metadata
    delete_image_metadata("path/to/your/image.jpg", "path/to/output/image.jpg")
    ```

## Örnek Kullanım
```python
image_path = "a.jpg"
output_path = "aa.jpg"
display_metadata(image_path)
delete_image_metadata(image_path, output_path)
display_metadata(output_path)
```

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## İletişim

Proje ile ilgili herhangi bir sorunuz veya öneriniz varsa, lütfen benimle [iletişime geçin](https://mefamex.com/contact/).
