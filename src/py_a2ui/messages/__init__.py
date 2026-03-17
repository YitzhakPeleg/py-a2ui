from typing import Annotated

from pydantic import Discriminator, Tag

from py_a2ui.messages.call_function import CallFunctionMessage as CallFunctionMessage
from py_a2ui.messages.create_surface import A2UI_VERSION as A2UI_VERSION
from py_a2ui.messages.create_surface import CreateSurfaceMessage as CreateSurfaceMessage
from py_a2ui.messages.delete_surface import DeleteSurfaceMessage as DeleteSurfaceMessage
from py_a2ui.messages.update_components import UpdateComponentsMessage as UpdateComponentsMessage
from py_a2ui.messages.update_data_model import UpdateDataModelMessage as UpdateDataModelMessage

ServerMessage = Annotated[
    Annotated[CallFunctionMessage, Tag("callFunction")]
    | Annotated[CreateSurfaceMessage, Tag("createSurface")]
    | Annotated[DeleteSurfaceMessage, Tag("deleteSurface")]
    | Annotated[UpdateComponentsMessage, Tag("updateComponents")]
    | Annotated[UpdateDataModelMessage, Tag("updateDataModel")],
    Discriminator("type"),
]
