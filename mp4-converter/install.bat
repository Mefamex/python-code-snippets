@echo off
chcp 65001


echo REQUIRED FILES:
echo - main.py           : Video işleme ve dönüştürme
echo - requirements.txt  : Gerekli bağımlılıkları içerir
echo - toExe.bat         : EXE dosyası oluşturma scripti
echo - README.md         : Kullanım talimatları
echo - install.bat       : Kurulum scripti (bu dosya)
echo - icon.ico          : Kurulum scripti (bu dosya)


:: Create and navigate to the converter directory
:: mkdir -p "converter"
:: cd "converter"


:: Create a virtual environment
python.exe -m venv .venv
call .venv\Scripts\deactivate.bat


:: Upgrade pip and install required packages
:: python.exe -m pip install -U pip
::python.exe -m pip install -U opencv-python argparse
python.exe -m pip install -U -r requirements.txt


