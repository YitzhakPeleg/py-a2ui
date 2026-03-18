from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_serializer, model_validator

from py_a2ui.actions.function_call import FunctionCall


class EventAction(BaseModel):
    """An action that dispatches an event to the server.

    Wire format: ``{"event": {"name": "submit", "context": {...}}}``
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    event_name: str = Field(alias="eventName")
    event_context: dict[str, Any] | None = Field(default=None, alias="eventContext")

    @model_validator(mode="before")
    @classmethod
    def _accept_wire_format(cls, data: Any) -> Any:
        """Accept wire format: {"event": {"name": "...", "context": {...}}}."""
        if isinstance(data, dict) and "event" in data and "event_name" not in data and "eventName" not in data:
            event = data["event"]
            return {"event_name": event["name"], "event_context": event.get("context")}
        return data

    @model_serializer(mode="wrap")
    def _serialize_wire(self, handler: Any) -> dict:
        """Serialize to wire format: {"event": {"name": "...", "context": {...}}}."""
        result: dict[str, Any] = {"name": self.event_name}
        if self.event_context is not None:
            result["context"] = self.event_context
        return {"event": result}


class FunctionAction(BaseModel):
    """An action that executes a function call.

    Wire format: ``{"functionCall": {"call": "openUrl", "args": {...}}}``
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    function_call: FunctionCall = Field(alias="functionCall")


type Action = EventAction | FunctionAction
