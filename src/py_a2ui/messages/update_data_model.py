from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.messages.create_surface import A2UI_VERSION


class UpdateDataModelMessage(BaseModel):
    """Updates the client data model for a surface."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    version: Literal["v0.10"] = A2UI_VERSION
    type: Literal["updateDataModel"] = "updateDataModel"
    surface_id: str = Field(alias="surfaceId")
    path: str | None = None
    value: Any = None
