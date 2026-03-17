from py_a2ui import Divider, Modal, Tab, Tabs


def test_divider_defaults():
    d = Divider(id="d1")
    data = d.model_dump(by_alias=True, exclude_none=True)
    assert data["axis"] == "horizontal"


def test_divider_vertical():
    d = Divider(id="d1", axis="vertical")
    data = d.model_dump(by_alias=True, exclude_none=True)
    assert data["axis"] == "vertical"


def test_modal():
    m = Modal(id="m1", trigger="btn", content="panel")
    data = m.model_dump(by_alias=True, exclude_none=True)
    assert data == {
        "id": "m1",
        "component": "Modal",
        "trigger": "btn",
        "content": "panel",
    }


def test_tabs():
    t = Tabs(id="t1", tabs=[Tab(title="Tab 1", child="p1"), Tab(title="Tab 2", child="p2")])
    data = t.model_dump(by_alias=True, exclude_none=True)
    assert len(data["tabs"]) == 2
    assert data["tabs"][0] == {"title": "Tab 1", "child": "p1"}
