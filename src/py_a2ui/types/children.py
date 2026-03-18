from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.types.base import ComponentCommon, ComponentId


class DynamicChildTemplate(BaseModel):
    """A dynamic child list that iterates over a data model array."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    component_id: ComponentId = Field(alias="componentId")
    path: str


type ChildRef = ComponentId | ComponentCommon
type StaticChildList = list[ChildRef]
type ChildList = StaticChildList | DynamicChildTemplate
