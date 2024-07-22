from datetime import datetime
from src._road.road import RoadUnit
from src.bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.bud.idea import IdeaUnit, ideaunit_shop
from src.bud.reason_idea import reasonunit_shop
from src.bud.group import awardlink_shop
from src.bud.reason_doer import doerunit_shop
from src.bud.examples.example_buds import (
    get_budunit_1Task_1CE0MinutesReason_1Fact,
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_with7amCleanTableReason,
    get_budunit_with_4_levels_and_2reasons_2facts,
    budunit_v001,
    budunit_v001_with_large_agenda,
    budunit_v002,
)
from src.bud.examples.example_time import get_budunit_sue_TimeExample


def get_tasks_count(agenda_dict: dict[RoadUnit, IdeaUnit]) -> int:
    return sum(bool(x_ideaunit._task) for x_ideaunit in agenda_dict.values())


def test_BudUnit_get_agenda_dict_ReturnsCorrectObj():
    # ESTABLISH
    yao_bud = get_budunit_with_4_levels()

    # WHEN
    agenda_dict = yao_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    print(f"{agenda_dict.keys()=}")
    assert yao_bud.make_l1_road("casa") in agenda_dict.keys()
    assert yao_bud.make_l1_road("cat have dinner") in agenda_dict.keys()


def test_BudUnit_get_agenda_dict_ReturnsAgendaWithOnlyCorrectItems():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = x_bud.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_bud.make_road(week_road, sun_text)
    x_bud.set_fact(base=week_road, pick=sun_road)

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    # for agenda_item in agenda_dict:
    #     yr_elucidation(idea=agenda_item)
    # yr_elucidation(idea=agenda_dict[0])

    assert len(agenda_dict) == 1
    print(f"{agenda_dict=}")
    assert x_bud.make_l1_road("cat have dinner") in agenda_dict.keys()


def test_BudUnit_get_agenda_dict_WithLargeBud_fund():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels_and_2reasons_2facts()

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    assert agenda_dict.get(x_bud.make_l1_road("cat have dinner"))._fund_ratio

    casa_text = "casa"
    print(f"{agenda_dict.keys()=} {x_bud.make_l1_road(casa_text)=}")
    print(f"{agenda_dict.get(x_bud.make_l1_road(casa_text))._label=}")
    assert agenda_dict.get(x_bud.make_l1_road(casa_text))._fund_ratio


def test_BudUnit_get_agenda_dict_WithNo7amItemExample():
    # ESTABLISH
    x_bud = get_budunit_with7amCleanTableReason()

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    clean_text = "clean table"
    print(f"{agenda_dict.keys()=} {x_bud.make_l1_road(clean_text)=}")
    # print(f"{agenda_dict[0]._label=}")
    assert len(agenda_dict) == 1

    cat_text = "cat have dinner"
    cat_agenda_item = agenda_dict.get(x_bud.make_l1_road(cat_text))
    assert cat_agenda_item._label != clean_text


def test_BudUnit_get_agenda_dict_With7amItemExample():
    # ESTABLISH
    # set facts as midnight to 8am
    x_bud = get_budunit_with7amCleanTableReason()
    print(f"{len(x_bud.get_agenda_dict())=}")
    assert len(x_bud.get_agenda_dict()) == 1
    timetech_road = x_bud.make_l1_road("timetech")
    day24hr_road = x_bud.make_road(timetech_road, "24hr day")
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    housemanagement_text = "housemanagement"
    housemanagement_road = x_bud.make_l1_road(housemanagement_text)
    clean_text = "clean table"
    clean_road = x_bud.make_road(housemanagement_road, clean_text)

    # WHEN
    x_bud.set_fact(day24hr_road, day24hr_road, day24hr_open, day24hr_nigh, True)

    # THEN
    print(x_bud._idearoot._factunits[day24hr_road])
    print(x_bud.get_idea_obj(clean_road)._reasonunits)
    print(x_bud.get_idea_obj(clean_road)._active)
    agenda_dict = x_bud.get_agenda_dict()
    print(f"{len(agenda_dict)=} {agenda_dict.keys()=}")
    assert len(agenda_dict) == 6
    clean_item = agenda_dict.get(clean_road)
    assert clean_item._label == clean_text


def test_BudUnit_get_agenda_dict_DoesNotReturnPledgeItemsOutsideRange():
    # ESTABLISH
    sue_text = "Sue"
    sue_bud = get_budunit_sue_TimeExample()
    clean_text = "clean"
    clean_road = sue_bud.make_l1_road(clean_text)
    sue_bud.set_l1_idea(ideaunit_shop(clean_text, pledge=True))
    time_road = sue_bud.make_l1_road("time")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    jajaday = sue_bud.make_road(jajatime_road, "day")

    sue_bud.edit_idea_attr(
        road=clean_road,
        reason_base=jajatime_road,
        reason_premise=jajaday,
        begin=480,
        close=480,
    )

    # WHEN
    open_x = 1063971180
    nigh_x1 = 2063971523
    sue_bud.set_fact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x1)

    # THEN
    agenda_dict = sue_bud.get_agenda_dict()
    print(f"{agenda_dict.keys()=}")
    assert len(agenda_dict) == 1
    assert clean_road in agenda_dict.keys()

    # WHEN
    nigh_x2 = 1063971923
    sue_bud.set_fact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x2)

    # THEN
    agenda_dict = sue_bud.get_agenda_dict()
    assert len(agenda_dict) == 0


def test_budunit_v001_AgendaExists():
    # ESTABLISH
    x_bud = budunit_v001()
    min_text = "day_minute"
    min_road = x_bud.make_l1_road(min_text)
    x_bud.set_fact(base=min_road, pick=min_road, open=0, nigh=1399)
    assert x_bud
    # for idea_kid in x_bud._idearoot._kids.values():
    #     # print(idea_kid._label)
    #     assert str(type(idea_kid)) != "<class 'str'>"
    #     assert idea_kid.pledge is not None

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert len(agenda_dict) > 0
    assert len(agenda_dict) == 17
    # assert agenda_dict[0].pledge is not None
    # assert str(type(agenda_dict[0])) != "<class 'str'>"
    # assert str(type(agenda_dict[9])) != "<class 'str'>"
    # assert str(type(agenda_dict[12])) != "<class 'str'>"


def test_BudUnit_get_agenda_dict_BudUnitHasCorrectAttributes_budunit_v001():
    # ESTABLISH
    x_bud = budunit_v001()

    day_min_text = "day_minute"
    day_min_road = x_bud.make_l1_road(day_min_text)
    x_bud.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)
    month_week_text = "month_week"
    month_week_road = x_bud.make_l1_road(month_week_text)
    nations_text = "Nation-States"
    nations_road = x_bud.make_l1_road(nations_text)
    mood_text = "Moods"
    mood_road = x_bud.make_l1_road(mood_text)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = x_bud.make_l1_road(aaron_text)
    # internet_text = "Internet"
    # internet_road = x_bud.make_l1_road(internet_text)
    year_month_text = "year_month"
    year_month_road = x_bud.make_l1_road(year_month_text)
    x_bud.set_fact(base=month_week_road, pick=month_week_road)
    x_bud.set_fact(base=nations_road, pick=nations_road)
    x_bud.set_fact(base=mood_road, pick=mood_road)
    x_bud.set_fact(base=aaron_road, pick=aaron_road)
    # x_bud.set_fact(base=internet_road, pick=internet_road)
    x_bud.set_fact(base=year_month_road, pick=year_month_road)
    # season_text = "Seasons"
    # season_road = x_bud.make_l1_road(season_text)
    # x_bud.set_fact(base=season_road, pick=season_road)
    ced_week_text = "ced_week"
    ced_week_road = x_bud.make_l1_road(ced_week_text)
    x_bud.set_fact(base=ced_week_road, pick=ced_week_road)
    # water_text = "WaterExistence"
    # water_road = x_bud.make_l1_road(water_text)
    # x_bud.set_fact(base=water_road, pick=water_road)
    # movie_text = "No Movie playing"
    # movie_road = x_bud.make_l1_road(movie_text)
    # x_bud.set_fact(base=movie_road, pick=movie_text)

    # WHEN
    idea_pledge_list = x_bud.get_agenda_dict()

    # THEN
    assert len(idea_pledge_list) == 27

    week1_road = x_bud.make_road(month_week_road, "1st week")
    x_bud.set_fact(month_week_road, week1_road)
    idea_pledge_list = x_bud.get_agenda_dict()
    assert len(idea_pledge_list) == 27

    weekday_text = "weekdays"
    weekday_road = x_bud.make_l1_road(weekday_text)
    monday_text = "Monday"
    monday_road = x_bud.make_road(weekday_road, monday_text)

    x_bud.set_fact(base=weekday_road, pick=monday_road)
    idea_pledge_list = x_bud.get_agenda_dict()
    assert len(idea_pledge_list) == 39

    x_bud.set_fact(base=weekday_road, pick=weekday_road)
    idea_pledge_list = x_bud.get_agenda_dict()
    assert len(idea_pledge_list) == 53

    # x_bud.set_fact(base=nations_road, pick=nations_road)
    # idea_pledge_list = x_bud.get_agenda_dict()
    # assert len(idea_pledge_list) == 53

    # for base in x_bud.get_missing_fact_bases():
    #     print(f"{base=}")

    # for agenda_item in idea_pledge_list:
    #     print(f"{agenda_item._uid=} {agenda_item._parent_road=}")

    # for agenda_item in idea_pledge_list:
    #     # print(f"{agenda_item._parent_road=}")
    #     pass

    print(len(idea_pledge_list))


def test_BudUnit_get_agenda_dict_BudUnitCanFilterOnBase_budunit_v001_with_large_agenda():
    # ESTABLISH
    x_bud = budunit_v001_with_large_agenda()
    week_text = "weekdays"
    week_road = x_bud.make_l1_road(week_text)
    print(f"{type(x_bud)=}")
    # for base in x_bud.get_missing_fact_bases():
    #     print(f"{base=}")

    # for agenda_item in x_bud.get_agenda_dict():
    #     print(
    #         f"{agenda_item._parent_road=} {agenda_item._label} {len(agenda_item._reasonunits)=}"
    #     )
    #     for reason in agenda_item._reasonunits.values():
    #         if reason.base == weekdays:
    #             print(f"         {weekdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(x_bud.get_agenda_dict()) == 63

    # WHEN
    pledge_list = x_bud.get_agenda_dict(necessary_base=week_road)

    # THEN
    assert len(pledge_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(pledge_list) == 29


def test_BudUnit_set_agenda_task_as_complete_SetsAttrCorrectly_Range():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")

    run_text = "run"
    run_road = zia_bud.make_l1_road(run_text)
    time_road = zia_bud.make_l1_road("time")
    day_text = "day"
    day_road = zia_bud.make_road(time_road, day_text)

    zia_bud.set_l1_idea(ideaunit_shop(run_text, pledge=True))
    zia_bud.set_idea(ideaunit_shop(day_text, _begin=0, _close=500), time_road)
    zia_bud.edit_idea_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=25,
        reason_premise_nigh=81,
    )
    zia_bud.set_fact(base=day_road, pick=day_road, open=30, nigh=87)
    zia_bud.get_agenda_dict()
    run_reasonunits = zia_bud._idearoot._kids[run_text]._reasonunits[day_road]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_road]._status=}")
    print(f"{run_reasonunits.premises[day_road]._task=}")
    print(f"{zia_bud.get_reason_bases()=}")
    assert len(zia_bud.get_idea_dict()) == 4
    assert len(zia_bud.get_agenda_dict()) == 1
    print(f"{zia_bud.get_agenda_dict().keys()=}")
    assert zia_bud.get_agenda_dict().get(run_road)._task == True

    # WHEN
    zia_bud.set_agenda_task_complete(task_road=run_road, base=day_road)

    # THEN
    agenda_dict = zia_bud.get_agenda_dict()
    assert len(agenda_dict) == 0
    assert agenda_dict == {}


def test_BudUnit_set_agenda_task_as_complete_SetsAttrCorrectly_Division():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")

    run_text = "run"
    run_road = zia_bud.make_l1_road(run_text)
    time_text = "time"
    time_road = zia_bud.make_l1_road(time_text)
    day_text = "day"
    day_road = zia_bud.make_road(time_road, day_text)

    zia_bud.set_l1_idea(ideaunit_shop(run_text, pledge=True))
    zia_bud.set_idea(ideaunit_shop(day_text, _begin=0, _close=500), time_road)
    zia_bud.edit_idea_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=1,
        reason_premise_nigh=1,
        reason_premise_divisor=2,
    )

    run_idea = zia_bud.get_idea_obj(run_road)
    # print(f"{run_idea._factheirs=}")
    zia_bud.set_fact(base=day_road, pick=day_road, open=1, nigh=2)
    assert len(zia_bud.get_agenda_dict()) == 1
    zia_bud.set_fact(base=day_road, pick=day_road, open=2, nigh=2)
    assert len(zia_bud.get_agenda_dict()) == 0
    zia_bud.set_fact(base=day_road, pick=day_road, open=400, nigh=400)
    assert len(zia_bud.get_agenda_dict()) == 0
    zia_bud.set_fact(base=day_road, pick=day_road, open=401, nigh=402)
    assert len(zia_bud.get_agenda_dict()) == 1
    # print(f"{run_idea._factheirs=}")
    print(f"{run_idea._factunits=}")

    # WHEN
    zia_bud.set_agenda_task_complete(task_road=run_road, base=day_road)

    # THEN
    print(f"{run_idea._factunits=}")
    # print(f"{run_idea._factheirs=}")
    assert len(zia_bud.get_agenda_dict()) == 0


def test_budunit_get_from_json_CorrectlyLoadsPledgeFromJSON():
    # ESTABLISH
    x_bud_json = budunit_v001().get_json()

    # WHEN
    x_bud = budunit_get_from_json(x_bud_json=x_bud_json)

    # THEN
    assert len(x_bud.get_idea_dict()) == 253
    print(f"{len(x_bud.get_idea_dict())=}")
    casa_text = "casa"
    casa_road = x_bud.make_l1_road(casa_text)
    body_text = "exercise"
    body_road = x_bud.make_road(casa_road, body_text)
    veg_text = "cook veggies every morning"
    veg_road = x_bud.make_road(body_road, veg_text)
    veg_idea = x_bud.get_idea_obj(veg_road)
    assert not veg_idea._active
    assert veg_idea.pledge

    # idea_list = x_bud.get_idea_dict()
    # pledge_true_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
    #         assert idea._active in (True, False)
    #     assert idea.pledge in (True, False)
    #     # if idea._active:
    #     #     print(idea._label)
    #     if idea.pledge:
    #         pledge_true_count += 1
    #         # if idea.pledge is False:
    #         #     print(f"pledge is false {idea._label}")
    #         # for reason in idea._reasonunits.values():
    #         #     assert reason._status in (True, False)
    # assert pledge_true_count > 0

    # WHEN
    day_min_text = "day_minute"
    day_min_road = x_bud.make_l1_road(day_min_text)
    x_bud.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)

    # THEN
    assert len(x_bud.get_agenda_dict()) > 0


def test_BudUnit_create_agenda_item_CorrectlyCreatesAllBudAttributes():
    # WHEN "I am cleaning the cookery since I'm in the flat and it's 8am and it's dirty and it's for my family"

    # ESTABLISH
    sue_bud = get_budunit_sue_TimeExample()
    assert len(sue_bud._accts) == 0
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert len(sue_bud._idearoot._kids) == 1

    clean_things_text = "cleaning things"
    clean_things_road = sue_bud.make_l1_road(clean_things_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = sue_bud.make_road(clean_things_road, clean_cookery_text)
    clean_cookery_idea = ideaunit_shop(
        clean_cookery_text, _parent_road=clean_things_road
    )
    print(f"{clean_cookery_idea.get_road()=}")
    house_text = "house"
    house_road = sue_bud.make_l1_road(house_text)
    cookery_room_text = "cookery room"
    cookery_room_road = sue_bud.make_road(house_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = sue_bud.make_road(cookery_room_road, cookery_dirty_text)

    # create gregorian timeline
    time_road = sue_bud.make_l1_road("time")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    daytime_road = sue_bud.make_road(jajatime_road, "day")
    open_8am = 480
    nigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_road)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
    clean_cookery_idea.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_road)
    daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
    clean_cookery_idea.set_reasonunit(reason=daytime_reason)

    family_text = ",family"
    awardlink_z = awardlink_shop(group_id=family_text)
    clean_cookery_idea.set_awardlink(awardlink_z)

    assert len(sue_bud._accts) == 0
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert len(sue_bud._idearoot._kids) == 1
    assert sue_bud.get_idea_obj(daytime_road)._begin == 0
    assert sue_bud.get_idea_obj(daytime_road)._close == 1440
    print(f"{clean_cookery_idea.get_road()=}")

    # ESTABLISH
    sue_bud.set_dominate_pledge_idea(idea_kid=clean_cookery_idea)

    # THEN
    # for idea_kid in sue_bud._idearoot._kids.keys():
    #     print(f"  {idea_kid=}")

    print(f"{clean_cookery_idea.get_road()=}")
    assert sue_bud.get_idea_obj(clean_cookery_road) is not None
    assert sue_bud.get_idea_obj(clean_cookery_road)._label == clean_cookery_text
    assert sue_bud.get_idea_obj(clean_cookery_road).pledge
    assert len(sue_bud.get_idea_obj(clean_cookery_road)._reasonunits) == 2
    assert sue_bud.get_idea_obj(clean_things_road) is not None
    assert sue_bud.get_idea_obj(cookery_room_road) is not None
    assert sue_bud.get_idea_obj(cookery_dirty_road) is not None
    assert sue_bud.get_idea_obj(daytime_road)._begin == 0
    assert sue_bud.get_idea_obj(daytime_road)._close == 1440
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert sue_bud.get_acctunit_group_ids_dict().get(family_text) is None

    assert len(sue_bud._idearoot._kids) == 3


def test_BudUnit_set_fact_Isue116Resolved_correctlySetsTaskAsTrue():
    # ESTABLISH
    yao_bud = budunit_v002()

    assert len(yao_bud.get_agenda_dict()) == 44
    time_road = yao_bud.make_l1_road("time")
    jajatime_road = yao_bud.make_road(time_road, "jajatime")

    # WHEN
    yao_bud.set_fact(jajatime_road, jajatime_road, open=1063998720, nigh=1064130373)
    pledge_idea_list = yao_bud.get_agenda_dict()

    # THEN
    assert len(pledge_idea_list) == 66
    db_road = yao_bud.make_l1_road("D&B")
    night_text = "late_night_go_to_sleep"
    night_road = yao_bud.make_road(db_road, night_text)
    night_idea = yao_bud._idea_dict.get(night_road)
    # for idea_x in yao_bud.get_agenda_dict():
    #     # if idea_x._task != True:
    #     #     print(f"{len(pledge_idea_list)=} {idea_x._task=} {idea_x.get_road()}")
    #     if idea_x._label == night_label:
    #         night_idea = idea_x
    #         print(f"{idea_x.get_road()=}")

    print(f"\nIdea = '{night_text}' and reason '{jajatime_road}'")
    factheir_jajatime = night_idea._factheirs.get(jajatime_road)
    print(f"\n{factheir_jajatime=}")

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


def test_BudUnit_agenda_IsSetByDoerUnit_1AcctGroup():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    casa_text = "casa"
    casa_road = yao_bud.make_road(yao_text, casa_text)
    yao_bud.set_l1_idea(ideaunit_shop(casa_text, pledge=True))
    assert len(yao_bud.get_agenda_dict()) == 1

    sue_text = "Sue"
    yao_bud.add_acctunit(sue_text)
    doerunit_sue = doerunit_shop()
    doerunit_sue.set_grouphold(group_id=sue_text)
    assert len(yao_bud.get_agenda_dict()) == 1

    # WHEN
    yao_bud.edit_idea_attr(road=casa_road, doerunit=doerunit_sue)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 0

    # WHEN
    yao_bud.add_acctunit(yao_text)
    doerunit_yao = doerunit_shop()
    doerunit_yao.set_grouphold(group_id=yao_text)

    # WHEN
    yao_bud.edit_idea_attr(road=casa_road, doerunit=doerunit_yao)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 1

    # agenda_dict = yao_bud.get_agenda_dict()
    # print(f"{agenda_dict[0]._label=}")


def test_BudUnit_get_agenda_dict_IsSetByDoerUnit_2AcctGroup():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_acctunit(yao_text)
    casa_text = "casa"
    casa_road = yao_bud.make_road(yao_text, casa_text)
    yao_bud.set_l1_idea(ideaunit_shop(casa_text, pledge=True))

    sue_text = "Sue"
    yao_bud.add_acctunit(sue_text)
    run_text = ",runners"
    sue_acctunit = yao_bud.get_acct(sue_text)
    sue_acctunit.add_membership(run_text)

    run_doerunit = doerunit_shop()
    run_doerunit.set_grouphold(group_id=run_text)
    assert len(yao_bud.get_agenda_dict()) == 1

    # WHEN
    yao_bud.edit_idea_attr(road=casa_road, doerunit=run_doerunit)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 0

    # WHEN
    yao_acctunit = yao_bud.get_acct(yao_text)
    yao_acctunit.add_membership(run_text)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 1


def test_IdeaCore_get_agenda_dict_ReturnsCorrectObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # ESTABLISH
    sue_bud = get_budunit_sue_TimeExample()

    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    laundry_text = "do_laundry"
    laundry_road = sue_bud.make_road(casa_road, laundry_text)
    sue_bud.set_l1_idea(ideaunit_shop(casa_text))
    sue_bud.set_idea(ideaunit_shop(laundry_text, pledge=True), casa_road)
    time_road = sue_bud.make_l1_road("time")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    sue_bud.edit_idea_attr(
        road=laundry_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=3420.0,
        reason_premise_nigh=3420.0,
        reason_premise_divisor=10080.0,
    )
    print("set first fact")
    sue_bud.set_fact(jajatime_road, jajatime_road, 1064131200, nigh=1064135133)
    print("get 1st agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")
    assert sue_agenda_dict == {}

    laundry_idea = sue_bud.get_idea_obj(laundry_road)
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
    # for x_ideaunit in sue_bud._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")

    # WHEN
    print("set 2nd fact")
    sue_bud.set_fact(jajatime_road, jajatime_road, 1064131200, nigh=1064136133)
    print("get 2nd agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")

    laundry_idea = sue_bud.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_factheir = laundry_idea._factheirs.get(jajatime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.nigh % 10080=}"
    # )
    # for x_ideaunit in sue_bud._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")
    #         jaja_factheir = x_ideaunit._factheirs.get(jajatime_road)
    #         print(f"{jaja_factheir.open % 10080=}")
    #         print(f"{jaja_factheir.nigh % 10080=}")

    # THEN
    assert sue_agenda_dict == {}


def test_BudUnit_get_all_pledges_ReturnsCorrectObj():
    # ESTABLISH
    zia_text = "Zia"
    zia_bud = budunit_shop(zia_text)
    casa_text = "casa"
    casa_road = zia_bud.make_l1_road(casa_text)
    clean_text = "clean"
    clean_road = zia_bud.make_road(casa_road, clean_text)
    sweep_text = "sweep"
    sweep_road = zia_bud.make_road(clean_road, sweep_text)
    couch_text = "couch"
    couch_road = zia_bud.make_road(casa_road, couch_text)
    zia_bud.set_idea(ideaunit_shop(couch_text), casa_road)
    zia_bud.set_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    zia_bud.set_idea(ideaunit_shop(sweep_text, pledge=True), clean_road)
    sweep_idea = zia_bud.get_idea_obj(sweep_road)
    yao_text = "Yao"
    zia_bud.add_acctunit(yao_text)
    sweep_idea._doerunit.set_grouphold(yao_text)
    print(f"{sweep_idea}")
    agenda_dict = zia_bud.get_agenda_dict()
    assert agenda_dict.get(clean_road) is not None
    assert agenda_dict.get(sweep_road) is None
    assert agenda_dict.get(couch_road) is None

    # WHEN
    all_pledges_dict = zia_bud.get_all_pledges()

    # THEN
    assert all_pledges_dict.get(sweep_road) == zia_bud.get_idea_obj(sweep_road)
    assert all_pledges_dict.get(clean_road) == zia_bud.get_idea_obj(clean_road)
    assert all_pledges_dict.get(couch_road) is None
