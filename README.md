# Load Brazilian cities and states from IBGE

This is a simple script to build a list of Brazilian cities and states from [IBGE](http://www.ibge.gov.br/english/) (using [Cidades](http://cidades.ibge.gov.br/) portal).

## Usage

Run `$ python3 cities.py` and you'll have 4 new files: `cities.csv`, `cities.json`, `states.csv` and `states.json`.

## Installation

This script requires [Python 3.5](https://python.org) and one `pip` installable package. If you have `python3` alreayd available these few lines should get you started: 

```console
$ git clone https://github.com/cuducos/brazilian-cities
$ cd brazilian-cities
$ python3 -m venv brazilian-cities
$ source brazilian-cities/bin/activate
$ python3 -m pip install -r requirements.txt
```

**If you use Windows** replace `source brazilian-cities/bin/activate` by `brazilian-cities\Scripts\activate`.

## File formats

### CSV

#### Cities

```csv
code,name,state
520005,Abadia de Goiás,GO
310010,Abadia dos Dourados,MG
520010,Abadiânia,GO
…
```

#### States

```csv
code,abbr,name
12,AC,Acre
27,AL,Alagoas
16,AP,Amapá
…
```

### JSON

#### Cities

```json
[
  {
    "name": "Abadia de Goiás",
    "code": "520005",
    "state": "GO"
  },
  {
    "name": "Abadia dos Dourados",
    "code": "310010",
    "state": "MG"
  },
  {
    "name": "Abadiânia",
    "code": "520010",
    "state": "GO"
  },
  …
]
```

#### States

```json
[
  {
    "name": "Acre",
    "abbr": "AC",
    "code": "12"
  },
  {
    "name": "Alagoas",
    "abbr": "AL",
    "code": "27"
  },
  {
    "name": "Amapá",
    "abbr": "AP",
    "code": "16"
  },
  …
]
```