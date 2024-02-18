from dataclasses import dataclass
from typing import Iterator


@dataclass
class Tag:
    """Reduce the size of f-strings when using `rich`.
    >>> from rich import print
    >>> p = Tag("pink1")
    >>> c = Tag("cyan")
    >>> print(f"{p}This{p.o} {c}is{c.o} {p}a{p.o} {c}string")
    >>> same as
    >>> print("[pink1]This[/pink1] [cyan]is[/cyan] [pink1]a[/pink1] [cyan]string")"""

    name: str

    def __str__(self) -> str:
        return f"[{self.name}]"

    @property
    def o(self) -> str:
        """Closing tag for this tag."""
        return f"[/{self.name}]"

    @property
    def off(self) -> str:
        """Closing tag for this tag."""
        return self.o


class ColorMap:
    """Color map for the rich colors at https://rich.readthedocs.io/en/stable/appendix/colors.html

    See color options conveniently with your IDE's autocomplete.

    Each color has two `Tag` properties: one using the full name and one using an abbreviation.

    `ColorMap.aquamarine1` and `ColorMap.a1` return equivalent `Tag` instances.

    >>> from rich import print
    >>> 'To alternate colors, instead of doing this:'
    >>> print("[aquamarine1]This [light_pink4]is [aquamarine]a [light_pink4]string")
    >>> 'You can do:'
    >>> c = ColorMap()
    >>> print(f"{c.a1}This {c.lp4}is {c.a1}a {c.lp4}string")"""

    @property
    def _toggle_list(self) -> list[Tag]:
        return [
            getattr(self, obj)
            for obj in dir(self)
            if not obj.startswith("_") and isinstance(getattr(self, obj), Tag)
        ]

    def __len__(self) -> int:
        return len(self._toggle_list)

    def __iter__(self) -> Iterator[Tag]:
        for toggle in self._toggle_list:
            yield toggle

    def __getitem__(self, key: int) -> Tag:
        return self._toggle_list[key]
