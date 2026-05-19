# -*- coding: utf-8 -*- 
#!/usr/bin/env python3 

"""
===========================================================
                CHECK SCRIPT DEPENDENCIES
===========================================================

Description:
    Python modüllerinin bağımlılıklarını otomatik olarak kontrol eden, yükleyen ve güncelleyen 
    yardımcı sınıf. Proje geliştirme sürecinde gerekli bağımlılıkların eksikliğini tespit eder,
    otomatik olarak yükler ve sürüm uyumluluğunu kontrol eder.
    
    Bu modülü hem import ederek hem de doğrudan script içine yerleştirerek kullanabilirsiniz.
    
Author:
    Mefamex (info@mefamex.com) (https://mefamex.com)

Features: 
    - Tek veya çoklu modül bağımlılık kontrolü
    - Eksik modüllerin otomatik yüklenmesi
    - Gelişmiş sürüm uyumluluğu kontrolü (>=, <=, ==, !=, >, <, ~=)
    - Otomatik modül güncelleme özelliği
    - Detaylı hata yönetimi ve özel exception sınıfları
    - Verbose mod ile detaylı çıktı kontrolü
    - Timeout yönetimi
    - Modül durum bilgisi alma (get_modules_status)
    - Boolean sonuç döndürme (check_multiple_modules_bool)
    - Farklı pip/import ismi desteği (pip_name|import_name syntax)
    - PyPI güncel sürüm kontrolü
    - Packaging library desteği ile gelişmiş sürüm yönetimi

Modules:
    - subprocess: Pip komutlarının çalıştırılması için
    - sys: Python sistem bilgileri ve modül yolları
    - importlib: Modül bulma ve import işlemleri
    - re: Sürüm gereksinimlerinin parsing işlemi
    - warnings: Uyarı mesajları için
    - typing: Type hints desteği
    - packaging.version: Gelişmiş sürüm karşılaştırması
    - packaging.specifiers: Sürüm gereksinim kontrolü

Classes:
    - CheckFileDependencies: Ana bağımlılık kontrolü sınıfı
    - DependencyError: Temel bağımlılık hatası
    - ModuleInstallationError: Modül yükleme hatası
    - ModuleUpdateError: Modül güncelleme hatası
    - VersionComparisonError: Sürüm karşılaştırma hatası

Main Methods:
    - check_requirements_txt( requirements_file: str, ... ): requirements.txt dosyasını kontrol et
    - ensure_module(module_name, ...): Tek modül kontrolü
    - check_multiple_modules(modules_list, ...): Çoklu modül kontrolü (detaylı sonuç)
    - check_multiple_modules_bool(modules_list, ... ): Çoklu modül kontrolü (boolean sonuç)
    - get_modules_status(modules_list, verbose): Modül durum bilgisi alma (yükleme yapmadan)
    - get_installed_version(module_name): Yüklü modül sürümünü getir
    - is_version_compatible(current_version, required_version): Sürüm uyumluluğu kontrolü
    - check_module_newer_version(module_name): PyPI'da yeni sürüm kontrolü
    - update_module(module_name, check_newer, verbose, timeout): Modül güncelleme
    - install_module(module_name, verbose, timeout): Modül yükleme
    - is_module_available(module_name): Modül varlık kontrolü

Helper Methods:
    - _parse_module_requirement(module_requirement): Modül gereksinim parsing
    - run_cmd_command(command, timeout): Güvenli komut çalıştırma
    - print_class_static_vars(): Sınıf ayarlarını gösterme

Usage:
    1. Modülleri import edin ve CheckFileDependencies sınıfını kullanın.
    2. Kontrol edilecek modül(ler)i belirtin (sürüm gereksinimleri opsiyonel).
    3. Tek modül: `CheckFileDependencies.ensure_module("numpy>=1.20.0")`
    4. Çoklu modül (detaylı): `CheckFileDependencies.check_multiple_modules(["requests", "pandas>=1.3.0"])`
    5. Çoklu modül (boolean): `CheckFileDependencies.check_multiple_modules_bool(["requests", "pandas>=1.3.0"])`
    6. Durum bilgisi: `CheckFileDependencies.get_modules_status(["requests", "pandas"])`
    7. Farklı pip/import ismi: `CheckFileDependencies.ensure_module("Pillow|PIL>=8.0.0")`

Advanced Syntax:
    - Standart: "numpy>=1.20.0"
    - Farklı pip/import ismi: "Pillow|PIL>=8.0.0"
    - Sadece pip ismi farklı: "beautifulsoup4|bs4"
    - Sürüm operatörleri: ">=", "<=", "==", "!=", ">", "<", "~="

Requirements:
    - Python 3.6 veya üstü
    - pip package manager
    - İnternet bağlantısı (modül yükleme için)
    Core Dependencies:
        - subprocess (built-in)
        - sys (built-in)
        - importlib (built-in)
        - re (built-in)
        - warnings (built-in)
        - typing (built-in)
        - packaging (external - otomatik yüklenecek)

Installation:
    1. Tek dosya olarak kullanım:
        - Bu dosyayı projenize kopyalayın
        - Python -> from check_file_dependencies import CheckFileDependencies

Documentation: 
    - Detaylı kullanım örnekleri: USAGE_EXAMPLE() fonksiyonu
    - API dokümantasyonu: Kod içi docstring'ler
    - Online dokümantasyon: https://github.com/Mefamex/Python_Code_Snippets

License:
    MIT Lisansı (https://opensource.org/licenses/MIT)

Changelog:
    - 1.0.0 (2025-07-19): First stable release
    - 1.0.1 (2025-08-07): Major update with new features:
        * Çoklu modül ve sürüm kontrolü geliştirildi
        * pip_name|import_name desteği eklendi
        * PyPI güncel sürüm kontrolü ve packaging entegrasyonu
        * Hata yönetimi ve verbose çıktı iyileştirildi
        * Kapsamlı test ve kullanım örnekleri eklendi
        * Timeout yönetimi eklendi
    - 1.0.2 (2025-08-11):
        * requirements.txt toplu kontrol ve CLI desteği
        * Modül yükleme/güncellemede sürüm zorunluluğu desteği
        * Sonsuz döngü ve tekrar kurulum hataları düzeltildi
        * Çıktı hizalama ve özet raporlar geliştirildi
        * Küçük hata düzeltmeleri ve performans iyileştirmeleri

Contributors: mefamex

Contact:
    - Email: info@mefamex.com
    - Website: https://mefamex.com
    - GitHub: https://github.com/Mefamex/Python_Code_Snippets

Additional Information:
    Bu modül, Python projelerinde bağımlılık yönetimini otomatikleştirmek için tasarlanmıştır.
    Production ortamlarında kullanımdan önce test edilmesi önerilir.
    Desteklenen sürüm operatörleri:
    - >=: Büyük eşit
    - <=: Küçük eşit  
    - ==: Eşit
    - !=: Eşit değil
    - >: Büyük
    - <: Küçük
    - ~=: Uyumlu sürüm
    
    Yeni özellikler:
    - Gelişmiş modül durumu kontrolü
    - Daha iyi hata mesajları ve istisna yönetimi
    - Kullanıcı dostu CLI arayüzü

Notes:
    - Modül yükleme işlemleri pip üzerinden yapılır
    - İnternet bağlantısı gereklidir (yeni modül yüklemek için)
    - Timeout değeri varsayılan 300 saniyedir
    - Verbose mod varsayılan olarak kapalıdır (v2.0'da değişti)
    - Packaging kütüphanesi otomatik olarak yüklenecektir

Performance:
    - Gelişmiş caching mekanizması
    - Optimized version comparison
    - Batch operation support
    - Timeout management for slow networks

Disclaimer and Legal Notice:
    Bu yazılım, herhangi bir garanti olmaksızın "olduğu gibi" sağlanmaktadır.
    Yazar, bu yazılımın kullanımı sonucunda oluşabilecek zararlardan sorumlu değildir.
    Kullanıcılar, yazılımı kendi sorumlulukları altında kullanmalıdır.
    
    MIT Lisansı kapsamında açık kaynak olarak dağıtılır ve kullanıcılar lisans 
    koşullarına uymakla yükümlüdür. Yazılımın değiştirilmesi, dağıtılması veya 
    kullanılması lisans koşullarına uygun olmalıdır.
===========================================================

"""

__version__ = "1.0.2"
__author__ = "Mefamex"
__email__ = "info@mefamex.com"
__license__ = "MIT"
__status__ = "STABLE"

__project_name__ = "check_file_dependencies"
__url__ = "https://mefamex.com"
__url_github__ = "https://github.com/Mefamex/Python_Code_Snippets"
__copyright__ = "Copyright (c) 2025 Mefamex"
__description__ = "Gelişmiş Python modül bağımlılık yönetimi ve otomatik yükleme aracı"
__date__ = "2025-07-19"
__date_modify__ = "2025-08-07"
__python_version__ = ">=3.6" 
__dependencies__ = {
    "subprocess": "built-in",
    "sys": "built-in", 
    "importlib": "built-in",
    "re": "built-in",
    "argparse": "built-in",
    "typing": "built-in",
    "packaging": "external - auto-install"
}
#===============================================================================


#============================ IMPORTS ==========================================
import os, sys, subprocess, importlib, importlib.util, re, argparse
from typing import Optional, List, Union, Tuple, Dict, Any
from packaging.version import Version
from packaging.specifiers import SpecifierSet
#===============================================================================


#============================ CUSTOM EXCEPTIONS ============================
class DependencyError(Exception): pass
class ModuleInstallationError(DependencyError): pass
class ModuleUpdateError(DependencyError): pass
class VersionComparisonError(DependencyError): pass
#===============================================================================

class CheckFileDependencies:
    # STATIC VARIABLES
    TIMEOUT    : int  = 300
    AUTO_UPDATE: bool = False
    VERBOSE    : bool = True
    VERBOSE_def: bool = False
    ######################
    @staticmethod
    def print_class_static_vars():print( f" CheckFileDependencies:\n TIMEOUT     : {CheckFileDependencies.TIMEOUT}\n AUTO_UPDATE : {CheckFileDependencies.AUTO_UPDATE}\n VERBOSE     : {CheckFileDependencies.VERBOSE}\n VERBOSE_RUN : {CheckFileDependencies.VERBOSE_def}")


    @staticmethod
    def check_requirements_txt(requirements_path: str = "requirements.txt", auto_update: bool = False, verbose: bool = False, timeout: int = 300) -> dict:
        """  requirements.txt dosyasındaki tüm bağımlılıkları kontrol eder, eksik veya uyumsuz olanları yükler/günceller.
        Returns: dict: Her modül için sonuç (True/False/hata mesajı)  """
        if not os.path.isfile(requirements_path):
            if verbose: print(f"[REQ] ❌ Dosya bulunamadı: {requirements_path}")
            raise FileNotFoundError(f"requirements.txt bulunamadı: {requirements_path}")
        modules = []
        with open(requirements_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().replace(" ", "").replace("\n", ""). replace("\r", ""). replace("\t", ""). replace("\v", "")
                if not line or line.startswith("#"): continue
                modules.append(line)
        if verbose:  print(f"[REQ] 🔍 {requirements_path} içindeki {len(modules)} modül kontrol ediliyor...")
        results = CheckFileDependencies.check_multiple_modules( modules_list=modules, auto_update=auto_update, verbose=verbose, timeout=timeout )
        if verbose:  print(f"[REQ] ✅ requirements.txt kontrolü tamamlandı.")
        return results


    @staticmethod
    def check_multiple_modules_bool(modules_list: List[str], auto_update: bool = AUTO_UPDATE, verbose: bool = VERBOSE, timeout: int = TIMEOUT) -> bool:
        """ Check multiple modules and return True only if ALL modules are successfully processed.
        Returns: bool: True if ALL modules successful, False if ANY module fails """
        if CheckFileDependencies.VERBOSE_def: print(f"check_multiple_modules_bool {modules_list}, auto_update: {auto_update}, verbose: {verbose}, timeout: {timeout}")
        try:
            results = CheckFileDependencies.check_multiple_modules( modules_list=modules_list, auto_update=auto_update, verbose=verbose, timeout=timeout )
            all_successful = all(result is True for result in results.values())
            if CheckFileDependencies.VERBOSE_def: print(f"check_multiple_modules_bool result: {all_successful} ({sum(1 for result in results.values() if result is True)}/{len(results)} successful)")
            return all_successful
        except Exception as e:
            if verbose: print(f"[MODULES_BOOL] ❌ Exception occurred: {str(e)}")
            if CheckFileDependencies.VERBOSE_def: print(f"check_multiple_modules_bool exception: {str(e)}")
            return False
    
    
    @staticmethod
    def check_multiple_modules(modules_list: List[str], auto_update: bool = AUTO_UPDATE, verbose: bool = VERBOSE, timeout: int = TIMEOUT) -> Dict[str, Union[bool, str]]:
        """ Check multiple modules at once and return a dictionary with results.
            Returns: Dictionary with module names as keys and True/False/error_message as values
            Example:  modules = ["requests", "numpy>=1.20.0", "Pillow|PIL>=8.0.0"] """
        if CheckFileDependencies.VERBOSE_def:   print(f"\ncheck_multiple_modules {modules_list}, auto_update: {auto_update}, verbose: {verbose}, timeout: {timeout}")
        if not isinstance(modules_list, (list, tuple)):  raise ValueError("modules_list must be a list or tuple")
        if not modules_list: return {} if not verbose else (print("[MODULE] ⚠️  Empty modules list provided") or {})
        results, successful_count, failed_count = {}, 0, 0
        if verbose: print(f"\n[MODULE] 🔍 Checking {len(modules_list)} modules...\n"+"=" * 60)
        for i, module_name in enumerate(modules_list, 1):
            if not isinstance(module_name, str) or not module_name.strip():
                error_msg = f"Invalid module name at index {i-1}: must be non-empty string"
                results[str(module_name)],failed_count  = error_msg, failed_count + 1
                if verbose: print(f"[MODULE] ❌ ERROR [{i}/{len(modules_list)}]: {error_msg}")
                continue
            module_name = module_name.strip()
            pip_name, version_req, import_name = CheckFileDependencies._parse_module_requirement(module_name)
            if verbose:  print(f"[MODULE] 📦              :[{i}/{len(modules_list)}] {pip_name}{f' (version: {version_req})' if version_req else ''}{f' [import: {import_name}]' if pip_name != import_name else ''}")
            try:
                success = CheckFileDependencies.ensure_module( module_name=module_name, auto_update=auto_update, verbose=verbose, time_out=timeout )
                if success: results[module_name], successful_count = True, successful_count + 1
                else: results[module_name], failed_count = False, failed_count + 1
                if verbose: print(f'[MODULE] {"✅" if success else "❌"}'+f' [{i:>2d}/{len(modules_list):<2d}]'.ljust(13)+f': {pip_name}')
            except Exception as e:
                error_msg = f"Error processing {pip_name}: {str(e)}"
                results[module_name], failed_count = error_msg, failed_count + 1
                if verbose: print(f"[MODULE] ❌ [{i}/{len(modules_list)}] Exception: {pip_name} - {str(e)}")
        if verbose:
            print("\n" + "=" * 60)
            print(f"[MODULE] 📊 SUMMARY:")
            print(f"[MODULE]    Total modules: {len(modules_list)}")
            print(f"[MODULE]    ✅ Successful: {successful_count}")
            print(f"[MODULE]    ❌ Failed: {failed_count}")
            print(f"[MODULE]    📈 Success rate: {(successful_count/(successful_count+failed_count)*100) if (successful_count+failed_count) > 0 else 0:.1f}%")
            if failed_count > 0:
                print(f"\n[MODULE] ❌ Failed modules:")
                for module, result in results.items():
                    if result is not True:print(f"[MODULE]    - {CheckFileDependencies._parse_module_requirement(module)[0]}: {result}")
        return results



    @staticmethod
    def get_modules_status(modules_list: List[str], verbose: bool = VERBOSE) -> Dict[str, Dict[str, Union[str, bool]]]:
        """  Get detailed status information for multiple modules without installing them.
            Returns: Dictionary with detailed status for each module """
        if CheckFileDependencies.VERBOSE_def:  print(f"get_modules_status {modules_list}, verbose: {verbose}")
        if not isinstance(modules_list, (list, tuple)): raise ValueError("modules_list must be a list or tuple")
        results = {}
        if verbose: print(f"[STATUS] 🔍 Getting status for {len(modules_list)} modules...")
        for module_name in modules_list:
            if not isinstance(module_name, str) or not module_name.strip(): continue
            module_name = module_name.strip()
            pip_name, version_req, import_name = CheckFileDependencies._parse_module_requirement(module_name)
            status = { 'pip_name': pip_name, 'import_name': import_name, 'version_requirement': version_req, 'installed': False, 'current_version': '', 'version_compatible': False, 'has_newer_version': False, 'error': None }
            try:
                status['installed'] = CheckFileDependencies.is_module_available(import_name)
                if status['installed']:
                    current_version = CheckFileDependencies.get_installed_version(module_name)
                    status['current_version'] = current_version
                    if version_req and current_version:
                        try: status['version_compatible'] = CheckFileDependencies.is_version_compatible(current_version, version_req)
                        except: status['version_compatible'] = False
                    else: status['version_compatible'] = True if not version_req else False
                    try: status['has_newer_version'] = CheckFileDependencies.check_module_newer_version(module_name)
                    except: status['has_newer_version'] = False
            except Exception as e: status['error'] = str(e)
            results[module_name] = status
            if verbose:
                status_icon = "✅" if status['installed'] and status['version_compatible'] else "❌"
                print(f"[STATUS] {status_icon} {pip_name}: installed={status['installed']}, version={status['current_version']}, compatible={status['version_compatible']}")
        return results



    @staticmethod
    def ensure_module(module_name: str, auto_update: bool = AUTO_UPDATE, verbose: bool = VERBOSE, time_out: int = TIMEOUT) -> bool:
        """ Ensure a module is available, optionally updating it if necessary. """
        if auto_update is None: auto_update = CheckFileDependencies.AUTO_UPDATE
        if verbose is None: verbose = CheckFileDependencies.VERBOSE
        if time_out is not None: time_out = CheckFileDependencies.TIMEOUT
        if CheckFileDependencies.VERBOSE_def: print(f"ensure_module '{module_name}' , auto_update: {auto_update}, verbose: {verbose}, timeout: {time_out}")
        if not isinstance(module_name, str) or not module_name.strip(): 
            if verbose: print(f"\n[MODULE] ❌ ERROR       : module_name have to be a non-empty string")
            raise ValueError("module_name must be a non-empty string")
        pip_name, version_requirement, import_name = CheckFileDependencies._parse_module_requirement(module_name)
        if verbose: print(f"\n[MODULE] 🔍 checking     : {pip_name} ({import_name}{', ' + version_requirement if version_requirement else ''})")
        try: # check module is available
            if not CheckFileDependencies.is_module_available(module_name):
                if verbose: print(f"[MODULE] ❓ not exist    : {pip_name}")
                if not CheckFileDependencies.install_module(module_name, verbose, time_out): return False
            else: # Module not available, try to install it
                current_version = CheckFileDependencies.get_installed_version(module_name)
                if not current_version:
                    if verbose: print(f"[MODULE] ❌ ERROR       : {pip_name} (version not found)")
                    return False
                if not auto_update and not version_requirement: 
                    if verbose: print(f"[MODULE] ✅ ready to use : {pip_name}{f" (v{current_version})" if current_version else ""}")
                elif auto_update: CheckFileDependencies.update_module(module_name=module_name, check_newer=True, verbose=verbose, timeout=time_out)
                elif version_requirement:
                    try: # check version requirement
                        if not CheckFileDependencies.is_version_compatible(current_version, version_requirement):
                            if verbose: print(f"[MODULE] ⚠️  version mismatch: {pip_name} (current: {current_version}, required: {version_requirement})")
                            return CheckFileDependencies.update_module(module_name=module_name, check_newer=False, verbose=verbose, timeout=time_out)
                        else: # Version requirement is met, dont update
                            if verbose: print(f"[MODULE] ✅ ready to use : {pip_name}{f" (v{current_version})" if current_version else ""}")
                    except VersionComparisonError as e:
                        if verbose: print(f"[MODULE] ⚠️  version check failed: {pip_name} - {str(e)}")
                        raise VersionComparisonError(f"Version comparison error for {pip_name}: {str(e)}")
                    except Exception as e:
                        if verbose: print(f"[MODULE] ❌ ERROR       : {pip_name}\n\n{ f"Unexpected error: {pip_name} - {str(e)}"}")
                        raise DependencyError( f"Unexpected error: {pip_name} - {str(e)}")
                else: raise Exception(f"Unexpected state: {pip_name} - version_requirement: {version_requirement}, current_version: {current_version}")
        except (ValueError, VersionComparisonError, DependencyError): raise
        except Exception as e:
            if verbose: print(f"[MODULE] ❌ ERROR       : {pip_name}\n\n{ f"Unexpected error: {pip_name} - {str(e)}"}")
            raise DependencyError( f"Unexpected error: {pip_name} - {str(e)}")
        return True
    
    
    @staticmethod
    def update_module(module_name:str,check_newer:bool=True,verbose:bool=VERBOSE, timeout: int = TIMEOUT) -> bool:
        """ Update a module using pip and return True if successful, False otherwise."""
        if CheckFileDependencies.VERBOSE_def: print(f"update_module '{module_name}' , verbose: {verbose}, timeout: {timeout}")
        if not isinstance(module_name, str) or not module_name.strip():  raise ValueError("module_name must be a non-empty string")
        pip_name, _, import_name = CheckFileDependencies._parse_module_requirement(module_name)
        if not CheckFileDependencies.is_module_available(import_name): raise ModuleInstallationError(f"Module '{import_name}' is not installed.") 
        if check_newer and not CheckFileDependencies.check_module_newer_version(module_name):
            if verbose: print(f"[MODULE] ✅ up-to-date   : {pip_name}")
            return True
        if verbose: print(f"[MODULE] 🔄 updating     : {pip_name}")
        return CheckFileDependencies.install_module(module_name, verbose=verbose, timeout=timeout)


    @staticmethod
    def install_module(module_name: str, verbose: bool = VERBOSE, timeout: int = TIMEOUT) -> bool:
        """ Install a module using pip and return True if successful, False otherwise."""
        if CheckFileDependencies.VERBOSE_def: print(f"install_module '{module_name}' , verbose: {verbose}, timeout: {timeout}")
        if not isinstance(module_name, str) or not module_name.strip(): raise ValueError("module_name must be a non-empty string")
        pip_name, version_req, _ = CheckFileDependencies._parse_module_requirement(module_name)
        # Sürüm gereksinimi varsa pip_name'e ekle
        pip_install_str = pip_name + (version_req if version_req else "")
        command = [sys.executable, "-m", "pip", "install", "-U", pip_install_str]
        if verbose: print(f"[MODULE] 📥 installing   : {pip_install_str}")
        try:
            success, stdout, stderr = CheckFileDependencies.run_cmd_command(command, timeout=timeout)
            if not success:  
                error_msg = f"Module installation failed: {pip_install_str} - {stderr}"
                if verbose: print(f"[MODULE] ❌ ERROR INSTALL: {pip_install_str}\n\n{stderr}")
                raise ModuleInstallationError(error_msg)
        except subprocess.TimeoutExpired as e: 
            error_msg = f"Module installation timeout: {pip_install_str}"
            if verbose: print(f"[MODULE] ❌ TIMEOUT INSTALL: {pip_install_str}")
            raise ModuleInstallationError(error_msg)
        except ModuleInstallationError:  raise 
        except Exception as e:
            error_msg = f"Module installation failed: {pip_install_str} - {str(e)}"
            if verbose: print(f"[MODULE] ❌ ERROR INSTALL: {pip_install_str}\n\n{str(e)}")
            raise ModuleInstallationError(error_msg)
        if verbose: print(f"[MODULE] ✅ installed    : {pip_install_str}")
        return True

    @staticmethod
    def check_module_newer_version(module_name: str) -> bool:
        """ Check if module has a newer version available on PyPI """
        if CheckFileDependencies.VERBOSE_def: print(f"check_module_newer_version '{module_name}'")
        pip_name, _, import_name = CheckFileDependencies._parse_module_requirement(module_name)
        if not CheckFileDependencies.is_module_available(import_name):  raise ModuleInstallationError(f"Module '{import_name}' is not installed.")
        current_version = CheckFileDependencies.get_installed_version(module_name)
        if not current_version: return False
        try:
            command = [sys.executable, "-m", "pip", "index", "versions", pip_name]
            success, stdout, stderr = CheckFileDependencies.run_cmd_command(command)
            if success and stdout:
                lines = stdout.strip().split('\n')
                for line in lines:
                    if 'Available versions:' in line:
                        try: 
                            latest_version = line.split('Available versions:')[-1].strip().split(',')[0].strip()
                            return Version(latest_version) > Version(current_version)
                        except Exception: pass
            try:
                import requests
                response = requests.get(f"https://pypi.org/pypi/{pip_name}/json")
                if response.status_code == 200: 
                    data = response.json()
                    latest_version = data['info']['version']  # .data hatası düzeltildi
                    return Version(latest_version) > Version(current_version)
            except ImportError:  pass
            except Exception: pass
            return False
        except Exception: return False


    @staticmethod
    def is_version_compatible(current_version: str, required_version: str) -> bool:
        """Check if the current version meets the required version."""
        if CheckFileDependencies.VERBOSE_def: print(f"check_version_compatibility '{current_version}' , '{required_version}'")
        required_version = required_version.strip()
        if not re.match(r'.*(>=|<=|==|!=|~=|>|<).*', required_version):  required_version = f">={required_version}"
        try: return Version(current_version) in SpecifierSet(required_version)
        except Exception as e: raise VersionComparisonError(f"Version comparison error: {str(e)} for current: {current_version} and required: {required_version}")


    @staticmethod
    def get_installed_version(module_name: str) -> str:
        """Get the installed version of a module. """
        if CheckFileDependencies.VERBOSE_def: print(f"get_installed_version '{module_name}'")
        pip_name, version_requirement, import_name = CheckFileDependencies._parse_module_requirement(module_name)
        try:
            if not CheckFileDependencies.is_module_available(import_name): 
                print(f"Module '{module_name} -> {import_name}' is not installed.")
                return ""
            module = importlib.import_module(import_name)
            if hasattr(module, '__version__'):
                result = getattr(module, '__version__', None)
                if result and isinstance(result, str): return str(result.strip())
            for attr in ['version', 'VERSION', '__VERSION__']:
                if hasattr(module, attr):
                    result = getattr(module, attr, None)
                    if result and isinstance(result, str): return str(result.strip())
            try: #build-in modules
                command = [sys.executable, "-m", "pip", "show", pip_name]
                success, stdout, stderr = CheckFileDependencies.run_cmd_command(command)
                if success and stdout:
                    for line in stdout.split('\n'):
                        if 'Version:' in line:
                            version = line.split('Version:')[1].strip().split(" ")[0].strip().split("\n")[0].strip()
                            if version: return version
            except:
                pass
            print(f"Module '{module_name} -> {import_name}' is installed but version could not be determined.")
            return ""
        except Exception as e: 
            print(f"Module '{module_name} -> module:{import_name}' version check failed: {str(e)}")
            return ""


    @staticmethod
    def is_module_available(module_name: str) -> Union[bool, Tuple[bool, str]]:
        """Determine if a module is present in the current Python environment."""
        if CheckFileDependencies.VERBOSE_def: print(f"is_module_available '{module_name}'")
        _, _, import_name = CheckFileDependencies._parse_module_requirement(module_name)
        try:
            return importlib.util.find_spec(import_name) is not None
        except (ImportError, ValueError, ModuleNotFoundError) as e:
            try:  return importlib.import_module(import_name) is not None, str(e)
            except Exception as e: return False, str(e)
        except Exception as e: return False, str(e)


    @staticmethod
    def run_cmd_command(command: List[str], timeout: int = TIMEOUT) -> Tuple[bool, str, str]:
        """ Run a command safely and return the result."""
        if CheckFileDependencies.VERBOSE_def: print(f"run_cmd_command '{command}'")
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired: return False, "", f"TIMEOUT : {timeout} -> {command}"
        except Exception as e:  return False, "", f"Komut çalıştırma hatası: {str(e)}"
    
    
    @staticmethod
    def _parse_module_requirement(module_requirement: str) -> Tuple[str, Optional[str], str]:
        """
        Parse a module requirement string and return a tuple of (pip_name, version_requirement, import_name).
        "venv-py|venv>=1.0.0" -> ("venv-py", ">=1.0.0", "venv")
        "numpy>=1.20.0"       -> ("numpy", ">=1.20.0", "numpy")
        "requests"            -> ("requests", None, "requests")
        """
        if CheckFileDependencies.VERBOSE_def: print(f"_parse_module_requirement '{module_requirement}'")
        # pip_name|Import_name verison
        if "|" in module_requirement:
            pip_part, import_part = [x.strip() for x in module_requirement.split("|", 1)]
            import_match = re.match(r'^([a-zA-Z0-9_\-\.]+)(>=|<=|==|!=|~=|>|<)(.+)$', import_part)
            if import_match: import_name, version_req = import_match.group(1), f"{import_match.group(2)}{import_match.group(3)}"
            else: import_name, version_req = import_part, None
            return pip_part, version_req, import_name
        else:
            match = re.match(r'^([a-zA-Z0-9_\-\.]+)((?:>=|<=|==|!=|~=|>|<).+)$', module_requirement.strip())
            if match:
                name = match.group(1)
                version_req = match.group(2)
                return name, version_req, name.replace("-", "_")
            else:
                name = module_requirement.strip()
                return name, None, name.replace("-", "_")
    
    

#===============================================================================







def USAGE_EXAMPLE():
    """ CheckFileDependencies sınıfının tüm özelliklerini gösteren kapsamlı kullanım örnekleri.
        Bu fonksiyon, modülün nasıl kullanılacağını adım adım gösterir. """
    
    print("=" * 80)
    print("🚀 CheckFileDependencies - KULLANIM ÖRNEKLERİ")
    print("=" * 80)



    # 1. TEMEL AYARLAR
    print("\n📋 1. TEMEL AYARLAR VE YAPILANDIRMA")
    print("-" * 50)

    # Mevcut ayarları göster
    print("🔧 Mevcut ayarlar:")
    CheckFileDependencies.print_class_static_vars()

    # Ayarları değiştir
    print("\n🔧 Ayarları değiştirme:")
    CheckFileDependencies.VERBOSE = True
    CheckFileDependencies.AUTO_UPDATE = False
    CheckFileDependencies.TIMEOUT = 60
    CheckFileDependencies.VERBOSE_def = False
    print("✅ Ayarlar güncellendi!")
    CheckFileDependencies.print_class_static_vars()



    
    # 2. TEK MODÜL KONTROLÜ
    print("\n\n📦 2. TEK MODÜL KONTROLÜ (ensure_module)")
    print("-" * 50)
    
    print("🔹 Basit modül kontrolü:")
    # Tek satır: CheckFileDependencies.ensure_module("requests")
    try:
        result = CheckFileDependencies.ensure_module("requests", verbose=True)
        print(f"✅ Sonuç: {result}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    print("\n🔹 Sürüm gereksinimi ile:")
    # Tek satır: CheckFileDependencies.ensure_module("numpy>=1.20.0", auto_update=True)
    try:
        result = CheckFileDependencies.ensure_module("numpy>=1.20.0", auto_update=True, verbose=True)
        print(f"✅ Sonuç: {result}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    
    print("\n🔹 Farklı pip/import ismi ile:")
    # Tek satır: CheckFileDependencies.ensure_module("Pillow|PIL>=8.0.0")
    try:
        result = CheckFileDependencies.ensure_module("Pillow|PIL>=8.0.0", verbose=True)
        print(f"✅ Sonuç: {result}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    


    
    # 3. ÇOKLU MODÜL KONTROLÜ
    print("\n\n📦 3. ÇOKLU MODÜL KONTROLÜ (check_multiple_modules)")
    print("-" * 50)
    
    modules_list = [
        "requests",
        "colorama>=0.4.0", 
        "six",
        "setuptools"
    ]
    
    print("🔹 Birden fazla modül kontrolü:")
    print(f"Kontrol edilecek modüller: {modules_list}")


    
    # Tek satır: results = CheckFileDependencies.check_multiple_modules(["requests", "colorama>=0.4.0"])
    try:
        results = CheckFileDependencies.check_multiple_modules(
            modules_list=modules_list,
            auto_update=False,
            verbose=True,
            timeout=60
        )
        print(f"\n📊 Detaylı sonuçlar:")
        for module, result in results.items():
            status = "✅" if result is True else "❌"
            print(f"  {status} {module}: {result}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    


    
    # 4. BOOLEAN SONUÇ KONTROLÜ
    print("\n\n✅ 4. BOOLEAN SONUÇ KONTROLÜ (check_multiple_modules_bool)")
    print("-" * 50)
    
    print("🔹 Tümü başarılı mı kontrolü:")
    # Tek satır: success = CheckFileDependencies.check_multiple_modules_bool(["requests", "six"])
    try:
        all_success = CheckFileDependencies.check_multiple_modules_bool(
            modules_list=modules_list,
            auto_update=False,
            verbose=False,
            timeout=60
        )
        print(f"📈 Tüm modüller başarılı: {'✅ EVET' if all_success else '❌ HAYIR'}")
        
        # Pratik kullanım örneği
        if all_success:
            print("🎉 Tüm bağımlılıklar hazır - Ana kodu çalıştırabilirsiniz!")
        else:
            print("⚠️  Bazı bağımlılıklar eksik - Lütfen sorunları çözün!")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    


    
    # 5. MODÜL DURUM BİLGİSİ
    print("\n\n📊 5. MODÜL DURUM BİLGİSİ (get_modules_status)")
    print("-" * 50)
    
    print("🔹 Modül durumlarını kontrol et (yüklemeden):")
    # Tek satır: status = CheckFileDependencies.get_modules_status(["requests", "numpy"])
    try:
        status_info = CheckFileDependencies.get_modules_status(
            modules_list=["requests", "colorama", "nonexistent-module-xyz"],
            verbose=False
        )
        
        print("\n📋 Durum raporu:")
        for module, info in status_info.items():
            print(f"\n  📦 {module}:")
            print(f"    • Pip adı: {info['pip_name']}")
            print(f"    • Import adı: {info['import_name']}")
            print(f"    • Yüklü: {'✅' if info['installed'] else '❌'}")
            print(f"    • Mevcut sürüm: {info['current_version'] or 'N/A'}")
            print(f"    • Uyumlu: {'✅' if info['version_compatible'] else '❌'}")
            print(f"    • Yeni sürüm var: {'🔄' if info['has_newer_version'] else '✅'}")
            if info['error']:
                print(f"    • Hata: {info['error']}")
                
    except Exception as e:
        print(f"❌ Hata: {e}")
    


    
    # 6. SÜRÜM İŞLEMLERİ
    print("\n\n🔄 6. SÜRÜM İŞLEMLERİ")
    print("-" * 50)
    
    test_module = "colorama"
    
    print(f"🔹 {test_module} modülü sürüm bilgileri:")
    try:
        # Tek satır: version = CheckFileDependencies.get_installed_version("colorama")
        current_version = CheckFileDependencies.get_installed_version(test_module)
        print(f"  📌 Mevcut sürüm: {current_version or 'Bulunamadı'}")
        
        # Tek satır: has_newer = CheckFileDependencies.check_module_newer_version("colorama")
        if current_version:
            has_newer = CheckFileDependencies.check_module_newer_version(test_module)
            print(f"  🔄 Yeni sürüm var: {'EVET' if has_newer else 'HAYIR'}")
            
            # Sürüm uyumluluğu testi
            # Tek satır: compatible = CheckFileDependencies.is_version_compatible("0.4.6", ">=0.4.0")
            compatible = CheckFileDependencies.is_version_compatible(current_version, ">=0.4.0")
            print(f"  ✅ Sürüm uyumlu (>=0.4.0): {'EVET' if compatible else 'HAYIR'}")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    


    
    # 7. ÖZEL DURUMLAR VE HATA YÖNETİMİ
    print("\n\n⚠️  7. ÖZEL DURUMLAR VE HATA YÖNETİMİ")
    print("-" * 50)
    
    print("🔹 Hatalı modül adı:")
    try:
        CheckFileDependencies.ensure_module("", verbose=False)
    except ValueError as e:
        print(f"  ✅ Beklenen hata yakalandı: {e}")
    
    print("\n🔹 Olmayan modül:")
    try:
        result = CheckFileDependencies.ensure_module("nonexistent-super-fake-module-xyz", verbose=False)
        print(f"  📊 Sonuç: {result}")
    except Exception as e:
        print(f"  ⚠️  Hata: {type(e).__name__}: {e}")
    
    print("\n🔹 Geçersiz sürüm formatı:")
    try:
        CheckFileDependencies.is_version_compatible("1.0.0", "invalid-version-format")
    except VersionComparisonError as e:
        print(f"  ✅ Beklenen hata yakalandı: {e}")
    


    
    # 8. PRAKTİK KULLANIM ÖRNEKLERİ
    print("\n\n🎯 8. PRAKTİK KULLANIM ÖRNEKLERİ")
    print("-" * 50)
    
    print("🔹 Script başlangıcında bağımlılık kontrolü:")
    print("""
    # Script başında:
    required_modules = ["requests", "pandas>=1.3.0", "matplotlib"]
    if CheckFileDependencies.check_multiple_modules_bool(required_modules):
        import requests, pandas as pd, matplotlib.pyplot as plt
        print("✅ Tüm modüller hazır!")
    else:
        print("❌ Eksik modüller var!")
        exit(1)
    """)
    
    print("\n🔹 Conditional import:")
    print("""
    # Opsiyonel modül kontrolü:
    if CheckFileDependencies.ensure_module("seaborn", verbose=False):
        import seaborn as sns
        print("Seaborn kullanılabilir")
    else:
        print("Seaborn olmadan devam ediliyor")
    """)
    
    print("\n🔹 Toplu güncelleme:")
    print("""
    # Tüm modülleri güncelle:
    modules = ["requests", "numpy", "pandas"]
    CheckFileDependencies.check_multiple_modules(modules, auto_update=True)
    """)
    


    
    # 9. TEK SATIRLIK KULLANIM ÖRNEKLERİ
    print("\n\n⚡ 9. TEK SATIRLIK KULLANIM ÖRNEKLERİ")
    print("-" * 50)
    
    examples = [
        'ensure_module("requests")',
        'ensure_module("numpy>=1.20.0", auto_update=True)',
        'check_multiple_modules(["requests", "pandas"])',
        'success = check_multiple_modules_bool(["numpy", "matplotlib"])',
        'version = get_installed_version("requests")',
        'status = get_modules_status(["numpy", "pandas"])',
        'compatible = is_version_compatible("1.0.0", ">=0.9.0")',
        'has_newer = check_module_newer_version("requests")',
        'update_module("numpy")',
        'install_module("new-package")'
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"  {i:2d}. {example}")
    


    
    # 10. SONUÇ VE TAVSİYELER
    print("\n\n🎉 10. SONUÇ VE TAVSİYELER")
    print("-" * 50)
    
    recommendations = [
        "✅ Production'da verbose=False kullanın",
        "✅ Timeout değerini ağ hızınıza göre ayarlayın", 
        "✅ auto_update=True'yu dikkatli kullanın",
        "✅ Sürüm gereksinimlerini net belirtin",
        "✅ Exception handling yapın",
        "✅ Script başında bağımlılık kontrolü yapın",
        "✅ Kritik modüller için check_multiple_modules_bool kullanın",
        "✅ Test ortamında önce deneyin"
    ]
    
    for rec in recommendations:
        print(f"  {rec}")
    
    print(f"\n{'='*80}")
    print("🎯 CheckFileDependencies kullanıma hazır!")
    print("📖 Daha fazla bilgi için: https://github.com/Mefamex/Python_Code_Snippets")
    print(f"{'='*80}")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python modül bağımlılıklarını kontrol et ve yükle/güncelle.")
    parser.add_argument("-r", "--requirements", type=str, default="requirements.txt",help="requirements.txt dosya yolu (varsayılan: requirements.txt)" )
    parser.add_argument("-v", "--verbose", action="store_true", help="Detaylı çıktı göster")
    parser.add_argument("-a", "--auto-update", action="store_true", help="Sürüm uyumsuzluklarında otomatik güncelle")
    parser.add_argument( "-t", "--timeout", type=int, default=300, help="Her pip işlemi için zaman aşımı (saniye)" )

    args = parser.parse_args()

    print(f"\n[CheckFileDependencies] requirements.txt kontrolü başlatılıyor: {args.requirements}\n")
    try:
        results = CheckFileDependencies.check_requirements_txt( requirements_path=args.requirements, auto_update=args.auto_update, verbose=args.verbose, timeout=args.timeout )
        failed = [k for k, v in results.items() if v is not True]
        if failed:
            print(f"\n❌ Eksik veya hatalı modüller ({len(failed)}):")
            for mod in failed:  print(f"  - {mod}: {results[mod]}")
            exit(1)
        else:
            print("\n✅ Tüm bağımlılıklar yüklü ve uyumlu!")
            exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        exit(2)
