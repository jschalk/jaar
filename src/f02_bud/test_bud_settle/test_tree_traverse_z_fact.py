from src.f02_bud.reason_item import factunit_shop, factunit_shop, factheir_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.examples.example_buds import get_budunit_1Task_1CE0MinutesReason_1Fact
from src.f02_bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_settle_bud_ChangesItemUnit_pledge_task():
    # ESTABLISH
    yao_bud = get_budunit_1Task_1CE0MinutesReason_1Fact()
    hour_str = "hour"
    hour_road = yao_bud.make_l1_road(hour_str)

    # WHEN
    yao_bud.set_fact(base=hour_road, pick=hour_road, fopen=82, fnigh=85)

    # THEN
    mail_road = yao_bud.make_l1_road("obtain mail")
    item_dict = yao_bud.get_item_dict()
    mail_item = item_dict.get(mail_road)
    yao_bud.set_fact(base=hour_road, pick=hour_road, fopen=82, fnigh=95)
    assert mail_item.pledge is True
    assert mail_item._task is False

    # WHEN
    yao_bud.settle_bud()

    # THEN
    mail_item = yao_bud.get_item_obj(mail_road)
    assert mail_item.pledge
    assert mail_item._task


def test_BudUnit_settle_bud_ExecutesWithRangeRootFacts():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_road = zia_bud.make_l1_road(casa_str)
    zia_bud.set_l1_item(itemunit_shop(casa_str))
    clean_str = "clean"
    clean_road = zia_bud.make_road(casa_road, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_item = itemunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_gogo_want = -2
    sweep_stop_want = 1
    sweep_item = itemunit_shop(sweep_str, gogo_want=sweep_gogo_want)
    sweep_item.stop_want = sweep_stop_want
    zia_bud.set_item(clean_item, parent_road=casa_road)
    zia_bud.set_fact(base=clean_road, pick=clean_road, fopen=1, fnigh=5)
    assert zia_bud._itemroot._factheirs == {}

    # WHEN
    zia_bud.settle_bud()

    # THEN
    assert zia_bud._itemroot._factheirs != {}
    clean_factheir = factheir_shop(clean_road, clean_road, 1.0, 5.0)
    assert zia_bud._itemroot._factheirs == {clean_factheir.base: clean_factheir}


def test_BudUnit_settle_bud_RaisesErrorIfNonRangeRootHasFactUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    casa_str = "casa"
    casa_road = zia_bud.make_l1_road(casa_str)
    zia_bud.set_l1_item(itemunit_shop(casa_str))
    clean_str = "clean"
    clean_road = zia_bud.make_road(casa_road, clean_str)
    clean_begin = -3
    clean_close = 7
    clean_item = itemunit_shop(clean_str, begin=clean_begin, close=clean_close)
    sweep_str = "sweep"
    sweep_road = zia_bud.make_road(clean_road, sweep_str)
    sweep_item = itemunit_shop(sweep_str, addin=2)
    zia_bud.set_item(clean_item, parent_road=casa_road)
    zia_bud.set_item(sweep_item, parent_road=clean_road)
    zia_bud.set_fact(sweep_road, sweep_road, fopen=1, fnigh=5)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.settle_bud()
    assert (
        str(excinfo.value)
        == f"Cannot have fact for range inheritor '{sweep_road}'. A ranged fact item must have _begin, _close attributes"
    )


def test_BudUnit_settle_bud_FactHeirsCorrectlyInherited():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_str = "swim"
    swim_road = zia_bud.make_l1_road(swim_str)
    zia_bud.set_l1_item(itemunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    fast_road = zia_bud.make_road(swim_road, fast_str)
    slow_road = zia_bud.make_road(swim_road, slow_str)
    zia_bud.set_item(itemunit_shop(fast_str), parent_road=swim_road)
    zia_bud.set_item(itemunit_shop(slow_str), parent_road=swim_road)

    earth_str = "earth"
    earth_road = zia_bud.make_l1_road(earth_str)
    zia_bud.set_l1_item(itemunit_shop(earth_str))

    swim_item = zia_bud.get_item_obj(swim_road)
    fast_item = zia_bud.get_item_obj(fast_road)
    slow_item = zia_bud.get_item_obj(slow_road)
    zia_bud.set_fact(base=earth_road, pick=earth_road, fopen=1.0, fnigh=5.0)
    assert swim_item._factheirs == {}
    assert fast_item._factheirs == {}
    assert slow_item._factheirs == {}

    # WHEN
    zia_bud.settle_bud()

    # THEN
    assert swim_item._factheirs != {}
    assert fast_item._factheirs != {}
    assert slow_item._factheirs != {}
    factheir_set_range = factheir_shop(earth_road, earth_road, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.base: factheir_set_range}
    assert swim_item._factheirs == factheirs_set_range
    assert fast_item._factheirs == factheirs_set_range
    assert slow_item._factheirs == factheirs_set_range
    print(f"{swim_item._factheirs=}")
    assert len(swim_item._factheirs) == 1

    # WHEN
    swim_earth_factheir = swim_item._factheirs.get(earth_road)
    swim_earth_factheir.set_range_null()

    # THEN
    fact_none_range = factheir_shop(earth_road, earth_road, None, None)
    facts_none_range = {fact_none_range.base: fact_none_range}
    assert swim_item._factheirs == facts_none_range
    assert fast_item._factheirs == factheirs_set_range
    assert slow_item._factheirs == factheirs_set_range

    fact_x1 = swim_item._factheirs.get(earth_road)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_BudUnit_settle_bud_FactUnitMoldsFactHeir():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")
    swim_str = "swim"
    swim_road = zia_bud.make_l1_road(swim_str)
    zia_bud.set_l1_item(itemunit_shop(swim_str))
    swim_item = zia_bud.get_item_obj(swim_road)

    fast_str = "fast"
    slow_str = "slow"
    zia_bud.set_item(itemunit_shop(fast_str), parent_road=swim_road)
    zia_bud.set_item(itemunit_shop(slow_str), parent_road=swim_road)

    earth_str = "earth"
    earth_road = zia_bud.make_l1_road(earth_str)
    zia_bud.set_l1_item(itemunit_shop(earth_str))

    assert swim_item._factheirs == {}

    # WHEN
    zia_bud.set_fact(base=earth_road, pick=earth_road, fopen=1.0, fnigh=5.0)
    zia_bud.settle_bud()

    # THEN
    first_earthheir = factheir_shop(earth_road, earth_road, fopen=1.0, fnigh=5.0)
    first_earthdict = {first_earthheir.base: first_earthheir}
    assert swim_item._factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    zia_bud.set_fact(base=earth_road, pick=earth_road, fopen=3.0, fnigh=5.0)
    zia_bud.settle_bud()

    # THEN
    after_earthheir = factheir_shop(earth_road, earth_road, fopen=3.0, fnigh=5.0)
    after_earthdict = {after_earthheir.base: after_earthheir}
    assert swim_item._factheirs == after_earthdict


def test_BudUnit_settle_bud_FactHeirCorrectlyDeletesFactUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    swim_str = "swim"
    swim_road = sue_bud.make_l1_road(swim_str)
    sue_bud.set_l1_item(itemunit_shop(swim_str))
    fast_str = "fast"
    slow_str = "slow"
    sue_bud.set_item(itemunit_shop(fast_str), parent_road=swim_road)
    sue_bud.set_item(itemunit_shop(slow_str), parent_road=swim_road)
    earth_str = "earth"
    earth_road = sue_bud.make_l1_road(earth_str)
    sue_bud.set_l1_item(itemunit_shop(earth_str))
    swim_item = sue_bud.get_item_obj(swim_road)
    first_earthheir = factheir_shop(earth_road, earth_road, fopen=200.0, fnigh=500.0)
    first_earthdict = {first_earthheir.base: first_earthheir}
    sue_bud.set_fact(earth_road, earth_road, fopen=200.0, fnigh=500.0)
    assert swim_item._factheirs == {}

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert swim_item._factheirs == first_earthdict

    # WHEN
    earth_curb = factunit_shop(earth_road, earth_road, fopen=3.0, fnigh=4.0)
    swim_item.set_factunit(factunit=earth_curb)
    sue_bud.settle_bud()

    # THEN
    assert swim_item._factheirs == first_earthdict
    assert swim_item.factunits == {}


def test_BudUnit_settle_bud_SetsTaskAsComplete():
    # ESTABLISH
    yao_bud = get_budunit_1Task_1CE0MinutesReason_1Fact()
    mail_str = "obtain mail"
    assert yao_bud is not None
    assert len(yao_bud._itemroot._kids[mail_str].reasonunits) == 1
    item_dict = yao_bud.get_item_dict()
    mail_item = item_dict.get(yao_bud.make_l1_road(mail_str))
    hour_str = "hour"
    hour_road = yao_bud.make_l1_road(hour_str)
    yao_bud.set_fact(hour_road, hour_road, fopen=82, fnigh=85)
    assert mail_item.pledge
    assert mail_item._task

    # WHEN
    yao_bud.settle_bud()

    # THEN
    assert mail_item.pledge
    assert not mail_item._task
