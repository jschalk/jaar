from pytest import raises as pytest_raises
from src.ch05_reason_logic.reason import factheir_shop, factunit_shop
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.example_beliefs import (
    get_beliefunit_1Chore_1CE0MinutesReason_1Fact,
)


def test_BeliefUnit_cashout_ChangesPlanUnit_task_chore():
    # ESTABLISH
    yao_belief = get_beliefunit_1Chore_1CE0MinutesReason_1Fact()
    hr_str = "hr"
    hr_rope = yao_belief.make_l1_rope(hr_str)

    # WHEN
    yao_belief.add_fact(
        fact_context=hr_rope, fact_state=hr_rope, fact_lower=82, fact_upper=85
    )

    # THEN
    mail_rope = yao_belief.make_l1_rope("obtain mail")
    plan_dict = yao_belief.get_plan_dict()
    mail_plan = plan_dict.get(mail_rope)
    yao_belief.add_fact(
        fact_context=hr_rope, fact_state=hr_rope, fact_lower=82, fact_upper=95
    )
    assert mail_plan.task is True
    assert mail_plan.chore is False

    # WHEN
    yao_belief.cashout()

    # THEN
    mail_plan = yao_belief.get_plan_obj(mail_rope)
    assert mail_plan.task
    assert mail_plan.chore


def test_BeliefUnit_cashout_ExecutesWithRangeRootFacts():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_belief.make_l1_rope(casa_str)
    zia_belief.set_l1_plan(planunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = zia_belief.make_rope(casa_rope, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_plan = planunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_gogo_want = -2
    sweep_stop_want = 1
    sweep_plan = planunit_shop(sweep_str, gogo_want=sweep_gogo_want)
    sweep_plan.stop_want = sweep_stop_want
    zia_belief.set_plan(clean_plan, parent_rope=casa_rope)
    zia_belief.add_fact(
        fact_context=clean_rope, fact_state=clean_rope, fact_lower=1, fact_upper=5
    )
    assert zia_belief.planroot.factheirs == {}

    # WHEN
    zia_belief.cashout()

    # THEN
    assert zia_belief.planroot.factheirs != {}
    clean_factheir = factheir_shop(clean_rope, clean_rope, 1.0, 5.0)
    assert zia_belief.planroot.factheirs == {
        clean_factheir.fact_context: clean_factheir
    }


def test_BeliefUnit_cashout_RaisesErrorIfNon_RangeRootHasFactUnit():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_belief.make_l1_rope(casa_str)
    zia_belief.set_l1_plan(planunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = zia_belief.make_rope(casa_rope, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_plan = planunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_rope = zia_belief.make_rope(clean_rope, sweep_str)
    sweep_plan = planunit_shop(sweep_str, addin=2)
    zia_belief.set_plan(clean_plan, parent_rope=casa_rope)
    zia_belief.set_plan(sweep_plan, parent_rope=clean_rope)
    zia_belief.add_fact(sweep_rope, sweep_rope, fact_lower=1, fact_upper=5)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        zia_belief.cashout()

    # THEN
    assert (
        str(excinfo.value)
        == f"Cannot have fact for range inheritor '{sweep_rope}'. A ranged fact plan must have _begin, _close"
    )


def test_BeliefUnit_cashout_FactHeirsInherited():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    swim_str = "swim"
    swim_rope = zia_belief.make_l1_rope(swim_str)
    zia_belief.set_l1_plan(planunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    fast_rope = zia_belief.make_rope(swim_rope, fast_str)
    slow_rope = zia_belief.make_rope(swim_rope, slow_str)
    zia_belief.set_plan(planunit_shop(fast_str), parent_rope=swim_rope)
    zia_belief.set_plan(planunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_belief.make_l1_rope(earth_str)
    zia_belief.set_l1_plan(planunit_shop(earth_str))

    swim_plan = zia_belief.get_plan_obj(swim_rope)
    fast_plan = zia_belief.get_plan_obj(fast_rope)
    slow_plan = zia_belief.get_plan_obj(slow_rope)
    zia_belief.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    assert swim_plan.factheirs == {}
    assert fast_plan.factheirs == {}
    assert slow_plan.factheirs == {}

    # WHEN
    zia_belief.cashout()

    # THEN
    assert swim_plan.factheirs != {}
    assert fast_plan.factheirs != {}
    assert slow_plan.factheirs != {}
    factheir_set_range = factheir_shop(earth_rope, earth_rope, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.fact_context: factheir_set_range}
    assert swim_plan.factheirs == factheirs_set_range
    assert fast_plan.factheirs == factheirs_set_range
    assert slow_plan.factheirs == factheirs_set_range
    print(f"{swim_plan.factheirs=}")
    assert len(swim_plan.factheirs) == 1

    # WHEN
    swim_earth_factheir = swim_plan.factheirs.get(earth_rope)
    swim_earth_factheir.set_range_null()

    # THEN
    fact_none_range = factheir_shop(earth_rope, earth_rope, None, None)
    facts_none_range = {fact_none_range.fact_context: fact_none_range}
    assert swim_plan.factheirs == facts_none_range
    assert fast_plan.factheirs == factheirs_set_range
    assert slow_plan.factheirs == factheirs_set_range

    fact_x1 = swim_plan.factheirs.get(earth_rope)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_BeliefUnit_cashout_FactUnitMoldsFactHeir():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    swim_str = "swim"
    swim_rope = zia_belief.make_l1_rope(swim_str)
    zia_belief.set_l1_plan(planunit_shop(swim_str))
    swim_plan = zia_belief.get_plan_obj(swim_rope)

    fast_str = "fast"
    slow_str = "slow"
    zia_belief.set_plan(planunit_shop(fast_str), parent_rope=swim_rope)
    zia_belief.set_plan(planunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_belief.make_l1_rope(earth_str)
    zia_belief.set_l1_plan(planunit_shop(earth_str))

    assert swim_plan.factheirs == {}

    # WHEN
    zia_belief.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    zia_belief.cashout()

    # THEN
    first_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=1.0, fact_upper=5.0
    )
    first_earthdict = {first_earthheir.fact_context: first_earthheir}
    assert swim_plan.factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(fact_context=earth_rope, fact_state=earth_rope, reason_lower=3.0, reason_upper=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    zia_belief.add_fact(
        fact_context=earth_rope, fact_state=earth_rope, fact_lower=3.0, fact_upper=5.0
    )
    zia_belief.cashout()

    # THEN
    after_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=3.0, fact_upper=5.0
    )
    after_earthdict = {after_earthheir.fact_context: after_earthheir}
    assert swim_plan.factheirs == after_earthdict


def test_BeliefUnit_cashout_FactHeirDeletesFactUnit():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    swim_str = "swim"
    swim_rope = sue_belief.make_l1_rope(swim_str)
    sue_belief.set_l1_plan(planunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    sue_belief.set_plan(planunit_shop(fast_str), parent_rope=swim_rope)
    sue_belief.set_plan(planunit_shop(slow_str), parent_rope=swim_rope)
    earth_str = "earth"
    earth_rope = sue_belief.make_l1_rope(earth_str)
    sue_belief.set_l1_plan(planunit_shop(earth_str))
    swim_plan = sue_belief.get_plan_obj(swim_rope)
    first_earthheir = factheir_shop(
        earth_rope, earth_rope, fact_lower=200.0, fact_upper=500.0
    )
    first_earthdict = {first_earthheir.fact_context: first_earthheir}
    sue_belief.add_fact(earth_rope, earth_rope, fact_lower=200.0, fact_upper=500.0)
    assert swim_plan.factheirs == {}

    # WHEN
    sue_belief.cashout()

    # THEN
    assert swim_plan.factheirs == first_earthdict

    # WHEN
    earth_curb = factunit_shop(earth_rope, earth_rope, fact_lower=3.0, fact_upper=4.0)
    swim_plan.set_factunit(factunit=earth_curb)
    sue_belief.cashout()

    # THEN
    assert swim_plan.factheirs == first_earthdict
    assert swim_plan.factunits == {}


def test_BeliefUnit_cashout_SetsChoreAsComplete():
    # ESTABLISH
    yao_belief = get_beliefunit_1Chore_1CE0MinutesReason_1Fact()
    mail_str = "obtain mail"
    assert yao_belief is not None
    assert len(yao_belief.planroot.kids[mail_str].reasonunits) == 1
    plan_dict = yao_belief.get_plan_dict()
    mail_plan = plan_dict.get(yao_belief.make_l1_rope(mail_str))
    hr_str = "hr"
    hr_rope = yao_belief.make_l1_rope(hr_str)
    yao_belief.add_fact(hr_rope, hr_rope, fact_lower=82, fact_upper=85)
    assert mail_plan.task
    assert mail_plan.chore

    # WHEN
    yao_belief.cashout()

    # THEN
    assert mail_plan.task
    assert not mail_plan.chore
