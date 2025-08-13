@echo off
chcp 65001 >nul 2>&1
setlocal ENABLEDELAYEDEXPANSION

REM ------------------------------------------------------------
REM Ayarlar
REM ------------------------------------------------------------
set APP_NAME=LocalHost-server
set ENTRY=main.py
set ICON=icon.ico
set PY_MIN=3.6
set VENV_DIR=.venv
set ONEFILE=1
set CLEAN_BUILD=1

cd /d "%~dp0"





echo ================================================================
echo               %APP_NAME% - Python to EXE Donusturucu
echo ================================================================
echo  Bu arac %ENTRY% icin tek .exe olusturur (PyInstaller)
echo  Python olmayan makinelerde calistirmak icin kullanilir
echo ------------------------------------------------
echo  Gereksinimler:
echo    - Python %PY_MIN% +
echo    - pip ile pyinstaller
echo ================================================================
echo.






echo [1/8] Python kontrol ediliyor...
python --version >nul 2>&1 || (
    echo ❌ Python bulunamadi. https://python.org
    pause & exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version') do set PY_VER=%%v
echo ✅ Python: %PY_VER%
echo.







echo [2/8] Sanal ortam kontrolu...
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
    REM Parantezleri kaçır: ^(
    echo ✅ Sanal ortam aktif ^(%VENV_DIR%^) 
) else (
    echo ⚠️  Sanal ortam yok, sistem Python kullanilacak
)
echo.







echo [3/8] PyInstaller kontrolu...
python -m pip show pyinstaller >nul 2>&1 || (
    echo ⏳ PyInstaller kuruluyor...
    python -m pip install -U pyinstaller || (
        echo ❌ PyInstaller kurulamadı
        pause & exit /b 1
    )
)
echo ✅ PyInstaller hazir
echo.







if "%CLEAN_BUILD%"=="1" (
    echo [4/8] Eski build temizleniyor...
    if exist build rmdir /s /q build
    if exist dist rmdir /s /q dist
    del /q "%APP_NAME%.spec" 2>nul
    echo ✅ Temiz
) else (
    echo [4/8] Temizlik atlandi
)
echo.






echo [5/8] PyInstaller komutu hazirlaniyor...
set CMD=pyinstaller "%ENTRY%"
if "%ONEFILE%"=="1" set CMD=%CMD% --onefile
set CMD=%CMD% --name "%APP_NAME%" --console
if exist "%ICON%" set CMD=%CMD% --icon "%ICON%"
set CMD=%CMD% --distpath dist --workpath build --specpath .
echo Komut: %CMD%
echo.







echo [6/8] Derleniyor...
%CMD%
if errorlevel 1 (
    echo ❌ Derleme hatali
    pause & exit /b 1
)
echo ✅ Derleme tamamlandi
echo.







echo [7/8] Çikti dogrulama...
if not exist "dist\%APP_NAME%.exe" (
    echo ❌ Beklenen dosya yok: dist\%APP_NAME%.exe
    dir dist
    pause & exit /b 1
)
for %%I in ("dist\%APP_NAME%.exe") do set SIZE_B=%%~zI
set /a SIZE_MB=%SIZE_B%/1024/1024
echo ✅ Olusan: dist\%APP_NAME%.exe  (~%SIZE_MB% MB)
echo.








echo [8/8] Test calistirma...
call dist\%APP_NAME%.exe --version >nul 2>&1
if errorlevel 1 (
    echo ℹ️  --version parametresi yok veya test atlandi
) else (
    echo ✅ Test basarili (--version^) 
)








echo.
echo ================================================================
echo                 ISLEM TAMAMLANDI - %APP_NAME%.exe
echo ================================================================
echo Ornek:
echo   dist\%APP_NAME%.exe
echo   dist\%APP_NAME%.exe -p 8080
echo   dist\%APP_NAME%.exe -r 9000-9050
echo   dist\%APP_NAME%.exe --help
echo.
pause