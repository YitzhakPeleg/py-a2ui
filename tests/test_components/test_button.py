from py_a2ui import Button, ButtonVariant, EventAction


def test_button_with_event_action():
    btn = Button(
        id="submit",
        child="label",
        variant=ButtonVariant.PRIMARY,
        action=EventAction(event_name="submit"),
    )
    data = btn.model_dump(by_alias=True, exclude_none=True)
    assert data == {
        "id": "submit",
        "component": "Button",
        "child": "label",
        "variant": "primary",
        "action": {"eventName": "submit"},
    }


def test_button_default_variant():
    btn = Button(
        id="btn",
        child="label",
        action=EventAction(event_name="click"),
    )
    assert btn.variant == ButtonVariant.DEFAULT
