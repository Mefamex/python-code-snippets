# PYTHON - VENV Create Project


Taşınabilir, sanal ortam ile, bilgisayarınızdaki diğer Python projelerinden bağımsız olarak, yeni bir Python projesi oluşturmak için aşağıdaki adımları takip edebilirsiniz.


## İÇİNDEKİLER
- [PYTHON - VENV Create Project](#python---venv-create-project)
  - [İÇİNDEKİLER](#i̇çi̇ndeki̇ler)
  - [CREATE PYTHON PROJECT BASE](#create-python-project-base)
  - [ADD MODULES](#add-modules)
  - [REMOVE MODULES](#remove-modules)
  - [UPDATE](#update)
  - [EXPORT MODULES](#export-modules)
  - [MOVE PROJECT](#move-project)



## CREATE PYTHON PROJECT BASE

- `uv` : kullanıcaktım ama çok eksiği var...

- `venv` modülü ile sanal ortam oluşturun.

``` bash
:: UPDATE : python packages
python -m pip install -U pip
python -m pip install -U wheel setuptools venv-py


:: CREATE PYTHON: Project Directory
mkdir [project_name]
cd [project_name]


:: UV-VENV : Create a Virtual Environment
python -m venv .venv 


:: ACTIVATE VENV
call .venv\Scripts\activate


:: INSTALL BASE 
python.exe -m pip install -U pip venv-py
python.exe -m pip freeze > requirements.txt
ECHO # -*- coding: utf-8 -*- >> main.py
python -c "import datetime;print('# Created on: '+datetime.datetime.now().isoformat(timespec='seconds')+'Z')" >> main.py
```



<br><br><br>



## ADD MODULES

- Sanal ortamın aktif olduğundan emin olun.

    ``` bash
    call .venv\Scripts\activate

    python.exe -m pip install -U requests
    ```



<br><br><br>


## REMOVE MODULES

- Sanal ortamın aktif olduğundan emin olun.
    ``` bash
    call .venv\Scripts\activate

    python.exe -m pip uninstall <package>
    ```



<br><br><br>



## UPDATE 

- Sanal ortamın aktif olduğundan emin olun.

    ``` bash
    call .venv\Scripts\activate

    python.exe -m pip install -U <package1> <package2> ...
    python.exe -m pip freeze > requirements.txt
    ```




<br><br><br>




## EXPORT MODULES

- Sanal ortamın aktif olduğundan emin olun.

- Sanal ortamın aktif olduğundan emin olun.
- Sanal ortamdaki tüm paketleri ``requirements.txt`` dosyasına yazdır

``` bash
call .venv\Scripts\activate

python.exe -m pip freeze > requirements.txt

:: Top level packages
python.exe -m pip list --not-required --format freeze > _indirect_packages.txt

```






<br><br><br>





## MOVE PROJECT



```bash
:: 1. Proje dizinine gidin
cd [project_name]

:: 2. Yeni ve temiz bir sanal ortam oluşturun
python -m venv .venv

:: 3. Yeni sanal ortamı aktive edin
call .venv\Scripts\activate

:: 4. Tüm bağımlılıkları uv.lock dosyasına göre senkronize edin
python -m pip install -U -r requirements.txt
```

