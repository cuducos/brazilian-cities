from csv import DictWriter
from json import dump, loads
from pathlib import Path
from urllib.request import urlopen


URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
CITIES = "cities"
STATES = "states"
HEADERS = {CITIES: ("code", "name", "state"), STATES: ("code", "abbr", "name")}
FORMATS = ("csv", "json")


def scrapper():
    states_yielded = set()

    print(f"Fetching {URL}…")

    response = urlopen(URL)
    body = response.read()
    data = body.decode("utf8")

    for obj in loads(data):
        city = {
            "code": obj["id"],
            "name": obj["nome"],
            "state": obj["microrregiao"]["mesorregiao"]["UF"]["sigla"],
        }
        yield (CITIES, city)

        if city["state"] in states_yielded:
            continue

        state = {
            "abbr": city["state"],
            "code": obj["microrregiao"]["mesorregiao"]["UF"]["id"],
            "name": obj["microrregiao"]["mesorregiao"]["UF"]["nome"],
        }
        yield (STATES, state)
        states_yielded.add(state["abbr"])


class Writer:
    @staticmethod
    def key_for(name, ext):
        return f"{name}.{ext}"

    def __init__(self, scrapper):
        self.scrapper = scrapper
        self.data = {CITIES: [], STATES: []}
        self.paths = {
            name: Path(name)
            for name in (self.key_for(name, ext) for name in HEADERS for ext in FORMATS)
        }

    def sort_data(self):
        print("Sorting data…")
        for name in HEADERS:
            self.data[name] = sorted(self.data[name], key=lambda row: row["name"])

    def write_csv(self):
        for name, headers in HEADERS.items():
            key = self.key_for(name, "csv")
            with self.paths[key].open("w", encoding="utf-8") as handler:
                writer = DictWriter(handler, fieldnames=headers)
                writer.writeheader()
                for line in self.data[name]:
                    writer.writerow(line)

    def write_json(self):
        for name in HEADERS:
            key = self.key_for(name, "json")
            with self.paths[key].open("w", encoding="utf-8") as handler:
                dump(self.data[name], handler, ensure_ascii=False)

        unified = {}
        for state in self.data[STATES]:
            key = state["abbr"]
            unified[key] = state.copy()
            unified[key][CITIES] = []
        for city in self.data[CITIES]:
            key = city["state"]
            unified[key][CITIES].append(city)

        with Path("states_and_cities.json").open("w", encoding="utf-8") as handler:
            dump(unified, handler, ensure_ascii=False)

    def __call__(self):
        for name, row in self.scrapper:
            self.data[name].append(row)

        self.sort_data()

        for path in self.paths.values():
            if path.exists():
                path.unlink()

        for name in HEADERS:
            print(f"Saving {len(self.data[name])} {name}…")
            self.write_csv()
            self.write_json()


def main():
    data = scrapper()
    writer = Writer(data)
    return writer()


if __name__ == "__main__":
    main()
    print("Done!")
