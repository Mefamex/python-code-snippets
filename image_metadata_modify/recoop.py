from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image):
    exif_data = image._getexif()
    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif_data[tag_name] = exif_data.pop(tag)
        return exif_data
    else:
        return None

def display_metadata(metadata):
    if metadata:
        print("Mevcut Meta Veriler:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print("Resimde meta veri bulunmuyor.")

def modify_metadata(metadata):
    if metadata:
        print("\nMeta Verileri Değiştir (Boş bırakmak için Enter'a basın):")
        for key in metadata.keys():
            new_value = input(f"{key}: ")
            if new_value:
                metadata[key] = new_value
    return metadata

def add_metadata(metadata):
    if metadata is None:
        metadata = {}
    print("\nEklemek İstediğiniz Meta Verileri Girin (Boş bırakmak için Enter'a basın):")
    while True:
        key = input("Anahtar (örn. 'Subject'): ")
        if not key:
            break
        value = input("Değer: ")
        if not value:
            break
        metadata[key] = value
    return metadata

def save_metadata(image_path, metadata):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is None:
        exif_data = {}
    for key, value in metadata.items():
        tag_id = get_tag_id(key)
        if tag_id:
            exif_data[tag_id] = value
    image.save(image_path, exif=exif_data)
    print(f"Meta veriler '{image_path}' dosyasına kaydedildi.")

def get_tag_id(tag_name):
    for tag, tag_id in TAGS.items():
        if TAGS.get(tag, tag) == tag_name:
            return tag
    return None

if __name__ == "__main__":
    image_path = input("Resim dosyasının yolunu girin: ")
    try:
        image = Image.open(image_path)
        metadata = get_exif_data(image)
        display_metadata(metadata)
        metadata = modify_metadata(metadata)
        metadata = add_metadata(metadata)
        save_metadata(image_path, metadata)
    except FileNotFoundError:
        print("Dosya bulunamadı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        

