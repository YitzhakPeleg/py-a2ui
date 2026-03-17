from py_a2ui.functions.logic import and_, not_, or_


def test_and():
    fc = and_(True, False)
    assert fc.call == "and"
    assert fc.args == {"values": [True, False]}


def test_or():
    fc = or_(True, False)
    assert fc.call == "or"
    assert fc.args == {"values": [True, False]}


def test_not():
    fc = not_(True)
    assert fc.call == "not"
    assert fc.args == {"value": True}
