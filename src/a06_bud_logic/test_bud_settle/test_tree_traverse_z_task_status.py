from src.a01_way_logic.way import to_way
from src.a02_finance_logic.finance_config import default_fund_pool
from src.a04_reason_logic.reason_idea import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.a05_idea_logic.idea import ideaunit_shop
from src.a05_idea_logic.healer import healerlink_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_graphics import display_ideatree
from src.a06_bud_logic._utils.example_buds import (
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_with7amCleanTableReason,
    budunit_v001,
    from_list_get_active,
)


def test_BudUnit_settle_bud_SetsStatus_active_WhenFactSaysNo():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_way = sue_budunit.make_l1_way(week_str)
    sun_str = "Sunday"
    sun_way = sue_budunit.make_way(week_way, sun_str)

    # for idea in sue_budunit._idea_dict.values():
    #     print(f"{casa_way=} {idea.get_idea_way()=}")
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    assert sue_budunit.get_idea_obj(casa_way)._active is None

    # WHEN
    sue_budunit.add_fact(fcontext=week_way, fbranch=sun_way)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._idea_dict != {}
    assert len(sue_budunit._idea_dict) == 17

    # for idea in sue_budunit._idea_dict.values():
    #     print(f"{casa_way=} {idea.get_idea_way()=}")
    assert sue_budunit.get_idea_obj(casa_way)._active is False


def test_BudUnit_settle_bud_SetsStatus_active_WhenFactModifies():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_way = sue_budunit.make_l1_way(week_str)
    sun_str = "Wednesday"
    sun_way = sue_budunit.make_way(week_way, sun_str)
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)

    # WHEN
    sue_budunit.add_fact(fcontext=week_way, fbranch=sun_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._idea_dict
    assert len(sue_budunit._idea_dict) == 17
    assert sue_budunit._idea_dict.get(casa_way)._active is False

    # WHEN
    states_str = "nation-state"
    states_way = sue_budunit.make_l1_way(states_str)
    usa_str = "USA"
    usa_way = sue_budunit.make_way(states_way, usa_str)
    sue_budunit.add_fact(fcontext=states_way, fbranch=usa_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._idea_dict
    assert len(sue_budunit._idea_dict) == 17
    assert sue_budunit._idea_dict.get(casa_way)._active

    # WHEN
    france_str = "France"
    france_way = sue_budunit.make_way(states_way, france_str)
    sue_budunit.add_fact(fcontext=states_way, fbranch=france_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._idea_dict
    assert len(sue_budunit._idea_dict) == 17
    assert sue_budunit._idea_dict.get(casa_way)._active is False


def test_BudUnit_settle_bud_CorrectlySets_idea_dict():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_way = sue_budunit.make_l1_way(week_str)
    wed_str = "Wednesday"
    wed_way = sue_budunit.make_way(week_way, wed_str)
    state_str = "nation-state"
    state_way = sue_budunit.make_l1_way(state_str)
    france_str = "France"
    france_way = sue_budunit.make_way(state_way, france_str)
    sue_budunit.add_fact(fcontext=week_way, fbranch=wed_way)
    sue_budunit.add_fact(fcontext=state_way, fbranch=france_way)

    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_idea = sue_budunit.get_idea_obj(casa_way)
    print(f"{sue_budunit.owner_name=} {len(casa_idea.reasonunits)=}")
    # print(f"{casa_idea.reasonunits=}")
    print(f"{sue_budunit.owner_name=} {len(sue_budunit.idearoot.factunits)=}")
    # print(f"{sue_budunit.idearoot.factunits=}")

    sue_budunit.settle_bud()
    assert sue_budunit._idea_dict
    assert len(sue_budunit._idea_dict) == 17

    usa_str = "USA"
    usa_way = sue_budunit.make_way(state_way, usa_str)
    oregon_str = "Oregon"
    oregon_way = sue_budunit.make_way(usa_way, oregon_str)

    wed = premiseunit_shop(pbranch=wed_way)
    wed._status = True
    wed._task = False
    usa = premiseunit_shop(pbranch=usa_way)
    usa._status = True
    usa._task = False

    wed_lu = reasonunit_shop(week_way, premises={wed.pbranch: wed})
    sta_lu = reasonunit_shop(state_way, premises={usa.pbranch: usa})
    wed_lh = reasonheir_shop(
        rcontext=week_way,
        premises={wed.pbranch: wed},
        _status=True,
        _task=False,
        _rcontext_idea_active_value=True,
    )
    sta_lh = reasonheir_shop(
        rcontext=state_way,
        premises={usa.pbranch: usa},
        _status=True,
        _task=False,
        _rcontext_idea_active_value=True,
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
    sue_budunit.add_fact(fcontext=state_way, fbranch=oregon_way)
    sue_budunit.settle_bud()

    # THEN
    casa_idea = sue_budunit._idea_dict.get(casa_way)
    print(f"\nlook at {casa_idea.get_idea_way()=}")
    assert casa_idea.parent_way == to_way(sue_budunit.fisc_word)
    assert casa_idea._kids == {}
    assert casa_idea.mass == 30
    assert casa_idea.idea_word == casa_str
    assert casa_idea._level == 1
    assert casa_idea._active
    assert casa_idea.pledge
    # print(f"{casa_idea._reasonheirs=}")
    x_reasonheir_state = casa_idea._reasonheirs[state_way]
    print(f"  {x_reasonheir_state=}")
    print(f"  {x_reasonheir_state._status=}\n")
    # assert casa_idea._reasonheirs == x1_reasonheirs

    assert len(casa_idea._reasonheirs) == len(x1_reasonheirs)
    week_reasonheir = casa_idea._reasonheirs.get(week_way)
    # usa_premise = week_reasonheir.premises.get(usa_way)
    print(f"    {casa_idea.idea_word=}")
    # print(f"    {usa_premise.rcontext=}")
    # print(f"    {usa_premise._task=}")
    # print(f"    {usa_premise._task=}")
    assert week_reasonheir._task is False
    # print(f"      premises: {w=}")
    # w_branch = usa_premise.premises[wed_way].pbranch
    # print(f"      {w_branch=}")
    # assert usa_premise._task == w_branch._task
    # assert usa_premise._status == w_branch._status
    # assert week_reasonheir.premises == week_reasonheir.premises

    # assert casa_idea.reasonunits == x1_reasonunits

    # print("iterate through every idea...")
    # for x_idea in idea_dict:
    #     if str(type(x_idea)).find(".idea.IdeaUnit'>") > 0:
    #         assert x_idea._active is not None

    #     # print("")
    #     # print(f"{x_idea.idea_word=}")
    #     # print(f"{len(x_idea.reasonunits)=}")
    #     print(
    #         f"  {x_idea.idea_word} iterate through every reasonheir... {len(x_idea._reasonheirs)=} {x_idea.idea_word=}"
    #     )
    #     # print(f"{x_idea._reasonheirs=}")
    #     for reason in x_idea._reasonheirs.values():
    #         assert str(type(reason)).find(".reason.ReasonHeir'>") > 0
    #         print(f"    {reason.rcontext=}")
    #         assert reason._status is not None
    #         for premise_x in reason.premises.values():
    #             assert premise_x._status is not None
    #         assert _check_all_objects_in_dict_are_correct_type(
    #             x_dict=reason.premises, type_str="src.s2_budunit.reason.PremiseUnit"
    #         )


# def _check_all_objects_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
#     bool_x = True
#     for x_value in x_dict.values():
#         if type_str not in str(type(x_value)):
#             bool_x = False
#         print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
#     return bool_x


def test_BudUnit_settle_bud_CorrectlyCalculatesRangeAttributes():
    # ESTABLISH
    sue_budunit = get_budunit_with7amCleanTableReason()
    sue_budunit.settle_bud()
    house_str = "housemanagement"
    house_way = sue_budunit.make_l1_way(house_str)
    clean_str = "clean table"
    clean_way = sue_budunit.make_way(house_way, clean_str)
    assert sue_budunit._idea_dict.get(clean_way)._active is False

    # set facts as midevening to 8am
    time_str = "timetech"
    time_way = sue_budunit.make_l1_way(time_str)
    day24hr_str = "24hr day"
    day24hr_way = sue_budunit.make_way(time_way, day24hr_str)
    day24hr_rcontext = day24hr_way
    day24hr_fbranch = day24hr_way
    day24hr_popen = 0.0
    day24hr_pnigh = 8.0

    # WHEN
    sue_budunit.add_fact(
        day24hr_rcontext,
        fbranch=day24hr_fbranch,
        fopen=day24hr_popen,
        fnigh=day24hr_pnigh,
    )

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._idea_dict.get(clean_way)._active

    # WHEN
    # set facts as 8am to 10am
    day24hr_popen = 8.0
    day24hr_pnigh = 10.0
    print(sue_budunit.idearoot.factunits[day24hr_way])
    sue_budunit.add_fact(
        day24hr_rcontext,
        fbranch=day24hr_fbranch,
        fopen=day24hr_popen,
        fnigh=day24hr_pnigh,
    )
    print(sue_budunit.idearoot.factunits[day24hr_way])
    print(sue_budunit.idearoot._kids[house_str]._kids[clean_str].reasonunits)
    # sue_budunit.idearoot._kids["housemanagement"]._kids[clean_str]._active = None

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._idea_dict.get(clean_way)._active is False


def test_BudUnit_get_agenda_dict_ReturnsObj():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()

    # WHEN
    pledge_ideas = sue_budunit.get_agenda_dict()

    # THEN
    assert pledge_ideas is not None
    assert len(pledge_ideas) > 0
    assert len(pledge_ideas) == 1


def test_BudUnit_settle_bud_CorrectlySetsData_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    print(f"{yao_budunit.get_reason_rcontexts()=}")
    # day_hour = f"{yao_budunit.fisc_word},day_hour"
    # yao_budunit.add_fact(fcontext=day_hour, fbranch=day_hour, popen=0, pnigh=23)
    day_min_str = "day_minute"
    day_min_way = yao_budunit.make_l1_way(day_min_str)
    yao_budunit.add_fact(fcontext=day_min_way, fbranch=day_min_way, fopen=0, fnigh=1439)

    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fcontext=mood_way, fbranch=mood_way)
    print(f"{yao_budunit.get_reason_rcontexts()=}")

    yr_mon_str = "year_month"
    yr_mon_way = yao_budunit.make_l1_way(yr_mon_str)
    yao_budunit.add_fact(fcontext=yr_mon_way, fbranch=yr_mon_way)
    inter_str = "Interweb"
    inter_way = yao_budunit.make_l1_way(inter_str)
    yao_budunit.add_fact(fcontext=inter_way, fbranch=inter_way)
    assert yao_budunit is not None
    # print(f"{yao_budunit.owner_name=}")
    # print(f"{len(yao_budunit.idearoot._kids)=}")
    ulty_str = "Ultimate Frisbee"
    ulty_way = yao_budunit.make_l1_way(ulty_str)

    # if yao_budunit.idearoot._kids["Ultimate Frisbee"].idea_word == "Ultimate Frisbee":
    assert yao_budunit.idearoot._kids[ulty_str].reasonunits is not None
    assert yao_budunit.owner_name is not None

    # for fact in yao_budunit.idearoot.factunits.values():
    #     print(f"{fact=}")

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    # print(f"{str(type(idea))=}")
    # print(f"{len(idea_dict)=}")
    laundry_str = "laundry monday"
    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    laundry_way = yao_budunit.make_way(cleaning_way, laundry_str)

    # for idea in idea_dict:
    #     assert (
    #         str(type(idea)).find(".idea.IdeaUnit'>") > 0
    #         or str(type(idea)).find(".idea.IdeaUnit'>") > 0
    #     )
    #     # print(f"{idea.idea_word=}")
    #     if idea.idea_word == laundry_str:
    #         for reason in idea.reasonunits.values():
    #             print(f"{idea.idea_word=} {reason.rcontext=}")  # {reason.premises=}")
    # assert idea._active is False
    assert yao_budunit._idea_dict.get(laundry_way)._active is False

    # WHEN
    week_str = "weekdays"
    week_way = yao_budunit.make_l1_way(week_str)
    mon_str = "Monday"
    mon_way = yao_budunit.make_way(week_way, mon_str)
    yao_budunit.add_fact(fcontext=week_way, fbranch=mon_way)
    yao_budunit.settle_bud()

    # THEN
    assert yao_budunit._idea_dict.get(laundry_way)._active is False


def test_BudUnit_settle_bud_OptionWeekdaysReturnsObj_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()

    day_hr_str = "day_hour"
    day_hr_way = yao_budunit.make_l1_way(day_hr_str)
    yao_budunit.add_fact(fcontext=day_hr_way, fbranch=day_hr_way, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_way = yao_budunit.make_l1_way(day_min_str)
    yao_budunit.add_fact(fcontext=day_min_way, fbranch=day_min_way, fopen=0, fnigh=59)
    mon_wk_str = "month_week"
    mon_wk_way = yao_budunit.make_l1_way(mon_wk_str)
    yao_budunit.add_fact(fcontext=mon_wk_way, fbranch=mon_wk_way)
    nation_str = "Nation-States"
    nation_way = yao_budunit.make_l1_way(nation_str)
    yao_budunit.add_fact(fcontext=nation_way, fbranch=nation_way)
    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fcontext=mood_way, fbranch=mood_way)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_way = yao_budunit.make_l1_way(aaron_str)
    yao_budunit.add_fact(fcontext=aaron_way, fbranch=aaron_way)
    inter_str = "Interweb"
    inter_way = yao_budunit.make_l1_way(inter_str)
    yao_budunit.add_fact(fcontext=inter_way, fbranch=inter_way)
    yr_mon_str = "year_month"
    yr_mon_way = yao_budunit.make_l1_way(yr_mon_str)
    yao_budunit.add_fact(fcontext=yr_mon_way, fbranch=yr_mon_way, fopen=0, fnigh=1000)

    yao_budunit.settle_bud()
    missing_facts = yao_budunit.get_missing_fact_rcontexts()
    # for missing_fact, count in missing_facts.items():
    #     print(f"{missing_fact=} {count=}")

    week_str = "weekdays"
    week_way = yao_budunit.make_l1_way(week_str)
    mon_str = "Monday"
    mon_way = yao_budunit.make_way(week_way, mon_str)
    tue_str = "Tuesday"
    tue_way = yao_budunit.make_way(week_way, tue_str)
    mon_premise_x = premiseunit_shop(pbranch=mon_way)
    mon_premise_x._status = False
    mon_premise_x._task = False
    tue_premise_x = premiseunit_shop(pbranch=tue_way)
    tue_premise_x._status = False
    tue_premise_x._task = False
    mt_premises = {
        mon_premise_x.pbranch: mon_premise_x,
        tue_premise_x.pbranch: tue_premise_x,
    }
    mt_reasonunit = reasonunit_shop(week_way, premises=mt_premises)
    mt_reasonheir = reasonheir_shop(week_way, premises=mt_premises, _status=False)
    x_idearoot = yao_budunit.get_idea_obj(to_way(yao_budunit.fisc_word))
    x_idearoot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_budunit.reasonunits[week_way].rcontext=}")
    # print(f"{yao_budunit.reasonunits[week_way].premises[mon_way].pbranch=}")
    # print(f"{yao_budunit.reasonunits[week_way].premises[tue_way].pbranch=}")
    week_reasonunit = x_idearoot.reasonunits[week_way]
    print(f"{week_reasonunit.premises=}")
    premise_mon = week_reasonunit.premises.get(mon_way)
    premise_tue = week_reasonunit.premises.get(tue_way)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.pbranch]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.pbranch]
    assert week_reasonunit == mt_reasonunit

    # WHEN
    idea_dict = yao_budunit.get_idea_dict()

    # THEN
    gen_week_reasonheir = x_idearoot.get_reasonheir(week_way)
    gen_mon_premise = gen_week_reasonheir.premises.get(mon_way)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_way)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_way)
    assert gen_week_reasonheir.premises == mt_reasonheir.premises
    assert gen_week_reasonheir == mt_reasonheir

    casa_str = "casa"
    casa_way = yao_budunit.make_l1_way(casa_str)
    bird_str = "say hi to birds"
    bird_way = yao_budunit.make_way(casa_way, bird_str)
    assert from_list_get_active(bird_way, idea_dict) is False

    # yao_budunit.add_fact(fcontext=week_way, fbranch=mon_way)
    # idea_dict = yao_budunit.get_idea_dict()
    # casa_idea = x_idearoot._kids[casa_str]
    # twee_idea = casa_idea._kids[bird_str]
    # print(f"{len(x_idearoot._reasonheirs)=}")
    # print(f"{len(casa_idea._reasonheirs)=}")
    # print(f"{len(twee_idea._reasonheirs)=}")

    # assert YR.get_active(way=bird_idea, idea_dict=idea_dict) is True

    # yao_budunit.add_fact(fcontext=f"{yao_budunit.fisc_word},weekdays", fbranch=f"{yao_budunit.fisc_word},weekdays,Tuesday")
    # idea_dict = yao_budunit.get_idea_dict()
    # assert YR.get_active(way=bird_idea, idea_dict=idea_dict) is True

    # yao_budunit.add_fact(fcontext=f"{yao_budunit.fisc_word},weekdays", fbranch=f"{yao_budunit.fisc_word},weekdays,Wednesday")
    # idea_dict = yao_budunit.get_idea_dict()
    # assert YR.get_active(way=bird_idea, idea_dict=idea_dict) is False


def test_BudUnit_settle_bud_CorrectlySetsIdeaUnitsActiveWithEvery6WeeksReason_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    day_str = "day_hour"
    day_way = yao_budunit.make_l1_way(day_str)
    min_str = "day_minute"
    min_way = yao_budunit.make_l1_way(day_str)

    # WHEN
    yao_budunit.add_fact(fcontext=day_way, fbranch=day_way, fopen=0, fnigh=23)
    yao_budunit.add_fact(fcontext=min_way, fbranch=min_way, fopen=0, fnigh=59)
    yao_budunit.settle_bud()

    # THEN
    ced_week_rcontext = yao_budunit.make_l1_way("ced_week")

    pdivisor = None
    popen = None
    pnigh = None
    print(f"{len(yao_budunit._idea_dict)=}")

    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    clean_couch_way = yao_budunit.make_way(cleaning_way, "clean sheets couch blankets")
    clean_sheet_idea = yao_budunit.get_idea_obj(clean_couch_way)
    # print(f"{clean_sheet_idea.reasonunits.values()=}")
    ced_week_reason = clean_sheet_idea.reasonunits.get(ced_week_rcontext)
    ced_week_premise = ced_week_reason.premises.get(ced_week_rcontext)
    print(
        f"{clean_sheet_idea.idea_word=} {ced_week_reason.rcontext=} {ced_week_premise.pbranch=}"
    )
    # print(f"{clean_sheet_idea.idea_word=} {ced_week_reason.rcontext=} {premise_x=}")
    pdivisor = ced_week_premise.pdivisor
    popen = ced_week_premise.popen
    pnigh = ced_week_premise.pnigh
    # print(f"{idea.reasonunits=}")
    assert clean_sheet_idea._active is False

    # for idea in idea_dict:
    #     # print(f"{idea.parent_way=}")
    #     if idea.idea_word == "clean sheets couch blankets":
    #         print(f"{idea.get_idea_way()=}")

    assert pdivisor == 6
    assert popen == 1
    print(
        f"There exists a idea with a reason_rcontext {ced_week_rcontext} that also has lemmet div =6 and popen/pnigh =1"
    )
    # print(f"{len(idea_dict)=}")
    ced_week_popen = 6001

    # WHEN
    yao_budunit.add_fact(
        ced_week_rcontext,
        fbranch=ced_week_rcontext,
        fopen=ced_week_popen,
        fnigh=ced_week_popen,
    )
    nation_str = "Nation-States"
    nation_way = yao_budunit.make_l1_way(nation_str)
    yao_budunit.add_fact(fcontext=nation_way, fbranch=nation_way)
    print(
        f"Nation-states set and also fact set: {ced_week_rcontext=} with {ced_week_popen=} and {ced_week_popen=}"
    )
    print(f"{yao_budunit.idearoot.factunits=}")
    yao_budunit.settle_bud()

    # THEN
    week_str = "ced_week"
    week_way = yao_budunit.make_l1_way(week_str)
    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    clean_couch_str = "clean sheets couch blankets"
    clean_couch_way = yao_budunit.make_way(cleaning_way, clean_couch_str)
    clean_couch_idea = yao_budunit.get_idea_obj(way=clean_couch_way)
    week_reason = clean_couch_idea.reasonunits.get(week_way)
    week_premise = week_reason.premises.get(week_way)
    print(f"{clean_couch_idea.idea_word=} {week_reason.rcontext=} {week_premise=}")
    assert week_premise.pdivisor == 6 and week_premise.popen == 1


def test_BudUnit_settle_bud_EveryIdeaHasActiveStatus_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    print(f"{len(yao_budunit._idea_dict)=}")
    # first_idea_kid_count = 0
    # first_idea_kid_none_count = 0
    # first_idea_kid_true_count = 0
    # first_idea_kid_false_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
    #         first_idea_kid_count += 1
    #         if idea._active is None:
    #             first_idea_kid_none_count += 1
    #         elif idea._active:
    #             first_idea_kid_true_count += 1
    #         elif idea._active is False:
    #             first_idea_kid_false_count += 1

    # print(f"{first_idea_kid_count=}")
    # print(f"{first_idea_kid_none_count=}")
    # print(f"{first_idea_kid_true_count=}")
    # print(f"{first_idea_kid_false_count=}")

    # idea_kid_count = 0
    # for idea in idea_list_without_idearoot:
    #     idea_kid_count += 1
    #     print(f"{idea.idea_word=} {idea_kid_count=}")
    #     assert idea._active is not None
    #     assert idea._active in (True, False)
    # assert idea_kid_count == len(idea_list_without_idearoot)

    assert len(yao_budunit._idea_dict) == sum(
        idea._active is not None for idea in yao_budunit._idea_dict.values()
    )


def test_BudUnit_settle_bud_EveryTwoMonthReturnsObj_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    minute_str = "day_minute"
    minute_way = yao_budunit.make_l1_way(minute_str)
    yao_budunit.add_fact(fcontext=minute_way, fbranch=minute_way, fopen=0, fnigh=1399)
    month_str = "month_week"
    month_way = yao_budunit.make_l1_way(month_str)
    yao_budunit.add_fact(fcontext=month_way, fbranch=month_way)
    nations_str = "Nation-States"
    nations_way = yao_budunit.make_l1_way(nations_str)
    yao_budunit.add_fact(fcontext=nations_way, fbranch=nations_way)
    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fcontext=mood_way, fbranch=mood_way)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_way = yao_budunit.make_l1_way(aaron_str)
    yao_budunit.add_fact(fcontext=aaron_way, fbranch=aaron_way)
    interweb_str = "Interweb"
    interweb_way = yao_budunit.make_l1_way(interweb_str)
    yao_budunit.add_fact(fcontext=interweb_way, fbranch=interweb_way)
    weekdays_str = "weekdays"
    weekdays_way = yao_budunit.make_l1_way(weekdays_str)
    yao_budunit.add_fact(fcontext=weekdays_way, fbranch=weekdays_way)
    idea_dict = yao_budunit.get_idea_dict()
    print(f"{len(idea_dict)=}")

    casa_str = "casa"
    casa_way = yao_budunit.make_l1_way(casa_str)
    clean_str = "cleaning"
    clean_way = yao_budunit.make_way(casa_way, clean_str)
    mat_idea_word = "deep clean play mat"
    mat_way = yao_budunit.make_way(clean_way, mat_idea_word)
    assert from_list_get_active(mat_way, idea_dict) is False

    year_month_rcontext = yao_budunit.make_l1_way("year_month")
    print(f"{year_month_rcontext=}, {year_month_rcontext=}")

    # WHEN
    yao_budunit.add_fact(
        year_month_rcontext, fbranch=year_month_rcontext, fopen=0, fnigh=8
    )
    ced_week = yao_budunit.make_l1_way("ced_week")
    yao_budunit.add_fact(fcontext=ced_week, fbranch=ced_week, fopen=0, fnigh=4)
    yao_budunit.settle_bud()

    # THEN
    print(f"{len(idea_dict)=}")
    print(f"{len(yao_budunit.idearoot.factunits)=}")
    assert from_list_get_active(mat_way, yao_budunit._idea_dict)


def test_BudUnit_settle_bud_CorrectlySetsEmpty_sum_healerlink_share():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    assert sue_budunit._sum_healerlink_share == 0
    assert sue_budunit._keep_dict == {}

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._sum_healerlink_share == 0
    assert sue_budunit._keep_dict == {}


def test_BudUnit_settle_bud_CorrectlySets_sum_healerlink_share(graphics_bool):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    sue_budunit.add_acctunit("Sue")
    sue_budunit.settle_bud()
    nation_way = sue_budunit.make_l1_way("nation-state")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_budunit.edit_idea_attr(oregon_way, problem_bool=True, healerlink=sue_healerlink)
    oregon_idea = sue_budunit.get_idea_obj(oregon_way)
    print(f"{oregon_idea._fund_ratio=}")
    assert sue_budunit._sum_healerlink_share == 0
    assert oregon_idea._healerlink_ratio == 0

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._sum_healerlink_share == 0.038461539 * default_fund_pool()
    assert oregon_idea._healerlink_ratio == 1

    # WHEN
    week_way = sue_budunit.make_l1_way("weekdays")
    sue_budunit.edit_idea_attr(week_way, problem_bool=True)
    mon_way = sue_budunit.make_way(week_way, "Monday")
    sue_budunit.edit_idea_attr(mon_way, healerlink=sue_healerlink)
    mon_idea = sue_budunit.get_idea_obj(mon_way)
    # print(f"{mon_idea.problem_bool=} {mon_idea._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._sum_healerlink_share != 0.038461539 * default_fund_pool()
    assert sue_budunit._sum_healerlink_share == 0.06923077 * default_fund_pool()
    assert oregon_idea._healerlink_ratio == 0.5555555571604938
    assert mon_idea._healerlink_ratio == 0.4444444428395062

    # WHEN
    tue_way = sue_budunit.make_way(week_way, "Tuesday")
    sue_budunit.edit_idea_attr(tue_way, healerlink=sue_healerlink)
    tue_idea = sue_budunit.get_idea_obj(tue_way)
    # print(f"{tue_idea.problem_bool=} {tue_idea._fund_ratio=}")
    # sat_way = sue_budunit.make_way(week_way, "Saturday")
    # sat_idea = sue_budunit.get_idea_obj(sat_way)
    # print(f"{sat_idea.problem_bool=} {sat_idea._fund_ratio=}")
    sue_budunit.settle_bud()

    # THEN
    assert (
        sue_budunit._sum_healerlink_share != 0.06923076923076923 * default_fund_pool()
    )
    assert sue_budunit._sum_healerlink_share == 0.100000001 * default_fund_pool()
    assert oregon_idea._healerlink_ratio == 0.38461538615384616
    assert mon_idea._healerlink_ratio == 0.3076923069230769
    assert tue_idea._healerlink_ratio == 0.3076923069230769

    # WHEN
    sue_budunit.edit_idea_attr(week_way, healerlink=sue_healerlink)
    week_idea = sue_budunit.get_idea_obj(week_way)
    print(f"{week_idea.idea_word=} {week_idea.problem_bool=} {week_idea._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    display_ideatree(sue_budunit, "Keep", graphics_bool)
    assert sue_budunit._sum_healerlink_share == 0
    assert oregon_idea._healerlink_ratio == 0
    assert mon_idea._healerlink_ratio == 0
    assert tue_idea._healerlink_ratio == 0


def test_BudUnit_settle_bud_CorrectlySets_keep_dict_v1(graphics_bool):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    sue_budunit.add_acctunit("Sue")
    sue_budunit.settle_bud()
    nation_way = sue_budunit.make_l1_way("nation-state")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_budunit.edit_idea_attr(oregon_way, problem_bool=True, healerlink=sue_healerlink)
    assert len(sue_budunit._keep_dict) == 0
    assert sue_budunit._keep_dict.get(oregon_way) is None

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert len(sue_budunit._keep_dict) == 1
    assert sue_budunit._keep_dict.get(oregon_way) is not None

    # WHEN
    week_way = sue_budunit.make_l1_way("weekdays")
    sue_budunit.edit_idea_attr(week_way, problem_bool=True)
    mon_way = sue_budunit.make_way(week_way, "Monday")
    sue_budunit.edit_idea_attr(mon_way, healerlink=sue_healerlink)
    # mon_idea = sue_budunit.get_idea_obj(mon_way)
    # print(f"{mon_idea.problem_bool=} {mon_idea._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    assert len(sue_budunit._keep_dict) == 2
    assert sue_budunit._keep_dict.get(oregon_way) is not None
    assert sue_budunit._keep_dict.get(mon_way) is not None

    # WHEN
    tue_way = sue_budunit.make_way(week_way, "Tuesday")
    sue_budunit.edit_idea_attr(tue_way, healerlink=sue_healerlink)
    # tue_idea = sue_budunit.get_idea_obj(tue_way)
    # print(f"{tue_idea.problem_bool=} {tue_idea._fund_ratio=}")
    # sat_way = sue_budunit.make_way(week_way, "Saturday")
    # sat_idea = sue_budunit.get_idea_obj(sat_way)
    # print(f"{sat_idea.problem_bool=} {sat_idea._fund_ratio=}")
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._keep_dict) == 3
    assert sue_budunit._keep_dict.get(oregon_way) is not None
    assert sue_budunit._keep_dict.get(mon_way) is not None
    assert sue_budunit._keep_dict.get(tue_way) is not None

    # WHEN
    sue_budunit.edit_idea_attr(week_way, healerlink=sue_healerlink)
    week_idea = sue_budunit.get_idea_obj(week_way)
    print(f"{week_idea.idea_word=} {week_idea.problem_bool=} {week_idea._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    display_ideatree(sue_budunit, "Keep", graphics_bool)
    assert len(sue_budunit._keep_dict) == 0
    assert sue_budunit._keep_dict == {}


def test_BudUnit_settle_bud_CorrectlySets_healers_dict():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    sue_budunit.add_acctunit(sue_str)
    sue_budunit.add_acctunit(bob_str)
    assert sue_budunit._healers_dict == {}

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._healers_dict == {}

    # ESTABLISH
    nation_way = sue_budunit.make_l1_way("nation-state")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_idea_attr(oregon_way, problem_bool=True, healerlink=sue_healerlink)

    week_way = sue_budunit.make_l1_way("weekdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_budunit.edit_idea_attr(week_way, problem_bool=True, healerlink=bob_healerlink)
    assert sue_budunit._healers_dict == {}

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._healers_dict) == 2
    week_idea = sue_budunit.get_idea_obj(week_way)
    assert sue_budunit._healers_dict.get(bob_str) == {week_way: week_idea}
    oregon_idea = sue_budunit.get_idea_obj(oregon_way)
    assert sue_budunit._healers_dict.get(sue_str) == {oregon_way: oregon_idea}


def test_BudUnit_settle_bud_CorrectlySets_keeps_buildable_True():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    sue_budunit.add_acctunit(sue_str)
    sue_budunit.add_acctunit(bob_str)
    assert sue_budunit._keeps_buildable is False

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._keeps_buildable

    # ESTABLISH
    nation_way = sue_budunit.make_l1_way("nation-state")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_idea_attr(oregon_way, problem_bool=True, healerlink=sue_healerlink)

    week_way = sue_budunit.make_l1_way("weekdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_budunit.edit_idea_attr(week_way, problem_bool=True, healerlink=bob_healerlink)

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._keeps_buildable


def test_BudUnit_settle_bud_CorrectlySets_keeps_buildable_False():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    sue_budunit.add_acctunit(sue_str)
    sue_budunit.add_acctunit(bob_str)
    assert sue_budunit._keeps_buildable is False

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._keeps_buildable

    # ESTABLISH
    nation_way = sue_budunit.make_l1_way("nation-state")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    bend_str = "Be/nd"
    bend_way = sue_budunit.make_way(oregon_way, bend_str)
    sue_budunit.set_idea(ideaunit_shop(bend_str), oregon_way)
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_idea_attr(bend_way, problem_bool=True, healerlink=sue_healerlink)
    assert sue_budunit._keeps_buildable

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._keeps_buildable is False
