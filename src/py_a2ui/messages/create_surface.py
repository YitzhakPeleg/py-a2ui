from typing import Any

from pydantic import Field

from py_a2ui.messages.base import A2UI_VERSION as A2UI_VERSION
from py_a2ui.messages.base import A2UIMessage


class CreateSurfaceMessage(A2UIMessage):
    """Initiates a new UI surface."""

    surface_id: str = Field(alias="surfaceId")
    catalog_id: str = Field(alias="catalogId")
    theme: dict[str, Any] | None = None
    send_data_model: bool = Field(default=False, alias="sendDataModel")
