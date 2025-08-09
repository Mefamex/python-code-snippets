:: UPDATE : python packages
python -m pip install -U pip
python -m pip install -U wheel setuptools PyInstaller 



:: CREATE PYTHON: Project Directory
mkdir [project_name]
cd [project_name]


:: UV-VENV : Create a Virtual Environment
python -m venv .venv 


:: ACTIVATE VENV
call .venv\Scripts\activate


:: INSTALL BASE 
python.exe -m pip install -U pip
python.exe -m pip freeze > requirements.txt
ECHO # -*- coding: utf-8 -*- >> main.py
python -c "import datetime; print('# Created on: '+datetime.datetime.now().isoformat(timespec='seconds')+'Z')" >> main.py







:: INITIALIZE FILES
ECHO. >> main.py
ECHO def main(): >> main.py
ECHO     print("Hello, World!") >> main.py
ECHO. >> main.py
ECHO if __name__ == "__main__": >> main.py
ECHO     main() >> main.py
ECHO. >> main.py

ECHO .venv\Scripts\activate >> _activate

for %%i in (.) do set "folder_name=%%~nxi"
ECHO # %folder_name% >> README.md
ECHO. >> README.md
ECHO > Created on: %date% >> README.md
ECHO. >> README.md
ECHO. >> README.md
ECHO ## Description: >> README.md
ECHO. >> README.md
ECHO. >> README.md
ECHO ## Usage: >> README.md
ECHO. >> README.md
ECHO. >> README.md
ECHO ## License: >> README.md
ECHO. >> README.md
ECHO. >> README.md
ECHO ## Author: >> README.md
ECHO. >> README.md
ECHO. >> README.md
ECHO ## Project Structure: >> README.md
ECHO. >> README.md
ECHO. >> README.md

ECHO.
ECHO Project %folder_name% created successfully!