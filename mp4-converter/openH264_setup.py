# -*- coding: utf-8 -*-

# created on : 2025-08-11
# updated on : 2025-08-11
# linked     :  
#       - github.com/Mefamex/python-code-snippets/mp4-converter
#       - mefamex.com/projects
"""
OpenH264 DLL dosyasını bulur, gerekirse kurar ve H264 codec desteğini kontrol eder.

Bu modül, OpenCV ile H264 video kodlaması için gerekli olan openh264*.dll dosyasının sistemde bulunup bulunmadığını denetler.

Eğer DLL bulunamazsa, otomatik olarak indirilen veya mevcut olan .bz2 arşivinden çıkartıp Python dizinine kopyalar.

Ayrıca, H264 codec'in kullanılabilirliğini test eder ve eksikse kullanıcıyı bilgilendirir.
"""

import os, sys, bz2, shutil
import urllib.request
from pathlib import Path
from typing import Optional

try: import cv2
except ImportError:
    print("❌ OpenCV kütüphanesi bulunamadı! pip install opencv-python")
    cv2 = None

# OpenCV'nin desteklediği OpenH264 versiyonları
COMPATIBLE_VERSIONS = [ "1.8.0", "2.1.1",  "2.3.1", "2.4.1" ]

def get_opencv_expected_version() -> str:
    """OpenCV'nin beklediği OpenH264 versiyonunu döndürür"""
    if not cv2:  return "1.8.0" 
    
    opencv_version = cv2.__version__
    # OpenCV versiyonuna göre uyumlu OpenH264 versiyonu
    if opencv_version.startswith("4.8") or opencv_version.startswith("4.9"):  return "2.3.1"
    elif opencv_version.startswith("4.6") or opencv_version.startswith("4.7"): return "2.1.1"
    else: return "1.8.0"

def download_openh264_dll(version: str = "") -> Optional[Path]:
    """Belirtilen OpenH264 versiyonunu indirir"""
    if not version or version == "": version = get_opencv_expected_version()
    print(f"📥 OpenH264 v{version} indiriliyor...")
    url = f"https://github.com/cisco/openh264/releases/download/v{version}/openh264-{version}-win64.dll.bz2"
    
    try:
        # İndirme klasörünü script'in bulunduğu klasör olarak ayarla
        script_dir = Path(__file__).parent
        download_path = script_dir / f"openh264-{version}-win64.dll.bz2"
        
        print(f"🌐 URL: {url}")
        print(f"📁 Hedef: {download_path}")
        
        if download_path.exists():
            print(f"✅ Dosya zaten mevcut: {download_path.name}")
            return download_path
            
        print(f"🔄 İndiriliyor...")
        urllib.request.urlretrieve(url, download_path)
        print(f"✅ İndirme tamamlandı: {download_path.name}")
        return download_path
    except Exception as e:
        print(f"❌ İndirme hatası: {e}")
        print(f"⚠️  Ağ bağlantısı veya GitHub erişim sorunu olabilir")
        return None

def find_openh264_dll() -> Optional[Path]:
    """OpenH264 DLL dosyasını sistem genelinde arar"""
    print("🔍 OpenH264 DLL dosyası aranıyor...")
    patterns = ["openh264*.dll", "*openh264*.dll", "libopenh264*.dll"]
    search_paths = [
        Path("."),  # Mevcut dizin
        Path(".."), # Üst dizin
        Path.cwd(),  # Çalışma dizini
        Path(sys.executable).parent,  # Python dizini
        Path(sys.executable).parent / "DLLs",  # Python DLLs dizini
        Path(os.environ.get('CONDA_PREFIX', '')) if 'CONDA_PREFIX' in os.environ else Path(),  # Conda env
        Path.home() / "Downloads",  # İndirilenler
        Path.home() / "Desktop",  # Kullanıcının Masaüstü dizini
        Path("C:/Windows/System32") if os.name == 'nt' else Path("/usr/lib"),  # System32
        Path(os.getcwd()).parent,  # Üst dizin
        Path(__file__).parent,  # Bu dosyanın bulunduğu dizin
    ]
    
    # Geçerli paths filtrele
    valid_paths = [p for p in search_paths if p.exists()]
    for search_path in valid_paths:
        print(f"  📂 Aranan: {search_path}") 
        for pattern in patterns:
            try:
                dll_files = list(search_path.glob(pattern))
                if dll_files:
                    # Önce uyumlu versiyon ara
                    for dll_file in dll_files:
                        for version in COMPATIBLE_VERSIONS:
                            if version in dll_file.name:
                                print(f"✅ Uyumlu OpenH264 DLL bulundu: {dll_file}")
                                return dll_file
                    # Uyumlu versiyon yoksa, uyumlu olanı indirmeyi dene
                    latest_dll = sorted(dll_files, key=lambda x: x.name, reverse=True)[0]
                    print(f"⚠️  OpenH264 DLL bulundu ancak versiyon uyumsuz: {latest_dll.name}")
                    print(f"🔄 Uyumlu versiyon indiriliyor...")
                    expected_version = get_opencv_expected_version()
                    bz2_file = download_openh264_dll(expected_version)
                    if bz2_file:
                        compatible_dll = extract_bz2_file(bz2_file)
                        if compatible_dll:
                            print(f"✅ Uyumlu versiyon indirildi: {compatible_dll.name}")
                            return compatible_dll
                    # İndirme başarısızsa mevcut olanı döndür
                    print(f"⚠️  İndirme başarısız, mevcut versiyon kullanılacak: {latest_dll.name}")
                    return latest_dll
            except Exception as e:
                print(f"  ⚠️  Arama hatası {search_path}: {e}")
                continue
    print("❌ OpenH264 DLL dosyası bulunamadı!")
    return None

def find_openh264_dll_silent() -> Optional[Path]:
    """OpenH264 DLL dosyasını sessizce arar (emoji ve print yok)"""
    patterns = ["openh264*.dll", "*openh264*.dll", "libopenh264*.dll"]
    search_paths = [
        Path("."),  # Mevcut dizin
        Path(".."), # Üst dizin
        Path.cwd(),  # Çalışma dizini
        Path(sys.executable).parent,  # Python dizini
        Path(sys.executable).parent / "DLLs",  # Python DLLs dizini
        Path(os.environ.get('CONDA_PREFIX', '')) if 'CONDA_PREFIX' in os.environ else Path(),  # Conda env
        Path.home() / "Downloads",  # İndirilenler
        Path.home() / "Desktop",  # Kullanıcının Masaüstü dizini
        Path("C:/Windows/System32") if os.name == 'nt' else Path("/usr/lib"),  # System32
        Path(os.getcwd()).parent,  # Üst dizin
        Path(__file__).parent,  # Bu dosyanın bulunduğu dizin
    ]
    
    # Geçerli paths filtrele
    valid_paths = [p for p in search_paths if p.exists()]
    
    for search_path in valid_paths:
        for pattern in patterns:
            try:
                dll_files = list(search_path.glob(pattern))
                if dll_files:
                    # Önce uyumlu versiyon ara
                    for dll_file in dll_files:
                        for version in COMPATIBLE_VERSIONS:
                            if version in dll_file.name:  return dll_file
                    latest_dll = sorted(dll_files, key=lambda x: x.name, reverse=True)[0]
                    return latest_dll
            except Exception:
                continue
    return None

def extract_bz2_file(bz2_path: Path) -> Optional[Path]:
    """BZ2 dosyasını çıkartır"""
    try:
        print(f"📦 BZ2 dosyası çıkartılıyor: {bz2_path.name}")
        extracted_name = bz2_path.name.replace('.bz2', '')
        extracted_path = bz2_path.parent / extracted_name
        if extracted_path.exists():
            print(f"✅ Dosya zaten var: {extracted_path}")
            return extracted_path
        with bz2.BZ2File(bz2_path, 'rb') as source:
            with open(extracted_path, 'wb') as target: shutil.copyfileobj(source, target)
        print(f"✅ BZ2 dosyası çıkartıldı: {extracted_path.name}")
        return extracted_path
    except Exception as e:
        print(f"❌ BZ2 çıkartma hatası: {e}")
        return None

def install_openh264_dll() -> bool:
    """OpenH264 DLL'ini bulur ve Python dizinine kurar"""
    try:
        # Önce mevcut DLL'i ara
        dll_file = find_openh264_dll()
        # Bulunamazsa uyumlu versiyonu indir
        if not dll_file:
            print("💾 Uyumlu OpenH264 versiyonu indiriliyor...")
            expected_version = get_opencv_expected_version()
            bz2_file = download_openh264_dll(expected_version)
            if bz2_file: dll_file = extract_bz2_file(bz2_file)
            if not dll_file:
                print("⚠️  OpenH264 DLL bulunamadı veya indirilemedi. H264 codec kullanılamayabilir.")
                return False
        
        # BZ2 dosyasıysa çıkart
        if dll_file.suffix.lower() == '.bz2':
            dll_file = extract_bz2_file(dll_file)
            if not dll_file:return False
        
        # DLL dosyasının varlığını kontrol et
        if not dll_file.exists():
            print(f"❌ DLL dosyası mevcut değil: {dll_file}")
            return False
        
        # Python dizinine kopyala - DÜZELTME: .parent eklendi
        python_dir = Path(sys.executable).parent
        target_path = python_dir / dll_file.name
        
        print(f"📍 Kaynak DLL: {dll_file}")
        print(f"📍 Hedef dizin: {python_dir}")
        print(f"📍 Hedef dosya: {target_path}")
        
        # Zaten varsa kontrol et
        if target_path.exists():
            print(f"✅ OpenH264 DLL zaten kurulu: {target_path.name}")
            return True
        try:
            # Kopyala
            shutil.copy2(dll_file, target_path)
            print(f"✅ OpenH264 DLL kuruldu: {target_path}")
            if target_path.exists(): print(f"📏 Kopyalanan dosya boyutu: {target_path.stat().st_size} bytes")
        except PermissionError:
            print(f"⚠️  Python dizinine kopyalama yetkisi yok: {python_dir}")
            print(f"📋 Alternatif olarak DLL bulunuyor: {dll_file}")
            
            # Yerel klasöre kopyala
            local_target = Path(__file__).parent / dll_file.name
            if not local_target.exists():
                try:
                    shutil.copy2(dll_file, local_target)
                    print(f"✅ DLL yerel klasöre kopyalandı: {local_target}")
                except Exception as e:
                    print(f"❌ Yerel kopyalama da başarısız: {e}")
            return True  # DLL mevcut, sadece kopyalama sorunu
        except Exception as e:
            print(f"❌ Kopyalama hatası: {e}")
            return False
        
        # Ayrıca OpenCV'nin beklediği isimle de kopyala
        expected_version = get_opencv_expected_version()
        expected_name = f"openh264-{expected_version}-win64.dll"
        expected_path = python_dir / expected_name
        
        if not expected_path.exists() and expected_name != dll_file.name:
            try:
                shutil.copy2(dll_file, expected_path)
                print(f"✅ OpenH264 DLL uyumlu isimle de kopyalandı: {expected_name}")
            except PermissionError: print(f"⚠️  Uyumlu isimle kopyalama yetkisi yok, mevcut versiyon kullanılacak")
            except Exception as e: print(f"⚠️  Uyumlu isim kopyalama hatası: {e}")
        return True
        
    except PermissionError:
        print("❌ Yetki hatası! Administrator yetkisiyle çalıştırın.")
        return False
    except Exception as e:
        print(f"❌ OpenH264 DLL kurulum hatası: {e}")
        print(f"🔧 Hata türü: {type(e).__name__}")
        return False




def check_openh264() -> bool:
    """H264 codec desteğini test eder"""
    if not cv2:
        print("❌ OpenCV yüklü değil!")
        return False
    
    try:
        print(f"📋 OpenCV versiyonu: {cv2.__version__}")
        expected_version = get_opencv_expected_version()
        print(f"📋 Beklenen OpenH264 versiyonu: {expected_version}")
        fourcc = cv2.VideoWriter.fourcc(*'H264')
        import tempfile, os
        
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file: test_path = Path(temp_file.name)
            writer = cv2.VideoWriter(str(test_path), fourcc, 1.0, (100, 100))
            is_opened = writer.isOpened()
            if writer is not None: writer.release()
            try:
                if test_path.exists():
                    os.unlink(str(test_path))
            except (OSError, PermissionError):  pass
            if is_opened:
                print("✅ H264 codec kullanılabilir!")
                return True
            else:
                print("⚠️  H264 codec VideoWriter testi başarısız")
                return False
        except Exception as test_error:
            print(f"⚠️  H264 codec testi hatası: {test_error}")
            try:
                if 'test_path' in locals() and test_path.exists():  os.unlink(str(test_path))
            except: pass
            return False
    except Exception as e:
        print(f"⚠️  H264 codec genel hatası: {e}")
        return False




def fix_codec_compatibility():
    """Codec uyumluluk sorunlarını çözer"""
    print("🔧 Codec uyumluluk sorunu tespit edildi, düzeltiliyor...")
    python_dir = Path(sys.executable).parent
    existing_dlls = list(python_dir.glob("openh264*.dll"))
    
    if existing_dlls:
        print(f"📋 Mevcut DLL'ler: {[dll.name for dll in existing_dlls]}")
        expected_version = get_opencv_expected_version()
        print(f"💾 OpenCV uyumlu versiyon indiriliyor: v{expected_version}")
        bz2_file = download_openh264_dll(expected_version)
        if bz2_file:
            dll_file = extract_bz2_file(bz2_file)
            if dll_file:
                try:
                    target_path = python_dir / dll_file.name
                    shutil.copy2(dll_file, target_path)
                    print(f"✅ Uyumlu versiyon kuruldu: {dll_file.name}")
                    return True
                except PermissionError:
                    print(f"⚠️  Kurulum yetkisi yok, ancak uyumlu DLL indirildi: {dll_file}")
                    return True  # DLL var, sadece kopyalama sorunu
        else: print("⚠️  İndirme başarısız, mevcut DLL'ler kullanılacak")
    return False



def main() -> None:
    """Main function starts all"""
    print("🚀 OpenH264 kontrol ve kurulum başlatılıyor...\n")
    try:
        install_success = install_openh264_dll()
        if install_success:
            codec_success = check_openh264()
            if codec_success: print("\n🎉 OpenH264 kurulumu ve testi başarılı!")
            else:
                print("\n⚠️ H264 codec testi başarısız! Uyumluluk sorunu düzeltiliyor...")
                fix_success = fix_codec_compatibility()
                if fix_success:
                    final_test = check_openh264()
                    if final_test: print("\n🎉 Uyumluluk sorunu çözüldü!")
                    else: print("\n❌ Uyumluluk sorunu çözülemedi!")
                else: print("\n❌ Uyumluluk düzeltmesi başarısız!")
        else: print("\n❌ OpenH264 kurulumu başarısız!")
    except Exception as e:
        print(f"\n⚠️  OpenH264 setup hatası: {e}")


if __name__ == "__main__":
    main()