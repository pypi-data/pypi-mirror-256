import string
from dataclasses import dataclass

from rich.color import Color
from typing_extensions import Self

from .colormap import Tag


@dataclass
class RGB:
    """
    Dataclass representing a 3 channel RGB color that is converted to a `rich` tag when casted to a string.

    >>> color = RGB(100, 100, 100)
    >>> str(color)
    >>> "[rgb(100,100,100)]"
    >>> from rich.console import Console
    >>> console = Console()
    >>> console.print(f"{color}Yeehaw")

    Can also be initialized using a color name from https://rich.readthedocs.io/en/stable/appendix/colors.html

    >>> color = RGB(name="magenta3")
    >>> print(color)
    >>> "[rgb(215,0,215)]"

    Supports addition and subtraction of `RGB` objects as well as scalar multiplication and division.

    >>> color1 = RGB(100, 100, 100)
    >>> color2 = RGB(25, 50, 75)
    >>> print(color1 + color2)
    >>> "[rgb(125,150,175)]"
    >>> print(color2 * 2)
    >>> "[rgb(50,100,150)]"
    """

    # Typing these as floats so `Gradient` can fractionally increment them
    # When casted to a string, the values will be rounded to integers
    r: float = 0
    g: float = 0
    b: float = 0
    name: str = ""

    def __post_init__(self):
        if self.name:
            self.r, self.g, self.b = Color.parse(self.name).get_truecolor()

    def __str__(self) -> str:
        return f"[rgb({round(self.r)},{round(self.g)},{round(self.b)})]"

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.r - other.r, self.g - other.g, self.b - other.b)

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.r + other.r, self.g + other.g, self.b + other.b)

    def __truediv__(self, val: float) -> Self:
        return self.__class__(self.r / val, self.g / val, self.b / val)

    def __mul__(self, val: float) -> Self:
        return self.__class__(self.r * val, self.g * val, self.b * val)

    def __eq__(self, other: Self) -> bool:
        return all(getattr(self, c) == getattr(other, c) for c in "rgb")


class Gradient:
    """
    Apply a color gradient to strings when using `rich`.

    When applied to a string, each character will increment in color from a start to a stop color.

    Start and stop colors can be specified by either
    a 3 tuple representing RGB values,
    a `shortrich.Tag` object,
    or a color name from https://rich.readthedocs.io/en/stable/appendix/colors.html.

    Tuple:
    >>> gradient = Gradient((255, 0, 0), (0, 255, 0))

    `shortrich.Tag`:
    >>> colors = shortrich.ColorMap()
    >>> gradient = Gradient(colors.red, colors.green)

    Name:
    >>> gradient = Gradient("red", "green")

    Usage:
    >>> from shortrich import Gradient
    >>> from rich.console import Console
    >>> console = Console()
    >>> gradient = Gradient("red", "green")
    >>> text = "Yeehaw"
    >>> gradient_text = gradient.apply(text)
    >>> # This produces:
    >>> print(gradient_text)
    >>> "[rgb(128,0,0)]Y[/][rgb(102,25,0)]e[/][rgb(76,51,0)]e[/][rgb(51,76,0)]h[/][rgb(25,102,0)]a[/][rgb(0,128,0)]w[/]"
    >>> # When used with `console.print`, each character will be a different color
    >>> console.print(gradient_text)

    """

    def __init__(
        self,
        start: tuple[int, int, int] | str | Tag = "pink1",
        stop: tuple[int, int, int] | str | Tag = "turquoise2",
    ):
        self._start = self._parse(start)
        self._stop = self._parse(stop)

    @property
    def start(self) -> RGB:
        """The starting color for the gradient."""
        return self._start

    @start.setter
    def start(self, color: str | Tag | tuple[int, int, int]):
        self._start = self._parse(color)

    @property
    def stop(self) -> RGB:
        """The ending color for the gradient."""
        return self._stop

    @stop.setter
    def stop(self, color: str | Tag | tuple[int, int, int]):
        self._stop = self._parse(color)

    @property
    def valid_characters(self) -> str:
        """Characters a color step can be applied to."""
        return string.ascii_letters + string.digits + string.punctuation

    def _parse(self, color: str | Tag | tuple[int, int, int]) -> RGB:
        if isinstance(color, str):
            return RGB(name=color)
        elif isinstance(color, Tag):
            return RGB(name=color.name)
        elif isinstance(color, tuple):
            return RGB(*color)
        raise ValueError(f"{color!r} is an invalid type.")

    def _get_step_sizes(self, total_steps: int) -> RGB:
        """Returns a `RGB` object representing the step size for each color channel."""
        return (self.stop - self.start) / total_steps

    def _get_gradient_color(self, step: int, step_sizes: RGB) -> RGB:
        """Returns a `RGB` object representing the color at `step`."""
        return self.start + (step_sizes * step)

    def _get_num_steps(self, text: str) -> int:
        """Returns the number of steps the gradient should be divided into."""
        return len([ch for ch in text if ch in self.valid_characters]) - 1

    def apply(self, text: str) -> str:
        """Apply the gradient to ascii letters, digits, and punctuation in `text`."""
        steps = self._get_num_steps(text)
        step_sizes = self._get_step_sizes(steps)
        gradient_text = ""
        step = 0
        for ch in text:
            if ch in self.valid_characters:
                gradient_text += f"{self._get_gradient_color(step, step_sizes)}{ch}[/]"
                step += 1
            else:
                gradient_text += ch
        return gradient_text
