from src.bud.reason_idea import factunit_shop, factunit_shop, factheir_shop
from src.bud.idea import ideaunit_shop
from src.bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_1Task_1CE0MinutesReason_1Fact,
)
from src.bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_set_fact_IsAbleToEditFactUnitAnyAncestor_Idea_1():
    # ESTABLISH
    yao_bud = get_budunit_1Task_1CE0MinutesReason_1Fact()
    ced_min_label = "CE0_minutes"
    ced_road = yao_bud.make_l1_road(ced_min_label)

    # WHEN
    yao_bud.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)

    # THEN
    mail_road = yao_bud.make_l1_road("obtain mail")
    idea_dict = yao_bud.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task is False

    # WHEN
    yao_bud.set_fact(base=ced_road, pick=ced_road, open=82, nigh=95)

    # THEN
    idea_dict = yao_bud.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task == True


def test_BudUnit_set_fact_CorrectlyModifiesAttr_1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")
    sunday_road = sue_bud.make_road(weekday_road, "Sunday")
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_bud_fact)
    x_idearoot = sue_bud._idearoot
    x_idearoot._factunits = {sunday_bud_fact.base: sunday_bud_fact}
    assert x_idearoot._factunits is not None
    x_idearoot._factunits = {}
    assert not x_idearoot._factunits

    # ESTABLISH
    sue_bud.set_fact(base=weekday_road, pick=sunday_road)

    # THEN
    assert x_idearoot._factunits == {sunday_bud_fact.base: sunday_bud_fact}

    # ESTABLISH
    x_idearoot._factunits = {}
    assert not x_idearoot._factunits
    usa_week_road = sue_bud.make_l1_road("nation-state")
    usa_week_unit = factunit_shop(usa_week_road, usa_week_road, open=608, nigh=610)
    x_idearoot._factunits = {usa_week_unit.base: usa_week_unit}

    x_idearoot._factunits = {}
    assert not x_idearoot._factunits

    # WHEN
    sue_bud.set_fact(base=usa_week_road, pick=usa_week_road, open=608, nigh=610)

    # THEN
    assert x_idearoot._factunits is not None
    assert x_idearoot._factunits == {usa_week_unit.base: usa_week_unit}


def test_BudUnit_set_fact_CorrectlyModifiesAttr_2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")
    sunday_road = sue_bud.make_road(weekday_road, "Sunday")

    # WHEN
    sue_bud.set_fact(base=weekday_road, pick=sunday_road)

    # THEN
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    x_idearoot = sue_bud._idearoot
    assert x_idearoot._factunits == {sunday_bud_fact.base: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_pick_IsNone():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")

    # WHEN
    sue_bud.set_fact(base=weekday_road, open=5, nigh=7)

    # THEN
    sunday_bud_fact = factunit_shop(weekday_road, weekday_road, 5, 7)
    x_idearoot = sue_bud._idearoot
    assert x_idearoot._factunits == {sunday_bud_fact.base: sunday_bud_fact}


def test_BudUnit_set_fact_CorrectlyModifiesAttrWhen_open_IsNone():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")
    sue_bud.set_fact(base=weekday_road, open=5, nigh=7)
    x_idearoot = sue_bud._idearoot
    assert x_idearoot._factunits.get(weekday_road) == factunit_shop(
        weekday_road, weekday_road, 5, 7
    )

    # WHEN
    sue_bud.set_fact(base=weekday_road, nigh=10)

    # THEN
    assert x_idearoot._factunits.get(weekday_road) == factunit_shop(
        weekday_road, weekday_road, 5, 10
    )


def test_BudUnit_set_fact_FailsToCreateWhenBaseAndFactAreDifferenctAndFactIdeaIsNotRangeRoot():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    bob_bud.set_l1_idea(time_idea)
    time_road = bob_bud.make_l1_road(time_text)
    a1st = "age1st"
    a1st_road = bob_bud.make_road(time_road, a1st)
    a1st_idea = ideaunit_shop(a1st, _begin=0, _close=20)
    bob_bud.set_idea(a1st_idea, parent_road=time_road)
    a1e1st_text = "a1_era1st"
    a1e1st_idea = ideaunit_shop(a1e1st_text, _begin=20, _close=30)
    bob_bud.set_idea(a1e1st_idea, parent_road=a1st_road)
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
    sue_bud = get_budunit_with_4_levels()
    weekday_road = sue_bud.make_l1_road("weekdays")
    sunday_road = sue_bud.make_road(weekday_road, "Sunday")
    sue_bud.set_fact(base=weekday_road, pick=sunday_road)
    sunday_bud_fact = factunit_shop(base=weekday_road, pick=sunday_road)
    x_idearoot = sue_bud._idearoot
    assert x_idearoot._factunits == {sunday_bud_fact.base: sunday_bud_fact}

    # WHEN
    sue_bud.del_fact(base=weekday_road)

    # THEN
    assert x_idearoot._factunits == {}


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


def test_BudUnit_get_rangeroot_factunits_ReturnsObjsScenario0():
    # ESTABLISH a single ranged fact
    sue_bud = budunit_shop("Sue")
    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    sue_bud.set_l1_idea(time_idea)

    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text, pledge=True)
    sue_bud.set_l1_idea(clean_idea)
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
    sue_bud.set_l1_idea(place_idea)
    place_road = sue_bud.make_l1_road(place_text)
    sue_bud.set_fact(base=place_road, pick=place_road, open=5, nigh=10)
    print(f"When one ranged fact added {sue_bud._idearoot._factunits=}")
    assert len(sue_bud._idearoot._factunits) == 2

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2

    # WHEN one non-ranged_fact added
    mood = "mood_x"
    sue_bud.set_l1_idea(ideaunit_shop(mood))
    m_road = sue_bud.make_l1_road(mood)
    sue_bud.set_fact(base=m_road, pick=m_road)
    print(f"When one non-ranged_fact added {sue_bud._idearoot._factunits=}")
    assert len(sue_bud._idearoot._factunits) == 3

    # THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 2


def test_BudUnit_get_rangeroot_factunits_ReturnsObjsScenario1():
    # ESTABLISH a two ranged facts where one is "range-root" get_root_ranged_facts returns one "range-root" fact
    sue_bud = budunit_shop("Sue")
    time_text = "time"
    sue_bud.set_l1_idea(ideaunit_shop(time_text, _begin=0, _close=140))
    time_road = sue_bud.make_l1_road(time_text)
    mood_x = "mood_x"
    sue_bud.set_l1_idea(ideaunit_shop(mood_x))
    m_x_road = sue_bud.make_l1_road(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_bud.set_idea(ideaunit_shop(happy), parent_road=m_x_road)
    sue_bud.set_idea(ideaunit_shop(sad), parent_road=m_x_road)
    sue_bud.set_fact(base=time_road, pick=time_road, open=5, nigh=10)
    sue_bud.set_fact(base=m_x_road, pick=sue_bud.make_road(m_x_road, happy))
    print(
        f"Establish a root ranged fact and non-range fact:\n{sue_bud._idearoot._factunits=}"
    )
    assert len(sue_bud._idearoot._factunits) == 2

    # WHEN / THEN
    assert len(sue_bud._get_rangeroot_factunits()) == 1
    assert sue_bud._get_rangeroot_factunits()[0].base == time_road


def test_BudUnit_create_lemma_facts_CorrectlyCreates1stLevelLemmaFact_Scenario1():
    sue_bud = budunit_shop("Sue")
    # # the pledge
    # clean = "clean"
    # sue_bud.set_idea(ideaunit_shop(clean, pledge=True))

    time_text = "time"
    sue_bud.set_l1_idea(ideaunit_shop(time_text, _begin=0, _close=140))
    time_road = sue_bud.make_l1_road(time_text)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _gogo_want=0, _stop_want=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _gogo_want=20, _stop_want=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _gogo_want=40, _stop_want=60)
    age4th_idea = ideaunit_shop(age4th_text, _gogo_want=60, _stop_want=80)
    age5th_idea = ideaunit_shop(age5th_text, _gogo_want=80, _stop_want=100)
    age6th_idea = ideaunit_shop(age6th_text, _gogo_want=100, _stop_want=120)
    age7th_idea = ideaunit_shop(age7th_text, _gogo_want=120, _stop_want=140)
    sue_bud.set_idea(age1st_idea, parent_road=time_road)
    sue_bud.set_idea(age2nd_idea, parent_road=time_road)
    sue_bud.set_idea(age3rd_idea, parent_road=time_road)
    sue_bud.set_idea(age4th_idea, parent_road=time_road)
    sue_bud.set_idea(age5th_idea, parent_road=time_road)
    sue_bud.set_idea(age6th_idea, parent_road=time_road)
    sue_bud.set_idea(age7th_idea, parent_road=time_road)

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


def test_BudUnit_create_lemma_facts_CorrectlyCreates1stLevelLemmaFact_Scenario2():
    sue_bud = budunit_shop("Sue")
    # # the pledge
    # clean = "clean"
    # sue_bud.set_idea(ideaunit_shop(clean, pledge=True))

    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    time_road = sue_bud.make_l1_road(time_text)
    sue_bud.set_l1_idea(time_idea)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _gogo_want=0, _stop_want=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _gogo_want=20, _stop_want=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _gogo_want=40, _stop_want=60)
    age4th_idea = ideaunit_shop(age4th_text, _gogo_want=60, _stop_want=80)
    age5th_idea = ideaunit_shop(age5th_text, _gogo_want=80, _stop_want=100)
    age6th_idea = ideaunit_shop(age6th_text, _gogo_want=100, _stop_want=120)
    age7th_idea = ideaunit_shop(age7th_text, _gogo_want=120, _stop_want=140)
    sue_bud.set_idea(age1st_idea, parent_road=time_road)
    sue_bud.set_idea(age2nd_idea, parent_road=time_road)
    sue_bud.set_idea(age3rd_idea, parent_road=time_road)
    sue_bud.set_idea(age4th_idea, parent_road=time_road)
    sue_bud.set_idea(age5th_idea, parent_road=time_road)
    sue_bud.set_idea(age6th_idea, parent_road=time_road)
    sue_bud.set_idea(age7th_idea, parent_road=time_road)

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


def test_BudUnit_create_lemma_facts_CorrectlyCreates1stLevelLemmaFact_Scenario3():
    sue_bud = budunit_shop("Sue")
    # # the pledge
    # clean = "clean"
    # sue_bud.set_idea(ideaunit_shop(clean, pledge=True))

    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    time_road = sue_bud.make_l1_road(time_text)
    sue_bud.set_l1_idea(time_idea)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _gogo_want=0, _stop_want=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _gogo_want=20, _stop_want=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _gogo_want=40, _stop_want=60)
    age4th_idea = ideaunit_shop(age4th_text, _gogo_want=60, _stop_want=80)
    age5th_idea = ideaunit_shop(age5th_text, _gogo_want=80, _stop_want=100)
    age6th_idea = ideaunit_shop(age6th_text, _gogo_want=100, _stop_want=120)
    age7th_idea = ideaunit_shop(age7th_text, _gogo_want=120, _stop_want=140)
    sue_bud.set_idea(age1st_idea, parent_road=time_road)
    sue_bud.set_idea(age2nd_idea, parent_road=time_road)
    sue_bud.set_idea(age3rd_idea, parent_road=time_road)
    sue_bud.set_idea(age4th_idea, parent_road=time_road)
    sue_bud.set_idea(age5th_idea, parent_road=time_road)
    sue_bud.set_idea(age6th_idea, parent_road=time_road)
    sue_bud.set_idea(age7th_idea, parent_road=time_road)

    a2_road = sue_bud.make_road(time_road, age2nd_text)
    a2e1st_text = "a1_era1st"
    a2e2nd_text = "a1_era2nd"
    a2e3rd_text = "a1_era3rd"
    a2e4th_text = "a1_era4th"
    a2e1st_idea = ideaunit_shop(a2e1st_text, _gogo_want=20, _stop_want=30)
    a2e2nd_idea = ideaunit_shop(a2e2nd_text, _gogo_want=30, _stop_want=34)
    a2e3rd_idea = ideaunit_shop(a2e3rd_text, _gogo_want=34, _stop_want=38)
    a2e4th_idea = ideaunit_shop(a2e4th_text, _gogo_want=38, _stop_want=40)
    sue_bud.set_idea(a2e1st_idea, parent_road=a2_road)
    sue_bud.set_idea(a2e2nd_idea, parent_road=a2_road)
    sue_bud.set_idea(a2e3rd_idea, parent_road=a2_road)
    sue_bud.set_idea(a2e4th_idea, parent_road=a2_road)

    a3_road = sue_bud.make_road(time_road, age3rd_text)
    a3e1st_text = "a3_era1st"
    a3e2nd_text = "a3_era2nd"
    a3e3rd_text = "a3_era3rd"
    a3e4th_text = "a3_era4th"
    a3e1st_idea = ideaunit_shop(a3e1st_text, _gogo_want=40, _stop_want=45)
    a3e2nd_idea = ideaunit_shop(a3e2nd_text, _gogo_want=45, _stop_want=50)
    a3e3rd_idea = ideaunit_shop(a3e3rd_text, _gogo_want=55, _stop_want=58)
    a3e4th_idea = ideaunit_shop(a3e4th_text, _gogo_want=58, _stop_want=60)
    sue_bud.set_idea(a3e1st_idea, parent_road=a3_road)
    sue_bud.set_idea(a3e2nd_idea, parent_road=a3_road)
    sue_bud.set_idea(a3e3rd_idea, parent_road=a3_road)
    sue_bud.set_idea(a3e4th_idea, parent_road=a3_road)

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
    assert sue_bud._idearoot.get_kid(situations_text) is not None
    assert sue_bud.get_idea_obj(situations_road) is not None
    assert sue_bud.get_idea_obj(climate_road) is not None
