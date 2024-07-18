from src.bud.reason_idea import factunit_shop, factunit_shop, factheir_shop
from src.bud.idea import ideaunit_shop
from src.bud.examples.example_buds import (
    get_bud_with_4_levels as examples_get_bud_with_4_levels,
    get_bud_1Task_1CE0MinutesReason_1Fact as example_buds_get_bud_1Task_1CE0MinutesReason_1Fact,
)
from src.bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_set_fact_CorrectlyModifiesAttr_1():
    # ESTABLISH
    x_bud = examples_get_bud_with_4_levels()
    weekday_road = x_bud.make_l1_road("weekdays")
    sunday_road = x_bud.make_road(weekday_road, "Sunday")
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_bud_fact)
    x_idearoot = x_bud._idearoot
    x_idearoot._factunits = {sunday_bud_fact.base: sunday_bud_fact}
    assert x_idearoot._factunits != None
    x_idearoot._factunits = {}
    assert not x_idearoot._factunits

    # ESTABLISH
    x_bud.set_fact(base=weekday_road, pick=sunday_road)

    # THEN
    assert x_idearoot._factunits == {sunday_bud_fact.base: sunday_bud_fact}

    # ESTABLISH
    x_idearoot._factunits = {}
    assert not x_idearoot._factunits
    usa_week_road = x_bud.make_l1_road("nation-state")
    usa_week_unit = factunit_shop(usa_week_road, usa_week_road, open=608, nigh=610)
    x_idearoot._factunits = {usa_week_unit.base: usa_week_unit}

    x_idearoot._factunits = {}
    assert not x_idearoot._factunits

    # WHEN
    x_bud.set_fact(base=usa_week_road, pick=usa_week_road, open=608, nigh=610)

    # THEN
    assert x_idearoot._factunits != None
    assert x_idearoot._factunits == {usa_week_unit.base: usa_week_unit}


def test_BudUnit_set_fact_CorrectlyModifiesAttr_2():
    # ESTABLISH
    x_bud = examples_get_bud_with_4_levels()
    weekday_road = x_bud.make_l1_road("weekdays")
    sunday_road = x_bud.make_road(weekday_road, "Sunday")

    # WHEN
    x_bud.set_fact(base=weekday_road, pick=sunday_road)

    # THEN
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    x_idearoot = x_bud._idearoot
    assert x_idearoot._factunits == {sunday_bud_fact.base: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_pick_IsNone():
    # ESTABLISH
    x_bud = examples_get_bud_with_4_levels()
    weekday_road = x_bud.make_l1_road("weekdays")

    # WHEN
    x_bud.set_fact(base=weekday_road, open=5, nigh=7)

    # THEN
    sunday_bud_fact = factunit_shop(weekday_road, weekday_road, 5, 7)
    x_idearoot = x_bud._idearoot
    assert x_idearoot._factunits == {sunday_bud_fact.base: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_open_IsNone():
    # ESTABLISH
    x_bud = examples_get_bud_with_4_levels()
    weekday_road = x_bud.make_l1_road("weekdays")
    x_bud.set_fact(base=weekday_road, open=5, nigh=7)
    x_idearoot = x_bud._idearoot
    assert x_idearoot._factunits.get(weekday_road) == factunit_shop(
        weekday_road, weekday_road, 5, 7
    )

    # WHEN
    x_bud.set_fact(base=weekday_road, nigh=10)

    # THEN
    assert x_idearoot._factunits.get(weekday_road) == factunit_shop(
        weekday_road, weekday_road, 5, 10
    )


def test_BudUnit_set_fact_FailsToCreateWhenBaseAndFactAreDifferenctAndFactIdeaIsNotRangeRoot():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    bob_bud.add_l1_idea(time_idea)
    time_road = bob_bud.make_l1_road(time_text)
    a1st = "age1st"
    a1st_road = bob_bud.make_road(time_road, a1st)
    a1st_idea = ideaunit_shop(a1st, _begin=0, _close=20)
    bob_bud.add_idea(a1st_idea, parent_road=time_road)
    a1e1st_text = "a1_era1st"
    a1e1st_idea = ideaunit_shop(a1e1st_text, _begin=20, _close=30)
    bob_bud.add_idea(a1e1st_idea, parent_road=a1st_road)
    a1e1_road = bob_bud.make_road(a1st_road, a1e1st_text)
    assert bob_bud._idearoot._factunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_bud.set_fact(base=a1e1_road, pick=a1e1_road, open=20, nigh=23)
    assert (
        str(excinfo.value)
        == f"Non range-root fact:{a1e1_road} can only be set by range-root fact"
    )


def test_BudUnit_del_fact_CorrectlyModifiesAttr():
    # ESTABLISH
    x_bud = examples_get_bud_with_4_levels()
    weekday_road = x_bud.make_l1_road("weekdays")
    sunday_road = x_bud.make_road(weekday_road, "Sunday")
    x_bud.set_fact(base=weekday_road, pick=sunday_road)
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    x_idearoot = x_bud._idearoot
    assert x_idearoot._factunits == {sunday_bud_fact.base: sunday_bud_fact}

    # WHEN
    x_bud.del_fact(base=weekday_road)

    # THEN
    assert x_idearoot._factunits == {}


def test_BudUnit_get_idea_list_FactHeirsCorrectlyInherited():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    swim_text = "swim"
    swim_road = bob_bud.make_l1_road(swim_text)
    bob_bud.add_l1_idea(ideaunit_shop(swim_text))
    fast_text = "fast"
    slow_text = "slow"
    fast_road = bob_bud.make_road(swim_road, fast_text)
    slow_road = bob_bud.make_road(swim_road, slow_text)
    bob_bud.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    bob_bud.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)

    earth_text = "earth"
    earth_road = bob_bud.make_l1_road(earth_text)
    bob_bud.add_l1_idea(ideaunit_shop(earth_text))

    swim_idea = bob_bud.get_idea_obj(swim_road)
    fast_idea = bob_bud.get_idea_obj(fast_road)
    slow_idea = bob_bud.get_idea_obj(slow_road)

    assert swim_idea._factheirs == {}
    assert fast_idea._factheirs == {}
    assert slow_idea._factheirs == {}

    # WHEN
    bob_bud.set_fact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)
    factheir_set_range = factheir_shop(earth_road, earth_road, 1.0, 5.0)
    factheirs_set_range = {factheir_set_range.base: factheir_set_range}
    fact_none_range = factheir_shop(earth_road, earth_road, None, None)
    facts_none_range = {fact_none_range.base: fact_none_range}

    # THEN
    assert swim_idea._factheirs != None
    assert fast_idea._factheirs != None
    assert slow_idea._factheirs != None
    assert swim_idea._factheirs == factheirs_set_range
    assert fast_idea._factheirs == factheirs_set_range
    assert slow_idea._factheirs == factheirs_set_range
    print(f"{swim_idea._factheirs=}")
    assert len(swim_idea._factheirs) == 1

    # WHEN
    swim_idea._factheirs.get(earth_road).set_range_null()

    # THEN
    assert swim_idea._factheirs == facts_none_range
    assert fast_idea._factheirs == factheirs_set_range
    assert slow_idea._factheirs == factheirs_set_range

    fact_x1 = swim_idea._factheirs.get(earth_road)
    fact_x1.set_range_null()
    print(type(fact_x1))
    assert str(type(fact_x1)).find(".reason.FactHeir'>")


def test_BudUnit_get_idea_list_FactUnitCorrectlyTransformsfactheir_shop():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    swim_text = "swim"
    swim_road = bob_bud.make_l1_road(swim_text)
    bob_bud.add_l1_idea(ideaunit_shop(swim_text))
    swim_idea = bob_bud.get_idea_obj(swim_road)

    fast_text = "fast"
    slow_text = "slow"
    bob_bud.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    bob_bud.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)

    earth_text = "earth"
    earth_road = bob_bud.make_l1_road(earth_text)
    bob_bud.add_l1_idea(ideaunit_shop(earth_text))

    assert swim_idea._factheirs == {}

    # WHEN
    bob_bud.set_fact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)

    # THEN
    first_earthheir = factheir_shop(earth_road, earth_road, open=1.0, nigh=5.0)
    first_earthdict = {first_earthheir.base: first_earthheir}
    assert swim_idea._factheirs == first_earthdict

    # WHEN
    # earth_curb = factunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    # swim_y.set_factunit(factunit=earth_curb) Not sure what this is for. Testing what "set_factunit" does with the parameters, but what?
    bob_bud.set_fact(base=earth_road, pick=earth_road, open=3.0, nigh=5.0)

    # THEN
    after_earthheir = factheir_shop(earth_road, earth_road, open=3.0, nigh=5.0)
    after_earthdict = {after_earthheir.base: after_earthheir}
    assert swim_idea._factheirs == after_earthdict


def test_BudUnit_get_idea_list_FactHeirCorrectlyDeletesFactUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    swim_text = "swim"
    swim_road = sue_bud.make_l1_road(swim_text)
    sue_bud.add_l1_idea(ideaunit_shop(swim_text))
    fast_text = "fast"
    slow_text = "slow"
    sue_bud.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    sue_bud.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)
    earth_text = "earth"
    earth_road = sue_bud.make_l1_road(earth_text)
    sue_bud.add_l1_idea(ideaunit_shop(earth_text))

    swim_idea = sue_bud.get_idea_obj(swim_road)

    first_earthheir = factheir_shop(earth_road, earth_road, open=200.0, nigh=500.0)
    first_earthdict = {first_earthheir.base: first_earthheir}

    assert swim_idea._factheirs == {}

    # WHEN
    sue_bud.set_fact(base=earth_road, pick=earth_road, open=200.0, nigh=500.0)

    # THEN
    assert swim_idea._factheirs == first_earthdict

    earth_curb = factunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    swim_idea.set_factunit(factunit=earth_curb)
    sue_bud.settle_bud()
    assert swim_idea._factheirs == first_earthdict
    assert swim_idea._factunits == {}


def test_get_ranged_facts():
    # ESTABLISH a single ranged fact
    sue_bud = budunit_shop("Sue")
    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    sue_bud.add_l1_idea(time_idea)

    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text, pledge=True)
    sue_bud.add_l1_idea(clean_idea)
    c_road = sue_bud.make_l1_road(clean_text)
    time_road = sue_bud.make_l1_road(time_text)
    # sue_bud.edit_idea_attr(road=c_road, reason_base=time_road, reason_premise=time_road, reason_premise_open=5, reason_premise_nigh=10)

    sue_bud.set_fact(base=time_road, pick=time_road, open=5, nigh=10)
    print(f"Establish a single ranged fact {sue_bud._idearoot._factunits=}")
    assert len(sue_bud._idearoot._factunits) == 1

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1

    # WHEN one ranged fact added
    place_text = "place_x"
    place_idea = ideaunit_shop(place_text, _begin=600, _close=800)
    sue_bud.add_l1_idea(place_idea)
    place_road = sue_bud.make_l1_road(place_text)
    sue_bud.set_fact(base=place_road, pick=place_road, open=5, nigh=10)
    print(f"When one ranged fact added {sue_bud._idearoot._factunits=}")
    assert len(sue_bud._idearoot._factunits) == 2

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2

    # WHEN one non-ranged_fact added
    mood = "mood_x"
    sue_bud.add_l1_idea(ideaunit_shop(mood))
    m_road = sue_bud.make_l1_road(mood)
    sue_bud.set_fact(base=m_road, pick=m_road)
    print(f"When one non-ranged_fact added {sue_bud._idearoot._factunits=}")
    assert len(sue_bud._idearoot._factunits) == 3

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2


def test_get_roots_ranged_facts():
    # ESTABLISH a two ranged facts where one is "range-root" get_root_ranged_facts returns one "range-root" fact
    sue_bud = budunit_shop("Sue")
    time_text = "time"
    sue_bud.add_l1_idea(ideaunit_shop(time_text, _begin=0, _close=140))
    time_road = sue_bud.make_l1_road(time_text)
    mood_x = "mood_x"
    sue_bud.add_l1_idea(ideaunit_shop(mood_x))
    m_x_road = sue_bud.make_l1_road(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_bud.add_idea(ideaunit_shop(happy), parent_road=m_x_road)
    sue_bud.add_idea(ideaunit_shop(sad), parent_road=m_x_road)
    sue_bud.set_fact(base=time_road, pick=time_road, open=5, nigh=10)
    sue_bud.set_fact(base=m_x_road, pick=sue_bud.make_road(m_x_road, happy))
    print(
        f"Establish a root ranged fact and non-range fact:\n{sue_bud._idearoot._factunits=}"
    )
    assert len(sue_bud._idearoot._factunits) == 2

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1
    assert sue_bud._get_rangeroot_factunits()[0].base == time_road

    # a fact who's idea range is defined by numeric_root is not "rangeroot"
    mirror_x = "mirror_x"
    sue_bud.add_l1_idea(ideaunit_shop(mirror_x, _numeric_road=time_text))
    m_x_road = sue_bud.make_l1_road(mirror_x)
    sue_bud.set_fact(base=m_x_road, pick=time_road, open=5, nigh=10)
    assert len(sue_bud._idearoot._factunits) == 3

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1
    assert sue_bud._get_rangeroot_factunits()[0].base == time_road


def test_create_lemma_facts_CorrectlyCreates1stLevelLemmaFact_Scenario1():
    sue_bud = budunit_shop("Sue")
    # # the pledge
    # clean = "clean"
    # sue_bud.add_idea(ideaunit_shop(clean, pledge=True))

    time_text = "time"
    sue_bud.add_l1_idea(ideaunit_shop(time_text, _begin=0, _close=140))
    time_road = sue_bud.make_l1_road(time_text)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _begin=0, _close=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _begin=20, _close=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _begin=40, _close=60)
    age4th_idea = ideaunit_shop(age4th_text, _begin=60, _close=80)
    age5th_idea = ideaunit_shop(age5th_text, _begin=80, _close=100)
    age6th_idea = ideaunit_shop(age6th_text, _begin=100, _close=120)
    age7th_idea = ideaunit_shop(age7th_text, _begin=120, _close=140)
    sue_bud.add_idea(age1st_idea, parent_road=time_road)
    sue_bud.add_idea(age2nd_idea, parent_road=time_road)
    sue_bud.add_idea(age3rd_idea, parent_road=time_road)
    sue_bud.add_idea(age4th_idea, parent_road=time_road)
    sue_bud.add_idea(age5th_idea, parent_road=time_road)
    sue_bud.add_idea(age6th_idea, parent_road=time_road)
    sue_bud.add_idea(age7th_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_bud.set_fact(base=time_road, pick=time_road, open=45, nigh=45)
    lemma_dict = sue_bud._get_lemma_factunits()
    print(f"{len(lemma_dict)=}")
    print(f"{lemma_dict=}")
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[sue_bud.make_road(time_road, age1st_text)]
    age2nd_lemma = lemma_dict[sue_bud.make_road(time_road, age2nd_text)]
    age3rd_lemma = lemma_dict[sue_bud.make_road(time_road, age3rd_text)]
    age4th_lemma = lemma_dict[sue_bud.make_road(time_road, age4th_text)]
    age5th_lemma = lemma_dict[sue_bud.make_road(time_road, age5th_text)]
    age6th_lemma = lemma_dict[sue_bud.make_road(time_road, age6th_text)]
    age7th_lemma = lemma_dict[sue_bud.make_road(time_road, age7th_text)]
    assert age1st_lemma.open is None
    assert age2nd_lemma.open is None
    assert age3rd_lemma.open == 45
    assert age4th_lemma.open is None
    assert age5th_lemma.open is None
    assert age6th_lemma.open is None
    assert age7th_lemma.open is None
    assert age1st_lemma.nigh is None
    assert age2nd_lemma.nigh is None
    assert age3rd_lemma.nigh == 45
    assert age4th_lemma.nigh is None
    assert age5th_lemma.nigh is None
    assert age6th_lemma.nigh is None
    assert age7th_lemma.nigh is None


def test_create_lemma_facts_CorrectlyCreates1stLevelLemmaFact_Scenario2():
    sue_bud = budunit_shop("Sue")
    # # the pledge
    # clean = "clean"
    # sue_bud.add_idea(ideaunit_shop(clean, pledge=True))

    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    time_road = sue_bud.make_l1_road(time_text)
    sue_bud.add_l1_idea(time_idea)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _begin=0, _close=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _begin=20, _close=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _begin=40, _close=60)
    age4th_idea = ideaunit_shop(age4th_text, _begin=60, _close=80)
    age5th_idea = ideaunit_shop(age5th_text, _begin=80, _close=100)
    age6th_idea = ideaunit_shop(age6th_text, _begin=100, _close=120)
    age7th_idea = ideaunit_shop(age7th_text, _begin=120, _close=140)
    sue_bud.add_idea(age1st_idea, parent_road=time_road)
    sue_bud.add_idea(age2nd_idea, parent_road=time_road)
    sue_bud.add_idea(age3rd_idea, parent_road=time_road)
    sue_bud.add_idea(age4th_idea, parent_road=time_road)
    sue_bud.add_idea(age5th_idea, parent_road=time_road)
    sue_bud.add_idea(age6th_idea, parent_road=time_road)
    sue_bud.add_idea(age7th_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_bud.set_fact(base=time_road, pick=time_road, open=35, nigh=65)
    lemma_dict = sue_bud._get_lemma_factunits()
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[sue_bud.make_road(time_road, age1st_text)]
    age2nd_lemma = lemma_dict[sue_bud.make_road(time_road, age2nd_text)]
    age3rd_lemma = lemma_dict[sue_bud.make_road(time_road, age3rd_text)]
    age4th_lemma = lemma_dict[sue_bud.make_road(time_road, age4th_text)]
    age5th_lemma = lemma_dict[sue_bud.make_road(time_road, age5th_text)]
    age6th_lemma = lemma_dict[sue_bud.make_road(time_road, age6th_text)]
    age7th_lemma = lemma_dict[sue_bud.make_road(time_road, age7th_text)]
    assert age1st_lemma.open is None
    assert age2nd_lemma.open == 35
    assert age3rd_lemma.open == 40
    assert age4th_lemma.open == 60
    assert age5th_lemma.open is None
    assert age6th_lemma.open is None
    assert age7th_lemma.open is None
    assert age1st_lemma.nigh is None
    assert age2nd_lemma.nigh == 40
    assert age3rd_lemma.nigh == 60
    assert age4th_lemma.nigh == 65
    assert age5th_lemma.nigh is None
    assert age6th_lemma.nigh is None
    assert age7th_lemma.nigh is None


def test_create_lemma_facts_CorrectlyCreates1stLevelLemmaFact_Scenario3():
    sue_bud = budunit_shop("Sue")
    # # the pledge
    # clean = "clean"
    # sue_bud.add_idea(ideaunit_shop(clean, pledge=True))

    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    time_road = sue_bud.make_l1_road(time_text)
    sue_bud.add_l1_idea(time_idea)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _begin=0, _close=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _begin=20, _close=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _begin=40, _close=60)
    age4th_idea = ideaunit_shop(age4th_text, _begin=60, _close=80)
    age5th_idea = ideaunit_shop(age5th_text, _begin=80, _close=100)
    age6th_idea = ideaunit_shop(age6th_text, _begin=100, _close=120)
    age7th_idea = ideaunit_shop(age7th_text, _begin=120, _close=140)
    sue_bud.add_idea(age1st_idea, parent_road=time_road)
    sue_bud.add_idea(age2nd_idea, parent_road=time_road)
    sue_bud.add_idea(age3rd_idea, parent_road=time_road)
    sue_bud.add_idea(age4th_idea, parent_road=time_road)
    sue_bud.add_idea(age5th_idea, parent_road=time_road)
    sue_bud.add_idea(age6th_idea, parent_road=time_road)
    sue_bud.add_idea(age7th_idea, parent_road=time_road)

    a2_road = sue_bud.make_road(time_road, age2nd_text)
    a2e1st_text = "a1_era1st"
    a2e2nd_text = "a1_era2nd"
    a2e3rd_text = "a1_era3rd"
    a2e4th_text = "a1_era4th"
    a2e1st_idea = ideaunit_shop(a2e1st_text, _begin=20, _close=30)
    a2e2nd_idea = ideaunit_shop(a2e2nd_text, _begin=30, _close=34)
    a2e3rd_idea = ideaunit_shop(a2e3rd_text, _begin=34, _close=38)
    a2e4th_idea = ideaunit_shop(a2e4th_text, _begin=38, _close=40)
    sue_bud.add_idea(a2e1st_idea, parent_road=a2_road)
    sue_bud.add_idea(a2e2nd_idea, parent_road=a2_road)
    sue_bud.add_idea(a2e3rd_idea, parent_road=a2_road)
    sue_bud.add_idea(a2e4th_idea, parent_road=a2_road)

    a3_road = sue_bud.make_road(time_road, age3rd_text)
    a3e1st_text = "a3_era1st"
    a3e2nd_text = "a3_era2nd"
    a3e3rd_text = "a3_era3rd"
    a3e4th_text = "a3_era4th"
    a3e1st_idea = ideaunit_shop(a3e1st_text, _begin=40, _close=45)
    a3e2nd_idea = ideaunit_shop(a3e2nd_text, _begin=45, _close=50)
    a3e3rd_idea = ideaunit_shop(a3e3rd_text, _begin=55, _close=58)
    a3e4th_idea = ideaunit_shop(a3e4th_text, _begin=58, _close=60)
    sue_bud.add_idea(a3e1st_idea, parent_road=a3_road)
    sue_bud.add_idea(a3e2nd_idea, parent_road=a3_road)
    sue_bud.add_idea(a3e3rd_idea, parent_road=a3_road)
    sue_bud.add_idea(a3e4th_idea, parent_road=a3_road)

    # set for instant moment in 3rd age
    sue_bud.set_fact(base=time_road, pick=time_road, open=35, nigh=55)
    lemma_dict = sue_bud._get_lemma_factunits()
    assert len(lemma_dict) == 15
    a2e1st_lemma = lemma_dict[sue_bud.make_road(a2_road, a2e1st_text)]
    a2e2nd_lemma = lemma_dict[sue_bud.make_road(a2_road, a2e2nd_text)]
    a2e3rd_lemma = lemma_dict[sue_bud.make_road(a2_road, a2e3rd_text)]
    a2e4th_lemma = lemma_dict[sue_bud.make_road(a2_road, a2e4th_text)]
    a3e1st_lemma = lemma_dict[sue_bud.make_road(a3_road, a3e1st_text)]
    a3e2nd_lemma = lemma_dict[sue_bud.make_road(a3_road, a3e2nd_text)]
    a3e3rd_lemma = lemma_dict[sue_bud.make_road(a3_road, a3e3rd_text)]
    a3e4th_lemma = lemma_dict[sue_bud.make_road(a3_road, a3e4th_text)]
    assert a2e1st_lemma.open is None
    assert a2e2nd_lemma.open is None
    assert a2e3rd_lemma.open == 35
    assert a2e4th_lemma.open == 38
    assert a3e1st_lemma.open == 40
    assert a3e2nd_lemma.open == 45
    assert a3e3rd_lemma.open is None
    assert a3e4th_lemma.open is None
    assert a2e1st_lemma.nigh is None
    assert a2e2nd_lemma.nigh is None
    assert a2e3rd_lemma.nigh == 38
    assert a2e4th_lemma.nigh == 40
    assert a3e1st_lemma.nigh == 45
    assert a3e2nd_lemma.nigh == 50
    assert a3e3rd_lemma.nigh is None
    assert a3e4th_lemma.nigh is None


def test_create_lemma_facts_CorrectlyCreates1stLevelLemmaFact_Scenario4():
    sue_bud = budunit_shop("Sue")
    arsub1 = "descending_subsecction1"
    arsub1_idea = ideaunit_shop(arsub1, _begin=0, _close=140)
    as1_road = sue_bud.make_l1_road(arsub1)
    sue_bud.add_l1_idea(arsub1_idea)
    # range-root idea has range_source_road
    time_text = "time"
    time_idea = ideaunit_shop(
        time_text, _begin=0, _close=140, _range_source_road=as1_road
    )
    sue_bud.add_l1_idea(time_idea)

    arsub2 = "descending_subsecction2"
    arsub2_idea = ideaunit_shop(arsub2, _begin=0, _close=20)
    as2_road = sue_bud.make_l1_road(arsub2)
    sue_bud.add_l1_idea(arsub2_idea)

    # non-range-root child idea has range_source_road
    time_road = sue_bud.make_l1_road(time_text)
    age1st = "age1st"
    age1st_idea = ideaunit_shop(
        age1st, _begin=0, _close=20, _range_source_road=as2_road
    )
    sue_bud.add_idea(age1st_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_bud.set_fact(base=time_road, pick=time_road, open=35, nigh=55)
    lemma_dict = sue_bud._get_lemma_factunits()
    assert len(lemma_dict) == 3
    a1_lemma = lemma_dict[sue_bud.make_road(time_road, age1st)]
    as1_lemma = lemma_dict[as1_road]
    as2_lemma = lemma_dict[as2_road]
    assert a1_lemma.open is None
    assert as1_lemma.open == 35
    assert as2_lemma.open is None
    assert a1_lemma.nigh is None
    assert as1_lemma.nigh == 55
    assert as2_lemma.nigh is None


def test_create_lemma_facts_CorrectlyCreatesNthLevelLemmaFact_Scenario4_1():
    sue_bud = budunit_shop("Sue")
    sue_bud.set_time_hreg_ideas(c400_count=7)
    time_road = sue_bud.make_l1_road("time")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    timetech_road = sue_bud.make_road(time_road, "tech")
    sue_bud.set_fact(jajatime_road, jajatime_road, open=1500, nigh=1500)
    lhu = sue_bud._get_lemma_factunits()

    assert lhu[sue_bud.make_road(jajatime_road, "400 year segment")].open == 1500
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segment")].nigh == 1500
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].open > 0
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].open < 1
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].nigh > 0
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].nigh < 1
    assert lhu[sue_bud.make_road(jajatime_road, "days")].open >= 1
    assert lhu[sue_bud.make_road(jajatime_road, "days")].open <= 2
    assert lhu[sue_bud.make_road(jajatime_road, "days")].nigh >= 1
    assert lhu[sue_bud.make_road(jajatime_road, "days")].nigh <= 2
    assert lhu[sue_bud.make_road(jajatime_road, "day")].open == 60
    assert lhu[sue_bud.make_road(jajatime_road, "day")].nigh == 60
    assert lhu[sue_bud.make_road(jajatime_road, "week")].open == 1500
    assert int(lhu[sue_bud.make_road(jajatime_road, "week")].nigh) == 1500
    assert lhu[sue_bud.make_road(timetech_road, "week")].open == 1500
    assert int(lhu[sue_bud.make_road(timetech_road, "week")].nigh) == 1500


def test_create_lemma_facts_CorrectlyCreatesNthLevelLemmaFact_Scenario5():
    sue_bud = budunit_shop("Sue")
    sue_bud.set_time_hreg_ideas(c400_count=7)
    time_road = sue_bud.make_l1_road("time")
    timetech_road = sue_bud.make_road(time_road, "tech")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    sue_bud.set_fact(jajatime_road, jajatime_road, 1500, nigh=1063954002)
    lhu = sue_bud._get_lemma_factunits()

    assert lhu[sue_bud.make_road(jajatime_road, "400 year segment")].open == 0
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segment")].nigh == 210379680
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].open > 0
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].open < 1
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].nigh > 5
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].nigh < 6
    lemma_days = lhu[sue_bud.make_road(jajatime_road, "days")]
    assert int(lemma_days.open) == 1  # 0 / 1440
    assert int(lemma_days.nigh) == 738856  # 1063953183 / 1440
    lemma_day = lhu[sue_bud.make_road(jajatime_road, "day")]
    assert lemma_day.open == 0  # 0 / 1440
    assert lemma_day.nigh == 1440  # 1362  # 1063953183 / 1440
    lemma_jajatime_week = lhu[sue_bud.make_road(jajatime_road, "week")]
    assert lemma_jajatime_week.open == 0  # 0 / 1440
    assert int(lemma_jajatime_week.nigh) == 10080  # 1063953183 / 1440
    lemma_timetech_week = lhu[sue_bud.make_road(jajatime_road, "week")]
    assert lemma_timetech_week.open == 0  # 0 / 1440
    assert int(lemma_timetech_week.nigh) == 10080  # 1063953183 / 1440


def test_create_lemma_facts_CorrectlyCreatesNthLevelLemmaFact_Scenario6():
    sue_bud = budunit_shop("Sue")
    sue_bud.set_time_hreg_ideas(c400_count=7)
    time_road = sue_bud.make_l1_road("time")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    sue_bud.set_fact(jajatime_road, jajatime_road, 1063954000, nigh=1063954002)
    lhu = sue_bud._get_lemma_factunits()

    assert lhu[sue_bud.make_road(jajatime_road, "400 year segment")].open == 12055600.0
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segment")].nigh == 12055602.0
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].open > 5
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].open < 6
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].nigh > 5
    assert lhu[sue_bud.make_road(jajatime_road, "400 year segments")].nigh < 6
    lemma_days = lhu[sue_bud.make_road(jajatime_road, "days")]
    assert int(lemma_days.open) == 738856  # 1063954000 / 1440
    assert int(lemma_days.nigh) == 738856  # 1063954000 / 1440
    lemma_day = lhu[sue_bud.make_road(jajatime_road, "day")]
    assert lemma_day.open == 1360  # 0 / 1440
    assert int(lemma_day.nigh) == 1362  # 1063953183 / 1440


def test_create_lemma_facts_CorrectlyCreatesNthLevelLemmaFact_Scenario7():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud.set_time_hreg_ideas(c400_count=7)
    time_road = sue_bud.make_l1_road("time")
    timetech_road = sue_bud.make_road(time_road, "tech")
    techweek_road = sue_bud.make_road(timetech_road, "week")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")

    # WHEN minute range that should be Thursday to Monday midnight
    sue_bud.set_fact(jajatime_road, jajatime_road, 1063951200, nigh=1063956960)
    lhu = sue_bud._get_lemma_factunits()

    # THEN
    week_open = lhu[sue_bud.make_road(jajatime_road, "week")].open
    week_nigh = lhu[sue_bud.make_road(jajatime_road, "week")].nigh
    week_text = "week"
    print(
        f"for {sue_bud.make_road(jajatime_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_bud.make_road(jajatime_road, "week")].open == 7200
    assert lhu[sue_bud.make_road(jajatime_road, "week")].nigh == 2880

    week_open = lhu[sue_bud.make_road(timetech_road, "week")].open
    week_nigh = lhu[sue_bud.make_road(timetech_road, "week")].nigh
    print(
        f"for {sue_bud.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_bud.make_road(timetech_road, "week")].open == 7200
    assert lhu[sue_bud.make_road(timetech_road, "week")].nigh == 2880
    print(f"{techweek_road=}")
    print(lhu[techweek_road])
    print(lhu[sue_bud.make_road(techweek_road, "Thursday")])
    print(lhu[sue_bud.make_road(techweek_road, "Friday")])
    print(lhu[sue_bud.make_road(techweek_road, "Saturday")])
    print(lhu[sue_bud.make_road(techweek_road, "Sunday")])
    print(lhu[sue_bud.make_road(techweek_road, "Monday")])
    print(lhu[sue_bud.make_road(techweek_road, "Tuesday")])
    print(lhu[sue_bud.make_road(techweek_road, "Wednesday")])


def test_create_lemma_facts_CorrectlyCreatesNthLevelLemmaFact_Scenario8():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud.set_time_hreg_ideas(c400_count=7)
    time_road = sue_bud.make_l1_road("time")
    timetech_road = sue_bud.make_road(time_road, "tech")
    techweek_road = sue_bud.make_road(timetech_road, "week")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")

    # WHEN minute range that should be Thursday to Monday midnight
    sue_bud.set_fact(jajatime_road, jajatime_road, 1063951200, nigh=1063951200)
    lhu = sue_bud._get_lemma_factunits()

    # THEN
    week_open = lhu[techweek_road].open
    week_nigh = lhu[techweek_road].nigh
    print(f"for {techweek_road}: {week_open=} {week_nigh=}")
    assert lhu[techweek_road].open == 7200
    assert lhu[techweek_road].nigh == 7200

    week_open = lhu[sue_bud.make_road(timetech_road, "week")].open
    week_nigh = lhu[sue_bud.make_road(timetech_road, "week")].nigh
    week_text = "week"
    print(
        f"for {sue_bud.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_bud.make_road(timetech_road, "week")].open == 7200
    assert lhu[sue_bud.make_road(timetech_road, "week")].nigh == 7200
    print(lhu[techweek_road])
    print(lhu[sue_bud.make_road(techweek_road, "Thursday")])
    print(lhu[sue_bud.make_road(techweek_road, "Friday")])
    print(lhu[sue_bud.make_road(techweek_road, "Saturday")])
    print(lhu[sue_bud.make_road(techweek_road, "Sunday")])
    print(lhu[sue_bud.make_road(techweek_road, "Monday")])
    print(lhu[sue_bud.make_road(techweek_road, "Tuesday")])
    print(lhu[sue_bud.make_road(techweek_road, "Wednesday")])


def test_BudUnit_set_fact_create_missing_ideas_CreatesBaseAndFact():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    situations_text = "situations"
    situations_road = sue_bud.make_l1_road(situations_text)
    climate_text = "climate"
    climate_road = sue_bud.make_road(situations_road, climate_text)
    assert sue_bud._idearoot.get_kid(situations_text) is None

    # WHEN
    sue_bud.set_fact(situations_road, climate_road, create_missing_ideas=True)

    # THEN
    assert sue_bud._idearoot.get_kid(situations_text) != None
    assert sue_bud.get_idea_obj(situations_road) != None
    assert sue_bud.get_idea_obj(climate_road) != None


def test_BudUnit_get_fact_ReturnsFactUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    situations_text = "situations"
    situations_road = sue_bud.make_l1_road(situations_text)
    climate_text = "climate"
    climate_road = sue_bud.make_road(situations_road, climate_text)
    sue_bud.set_fact(situations_road, climate_road, create_missing_ideas=True)

    # WHEN
    generated_situations_base = sue_bud.get_fact(situations_road)

    # THEN
    static_situations_base = sue_bud._idearoot._factunits.get(situations_road)
    assert generated_situations_base == static_situations_base


def test_BudUnit_set_fact_IsAbleToSetTaskAsComplete():
    # ESTABLISH
    x_bud = example_buds_get_bud_1Task_1CE0MinutesReason_1Fact()
    mail_text = "obtain mail"
    assert x_bud != None
    assert len(x_bud._idearoot._kids[mail_text]._reasonunits) == 1
    idea_dict = x_bud.get_idea_dict()
    # for idea in idea_dict:
    #     print(idea._label)
    mail_idea = idea_dict.get(x_bud.make_l1_road(mail_text))
    assert mail_idea.pledge == True
    assert mail_idea._task == True

    # WHEN
    ced_min_label = "CE0_minutes"
    ced_road = x_bud.make_l1_road(ced_min_label)
    x_bud.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    x_bud.settle_bud()

    # THEN
    assert mail_idea.pledge == True
    assert mail_idea._task is False
