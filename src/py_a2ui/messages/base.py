"""Base class for all A2UI server-to-client messages."""

import json as _json
from typing import Any

import inflection
from pydantic import BaseModel, ConfigDict

A2UI_VERSION = "v0.9"


class A2UIMessage(BaseModel):
    """Base for all A2UI server-to-client messages."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    @property
    def version(self) -> str:
        """The A2UI protocol version this package targets."""
        return A2UI_VERSION

    @property
    def _message_key(self) -> str:
        """Derive wire key from class name: CreateSurfaceMessage -> createSurface."""
        name = type(self).__name__.removesuffix("Message")
        return inflection.camelize(inflection.underscore(name), uppercase_first_letter=False)

    def export(self) -> dict:
        """Produce A2UI wire-format dict with type-as-key envelope."""
        payload = self.model_dump(by_alias=True, exclude_none=True)
        return {"version": self.version, self._message_key: payload}

    def export_json(self, **kw: Any) -> str:
        """Serialize to A2UI wire-format JSON string."""
        return _json.dumps(self.export(), **kw)
