from enum import StrEnum
from typing import Literal

from pydantic import Field

from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.children import ChildList


class Justify(StrEnum):
    CENTER = "center"
    END = "end"
    SPACE_AROUND = "spaceAround"
    SPACE_BETWEEN = "spaceBetween"
    SPACE_EVENLY = "spaceEvenly"
    START = "start"
    STRETCH = "stretch"


class Align(StrEnum):
    START = "start"
    CENTER = "center"
    END = "end"
    STRETCH = "stretch"


class Row(ComponentCommon):
    """A layout component that arranges its children horizontally."""

    component: Literal["Row"] = "Row"
    children: ChildList
    justify: Justify = Field(default=Justify.START)
    align: Align = Field(default=Align.STRETCH)
