# TODO: add these functions and include them in the project

def append_lines(path: str, lines: list, delimiter: str):
    pass


def append_line(path: str, line: str):
    pass


def write_lines(path: str, lines: list, delimiter: str):
    with open(path, "w") as file:
        file.write(delimiter.join(lines))


def free_file(path: str):
    pass
