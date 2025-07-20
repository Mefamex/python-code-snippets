#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
===============================================================================
                        Directory Explorer
===============================================================================
Description:
    Dizinlerin yapısını esnek bir şekilde görselleştirmek ve dışa aktarmak için geliştirilmiştir.
    Araç, özyinelemeli dizin tarama, boyut hesaplama ve sonuçları JSON ile TXT formatında 
        dışa aktarma gibi özellikler sunar.

Author:
    Mefamex (info@mefamex.com) (https://mefamex.com)

Features: 
    - Dizin yapısını özyinelemeli olarak tarar ve analiz eder
    - Klasör ve dosya boyutlarını hesaplar
    - Sonuçları JSON ve TXT olarak dışa aktarır
    - Özelleştirilebilir çıktı ve kolay komut satırı kullanımı

Modules:
    - ClassFile: Dosya nesnesi oluşturma ve boyut hesaplama
    - ClassDirectory: Dizin nesnesi oluşturma, yürüme ve dönüştürme
    - DirectoryExplorer: Çalıştırma ve dışa aktarma için ana arayüz

Classes:
    - C_file: Dosya bilgisi için veri sınıfı
    - C_folder: Klasör bilgisi için veri sınıfı
    - ClassFile: Dosya işlemleri için statik metotlar
    - ClassDirectory: Dizin işlemleri için statik metotlar
    - DirectoryExplorer: Kullanıcı etkileşimi için ana sınıf

Functions:
    - _print_info(message, sleeping): Renkli bilgi mesajı yazdırır
    - Dosya/klasör işlemleri ve dışa aktarma için tüm sınıf metotları

Usage:
    1. Kök dizini ve çıktı dizinini belirtin.
    2. İsteğe bağlı olarak hariç tutulacak dizin ve dosya adlarını girin.
    3. cmd -> `python directory_explorer_v1_1_0.py [path] [--no-print] [--no-json] [--no-txt]`
    4. Sonuç olarak belirtilen dizinde JSON ve/veya TXT dosyası oluşacaktır.

Requirements:
    - Python 3.7 veya üstü
    - Dependencies:
        - os, json, datetime, pathlib, typing, argparse, dataclasses, re, time (standart)

Installation:
    1. Dosyayı .py uzantılı olarak kaydedin.
    2. Tüm bağımlılıklar standart kütüphane olduğu için ek kurulum gerekmez.
    3. `if __name__ == "__main__":` bloğunu ihtiyaca göre düzenleyin.
    4. cmd -> `python directory_explorer.py [path] [--no-print] [--no-json] [--no-txt]`

Documentation: 
    - Detaylı bilgi için README.md dosyasına bakınız

License:
    MIT Lisansı (https://opensource.org/licenses/MIT)

Changelog:
    - 1.0.0 (2024-08-25): İlk sürüm
    - 1.1.0 (2025-07-19): Büyük iyileştirmeler ve yapı değişiklikleri

Contributors: None

Contact:
    info@mefamex.com
    https://mefamex.com
    https://github.com/Mefamex/Python_Code_Snippets

Additional Information:
    Daha fazla script ve araç için GitHub depomu ziyaret edin: https://github.com/Mefamex

Notes:
    - Bu proje esnek ve profesyonel dizin analizi için tasarlanmıştır.
    - Tüm kod okunabilirlik ve genişletilebilirlik gözetilerek yazılmıştır.

Disclaimer and Legal Notice:
    Bu yazılım, herhangi bir garanti olmaksızın "olduğu gibi" sağlanmaktadır.
    Yazar, bu yazılımın kullanımı sonucunda oluşabilecek zararlardan sorumlu değildir.
    Kullanıcılar, yazılımı kendi sorumlulukları altında kullanmalıdır.
    Açık kaynak lisansı ile dağıtılır ve kullanıcılar lisans koşullarına uymakla yükümlüdür.
    Yazılımın değiştirilmesi, dağıtılması veya kullanılması lisans koşullarına uygun olmalıdır.
===============================================================================
"""

__version__ = "1.1.0"
__author__ = "Mefamex"
__email__ = "info@mefamex.com"
__license__ = "MIT"
__status__ = "STABLE"  

__project_name__ = "directory-explorer"
__url__ = "https://mefamex.com"
__url_github__ = "https://github.com/Mefamex/Python_Code_Snippets"
__copyright__ = "Copyright (c) 2025 Mefamex"
__description__ = "A flexible directory structure visualization tool for Python."
__date__ = "2024-08-25" 
__date_modify__ = "2025-07-19"
__python_version__ = ">=3.7" 
__dependencies__ = {
    "python": ">=3.7",
    "os": "built-in",
    "json": "built-in",
    "time": "built-in",
    "re": "built-in",
    "argparse": "built-in",
    "datetime": "built-in",
    "pathlib": "built-in",
    "dataclasses": "built-in",
    "typing": "built-in"
}

#============================ IMPORTS =========================================
import os, json, time, re, argparse
from datetime import datetime
from typing import Dict, List, Union, Optional
from pathlib import Path
from dataclasses import dataclass, field
#==============================================================================


#============================ STATIC METHODS ==================================
def _print_info(message: str, sleeping: float = 0.1) -> None:
    """ Print information messages with ANSI color formatting. """
    RESET, BLUE, YELLOW, GREEN, CYAN = "\033[0m", "\033[1;34m", "\033[1;33m", "\033[1;32m", "\033[1;36m"
    output, msg = f"{BLUE}[INFO]{RESET} ", message
    def color_quotes(m): return f"{GREEN}{m.group(0)}{YELLOW}"
    msg = re.sub(r"(['\"])(.*?)(\1)", color_quotes, msg)
    if ":" in msg:
        parts = msg.split(":", 1)
        msg = f"{YELLOW}{parts[0]}:{CYAN}{parts[1]}{RESET}"
    else: msg = f"{YELLOW}{msg}{RESET}"
    print(output + msg)
    if sleeping > 0.0: time.sleep(sleeping)
#==============================================================================


#============================ DATA STRUCTURES =================================
@dataclass
class C_file:
    name: str
    path: Path
    size: int = 0
    date: datetime = datetime(1, 1, 1)
    is_sized: bool = False
    
@dataclass
class C_folder:
    name: str
    path: Path
    size: int = 0
    date: datetime = datetime(1, 1, 1)
    files: List[C_file] = field(default_factory=list)
    folders: List['C_folder' ] = field(default_factory=list)
    is_sized: bool = False
    is_walked: bool = False
#==============================================================================


#============================ DATA PROCESSING CLASSES ========================
class ClassFile:
    @staticmethod
    def create_class_file(path: Path) -> C_file:
        if not path.exists(): return C_file(name="", path=path, size=0, date=datetime(2000, 1, 1), is_sized=False)
        if not path.is_file(): return C_file(name="", path=path, size=0, date=datetime(2000, 1, 1), is_sized=False)
        return C_file(name=path.name, path=path, size=path.stat().st_size if path.is_file() else 0, date=datetime.fromtimestamp(path.stat().st_mtime) if path.is_file() else datetime(2000, 1, 1), is_sized=False)

    @staticmethod
    def to_dict_data(file: C_file) -> Dict[str, Union[str, int]]:
        """ Convert the C_file object to a dictionary. """
        #date format : YYYY-MM-DD HH:MM:SS
        return {"name": file.name, "path": str(file.path), "date": file.date.strftime("%Y-%m-%d %H:%M:%S"), "size": f"{file.size:,}".replace(",", ".")}

    @staticmethod
    def calculate_size(object: C_file) -> int:
        """ try to get the size of the file """
        try: 
            object.size = object.path.stat().st_size
            object.is_sized = True
        except Exception: 
            object.size = 0
            object.is_sized = False
        return object.size if object.is_sized else 0

class ClassDirectory:
    @staticmethod
    def create_class_directory(path: Path) -> Union[C_folder, bool]:
        if not path.exists(): return False
        if not path.is_dir(): return False
        return C_folder(name=path.name, path=path, size=0, date=datetime(1, 1, 1), is_sized=False)

    @staticmethod
    def to_dict_data(folder: C_folder) -> Dict[str, Union[str, int, list, dict]]:
        """ Convert the C_folder object to a dictionary. """
        return { "name": folder.name, "path": str(folder.path), "date": folder.date.strftime("%Y-%m-%d %H:%M:%S"), "size": f"{folder.size:,}".replace(",", "."), "files": [ClassFile.to_dict_data(f) for f in folder.files], "folders": [ClassDirectory.to_dict_data(f) for f in folder.folders]}

    @staticmethod
    def walk(object: C_folder, force_walk:bool = False) -> bool:
        """ Walk through the directory and return a boolean indicating success or failure."""
        if not isinstance(object, C_folder): return False
        if not object.path.exists() or not object.path.is_dir(): return False
        if object.is_walked and not force_walk: return True
        # check path is valid and not empty
        try: 
            if not object.path.is_dir(): return False
            filenames = os.listdir(object.path)
            if not filenames: 
                object.is_walked = True
                object.is_sized = True
                object.size = 0
                object.files = []
                object.folders = []
                return True
        except Exception: return False
        object.files = []
        object.folders = []
        object.size = 0
        last_modified = datetime(1, 1, 1)
        for entry in os.listdir(object.path):
            full_path = object.path / entry
            if full_path.is_file():
                newFile = ClassFile.create_class_file(full_path)
                object.size += ClassFile.calculate_size(newFile)
                object.files.append(newFile)
                if newFile.date > last_modified: last_modified = newFile.date
            elif full_path.is_dir():
                newFolder = ClassDirectory.create_class_directory(full_path)
                if not isinstance(newFolder, C_folder): continue
                ClassDirectory.walk(newFolder)
                object.size += newFolder.size
                if newFolder.date > last_modified: last_modified = newFolder.date
                object.folders.append(newFolder)
        object.date = last_modified
        object.is_walked = True
        object.is_sized = True
        return True
#==============================================================================


#============================ MAIN CLASS =====================================
class DirectoryExplorer:
    def __init__(self, path: Optional[Union[str, Path]] = None):
        path = Path(path) if path else Path.cwd()
        self.data: C_folder # ignore value, checked everywhere
        if not self.__set_main_path(path): raise ValueError(f"Invalid path provided: {path}")
        self.TABSIZE = 4  # Number of spaces for indentation in the output
        _print_info(f"DirectoryExplorer initialized with path: {self.data.path}")

    def run(self, path: Optional[Union[str, Path]] = None, print_data: bool = True, exportJson: bool = True, exportTxt: bool = True) -> bool:
        """ Run the DirectoryExplorer with the given path. """
        _print_info(f"Running DirectoryExplorer with path: {path if path else self.data.path}")
        if path:
            if not isinstance(path, (str, Path)): raise TypeError("Path must be a string or a Path object.")
            if not self.__set_main_path(Path(path)): raise ValueError(f"Invalid path provided: {path}")
        if not self.data: raise ValueError("Data is not set.")
        if not isinstance(self.data, C_folder): raise TypeError("Data must be a C_folder object.")
        if not self.data.path.exists(): raise FileNotFoundError(f"Path {self.data.path} does not exist.")
        if not self.data.path.is_dir(): raise NotADirectoryError(f"Path {self.data.path} is not a directory.")
        _print_info(f"DirectoryExplorer is ready to explore: {self.data.path}")
        if not self.data.is_walked or not self.data.is_sized:
            _print_info("Data is not ready, exploring the directory...")
            self.explore(self.data.path)
        _print_info("DirectoryExplorer is ready for exploration.")
        self.check_data_ready(doitNow=False)
        _print_info("DirectoryExplorer is ready to use.")
        self.explore()
        if print_data: self.print_data()
        if exportJson: self.export_data_json()
        if exportTxt : self.export_to_txt()
        _print_info("DirectoryExplorer run completed successfully.")
        return True
    
    def __set_main_path(self, path: Union[str, Path]) -> bool:
        _print_info(f"Setting main path to: {str(path)}")
        if not isinstance(path, (str, Path)):
            raise TypeError("Path must be a string or a Path object.")
        newPath = ClassDirectory.create_class_directory(Path(path))
        if not isinstance(newPath, C_folder):
            if not Path(path).exists():
                raise FileNotFoundError(f"Path {path} does not exist.")
            if not Path(path).is_dir():
                raise NotADirectoryError(f"Path {path} is not a directory.")
            raise ValueError("Invalid path provided.")
        self.data = newPath
        return True

    def check_data_ready(self, doitNow : bool = True):
        """ Check if the data is ready for exploration. """
        falseCounter: int = 0
        if not self.data: falseCounter += 1
        if not isinstance(self.data, C_folder): falseCounter += 1
        if not self.data.is_walked: falseCounter += 1
        if not self.data.is_sized: falseCounter += 1
        if falseCounter > 0:
            if doitNow:
                if not self.data.path: raise ValueError("Path is not set.")
                self.explore()
            else:  raise RuntimeError(f"Data is not ready. {falseCounter} checks failed.")
        return True
    
    def explore(self, path: Optional[Union[str, Path]] = None) -> None :
        """ Explore the directory and return a C_folder object with all files and folders. """
        if path is not None and not isinstance(path, (str, Path)):
            raise TypeError("Path must be a string or a Path object.")
        _print_info(f"Exploring directory: {path if path else self.data.path}")
        if not ClassDirectory.walk(self.data): raise RuntimeError("Failed to walk through the directory.")
        if not self.data.is_walked: raise RuntimeError("Directory has not been walked yet.")
        if not self.data.is_sized: raise RuntimeError("Directory has not been sized yet.")
        return

    def get_data_dict(self) -> Dict[str, Union[str, int, list, dict]]:
        """ Get the data in Dictionary format. """
        _print_info(f"Getting data in dictionary format...")
        self.check_data_ready()
        return ClassDirectory.to_dict_data(self.data)
    
    def get_data_json(self, data: Optional[Dict] = None) -> str:
        """ Get the data in JSON format. """
        _print_info(f"Getting data in JSON format...")
        if data:
            if not isinstance(data, dict): raise TypeError("Data must be a dictionary.")
        else:
            self.check_data_ready()
            data = self.get_data_dict()
        if "_comment" not in data: data = {"_comment": "script: github.com/Mefamex/Python_Code_Snippets/directory_explorer ; Licence: MIT ; Have a good code", **data}
        return json.dumps(data, indent=4, ensure_ascii=False)

    def print_data(self) -> None:
        """ Print the data in a pretty format. """
        _print_info("Printing data...")
        self.check_data_ready()
        print(self.get_data_json())
    
    def export_data_json(self) -> None:
        """ Export the data to a JSON file. """
        _print_info("Exporting data to JSON file...")
        self.check_data_ready()
        file_name = f"DirectoryExplorer_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.json"
        with open(self.data.path / file_name, "w", encoding="utf-8") as f: f.write(self.get_data_json())
        _print_info(f"Data exported successfully to '{self.data.path / file_name}'.")
    
    def export_to_txt(self) -> None:
        """ Export the data to a text file. """
        _print_info("Exporting data to text file...")
        self.check_data_ready()
        file_name = f"DirectoryExplorer_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.txt"
        def get_max_name_length(folder, depth=0):
            max_len = 0
            for file in folder.files:
                fname = "|    " * (depth+1) + file.name
                if len(fname) > max_len: max_len = len(fname)
            for subfolder in folder.folders:
                sub_max = get_max_name_length(subfolder, depth+1)
                if sub_max > max_len: max_len = sub_max
            return max_len
        max_name_length = get_max_name_length(self.data, 0)
        def write_tree(folder, depth=0):
            indent = "|    " * depth
            f.write(f"{indent}{folder.name}({len(folder.folders)}){'-'*50} {folder.date.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for file in folder.files:
                fname = file.name
                size = str(file.size)
                date = file.date.strftime('%Y-%m-%d %H:%M:%S')
                file_indent = indent + "|    "
                name_part = f"{file_indent}{fname}"
                space_count = max_name_length - len(name_part) + 2
                f.write(f"{name_part}{' ' * space_count}{size} {date}\n")
            for subfolder in folder.folders: write_tree(subfolder, depth+1)
        with open(self.data.path / file_name, "w", encoding="utf-8") as f: write_tree(self.data, 0)
        _print_info(f"Data exported successfully to '{self.data.path / file_name}'.")
#==============================================================================


#============================ MAIN EXECUTION ==================================
if __name__ == "__main__":
    #Default Path: 
    # default_path = str(Path.home() / "Desktop")  # Default to Desktop
    # default_path = str(Path(__file__).parent)    # Default to script directory
    default_path = str(Path.cwd())  # Default to current working directory


    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Directory Structure Visualization Tool: Explore, print, and export directory structures easily.")
    parser.add_argument("path", nargs="?", default=str(default_path), help="Root directory path to explore (default: current working directory)")
    parser.add_argument("--no-print", dest="print_data", action="store_false", help="Do not print the directory data to the console.")
    parser.add_argument("--no-json", dest="export_json", action="store_false", help="Do not export the directory data to a JSON file.")
    parser.add_argument("--no-txt", dest="export_txt", action="store_false", help="Do not export the directory data to a TXT file.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    
    # print docstring of file
    if __doc__:
        lines = [line for line in __doc__.splitlines()] + ["\n","="*60,"\t\t\tPROGRESS STARTED\t\t\t","="*60,"\n"]
        total_chars = sum(len(line) for line in lines) or 1
        for line in lines:
            print(line)
            time.sleep((len(line) / total_chars) * 2)

    
    # Check if the provided path is valid
    try:
        if not args.path:
            try: args.path = str(os.getcwd())
            except Exception as e:
                _print_info(f"Error: {e}")
                exit(1)
        if not isinstance(args.path, (str, Path)): raise TypeError("Path must be a string or a Path object.")
        _print_info(f"Starting DirectoryExplorer with path: {args.path}")
        time.sleep(3)

    
    # Initialize DirectoryExplorer with the provided path
        explorer = DirectoryExplorer(args.path)
        explorer.run(
            print_data=args.print_data,
            exportJson=args.export_json,
            exportTxt=args.export_txt
        )
        _print_info("DirectoryExplorer finished successfully.")
    except Exception as e:
        _print_info(f"Error: {e}")
        exit(1)

