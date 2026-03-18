from pydantic import BaseModel, ConfigDict

from py_a2ui.actions.function_call import FunctionCall


class DataBinding(BaseModel):
    """Reference to a value in the client data model via JSON Pointer."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    path: str


# Dynamic value unions: literal | DataBinding | FunctionCall.
# FunctionCall enables using built-in functions (formatString, required, etc.)
# directly as component values or validation conditions.
type DynamicString = str | DataBinding | FunctionCall
type DynamicNumber = int | float | DataBinding | FunctionCall
type DynamicBoolean = bool | DataBinding | FunctionCall
type DynamicStringList = list[str] | DataBinding | FunctionCall
