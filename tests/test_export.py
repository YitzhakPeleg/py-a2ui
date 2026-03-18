"""Tests for the flatten/export functionality."""

import pytest

from py_a2ui import (
    Button,
    Card,
    Column,
    DynamicChildTemplate,
    EventAction,
    List,
    Modal,
    Row,
    Tab,
    Tabs,
    Text,
    UpdateComponentsMessage,
    flatten,
)


def test_nested_construction_and_export():
    """Nested components are flattened to wire-format dicts."""
    msg = UpdateComponentsMessage(
        surface_id="test",
        components=[
            Column(
                id="root",
                children=[
                    Text(text="Hello", variant="h1"),
                    Card(child=Text(text="Inner")),
                ],
            ),
        ],
    )
    result = msg.export()
    assert result["version"] == "v0.10"
    assert result["type"] == "updateComponents"
    assert result["surfaceId"] == "test"

    comps = result["components"]
    # Flattened order: Text (leaf), Text (leaf), Card, Column (DFS post-order-ish)
    # Actually: walk root first, encounter children, recurse into each
    # The root is processed first: it walks children, flattens them, then appends itself
    # Wait - looking at export.py, children are flattened BEFORE the parent is appended
    # So order is: text_1, text_2 (inner Card child), card_3, root (Column)

    # Let's just verify the IDs and structure
    ids = [c["id"] for c in comps]
    assert "root" in ids

    # Find root component
    root = next(c for c in comps if c["id"] == "root")
    assert root["component"] == "Column"
    # Children should be string IDs now
    assert all(isinstance(ch, str) for ch in root["children"])


def test_auto_id_generation_pattern():
    """Auto-generated IDs follow {type}_{counter} pattern."""
    components = [
        Column(
            id="root",
            children=[
                Text(text="First"),
                Text(text="Second"),
                Card(child=Text(text="Third")),
            ],
        ),
    ]
    result = flatten(components)
    ids = [c["id"] for c in result]

    # Auto-generated IDs: counter increments for every component
    # Order: Text("First")=text_1, Text("Second")=text_2, Text("Third")=text_N, Card=card_N
    assert "text_1" in ids
    assert "text_2" in ids
    assert "root" in ids
    # Card and inner text also get auto IDs
    card_ids = [i for i in ids if i.startswith("card_")]
    assert len(card_ids) == 1
    text_ids = [i for i in ids if i.startswith("text_")]
    assert len(text_ids) == 3


def test_explicit_id_preserved():
    """Explicit IDs on inner components are preserved."""
    components = [
        Column(
            id="root",
            children=[
                Text(id="my-title", text="Hello"),
            ],
        ),
    ]
    result = flatten(components)
    ids = [c["id"] for c in result]
    assert "my-title" in ids
    assert "root" in ids


def test_dynamic_child_template_passthrough():
    """DynamicChildTemplate children pass through without modification."""
    components = [
        List(
            id="items",
            children=DynamicChildTemplate(component_id="item_row", path="/items"),
        ),
    ]
    result = flatten(components)
    assert len(result) == 1
    items = result[0]
    assert items["id"] == "items"
    # DynamicChildTemplate should be serialized as dict
    assert items["children"]["componentId"] == "item_row"
    assert items["children"]["path"] == "/items"


def test_missing_root_id_raises():
    """Top-level components without id raise ValueError."""
    with pytest.raises(ValueError, match="must have an explicit id"):
        flatten([Text(text="No ID")])


def test_duplicate_id_raises():
    """Duplicate IDs across the tree raise ValueError."""
    with pytest.raises(ValueError, match="Duplicate component id"):
        flatten(
            [
                Column(
                    id="root",
                    children=[
                        Text(id="dupe", text="One"),
                        Text(id="dupe", text="Two"),
                    ],
                ),
            ]
        )


def test_mixed_nesting_string_and_object():
    """Mix of string IDs and nested objects in children."""
    components = [
        Column(
            id="root",
            children=[
                "external_ref",
                Text(text="Nested"),
            ],
        ),
    ]
    result = flatten(components)
    root = next(c for c in result if c["id"] == "root")
    assert root["children"] == ["external_ref", "text_1"]


def test_button_nested_child():
    """Button with nested Text child."""
    components = [
        Button(
            id="btn",
            child=Text(text="Click Me"),
            action=EventAction(event_name="click"),
        ),
    ]
    result = flatten(components)
    assert len(result) == 2
    text_comp = next(c for c in result if c["component"] == "Text")
    btn_comp = next(c for c in result if c["component"] == "Button")
    assert btn_comp["child"] == text_comp["id"]
    assert text_comp["text"] == "Click Me"


def test_modal_nested_trigger_and_content():
    """Modal with nested trigger and content components."""
    components = [
        Modal(
            id="modal",
            trigger=Button(
                child=Text(text="Open"),
                action=EventAction(event_name="open"),
            ),
            content=Column(
                children=[
                    Text(text="Modal body"),
                ]
            ),
        ),
    ]
    result = flatten(components)
    modal = next(c for c in result if c["id"] == "modal")
    assert isinstance(modal["trigger"], str)
    assert isinstance(modal["content"], str)
    # All components flattened
    assert len(result) == 5  # Text("Open"), Button, Text("Modal body"), Column, Modal


def test_tabs_nested_children():
    """Tabs with nested child components in each tab."""
    components = [
        Tabs(
            id="tabs",
            tabs=[
                Tab(title="Tab 1", child=Column(children=[Text(text="Page 1")])),
                Tab(title="Tab 2", child=Text(text="Page 2")),
            ],
        ),
    ]
    result = flatten(components)
    tabs_comp = next(c for c in result if c["id"] == "tabs")
    # Tab children should be string IDs
    assert isinstance(tabs_comp["tabs"][0]["child"], str)
    assert isinstance(tabs_comp["tabs"][1]["child"], str)


def test_export_json():
    """export_json() returns valid JSON string."""
    msg = UpdateComponentsMessage(
        surface_id="test",
        components=[Text(id="t1", text="Hi")],
    )
    json_str = msg.export_json(indent=2)
    import json

    parsed = json.loads(json_str)
    assert parsed["surfaceId"] == "test"
    assert parsed["components"][0]["id"] == "t1"


def test_deeply_nested_tree():
    """A deeply nested tree flattens correctly."""
    msg = UpdateComponentsMessage(
        surface_id="deep",
        components=[
            Column(
                id="root",
                children=[
                    Card(
                        child=Column(
                            children=[
                                Card(
                                    child=Column(
                                        children=[
                                            Text(text="Leaf"),
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                ],
            ),
        ],
    )
    result = msg.export()
    comps = result["components"]
    # Should have: Text, Column, Card, Column, Card, Column(root) = 6
    assert len(comps) == 6
    # All should have IDs
    for c in comps:
        assert "id" in c
        assert c["id"] is not None


def test_row_nested_children():
    """Row with nested components in children."""
    components = [
        Row(
            id="row",
            children=[
                Text(text="Left"),
                Text(text="Right"),
            ],
        ),
    ]
    result = flatten(components)
    row = next(c for c in result if c["id"] == "row")
    assert len(row["children"]) == 2
    assert all(isinstance(ch, str) for ch in row["children"])


def test_id_none_allowed_for_inner_components():
    """Inner components with id=None get auto-generated IDs."""
    col = Column(
        id="root",
        children=[
            Text(text="A"),
            Text(text="B"),
        ],
    )
    assert col.children[0].id is None
    assert col.children[1].id is None

    result = flatten([col])
    text_ids = [c["id"] for c in result if c["component"] == "Text"]
    assert len(text_ids) == 2
    assert text_ids[0] != text_ids[1]
