from src.a05_item_logic.item import itemunit_shop
from src.a01_way_logic.way import get_default_fisc_tag as root_tag
from pytest import raises as pytest_raises


def test_itemunit_shop_With_root_TrueReturnsObj():
    # ESTABLISH / WHEN
    x_itemroot = itemunit_shop(root=True)

    # THEN
    assert x_itemroot
    assert x_itemroot.root
    assert x_itemroot.item_tag == root_tag()
    assert x_itemroot._kids == {}
    assert x_itemroot.root is True


def test_ItemUnit_set_item_tag_get_default_fisc_tag_DoesNotRaisesError():
    # ESTABLISH
    x_itemroot = itemunit_shop(root=True)

    # WHEN
    x_itemroot.set_item_tag(item_tag=root_tag())

    # THEN
    assert x_itemroot.item_tag == root_tag()


def test_ItemUnit_set_item_tag_DoesNotRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_itemroot = itemunit_shop(root=True, fisc_tag=el_paso_str)

    # WHEN
    x_itemroot.set_item_tag(item_tag=el_paso_str)

    # THEN
    assert x_itemroot.item_tag == el_paso_str


def test_ItemUnit_set_item_tag_DoesRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_itemroot = itemunit_shop(root=True, fisc_tag=el_paso_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_itemroot.set_item_tag(item_tag=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set itemroot to string different than '{el_paso_str}'"
    )


def test_ItemUnit_set_item_tag_RaisesErrorWhenfisc_tag_IsNone():
    # ESTABLISH
    x_itemroot = itemunit_shop(root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_itemroot.set_item_tag(item_tag=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set itemroot to string different than '{root_tag()}'"
    )
