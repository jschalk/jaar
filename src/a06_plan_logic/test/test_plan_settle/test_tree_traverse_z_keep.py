from pytest import raises as pytest_raises
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic._util.example_plans import get_planunit_with_4_levels
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_settle_plan_CorrectlySets_keeps_justified_WhenPlanUnit_Empty():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    assert sue_plan._keeps_justified is False

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert sue_plan._keeps_justified


def test_PlanUnit_settle_plan_CorrectlySets_keeps_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    assert sue_plan._keeps_justified is False

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert sue_plan._keeps_justified


def test_PlanUnit_settle_plan_CorrectlySets_keeps_justified_WhenSingleConceptUnit_healerlink_any_group_title_exists_IsTrue():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan.set_l1_concept(
        conceptunit_shop("Texas", healerlink=healerlink_shop({"Yao"}))
    )
    assert sue_plan._keeps_justified is False

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert sue_plan._keeps_justified is False


def test_PlanUnit_settle_plan_CorrectlySets_keeps_justified_WhenSingleProblemAndKeep():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_str = "Yao"
    sue_plan.add_acctunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})
    sue_plan.set_l1_concept(
        conceptunit_shop("Texas", healerlink=yao_healerlink, problem_bool=True)
    )
    assert sue_plan._keeps_justified is False

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert sue_plan._keeps_justified


def test_PlanUnit_settle_plan_CorrectlySets_keeps_justified_WhenKeepIsLevelAboveProblem():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_str = "Yao"
    sue_plan.add_acctunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})

    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    sue_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
    ep_str = "El Paso"
    sue_plan.set_concept(
        conceptunit_shop(ep_str, healerlink=yao_healerlink), texas_rope
    )
    assert sue_plan._keeps_justified is False

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert sue_plan._keeps_justified


def test_PlanUnit_settle_plan_CorrectlySets_keeps_justified_WhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    sue_plan.set_l1_concept(conceptunit_shop(texas_str, healerlink=yao_healerlink))
    sue_plan.set_concept(conceptunit_shop("El Paso", problem_bool=True), texas_rope)
    assert sue_plan._keeps_justified is False

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert sue_plan._keeps_justified is False


def test_PlanUnit_settle_plan_CorrectlyRaisesErrorWhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    texas_concept = conceptunit_shop(texas_str, healerlink=yao_healerlink)
    sue_plan.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop("El Paso", problem_bool=True)
    sue_plan.set_concept(elpaso_concept, texas_rope)
    assert sue_plan._keeps_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.settle_plan(keep_exceptions=True)
    assert (
        str(excinfo.value)
        == f"ConceptUnit '{elpaso_concept.get_concept_rope()}' cannot sponsor ancestor keeps."
    )


def test_PlanUnit_settle_plan_CorrectlySets_keeps_justified_WhenTwoKeepsAre_OnTheEqualLine():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    texas_concept = conceptunit_shop(
        texas_str, healerlink=yao_healerlink, problem_bool=True
    )
    sue_plan.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop(
        "El Paso", healerlink=yao_healerlink, problem_bool=True
    )
    sue_plan.set_concept(elpaso_concept, texas_rope)
    assert sue_plan._keeps_justified is False

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert sue_plan._keeps_justified is False


def test_PlanUnit_get_concept_dict_RaisesErrorWhen_keeps_justified_IsFalse():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_plan.make_l1_rope(texas_str)
    texas_concept = conceptunit_shop(
        texas_str, healerlink=yao_healerlink, problem_bool=True
    )
    sue_plan.set_l1_concept(texas_concept)
    elpaso_concept = conceptunit_shop(
        "El Paso", healerlink=yao_healerlink, problem_bool=True
    )
    sue_plan.set_concept(elpaso_concept, texas_rope)
    sue_plan.settle_plan()
    assert sue_plan._keeps_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_concept_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because _keeps_justified={sue_plan._keeps_justified}."
    )
