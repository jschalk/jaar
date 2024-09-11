from src.bud.reason_idea import factunit_shop, factunit_shop, factheir_shop
from src.bud.idea import ideaunit_shop
from src.bud.examples.example_buds import get_budunit_1Task_1CE0MinutesReason_1Fact
from src.bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_settle_bud_ChangesIdeaUnit_pledge_task():
    # ESTABLISH
    yao_bud = get_budunit_1Task_1CE0MinutesReason_1Fact()
    hour_str = "hour"
    hour_road = yao_bud.make_l1_road(hour_str)

    # WHEN
    yao_bud.set_fact(base=hour_road, pick=hour_road, fopen=82, fnigh=85)

    # THEN
    mail_road = yao_bud.make_l1_road("obtain mail")
    idea_dict = yao_bud.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    yao_bud.set_fact(base=hour_road, pick=hour_road, fopen=82, fnigh=95)
    assert mail_idea.pledge is True
    assert mail_idea._task is False

    # WHEN
    yao_bud.settle_bud()

    # THEN
    mail_idea = yao_bud.get_idea_obj(mail_road)
    assert mail_idea.pledge
    assert mail_idea._task


def test_BudUnit_settle_bud_ExecutesWithRangeRootFacts():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_road = zia_bud.make_l1_road(casa_str)
    zia_bud.set_l1_idea(ideaunit_shop(casa_str))
    clean_str = "clean"
    clean_road = zia_bud.make_road(casa_road, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_idea = ideaunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_gogo_want = -2
    sweep_stop_want = 1
    sweep_idea = ideaunit_shop(sweep_str, gogo_want=sweep_gogo_want)
    sweep_idea.stop_want = sweep_stop_want
    zia_bud.set_idea(clean_idea, parent_road=casa_road)
    zia_bud.set_fact(base=clean_road, pick=clean_road, fopen=1, fnigh=5)
    assert zia_bud._idearoot._factheirs == {}

    # WHEN
    zia_bud.settle_bud()

    # THEN
    assert zia_bud._idearoot._factheirs != {}
    clean_factheir = factheir_shop(clean_road, clean_road, 1.0, 5.0)
    assert zia_bud._idearoot._factheirs == {clean_factheir.base: clean_factheir}


def test_BudUnit_settle_bud_RaisesErrorIfNonRangeRootHasFactUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_road = zia_bud.make_l1_road(casa_str)
    zia_bud.set_l1_idea(ideaunit_shop(casa_str))
    clean_str = "clean"
    clean_road = zia_bud.make_road(casa_road, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_idea = ideaunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_road = zia_bud.make_road(clean_road, sweep_str)
    sweep_idea = ideaunit_shop(sweep_str, addin=2)
    zia_bud.set_idea(clean_idea, parent_road=casa_road)
    zia_bud.set_idea(sweep_idea, parent_road=clean_road)
    zia_bud.set_fact(sweep_road, sweep_road, fopen=1, fnigh=5)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.settle_bud()
    assert (
        str(excinfo.value)
        == f"Cannot have fact for range inheritor '{sweep_road}'. A ranged fact idea must have _begin, _close attributes"
    )


def test_BudUnit_settle_bud_FactHeirsCorrectlyInherited():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_str = "swim"
    swim_road = zia_bud.make_l1_road(swim_str)
    zia_bud.set_l1_idea(ideaunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    fast_road = zia_bud.make_road(swim_road, fast_str)
    slow_road = zia_bud.make_road(swim_road, slow_str)
    zia_bud.set_idea(ideaunit_shop(fast_str), parent_road=swim_road)
    zia_bud.set_idea(ideaunit_shop(slow_str), parent_road=swim_road)

    earth_str = "earth"
    earth_road = zia_bud.make_l1_road(earth_str)
    zia_bud.set_l1_idea(ideaunit_shop(earth_str))

    swim_idea = zia_bud.get_idea_obj(swim_road)
    fast_idea = zia_bud.get_idea_obj(fast_road)
    slow_idea = zia_bud.get_idea_obj(slow_road)
    zia_bud.set_fact(base=earth_road, pick=earth_road, fopen=1.0, fnigh=5.0)
    assert swim_idea._factheirs == {}
    assert fast_idea._factheirs == {}
    assert slow_idea._factheirs == {}

    # WHEN
    zia_bud.settle_bud()

    # THEN
    assert swim_idea._factheirs != {}
    assert fast_idea._factheirs != {}
    assert slow_idea._factheirs != {}
    factheir_set_range = factheir_shop(earth_road, earth_road, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.base: factheir_set_range}
    assert swim_idea._factheirs == factheirs_set_range
    assert fast_idea._factheirs == factheirs_set_range
    assert slow_idea._factheirs == factheirs_set_range
    print(f"{swim_idea._factheirs=}")
    assert len(swim_idea._factheirs) == 1

    # WHEN
    swim_earth_factheir = swim_idea._factheirs.get(earth_road)
    swim_earth_factheir.set_range_null()

    # THEN
    fact_none_range = factheir_shop(earth_road, earth_road, None, None)
    facts_none_range = {fact_none_range.base: fact_none_range}
    assert swim_idea._factheirs == facts_none_range
    assert fast_idea._factheirs == factheirs_set_range
    assert slow_idea._factheirs == factheirs_set_range

    fact_x1 = swim_idea._factheirs.get(earth_road)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_BudUnit_settle_bud_FactUnitTransformsFactHeir():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_str = "swim"
    swim_road = zia_bud.make_l1_road(swim_str)
    zia_bud.set_l1_idea(ideaunit_shop(swim_str))
    swim_idea = zia_bud.get_idea_obj(swim_road)

    fast_str = "fast"
    slow_str = "slow"
    zia_bud.set_idea(ideaunit_shop(fast_str), parent_road=swim_road)
    zia_bud.set_idea(ideaunit_shop(slow_str), parent_road=swim_road)

    earth_str = "earth"
    earth_road = zia_bud.make_l1_road(earth_str)
    zia_bud.set_l1_idea(ideaunit_shop(earth_str))

    assert swim_idea._factheirs == {}

    # WHEN
    zia_bud.set_fact(base=earth_road, pick=earth_road, fopen=1.0, fnigh=5.0)
    zia_bud.settle_bud()

    # THEN
    first_earthheir = factheir_shop(earth_road, earth_road, fopen=1.0, fnigh=5.0)
    first_earthdict = {first_earthheir.base: first_earthheir}
    assert swim_idea._factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    zia_bud.set_fact(base=earth_road, pick=earth_road, fopen=3.0, fnigh=5.0)
    zia_bud.settle_bud()

    # THEN
    after_earthheir = factheir_shop(earth_road, earth_road, fopen=3.0, fnigh=5.0)
    after_earthdict = {after_earthheir.base: after_earthheir}
    assert swim_idea._factheirs == after_earthdict


def test_BudUnit_settle_bud_FactHeirCorrectlyDeletesFactUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    swim_str = "swim"
    swim_road = sue_bud.make_l1_road(swim_str)
    sue_bud.set_l1_idea(ideaunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    sue_bud.set_idea(ideaunit_shop(fast_str), parent_road=swim_road)
    sue_bud.set_idea(ideaunit_shop(slow_str), parent_road=swim_road)
    earth_str = "earth"
    earth_road = sue_bud.make_l1_road(earth_str)
    sue_bud.set_l1_idea(ideaunit_shop(earth_str))
    swim_idea = sue_bud.get_idea_obj(swim_road)
    first_earthheir = factheir_shop(earth_road, earth_road, fopen=200.0, fnigh=500.0)
    first_earthdict = {first_earthheir.base: first_earthheir}
    sue_bud.set_fact(earth_road, earth_road, fopen=200.0, fnigh=500.0)
    assert swim_idea._factheirs == {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert swim_idea._factheirs == first_earthdict

    # WHEN
    earth_curb = factunit_shop(earth_road, earth_road, fopen=3.0, fnigh=4.0)
    swim_idea.set_factunit(factunit=earth_curb)
    sue_bud.settle_bud()

    # THEN
    assert swim_idea._factheirs == first_earthdict
    assert swim_idea.factunits == {}


def test_BudUnit_settle_bud_SetsTaskAsComplete():
    # ESTABLISH
    yao_bud = get_budunit_1Task_1CE0MinutesReason_1Fact()
    mail_str = "obtain mail"
    assert yao_bud is not None
    assert len(yao_bud._idearoot._kids[mail_str].reasonunits) == 1
    idea_dict = yao_bud.get_idea_dict()
    mail_idea = idea_dict.get(yao_bud.make_l1_road(mail_str))
    hour_str = "hour"
    hour_road = yao_bud.make_l1_road(hour_str)
    yao_bud.set_fact(hour_road, hour_road, fopen=82, fnigh=85)
    assert mail_idea.pledge
    assert mail_idea._task

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert mail_idea.pledge
    assert not mail_idea._task
