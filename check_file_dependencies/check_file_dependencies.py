#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 

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
    - Sürüm uyumluluğu kontrolü (>=, <=, ==, !=, >, <, ~=)
    - Otomatik modül güncelleme özelliği
    - Detaylı hata yönetimi ve özel exception sınıfları
    - Verbose mod ile detaylı çıktı kontrolü
    - Timeout yönetimi

Modules:
    - subprocess: Pip komutlarının çalıştırılması için
    - sys: Python sistem bilgileri ve modül yolları
    - importlib: Modül bulma ve import işlemleri
    - re: Sürüm gereksinimlerinin parsing işlemi
    - warnings: Uyarı mesajları için
    - typing: Type hints desteği

Classes:
    - CheckFileDependencies: Ana bağımlılık kontrolü sınıfı
    - DependencyError: Temel bağımlılık hatası
    - ModuleInstallationError: Modül yükleme hatası
    - ModuleUpdateError: Modül güncelleme hatası
    - VersionComparisonError: Sürüm karşılaştırma hatası

Functions:
    - ensure_module(module_name, auto_update, verbose): Tek modül kontrolü
    - check_multiple_modules(modules_list, auto_update, verbose): Çoklu modül kontrolü
    - get_installed_version(module_name): Yüklü modül sürümünü getir
    - compare_versions(current_version, required_version): Sürüm karşılaştırması

Usage:
    1. Modülleri import edin ve CheckFileDependencies sınıfını kullanın.
    2. Kontrol edilecek modül(ler)i belirtin (sürüm gereksinimleri opsiyonel).
    3. Tek modül: `CheckFileDependencies.ensure_module("numpy>=1.20.0")`
    4. Çoklu modül: `CheckFileDependencies.check_multiple_modules(["requests", "pandas>=1.3.0"])`
    5. Sonuç olarak modüller otomatik yüklenecek/güncellenecek ve kontrol edilecektir.

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

Installation:
    1. Tek dosya olarak kullanım:
        - Bu dosyayı projenize kopyalayın
        - Python -> from check_file_dependencies import CheckFileDependencies

Documentation: 
    - Detaylı kullanım örnekleri: README.md
    - API dokümantasyonu: Kod içi docstring'ler
    - Online dokümantasyon: https://github.com/Mefamex/Python_Code_Snippets

License:
    MIT Lisansı (https://opensource.org/licenses/MIT)

Changelog:
    - 1.0.0 (2025-07-19): First stable release

Contributors: None

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

Notes:
    - Modül yükleme işlemleri pip üzerinden yapılır
    - İnternet bağlantısı gereklidir (yeni modül yüklemek için)
    - Timeout değeri varsayılan 300 saniyedir
    - Verbose mod varsayılan olarak açıktır

Disclaimer and Legal Notice:
    Bu yazılım, herhangi bir garanti olmaksızın "olduğu gibi" sağlanmaktadır.
    Yazar, bu yazılımın kullanımı sonucunda oluşabilecek zararlardan sorumlu değildir.
    Kullanıcılar, yazılımı kendi sorumlulukları altında kullanmalıdır.
    
    MIT Lisansı kapsamında açık kaynak olarak dağıtılır ve kullanıcılar lisans 
    koşullarına uymakla yükümlüdür. Yazılımın değiştirilmesi, dağıtılması veya 
    kullanılması lisans koşullarına uygun olmalıdır.
===========================================================

"""

__version__ = "1.0.0"
__author__ = "Mefamex"
__email__ = "info@mefamex.com"
__license__ = "MIT"
__status__ = "STABLE"

__project_name__ = "check_file_dependencies"
__url__ = "https://mefamex.com"
__url_github__ = "https://github.com/Mefamex/Python_Code_Snippets"
__copyright__ = "Copyright (c) 2025 Mefamex"
__description__ = "Python modül bağımlılıklarını otomatik kontrol eden, yükleyen ve güncelleyen araç"
__date__ = "2025-07-19"
__date_modify__ = "2025-07-19"
__python_version__ = ">=3.6" 
__dependencies__ = {
    "subprocess": "built-in",
    "sys": "built-in", 
    "importlib": "built-in",
    "re": "built-in",
    "warnings": "built-in",
    "typing": "built-in"
}
#===============================================================================


#============================ IMPORTS ==========================================
import subprocess, sys, importlib, importlib.util, re, warnings
from typing import Optional, List, Union, Tuple, Dict, Any
#===============================================================================


#============================ CUSTOM EXCEPTIONS ============================
class DependencyError(Exception): pass
class ModuleInstallationError(DependencyError): pass
class ModuleUpdateError(DependencyError): pass
class VersionComparisonError(DependencyError): pass
#===============================================================================


#============================ MAIN CLASS =======================================
class CheckFileDependencies:
    # STATIC VARIABLES
    TIMEOUT    : int  = 300
    AUTO_UPDATE: bool = True
    VERBOSE    : bool = True
    ##########################
    
    @staticmethod
    def ensure_module(module_name: str, auto_update: Optional[bool] = None, verbose: Optional[bool] = None, time_out: Optional[int] = None) -> bool:
        """
        Verilen modülü yüklü olup olmadığını kontrol eder. 
        
        verbose: eğer false ise, modülün yüklü olduğunu söylemez.
        auto_update: eğer true ise, modülün güncel olup olmadığını kontrol eder.
        
        Eğer modül yüklü değilse, yükler.
        Eğer modül yüklü ise ve auto_update true ise, modülü günceller
        Eğer modül yüklü değilse ve yüklenemezse, hata oluşturur.
        Eğer modül yüklü ise ve güncellenemezse, hata oluşturur.
        Eğer modül yüklü ise ve güncel ise, hiçbir şey yapmaz. verbose true ise, modülün yüklü olduğunu söyler.
        """
        if auto_update is None: auto_update = CheckFileDependencies.AUTO_UPDATE
        if verbose is None: verbose = CheckFileDependencies.VERBOSE
        if time_out is not None: CheckFileDependencies.TIMEOUT = time_out
        if not isinstance(module_name, str) or not module_name.strip(): raise ValueError("module_name have to be a non-empty string")
        parsed_name, version_requirement = CheckFileDependencies._parse_module_requirement(module_name)
        try:
            is_available = CheckFileDependencies._is_module_available(parsed_name)
            if is_available:
                current_version = CheckFileDependencies.get_installed_version(parsed_name)
                if version_requirement and current_version:
                    try:
                        version_ok = CheckFileDependencies.compare_versions(current_version, version_requirement)
                        if not version_ok:
                            print(f"[MODULE] ⚠️  version mismatch: {parsed_name} (current: {current_version}, required: {version_requirement})")
                            success, stdout, stderr = CheckFileDependencies._run_pip_command([ sys.executable, "-m", "pip", "install", "--upgrade", module_name ])
                            if not success:
                                error_msg = f"Modül güncelleme başarısız: {parsed_name}\nHata: {stderr}"
                                print(f"[MODULE] ❌ ERROR       : {parsed_name}\n\n{error_msg}")
                                raise ModuleUpdateError(error_msg)
                            if verbose: print(f"[MODULE] 🔄 updated     : {parsed_name}")
                            return True
                    except VersionComparisonError as e:
                        print(f"[MODULE] ⚠️  version check failed: {parsed_name} - {str(e)}")
                        warnings.warn(f"Versiyon kontrolü başarısız: {str(e)}")
                # AUTO UPDATE
                if auto_update and not version_requirement:
                    if verbose: print(f"[MODULE] 🔄 updating    : {parsed_name}")
                    success, stdout, stderr = CheckFileDependencies._run_pip_command([sys.executable, "-m", "pip", "install", "--upgrade", parsed_name])
                    if not success:
                        error_msg = f"Modül güncelleme başarısız: {parsed_name}\nHata: {stderr}"
                        print(f"[MODULE] ❌ ERROR       : {parsed_name}\n\n{error_msg}")
                        raise ModuleUpdateError(error_msg)
                    if verbose: print(f"[MODULE] ✅ updated     : {parsed_name}")
                    return True
                if verbose: print(f"[MODULE] ✅ ready to use: {parsed_name}{f" (v{current_version})" if current_version else ""}")
                return True
            else:
                print(f"[MODULE] ❓ not exist   : {parsed_name}\n[MODULE] 📥 downloading : {module_name}")
                success, stdout, stderr = CheckFileDependencies._run_pip_command([ sys.executable, "-m", "pip", "install", module_name ])
                if not success:
                    if verbose: print(f"[MODULE] ❌ ERROR       : {parsed_name}\n\n{f"Modül yükleme başarısız: {module_name}\nHata: {stderr}"}")
                    raise ModuleInstallationError(f"Modül yükleme başarısız: {module_name}\nHata: {stderr}")
                if not CheckFileDependencies._is_module_available(parsed_name):
                    print(f"[MODULE] ❌ ERROR       : {parsed_name}\n\n{f"Modül yüklendi ama import edilemiyor: {parsed_name}"}")
                    raise ModuleInstallationError(f"Modül yüklendi ama import edilemiyor: {parsed_name}")
                if verbose: print(f"[MODULE] ✅ installed   : {parsed_name}")
                return True
        except (ModuleInstallationError, ModuleUpdateError, VersionComparisonError): raise
        except Exception as e:
            print(f"[MODULE] ❌ ERROR       : {parsed_name}\n\n{ f"Beklenmeyen hata: {parsed_name} - {str(e)}"}")
            raise DependencyError( f"Beklenmeyen hata: {parsed_name} - {str(e)}")
    
    @staticmethod
    def check_multiple_modules(modules_list: List[str], auto_update: Optional[bool] = None, verbose: Optional[bool] = None, time_out: Optional[int] = None) -> Dict[str, bool]:
        """ Check multiple modules for dependencies and return a dictionary with results."""
        if auto_update is None: auto_update = CheckFileDependencies.AUTO_UPDATE
        if verbose is None: verbose = CheckFileDependencies.VERBOSE
        if time_out is not None: CheckFileDependencies.TIMEOUT = time_out
        if not isinstance(modules_list, (list, tuple)) or not modules_list: raise ValueError("modules_list have to be a non-empty list ")
        results, failed_modules = {}, []
        print(f"\n[MODULE] Starting dependency check for {len(modules_list)} modules...\n{"=" * 60}")
        for module in modules_list:
            try:
                result = CheckFileDependencies.ensure_module(module, auto_update=auto_update, verbose=verbose)
                results[module] = result
            except Exception as e:
                results[module] = False
                failed_modules.append((module, str(e)))
                print(f"[MODULE] ❌ Failed: {module}")
        print(f"{"=" * 60}\n[MODULE] Summary: {sum(1 for r in results.values() if r)}/{len(modules_list)} successful")
        if failed_modules: print(f"[MODULE] Failed modules:\n" + "\n".join([f"  - {module}: {error}" for module, error in failed_modules]))
        return results


    @staticmethod
    def _run_pip_command(command: List[str], timeout: int = TIMEOUT) -> Tuple[bool, str, str]:
        """ Run a pip command safely and return the result."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired: return False, "", f"TIMEOUT : {timeout} -> {command}"
        except Exception as e:  return False, "", f"Komut çalıştırma hatası: {str(e)}"


    @staticmethod
    def _parse_module_requirement(module_requirement: str) -> Tuple[str, Optional[str]]:
        """ Parse modul requirement string to extract module name and version. "numpy>=1.20.0" -> ("numpy", ">=1.20.0") """
        match = re.match(r'^([a-zA-Z0-9_\-\.]+)(>=|<=|==|!=|~=|>|<)(.+)$', module_requirement.strip())
        if match: return match.group(1), f"{match.group(2)}{match.group(3)}"
        else: return module_requirement.strip(), None


    @staticmethod
    def get_installed_version(module_name: str) -> Optional[str]:
        """ return the installed version of the module or None if not found. """
        try:
            import pkg_resources
            return pkg_resources.get_distribution(module_name).version
        except:
            try:
                if sys.version_info >= (3, 8):
                    import importlib.metadata
                    return importlib.metadata.version(module_name)
            except: pass
            try:
                module = importlib.import_module(module_name)
                return getattr(module, '__version__', None)
            except:  return None
    
    
    @staticmethod
    def compare_versions(current_version: str, required_version: str) -> bool:
        """ Compare two version strings and return True if current_version meets the required_version condition."""
        try:
            match = re.match(r'^(>=|<=|==|!=|~=|>|<)(.+)$', required_version)
            if not match: raise VersionComparisonError(f"Geçersiz versiyon formatı: {required_version}")
            op, target = match.groups()
            def parse_version(v):
                try: return tuple(map(int, v.split(".")))
                except ValueError: return v
            current_v, target_v = parse_version(current_version), parse_version(target)
            ops = {
                ">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b,  "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
                ">": lambda a, b: a > b, "<": lambda a, b: a < b, "~=": lambda a, b: isinstance(a, tuple) and isinstance(b, tuple) and  a >= b and a[:-1] == b[:-1]
            }
            if op not in ops: raise VersionComparisonError(f"Desteklenmeyen operatör: {op}")
            return ops[op](current_v, target_v)
        except Exception as e: raise VersionComparisonError(f"Versiyon karşılaştırma hatası: {str(e)}")

    @staticmethod
    def _is_module_available(module_name: str) -> bool:
        """ Check if a module is available in the current environment. """
        try:
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except (ImportError, ValueError, ModuleNotFoundError):
            try:
                importlib.import_module(module_name)
                return True
            except: return False
#===============================================================================


#============================ USAGE EXAMPLE ====================================
"""
CheckFileDependencies.TIMEOUT = 30
CheckFileDependencies.AUTO_UPDATE = True
CheckFileDependencies.VERBOSE = True

moduleList = [
    "numpy>=1.20.0",
    "requests",
    "importlib"
]

if not CheckFileDependencies.check_multiple_modules(moduleList):
    print("[MODULE] ❌ Some modules are missing or incompatible.")
    raise SystemExit(1)


======================== ONE LINE EXAMPLE ======================================

CheckFileDependencies.check_multiple_modules([
    "numpy>=1.20.0",
    "requests",
    "importlib"
],auto_update=False, verbose=True)

"""
#===============================================================================








