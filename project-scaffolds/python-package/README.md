# cluedo


## Running Modules

### Webserver

### Google news crawler

### Cluedo database processor

### Training

## Prerequisite

* python 3.5+
* setuptools (pip install setuptools)
* wheel (pip install wheel)

## Setup virtual env

* python -m venv .env
* activate virtual env : .env\Scripts\activate (win)
* pip install -r requirements.txt

## Settings

### Application environment variables

```sh
export CLUEDO_HOME=/path/to/cluedo/home

# default /<user_home>/cluedo
```

### DB
```sh
settings.py 

DATABASE = {
    'TYPE' : 'sqlite3',
    'NAME' : 'sqlite:///<>path>/<dbname>.db',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    'CONF': {}
}
```

## Installation

```sh
./scripts/build.sh
```

## Initialize DB

```sh
cluedo-initdb
```

## Setup scrapy

### Running google news spider
> configure settings.py
* SCRAPY_OUTPUT_DIR
* SCRAPY_GNEWS_REGION_CODE


> install cluedo package <br/>

> cluedo-gnews-spider
