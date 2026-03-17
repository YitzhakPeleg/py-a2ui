import pytest
from pydantic import ValidationError

from py_a2ui import (
    CheckBox,
    ChoiceOption,
    ChoicePicker,
    DataBinding,
    DateTimeInput,
    Slider,
    TextField,
)


def test_text_field_defaults():
    tf = TextField(id="name", label="Name")
    data = tf.model_dump(by_alias=True, exclude_none=True)
    assert data == {
        "id": "name",
        "component": "TextField",
        "label": "Name",
        "variant": "shortText",
    }


def test_text_field_with_data_binding():
    tf = TextField(id="name", label="Name", value=DataBinding(path="/user/name"))
    data = tf.model_dump(by_alias=True, exclude_none=True)
    assert data["value"] == {"path": "/user/name"}


def test_checkbox():
    cb = CheckBox(id="agree", label="I agree", value=True)
    data = cb.model_dump(by_alias=True, exclude_none=True)
    assert data["value"] is True


def test_choice_picker():
    cp = ChoicePicker(
        id="color",
        options=[ChoiceOption(label="Red", value="red"), ChoiceOption(label="Blue", value="blue")],
        value=["red"],
    )
    data = cp.model_dump(by_alias=True, exclude_none=True)
    assert data["options"] == [{"label": "Red", "value": "red"}, {"label": "Blue", "value": "blue"}]
    assert data["value"] == ["red"]


def test_slider():
    s = Slider(id="vol", max=100, value=50)
    data = s.model_dump(by_alias=True, exclude_none=True)
    assert data["min"] == 0
    assert data["max"] == 100
    assert data["value"] == 50


def test_date_time_input():
    dt = DateTimeInput(id="date", value="2026-03-17", enable_date=True)
    data = dt.model_dump(by_alias=True, exclude_none=True)
    assert data["enableDate"] is True
    assert data["enableTime"] is False


def test_text_field_invalid_variant():
    with pytest.raises(ValidationError):
        TextField(id="x", label="X", variant="invalid")
