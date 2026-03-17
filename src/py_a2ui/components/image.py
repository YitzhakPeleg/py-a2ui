from enum import StrEnum
from typing import Literal

from pydantic import Field

from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicString


class ImageFit(StrEnum):
    CONTAIN = "contain"
    COVER = "cover"
    FILL = "fill"
    NONE = "none"
    SCALE_DOWN = "scaleDown"


class ImageVariant(StrEnum):
    ICON = "icon"
    AVATAR = "avatar"
    SMALL_FEATURE = "smallFeature"
    MEDIUM_FEATURE = "mediumFeature"
    LARGE_FEATURE = "largeFeature"
    HEADER = "header"


class Image(ComponentCommon):
    """An image display component."""

    component: Literal["Image"] = "Image"
    url: DynamicString
    fit: ImageFit = Field(default=ImageFit.FILL)
    variant: ImageVariant = Field(default=ImageVariant.MEDIUM_FEATURE)
