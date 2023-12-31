from src.agenda.required_idea import (
    acptfactunit_shop,
    acptfactunit_shop,
    acptfactheir_shop,
)
from src.agenda.idea import ideaunit_shop, RoadUnit
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as examples_get_agenda_with_4_levels,
)
from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_agenda_acptfact_exists():
    # GIVEN
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")
    sunday_agenda_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_agenda_acptfact)
    x_agenda._idearoot._acptfactunits = {
        sunday_agenda_acptfact.base: sunday_agenda_acptfact
    }
    assert x_agenda._idearoot._acptfactunits != None
    x_agenda._idearoot._acptfactunits = {}
    assert not x_agenda._idearoot._acptfactunits
    x_agenda.set_acptfact(base=weekday_road, pick=sunday_road)
    assert x_agenda._idearoot._acptfactunits == {
        sunday_agenda_acptfact.base: sunday_agenda_acptfact
    }

    x_agenda._idearoot._acptfactunits = {}
    assert not x_agenda._idearoot._acptfactunits
    usa_week_road = x_agenda.make_l1_road("nation-state")
    usa_week_unit = acptfactunit_shop(usa_week_road, usa_week_road, open=608, nigh=610)
    x_agenda._idearoot._acptfactunits = {usa_week_unit.base: usa_week_unit}

    x_agenda._idearoot._acptfactunits = {}
    assert not x_agenda._idearoot._acptfactunits
    x_agenda.set_acptfact(base=usa_week_road, pick=usa_week_road, open=608, nigh=610)
    assert x_agenda._idearoot._acptfactunits != None
    assert x_agenda._idearoot._acptfactunits == {usa_week_unit.base: usa_week_unit}


def test_agenda_acptfact_create():
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")
    x_agenda.set_acptfact(base=weekday_road, pick=sunday_road)
    sunday_agenda_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    assert x_agenda._idearoot._acptfactunits == {
        sunday_agenda_acptfact.base: sunday_agenda_acptfact
    }


def test_set_acptfact_FailsToCreateWhenBaseAndAcptFactAreDifferenctAndAcptFactIdeaIsNotRangeRoot():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    bob_agenda.add_idea(time_idea, bob_agenda._economy_id)
    time_road = bob_agenda.make_l1_road(time_text)
    a1st = "age1st"
    a1st_road = bob_agenda.make_road(time_road, a1st)
    a1st_idea = ideaunit_shop(a1st, _begin=0, _close=20)
    bob_agenda.add_idea(a1st_idea, parent_road=time_road)
    a1e1st_text = "a1_era1st"
    a1e1st_idea = ideaunit_shop(a1e1st_text, _begin=20, _close=30)
    bob_agenda.add_idea(a1e1st_idea, parent_road=a1st_road)
    a1e1_road = bob_agenda.make_road(a1st_road, a1e1st_text)
    assert bob_agenda._idearoot._acptfactunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_agenda.set_acptfact(base=a1e1_road, pick=a1e1_road, open=20, nigh=23)
    assert (
        str(excinfo.value)
        == f"Non range-root acptfact:{a1e1_road} can only be set by range-root acptfact"
    )


def test_agenda_acptfact_create():
    # GIVEN
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")
    x_agenda.set_acptfact(base=weekday_road, pick=sunday_road)
    sunday_agenda_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    assert x_agenda._idearoot._acptfactunits == {
        sunday_agenda_acptfact.base: sunday_agenda_acptfact
    }

    # WHEN
    x_agenda.del_acptfact(base=weekday_road)

    # THEN
    assert x_agenda._idearoot._acptfactunits == {}


def test_agenda_get_idea_list_AcptFactHeirsCorrectlyInherited():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    swim_text = "swim"
    swim_road = bob_agenda.make_l1_road(swim_text)
    bob_agenda.add_idea(ideaunit_shop(swim_text), parent_road=bob_agenda._economy_id)
    fast_text = "fast"
    slow_text = "slow"
    fast_road = bob_agenda.make_road(swim_road, fast_text)
    slow_road = bob_agenda.make_road(swim_road, slow_text)
    bob_agenda.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    bob_agenda.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)

    earth_text = "earth"
    earth_road = bob_agenda.make_l1_road(earth_text)
    bob_agenda.add_idea(ideaunit_shop(earth_text), parent_road=bob_agenda._economy_id)

    swim_idea = bob_agenda.get_idea_obj(swim_road)
    fast_idea = bob_agenda.get_idea_obj(fast_road)
    slow_idea = bob_agenda.get_idea_obj(slow_road)

    assert swim_idea._acptfactheirs == {}
    assert fast_idea._acptfactheirs == {}
    assert slow_idea._acptfactheirs == {}

    # WHEN
    bob_agenda.set_acptfact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)
    acptfactheir_set_range = acptfactheir_shop(earth_road, earth_road, 1.0, 5.0)
    acptfactheirs_set_range = {acptfactheir_set_range.base: acptfactheir_set_range}
    acptfact_none_range = acptfactheir_shop(earth_road, earth_road, None, None)
    acptfacts_none_range = {acptfact_none_range.base: acptfact_none_range}

    # THEN
    assert swim_idea._acptfactheirs != None
    assert fast_idea._acptfactheirs != None
    assert slow_idea._acptfactheirs != None
    assert swim_idea._acptfactheirs == acptfactheirs_set_range
    assert fast_idea._acptfactheirs == acptfactheirs_set_range
    assert slow_idea._acptfactheirs == acptfactheirs_set_range
    print(f"{swim_idea._acptfactheirs=}")
    assert len(swim_idea._acptfactheirs) == 1

    # WHEN
    swim_idea._acptfactheirs.get(earth_road).set_range_null()

    # THEN
    assert swim_idea._acptfactheirs == acptfacts_none_range
    assert fast_idea._acptfactheirs == acptfactheirs_set_range
    assert slow_idea._acptfactheirs == acptfactheirs_set_range

    acptfact_x1 = swim_idea._acptfactheirs.get(earth_road)
    acptfact_x1.set_range_null()
    print(type(acptfact_x1))
    assert str(type(acptfact_x1)).find(".required.AcptFactHeir'>")


def test_agenda_get_idea_list_AcptFactUnitCorrectlyTransformsacptfactheir_shop():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    swim_text = "swim"
    swim_road = bob_agenda.make_l1_road(swim_text)
    bob_agenda.add_idea(ideaunit_shop(swim_text), parent_road=bob_agenda._economy_id)
    swim_idea = bob_agenda.get_idea_obj(swim_road)

    fast_text = "fast"
    slow_text = "slow"
    bob_agenda.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    bob_agenda.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)

    earth_text = "earth"
    earth_road = bob_agenda.make_l1_road(earth_text)
    bob_agenda.add_idea(ideaunit_shop(earth_text), parent_road=bob_agenda._economy_id)

    assert swim_idea._acptfactheirs == {}

    # WHEN
    bob_agenda.set_acptfact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)

    # THEN
    first_earthheir = acptfactheir_shop(earth_road, earth_road, open=1.0, nigh=5.0)
    first_earthdict = {first_earthheir.base: first_earthheir}
    assert swim_idea._acptfactheirs == first_earthdict

    # WHEN
    # earth_curb = acptfactunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    # swim_y.set_acptfactunit(acptfactunit=earth_curb) Not sure what this is for. Testing how "set_acptfactunit" works?
    bob_agenda.set_acptfact(base=earth_road, pick=earth_road, open=3.0, nigh=5.0)

    # THEN
    after_earthheir = acptfactheir_shop(earth_road, earth_road, open=3.0, nigh=5.0)
    after_earthdict = {after_earthheir.base: after_earthheir}
    assert swim_idea._acptfactheirs == after_earthdict


def test_agenda_get_idea_list_AcptFactHeirCorrectlyDeletesAcptFactUnit():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    swim_text = "swim"
    swim_road = sue_agenda.make_l1_road(swim_text)
    sue_agenda.add_idea(ideaunit_shop(swim_text), parent_road=sue_agenda._economy_id)
    fast_text = "fast"
    slow_text = "slow"
    sue_agenda.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    sue_agenda.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)
    earth_text = "earth"
    earth_road = sue_agenda.make_l1_road(earth_text)
    sue_agenda.add_idea(ideaunit_shop(earth_text), parent_road=sue_agenda._economy_id)

    swim_idea = sue_agenda.get_idea_obj(swim_road)

    first_earthheir = acptfactheir_shop(earth_road, earth_road, open=200.0, nigh=500.0)
    first_earthdict = {first_earthheir.base: first_earthheir}

    assert swim_idea._acptfactheirs == {}

    # WHEN
    sue_agenda.set_acptfact(base=earth_road, pick=earth_road, open=200.0, nigh=500.0)

    # THEN
    assert swim_idea._acptfactheirs == first_earthdict

    earth_curb = acptfactunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    swim_idea.set_acptfactunit(acptfactunit=earth_curb)
    sue_agenda.set_agenda_metrics()
    assert swim_idea._acptfactheirs == first_earthdict
    assert swim_idea._acptfactunits == {}


def test_get_ranged_acptfacts():
    # GIVEN a single ranged acptfact
    sue_agenda = agendaunit_shop("Sue")
    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    sue_agenda.add_idea(time_idea, parent_road=sue_agenda._economy_id)

    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text, promise=True)
    sue_agenda.add_idea(clean_idea, parent_road=sue_agenda._economy_id)
    c_road = sue_agenda.make_l1_road(clean_text)
    time_road = sue_agenda.make_l1_road(time_text)
    # sue_agenda.edit_idea_attr(road=c_road, required_base=time_road, required_sufffact=time_road, required_sufffact_open=5, required_sufffact_nigh=10)

    sue_agenda.set_acptfact(base=time_road, pick=time_road, open=5, nigh=10)
    print(f"Given a single ranged acptfact {sue_agenda._idearoot._acptfactunits=}")
    assert len(sue_agenda._idearoot._acptfactunits) == 1

    # WHEN / THEN
    assert len(sue_agenda._get_rangeroot_acptfactunits()) == 1

    # WHEN one ranged acptfact added
    place_text = "place_x"
    place_idea = ideaunit_shop(place_text, _begin=600, _close=800)
    sue_agenda.add_idea(place_idea, parent_road=sue_agenda._economy_id)
    place_road = sue_agenda.make_l1_road(place_text)
    sue_agenda.set_acptfact(base=place_road, pick=place_road, open=5, nigh=10)
    print(f"When one ranged acptfact added {sue_agenda._idearoot._acptfactunits=}")
    assert len(sue_agenda._idearoot._acptfactunits) == 2

    # THEN
    assert len(sue_agenda._get_rangeroot_acptfactunits()) == 2

    # WHEN one non-ranged_acptfact added
    mood = "mood_x"
    sue_agenda.add_idea(ideaunit_shop(mood), parent_road=sue_agenda._economy_id)
    m_road = sue_agenda.make_l1_road(mood)
    sue_agenda.set_acptfact(base=m_road, pick=m_road)
    print(f"When one non-ranged_acptfact added {sue_agenda._idearoot._acptfactunits=}")
    assert len(sue_agenda._idearoot._acptfactunits) == 3

    # THEN
    assert len(sue_agenda._get_rangeroot_acptfactunits()) == 2


def test_get_roots_ranged_acptfacts():
    # GIVEN a two ranged acptfacts where one is "range-root" get_root_ranged_acptfacts returns one "range-root" acptfact
    sue_agenda = agendaunit_shop("Sue")
    time_text = "time"
    sue_agenda.add_idea(
        idea_kid=ideaunit_shop(time_text, _begin=0, _close=140),
        parent_road=sue_agenda._economy_id,
    )
    time_road = sue_agenda.make_l1_road(time_text)
    mood_x = "mood_x"
    sue_agenda.add_idea(ideaunit_shop(mood_x), parent_road=sue_agenda._economy_id)
    m_x_road = sue_agenda.make_l1_road(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_agenda.add_idea(ideaunit_shop(happy), parent_road=m_x_road)
    sue_agenda.add_idea(ideaunit_shop(sad), parent_road=m_x_road)
    sue_agenda.set_acptfact(base=time_road, pick=time_road, open=5, nigh=10)
    sue_agenda.set_acptfact(base=m_x_road, pick=sue_agenda.make_road(m_x_road, happy))
    print(
        f"Given a root ranged acptfact and non-range acptfact:\n{sue_agenda._idearoot._acptfactunits=}"
    )
    assert len(sue_agenda._idearoot._acptfactunits) == 2

    # WHEN / THEN
    assert len(sue_agenda._get_rangeroot_acptfactunits()) == 1
    assert sue_agenda._get_rangeroot_acptfactunits()[0].base == time_road

    # a acptfact who's idea range is defined by numeric_root is not "rangeroot"
    mirrow_x = "mirrow_x"
    sue_agenda.add_idea(
        idea_kid=ideaunit_shop(mirrow_x, _numeric_road=time_text),
        parent_road=sue_agenda._economy_id,
    )
    m_x_road = sue_agenda.make_l1_road(mirrow_x)
    sue_agenda.set_acptfact(base=m_x_road, pick=time_road, open=5, nigh=10)
    assert len(sue_agenda._idearoot._acptfactunits) == 3

    # WHEN / THEN
    assert len(sue_agenda._get_rangeroot_acptfactunits()) == 1
    assert sue_agenda._get_rangeroot_acptfactunits()[0].base == time_road


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario1():
    sue_agenda = agendaunit_shop("Sue")
    # # the action
    # clean = "clean"
    # sue_agenda.add_idea(ideaunit_shop(clean, promise=True), parent_road=sue_agenda._economy_id)

    time_text = "time"
    sue_agenda.add_idea(
        idea_kid=ideaunit_shop(time_text, _begin=0, _close=140),
        parent_road=sue_agenda._economy_id,
    )
    time_road = sue_agenda.make_l1_road(time_text)
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
    sue_agenda.add_idea(age1st_idea, parent_road=time_road)
    sue_agenda.add_idea(age2nd_idea, parent_road=time_road)
    sue_agenda.add_idea(age3rd_idea, parent_road=time_road)
    sue_agenda.add_idea(age4th_idea, parent_road=time_road)
    sue_agenda.add_idea(age5th_idea, parent_road=time_road)
    sue_agenda.add_idea(age6th_idea, parent_road=time_road)
    sue_agenda.add_idea(age7th_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_agenda.set_acptfact(base=time_road, pick=time_road, open=45, nigh=45)
    lemma_dict = sue_agenda._get_lemma_acptfactunits()
    print(f"{len(lemma_dict)=}")
    print(f"{lemma_dict=}")
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[sue_agenda.make_road(time_road, age1st_text)]
    age2nd_lemma = lemma_dict[sue_agenda.make_road(time_road, age2nd_text)]
    age3rd_lemma = lemma_dict[sue_agenda.make_road(time_road, age3rd_text)]
    age4th_lemma = lemma_dict[sue_agenda.make_road(time_road, age4th_text)]
    age5th_lemma = lemma_dict[sue_agenda.make_road(time_road, age5th_text)]
    age6th_lemma = lemma_dict[sue_agenda.make_road(time_road, age6th_text)]
    age7th_lemma = lemma_dict[sue_agenda.make_road(time_road, age7th_text)]
    # assert age1st_lemma.active == False
    # assert age2nd_lemma.active == False
    # assert age3rd_lemma.active == True
    # assert age4th_lemma.active == False
    # assert age5th_lemma.active == False
    # assert age6th_lemma.active == False
    # assert age7th_lemma.active == False
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


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario2():
    sue_agenda = agendaunit_shop("Sue")
    # # the action
    # clean = "clean"
    # sue_agenda.add_idea(ideaunit_shop(clean, promise=True), parent_road=sue_agenda._economy_id)

    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    time_road = sue_agenda.make_l1_road(time_text)
    sue_agenda.add_idea(time_idea, parent_road=sue_agenda._economy_id)
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
    sue_agenda.add_idea(age1st_idea, parent_road=time_road)
    sue_agenda.add_idea(age2nd_idea, parent_road=time_road)
    sue_agenda.add_idea(age3rd_idea, parent_road=time_road)
    sue_agenda.add_idea(age4th_idea, parent_road=time_road)
    sue_agenda.add_idea(age5th_idea, parent_road=time_road)
    sue_agenda.add_idea(age6th_idea, parent_road=time_road)
    sue_agenda.add_idea(age7th_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_agenda.set_acptfact(base=time_road, pick=time_road, open=35, nigh=65)
    lemma_dict = sue_agenda._get_lemma_acptfactunits()
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[sue_agenda.make_road(time_road, age1st_text)]
    age2nd_lemma = lemma_dict[sue_agenda.make_road(time_road, age2nd_text)]
    age3rd_lemma = lemma_dict[sue_agenda.make_road(time_road, age3rd_text)]
    age4th_lemma = lemma_dict[sue_agenda.make_road(time_road, age4th_text)]
    age5th_lemma = lemma_dict[sue_agenda.make_road(time_road, age5th_text)]
    age6th_lemma = lemma_dict[sue_agenda.make_road(time_road, age6th_text)]
    age7th_lemma = lemma_dict[sue_agenda.make_road(time_road, age7th_text)]
    # assert age1st_lemma.active == False
    # assert age2nd_lemma.active == True
    # assert age3rd_lemma.active == True
    # assert age4th_lemma.active == True
    # assert age5th_lemma.active == False
    # assert age6th_lemma.active == False
    # assert age7th_lemma.active == False
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


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario3():
    sue_agenda = agendaunit_shop("Sue")
    # # the action
    # clean = "clean"
    # sue_agenda.add_idea(ideaunit_shop(clean, promise=True), parent_road=sue_agenda._economy_id)

    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    time_road = sue_agenda.make_l1_road(time_text)
    sue_agenda.add_idea(time_idea, parent_road=sue_agenda._economy_id)
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
    sue_agenda.add_idea(age1st_idea, parent_road=time_road)
    sue_agenda.add_idea(age2nd_idea, parent_road=time_road)
    sue_agenda.add_idea(age3rd_idea, parent_road=time_road)
    sue_agenda.add_idea(age4th_idea, parent_road=time_road)
    sue_agenda.add_idea(age5th_idea, parent_road=time_road)
    sue_agenda.add_idea(age6th_idea, parent_road=time_road)
    sue_agenda.add_idea(age7th_idea, parent_road=time_road)

    a2_road = sue_agenda.make_road(time_road, age2nd_text)
    a2e1st_text = "a1_era1st"
    a2e2nd_text = "a1_era2nd"
    a2e3rd_text = "a1_era3rd"
    a2e4th_text = "a1_era4th"
    a2e1st_idea = ideaunit_shop(a2e1st_text, _begin=20, _close=30)
    a2e2nd_idea = ideaunit_shop(a2e2nd_text, _begin=30, _close=34)
    a2e3rd_idea = ideaunit_shop(a2e3rd_text, _begin=34, _close=38)
    a2e4th_idea = ideaunit_shop(a2e4th_text, _begin=38, _close=40)
    sue_agenda.add_idea(a2e1st_idea, parent_road=a2_road)
    sue_agenda.add_idea(a2e2nd_idea, parent_road=a2_road)
    sue_agenda.add_idea(a2e3rd_idea, parent_road=a2_road)
    sue_agenda.add_idea(a2e4th_idea, parent_road=a2_road)

    a3_road = sue_agenda.make_road(time_road, age3rd_text)
    a3e1st_text = "a3_era1st"
    a3e2nd_text = "a3_era2nd"
    a3e3rd_text = "a3_era3rd"
    a3e4th_text = "a3_era4th"
    a3e1st_idea = ideaunit_shop(a3e1st_text, _begin=40, _close=45)
    a3e2nd_idea = ideaunit_shop(a3e2nd_text, _begin=45, _close=50)
    a3e3rd_idea = ideaunit_shop(a3e3rd_text, _begin=55, _close=58)
    a3e4th_idea = ideaunit_shop(a3e4th_text, _begin=58, _close=60)
    sue_agenda.add_idea(a3e1st_idea, parent_road=a3_road)
    sue_agenda.add_idea(a3e2nd_idea, parent_road=a3_road)
    sue_agenda.add_idea(a3e3rd_idea, parent_road=a3_road)
    sue_agenda.add_idea(a3e4th_idea, parent_road=a3_road)

    # set for instant moment in 3rd age
    sue_agenda.set_acptfact(base=time_road, pick=time_road, open=35, nigh=55)
    lemma_dict = sue_agenda._get_lemma_acptfactunits()
    assert len(lemma_dict) == 15
    a2e1st_lemma = lemma_dict[sue_agenda.make_road(a2_road, a2e1st_text)]
    a2e2nd_lemma = lemma_dict[sue_agenda.make_road(a2_road, a2e2nd_text)]
    a2e3rd_lemma = lemma_dict[sue_agenda.make_road(a2_road, a2e3rd_text)]
    a2e4th_lemma = lemma_dict[sue_agenda.make_road(a2_road, a2e4th_text)]
    a3e1st_lemma = lemma_dict[sue_agenda.make_road(a3_road, a3e1st_text)]
    a3e2nd_lemma = lemma_dict[sue_agenda.make_road(a3_road, a3e2nd_text)]
    a3e3rd_lemma = lemma_dict[sue_agenda.make_road(a3_road, a3e3rd_text)]
    a3e4th_lemma = lemma_dict[sue_agenda.make_road(a3_road, a3e4th_text)]
    # assert a2e1st_lemma.active == False
    # assert a2e2nd_lemma.active == False
    # assert a2e3rd_lemma.active == True
    # assert a2e4th_lemma.active == True
    # assert a3e1st_lemma.active == True
    # assert a3e2nd_lemma.active == True
    # assert a3e3rd_lemma.active == False
    # assert a3e4th_lemma.active == False
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


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario4():
    sue_agenda = agendaunit_shop("Sue")
    arsub1 = "descretional_subsection1"
    arsub1_idea = ideaunit_shop(arsub1, _begin=0, _close=140)
    as1_road = sue_agenda.make_l1_road(arsub1)
    sue_agenda.add_idea(arsub1_idea, sue_agenda._economy_id)
    # range-root idea has range_source_road
    time_text = "time"
    time_idea = ideaunit_shop(
        time_text, _begin=0, _close=140, _range_source_road=as1_road
    )
    sue_agenda.add_idea(time_idea, parent_road=sue_agenda._economy_id)

    arsub2 = "descretional_subsection2"
    arsub2_idea = ideaunit_shop(arsub2, _begin=0, _close=20)
    as2_road = sue_agenda.make_l1_road(arsub2)
    sue_agenda.add_idea(arsub2_idea, parent_road=sue_agenda._economy_id)

    # non-range-root child idea has range_source_road
    time_road = sue_agenda.make_l1_road(time_text)
    age1st = "age1st"
    age1st_idea = ideaunit_shop(
        age1st, _begin=0, _close=20, _range_source_road=as2_road
    )
    sue_agenda.add_idea(age1st_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_agenda.set_acptfact(base=time_road, pick=time_road, open=35, nigh=55)
    lemma_dict = sue_agenda._get_lemma_acptfactunits()
    assert len(lemma_dict) == 3
    a1_lemma = lemma_dict[sue_agenda.make_road(time_road, age1st)]
    as1_lemma = lemma_dict[as1_road]
    as2_lemma = lemma_dict[as2_road]
    # assert a1_lemma.active == False
    # assert as1_lemma.active == True
    # assert as2_lemma.active == False
    assert a1_lemma.open is None
    assert as1_lemma.open == 35
    assert as2_lemma.open is None
    assert a1_lemma.nigh is None
    assert as1_lemma.nigh == 55
    assert as2_lemma.nigh is None


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario4_1():
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")
    timetech_road = sue_agenda.make_road(time_road, "tech")
    sue_agenda.set_acptfact(jajatime_road, jajatime_road, open=1500, nigh=1500)
    lhu = sue_agenda._get_lemma_acptfactunits()

    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycle")].open == 1500
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycle")].nigh == 1500
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].open > 0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].open < 1
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].nigh > 0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].nigh < 1
    assert lhu[sue_agenda.make_road(jajatime_road, "days")].open >= 1
    assert lhu[sue_agenda.make_road(jajatime_road, "days")].open <= 2
    assert lhu[sue_agenda.make_road(jajatime_road, "days")].nigh >= 1
    assert lhu[sue_agenda.make_road(jajatime_road, "days")].nigh <= 2
    assert lhu[sue_agenda.make_road(jajatime_road, "day")].open == 60
    assert lhu[sue_agenda.make_road(jajatime_road, "day")].nigh == 60
    assert lhu[sue_agenda.make_road(jajatime_road, "week")].open == 1500
    assert int(lhu[sue_agenda.make_road(jajatime_road, "week")].nigh) == 1500
    assert lhu[sue_agenda.make_road(timetech_road, "week")].open == 1500
    assert int(lhu[sue_agenda.make_road(timetech_road, "week")].nigh) == 1500


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario5():
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    timetech_road = sue_agenda.make_road(time_road, "tech")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")
    sue_agenda.set_acptfact(jajatime_road, jajatime_road, 1500, nigh=1063954002)
    lhu = sue_agenda._get_lemma_acptfactunits()

    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycle")].open == 0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycle")].nigh == 210379680
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].open > 0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].open < 1
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].nigh > 5
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].nigh < 6
    lemma_days = lhu[sue_agenda.make_road(jajatime_road, "days")]
    assert int(lemma_days.open) == 1  # 0 / 1440
    assert int(lemma_days.nigh) == 738856  # 1063953183 / 1440
    lemma_day = lhu[sue_agenda.make_road(jajatime_road, "day")]
    assert lemma_day.open == 0  # 0 / 1440
    assert lemma_day.nigh == 1440  # 1362  # 1063953183 / 1440
    lemma_jajatime_week = lhu[sue_agenda.make_road(jajatime_road, "week")]
    assert lemma_jajatime_week.open == 0  # 0 / 1440
    assert int(lemma_jajatime_week.nigh) == 10080  # 1063953183 / 1440
    lemma_timetech_week = lhu[sue_agenda.make_road(jajatime_road, "week")]
    assert lemma_timetech_week.open == 0  # 0 / 1440
    assert int(lemma_timetech_week.nigh) == 10080  # 1063953183 / 1440


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario6():
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")
    sue_agenda.set_acptfact(jajatime_road, jajatime_road, 1063954000, nigh=1063954002)
    lhu = sue_agenda._get_lemma_acptfactunits()

    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycle")].open == 12055600.0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycle")].nigh == 12055602.0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].open > 5
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].open < 6
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].nigh > 5
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year cycles")].nigh < 6
    lemma_days = lhu[sue_agenda.make_road(jajatime_road, "days")]
    assert int(lemma_days.open) == 738856  # 1063954000 / 1440
    assert int(lemma_days.nigh) == 738856  # 1063954000 / 1440
    lemma_day = lhu[sue_agenda.make_road(jajatime_road, "day")]
    assert lemma_day.open == 1360  # 0 / 1440
    assert int(lemma_day.nigh) == 1362  # 1063953183 / 1440


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario7():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    timetech_road = sue_agenda.make_road(time_road, "tech")
    techweek_road = sue_agenda.make_road(timetech_road, "week")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")

    # WHEN given a minute range that should be Thursday to Monday midnight
    sue_agenda.set_acptfact(jajatime_road, jajatime_road, 1063951200, nigh=1063956960)
    lhu = sue_agenda._get_lemma_acptfactunits()

    # THEN
    week_open = lhu[sue_agenda.make_road(jajatime_road, "week")].open
    week_nigh = lhu[sue_agenda.make_road(jajatime_road, "week")].nigh
    week_text = "week"
    print(
        f"for {sue_agenda.make_road(jajatime_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_agenda.make_road(jajatime_road, "week")].open == 7200
    assert lhu[sue_agenda.make_road(jajatime_road, "week")].nigh == 2880

    week_open = lhu[sue_agenda.make_road(timetech_road, "week")].open
    week_nigh = lhu[sue_agenda.make_road(timetech_road, "week")].nigh
    print(
        f"for {sue_agenda.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_agenda.make_road(timetech_road, "week")].open == 7200
    assert lhu[sue_agenda.make_road(timetech_road, "week")].nigh == 2880
    print(f"{techweek_road=}")
    print(lhu[techweek_road])
    print(lhu[sue_agenda.make_road(techweek_road, "Thursday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Friday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Saturday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Sunday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Monday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Tuesday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Wednesday")])

    # assert lhu[sue_agenda.make_road(timetech_road,"week,Thursday")].active == True
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Friday")].active == True
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Saturday")].active == True
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Sunday")].active == True
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Monday")].active == False
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Tuesday")].active == False
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Wednesday")].active == False


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario8():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    timetech_road = sue_agenda.make_road(time_road, "tech")
    techweek_road = sue_agenda.make_road(timetech_road, "week")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")

    # WHEN given a minute range that should be Thursday to Monday midnight
    sue_agenda.set_acptfact(jajatime_road, jajatime_road, 1063951200, nigh=1063951200)
    lhu = sue_agenda._get_lemma_acptfactunits()

    # THEN
    week_open = lhu[techweek_road].open
    week_nigh = lhu[techweek_road].nigh
    print(f"for {techweek_road}: {week_open=} {week_nigh=}")
    assert lhu[techweek_road].open == 7200
    assert lhu[techweek_road].nigh == 7200

    week_open = lhu[sue_agenda.make_road(timetech_road, "week")].open
    week_nigh = lhu[sue_agenda.make_road(timetech_road, "week")].nigh
    week_text = "week"
    print(
        f"for {sue_agenda.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_agenda.make_road(timetech_road, "week")].open == 7200
    assert lhu[sue_agenda.make_road(timetech_road, "week")].nigh == 7200
    print(lhu[techweek_road])
    print(lhu[sue_agenda.make_road(techweek_road, "Thursday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Friday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Saturday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Sunday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Monday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Tuesday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Wednesday")])

    # assert lhu[sue_agenda.make_road(timetech_road,"week,Thursday")].active == True
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Friday")].active == False
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Saturday")].active == False
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Sunday")].active == False
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Monday")].active == False
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Tuesday")].active == False
    # assert lhu[sue_agenda.make_road(timetech_road,"week,Wednesday")].active == False


def test_agenda_set_acptfact_create_missing_ideas_CreatesBaseAndAcptFact():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    trouble_text = ""
    trouble_road = sue_agenda.make_l1_road(trouble_text)
    climate_text = "climate"
    climate_road = sue_agenda.make_road(trouble_road, climate_text)
    assert sue_agenda._idearoot.get_kid(trouble_text) is None

    # WHEN
    sue_agenda.set_acptfact(trouble_road, climate_road, create_missing_ideas=True)

    # THEN
    assert sue_agenda._idearoot.get_kid(trouble_text) != None
    assert sue_agenda.get_idea_obj(trouble_road) != None
    assert sue_agenda.get_idea_obj(climate_road) != None


def test_agenda_get_acptfactunits_base_and_acptfact_list_CorrectlyReturnsListOfAcptFactUnits():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    trouble_text = "troubles"
    trouble_road = sue_agenda.make_l1_road(trouble_text)
    climate_text = "climate"
    climate_road = sue_agenda.make_road(trouble_road, climate_text)
    sue_agenda.set_acptfact(trouble_road, climate_road, create_missing_ideas=True)

    weather_text = "weather"
    weather_road = sue_agenda.make_l1_road(weather_text)
    windy_text = "windy"
    windy_road = sue_agenda.make_road(weather_road, windy_text)
    sue_agenda.set_acptfact(weather_road, windy_road, create_missing_ideas=True)
    hot_text = "hot"
    hot_road = sue_agenda.make_road(weather_road, hot_text)
    sue_agenda.set_acptfact(base=weather_road, pick=hot_road, create_missing_ideas=True)
    cold_text = "cold"
    cold_road = sue_agenda.make_road(weather_road, cold_text)
    sue_agenda.set_acptfact(weather_road, cold_road, create_missing_ideas=True)

    games_text = "games"
    games_road = sue_agenda.make_l1_road(games_text)
    football_text = "football"
    football_road = sue_agenda.make_road(weather_road, football_text)
    sue_agenda.set_acptfact(games_road, football_road, create_missing_ideas=True)

    # WHEN
    acptfactunit_list_x = sue_agenda.get_acptfactunits_base_and_acptfact_list()

    # THEN
    assert acptfactunit_list_x[0][0] == ""
    assert acptfactunit_list_x[1][0] == games_road
    assert acptfactunit_list_x[1][1] == football_road
    assert acptfactunit_list_x[2][0] == trouble_road
    assert acptfactunit_list_x[2][1] == climate_road
    assert acptfactunit_list_x[3][0] == weather_road
    assert acptfactunit_list_x[3][1] == cold_road
    assert len(acptfactunit_list_x) == 4
