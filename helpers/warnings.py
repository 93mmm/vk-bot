from colorama import Fore, Style


def colored_text(*strings: str, color: str="R", sep: str=" ") -> str:
    rs = Style.RESET_ALL
    strings = sep.join(strings)
    if color == "B":
        color = Fore.BLUE
    elif color == "G":
        color = Fore.GREEN
    else:
        color = Fore.RED
    return f"{color}{strings}{rs}"


def warn(*strings: str, sep: str=" "):
    strings = sep.join(strings)
    print(f"{colored_text('WARNING:')} {strings}")


def log_percents(percentage: int, *strings, sep=" "):
    strings = sep.join(strings)
    if percentage < 100:
        reached = colored_text(f"Reached {percentage}%", color="B")
        print("\r" + " " * 50, f"\r{reached}: {strings}", end="")
    else:
        reached = colored_text(f"Reached {percentage}%", color="G")
        print("\r" + " " * 50, f"\r{reached}: {strings}")
