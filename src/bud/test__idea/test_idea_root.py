from src.bud.idea import ideaunit_shop
from src._road.road import get_default_real_id_roadnode as root_label
from pytest import raises as pytest_raises


def test_ideaunit_shop_With_root_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    x_idearoot = ideaunit_shop(_root=True)

    # THEN
    assert x_idearoot
    assert x_idearoot._root
    assert x_idearoot._label == root_label()
    assert x_idearoot._kids == {}
    assert x_idearoot._root == True


def test_IdeaUnit_set_label_get_default_real_id_roadnode_DoesNotRaisesError():
    # ESTABLISH
    x_idearoot = ideaunit_shop(_root=True)

    # WHEN

    x_idearoot.set_label(_label=root_label())

    # THEN
    assert x_idearoot._label == root_label()


def test_IdeaUnit_set_label_CorrectlyDoesNotRaisesError():
    # ESTABLISH
    el_paso_text = "El Paso"
    x_idearoot = ideaunit_shop(_root=True, _bud_real_id=el_paso_text)

    # WHEN
    x_idearoot.set_label(_label=el_paso_text)

    # THEN
    assert x_idearoot._label == el_paso_text


def test_IdeaUnit_set_label_DoesRaisesError():
    # ESTABLISH
    el_paso_text = "El Paso"
    x_idearoot = ideaunit_shop(_root=True, _bud_real_id=el_paso_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_idearoot.set_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{el_paso_text}'"
    )


def test_IdeaUnit_set_label_RaisesErrorWhen_bud_real_id_IsNone():
    # ESTABLISH
    x_idearoot = ideaunit_shop(_root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_idearoot.set_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{root_label()}'"
    )


def test_IdeaUnit_set_label_bud_real_id_EqualRootLabelDoesNotRaisesError():
    # ESTABLISH
    x_idearoot = ideaunit_shop(_root=True, _bud_real_id=root_label())

    # WHEN
    x_idearoot.set_label(_label=root_label())

    # THEN
    assert x_idearoot._label == root_label()
