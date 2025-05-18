from src.a05_concept_logic.healer import healerlink_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels
from pytest import raises as pytest_raises


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenBudUnit_Empty():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenSingleConceptUnit_healerlink_any_group_title_exists_IsTrue():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud.set_l1_concept(
        conceptunit_shop("Texas", healerlink=healerlink_shop({"Yao"}))
    )
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified is False


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenSingleProblemAndKeep():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})
    sue_bud.set_l1_concept(
        conceptunit_shop("Texas", healerlink=yao_healerlink, problem_bool=True)
    )
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenKeepIsLevelAboveProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})

    texas_str = "Texas"
    texas_way = sue_bud.make_l1_way(texas_str)
    sue_bud.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    ep_str = "El Paso"
    sue_bud.set_concept(conceptunit_shop(ep_str, healerlink=yao_healerlink), texas_way)
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_str = "Texas"
    texas_way = sue_bud.make_l1_way(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    sue_bud.set_l1_concept(conceptunit_shop(texas_str, healerlink=yao_healerlink))
    sue_bud.set_concept(conceptunit_shop("El Paso", problem_bool=True), texas_way)
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified is False


def test_BudUnit_settle_bud_CorrectlyRaisesErrorWhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    texas_str = "Texas"
    texas_way = sue_bud.make_l1_way(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    texas_concept = conceptunit_shop(texas_str, healerlink=yao_healerlink)
    sue_bud.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop("El Paso", problem_bool=True)
    sue_bud.set_concept(elpaso_concept, texas_way)
    assert sue_bud._keeps_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.settle_bud(keep_exceptions=True)
    assert (
        str(excinfo.value)
        == f"ConceptUnit '{elpaso_concept.get_concept_way()}' cannot sponsor ancestor keeps."
    )


def test_BudUnit_settle_bud_CorrectlySets_keeps_justified_WhenTwoKeepsAre_OnTheEqualLine():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_way = sue_bud.make_l1_way(texas_str)
    texas_concept = conceptunit_shop(
        texas_str, healerlink=yao_healerlink, problem_bool=True
    )
    sue_bud.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop(
        "El Paso", healerlink=yao_healerlink, problem_bool=True
    )
    sue_bud.set_concept(elpaso_concept, texas_way)
    assert sue_bud._keeps_justified is False

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._keeps_justified is False


def test_BudUnit_get_concept_dict_RaisesErrorWhen_keeps_justified_IsFalse():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_way = sue_bud.make_l1_way(texas_str)
    texas_concept = conceptunit_shop(
        texas_str, healerlink=yao_healerlink, problem_bool=True
    )
    sue_bud.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop(
        "El Paso", healerlink=yao_healerlink, problem_bool=True
    )
    sue_bud.set_concept(elpaso_concept, texas_way)
    sue_bud.settle_bud()
    assert sue_bud._keeps_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_bud.get_concept_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because _keeps_justified={sue_bud._keeps_justified}."
    )
