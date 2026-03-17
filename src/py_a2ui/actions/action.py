from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.actions.function_call import FunctionCall


class EventAction(BaseModel):
    """An action that dispatches an event to the server."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    event_name: str = Field(alias="eventName")
    event_context: dict[str, Any] | None = Field(default=None, alias="eventContext")


class FunctionAction(BaseModel):
    """An action that executes a function call."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    function_call: FunctionCall = Field(alias="functionCall")


type Action = EventAction | FunctionAction
