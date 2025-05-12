from src.a01_way_logic.way import WayStr
from src.a04_reason_logic.reason_team import teamunit_shop
from src.a05_idea_logic.idea import IdeaUnit, ideaunit_shop
from src.a06_bud_logic.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.a06_bud_logic._utils.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_with7amCleanTableReason,
    get_budunit_with_4_levels_and_2reasons_2facts,
    budunit_v001,
    budunit_v001_with_large_agenda,
    budunit_v002,
)


def get_tasks_count(agenda_dict: dict[WayStr, IdeaUnit]) -> int:
    return sum(bool(x_ideaunit._task) for x_ideaunit in agenda_dict.values())


def test_BudUnit_get_agenda_dict_ReturnsObj():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()

    # WHEN
    agenda_dict = sue_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    print(f"{agenda_dict.keys()=}")
    assert sue_bud.make_l1_way("casa") in agenda_dict.keys()
    assert sue_bud.make_l1_way("cat have dinner") in agenda_dict.keys()


def test_BudUnit_get_agenda_dict_ReturnsAgendaWithOnlyCorrectIdeas():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_way = x_bud.make_l1_way(week_str)
    sun_str = "Sunday"
    sun_way = x_bud.make_way(week_way, sun_str)
    x_bud.add_fact(fcontext=week_way, fbranch=sun_way)

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    print(f"{agenda_dict=}")
    assert x_bud.make_l1_way("cat have dinner") in agenda_dict.keys()


def test_BudUnit_get_agenda_dict_WithLargeBud_fund():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels_and_2reasons_2facts()

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    assert agenda_dict.get(x_bud.make_l1_way("cat have dinner"))._fund_ratio

    casa_str = "casa"
    print(f"{agenda_dict.keys()=} {x_bud.make_l1_way(casa_str)=}")
    print(f"{agenda_dict.get(x_bud.make_l1_way(casa_str)).idea_tag=}")
    assert agenda_dict.get(x_bud.make_l1_way(casa_str))._fund_ratio


def test_BudUnit_get_agenda_dict_WithNo7amIdeaExample():
    # ESTABLISH
    x_bud = get_budunit_with7amCleanTableReason()

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    clean_str = "clean table"
    print(f"{agenda_dict.keys()=} {x_bud.make_l1_way(clean_str)=}")
    # print(f"{agenda_dict[0].idea_tag=}")
    assert len(agenda_dict) == 1

    cat_str = "cat have dinner"
    cat_agenda_idea = agenda_dict.get(x_bud.make_l1_way(cat_str))
    assert cat_agenda_idea.idea_tag != clean_str


def test_BudUnit_get_agenda_dict_With7amIdeaExample():
    # ESTABLISH
    # set facts as midevening to 8am
    x_bud = get_budunit_with7amCleanTableReason()
    print(f"{len(x_bud.get_agenda_dict())=}")
    assert len(x_bud.get_agenda_dict()) == 1
    timetech_way = x_bud.make_l1_way("timetech")
    day24hr_way = x_bud.make_way(timetech_way, "24hr day")
    day24hr_open = 0.0
    day24hr_pnigh = 8.0
    housemanagement_str = "housemanagement"
    housemanagement_way = x_bud.make_l1_way(housemanagement_str)
    clean_str = "clean table"
    clean_way = x_bud.make_way(housemanagement_way, clean_str)

    # WHEN
    x_bud.add_fact(day24hr_way, day24hr_way, day24hr_open, day24hr_pnigh, True)

    # THEN
    print(x_bud.idearoot.factunits[day24hr_way])
    print(x_bud.get_idea_obj(clean_way).reasonunits)
    print(x_bud.get_idea_obj(clean_way)._active)
    agenda_dict = x_bud.get_agenda_dict()
    print(f"{len(agenda_dict)=} {agenda_dict.keys()=}")
    assert len(agenda_dict) == 6
    clean_idea = agenda_dict.get(clean_way)
    assert clean_idea.idea_tag == clean_str


def test_budunit_v001_AgendaExists():
    # ESTABLISH
    yao_bud = budunit_v001()
    min_str = "day_minute"
    min_way = yao_bud.make_l1_way(min_str)
    yao_bud.add_fact(fcontext=min_way, fbranch=min_way, fopen=0, fnigh=1399)
    assert yao_bud
    # for idea_kid in yao_bud.idearoot._kids.values():
    #     # print(idea_kid.idea_tag)
    #     assert str(type(idea_kid)) != "<class 'str'>"
    #     assert idea_kid.pledge is not None

    # WHEN
    agenda_dict = yao_bud.get_agenda_dict()

    # THEN
    assert len(agenda_dict) > 0
    assert len(agenda_dict) == 17
    # assert agenda_dict[0].pledge is not None
    # assert str(type(agenda_dict[0])) != "<class 'str'>"
    # assert str(type(agenda_dict[9])) != "<class 'str'>"
    # assert str(type(agenda_dict[12])) != "<class 'str'>"


def test_BudUnit_get_agenda_dict_BudUnitHasCorrectAttributes_budunit_v001():
    # ESTABLISH
    yao_bud = budunit_v001()

    day_min_str = "day_minute"
    day_min_way = yao_bud.make_l1_way(day_min_str)
    yao_bud.add_fact(fcontext=day_min_way, fbranch=day_min_way, fopen=0, fnigh=1399)
    month_week_str = "month_week"
    month_week_way = yao_bud.make_l1_way(month_week_str)
    nations_str = "Nation-States"
    nations_way = yao_bud.make_l1_way(nations_str)
    mood_str = "Moods"
    mood_way = yao_bud.make_l1_way(mood_str)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_way = yao_bud.make_l1_way(aaron_str)
    # interweb_str = "Interweb"
    # interweb_way = yao_bud.make_l1_way(interweb_str)
    year_month_str = "year_month"
    year_month_way = yao_bud.make_l1_way(year_month_str)
    yao_bud.add_fact(fcontext=month_week_way, fbranch=month_week_way)
    yao_bud.add_fact(fcontext=nations_way, fbranch=nations_way)
    yao_bud.add_fact(fcontext=mood_way, fbranch=mood_way)
    yao_bud.add_fact(fcontext=aaron_way, fbranch=aaron_way)
    # yao_bud.add_fact(fcontext=interweb_way, fbranch=interweb_way)
    yao_bud.add_fact(fcontext=year_month_way, fbranch=year_month_way)
    # season_str = "Seasons"
    # season_way = yao_bud.make_l1_way(season_str)
    # yao_bud.add_fact(fcontext=season_way, fbranch=season_way)
    ced_week_str = "ced_week"
    ced_week_way = yao_bud.make_l1_way(ced_week_str)
    yao_bud.add_fact(fcontext=ced_week_way, fbranch=ced_week_way)
    # water_str = "WaterExistence"
    # water_way = yao_bud.make_l1_way(water_str)
    # yao_bud.add_fact(fcontext=water_way, fbranch=water_way)
    # movie_str = "No Movie playing"
    # movie_way = yao_bud.make_l1_way(movie_str)
    # yao_bud.add_fact(fcontext=movie_way, fbranch=movie_str)

    # WHEN
    idea_pledge_list = yao_bud.get_agenda_dict()

    # THEN
    assert len(idea_pledge_list) == 27

    week1_way = yao_bud.make_way(month_week_way, "1st week")
    yao_bud.add_fact(month_week_way, week1_way)
    idea_pledge_list = yao_bud.get_agenda_dict()
    assert len(idea_pledge_list) == 27

    weekday_str = "weekdays"
    weekday_way = yao_bud.make_l1_way(weekday_str)
    monday_str = "Monday"
    monday_way = yao_bud.make_way(weekday_way, monday_str)

    yao_bud.add_fact(fcontext=weekday_way, fbranch=monday_way)
    idea_pledge_list = yao_bud.get_agenda_dict()
    assert len(idea_pledge_list) == 39

    yao_bud.add_fact(fcontext=weekday_way, fbranch=weekday_way)
    idea_pledge_list = yao_bud.get_agenda_dict()
    assert len(idea_pledge_list) == 53

    # yao_bud.add_fact(fcontext=nations_way, fbranch=nations_way)
    # idea_pledge_list = yao_bud.get_agenda_dict()
    # assert len(idea_pledge_list) == 53

    # for rcontext in yao_bud.get_missing_fact_rcontexts():
    #     print(f"{rcontext=}")

    # for agenda_idea in idea_pledge_list:
    #     print(f"{agenda_idea._uid=} {agenda_idea.parent_way=}")

    # for agenda_idea in idea_pledge_list:
    #     # print(f"{agenda_idea.parent_way=}")
    #     pass

    print(len(idea_pledge_list))


def test_BudUnit_get_agenda_dict_BudUnitCanCleanOnRcontext_budunit_v001_with_large_agenda():
    # ESTABLISH
    yao_bud = budunit_v001_with_large_agenda()
    week_str = "weekdays"
    week_way = yao_bud.make_l1_way(week_str)
    print(f"{type(yao_bud)=}")
    # for rcontext in yao_bud.get_missing_fact_rcontexts():
    #     print(f"{rcontext=}")

    # for agenda_idea in yao_bud.get_agenda_dict():
    #     print(
    #         f"{agenda_idea.parent_way=} {agenda_idea.idea_tag} {len(agenda_idea.reasonunits)=}"
    #     )
    #     for reason in agenda_idea.reasonunits.values():
    #         if reason.rcontext == weekdays:
    #             print(f"         {weekdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(yao_bud.get_agenda_dict()) == 63

    # WHEN
    pledge_list = yao_bud.get_agenda_dict(necessary_rcontext=week_way)

    # THEN
    assert len(pledge_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(pledge_list) == 29


def test_BudUnit_set_agenda_task_as_complete_SetsAttrCorrectly_Range():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")

    run_str = "run"
    run_way = zia_bud.make_l1_way(run_str)
    time_way = zia_bud.make_l1_way("time")
    day_str = "day"
    day_way = zia_bud.make_way(time_way, day_str)

    zia_bud.set_l1_idea(ideaunit_shop(run_str, pledge=True))
    zia_bud.set_idea(ideaunit_shop(day_str, begin=0, close=500), time_way)
    zia_bud.edit_idea_attr(
        run_way,
        reason_rcontext=day_way,
        reason_premise=day_way,
        reason_premise_open=25,
        reason_pnigh=81,
    )
    zia_bud.add_fact(fcontext=day_way, fbranch=day_way, fopen=30, fnigh=87)
    zia_bud.get_agenda_dict()
    run_reasonunits = zia_bud.idearoot._kids[run_str].reasonunits[day_way]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_way]._status=}")
    print(f"{run_reasonunits.premises[day_way]._task=}")
    print(f"{zia_bud.get_reason_rcontexts()=}")
    assert len(zia_bud.get_idea_dict()) == 4
    assert len(zia_bud.get_agenda_dict()) == 1
    print(f"{zia_bud.get_agenda_dict().keys()=}")
    assert zia_bud.get_agenda_dict().get(run_way)._task is True

    # WHEN
    zia_bud.set_agenda_task_complete(task_way=run_way, rcontext=day_way)

    # THEN
    agenda_dict = zia_bud.get_agenda_dict()
    assert len(agenda_dict) == 0
    assert agenda_dict == {}


def test_BudUnit_set_agenda_task_as_complete_SetsAttrCorrectly_Division():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")

    run_str = "run"
    run_way = zia_bud.make_l1_way(run_str)
    time_str = "time"
    time_way = zia_bud.make_l1_way(time_str)
    day_str = "day"
    day_way = zia_bud.make_way(time_way, day_str)

    zia_bud.set_l1_idea(ideaunit_shop(run_str, pledge=True))
    zia_bud.set_idea(ideaunit_shop(day_str, begin=0, close=500), time_way)
    zia_bud.edit_idea_attr(
        run_way,
        reason_rcontext=day_way,
        reason_premise=day_way,
        reason_premise_open=1,
        reason_pnigh=1,
        reason_premise_divisor=2,
    )

    run_idea = zia_bud.get_idea_obj(run_way)
    # print(f"{run_idea._factheirs=}")
    zia_bud.add_fact(fcontext=day_way, fbranch=day_way, fopen=1, fnigh=2)
    assert len(zia_bud.get_agenda_dict()) == 1
    zia_bud.add_fact(fcontext=day_way, fbranch=day_way, fopen=2, fnigh=2)
    assert len(zia_bud.get_agenda_dict()) == 0
    zia_bud.add_fact(fcontext=day_way, fbranch=day_way, fopen=400, fnigh=400)
    assert len(zia_bud.get_agenda_dict()) == 0
    zia_bud.add_fact(fcontext=day_way, fbranch=day_way, fopen=401, fnigh=402)
    assert len(zia_bud.get_agenda_dict()) == 1
    # print(f"{run_idea._factheirs=}")
    print(f"{run_idea.factunits=}")

    # WHEN
    zia_bud.set_agenda_task_complete(task_way=run_way, rcontext=day_way)

    # THEN
    print(f"{run_idea.factunits=}")
    # print(f"{run_idea._factheirs=}")
    assert len(zia_bud.get_agenda_dict()) == 0


def test_budunit_get_from_json_CorrectlyLoadsPledgeFromJSON():
    # ESTABLISH
    yao_bud_json = budunit_v001().get_json()

    # WHEN
    yao_bud = budunit_get_from_json(x_bud_json=yao_bud_json)

    # THEN
    assert len(yao_bud.get_idea_dict()) == 252
    print(f"{len(yao_bud.get_idea_dict())=}")
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    body_str = "exercise"
    body_way = yao_bud.make_way(casa_way, body_str)
    veg_str = "cook veggies every morning"
    veg_way = yao_bud.make_way(body_way, veg_str)
    veg_idea = yao_bud.get_idea_obj(veg_way)
    assert not veg_idea._active
    assert veg_idea.pledge

    # idea_list = yao_bud.get_idea_dict()
    # pledge_true_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
    #         assert idea._active in (True, False)
    #     assert idea.pledge in (True, False)
    #     # if idea._active:
    #     #     print(idea.idea_tag)
    #     if idea.pledge:
    #         pledge_true_count += 1
    #         # if idea.pledge is False:
    #         #     print(f"pledge is false {idea.idea_tag}")
    #         # for reason in idea.reasonunits.values():
    #         #     assert reason._status in (True, False)
    # assert pledge_true_count > 0

    # WHEN
    day_min_str = "day_minute"
    day_min_way = yao_bud.make_l1_way(day_min_str)
    yao_bud.add_fact(fcontext=day_min_way, fbranch=day_min_way, fopen=0, fnigh=1399)

    # THEN
    assert len(yao_bud.get_agenda_dict()) > 0


def test_BudUnit_set_fact_Isue116Resolved_correctlySetsTaskAsTrue():
    # ESTABLISH
    yao_bud = budunit_v002()

    assert len(yao_bud.get_agenda_dict()) == 44
    time_way = yao_bud.make_l1_way("time")
    gregtime_way = yao_bud.make_way(time_way, "gregtime")

    # WHEN
    yao_bud.add_fact(gregtime_way, gregtime_way, fopen=1063998720, fnigh=1064130373)
    pledge_idea_list = yao_bud.get_agenda_dict()

    # THEN
    assert len(pledge_idea_list) == 66
    db_way = yao_bud.make_l1_way("D&B")
    evening_str = "late_evening_go_to_sleep"
    evening_way = yao_bud.make_way(db_way, evening_str)
    evening_idea = yao_bud._idea_dict.get(evening_way)
    # for idea_x in yao_bud.get_agenda_dict():
    #     # if idea_x._task != True:
    #     #     print(f"{len(pledge_idea_list)=} {idea_x._task=} {idea_x.get_idea_way()}")
    #     if idea_x.idea_tag == evening_idea_tag:
    #         evening_idea = idea_x
    #         print(f"{idea_x.get_idea_way()=}")

    print(f"\nIdea = '{evening_str}' and reason '{gregtime_way}'")
    factheir_gregtime = evening_idea._factheirs.get(gregtime_way)
    print(f"\n{factheir_gregtime=}")

    # for reasonheir in agenda_idea._reasonheirs.values():
    #     print(f"{reasonheir.rcontext=} {reasonheir._status=} {reasonheir._task=}")
    reasonheir_gregtime = evening_idea._reasonheirs.get(gregtime_way)
    reasonheir_str = f"\nreasonheir_gregtime= '{reasonheir_gregtime.rcontext}', status={reasonheir_gregtime._status}, task={reasonheir_gregtime._task}"
    print(reasonheir_str)

    premiseunit = reasonheir_gregtime.premises.get(gregtime_way)
    print(f"----\n {premiseunit=}")
    print(f" {premiseunit._get_task_status(factheir=factheir_gregtime)=}")
    print(f" {premiseunit._status=} , {premiseunit._is_range()=} premiseunit fails")
    print(
        f" {premiseunit._status=} , {premiseunit._is_segregate()=} premiseunit passes"
    )
    # segr_obj = premisestatusfinder_shop(
    #     premise_open=premiseunit.open,
    #     pnigh=premiseunit.pnigh,
    #     premise_divisor=premiseunit.divisor,
    #     fact_open_full=factheir_gregtime.open,
    #     fnigh_full=factheir_gregtime.pnigh,
    # )
    # print(
    #     f"----\n  {segr_obj.premise_open=}  {segr_obj.pnigh=}  {segr_obj.premise_divisor=}"
    # )
    # print(
    #     f"       {segr_obj.fact_open_full=}         {segr_obj.fnigh_full=} \tdifference:{segr_obj.fnigh_full-segr_obj.fact_open_full}"
    # )

    # print(f"  {segr_obj.get_active()=}  {segr_obj.get_task_status()=}")
    assert get_tasks_count(pledge_idea_list) == 64


def test_BudUnit_agenda_IsSetByTeamUnit_1AcctGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    yao_bud.set_l1_idea(ideaunit_shop(casa_str, pledge=True))
    assert len(yao_bud.get_agenda_dict()) == 1

    sue_str = "Sue"
    yao_bud.add_acctunit(sue_str)
    teamunit_sue = teamunit_shop()
    teamunit_sue.set_teamlink(team_label=sue_str)
    assert len(yao_bud.get_agenda_dict()) == 1

    # WHEN
    yao_bud.edit_idea_attr(casa_way, teamunit=teamunit_sue)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 0

    # WHEN
    yao_bud.add_acctunit(yao_str)
    teamunit_yao = teamunit_shop()
    teamunit_yao.set_teamlink(team_label=yao_str)

    # WHEN
    yao_bud.edit_idea_attr(casa_way, teamunit=teamunit_yao)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 1

    # agenda_dict = yao_bud.get_agenda_dict()
    # print(f"{agenda_dict[0].idea_tag=}")


def test_BudUnit_get_agenda_dict_IsSetByTeamUnit_2AcctGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(yao_str)
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    yao_bud.set_l1_idea(ideaunit_shop(casa_str, pledge=True))

    sue_str = "Sue"
    yao_bud.add_acctunit(sue_str)
    run_str = ";runners"
    sue_acctunit = yao_bud.get_acct(sue_str)
    sue_acctunit.add_membership(run_str)

    run_teamunit = teamunit_shop()
    run_teamunit.set_teamlink(team_label=run_str)
    assert len(yao_bud.get_agenda_dict()) == 1

    # WHEN
    yao_bud.edit_idea_attr(casa_way, teamunit=run_teamunit)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 0

    # WHEN
    yao_acctunit = yao_bud.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 1


def test_BudUnit_get_all_pledges_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    zia_bud = budunit_shop(zia_str)
    casa_str = "casa"
    casa_way = zia_bud.make_l1_way(casa_str)
    clean_str = "clean"
    clean_way = zia_bud.make_way(casa_way, clean_str)
    sweep_str = "sweep"
    sweep_way = zia_bud.make_way(clean_way, sweep_str)
    couch_str = "couch"
    couch_way = zia_bud.make_way(casa_way, couch_str)
    zia_bud.set_idea(ideaunit_shop(couch_str), casa_way)
    zia_bud.set_idea(ideaunit_shop(clean_str, pledge=True), casa_way)
    zia_bud.set_idea(ideaunit_shop(sweep_str, pledge=True), clean_way)
    sweep_idea = zia_bud.get_idea_obj(sweep_way)
    yao_str = "Yao"
    zia_bud.add_acctunit(yao_str)
    sweep_idea.teamunit.set_teamlink(yao_str)
    print(f"{sweep_idea}")
    agenda_dict = zia_bud.get_agenda_dict()
    assert agenda_dict.get(clean_way) is not None
    assert agenda_dict.get(sweep_way) is None
    assert agenda_dict.get(couch_way) is None

    # WHEN
    all_pledges_dict = zia_bud.get_all_pledges()

    # THEN
    assert all_pledges_dict.get(sweep_way) == zia_bud.get_idea_obj(sweep_way)
    assert all_pledges_dict.get(clean_way) == zia_bud.get_idea_obj(clean_way)
    assert all_pledges_dict.get(couch_way) is None
