from typing import Literal

from pydantic import Field

from py_a2ui.actions.check import Checkable
from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicNumber, DynamicString


class Slider(Checkable, ComponentCommon):
    """A slider input for selecting a numeric value."""

    component: Literal["Slider"] = "Slider"
    label: DynamicString | None = None
    min: float = Field(default=0)
    max: float
    value: DynamicNumber
