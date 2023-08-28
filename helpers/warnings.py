from colorama import Fore, Style

R = Fore.RED
G = Fore.GREEN
B = Fore.BLUE
RS = Style.RESET_ALL


def warn(*strings: str, sep: str=" "):
    strings = sep.join(strings)
    print(f"{R}WARNING:{RS} {strings}")


def log_percents(percentage: int, *strings, sep=" "):
    strings = sep.join(strings)
    if percentage < 100:
        print("\r" + " " * 50, f"\r{B}Reached {percentage}%{RS}: {strings}", end="")
    else:
        print("\r" + " " * 50, f"\r{G}Reached {percentage}%{RS}: {strings}")


def colored_text(*strings: str, color: str="R", sep: str=" ") -> str:
    strings = sep.join(strings)
    if color == "B":
        color = B
    elif color == "G":
        color = G
    else:
        color = R
    return f"{color}{strings}{RS}"
