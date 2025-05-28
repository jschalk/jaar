from src.a04_reason_logic.reason_concept import factunit_shop, factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels
from pytest import raises as pytest_raises


def test_BudUnit_set_fact_CorrectlyModifiesAttr_1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")
    sunday_way = sue_bud.make_way(weekday_way, "Sunday")
    sunday_bud_fact = factunit_shop(fcontext=weekday_way, fbranch=sunday_way)
    print(sunday_bud_fact)
    x_conceptroot = sue_bud.conceptroot
    x_conceptroot.factunits = {sunday_bud_fact.fcontext: sunday_bud_fact}
    assert x_conceptroot.factunits is not None
    x_conceptroot.factunits = {}
    assert not x_conceptroot.factunits

    # ESTABLISH
    sue_bud.add_fact(fcontext=weekday_way, fbranch=sunday_way)

    # THEN
    assert x_conceptroot.factunits == {sunday_bud_fact.fcontext: sunday_bud_fact}

    # ESTABLISH
    x_conceptroot.factunits = {}
    assert not x_conceptroot.factunits
    usa_week_way = sue_bud.make_l1_way("nation")
    usa_week_fact = factunit_shop(usa_week_way, usa_week_way, fopen=608, fnigh=610)
    x_conceptroot.factunits = {usa_week_fact.fcontext: usa_week_fact}

    x_conceptroot.factunits = {}
    assert not x_conceptroot.factunits

    # WHEN
    sue_bud.add_fact(fcontext=usa_week_way, fbranch=usa_week_way, fopen=608, fnigh=610)

    # THEN
    assert x_conceptroot.factunits is not None
    assert x_conceptroot.factunits == {usa_week_fact.fcontext: usa_week_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttr_2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")
    sunday_way = sue_bud.make_way(weekday_way, "Sunday")

    # WHEN
    sue_bud.add_fact(fcontext=weekday_way, fbranch=sunday_way)

    # THEN
    sunday_bud_fact = factunit_shop(fcontext=weekday_way, fbranch=sunday_way)
    x_conceptroot = sue_bud.conceptroot
    assert x_conceptroot.factunits == {sunday_bud_fact.fcontext: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_fbranch_IsNone():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")

    # WHEN
    sue_bud.add_fact(fcontext=weekday_way, fopen=5, fnigh=7)

    # THEN
    sunday_bud_fact = factunit_shop(weekday_way, weekday_way, 5, 7)
    x_conceptroot = sue_bud.conceptroot
    assert x_conceptroot.factunits == {sunday_bud_fact.fcontext: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_popen_IsNone():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")
    sue_bud.add_fact(fcontext=weekday_way, fopen=5, fnigh=7)
    x_conceptroot = sue_bud.conceptroot
    x7_factunit = factunit_shop(weekday_way, weekday_way, 5, 7)
    assert x_conceptroot.factunits.get(weekday_way) == x7_factunit

    # WHEN
    sue_bud.add_fact(fcontext=weekday_way, fnigh=10)

    # THEN
    x10_factunit = factunit_shop(weekday_way, weekday_way, 5, 10)
    assert x_conceptroot.factunits.get(weekday_way) == x10_factunit


def test_BudUnit_set_fact_FailsToCreateWhenRcontextAndFactAreDifferenctAndFactConceptIsNot_RangeRoot():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    time_str = "time"
    time_concept = conceptunit_shop(time_str, begin=0, close=140)
    bob_bud.set_l1_concept(time_concept)
    time_way = bob_bud.make_l1_way(time_str)
    a1st = "age1st"
    a1st_way = bob_bud.make_way(time_way, a1st)
    a1st_concept = conceptunit_shop(a1st, begin=0, close=20)
    bob_bud.set_concept(a1st_concept, parent_way=time_way)
    a1e1st_str = "a1_era1st"
    a1e1st_concept = conceptunit_shop(a1e1st_str, begin=20, close=30)
    bob_bud.set_concept(a1e1st_concept, parent_way=a1st_way)
    a1e1_way = bob_bud.make_way(a1st_way, a1e1st_str)
    assert bob_bud.conceptroot.factunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_bud.add_fact(fcontext=a1e1_way, fbranch=a1e1_way, fopen=20, fnigh=23)
    x_str = f"Non range-root fact:{a1e1_way} can only be set by range-root fact"
    assert str(excinfo.value) == x_str


def test_BudUnit_del_fact_CorrectlyModifiesAttr():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_way = sue_bud.make_l1_way("weekdays")
    sunday_way = sue_bud.make_way(weekday_way, "Sunday")
    sue_bud.add_fact(fcontext=weekday_way, fbranch=sunday_way)
    sunday_bud_fact = factunit_shop(fcontext=weekday_way, fbranch=sunday_way)
    x_conceptroot = sue_bud.conceptroot
    assert x_conceptroot.factunits == {sunday_bud_fact.fcontext: sunday_bud_fact}

    # WHEN
    sue_bud.del_fact(fcontext=weekday_way)

    # THEN
    assert x_conceptroot.factunits == {}


def test_BudUnit_get_fact_ReturnsFactUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    situations_str = "situations"
    situations_way = sue_bud.make_l1_way(situations_str)
    climate_str = "climate"
    climate_way = sue_bud.make_way(situations_way, climate_str)
    sue_bud.add_fact(situations_way, climate_way, create_missing_concepts=True)

    # WHEN
    generated_situations_rcontext = sue_bud.get_fact(situations_way)

    # THEN
    static_situations_rcontext = sue_bud.conceptroot.factunits.get(situations_way)
    assert generated_situations_rcontext == static_situations_rcontext


def test_BudUnit_get_rangeroot_factunits_ReturnsObjsScenario0():
    # ESTABLISH a single ranged fact
    sue_bud = budunit_shop("Sue")
    time_str = "time"
    time_concept = conceptunit_shop(time_str, begin=0, close=140)
    sue_bud.set_l1_concept(time_concept)

    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str, pledge=True)
    sue_bud.set_l1_concept(clean_concept)
    c_way = sue_bud.make_l1_way(clean_str)
    time_way = sue_bud.make_l1_way(time_str)
    # sue_bud.edit_concept_attr(c_way, reason_rcontext=time_way, reason_premise=time_way, popen=5, reason_pnigh=10)

    sue_bud.add_fact(fcontext=time_way, fbranch=time_way, fopen=5, fnigh=10)
    print(f"Establish a single ranged fact {sue_bud.conceptroot.factunits=}")
    assert len(sue_bud.conceptroot.factunits) == 1

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1

    # WHEN one ranged fact added
    place_str = "place_x"
    place_concept = conceptunit_shop(place_str, begin=600, close=800)
    sue_bud.set_l1_concept(place_concept)
    place_way = sue_bud.make_l1_way(place_str)
    sue_bud.add_fact(fcontext=place_way, fbranch=place_way, fopen=5, fnigh=10)
    print(f"When one ranged fact added {sue_bud.conceptroot.factunits=}")
    assert len(sue_bud.conceptroot.factunits) == 2

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2

    # WHEN one non-ranged_fact added
    mood = "mood_x"
    sue_bud.set_l1_concept(conceptunit_shop(mood))
    m_way = sue_bud.make_l1_way(mood)
    sue_bud.add_fact(fcontext=m_way, fbranch=m_way)
    print(f"When one non-ranged_fact added {sue_bud.conceptroot.factunits=}")
    assert len(sue_bud.conceptroot.factunits) == 3

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2


def test_BudUnit_get_rangeroot_factunits_ReturnsObjsScenario1():
    # ESTABLISH a two ranged facts where one is "range-root" get_root_ranged_facts returns one "range-root" fact
    sue_bud = budunit_shop("Sue")
    time_str = "time"
    sue_bud.set_l1_concept(conceptunit_shop(time_str, begin=0, close=140))
    time_way = sue_bud.make_l1_way(time_str)
    mood_x = "mood_x"
    sue_bud.set_l1_concept(conceptunit_shop(mood_x))
    m_x_way = sue_bud.make_l1_way(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_bud.set_concept(conceptunit_shop(happy), parent_way=m_x_way)
    sue_bud.set_concept(conceptunit_shop(sad), parent_way=m_x_way)
    sue_bud.add_fact(fcontext=time_way, fbranch=time_way, fopen=5, fnigh=10)
    sue_bud.add_fact(fcontext=m_x_way, fbranch=sue_bud.make_way(m_x_way, happy))
    print(
        f"Establish a root ranged fact and non-range fact:\n{sue_bud.conceptroot.factunits=}"
    )
    assert len(sue_bud.conceptroot.factunits) == 2

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1
    assert sue_bud._get_rangeroot_factunits()[0].fcontext == time_way


def test_BudUnit_set_fact_create_missing_concepts_CreatesRcontextAndFact():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    situations_str = "situations"
    situations_way = sue_bud.make_l1_way(situations_str)
    climate_str = "climate"
    climate_way = sue_bud.make_way(situations_way, climate_str)
    assert sue_bud.conceptroot.get_kid(situations_str) is None

    # WHEN
    sue_bud.add_fact(situations_way, climate_way, create_missing_concepts=True)

    # THEN
    assert sue_bud.conceptroot.get_kid(situations_str) is not None
    assert sue_bud.get_concept_obj(situations_way) is not None
    assert sue_bud.get_concept_obj(climate_way) is not None
