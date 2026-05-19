# -*- coding: utf-8 -*- 

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
    - Python 3.9+
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
__email__ = "info@mefamex.com"
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


import io, os, sys, subprocess 
from time import sleep
from pathlib import Path
from resize import Resize

try: sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except (ValueError, AttributeError): pass


# check
try : import argparse 
except : subprocess.call(['python.exe','-m',"pip","install","-U","argparse"], text=True,encoding='utf-8')
import argparse


DEF_CODECS: list[str] = ['mp4v', 'XVID', 'H264', 'MJPG', 'X264', 'DIVX', 'VP80', 'VP90', 'HEVC', 'AV01']
DEF_EXTENSIONS: list[str] = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v', '3gp', 'asf', 'mpg', 'mpeg', 'mp2', 'mts', 'm2ts', 'ts', 'vob', 'ogv', 'dv', 'rm', 'rmvb']

# Codec açıklamaları ve önerileri
CODEC_INFO: dict[str, str] = {
    'mp4v': 'En uyumlu, orta kalite, orta dosya boyutu',
    'XVID': 'Eski cihazlarla uyumlu, iyi sıkıştırma',
    'H264': 'Modern standart, yüksek kalite (mükemmel uyumluluk)',
    'MJPG': 'En güvenli, düşük sıkıştırma, büyük dosya',
    'X264': 'H264 alternatifi, iyi kalite',
    'DIVX': 'XVID benzeri, popüler codec',
    'VP80': 'Google VP8, açık kaynak',
    'VP90': 'Google VP9, VP8\'den daha iyi',
    'HEVC': 'H265, en iyi sıkıştırma, yeni cihazlar',
    'AV01': 'AV1, gelecek nesil, en iyi sıkıştırma',
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
    for key, value in d.items():  r += f"    {key.rjust(max_key_length)} : {value}\n"
    return(r)

############### resize CLASS  ####################
DEF_CODEC : str = 'mp4v'
DEF_FPS   : float = 30.0
DEF_HEIGHT: int = 1080


def get_user_input():
    """Kullanıcıdan video dönüştürme parametrelerini al"""
    for q in bilgilendirme.split("\n"):
        print(q,flush=True )
        sleep(0.03)
    sleep(1)
    print("\n" + "="*50 + "🎬 VIDEO DÖNÜŞTÜRÜCÜ"+ "="*50+ "\n\n")
    video_files = []
    while True:
        path = input("MEVCUT KLASÖR: "+os.getcwd()+" <- (enter)"+"\n📁 Video dosyası veya klasör yolu: ").strip().removeprefix('\t').removesuffix('\t').removeprefix('\n').removesuffix('\n').removeprefix('"').removesuffix('"').removeprefix('\'').removesuffix('\'')
        if path in ["\n", ""]: path = os.getcwd()
        path = Path(path.strip('\'"')).resolve()
        if not Path(path).exists(): print(f"❌ Yol bulunamadı: {path}")
        if path.is_file(): break
        elif path.is_dir():
            video_files = [Path(path) / q for q in os.listdir(path) if q.lower().endswith(tuple(DEF_EXTENSIONS))]
            if video_files: break
            print("❌ Klasörde video dosyası bulunamadı!")
        else: print("❌ Geçersiz yol!  üst dizini: ", path.parent)
    print(f"\n🎬 Seçilen dizin   : {path}")
    if video_files: print(f"🎬 Seçilen videolar: {len(video_files)} adet "+ "\n    - ".join(str(f) for f in video_files))
    # HEIGHT
    height = None
    while True:
        height, height_input = DEF_HEIGHT, input(f"\n📏 Hedef yükseklik (varsayılan: {DEF_HEIGHT}): ").strip()
        if not height_input: break
        try:
            height = int(height_input)
            if height > 240 and height < 4320: break
            print("❌ Yükseklik 240-4320 arasında olmalı!")
        except ValueError: print("❌ Geçersiz sayı!")
    print(f"📏 Hedef yükseklik: {height} px (varsayılan: {DEF_HEIGHT})")
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
    print(f"⚡ Hedef FPS: {fps} (varsayılan: {DEF_FPS})")
    # CODEC
    codec = ""
    print(f"\n🎥 Codec seçenekleri: {', '.join(DEF_CODECS)}\n{flat_dict(CODEC_INFO)}")
    while codec not in DEF_CODECS or not codec:
        codec = input("🎥 Codec (varsayılan: mp4v -> enter): ").strip()
        if codec in ["\n", ""]: codec = DEF_CODEC
        if codec not in DEF_CODECS: print(f"❌ Geçersiz codec! Seçenekler: {', '.join(DEF_CODECS)}")
        else: break
        print(f"\n🎥 Hedef codec: {codec} (varsayılan: {DEF_CODEC})")
    return str(path), height, fps, codec


bilgilendirme = f"""

Boyut: -h
    360p  = 0.5x dosya boyutu  {"varsayilan" if DEF_HEIGHT == 360 else ""}
    480p  = 0.75x dosya boyutu {"varsayilan" if DEF_HEIGHT == 480 else ""}
    720p  = 1x dosya boyutu    {"varsayilan" if DEF_HEIGHT == 720 else ""}
    1080p = 2x dosya boyutu    {"varsayilan" if DEF_HEIGHT == 1080 else ""}
    1440p = 5x dosya boyutu    {"varsayilan" if DEF_HEIGHT == 1440 else ""}
    2160p = 10x dosya boyutu   {"varsayilan" if DEF_HEIGHT == 2160 else ""}

fps: -f
    24    = 0.5x dosya boyutu {"varsayilan" if DEF_FPS == 24 else ""}
    30    = 1x dosya boyutu   {"varsayilan" if DEF_FPS == 30 else ""}
    60    = 2x dosya boyutu   {"varsayilan" if DEF_FPS == 60 else ""}
    120   = 4x dosya boyutu   {"varsayilan" if DEF_FPS == 120 else ""}

codec: -c
{flat_dict(CODEC_INFO)}

format: -d
{flat_dict(DEF_EXTENSIONS_INFO)}

Oneriler: 
{flat_dict(QUALITY_PRESETS)}

Örnekler:
    path or file  -y <yükseklik>  -f <fps>  -c <codec>
    video.mp4                          # Varsayilan ayarlarla
    video.mp4 -y 1080                  # 1080p'ye donustur
    Folder{os.sep}   -y 720 -f 24             # 720p, 24fps
    Folder{os.sep}   -y 480 -f 30 -c XVID     # 480p, 30fps, XVID codec

"""





def main():
    # PyInstaller'da stdout problemi için güvenli print
    try: print(f"Python yolu : {sys.executable} \nMevcut dizin: {os.getcwd()}\n\n")
    except: pass
    
    # OpenH264 setup'ını PyInstaller'da atla
    if not getattr(sys, 'frozen', False):
        try: 
            import openH264_setup
            openH264_setup.main()
        except Exception as e:
            try: print(f"⚠️ OpenH264 setup atlandı: {e}")
            except: pass
    else:
        try: print("📦 EXE modunda çalışıyor, OpenH264 setup atlandı")
        except: pass
    
    sleep(1)
    # Komut satırı argümanları parse et
    parser = argparse.ArgumentParser(
        description='Video Dönüştürücü - Video dosyalarını yeniden boyutlandırır',
        usage='%(prog)s  <video_path(file or dir)> [-y <height>] [-f <fps>] [-c <codec>]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog= bilgilendirme + ""
        )
    
    parser.add_argument('path', nargs='?', help='Video dosyası yolu')
    parser.add_argument('-y', '--height', type=int, default=DEF_HEIGHT, help='Hedef yükseklik (varsayılan: {})'.format(DEF_HEIGHT))
    parser.add_argument('-f', '--fps', type=float,  help='Hedef FPS (varsayılan: {})'.format(DEF_FPS))
    parser.add_argument('-c', '--codec', choices=DEF_CODECS,  default=DEF_CODEC, help='Video codec (varsayılan: mp4v)')
    parser.add_argument('--help-me', action='store_true', help='Kullanıcıdan interaktif parametre al')
    # PyInstaller uyumluluğu için özel version handler
    parser.add_argument('--version', action='store_true', help='Versiyon bilgisini göster')
    
    # Önce argümanları parse et ve version kontrolü yap
    try:
        args = parser.parse_args()
        if args.version:
            print(f'{__project_name__} v{__version__} by {__author__}')
            sys.exit(0)
    except SystemExit as e: sys.exit(e.code)
    try:
        if len(sys.argv) == 1 or '--help-me' in sys.argv:
            try:
                video_path, height, fps, codec = get_user_input()
                args.path = Path(video_path.strip('\'"')).resolve()
                args.height = height
                args.fps = fps
                args.codec = codec
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
            print(f"🚀 Başlatılıyor...")
            print(f"📁 Dosya    : {args.path}")
            print(f"📏 Yükseklik: {args.height}px")
            print(f"⚡ FPS      : {args.fps if args.fps else DEF_FPS}")
            print(f"🎥 Codec    : {args.codec}")
            Resize(args.path, height=args.height, fps=args.fps, codec=args.codec)
        if video_path.is_dir():
            print(f"🚀 Başlatılıyor...")
            video_files = [video_file for video_file in video_path.glob("*") if video_file.suffix.lower().lstrip('.') in [ext.lower() for ext in DEF_EXTENSIONS]]
            print(f"📁 Klasör   : {len(video_files)} adet ->  {args.path}")
            print(f"📏 Yükseklik: {args.height}px")
            print(f"⚡ FPS      : {args.fps if args.fps else DEF_FPS}")
            print(f"🎥 Codec    : {args.codec}\n")
            sleep(5)
            for video_file in video_files:
                print(f"\n📁 Dosya : {video_files.index(video_file)+1}/{len(video_files)} {video_file}")
                Resize(video_file, height=args.height, fps=args.fps, codec=args.codec)
    except Exception as e:
        print(f"\n\n❌ Hata oluştu: {e}")
        sleep(1000)
        sys.exit(1)
    sleep(1)
    # Kullanıcıdan "r" tuşuna basmasını iste, "r" ise yeniden başlat, değilse çık
    cevap = input("Yeniden başlatmak için 'r' tuşuna basın, çıkmak için herhangi bir tuşa basın...").strip().lower()
    if cevap == "r":
        if getattr(sys, 'frozen', False): os.execv(sys.executable, [sys.executable] + sys.argv[1:])
        else: os.execv(sys.executable, ['python'] + sys.argv)
    else:
        print("Program sonlandırıldı.")
        sys.exit(0)


#import subprocess; subprocess.run(['ffmpeg', '-i', 'a.mp4', '-vf', 'scale=-1:1080', 'movie_resized.mp4'])
if __name__ == "__main__":
    main()