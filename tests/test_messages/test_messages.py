from py_a2ui import (
    CreateSurfaceMessage,
    DeleteSurfaceMessage,
    UpdateDataModelMessage,
)


def test_create_surface():
    msg = CreateSurfaceMessage(surface_id="s1", catalog_id="basic")
    data = msg.model_dump(by_alias=True, exclude_none=True)
    assert data == {
        "version": "v0.10",
        "type": "createSurface",
        "surfaceId": "s1",
        "catalogId": "basic",
        "sendDataModel": False,
    }


def test_delete_surface():
    msg = DeleteSurfaceMessage(surface_id="s1")
    data = msg.model_dump(by_alias=True, exclude_none=True)
    assert data == {
        "version": "v0.10",
        "type": "deleteSurface",
        "surfaceId": "s1",
    }


def test_update_data_model():
    msg = UpdateDataModelMessage(surface_id="s1", path="/user/name", value="Alice")
    data = msg.model_dump(by_alias=True, exclude_none=True)
    assert data["surfaceId"] == "s1"
    assert data["path"] == "/user/name"
    assert data["value"] == "Alice"
