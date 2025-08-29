from pytest import raises as pytest_raises
from src.a05_plan_logic.healer import healerunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.example_beliefs import get_beliefunit_with_4_levels


def test_BeliefUnit_cash_out_Sets_keeps_justified_WhenBeliefUnit_Empty():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    assert sue_belief.keeps_justified is False

    # WHEN
    sue_belief.cash_out()

    # THEN
    assert sue_belief.keeps_justified


def test_BeliefUnit_cash_out_Sets_keeps_justified_WhenThereAreNotAny():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    assert sue_belief.keeps_justified is False

    # WHEN
    sue_belief.cash_out()

    # THEN
    assert sue_belief.keeps_justified


def test_BeliefUnit_cash_out_Sets_keeps_justified_WhenSinglePlanUnit_healerunit_any_group_title_exists_IsTrue():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief.set_l1_plan(planunit_shop("Texas", healerunit=healerunit_shop({"Yao"})))
    assert sue_belief.keeps_justified is False

    # WHEN
    sue_belief.cash_out()

    # THEN
    assert sue_belief.keeps_justified is False


def test_BeliefUnit_cash_out_Sets_keeps_justified_WhenSingleProblemAndKeep():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_str = "Yao"
    sue_belief.add_voiceunit(yao_str)
    yao_healerunit = healerunit_shop({yao_str})
    sue_belief.set_l1_plan(
        planunit_shop("Texas", healerunit=yao_healerunit, problem_bool=True)
    )
    assert sue_belief.keeps_justified is False

    # WHEN
    sue_belief.cash_out()

    # THEN
    assert sue_belief.keeps_justified


def test_BeliefUnit_cash_out_Sets_keeps_justified_WhenKeepIsLevelAboveProblem():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_str = "Yao"
    sue_belief.add_voiceunit(yao_str)
    yao_healerunit = healerunit_shop({yao_str})

    texas_str = "Texas"
    texas_rope = sue_belief.make_l1_rope(texas_str)
    sue_belief.set_l1_plan(planunit_shop(texas_str, problem_bool=True))
    ep_str = "El Paso"
    sue_belief.set_plan(planunit_shop(ep_str, healerunit=yao_healerunit), texas_rope)
    assert sue_belief.keeps_justified is False

    # WHEN
    sue_belief.cash_out()

    # THEN
    assert sue_belief.keeps_justified


def test_BeliefUnit_cash_out_Sets_keeps_justified_WhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_belief.make_l1_rope(texas_str)
    yao_healerunit = healerunit_shop({"Yao"})
    sue_belief.set_l1_plan(planunit_shop(texas_str, healerunit=yao_healerunit))
    sue_belief.set_plan(planunit_shop("El Paso", problem_bool=True), texas_rope)
    assert sue_belief.keeps_justified is False

    # WHEN
    sue_belief.cash_out()

    # THEN
    assert sue_belief.keeps_justified is False


def test_BeliefUnit_cash_out_RaisesErrorWhenKeepIsLevelBelowProblem():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    texas_str = "Texas"
    texas_rope = sue_belief.make_l1_rope(texas_str)
    yao_healerunit = healerunit_shop({"Yao"})
    texas_plan = planunit_shop(texas_str, healerunit=yao_healerunit)
    sue_belief.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", problem_bool=True)
    sue_belief.set_plan(elpaso_plan, texas_rope)
    assert sue_belief.keeps_justified is False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_belief.cash_out(keep_exceptions=True)

    # THEN
    assert (
        str(excinfo.value)
        == f"PlanUnit '{elpaso_plan.get_plan_rope()}' cannot sponsor ancestor keeps."
    )


def test_BeliefUnit_cash_out_Sets_keeps_justified_WhenTwoKeepsAre_OnTheEqualLine():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_healerunit = healerunit_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_belief.make_l1_rope(texas_str)
    texas_plan = planunit_shop(texas_str, healerunit=yao_healerunit, problem_bool=True)
    sue_belief.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", healerunit=yao_healerunit, problem_bool=True)
    sue_belief.set_plan(elpaso_plan, texas_rope)
    assert sue_belief.keeps_justified is False

    # WHEN
    sue_belief.cash_out()

    # THEN
    assert sue_belief.keeps_justified is False


def test_BeliefUnit_get_plan_dict_RaisesErrorWhen_keeps_justified_IsFalse():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_healerunit = healerunit_shop({"Yao"})
    texas_str = "Texas"
    texas_rope = sue_belief.make_l1_rope(texas_str)
    texas_plan = planunit_shop(texas_str, healerunit=yao_healerunit, problem_bool=True)
    sue_belief.set_l1_plan(texas_plan)
    elpaso_plan = planunit_shop("El Paso", healerunit=yao_healerunit, problem_bool=True)
    sue_belief.set_plan(elpaso_plan, texas_rope)
    sue_belief.cash_out()
    assert sue_belief.keeps_justified is False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_belief.get_plan_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because keeps_justified={sue_belief.keeps_justified}."
    )
