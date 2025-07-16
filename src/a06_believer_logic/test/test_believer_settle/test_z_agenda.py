from src.a01_term_logic.rope import RopeTerm
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_plan_logic.plan import PlanUnit, planunit_shop
from src.a06_believer_logic.believer import (
    believerunit_shop,
    get_from_json as believerunit_get_from_json,
)
from src.a06_believer_logic.test._util.example_believers import (
    believerunit_v001,
    believerunit_v001_with_large_agenda,
    believerunit_v002,
    get_believerunit_with7amCleanTableReason,
    get_believerunit_with_4_levels,
    get_believerunit_with_4_levels_and_2reasons,
    get_believerunit_with_4_levels_and_2reasons_2facts,
)


def get_chores_count(agenda_dict: dict[RopeTerm, PlanUnit]) -> int:
    return sum(bool(x_planunit._chore) for x_planunit in agenda_dict.values())


def test_BelieverUnit_get_agenda_dict_ReturnsObj_WithTwoPlans():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()

    # WHEN
    agenda_dict = sue_believer.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    print(f"{agenda_dict.keys()=}")
    assert sue_believer.make_l1_rope("casa") in agenda_dict.keys()
    assert sue_believer.make_l1_rope("cat have dinner") in agenda_dict.keys()


def test_BelieverUnit_get_agenda_dict_ReturnsAgendaWithOnlyCorrectPlans():
    # ESTABLISH
    x_believer = get_believerunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_rope = x_believer.make_l1_rope(wk_str)
    sun_str = "Sunday"
    sun_rope = x_believer.make_rope(wk_rope, sun_str)
    x_believer.add_fact(f_context=wk_rope, f_state=sun_rope)

    # WHEN
    agenda_dict = x_believer.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    print(f"{agenda_dict=}")
    assert x_believer.make_l1_rope("cat have dinner") in agenda_dict.keys()


def test_BelieverUnit_get_agenda_dict_WithLargeBeliever_fund():
    # ESTABLISH
    x_believer = get_believerunit_with_4_levels_and_2reasons_2facts()

    # WHEN
    agenda_dict = x_believer.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    assert agenda_dict.get(x_believer.make_l1_rope("cat have dinner"))._fund_ratio

    casa_str = "casa"
    print(f"{agenda_dict.keys()=} {x_believer.make_l1_rope(casa_str)=}")
    print(f"{agenda_dict.get(x_believer.make_l1_rope(casa_str)).plan_label=}")
    assert agenda_dict.get(x_believer.make_l1_rope(casa_str))._fund_ratio


def test_BelieverUnit_get_agenda_dict_WithNo7amPlanExample():
    # ESTABLISH
    x_believer = get_believerunit_with7amCleanTableReason()

    # WHEN
    agenda_dict = x_believer.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    clean_str = "clean table"
    print(f"{agenda_dict.keys()=} {x_believer.make_l1_rope(clean_str)=}")
    # print(f"{agenda_dict[0].plan_label=}")
    assert len(agenda_dict) == 1

    cat_str = "cat have dinner"
    cat_agenda_plan = agenda_dict.get(x_believer.make_l1_rope(cat_str))
    assert cat_agenda_plan.plan_label != clean_str


def test_BelieverUnit_get_agenda_dict_With7amPlanExample():
    # ESTABLISH
    # set facts as midevening to 8am
    x_believer = get_believerunit_with7amCleanTableReason()
    print(f"{len(x_believer.get_agenda_dict())=}")
    assert len(x_believer.get_agenda_dict()) == 1
    timetech_rope = x_believer.make_l1_rope("timetech")
    day24hr_rope = x_believer.make_rope(timetech_rope, "24hr day")
    day24hr_r_lower = 0.0
    day24hr_r_upper = 8.0
    housemanagement_str = "housemanagement"
    housemanagement_rope = x_believer.make_l1_rope(housemanagement_str)
    clean_str = "clean table"
    clean_rope = x_believer.make_rope(housemanagement_rope, clean_str)

    # WHEN
    x_believer.add_fact(
        day24hr_rope, day24hr_rope, day24hr_r_lower, day24hr_r_upper, True
    )

    # THEN
    print(x_believer.planroot.factunits[day24hr_rope])
    print(x_believer.get_plan_obj(clean_rope).reasonunits)
    print(x_believer.get_plan_obj(clean_rope)._active)
    agenda_dict = x_believer.get_agenda_dict()
    print(f"{len(agenda_dict)=} {agenda_dict.keys()=}")
    assert len(agenda_dict) == 6
    clean_plan = agenda_dict.get(clean_rope)
    assert clean_plan.plan_label == clean_str


def test_believerunit_v001_AgendaExists():
    # ESTABLISH
    yao_believer = believerunit_v001()
    min_str = "day_minute"
    min_rope = yao_believer.make_l1_rope(min_str)
    yao_believer.add_fact(f_context=min_rope, f_state=min_rope, f_lower=0, f_upper=1399)
    assert yao_believer
    # for plan_kid in yao_believer.planroot._kids.values():
    #     # print(plan_kid.plan_label)
    #     assert str(type(plan_kid)) != "<class 'str'>"
    #     assert plan_kid.task is not None

    # WHEN
    agenda_dict = yao_believer.get_agenda_dict()

    # THEN
    assert len(agenda_dict) > 0
    assert len(agenda_dict) == 17
    # assert agenda_dict[0].task is not None
    # assert str(type(agenda_dict[0])) != "<class 'str'>"
    # assert str(type(agenda_dict[9])) != "<class 'str'>"
    # assert str(type(agenda_dict[12])) != "<class 'str'>"


def test_BelieverUnit_get_agenda_dict_BelieverUnitHasCorrectAttributes_believerunit_v001():
    # ESTABLISH
    yao_believer = believerunit_v001()

    day_min_str = "day_minute"
    day_min_rope = yao_believer.make_l1_rope(day_min_str)
    yao_believer.add_fact(
        f_context=day_min_rope, f_state=day_min_rope, f_lower=0, f_upper=1399
    )
    month_wk_str = "month_wk"
    month_wk_rope = yao_believer.make_l1_rope(month_wk_str)
    nations_str = "Nation-States"
    nations_rope = yao_believer.make_l1_rope(nations_str)
    mood_str = "Moods"
    mood_rope = yao_believer.make_l1_rope(mood_str)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_believer.make_l1_rope(aaron_str)
    # interweb_str = "Interweb"
    # interweb_rope = yao_believer.make_l1_rope(interweb_str)
    yr_month_str = "yr_month"
    yr_month_rope = yao_believer.make_l1_rope(yr_month_str)
    yao_believer.add_fact(f_context=month_wk_rope, f_state=month_wk_rope)
    yao_believer.add_fact(f_context=nations_rope, f_state=nations_rope)
    yao_believer.add_fact(f_context=mood_rope, f_state=mood_rope)
    yao_believer.add_fact(f_context=aaron_rope, f_state=aaron_rope)
    # yao_believer.add_fact(f_context=interweb_rope, f_state=interweb_rope)
    yao_believer.add_fact(f_context=yr_month_rope, f_state=yr_month_rope)
    # season_str = "Seasons"
    # season_rope = yao_believer.make_l1_rope(season_str)
    # yao_believer.add_fact(f_context=season_rope, f_state=season_rope)
    ced_wk_str = "ced_wk"
    ced_wk_rope = yao_believer.make_l1_rope(ced_wk_str)
    yao_believer.add_fact(f_context=ced_wk_rope, f_state=ced_wk_rope)
    # water_str = "WaterExistence"
    # water_rope = yao_believer.make_l1_rope(water_str)
    # yao_believer.add_fact(f_context=water_rope, f_state=water_rope)
    # movie_str = "No Movie playing"
    # movie_rope = yao_believer.make_l1_rope(movie_str)
    # yao_believer.add_fact(f_context=movie_rope, f_state=movie_str)

    # WHEN
    plan_task_list = yao_believer.get_agenda_dict()

    # THEN
    assert len(plan_task_list) == 27

    wk1_rope = yao_believer.make_rope(month_wk_rope, "1st wk")
    yao_believer.add_fact(month_wk_rope, wk1_rope)
    plan_task_list = yao_believer.get_agenda_dict()
    assert len(plan_task_list) == 27

    wkday_str = "wkdays"
    wkday_rope = yao_believer.make_l1_rope(wkday_str)
    monday_str = "Monday"
    monday_rope = yao_believer.make_rope(wkday_rope, monday_str)

    yao_believer.add_fact(f_context=wkday_rope, f_state=monday_rope)
    plan_task_list = yao_believer.get_agenda_dict()
    assert len(plan_task_list) == 39

    yao_believer.add_fact(f_context=wkday_rope, f_state=wkday_rope)
    plan_task_list = yao_believer.get_agenda_dict()
    assert len(plan_task_list) == 53

    # yao_believer.add_fact(f_context=nations_rope, f_state=nations_rope)
    # plan_task_list = yao_believer.get_agenda_dict()
    # assert len(plan_task_list) == 53

    # for r_context in yao_believer.get_missing_fact_r_contexts():
    #     print(f"{r_context=}")

    # for agenda_plan in plan_task_list:
    #     print(f"{agenda_plan._uid=} {agenda_plan.parent_rope=}")

    # for agenda_plan in plan_task_list:
    #     # print(f"{agenda_plan.parent_rope=}")
    #     pass

    print(len(plan_task_list))


def test_BelieverUnit_get_agenda_dict_BelieverUnitCanCleanOn_r_context_believerunit_v001_with_large_agenda():
    # ESTABLISH
    yao_believer = believerunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_rope = yao_believer.make_l1_rope(wk_str)
    print(f"{type(yao_believer)=}")
    # for r_context in yao_believer.get_missing_fact_r_contexts():
    #     print(f"{r_context=}")

    # for agenda_plan in yao_believer.get_agenda_dict():
    #     print(
    #         f"{agenda_plan.parent_rope=} {agenda_plan.plan_label} {len(agenda_plan.reasonunits)=}"
    #     )
    #     for reason in agenda_plan.reasonunits.values():
    #         if reason.r_context == wkdays:
    #             print(f"         {wkdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(yao_believer.get_agenda_dict()) == 63

    # WHEN
    task_list = yao_believer.get_agenda_dict(necessary_r_context=wk_rope)

    # THEN
    assert len(task_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(task_list) == 29


def test_BelieverUnit_set_agenda_chore_as_complete_SetsAttrCorrectly_Range():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")

    run_str = "run"
    run_rope = zia_believer.make_l1_rope(run_str)
    time_rope = zia_believer.make_l1_rope("time")
    day_str = "day"
    day_rope = zia_believer.make_rope(time_rope, day_str)

    zia_believer.set_l1_plan(planunit_shop(run_str, task=True))
    zia_believer.set_plan(planunit_shop(day_str, begin=0, close=500), time_rope)
    zia_believer.edit_plan_attr(
        run_rope,
        reason_r_context=day_rope,
        reason_case=day_rope,
        r_lower=25,
        reason_r_upper=81,
    )
    zia_believer.add_fact(f_context=day_rope, f_state=day_rope, f_lower=30, f_upper=87)
    zia_believer.get_agenda_dict()
    run_reasonunits = zia_believer.planroot._kids[run_str].reasonunits[day_rope]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.cases[day_rope]._status=}")
    print(f"{run_reasonunits.cases[day_rope]._chore=}")
    print(f"{zia_believer.get_reason_r_contexts()=}")
    assert len(zia_believer.get_plan_dict()) == 4
    assert len(zia_believer.get_agenda_dict()) == 1
    print(f"{zia_believer.get_agenda_dict().keys()=}")
    assert zia_believer.get_agenda_dict().get(run_rope)._chore is True

    # WHEN
    zia_believer.set_agenda_chore_complete(chore_rope=run_rope, r_context=day_rope)

    # THEN
    agenda_dict = zia_believer.get_agenda_dict()
    assert len(agenda_dict) == 0
    assert agenda_dict == {}


def test_BelieverUnit_set_agenda_chore_as_complete_SetsAttrCorrectly_Division():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")

    run_str = "run"
    run_rope = zia_believer.make_l1_rope(run_str)
    time_str = "time"
    time_rope = zia_believer.make_l1_rope(time_str)
    day_str = "day"
    day_rope = zia_believer.make_rope(time_rope, day_str)

    zia_believer.set_l1_plan(planunit_shop(run_str, task=True))
    zia_believer.set_plan(planunit_shop(day_str, begin=0, close=500), time_rope)
    zia_believer.edit_plan_attr(
        run_rope,
        reason_r_context=day_rope,
        reason_case=day_rope,
        r_lower=1,
        reason_r_upper=1,
        r_divisor=2,
    )

    run_plan = zia_believer.get_plan_obj(run_rope)
    # print(f"{run_plan._factheirs=}")
    zia_believer.add_fact(f_context=day_rope, f_state=day_rope, f_lower=1, f_upper=2)
    assert len(zia_believer.get_agenda_dict()) == 1
    zia_believer.add_fact(f_context=day_rope, f_state=day_rope, f_lower=2, f_upper=2)
    assert len(zia_believer.get_agenda_dict()) == 0
    zia_believer.add_fact(
        f_context=day_rope, f_state=day_rope, f_lower=400, f_upper=400
    )
    assert len(zia_believer.get_agenda_dict()) == 0
    zia_believer.add_fact(
        f_context=day_rope, f_state=day_rope, f_lower=401, f_upper=402
    )
    assert len(zia_believer.get_agenda_dict()) == 1
    # print(f"{run_plan._factheirs=}")
    print(f"{run_plan.factunits=}")

    # WHEN
    zia_believer.set_agenda_chore_complete(chore_rope=run_rope, r_context=day_rope)

    # THEN
    print(f"{run_plan.factunits=}")
    # print(f"{run_plan._factheirs=}")
    assert len(zia_believer.get_agenda_dict()) == 0


def test_believerunit_get_from_json_CorrectlyLoadsTaskFromJSON():
    # ESTABLISH
    yao_believer_json = believerunit_v001().get_json()

    # WHEN
    yao_believer = believerunit_get_from_json(x_believer_json=yao_believer_json)

    # THEN
    assert len(yao_believer.get_plan_dict()) == 252
    print(f"{len(yao_believer.get_plan_dict())=}")
    casa_str = "casa"
    casa_rope = yao_believer.make_l1_rope(casa_str)
    body_str = "exercise"
    body_rope = yao_believer.make_rope(casa_rope, body_str)
    veg_str = "cook veggies every morning"
    veg_rope = yao_believer.make_rope(body_rope, veg_str)
    veg_plan = yao_believer.get_plan_obj(veg_rope)
    assert not veg_plan._active
    assert veg_plan.task

    # plan_list = yao_believer.get_plan_dict()
    # task_true_count = 0
    # for plan in plan_list:
    #     if str(type(plan)).find(".plan.PlanUnit'>") > 0:
    #         assert plan._active in (True, False)
    #     assert plan.task in (True, False)
    #     # if plan._active:
    #     #     print(plan.plan_label)
    #     if plan.task:
    #         task_true_count += 1
    #         # if plan.task is False:
    #         #     print(f"task is false {plan.plan_label}")
    #         # for reason in plan.reasonunits.values():
    #         #     assert reason._status in (True, False)
    # assert task_true_count > 0

    # WHEN
    day_min_str = "day_minute"
    day_min_rope = yao_believer.make_l1_rope(day_min_str)
    yao_believer.add_fact(
        f_context=day_min_rope, f_state=day_min_rope, f_lower=0, f_upper=1399
    )

    # THEN
    assert len(yao_believer.get_agenda_dict()) > 0


def test_BelieverUnit_set_fact_Isue116Resolved_SetsChoreAsTrue():
    # ESTABLISH
    yao_believer = believerunit_v002()
    print(f"{yao_believer.get_reason_r_contexts()=}")

    assert len(yao_believer.get_agenda_dict()) == 44
    time_rope = yao_believer.make_l1_rope("time")
    gregtime_rope = yao_believer.make_rope(time_rope, "gregtime")

    # WHEN
    yao_believer.add_fact(
        gregtime_rope, gregtime_rope, f_lower=1063998720, f_upper=1064130373
    )
    task_plan_list = yao_believer.get_agenda_dict()

    # THEN
    assert len(task_plan_list) == 66
    db_rope = yao_believer.make_l1_rope("D&B")
    evening_str = "late_evening_go_to_sleep"
    evening_rope = yao_believer.make_rope(db_rope, evening_str)
    evening_plan = yao_believer._plan_dict.get(evening_rope)
    # for plan_x in yao_believer.get_agenda_dict():
    #     # if plan_x._chore != True:
    #     #     print(f"{len(task_plan_list)=} {plan_x._chore=} {plan_x.get_plan_rope()}")
    #     if plan_x.plan_label == evening_plan_label:
    #         evening_plan = plan_x
    #         print(f"{plan_x.get_plan_rope()=}")

    print(f"\nPlan = '{evening_str}' and reason '{gregtime_rope}'")
    factheir_gregtime = evening_plan._factheirs.get(gregtime_rope)
    print(f"\n{factheir_gregtime=}")

    # for reasonheir in agenda_plan._reasonheirs.values():
    #     print(f"{reasonheir.r_context=} {reasonheir._status=} {reasonheir._chore=}")
    reasonheir_gregtime = evening_plan._reasonheirs.get(gregtime_rope)
    reasonheir_str = f"\nreasonheir_gregtime= '{reasonheir_gregtime.r_context}', status={reasonheir_gregtime._status}, chore={reasonheir_gregtime._chore}"
    print(reasonheir_str)

    caseunit = reasonheir_gregtime.cases.get(gregtime_rope)
    print(f"----\n {caseunit=}")
    print(f" {caseunit._get_chore_status(factheir=factheir_gregtime)=}")
    print(f" {caseunit._status=} , {caseunit._is_range()=} caseunit fails")
    print(f" {caseunit._status=} , {caseunit._is_segregate()=} caseunit passes")
    # segr_obj = casestatusfinder_shop(
    #     r_lower=caseunit.r_lower,
    #     r_upper=caseunit.r_upper,
    #     r_divisor=caseunit.r_divisor,
    #     f_lower_full=factheir_gregtime.r_lower,
    #     f_upper_full=factheir_gregtime.r_upper,
    # )
    # print(
    #     f"----\n  {segr_obj.r_lower=}  {segr_obj.r_upper=}  {segr_obj.r_divisor=}"
    # )
    # print(
    #     f"       {segr_obj.f_lower_full=}         {segr_obj.f_upper_full=} \tdifference:{segr_obj.f_upper_full-segr_obj.f_lower_full}"
    # )

    # print(f"  {segr_obj.get_active()=}  {segr_obj.get_chore_status()=}")
    assert get_chores_count(task_plan_list) == 64


def test_BelieverUnit_agenda_IsSetByLaborUnit_1PartnerGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_believer = believerunit_shop(yao_str)
    casa_str = "casa"
    casa_rope = yao_believer.make_l1_rope(casa_str)
    yao_believer.set_l1_plan(planunit_shop(casa_str, task=True))
    assert len(yao_believer.get_agenda_dict()) == 1

    sue_str = "Sue"
    yao_believer.add_partnerunit(sue_str)
    laborunit_sue = laborunit_shop()
    laborunit_sue.set_laborlink(labor_title=sue_str)
    assert len(yao_believer.get_agenda_dict()) == 1

    # WHEN
    yao_believer.edit_plan_attr(casa_rope, laborunit=laborunit_sue)

    # THEN
    assert len(yao_believer.get_agenda_dict()) == 0

    # WHEN
    yao_believer.add_partnerunit(yao_str)
    laborunit_yao = laborunit_shop()
    laborunit_yao.set_laborlink(labor_title=yao_str)

    # WHEN
    yao_believer.edit_plan_attr(casa_rope, laborunit=laborunit_yao)

    # THEN
    assert len(yao_believer.get_agenda_dict()) == 1

    # agenda_dict = yao_believer.get_agenda_dict()
    # print(f"{agenda_dict[0].plan_label=}")


def test_BelieverUnit_get_agenda_dict_IsSetByLaborUnit_2PartnerGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_believer = believerunit_shop(yao_str)
    yao_believer.add_partnerunit(yao_str)
    casa_str = "casa"
    casa_rope = yao_believer.make_l1_rope(casa_str)
    yao_believer.set_l1_plan(planunit_shop(casa_str, task=True))

    sue_str = "Sue"
    yao_believer.add_partnerunit(sue_str)
    run_str = ";runners"
    sue_partnerunit = yao_believer.get_partner(sue_str)
    sue_partnerunit.add_membership(run_str)

    run_laborunit = laborunit_shop()
    run_laborunit.set_laborlink(labor_title=run_str)
    assert len(yao_believer.get_agenda_dict()) == 1

    # WHEN
    yao_believer.edit_plan_attr(casa_rope, laborunit=run_laborunit)

    # THEN
    assert len(yao_believer.get_agenda_dict()) == 0

    # WHEN
    yao_partnerunit = yao_believer.get_partner(yao_str)
    yao_partnerunit.add_membership(run_str)

    # THEN
    assert len(yao_believer.get_agenda_dict()) == 1


def test_BelieverUnit_get_all_tasks_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    zia_believer = believerunit_shop(zia_str)
    casa_str = "casa"
    casa_rope = zia_believer.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = zia_believer.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = zia_believer.make_rope(clean_rope, sweep_str)
    couch_str = "couch"
    couch_rope = zia_believer.make_rope(casa_rope, couch_str)
    zia_believer.set_plan(planunit_shop(couch_str), casa_rope)
    zia_believer.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    zia_believer.set_plan(planunit_shop(sweep_str, task=True), clean_rope)
    sweep_plan = zia_believer.get_plan_obj(sweep_rope)
    yao_str = "Yao"
    zia_believer.add_partnerunit(yao_str)
    sweep_plan.laborunit.set_laborlink(yao_str)
    print(f"{sweep_plan}")
    agenda_dict = zia_believer.get_agenda_dict()
    assert agenda_dict.get(clean_rope) is not None
    assert agenda_dict.get(sweep_rope) is None
    assert agenda_dict.get(couch_rope) is None

    # WHEN
    all_tasks_dict = zia_believer.get_all_tasks()

    # THEN
    assert all_tasks_dict.get(sweep_rope) == zia_believer.get_plan_obj(sweep_rope)
    assert all_tasks_dict.get(clean_rope) == zia_believer.get_plan_obj(clean_rope)
    assert all_tasks_dict.get(couch_rope) is None
