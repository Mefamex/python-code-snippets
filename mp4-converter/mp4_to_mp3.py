import os
from moviepy import VideoFileClip

def mp4_to_mp3(input_file: str, output_file: str | None = None):
    """MP4 dosyasını MP3 formatına dönüştürür."""
    
    if not os.path.exists(input_file):
        print(f"Hata: '{input_file}' dosyası bulunamadı!")
        return False
    
    output_file = output_file or os.path.splitext(input_file)[0] + ".mp3"
    
    try:
        with VideoFileClip(input_file) as video:
            if not video.audio: 
                print("Hata: Video dosyasında ses bulunamadı!")
                return 
            else : video.audio.write_audiofile(output_file, verbose=False, logger=None)
        print(f"✅ Dönüştürme tamamlandı: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        



mp4_to_mp3("a.mp4")