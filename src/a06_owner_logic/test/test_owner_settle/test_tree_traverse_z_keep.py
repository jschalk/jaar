from pytest import raises as pytest_raises
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.example_owners import get_ownerunit_with_4_levels


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_justified_WhenOwnerUnit_Empty():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    assert sue_owner._keeps_justified is False

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner._keeps_justified


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()
    assert sue_owner._keeps_justified is False

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner._keeps_justified


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_justified_WhenSingleConceptUnit_healerlink_any_group_title_exists_IsTrue():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    sue_owner.set_l1_concept(
        conceptunit_shop("Texas", healerlink=healerlink_shop({"Yao"}))
    )
    assert sue_owner._keeps_justified is False

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner._keeps_justified is False


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_justified_WhenSingleProblemAndKeep():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    yao_str = "Yao"
    sue_owner.add_acctunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})
    sue_owner.set_l1_concept(
        conceptunit_shop("Texas", healerlink=yao_healerlink, problem_bool=True)
    )
    assert sue_owner._keeps_justified is False

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner._keeps_justified


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_justified_WhenKeepIsLevelAboveProblem():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    yao_str = "Yao"
    sue_owner.add_acctunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})

    texas_str = "Texas"
    texas_rope = sue_owner.make_l1_rope(texas_str)
    sue_owner.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    ep_str = "El Paso"
    sue_owner.set_concept(
        conceptunit_shop(ep_str, healerlink=yao_healerlink), texas_rope
    )
    assert sue_owner._keeps_justified is False

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner._keeps_justified


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_justified_WhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_owner.make_l1_rope(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    sue_owner.set_l1_concept(conceptunit_shop(texas_str, healerlink=yao_healerlink))
    sue_owner.set_concept(conceptunit_shop("El Paso", problem_bool=True), texas_rope)
    assert sue_owner._keeps_justified is False

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner._keeps_justified is False


def test_OwnerUnit_settle_owner_CorrectlyRaisesErrorWhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_owner.make_l1_rope(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    texas_concept = conceptunit_shop(texas_str, healerlink=yao_healerlink)
    sue_owner.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop("El Paso", problem_bool=True)
    sue_owner.set_concept(elpaso_concept, texas_rope)
    assert sue_owner._keeps_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_owner.settle_owner(keep_exceptions=True)
    assert (
        str(excinfo.value)
        == f"ConceptUnit '{elpaso_concept.get_concept_rope()}' cannot sponsor ancestor keeps."
    )


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_justified_WhenTwoKeepsAre_OnTheEqualLine():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_owner.make_l1_rope(texas_str)
    texas_concept = conceptunit_shop(
        texas_str, healerlink=yao_healerlink, problem_bool=True
    )
    sue_owner.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop(
        "El Paso", healerlink=yao_healerlink, problem_bool=True
    )
    sue_owner.set_concept(elpaso_concept, texas_rope)
    assert sue_owner._keeps_justified is False

    # WHEN
    sue_owner.settle_owner()

    # THEN
    assert sue_owner._keeps_justified is False


def test_OwnerUnit_get_concept_dict_RaisesErrorWhen_keeps_justified_IsFalse():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_owner.make_l1_rope(texas_str)
    texas_concept = conceptunit_shop(
        texas_str, healerlink=yao_healerlink, problem_bool=True
    )
    sue_owner.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop(
        "El Paso", healerlink=yao_healerlink, problem_bool=True
    )
    sue_owner.set_concept(elpaso_concept, texas_rope)
    sue_owner.settle_owner()
    assert sue_owner._keeps_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_owner.get_concept_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because _keeps_justified={sue_owner._keeps_justified}."
    )
