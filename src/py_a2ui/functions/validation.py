import re

from pydantic import NonNegativeInt, validate_call

from py_a2ui.actions.function_call import FunctionCall, ReturnType


def required() -> FunctionCall:
    """Check that a value is not null, undefined, or empty."""
    return FunctionCall(call="required", return_type=ReturnType.BOOLEAN)


def regex(pattern: str) -> FunctionCall:
    """Check that a value matches a regex pattern.

    Raises:
        ValueError: If the pattern is not a valid regular expression.
    """
    try:
        re.compile(pattern)
    except re.error as e:
        msg = f"Invalid regex pattern: {e}"
        raise ValueError(msg) from e
    return FunctionCall(call="regex", args={"pattern": pattern}, return_type=ReturnType.BOOLEAN)


@validate_call
def length(*, min: NonNegativeInt | None = None, max: NonNegativeInt | None = None) -> FunctionCall:
    """Check string length within optional min/max bounds.

    Raises:
        ValueError: If both min and max are provided and max < min.
    """
    if min is not None and max is not None and max < min:
        msg = f"max ({max}) must be >= min ({min})"
        raise ValueError(msg)
    args = {k: v for k, v in {"min": min, "max": max}.items() if v is not None}
    return FunctionCall(call="length", args=args or None, return_type=ReturnType.BOOLEAN)


def numeric(*, min: float | None = None, max: float | None = None) -> FunctionCall:
    """Check that a numeric value is within optional min/max bounds.

    Raises:
        ValueError: If both min and max are provided and max < min.
    """
    if min is not None and max is not None and max < min:
        msg = f"max ({max}) must be >= min ({min})"
        raise ValueError(msg)
    args = {k: v for k, v in {"min": min, "max": max}.items() if v is not None}
    return FunctionCall(call="numeric", args=args or None, return_type=ReturnType.BOOLEAN)


def email() -> FunctionCall:
    """Validate email format."""
    return FunctionCall(call="email", return_type=ReturnType.BOOLEAN)
