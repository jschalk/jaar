from src.a01_term_logic.way import WayTerm
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.concept import ConceptUnit, conceptunit_shop
from src.a06_bud_logic._test_util.example_buds import (
    budunit_v001,
    budunit_v001_with_large_agenda,
    budunit_v002,
    get_budunit_with7amCleanTableReason,
    get_budunit_with_4_levels,
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_with_4_levels_and_2reasons_2facts,
)
from src.a06_bud_logic.bud import budunit_shop, get_from_json as budunit_get_from_json


def get_chores_count(agenda_dict: dict[WayTerm, ConceptUnit]) -> int:
    return sum(bool(x_conceptunit._chore) for x_conceptunit in agenda_dict.values())


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


def test_BudUnit_get_agenda_dict_ReturnsAgendaWithOnlyCorrectConcepts():
    # ESTABLISH
    x_bud = get_budunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_way = x_bud.make_l1_way(wk_str)
    sun_str = "Sunday"
    sun_way = x_bud.make_way(wk_way, sun_str)
    x_bud.add_fact(fcontext=wk_way, fstate=sun_way)

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
    print(f"{agenda_dict.get(x_bud.make_l1_way(casa_str)).concept_label=}")
    assert agenda_dict.get(x_bud.make_l1_way(casa_str))._fund_ratio


def test_BudUnit_get_agenda_dict_WithNo7amConceptExample():
    # ESTABLISH
    x_bud = get_budunit_with7amCleanTableReason()

    # WHEN
    agenda_dict = x_bud.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    clean_str = "clean table"
    print(f"{agenda_dict.keys()=} {x_bud.make_l1_way(clean_str)=}")
    # print(f"{agenda_dict[0].concept_label=}")
    assert len(agenda_dict) == 1

    cat_str = "cat have dinner"
    cat_agenda_concept = agenda_dict.get(x_bud.make_l1_way(cat_str))
    assert cat_agenda_concept.concept_label != clean_str


def test_BudUnit_get_agenda_dict_With7amConceptExample():
    # ESTABLISH
    # set facts as midevening to 8am
    x_bud = get_budunit_with7amCleanTableReason()
    print(f"{len(x_bud.get_agenda_dict())=}")
    assert len(x_bud.get_agenda_dict()) == 1
    timetech_way = x_bud.make_l1_way("timetech")
    day24hr_way = x_bud.make_way(timetech_way, "24hr day")
    day24hr_popen = 0.0
    day24hr_pnigh = 8.0
    housemanagement_str = "housemanagement"
    housemanagement_way = x_bud.make_l1_way(housemanagement_str)
    clean_str = "clean table"
    clean_way = x_bud.make_way(housemanagement_way, clean_str)

    # WHEN
    x_bud.add_fact(day24hr_way, day24hr_way, day24hr_popen, day24hr_pnigh, True)

    # THEN
    print(x_bud.conceptroot.factunits[day24hr_way])
    print(x_bud.get_concept_obj(clean_way).reasonunits)
    print(x_bud.get_concept_obj(clean_way)._active)
    agenda_dict = x_bud.get_agenda_dict()
    print(f"{len(agenda_dict)=} {agenda_dict.keys()=}")
    assert len(agenda_dict) == 6
    clean_concept = agenda_dict.get(clean_way)
    assert clean_concept.concept_label == clean_str


def test_budunit_v001_AgendaExists():
    # ESTABLISH
    yao_bud = budunit_v001()
    min_str = "day_minute"
    min_way = yao_bud.make_l1_way(min_str)
    yao_bud.add_fact(fcontext=min_way, fstate=min_way, fopen=0, fnigh=1399)
    assert yao_bud
    # for concept_kid in yao_bud.conceptroot._kids.values():
    #     # print(concept_kid.concept_label)
    #     assert str(type(concept_kid)) != "<class 'str'>"
    #     assert concept_kid.task is not None

    # WHEN
    agenda_dict = yao_bud.get_agenda_dict()

    # THEN
    assert len(agenda_dict) > 0
    assert len(agenda_dict) == 17
    # assert agenda_dict[0].task is not None
    # assert str(type(agenda_dict[0])) != "<class 'str'>"
    # assert str(type(agenda_dict[9])) != "<class 'str'>"
    # assert str(type(agenda_dict[12])) != "<class 'str'>"


def test_BudUnit_get_agenda_dict_BudUnitHasCorrectAttributes_budunit_v001():
    # ESTABLISH
    yao_bud = budunit_v001()

    day_min_str = "day_minute"
    day_min_way = yao_bud.make_l1_way(day_min_str)
    yao_bud.add_fact(fcontext=day_min_way, fstate=day_min_way, fopen=0, fnigh=1399)
    month_wk_str = "month_wk"
    month_wk_way = yao_bud.make_l1_way(month_wk_str)
    nations_str = "Nation-States"
    nations_way = yao_bud.make_l1_way(nations_str)
    mood_str = "Moods"
    mood_way = yao_bud.make_l1_way(mood_str)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_way = yao_bud.make_l1_way(aaron_str)
    # interweb_str = "Interweb"
    # interweb_way = yao_bud.make_l1_way(interweb_str)
    yr_month_str = "yr_month"
    yr_month_way = yao_bud.make_l1_way(yr_month_str)
    yao_bud.add_fact(fcontext=month_wk_way, fstate=month_wk_way)
    yao_bud.add_fact(fcontext=nations_way, fstate=nations_way)
    yao_bud.add_fact(fcontext=mood_way, fstate=mood_way)
    yao_bud.add_fact(fcontext=aaron_way, fstate=aaron_way)
    # yao_bud.add_fact(fcontext=interweb_way, fstate=interweb_way)
    yao_bud.add_fact(fcontext=yr_month_way, fstate=yr_month_way)
    # season_str = "Seasons"
    # season_way = yao_bud.make_l1_way(season_str)
    # yao_bud.add_fact(fcontext=season_way, fstate=season_way)
    ced_wk_str = "ced_wk"
    ced_wk_way = yao_bud.make_l1_way(ced_wk_str)
    yao_bud.add_fact(fcontext=ced_wk_way, fstate=ced_wk_way)
    # water_str = "WaterExistence"
    # water_way = yao_bud.make_l1_way(water_str)
    # yao_bud.add_fact(fcontext=water_way, fstate=water_way)
    # movie_str = "No Movie playing"
    # movie_way = yao_bud.make_l1_way(movie_str)
    # yao_bud.add_fact(fcontext=movie_way, fstate=movie_str)

    # WHEN
    concept_task_list = yao_bud.get_agenda_dict()

    # THEN
    assert len(concept_task_list) == 27

    wk1_way = yao_bud.make_way(month_wk_way, "1st wk")
    yao_bud.add_fact(month_wk_way, wk1_way)
    concept_task_list = yao_bud.get_agenda_dict()
    assert len(concept_task_list) == 27

    wkday_str = "wkdays"
    wkday_way = yao_bud.make_l1_way(wkday_str)
    monday_str = "Monday"
    monday_way = yao_bud.make_way(wkday_way, monday_str)

    yao_bud.add_fact(fcontext=wkday_way, fstate=monday_way)
    concept_task_list = yao_bud.get_agenda_dict()
    assert len(concept_task_list) == 39

    yao_bud.add_fact(fcontext=wkday_way, fstate=wkday_way)
    concept_task_list = yao_bud.get_agenda_dict()
    assert len(concept_task_list) == 53

    # yao_bud.add_fact(fcontext=nations_way, fstate=nations_way)
    # concept_task_list = yao_bud.get_agenda_dict()
    # assert len(concept_task_list) == 53

    # for rcontext in yao_bud.get_missing_fact_rcontexts():
    #     print(f"{rcontext=}")

    # for agenda_concept in concept_task_list:
    #     print(f"{agenda_concept._uid=} {agenda_concept.parent_way=}")

    # for agenda_concept in concept_task_list:
    #     # print(f"{agenda_concept.parent_way=}")
    #     pass

    print(len(concept_task_list))


def test_BudUnit_get_agenda_dict_BudUnitCanCleanOnRcontext_budunit_v001_with_large_agenda():
    # ESTABLISH
    yao_bud = budunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_way = yao_bud.make_l1_way(wk_str)
    print(f"{type(yao_bud)=}")
    # for rcontext in yao_bud.get_missing_fact_rcontexts():
    #     print(f"{rcontext=}")

    # for agenda_concept in yao_bud.get_agenda_dict():
    #     print(
    #         f"{agenda_concept.parent_way=} {agenda_concept.concept_label} {len(agenda_concept.reasonunits)=}"
    #     )
    #     for reason in agenda_concept.reasonunits.values():
    #         if reason.rcontext == wkdays:
    #             print(f"         {wkdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(yao_bud.get_agenda_dict()) == 63

    # WHEN
    task_list = yao_bud.get_agenda_dict(necessary_rcontext=wk_way)

    # THEN
    assert len(task_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(task_list) == 29


def test_BudUnit_set_agenda_chore_as_complete_SetsAttrCorrectly_Range():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")

    run_str = "run"
    run_way = zia_bud.make_l1_way(run_str)
    time_way = zia_bud.make_l1_way("time")
    day_str = "day"
    day_way = zia_bud.make_way(time_way, day_str)

    zia_bud.set_l1_concept(conceptunit_shop(run_str, task=True))
    zia_bud.set_concept(conceptunit_shop(day_str, begin=0, close=500), time_way)
    zia_bud.edit_concept_attr(
        run_way,
        reason_rcontext=day_way,
        reason_premise=day_way,
        popen=25,
        reason_pnigh=81,
    )
    zia_bud.add_fact(fcontext=day_way, fstate=day_way, fopen=30, fnigh=87)
    zia_bud.get_agenda_dict()
    run_reasonunits = zia_bud.conceptroot._kids[run_str].reasonunits[day_way]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_way]._status=}")
    print(f"{run_reasonunits.premises[day_way]._chore=}")
    print(f"{zia_bud.get_reason_rcontexts()=}")
    assert len(zia_bud.get_concept_dict()) == 4
    assert len(zia_bud.get_agenda_dict()) == 1
    print(f"{zia_bud.get_agenda_dict().keys()=}")
    assert zia_bud.get_agenda_dict().get(run_way)._chore is True

    # WHEN
    zia_bud.set_agenda_chore_complete(chore_way=run_way, rcontext=day_way)

    # THEN
    agenda_dict = zia_bud.get_agenda_dict()
    assert len(agenda_dict) == 0
    assert agenda_dict == {}


def test_BudUnit_set_agenda_chore_as_complete_SetsAttrCorrectly_Division():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")

    run_str = "run"
    run_way = zia_bud.make_l1_way(run_str)
    time_str = "time"
    time_way = zia_bud.make_l1_way(time_str)
    day_str = "day"
    day_way = zia_bud.make_way(time_way, day_str)

    zia_bud.set_l1_concept(conceptunit_shop(run_str, task=True))
    zia_bud.set_concept(conceptunit_shop(day_str, begin=0, close=500), time_way)
    zia_bud.edit_concept_attr(
        run_way,
        reason_rcontext=day_way,
        reason_premise=day_way,
        popen=1,
        reason_pnigh=1,
        pdivisor=2,
    )

    run_concept = zia_bud.get_concept_obj(run_way)
    # print(f"{run_concept._factheirs=}")
    zia_bud.add_fact(fcontext=day_way, fstate=day_way, fopen=1, fnigh=2)
    assert len(zia_bud.get_agenda_dict()) == 1
    zia_bud.add_fact(fcontext=day_way, fstate=day_way, fopen=2, fnigh=2)
    assert len(zia_bud.get_agenda_dict()) == 0
    zia_bud.add_fact(fcontext=day_way, fstate=day_way, fopen=400, fnigh=400)
    assert len(zia_bud.get_agenda_dict()) == 0
    zia_bud.add_fact(fcontext=day_way, fstate=day_way, fopen=401, fnigh=402)
    assert len(zia_bud.get_agenda_dict()) == 1
    # print(f"{run_concept._factheirs=}")
    print(f"{run_concept.factunits=}")

    # WHEN
    zia_bud.set_agenda_chore_complete(chore_way=run_way, rcontext=day_way)

    # THEN
    print(f"{run_concept.factunits=}")
    # print(f"{run_concept._factheirs=}")
    assert len(zia_bud.get_agenda_dict()) == 0


def test_budunit_get_from_json_CorrectlyLoadsTaskFromJSON():
    # ESTABLISH
    yao_bud_json = budunit_v001().get_json()

    # WHEN
    yao_bud = budunit_get_from_json(x_bud_json=yao_bud_json)

    # THEN
    assert len(yao_bud.get_concept_dict()) == 252
    print(f"{len(yao_bud.get_concept_dict())=}")
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    body_str = "exercise"
    body_way = yao_bud.make_way(casa_way, body_str)
    veg_str = "cook veggies every morning"
    veg_way = yao_bud.make_way(body_way, veg_str)
    veg_concept = yao_bud.get_concept_obj(veg_way)
    assert not veg_concept._active
    assert veg_concept.task

    # concept_list = yao_bud.get_concept_dict()
    # task_true_count = 0
    # for concept in concept_list:
    #     if str(type(concept)).find(".concept.ConceptUnit'>") > 0:
    #         assert concept._active in (True, False)
    #     assert concept.task in (True, False)
    #     # if concept._active:
    #     #     print(concept.concept_label)
    #     if concept.task:
    #         task_true_count += 1
    #         # if concept.task is False:
    #         #     print(f"task is false {concept.concept_label}")
    #         # for reason in concept.reasonunits.values():
    #         #     assert reason._status in (True, False)
    # assert task_true_count > 0

    # WHEN
    day_min_str = "day_minute"
    day_min_way = yao_bud.make_l1_way(day_min_str)
    yao_bud.add_fact(fcontext=day_min_way, fstate=day_min_way, fopen=0, fnigh=1399)

    # THEN
    assert len(yao_bud.get_agenda_dict()) > 0


def test_BudUnit_set_fact_Isue116Resolved_correctlySetsChoreAsTrue():
    # ESTABLISH
    yao_bud = budunit_v002()
    print(f"{yao_bud.get_reason_rcontexts()=}")

    assert len(yao_bud.get_agenda_dict()) == 44
    time_way = yao_bud.make_l1_way("time")
    gregtime_way = yao_bud.make_way(time_way, "gregtime")

    # WHEN
    yao_bud.add_fact(gregtime_way, gregtime_way, fopen=1063998720, fnigh=1064130373)
    task_concept_list = yao_bud.get_agenda_dict()

    # THEN
    assert len(task_concept_list) == 66
    db_way = yao_bud.make_l1_way("D&B")
    evening_str = "late_evening_go_to_sleep"
    evening_way = yao_bud.make_way(db_way, evening_str)
    evening_concept = yao_bud._concept_dict.get(evening_way)
    # for concept_x in yao_bud.get_agenda_dict():
    #     # if concept_x._chore != True:
    #     #     print(f"{len(task_concept_list)=} {concept_x._chore=} {concept_x.get_concept_way()}")
    #     if concept_x.concept_label == evening_concept_label:
    #         evening_concept = concept_x
    #         print(f"{concept_x.get_concept_way()=}")

    print(f"\nConcept = '{evening_str}' and reason '{gregtime_way}'")
    factheir_gregtime = evening_concept._factheirs.get(gregtime_way)
    print(f"\n{factheir_gregtime=}")

    # for reasonheir in agenda_concept._reasonheirs.values():
    #     print(f"{reasonheir.rcontext=} {reasonheir._status=} {reasonheir._chore=}")
    reasonheir_gregtime = evening_concept._reasonheirs.get(gregtime_way)
    reasonheir_str = f"\nreasonheir_gregtime= '{reasonheir_gregtime.rcontext}', status={reasonheir_gregtime._status}, chore={reasonheir_gregtime._chore}"
    print(reasonheir_str)

    premiseunit = reasonheir_gregtime.premises.get(gregtime_way)
    print(f"----\n {premiseunit=}")
    print(f" {premiseunit._get_chore_status(factheir=factheir_gregtime)=}")
    print(f" {premiseunit._status=} , {premiseunit._is_range()=} premiseunit fails")
    print(
        f" {premiseunit._status=} , {premiseunit._is_segregate()=} premiseunit passes"
    )
    # segr_obj = premisestatusfinder_shop(
    #     popen=premiseunit.popen,
    #     pnigh=premiseunit.pnigh,
    #     pdivisor=premiseunit.pdivisor,
    #     fopen_full=factheir_gregtime.popen,
    #     fnigh_full=factheir_gregtime.pnigh,
    # )
    # print(
    #     f"----\n  {segr_obj.popen=}  {segr_obj.pnigh=}  {segr_obj.pdivisor=}"
    # )
    # print(
    #     f"       {segr_obj.fopen_full=}         {segr_obj.fnigh_full=} \tdifference:{segr_obj.fnigh_full-segr_obj.fopen_full}"
    # )

    # print(f"  {segr_obj.get_active()=}  {segr_obj.get_chore_status()=}")
    assert get_chores_count(task_concept_list) == 64


def test_BudUnit_agenda_IsSetByLaborUnit_1AcctGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    yao_bud.set_l1_concept(conceptunit_shop(casa_str, task=True))
    assert len(yao_bud.get_agenda_dict()) == 1

    sue_str = "Sue"
    yao_bud.add_acctunit(sue_str)
    laborunit_sue = laborunit_shop()
    laborunit_sue.set_laborlink(labor_title=sue_str)
    assert len(yao_bud.get_agenda_dict()) == 1

    # WHEN
    yao_bud.edit_concept_attr(casa_way, laborunit=laborunit_sue)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 0

    # WHEN
    yao_bud.add_acctunit(yao_str)
    laborunit_yao = laborunit_shop()
    laborunit_yao.set_laborlink(labor_title=yao_str)

    # WHEN
    yao_bud.edit_concept_attr(casa_way, laborunit=laborunit_yao)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 1

    # agenda_dict = yao_bud.get_agenda_dict()
    # print(f"{agenda_dict[0].concept_label=}")


def test_BudUnit_get_agenda_dict_IsSetByLaborUnit_2AcctGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(yao_str)
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    yao_bud.set_l1_concept(conceptunit_shop(casa_str, task=True))

    sue_str = "Sue"
    yao_bud.add_acctunit(sue_str)
    run_str = ";runners"
    sue_acctunit = yao_bud.get_acct(sue_str)
    sue_acctunit.add_membership(run_str)

    run_laborunit = laborunit_shop()
    run_laborunit.set_laborlink(labor_title=run_str)
    assert len(yao_bud.get_agenda_dict()) == 1

    # WHEN
    yao_bud.edit_concept_attr(casa_way, laborunit=run_laborunit)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 0

    # WHEN
    yao_acctunit = yao_bud.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)

    # THEN
    assert len(yao_bud.get_agenda_dict()) == 1


def test_BudUnit_get_all_tasks_ReturnsObj():
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
    zia_bud.set_concept(conceptunit_shop(couch_str), casa_way)
    zia_bud.set_concept(conceptunit_shop(clean_str, task=True), casa_way)
    zia_bud.set_concept(conceptunit_shop(sweep_str, task=True), clean_way)
    sweep_concept = zia_bud.get_concept_obj(sweep_way)
    yao_str = "Yao"
    zia_bud.add_acctunit(yao_str)
    sweep_concept.laborunit.set_laborlink(yao_str)
    print(f"{sweep_concept}")
    agenda_dict = zia_bud.get_agenda_dict()
    assert agenda_dict.get(clean_way) is not None
    assert agenda_dict.get(sweep_way) is None
    assert agenda_dict.get(couch_way) is None

    # WHEN
    all_tasks_dict = zia_bud.get_all_tasks()

    # THEN
    assert all_tasks_dict.get(sweep_way) == zia_bud.get_concept_obj(sweep_way)
    assert all_tasks_dict.get(clean_way) == zia_bud.get_concept_obj(clean_way)
    assert all_tasks_dict.get(couch_way) is None
