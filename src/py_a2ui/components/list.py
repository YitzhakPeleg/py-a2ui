from typing import Literal

from pydantic import Field

from py_a2ui.components.row import Align
from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.children import ChildList


class List(ComponentCommon):
    """A list layout component."""

    component: Literal["List"] = "List"
    children: ChildList
    direction: Literal["vertical", "horizontal"] = Field(default="vertical")
    align: Align = Field(default=Align.STRETCH)
