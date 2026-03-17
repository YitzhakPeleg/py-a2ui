from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.actions.check import Checkable
from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicString, DynamicStringList


class ChoiceOption(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    label: str
    value: str


class ChoicePicker(Checkable, ComponentCommon):
    """A selection component for choosing from a list of options."""

    component: Literal["ChoicePicker"] = "ChoicePicker"
    label: DynamicString | None = None
    variant: Literal["multipleSelection", "mutuallyExclusive"] = Field(default="mutuallyExclusive")
    options: list[ChoiceOption]
    value: DynamicStringList
    display_style: Literal["checkbox", "chips"] = Field(default="checkbox", alias="displayStyle")
    filterable: bool = Field(default=False)
