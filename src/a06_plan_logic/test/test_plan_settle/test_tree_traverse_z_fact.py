from pytest import raises as pytest_raises
from src.a04_reason_logic.reason_concept import factheir_shop, factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.example_plans import (
    get_planunit_1Chore_1CE0MinutesReason_1Fact,
)


def test_PlanUnit_settle_plan_ChangesConceptUnit_task_chore():
    # ESTABLISH
    yao_plan = get_planunit_1Chore_1CE0MinutesReason_1Fact()
    hr_str = "hr"
    hr_rope = yao_plan.make_l1_rope(hr_str)

    # WHEN
    yao_plan.add_fact(fcontext=hr_rope, fstate=hr_rope, fopen=82, fnigh=85)

    # THEN
    mail_rope = yao_plan.make_l1_rope("obtain mail")
    concept_dict = yao_plan.get_concept_dict()
    mail_concept = concept_dict.get(mail_rope)
    yao_plan.add_fact(fcontext=hr_rope, fstate=hr_rope, fopen=82, fnigh=95)
    assert mail_concept.task is True
    assert mail_concept._chore is False

    # WHEN
    yao_plan.settle_plan()

    # THEN
    mail_concept = yao_plan.get_concept_obj(mail_rope)
    assert mail_concept.task
    assert mail_concept._chore


def test_PlanUnit_settle_plan_ExecutesWithRangeRootFacts():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_plan.make_l1_rope(casa_str)
    zia_plan.set_l1_concept(conceptunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = zia_plan.make_rope(casa_rope, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_concept = conceptunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_gogo_want = -2
    sweep_stop_want = 1
    sweep_concept = conceptunit_shop(sweep_str, gogo_want=sweep_gogo_want)
    sweep_concept.stop_want = sweep_stop_want
    zia_plan.set_concept(clean_concept, parent_rope=casa_rope)
    zia_plan.add_fact(fcontext=clean_rope, fstate=clean_rope, fopen=1, fnigh=5)
    assert zia_plan.conceptroot._factheirs == {}

    # WHEN
    zia_plan.settle_plan()

    # THEN
    assert zia_plan.conceptroot._factheirs != {}
    clean_factheir = factheir_shop(clean_rope, clean_rope, 1.0, 5.0)
    assert zia_plan.conceptroot._factheirs == {clean_factheir.fcontext: clean_factheir}


def test_PlanUnit_settle_plan_RaisesErrorIfNonRangeRootHasFactUnit():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_plan.make_l1_rope(casa_str)
    zia_plan.set_l1_concept(conceptunit_shop(casa_str))
    clean_str = "clean"
    clean_rope = zia_plan.make_rope(casa_rope, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_concept = conceptunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_rope = zia_plan.make_rope(clean_rope, sweep_str)
    sweep_concept = conceptunit_shop(sweep_str, addin=2)
    zia_plan.set_concept(clean_concept, parent_rope=casa_rope)
    zia_plan.set_concept(sweep_concept, parent_rope=clean_rope)
    zia_plan.add_fact(sweep_rope, sweep_rope, fopen=1, fnigh=5)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.settle_plan()
    assert (
        str(excinfo.value)
        == f"Cannot have fact for range inheritor '{sweep_rope}'. A ranged fact concept must have _begin, _close"
    )


def test_PlanUnit_settle_plan_FactHeirsCorrectlyInherited():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    swim_str = "swim"
    swim_rope = zia_plan.make_l1_rope(swim_str)
    zia_plan.set_l1_concept(conceptunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    fast_rope = zia_plan.make_rope(swim_rope, fast_str)
    slow_rope = zia_plan.make_rope(swim_rope, slow_str)
    zia_plan.set_concept(conceptunit_shop(fast_str), parent_rope=swim_rope)
    zia_plan.set_concept(conceptunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_plan.make_l1_rope(earth_str)
    zia_plan.set_l1_concept(conceptunit_shop(earth_str))

    swim_concept = zia_plan.get_concept_obj(swim_rope)
    fast_concept = zia_plan.get_concept_obj(fast_rope)
    slow_concept = zia_plan.get_concept_obj(slow_rope)
    zia_plan.add_fact(fcontext=earth_rope, fstate=earth_rope, fopen=1.0, fnigh=5.0)
    assert swim_concept._factheirs == {}
    assert fast_concept._factheirs == {}
    assert slow_concept._factheirs == {}

    # WHEN
    zia_plan.settle_plan()

    # THEN
    assert swim_concept._factheirs != {}
    assert fast_concept._factheirs != {}
    assert slow_concept._factheirs != {}
    factheir_set_range = factheir_shop(earth_rope, earth_rope, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.fcontext: factheir_set_range}
    assert swim_concept._factheirs == factheirs_set_range
    assert fast_concept._factheirs == factheirs_set_range
    assert slow_concept._factheirs == factheirs_set_range
    print(f"{swim_concept._factheirs=}")
    assert len(swim_concept._factheirs) == 1

    # WHEN
    swim_earth_factheir = swim_concept._factheirs.get(earth_rope)
    swim_earth_factheir.set_range_null()

    # THEN
    fact_none_range = factheir_shop(earth_rope, earth_rope, None, None)
    facts_none_range = {fact_none_range.fcontext: fact_none_range}
    assert swim_concept._factheirs == facts_none_range
    assert fast_concept._factheirs == factheirs_set_range
    assert slow_concept._factheirs == factheirs_set_range

    fact_x1 = swim_concept._factheirs.get(earth_rope)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_PlanUnit_settle_plan_FactUnitMoldsFactHeir():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    swim_str = "swim"
    swim_rope = zia_plan.make_l1_rope(swim_str)
    zia_plan.set_l1_concept(conceptunit_shop(swim_str))
    swim_concept = zia_plan.get_concept_obj(swim_rope)

    fast_str = "fast"
    slow_str = "slow"
    zia_plan.set_concept(conceptunit_shop(fast_str), parent_rope=swim_rope)
    zia_plan.set_concept(conceptunit_shop(slow_str), parent_rope=swim_rope)

    earth_str = "earth"
    earth_rope = zia_plan.make_l1_rope(earth_str)
    zia_plan.set_l1_concept(conceptunit_shop(earth_str))

    assert swim_concept._factheirs == {}

    # WHEN
    zia_plan.add_fact(fcontext=earth_rope, fstate=earth_rope, fopen=1.0, fnigh=5.0)
    zia_plan.settle_plan()

    # THEN
    first_earthheir = factheir_shop(earth_rope, earth_rope, fopen=1.0, fnigh=5.0)
    first_earthdict = {first_earthheir.fcontext: first_earthheir}
    assert swim_concept._factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(fcontext=earth_rope, fstate=earth_rope, popen=3.0, pnigh=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    zia_plan.add_fact(fcontext=earth_rope, fstate=earth_rope, fopen=3.0, fnigh=5.0)
    zia_plan.settle_plan()

    # THEN
    after_earthheir = factheir_shop(earth_rope, earth_rope, fopen=3.0, fnigh=5.0)
    after_earthdict = {after_earthheir.fcontext: after_earthheir}
    assert swim_concept._factheirs == after_earthdict


def test_PlanUnit_settle_plan_FactHeirCorrectlyDeletesFactUnit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    swim_str = "swim"
    swim_rope = sue_plan.make_l1_rope(swim_str)
    sue_plan.set_l1_concept(conceptunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    sue_plan.set_concept(conceptunit_shop(fast_str), parent_rope=swim_rope)
    sue_plan.set_concept(conceptunit_shop(slow_str), parent_rope=swim_rope)
    earth_str = "earth"
    earth_rope = sue_plan.make_l1_rope(earth_str)
    sue_plan.set_l1_concept(conceptunit_shop(earth_str))
    swim_concept = sue_plan.get_concept_obj(swim_rope)
    first_earthheir = factheir_shop(earth_rope, earth_rope, fopen=200.0, fnigh=500.0)
    first_earthdict = {first_earthheir.fcontext: first_earthheir}
    sue_plan.add_fact(earth_rope, earth_rope, fopen=200.0, fnigh=500.0)
    assert swim_concept._factheirs == {}

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert swim_concept._factheirs == first_earthdict

    # WHEN
    earth_curb = factunit_shop(earth_rope, earth_rope, fopen=3.0, fnigh=4.0)
    swim_concept.set_factunit(factunit=earth_curb)
    sue_plan.settle_plan()

    # THEN
    assert swim_concept._factheirs == first_earthdict
    assert swim_concept.factunits == {}


def test_PlanUnit_settle_plan_SetsChoreAsComplete():
    # ESTABLISH
    yao_plan = get_planunit_1Chore_1CE0MinutesReason_1Fact()
    mail_str = "obtain mail"
    assert yao_plan is not None
    assert len(yao_plan.conceptroot._kids[mail_str].reasonunits) == 1
    concept_dict = yao_plan.get_concept_dict()
    mail_concept = concept_dict.get(yao_plan.make_l1_rope(mail_str))
    hr_str = "hr"
    hr_rope = yao_plan.make_l1_rope(hr_str)
    yao_plan.add_fact(hr_rope, hr_rope, fopen=82, fnigh=85)
    assert mail_concept.task
    assert mail_concept._chore

    # WHEN
    yao_plan.settle_plan()

    # THEN
    assert mail_concept.task
    assert not mail_concept._chore
