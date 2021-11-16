# Load Brazilian cities and states from IBGE

This is a simple script to build a list of Brazilian cities and states from [IBGE](http://www.ibge.gov.br/english/) (using [Cidades](http://cidades.ibge.gov.br/) portal).

## Usage

This script requires [Python 3.5](https://python.org) or newer, and no external dependencies.

Run `$ python cities.py` and you'll have 4 new files: `cities.csv`, `cities.json`, `states.csv` and `states.json`.

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
