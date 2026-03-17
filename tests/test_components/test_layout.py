from py_a2ui import Align, Column, Justify, List, Row


def test_row_defaults():
    r = Row(id="r1", children=["a", "b"])
    data = r.model_dump(by_alias=True, exclude_none=True)
    assert data == {
        "id": "r1",
        "component": "Row",
        "children": ["a", "b"],
        "justify": "start",
        "align": "stretch",
    }


def test_column_center():
    c = Column(id="c1", children=["x"], justify=Justify.CENTER, align=Align.CENTER)
    data = c.model_dump(by_alias=True, exclude_none=True)
    assert data["justify"] == "center"
    assert data["align"] == "center"


def test_list_horizontal():
    lst = List(id="l1", children=["a"], direction="horizontal")
    data = lst.model_dump(by_alias=True, exclude_none=True)
    assert data["direction"] == "horizontal"
