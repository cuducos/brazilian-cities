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
name,state
Abadia de Goiás,GO
Abadia dos Dourados,MG
Abadiânia,GO
…
```

#### States

```csv
abbr,name
AC,Acre
AL,Alagoas
AP,Amapá
…
```

### JSON

#### Cities

```json
[
  {
    "name": "Abadia de Goiás",
    "state": "GO"
  },
  {
    "name": "Abadia dos Dourados",
    "state": "MG"
  },
  {
    "name": "Abadiânia",
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
    "abbr": "AC"
  },
  {
    "name": "Alagoas",
    "abbr": "AL"
  },
  {
    "name": "Amap\u00e1",
    "abbr": "AP"
  },
  …
]
```