from src.f02_bud.item import itemunit_shop
from src.f01_road.road import get_default_cmty_title as root_title
from pytest import raises as pytest_raises


def test_itemunit_shop_With_root_TrueReturnsObj():
    # ESTABLISH / WHEN
    x_itemroot = itemunit_shop(_root=True)

    # THEN
    assert x_itemroot
    assert x_itemroot._root
    assert x_itemroot._item_title == root_title()
    assert x_itemroot._kids == {}
    assert x_itemroot._root is True


def test_ItemUnit_set_item_title_get_default_cmty_title_DoesNotRaisesError():
    # ESTABLISH
    x_itemroot = itemunit_shop(_root=True)

    # WHEN
    x_itemroot.set_item_title(_item_title=root_title())

    # THEN
    assert x_itemroot._item_title == root_title()


def test_ItemUnit_set_item_title_DoesNotRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_itemroot = itemunit_shop(_root=True, _bud_cmty_title=el_paso_str)

    # WHEN
    x_itemroot.set_item_title(_item_title=el_paso_str)

    # THEN
    assert x_itemroot._item_title == el_paso_str


def test_ItemUnit_set_item_title_DoesRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_itemroot = itemunit_shop(_root=True, _bud_cmty_title=el_paso_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_itemroot.set_item_title(_item_title=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set itemroot to string different than '{el_paso_str}'"
    )


def test_ItemUnit_set_item_title_RaisesErrorWhen_bud_cmty_title_IsNone():
    # ESTABLISH
    x_itemroot = itemunit_shop(_root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_itemroot.set_item_title(_item_title=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set itemroot to string different than '{root_title()}'"
    )
