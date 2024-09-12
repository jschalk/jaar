from src.bud.idea import ideaunit_shop
from src._road.road import get_default_pecun_id_roadnode as root_label
from pytest import raises as pytest_raises


def test_ideaunit_shop_With_root_TrueReturnsObj():
    # ESTABLISH / WHEN
    x_idearoot = ideaunit_shop(_root=True)

    # THEN
    assert x_idearoot
    assert x_idearoot._root
    assert x_idearoot._label == root_label()
    assert x_idearoot._kids == {}
    assert x_idearoot._root is True


def test_IdeaUnit_set_label_get_default_pecun_id_roadnode_DoesNotRaisesError():
    # ESTABLISH
    x_idearoot = ideaunit_shop(_root=True)

    # WHEN
    x_idearoot.set_label(_label=root_label())

    # THEN
    assert x_idearoot._label == root_label()


def test_IdeaUnit_set_label_DoesNotRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_idearoot = ideaunit_shop(_root=True, _bud_pecun_id=el_paso_str)

    # WHEN
    x_idearoot.set_label(_label=el_paso_str)

    # THEN
    assert x_idearoot._label == el_paso_str


def test_IdeaUnit_set_label_DoesRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_idearoot = ideaunit_shop(_root=True, _bud_pecun_id=el_paso_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_idearoot.set_label(_label=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{el_paso_str}'"
    )


def test_IdeaUnit_set_label_RaisesErrorWhen_bud_pecun_id_IsNone():
    # ESTABLISH
    x_idearoot = ideaunit_shop(_root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_idearoot.set_label(_label=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{root_label()}'"
    )
