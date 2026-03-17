from enum import StrEnum
from typing import Literal

from pydantic import Field

from py_a2ui.actions.check import Checkable
from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicString


class TextFieldVariant(StrEnum):
    LONG_TEXT = "longText"
    NUMBER = "number"
    SHORT_TEXT = "shortText"
    OBSCURED = "obscured"


class TextField(Checkable, ComponentCommon):
    """A text input field."""

    component: Literal["TextField"] = "TextField"
    label: DynamicString
    value: DynamicString | None = None
    variant: TextFieldVariant = Field(default=TextFieldVariant.SHORT_TEXT)
