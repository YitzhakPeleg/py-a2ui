from typing import Literal

from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicString


class Video(ComponentCommon):
    """A video player component."""

    component: Literal["Video"] = "Video"
    url: DynamicString
