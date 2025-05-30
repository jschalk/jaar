from src.a04_reason_logic.reason_concept import (
    factunit_shop,
    factunit_shop,
    factheir_shop,
)
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._test_util.example_buds import (
    get_budunit_1Task_1CE0MinutesReason_1Fact,
)
from pytest import raises as pytest_raises


def test_BudUnit_settle_bud_ChangesConceptUnit_pledge_task():
    # ESTABLISH
    yao_bud = get_budunit_1Task_1CE0MinutesReason_1Fact()
    hr_str = "hr"
    hr_way = yao_bud.make_l1_way(hr_str)

    # WHEN
    yao_bud.add_fact(fcontext=hr_way, fstate=hr_way, fopen=82, fnigh=85)

    # THEN
    mail_way = yao_bud.make_l1_way("obtain mail")
    concept_dict = yao_bud.get_concept_dict()
    mail_concept = concept_dict.get(mail_way)
    yao_bud.add_fact(fcontext=hr_way, fstate=hr_way, fopen=82, fnigh=95)
    assert mail_concept.pledge is True
    assert mail_concept._task is False

    # WHEN
    yao_bud.settle_bud()

    # THEN
    mail_concept = yao_bud.get_concept_obj(mail_way)
    assert mail_concept.pledge
    assert mail_concept._task


def test_BudUnit_settle_bud_ExecutesWithRangeRootFacts():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_way = zia_bud.make_l1_way(casa_str)
    zia_bud.set_l1_concept(conceptunit_shop(casa_str))
    clean_str = "clean"
    clean_way = zia_bud.make_way(casa_way, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_concept = conceptunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_gogo_want = -2
    sweep_stop_want = 1
    sweep_concept = conceptunit_shop(sweep_str, gogo_want=sweep_gogo_want)
    sweep_concept.stop_want = sweep_stop_want
    zia_bud.set_concept(clean_concept, parent_way=casa_way)
    zia_bud.add_fact(fcontext=clean_way, fstate=clean_way, fopen=1, fnigh=5)
    assert zia_bud.conceptroot._factheirs == {}

    # WHEN
    zia_bud.settle_bud()

    # THEN
    assert zia_bud.conceptroot._factheirs != {}
    clean_factheir = factheir_shop(clean_way, clean_way, 1.0, 5.0)
    assert zia_bud.conceptroot._factheirs == {clean_factheir.fcontext: clean_factheir}


def test_BudUnit_settle_bud_RaisesErrorIfNonRangeRootHasFactUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_way = zia_bud.make_l1_way(casa_str)
    zia_bud.set_l1_concept(conceptunit_shop(casa_str))
    clean_str = "clean"
    clean_way = zia_bud.make_way(casa_way, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_concept = conceptunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_way = zia_bud.make_way(clean_way, sweep_str)
    sweep_concept = conceptunit_shop(sweep_str, addin=2)
    zia_bud.set_concept(clean_concept, parent_way=casa_way)
    zia_bud.set_concept(sweep_concept, parent_way=clean_way)
    zia_bud.add_fact(sweep_way, sweep_way, fopen=1, fnigh=5)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.settle_bud()
    assert (
        str(excinfo.value)
        == f"Cannot have fact for range inheritor '{sweep_way}'. A ranged fact concept must have _begin, _close"
    )


def test_BudUnit_settle_bud_FactHeirsCorrectlyInherited():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_str = "swim"
    swim_way = zia_bud.make_l1_way(swim_str)
    zia_bud.set_l1_concept(conceptunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    fast_way = zia_bud.make_way(swim_way, fast_str)
    slow_way = zia_bud.make_way(swim_way, slow_str)
    zia_bud.set_concept(conceptunit_shop(fast_str), parent_way=swim_way)
    zia_bud.set_concept(conceptunit_shop(slow_str), parent_way=swim_way)

    earth_str = "earth"
    earth_way = zia_bud.make_l1_way(earth_str)
    zia_bud.set_l1_concept(conceptunit_shop(earth_str))

    swim_concept = zia_bud.get_concept_obj(swim_way)
    fast_concept = zia_bud.get_concept_obj(fast_way)
    slow_concept = zia_bud.get_concept_obj(slow_way)
    zia_bud.add_fact(fcontext=earth_way, fstate=earth_way, fopen=1.0, fnigh=5.0)
    assert swim_concept._factheirs == {}
    assert fast_concept._factheirs == {}
    assert slow_concept._factheirs == {}

    # WHEN
    zia_bud.settle_bud()

    # THEN
    assert swim_concept._factheirs != {}
    assert fast_concept._factheirs != {}
    assert slow_concept._factheirs != {}
    factheir_set_range = factheir_shop(earth_way, earth_way, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.fcontext: factheir_set_range}
    assert swim_concept._factheirs == factheirs_set_range
    assert fast_concept._factheirs == factheirs_set_range
    assert slow_concept._factheirs == factheirs_set_range
    print(f"{swim_concept._factheirs=}")
    assert len(swim_concept._factheirs) == 1

    # WHEN
    swim_earth_factheir = swim_concept._factheirs.get(earth_way)
    swim_earth_factheir.set_range_null()

    # THEN
    fact_none_range = factheir_shop(earth_way, earth_way, None, None)
    facts_none_range = {fact_none_range.fcontext: fact_none_range}
    assert swim_concept._factheirs == facts_none_range
    assert fast_concept._factheirs == factheirs_set_range
    assert slow_concept._factheirs == factheirs_set_range

    fact_x1 = swim_concept._factheirs.get(earth_way)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_BudUnit_settle_bud_FactUnitMoldsFactHeir():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_str = "swim"
    swim_way = zia_bud.make_l1_way(swim_str)
    zia_bud.set_l1_concept(conceptunit_shop(swim_str))
    swim_concept = zia_bud.get_concept_obj(swim_way)

    fast_str = "fast"
    slow_str = "slow"
    zia_bud.set_concept(conceptunit_shop(fast_str), parent_way=swim_way)
    zia_bud.set_concept(conceptunit_shop(slow_str), parent_way=swim_way)

    earth_str = "earth"
    earth_way = zia_bud.make_l1_way(earth_str)
    zia_bud.set_l1_concept(conceptunit_shop(earth_str))

    assert swim_concept._factheirs == {}

    # WHEN
    zia_bud.add_fact(fcontext=earth_way, fstate=earth_way, fopen=1.0, fnigh=5.0)
    zia_bud.settle_bud()

    # THEN
    first_earthheir = factheir_shop(earth_way, earth_way, fopen=1.0, fnigh=5.0)
    first_earthdict = {first_earthheir.fcontext: first_earthheir}
    assert swim_concept._factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(fcontext=earth_way, fstate=earth_way, popen=3.0, pnigh=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    zia_bud.add_fact(fcontext=earth_way, fstate=earth_way, fopen=3.0, fnigh=5.0)
    zia_bud.settle_bud()

    # THEN
    after_earthheir = factheir_shop(earth_way, earth_way, fopen=3.0, fnigh=5.0)
    after_earthdict = {after_earthheir.fcontext: after_earthheir}
    assert swim_concept._factheirs == after_earthdict


def test_BudUnit_settle_bud_FactHeirCorrectlyDeletesFactUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    swim_str = "swim"
    swim_way = sue_bud.make_l1_way(swim_str)
    sue_bud.set_l1_concept(conceptunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    sue_bud.set_concept(conceptunit_shop(fast_str), parent_way=swim_way)
    sue_bud.set_concept(conceptunit_shop(slow_str), parent_way=swim_way)
    earth_str = "earth"
    earth_way = sue_bud.make_l1_way(earth_str)
    sue_bud.set_l1_concept(conceptunit_shop(earth_str))
    swim_concept = sue_bud.get_concept_obj(swim_way)
    first_earthheir = factheir_shop(earth_way, earth_way, fopen=200.0, fnigh=500.0)
    first_earthdict = {first_earthheir.fcontext: first_earthheir}
    sue_bud.add_fact(earth_way, earth_way, fopen=200.0, fnigh=500.0)
    assert swim_concept._factheirs == {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert swim_concept._factheirs == first_earthdict

    # WHEN
    earth_curb = factunit_shop(earth_way, earth_way, fopen=3.0, fnigh=4.0)
    swim_concept.set_factunit(factunit=earth_curb)
    sue_bud.settle_bud()

    # THEN
    assert swim_concept._factheirs == first_earthdict
    assert swim_concept.factunits == {}


def test_BudUnit_settle_bud_SetsTaskAsComplete():
    # ESTABLISH
    yao_bud = get_budunit_1Task_1CE0MinutesReason_1Fact()
    mail_str = "obtain mail"
    assert yao_bud is not None
    assert len(yao_bud.conceptroot._kids[mail_str].reasonunits) == 1
    concept_dict = yao_bud.get_concept_dict()
    mail_concept = concept_dict.get(yao_bud.make_l1_way(mail_str))
    hr_str = "hr"
    hr_way = yao_bud.make_l1_way(hr_str)
    yao_bud.add_fact(hr_way, hr_way, fopen=82, fnigh=85)
    assert mail_concept.pledge
    assert mail_concept._task

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert mail_concept.pledge
    assert not mail_concept._task
