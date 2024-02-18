"""
haitch - a lazy HTML element builder.
=====================================

Import any element you like from the root module:

>>> import haitch as H

Lazily build a dom tree by passing children and/or attributes to the
`__init__` and/or `__call__` methods:

>>> dom = H.a(href="https://example.com")("Check out my website")

In order render the object to HTML, you need to invoke the `__str__` method:

>>> str(dom)
'<a href="https://example.com">Check out my website</a>'
"""

from haitch._element import Element, fragment
from haitch._typing import Html, HtmlElement
from haitch._void_elements._area import AreaElement, area
from haitch._void_elements._base import BaseElement, base
from haitch._void_elements._br import BrElement, br
from haitch._void_elements._col import ColElement, col
from haitch._void_elements._embed import EmbedElement, embed
from haitch._void_elements._hr import HrElement, hr
from haitch._void_elements._img import ImgElement, img
from haitch._void_elements._input import InputElement, input
from haitch._void_elements._link import LinkElement, link
from haitch._void_elements._meta import MetaElement, meta
from haitch._void_elements._source import SourceElement, source
from haitch._void_elements._track import TrackElement, track
from haitch._void_elements._void_element import VoidElement
from haitch._void_elements._wbr import WbrElement, wbr

__all__ = [
    "AreaElement",
    "BaseElement",
    "BrElement",
    "ColElement",
    "Element",
    "EmbedElement",
    "HrElement",
    "Html",
    "HtmlElement",
    "ImgElement",
    "InputElement",
    "LinkElement",
    "MetaElement",
    "SourceElement",
    "TrackElement",
    "VoidElement",
    "WbrElement",
    "area",
    "base",
    "br",
    "col",
    "embed",
    "fragment",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
]


def __getattr__(tag: str) -> Element:
    return Element(tag)
