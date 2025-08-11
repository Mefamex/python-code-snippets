@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
REM Script dizinine geç
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Mevcut klasor: %CD%
echo.

echo ==================================================================
echo                     VIDEO RESIZER TOOL
echo                   Python to EXE Converter
echo ==================================================================
echo.
echo Bu tool main.py dosyasini tek exe dosyasina donusturur
echo Python olmayan bilgisayarlarda da calisabilir hale getirir
echo.
echo Gereksinimler:
echo - Python 3.8+ yüklü olmalı
echo - pip ile pyinstaller kurulu olmalı
echo.
echo Kullanım: toExe.bat dosyasına çift tıklayın
echo ==================================================================

title Video Resizer - Python to EXE Converter

REM Python kontrolü
echo [1/10] Python kontrolu yapiliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ HATA: Python bulunamadi! 
    echo    Python 3.9+ yuklu oldugundan emin olun
    echo    https://python.org adresinden indirebilirsiniz
    pause
    exit /b 1
)
python --version
echo ✅ Python bulundu
echo.
echo.
echo.
echo.
echo.

REM Virtual environment kontrolü
echo [2/10] Virtual environment kontrol ediliyor...
if exist ".venv\" (
    call .venv\Scripts\activate.bat >nul 2>&1
    echo Virtual environment aktif edildi
    python.exe -m pip -V 
    echo ✅ Virtual environment bulundu (.venv^)
) else (
    echo ⚠️  Virtual environment bulunamadi
    echo Sistem Python kullanilacak
)
echo.
echo.
echo.
echo.
echo.

REM Pip güncellemesi
echo.
echo [3/10] Pip guncelleniyor...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Pip guncellenemedi, mevcut surum kullanilacak
) else (
    echo ✅ Pip guncellendi
)
echo.
echo.
echo.
echo.
echo.

REM PyInstaller kontrolü ve kurulumu
echo [4/10] PyInstaller kontrol ediliyor...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ❌ PyInstaller bulunamadi, kuruluyor...
    pip install --upgrade pyinstaller
    if errorlevel 1 (
        echo ❌ HATA: PyInstaller kurulamadi!
        pause
        exit /b 1
    )
    echo ✅ PyInstaller kuruldu
) else (
    echo ✅ PyInstaller mevcut, guncelleniyor...
    pip install --upgrade pyinstaller
    if errorlevel 1 (
        echo ⚠️  PyInstaller guncellenemedi, mevcut surum kullanilacak
    ) else (
        echo ✅ PyInstaller guncellendi
    )
)
echo.
echo.
echo.
echo.
echo.

REM OpenCV ve diğer dependencies kontrolü
echo [5/10] Gerekli kutuphaneler kontrol ediliyor...
python -c "import cv2; print('✅ OpenCV version:', cv2.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ OpenCV bulunamadi, kuruluyor...
    pip install --upgrade opencv-python
    if errorlevel 1 (
        echo ❌ HATA: OpenCV kurulamadi!
        pause
        exit /b 1
    )
    echo ✅ OpenCV kuruldu
) else (
    echo ✅ OpenCV mevcut, guncelleniyor...
    pip install --upgrade opencv-python
    if errorlevel 1 (
        echo ⚠️  OpenCV guncellenemedi, mevcut surum kullanilacak
    ) else (
        echo ✅ OpenCV guncellendi
    )
)

REM NumPy kontrolü
python -c "import numpy; print('✅ NumPy version:', numpy.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ NumPy bulunamadi, kuruluyor...
    pip install --upgrade numpy
) else (
    echo ✅ NumPy mevcut
)
echo.
echo.
echo.
echo.
echo.

REM OpenH264 kurulum ve yol tespiti
echo [6/10] OpenH264 codec kontrol ediliyor ve yolu tespit ediliyor...
python openH264_setup.py
echo.
echo.
echo.
echo.
echo.

REM OpenH264 DLL yolunu tespit et
echo 🔍 OpenH264 DLL yolu tespit ediliyor...
set "OPENH264_PATH="
for /f "delims=" %%i in ('python get_dll_path.py') do set "OPENH264_PATH=%%i"

if "%OPENH264_PATH%"=="" (
    echo ⚠️  OpenH264 DLL bulunamadi, EXE'ye dahil edilmeyecek
    set OPENH264_ADD_DATA=
) else (
    echo ✅ OpenH264 DLL bulundu: %OPENH264_PATH%
    set OPENH264_ADD_DATA=--add-data "%OPENH264_PATH%;."
)
echo.

REM Requirements.txt kontrolü ve kurulumu
if exist "requirements.txt" (
    echo ✅ requirements.txt dosyasi bulundu, eksik paketler kuruluyor...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ⚠️  Bazı paketler kurulamadi, mevcut paketlerle devam edilecek
    )
)
echo.

REM Eski build dosyalarını temizle
echo [7/10] Eski build dosyalari temizleniyor...
if exist "build\" rmdir /s /q "build"
if exist "dist\" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo ✅ Temizlendi
echo.
echo.
echo.
echo.
echo.

REM EXE oluştur
echo [8/10] EXE dosyasi olusturuluyor...
echo Bu islem birkaç dakika surebilir, lutfen bekleyin...
echo.
echo.
echo.
echo.
echo.

REM PyInstaller komutunu oluştur
set "PYINSTALLER_CMD=pyinstaller"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --onefile"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --console"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --name VideoResizer"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --icon=icon.ico"
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "openH264_setup.py;."
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "get_dll_path.py;."
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "requirements.txt;."
set PYINSTALLER_CMD=%PYINSTALLER_CMD% --add-data "resize.py;."

REM OpenH264 DLL'ini ekle (varsa)
if defined OPENH264_ADD_DATA (
    set PYINSTALLER_CMD=%PYINSTALLER_CMD% %OPENH264_ADD_DATA%
    echo 📦 OpenH264 DLL EXE'ye dahil ediliyor: %OPENH264_PATH%
)

REM Diğer parametreleri ekle
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import cv2"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import numpy"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import pathlib"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import bz2"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import shutil"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import glob"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import asyncio"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import urllib"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --hidden-import urllib.request"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --collect-submodules cv2"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --collect-submodules numpy"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --distpath ./dist"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --workpath ./build"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% --specpath ./"
set "PYINSTALLER_CMD=%PYINSTALLER_CMD% main.py"

REM Komutu çalıştır
echo 🚀 PyInstaller komutu çalıştırılıyor...
echo %PYINSTALLER_CMD%
echo.
%PYINSTALLER_CMD%

if errorlevel 1 (
    echo.
    echo ❌ HATA: EXE olusturulamadi!
    echo Hata detaylari yukarida gorulebilir
    pause
    exit /b 1
)

echo.
echo ✅ EXE dosyasi basariyla olusturuldu!
echo.
echo.
echo.
echo.

REM Sonuç kontrolü
echo [9/10] Sonuc kontrol ediliyor...
if exist "dist\VideoResizer.exe" (
    echo ✅ VideoResizer.exe basariyla olusturuldu!
    echo.
    echo 📁 Dosya konumu: %CD%\dist\VideoResizer.exe
    
    REM Dosya boyutunu göster
    for %%I in ("dist\VideoResizer.exe") do (
        set /a "SIZE_MB=%%~zI/1024/1024"
        echo 📏 Dosya boyutu: %%~zI bytes (~!SIZE_MB! MB)
    )
    
    REM Test çalıştır
    echo [10/10] EXE dosyasi test ediliyor...
    dist\VideoResizer.exe --version >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  EXE test edilemedi, ancak dosya olusturuldu
    ) else (
        echo ✅ EXE dosyasi test edildi ve calisiyor
    )
    
    echo.
    echo ================================================================
    echo                         BASARILI!
    echo ================================================================
    echo.
    echo VideoResizer.exe dosyasi olusturuldu.
    echo Bu dosyayi Python yuklu olmayan bilgisayarlara kopyalayabilirsiniz.
    echo.
    if not "%OPENH264_PATH%"=="" (
        echo 🎥 OpenH264 codec dahil edildi - H264 destegi mevcut
    ) else (
        echo ⚠️  OpenH264 dahil edilemedi - H264 desteği sınırlı olabilir
    )
    echo.
    echo Kullanim ornekleri:
    echo   VideoResizer.exe
    echo   VideoResizer.exe video.mp4
    echo   VideoResizer.exe video.mp4 -y 1080 -f 30
    echo   VideoResizer.exe --help
    echo.
)

REM Eğer EXE oluşturulamadıysa hata mesajı göster
if not exist "dist\VideoResizer.exe" (
    echo ❌ HATA: VideoResizer.exe olusturulamadi!
    echo dist klasorunu kontrol edin
    echo.
)

echo Temizlik yapiliyor...
if exist "build\" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo.
echo ================================================================
echo                     ISLEM TAMAMLANDI
echo ================================================================
echo.
pause