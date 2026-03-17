from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.actions.function_call import FunctionCall
from py_a2ui.messages.create_surface import A2UI_VERSION


class CallFunctionMessage(BaseModel):
    """Server-invoked function call."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    version: Literal["v0.10"] = A2UI_VERSION
    type: Literal["callFunction"] = "callFunction"
    function_call_id: str = Field(alias="functionCallId")
    call_function: FunctionCall = Field(alias="callFunction")
    want_response: bool = Field(default=False, alias="wantResponse")
