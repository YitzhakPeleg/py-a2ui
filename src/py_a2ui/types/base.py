from pydantic import BaseModel, ConfigDict

from py_a2ui.types.accessibility import AccessibilityAttributes

type ComponentId = str


class ComponentCommon(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: ComponentId
    accessibility: AccessibilityAttributes | None = None
    weight: float | None = None
