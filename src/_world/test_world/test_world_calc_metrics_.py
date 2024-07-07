from datetime import datetime
from src._road.road import RoadUnit
from src._world.world import worldunit_shop, get_from_json as worldunit_get_from_json
from src._world.idea import IdeaUnit, ideaunit_shop
from src._world.reason_idea import reasonunit_shop
from src._world.beliefunit import beliefunit_shop, fiscallink_shop
from src._world.char import charlink_shop
from src._world.reason_culture import cultureunit_shop
from src._world.examples.example_worlds import (
    get_world_with_4_levels as example_worlds_get_world_with_4_levels,
    get_world_with_4_levels_and_2reasons as example_worlds_get_world_with_4_levels_and_2reasons,
    get_world_with7amCleanTableReason as example_worlds_get_world_with7amCleanTableReason,
    get_world_with_4_levels_and_2reasons_2facts as example_worlds_get_world_with_4_levels_and_2reasons_2facts,
    world_v001 as example_worlds_world_v001,
    world_v001_with_large_agenda as example_worlds_world_v001_with_large_agenda,
    world_v002 as example_worlds_world_v002,
)


def test_WorldUnit_get_agenda_dict_ReturnsCorrectObj():
    # GIVEN
    bob_world = example_worlds_get_world_with_4_levels()

    # WHEN
    agenda_dict = bob_world.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    print(f"{agenda_dict.keys()=}")
    assert bob_world.make_l1_road("casa") in agenda_dict.keys()
    assert bob_world.make_l1_road("feed cat") in agenda_dict.keys()


def test_WorldUnit_get_agenda_dict_ReturnsAgendaWithOnlyCorrectItems():
    # GIVEN
    x_world = example_worlds_get_world_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = x_world.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_world.make_road(week_road, sun_text)
    x_world.set_fact(base=week_road, pick=sun_road)

    # WHEN
    agenda_dict = x_world.get_agenda_dict()

    # THEN
    assert agenda_dict
    # for agenda_item in agenda_dict:
    #     yr_elucidation(idea=agenda_item)
    # yr_elucidation(idea=agenda_dict[0])

    assert len(agenda_dict) == 1
    print(f"{agenda_dict=}")
    assert x_world.make_l1_road("feed cat") in agenda_dict.keys()


def test_WorldUnit_get_agenda_dict_WithLargeWorldImportance():
    # GIVEN
    x_world = example_worlds_get_world_with_4_levels_and_2reasons_2facts()

    # WHEN
    agenda_dict = x_world.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    assert agenda_dict.get(x_world.make_l1_road("feed cat"))._world_importance

    casa_text = "casa"
    print(f"{agenda_dict.keys()=} {x_world.make_l1_road(casa_text)=}")
    print(f"{agenda_dict.get(x_world.make_l1_road(casa_text))._label=}")
    assert agenda_dict.get(x_world.make_l1_road(casa_text))._world_importance


def test_WorldUnit_get_agenda_WithNo7amItemExample():
    # GIVEN
    x_world = example_worlds_get_world_with7amCleanTableReason()

    # WHEN
    agenda_dict = x_world.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    clean_text = "clean table"
    print(f"{agenda_dict.keys()=} {x_world.make_l1_road(clean_text)=}")
    # print(f"{agenda_dict[0]._label=}")
    assert len(agenda_dict) == 1

    cat_text = "feed cat"
    cat_agenda_item = agenda_dict.get(x_world.make_l1_road(cat_text))
    assert cat_agenda_item._label != clean_text


def test_WorldUnit_get_agenda_With7amItemExample():
    # GIVEN
    # set facts as midnight to 8am
    x_world = example_worlds_get_world_with7amCleanTableReason()
    print(f"{len(x_world.get_agenda_dict())=}")
    assert len(x_world.get_agenda_dict()) == 1

    # WHEN
    timetech_road = x_world.make_l1_road("timetech")
    day24hr_road = x_world.make_road(timetech_road, "24hr day")
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    housemanagement_text = "housemanagement"
    housemanagement_road = x_world.make_l1_road(housemanagement_text)
    clean_text = "clean table"
    clean_road = x_world.make_road(housemanagement_road, clean_text)
    x_world.set_fact(
        base=day24hr_road, pick=day24hr_road, open=day24hr_open, nigh=day24hr_nigh
    )
    print(x_world._idearoot._factunits[day24hr_road])
    print(x_world._idearoot._kids[housemanagement_text]._kids[clean_text]._reasonunits)
    print(x_world._idearoot._kids[housemanagement_text]._kids[clean_text]._active)

    # THEN
    agenda_dict = x_world.get_agenda_dict()
    print(f"{len(agenda_dict)=} {agenda_dict.keys()=}")
    assert len(agenda_dict) == 6
    clean_item = agenda_dict.get(clean_road)
    assert clean_item._label == clean_text


def test_WorldUnit_get_agenda_DoesNotReturnPledgeItemsOutsideRange():
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    zia_world.set_time_hreg_ideas(c400_count=7)
    clean_text = "clean"
    clean_road = zia_world.make_l1_road(clean_text)
    zia_world.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    time_road = zia_world.make_l1_road("time")
    jajatime_road = zia_world.make_road(time_road, "jajatime")
    jajaday = zia_world.make_road(jajatime_road, "day")

    zia_world.edit_idea_attr(
        road=clean_road,
        reason_base=jajatime_road,
        reason_premise=jajaday,
        begin=480,
        close=480,
    )

    open_x = 1063971180
    nigh_x1 = 2063971523
    zia_world.set_fact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x1)

    agenda_dict = zia_world.get_agenda_dict()
    print(f"{agenda_dict.keys()=}")
    assert len(agenda_dict) == 1
    assert clean_road in agenda_dict.keys()

    nigh_x2 = 1063971923
    zia_world.set_fact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x2)

    agenda_dict = zia_world.get_agenda_dict()
    assert len(agenda_dict) == 0


def test_WorldUnit_get_all_pledges_ReturnsCorrectObj():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    casa_text = "casa"
    casa_road = zia_world.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = zia_world.make_road(casa_road, clean_text)
    sweep_text = "sweep"
    sweep_road = zia_world.make_road(clean_road, sweep_text)
    couch_text = "couch"
    couch_road = zia_world.make_road(casa_road, couch_text)
    zia_world.add_idea(ideaunit_shop(couch_text), casa_road)
    zia_world.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    zia_world.add_idea(ideaunit_shop(sweep_text, pledge=True), clean_road)
    sweep_idea = zia_world.get_idea_obj(sweep_road)
    bob_text = "Bob"
    zia_world.add_charunit(bob_text)
    sweep_idea._cultureunit.set_heldbelief(bob_text)
    print(f"{sweep_idea}")
    agenda_dict = zia_world.get_agenda_dict()
    assert agenda_dict.get(clean_road) != None
    assert agenda_dict.get(sweep_road) is None
    assert agenda_dict.get(couch_road) is None

    # WHEN
    all_pledges_dict = zia_world.get_all_pledges()

    # THEN
    assert all_pledges_dict.get(sweep_road) == zia_world.get_idea_obj(sweep_road)
    assert all_pledges_dict.get(clean_road) == zia_world.get_idea_obj(clean_road)
    assert all_pledges_dict.get(couch_road) is None


def test_example_worlds_world_v001_AgendaExists():
    # GIVEN
    x_world = example_worlds_world_v001()
    min_text = "day_minute"
    min_road = x_world.make_l1_road(min_text)
    x_world.set_fact(base=min_road, pick=min_road, open=0, nigh=1399)
    assert x_world
    # for idea_kid in x_world._idearoot._kids.values():
    #     # print(idea_kid._label)
    #     assert str(type(idea_kid)) != "<class 'str'>"
    #     assert idea_kid.pledge != None

    # WHEN
    agenda_dict = x_world.get_agenda_dict()

    # THEN
    assert len(agenda_dict) > 0
    assert len(agenda_dict) == 17
    # assert agenda_dict[0].pledge != None
    # assert str(type(agenda_dict[0])) != "<class 'str'>"
    # assert str(type(agenda_dict[9])) != "<class 'str'>"
    # assert str(type(agenda_dict[12])) != "<class 'str'>"


def test_example_worlds_world_v001_WorldHasCorrectAttributes():
    # GIVEN
    x_world = example_worlds_world_v001()

    day_min_text = "day_minute"
    day_min_road = x_world.make_l1_road(day_min_text)
    x_world.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)
    month_week_text = "month_week"
    month_week_road = x_world.make_l1_road(month_week_text)
    nations_text = "Nation-States"
    nations_road = x_world.make_l1_road(nations_text)
    mood_text = "Moods"
    mood_road = x_world.make_l1_road(mood_text)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = x_world.make_l1_road(aaron_text)
    # internet_text = "Internet"
    # internet_road = x_world.make_l1_road(internet_text)
    year_month_text = "year_month"
    year_month_road = x_world.make_l1_road(year_month_text)
    x_world.set_fact(base=month_week_road, pick=month_week_road)
    x_world.set_fact(base=nations_road, pick=nations_road)
    x_world.set_fact(base=mood_road, pick=mood_road)
    x_world.set_fact(base=aaron_road, pick=aaron_road)
    # x_world.set_fact(base=internet_road, pick=internet_road)
    x_world.set_fact(base=year_month_road, pick=year_month_road)
    # season_text = "Seasons"
    # season_road = x_world.make_l1_road(season_text)
    # x_world.set_fact(base=season_road, pick=season_road)
    ced_week_text = "ced_week"
    ced_week_road = x_world.make_l1_road(ced_week_text)
    x_world.set_fact(base=ced_week_road, pick=ced_week_road)
    # water_text = "WaterExistence"
    # water_road = x_world.make_l1_road(water_text)
    # x_world.set_fact(base=water_road, pick=water_road)
    # movie_text = "No Movie playing"
    # movie_road = x_world.make_l1_road(movie_text)
    # x_world.set_fact(base=movie_road, pick=movie_text)

    # WHEN
    idea_pledge_list = x_world.get_agenda_dict()

    # THEN
    assert len(idea_pledge_list) == 27

    week1_road = x_world.make_road(month_week_road, "1st week")
    x_world.set_fact(month_week_road, week1_road)
    idea_pledge_list = x_world.get_agenda_dict()
    assert len(idea_pledge_list) == 27

    weekday_text = "weekdays"
    weekday_road = x_world.make_l1_road(weekday_text)
    monday_text = "Monday"
    monday_road = x_world.make_road(weekday_road, monday_text)

    x_world.set_fact(base=weekday_road, pick=monday_road)
    idea_pledge_list = x_world.get_agenda_dict()
    assert len(idea_pledge_list) == 39

    x_world.set_fact(base=weekday_road, pick=weekday_road)
    idea_pledge_list = x_world.get_agenda_dict()
    assert len(idea_pledge_list) == 53

    # x_world.set_fact(base=nations_road, pick=nations_road)
    # idea_pledge_list = x_world.get_agenda_dict()
    # assert len(idea_pledge_list) == 53

    # for base in x_world.get_missing_fact_bases():
    #     print(f"{base=}")

    # for agenda_item in idea_pledge_list:
    #     print(f"{agenda_item._uid=} {agenda_item._parent_road=}")

    # for agenda_item in idea_pledge_list:
    #     # print(f"{agenda_item._parent_road=}")
    #     pass

    print(len(idea_pledge_list))


def test_example_worlds_world_v001_with_large_agenda_WorldCanFiltersOnBase():
    # GIVEN
    x_world = example_worlds_world_v001_with_large_agenda()
    week_text = "weekdays"
    week_road = x_world.make_l1_road(week_text)
    print(f"{type(x_world)=}")
    # for base in x_world.get_missing_fact_bases():
    #     print(f"{base=}")

    # for agenda_item in x_world.get_agenda_dict():
    #     print(
    #         f"{agenda_item._parent_road=} {agenda_item._label} {len(agenda_item._reasonunits)=}"
    #     )
    #     for reason in agenda_item._reasonunits.values():
    #         if reason.base == weekdays:
    #             print(f"         {weekdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(x_world.get_agenda_dict()) == 63

    # WHEN
    pledge_list = x_world.get_agenda_dict(necessary_base=week_road)

    # THEN
    assert len(pledge_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(pledge_list) == 29


def test_WorldUnit_set_agenda_task_as_complete_SetsAttrCorrectly_Range():
    # GIVEN
    zia_world = worldunit_shop("Zia")

    run_text = "run"
    run_road = zia_world.make_l1_road(run_text)
    time_road = zia_world.make_l1_road("time")
    day_text = "day"
    day_road = zia_world.make_road(time_road, day_text)

    zia_world.add_l1_idea(ideaunit_shop(run_text, pledge=True))
    zia_world.add_idea(ideaunit_shop(day_text, _begin=0, _close=500), time_road)
    zia_world.edit_idea_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=25,
        reason_premise_nigh=81,
    )
    zia_world.set_fact(base=day_road, pick=day_road, open=30, nigh=87)
    zia_world.get_agenda_dict()
    run_reasonunits = zia_world._idearoot._kids[run_text]._reasonunits[day_road]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_road]._status=}")
    print(f"{run_reasonunits.premises[day_road]._task=}")
    print(f"{zia_world.get_reason_bases()=}")
    assert len(zia_world.get_idea_dict()) == 4
    assert len(zia_world.get_agenda_dict()) == 1
    print(f"{zia_world.get_agenda_dict().keys()=}")
    assert zia_world.get_agenda_dict().get(run_road)._task == True

    # WHEN
    zia_world.set_agenda_task_complete(task_road=run_road, base=day_road)

    # THEN
    agenda_dict = zia_world.get_agenda_dict()
    assert len(agenda_dict) == 0
    assert agenda_dict == {}


def test_WorldUnit_set_agenda_task_as_complete_SetsAttrCorrectly_Division():
    # GIVEN
    zia_world = worldunit_shop("Zia")

    run_text = "run"
    run_road = zia_world.make_l1_road(run_text)
    time_text = "time"
    time_road = zia_world.make_l1_road(time_text)
    day_text = "day"
    day_road = zia_world.make_road(time_road, day_text)

    zia_world.add_l1_idea(ideaunit_shop(run_text, pledge=True))
    zia_world.add_idea(ideaunit_shop(day_text, _begin=0, _close=500), time_road)
    zia_world.edit_idea_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=1,
        reason_premise_nigh=1,
        reason_premise_divisor=2,
    )

    run_idea = zia_world.get_idea_obj(run_road)
    # print(f"{run_idea._factheirs=}")
    zia_world.set_fact(base=day_road, pick=day_road, open=1, nigh=2)
    assert len(zia_world.get_agenda_dict()) == 1
    zia_world.set_fact(base=day_road, pick=day_road, open=2, nigh=2)
    assert len(zia_world.get_agenda_dict()) == 0
    zia_world.set_fact(base=day_road, pick=day_road, open=400, nigh=400)
    assert len(zia_world.get_agenda_dict()) == 0
    zia_world.set_fact(base=day_road, pick=day_road, open=401, nigh=402)
    assert len(zia_world.get_agenda_dict()) == 1
    # print(f"{run_idea._factheirs=}")
    print(f"{run_idea._factunits=}")

    # WHEN
    zia_world.set_agenda_task_complete(task_road=run_road, base=day_road)
    print(f"{run_idea._factunits=}")
    # print(f"{run_idea._factheirs=}")
    assert len(zia_world.get_agenda_dict()) == 0


def test_worldunit_get_from_json_CorrectlyLoadsPledgeFromJSON():
    # GIVEN
    x_world_json = example_worlds_world_v001().get_json()

    # WHEN
    x_world = worldunit_get_from_json(x_world_json=x_world_json)

    # THEN
    assert len(x_world.get_idea_dict()) == 253
    print(f"{len(x_world.get_idea_dict())=}")
    casa_text = "casa"
    casa_road = x_world.make_l1_road(casa_text)
    body_text = "exercise"
    body_road = x_world.make_road(casa_road, body_text)
    veg_text = "cook veggies every morning"
    veg_road = x_world.make_road(body_road, veg_text)
    veg_idea = x_world.get_idea_obj(veg_road)
    assert not veg_idea._active
    assert veg_idea.pledge

    # idea_list = x_world.get_idea_dict()
    # pledge_true_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
    #         assert idea._active in (True, False)
    #     assert idea.pledge in (True, False)
    #     # if idea._active == True:
    #     #     print(idea._label)
    #     if idea.pledge == True:
    #         pledge_true_count += 1
    #         # if idea.pledge is False:
    #         #     print(f"pledge is false {idea._label}")
    #         # for reason in idea._reasonunits.values():
    #         #     assert reason._status in (True, False)
    # assert pledge_true_count > 0

    # WHEN
    day_min_text = "day_minute"
    day_min_road = x_world.make_l1_road(day_min_text)
    x_world.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)

    # THEN
    assert len(x_world.get_agenda_dict()) > 0


def test_set_fact_WeekdayWorldItemsCorrectlyReturned():
    # GIVEN
    zia_world = worldunit_shop("Zia")
    zia_world.set_time_hreg_ideas(c400_count=7)

    things_text = "things to do"
    zia_world.add_l1_idea(ideaunit_shop(things_text))
    t_road = zia_world.make_l1_road(things_text)
    clean = "clean"
    run = "run"
    swim = "swim"
    jog = "jog"
    veg = "veg"
    lift = "lift"
    zia_world.add_idea(ideaunit_shop(clean, pledge=True), parent_road=t_road)
    zia_world.add_idea(ideaunit_shop(run, pledge=True), parent_road=t_road)
    zia_world.add_idea(ideaunit_shop(swim, pledge=True), parent_road=t_road)
    zia_world.add_idea(ideaunit_shop(jog, pledge=True), parent_road=t_road)
    zia_world.add_idea(ideaunit_shop(veg, pledge=True), parent_road=t_road)
    zia_world.add_idea(ideaunit_shop(lift, pledge=True), parent_road=t_road)
    time_text = "time"
    time_road = zia_world.make_l1_road(time_text)
    jaja_text = "jajatime"
    jaja_road = zia_world.make_road(time_road, jaja_text)
    tech_text = "tech"
    tech_road = zia_world.make_road(time_road, tech_text)
    w_road = zia_world.make_road(tech_road, "week")
    mon_road = zia_world.make_road(w_road, "Monday")
    tue_road = zia_world.make_road(w_road, "Tuesday")
    wed_road = zia_world.make_road(w_road, "Wednesday")
    thu_road = zia_world.make_road(w_road, "Thursday")
    fri_road = zia_world.make_road(w_road, "Friday")
    sat_road = zia_world.make_road(w_road, "Saturday")
    sun_road = zia_world.make_road(w_road, "Sunday")
    t_road = zia_world.make_l1_road(things_text)
    c_road = zia_world.make_road(t_road, clean)
    r_road = zia_world.make_road(t_road, run)
    s_road = zia_world.make_road(t_road, swim)
    j_road = zia_world.make_road(t_road, jog)
    v_road = zia_world.make_road(t_road, veg)
    l_road = zia_world.make_road(t_road, lift)

    zia_world.edit_idea_attr(c_road, reason_base=tue_road, reason_premise=tue_road)
    zia_world.edit_idea_attr(r_road, reason_base=wed_road, reason_premise=wed_road)
    zia_world.edit_idea_attr(s_road, reason_base=thu_road, reason_premise=thu_road)
    zia_world.edit_idea_attr(j_road, reason_base=fri_road, reason_premise=fri_road)
    zia_world.edit_idea_attr(v_road, reason_base=sat_road, reason_premise=sat_road)
    zia_world.edit_idea_attr(l_road, reason_base=sun_road, reason_premise=sun_road)

    c_idea = zia_world.get_idea_obj(c_road)
    c_reason = c_idea._reasonunits
    # for reason_y in c_reason.values():
    #     for premise_y in reason_y.premises.values():
    #         print(
    #             f"Idea: {c_idea.get_road()}  Reason: {reason_y.base} open:{premise_y.open} nigh:{premise_y.nigh} diff:{premise_y.nigh-premise_y.open}"
    #         )

    # for base, count_x in zia_world.get_reason_bases().items():
    #     print(f"Reasons: {base=} Count: {count_x}")

    mon_dt = datetime(2000, 1, 3)
    tue_dt = datetime(2000, 1, 4)
    wed_dt = datetime(2000, 1, 5)
    thu_dt = datetime(2000, 1, 6)
    fri_dt = datetime(2000, 1, 7)
    sat_dt = datetime(2000, 1, 1)
    sun_dt = datetime(2000, 1, 2)
    mon_min = zia_world.get_time_min_from_dt(dt=mon_dt)
    tue_min = zia_world.get_time_min_from_dt(dt=tue_dt)
    wed_min = zia_world.get_time_min_from_dt(dt=wed_dt)
    thu_min = zia_world.get_time_min_from_dt(dt=thu_dt)
    fri_min = zia_world.get_time_min_from_dt(dt=fri_dt)
    sat_min = zia_world.get_time_min_from_dt(dt=sat_dt)
    sun_min = zia_world.get_time_min_from_dt(dt=sun_dt)
    assert zia_world._idearoot._factunits.get(jaja_road) is None

    # WHEN
    print("\nset fact for Sunday")
    zia_world.set_fact(base=jaja_road, pick=jaja_road, open=sun_min, nigh=sun_min)
    # for fact in zia_world._idearoot._factunits.values():
    #     print(f"{fact.base=} (H: {fact.fact}) {fact.=} {fact.open=} {fact.nigh=}")

    # THEN
    assert len(zia_world._idearoot._factunits) == 7
    print(zia_world._idearoot._factunits[jaja_road])
    print(zia_world._idearoot._factunits[sat_road])
    print(zia_world._idearoot._factunits[sun_road])
    print(zia_world._idearoot._factunits[tue_road])
    print(zia_world._idearoot._factunits[wed_road])
    print(zia_world._idearoot._factunits[thu_road])
    print(zia_world._idearoot._factunits[fri_road])
    assert zia_world._idearoot._factunits[sun_road]
    assert zia_world._idearoot._factunits[sun_road].open == 1440
    assert zia_world._idearoot._factunits[sun_road].nigh == 1440

    # WHEN
    print("\nset fact for Sat through Monday")
    zia_world.set_fact(base=jaja_road, pick=jaja_road, open=sat_min, nigh=mon_min)
    # for fact in zia_world._idearoot._factunits.values():
    #     print(f"{fact.base=} (H: {fact.fact}) {fact.=} {fact.open=} {fact.nigh=}")

    # THEN
    assert zia_world._idearoot._factunits[sat_road]
    assert zia_world._idearoot._factunits[sat_road].open == 0
    assert zia_world._idearoot._factunits[sat_road].nigh == 1440
    assert zia_world._idearoot._factunits[sun_road].open == 1440
    assert zia_world._idearoot._factunits[sun_road].nigh == 2880

    # WHEN
    print("\nset facts for Sunday through Friday")
    zia_world.set_fact(base=jaja_road, pick=jaja_road, open=sun_min, nigh=fri_min)
    # for fact in zia_world._idearoot._factunits.values():
    #     print(f"{fact.base=} (H: {fact.fact}) {fact.=} {fact.open=} {fact.nigh=}")

    # THEN
    assert zia_world._idearoot._factunits[sun_road].open == 1440
    assert zia_world._idearoot._factunits[sun_road].nigh == 2880

    # # WHEN
    # print("\nset facts for 10 day stretch")
    # dayzero_dt = datetime(2010, 1, 3)
    # dayten_dt = datetime(2010, 1, 13)
    # dayzero_min = zia_world.get_time_min_from_dt(dt=dayzero_dt)
    # dayten_min = zia_world.get_time_min_from_dt(dt=dayten_dt)
    # zia_world.set_fact(jaja_road, jaja_road, open=dayzero_min, nigh=dayten_min)
    # for fact in zia_world._idearoot._factunits.values():
    #     print(f"{fact.base=} (H: {fact.fact}) {fact.=} {fact.open=} {fact.nigh=}")


def test_WorldUnit_create_agenda_item_CorrectlyCreatesAllWorldAttributes():
    # WHEN "I am cleaning the cookery since I'm in the flat and it's 8am and it's dirty and it's for my family"

    # GIVEN
    zia_world = worldunit_shop("Zia")

    zia_world.calc_world_metrics()
    assert len(zia_world._chars) == 0
    assert len(zia_world._beliefs) == 0
    assert len(zia_world._idearoot._kids) == 0

    clean_things_text = "cleaning things"
    clean_things_road = zia_world.make_l1_road(clean_things_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = zia_world.make_road(clean_things_road, clean_cookery_text)
    clean_cookery_idea = ideaunit_shop(
        _label=clean_cookery_text, _parent_road=clean_things_road
    )
    print(f"{clean_cookery_idea.get_road()=}")
    house_text = "house"
    house_road = zia_world.make_l1_road(house_text)
    cookery_room_text = "cookery room"
    cookery_room_road = zia_world.make_road(house_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = zia_world.make_road(cookery_room_road, cookery_dirty_text)

    # create gregorian timeline
    zia_world.set_time_hreg_ideas(c400_count=7)
    time_road = zia_world.make_l1_road("time")
    jajatime_road = zia_world.make_road(time_road, "jajatime")
    daytime_road = zia_world.make_road(jajatime_road, "day")
    open_8am = 480
    nigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_road)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
    clean_cookery_idea.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_road)
    daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
    clean_cookery_idea.set_reasonunit(reason=daytime_reason)

    # anna_text = "anna"
    # anna_charunit = charunit_shop(char_id=anna_text)
    # anna_charlink = charlink_shop(char_id=anna_text)
    # beto_text = "beto"
    # beto_charunit = charunit_shop(char_id=beto_text)
    # beto_charlink = charlink_shop(char_id=beto_text)

    family_text = ",family"
    # beliefunit_z = beliefunit_shop(belief_id=family_text)
    # beliefunit_z.set_charlink(charlink=anna_charlink)
    # beliefunit_z.set_charlink(charlink=beto_charlink)
    fiscallink_z = fiscallink_shop(belief_id=family_text)
    clean_cookery_idea.set_fiscallink(fiscallink=fiscallink_z)

    assert len(zia_world._chars) == 0
    assert len(zia_world._beliefs) == 0
    assert len(zia_world._idearoot._kids) == 1
    assert zia_world.get_idea_obj(daytime_road)._begin == 0
    assert zia_world.get_idea_obj(daytime_road)._close == 1440
    print(f"{clean_cookery_idea.get_road()=}")

    # GIVEN
    zia_world.set_dominate_pledge_idea(idea_kid=clean_cookery_idea)

    # THEN
    # for idea_kid in zia_world._idearoot._kids.keys():
    #     print(f"  {idea_kid=}")

    print(f"{clean_cookery_idea.get_road()=}")
    assert zia_world.get_idea_obj(clean_cookery_road) != None
    assert zia_world.get_idea_obj(clean_cookery_road)._label == clean_cookery_text
    assert zia_world.get_idea_obj(clean_cookery_road).pledge
    assert len(zia_world.get_idea_obj(clean_cookery_road)._reasonunits) == 2
    assert zia_world.get_idea_obj(clean_things_road) != None
    assert zia_world.get_idea_obj(cookery_room_road) != None
    assert zia_world.get_idea_obj(cookery_dirty_road) != None
    assert zia_world.get_idea_obj(daytime_road)._begin == 0
    assert zia_world.get_idea_obj(daytime_road)._close == 1440
    assert len(zia_world._beliefs) == 1
    assert zia_world._beliefs.get(family_text) != None
    assert zia_world._beliefs.get(family_text)._chars in (None, {})

    assert len(zia_world._idearoot._kids) == 3


def get_tasks_count(agenda_dict: dict[RoadUnit, IdeaUnit]) -> int:
    return sum(bool(x_ideaunit._task) for x_ideaunit in agenda_dict.values())


def test_Isue116Resolved_correctlySetsTaskAsTrue():
    # GIVEN
    bob_world = example_worlds_world_v002()

    assert len(bob_world.get_agenda_dict()) == 44
    time_road = bob_world.make_l1_road("time")
    jajatime_road = bob_world.make_road(time_road, "jajatime")

    # WHEN
    bob_world.set_fact(
        base=jajatime_road, pick=jajatime_road, open=1063998720, nigh=1064130373
    )
    pledge_idea_list = bob_world.get_agenda_dict()

    # THEN
    assert len(pledge_idea_list) == 66
    db_road = bob_world.make_l1_road("D&B")
    night_text = "late_night_go_to_sleep"
    night_road = bob_world.make_road(db_road, night_text)
    night_idea = bob_world._idea_dict.get(night_road)
    # for idea_x in bob_world.get_agenda_dict():
    #     # if idea_x._task != True:
    #     #     print(f"{len(pledge_idea_list)=} {idea_x._task=} {idea_x.get_road()}")
    #     if idea_x._label == night_label:
    #         night_idea = idea_x
    #         print(f"{idea_x.get_road()=}")

    print(f"\nIdea = '{night_text}' and reason '{jajatime_road}'")
    factheir_jajatime = night_idea._factheirs.get(jajatime_road)
    print(f"\n{factheir_jajatime=}")
    print(f"      {bob_world.get_jajatime_repeating_legible_text(open=1063998720)}")
    print(f"      {bob_world.get_jajatime_repeating_legible_text(open=1064130373)}")

    # for reasonheir in agenda_item._reasonheirs.values():
    #     print(f"{reasonheir.base=} {reasonheir._status=} {reasonheir._task=}")
    reasonheir_jajatime = night_idea._reasonheirs.get(jajatime_road)
    reasonheir_text = f"\nreasonheir_jajatime= '{reasonheir_jajatime.base}', status={reasonheir_jajatime._status}, task={reasonheir_jajatime._task}"
    print(reasonheir_text)

    premiseunit = reasonheir_jajatime.premises.get(jajatime_road)
    print(f"----\n {premiseunit=}")
    print(f" {premiseunit._get_task_status(factheir=factheir_jajatime)=}")
    print(f" {premiseunit._status=} , {premiseunit._is_range()=} premiseunit fails")
    print(
        f" {premiseunit._status=} , {premiseunit._is_segregate()=} premiseunit passes"
    )
    # segr_obj = premisestatusfinder_shop(
    #     premise_open=premiseunit.open,
    #     premise_nigh=premiseunit.nigh,
    #     premise_divisor=premiseunit.divisor,
    #     fact_open_full=factheir_jajatime.open,
    #     fact_nigh_full=factheir_jajatime.nigh,
    # )
    # print(
    #     f"----\n  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    # )
    # print(
    #     f"       {segr_obj.fact_open_full=}         {segr_obj.fact_nigh_full=} \tdifference:{segr_obj.fact_nigh_full-segr_obj.fact_open_full}"
    # )

    # # print(f"  {segr_obj.premise_open_trans=}  {segr_obj.premise_nigh_trans=}")
    # print(f"  {segr_obj.get_active()=}  {segr_obj.get_task_status()=}")
    assert get_tasks_count(pledge_idea_list) == 64


def test_agenda_IsSetByCultureUnit_1CharBelief():
    # GIVEN
    bob_text = "Bob"
    bob_world = worldunit_shop(bob_text)
    casa_text = "casa"
    casa_road = bob_world.make_road(bob_text, casa_text)
    bob_world.add_l1_idea(ideaunit_shop(casa_text, pledge=True))
    assert len(bob_world.get_agenda_dict()) == 1

    sue_text = "Sue"
    bob_world.add_charunit(char_id=sue_text)
    cultureunit_sue = cultureunit_shop()
    cultureunit_sue.set_heldbelief(belief_id=sue_text)
    assert len(bob_world.get_agenda_dict()) == 1

    # WHEN
    bob_world.edit_idea_attr(road=casa_road, cultureunit=cultureunit_sue)

    # THEN
    assert len(bob_world.get_agenda_dict()) == 0

    # WHEN
    bob_world.add_charunit(char_id=bob_text)
    cultureunit_bob = cultureunit_shop()
    cultureunit_bob.set_heldbelief(belief_id=bob_text)

    # WHEN
    bob_world.edit_idea_attr(road=casa_road, cultureunit=cultureunit_bob)

    # THEN
    assert len(bob_world.get_agenda_dict()) == 1

    # agenda_dict = bob_world.get_agenda_dict()
    # print(f"{agenda_dict[0]._label=}")


def test_agenda_IsSetByCultureUnit_2CharBelief():
    # GIVEN
    bob_text = "Bob"
    bob_world = worldunit_shop(bob_text)
    bob_world.add_charunit(char_id=bob_text)
    casa_text = "casa"
    casa_road = bob_world.make_road(bob_text, casa_text)
    bob_world.add_l1_idea(ideaunit_shop(casa_text, pledge=True))

    sue_text = "Sue"
    bob_world.add_charunit(char_id=sue_text)

    run_text = ",runners"
    run_belief = beliefunit_shop(belief_id=run_text)
    run_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    bob_world.set_beliefunit(y_beliefunit=run_belief)

    run_cultureunit = cultureunit_shop()
    run_cultureunit.set_heldbelief(belief_id=run_text)
    assert len(bob_world.get_agenda_dict()) == 1

    # WHEN
    bob_world.edit_idea_attr(road=casa_road, cultureunit=run_cultureunit)

    # THEN
    assert len(bob_world.get_agenda_dict()) == 0

    # WHEN
    run_belief.set_charlink(charlink=charlink_shop(char_id=bob_text))
    bob_world.set_beliefunit(y_beliefunit=run_belief)

    # THEN
    assert len(bob_world.get_agenda_dict()) == 1


def test_IdeaCore_get_agenda_dict_ReturnsCorrectObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # GIVEN
    bob_world = worldunit_shop("Bob")
    bob_world.set_time_hreg_ideas(7)

    casa_text = "casa"
    casa_road = bob_world.make_l1_road(casa_text)
    laundry_text = "do_laundry"
    laundry_road = bob_world.make_road(casa_road, laundry_text)
    bob_world.add_l1_idea(ideaunit_shop(casa_text))
    bob_world.add_idea(ideaunit_shop(laundry_text, pledge=True), casa_road)
    time_road = bob_world.make_l1_road("time")
    jajatime_road = bob_world.make_road(time_road, "jajatime")
    bob_world.edit_idea_attr(
        road=laundry_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=3420.0,
        reason_premise_nigh=3420.0,
        reason_premise_divisor=10080.0,
    )
    print("set first fact")
    bob_world.set_fact(jajatime_road, jajatime_road, 1064131200, nigh=1064135133)
    print("get 1st agenda dictionary")
    bob_agenda_dict = bob_world.get_agenda_dict()
    print(f"{bob_agenda_dict.keys()=}")
    assert bob_agenda_dict == {}

    laundry_idea = bob_world.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_factheir = laundry_idea._factheirs.get(jajatime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.nigh % 10080=}"
    # )
    # print(f"{laundry_reasonheir.base=} {laundry_premise=}")
    # for x_ideaunit in bob_world._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")

    # WHEN
    print("set 2nd fact")
    bob_world.set_fact(jajatime_road, jajatime_road, 1064131200, nigh=1064136133)
    print("get 2nd agenda dictionary")
    bob_agenda_dict = bob_world.get_agenda_dict()
    print(f"{bob_agenda_dict.keys()=}")

    laundry_idea = bob_world.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_factheir = laundry_idea._factheirs.get(jajatime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.nigh % 10080=}"
    # )
    # for x_ideaunit in bob_world._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")
    #         jaja_factheir = x_ideaunit._factheirs.get(jajatime_road)
    #         print(f"{jaja_factheir.open % 10080=}")
    #         print(f"{jaja_factheir.nigh % 10080=}")

    # THEN
    assert bob_agenda_dict == {}
