from datetime import datetime
from src._road.road import RoadUnit
from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.agenda.fact import FactUnit, factunit_shop
from src.agenda.reason_fact import reasonunit_shop
from src.agenda.idea import ideaunit_shop, balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_assign import assignedunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_with_4_levels_and_2reasons as example_agendas_get_agenda_with_4_levels_and_2reasons,
    get_agenda_with7amCleanTableReason as example_agendas_get_agenda_with7amCleanTableReason,
    get_agenda_with_4_levels_and_2reasons_2beliefs as example_agendas_get_agenda_with_4_levels_and_2reasons_2beliefs,
    agenda_v001 as example_agendas_agenda_v001,
    agenda_v001_with_large_intent as example_agendas_agenda_v001_with_large_intent,
    agenda_v002 as example_agendas_agenda_v002,
)


def test_AgendaUnit_get_intent_dict_ReturnsCorrectObj():
    # GIVEN
    bob_agenda = example_agendas_get_agenda_with_4_levels()

    # WHEN
    intent_dict = bob_agenda.get_intent_dict()

    # THEN
    assert intent_dict
    assert len(intent_dict) == 2
    print(f"{intent_dict.keys()=}")
    assert bob_agenda.make_l1_road("casa") in intent_dict.keys()
    assert bob_agenda.make_l1_road("feed cat") in intent_dict.keys()


def test_AgendaUnit_get_intent_dict_ReturnsIntentWithOnlyCorrectItems():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_agenda.make_road(week_road, sun_text)
    x_agenda.set_belief(base=week_road, pick=sun_road)

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert intent_dict
    # for intent_item in intent_dict:
    #     yr_elucidation(fact=intent_item)
    # yr_elucidation(fact=intent_dict[0])

    assert len(intent_dict) == 1
    print(f"{intent_dict=}")
    assert x_agenda.make_l1_road("feed cat") in intent_dict.keys()


def test_AgendaUnit_get_intent_dict_WithLargeAgendaImportance():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels_and_2reasons_2beliefs()

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert intent_dict
    assert len(intent_dict) == 2
    assert intent_dict.get(x_agenda.make_l1_road("feed cat"))._agenda_importance

    casa_text = "casa"
    print(f"{intent_dict.keys()=} {x_agenda.make_l1_road(casa_text)=}")
    print(f"{intent_dict.get(x_agenda.make_l1_road(casa_text))._label=}")
    assert intent_dict.get(x_agenda.make_l1_road(casa_text))._agenda_importance


def test_AgendaUnit_get_intent_WithNo7amItemExample():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with7amCleanTableReason()

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert intent_dict
    assert len(intent_dict) == 1
    clean_text = "clean table"
    print(f"{intent_dict.keys()=} {x_agenda.make_l1_road(clean_text)=}")
    # print(f"{intent_dict[0]._label=}")
    assert len(intent_dict) == 1

    cat_text = "feed cat"
    cat_intent_item = intent_dict.get(x_agenda.make_l1_road(cat_text))
    assert cat_intent_item._label != clean_text


def test_AgendaUnit_get_intent_With7amItemExample():
    # GIVEN
    # set beliefs as midnight to 8am
    x_agenda = example_agendas_get_agenda_with7amCleanTableReason()
    print(f"{len(x_agenda.get_intent_dict())=}")
    assert len(x_agenda.get_intent_dict()) == 1

    # WHEN
    timetech_road = x_agenda.make_l1_road("timetech")
    day24hr_road = x_agenda.make_road(timetech_road, "24hr day")
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    housemanagement_text = "housemanagement"
    housemanagement_road = x_agenda.make_l1_road(housemanagement_text)
    clean_text = "clean table"
    clean_road = x_agenda.make_road(housemanagement_road, clean_text)
    x_agenda.set_belief(
        base=day24hr_road, pick=day24hr_road, open=day24hr_open, nigh=day24hr_nigh
    )
    print(x_agenda._factroot._beliefunits[day24hr_road])
    print(x_agenda._factroot._kids[housemanagement_text]._kids[clean_text]._reasonunits)
    print(x_agenda._factroot._kids[housemanagement_text]._kids[clean_text]._active)

    # THEN
    intent_dict = x_agenda.get_intent_dict()
    print(f"{len(intent_dict)=} {intent_dict.keys()=}")
    assert len(intent_dict) == 6
    clean_item = intent_dict.get(clean_road)
    assert clean_item._label == clean_text


def test_AgendaUnit_get_intent_DoesNotReturnPledgeItemsOutsideRange():
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.set_time_hreg_facts(c400_count=7)
    clean_text = "clean"
    clean_road = zia_agenda.make_l1_road(clean_text)
    zia_agenda.add_l1_fact(factunit_shop(clean_text, pledge=True))
    time_road = zia_agenda.make_l1_road("time")
    jajatime_road = zia_agenda.make_road(time_road, "jajatime")
    jajaday = zia_agenda.make_road(jajatime_road, "day")

    zia_agenda.edit_fact_attr(
        road=clean_road,
        reason_base=jajatime_road,
        reason_premise=jajaday,
        begin=480,
        close=480,
    )

    open_x = 1063971180
    nigh_x1 = 2063971523
    zia_agenda.set_belief(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x1)

    intent_dict = zia_agenda.get_intent_dict()
    print(f"{intent_dict.keys()=}")
    assert len(intent_dict) == 1
    assert clean_road in intent_dict.keys()

    nigh_x2 = 1063971923
    zia_agenda.set_belief(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x2)

    intent_dict = zia_agenda.get_intent_dict()
    assert len(intent_dict) == 0


def test_AgendaUnit_get_all_pledges_ReturnsCorrectObj():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    casa_text = "casa"
    casa_road = zia_agenda.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = zia_agenda.make_road(casa_road, clean_text)
    sweep_text = "sweep"
    sweep_road = zia_agenda.make_road(clean_road, sweep_text)
    couch_text = "couch"
    couch_road = zia_agenda.make_road(casa_road, couch_text)
    zia_agenda.add_fact(factunit_shop(couch_text), casa_road)
    zia_agenda.add_fact(factunit_shop(clean_text, pledge=True), casa_road)
    zia_agenda.add_fact(factunit_shop(sweep_text, pledge=True), clean_road)
    sweep_fact = zia_agenda.get_fact_obj(sweep_road)
    bob_text = "Bob"
    zia_agenda.add_partyunit(bob_text)
    sweep_fact._assignedunit.set_suffidea(bob_text)
    print(f"{sweep_fact}")
    intent_dict = zia_agenda.get_intent_dict()
    assert intent_dict.get(clean_road) != None
    assert intent_dict.get(sweep_road) is None
    assert intent_dict.get(couch_road) is None

    # WHEN
    all_pledges_dict = zia_agenda.get_all_pledges()

    # THEN
    assert all_pledges_dict.get(sweep_road) == zia_agenda.get_fact_obj(sweep_road)
    assert all_pledges_dict.get(clean_road) == zia_agenda.get_fact_obj(clean_road)
    assert all_pledges_dict.get(couch_road) is None


def test_example_agendas_agenda_v001_IntentExists():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    min_text = "day_minute"
    min_road = x_agenda.make_l1_road(min_text)
    x_agenda.set_belief(base=min_road, pick=min_road, open=0, nigh=1399)
    assert x_agenda
    # for fact_kid in x_agenda._factroot._kids.values():
    #     # print(fact_kid._label)
    #     assert str(type(fact_kid)) != "<class 'str'>"
    #     assert fact_kid.pledge != None

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert len(intent_dict) > 0
    assert len(intent_dict) == 17
    # assert intent_dict[0].pledge != None
    # assert str(type(intent_dict[0])) != "<class 'str'>"
    # assert str(type(intent_dict[9])) != "<class 'str'>"
    # assert str(type(intent_dict[12])) != "<class 'str'>"


def test_example_agendas_agenda_v001_AgendaHasCorrectAttributes():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()

    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=1399)
    month_week_text = "month_week"
    month_week_road = x_agenda.make_l1_road(month_week_text)
    nations_text = "Nation-States"
    nations_road = x_agenda.make_l1_road(nations_text)
    mood_text = "Moods"
    mood_road = x_agenda.make_l1_road(mood_text)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = x_agenda.make_l1_road(aaron_text)
    # internet_text = "Internet"
    # internet_road = x_agenda.make_l1_road(internet_text)
    year_month_text = "year_month"
    year_month_road = x_agenda.make_l1_road(year_month_text)
    x_agenda.set_belief(base=month_week_road, pick=month_week_road)
    x_agenda.set_belief(base=nations_road, pick=nations_road)
    x_agenda.set_belief(base=mood_road, pick=mood_road)
    x_agenda.set_belief(base=aaron_road, pick=aaron_road)
    # x_agenda.set_belief(base=internet_road, pick=internet_road)
    x_agenda.set_belief(base=year_month_road, pick=year_month_road)
    # season_text = "Seasons"
    # season_road = x_agenda.make_l1_road(season_text)
    # x_agenda.set_belief(base=season_road, pick=season_road)
    ced_week_text = "ced_week"
    ced_week_road = x_agenda.make_l1_road(ced_week_text)
    x_agenda.set_belief(base=ced_week_road, pick=ced_week_road)
    # water_text = "WaterExistence"
    # water_road = x_agenda.make_l1_road(water_text)
    # x_agenda.set_belief(base=water_road, pick=water_road)
    # movie_text = "No Movie playing"
    # movie_road = x_agenda.make_l1_road(movie_text)
    # x_agenda.set_belief(base=movie_road, pick=movie_text)

    # WHEN
    fact_action_list = x_agenda.get_intent_dict()

    # THEN
    assert len(fact_action_list) == 27

    week1_road = x_agenda.make_road(month_week_road, "1st week")
    x_agenda.set_belief(month_week_road, week1_road)
    fact_action_list = x_agenda.get_intent_dict()
    assert len(fact_action_list) == 27

    weekday_text = "weekdays"
    weekday_road = x_agenda.make_l1_road(weekday_text)
    monday_text = "Monday"
    monday_road = x_agenda.make_road(weekday_road, monday_text)

    x_agenda.set_belief(base=weekday_road, pick=monday_road)
    fact_action_list = x_agenda.get_intent_dict()
    assert len(fact_action_list) == 39

    x_agenda.set_belief(base=weekday_road, pick=weekday_road)
    fact_action_list = x_agenda.get_intent_dict()
    assert len(fact_action_list) == 53

    # x_agenda.set_belief(base=nations_road, pick=nations_road)
    # fact_action_list = x_agenda.get_intent_dict()
    # assert len(fact_action_list) == 53

    # for base in x_agenda.get_missing_belief_bases():
    #     print(f"{base=}")

    # for intent_item in fact_action_list:
    #     print(f"{intent_item._uid=} {intent_item._parent_road=}")

    # for intent_item in fact_action_list:
    #     # print(f"{intent_item._parent_road=}")
    #     pass

    print(len(fact_action_list))


def test_example_agendas_agenda_v001_with_large_intent_AgendaCanFiltersOnBase():
    # GIVEN
    x_agenda = example_agendas_agenda_v001_with_large_intent()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    print(f"{type(x_agenda)=}")
    # for base in x_agenda.get_missing_belief_bases():
    #     print(f"{base=}")

    # for intent_item in x_agenda.get_intent_dict():
    #     print(
    #         f"{intent_item._parent_road=} {intent_item._label} {len(intent_item._reasonunits)=}"
    #     )
    #     for reason in intent_item._reasonunits.values():
    #         if reason.base == weekdays:
    #             print(f"         {weekdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(x_agenda.get_intent_dict()) == 63

    # WHEN
    action_list = x_agenda.get_intent_dict(base=week_road)

    # THEN
    assert len(action_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(action_list) == 29


def test_AgendaUnit_set_intent_task_as_complete_SetsAttrCorrectly_Range():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    run_text = "run"
    run_road = zia_agenda.make_l1_road(run_text)
    time_road = zia_agenda.make_l1_road("time")
    day_text = "day"
    day_road = zia_agenda.make_road(time_road, day_text)

    zia_agenda.add_l1_fact(factunit_shop(run_text, pledge=True))
    zia_agenda.add_fact(factunit_shop(day_text, _begin=0, _close=500), time_road)
    zia_agenda.edit_fact_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=25,
        reason_premise_nigh=81,
    )
    zia_agenda.set_belief(base=day_road, pick=day_road, open=30, nigh=87)
    zia_agenda.get_intent_dict()
    run_reasonunits = zia_agenda._factroot._kids[run_text]._reasonunits[day_road]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_road]._status=}")
    print(f"{run_reasonunits.premises[day_road]._task=}")
    print(f"{zia_agenda.get_reason_bases()=}")
    assert len(zia_agenda.get_fact_dict()) == 4
    assert len(zia_agenda.get_intent_dict()) == 1
    print(f"{zia_agenda.get_intent_dict().keys()=}")
    assert zia_agenda.get_intent_dict().get(run_road)._task == True

    # WHEN
    zia_agenda.set_intent_task_complete(task_road=run_road, base=day_road)

    # THEN
    intent_dict = zia_agenda.get_intent_dict()
    assert len(intent_dict) == 0
    assert intent_dict == {}


def test_AgendaUnit_set_intent_task_as_complete_SetsAttrCorrectly_Division():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    run_text = "run"
    run_road = zia_agenda.make_l1_road(run_text)
    time_text = "time"
    time_road = zia_agenda.make_l1_road(time_text)
    day_text = "day"
    day_road = zia_agenda.make_road(time_road, day_text)

    zia_agenda.add_l1_fact(factunit_shop(run_text, pledge=True))
    zia_agenda.add_fact(factunit_shop(day_text, _begin=0, _close=500), time_road)
    zia_agenda.edit_fact_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=1,
        reason_premise_nigh=1,
        reason_premise_divisor=2,
    )

    run_fact = zia_agenda.get_fact_obj(run_road)
    # print(f"{run_fact._beliefheirs=}")
    zia_agenda.set_belief(base=day_road, pick=day_road, open=1, nigh=2)
    assert len(zia_agenda.get_intent_dict()) == 1
    zia_agenda.set_belief(base=day_road, pick=day_road, open=2, nigh=2)
    assert len(zia_agenda.get_intent_dict()) == 0
    zia_agenda.set_belief(base=day_road, pick=day_road, open=400, nigh=400)
    assert len(zia_agenda.get_intent_dict()) == 0
    zia_agenda.set_belief(base=day_road, pick=day_road, open=401, nigh=402)
    assert len(zia_agenda.get_intent_dict()) == 1
    # print(f"{run_fact._beliefheirs=}")
    print(f"{run_fact._beliefunits=}")

    # WHEN
    zia_agenda.set_intent_task_complete(task_road=run_road, base=day_road)
    print(f"{run_fact._beliefunits=}")
    # print(f"{run_fact._beliefheirs=}")
    assert len(zia_agenda.get_intent_dict()) == 0


def test_agendaunit_get_from_json_CorrectlyLoadsActionFromJSON():
    # GIVEN
    x_agenda_json = example_agendas_agenda_v001().get_json()

    # WHEN
    x_agenda = agendaunit_get_from_json(x_agenda_json=x_agenda_json)

    # THEN
    assert len(x_agenda.get_fact_dict()) == 253
    print(f"{len(x_agenda.get_fact_dict())=}")
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    body_text = "exercise"
    body_road = x_agenda.make_road(casa_road, body_text)
    veg_text = "cook veggies every morning"
    veg_road = x_agenda.make_road(body_road, veg_text)
    veg_fact = x_agenda.get_fact_obj(veg_road)
    assert not veg_fact._active
    assert veg_fact.pledge

    # fact_list = x_agenda.get_fact_dict()
    # action_true_count = 0
    # for fact in fact_list:
    #     if str(type(fact)).find(".fact.FactUnit'>") > 0:
    #         assert fact._active in (True, False)
    #     assert fact.pledge in (True, False)
    #     # if fact._active == True:
    #     #     print(fact._label)
    #     if fact.pledge == True:
    #         action_true_count += 1
    #         # if fact.pledge is False:
    #         #     print(f"action is false {fact._label}")
    #         # for reason in fact._reasonunits.values():
    #         #     assert reason._status in (True, False)
    # assert action_true_count > 0

    # WHEN
    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=1399)

    # THEN
    assert len(x_agenda.get_intent_dict()) > 0


def test_set_belief_WeekdayAgendaItemsCorrectlyReturned():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")
    zia_agenda.set_time_hreg_facts(c400_count=7)

    things_text = "things to do"
    zia_agenda.add_l1_fact(factunit_shop(things_text))
    t_road = zia_agenda.make_l1_road(things_text)
    clean = "clean"
    run = "run"
    swim = "swim"
    jog = "jog"
    veg = "veg"
    lift = "lift"
    zia_agenda.add_fact(factunit_shop(clean, pledge=True), parent_road=t_road)
    zia_agenda.add_fact(factunit_shop(run, pledge=True), parent_road=t_road)
    zia_agenda.add_fact(factunit_shop(swim, pledge=True), parent_road=t_road)
    zia_agenda.add_fact(factunit_shop(jog, pledge=True), parent_road=t_road)
    zia_agenda.add_fact(factunit_shop(veg, pledge=True), parent_road=t_road)
    zia_agenda.add_fact(factunit_shop(lift, pledge=True), parent_road=t_road)
    time_text = "time"
    time_road = zia_agenda.make_l1_road(time_text)
    jaja_text = "jajatime"
    jaja_road = zia_agenda.make_road(time_road, jaja_text)
    tech_text = "tech"
    tech_road = zia_agenda.make_road(time_road, tech_text)
    w_road = zia_agenda.make_road(tech_road, "week")
    mon_road = zia_agenda.make_road(w_road, "Monday")
    tue_road = zia_agenda.make_road(w_road, "Tuesday")
    wed_road = zia_agenda.make_road(w_road, "Wednesday")
    thu_road = zia_agenda.make_road(w_road, "Thursday")
    fri_road = zia_agenda.make_road(w_road, "Friday")
    sat_road = zia_agenda.make_road(w_road, "Saturday")
    sun_road = zia_agenda.make_road(w_road, "Sunday")
    t_road = zia_agenda.make_l1_road(things_text)
    c_road = zia_agenda.make_road(t_road, clean)
    r_road = zia_agenda.make_road(t_road, run)
    s_road = zia_agenda.make_road(t_road, swim)
    j_road = zia_agenda.make_road(t_road, jog)
    v_road = zia_agenda.make_road(t_road, veg)
    l_road = zia_agenda.make_road(t_road, lift)

    zia_agenda.edit_fact_attr(c_road, reason_base=tue_road, reason_premise=tue_road)
    zia_agenda.edit_fact_attr(r_road, reason_base=wed_road, reason_premise=wed_road)
    zia_agenda.edit_fact_attr(s_road, reason_base=thu_road, reason_premise=thu_road)
    zia_agenda.edit_fact_attr(j_road, reason_base=fri_road, reason_premise=fri_road)
    zia_agenda.edit_fact_attr(v_road, reason_base=sat_road, reason_premise=sat_road)
    zia_agenda.edit_fact_attr(l_road, reason_base=sun_road, reason_premise=sun_road)

    c_fact = zia_agenda.get_fact_obj(c_road)
    c_reason = c_fact._reasonunits
    # for reason_y in c_reason.values():
    #     for premise_y in reason_y.premises.values():
    #         print(
    #             f"Fact: {c_fact.get_road()}  Reason: {reason_y.base} open:{premise_y.open} nigh:{premise_y.nigh} diff:{premise_y.nigh-premise_y.open}"
    #         )

    # for base, count_x in zia_agenda.get_reason_bases().items():
    #     print(f"Reasons: {base=} Count: {count_x}")

    mon_dt = datetime(2000, 1, 3)
    tue_dt = datetime(2000, 1, 4)
    wed_dt = datetime(2000, 1, 5)
    thu_dt = datetime(2000, 1, 6)
    fri_dt = datetime(2000, 1, 7)
    sat_dt = datetime(2000, 1, 1)
    sun_dt = datetime(2000, 1, 2)
    mon_min = zia_agenda.get_time_min_from_dt(dt=mon_dt)
    tue_min = zia_agenda.get_time_min_from_dt(dt=tue_dt)
    wed_min = zia_agenda.get_time_min_from_dt(dt=wed_dt)
    thu_min = zia_agenda.get_time_min_from_dt(dt=thu_dt)
    fri_min = zia_agenda.get_time_min_from_dt(dt=fri_dt)
    sat_min = zia_agenda.get_time_min_from_dt(dt=sat_dt)
    sun_min = zia_agenda.get_time_min_from_dt(dt=sun_dt)
    assert zia_agenda._factroot._beliefunits.get(jaja_road) is None

    # WHEN
    print("\nset belief for Sunday")
    zia_agenda.set_belief(base=jaja_road, pick=jaja_road, open=sun_min, nigh=sun_min)
    # for belief in zia_agenda._factroot._beliefunits.values():
    #     print(f"{belief.base=} (H: {belief.belief}) {belief.=} {belief.open=} {belief.nigh=}")

    # THEN
    assert len(zia_agenda._factroot._beliefunits) == 7
    print(zia_agenda._factroot._beliefunits[jaja_road])
    print(zia_agenda._factroot._beliefunits[sat_road])
    print(zia_agenda._factroot._beliefunits[sun_road])
    print(zia_agenda._factroot._beliefunits[tue_road])
    print(zia_agenda._factroot._beliefunits[wed_road])
    print(zia_agenda._factroot._beliefunits[thu_road])
    print(zia_agenda._factroot._beliefunits[fri_road])
    assert zia_agenda._factroot._beliefunits[sun_road]
    assert zia_agenda._factroot._beliefunits[sun_road].open == 1440
    assert zia_agenda._factroot._beliefunits[sun_road].nigh == 1440

    # WHEN
    print("\nset belief for Sat through Monday")
    zia_agenda.set_belief(base=jaja_road, pick=jaja_road, open=sat_min, nigh=mon_min)
    # for belief in zia_agenda._factroot._beliefunits.values():
    #     print(f"{belief.base=} (H: {belief.belief}) {belief.=} {belief.open=} {belief.nigh=}")

    # THEN
    assert zia_agenda._factroot._beliefunits[sat_road]
    assert zia_agenda._factroot._beliefunits[sat_road].open == 0
    assert zia_agenda._factroot._beliefunits[sat_road].nigh == 1440
    assert zia_agenda._factroot._beliefunits[sun_road].open == 1440
    assert zia_agenda._factroot._beliefunits[sun_road].nigh == 2880

    # WHEN
    print("\nset beliefs for Sunday through Friday")
    zia_agenda.set_belief(base=jaja_road, pick=jaja_road, open=sun_min, nigh=fri_min)
    # for belief in zia_agenda._factroot._beliefunits.values():
    #     print(f"{belief.base=} (H: {belief.belief}) {belief.=} {belief.open=} {belief.nigh=}")

    # THEN
    assert zia_agenda._factroot._beliefunits[sun_road].open == 1440
    assert zia_agenda._factroot._beliefunits[sun_road].nigh == 2880

    # # WHEN
    # print("\nset beliefs for 10 day stretch")
    # dayzero_dt = datetime(2010, 1, 3)
    # dayten_dt = datetime(2010, 1, 13)
    # dayzero_min = zia_agenda.get_time_min_from_dt(dt=dayzero_dt)
    # dayten_min = zia_agenda.get_time_min_from_dt(dt=dayten_dt)
    # zia_agenda.set_belief(jaja_road, jaja_road, open=dayzero_min, nigh=dayten_min)
    # for belief in zia_agenda._factroot._beliefunits.values():
    #     print(f"{belief.base=} (H: {belief.belief}) {belief.=} {belief.open=} {belief.nigh=}")


def test_AgendaUnit_create_intent_item_CorrectlyCreatesAllAgendaAttributes():
    # WHEN "I am cleaning the cookery since I'm in the apartment and it's 8am and it's dirty and I'm doing this for my family"

    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    zia_agenda.calc_agenda_metrics()
    assert len(zia_agenda._partys) == 0
    assert len(zia_agenda._ideas) == 0
    assert len(zia_agenda._factroot._kids) == 0

    clean_things_text = "cleaning things"
    clean_things_road = zia_agenda.make_l1_road(clean_things_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = zia_agenda.make_road(clean_things_road, clean_cookery_text)
    clean_cookery_fact = factunit_shop(
        _label=clean_cookery_text, _parent_road=clean_things_road
    )
    print(f"{clean_cookery_fact.get_road()=}")
    house_text = "house"
    house_road = zia_agenda.make_l1_road(house_text)
    cookery_room_text = "cookery room"
    cookery_room_road = zia_agenda.make_road(house_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = zia_agenda.make_road(cookery_room_road, cookery_dirty_text)

    # create gregorian timeline
    zia_agenda.set_time_hreg_facts(c400_count=7)
    time_road = zia_agenda.make_l1_road("time")
    jajatime_road = zia_agenda.make_road(time_road, "jajatime")
    daytime_road = zia_agenda.make_road(jajatime_road, "day")
    open_8am = 480
    nigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_road)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
    clean_cookery_fact.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_road)
    daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
    clean_cookery_fact.set_reasonunit(reason=daytime_reason)

    # anna_text = "anna"
    # anna_partyunit = partyunit_shop(party_id=anna_text)
    # anna_partylink = partylink_shop(party_id=anna_text)
    # beto_text = "beto"
    # beto_partyunit = partyunit_shop(party_id=beto_text)
    # beto_partylink = partylink_shop(party_id=beto_text)

    family_text = ",family"
    # ideaunit_z = ideaunit_shop(idea_id=family_text)
    # ideaunit_z.set_partylink(partylink=anna_partylink)
    # ideaunit_z.set_partylink(partylink=beto_partylink)
    balancelink_z = balancelink_shop(idea_id=family_text)
    clean_cookery_fact.set_balancelink(balancelink=balancelink_z)

    assert len(zia_agenda._partys) == 0
    assert len(zia_agenda._ideas) == 0
    assert len(zia_agenda._factroot._kids) == 1
    assert zia_agenda.get_fact_obj(daytime_road)._begin == 0
    assert zia_agenda.get_fact_obj(daytime_road)._close == 1440
    print(f"{clean_cookery_fact.get_road()=}")

    # GIVEN
    zia_agenda.set_dominate_pledge_fact(fact_kid=clean_cookery_fact)

    # THEN
    # for fact_kid in zia_agenda._factroot._kids.keys():
    #     print(f"  {fact_kid=}")

    print(f"{clean_cookery_fact.get_road()=}")
    assert zia_agenda.get_fact_obj(clean_cookery_road) != None
    assert zia_agenda.get_fact_obj(clean_cookery_road)._label == clean_cookery_text
    assert zia_agenda.get_fact_obj(clean_cookery_road).pledge
    assert len(zia_agenda.get_fact_obj(clean_cookery_road)._reasonunits) == 2
    assert zia_agenda.get_fact_obj(clean_things_road) != None
    assert zia_agenda.get_fact_obj(cookery_room_road) != None
    assert zia_agenda.get_fact_obj(cookery_dirty_road) != None
    assert zia_agenda.get_fact_obj(daytime_road)._begin == 0
    assert zia_agenda.get_fact_obj(daytime_road)._close == 1440
    assert len(zia_agenda._ideas) == 1
    assert zia_agenda._ideas.get(family_text) != None
    assert zia_agenda._ideas.get(family_text)._partys in (None, {})

    assert len(zia_agenda._factroot._kids) == 3


def get_tasks_count(intent_dict: dict[RoadUnit:FactUnit]) -> int:
    return sum(bool(x_factunit._task) for x_factunit in intent_dict.values())


def test_Isue116Resolved_correctlySetsTaskAsTrue():
    # GIVEN
    bob_agenda = example_agendas_agenda_v002()

    assert len(bob_agenda.get_intent_dict()) == 44
    time_road = bob_agenda.make_l1_road("time")
    jajatime_road = bob_agenda.make_road(time_road, "jajatime")

    # WHEN
    bob_agenda.set_belief(
        base=jajatime_road, pick=jajatime_road, open=1063998720, nigh=1064130373
    )
    action_fact_list = bob_agenda.get_intent_dict()

    # THEN
    assert len(action_fact_list) == 66
    db_road = bob_agenda.make_l1_road("D&B")
    night_text = "late_night_go_to_sleep"
    night_road = bob_agenda.make_road(db_road, night_text)
    night_fact = bob_agenda._fact_dict.get(night_road)
    # for fact_x in bob_agenda.get_intent_dict():
    #     # if fact_x._task != True:
    #     #     print(f"{len(action_fact_list)=} {fact_x._task=} {fact_x.get_road()}")
    #     if fact_x._label == night_label:
    #         night_fact = fact_x
    #         print(f"{fact_x.get_road()=}")

    print(f"\nFact = '{night_text}' and reason '{jajatime_road}'")
    beliefheir_jajatime = night_fact._beliefheirs.get(jajatime_road)
    print(f"\n{beliefheir_jajatime=}")
    print(f"      {bob_agenda.get_jajatime_repeating_legible_text(open=1063998720)}")
    print(f"      {bob_agenda.get_jajatime_repeating_legible_text(open=1064130373)}")

    # for reasonheir in intent_item._reasonheirs.values():
    #     print(f"{reasonheir.base=} {reasonheir._status=} {reasonheir._task=}")
    reasonheir_jajatime = night_fact._reasonheirs.get(jajatime_road)
    reasonheir_text = f"\nreasonheir_jajatime= '{reasonheir_jajatime.base}', status={reasonheir_jajatime._status}, task={reasonheir_jajatime._task}"
    print(reasonheir_text)

    premiseunit = reasonheir_jajatime.premises.get(jajatime_road)
    print(f"----\n {premiseunit=}")
    print(f" {premiseunit._get_task_status(beliefheir=beliefheir_jajatime)=}")
    print(f" {premiseunit._status=} , {premiseunit._is_range()=} premiseunit fails")
    print(
        f" {premiseunit._status=} , {premiseunit._is_segregate()=} premiseunit passes"
    )
    # segr_obj = premisestatusfinder_shop(
    #     premise_open=premiseunit.open,
    #     premise_nigh=premiseunit.nigh,
    #     premise_divisor=premiseunit.divisor,
    #     belief_open_full=beliefheir_jajatime.open,
    #     belief_nigh_full=beliefheir_jajatime.nigh,
    # )
    # print(
    #     f"----\n  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    # )
    # print(
    #     f"       {segr_obj.belief_open_full=}         {segr_obj.belief_nigh_full=} \tdifference:{segr_obj.belief_nigh_full-segr_obj.belief_open_full}"
    # )

    # # print(f"  {segr_obj.premise_open_trans=}  {segr_obj.premise_nigh_trans=}")
    # print(f"  {segr_obj.get_active()=}  {segr_obj.get_task_status()=}")
    assert get_tasks_count(action_fact_list) == 64


def test_intent_IsSetByAssignedUnit_1PartyIdea():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)
    casa_text = "casa"
    casa_road = bob_agenda.make_road(bob_text, casa_text)
    bob_agenda.add_l1_fact(factunit_shop(casa_text, pledge=True))
    assert len(bob_agenda.get_intent_dict()) == 1

    sue_text = "Sue"
    bob_agenda.add_partyunit(party_id=sue_text)
    assignedunit_sue = assignedunit_shop()
    assignedunit_sue.set_suffidea(idea_id=sue_text)
    assert len(bob_agenda.get_intent_dict()) == 1

    # WHEN
    bob_agenda.edit_fact_attr(road=casa_road, assignedunit=assignedunit_sue)

    # THEN
    assert len(bob_agenda.get_intent_dict()) == 0

    # WHEN
    bob_agenda.add_partyunit(party_id=bob_text)
    assignedunit_bob = assignedunit_shop()
    assignedunit_bob.set_suffidea(idea_id=bob_text)

    # WHEN
    bob_agenda.edit_fact_attr(road=casa_road, assignedunit=assignedunit_bob)

    # THEN
    assert len(bob_agenda.get_intent_dict()) == 1

    # intent_dict = bob_agenda.get_intent_dict()
    # print(f"{intent_dict[0]._label=}")


def test_intent_IsSetByAssignedUnit_2PartyIdea():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)
    bob_agenda.add_partyunit(party_id=bob_text)
    casa_text = "casa"
    casa_road = bob_agenda.make_road(bob_text, casa_text)
    bob_agenda.add_l1_fact(factunit_shop(casa_text, pledge=True))

    sue_text = "Sue"
    bob_agenda.add_partyunit(party_id=sue_text)

    run_text = ",runners"
    run_idea = ideaunit_shop(idea_id=run_text)
    run_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    bob_agenda.set_ideaunit(y_ideaunit=run_idea)

    run_assignedunit = assignedunit_shop()
    run_assignedunit.set_suffidea(idea_id=run_text)
    assert len(bob_agenda.get_intent_dict()) == 1

    # WHEN
    bob_agenda.edit_fact_attr(road=casa_road, assignedunit=run_assignedunit)

    # THEN
    assert len(bob_agenda.get_intent_dict()) == 0

    # WHEN
    run_idea.set_partylink(partylink=partylink_shop(party_id=bob_text))
    bob_agenda.set_ideaunit(y_ideaunit=run_idea)

    # THEN
    assert len(bob_agenda.get_intent_dict()) == 1


def test_FactCore_get_intent_dict_ReturnsCorrectObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    bob_agenda.set_time_hreg_facts(7)

    casa_text = "casa"
    casa_road = bob_agenda.make_l1_road(casa_text)
    laundry_text = "do_laundry"
    laundry_road = bob_agenda.make_road(casa_road, laundry_text)
    bob_agenda.add_l1_fact(factunit_shop(casa_text))
    bob_agenda.add_fact(factunit_shop(laundry_text, pledge=True), casa_road)
    time_road = bob_agenda.make_l1_road("time")
    jajatime_road = bob_agenda.make_road(time_road, "jajatime")
    bob_agenda.edit_fact_attr(
        road=laundry_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=3420.0,
        reason_premise_nigh=3420.0,
        reason_premise_divisor=10080.0,
    )
    print("set first belief")
    bob_agenda.set_belief(jajatime_road, jajatime_road, 1064131200, nigh=1064135133)
    print("get 1st intent dictionary")
    bob_intent_dict = bob_agenda.get_intent_dict()
    print(f"{bob_intent_dict.keys()=}")
    assert bob_intent_dict == {}

    laundry_fact = bob_agenda.get_fact_obj(laundry_road)
    laundry_reasonheir = laundry_fact.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_beliefheir = laundry_fact._beliefheirs.get(jajatime_road)
    # print(
    #     f"{laundry_fact._active=} {laundry_premise.open=} {laundry_beliefheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_fact._active=} {laundry_premise.nigh=} {laundry_beliefheir.nigh % 10080=}"
    # )
    # print(f"{laundry_reasonheir.base=} {laundry_premise=}")
    # for x_factunit in bob_agenda._fact_dict.values():
    #     if x_factunit._label in [laundry_text]:
    #         print(f"{x_factunit._label=} {x_factunit._begin=} {x_factunit._close=}")
    #         print(f"{x_factunit._kids.keys()=}")

    # WHEN
    print("set 2nd belief")
    bob_agenda.set_belief(jajatime_road, jajatime_road, 1064131200, nigh=1064136133)
    print("get 2nd intent dictionary")
    bob_intent_dict = bob_agenda.get_intent_dict()
    print(f"{bob_intent_dict.keys()=}")

    laundry_fact = bob_agenda.get_fact_obj(laundry_road)
    laundry_reasonheir = laundry_fact.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_beliefheir = laundry_fact._beliefheirs.get(jajatime_road)
    # print(
    #     f"{laundry_fact._active=} {laundry_premise.open=} {laundry_beliefheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_fact._active=} {laundry_premise.nigh=} {laundry_beliefheir.nigh % 10080=}"
    # )
    # for x_factunit in bob_agenda._fact_dict.values():
    #     if x_factunit._label in [laundry_text]:
    #         print(f"{x_factunit._label=} {x_factunit._begin=} {x_factunit._close=}")
    #         print(f"{x_factunit._kids.keys()=}")
    #         jaja_beliefheir = x_factunit._beliefheirs.get(jajatime_road)
    #         print(f"{jaja_beliefheir.open % 10080=}")
    #         print(f"{jaja_beliefheir.nigh % 10080=}")

    # THEN
    assert bob_intent_dict == {}
