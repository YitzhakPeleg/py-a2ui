from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

A2UI_VERSION = "v0.10"


class CreateSurfaceMessage(BaseModel):
    """Initiates a new UI surface."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    version: Literal["v0.10"] = A2UI_VERSION
    type: Literal["createSurface"] = "createSurface"
    surface_id: str = Field(alias="surfaceId")
    catalog_id: str = Field(alias="catalogId")
    theme: dict[str, Any] | None = None
    send_data_model: bool = Field(default=False, alias="sendDataModel")
