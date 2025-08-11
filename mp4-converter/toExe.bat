@echo off
chcp 65001 >nul 2>&1
REM ==================================================================
REM                     VIDEO RESIZER TOOL
REM                   Python to EXE Converter
REM ==================================================================
REM
REM Bu batch dosyası main.py dosyasını tek bir exe dosyasına dönüştürür
REM Böylece Python yüklü olmayan bilgisayarlarda da çalışabilir
REM
REM Gereksinimler:
REM - Python 3.8+ yüklü olmalı
REM - pip ile pyinstaller kurulu olmalı
REM
REM Kullanım: toExe.bat dosyasına çift tıklayın
REM ==================================================================

title Video Resizer - Python to EXE Converter

echo.
echo ================================================================
echo                    VIDEO RESIZER TOOL
echo                 Python to EXE Converter
echo ================================================================
echo.
echo Bu tool main.py dosyasini tek exe dosyasina donusturur
echo Python olmayan bilgisayarlarda da calisabilir hale getirir
echo.

REM Mevcut klasörü kaydet
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Mevcut klasor: %CD%
echo.

REM Python kontrolü
echo [1/8] Python kontrolu yapiliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ HATA: Python bulunamadi! 
    echo    Python 3.8+ yuklu oldugundan emin olun
    echo    https://python.org adresinden indirebilirsiniz
    pause
    exit /b 1
)
python --version
echo ✅ Python bulundu
echo.

REM Virtual environment kontrolü
echo [2/8] Virtual environment kontrol ediliyor...
if exist ".venv\" (
    echo ✅ Virtual environment bulundu (.venv^)
    call .venv\Scripts\activate.bat >nul 2>&1
    echo Virtual environment aktif edildi
) else (
    echo ⚠️  Virtual environment bulunamadi
    echo Sistem Python kullanilacak
)
echo.

REM Pip güncellemesi
echo.
echo [3/8] Pip guncelleniyor...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Pip guncellenemedi, mevcut surum kullanilacak
) else (
    echo ✅ Pip guncellendi
)
echo.

REM PyInstaller kontrolü ve kurulumu
echo [4/8] PyInstaller kontrol ediliyor...
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

REM OpenCV kontrolü
echo [5/8] OpenCV kontrol ediliyor...
python -c "import cv2; print('OpenCV version:', cv2.__version__)" 2>nul
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
echo.

REM Eski build dosyalarını temizle
echo [6/8] Eski build dosyalari temizleniyor...
if exist "build\" rmdir /s /q "build"
if exist "dist\" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo ✅ Temizlendi
echo.

REM EXE oluştur
echo [7/8] EXE dosyasi olusturuluyor...
echo Bu islem birkaç dakika surebilir, lutfen bekleyin...
echo.

pyinstaller ^
    --onefile ^
    --console ^
    --name "VideoResizer" ^
    --icon=icon.ico ^
    --add-data "main.py;." ^
    --hidden-import cv2 ^
    --hidden-import numpy ^
    --hidden-import pathlib ^
    --collect-submodules cv2 ^
    --distpath "./dist" ^
    --workpath "./build" ^
    --specpath "./" ^
    main.py

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

REM Sonuç kontrolü
echo [8/8] Sonuc kontrol ediliyor...
if exist "dist\VideoResizer.exe" (
    echo ✅ VideoResizer.exe basariyla olusturuldu!
    echo.
    echo 📁 Dosya konumu: %CD%\dist\VideoResizer.exe
    
    REM Dosya boyutunu göster
    for %%I in ("dist\VideoResizer.exe") do echo 📏 Dosya boyutu: %%~zI bytes
    
    echo.
    echo ================================================================
    echo                         BASARILI!
    echo ================================================================
    echo.
    echo VideoResizer.exe dosyasi olusturuldu.
    echo Bu dosyayi Python yuklu olmayan bilgisayarlara kopyalayabilirsiniz.
    echo.
    echo Kullanim ornekleri:
    echo   VideoResizer.exe
    echo   VideoResizer.exe video.mp4
    echo   VideoResizer.exe video.mp4 -y 1080 -f 30
    echo   VideoResizer.exe --help
    echo.
    
    REM Klasörü aç
    choice /c YN /m "dist klasorunu acmak ister misiniz? (Y/N)"
    if !errorlevel!==1 (
        explorer "dist"
    )
    
) else (
    echo ❌ HATA: VideoResizer.exe olusturulamadi!
    echo dist klasorunu kontrol edin
)

echo.
echo Temizlik yapiliyor...
if exist "build\" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo.
echo ================================================================
echo                     ISLEM TAMAMLANDI
echo ================================================================
echo.
pause 

