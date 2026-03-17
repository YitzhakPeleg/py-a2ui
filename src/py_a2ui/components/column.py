from typing import Literal

from pydantic import Field

from py_a2ui.components.row import Align, Justify
from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.children import ChildList


class Column(ComponentCommon):
    """A layout component that arranges its children vertically."""

    component: Literal["Column"] = "Column"
    children: ChildList
    justify: Justify = Field(default=Justify.START)
    align: Align = Field(default=Align.STRETCH)
