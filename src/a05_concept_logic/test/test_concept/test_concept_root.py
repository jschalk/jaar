from pytest import raises as pytest_raises
from src.a05_concept_logic.concept import (
    conceptunit_shop,
    get_default_belief_label as root_label,
)


def test_conceptunit_shop_With_root_TrueReturnsObj():
    # ESTABLISH / WHEN
    x_conceptroot = conceptunit_shop(root=True)

    # THEN
    assert x_conceptroot
    assert x_conceptroot.root
    assert x_conceptroot.concept_label == root_label()
    assert x_conceptroot._kids == {}
    assert x_conceptroot.root is True


def test_ConceptUnit_set_concept_label_get_default_belief_label_DoesNotRaisesError():
    # ESTABLISH
    x_conceptroot = conceptunit_shop(root=True)

    # WHEN
    x_conceptroot.set_concept_label(concept_label=root_label())

    # THEN
    assert x_conceptroot.concept_label == root_label()


def test_ConceptUnit_set_concept_label_DoesNotRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_conceptroot = conceptunit_shop(root=True, belief_label=el_paso_str)

    # WHEN
    x_conceptroot.set_concept_label(concept_label=el_paso_str)

    # THEN
    assert x_conceptroot.concept_label == el_paso_str


def test_ConceptUnit_set_concept_label_DoesRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_conceptroot = conceptunit_shop(root=True, belief_label=el_paso_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_conceptroot.set_concept_label(concept_label=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set conceptroot to string different than '{el_paso_str}'"
    )


def test_ConceptUnit_set_concept_label_RaisesErrorWhenbelief_label_IsNone():
    # ESTABLISH
    x_conceptroot = conceptunit_shop(root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_conceptroot.set_concept_label(concept_label=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set conceptroot to string different than '{root_label()}'"
    )
