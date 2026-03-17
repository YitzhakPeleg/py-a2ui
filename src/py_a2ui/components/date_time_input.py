from typing import Literal

from pydantic import Field

from py_a2ui.actions.check import Checkable
from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicString


class DateTimeInput(Checkable, ComponentCommon):
    """A date and/or time input component. Values use ISO 8601 format."""

    component: Literal["DateTimeInput"] = "DateTimeInput"
    value: DynamicString
    enable_date: bool = Field(default=False, alias="enableDate")
    enable_time: bool = Field(default=False, alias="enableTime")
    min: DynamicString | None = None
    max: DynamicString | None = None
    label: DynamicString | None = None
