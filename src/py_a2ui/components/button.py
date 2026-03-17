from enum import StrEnum
from typing import Literal

from pydantic import Field

from py_a2ui.actions.action import Action
from py_a2ui.types.base import ComponentCommon, ComponentId


class ButtonVariant(StrEnum):
    DEFAULT = "default"
    PRIMARY = "primary"
    BORDERLESS = "borderless"


class Button(ComponentCommon):
    """An interactive button component."""

    component: Literal["Button"] = "Button"
    child: ComponentId
    variant: ButtonVariant = Field(default=ButtonVariant.DEFAULT)
    action: Action
