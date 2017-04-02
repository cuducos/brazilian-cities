import re
from csv import DictWriter
from json import dump
from urllib.request import urlopen

from bs4 import BeautifulSoup

BASE_URL = 'http://cidades.ibge.gov.br'
RE_CODE_UF = re.compile('coduf=(\d+)')
RE_CODE_CITY = re.compile('codmun=(\d+)')


def get_list_items_from(url, id_, encoding='utf-8'):
    """
    Generator with <li> elements from a HTML list with `id_` as the ID.
    :param url: (str) URL to fetch
    :param id_: (str) ID attribute of a HTML list
    :return: (generator) with list item BeautifulSoup objects
    """
    print('Fetching ' + url)
    html = BeautifulSoup(urlopen(url).read(), 'html.parser')
    objs = html.find(id=id_)
    for obj in objs.find_all('li'):
        yield obj


def get_states():
    """
    Generator that returns dictionaries with each state abbreviation, name, and
    the URL to this state webapage.
    """
    url = BASE_URL + '/xtras/home.php'
    for state in get_list_items_from(url, 'menu_ufs'):
        url = state.a.get('href').replace('..', BASE_URL)
        match = RE_CODE_UF.search(url)
        yield dict(code=match.group(1), abbr=state.string, name=state.a.get('title'), url=url)


def get_cities_from_state(state, url):
    """
    Generator that returns dictionaries with the city name and the abbreviation
    to its state.
    """
    for city in get_list_items_from(url, 'lista_municipios'):
        city_url = city.a.get('href').replace('..', BASE_URL)
        match = RE_CODE_CITY.search(city_url)
        yield dict(code=match.group(1), name=city.string, state=state)


def get_cities(states):
    """
    Wrapper for get_cities_from_state().
    :param states: (iterale) like get_states() generator
    :return: (generator) of diciotnaries like get_cities_from_state()
    """
    for state in states:
        yield from get_cities_from_state(state['abbr'], state['url'])


def clean_dict(dictionary, keys):
    """Returns a dictionary filtering its keys by the argument `keys`."""
    return {k: v for k, v in dictionary.items() if k in keys}


def write_csv(name, data, headers):
    """
    :param name: (str) CSV file path and name
    :param data: (iterable) with dictionary containing the data to be written
    :param headers: (iterable) with the headers for the CSV file
    """
    with open(name, 'w', encoding='utf-8') as handler:
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
    with open(name, 'w', encoding='utf-8') as handler:
        dump(data, handler, ensure_ascii=False)


if __name__ == '__main__':
    states = sorted([state for state in get_states()], key=lambda x: x['name'])
    state_headers = ('code', 'abbr', 'name')

    cities = sorted([c for c in get_cities(states)], key=lambda x: x['name'])
    city_headers = ('code', 'name', 'state')

    print('\nSaving {} states'.format(len(states)))
    write_csv('states.csv', states, state_headers)
    write_json('states.json', states, state_headers)

    print('Saving {} cities'.format(len(cities)))
    write_csv('cities.csv', cities, city_headers)
    write_json('cities.json', cities, city_headers)

    print('\nDone!')
