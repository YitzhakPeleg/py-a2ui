from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ReturnType(StrEnum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"
    VOID = "void"


class CallableFrom(StrEnum):
    CLIENT_ONLY = "clientOnly"
    REMOTE_ONLY = "remoteOnly"
    CLIENT_OR_REMOTE = "clientOrRemote"


class FunctionCall(BaseModel):
    """A call to a built-in or custom function."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    call: str = Field(description="The name of the built-in function to invoke, e.g. 'formatString', 'openUrl'")
    args: dict[str, Any] | None = None
    return_type: ReturnType = Field(default=ReturnType.BOOLEAN, alias="returnType")
    callable_from: CallableFrom = Field(default=CallableFrom.CLIENT_ONLY, alias="callableFrom")
