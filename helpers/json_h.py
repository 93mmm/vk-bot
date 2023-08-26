from json import load, dumps

def read_json(path: str) -> dict | list:
    with open(path) as file:
        return load(file)


def write_json(path: str, data: dict | list):
    with open(path, "w", encoding="utf-8") as file:
        file.write(dumps(data, indent=4, ensure_ascii=False))
