from pydantic import HttpUrl, TypeAdapter

from py_a2ui.actions.function_call import FunctionCall, ReturnType

_http_url_adapter = TypeAdapter(HttpUrl)


def open_url(url: str | HttpUrl) -> FunctionCall:
    """Open a URL.

    Validates that the URL is a well-formed HTTP(S) URL.

    Raises:
        ValidationError: If the URL is not a valid HTTP(S) URL.
    """
    validated = _http_url_adapter.validate_python(url)
    return FunctionCall(call="openUrl", args={"url": str(validated)}, return_type=ReturnType.VOID)
