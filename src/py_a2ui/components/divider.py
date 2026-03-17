from typing import Literal

from pydantic import Field

from py_a2ui.types.base import ComponentCommon


class Divider(ComponentCommon):
    """A visual divider line."""

    component: Literal["Divider"] = "Divider"
    axis: Literal["horizontal", "vertical"] = Field(default="horizontal")
