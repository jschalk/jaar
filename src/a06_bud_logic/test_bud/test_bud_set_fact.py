from src.a04_reason_logic.reason_item import factunit_shop, factunit_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels
from pytest import raises as pytest_raises


def test_BudUnit_set_fact_CorrectlyModifiesAttr_1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")
    sunday_road = sue_bud.make_road(weekday_road, "Sunday")
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_bud_fact)
    x_itemroot = sue_bud.itemroot
    x_itemroot.factunits = {sunday_bud_fact.base: sunday_bud_fact}
    assert x_itemroot.factunits is not None
    x_itemroot.factunits = {}
    assert not x_itemroot.factunits

    # ESTABLISH
    sue_bud.add_fact(base=weekday_road, pick=sunday_road)

    # THEN
    assert x_itemroot.factunits == {sunday_bud_fact.base: sunday_bud_fact}

    # ESTABLISH
    x_itemroot.factunits = {}
    assert not x_itemroot.factunits
    usa_week_road = sue_bud.make_l1_road("nation-state")
    usa_week_unit = factunit_shop(usa_week_road, usa_week_road, fopen=608, fnigh=610)
    x_itemroot.factunits = {usa_week_unit.base: usa_week_unit}

    x_itemroot.factunits = {}
    assert not x_itemroot.factunits

    # WHEN
    sue_bud.add_fact(base=usa_week_road, pick=usa_week_road, fopen=608, fnigh=610)

    # THEN
    assert x_itemroot.factunits is not None
    assert x_itemroot.factunits == {usa_week_unit.base: usa_week_unit}


def test_BudUnit_set_fact_CorrectlyModifiesAttr_2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")
    sunday_road = sue_bud.make_road(weekday_road, "Sunday")

    # WHEN
    sue_bud.add_fact(base=weekday_road, pick=sunday_road)

    # THEN
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    x_itemroot = sue_bud.itemroot
    assert x_itemroot.factunits == {sunday_bud_fact.base: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_pick_IsNone():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")

    # WHEN
    sue_bud.add_fact(base=weekday_road, fopen=5, fnigh=7)

    # THEN
    sunday_bud_fact = factunit_shop(weekday_road, weekday_road, 5, 7)
    x_itemroot = sue_bud.itemroot
    assert x_itemroot.factunits == {sunday_bud_fact.base: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_open_IsNone():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")
    sue_bud.add_fact(base=weekday_road, fopen=5, fnigh=7)
    x_itemroot = sue_bud.itemroot
    x7_factunit = factunit_shop(weekday_road, weekday_road, 5, 7)
    assert x_itemroot.factunits.get(weekday_road) == x7_factunit

    # WHEN
    sue_bud.add_fact(base=weekday_road, fnigh=10)

    # THEN
    x10_factunit = factunit_shop(weekday_road, weekday_road, 5, 10)
    assert x_itemroot.factunits.get(weekday_road) == x10_factunit


def test_BudUnit_set_fact_FailsToCreateWhenBaseAndFactAreDifferenctAndFactItemIsNot_RangeRoot():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    time_str = "time"
    time_item = itemunit_shop(time_str, begin=0, close=140)
    bob_bud.set_l1_item(time_item)
    time_road = bob_bud.make_l1_road(time_str)
    a1st = "age1st"
    a1st_road = bob_bud.make_road(time_road, a1st)
    a1st_item = itemunit_shop(a1st, begin=0, close=20)
    bob_bud.set_item(a1st_item, parent_road=time_road)
    a1e1st_str = "a1_era1st"
    a1e1st_item = itemunit_shop(a1e1st_str, begin=20, close=30)
    bob_bud.set_item(a1e1st_item, parent_road=a1st_road)
    a1e1_road = bob_bud.make_road(a1st_road, a1e1st_str)
    assert bob_bud.itemroot.factunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_bud.add_fact(base=a1e1_road, pick=a1e1_road, fopen=20, fnigh=23)
    x_str = f"Non range-root fact:{a1e1_road} can only be set by range-root fact"
    assert str(excinfo.value) == x_str


def test_BudUnit_del_fact_CorrectlyModifiesAttr():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")
    sunday_road = sue_bud.make_road(weekday_road, "Sunday")
    sue_bud.add_fact(base=weekday_road, pick=sunday_road)
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    x_itemroot = sue_bud.itemroot
    assert x_itemroot.factunits == {sunday_bud_fact.base: sunday_bud_fact}

    # WHEN
    sue_bud.del_fact(base=weekday_road)

    # THEN
    assert x_itemroot.factunits == {}


def test_BudUnit_get_fact_ReturnsFactUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    situations_str = "situations"
    situations_road = sue_bud.make_l1_road(situations_str)
    climate_str = "climate"
    climate_road = sue_bud.make_road(situations_road, climate_str)
    sue_bud.add_fact(situations_road, climate_road, create_missing_items=True)

    # WHEN
    generated_situations_base = sue_bud.get_fact(situations_road)

    # THEN
    static_situations_base = sue_bud.itemroot.factunits.get(situations_road)
    assert generated_situations_base == static_situations_base


def test_BudUnit_get_rangeroot_factunits_ReturnsObjsScenario0():
    # ESTABLISH a single ranged fact
    sue_bud = budunit_shop("Sue")
    time_str = "time"
    time_item = itemunit_shop(time_str, begin=0, close=140)
    sue_bud.set_l1_item(time_item)

    clean_str = "clean"
    clean_item = itemunit_shop(clean_str, pledge=True)
    sue_bud.set_l1_item(clean_item)
    c_road = sue_bud.make_l1_road(clean_str)
    time_road = sue_bud.make_l1_road(time_str)
    # sue_bud.edit_item_attr(road=c_road, reason_base=time_road, reason_premise=time_road, reason_premise_open=5, reason_premise_nigh=10)

    sue_bud.add_fact(base=time_road, pick=time_road, fopen=5, fnigh=10)
    print(f"Establish a single ranged fact {sue_bud.itemroot.factunits=}")
    assert len(sue_bud.itemroot.factunits) == 1

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1

    # WHEN one ranged fact added
    place_str = "place_x"
    place_item = itemunit_shop(place_str, begin=600, close=800)
    sue_bud.set_l1_item(place_item)
    place_road = sue_bud.make_l1_road(place_str)
    sue_bud.add_fact(base=place_road, pick=place_road, fopen=5, fnigh=10)
    print(f"When one ranged fact added {sue_bud.itemroot.factunits=}")
    assert len(sue_bud.itemroot.factunits) == 2

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2

    # WHEN one non-ranged_fact added
    mood = "mood_x"
    sue_bud.set_l1_item(itemunit_shop(mood))
    m_road = sue_bud.make_l1_road(mood)
    sue_bud.add_fact(base=m_road, pick=m_road)
    print(f"When one non-ranged_fact added {sue_bud.itemroot.factunits=}")
    assert len(sue_bud.itemroot.factunits) == 3

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2


def test_BudUnit_get_rangeroot_factunits_ReturnsObjsScenario1():
    # ESTABLISH a two ranged facts where one is "range-root" get_root_ranged_facts returns one "range-root" fact
    sue_bud = budunit_shop("Sue")
    time_str = "time"
    sue_bud.set_l1_item(itemunit_shop(time_str, begin=0, close=140))
    time_road = sue_bud.make_l1_road(time_str)
    mood_x = "mood_x"
    sue_bud.set_l1_item(itemunit_shop(mood_x))
    m_x_road = sue_bud.make_l1_road(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_bud.set_item(itemunit_shop(happy), parent_road=m_x_road)
    sue_bud.set_item(itemunit_shop(sad), parent_road=m_x_road)
    sue_bud.add_fact(base=time_road, pick=time_road, fopen=5, fnigh=10)
    sue_bud.add_fact(base=m_x_road, pick=sue_bud.make_road(m_x_road, happy))
    print(
        f"Establish a root ranged fact and non-range fact:\n{sue_bud.itemroot.factunits=}"
    )
    assert len(sue_bud.itemroot.factunits) == 2

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1
    assert sue_bud._get_rangeroot_factunits()[0].base == time_road


def test_BudUnit_set_fact_create_missing_items_CreatesBaseAndFact():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    situations_str = "situations"
    situations_road = sue_bud.make_l1_road(situations_str)
    climate_str = "climate"
    climate_road = sue_bud.make_road(situations_road, climate_str)
    assert sue_bud.itemroot.get_kid(situations_str) is None

    # WHEN
    sue_bud.add_fact(situations_road, climate_road, create_missing_items=True)

    # THEN
    assert sue_bud.itemroot.get_kid(situations_str) is not None
    assert sue_bud.get_item_obj(situations_road) is not None
    assert sue_bud.get_item_obj(climate_road) is not None
