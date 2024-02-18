# demo package py

## Build locally
```bash
python3 setup.py sdist bdist_wheel
```

## Installation locally

```bash
pip install dist/...whl
```

## Upload to pypi

```bash
pip install twine

```

```bash
twine upload dist/*
username = __token__
password = pypi-.........
```


```bash
pip install demopackagepy
```


## Minimum setup.py
```bash
from setuptools import setup, find_packages

setup(
    name="scrapethat",
    version="1.0.3",
    author="Mihaly Orsos",
    author_email="ormraat.pte@gmail.com",
    description="Tools for faster scraping",
    url="https://github.com/misrori/scrapethat",
    license="MIT",
    install_requires=["bs4", "requests", "pandas", "cloudscraper"],
    packages=find_packages()
)


```
