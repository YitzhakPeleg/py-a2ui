import pytest
from pydantic import ValidationError

from py_a2ui.functions.navigation import open_url


def test_open_url_valid():
    fc = open_url("https://example.com")
    assert fc.call == "openUrl"
    assert fc.args is not None
    assert "url" in fc.args


def test_open_url_with_path():
    fc = open_url("https://example.com/path?q=1")
    assert fc.args is not None
    assert "example.com" in fc.args["url"]


def test_open_url_invalid():
    with pytest.raises(ValidationError):
        open_url("not-a-url")


def test_open_url_ftp_rejected():
    with pytest.raises(ValidationError):
        open_url("ftp://example.com")
