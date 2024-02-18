import ast
import re
from string import digits

from bs4 import Tag
from gruel import Gruel
from pathier import Pathier, Pathish
from rich.pretty import pprint
from rich.traceback import install

install(show_locals=True)

root = Pathier(__file__).parent


def scrape_colors() -> list[str]:
    url = "https://rich.readthedocs.io/en/stable/appendix/colors.html"
    soup = Gruel.as_soup(Gruel.request(url))
    pre = soup.find("pre")
    assert isinstance(pre, Tag)
    colors = []
    for span in pre.find_all("span"):
        text = span.text.strip()
        if text.startswith('"'):
            colors.append(text.strip('"'))
    return colors


def sort(colors: list[str]) -> list[str]:
    # putting 'black' at the end b/c it'll get used the least and 'blue' can get shorter abbreviation
    basics = [
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "white",
        "cyan",
        "pink",
        "orange",
        "purple",
        "turquoise",
    ]
    colors.remove("black")
    colors = sorted(colors)
    colors = sorted(colors, key=lambda c: c.strip(digits) not in basics)
    colors = sorted(colors, key=lambda c: "_" in c)
    colors.append("black")
    return colors


def save(colors: list[str]) -> None:
    (root / "colors.txt").join(colors)


def read() -> list[str]:
    return (root / "colors.txt").split()


def abbreviate(color: str, depth: int = 1) -> str:
    """
    >>> abbreviate("dark_olive_green1")
    >>> "dog1"
    >>> abbreviate("dark_olive_green1", 2)
    >>> "daolgr1"
    """

    words = color.split("_")
    abbreviation = "".join(word[:depth] for word in words)
    return abbreviation


def make_map(colors: list[str]) -> dict[str, str]:
    mapping = {}
    added_bases = {}
    for color in colors:
        if color.startswith("grey"):
            mapping[color] = color
        else:
            hits = re.findall(r".([0-9]+)", color)
            num = hits[0] if hits else ""
            color = color.strip(num)
            if color in added_bases:
                abbreviation = added_bases[color]
            else:
                depth = (
                    1 if all(color[0] not in k for k in mapping) or "_" in color else 2
                )
                abbreviation = abbreviate(color, depth)
                depth += 1
                while abbreviation + num in mapping:
                    abbreviation = abbreviate(color, depth)
                    depth += 1
            mapping[abbreviation + num] = color + num
            added_bases.setdefault(color, abbreviation)
    return mapping


def pair_to_property(
    abbreviation: str, name: str
) -> tuple[ast.FunctionDef, ast.FunctionDef]:
    color = ast.FunctionDef(
        name=name,
        args=["self"],
        returns=ast.expr(
            value=f'TagToggle("{name}")',
            body=[],
            decorator_list=[ast.Name("property", ast.Load())],
        ),
    )
    short = ast.FunctionDef(
        name=abbreviation,
        args=["self"],
        returns=ast.expr(
            value=f"self.{name}",
            body=[],
            decorator_list=[ast.Name("property", ast.Load())],
        ),
    )
    return color, short


def main():
    """ """
    save(scrape_colors())
    colors = sort(read())
    colors.remove("black")
    colors.remove("bright_black")
    colors.append("black")
    colors.append("bright_black")
    mapping = make_map(colors)
    mapping = {k: mapping[k] for k in sorted(mapping, key=lambda m: mapping[m])}
    pprint(mapping)
    (root / "colormap.json").dumps(mapping, indent=2)


if __name__ == "__main__":
    main()
