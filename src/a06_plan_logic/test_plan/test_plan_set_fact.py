from pytest import raises as pytest_raises
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic._test_util.example_plans import get_planunit_with_4_levels
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_set_fact_CorrectlyModifiesAttr_1():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wkday_rope = sue_plan.make_l1_rope("wkdays")
    sunday_rope = sue_plan.make_rope(wkday_rope, "Sunday")
    sunday_plan_fact = factunit_shop(fcontext=wkday_rope, fstate=sunday_rope)
    print(sunday_plan_fact)
    x_conceptroot = sue_plan.conceptroot
    x_conceptroot.factunits = {sunday_plan_fact.fcontext: sunday_plan_fact}
    assert x_conceptroot.factunits is not None
    x_conceptroot.factunits = {}
    assert not x_conceptroot.factunits

    # ESTABLISH
    sue_plan.add_fact(fcontext=wkday_rope, fstate=sunday_rope)

    # THEN
    assert x_conceptroot.factunits == {sunday_plan_fact.fcontext: sunday_plan_fact}

    # ESTABLISH
    x_conceptroot.factunits = {}
    assert not x_conceptroot.factunits
    usa_wk_rope = sue_plan.make_l1_rope("nation")
    usa_wk_fact = factunit_shop(usa_wk_rope, usa_wk_rope, fopen=608, fnigh=610)
    x_conceptroot.factunits = {usa_wk_fact.fcontext: usa_wk_fact}

    x_conceptroot.factunits = {}
    assert not x_conceptroot.factunits

    # WHEN
    sue_plan.add_fact(fcontext=usa_wk_rope, fstate=usa_wk_rope, fopen=608, fnigh=610)

    # THEN
    assert x_conceptroot.factunits is not None
    assert x_conceptroot.factunits == {usa_wk_fact.fcontext: usa_wk_fact}


def test_PlanUnit_set_fact_CorrectlyModifiesAttr_2():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wkday_rope = sue_plan.make_l1_rope("wkdays")
    sunday_rope = sue_plan.make_rope(wkday_rope, "Sunday")

    # WHEN
    sue_plan.add_fact(fcontext=wkday_rope, fstate=sunday_rope)

    # THEN
    sunday_plan_fact = factunit_shop(fcontext=wkday_rope, fstate=sunday_rope)
    x_conceptroot = sue_plan.conceptroot
    assert x_conceptroot.factunits == {sunday_plan_fact.fcontext: sunday_plan_fact}


def test_PlanUnit_set_fact_CorrectlyModifiesAttrWhen_fstate_IsNone():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wkday_rope = sue_plan.make_l1_rope("wkdays")

    # WHEN
    sue_plan.add_fact(fcontext=wkday_rope, fopen=5, fnigh=7)

    # THEN
    sunday_plan_fact = factunit_shop(wkday_rope, wkday_rope, 5, 7)
    x_conceptroot = sue_plan.conceptroot
    assert x_conceptroot.factunits == {sunday_plan_fact.fcontext: sunday_plan_fact}


def test_PlanUnit_set_fact_CorrectlyModifiesAttrWhen_popen_IsNone():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wkday_rope = sue_plan.make_l1_rope("wkdays")
    sue_plan.add_fact(fcontext=wkday_rope, fopen=5, fnigh=7)
    x_conceptroot = sue_plan.conceptroot
    x7_factunit = factunit_shop(wkday_rope, wkday_rope, 5, 7)
    assert x_conceptroot.factunits.get(wkday_rope) == x7_factunit

    # WHEN
    sue_plan.add_fact(fcontext=wkday_rope, fnigh=10)

    # THEN
    x10_factunit = factunit_shop(wkday_rope, wkday_rope, 5, 10)
    assert x_conceptroot.factunits.get(wkday_rope) == x10_factunit


def test_PlanUnit_set_fact_FailsToCreateWhenRcontextAndFactAreDifferenctAndFactConceptIsNot_RangeRoot():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    time_str = "time"
    time_concept = conceptunit_shop(time_str, begin=0, close=140)
    bob_plan.set_l1_concept(time_concept)
    time_rope = bob_plan.make_l1_rope(time_str)
    a1st = "age1st"
    a1st_rope = bob_plan.make_rope(time_rope, a1st)
    a1st_concept = conceptunit_shop(a1st, begin=0, close=20)
    bob_plan.set_concept(a1st_concept, parent_rope=time_rope)
    a1e1st_str = "a1_era1st"
    a1e1st_concept = conceptunit_shop(a1e1st_str, begin=20, close=30)
    bob_plan.set_concept(a1e1st_concept, parent_rope=a1st_rope)
    a1e1_rope = bob_plan.make_rope(a1st_rope, a1e1st_str)
    assert bob_plan.conceptroot.factunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_plan.add_fact(fcontext=a1e1_rope, fstate=a1e1_rope, fopen=20, fnigh=23)
    x_str = f"Non range-root fact:{a1e1_rope} can only be set by range-root fact"
    assert str(excinfo.value) == x_str


def test_PlanUnit_del_fact_CorrectlyModifiesAttr():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wkday_rope = sue_plan.make_l1_rope("wkdays")
    sunday_rope = sue_plan.make_rope(wkday_rope, "Sunday")
    sue_plan.add_fact(fcontext=wkday_rope, fstate=sunday_rope)
    sunday_plan_fact = factunit_shop(fcontext=wkday_rope, fstate=sunday_rope)
    x_conceptroot = sue_plan.conceptroot
    assert x_conceptroot.factunits == {sunday_plan_fact.fcontext: sunday_plan_fact}

    # WHEN
    sue_plan.del_fact(fcontext=wkday_rope)

    # THEN
    assert x_conceptroot.factunits == {}


def test_PlanUnit_get_fact_ReturnsFactUnit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    situations_str = "situations"
    situations_rope = sue_plan.make_l1_rope(situations_str)
    climate_str = "climate"
    climate_rope = sue_plan.make_rope(situations_rope, climate_str)
    sue_plan.add_fact(situations_rope, climate_rope, create_missing_concepts=True)

    # WHEN
    generated_situations_rcontext = sue_plan.get_fact(situations_rope)

    # THEN
    static_situations_rcontext = sue_plan.conceptroot.factunits.get(situations_rope)
    assert generated_situations_rcontext == static_situations_rcontext


def test_PlanUnit_get_rangeroot_factunits_ReturnsObjsScenario0():
    # ESTABLISH a single ranged fact
    sue_plan = planunit_shop("Sue")
    time_str = "time"
    time_concept = conceptunit_shop(time_str, begin=0, close=140)
    sue_plan.set_l1_concept(time_concept)

    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str, task=True)
    sue_plan.set_l1_concept(clean_concept)
    c_rope = sue_plan.make_l1_rope(clean_str)
    time_rope = sue_plan.make_l1_rope(time_str)
    # sue_plan.edit_concept_attr(c_rope, reason_rcontext=time_rope, reason_premise=time_rope, popen=5, reason_pnigh=10)

    sue_plan.add_fact(fcontext=time_rope, fstate=time_rope, fopen=5, fnigh=10)
    print(f"Establish a single ranged fact {sue_plan.conceptroot.factunits=}")
    assert len(sue_plan.conceptroot.factunits) == 1

    # WHEN / THEN
    assert len(sue_plan._get_rangeroot_factunits()) == 1

    # WHEN one ranged fact added
    place_str = "place_x"
    place_concept = conceptunit_shop(place_str, begin=600, close=800)
    sue_plan.set_l1_concept(place_concept)
    place_rope = sue_plan.make_l1_rope(place_str)
    sue_plan.add_fact(fcontext=place_rope, fstate=place_rope, fopen=5, fnigh=10)
    print(f"When one ranged fact added {sue_plan.conceptroot.factunits=}")
    assert len(sue_plan.conceptroot.factunits) == 2

    # THEN
    assert len(sue_plan._get_rangeroot_factunits()) == 2

    # WHEN one non-ranged_fact added
    mood = "mood_x"
    sue_plan.set_l1_concept(conceptunit_shop(mood))
    m_rope = sue_plan.make_l1_rope(mood)
    sue_plan.add_fact(fcontext=m_rope, fstate=m_rope)
    print(f"When one non-ranged_fact added {sue_plan.conceptroot.factunits=}")
    assert len(sue_plan.conceptroot.factunits) == 3

    # THEN
    assert len(sue_plan._get_rangeroot_factunits()) == 2


def test_PlanUnit_get_rangeroot_factunits_ReturnsObjsScenario1():
    # ESTABLISH a two ranged facts where one is "range-root" get_root_ranged_facts returns one "range-root" fact
    sue_plan = planunit_shop("Sue")
    time_str = "time"
    sue_plan.set_l1_concept(conceptunit_shop(time_str, begin=0, close=140))
    time_rope = sue_plan.make_l1_rope(time_str)
    mood_x = "mood_x"
    sue_plan.set_l1_concept(conceptunit_shop(mood_x))
    m_x_rope = sue_plan.make_l1_rope(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_plan.set_concept(conceptunit_shop(happy), parent_rope=m_x_rope)
    sue_plan.set_concept(conceptunit_shop(sad), parent_rope=m_x_rope)
    sue_plan.add_fact(fcontext=time_rope, fstate=time_rope, fopen=5, fnigh=10)
    sue_plan.add_fact(fcontext=m_x_rope, fstate=sue_plan.make_rope(m_x_rope, happy))
    print(
        f"Establish a root ranged fact and non-range fact:\n{sue_plan.conceptroot.factunits=}"
    )
    assert len(sue_plan.conceptroot.factunits) == 2

    # WHEN / THEN
    assert len(sue_plan._get_rangeroot_factunits()) == 1
    assert sue_plan._get_rangeroot_factunits()[0].fcontext == time_rope


def test_PlanUnit_set_fact_create_missing_concepts_CreatesRcontextAndFact():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    situations_str = "situations"
    situations_rope = sue_plan.make_l1_rope(situations_str)
    climate_str = "climate"
    climate_rope = sue_plan.make_rope(situations_rope, climate_str)
    assert sue_plan.conceptroot.get_kid(situations_str) is None

    # WHEN
    sue_plan.add_fact(situations_rope, climate_rope, create_missing_concepts=True)

    # THEN
    assert sue_plan.conceptroot.get_kid(situations_str) is not None
    assert sue_plan.get_concept_obj(situations_rope) is not None
    assert sue_plan.get_concept_obj(climate_rope) is not None
