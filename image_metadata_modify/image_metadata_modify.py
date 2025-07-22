# -*- coding: utf-8 -*-
# Created on Friday, July 19 15:30:00 2024
# @author: mefamex

# project_name = "image-meta-dataset"
# project_version = "1.0.0"
# project_author = "Mefamex"
# project_date = "29.01.2025"
# project_description = "This is a project description"
# project_license = "MIT"
# project_repository = "https://github.com/Mefamex/image-meta-dataset"
# project_url = "https://mefamex.com/projects/image-meta-dataset"

# pip install piexif pillow 
from PIL import Image
import os, piexif, piexif.helper

print("----------------------------------------\n"+os.getcwd())
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))
print(__file__)
print("Pillow Version:", Image.__version__, "\n----------------------------------------\n")

from PIL import Image
import os, piexif, piexif.helper 



def display_metadata(image_path):
    if not os.path.exists(image_path):
        print(f"Hata: {image_path} bulunamadı.")
        return
    
    image = Image.open(image_path)
    exif_bytes = image.info.get("exif")
    exif_data = piexif.load(exif_bytes) if exif_bytes else {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
    
    print("Mevcut Metadata:")
    for ifd in exif_data:
        if exif_data[ifd] is None or isinstance(exif_data[ifd], bytes):
            continue
        for tag, value in exif_data[ifd].items():
            try:
                if isinstance(value, bytes):
                    value = value.decode(errors='ignore')
                print(f"{piexif.TAGS[ifd][tag]['name']}: {value}")
            except KeyError:
                print(f"{tag}: {value}")
    print("............................................")


def delete_image_metadata(image_path, output_path):
    if not os.path.exists(image_path):
        print(f"Hata: {image_path} bulunamadı.")
        return
    image = Image.open(image_path)
    exif_bytes = image.info.get("exif")
    exif_data = piexif.load(exif_bytes) if exif_bytes else {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
    exif_bytes = piexif.dump(exif_data)
    image.save(output_path, exif=exif_bytes)
    print(f"{image_path} dosyasındaki metadata başarıyla silindi ve {output_path} dosyasına kaydedildi.")
    print("............................................")


# Örnek Kullanım
image_path = "a.jpg"
output_path = "aa.jpg"
display_metadata(image_path)
delete_image_metadata(image_path, output_path)
display_metadata(output_path)
