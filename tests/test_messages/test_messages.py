from py_a2ui import (
    CreateSurfaceMessage,
    DeleteSurfaceMessage,
    UpdateDataModelMessage,
)


def test_create_surface_export():
    msg = CreateSurfaceMessage(surface_id="s1", catalog_id="basic")
    data = msg.export()
    assert data == {
        "version": "v0.9",
        "createSurface": {
            "surfaceId": "s1",
            "catalogId": "basic",
            "sendDataModel": False,
        },
    }


def test_delete_surface_export():
    msg = DeleteSurfaceMessage(surface_id="s1")
    data = msg.export()
    assert data == {
        "version": "v0.9",
        "deleteSurface": {
            "surfaceId": "s1",
        },
    }


def test_update_data_model_export():
    msg = UpdateDataModelMessage(surface_id="s1", path="/user/name", value="Alice")
    data = msg.export()
    assert data["version"] == "v0.9"
    payload = data["updateDataModel"]
    assert payload["surfaceId"] == "s1"
    assert payload["path"] == "/user/name"
    assert payload["value"] == "Alice"


def test_create_surface_export_json():
    msg = CreateSurfaceMessage(surface_id="s1", catalog_id="basic")
    json_str = msg.export_json()
    assert '"version": "v0.9"' in json_str
    assert '"createSurface"' in json_str


def test_message_version_property():
    msg = DeleteSurfaceMessage(surface_id="s1")
    assert msg.version == "0.9"
