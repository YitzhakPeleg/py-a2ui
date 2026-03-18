from typing import Annotated, Any

from pydantic import Discriminator, Tag

from py_a2ui.messages.base import A2UI_VERSION as A2UI_VERSION
from py_a2ui.messages.base import A2UIMessage as A2UIMessage
from py_a2ui.messages.create_surface import CreateSurfaceMessage as CreateSurfaceMessage
from py_a2ui.messages.delete_surface import DeleteSurfaceMessage as DeleteSurfaceMessage
from py_a2ui.messages.update_components import UpdateComponentsMessage as UpdateComponentsMessage
from py_a2ui.messages.update_data_model import UpdateDataModelMessage as UpdateDataModelMessage

_MESSAGE_KEYS = frozenset(("createSurface", "updateComponents", "updateDataModel", "deleteSurface"))


def _server_message_discriminator(raw: Any) -> str:
    if not isinstance(raw, dict):
        raise TypeError(f"Expected dict, got {type(raw).__name__}")
    found = _MESSAGE_KEYS & raw.keys()
    match len(found):
        case 1:
            return found.pop()
        case 0:
            raise ValueError(f"No recognized message key in {raw.keys()}")
        case _:
            raise ValueError(f"Multiple message keys found: {found}")


ServerMessage = Annotated[
    Annotated[CreateSurfaceMessage, Tag("createSurface")]
    | Annotated[DeleteSurfaceMessage, Tag("deleteSurface")]
    | Annotated[UpdateComponentsMessage, Tag("updateComponents")]
    | Annotated[UpdateDataModelMessage, Tag("updateDataModel")],
    Discriminator(_server_message_discriminator),
]
