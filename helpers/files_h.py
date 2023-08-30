from const import EXCEPTIONS_FILE, RECEIVED_MESSAGES_FILE
from .warnings import warn

from json import load, dumps


# * text files
def append_line(path: str, line: str):
    with open(path, "a") as file:
        file.write(line)


def write_lines(path: str, *lines: str, delimiter: str=" "):
    with open(path, "w") as file:
        file.write(delimiter.join(lines))


def free_file(path: str):
    write_lines(path, "")


def log_exception(line: str):
    append_line(EXCEPTIONS_FILE, line)
    warn("Exception occurred!")


def log_received(line: str):
    append_line(RECEIVED_MESSAGES_FILE, line)


# * JSON files
def read_json(path: str) -> dict | list:
    with open(path) as file:
        return load(file)


def write_json(path: str, data: dict | list):
    with open(path, "w", encoding="utf-8") as file:
        file.write(dumps(data, indent=4, ensure_ascii=False))
