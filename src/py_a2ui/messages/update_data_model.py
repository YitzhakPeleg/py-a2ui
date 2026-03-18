from typing import Any

from pydantic import Field

from py_a2ui.messages.base import A2UIMessage


class UpdateDataModelMessage(A2UIMessage):
    """Updates the client data model for a surface."""

    surface_id: str = Field(alias="surfaceId")
    path: str | None = None
    value: Any = None
