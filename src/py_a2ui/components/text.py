from enum import StrEnum
from typing import Literal

from pydantic import Field

from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.dynamic import DynamicString


class TextVariant(StrEnum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    CAPTION = "caption"
    BODY = "body"


class Text(ComponentCommon):
    """A text display component. Supports simple Markdown formatting."""

    component: Literal["Text"] = "Text"
    text: DynamicString
    variant: TextVariant = Field(default=TextVariant.BODY)
