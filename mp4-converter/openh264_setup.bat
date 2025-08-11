@echo off
chcp 65001 >nul 2>&1
REM Script dizinine geç
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"
echo Mevcut klasor: %CD%
echo.


title OpenH264 Codec Fix

echo.
echo ================================================================
echo                  OpenH264 Codec Düzeltme
echo ================================================================
echo.
echo Bu script OpenH264 codec uyumluluk sorunlarını çözer
echo.

if exist ".venv\" (
    echo ✅ Virtual environment aktif ediliyor...
    call .venv\Scripts\activate.bat
)

echo 🔧 OpenH264 uyumluluk sorunu düzeltiliyor...
python.exe openH264_setup.py

echo.
echo ================================================================
echo                    İşlem Tamamlandı
echo ================================================================
echo.
pause

