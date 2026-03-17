from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.types.base import ComponentCommon, ComponentId
from py_a2ui.types.dynamic import DynamicString


class Tab(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    title: DynamicString
    child: ComponentId


class Tabs(ComponentCommon):
    """A tabbed container with multiple named tabs."""

    component: Literal["Tabs"] = "Tabs"
    tabs: list[Tab] = Field(min_length=1)
