from src.agenda.idea import IdeaRoot, idearoot_shop
from src.agenda.road import get_default_culture_root_label as root_label
from pytest import raises as pytest_raises


def test_IdeaRoot_exists():
    # GIVEN / WHEN
    new_obj = IdeaRoot()

    # THEN
    assert new_obj
    assert new_obj._label is None
    assert new_obj._kids is None


def test_idearoot_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    new_obj = idearoot_shop()

    # THEN
    assert new_obj
    assert new_obj._label == root_label()
    assert new_obj._kids is None


def test_IdeaRoot_set_idea_label_get_default_culture_root_label_DoesNotRaisesError():
    # GIVEN
    new_obj = idearoot_shop()

    # WHEN

    new_obj.set_idea_label(_label=root_label())

    # THEN
    assert new_obj._label == root_label()


def test_IdeaRoot_set_idea_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    new_obj = idearoot_shop()
    culture_title = "El Paso"

    # WHEN
    new_obj.set_idea_label(_label=culture_title, agenda_culture_title=culture_title)

    # THEN
    assert new_obj._label == culture_title


def test_IdeaRoot_set_idea_label_InCorrectlyDoesRaisesError():
    # GIVEN
    new_obj = idearoot_shop()
    culture_title = "El Paso"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, agenda_culture_title=culture_title)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{culture_title}'"
    )


def test_IdeaRoot_set_idea_label_RaisesErrorWhen_agenda_culture_title_IsNone():
    # GIVEN
    new_obj = idearoot_shop()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, agenda_culture_title=None)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )


def test_IdeaRoot_set_idea_label_agenda_culture_title_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    new_obj = idearoot_shop()

    # WHEN
    new_obj.set_idea_label(_label=root_label(), agenda_culture_title=root_label())

    # THEN
    assert new_obj._label == root_label()
