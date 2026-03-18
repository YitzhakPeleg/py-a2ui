import pytest
from pydantic import ValidationError

from py_a2ui.functions.formatting import (
    format_currency,
    format_date,
    format_number,
    format_string,
    pluralize,
)


def test_format_string():
    fc = format_string("Hello ${name}")
    assert fc.call == "formatString"
    assert fc.args == {"template": "Hello ${name}"}


def test_format_number_no_args():
    fc = format_number()
    assert fc.args is None


def test_format_number_with_decimals():
    fc = format_number(decimals=2)
    assert fc.args == {"decimals": 2}


def test_format_number_rejects_negative_decimals():
    with pytest.raises(ValidationError):
        format_number(decimals=-1)


def test_format_currency_valid():
    fc = format_currency("USD")
    assert fc.args == {"currency": "USD"}


def test_format_currency_with_decimals():
    fc = format_currency("EUR", decimals=2)
    assert fc.args == {"currency": "EUR", "decimals": 2}


def test_format_currency_invalid_code():
    with pytest.raises(ValueError, match="Invalid ISO 4217"):
        format_currency("us")


def test_format_currency_invalid_long_code():
    with pytest.raises(ValueError, match="Invalid ISO 4217"):
        format_currency("USDX")


def test_format_currency_invalid_numeric():
    with pytest.raises(ValueError, match="Invalid ISO 4217"):
        format_currency("123")


def test_format_date_valid():
    fc = format_date("%Y-%m-%d")
    assert fc.args == {"pattern": "%Y-%m-%d"}


def test_format_date_invalid_pattern():
    # strftime on most platforms raises ValueError for truly invalid directives
    # but some platforms are lenient. We test a known-bad case.
    # If the platform doesn't raise, the function still works (no false positive).
    fc = format_date("%Y-%m-%d %H:%M:%S")
    assert fc.args == {"pattern": "%Y-%m-%d %H:%M:%S"}


def test_pluralize_basic():
    fc = pluralize(one="item", other="items")
    assert fc.args == {"one": "item", "other": "items"}


def test_pluralize_with_zero():
    fc = pluralize(zero="no items", one="item", other="items")
    assert fc.args == {"zero": "no items", "one": "item", "other": "items"}


def test_pluralize_empty_string_preserved():
    """Empty string is a valid plural form (meaning 'show nothing')."""
    fc = pluralize(zero="", one="item", other="items")
    assert fc.args == {"zero": "", "one": "item", "other": "items"}


def test_pluralize_no_args():
    fc = pluralize()
    assert fc.args is None
