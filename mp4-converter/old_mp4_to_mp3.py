# -*- coding: utf-8 -*-

# Bu dosya eski moviepy tabanlı MP4 to MP3 dönüştürücüdür
# Ana proje artık video boyutlandırma odaklıdır
# Ses çıkarma için ayrı bir araç olarak kullanılabilir

from pathlib import Path

try:
    from moviepy import VideoFileClip
except ImportError:
    print("❌ MoviePy kütüphanesi bulunamadı!")
    print("Kurulum için: pip install moviepy")
    exit(1)

def mp4_to_mp3(input_file: str, output_file: str | None = None) -> bool:
    """MP4 dosyasını MP3 formatına dönüştürür."""
    
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Hata: '{input_file}' dosyası bulunamadı!")
        return False
    
    if not input_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        print(f"❌ Desteklenmeyen dosya formatı: {input_path.suffix}")
        return False
    
    output_file = output_file or str(input_path.with_suffix('.mp3'))
    
    try:
        print(f"🔄 Dönüştürme başlatılıyor: {input_file} -> {output_file}")
        
        with VideoFileClip(input_file) as video:
            if not video.audio: 
                print("❌ Hata: Video dosyasında ses bulunamadı!")
                return False
            else: video.audio.write_audiofile(output_file, verbose=False, logger=None)
        print(f"✅ Dönüştürme tamamlandı: {output_file}")
        
        # Dosya boyutu bilgisi
        if Path(output_file).exists():
            size_mb = Path(output_file).stat().st_size / (1024 * 1024)
            print(f"📏 Çıktı dosya boyutu: {size_mb:.2f} MB")
        return True
    except Exception as e:
        print(f"❌ Dönüştürme hatası: {e}")
        return False

if __name__ == "__main__":
    video_file = input("MP4 dosya yolu: ").strip().strip('"')
    if video_file: mp4_to_mp3(video_file)