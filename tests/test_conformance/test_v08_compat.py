"""Tests for v0.8 export compatibility.

Validates that py-a2ui objects exported with version="0.8" produce
valid v0.8 wire format, compared against official v0.8 example files.
"""

import json
from pathlib import Path

import pytest

from py_a2ui import (
    Button,
    ButtonVariant,
    Column,
    CreateSurfaceMessage,
    DeleteSurfaceMessage,
    Divider,
    EventAction,
    FunctionAction,
    FunctionCall,
    Icon,
    Image,
    Row,
    Text,
    TextField,
    TextFieldVariant,
    TextVariant,
    UpdateComponentsMessage,
    UpdateDataModelMessage,
)

CASES_V08_DIR = Path(__file__).parent / "cases_v08"


# ---------------------------------------------------------------------------
# Envelope tests
# ---------------------------------------------------------------------------


class TestV08Envelope:
    """Verify v0.8 message envelope format."""

    def test_no_version_field(self):
        """v0.8 messages have no version field."""
        msg = DeleteSurfaceMessage(surface_id="test")
        data = msg.export(version="0.8")
        assert "version" not in data

    def test_delete_surface_key_unchanged(self):
        """deleteSurface key is the same in v0.8."""
        msg = DeleteSurfaceMessage(surface_id="test")
        data = msg.export(version="0.8")
        assert "deleteSurface" in data
        assert data["deleteSurface"]["surfaceId"] == "test"

    def test_create_surface_becomes_begin_rendering(self):
        """createSurface → beginRendering with root field."""
        msg = CreateSurfaceMessage(
            surface_id="s1",
            catalog_id="https://example.com/catalog.json",
        )
        data = msg.export(version="0.8")
        assert "beginRendering" in data
        assert "createSurface" not in data
        br = data["beginRendering"]
        assert br["surfaceId"] == "s1"
        assert br["catalogId"] == "https://example.com/catalog.json"
        assert br["root"] == "root"  # default root

    def test_create_surface_theme_becomes_styles(self):
        """theme → styles in v0.8 beginRendering."""
        msg = CreateSurfaceMessage(
            surface_id="s1",
            catalog_id="cat",
            theme={"primaryColor": "#ff0000"},
        )
        data = msg.export(version="0.8")
        br = data["beginRendering"]
        assert "theme" not in br
        assert br["styles"] == {"primaryColor": "#ff0000"}

    def test_update_components_becomes_surface_update(self):
        """updateComponents → surfaceUpdate in v0.8."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[Text(id="t1", text="Hello")],
        )
        data = msg.export(version="0.8")
        assert "surfaceUpdate" in data
        assert "updateComponents" not in data
        su = data["surfaceUpdate"]
        assert su["surfaceId"] == "s1"
        assert len(su["components"]) == 1

    def test_update_data_model_becomes_data_model_update(self):
        """updateDataModel → dataModelUpdate in v0.8."""
        msg = UpdateDataModelMessage(
            surface_id="s1",
            path="/",
            value={"name": "test"},
        )
        data = msg.export(version="0.8")
        assert "dataModelUpdate" in data
        assert "updateDataModel" not in data
        dmu = data["dataModelUpdate"]
        assert dmu["surfaceId"] == "s1"

    def test_v09_export_still_works(self):
        """Default export still produces v0.9 format."""
        msg = DeleteSurfaceMessage(surface_id="test")
        data = msg.export()
        assert data["version"] == "v0.9"
        assert "deleteSurface" in data


# ---------------------------------------------------------------------------
# Component structure tests
# ---------------------------------------------------------------------------


class TestV08ComponentStructure:
    """Verify v0.8 nested component wrapper format."""

    def test_text_component_nested_wrapper(self):
        """Text becomes {"id","component":{"Text":{"text":{"literalString":...},"usageHint":...}}}."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[Text(id="t1", text="Hello", variant=TextVariant.H1)],
        )
        data = msg.export(version="0.8")
        comp = data["surfaceUpdate"]["components"][0]
        assert comp["id"] == "t1"
        assert "Text" in comp["component"]
        text_inner = comp["component"]["Text"]
        assert text_inner["text"] == {"literalString": "Hello"}
        assert text_inner["usageHint"] == "h1"

    def test_text_data_binding(self):
        """Data bindings stay as {path: "/..."}."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[Text(id="t1", text={"path": "/name"})],
        )
        data = msg.export(version="0.8")
        text_inner = data["surfaceUpdate"]["components"][0]["component"]["Text"]
        assert text_inner["text"] == {"path": "/name"}

    def test_column_children_explicit_list(self):
        """Children array becomes {explicitList: [...]}."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                Column(
                    id="col",
                    children=[
                        Text(text="A"),
                        Text(text="B"),
                    ],
                ),
            ],
        )
        data = msg.export(version="0.8")
        components = data["surfaceUpdate"]["components"]
        # Find the Column component
        col = next(c for c in components if "Column" in c["component"])
        children = col["component"]["Column"]["children"]
        assert "explicitList" in children
        assert len(children["explicitList"]) == 2

    def test_row_field_renames(self):
        """Row: justify → distribution, align → alignment."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                Row(id="r1", children=["c1"], justify="spaceBetween", align="center"),
            ],
        )
        data = msg.export(version="0.8")
        row_inner = data["surfaceUpdate"]["components"][0]["component"]["Row"]
        assert row_inner["distribution"] == "spaceBetween"
        assert row_inner["alignment"] == "center"
        assert "justify" not in row_inner
        assert "align" not in row_inner

    def test_button_variant_primary(self):
        """Button variant=primary becomes primary=true in v0.8."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                Button(
                    id="btn",
                    child="label",
                    variant=ButtonVariant.PRIMARY,
                    action=EventAction(event_name="click"),
                ),
            ],
        )
        data = msg.export(version="0.8")
        btn_inner = data["surfaceUpdate"]["components"][0]["component"]["Button"]
        assert btn_inner.get("primary") is True
        assert "variant" not in btn_inner

    def test_button_default_variant_no_primary(self):
        """Button variant=default → no primary field in v0.8."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                Button(
                    id="btn",
                    child="label",
                    variant=ButtonVariant.DEFAULT,
                    action=EventAction(event_name="click"),
                ),
            ],
        )
        data = msg.export(version="0.8")
        btn_inner = data["surfaceUpdate"]["components"][0]["component"]["Button"]
        assert "primary" not in btn_inner
        assert "variant" not in btn_inner

    def test_text_field_renames(self):
        """TextField: value → text, variant → textFieldType."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                TextField(
                    id="tf1",
                    label="Email",
                    value={"path": "/email"},
                    variant=TextFieldVariant.OBSCURED,
                ),
            ],
        )
        data = msg.export(version="0.8")
        tf_inner = data["surfaceUpdate"]["components"][0]["component"]["TextField"]
        assert tf_inner["text"] == {"path": "/email"}
        assert tf_inner["textFieldType"] == "obscured"
        assert "value" not in tf_inner
        assert "variant" not in tf_inner

    def test_divider_empty_inner(self):
        """Divider becomes {"Divider": {}}."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[Divider(id="d1")],
        )
        data = msg.export(version="0.8")
        comp = data["surfaceUpdate"]["components"][0]
        assert comp["component"]["Divider"] == {}

    def test_icon_name_wrapped(self):
        """Icon name is a DynamicString, should be wrapped."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[Icon(id="i1", name="favorite")],
        )
        data = msg.export(version="0.8")
        icon_inner = data["surfaceUpdate"]["components"][0]["component"]["Icon"]
        assert icon_inner["name"] == {"literalString": "favorite"}

    def test_image_variant_becomes_usage_hint(self):
        """Image: variant → usageHint."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[Image(id="img", url="https://example.com/img.jpg", variant="icon")],
        )
        data = msg.export(version="0.8")
        img_inner = data["surfaceUpdate"]["components"][0]["component"]["Image"]
        assert img_inner["usageHint"] == "icon"
        assert "variant" not in img_inner

    def test_weight_preserved(self):
        """Component weight stays at the outer level."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                Row(id="r1", children=["a", "b"]),
            ],
        )
        # Manually add weight to test (weight is set on the component wrapper, not model)
        data = msg.export(version="0.8")
        # Weight is only present if the v0.9 flat component had it
        # This test verifies the structure doesn't break when weight is absent
        comp = data["surfaceUpdate"]["components"][0]
        assert "weight" not in comp  # not set, so not present


# ---------------------------------------------------------------------------
# Action conversion tests
# ---------------------------------------------------------------------------


class TestV08ActionFormat:
    """Verify v0.8 action format."""

    def test_event_action_simple(self):
        """EventAction becomes {name, context: []}."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                Button(
                    id="btn",
                    child="label",
                    action=EventAction(event_name="submit"),
                ),
            ],
        )
        data = msg.export(version="0.8")
        action = data["surfaceUpdate"]["components"][0]["component"]["Button"]["action"]
        assert action["name"] == "submit"
        assert action["context"] == []

    def test_event_action_with_context(self):
        """EventAction context dict → list of {key, value} entries."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                Button(
                    id="btn",
                    child="label",
                    action=EventAction(
                        event_name="submit",
                        event_context={"user": "test"},
                    ),
                ),
            ],
        )
        data = msg.export(version="0.8")
        action = data["surfaceUpdate"]["components"][0]["component"]["Button"]["action"]
        assert action["name"] == "submit"
        assert len(action["context"]) == 1
        assert action["context"][0]["key"] == "user"
        assert action["context"][0]["value"] == {"literalString": "test"}

    def test_function_action_raises(self):
        """FunctionAction raises ValueError for v0.8."""
        msg = UpdateComponentsMessage(
            surface_id="s1",
            components=[
                Button(
                    id="btn",
                    child="label",
                    action=FunctionAction(
                        function_call=FunctionCall(call="openUrl", args={"url": "https://example.com"}),
                    ),
                ),
            ],
        )
        with pytest.raises(ValueError, match="FunctionAction not supported"):
            msg.export(version="0.8")


# ---------------------------------------------------------------------------
# Data model conversion tests
# ---------------------------------------------------------------------------


class TestV08DataModel:
    """Verify v0.8 dataModelUpdate format."""

    def test_value_dict_becomes_contents(self):
        """value dict → contents array with typed entries."""
        msg = UpdateDataModelMessage(
            surface_id="s1",
            path="/",
            value={"name": "Alice", "age": 30},
        )
        data = msg.export(version="0.8")
        dmu = data["dataModelUpdate"]
        assert "contents" in dmu
        assert "value" not in dmu
        contents = dmu["contents"]
        name_entry = next(e for e in contents if e["key"] == "name")
        assert name_entry["valueString"] == "Alice"
        age_entry = next(e for e in contents if e["key"] == "age")
        assert age_entry["valueNumber"] == 30


# ---------------------------------------------------------------------------
# Comparison with official v0.8 examples
# ---------------------------------------------------------------------------


def _load_v08_example(subdir: str, filename: str) -> list[dict]:
    """Load a v0.8 example file."""
    path = CASES_V08_DIR / subdir / filename
    return json.loads(path.read_text())


def _find_message(messages: list[dict], key: str) -> dict | None:
    """Find a message by its key."""
    for msg in messages:
        if key in msg:
            return msg
    return None


class TestV08ExampleStructure:
    """Verify v0.8 example files match expected structure patterns."""

    @pytest.mark.parametrize(
        "filename", sorted(f.name for f in (CASES_V08_DIR / "minimal").iterdir() if f.suffix == ".json")
    )
    def test_minimal_examples_valid_structure(self, filename: str):
        """Every minimal example has surfaceUpdate + beginRendering."""
        messages = _load_v08_example("minimal", filename)

        su = _find_message(messages, "surfaceUpdate")
        assert su is not None, f"Missing surfaceUpdate in {filename}"
        assert "surfaceId" in su["surfaceUpdate"]
        assert "components" in su["surfaceUpdate"]

        br = _find_message(messages, "beginRendering")
        assert br is not None, f"Missing beginRendering in {filename}"
        assert "surfaceId" in br["beginRendering"]
        assert "root" in br["beginRendering"]

        # No version field in any v0.8 message
        for msg in messages:
            assert "version" not in msg

    @pytest.mark.parametrize(
        "filename", sorted(f.name for f in (CASES_V08_DIR / "basic").iterdir() if f.suffix == ".json")
    )
    def test_basic_examples_valid_structure(self, filename: str):
        """Every basic example has surfaceUpdate + beginRendering."""
        messages = _load_v08_example("basic", filename)

        su = _find_message(messages, "surfaceUpdate")
        assert su is not None, f"Missing surfaceUpdate in {filename}"

        br = _find_message(messages, "beginRendering")
        assert br is not None, f"Missing beginRendering in {filename}"

        for msg in messages:
            assert "version" not in msg

    @pytest.mark.parametrize(
        "filename", sorted(f.name for f in (CASES_V08_DIR / "minimal").iterdir() if f.suffix == ".json")
    )
    def test_minimal_component_format(self, filename: str):
        """All components in minimal examples use nested wrapper format."""
        messages = _load_v08_example("minimal", filename)
        su = _find_message(messages, "surfaceUpdate")
        for comp in su["surfaceUpdate"]["components"]:
            assert "id" in comp
            assert isinstance(comp["component"], dict), (
                f"Component {comp['id']} should have nested wrapper, got {type(comp['component'])}"
            )
            # Exactly one key in the component wrapper
            assert len(comp["component"]) == 1, f"Component {comp['id']} wrapper should have exactly one key"


class TestV08ExportMatchesExamples:
    """Build py-a2ui objects and verify export(version='0.8') matches v0.8 examples."""

    def test_simple_text(self):
        """Replicate minimal/1_simple_text.json."""
        msg = UpdateComponentsMessage(
            surface_id="1_simple_text",
            components=[Text(id="root", text="Hello, Minimal Catalog!", variant=TextVariant.H1)],
        )
        data = msg.export(version="0.8")

        expected = _load_v08_example("minimal", "1_simple_text.json")
        expected_su = _find_message(expected, "surfaceUpdate")["surfaceUpdate"]

        assert data["surfaceUpdate"]["surfaceId"] == expected_su["surfaceId"]
        comp = data["surfaceUpdate"]["components"][0]
        expected_comp = expected_su["components"][0]
        assert comp["id"] == expected_comp["id"]
        assert comp["component"]["Text"]["text"] == expected_comp["component"]["Text"]["text"]
        assert comp["component"]["Text"]["usageHint"] == expected_comp["component"]["Text"]["usageHint"]

    def test_interactive_button(self):
        """Replicate minimal/3_interactive_button.json component structure."""
        msg = UpdateComponentsMessage(
            surface_id="3_interactive_button",
            components=[
                Column(id="root", children=["title", "action_button"], justify="center", align="center"),
                Text(id="title", text="Click the button below", variant=TextVariant.BODY),
                Button(
                    id="action_button",
                    child="button_label",
                    variant=ButtonVariant.PRIMARY,
                    action=EventAction(event_name="button_clicked"),
                ),
                Text(id="button_label", text="Click Me"),
            ],
        )
        data = msg.export(version="0.8")

        expected = _load_v08_example("minimal", "3_interactive_button.json")
        expected_su = _find_message(expected, "surfaceUpdate")["surfaceUpdate"]

        # Check Column
        col = data["surfaceUpdate"]["components"][0]
        exp_col = expected_su["components"][0]
        assert col["component"]["Column"]["children"] == exp_col["component"]["Column"]["children"]
        assert col["component"]["Column"]["distribution"] == exp_col["component"]["Column"]["distribution"]
        assert col["component"]["Column"]["alignment"] == exp_col["component"]["Column"]["alignment"]

        # Check Button
        btn = next(c for c in data["surfaceUpdate"]["components"] if "Button" in c["component"])
        exp_btn = next(c for c in expected_su["components"] if "Button" in c["component"])
        assert btn["component"]["Button"]["primary"] == exp_btn["component"]["Button"]["primary"]
        assert btn["component"]["Button"]["action"]["name"] == exp_btn["component"]["Button"]["action"]["name"]
