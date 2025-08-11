# -*- coding: utf-8 -*- 
#!/usr/bin/env python3 

"""
===========================================================
        ADVANCED PYTHON PROJECT STRUCTURE CREATOR
===========================================================

Description:
    Bu script, Python uygulamaları için gelişmiş bir klasör yapısı oluşturmayı amaçlamaktadır.
    Kullanıcıların projelerini daha iyi organize etmelerine yardımcı olur. Otomatik olarak
    modern Python projesi için gerekli tüm dosya ve klasörleri oluşturur.

Author:
    mefamex (info@mefamex.com) (https://mefamex.com)

Links: 
    - https://mefamex.com/projects/
    - https://github.com/Mefamex/python-code-snippets/

Features: 
    - Gelişmiş Python proje yapısı oluşturma
    - Src-layout pattern desteği
    - Test yapısı (unit, integration, e2e, performance)
    - GitHub Actions workflow'ları
    - Docker desteği
    - Dokümantasyon yapısı (Sphinx)
    - Pre-commit hooks
    - Otomatik dosya içeriği oluşturma

Modules:
    - CreateStructure: Ana proje yapısı oluşturucu sınıfı
    - GET_PROJECT_STRUCTURE: Proje dosya listesi fonksiyonu

Classes:
    - CreateStructure: Proje yapısı oluşturma ve yönetimi

Functions:
    - GET_PROJECT_STRUCTURE(): Proje dosya yapısını döndürür
    - write_py(): Python dosyaları için şablon içerik oluşturur
    - write_md(): Markdown dosyaları için şablon içerik oluşturur

Usage:
    python advanced_structure_create.py [proje_adı]
    
    Etkileşimli mod:
    - Enter: Mevcut proje adını kullan
    - "..": Bir üst dizine çık
    - ".": Mevcut klasör adını kullan
    - "klasör/": Belirtilen klasöre geç
    - "yeni_ad": Yeni proje adı belirle

Requirements:
    - Python 3.8+
    - os, sys, datetime modülleri (standart kütüphane)

Installation:
    Tek dosya, bağımlılık gerektirmez. Doğrudan çalıştırılabilir.

Documentation: 
    Dosya içinde detaylı açıklamalar ve kullanım örnekleri mevcut.

License:
    MIT Lisansı (https://opensource.org/licenses/MIT)

Changelog:
    - 1.0.1 (2025-08-11): Düzeltmeler ve iyileştirmeler
    - 1.0.0 (2025-08-10): İlk sürüm

Contributors:
    - mefamex (ana geliştirici)

Contact:
    E-posta: info@mefamex.com
    Web    : https://mefamex.com

Additional Information:
    Bu araç, modern Python geliştirme standartlarına uygun proje yapıları oluşturur.
    Src-layout pattern, pytest, tox, pre-commit, GitHub Actions gibi endüstri 
    standartlarını destekler.

Notes:
    - Mevcut dosyaların üzerine yazmaz, sadece boş dosyalara içerik ekler
    - Platform bağımsız çalışır (Windows/Linux/macOS)
    - Proje adında özel karakterler otomatik olarak temizlenir

Disclaimer and Legal Notice:
    Bu yazılım, herhangi bir garanti olmaksızın "olduğu gibi" sağlanmaktadır. 
    Yazar, bu yazılımın kullanımı sonucunda oluşabilecek herhangi bir zarardan sorumlu 
    değildir. Kullanıcılar, yazılımı kendi sorumlulukları altında kullanmalıdır.
    
    Bu yazılım, açık kaynak lisansı altında dağıtılmaktadır ve kullanıcılar, 
    lisans koşullarına uymakla yükümlüdür. Yazılımın herhangi bir şekilde değiştirilmesi, 
    dağıtılması veya kullanılması, lisans koşullarına uygun olarak yapılmalıdır.
===========================================================

"""

__version__ = "1.0.1"
__author__ = "mefamex"
__email__ = "info@mefamex.com"
__license__ = "MIT"
__status__ = "DEVELOPMENT"

__project_name__ = "advanced_py_project_structure_create"
__url__ = "https://mefamex.com/projects/"
__url_github__ = "https://github.com/Mefamex/python-code-snippets/"
__copyright__ = "Copyright © 2025 mefamex"
__description__ = "Python uygulamaları için gelişmiş klasör yapısı oluşturucu"
__date__ = "2025-08-10"
__date_modify__ = "2025-08-11"
__python_version__ = "3.8+" 
__dependencies__ = {
    "required": [],  # Standart kütüphane modülleri kullanılıyor
}

#================================================================================




#============================  IMPORTS =========================================
import os, sys, datetime
from time import sleep 
from typing import Final # for const variables
#================================================================================



#============================  CONSTS =========================================
PATH_SEP: Final[str] = os.path.sep
#================================================================================




#============================  PROJECT STRUCTURE =========================================

def GET_PROJECT_STRUCTURE(name: str) -> list[str]:
    project_name: str = name.strip() + ""
    return [p.replace("/", PATH_SEP) for p in  [
        "README.md",
        "LICENSE",
        ".gitignore",
        ".gitattributes",
        ".python-version",
        "pyproject.toml",
        "setup.py",
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
        "tox.ini",
        "Dockerfile",
        "docker-compose.yml",
        "Makefile",
        ".env.example",
        ".env",
        ".pre-commit-config.yaml",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        f"src/{project_name}/__init__.py",
        f"src/{project_name}/__main__.py",
        f"src/{project_name}/cli.py",
        f"src/{project_name}/config.py",
        f"src/{project_name}/constants.py",
        f"src/{project_name}/exceptions.py",
        f"src/{project_name}/utils.py",
        f"src/{project_name}/logger.py",
        f"src/{project_name}/version.py",
        f"src/{project_name}/core/__init__.py",
        f"src/{project_name}/core/base.py",
        f"src/{project_name}/core/models.py",
        f"src/{project_name}/core/services.py",
        f"src/{project_name}/api/__init__.py",
        f"src/{project_name}/api/routes.py",
        f"src/{project_name}/api/middleware.py",
        f"src/{project_name}/api/serializers.py",
        f"src/{project_name}/data/__init__.py",
        f"src/{project_name}/data/database.py",
        f"src/{project_name}/data/repositories.py",
        f"src/{project_name}/data/migrations/__init__.py",
        f"src/{project_name}/external/__init__.py",
        f"src/{project_name}/external/clients.py",
        f"src/{project_name}/external/adapters.py",
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/test_data/__init__.py",
        "tests/test_data/sample_files/.gitkeep",
        "tests/fixtures/__init__.py",
        "tests/fixtures/sample_data.py",
        "tests/unit/__init__.py",
        "tests/unit/test_core.py",
        "tests/unit/test_utils.py",
        "tests/unit/test_config.py",
        "tests/unit/test_logger.py",
        "tests/unit/test_services.py",
        "tests/integration/__init__.py",
        "tests/integration/test_api.py",
        "tests/integration/test_database.py",
        "tests/integration/test_external_services.py",
        "tests/e2e/__init__.py",
        "tests/e2e/test_workflows.py",
        "tests/performance/__init__.py",
        "tests/performance/test_benchmarks.py",
        "docs/conf.py",
        "docs/index.rst",
        "docs/installation.md",
        "docs/usage.md",
        "docs/api-reference.md",
        "docs/development.md",
        "docs/deployment.md",
        "docs/architecture.md",
        "docs/troubleshooting.md",
        "docs/changelog.md",
        "docs/_static/custom.css",
        "docs/_templates/.gitkeep",
        "docs/assets/images/.gitkeep",
        "docs/assets/diagrams/.gitkeep",
        "scripts/setup.sh",
        "scripts/setup.bat",
        "scripts/deploy.py",
        "scripts/migrate.py",
        "scripts/generate_docs.py",
        "scripts/check_dependencies.py",
        "scripts/release.py",
        "data/raw/.gitkeep",
        "data/processed/.gitkeep",
        "data/external/.gitkeep",
        "data/samples/.gitkeep",
        "configs/development.yml",
        "configs/production.yml",
        "configs/staging.yml",
        "configs/testing.yml",
        "configs/logging.yml",
        "examples/basic_usage.py",
        "examples/advanced_features.py",
        "examples/integration_samples/.gitkeep",
        "logs/.gitkeep",
        "build/.gitkeep",
        "dist/.gitkeep",
        ".github/workflows/ci.yml",
        ".github/workflows/cd.yml",
        ".github/workflows/tests.yml",
        ".github/workflows/security.yml",
        ".github/workflows/release.yml",
        ".github/workflows/docs.yml",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/ISSUE_TEMPLATE/security_report.md",
        ".github/pull_request_template.md",
        ".github/dependabot.yml"
    ] ]
#================================================================================





#============================ MAIN CLASS =========================================

class CreateStructure:
    def __init__(self, project_name: str = "my_awesome_project") -> None:
        self.PROJECT_NAME = project_name + ""

    def run(self) -> None:
        self.set_project_name()
        self.create_folder()
        self.create_structure() 
        print(f"[INFO] Proje yapısı oluşturuldu: {self.PROJECT_NAME}")
    
    def set_project_name(self) -> None:
        sleep(0.5)
        print(f'\n\n"name"    -> yeni isim gir\n".."      -> bir üst klasöre çık\n"."       -> mevcut klasörü kullan\n"klasör{os.path.sep}" -> o klasöre geç\n')
        print(f'\n[INFO] Proje adı    : "{self.PROJECT_NAME}" ({os.getcwd()})\n')
        inp= input("[ASK ] Proje oluşturulsun mu?\n             (enter) / (yeni proje adı) ->").strip()
        if inp.lower() in ["y", "yes", ""]:  
            print(f"\n[INFO] Proje oluşturuluyor : \n         ->  {self.PROJECT_NAME}\n         ->  {os.path.abspath(self.PROJECT_NAME)}\n")
            return
        elif inp.lower() == "..":
            os.chdir("..")
        elif inp.lower() == ".": 
            self.PROJECT_NAME = os.path.basename(os.getcwd())
            os.chdir("..")
        elif inp.endswith(os.path.sep):
            os.chdir(inp)
        else:
            self.PROJECT_NAME = inp+""
            print(f'[OKEY] ')
        self.set_project_name()
        sleep(0.5)

    def create_folder(self):
        """ Create the project folder and chdir"""
        os.makedirs(self.PROJECT_NAME, exist_ok=True)
        os.chdir(self.PROJECT_NAME)
        print(f"\n[INFO] Proje klasörü oluşturuldu: {self.PROJECT_NAME}")
        print(f"[INFO] Proje klasörüne geçildi  : {os.getcwd()}\n")


    def create_structure(self) -> None:
        """ Dont forget: this function run on {PROJECT_NAME}"""
        NotEmpty = []
        structure = GET_PROJECT_STRUCTURE(self.PROJECT_NAME)
        base_depth = os.path.abspath(".").count(os.sep)
        for path in structure:
            full_path = os.path.join(path)
            dir_name = os.path.dirname(full_path)
            if dir_name and not os.path.exists(dir_name): os.makedirs(dir_name, exist_ok=True)
            if not path.endswith(os.path.sep):
                with open(full_path, "a", encoding="utf-8") as f: f.write("")
                depth = full_path.count(os.sep) - base_depth
                indent = "│    " * depth
                print(f"{indent}├── {os.path.basename(full_path)}",end="")
                isEmpty = True
                if full_path.endswith(".py"):
                    isEmpty = self.write_py(os.path.dirname(full_path), os.path.basename(full_path))
                if full_path.endswith(".md"):
                    isEmpty = self.write_md(os.path.dirname(full_path), os.path.basename(full_path))
                if isEmpty:print()
                else: 
                    print("   [ ! NOT EMPTY]")
                    NotEmpty += [full_path]
            sleep(0.05)
        if NotEmpty: 
            print(f"\n\n[INFO] Not empty files found:")
            for path in NotEmpty:
                print(f" - {path}")

    def write_md(self, root:str, file_name:str) -> bool:
        """ returns: bool: file is empty ? """
        relative_path= os.path.relpath(os.path.join(root, file_name), start=".")
        isEmpty = os.path.getsize(os.path.join(root, file_name)) == 0
        with open(os.path.join(root, file_name), "a", encoding="utf-8") as md_file: md_file.write(f'# {(file_name[:-3] if file_name.endswith(".md") else  file_name).upper()}\n\n> **project**: {self.PROJECT_NAME}<br>\n> **created**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>\n> **folder** : {relative_path}\n\n')
        return isEmpty

    def write_py(self, root:str, file_name:str) -> bool:
        """ returns: bool: file is empty ? """
        relative_path= os.path.relpath(os.path.join(root, file_name), start=".")
        isEmpty = os.path.getsize(os.path.join(root, file_name)) == 0
        with open(os.path.join(root, file_name), "a", encoding="utf-8") as py_file: py_file.write(f'# -*- coding: utf-8 -*-\n# created at: {datetime.datetime.now().isoformat(timespec="seconds")}Z\n\n"""\n===========================================================\n        {(relative_path).replace(os.path.sep," -> ")}\n===========================================================\n\nDescription:\nAuthor: Name (mail@site.com) (https://website.com)\nLinks: - https://github.com/\nFeatures: -\nModules: -\nClasses: -\nFunctions: -\nUsage: \nRequirements: -\nInstallation: -\nDocumentation: -\nLicense: -\nChangelog: - 1.0.0 ({datetime.datetime.now().strftime("%Y-%m-%d")}): created by autoStructer\nContributors: -\nContact: -\nAdditional Information: \nNotes: -\nDisclaimer and Legal Notice: \n\n===========================================================\n"""\n\n\nif __name__ == "__main__":\n    pass\n\n')
        return isEmpty







if __name__ == "__main__":
    structer = CreateStructure()
    if len(sys.argv) > 1: structer.PROJECT_NAME = sys.argv[1].strip()
    structer.run()

















#=================================================================================

"""

## Dizin Yapısı
```
my_awesome_project/
│
├── README.md                   # Ana proje dokümantasyonu
├── LICENSE                     # Lisans dosyası
├── .gitignore                  # Git ignore kuralları
├── .gitattributes              # Git attributları
├── .python-version             # Python versiyon tanımı (pyenv için)
├── pyproject.toml              # Modern Python proje konfigürasyonu
├── setup.py                    # Backward compatibility için (opsiyonel)
├── requirements.txt            # Üretim bağımlılıkları
├── requirements-dev.txt        # Geliştirme bağımlılıkları
├── requirements-test.txt       # Test bağımlılıkları
├── tox.ini                     # Multi-environment testing
├── Dockerfile                  # Docker containerization
├── docker-compose.yml          # Multi-container setup
├── Makefile                    # Otomatik komutlar
├── .env.example                # Örnek environment dosyası
├── .env                        # Gerçek environment (git'te ignore)
├── .pre-commit-config.yaml     # Pre-commit hooks konfigürasyonu
├── CHANGELOG.md                # Versiyon değişiklikleri
├── CONTRIBUTING.md             # Katkıda bulunma rehberi
├── SECURITY.md                 # Güvenlik politikası
│
├── src/                        # Kaynak kod ana dizini
│   └── my_awesome_project/     # Ana paket
│       ├── __init__.py         # Paket init dosyası (__version__ içermeli)
│       ├── __main__.py         # CLI entry point
│       ├── cli.py              # Command line interface
│       ├── config.py           # Konfigürasyon yönetimi
│       ├── constants.py        # Sabitler
│       ├── exceptions.py       # Özel hata sınıfları
│       ├── utils.py            # Yardımcı fonksiyonlar
│       ├── logger.py           # Logging konfigürasyonu
│       ├── version.py          # Versiyon yönetimi
│       │
│       ├── core/               # Çekirdek modüller
│       │   ├── __init__.py
│       │   ├── base.py         # Temel sınıflar
│       │   ├── models.py       # Veri modelleri
│       │   └── services.py     # İş mantığı servisleri
│       │
│       ├── api/                # API katmanı (eğer web uygulaması ise)
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   ├── middleware.py
│       │   └── serializers.py
│       │
│       ├── data/                 # Veri katmanı
│       │   ├── __init__.py
│       │   ├── database.py       # Veritabanı bağlantıları
│       │   ├── repositories.py   # Veri erişim katmanı
│       │   └── migrations/       # Veritabanı migrasyonları
│       │       └── __init__.py
│       │
│       └── external/             # Dış servis entegrasyonları
│           ├── __init__.py
│           ├── clients.py        # API clientları
│           └── adapters.py       # Adaptör pattern
│
├── tests/                        # Test dosyaları
│   ├── __init__.py
│   ├── conftest.py               # pytest konfigürasyonu
│   ├── test_data/                # Test veri dosyaları
│   │   ├── __init__.py
│   │   └── sample_files/
│   ├── fixtures/                 # Test fixture'ları
│   │   ├── __init__.py
│   │   └── sample_data.py
│   ├── unit/                     # Unit testler
│   │   ├── __init__.py
│   │   ├── test_core.py
│   │   ├── test_utils.py
│   │   ├── test_config.py
│   │   ├── test_logger.py
│   │   └── test_services.py
│   ├── integration/              # Entegrasyon testleri
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   ├── test_database.py
│   │   └── test_external_services.py
│   ├── e2e/                      # End-to-end testler
│   │   ├── __init__.py
│   │   └── test_workflows.py
│   └── performance/              # Performans testleri
│       ├── __init__.py
│       └── test_benchmarks.py
│
├── docs/                      # Dokümantasyon
│   ├── conf.py                # Sphinx konfigürasyonu
│   ├── index.rst              # Ana dokümantasyon (RST format)
│   ├── installation.md        # Kurulum rehberi
│   ├── usage.md               # Kullanım rehberi
│   ├── api-reference.md       # API referansı
│   ├── development.md         # Geliştirici rehberi
│   ├── deployment.md          # Deploy rehberi
│   ├── architecture.md        # Mimari dokümantasyonu
│   ├── troubleshooting.md     # Sorun giderme
│   ├── changelog.md           # Değişiklik geçmişi
│   ├── _static/               # Statik dosyalar (CSS, JS)
│   │   └── custom.css
│   ├── _templates/            # Sphinx şablonları
│   └── assets/                # Dokümantasyon görselleri
│       ├── images/
│       └── diagrams/
│
├── scripts/                   # Yardımcı scriptler
│   ├── setup.sh               # Kurulum scripti (Unix)
│   ├── setup.bat              # Kurulum scripti (Windows)
│   ├── deploy.py              # Deploy scripti
│   ├── migrate.py             # Veritabanı migration
│   ├── generate_docs.py       # Dokümantasyon oluşturma
│   ├── check_dependencies.py  # Dependency kontrolü
│   └── release.py             # Release otomasyonu
│
├── data/                      # Veri dosyaları
│   ├── raw/                   # Ham veri
│   ├── processed/             # İşlenmiş veri
│   ├── external/              # Dış kaynak veriler
│   └── samples/               # Örnek veriler
│
├── configs/                   # Konfigürasyon dosyaları
│   ├── development.yml
│   ├── production.yml
│   ├── staging.yml            # Staging ortamı
│   ├── testing.yml
│   └── logging.yml
│
├── examples/                  # Kullanım örnekleri
│   ├── basic_usage.py
│   ├── advanced_features.py
│   └── integration_samples/
│
├── logs/                      # Log dosyaları (git'te ignore)
│   └── .gitkeep
│
├── build/                     # Build çıktıları (git'te ignore)
│   └── .gitkeep
│
├── dist/                      # Dağıtım dosyaları (git'te ignore)
│   └── .gitkeep
│
├── .github/                   # GitHub Actions ve templates
    ├── workflows/
    │   ├── ci.yml             # Continuous Integration
    │   ├── cd.yml             # Continuous Deployment
    │   ├── tests.yml          # Test otomasyonu
    │   ├── security.yml       # Security scanning
    │   ├── release.yml        # Release otomasyonu
    │   └── docs.yml           # Documentation build
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── feature_request.md
    │   └── security_report.md
    ├── pull_request_template.md
    └── dependabot.yml         # Dependency updates
```
"""