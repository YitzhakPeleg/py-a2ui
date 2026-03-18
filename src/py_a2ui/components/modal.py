from typing import Literal

from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.children import ChildRef


class Modal(ComponentCommon):
    """A modal dialog with a trigger and content."""

    component: Literal["Modal"] = "Modal"
    trigger: ChildRef
    content: ChildRef
