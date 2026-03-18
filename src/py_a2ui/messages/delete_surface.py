from pydantic import Field

from py_a2ui.messages.base import A2UIMessage


class DeleteSurfaceMessage(A2UIMessage):
    """Removes a UI surface."""

    surface_id: str = Field(alias="surfaceId")
