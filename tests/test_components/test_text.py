from py_a2ui import Text, TextVariant


def test_text_defaults():
    t = Text(id="greeting", text="Hello")
    data = t.model_dump(by_alias=True, exclude_none=True)
    assert data == {
        "id": "greeting",
        "component": "Text",
        "text": "Hello",
        "variant": "body",
    }


def test_text_h1_variant():
    t = Text(id="title", text="Welcome", variant=TextVariant.H1)
    data = t.model_dump(by_alias=True, exclude_none=True)
    assert data["variant"] == "h1"


def test_text_variant_string():
    t = Text(id="title", text="Hi", variant="h2")
    assert t.variant == TextVariant.H2
