import re
from string import digits

import ast_comments as ast
import black
import isort
from pathier import Pathier, Pathish
from rich.pretty import pprint
from rich.traceback import install

install(show_locals=True)

root = Pathier(__file__).parent


def pair_to_property(
    name: str, abbreviation: str
) -> tuple[ast.FunctionDef, ast.FunctionDef]:
    """Generates a pair of class properties given a name and the abbreviation.

    >>> pair_to_property("pink", "p")

    returns

    >>> @property
    >>> def pink(self) -> Tag:
    >>>     return Tag("pink")
    >>>
    >>> @property
    >>> def p(self) -> Tag:
    >>>     return self.pink"""
    args = [ast.Name("self")]
    returns = ast.Name("TagToggle")
    decorator_list = [ast.Name("property")]
    color = ast.FunctionDef(
        name=name,
        args=args,
        returns=returns,
        body=[
            ast.Expr(ast.Constant(f"abbreviation: `{abbreviation}`")),
            ast.Return(ast.Name(f'TagToggle("{name}")')),
        ],
        decorator_list=decorator_list,
    )
    short = ast.FunctionDef(
        name=abbreviation,
        args=args,
        returns=returns,
        body=[
            ast.Expr(ast.Constant(name)),
            ast.Return(ast.Name(f"self.{name}")),
        ],
        decorator_list=decorator_list,
    )
    return color, short


def main():
    """ """
    module: ast.Module = ast.parse((root / "colortoggle.py").read_text())  # type: ignore
    mapping = (root / "colormap.json").loads()
    body = []
    for abbreviation, color in mapping.items():
        abbreviation = "or_" if abbreviation == "or" else abbreviation
        color_property, abbreviation_property = pair_to_property(color, abbreviation)
        if color.startswith("grey"):
            body.append(color_property)
        else:
            body.extend([color_property, abbreviation_property])
    for i, node in enumerate(module.body):
        if isinstance(node, ast.ClassDef) and node.name == "_ColorMap":
            node.body.extend(body)
            module.body[i] = node
    module = ast.fix_missing_locations(module)
    src = black.format_str(ast.unparse(module), mode=black.Mode())  # type: ignore
    (root / "src" / "shortrich" / "colormap.py").write_text(src)


if __name__ == "__main__":
    main()
