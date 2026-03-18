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
    data = msg.export()

    assert data["version"] == "v0.9"
    payload = data["updateComponents"]
    assert payload["surfaceId"] == "booking"
    assert len(payload["components"]) == 6

    # Verify root component
    root = payload["components"][0]
    assert root["component"] == "Column"
    assert root["children"] == ["title", "card1"]


def test_update_components_json_roundtrip():
    msg = UpdateComponentsMessage(
        surface_id="test",
        components=[Text(id="root", text="Hello")],
    )
    json_str = msg.export_json()
    parsed = json.loads(json_str)
    assert parsed["version"] == "v0.9"
    payload = parsed["updateComponents"]
    assert payload["surfaceId"] == "test"
    assert payload["components"][0]["text"] == "Hello"
