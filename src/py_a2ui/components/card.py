from typing import Literal

from py_a2ui.types.base import ComponentCommon, ComponentId


class Card(ComponentCommon):
    """A card container. Wraps a single child component."""

    component: Literal["Card"] = "Card"
    child: ComponentId
