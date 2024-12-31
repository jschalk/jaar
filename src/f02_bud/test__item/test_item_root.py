from src.f02_bud.item import itemunit_shop
from src.f01_road.road import get_default_gov_idea as root_idea
from pytest import raises as pytest_raises


def test_itemunit_shop_With_root_TrueReturnsObj():
    # ESTABLISH / WHEN
    x_itemroot = itemunit_shop(_root=True)

    # THEN
    assert x_itemroot
    assert x_itemroot._root
    assert x_itemroot._idee == root_idea()
    assert x_itemroot._kids == {}
    assert x_itemroot._root is True


def test_ItemUnit_set_idee_get_default_gov_idea_DoesNotRaisesError():
    # ESTABLISH
    x_itemroot = itemunit_shop(_root=True)

    # WHEN
    x_itemroot.set_idee(_idee=root_idea())

    # THEN
    assert x_itemroot._idee == root_idea()


def test_ItemUnit_set_idee_DoesNotRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_itemroot = itemunit_shop(_root=True, _bud_gov_idea=el_paso_str)

    # WHEN
    x_itemroot.set_idee(_idee=el_paso_str)

    # THEN
    assert x_itemroot._idee == el_paso_str


def test_ItemUnit_set_idee_DoesRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_itemroot = itemunit_shop(_root=True, _bud_gov_idea=el_paso_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_itemroot.set_idee(_idee=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set itemroot to string different than '{el_paso_str}'"
    )


def test_ItemUnit_set_idee_RaisesErrorWhen_bud_gov_idea_IsNone():
    # ESTABLISH
    x_itemroot = itemunit_shop(_root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_itemroot.set_idee(_idee=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set itemroot to string different than '{root_idea()}'"
    )
