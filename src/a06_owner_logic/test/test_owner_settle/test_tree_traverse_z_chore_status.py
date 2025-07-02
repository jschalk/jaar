from src.a01_term_logic.rope import to_rope
from src.a02_finance_logic.finance_config import default_fund_pool
from src.a04_reason_logic.reason_plan import (
    premiseunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.owner_graphics import display_plantree
from src.a06_owner_logic.test._util.example_owners import (
    from_list_get_active,
    get_ownerunit_with7amCleanTableReason,
    get_ownerunit_with_4_levels_and_2reasons,
    ownerunit_v001,
)


def test_OwnerUnit_settle_owner_SetsStatus_active_WhenFactSaysNo():
    # ESTABLISH
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_rope = sue_ownerunit.make_l1_rope(wk_str)
    sun_str = "Sunday"
    sun_rope = sue_ownerunit.make_rope(wk_rope, sun_str)

    # for plan in sue_ownerunit._plan_dict.values():
    #     print(f"{casa_rope=} {plan.get_plan_rope()=}")
    casa_str = "casa"
    casa_rope = sue_ownerunit.make_l1_rope(casa_str)
    assert sue_ownerunit.get_plan_obj(casa_rope)._active is None

    # WHEN
    sue_ownerunit.add_fact(fcontext=wk_rope, fstate=sun_rope)
    sue_ownerunit.settle_owner()

    # THEN
    assert sue_ownerunit._plan_dict != {}
    assert len(sue_ownerunit._plan_dict) == 17

    # for plan in sue_ownerunit._plan_dict.values():
    #     print(f"{casa_rope=} {plan.get_plan_rope()=}")
    assert sue_ownerunit.get_plan_obj(casa_rope)._active is False


def test_OwnerUnit_settle_owner_SetsStatus_active_WhenFactModifies():
    # ESTABLISH
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_rope = sue_ownerunit.make_l1_rope(wk_str)
    sun_str = "Wednesday"
    sun_rope = sue_ownerunit.make_rope(wk_rope, sun_str)
    casa_str = "casa"
    casa_rope = sue_ownerunit.make_l1_rope(casa_str)

    # WHEN
    sue_ownerunit.add_fact(fcontext=wk_rope, fstate=sun_rope)

    # THEN
    sue_ownerunit.settle_owner()
    assert sue_ownerunit._plan_dict
    assert len(sue_ownerunit._plan_dict) == 17
    assert sue_ownerunit._plan_dict.get(casa_rope)._active is False

    # WHEN
    nation_str = "nation"
    nation_rope = sue_ownerunit.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_ownerunit.make_rope(nation_rope, usa_str)
    sue_ownerunit.add_fact(fcontext=nation_rope, fstate=usa_rope)

    # THEN
    sue_ownerunit.settle_owner()
    assert sue_ownerunit._plan_dict
    assert len(sue_ownerunit._plan_dict) == 17
    assert sue_ownerunit._plan_dict.get(casa_rope)._active

    # WHEN
    france_str = "France"
    france_rope = sue_ownerunit.make_rope(nation_rope, france_str)
    sue_ownerunit.add_fact(fcontext=nation_rope, fstate=france_rope)

    # THEN
    sue_ownerunit.settle_owner()
    assert sue_ownerunit._plan_dict
    assert len(sue_ownerunit._plan_dict) == 17
    assert sue_ownerunit._plan_dict.get(casa_rope)._active is False


def test_OwnerUnit_settle_owner_CorrectlySets_plan_dict():
    # ESTABLISH
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()
    wk_str = "wkdays"
    wk_rope = sue_ownerunit.make_l1_rope(wk_str)
    wed_str = "Wednesday"
    wed_rope = sue_ownerunit.make_rope(wk_rope, wed_str)
    nation_str = "nation"
    nation_rope = sue_ownerunit.make_l1_rope(nation_str)
    france_str = "France"
    france_rope = sue_ownerunit.make_rope(nation_rope, france_str)
    sue_ownerunit.add_fact(fcontext=wk_rope, fstate=wed_rope)
    sue_ownerunit.add_fact(fcontext=nation_rope, fstate=france_rope)

    casa_str = "casa"
    casa_rope = sue_ownerunit.make_l1_rope(casa_str)
    casa_plan = sue_ownerunit.get_plan_obj(casa_rope)
    print(f"{sue_ownerunit.owner_name=} {len(casa_plan.reasonunits)=}")
    # print(f"{casa_plan.reasonunits=}")
    print(f"{sue_ownerunit.owner_name=} {len(sue_ownerunit.planroot.factunits)=}")
    # print(f"{sue_ownerunit.planroot.factunits=}")

    sue_ownerunit.settle_owner()
    assert sue_ownerunit._plan_dict
    assert len(sue_ownerunit._plan_dict) == 17

    usa_str = "USA"
    usa_rope = sue_ownerunit.make_rope(nation_rope, usa_str)
    oregon_str = "Oregon"
    oregon_rope = sue_ownerunit.make_rope(usa_rope, oregon_str)

    wed = premiseunit_shop(pstate=wed_rope)
    wed._status = True
    wed._chore = False
    usa = premiseunit_shop(pstate=usa_rope)
    usa._status = True
    usa._chore = False

    wed_lu = reasonunit_shop(wk_rope, premises={wed.pstate: wed})
    sta_lu = reasonunit_shop(nation_rope, premises={usa.pstate: usa})
    wed_lh = reasonheir_shop(
        rcontext=wk_rope,
        premises={wed.pstate: wed},
        _status=True,
        _chore=False,
        _rplan_active_value=True,
    )
    sta_lh = reasonheir_shop(
        rcontext=nation_rope,
        premises={usa.pstate: usa},
        _status=True,
        _chore=False,
        _rplan_active_value=True,
    )

    x1_reasonunits = {
        wed_lu.rcontext: wed_lu,
        sta_lu.rcontext: sta_lu,
    }
    x1_reasonheirs = {
        wed_lh.rcontext: wed_lh,
        sta_lh.rcontext: sta_lh,
    }

    # WHEN
    sue_ownerunit.add_fact(fcontext=nation_rope, fstate=oregon_rope)
    sue_ownerunit.settle_owner()

    # THEN
    casa_plan = sue_ownerunit._plan_dict.get(casa_rope)
    print(f"\nlook at {casa_plan.get_plan_rope()=}")
    assert casa_plan.parent_rope == to_rope(sue_ownerunit.belief_label)
    assert casa_plan._kids == {}
    assert casa_plan.mass == 30
    assert casa_plan.plan_label == casa_str
    assert casa_plan._level == 1
    assert casa_plan._active
    assert casa_plan.task
    # print(f"{casa_plan._reasonheirs=}")
    nation_reasonheir = casa_plan._reasonheirs[nation_rope]
    print(f"  {nation_reasonheir=}")
    print(f"  {nation_reasonheir._status=}\n")
    # assert casa_plan._reasonheirs == x1_reasonheirs

    assert len(casa_plan._reasonheirs) == len(x1_reasonheirs)
    wk_reasonheir = casa_plan._reasonheirs.get(wk_rope)
    # usa_premise = wk_reasonheir.premises.get(usa_rope)
    print(f"    {casa_plan.plan_label=}")
    # print(f"    {usa_premise.rcontext=}")
    # print(f"    {usa_premise._chore=}")
    # print(f"    {usa_premise._chore=}")
    assert wk_reasonheir._chore is False
    # print(f"      premises: {w=}")
    # w_state = usa_premise.premises[wed_rope].pstate
    # print(f"      {w_state=}")
    # assert usa_premise._chore == w_state._chore
    # assert usa_premise._status == w_state._status
    # assert wk_reasonheir.premises == wk_reasonheir.premises

    # assert casa_plan.reasonunits == x1_reasonunits

    # print("iterate through every plan...")
    # for x_plan in plan_dict:
    #     if str(type(x_plan)).find(".plan.PlanUnit'>") > 0:
    #         assert x_plan._active is not None

    #     # print("")
    #     # print(f"{x_plan.plan_label=}")
    #     # print(f"{len(x_plan.reasonunits)=}")
    #     print(
    #         f"  {x_plan.plan_label} iterate through every reasonheir... {len(x_plan._reasonheirs)=} {x_plan.plan_label=}"
    #     )
    #     # print(f"{x_plan._reasonheirs=}")
    #     for reason in x_plan._reasonheirs.values():
    #         assert str(type(reason)).find(".reason.ReasonHeir'>") > 0
    #         print(f"    {reason.rcontext=}")
    #         assert reason._status is not None
    #         for premise_x in reason.premises.values():
    #             assert premise_x._status is not None
    #         assert _check_all_objects_in_dict_are_correct_type(
    #             x_dict=reason.premises, type_str="src.s2_ownerunit.reason.PremiseUnit"
    #         )


# def _check_all_objects_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
#     bool_x = True
#     for x_value in x_dict.values():
#         if type_str not in str(type(x_value)):
#             bool_x = False
#         print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
#     return bool_x


def test_OwnerUnit_settle_owner_CorrectlyCalculatesRangeAttributes():
    # ESTABLISH
    sue_ownerunit = get_ownerunit_with7amCleanTableReason()
    sue_ownerunit.settle_owner()
    house_str = "housemanagement"
    house_rope = sue_ownerunit.make_l1_rope(house_str)
    clean_str = "clean table"
    clean_rope = sue_ownerunit.make_rope(house_rope, clean_str)
    assert sue_ownerunit._plan_dict.get(clean_rope)._active is False

    # set facts as midevening to 8am
    time_str = "timetech"
    time_rope = sue_ownerunit.make_l1_rope(time_str)
    day24hr_str = "24hr day"
    day24hr_rope = sue_ownerunit.make_rope(time_rope, day24hr_str)
    day24hr_rcontext = day24hr_rope
    day24hr_fstate = day24hr_rope
    day24hr_popen = 0.0
    day24hr_pnigh = 8.0

    # WHEN
    sue_ownerunit.add_fact(
        day24hr_rcontext,
        fstate=day24hr_fstate,
        fopen=day24hr_popen,
        fnigh=day24hr_pnigh,
    )

    # THEN
    sue_ownerunit.settle_owner()
    assert sue_ownerunit._plan_dict.get(clean_rope)._active

    # WHEN
    # set facts as 8am to 10am
    day24hr_popen = 8.0
    day24hr_pnigh = 10.0
    print(sue_ownerunit.planroot.factunits[day24hr_rope])
    sue_ownerunit.add_fact(
        day24hr_rcontext,
        fstate=day24hr_fstate,
        fopen=day24hr_popen,
        fnigh=day24hr_pnigh,
    )
    print(sue_ownerunit.planroot.factunits[day24hr_rope])
    print(sue_ownerunit.planroot._kids[house_str]._kids[clean_str].reasonunits)
    # sue_ownerunit.planroot._kids["housemanagement"]._kids[clean_str]._active = None

    # THEN
    sue_ownerunit.settle_owner()
    assert sue_ownerunit._plan_dict.get(clean_rope)._active is False


def test_OwnerUnit_get_agenda_dict_ReturnsObj_WithSingleTask():
    # ESTABLISH
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()

    # WHEN
    task_plans = sue_ownerunit.get_agenda_dict()

    # THEN
    assert task_plans is not None
    assert len(task_plans) > 0
    assert len(task_plans) == 1


def test_OwnerUnit_settle_owner_CorrectlySetsData_ownerunit_v001():
    # ESTABLISH
    yao_ownerunit = ownerunit_v001()
    print(f"{yao_ownerunit.get_reason_rcontexts()=}")
    # day_hr = f"{yao_ownerunit.belief_label},day_hr"
    # yao_ownerunit.add_fact(fcontext=day_hr, fstate=day_hr, popen=0, pnigh=23)
    day_min_str = "day_minute"
    day_min_rope = yao_ownerunit.make_l1_rope(day_min_str)
    yao_ownerunit.add_fact(
        fcontext=day_min_rope, fstate=day_min_rope, fopen=0, fnigh=1439
    )

    mood_str = "Moods"
    mood_rope = yao_ownerunit.make_l1_rope(mood_str)
    yao_ownerunit.add_fact(fcontext=mood_rope, fstate=mood_rope)
    print(f"{yao_ownerunit.get_reason_rcontexts()=}")

    yr_mon_str = "yr_month"
    yr_mon_rope = yao_ownerunit.make_l1_rope(yr_mon_str)
    yao_ownerunit.add_fact(fcontext=yr_mon_rope, fstate=yr_mon_rope)
    inter_str = "Interweb"
    inter_rope = yao_ownerunit.make_l1_rope(inter_str)
    yao_ownerunit.add_fact(fcontext=inter_rope, fstate=inter_rope)
    assert yao_ownerunit is not None
    # print(f"{yao_ownerunit.owner_name=}")
    # print(f"{len(yao_ownerunit.planroot._kids)=}")
    ulty_str = "Ultimate Frisbee"
    ulty_rope = yao_ownerunit.make_l1_rope(ulty_str)

    # if yao_ownerunit.planroot._kids["Ultimate Frisbee"].plan_label == "Ultimate Frisbee":
    assert yao_ownerunit.planroot._kids[ulty_str].reasonunits is not None
    assert yao_ownerunit.owner_name is not None

    # for fact in yao_ownerunit.planroot.factunits.values():
    #     print(f"{fact=}")

    # WHEN
    yao_ownerunit.settle_owner()

    # THEN
    # print(f"{str(type(plan))=}")
    # print(f"{len(plan_dict)=}")
    laundry_str = "laundry monday"
    casa_rope = yao_ownerunit.make_l1_rope("casa")
    cleaning_rope = yao_ownerunit.make_rope(casa_rope, "cleaning")
    laundry_rope = yao_ownerunit.make_rope(cleaning_rope, laundry_str)

    # for plan in plan_dict:
    #     assert (
    #         str(type(plan)).find(".plan.PlanUnit'>") > 0
    #         or str(type(plan)).find(".plan.PlanUnit'>") > 0
    #     )
    #     # print(f"{plan.plan_label=}")
    #     if plan.plan_label == laundry_str:
    #         for reason in plan.reasonunits.values():
    #             print(f"{plan.plan_label=} {reason.rcontext=}")  # {reason.premises=}")
    # assert plan._active is False
    assert yao_ownerunit._plan_dict.get(laundry_rope)._active is False

    # WHEN
    wk_str = "wkdays"
    wk_rope = yao_ownerunit.make_l1_rope(wk_str)
    mon_str = "Monday"
    mon_rope = yao_ownerunit.make_rope(wk_rope, mon_str)
    yao_ownerunit.add_fact(fcontext=wk_rope, fstate=mon_rope)
    yao_ownerunit.settle_owner()

    # THEN
    assert yao_ownerunit._plan_dict.get(laundry_rope)._active is False


def test_OwnerUnit_settle_owner_OptionWeekdaysReturnsObj_ownerunit_v001():
    # ESTABLISH
    yao_ownerunit = ownerunit_v001()

    day_hr_str = "day_hr"
    day_hr_rope = yao_ownerunit.make_l1_rope(day_hr_str)
    yao_ownerunit.add_fact(fcontext=day_hr_rope, fstate=day_hr_rope, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_rope = yao_ownerunit.make_l1_rope(day_min_str)
    yao_ownerunit.add_fact(
        fcontext=day_min_rope, fstate=day_min_rope, fopen=0, fnigh=59
    )
    mon_wk_str = "month_wk"
    mon_wk_rope = yao_ownerunit.make_l1_rope(mon_wk_str)
    yao_ownerunit.add_fact(fcontext=mon_wk_rope, fstate=mon_wk_rope)
    nation_str = "Nation-States"
    nation_rope = yao_ownerunit.make_l1_rope(nation_str)
    yao_ownerunit.add_fact(fcontext=nation_rope, fstate=nation_rope)
    mood_str = "Moods"
    mood_rope = yao_ownerunit.make_l1_rope(mood_str)
    yao_ownerunit.add_fact(fcontext=mood_rope, fstate=mood_rope)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_ownerunit.make_l1_rope(aaron_str)
    yao_ownerunit.add_fact(fcontext=aaron_rope, fstate=aaron_rope)
    inter_str = "Interweb"
    inter_rope = yao_ownerunit.make_l1_rope(inter_str)
    yao_ownerunit.add_fact(fcontext=inter_rope, fstate=inter_rope)
    yr_mon_str = "yr_month"
    yr_mon_rope = yao_ownerunit.make_l1_rope(yr_mon_str)
    yao_ownerunit.add_fact(
        fcontext=yr_mon_rope, fstate=yr_mon_rope, fopen=0, fnigh=1000
    )

    yao_ownerunit.settle_owner()
    missing_facts = yao_ownerunit.get_missing_fact_rcontexts()
    # for missing_fact, count in missing_facts.items():
    #     print(f"{missing_fact=} {count=}")

    wk_str = "wkdays"
    wk_rope = yao_ownerunit.make_l1_rope(wk_str)
    mon_str = "Monday"
    mon_rope = yao_ownerunit.make_rope(wk_rope, mon_str)
    tue_str = "Tuesday"
    tue_rope = yao_ownerunit.make_rope(wk_rope, tue_str)
    mon_premise_x = premiseunit_shop(pstate=mon_rope)
    mon_premise_x._status = False
    mon_premise_x._chore = False
    tue_premise_x = premiseunit_shop(pstate=tue_rope)
    tue_premise_x._status = False
    tue_premise_x._chore = False
    mt_premises = {
        mon_premise_x.pstate: mon_premise_x,
        tue_premise_x.pstate: tue_premise_x,
    }
    mt_reasonunit = reasonunit_shop(wk_rope, premises=mt_premises)
    mt_reasonheir = reasonheir_shop(wk_rope, premises=mt_premises, _status=False)
    x_planroot = yao_ownerunit.get_plan_obj(to_rope(yao_ownerunit.belief_label))
    x_planroot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_ownerunit.reasonunits[wk_rope].rcontext=}")
    # print(f"{yao_ownerunit.reasonunits[wk_rope].premises[mon_rope].pstate=}")
    # print(f"{yao_ownerunit.reasonunits[wk_rope].premises[tue_rope].pstate=}")
    wk_reasonunit = x_planroot.reasonunits[wk_rope]
    print(f"{wk_reasonunit.premises=}")
    premise_mon = wk_reasonunit.premises.get(mon_rope)
    premise_tue = wk_reasonunit.premises.get(tue_rope)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.pstate]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.pstate]
    assert wk_reasonunit == mt_reasonunit

    # WHEN
    plan_dict = yao_ownerunit.get_plan_dict()

    # THEN
    gen_wk_reasonheir = x_planroot.get_reasonheir(wk_rope)
    gen_mon_premise = gen_wk_reasonheir.premises.get(mon_rope)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_rope)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_rope)
    assert gen_wk_reasonheir.premises == mt_reasonheir.premises
    assert gen_wk_reasonheir == mt_reasonheir

    casa_str = "casa"
    casa_rope = yao_ownerunit.make_l1_rope(casa_str)
    bird_str = "say hi to birds"
    bird_rope = yao_ownerunit.make_rope(casa_rope, bird_str)
    assert from_list_get_active(bird_rope, plan_dict) is False

    # yao_ownerunit.add_fact(fcontext=wk_rope, fstate=mon_rope)
    # plan_dict = yao_ownerunit.get_plan_dict()
    # casa_plan = x_planroot._kids[casa_str]
    # twee_plan = casa_plan._kids[bird_str]
    # print(f"{len(x_planroot._reasonheirs)=}")
    # print(f"{len(casa_plan._reasonheirs)=}")
    # print(f"{len(twee_plan._reasonheirs)=}")

    # assert YR.get_active(rope=bird_plan, plan_dict=plan_dict) is True

    # yao_ownerunit.add_fact(fcontext=f"{yao_ownerunit.belief_label},wkdays", fstate=f"{yao_ownerunit.belief_label},wkdays,Tuesday")
    # plan_dict = yao_ownerunit.get_plan_dict()
    # assert YR.get_active(rope=bird_plan, plan_dict=plan_dict) is True

    # yao_ownerunit.add_fact(fcontext=f"{yao_ownerunit.belief_label},wkdays", fstate=f"{yao_ownerunit.belief_label},wkdays,Wednesday")
    # plan_dict = yao_ownerunit.get_plan_dict()
    # assert YR.get_active(rope=bird_plan, plan_dict=plan_dict) is False


def test_OwnerUnit_settle_owner_CorrectlySetsPlanUnitsActiveWithEvery6WeeksReason_ownerunit_v001():
    # ESTABLISH
    yao_ownerunit = ownerunit_v001()
    day_str = "day_hr"
    day_rope = yao_ownerunit.make_l1_rope(day_str)
    min_str = "day_minute"
    min_rope = yao_ownerunit.make_l1_rope(day_str)

    # WHEN
    yao_ownerunit.add_fact(fcontext=day_rope, fstate=day_rope, fopen=0, fnigh=23)
    yao_ownerunit.add_fact(fcontext=min_rope, fstate=min_rope, fopen=0, fnigh=59)
    yao_ownerunit.settle_owner()

    # THEN
    ced_wk_rcontext = yao_ownerunit.make_l1_rope("ced_wk")

    pdivisor = None
    popen = None
    pnigh = None
    print(f"{len(yao_ownerunit._plan_dict)=}")

    casa_rope = yao_ownerunit.make_l1_rope("casa")
    cleaning_rope = yao_ownerunit.make_rope(casa_rope, "cleaning")
    clean_couch_rope = yao_ownerunit.make_rope(
        cleaning_rope, "clean sheets couch blankets"
    )
    clean_sheet_plan = yao_ownerunit.get_plan_obj(clean_couch_rope)
    # print(f"{clean_sheet_plan.reasonunits.values()=}")
    ced_wk_reason = clean_sheet_plan.reasonunits.get(ced_wk_rcontext)
    ced_wk_premise = ced_wk_reason.premises.get(ced_wk_rcontext)
    print(
        f"{clean_sheet_plan.plan_label=} {ced_wk_reason.rcontext=} {ced_wk_premise.pstate=}"
    )
    # print(f"{clean_sheet_plan.plan_label=} {ced_wk_reason.rcontext=} {premise_x=}")
    pdivisor = ced_wk_premise.pdivisor
    popen = ced_wk_premise.popen
    pnigh = ced_wk_premise.pnigh
    # print(f"{plan.reasonunits=}")
    assert clean_sheet_plan._active is False

    # for plan in plan_dict:
    #     # print(f"{plan.parent_rope=}")
    #     if plan.plan_label == "clean sheets couch blankets":
    #         print(f"{plan.get_plan_rope()=}")

    assert pdivisor == 6
    assert popen == 1
    print(
        f"There exists a plan with a reason_rcontext {ced_wk_rcontext} that also has lemmet div =6 and popen/pnigh =1"
    )
    # print(f"{len(plan_dict)=}")
    ced_wk_popen = 6001

    # WHEN
    yao_ownerunit.add_fact(
        ced_wk_rcontext,
        fstate=ced_wk_rcontext,
        fopen=ced_wk_popen,
        fnigh=ced_wk_popen,
    )
    nation_str = "Nation-States"
    nation_rope = yao_ownerunit.make_l1_rope(nation_str)
    yao_ownerunit.add_fact(fcontext=nation_rope, fstate=nation_rope)
    print(
        f"Nation set and also fact set: {ced_wk_rcontext=} with {ced_wk_popen=} and {ced_wk_popen=}"
    )
    print(f"{yao_ownerunit.planroot.factunits=}")
    yao_ownerunit.settle_owner()

    # THEN
    wk_str = "ced_wk"
    wk_rope = yao_ownerunit.make_l1_rope(wk_str)
    casa_rope = yao_ownerunit.make_l1_rope("casa")
    cleaning_rope = yao_ownerunit.make_rope(casa_rope, "cleaning")
    clean_couch_str = "clean sheets couch blankets"
    clean_couch_rope = yao_ownerunit.make_rope(cleaning_rope, clean_couch_str)
    clean_couch_plan = yao_ownerunit.get_plan_obj(rope=clean_couch_rope)
    wk_reason = clean_couch_plan.reasonunits.get(wk_rope)
    wk_premise = wk_reason.premises.get(wk_rope)
    print(f"{clean_couch_plan.plan_label=} {wk_reason.rcontext=} {wk_premise=}")
    assert wk_premise.pdivisor == 6 and wk_premise.popen == 1


def test_OwnerUnit_settle_owner_EveryPlanHasActiveStatus_ownerunit_v001():
    # ESTABLISH
    yao_ownerunit = ownerunit_v001()

    # WHEN
    yao_ownerunit.settle_owner()

    # THEN
    print(f"{len(yao_ownerunit._plan_dict)=}")
    # first_plan_kid_count = 0
    # first_plan_kid_none_count = 0
    # first_plan_kid_true_count = 0
    # first_plan_kid_false_count = 0
    # for plan in plan_list:
    #     if str(type(plan)).find(".plan.PlanUnit'>") > 0:
    #         first_plan_kid_count += 1
    #         if plan._active is None:
    #             first_plan_kid_none_count += 1
    #         elif plan._active:
    #             first_plan_kid_true_count += 1
    #         elif plan._active is False:
    #             first_plan_kid_false_count += 1

    # print(f"{first_plan_kid_count=}")
    # print(f"{first_plan_kid_none_count=}")
    # print(f"{first_plan_kid_true_count=}")
    # print(f"{first_plan_kid_false_count=}")

    # plan_kid_count = 0
    # for plan in plan_list_without_planroot:
    #     plan_kid_count += 1
    #     print(f"{plan.plan_label=} {plan_kid_count=}")
    #     assert plan._active is not None
    #     assert plan._active in (True, False)
    # assert plan_kid_count == len(plan_list_without_planroot)

    assert len(yao_ownerunit._plan_dict) == sum(
        plan._active is not None for plan in yao_ownerunit._plan_dict.values()
    )


def test_OwnerUnit_settle_owner_EveryTwoMonthReturnsObj_ownerunit_v001():
    # ESTABLISH
    yao_ownerunit = ownerunit_v001()
    minute_str = "day_minute"
    minute_rope = yao_ownerunit.make_l1_rope(minute_str)
    yao_ownerunit.add_fact(
        fcontext=minute_rope, fstate=minute_rope, fopen=0, fnigh=1399
    )
    month_str = "month_wk"
    month_rope = yao_ownerunit.make_l1_rope(month_str)
    yao_ownerunit.add_fact(fcontext=month_rope, fstate=month_rope)
    nations_str = "Nation-States"
    nations_rope = yao_ownerunit.make_l1_rope(nations_str)
    yao_ownerunit.add_fact(fcontext=nations_rope, fstate=nations_rope)
    mood_str = "Moods"
    mood_rope = yao_ownerunit.make_l1_rope(mood_str)
    yao_ownerunit.add_fact(fcontext=mood_rope, fstate=mood_rope)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_rope = yao_ownerunit.make_l1_rope(aaron_str)
    yao_ownerunit.add_fact(fcontext=aaron_rope, fstate=aaron_rope)
    interweb_str = "Interweb"
    interweb_rope = yao_ownerunit.make_l1_rope(interweb_str)
    yao_ownerunit.add_fact(fcontext=interweb_rope, fstate=interweb_rope)
    wkdays_str = "wkdays"
    wkdays_rope = yao_ownerunit.make_l1_rope(wkdays_str)
    yao_ownerunit.add_fact(fcontext=wkdays_rope, fstate=wkdays_rope)
    plan_dict = yao_ownerunit.get_plan_dict()
    print(f"{len(plan_dict)=}")

    casa_str = "casa"
    casa_rope = yao_ownerunit.make_l1_rope(casa_str)
    clean_str = "cleaning"
    clean_rope = yao_ownerunit.make_rope(casa_rope, clean_str)
    mat_plan_label = "deep clean play mat"
    mat_rope = yao_ownerunit.make_rope(clean_rope, mat_plan_label)
    assert from_list_get_active(mat_rope, plan_dict) is False

    yr_month_rcontext = yao_ownerunit.make_l1_rope("yr_month")
    print(f"{yr_month_rcontext=}, {yr_month_rcontext=}")

    # WHEN
    yao_ownerunit.add_fact(
        yr_month_rcontext, fstate=yr_month_rcontext, fopen=0, fnigh=8
    )
    ced_wk = yao_ownerunit.make_l1_rope("ced_wk")
    yao_ownerunit.add_fact(fcontext=ced_wk, fstate=ced_wk, fopen=0, fnigh=4)
    yao_ownerunit.settle_owner()

    # THEN
    print(f"{len(plan_dict)=}")
    print(f"{len(yao_ownerunit.planroot.factunits)=}")
    assert from_list_get_active(mat_rope, yao_ownerunit._plan_dict)


def test_OwnerUnit_settle_owner_CorrectlySetsEmpty_sum_healerlink_share():
    # ESTABLISH
    sue_ownerunit = ownerunit_shop("Sue")
    assert sue_ownerunit._sum_healerlink_share == 0
    assert sue_ownerunit._keep_dict == {}

    # WHEN
    sue_ownerunit.settle_owner()

    # THEN
    assert sue_ownerunit._sum_healerlink_share == 0
    assert sue_ownerunit._keep_dict == {}


def test_OwnerUnit_settle_owner_CorrectlySets_sum_healerlink_share(graphics_bool):
    # ESTABLISH
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()
    sue_ownerunit.add_acctunit("Sue")
    sue_ownerunit.settle_owner()
    nation_rope = sue_ownerunit.make_l1_rope("nation")
    usa_rope = sue_ownerunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_ownerunit.make_rope(usa_rope, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_ownerunit.edit_plan_attr(
        oregon_rope, problem_bool=True, healerlink=sue_healerlink
    )
    oregon_plan = sue_ownerunit.get_plan_obj(oregon_rope)
    print(f"{oregon_plan._fund_ratio=}")
    assert sue_ownerunit._sum_healerlink_share == 0
    assert oregon_plan._healerlink_ratio == 0

    # WHEN
    sue_ownerunit.settle_owner()
    # THEN
    assert sue_ownerunit._sum_healerlink_share == 0.038461539 * default_fund_pool()
    assert oregon_plan._healerlink_ratio == 1

    # WHEN
    wk_rope = sue_ownerunit.make_l1_rope("wkdays")
    sue_ownerunit.edit_plan_attr(wk_rope, problem_bool=True)
    mon_rope = sue_ownerunit.make_rope(wk_rope, "Monday")
    sue_ownerunit.edit_plan_attr(mon_rope, healerlink=sue_healerlink)
    mon_plan = sue_ownerunit.get_plan_obj(mon_rope)
    # print(f"{mon_plan.problem_bool=} {mon_plan._fund_ratio=}")
    sue_ownerunit.settle_owner()
    # THEN
    assert sue_ownerunit._sum_healerlink_share != 0.038461539 * default_fund_pool()
    assert sue_ownerunit._sum_healerlink_share == 0.06923077 * default_fund_pool()
    assert oregon_plan._healerlink_ratio == 0.5555555571604938
    assert mon_plan._healerlink_ratio == 0.4444444428395062

    # WHEN
    tue_rope = sue_ownerunit.make_rope(wk_rope, "Tuesday")
    sue_ownerunit.edit_plan_attr(tue_rope, healerlink=sue_healerlink)
    tue_plan = sue_ownerunit.get_plan_obj(tue_rope)
    # print(f"{tue_plan.problem_bool=} {tue_plan._fund_ratio=}")
    # sat_rope = sue_ownerunit.make_rope(wk_rope, "Saturday")
    # sat_plan = sue_ownerunit.get_plan_obj(sat_rope)
    # print(f"{sat_plan.problem_bool=} {sat_plan._fund_ratio=}")
    sue_ownerunit.settle_owner()

    # THEN
    assert (
        sue_ownerunit._sum_healerlink_share != 0.06923076923076923 * default_fund_pool()
    )
    assert sue_ownerunit._sum_healerlink_share == 0.100000001 * default_fund_pool()
    assert oregon_plan._healerlink_ratio == 0.38461538615384616
    assert mon_plan._healerlink_ratio == 0.3076923069230769
    assert tue_plan._healerlink_ratio == 0.3076923069230769

    # WHEN
    sue_ownerunit.edit_plan_attr(wk_rope, healerlink=sue_healerlink)
    wk_plan = sue_ownerunit.get_plan_obj(wk_rope)
    print(f"{wk_plan.plan_label=} {wk_plan.problem_bool=} {wk_plan._fund_ratio=}")
    sue_ownerunit.settle_owner()
    # THEN
    display_plantree(sue_ownerunit, "Keep", graphics_bool)
    assert sue_ownerunit._sum_healerlink_share == 0
    assert oregon_plan._healerlink_ratio == 0
    assert mon_plan._healerlink_ratio == 0
    assert tue_plan._healerlink_ratio == 0


def test_OwnerUnit_settle_owner_CorrectlySets_keep_dict_v1(graphics_bool):
    # ESTABLISH
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()
    sue_ownerunit.add_acctunit("Sue")
    sue_ownerunit.settle_owner()
    nation_rope = sue_ownerunit.make_l1_rope("nation")
    usa_rope = sue_ownerunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_ownerunit.make_rope(usa_rope, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_ownerunit.edit_plan_attr(
        oregon_rope, problem_bool=True, healerlink=sue_healerlink
    )
    assert len(sue_ownerunit._keep_dict) == 0
    assert sue_ownerunit._keep_dict.get(oregon_rope) is None

    # WHEN
    sue_ownerunit.settle_owner()
    # THEN
    assert len(sue_ownerunit._keep_dict) == 1
    assert sue_ownerunit._keep_dict.get(oregon_rope) is not None

    # WHEN
    wk_rope = sue_ownerunit.make_l1_rope("wkdays")
    sue_ownerunit.edit_plan_attr(wk_rope, problem_bool=True)
    mon_rope = sue_ownerunit.make_rope(wk_rope, "Monday")
    sue_ownerunit.edit_plan_attr(mon_rope, healerlink=sue_healerlink)
    # mon_plan = sue_ownerunit.get_plan_obj(mon_rope)
    # print(f"{mon_plan.problem_bool=} {mon_plan._fund_ratio=}")
    sue_ownerunit.settle_owner()
    # THEN
    assert len(sue_ownerunit._keep_dict) == 2
    assert sue_ownerunit._keep_dict.get(oregon_rope) is not None
    assert sue_ownerunit._keep_dict.get(mon_rope) is not None

    # WHEN
    tue_rope = sue_ownerunit.make_rope(wk_rope, "Tuesday")
    sue_ownerunit.edit_plan_attr(tue_rope, healerlink=sue_healerlink)
    # tue_plan = sue_ownerunit.get_plan_obj(tue_rope)
    # print(f"{tue_plan.problem_bool=} {tue_plan._fund_ratio=}")
    # sat_rope = sue_ownerunit.make_rope(wk_rope, "Saturday")
    # sat_plan = sue_ownerunit.get_plan_obj(sat_rope)
    # print(f"{sat_plan.problem_bool=} {sat_plan._fund_ratio=}")
    sue_ownerunit.settle_owner()

    # THEN
    assert len(sue_ownerunit._keep_dict) == 3
    assert sue_ownerunit._keep_dict.get(oregon_rope) is not None
    assert sue_ownerunit._keep_dict.get(mon_rope) is not None
    assert sue_ownerunit._keep_dict.get(tue_rope) is not None

    # WHEN
    sue_ownerunit.edit_plan_attr(wk_rope, healerlink=sue_healerlink)
    wk_plan = sue_ownerunit.get_plan_obj(wk_rope)
    print(f"{wk_plan.plan_label=} {wk_plan.problem_bool=} {wk_plan._fund_ratio=}")
    sue_ownerunit.settle_owner()
    # THEN
    display_plantree(sue_ownerunit, "Keep", graphics_bool)
    assert len(sue_ownerunit._keep_dict) == 0
    assert sue_ownerunit._keep_dict == {}


def test_OwnerUnit_settle_owner_CorrectlySets_healers_dict():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()
    sue_ownerunit.add_acctunit(sue_str)
    sue_ownerunit.add_acctunit(bob_str)
    assert sue_ownerunit._healers_dict == {}

    # WHEN
    sue_ownerunit.settle_owner()
    # THEN
    assert sue_ownerunit._healers_dict == {}

    # ESTABLISH
    nation_rope = sue_ownerunit.make_l1_rope("nation")
    usa_rope = sue_ownerunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_ownerunit.make_rope(usa_rope, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_ownerunit.edit_plan_attr(
        oregon_rope, problem_bool=True, healerlink=sue_healerlink
    )

    wk_rope = sue_ownerunit.make_l1_rope("wkdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_ownerunit.edit_plan_attr(wk_rope, problem_bool=True, healerlink=bob_healerlink)
    assert sue_ownerunit._healers_dict == {}

    # WHEN
    sue_ownerunit.settle_owner()

    # THEN
    assert len(sue_ownerunit._healers_dict) == 2
    wk_plan = sue_ownerunit.get_plan_obj(wk_rope)
    assert sue_ownerunit._healers_dict.get(bob_str) == {wk_rope: wk_plan}
    oregon_plan = sue_ownerunit.get_plan_obj(oregon_rope)
    assert sue_ownerunit._healers_dict.get(sue_str) == {oregon_rope: oregon_plan}


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_buildable_True():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()
    sue_ownerunit.add_acctunit(sue_str)
    sue_ownerunit.add_acctunit(bob_str)
    assert sue_ownerunit._keeps_buildable is False

    # WHEN
    sue_ownerunit.settle_owner()
    # THEN
    assert sue_ownerunit._keeps_buildable

    # ESTABLISH
    nation_rope = sue_ownerunit.make_l1_rope("nation")
    usa_rope = sue_ownerunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_ownerunit.make_rope(usa_rope, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_ownerunit.edit_plan_attr(
        oregon_rope, problem_bool=True, healerlink=sue_healerlink
    )

    wk_rope = sue_ownerunit.make_l1_rope("wkdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_ownerunit.edit_plan_attr(wk_rope, problem_bool=True, healerlink=bob_healerlink)

    # WHEN
    sue_ownerunit.settle_owner()
    # THEN
    assert sue_ownerunit._keeps_buildable


def test_OwnerUnit_settle_owner_CorrectlySets_keeps_buildable_False():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    sue_ownerunit = get_ownerunit_with_4_levels_and_2reasons()
    sue_ownerunit.add_acctunit(sue_str)
    sue_ownerunit.add_acctunit(bob_str)
    assert sue_ownerunit._keeps_buildable is False

    # WHEN
    sue_ownerunit.settle_owner()
    # THEN
    assert sue_ownerunit._keeps_buildable

    # ESTABLISH
    nation_rope = sue_ownerunit.make_l1_rope("nation")
    usa_rope = sue_ownerunit.make_rope(nation_rope, "USA")
    oregon_rope = sue_ownerunit.make_rope(usa_rope, "Oregon")
    bend_str = "Be/nd"
    bend_rope = sue_ownerunit.make_rope(oregon_rope, bend_str)
    sue_ownerunit.set_plan(planunit_shop(bend_str), oregon_rope)
    sue_healerlink = healerlink_shop({sue_str})
    sue_ownerunit.edit_plan_attr(
        bend_rope, problem_bool=True, healerlink=sue_healerlink
    )
    assert sue_ownerunit._keeps_buildable

    # WHEN
    sue_ownerunit.settle_owner()
    # THEN
    assert sue_ownerunit._keeps_buildable is False
