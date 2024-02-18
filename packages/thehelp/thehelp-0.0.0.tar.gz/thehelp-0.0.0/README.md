# thehelp

Helpers for use with the [rich package](https://pypi.org/project/rich/).  

Type less when applying multiple colors to f-strings,
access all color names with your IDE's autocomplete,
and easily apply color gradients to text.

## Installation

Install with:

<pre>
pip install thehelp
</pre>



## Usage

The `Tag` class is essentially a wrapper to shorten using `rich` tags.  
When a `Tag` is casted to a string it is formatted with surrounding square brackets 
and the `o` or `off` properties can be accessed to return the matching closing tag.  

<pre>
from thehelp import Tag
p = Tag("pale_turquoise4")
c = Tag("cornflower_blue")
s = f"{p}This{p.o} {c}is{c.o} {p}a{p.o} {c}string"
</pre>

is equivalent to

<pre>
s = "[pale_turquoise4]This[/pale_turquoise4] [cornflower_blue]is[/cornflower_blue] [pale_turquoise4]a[/pale_turquoise4] [cornflower_blue]string"
</pre>

---
The `ColorMap` class contains two `Tag` properties for each 
[named color](https://rich.readthedocs.io/en/latest/appendix/colors.html) 
(except shades of grey, those only have a full name property):
one that's the full name of the color and one that's an abbreviated name, for convenience.  

This is useful for seeing color options using autocomplete:
![](imgs/autocomplete.png)

The class also supports iterating over the tags as well as selecting random colors:
![](imgs/iteration.png)

---
The `Gradient` class can be used to easily apply a color sweep across text:
![](imgs/gradient.png)