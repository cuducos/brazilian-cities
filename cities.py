import re
from csv import DictWriter
from json import dump, loads
from urllib.request import urlopen


CITIES_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/aniversarios"
STATES_URL = "https://cidades.ibge.gov.br/dist/main-client.js"
STATES_MARKER = "exports.ufs ="


def get_states(url=None):
    url = url or STATES_URL

    print("Fetching", url)
    with urlopen(url) as response:
        content = response.read().decode("utf8")

    start = content.index(STATES_MARKER) + len(STATES_MARKER)
    end = content.index("]", start) + 1
    chunk = content[start:end]

    for key in ("codigo", "nome", "slug", "sigla", "codigoCapital"):
        chunk = chunk.replace(key + ":", '"' + key + '":')

    for dirty in ("\\r", "\\n"):
        chunk = chunk.replace(dirty, "")

    for uf in loads(chunk):
        yield {"code": uf["codigo"], "abbr": uf["sigla"], "name": uf["nome"]}


def get_cities(url=None):
    url = url or CITIES_URL

    print("Fetching", url)
    with urlopen(url) as response:
        content = response.read().decode("utf8")

    for obj in loads(content):
        yield {"code": obj["codigo"], "name": obj["nome"], "state": obj["uf"]}


def clean_dict(dictionary, keys):
    """Returns a dictionary filtering its keys by the argument `keys`."""
    return {k: v for k, v in dictionary.items() if k in keys}


def write_csv(name, data, headers):
    """
    :param name: (str) CSV file path and name
    :param data: (iterable) with dictionary containing the data to be written
    :param headers: (iterable) with the headers for the CSV file
    """
    with open(name, "w", encoding="utf-8") as handler:
        writer = DictWriter(handler, fieldnames=list(headers))
        writer.writeheader()
        for line in data:
            writer.writerow(clean_dict(line, headers))


def write_json(name, data, headers=None):
    """
    :param name: (str) JSON file path and name
    :param data: (iterable) with dictionary containing the data to be written
    :param headers: (iterable) list with keys to keep in the JSON file
    """
    if headers:
        data = list(clean_dict(d, headers) for d in data)
    else:
        data = list(data)
    with open(name, "w", encoding="utf-8") as handler:
        dump(data, handler, ensure_ascii=False)


if __name__ == "__main__":
    states = sorted((state for state in get_states()), key=lambda x: x["name"])
    state_headers = ("code", "abbr", "name")

    print("Saving {} states".format(len(states)))
    write_csv("states.csv", states, state_headers)
    write_json("states.json", states, state_headers)

    cities = sorted((c for c in get_cities()), key=lambda x: x["name"])
    city_headers = ("code", "name", "state")

    print("Saving {} cities".format(len(cities)))
    write_csv("cities.csv", cities, city_headers)
    write_json("cities.json", cities, city_headers)

    print("Done!")
