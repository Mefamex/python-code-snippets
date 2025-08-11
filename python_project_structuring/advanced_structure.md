# Profesyonel Python Proje Yapısı

Kurumsal düzeyde Python projeleri için modern standartlara uygun, ölçeklenebilir, sürdürülebilir ve bakımı kolay bir kod tabanı oluşturmanıza yardımcı olan kapsamlı bir proje yapısı sunar. Bu yapı, ekip çalışmasını, test edilebilirliği ve sürekli entegrasyonu en iyi şekilde destekler.


## İçindekiler
- [Özellikler ve Faydalar](#özellikler-ve-faydalar)
- [Önemli Dosyaların İçerikleri](#önemli-dosyaların-i̇çerikleri)
  - [pyproject.toml](#pyprojecttoml)
  - [Makefile](#makefile)
  - [.gitignore](#gitignore)
  - [requirements-dev.txt](#requirements-devtxt)
  - [requirements-test.txt](#requirements-testtxt)
  - [tox.ini](#toxini)
  - [.pre-commit-config.yaml](#pre-commit-configyaml)



## Özellikler ve Faydalar

### ✅ Büyük Projeler İçin Uygun
- Modüler yapı ile kolay geliştirme
- Katmanlı mimari (core, api, data, external)
- Dependency injection friendly yapı

### ✅ Taşınabilir ve Anlaşılır
- Standart Python packaging (PEP 517/518)
- Açık klasör yapısı ve isimlendirme
- Kapsamlı dokümantasyon

### ✅ Kolay Dağıtım
- PyInstaller ile .exe oluşturma
- Docker containerization
- Wheel ve source distribution

### ✅ Sanal Ortam Yönetimi
- requirements.txt dosyaları
- Makefile ile otomatik kurulum
- pyproject.toml ile dependency yönetimi

### ✅ PEP8 Uyumlu
- Black ve isort entegrasyonu
- Flake8 linting
- MyPy type checking

### ✅ Git Entegrasyonu
- .gitignore ve .gitattributes
- GitHub Actions CI/CD
- Pre-commit hooks

### ✅ Test Altyapısı
- Pytest framework
- Unit, integration ve e2e testler
- Coverage raporlama

### ✅ Dokümantasyon
- README, CHANGELOG, CONTRIBUTING
- API dokümantasyonu
- Sphinx entegrasyonu

### ✅ Logging ve Hata Yönetimi
- Structlog kullanımı
- Özel exception sınıfları
- Konfigürasyonlu logging

### ✅ Performans ve Ölçeklenebilirlik
- Async/await desteği
- Efficient imports
- Profiling ve monitoring hazırlığı


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



<br><br>



## Önemli Dosyaların İçerikleri

### pyproject.toml
```toml
[build-system]
requires = ["setuptools>=65", "wheel", "setuptools-scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "my-awesome-project"
dynamic = ["version"]
description = "Profesyonel Python proje şablonu"
authors = [{name = "Your Name", email = "your.email@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"
keywords = ["python", "project", "template"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

dependencies = [
    "click>=8.0.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "structlog>=23.0.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.0.0",
    "pytest-xdist>=3.0.0",
    "pytest-benchmark>=4.0.0",
    "black>=23.0.0",
    "isort>=5.0.0",
    "flake8>=6.0.0",
    "flake8-docstrings>=1.7.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
    "tox>=4.0.0",
    "bandit>=1.7.0",
    "safety>=2.0.0",
]
docs = [
    "sphinx>=6.0.0",
    "sphinx-rtd-theme>=1.0.0",
    "myst-parser>=1.0.0",
    "sphinx-autodoc-typehints>=1.0.0",
]
build = [
    "pyinstaller>=5.0.0",
    "wheel>=0.40.0",
    "build>=0.10.0",
    "twine>=4.0.0",
]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.0.0",
    "pytest-xdist>=3.0.0",
    "pytest-benchmark>=4.0.0",
]

[project.scripts]
my-awesome-project = "my_awesome_project.cli:main"

[project.urls]
homepage = "https://github.com/username/my-awesome-project"
repository = "https://github.com/username/my-awesome-project"
documentation = "https://my-awesome-project.readthedocs.io"
changelog = "https://github.com/username/my-awesome-project/blob/main/CHANGELOG.md"
"Bug Tracker" = "https://github.com/username/my-awesome-project/issues"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools_scm]
write_to = "src/my_awesome_project/_version.py"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
src_paths = ["src", "tests"]

[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "-ra",
    "-q", 
    "--strict-markers",
    "--strict-config",
    "--cov=src/my_awesome_project",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=80"
]
testpaths = ["tests"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "e2e: marks tests as end-to-end tests",
    "benchmark: marks tests as performance benchmarks",
]
filterwarnings = [
    "error",
    "ignore::UserWarning",
    "ignore::DeprecationWarning",
]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### Makefile
```makefile
.PHONY: help install install-dev test test-all lint format clean build docs serve-docs security

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-15s %s\n", $1, $2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev,docs,build,test]"
	pre-commit install

test: ## Run tests with coverage
	pytest

test-all: ## Run all tests including slow ones
	pytest -m "not benchmark"

test-fast: ## Run fast tests only
	pytest -m "not slow and not integration"

test-integration: ## Run integration tests
	pytest -m "integration"

test-benchmark: ## Run performance benchmarks
	pytest -m "benchmark" --benchmark-only

lint: ## Run all linting tools
	flake8 src tests
	mypy src
	black --check src tests
	isort --check-only src tests

format: ## Format code with black and isort
	black src tests
	isort src tests

format-check: ## Check code formatting
	black --check --diff src tests
	isort --check-only --diff src tests

security: ## Run security checks
	bandit -r src/
	safety check

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build distribution packages
	python -m build

build-exe: ## Build executable with PyInstaller
	pyinstaller --onefile --name my-awesome-project src/my_awesome_project/__main__.py

publish: ## Publish to PyPI (requires authentication)
	python -m twine upload dist/*

publish-test: ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

docs: ## Build documentation
	cd docs && make html

docs-clean: ## Clean documentation build
	cd docs && make clean

serve-docs: ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000

venv: ## Create virtual environment
	python -m venv venv
	@echo "Activate virtual environment with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"

tox: ## Run tests in multiple Python versions
	tox

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

setup: venv install-dev ## Setup development environment
	@echo "Development environment ready!"
	@echo "Run 'source venv/bin/activate' to activate the virtual environment"

check: lint test security ## Run all checks (lint, test, security)

ci: check build ## Run CI pipeline locally

release-patch: ## Create a patch release
	python scripts/release.py patch

release-minor: ## Create a minor release
	python scripts/release.py minor

release-major: ## Create a major release
	python scripts/release.py major
```

### .gitignore
```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# Database
*.db
*.sqlite3

# Temporary files
tmp/
temp/
.tmp/

# Environment variables
.env
.env.local
.env.*.local

# Documentation builds
docs/_build/
docs/.doctrees/

# Jupyter Notebook
.ipynb_checkpoints

# mypy
.mypy_cache/
.dmypy.json
dmypy.json
```

### requirements-dev.txt
```txt
-r requirements.txt
-r requirements-test.txt
black>=23.0.0
isort>=5.0.0
flake8>=6.0.0
flake8-docstrings>=1.7.0
mypy>=1.0.0
pre-commit>=3.0.0
tox>=4.0.0
bandit>=1.7.0
safety>=2.0.0
pyinstaller>=5.0.0
wheel>=0.40.0
build>=0.10.0
twine>=4.0.0
```

### requirements-test.txt
```txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.0.0
pytest-xdist>=3.0.0
pytest-benchmark>=4.0.0
```

### tox.ini
```ini
[tox]
envlist = py39, py310, py311, py312, lint, type, security
isolated_build = true

[testenv]
deps = 
    -r requirements-test.txt
commands = pytest {posargs}

[testenv:lint]
deps = 
    flake8>=6.0.0
    flake8-docstrings>=1.7.0
    black>=23.0.0
    isort>=5.0.0
commands = 
    flake8 src tests
    black --check src tests
    isort --check-only src tests

[testenv:type]
deps = mypy>=1.0.0
commands = mypy src

[testenv:security]
deps = 
    bandit>=1.7.0
    safety>=2.0.0
commands = 
    bandit -r src/
    safety check

[testenv:docs]
deps = 
    sphinx>=6.0.0
    sphinx-rtd-theme>=1.0.0
    myst-parser>=1.0.0
commands = sphinx-build -b html docs docs/_build/html

[flake8]
max-line-length = 88
extend-ignore = E203, W503, E501
exclude = 
    .git,
    __pycache__,
    build,
    dist,
    *.egg-info,
    .venv,
    .tox
```

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile, black]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]

ci:
  autofix_commit_msg: |
    [pre-commit.ci] auto fixes from pre-commit.com hooks
  autofix_prs: true
  autoupdate_branch: ''
  autoupdate_commit_msg: '[pre-commit.ci] pre-commit autoupdate'
  autoupdate_schedule: weekly
  skip: []
  submodules: false
```
