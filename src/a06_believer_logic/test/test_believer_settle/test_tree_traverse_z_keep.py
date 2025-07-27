from pytest import raises as pytest_raises
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_with_4_levels,
)


def test_BelieverUnit_settle_believer_CorrectlySets_keeps_justified_WhenBelieverUnit_Empty():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    assert sue_believer._keeps_justified is False

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert sue_believer._keeps_justified


def test_BelieverUnit_settle_believer_CorrectlySets_keeps_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    assert sue_believer._keeps_justified is False

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert sue_believer._keeps_justified


def test_BelieverUnit_settle_believer_CorrectlySets_keeps_justified_WhenSinglePlanUnit_healerlink_any_group_title_exists_IsTrue():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    sue_believer.set_l1_plan(
        planunit_shop("Texas", healerlink=healerlink_shop({"Yao"}))
    )
    assert sue_believer._keeps_justified is False

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert sue_believer._keeps_justified is False


def test_BelieverUnit_settle_believer_CorrectlySets_keeps_justified_WhenSingleProblemAndKeep():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_str = "Yao"
    sue_believer.add_partnerunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})
    sue_believer.set_l1_plan(
        planunit_shop("Texas", healerlink=yao_healerlink, problem_bool=True)
    )
    assert sue_believer._keeps_justified is False

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert sue_believer._keeps_justified


def test_BelieverUnit_settle_believer_CorrectlySets_keeps_justified_WhenKeepIsLevelAboveProblem():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_str = "Yao"
    sue_believer.add_partnerunit(yao_str)
    yao_healerlink = healerlink_shop({yao_str})

    texas_str = "Texas"
    texas_rope = sue_believer.make_l1_rope(texas_str)
    sue_believer.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    ep_str = "El Paso"
    sue_believer.set_plan(planunit_shop(ep_str, healerlink=yao_healerlink), texas_rope)
    assert sue_believer._keeps_justified is False

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert sue_believer._keeps_justified


def test_BelieverUnit_settle_believer_CorrectlySets_keeps_justified_WhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_believer.make_l1_rope(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    sue_believer.set_l1_plan(planunit_shop(texas_str, healerlink=yao_healerlink))
    sue_believer.set_plan(planunit_shop("El Paso", problem_bool=True), texas_rope)
    assert sue_believer._keeps_justified is False

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert sue_believer._keeps_justified is False


def test_BelieverUnit_settle_believer_CorrectlyRaisesErrorWhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_believer.make_l1_rope(texas_str)
    yao_healerlink = healerlink_shop({"Yao"})
    texas_plan = planunit_shop(texas_str, healerlink=yao_healerlink)
    sue_believer.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", problem_bool=True)
    sue_believer.set_plan(elpaso_plan, texas_rope)
    assert sue_believer._keeps_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_believer.settle_believer(keep_exceptions=True)
    assert (
        str(excinfo.value)
        == f"PlanUnit '{elpaso_plan.get_plan_rope()}' cannot sponsor ancestor keeps."
    )


def test_BelieverUnit_settle_believer_CorrectlySets_keeps_justified_WhenTwoKeepsAre_OnTheEqualLine():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_believer.make_l1_rope(texas_str)
    texas_plan = planunit_shop(texas_str, healerlink=yao_healerlink, problem_bool=True)
    sue_believer.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", healerlink=yao_healerlink, problem_bool=True)
    sue_believer.set_plan(elpaso_plan, texas_rope)
    assert sue_believer._keeps_justified is False

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert sue_believer._keeps_justified is False


def test_BelieverUnit_get_plan_dict_RaisesErrorWhen_keeps_justified_IsFalse():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_healerlink = healerlink_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_believer.make_l1_rope(texas_str)
    texas_plan = planunit_shop(texas_str, healerlink=yao_healerlink, problem_bool=True)
    sue_believer.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", healerlink=yao_healerlink, problem_bool=True)
    sue_believer.set_plan(elpaso_plan, texas_rope)
    sue_believer.settle_believer()
    assert sue_believer._keeps_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_believer.get_plan_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because _keeps_justified={sue_believer._keeps_justified}."
    )
