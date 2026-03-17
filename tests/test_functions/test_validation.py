import pytest
from pydantic import ValidationError

from py_a2ui.functions.validation import email, length, numeric, regex, required


def test_required():
    fc = required()
    assert fc.call == "required"
    assert fc.args is None


def test_regex_valid():
    fc = regex(r"^\d{3}$")
    assert fc.args == {"pattern": r"^\d{3}$"}


def test_regex_invalid_pattern():
    with pytest.raises(ValueError, match="Invalid regex pattern"):
        regex("[invalid")


def test_length_min_only():
    fc = length(min=3)
    assert fc.args == {"min": 3}


def test_length_max_only():
    fc = length(max=10)
    assert fc.args == {"max": 10}


def test_length_min_and_max():
    fc = length(min=3, max=10)
    assert fc.args == {"min": 3, "max": 10}


def test_length_no_args():
    fc = length()
    assert fc.args is None


def test_length_max_less_than_min():
    with pytest.raises(ValueError, match=r"max .* must be >= min"):
        length(min=5, max=3)


def test_length_rejects_negative_min():
    with pytest.raises(ValidationError):
        length(min=-1)


def test_numeric_min_and_max():
    fc = numeric(min=0.0, max=100.0)
    assert fc.args == {"min": 0.0, "max": 100.0}


def test_numeric_max_less_than_min():
    with pytest.raises(ValueError, match=r"max .* must be >= min"):
        numeric(min=10, max=5)


def test_numeric_no_args():
    fc = numeric()
    assert fc.args is None


def test_email():
    fc = email()
    assert fc.call == "email"
    assert fc.args is None
