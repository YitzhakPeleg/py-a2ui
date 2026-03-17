from pydantic import BaseModel, ConfigDict


class DataBinding(BaseModel):
    """Reference to a value in the client data model via JSON Pointer."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    path: str


# Forward-reference-friendly type aliases.
# FunctionCall is defined in actions/ to avoid circular imports.
# These unions are resolved at runtime via TYPE_CHECKING + Annotated.
type DynamicString = str | DataBinding
type DynamicNumber = int | float | DataBinding
type DynamicBoolean = bool | DataBinding
type DynamicStringList = list[str] | DataBinding
