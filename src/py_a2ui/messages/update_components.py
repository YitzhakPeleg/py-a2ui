from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.components import AnyComponent
from py_a2ui.messages.create_surface import A2UI_VERSION


class UpdateComponentsMessage(BaseModel):
    """Updates the component tree for a surface."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    version: Literal["v0.10"] = A2UI_VERSION
    type: Literal["updateComponents"] = "updateComponents"
    surface_id: str = Field(alias="surfaceId")
    components: list[AnyComponent] = Field(min_length=1)
