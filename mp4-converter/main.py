# -*- coding: utf-8 -*- 
#!/usr/bin/env python3 

"""
===========================================================
                VIDEO RESIZER TOOL
===========================================================

Description:
    Video dosyalarını yeniden boyutlandırmak ve format dönüştürme yapmak için 
    geliştirilmiş komut satırı aracı. OpenCV tabanlı, hızlı ve güvenilir video 
    işleme imkanı sunar.

Author:
    Mefamex (info@mefamex.com) (https://mefamex.com)

Features: 
    - 20+ video formatını destekler (mp4, avi, mkv, mov, wmv, flv, vs.)
    - 10 farklı codec seçeneği (mp4v, XVID, H264, MJPG, vs.)
    - Tek dosya veya klasör işleme
    - Bozuk frame koruması ve hata yönetimi
    - Komut satırı ve interaktif mod
    - Gerçek zamanlı ilerleme takibi
    - Kalite preset'leri (web, mobile, hd, archive)

Classes:
    - Resize: Ana video işleme sınıfı, boyutlandırma ve codec dönüştürme

Functions:
    - main(): Ana program başlatıcı ve argüman parser
    - get_user_input(): Kullanıcıdan interaktif parametre alma
    - flat_dict(): Dictionary'leri düzgün formatla yazdırma

Usage:
    # Temel kullanım
    python main.py video.mp4
    
    # Parametreli kullanım
    python main.py video.mp4 -y 1080 -f 30 -c H264
    
    # Klasör işleme
    python main.py /path/to/videos/ -y 720
    
    # İnteraktif mod
    python main.py --help-me

Requirements:
    - Python 3.8+
    - Dependencies:
        - opencv-python (>=4.5.0)
        - pathlib (standart)
        - argparse (standart)

Installation:
    1. Gerekli paketleri yükle: `pip install opencv-python`
    2. Scripti çalıştır: `python main.py`

Supported Formats:
    Video: mp4, avi, mkv, mov, wmv, flv, webm, m4v, 3gp, asf, mpg, mpeg, 
            mp2, mts, m2ts, ts, vob, ogv, dv, rm, rmvb
    Codecs: mp4v, XVID, H264, MJPG, X264, DIVX, VP80, VP90, HEVC, AV01

License:
    MIT Lisansı (https://opensource.org/licenses/MIT)

Changelog:
    - 1.0.0 (2025-01-01): İlk sürüm
    - 1.0.1 (2025-08-11): Gelişmiş codec desteği ve hata yönetimi

Performance Tips:
    - 720p: Orta kalite, hızlı işleme (1080p de hızlı)
    - mp4v codec: En uyumlu, hızlı
    - H264: Yüksek kalite, yavaş işleme
    - XVID: Küçük dosya boyutu

Legal Notice:
    Bu yazılım "olduğu gibi" sağlanır. Kullanım riski kullanıcıya aittir.
    Video telif haklarına saygı gösterilmesi kullanıcının sorumluluğundadır.
===========================================================
"""

__version__ = "1.0.1"
__author__ = "mefamex"
__email__ = "info@mefaex.com"
__license__ = "MIT"
__status__ = "DEVELOPMENT"

__project_name__ = "Video Resizer Tool"
__url__ = "https://mefamex.com"
__url_github__ = "https://github.com/Mefamex/python-code-snippets"
__copyright__ = "2025 Mefamex"
__description__ = "OpenCV tabanlı video boyutlandırma ve format dönüştürme aracı"
__date__ = "2025-01-01"
__date_modify__ = "2025-08-11"
__python_version__ = "3.8+" 
__dependencies__ = {
    "opencv-python": ">=4.5.0",
    "pathlib": "built-in",
    "argparse": "built-in",
    "typing": "built-in"
}


#================================================================================


############### IMPORTS and CONFIG ####################


import os, sys, subprocess 
from time import sleep
from typing import Optional
from pathlib import Path

# check
try : import argparse 
except : subprocess.call(['python.exe','-m',"pip","install","-U","argparse"], text=True,encoding='utf-8')
try : import cv2 
except : subprocess.call(['python.exe','-m',"pip","install","-U","opencv-python"], text=True,encoding='utf-8')
try : import numpy 
except : subprocess.call(['python.exe','-m',"pip","install","-U","numpy"], text=True,encoding='utf-8')
#import
import argparse, cv2


DEF_CODEC : str = 'mp4v'
DEF_FPS   : float = 30.0
DEF_HEIGHT: int = 720
DEF_CODECS: list[str] = ['mp4v', 'XVID', 'H264', 'MJPG', 'X264', 'DIVX', 'VP80', 'VP90', 'HEVC', 'AV01']
DEF_EXTENSIONS: list[str] = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v', '3gp', 'asf', 'mpg', 'mpeg', 'mp2', 'mts', 'm2ts', 'ts', 'vob', 'ogv', 'dv', 'rm', 'rmvb']

# Codec açıklamaları ve önerileri
CODEC_INFO: dict[str, str] = {
    'mp4v': 'En uyumlu, orta kalite, orta dosya boyutu',
    'XVID': 'Eski cihazlarla uyumlu, iyi sıkıştırma',
    'H264': 'Modern standart, yüksek kalite (OpenH264 dll gerekli)',
    'MJPG': 'En güvenli, düşük sıkıştırma, büyük dosya',
    'X264': 'H264 alternatifi, iyi kalite',
    'DIVX': 'XVID benzeri, popüler codec',
    'VP80': 'Google VP8, açık kaynak',
    'VP90': 'Google VP9, VP8\'den daha iyi',
    'HEVC': 'H265, en iyi sıkıştırma, yeni cihazlar',
    'AV01': 'AV1, gelecek nesil, en iyi sıkıştırma'
}

# Uzantı açıklamaları
DEF_EXTENSIONS_INFO: dict[str, str] = {
    'mp4':  " En yaygın",
    'avi':  " Eski standart",
    'mkv':  " Matroska, açık kaynak",
    'mov':  " Apple QuickTime",
    'wmv':  " Windows Media",
    'flv':  " Flash Video",
    'webm': " Web video",
    'm4v':  " iTunes video",
    '3gp':  " Mobil video",
    'asf':  " Windows Media",
    'mpg':  " MPEG-1/2",
    'mpeg': " MPEG uzun form",
    'mp2':  " MPEG-2",
    'mts':  " AVCHD",
    'm2ts': " Blu-ray",
    'ts':   " Transport Stream",
    'vob':  " DVD video",
    'ogv':  " Ogg video",
    'dv':   " Digital Video",
    'rm':   " RealMedia",
    'rmvb': " RealMedia Variable Bitrate"
}

# Kalite/boyut önerileri
QUALITY_PRESETS: dict[str, dict] = {
    'web': {'codec': 'H264', 'height': 720, 'fps': 30},
    'mobile': {'codec': 'H264', 'height': 480, 'fps': 24},
    'hd': {'codec': 'H264', 'height': 1080, 'fps': 30},
    'small': {'codec': 'XVID', 'height': 480, 'fps': 24},
    'compatible': {'codec': 'mp4v', 'height': 720, 'fps': 30},
    'archive': {'codec': 'HEVC', 'height': 1080, 'fps': 30},
}

def flat_dict(d:dict, title=""):
    r, max_key_length = (f"{title}:\n" if title else ""), max(len(key) for key in d.keys())
    for key, value in d.items():  r += f"    - {key.rjust(max_key_length)}: {value}\n"
    return(r)

############### resize CLASS  ####################

class Resize:
    def __init__(self, input_file, height: Optional[int] = DEF_HEIGHT, fps: float = DEF_FPS, codec: str = DEF_CODEC):
        self.input_file: Path = Path.absolute(Path(input_file))
        self.clip: cv2.VideoCapture
        if not self.open_file(): return
        
        self.height: int = height if height else 720
        if fps is None: fps = self.clip.get(cv2.CAP_PROP_FPS)
        self.fps: float = fps
        self.codec: str = codec if codec else DEF_CODEC  # H264, mp4v, XVID, MJPG
        self.input_name: str = self.input_file.stem
        self.output_file: Path = self.input_file.parent / f"{self.input_name}_resized_{self.height}_{self.fps}fps_.mp4"
        self.output_name: str = self.output_file.stem
        self.bilgi_yazdir()
        sleep(3)
        
        if not self.resize_save(): return
        try: self.clip.release()
        except : pass

    def bilgi_yazdir(self): print(f"\nResizing video: {self.input_name}\n         path : {self.input_file}\n\n  output name : {self.output_name}\n  output path : {self.output_file}\n\n       height : {self.height}px <- {self.clip.get(cv2.CAP_PROP_FRAME_HEIGHT)} x {self.clip.get(cv2.CAP_PROP_FRAME_WIDTH)} px\n          fps : {self.fps} <- {self.clip.get(cv2.CAP_PROP_FPS)}\n        codec : {"".join([chr((int(self.clip.get(cv2.CAP_PROP_FOURCC)) >> 8 * i) & 0xFF) for i in range(4)])}\n")

    def open_file(self) -> bool:
        print("\nDOSYA AÇILIYOR")
        try:
            self.clip = cv2.VideoCapture(str(self.input_file))
        except Exception as e:
            print("\n"+str(e))
            print("\n HATA OLUŞTU DOSYA KAPATILIYOR")
            self.clip.release()
            return False
        sleep(1)
        return True

    def resize_save(self) -> bool:
        print("BOYUTLANDIRILIYOR")
        try:
            new_width : int = int(self.height * self.clip.get(cv2.CAP_PROP_FRAME_WIDTH) / self.clip.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(str(self.output_file), cv2.VideoWriter.fourcc(*self.codec), self.fps, (new_width, self.height))
            corrupted_frames, successful_frames, last_good_frame = 0, 0, None
            while True:
                frame_idx,total_frames  = int(self.clip.get(cv2.CAP_PROP_POS_FRAMES)), int(self.clip.get(cv2.CAP_PROP_FRAME_COUNT))+1
                if frame_idx % 50 == 0 or frame_idx == total_frames:  print(f"\rİlerleme: {(frame_idx/total_frames)*100:.2f}% - Bozuk frame: {corrupted_frames}", end="")
                ret, frame = self.clip.read()
                if not ret: break 
                # Frame Kontrolü
                if frame is None or frame.size == 0:
                    print(f"\nBozuk frame tespit edildi: {frame_idx}")
                    corrupted_frames += 1
                    if last_good_frame is not None: frame = last_good_frame.copy()
                    else: continue
                try:
                    if frame.shape[0] == 0 or frame.shape[1] == 0:
                        print(f"\nGeçersiz frame boyutu: {frame_idx}")
                        corrupted_frames += 1
                        if last_good_frame is not None:  frame = last_good_frame.copy()
                        else:  continue
                    resized_frame = cv2.resize(frame, (new_width, self.height))
                    if resized_frame is None or resized_frame.size == 0:
                        print(f"\nResize hatası: {frame_idx}")
                        corrupted_frames += 1
                        continue
                    out.write(resized_frame)
                    successful_frames += 1
                    last_good_frame = frame  # Geçerli frame'i sakla
                except Exception as e:
                    print(f"\nFrame işleme hatası {frame_idx}: {str(e)}")
                    corrupted_frames += 1
                    continue
            # Temizlik
            self.clip.release()
            out.release()
            cv2.destroyAllWindows()
            # Özet rapor
            print(f"\n{'='*50}")
            print(f"DÖNÜŞÜM TAMAMLANDI")
            print(f"Başarılı frame'ler: {successful_frames}")
            print(f"Bozuk frame'ler: {corrupted_frames}")
            print(f"Başarı oranı: %{(successful_frames/(successful_frames+corrupted_frames))*100:.1f}")
            print(f"{'='*50}")
            return True
        except Exception as e:
            print('\nDÖNÜŞTÜRME HATASI\n'+str(e))
            return False

def get_user_input():
    """Kullanıcıdan video dönüştürme parametrelerini al"""
    for q in bilgilendirme.split("\n"):
        print(q)
        sleep(0.05)
    sleep(1)
    print("\n" + "="*50 + "🎬 VIDEO DÖNÜŞTÜRÜCÜ"+ "="*50+ "\n\n")
    video_files = []
    while True:
        path = input("MEVCUT KLASÖR: "+os.getcwd()+" <- (enter)"+"\n📁 Video dosyası veya klasör yolu: ").strip() 
        if path in ["\n", ""]: path = os.getcwd()
        if not Path(path).exists(): print(f"❌ Yol bulunamadı: {path}")
        path = Path(path)
        if path.is_file(): break
        elif path.is_dir():
            video_files = [Path(path) / q for q in os.listdir(path) if q.lower().endswith(tuple(DEF_EXTENSIONS))]
            if video_files: break
            print("❌ Klasörde video dosyası bulunamadı!")
        else: print("❌ Geçersiz yol!")
    print(f"\n🎬 Seçilen dizin   : {path}")
    if video_files: print(f"🎬 Seçilen videolar: {len(video_files)} adet "+ "\n    - ".join(str(f) for f in video_files))
    # HEIGHT
    height = None
    while True:
        height, height_input = DEF_HEIGHT, input("\n📏 Hedef yükseklik (varsayılan: 720 , tavsiye: 1080): ").strip()
        if not height_input: break
        try:
            height = int(height_input)
            if height > 240 and height < 4320: break
            print("❌ Yükseklik 240-4320 arasında olmalı!")
        except ValueError: print("❌ Geçersiz sayı!")
    print(f"\n📏 Hedef yükseklik: {height} px (varsayılan: {DEF_HEIGHT})")
    # FPS
    fps = DEF_FPS
    while True:
        fps_input = input(f"\n⚡ FPS (varsayılan: {DEF_FPS}): ").strip()
        if fps_input:
            try:
                fps_input = float(fps_input)
                if not (1 <= fps_input <= 120): 
                    print(f"❌ FPS 1-120 arasında olmalı! (varsayılan: {DEF_FPS} -> enter)")
                    continue
                fps = fps_input
                break
            except ValueError:  print("❌ Geçersiz sayı!"); fps_input = None
        else: break
    print(f"\n⚡ Hedef FPS: {fps} (varsayılan: {DEF_FPS})")
    # CODEC
    codec = ""
    print(f"\n🎥 Codec seçenekleri: {', '.join(DEF_CODECS)}\n{flat_dict(CODEC_INFO)}\n")
    while codec not in DEF_CODECS or not codec:
        codec = input("\n🎥 Codec (varsayılan: mp4v -> enter): ").strip()
        if codec in ["\n", ""]: codec = DEF_CODEC
        if codec not in DEF_CODECS: print(f"❌ Geçersiz codec! Seçenekler: {', '.join(DEF_CODECS)}")
        else: break
        print(f"\n🎥 Hedef codec: {codec} (varsayılan: {DEF_CODEC})")
    return str(path), height, fps, codec


bilgilendirme = f"""
Örnekler:
    video.mp4                          # Varsayilan ayarlarla
    video.mp4 -y 1080                  # 1080p'ye donustur
    Folder{os.sep}   -y 720 -f 24             # 720p, 24fps
    Folder{os.sep}   -y 480 -f 30 -c XVID     # 480p, 30fps, XVID codec

Boyut: -h
    360p  = 0.5x dosya boyutu
    480p  = 0.75x dosya boyutu  
    720p  = 1x dosya boyutu   (varsayilan)
    1080p = 2x dosya boyutu
    1440p = 5x dosya boyutu
    2160p = 10x dosya boyutu

fps: -f
    24    = 0.5x dosya boyutu
    30    = 1x dosya boyutu   (varsayilan)
    60    = 2x dosya boyutu
    120   = 4x dosya boyutu

codec: -c
{flat_dict(CODEC_INFO)}

format: -d
{flat_dict(DEF_EXTENSIONS_INFO)}

Oneriler: 
{flat_dict(QUALITY_PRESETS)}
        """





def main():
    # Komut satırı argümanları parse et
    parser = argparse.ArgumentParser(
        description='Video Dönüştürücü - Video dosyalarını yeniden boyutlandırır',
        usage='%(prog)s  <video_path(file or dir)> [options]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog= bilgilendirme + ""
    )
    
    parser.add_argument('path', nargs='?', help='Video dosyası yolu')
    parser.add_argument('-y', '--height', type=int, default=DEF_HEIGHT, 
                        help='Hedef yükseklik (varsayılan: {})'.format(DEF_HEIGHT))
    parser.add_argument('-f', '--fps', type=float, 
                        help='Hedef FPS (varsayılan: {})'.format(DEF_FPS))
    parser.add_argument('-c', '--codec', choices=DEF_CODECS, 
                        default=DEF_CODEC, help='Video codec (varsayılan: mp4v)')
    parser.add_argument('--help-me', action='store_true', help='Kullanıcıdan interaktif parametre al')
    
    args = parser.parse_args()
    if len(sys.argv) == 1 or '--help-me' in sys.argv:
        try:
            video_path, height, fps, codec = get_user_input()
            args.path = video_path
            args.height = height
            args.fps = fps
            args.codec = codec
            Resize(video_path, height=height, fps=fps, codec=codec)
        except KeyboardInterrupt:
            print("\n\n❌ İşlem kullanıcı tarafından iptal edildi.")
            sys.exit(1)
    
    if not args.path:
        print("❌ Video dosyası yolu belirtilmedi!")
        print("Mevcut Klasör dizin olarak belirlendi: {}".format(os.getcwd()))
        args.path = os.getcwd()

    # Dosya kontrolü
    video_path = Path(args.path)
    if not video_path.is_file() and not video_path.is_dir():
        print(f"❌ Dosya veya klasör bulunamadı: {video_path}")
        sys.exit(1)
    if video_path.is_file():
        print(f"🚀 Dönüştürme başlatılıyor...")
        print(f"📁 Dosya: {args.path}")
        print(f"📏 Yükseklik: {args.height}px")
        print(f"⚡ FPS: {args.fps if args.fps else 'orijinal'}")
        print(f"🎥 Codec: {args.codec}")
        Resize(args.path, height=args.height, fps=args.fps, codec=args.codec)
    if video_path.is_dir():
        video_files = [video_file for video_file in video_path.glob("*") if video_file.suffix.lower().lstrip('.') in [ext.lower() for ext in DEF_EXTENSIONS]]
        print(f"📁 Klasör   :{len(video_files)} adet ->  {args.path}")
        print(f"📏 Yükseklik: {args.height}px")
        print(f"⚡       FPS: {args.fps if args.fps else 'orijinal'}")
        print(f"🎥    Codec: {args.codec}\n")
        print(f"🚀 Dönüştürme başlatılıyor...")
        sleep(5)
        for video_file in video_files:
            print(f"\n📁 Dosya : {video_files.index(video_file)+1}/{len(video_files)} {video_file}")
            Resize(video_file, height=args.height, fps=args.fps, codec=args.codec)


#import subprocess; subprocess.run(['ffmpeg', '-i', 'a.mp4', '-vf', 'scale=-1:1080', 'movie_resized.mp4'])
if __name__ == "__main__":
    main()