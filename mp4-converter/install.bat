@echo off
chcp 65001 >nul 2>&1
title Video Resizer Tool - Installation

REM Script dizinine geç
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo ================================================================
echo                    VIDEO RESIZER TOOL
echo                      Installation
echo ================================================================
echo.
echo Mevcut klasor: %CD%
echo.
echo REQUIRED FILES:
echo - main.py         : Video işleme ve dönüştürme
echo - requirements.txt: Gerekli bağımlılıkları içerir
echo - openH264_setup.py: H264 codec kurulum desteği
echo - install.bat     : Kurulum scripti (bu dosya)
echo.
echo DOCUMENTATION:
echo - README.md       : Kullanım talimatları
echo. 
echo FOR PUBLIC:
echo - toExe.bat       : EXE dosyası oluşturma scripti
echo - icon.ico        : Uygulama ikonu
echo. 
echo. 
echo. 
timeout /t 2 >nul

:: Python version check
echo [1/7] Python kontrolu yapiliyor...
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
echo. 
echo. 
timeout /t 2 >nul

:: Create and navigate to the converter directory
echo [2/7] Virtual environment olusturuluyor...
if exist ".venv\" (
    echo ⚠️  Mevcut virtual environment bulundu, yeniden kullanilacak
    call .venv\Scripts\activate.bat
) else (
    echo 🔧 Yeni virtual environment olusturuluyor...
    python.exe -m venv .venv
    call .venv\Scripts\activate.bat
    echo ✅ Virtual environment olusturuldu
)
echo.
echo Python and venv directory:
python.exe -m pip -V
echo. 
echo. 
echo. 
timeout /t 2 >nul

echo [3/7] Pip guncelleniyor...
python.exe -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Pip guncellenemedi, mevcut surum kullanilacak
) else (
    echo ✅ Pip guncellendi
)
echo. 
echo. 
echo. 
timeout /t 2 >nul

echo [4/7] Dependencies yukleniyor...
python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ HATA: Bağımlılıklar kurulamadi!
    echo requirements.txt dosyasini kontrol edin
    pause
    exit /b 1
) else (
    echo ✅ Tum bagimliliklar basariyla kuruldu
)
echo. 
echo. 
echo. 
timeout /t 2 >nul

echo [5/7] OpenH264 codec kontrol ediliyor...
python openH264_setup.py
echo ✅ OpenH264 kurulum kontrol edildi
echo.

echo [6/7] Test calistiriliyor...
python main.py --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Test tamamlanamadi, ancak kurulum devam ediyor
) else (
    echo ✅ Sistem testi basarili
)
echo. 
echo. 
echo. 
timeout /t 2 >nul

echo [7/7] Kurulum tamamlaniyor...
echo.
echo ================================================================
echo                      KURULUM BASARILI!
echo ================================================================
echo.
echo Video Resizer Tool basariyla kuruldu.
echo.
echo Kullanim ornekleri:
echo   python main.py
echo   python main.py video.mp4
echo   python main.py video.mp4 -y 1080 -f 30
echo   python main.py --help
echo.
echo EXE dosyasi olusturmak icin: toExe.bat
echo.
echo Kurulum klasoru    : %CD%
echo Virtual environment: %CD%\.venv
echo.
pause