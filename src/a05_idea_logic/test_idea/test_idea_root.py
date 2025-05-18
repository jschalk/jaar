from src.a05_idea_logic.idea import ideaunit_shop
from src.a01_way_logic.way import get_default_fisc_label as root_label
from pytest import raises as pytest_raises


def test_ideaunit_shop_With_root_TrueReturnsObj():
    # ESTABLISH / WHEN
    x_idearoot = ideaunit_shop(root=True)

    # THEN
    assert x_idearoot
    assert x_idearoot.root
    assert x_idearoot.idea_label == root_label()
    assert x_idearoot._kids == {}
    assert x_idearoot.root is True


def test_IdeaUnit_set_idea_label_get_default_fisc_label_DoesNotRaisesError():
    # ESTABLISH
    x_idearoot = ideaunit_shop(root=True)

    # WHEN
    x_idearoot.set_idea_label(idea_label=root_label())

    # THEN
    assert x_idearoot.idea_label == root_label()


def test_IdeaUnit_set_idea_label_DoesNotRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_idearoot = ideaunit_shop(root=True, fisc_label=el_paso_str)

    # WHEN
    x_idearoot.set_idea_label(idea_label=el_paso_str)

    # THEN
    assert x_idearoot.idea_label == el_paso_str


def test_IdeaUnit_set_idea_label_DoesRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_idearoot = ideaunit_shop(root=True, fisc_label=el_paso_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_idearoot.set_idea_label(idea_label=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{el_paso_str}'"
    )


def test_IdeaUnit_set_idea_label_RaisesErrorWhenfisc_label_IsNone():
    # ESTABLISH
    x_idearoot = ideaunit_shop(root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_idearoot.set_idea_label(idea_label=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string different than '{root_label()}'"
    )
