@echo off
REM netsweep quick launcher (Windows).
REM Usage:  run.bat [options]   (options are passed to main.py)
setlocal

REM UTF-8 code page for box characters and non-ASCII text.
chcp 65001 >nul

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
    python main.py %*
) else (
    py -3 main.py %*
)

endlocal
