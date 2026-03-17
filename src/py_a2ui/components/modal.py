from typing import Literal

from py_a2ui.types.base import ComponentCommon, ComponentId


class Modal(ComponentCommon):
    """A modal dialog with a trigger and content."""

    component: Literal["Modal"] = "Modal"
    trigger: ComponentId
    content: ComponentId
