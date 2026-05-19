@echo off
chcp 65001 >nul 2>&1
REM Script dizinine geç
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"
echo Mevcut klasor: %CD%
echo.

title Video Resizer Tool - Quick Run

echo.
echo ================================================================
echo                    VIDEO RESIZER TOOL
echo                      Quick Start
echo ================================================================
echo.
echo.
echo.
echo.
echo.

REM Virtual environment kontrolü ve aktivasyonu
if exist ".venv\" (
    echo ✅ Virtual environment aktif ediliyor...
    call .venv\Scripts\activate.bat >nul 2>&1
    echo ✅ Virtual environment aktif
) else (
    echo ⚠️  Virtual environment bulunamadi!
    echo Sistem Python kullanilacak veya once install.bat calistirin
)

echo.
echo 🚀 Video Resizer Tool baslatiliyor...
echo.
echo.
echo.
echo.
echo.

REM Ana program çalıştır
python.exe main.py

echo.
echo ================================================================
echo                     Program Sonlandi
echo ================================================================
echo.
pause
