from typing import Literal

from py_a2ui.actions.check import Checkable
from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicBoolean, DynamicString


class CheckBox(Checkable, ComponentCommon):
    """A checkbox input component."""

    component: Literal["CheckBox"] = "CheckBox"
    label: DynamicString
    value: DynamicBoolean
