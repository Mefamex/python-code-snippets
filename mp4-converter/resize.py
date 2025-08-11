# -*- coding: utf-8 -*- 

# created on : 2025-08-11
# updated on : 2025-08-11
# linked     :  
#       - github.com/Mefamex/python-code-snippets/mp4-converter
#       - mefamex.com/projects

"""_özet_
Belirtilen yüksekliğe göre MP4 videolarını yeniden boyutlandırmak için bir Python betiği/sınıfı.
Gerekirse FPS ve codec ayarlanabilir.
OpenCV kullanarak video karelerini okur, yeniden boyutlandırır ve kaydeder.
Bozuk kareleri sorunsuz şekilde işler, ilerleme ve özet çıktısı verir.
"""


import os, subprocess 
from time import sleep
from pathlib import Path

try : import cv2 
except : subprocess.call(['python.exe','-m',"pip","install","-U","opencv-python"], text=True,encoding='utf-8')
try : import numpy 
except : subprocess.call(['python.exe','-m',"pip","install","-U","numpy"], text=True,encoding='utf-8')
import cv2

#================================================================================



DEF_CODEC : str = 'mp4v'
DEF_FPS   : float = 30.0
DEF_HEIGHT: int = 720

class Resize:
    def __init__(self, input_file, height: int = DEF_HEIGHT, fps: float = DEF_FPS, codec: str = DEF_CODEC):
        try: 
            import openH264_setup
            openH264_setup.main()
        except: pass
        self.input_file: Path = Path.absolute(Path(str(input_file).strip('\'"')).resolve())
        self.clip: cv2.VideoCapture
        if not self._open_file(): return
        
        self.height: int = height
        if fps is None: fps = self.clip.get(cv2.CAP_PROP_FPS)
        self.fps: float = fps
        self.codec: str = codec if codec else DEF_CODEC  # H264, mp4v, XVID, MJPG
        self.input_name: str = self.input_file.stem
        self.output_file: Path = self.input_file.parent / f"{self.input_name}_{self.height}p_{self.fps}fps_{self.codec}_.{self.input_file.suffix}"
        self.output_name: str = self.output_file.stem
        self._bilgi_yazdir()
        sleep(3)

        if not self._resize_save(): return
        try: self.clip.release()
        except : pass
        

    def _bilgi_yazdir(self): 
        print(f"Resizing video: {self.input_name}")
        print(f"         path : {self.input_file}")
        print(f"  output name : {self.output_name}")
        print(f"  output path : {self.output_file}")
        print(f"       height : {self.height}p <- {self.clip.get(cv2.CAP_PROP_FRAME_HEIGHT)} x {self.clip.get(cv2.CAP_PROP_FRAME_WIDTH)} px")
        print(f"          fps : {self.fps} <- {self.clip.get(cv2.CAP_PROP_FPS)}")
        print(f"        codec : {"".join([chr((int(self.clip.get(cv2.CAP_PROP_FOURCC)) >> 8 * i) & 0xFF) for i in range(4)])}")

    def _open_file(self) -> bool:
        try:
            if not self.input_file.exists():
                print(f"❌ Dosya bulunamadı: {self.input_file}")
                return False
            
            self.clip = cv2.VideoCapture(str(self.input_file))
            
            if not self.clip.isOpened():
                print(f"❌ Dosya açılamadı: {self.input_file}")
                return False
                
        except Exception as e:
            print(f"❌ Dosya açma hatası: {e}")
            try:
                self.clip.release()
            except:
                pass
            return False
        sleep(1)
        return True

    def _resize_save(self) -> bool:
        try:
            new_width : int = int(self.height * self.clip.get(cv2.CAP_PROP_FRAME_WIDTH) / self.clip.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(str(self.output_file), cv2.VideoWriter.fourcc(*self.codec), self.fps, (new_width, self.height))
            corrupted_frames, successful_frames, last_good_frame = 0, 0, None
            while True:
                frame_idx,total_frames  = int(self.clip.get(cv2.CAP_PROP_POS_FRAMES)), int(self.clip.get(cv2.CAP_PROP_FRAME_COUNT))+1
                if frame_idx % 30 == 0 or frame_idx == total_frames:  
                    boyut = None
                    try: boyut = self.output_file.stat().st_size/(1024*1024)
                    except: pass
                    print(f'\rİlerleme: {(frame_idx/total_frames)*100:.2f}% - Bozuk frame: {corrupted_frames}  |  '+ f'{boyut:.2f} MB' if boyut else "", end="")
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
            print(f"\r{'='*50}")
            print(f"DÖNÜŞÜM TAMAMLANDI")
            print(f"Başarılı frame'ler: {successful_frames}")
            print(f"Bozuk frame'ler: {corrupted_frames}")
            print(f"Başarı oranı: %{(successful_frames/(successful_frames+corrupted_frames))*100:.1f}")
            input_size, output_size = None, None
            if self.output_file.exists(): output_size = self.output_file.stat().st_size
            if self.input_file.exists(): input_size = self.input_file.stat().st_size
            if input_size is not None and output_size is not None:  print(f"🎬 {input_size / (1024*1024):.2f} MB -> {output_size / (1024*1024):.2f} MB  |  {((output_size - input_size) / input_size * 100) if input_size else 0:.2f}%")
            print(f"{'='*50}")
            return True
        except Exception as e:
            print('\nDÖNÜŞTÜRME HATASI\n'+str(e))
            return False


if __name__ == "__main__":
    file_list = []
    for q in os.listdir(os.getcwd()):
        try:
            clip = cv2.VideoCapture(str(Path(q)))
            if clip.isOpened(): file_list.append(q)
        except Exception as e:pass

    for video_file in file_list:
        print(f"\n\n\n")
        Resize(Path(video_file))
