from pydantic import Field

from py_a2ui.components import AnyComponent
from py_a2ui.messages.base import A2UIMessage


class UpdateComponentsMessage(A2UIMessage):
    """Updates the component tree for a surface."""

    surface_id: str = Field(alias="surfaceId")
    components: list[AnyComponent] = Field(min_length=1)

    def export(self) -> dict:
        """Flatten nested component trees and return A2UI wire-format dict."""
        from py_a2ui.export import flatten

        return {
            "version": self.version,
            "updateComponents": {
                "surfaceId": self.surface_id,
                "components": flatten(self.components),
            },
        }

    def print_tree(self) -> None:
        """Print a Rich tree visualization of the component hierarchy."""
        from py_a2ui.tree import print_tree

        print_tree(self.components, label=self.surface_id)
