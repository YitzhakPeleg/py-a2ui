"""Base class for all A2UI server-to-client messages."""

import json as _json
from typing import Any, Literal

import inflection
from pydantic import BaseModel, ConfigDict

A2UIVersion = Literal["0.9", "0.8"]
A2UI_CURRENT_VERSION: A2UIVersion = "0.9"


class A2UIMessage(BaseModel):
    """Base for all A2UI server-to-client messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    @property
    def version(self) -> A2UIVersion:
        """The A2UI protocol version this package targets."""
        return A2UI_CURRENT_VERSION

    @property
    def _message_key(self) -> str:
        """Derive wire key from class name: CreateSurfaceMessage -> createSurface."""
        name = type(self).__name__.removesuffix("Message")
        return inflection.camelize(inflection.underscore(name), uppercase_first_letter=False)

    def export(self, *, version: A2UIVersion | None = None) -> dict:
        """Produce A2UI wire-format dict with type-as-key envelope.

        Args:
            version: Target A2UI version. Defaults to current ("0.9").
                     Pass "0.8" for v0.8 compatibility.
        """
        version = version or self.version
        payload = self.model_dump(by_alias=True, exclude_none=True)
        result = {"version": f"v{version}", self._message_key: payload}

        if version == "0.8":
            from py_a2ui.v08_compat import convert_message

            return convert_message(result)

        return result

    def export_json(self, *, version: A2UIVersion | None = None, **kw: Any) -> str:
        """Serialize to A2UI wire-format JSON string."""
        return _json.dumps(self.export(version=version), **kw)
