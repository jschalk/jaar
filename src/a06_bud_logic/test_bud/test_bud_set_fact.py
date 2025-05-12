from src.a04_reason_logic.reason_idea import factunit_shop, factunit_shop
from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels
from pytest import raises as pytest_raises


def test_BudUnit_set_fact_CorrectlyModifiesAttr_1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")
    sunday_way = sue_bud.make_way(weekday_way, "Sunday")
    sunday_bud_fact = factunit_shop(fbase=weekday_way, fneed=sunday_way)
    print(sunday_bud_fact)
    x_idearoot = sue_bud.idearoot
    x_idearoot.factunits = {sunday_bud_fact.fbase: sunday_bud_fact}
    assert x_idearoot.factunits is not None
    x_idearoot.factunits = {}
    assert not x_idearoot.factunits

    # ESTABLISH
    sue_bud.add_fact(fbase=weekday_way, fneed=sunday_way)

    # THEN
    assert x_idearoot.factunits == {sunday_bud_fact.fbase: sunday_bud_fact}

    # ESTABLISH
    x_idearoot.factunits = {}
    assert not x_idearoot.factunits
    usa_week_way = sue_bud.make_l1_way("nation-state")
    usa_week_fact = factunit_shop(usa_week_way, usa_week_way, fopen=608, fnigh=610)
    x_idearoot.factunits = {usa_week_fact.fbase: usa_week_fact}

    x_idearoot.factunits = {}
    assert not x_idearoot.factunits

    # WHEN
    sue_bud.add_fact(fbase=usa_week_way, fneed=usa_week_way, fopen=608, fnigh=610)

    # THEN
    assert x_idearoot.factunits is not None
    assert x_idearoot.factunits == {usa_week_fact.fbase: usa_week_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttr_2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")
    sunday_way = sue_bud.make_way(weekday_way, "Sunday")

    # WHEN
    sue_bud.add_fact(fbase=weekday_way, fneed=sunday_way)

    # THEN
    sunday_bud_fact = factunit_shop(fbase=weekday_way, fneed=sunday_way)
    x_idearoot = sue_bud.idearoot
    assert x_idearoot.factunits == {sunday_bud_fact.fbase: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_fneed_IsNone():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")

    # WHEN
    sue_bud.add_fact(fbase=weekday_way, fopen=5, fnigh=7)

    # THEN
    sunday_bud_fact = factunit_shop(weekday_way, weekday_way, 5, 7)
    x_idearoot = sue_bud.idearoot
    assert x_idearoot.factunits == {sunday_bud_fact.fbase: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_open_IsNone():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")
    sue_bud.add_fact(fbase=weekday_way, fopen=5, fnigh=7)
    x_idearoot = sue_bud.idearoot
    x7_factunit = factunit_shop(weekday_way, weekday_way, 5, 7)
    assert x_idearoot.factunits.get(weekday_way) == x7_factunit

    # WHEN
    sue_bud.add_fact(fbase=weekday_way, fnigh=10)

    # THEN
    x10_factunit = factunit_shop(weekday_way, weekday_way, 5, 10)
    assert x_idearoot.factunits.get(weekday_way) == x10_factunit


def test_BudUnit_set_fact_FailsToCreateWhenBaseAndFactAreDifferenctAndFactIdeaIsNot_RangeRoot():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    time_str = "time"
    time_idea = ideaunit_shop(time_str, begin=0, close=140)
    bob_bud.set_l1_idea(time_idea)
    time_way = bob_bud.make_l1_way(time_str)
    a1st = "age1st"
    a1st_way = bob_bud.make_way(time_way, a1st)
    a1st_idea = ideaunit_shop(a1st, begin=0, close=20)
    bob_bud.set_idea(a1st_idea, parent_way=time_way)
    a1e1st_str = "a1_era1st"
    a1e1st_idea = ideaunit_shop(a1e1st_str, begin=20, close=30)
    bob_bud.set_idea(a1e1st_idea, parent_way=a1st_way)
    a1e1_way = bob_bud.make_way(a1st_way, a1e1st_str)
    assert bob_bud.idearoot.factunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_bud.add_fact(fbase=a1e1_way, fneed=a1e1_way, fopen=20, fnigh=23)
    x_str = f"Non range-root fact:{a1e1_way} can only be set by range-root fact"
    assert str(excinfo.value) == x_str


def test_BudUnit_del_fact_CorrectlyModifiesAttr():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")
    sunday_way = sue_bud.make_way(weekday_way, "Sunday")
    sue_bud.add_fact(fbase=weekday_way, fneed=sunday_way)
    sunday_bud_fact = factunit_shop(fbase=weekday_way, fneed=sunday_way)
    x_idearoot = sue_bud.idearoot
    assert x_idearoot.factunits == {sunday_bud_fact.fbase: sunday_bud_fact}

    # WHEN
    sue_bud.del_fact(fbase=weekday_way)

    # THEN
    assert x_idearoot.factunits == {}


def test_BudUnit_get_fact_ReturnsFactUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    situations_str = "situations"
    situations_way = sue_bud.make_l1_way(situations_str)
    climate_str = "climate"
    climate_way = sue_bud.make_way(situations_way, climate_str)
    sue_bud.add_fact(situations_way, climate_way, create_missing_ideas=True)

    # WHEN
    generated_situations_base = sue_bud.get_fact(situations_way)

    # THEN
    static_situations_base = sue_bud.idearoot.factunits.get(situations_way)
    assert generated_situations_base == static_situations_base


def test_BudUnit_get_rangeroot_factunits_ReturnsObjsScenario0():
    # ESTABLISH a single ranged fact
    sue_bud = budunit_shop("Sue")
    time_str = "time"
    time_idea = ideaunit_shop(time_str, begin=0, close=140)
    sue_bud.set_l1_idea(time_idea)

    clean_str = "clean"
    clean_idea = ideaunit_shop(clean_str, pledge=True)
    sue_bud.set_l1_idea(clean_idea)
    c_way = sue_bud.make_l1_way(clean_str)
    time_way = sue_bud.make_l1_way(time_str)
    # sue_bud.edit_idea_attr(c_way, reason_base=time_way, reason_premise=time_way, reason_premise_open=5, reason_premise_nigh=10)

    sue_bud.add_fact(fbase=time_way, fneed=time_way, fopen=5, fnigh=10)
    print(f"Establish a single ranged fact {sue_bud.idearoot.factunits=}")
    assert len(sue_bud.idearoot.factunits) == 1

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1

    # WHEN one ranged fact added
    place_str = "place_x"
    place_idea = ideaunit_shop(place_str, begin=600, close=800)
    sue_bud.set_l1_idea(place_idea)
    place_way = sue_bud.make_l1_way(place_str)
    sue_bud.add_fact(fbase=place_way, fneed=place_way, fopen=5, fnigh=10)
    print(f"When one ranged fact added {sue_bud.idearoot.factunits=}")
    assert len(sue_bud.idearoot.factunits) == 2

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2

    # WHEN one non-ranged_fact added
    mood = "mood_x"
    sue_bud.set_l1_idea(ideaunit_shop(mood))
    m_way = sue_bud.make_l1_way(mood)
    sue_bud.add_fact(fbase=m_way, fneed=m_way)
    print(f"When one non-ranged_fact added {sue_bud.idearoot.factunits=}")
    assert len(sue_bud.idearoot.factunits) == 3

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2


def test_BudUnit_get_rangeroot_factunits_ReturnsObjsScenario1():
    # ESTABLISH a two ranged facts where one is "range-root" get_root_ranged_facts returns one "range-root" fact
    sue_bud = budunit_shop("Sue")
    time_str = "time"
    sue_bud.set_l1_idea(ideaunit_shop(time_str, begin=0, close=140))
    time_way = sue_bud.make_l1_way(time_str)
    mood_x = "mood_x"
    sue_bud.set_l1_idea(ideaunit_shop(mood_x))
    m_x_way = sue_bud.make_l1_way(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_bud.set_idea(ideaunit_shop(happy), parent_way=m_x_way)
    sue_bud.set_idea(ideaunit_shop(sad), parent_way=m_x_way)
    sue_bud.add_fact(fbase=time_way, fneed=time_way, fopen=5, fnigh=10)
    sue_bud.add_fact(fbase=m_x_way, fneed=sue_bud.make_way(m_x_way, happy))
    print(
        f"Establish a root ranged fact and non-range fact:\n{sue_bud.idearoot.factunits=}"
    )
    assert len(sue_bud.idearoot.factunits) == 2

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1
    assert sue_bud._get_rangeroot_factunits()[0].fbase == time_way


def test_BudUnit_set_fact_create_missing_ideas_CreatesBaseAndFact():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    situations_str = "situations"
    situations_way = sue_bud.make_l1_way(situations_str)
    climate_str = "climate"
    climate_way = sue_bud.make_way(situations_way, climate_str)
    assert sue_bud.idearoot.get_kid(situations_str) is None

    # WHEN
    sue_bud.add_fact(situations_way, climate_way, create_missing_ideas=True)

    # THEN
    assert sue_bud.idearoot.get_kid(situations_str) is not None
    assert sue_bud.get_idea_obj(situations_way) is not None
    assert sue_bud.get_idea_obj(climate_way) is not None
