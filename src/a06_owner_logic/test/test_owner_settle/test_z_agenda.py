from src.a01_term_logic.rope import RopeTerm
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_plan_logic.plan import PlanUnit, planunit_shop
from src.a06_owner_logic.owner import (
    get_from_json as ownerunit_get_from_json,
    ownerunit_shop,
)
from src.a06_owner_logic.test._util.example_owners import (
    get_ownerunit_with7amCleanTableReason,
    get_ownerunit_with_4_levels,
    get_ownerunit_with_4_levels_and_2reasons,
    get_ownerunit_with_4_levels_and_2reasons_2facts,
    ownerunit_v001,
    ownerunit_v001_with_large_agenda,
    ownerunit_v002,
)


def get_chores_count(agenda_dict: dict[RopeTerm, PlanUnit]) -> int:
    return sum(bool(x_planunit._chore) for x_planunit in agenda_dict.values())


def test_OwnerUnit_get_agenda_dict_ReturnsObj_WithTwoPlans():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels()

    # WHEN
    agenda_dict = sue_owner.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    print(f"{agenda_dict.keys()=}")
    assert sue_owner.make_l1_rope("casa") in agenda_dict.keys()
    assert sue_owner.make_l1_rope("cat have dinner") in agenda_dict.keys()


def test_OwnerUnit_get_agenda_dict_ReturnsAgendaWithOnlyCorrectPlans():
    # ESTABLISH
    x_owner = get_ownerunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_rope = x_owner.make_l1_rope(wk_str)
    sun_str = "Sunday"
    sun_rope = x_owner.make_rope(wk_rope, sun_str)
    x_owner.add_fact(fcontext=wk_rope, fstate=sun_rope)

    # WHEN
    agenda_dict = x_owner.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    print(f"{agenda_dict=}")
    assert x_owner.make_l1_rope("cat have dinner") in agenda_dict.keys()


def test_OwnerUnit_get_agenda_dict_WithLargeOwner_fund():
    # ESTABLISH
    x_owner = get_ownerunit_with_4_levels_and_2reasons_2facts()

    # WHEN
    agenda_dict = x_owner.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 2
    assert agenda_dict.get(x_owner.make_l1_rope("cat have dinner"))._fund_ratio

    casa_str = "casa"
    print(f"{agenda_dict.keys()=} {x_owner.make_l1_rope(casa_str)=}")
    print(f"{agenda_dict.get(x_owner.make_l1_rope(casa_str)).plan_label=}")
    assert agenda_dict.get(x_owner.make_l1_rope(casa_str))._fund_ratio


def test_OwnerUnit_get_agenda_dict_WithNo7amPlanExample():
    # ESTABLISH
    x_owner = get_ownerunit_with7amCleanTableReason()

    # WHEN
    agenda_dict = x_owner.get_agenda_dict()

    # THEN
    assert agenda_dict
    assert len(agenda_dict) == 1
    clean_str = "clean table"
    print(f"{agenda_dict.keys()=} {x_owner.make_l1_rope(clean_str)=}")
    # print(f"{agenda_dict[0].plan_label=}")
    assert len(agenda_dict) == 1

    cat_str = "cat have dinner"
    cat_agenda_plan = agenda_dict.get(x_owner.make_l1_rope(cat_str))
    assert cat_agenda_plan.plan_label != clean_str


def test_OwnerUnit_get_agenda_dict_With7amPlanExample():
    # ESTABLISH
    # set facts as midevening to 8am
    x_owner = get_ownerunit_with7amCleanTableReason()
    print(f"{len(x_owner.get_agenda_dict())=}")
    assert len(x_owner.get_agenda_dict()) == 1
    timetech_rope = x_owner.make_l1_rope("timetech")
    day24hr_rope = x_owner.make_rope(timetech_rope, "24hr day")
    day24hr_popen = 0.0
    day24hr_pnigh = 8.0
    housemanagement_str = "housemanagement"
    housemanagement_rope = x_owner.make_l1_rope(housemanagement_str)
    clean_str = "clean table"
    clean_rope = x_owner.make_rope(housemanagement_rope, clean_str)

    # WHEN
    x_owner.add_fact(day24hr_rope, day24hr_rope, day24hr_popen, day24hr_pnigh, True)

    # THEN
    print(x_owner.planroot.factunits[day24hr_rope])
    print(x_owner.get_plan_obj(clean_rope).reasonunits)
    print(x_owner.get_plan_obj(clean_rope)._active)
    agenda_dict = x_owner.get_agenda_dict()
    print(f"{len(agenda_dict)=} {agenda_dict.keys()=}")
    assert len(agenda_dict) == 6
    clean_plan = agenda_dict.get(clean_rope)
    assert clean_plan.plan_label == clean_str


def test_ownerunit_v001_AgendaExists():
    # ESTABLISH
    yao_owner = ownerunit_v001()
    min_str = "day_minute"
    min_rope = yao_owner.make_l1_rope(min_str)
    yao_owner.add_fact(fcontext=min_rope, fstate=min_rope, fopen=0, fnigh=1399)
    assert yao_owner
    # for plan_kid in yao_owner.planroot._kids.values():
    #     # print(plan_kid.plan_label)
    #     assert str(type(plan_kid)) != "<class 'str'>"
    #     assert plan_kid.task is not None

    # WHEN
    agenda_dict = yao_owner.get_agenda_dict()

    # THEN
    assert len(agenda_dict) > 0
    assert len(agenda_dict) == 17
    # assert agenda_dict[0].task is not None
    # assert str(type(agenda_dict[0])) != "<class 'str'>"
    # assert str(type(agenda_dict[9])) != "<class 'str'>"
    # assert str(type(agenda_dict[12])) != "<class 'str'>"


def test_OwnerUnit_get_agenda_dict_OwnerUnitHasCorrectAttributes_ownerunit_v001():
    # ESTABLISH
    yao_owner = ownerunit_v001()

    day_min_str = "day_minute"
    day_min_rope = yao_owner.make_l1_rope(day_min_str)
    yao_owner.add_fact(fcontext=day_min_rope, fstate=day_min_rope, fopen=0, fnigh=1399)
    month_wk_str = "month_wk"
    month_wk_rope = yao_owner.make_l1_rope(month_wk_str)
    nations_str = "Nation-States"
    nations_rope = yao_owner.make_l1_rope(nations_str)
    mood_str = "Moods"
    mood_rope = yao_owner.make_l1_rope(mood_str)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_owner.make_l1_rope(aaron_str)
    # interweb_str = "Interweb"
    # interweb_rope = yao_owner.make_l1_rope(interweb_str)
    yr_month_str = "yr_month"
    yr_month_rope = yao_owner.make_l1_rope(yr_month_str)
    yao_owner.add_fact(fcontext=month_wk_rope, fstate=month_wk_rope)
    yao_owner.add_fact(fcontext=nations_rope, fstate=nations_rope)
    yao_owner.add_fact(fcontext=mood_rope, fstate=mood_rope)
    yao_owner.add_fact(fcontext=aaron_rope, fstate=aaron_rope)
    # yao_owner.add_fact(fcontext=interweb_rope, fstate=interweb_rope)
    yao_owner.add_fact(fcontext=yr_month_rope, fstate=yr_month_rope)
    # season_str = "Seasons"
    # season_rope = yao_owner.make_l1_rope(season_str)
    # yao_owner.add_fact(fcontext=season_rope, fstate=season_rope)
    ced_wk_str = "ced_wk"
    ced_wk_rope = yao_owner.make_l1_rope(ced_wk_str)
    yao_owner.add_fact(fcontext=ced_wk_rope, fstate=ced_wk_rope)
    # water_str = "WaterExistence"
    # water_rope = yao_owner.make_l1_rope(water_str)
    # yao_owner.add_fact(fcontext=water_rope, fstate=water_rope)
    # movie_str = "No Movie playing"
    # movie_rope = yao_owner.make_l1_rope(movie_str)
    # yao_owner.add_fact(fcontext=movie_rope, fstate=movie_str)

    # WHEN
    plan_task_list = yao_owner.get_agenda_dict()

    # THEN
    assert len(plan_task_list) == 27

    wk1_rope = yao_owner.make_rope(month_wk_rope, "1st wk")
    yao_owner.add_fact(month_wk_rope, wk1_rope)
    plan_task_list = yao_owner.get_agenda_dict()
    assert len(plan_task_list) == 27

    wkday_str = "wkdays"
    wkday_rope = yao_owner.make_l1_rope(wkday_str)
    monday_str = "Monday"
    monday_rope = yao_owner.make_rope(wkday_rope, monday_str)

    yao_owner.add_fact(fcontext=wkday_rope, fstate=monday_rope)
    plan_task_list = yao_owner.get_agenda_dict()
    assert len(plan_task_list) == 39

    yao_owner.add_fact(fcontext=wkday_rope, fstate=wkday_rope)
    plan_task_list = yao_owner.get_agenda_dict()
    assert len(plan_task_list) == 53

    # yao_owner.add_fact(fcontext=nations_rope, fstate=nations_rope)
    # plan_task_list = yao_owner.get_agenda_dict()
    # assert len(plan_task_list) == 53

    # for rcontext in yao_owner.get_missing_fact_rcontexts():
    #     print(f"{rcontext=}")

    # for agenda_plan in plan_task_list:
    #     print(f"{agenda_plan._uid=} {agenda_plan.parent_rope=}")

    # for agenda_plan in plan_task_list:
    #     # print(f"{agenda_plan.parent_rope=}")
    #     pass

    print(len(plan_task_list))


def test_OwnerUnit_get_agenda_dict_OwnerUnitCanCleanOn_Rcontext_ownerunit_v001_with_large_agenda():
    # ESTABLISH
    yao_owner = ownerunit_v001_with_large_agenda()
    wk_str = "wkdays"
    wk_rope = yao_owner.make_l1_rope(wk_str)
    print(f"{type(yao_owner)=}")
    # for rcontext in yao_owner.get_missing_fact_rcontexts():
    #     print(f"{rcontext=}")

    # for agenda_plan in yao_owner.get_agenda_dict():
    #     print(
    #         f"{agenda_plan.parent_rope=} {agenda_plan.plan_label} {len(agenda_plan.reasonunits)=}"
    #     )
    #     for reason in agenda_plan.reasonunits.values():
    #         if reason.rcontext == wkdays:
    #             print(f"         {wkdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(yao_owner.get_agenda_dict()) == 63

    # WHEN
    task_list = yao_owner.get_agenda_dict(necessary_rcontext=wk_rope)

    # THEN
    assert len(task_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(task_list) == 29


def test_OwnerUnit_set_agenda_chore_as_complete_SetsAttrCorrectly_Range():
    # ESTABLISH
    zia_owner = ownerunit_shop("Zia")

    run_str = "run"
    run_rope = zia_owner.make_l1_rope(run_str)
    time_rope = zia_owner.make_l1_rope("time")
    day_str = "day"
    day_rope = zia_owner.make_rope(time_rope, day_str)

    zia_owner.set_l1_plan(planunit_shop(run_str, task=True))
    zia_owner.set_plan(planunit_shop(day_str, begin=0, close=500), time_rope)
    zia_owner.edit_plan_attr(
        run_rope,
        reason_rcontext=day_rope,
        reason_premise=day_rope,
        popen=25,
        reason_pnigh=81,
    )
    zia_owner.add_fact(fcontext=day_rope, fstate=day_rope, fopen=30, fnigh=87)
    zia_owner.get_agenda_dict()
    run_reasonunits = zia_owner.planroot._kids[run_str].reasonunits[day_rope]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_rope]._status=}")
    print(f"{run_reasonunits.premises[day_rope]._chore=}")
    print(f"{zia_owner.get_reason_rcontexts()=}")
    assert len(zia_owner.get_plan_dict()) == 4
    assert len(zia_owner.get_agenda_dict()) == 1
    print(f"{zia_owner.get_agenda_dict().keys()=}")
    assert zia_owner.get_agenda_dict().get(run_rope)._chore is True

    # WHEN
    zia_owner.set_agenda_chore_complete(chore_rope=run_rope, rcontext=day_rope)

    # THEN
    agenda_dict = zia_owner.get_agenda_dict()
    assert len(agenda_dict) == 0
    assert agenda_dict == {}


def test_OwnerUnit_set_agenda_chore_as_complete_SetsAttrCorrectly_Division():
    # ESTABLISH
    zia_owner = ownerunit_shop("Zia")

    run_str = "run"
    run_rope = zia_owner.make_l1_rope(run_str)
    time_str = "time"
    time_rope = zia_owner.make_l1_rope(time_str)
    day_str = "day"
    day_rope = zia_owner.make_rope(time_rope, day_str)

    zia_owner.set_l1_plan(planunit_shop(run_str, task=True))
    zia_owner.set_plan(planunit_shop(day_str, begin=0, close=500), time_rope)
    zia_owner.edit_plan_attr(
        run_rope,
        reason_rcontext=day_rope,
        reason_premise=day_rope,
        popen=1,
        reason_pnigh=1,
        pdivisor=2,
    )

    run_plan = zia_owner.get_plan_obj(run_rope)
    # print(f"{run_plan._factheirs=}")
    zia_owner.add_fact(fcontext=day_rope, fstate=day_rope, fopen=1, fnigh=2)
    assert len(zia_owner.get_agenda_dict()) == 1
    zia_owner.add_fact(fcontext=day_rope, fstate=day_rope, fopen=2, fnigh=2)
    assert len(zia_owner.get_agenda_dict()) == 0
    zia_owner.add_fact(fcontext=day_rope, fstate=day_rope, fopen=400, fnigh=400)
    assert len(zia_owner.get_agenda_dict()) == 0
    zia_owner.add_fact(fcontext=day_rope, fstate=day_rope, fopen=401, fnigh=402)
    assert len(zia_owner.get_agenda_dict()) == 1
    # print(f"{run_plan._factheirs=}")
    print(f"{run_plan.factunits=}")

    # WHEN
    zia_owner.set_agenda_chore_complete(chore_rope=run_rope, rcontext=day_rope)

    # THEN
    print(f"{run_plan.factunits=}")
    # print(f"{run_plan._factheirs=}")
    assert len(zia_owner.get_agenda_dict()) == 0


def test_ownerunit_get_from_json_CorrectlyLoadsTaskFromJSON():
    # ESTABLISH
    yao_owner_json = ownerunit_v001().get_json()

    # WHEN
    yao_owner = ownerunit_get_from_json(x_owner_json=yao_owner_json)

    # THEN
    assert len(yao_owner.get_plan_dict()) == 252
    print(f"{len(yao_owner.get_plan_dict())=}")
    casa_str = "casa"
    casa_rope = yao_owner.make_l1_rope(casa_str)
    body_str = "exercise"
    body_rope = yao_owner.make_rope(casa_rope, body_str)
    veg_str = "cook veggies every morning"
    veg_rope = yao_owner.make_rope(body_rope, veg_str)
    veg_plan = yao_owner.get_plan_obj(veg_rope)
    assert not veg_plan._active
    assert veg_plan.task

    # plan_list = yao_owner.get_plan_dict()
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
    day_min_rope = yao_owner.make_l1_rope(day_min_str)
    yao_owner.add_fact(fcontext=day_min_rope, fstate=day_min_rope, fopen=0, fnigh=1399)

    # THEN
    assert len(yao_owner.get_agenda_dict()) > 0


def test_OwnerUnit_set_fact_Isue116Resolved_correctlySetsChoreAsTrue():
    # ESTABLISH
    yao_owner = ownerunit_v002()
    print(f"{yao_owner.get_reason_rcontexts()=}")

    assert len(yao_owner.get_agenda_dict()) == 44
    time_rope = yao_owner.make_l1_rope("time")
    gregtime_rope = yao_owner.make_rope(time_rope, "gregtime")

    # WHEN
    yao_owner.add_fact(gregtime_rope, gregtime_rope, fopen=1063998720, fnigh=1064130373)
    task_plan_list = yao_owner.get_agenda_dict()

    # THEN
    assert len(task_plan_list) == 66
    db_rope = yao_owner.make_l1_rope("D&B")
    evening_str = "late_evening_go_to_sleep"
    evening_rope = yao_owner.make_rope(db_rope, evening_str)
    evening_plan = yao_owner._plan_dict.get(evening_rope)
    # for plan_x in yao_owner.get_agenda_dict():
    #     # if plan_x._chore != True:
    #     #     print(f"{len(task_plan_list)=} {plan_x._chore=} {plan_x.get_plan_rope()}")
    #     if plan_x.plan_label == evening_plan_label:
    #         evening_plan = plan_x
    #         print(f"{plan_x.get_plan_rope()=}")

    print(f"\nPlan = '{evening_str}' and reason '{gregtime_rope}'")
    factheir_gregtime = evening_plan._factheirs.get(gregtime_rope)
    print(f"\n{factheir_gregtime=}")

    # for reasonheir in agenda_plan._reasonheirs.values():
    #     print(f"{reasonheir.rcontext=} {reasonheir._status=} {reasonheir._chore=}")
    reasonheir_gregtime = evening_plan._reasonheirs.get(gregtime_rope)
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
    assert get_chores_count(task_plan_list) == 64


def test_OwnerUnit_agenda_IsSetByLaborUnit_1AcctGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    casa_str = "casa"
    casa_rope = yao_owner.make_l1_rope(casa_str)
    yao_owner.set_l1_plan(planunit_shop(casa_str, task=True))
    assert len(yao_owner.get_agenda_dict()) == 1

    sue_str = "Sue"
    yao_owner.add_acctunit(sue_str)
    laborunit_sue = laborunit_shop()
    laborunit_sue.set_laborlink(labor_title=sue_str)
    assert len(yao_owner.get_agenda_dict()) == 1

    # WHEN
    yao_owner.edit_plan_attr(casa_rope, laborunit=laborunit_sue)

    # THEN
    assert len(yao_owner.get_agenda_dict()) == 0

    # WHEN
    yao_owner.add_acctunit(yao_str)
    laborunit_yao = laborunit_shop()
    laborunit_yao.set_laborlink(labor_title=yao_str)

    # WHEN
    yao_owner.edit_plan_attr(casa_rope, laborunit=laborunit_yao)

    # THEN
    assert len(yao_owner.get_agenda_dict()) == 1

    # agenda_dict = yao_owner.get_agenda_dict()
    # print(f"{agenda_dict[0].plan_label=}")


def test_OwnerUnit_get_agenda_dict_IsSetByLaborUnit_2AcctGroup():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    yao_owner.add_acctunit(yao_str)
    casa_str = "casa"
    casa_rope = yao_owner.make_l1_rope(casa_str)
    yao_owner.set_l1_plan(planunit_shop(casa_str, task=True))

    sue_str = "Sue"
    yao_owner.add_acctunit(sue_str)
    run_str = ";runners"
    sue_acctunit = yao_owner.get_acct(sue_str)
    sue_acctunit.add_membership(run_str)

    run_laborunit = laborunit_shop()
    run_laborunit.set_laborlink(labor_title=run_str)
    assert len(yao_owner.get_agenda_dict()) == 1

    # WHEN
    yao_owner.edit_plan_attr(casa_rope, laborunit=run_laborunit)

    # THEN
    assert len(yao_owner.get_agenda_dict()) == 0

    # WHEN
    yao_acctunit = yao_owner.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)

    # THEN
    assert len(yao_owner.get_agenda_dict()) == 1


def test_OwnerUnit_get_all_tasks_ReturnsObj():
    # ESTABLISH
    zia_str = "Zia"
    zia_owner = ownerunit_shop(zia_str)
    casa_str = "casa"
    casa_rope = zia_owner.make_l1_rope(casa_str)
    clean_str = "clean"
    clean_rope = zia_owner.make_rope(casa_rope, clean_str)
    sweep_str = "sweep"
    sweep_rope = zia_owner.make_rope(clean_rope, sweep_str)
    couch_str = "couch"
    couch_rope = zia_owner.make_rope(casa_rope, couch_str)
    zia_owner.set_plan(planunit_shop(couch_str), casa_rope)
    zia_owner.set_plan(planunit_shop(clean_str, task=True), casa_rope)
    zia_owner.set_plan(planunit_shop(sweep_str, task=True), clean_rope)
    sweep_plan = zia_owner.get_plan_obj(sweep_rope)
    yao_str = "Yao"
    zia_owner.add_acctunit(yao_str)
    sweep_plan.laborunit.set_laborlink(yao_str)
    print(f"{sweep_plan}")
    agenda_dict = zia_owner.get_agenda_dict()
    assert agenda_dict.get(clean_rope) is not None
    assert agenda_dict.get(sweep_rope) is None
    assert agenda_dict.get(couch_rope) is None

    # WHEN
    all_tasks_dict = zia_owner.get_all_tasks()

    # THEN
    assert all_tasks_dict.get(sweep_rope) == zia_owner.get_plan_obj(sweep_rope)
    assert all_tasks_dict.get(clean_rope) == zia_owner.get_plan_obj(clean_rope)
    assert all_tasks_dict.get(couch_rope) is None
