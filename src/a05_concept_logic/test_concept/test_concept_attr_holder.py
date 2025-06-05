from src.a05_concept_logic.concept import ConceptAttrHolder, conceptattrholder_shop
from src.a05_concept_logic.healer import healerlink_shop


def test_ConceptAttrHolder_Exists():
    new_obj = ConceptAttrHolder()
    assert new_obj.mass is None
    assert new_obj.uid is None
    assert new_obj.reason is None
    assert new_obj.reason_rcontext is None
    assert new_obj.reason_premise is None
    assert new_obj.popen is None
    assert new_obj.reason_pnigh is None
    assert new_obj.pdivisor is None
    assert new_obj.reason_del_premise_rcontext is None
    assert new_obj.reason_del_premise_pstate is None
    assert new_obj.reason_rconcept_active_requisite is None
    assert new_obj.laborunit is None
    assert new_obj.healerlink is None
    assert new_obj.begin is None
    assert new_obj.close is None
    assert new_obj.addin is None
    assert new_obj.numor is None
    assert new_obj.denom is None
    assert new_obj.morph is None
    assert new_obj.task is None
    assert new_obj.factunit is None
    assert new_obj.descendant_task_count is None
    assert new_obj.all_acct_cred is None
    assert new_obj.all_acct_debt is None
    assert new_obj.awardlink is None
    assert new_obj.awardlink_del is None
    assert new_obj.is_expanded is None


def test_ConceptAttrHolder_CorrectlyCalculatesPremiseRanges():
    # ESTABLISH
    concept_attr = ConceptAttrHolder(reason_premise="some_way")
    assert concept_attr.popen is None
    assert concept_attr.reason_pnigh is None
    # assert concept_attr.reason_premise_numor is None
    assert concept_attr.pdivisor is None
    # assert concept_attr.reason_premise_morph is None

    # WHEN
    concept_attr.set_premise_range_influenced_by_premise_concept(
        popen=5.0,
        pnigh=20.0,
        # premise_numor,
        premise_denom=4.0,
        # premise_morph,
    )
    assert concept_attr.popen == 5.0
    assert concept_attr.reason_pnigh == 20.0
    # assert concept_attr.reason_premise_numor is None
    assert concept_attr.pdivisor == 4.0
    # assert concept_attr.reason_premise_morph is None


def test_conceptattrholder_shop_ReturnsObj():
    # ESTABLISH
    sue_healerlink = healerlink_shop({"Sue", "Yim"})

    # WHEN
    x_conceptattrholder = conceptattrholder_shop(healerlink=sue_healerlink)

    # THEN
    assert x_conceptattrholder.healerlink == sue_healerlink
