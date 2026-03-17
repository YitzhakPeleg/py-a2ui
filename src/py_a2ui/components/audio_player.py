from typing import Literal

from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicString


class AudioPlayer(ComponentCommon):
    """An audio player component."""

    component: Literal["AudioPlayer"] = "AudioPlayer"
    url: DynamicString
    description: DynamicString | None = None
