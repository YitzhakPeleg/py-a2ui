import json

from py_a2ui import (
    Button,
    Card,
    Column,
    EventAction,
    Text,
    UpdateComponentsMessage,
)


def test_update_components_booking_example():
    """Test the booking form example from the plan."""
    msg = UpdateComponentsMessage(
        surface_id="booking",
        components=[
            Column(id="root", children=["title", "card1"]),
            Text(id="title", text="Book Your Table", variant="h1"),
            Card(id="card1", child="form"),
            Column(id="form", children=["submit_btn"]),
            Button(
                id="submit_btn",
                child="submit_label",
                variant="primary",
                action=EventAction(event_name="submit"),
            ),
            Text(id="submit_label", text="Reserve"),
        ],
    )
    data = msg.model_dump(by_alias=True, exclude_none=True)

    assert data["version"] == "v0.10"
    assert data["type"] == "updateComponents"
    assert data["surfaceId"] == "booking"
    assert len(data["components"]) == 6

    # Verify root component
    root = data["components"][0]
    assert root["component"] == "Column"
    assert root["children"] == ["title", "card1"]


def test_update_components_json_roundtrip():
    msg = UpdateComponentsMessage(
        surface_id="test",
        components=[Text(id="root", text="Hello")],
    )
    json_str = msg.model_dump_json(by_alias=True, exclude_none=True)
    parsed = json.loads(json_str)
    assert parsed["surfaceId"] == "test"
    assert parsed["components"][0]["text"] == "Hello"
