from pydantic import BaseModel, ConfigDict

from py_a2ui.types.dynamic import DynamicBoolean


class CheckRule(BaseModel):
    """A validation rule with a condition and error message."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    condition: DynamicBoolean
    message: str


class Checkable(BaseModel):
    """Mixin for components that support validation checks."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    checks: list[CheckRule] | None = None
