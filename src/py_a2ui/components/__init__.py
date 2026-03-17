from typing import Annotated

from pydantic import Discriminator, Tag

from py_a2ui.components.audio_player import AudioPlayer as AudioPlayer
from py_a2ui.components.button import Button as Button
from py_a2ui.components.button import ButtonVariant as ButtonVariant
from py_a2ui.components.card import Card as Card
from py_a2ui.components.check_box import CheckBox as CheckBox
from py_a2ui.components.choice_picker import ChoiceOption as ChoiceOption
from py_a2ui.components.choice_picker import ChoicePicker as ChoicePicker
from py_a2ui.components.column import Column as Column
from py_a2ui.components.date_time_input import DateTimeInput as DateTimeInput
from py_a2ui.components.divider import Divider as Divider
from py_a2ui.components.icon import CustomIcon as CustomIcon
from py_a2ui.components.icon import Icon as Icon
from py_a2ui.components.icon import IconName as IconName
from py_a2ui.components.image import Image as Image
from py_a2ui.components.image import ImageFit as ImageFit
from py_a2ui.components.image import ImageVariant as ImageVariant
from py_a2ui.components.list import List as List
from py_a2ui.components.modal import Modal as Modal
from py_a2ui.components.row import Align as Align
from py_a2ui.components.row import Justify as Justify
from py_a2ui.components.row import Row as Row
from py_a2ui.components.slider import Slider as Slider
from py_a2ui.components.tabs import Tab as Tab
from py_a2ui.components.tabs import Tabs as Tabs
from py_a2ui.components.text import Text as Text
from py_a2ui.components.text import TextVariant as TextVariant
from py_a2ui.components.text_field import TextField as TextField
from py_a2ui.components.text_field import TextFieldVariant as TextFieldVariant
from py_a2ui.components.video import Video as Video

AnyComponent = Annotated[
    Annotated[AudioPlayer, Tag("AudioPlayer")]
    | Annotated[Button, Tag("Button")]
    | Annotated[Card, Tag("Card")]
    | Annotated[CheckBox, Tag("CheckBox")]
    | Annotated[ChoicePicker, Tag("ChoicePicker")]
    | Annotated[Column, Tag("Column")]
    | Annotated[DateTimeInput, Tag("DateTimeInput")]
    | Annotated[Divider, Tag("Divider")]
    | Annotated[Icon, Tag("Icon")]
    | Annotated[Image, Tag("Image")]
    | Annotated[List, Tag("List")]
    | Annotated[Modal, Tag("Modal")]
    | Annotated[Row, Tag("Row")]
    | Annotated[Slider, Tag("Slider")]
    | Annotated[Tabs, Tag("Tabs")]
    | Annotated[Text, Tag("Text")]
    | Annotated[TextField, Tag("TextField")]
    | Annotated[Video, Tag("Video")],
    Discriminator("component"),
]
