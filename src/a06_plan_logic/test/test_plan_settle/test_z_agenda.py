from src.a01_term_logic.rope import RopeTerm
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.concept import ConceptUnit, conceptunit_shop
from src.a06_plan_logic.plan import (
    get_from_json as planunit_get_from_json,
    planunit_shop,
)
from src.a06_plan_logic.test._util.example_plans import (
    get_planunit_with7amCleanTableReason,
    get_planunit_with_4_levels,
    get_planunit_with_4_levels_and_2reasons,
    get_planunit_with_4_levels_and_2reasons_2facts,
    planunit_v001,
    planunit_v001_with_large_agenda,
    planunit_v002,
)


def get_chores_count(agenda_dict: dict[RopeTerm, ConceptUnit]) -> int:
    return sum(bool(x_conceptunit._chore) for x_conceptunit in agenda_dict.values())


def test_PlanUnit_get_agenda_dict_ReturnsObj_WithTwoConcepts():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()

    # WHEN
    agenda_dict = sue_plan.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    print(f"{agenda_dict.keys()=}")
    assert sue_plan.make_l1_rope("casa") in agenda_dict.keys()
    assert sue_plan.make_l1_rope("cat have dinner") in agenda_dict.keys()


def test_PlanUnit_get_agenda_dict_ReturnsAgendaWithOnlyCorrectConcepts():
    # ESTABLISH
    x_plan = get_planunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_rope = x_plan.make_l1_rope(wk_str)
    sun_str = "Sunday"
    sun_rope = x_plan.make_rope(wk_rope, sun_str)
    x_plan.add_fact(fcontext=wk_rope, fstate=sun_rope)

    # WHEN
    agenda_dict = x_plan.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    print(f"{agenda_dict=}")
    assert x_plan.make_l1_rope("cat have dinner") in agenda_dict.keys()


def test_PlanUnit_get_agenda_dict_WithLargePlan_fund():
    # ESTABLISH
    x_plan = get_planunit_with_4_levels_and_2reasons_2facts()

    # WHEN
    agenda_dict = x_plan.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    assert agenda_dict.get(x_plan.make_l1_rope("cat have dinner"))._fund_ratio

    casa_str = "casa"
    print(f"{agenda_dict.keys()=} {x_plan.make_l1_rope(casa_str)=}")
    print(f"{agenda_dict.get(x_plan.make_l1_rope(casa_str)).concept_label=}")
    assert agenda_dict.get(x_plan.make_l1_rope(casa_str))._fund_ratio


def test_PlanUnit_get_agenda_dict_WithNo7amConceptExample():
    # ESTABLISH
    x_plan = get_planunit_with7amCleanTableReason()

    # WHEN
    agenda_dict = x_plan.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    clean_str = "clean table"
    print(f"{agenda_dict.keys()=} {x_plan.make_l1_rope(clean_str)=}")
    # print(f"{agenda_dict[0].concept_label=}")
    assert len(agenda_dict) == 1

    cat_str = "cat have dinner"
    cat_agenda_concept = agenda_dict.get(x_plan.make_l1_rope(cat_str))
    assert cat_agenda_concept.concept_label != clean_str


def test_PlanUnit_get_agenda_dict_With7amConceptExample():
    # ESTABLISH
    # set facts as midevening to 8am
    x_plan = get_planunit_with7amCleanTableReason()
    print(f"{len(x_plan.get_agenda_dict())=}")
    assert len(x_plan.get_agenda_dict()) == 1
    timetech_rope = x_plan.make_l1_rope("timetech")
    day24hr_rope = x_plan.make_rope(timetech_rope, "24hr day")
    day24hr_popen = 0.0
    day24hr_pnigh = 8.0
    housemanagement_str = "housemanagement"
    housemanagement_rope = x_plan.make_l1_rope(housemanagement_str)
    clean_str = "clean table"
    clean_rope = x_plan.make_rope(housemanagement_rope, clean_str)

    # WHEN
    x_plan.add_fact(day24hr_rope, day24hr_rope, day24hr_popen, day24hr_pnigh, True)

    # THEN
    print(x_plan.conceptroot.factunits[day24hr_rope])
    print(x_plan.get_concept_obj(clean_rope).reasonunits)
    print(x_plan.get_concept_obj(clean_rope)._active)
    agenda_dict = x_plan.get_agenda_dict()
    print(f"{len(agenda_dict)=} {agenda_dict.keys()=}")
    assert len(agenda_dict) == 6
    clean_concept = agenda_dict.get(clean_rope)
    assert clean_concept.concept_label == clean_str


def test_planunit_v001_AgendaExists():
    # ESTABLISH
    yao_plan = planunit_v001()
    min_str = "day_minute"
    min_rope = yao_plan.make_l1_rope(min_str)
    yao_plan.add_fact(fcontext=min_rope, fstate=min_rope, fopen=0, fnigh=1399)
    assert yao_plan
    # for concept_kid in yao_plan.conceptroot._kids.values():
    #     # print(concept_kid.concept_label)
    #     assert str(type(concept_kid)) != "<class 'str'>"
    #     assert concept_kid.task is not None

    # WHEN
    agenda_dict = yao_plan.get_agenda_dict()

    # THEN
    assert len(agenda_dict) > 0
    assert len(agenda_dict) == 17
    # assert agenda_dict[0].task is not None
    # assert str(type(agenda_dict[0])) != "<class 'str'>"
    # assert str(type(agenda_dict[9])) != "<class 'str'>"
    # assert str(type(agenda_dict[12])) != "<class 'str'>"


def test_PlanUnit_get_agenda_dict_PlanUnitHasCorrectAttributes_planunit_v001():
    # ESTABLISH
    yao_plan = planunit_v001()

    day_min_str = "day_minute"
    day_min_rope = yao_plan.make_l1_rope(day_min_str)
    yao_plan.add_fact(fcontext=day_min_rope, fstate=day_min_rope, fopen=0, fnigh=1399)
    month_wk_str = "month_wk"
    month_wk_rope = yao_plan.make_l1_rope(month_wk_str)
    nations_str = "Nation-States"
    nations_rope = yao_plan.make_l1_rope(nations_str)
    mood_str = "Moods"
    mood_rope = yao_plan.make_l1_rope(mood_str)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_plan.make_l1_rope(aaron_str)
    # interweb_str = "Interweb"
    # interweb_rope = yao_plan.make_l1_rope(interweb_str)
    yr_month_str = "yr_month"
    yr_month_rope = yao_plan.make_l1_rope(yr_month_str)
    yao_plan.add_fact(fcontext=month_wk_rope, fstate=month_wk_rope)
    yao_plan.add_fact(fcontext=nations_rope, fstate=nations_rope)
    yao_plan.add_fact(fcontext=mood_rope, fstate=mood_rope)
    yao_plan.add_fact(fcontext=aaron_rope, fstate=aaron_rope)
    # yao_plan.add_fact(fcontext=interweb_rope, fstate=interweb_rope)
    yao_plan.add_fact(fcontext=yr_month_rope, fstate=yr_month_rope)
    # season_str = "Seasons"
    # season_rope = yao_plan.make_l1_rope(season_str)
    # yao_plan.add_fact(fcontext=season_rope, fstate=season_rope)
    ced_wk_str = "ced_wk"
    ced_wk_rope = yao_plan.make_l1_rope(ced_wk_str)
    yao_plan.add_fact(fcontext=ced_wk_rope, fstate=ced_wk_rope)
    # water_str = "WaterExistence"
    # water_rope = yao_plan.make_l1_rope(water_str)
    # yao_plan.add_fact(fcontext=water_rope, fstate=water_rope)
    # movie_str = "No Movie playing"
    # movie_rope = yao_plan.make_l1_rope(movie_str)
    # yao_plan.add_fact(fcontext=movie_rope, fstate=movie_str)

    # WHEN
    concept_task_list = yao_plan.get_agenda_dict()

    # THEN
    assert len(concept_task_list) == 27

    wk1_rope = yao_plan.make_rope(month_wk_rope, "1st wk")
    yao_plan.add_fact(month_wk_rope, wk1_rope)
    concept_task_list = yao_plan.get_agenda_dict()
    assert len(concept_task_list) == 27

    wkday_str = "wkdays"
    wkday_rope = yao_plan.make_l1_rope(wkday_str)
    monday_str = "Monday"
    monday_rope = yao_plan.make_rope(wkday_rope, monday_str)

    yao_plan.add_fact(fcontext=wkday_rope, fstate=monday_rope)
    concept_task_list = yao_plan.get_agenda_dict()
    assert len(concept_task_list) == 39

    yao_plan.add_fact(fcontext=wkday_rope, fstate=wkday_rope)
    concept_task_list = yao_plan.get_agenda_dict()
    assert len(concept_task_list) == 53

    # yao_plan.add_fact(fcontext=nations_rope, fstate=nations_rope)
    # concept_task_list = yao_plan.get_agenda_dict()
    # assert len(concept_task_list) == 53

    # for rcontext in yao_plan.get_missing_fact_rcontexts():
    #     print(f"{rcontext=}")

    # for agenda_concept in concept_task_list:
    #     print(f"{agenda_concept._uid=} {agenda_concept.parent_rope=}")

    # for agenda_concept in concept_task_list:
    #     # print(f"{agenda_concept.parent_rope=}")
    #     pass

    print(len(concept_task_list))


def test_PlanUnit_get_agenda_dict_PlanUnitCanCleanOnRcontext_planunit_v001_with_large_agenda():
    # ESTABLISH
    yao_plan = planunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_rope = yao_plan.make_l1_rope(wk_str)
    print(f"{type(yao_plan)=}")
    # for rcontext in yao_plan.get_missing_fact_rcontexts():
    #     print(f"{rcontext=}")

    # for agenda_concept in yao_plan.get_agenda_dict():
    #     print(
    #         f"{agenda_concept.parent_rope=} {agenda_concept.concept_label} {len(agenda_concept.reasonunits)=}"
    #     )
    #     for reason in agenda_concept.reasonunits.values():
    #         if reason.rcontext == wkdays:
    #             print(f"         {wkdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(yao_plan.get_agenda_dict()) == 63

    # WHEN
    task_list = yao_plan.get_agenda_dict(necessary_rcontext=wk_rope)

    # THEN
    assert len(task_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(task_list) == 29


def test_PlanUnit_set_agenda_chore_as_complete_SetsAttrCorrectly_Range():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")

    run_str = "run"
    run_rope = zia_plan.make_l1_rope(run_str)
    time_rope = zia_plan.make_l1_rope("time")
    day_str = "day"
    day_rope = zia_plan.make_rope(time_rope, day_str)

    zia_plan.set_l1_concept(conceptunit_shop(run_str, task=True))
    zia_plan.set_concept(conceptunit_shop(day_str, begin=0, close=500), time_rope)
    zia_plan.edit_concept_attr(
        run_rope,
        reason_rcontext=day_rope,
        reason_premise=day_rope,
        popen=25,
        reason_pnigh=81,
    )
    zia_plan.add_fact(fcontext=day_rope, fstate=day_rope, fopen=30, fnigh=87)
    zia_plan.get_agenda_dict()
    run_reasonunits = zia_plan.conceptroot._kids[run_str].reasonunits[day_rope]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_rope]._status=}")
    print(f"{run_reasonunits.premises[day_rope]._chore=}")
    print(f"{zia_plan.get_reason_rcontexts()=}")
    assert len(zia_plan.get_concept_dict()) == 4
    assert len(zia_plan.get_agenda_dict()) == 1
    print(f"{zia_plan.get_agenda_dict().keys()=}")
    assert zia_plan.get_agenda_dict().get(run_rope)._chore is True

    # WHEN
    zia_plan.set_agenda_chore_complete(chore_rope=run_rope, rcontext=day_rope)

    # THEN
    agenda_dict = zia_plan.get_agenda_dict()
    assert len(agenda_dict) == 0
    assert agenda_dict == {}


def test_PlanUnit_set_agenda_chore_as_complete_SetsAttrCorrectly_Division():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")

    run_str = "run"
    run_rope = zia_plan.make_l1_rope(run_str)
    time_str = "time"
    time_rope = zia_plan.make_l1_rope(time_str)
    day_str = "day"
    day_rope = zia_plan.make_rope(time_rope, day_str)

    zia_plan.set_l1_concept(conceptunit_shop(run_str, task=True))
    zia_plan.set_concept(conceptunit_shop(day_str, begin=0, close=500), time_rope)
    zia_plan.edit_concept_attr(
        run_rope,
        reason_rcontext=day_rope,
        reason_premise=day_rope,
        popen=1,
        reason_pnigh=1,
        pdivisor=2,
    )

    run_concept = zia_plan.get_concept_obj(run_rope)
    # print(f"{run_concept._factheirs=}")
    zia_plan.add_fact(fcontext=day_rope, fstate=day_rope, fopen=1, fnigh=2)
    assert len(zia_plan.get_agenda_dict()) == 1
    zia_plan.add_fact(fcontext=day_rope, fstate=day_rope, fopen=2, fnigh=2)
    assert len(zia_plan.get_agenda_dict()) == 0
    zia_plan.add_fact(fcontext=day_rope, fstate=day_rope, fopen=400, fnigh=400)
    assert len(zia_plan.get_agenda_dict()) == 0
    zia_plan.add_fact(fcontext=day_rope, fstate=day_rope, fopen=401, fnigh=402)
    assert len(zia_plan.get_agenda_dict()) == 1
    # print(f"{run_concept._factheirs=}")
    print(f"{run_concept.factunits=}")

    # WHEN
    zia_plan.set_agenda_chore_complete(chore_rope=run_rope, rcontext=day_rope)

    # THEN
    print(f"{run_concept.factunits=}")
    # print(f"{run_concept._factheirs=}")
    assert len(zia_plan.get_agenda_dict()) == 0


def test_planunit_get_from_json_CorrectlyLoadsTaskFromJSON():
    # ESTABLISH
    yao_plan_json = planunit_v001().get_json()

    # WHEN
    yao_plan = planunit_get_from_json(x_plan_json=yao_plan_json)

    # THEN
    assert len(yao_plan.get_concept_dict()) == 252
    print(f"{len(yao_plan.get_concept_dict())=}")
    casa_str = "casa"
    casa_rope = yao_plan.make_l1_rope(casa_str)
    body_str = "exercise"
    body_rope = yao_plan.make_rope(casa_rope, body_str)
    veg_str = "cook veggies every morning"
    veg_rope = yao_plan.make_rope(body_rope, veg_str)
    veg_concept = yao_plan.get_concept_obj(veg_rope)
    assert not veg_concept._active
    assert veg_concept.task

    # concept_list = yao_plan.get_concept_dict()
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
    day_min_rope = yao_plan.make_l1_rope(day_min_str)
    yao_plan.add_fact(fcontext=day_min_rope, fstate=day_min_rope, fopen=0, fnigh=1399)

    # THEN
    assert len(yao_plan.get_agenda_dict()) > 0


def test_PlanUnit_set_fact_Isue116Resolved_correctlySetsChoreAsTrue():
    # ESTABLISH
    yao_plan = planunit_v002()
    print(f"{yao_plan.get_reason_rcontexts()=}")

    assert len(yao_plan.get_agenda_dict()) == 44
    time_rope = yao_plan.make_l1_rope("time")
    gregtime_rope = yao_plan.make_rope(time_rope, "gregtime")

    # WHEN
    yao_plan.add_fact(gregtime_rope, gregtime_rope, fopen=1063998720, fnigh=1064130373)
    task_concept_list = yao_plan.get_agenda_dict()

    # THEN
    assert len(task_concept_list) == 66
    db_rope = yao_plan.make_l1_rope("D&B")
    evening_str = "late_evening_go_to_sleep"
    evening_rope = yao_plan.make_rope(db_rope, evening_str)
    evening_concept = yao_plan._concept_dict.get(evening_rope)
    # for concept_x in yao_plan.get_agenda_dict():
    #     # if concept_x._chore != True:
    #     #     print(f"{len(task_concept_list)=} {concept_x._chore=} {concept_x.get_concept_rope()}")
    #     if concept_x.concept_label == evening_concept_label:
    #         evening_concept = concept_x
    #         print(f"{concept_x.get_concept_rope()=}")

    print(f"\nConcept = '{evening_str}' and reason '{gregtime_rope}'")
    factheir_gregtime = evening_concept._factheirs.get(gregtime_rope)
    print(f"\n{factheir_gregtime=}")

    # for reasonheir in agenda_concept._reasonheirs.values():
    #     print(f"{reasonheir.rcontext=} {reasonheir._status=} {reasonheir._chore=}")
    reasonheir_gregtime = evening_concept._reasonheirs.get(gregtime_rope)
    reasonheir_str = f"\nreasonheir_gregtime= '{reasonheir_gregtime.rcontext}', status={reasonheir_gregtime._status}, chore={reasonheir_gregtime._chore}"
    print(reasonheir_str)

    premiseunit = reasonheir_gregtime.premises.get(gregtime_rope)
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


def test_PlanUnit_agenda_IsSetByLaborUnit_1AcctGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    casa_str = "casa"
    casa_rope = yao_plan.make_l1_rope(casa_str)
    yao_plan.set_l1_concept(conceptunit_shop(casa_str, task=True))
    assert len(yao_plan.get_agenda_dict()) == 1

    sue_str = "Sue"
    yao_plan.add_acctunit(sue_str)
    laborunit_sue = laborunit_shop()
    laborunit_sue.set_laborlink(labor_title=sue_str)
    assert len(yao_plan.get_agenda_dict()) == 1

    # WHEN
    yao_plan.edit_concept_attr(casa_rope, laborunit=laborunit_sue)

    # THEN
    assert len(yao_plan.get_agenda_dict()) == 0

    # WHEN
    yao_plan.add_acctunit(yao_str)
    laborunit_yao = laborunit_shop()
    laborunit_yao.set_laborlink(labor_title=yao_str)

    # WHEN
    yao_plan.edit_concept_attr(casa_rope, laborunit=laborunit_yao)

    # THEN
    assert len(yao_plan.get_agenda_dict()) == 1

    # agenda_dict = yao_plan.get_agenda_dict()
    # print(f"{agenda_dict[0].concept_label=}")


def test_PlanUnit_get_agenda_dict_IsSetByLaborUnit_2AcctGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    yao_plan.add_acctunit(yao_str)
    casa_str = "casa"
    casa_rope = yao_plan.make_l1_rope(casa_str)
    yao_plan.set_l1_concept(conceptunit_shop(casa_str, task=True))

    sue_str = "Sue"
    yao_plan.add_acctunit(sue_str)
    run_str = ";runners"
    sue_acctunit = yao_plan.get_acct(sue_str)
    sue_acctunit.add_membership(run_str)

    run_laborunit = laborunit_shop()
    run_laborunit.set_laborlink(labor_title=run_str)
    assert len(yao_plan.get_agenda_dict()) == 1

    # WHEN
    yao_plan.edit_concept_attr(casa_rope, laborunit=run_laborunit)

    # THEN
    assert len(yao_plan.get_agenda_dict()) == 0

    # WHEN
    yao_acctunit = yao_plan.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)

    # THEN
    assert len(yao_plan.get_agenda_dict()) == 1


def test_PlanUnit_get_all_tasks_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    zia_plan = planunit_shop(zia_str)
    casa_str = "casa"
    casa_rope = zia_plan.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = zia_plan.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = zia_plan.make_rope(clean_rope, sweep_str)
    couch_str = "couch"
    couch_rope = zia_plan.make_rope(casa_rope, couch_str)
    zia_plan.set_concept(conceptunit_shop(couch_str), casa_rope)
    zia_plan.set_concept(conceptunit_shop(clean_str, task=True), casa_rope)
    zia_plan.set_concept(conceptunit_shop(sweep_str, task=True), clean_rope)
    sweep_concept = zia_plan.get_concept_obj(sweep_rope)
    yao_str = "Yao"
    zia_plan.add_acctunit(yao_str)
    sweep_concept.laborunit.set_laborlink(yao_str)
    print(f"{sweep_concept}")
    agenda_dict = zia_plan.get_agenda_dict()
    assert agenda_dict.get(clean_rope) is not None
    assert agenda_dict.get(sweep_rope) is None
    assert agenda_dict.get(couch_rope) is None

    # WHEN
    all_tasks_dict = zia_plan.get_all_tasks()

    # THEN
    assert all_tasks_dict.get(sweep_rope) == zia_plan.get_concept_obj(sweep_rope)
    assert all_tasks_dict.get(clean_rope) == zia_plan.get_concept_obj(clean_rope)
    assert all_tasks_dict.get(couch_rope) is None
