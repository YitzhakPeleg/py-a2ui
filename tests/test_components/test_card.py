from py_a2ui import Card


def test_card_serialization():
    c = Card(id="card1", child="content")
    data = c.model_dump(by_alias=True, exclude_none=True)
    assert data == {
        "id": "card1",
        "component": "Card",
        "child": "content",
    }
