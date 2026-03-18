import pytest

from py_a2ui.functions.logic import and_, not_, or_


def test_and():
    fc = and_(True, False)
    assert fc.call == "and"
    assert fc.args == {"values": [True, False]}


def test_and_rejects_fewer_than_two():
    with pytest.raises(ValueError, match="at least 2 conditions"):
        and_(True)
    with pytest.raises(ValueError, match="at least 2 conditions"):
        and_()


def test_or():
    fc = or_(True, False)
    assert fc.call == "or"
    assert fc.args == {"values": [True, False]}


def test_or_rejects_fewer_than_two():
    with pytest.raises(ValueError, match="at least 2 conditions"):
        or_(True)
    with pytest.raises(ValueError, match="at least 2 conditions"):
        or_()


def test_not():
    fc = not_(True)
    assert fc.call == "not"
    assert fc.args == {"value": True}
