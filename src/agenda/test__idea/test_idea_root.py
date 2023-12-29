from src.agenda.idea import idea_kid_shop
from src.agenda.road import get_default_economy_root_label as root_label
from pytest import raises as pytest_raises


def test_idea_kid_shop_With_is_root_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_idearoot = idea_kid_shop(_is_root=True)

    # THEN
    assert x_idearoot
    assert x_idearoot._is_root
    assert x_idearoot._label == root_label()
    assert x_idearoot._kids == {}
    assert x_idearoot._is_root == True


def test_IdeaUnit_set_idea_label_get_default_economy_root_label_DoesNotRaisesError():
    # GIVEN
    x_idearoot = idea_kid_shop(_is_root=True)

    # WHEN

    x_idearoot.set_idea_label(_label=root_label())

    # THEN
    assert x_idearoot._label == root_label()


def test_IdeaUnit_set_idea_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    el_paso_text = "El Paso"
    x_idearoot = idea_kid_shop(_is_root=True, _agenda_economy_id=el_paso_text)

    # WHEN
    x_idearoot.set_idea_label(_label=el_paso_text)

    # THEN
    assert x_idearoot._label == el_paso_text


def test_IdeaUnit_set_idea_label_DoesRaisesError():
    # GIVEN
    el_paso_text = "El Paso"
    x_idearoot = idea_kid_shop(_is_root=True, _agenda_economy_id=el_paso_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_idearoot.set_idea_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{el_paso_text}'"
    )


def test_IdeaUnit_set_idea_label_RaisesErrorWhen_agenda_economy_id_IsNone():
    # GIVEN
    x_idearoot = idea_kid_shop(_is_root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_idearoot.set_idea_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )


def test_IdeaUnit_set_idea_label_agenda_economy_id_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    x_idearoot = idea_kid_shop(_is_root=True, _agenda_economy_id=root_label())

    # WHEN
    x_idearoot.set_idea_label(_label=root_label())

    # THEN
    assert x_idearoot._label == root_label()
