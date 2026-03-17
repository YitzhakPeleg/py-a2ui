import re
from datetime import datetime
from typing import Any

from pydantic import NonNegativeInt, validate_call

from py_a2ui.actions.function_call import FunctionCall, ReturnType

_ISO_4217_RE = re.compile(r"^[A-Z]{3}$")


def format_string(template: str) -> FunctionCall:
    """Perform string interpolation using ${expression} syntax."""
    return FunctionCall(call="formatString", args={"template": template}, return_type=ReturnType.STRING)


@validate_call
def format_number(*, decimals: NonNegativeInt | None = None, grouping: bool | None = None) -> FunctionCall:
    """Format a number with optional decimal places and grouping."""
    args = {k: v for k, v in {"decimals": decimals, "grouping": grouping}.items() if v is not None}
    return FunctionCall(call="formatNumber", args=args or None, return_type=ReturnType.STRING)


@validate_call
def format_currency(currency: str, *, decimals: NonNegativeInt | None = None) -> FunctionCall:
    """Format a monetary amount with an ISO 4217 currency code (e.g. 'USD', 'EUR').

    Raises:
        ValueError: If currency is not a valid 3-letter ISO 4217 code.
    """
    if not _ISO_4217_RE.match(currency):
        msg = f"Invalid ISO 4217 currency code: {currency!r} (expected 3 uppercase letters, e.g. 'USD')"
        raise ValueError(msg)
    args: dict[str, Any] = {"currency": currency}
    if decimals is not None:
        args["decimals"] = decimals
    return FunctionCall(call="formatCurrency", args=args, return_type=ReturnType.STRING)


def format_date(pattern: str) -> FunctionCall:
    """Format a date using a strftime-compatible pattern (e.g. '%Y-%m-%d').

    Raises:
        ValueError: If the pattern is not a valid strftime format string.
    """
    try:
        datetime.now().strftime(pattern)
    except ValueError as e:
        msg = f"Invalid date format pattern: {e}"
        raise ValueError(msg) from e
    return FunctionCall(call="formatDate", args={"pattern": pattern}, return_type=ReturnType.STRING)


def pluralize(
    *, zero: str = "", one: str = "", two: str = "", few: str = "", many: str = "", other: str = ""
) -> FunctionCall:
    """Return a localized string based on CLDR plural category."""
    args = {
        k: v for k, v in {"zero": zero, "one": one, "two": two, "few": few, "many": many, "other": other}.items() if v
    }
    return FunctionCall(call="pluralize", args=args or None, return_type=ReturnType.STRING)
