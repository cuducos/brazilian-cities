from abc import ABC, abstractmethod, abstractproperty
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed
from csv import DictWriter
from json import dump, loads
from pathlib import Path
from urllib.request import urlopen


STATES_MARKER = "exports.ufs ="


class Scrapper(ABC):
    @abstractproperty
    def url(self):
        ...

    @abstractmethod
    def __iter__(self):
        ...

    @contextmanager
    def __call__(self):
        print(f"Fetching {self.url}…")
        response = urlopen(str(self.url))
        yield response.read().decode("utf8")


class StatesScrapper(Scrapper):
    url = "https://cidades.ibge.gov.br/dist/main-client.js"

    @property
    def states(self):
        with self() as content:
            start = content.index(STATES_MARKER) + len(STATES_MARKER)
            end = content.index("]", start) + 1
            chunk = content[start:end]

        for key in ("codigo", "nome", "slug", "sigla", "codigoCapital"):
            chunk = chunk.replace(f"{key}:", f'"{key}":')

        for dirty in ("\\r", "\\n"):
            chunk = chunk.replace(dirty, "")

        return loads(chunk)

    def __iter__(self):
        yield from (
            {
                "code": state["codigo"],
                "abbr": state["sigla"],
                "name": state["nome"],
            }
            for state in self.states
        )


class CitiesScrapper(Scrapper):
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/aniversarios"

    def __iter__(self):
        with self() as content:
            cities = loads(content)

        yield from (
            {"code": city["codigo"], "name": city["nome"], "state": city["uf"]}
            for city in cities
        )


class Writer:
    HEADERS = {
        "cities": ("code", "name", "state"),
        "states": ("code", "abbr", "name"),
    }

    def __init__(self, name, scrapper):
        self.name = name
        self.csv_path = Path(f"{name}.csv")
        self.json_path = Path(f"{name}.json")
        self.headers = self.HEADERS.get(name, [])
        self.data = self.sort_data(scrapper)

    def sort_data(self, generator):
        cleaned = (
            {key: value for key, value in row.items() if key in self.headers}
            for row in generator
        )
        return sorted(cleaned, key=lambda row: row["name"])

    def csv(self):
        with self.csv_path.open("w", encoding="utf-8") as handler:
            writer = DictWriter(handler, fieldnames=self.headers)
            writer.writeheader()
            for line in self.data:
                writer.writerow(line)

    def json(self):
        with self.json_path.open("w", encoding="utf-8") as handler:
            dump(self.data, handler, ensure_ascii=False)

    def __call__(self):
        if self.csv_path.exists():
            self.csv_path.unlink()

        if self.json_path.exists():
            self.json_path.unlink()

        print(f"Saving {len(self.data)} {self.name}…")
        self.csv()
        self.json()


def main(name):
    scrapper = {"states": StatesScrapper, "cities": CitiesScrapper}.get(name)
    writer = Writer(name, scrapper())
    return writer()


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = tuple(pool.submit(main, s) for s in ("states", "cities"))
        for result in as_completed(results):
            result.result()

    print("Done!")
