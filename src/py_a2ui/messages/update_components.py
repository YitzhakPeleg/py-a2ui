import json as _json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from py_a2ui.components import AnyComponent
from py_a2ui.messages.create_surface import A2UI_VERSION


class UpdateComponentsMessage(BaseModel):
    """Updates the component tree for a surface."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    version: Literal["v0.10"] = A2UI_VERSION
    type: Literal["updateComponents"] = "updateComponents"
    surface_id: str = Field(alias="surfaceId")
    components: list[AnyComponent] = Field(min_length=1)

    def export(self) -> dict[str, Any]:
        """Flatten nested component trees and return A2UI wire-format dict."""
        from py_a2ui.export import flatten

        return {
            "version": self.version,
            "type": self.type,
            "surfaceId": self.surface_id,
            "components": flatten(self.components),
        }

    def export_json(self, **json_kwargs: Any) -> str:
        """Flatten and serialize to a JSON string."""
        return _json.dumps(self.export(), **json_kwargs)

    def print_tree(self) -> None:
        """Print a Rich tree visualization of the component hierarchy."""
        from py_a2ui.tree import print_tree

        print_tree(self.components, label=self.surface_id)
