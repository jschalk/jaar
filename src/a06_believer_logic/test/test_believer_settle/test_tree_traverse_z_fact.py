from pytest import raises as pytest_raises
from src.a04_reason_logic.reason_plan import factheir_shop, factunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_1Chore_1CE0MinutesReason_1Fact,
)


def test_BelieverUnit_settle_believer_ChangesPlanUnit_task_chore():
    # ESTABLISH
    yao_believer = get_believerunit_1Chore_1CE0MinutesReason_1Fact()
    hr_str = "hr"
    hr_rope = yao_believer.make_l1_rope(hr_str)

    # WHEN
    yao_believer.add_fact(fcontext=hr_rope, fstate=hr_rope, fopen=82, fnigh=85)

    # THEN
    mail_rope = yao_believer.make_l1_rope("obtain mail")
    plan_dict = yao_believer.get_plan_dict()
    mail_plan = plan_dict.get(mail_rope)
    yao_believer.add_fact(fcontext=hr_rope, fstate=hr_rope, fopen=82, fnigh=95)
    assert mail_plan.task is True
    assert mail_plan._chore is False

    # WHEN
    yao_believer.settle_believer()

    # THEN
    mail_plan = yao_believer.get_plan_obj(mail_rope)
    assert mail_plan.task
    assert mail_plan._chore


def test_BelieverUnit_settle_believer_ExecutesWithRangeRootFacts():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_believer.make_l1_rope(casa_str)
    zia_believer.set_l1_plan(planunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = zia_believer.make_rope(casa_rope, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_plan = planunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_gogo_want = -2
    sweep_stop_want = 1
    sweep_plan = planunit_shop(sweep_str, gogo_want=sweep_gogo_want)
    sweep_plan.stop_want = sweep_stop_want
    zia_believer.set_plan(clean_plan, parent_rope=casa_rope)
    zia_believer.add_fact(fcontext=clean_rope, fstate=clean_rope, fopen=1, fnigh=5)
    assert zia_believer.planroot._factheirs == {}

    # WHEN
    zia_believer.settle_believer()

    # THEN
    assert zia_believer.planroot._factheirs != {}
    clean_factheir = factheir_shop(clean_rope, clean_rope, 1.0, 5.0)
    assert zia_believer.planroot._factheirs == {clean_factheir.fcontext: clean_factheir}


def test_BelieverUnit_settle_believer_RaisesErrorIfNon_RangeRootHasFactUnit():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_believer.make_l1_rope(casa_str)
    zia_believer.set_l1_plan(planunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = zia_believer.make_rope(casa_rope, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_plan = planunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_rope = zia_believer.make_rope(clean_rope, sweep_str)
    sweep_plan = planunit_shop(sweep_str, addin=2)
    zia_believer.set_plan(clean_plan, parent_rope=casa_rope)
    zia_believer.set_plan(sweep_plan, parent_rope=clean_rope)
    zia_believer.add_fact(sweep_rope, sweep_rope, fopen=1, fnigh=5)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        zia_believer.settle_believer()
    assert (
        str(excinfo.value)
        == f"Cannot have fact for range inheritor '{sweep_rope}'. A ranged fact plan must have _begin, _close"
    )


def test_BelieverUnit_settle_believer_FactHeirsCorrectlyInherited():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    swim_str = "swim"
    swim_rope = zia_believer.make_l1_rope(swim_str)
    zia_believer.set_l1_plan(planunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    fast_rope = zia_believer.make_rope(swim_rope, fast_str)
    slow_rope = zia_believer.make_rope(swim_rope, slow_str)
    zia_believer.set_plan(planunit_shop(fast_str), parent_rope=swim_rope)
    zia_believer.set_plan(planunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_believer.make_l1_rope(earth_str)
    zia_believer.set_l1_plan(planunit_shop(earth_str))

    swim_plan = zia_believer.get_plan_obj(swim_rope)
    fast_plan = zia_believer.get_plan_obj(fast_rope)
    slow_plan = zia_believer.get_plan_obj(slow_rope)
    zia_believer.add_fact(fcontext=earth_rope, fstate=earth_rope, fopen=1.0, fnigh=5.0)
    assert swim_plan._factheirs == {}
    assert fast_plan._factheirs == {}
    assert slow_plan._factheirs == {}

    # WHEN
    zia_believer.settle_believer()

    # THEN
    assert swim_plan._factheirs != {}
    assert fast_plan._factheirs != {}
    assert slow_plan._factheirs != {}
    factheir_set_range = factheir_shop(earth_rope, earth_rope, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.fcontext: factheir_set_range}
    assert swim_plan._factheirs == factheirs_set_range
    assert fast_plan._factheirs == factheirs_set_range
    assert slow_plan._factheirs == factheirs_set_range
    print(f"{swim_plan._factheirs=}")
    assert len(swim_plan._factheirs) == 1

    # WHEN
    swim_earth_factheir = swim_plan._factheirs.get(earth_rope)
    swim_earth_factheir.set_range_null()

    # THEN
    fact_none_range = factheir_shop(earth_rope, earth_rope, None, None)
    facts_none_range = {fact_none_range.fcontext: fact_none_range}
    assert swim_plan._factheirs == facts_none_range
    assert fast_plan._factheirs == factheirs_set_range
    assert slow_plan._factheirs == factheirs_set_range

    fact_x1 = swim_plan._factheirs.get(earth_rope)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_BelieverUnit_settle_believer_FactUnitMoldsFactHeir():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    swim_str = "swim"
    swim_rope = zia_believer.make_l1_rope(swim_str)
    zia_believer.set_l1_plan(planunit_shop(swim_str))
    swim_plan = zia_believer.get_plan_obj(swim_rope)

    fast_str = "fast"
    slow_str = "slow"
    zia_believer.set_plan(planunit_shop(fast_str), parent_rope=swim_rope)
    zia_believer.set_plan(planunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_believer.make_l1_rope(earth_str)
    zia_believer.set_l1_plan(planunit_shop(earth_str))

    assert swim_plan._factheirs == {}

    # WHEN
    zia_believer.add_fact(fcontext=earth_rope, fstate=earth_rope, fopen=1.0, fnigh=5.0)
    zia_believer.settle_believer()

    # THEN
    first_earthheir = factheir_shop(earth_rope, earth_rope, fopen=1.0, fnigh=5.0)
    first_earthdict = {first_earthheir.fcontext: first_earthheir}
    assert swim_plan._factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(fcontext=earth_rope, fstate=earth_rope, popen=3.0, pnigh=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    zia_believer.add_fact(fcontext=earth_rope, fstate=earth_rope, fopen=3.0, fnigh=5.0)
    zia_believer.settle_believer()

    # THEN
    after_earthheir = factheir_shop(earth_rope, earth_rope, fopen=3.0, fnigh=5.0)
    after_earthdict = {after_earthheir.fcontext: after_earthheir}
    assert swim_plan._factheirs == after_earthdict


def test_BelieverUnit_settle_believer_FactHeirCorrectlyDeletesFactUnit():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    swim_str = "swim"
    swim_rope = sue_believer.make_l1_rope(swim_str)
    sue_believer.set_l1_plan(planunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    sue_believer.set_plan(planunit_shop(fast_str), parent_rope=swim_rope)
    sue_believer.set_plan(planunit_shop(slow_str), parent_rope=swim_rope)
    earth_str = "earth"
    earth_rope = sue_believer.make_l1_rope(earth_str)
    sue_believer.set_l1_plan(planunit_shop(earth_str))
    swim_plan = sue_believer.get_plan_obj(swim_rope)
    first_earthheir = factheir_shop(earth_rope, earth_rope, fopen=200.0, fnigh=500.0)
    first_earthdict = {first_earthheir.fcontext: first_earthheir}
    sue_believer.add_fact(earth_rope, earth_rope, fopen=200.0, fnigh=500.0)
    assert swim_plan._factheirs == {}

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert swim_plan._factheirs == first_earthdict

    # WHEN
    earth_curb = factunit_shop(earth_rope, earth_rope, fopen=3.0, fnigh=4.0)
    swim_plan.set_factunit(factunit=earth_curb)
    sue_believer.settle_believer()

    # THEN
    assert swim_plan._factheirs == first_earthdict
    assert swim_plan.factunits == {}


def test_BelieverUnit_settle_believer_SetsChoreAsComplete():
    # ESTABLISH
    yao_believer = get_believerunit_1Chore_1CE0MinutesReason_1Fact()
    mail_str = "obtain mail"
    assert yao_believer is not None
    assert len(yao_believer.planroot._kids[mail_str].reasonunits) == 1
    plan_dict = yao_believer.get_plan_dict()
    mail_plan = plan_dict.get(yao_believer.make_l1_rope(mail_str))
    hr_str = "hr"
    hr_rope = yao_believer.make_l1_rope(hr_str)
    yao_believer.add_fact(hr_rope, hr_rope, fopen=82, fnigh=85)
    assert mail_plan.task
    assert mail_plan._chore

    # WHEN
    yao_believer.settle_believer()

    # THEN
    assert mail_plan.task
    assert not mail_plan._chore
