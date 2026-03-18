"""Tests for the Rich tree visualization."""

from io import StringIO

from rich.console import Console

from py_a2ui import (
    Button,
    Card,
    Column,
    EventAction,
    Text,
    UpdateComponentsMessage,
)
from py_a2ui.tree import build_tree


def _render_tree(components, label="Surface"):
    """Render a tree to a plain string for assertions."""
    tree = build_tree(components, label=label)
    buf = StringIO()
    console = Console(file=buf, force_terminal=False, width=120)
    console.print(tree)
    return buf.getvalue()


def test_tree_includes_component_types():
    """Tree output includes component type names."""
    output = _render_tree(
        [
            Column(
                id="root",
                children=[
                    Text(text="Hello", variant="h1"),
                ],
            ),
        ]
    )
    assert "Column" in output
    assert "Text" in output


def test_tree_includes_ids():
    """Tree output includes explicit and auto-generated IDs."""
    output = _render_tree(
        [
            Column(
                id="my-root",
                children=[
                    Text(text="Title"),
                ],
            ),
        ]
    )
    assert "my-root" in output
    assert "text_1" in output


def test_tree_includes_text_content():
    """Tree output includes text content in quotes."""
    output = _render_tree(
        [
            Text(id="t", text="Hello World"),
        ]
    )
    assert '"Hello World"' in output


def test_tree_truncates_long_text():
    """Long text content is truncated with ellipsis."""
    long_text = "A" * 50
    output = _render_tree(
        [
            Text(id="t", text=long_text),
        ]
    )
    assert "..." in output


def test_tree_shows_variant():
    """Non-default variant is shown."""
    output = _render_tree(
        [
            Text(id="t", text="Title", variant="h1"),
        ]
    )
    assert "h1" in output


def test_tree_shows_action_event():
    """Button action event name is shown."""
    output = _render_tree(
        [
            Button(
                id="btn",
                child=Text(text="Go"),
                action=EventAction(event_name="submit"),
            ),
        ]
    )
    assert "submit" in output


def test_tree_nested_structure():
    """Tree renders nested hierarchy."""
    output = _render_tree(
        [
            Column(
                id="root",
                children=[
                    Card(child=Text(text="Inner")),
                ],
            ),
        ]
    )
    assert "Column" in output
    assert "Card" in output
    assert "Text" in output
    assert "Inner" in output


def test_tree_string_refs():
    """String child refs are rendered as dim text."""
    output = _render_tree(
        [
            Column(id="root", children=["external_ref"]),
        ]
    )
    assert "external_ref" in output


def test_print_tree_method():
    """UpdateComponentsMessage.print_tree() executes without error."""
    msg = UpdateComponentsMessage(
        surface_id="test",
        components=[
            Column(
                id="root",
                children=[
                    Text(text="Hello"),
                ],
            ),
        ],
    )
    # Should not raise
    msg.print_tree()


def test_tree_custom_label():
    """Custom label is used as root node."""
    output = _render_tree(
        [Text(id="t", text="Hi")],
        label="my-surface",
    )
    assert "my-surface" in output
