from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict

from py_a2ui.types.base import ComponentCommon


class IconName(StrEnum):
    ACCOUNT_CIRCLE = "accountCircle"
    ADD = "add"
    ARROW_BACK = "arrowBack"
    ARROW_FORWARD = "arrowForward"
    ATTACH_FILE = "attachFile"
    CALENDAR_TODAY = "calendarToday"
    CALL = "call"
    CAMERA = "camera"
    CHECK = "check"
    CLOSE = "close"
    DELETE = "delete"
    DOWNLOAD = "download"
    EDIT = "edit"
    EVENT = "event"
    ERROR = "error"
    FAST_FORWARD = "fastForward"
    FAVORITE = "favorite"
    FAVORITE_OFF = "favoriteOff"
    FOLDER = "folder"
    HELP = "help"
    HOME = "home"
    INFO = "info"
    LOCATION_ON = "locationOn"
    LOCK = "lock"
    LOCK_OPEN = "lockOpen"
    MAIL = "mail"
    MENU = "menu"
    MORE_VERT = "moreVert"
    MORE_HORIZ = "moreHoriz"
    NOTIFICATIONS_OFF = "notificationsOff"
    NOTIFICATIONS = "notifications"
    PAUSE = "pause"
    PAYMENT = "payment"
    PERSON = "person"
    PHONE = "phone"
    PHOTO = "photo"
    PLAY = "play"
    PRINT = "print"
    REFRESH = "refresh"
    REWIND = "rewind"
    SEARCH = "search"
    SEND = "send"
    SETTINGS = "settings"
    SHARE = "share"
    SHOPPING_CART = "shoppingCart"
    SKIP_NEXT = "skipNext"
    SKIP_PREVIOUS = "skipPrevious"
    STAR = "star"
    STAR_HALF = "starHalf"
    STAR_OFF = "starOff"
    STOP = "stop"
    UPLOAD = "upload"
    VISIBILITY = "visibility"
    VISIBILITY_OFF = "visibilityOff"
    VOLUME_DOWN = "volumeDown"
    VOLUME_MUTE = "volumeMute"
    VOLUME_OFF = "volumeOff"
    VOLUME_UP = "volumeUp"
    WARNING = "warning"


class CustomIcon(BaseModel):
    """A custom icon referenced by path."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    path: str


class Icon(ComponentCommon):
    """An icon component. Supports built-in icon names or custom icon paths."""

    component: Literal["Icon"] = "Icon"
    name: IconName | CustomIcon
