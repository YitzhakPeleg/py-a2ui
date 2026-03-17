from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.messages.create_surface import A2UI_VERSION


class DeleteSurfaceMessage(BaseModel):
    """Removes a UI surface."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    version: Literal["v0.10"] = A2UI_VERSION
    type: Literal["deleteSurface"] = "deleteSurface"
    surface_id: str = Field(alias="surfaceId")
