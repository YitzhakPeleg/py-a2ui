"""Round-trip serialization tests: construct → JSON → parse back."""

import json

from pydantic import TypeAdapter

from py_a2ui import (
    AnyComponent,
    CheckBox,
    Column,
    DataBinding,
    Slider,
    Text,
)


def test_any_component_discriminator():
    """Verify AnyComponent discriminated union works for deserialization."""
    adapter = TypeAdapter(AnyComponent)

    raw = {"id": "t1", "component": "Text", "text": "Hello", "variant": "body"}
    comp = adapter.validate_python(raw)
    assert isinstance(comp, Text)
    assert comp.text == "Hello"


def test_any_component_roundtrip():
    col = Column(id="root", children=["a", "b"])
    data = col.model_dump(by_alias=True, exclude_none=True)
    adapter = TypeAdapter(AnyComponent)
    restored = adapter.validate_python(data)
    assert isinstance(restored, Column)
    assert restored.children == ["a", "b"]


def test_data_binding_roundtrip():
    cb = CheckBox(id="cb", label="Agree", value=DataBinding(path="/agreed"))
    data = cb.model_dump(by_alias=True, exclude_none=True)
    assert data["value"] == {"path": "/agreed"}

    restored = CheckBox.model_validate(data)
    assert isinstance(restored.value, DataBinding)
    assert restored.value.path == "/agreed"


def test_slider_numeric_roundtrip():
    s = Slider(id="s", max=100, value=42.5)
    json_str = s.model_dump_json(by_alias=True, exclude_none=True)
    restored = Slider.model_validate_json(json_str)
    assert restored.value == 42.5
    assert restored.max == 100


def test_full_json_output():
    """Verify JSON output uses camelCase aliases."""
    col = Column(id="root", children=["child1"])
    json_str = col.model_dump_json(by_alias=True, exclude_none=True)
    parsed = json.loads(json_str)
    assert "component" in parsed
    assert "children" in parsed
    assert "id" in parsed
