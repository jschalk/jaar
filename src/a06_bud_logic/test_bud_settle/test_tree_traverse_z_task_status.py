from src.a01_way_logic.way import to_way
from src.a02_finance_logic.finance_config import default_fund_pool
from src.a04_reason_logic.reason_concept import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_graphics import display_concepttree
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

    # for concept in sue_budunit._concept_dict.values():
    #     print(f"{casa_way=} {concept.get_concept_way()=}")
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    assert sue_budunit.get_concept_obj(casa_way)._active is None

    # WHEN
    sue_budunit.add_fact(fcontext=week_way, fstate=sun_way)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._concept_dict != {}
    assert len(sue_budunit._concept_dict) == 17

    # for concept in sue_budunit._concept_dict.values():
    #     print(f"{casa_way=} {concept.get_concept_way()=}")
    assert sue_budunit.get_concept_obj(casa_way)._active is False


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
    sue_budunit.add_fact(fcontext=week_way, fstate=sun_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._concept_dict
    assert len(sue_budunit._concept_dict) == 17
    assert sue_budunit._concept_dict.get(casa_way)._active is False

    # WHEN
    nation_str = "nation"
    nation_way = sue_budunit.make_l1_way(nation_str)
    usa_str = "USA"
    usa_way = sue_budunit.make_way(nation_way, usa_str)
    sue_budunit.add_fact(fcontext=nation_way, fstate=usa_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._concept_dict
    assert len(sue_budunit._concept_dict) == 17
    assert sue_budunit._concept_dict.get(casa_way)._active

    # WHEN
    france_str = "France"
    france_way = sue_budunit.make_way(nation_way, france_str)
    sue_budunit.add_fact(fcontext=nation_way, fstate=france_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._concept_dict
    assert len(sue_budunit._concept_dict) == 17
    assert sue_budunit._concept_dict.get(casa_way)._active is False


def test_BudUnit_settle_bud_CorrectlySets_concept_dict():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_way = sue_budunit.make_l1_way(week_str)
    wed_str = "Wednesday"
    wed_way = sue_budunit.make_way(week_way, wed_str)
    nation_str = "nation"
    nation_way = sue_budunit.make_l1_way(nation_str)
    france_str = "France"
    france_way = sue_budunit.make_way(nation_way, france_str)
    sue_budunit.add_fact(fcontext=week_way, fstate=wed_way)
    sue_budunit.add_fact(fcontext=nation_way, fstate=france_way)

    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_concept = sue_budunit.get_concept_obj(casa_way)
    print(f"{sue_budunit.owner_name=} {len(casa_concept.reasonunits)=}")
    # print(f"{casa_concept.reasonunits=}")
    print(f"{sue_budunit.owner_name=} {len(sue_budunit.conceptroot.factunits)=}")
    # print(f"{sue_budunit.conceptroot.factunits=}")

    sue_budunit.settle_bud()
    assert sue_budunit._concept_dict
    assert len(sue_budunit._concept_dict) == 17

    usa_str = "USA"
    usa_way = sue_budunit.make_way(nation_way, usa_str)
    oregon_str = "Oregon"
    oregon_way = sue_budunit.make_way(usa_way, oregon_str)

    wed = premiseunit_shop(pstate=wed_way)
    wed._status = True
    wed._task = False
    usa = premiseunit_shop(pstate=usa_way)
    usa._status = True
    usa._task = False

    wed_lu = reasonunit_shop(week_way, premises={wed.pstate: wed})
    sta_lu = reasonunit_shop(nation_way, premises={usa.pstate: usa})
    wed_lh = reasonheir_shop(
        rcontext=week_way,
        premises={wed.pstate: wed},
        _status=True,
        _task=False,
        _rcontext_concept_active_value=True,
    )
    sta_lh = reasonheir_shop(
        rcontext=nation_way,
        premises={usa.pstate: usa},
        _status=True,
        _task=False,
        _rcontext_concept_active_value=True,
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
    sue_budunit.add_fact(fcontext=nation_way, fstate=oregon_way)
    sue_budunit.settle_bud()

    # THEN
    casa_concept = sue_budunit._concept_dict.get(casa_way)
    print(f"\nlook at {casa_concept.get_concept_way()=}")
    assert casa_concept.parent_way == to_way(sue_budunit.fisc_label)
    assert casa_concept._kids == {}
    assert casa_concept.mass == 30
    assert casa_concept.concept_label == casa_str
    assert casa_concept._level == 1
    assert casa_concept._active
    assert casa_concept.pledge
    # print(f"{casa_concept._reasonheirs=}")
    nation_reasonheir = casa_concept._reasonheirs[nation_way]
    print(f"  {nation_reasonheir=}")
    print(f"  {nation_reasonheir._status=}\n")
    # assert casa_concept._reasonheirs == x1_reasonheirs

    assert len(casa_concept._reasonheirs) == len(x1_reasonheirs)
    week_reasonheir = casa_concept._reasonheirs.get(week_way)
    # usa_premise = week_reasonheir.premises.get(usa_way)
    print(f"    {casa_concept.concept_label=}")
    # print(f"    {usa_premise.rcontext=}")
    # print(f"    {usa_premise._task=}")
    # print(f"    {usa_premise._task=}")
    assert week_reasonheir._task is False
    # print(f"      premises: {w=}")
    # w_state = usa_premise.premises[wed_way].pstate
    # print(f"      {w_state=}")
    # assert usa_premise._task == w_state._task
    # assert usa_premise._status == w_state._status
    # assert week_reasonheir.premises == week_reasonheir.premises

    # assert casa_concept.reasonunits == x1_reasonunits

    # print("iterate through every concept...")
    # for x_concept in concept_dict:
    #     if str(type(x_concept)).find(".concept.ConceptUnit'>") > 0:
    #         assert x_concept._active is not None

    #     # print("")
    #     # print(f"{x_concept.concept_label=}")
    #     # print(f"{len(x_concept.reasonunits)=}")
    #     print(
    #         f"  {x_concept.concept_label} iterate through every reasonheir... {len(x_concept._reasonheirs)=} {x_concept.concept_label=}"
    #     )
    #     # print(f"{x_concept._reasonheirs=}")
    #     for reason in x_concept._reasonheirs.values():
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
    assert sue_budunit._concept_dict.get(clean_way)._active is False

    # set facts as midevening to 8am
    time_str = "timetech"
    time_way = sue_budunit.make_l1_way(time_str)
    day24hr_str = "24hr day"
    day24hr_way = sue_budunit.make_way(time_way, day24hr_str)
    day24hr_rcontext = day24hr_way
    day24hr_fstate = day24hr_way
    day24hr_popen = 0.0
    day24hr_pnigh = 8.0

    # WHEN
    sue_budunit.add_fact(
        day24hr_rcontext,
        fstate=day24hr_fstate,
        fopen=day24hr_popen,
        fnigh=day24hr_pnigh,
    )

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._concept_dict.get(clean_way)._active

    # WHEN
    # set facts as 8am to 10am
    day24hr_popen = 8.0
    day24hr_pnigh = 10.0
    print(sue_budunit.conceptroot.factunits[day24hr_way])
    sue_budunit.add_fact(
        day24hr_rcontext,
        fstate=day24hr_fstate,
        fopen=day24hr_popen,
        fnigh=day24hr_pnigh,
    )
    print(sue_budunit.conceptroot.factunits[day24hr_way])
    print(sue_budunit.conceptroot._kids[house_str]._kids[clean_str].reasonunits)
    # sue_budunit.conceptroot._kids["housemanagement"]._kids[clean_str]._active = None

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._concept_dict.get(clean_way)._active is False


def test_BudUnit_get_agenda_dict_ReturnsObj():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()

    # WHEN
    pledge_concepts = sue_budunit.get_agenda_dict()

    # THEN
    assert pledge_concepts is not None
    assert len(pledge_concepts) > 0
    assert len(pledge_concepts) == 1


def test_BudUnit_settle_bud_CorrectlySetsData_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    print(f"{yao_budunit.get_reason_rcontexts()=}")
    # day_hour = f"{yao_budunit.fisc_label},day_hour"
    # yao_budunit.add_fact(fcontext=day_hour, fstate=day_hour, popen=0, pnigh=23)
    day_min_str = "day_minute"
    day_min_way = yao_budunit.make_l1_way(day_min_str)
    yao_budunit.add_fact(fcontext=day_min_way, fstate=day_min_way, fopen=0, fnigh=1439)

    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fcontext=mood_way, fstate=mood_way)
    print(f"{yao_budunit.get_reason_rcontexts()=}")

    yr_mon_str = "year_month"
    yr_mon_way = yao_budunit.make_l1_way(yr_mon_str)
    yao_budunit.add_fact(fcontext=yr_mon_way, fstate=yr_mon_way)
    inter_str = "Interweb"
    inter_way = yao_budunit.make_l1_way(inter_str)
    yao_budunit.add_fact(fcontext=inter_way, fstate=inter_way)
    assert yao_budunit is not None
    # print(f"{yao_budunit.owner_name=}")
    # print(f"{len(yao_budunit.conceptroot._kids)=}")
    ulty_str = "Ultimate Frisbee"
    ulty_way = yao_budunit.make_l1_way(ulty_str)

    # if yao_budunit.conceptroot._kids["Ultimate Frisbee"].concept_label == "Ultimate Frisbee":
    assert yao_budunit.conceptroot._kids[ulty_str].reasonunits is not None
    assert yao_budunit.owner_name is not None

    # for fact in yao_budunit.conceptroot.factunits.values():
    #     print(f"{fact=}")

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    # print(f"{str(type(concept))=}")
    # print(f"{len(concept_dict)=}")
    laundry_str = "laundry monday"
    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    laundry_way = yao_budunit.make_way(cleaning_way, laundry_str)

    # for concept in concept_dict:
    #     assert (
    #         str(type(concept)).find(".concept.ConceptUnit'>") > 0
    #         or str(type(concept)).find(".concept.ConceptUnit'>") > 0
    #     )
    #     # print(f"{concept.concept_label=}")
    #     if concept.concept_label == laundry_str:
    #         for reason in concept.reasonunits.values():
    #             print(f"{concept.concept_label=} {reason.rcontext=}")  # {reason.premises=}")
    # assert concept._active is False
    assert yao_budunit._concept_dict.get(laundry_way)._active is False

    # WHEN
    week_str = "weekdays"
    week_way = yao_budunit.make_l1_way(week_str)
    mon_str = "Monday"
    mon_way = yao_budunit.make_way(week_way, mon_str)
    yao_budunit.add_fact(fcontext=week_way, fstate=mon_way)
    yao_budunit.settle_bud()

    # THEN
    assert yao_budunit._concept_dict.get(laundry_way)._active is False


def test_BudUnit_settle_bud_OptionWeekdaysReturnsObj_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()

    day_hr_str = "day_hour"
    day_hr_way = yao_budunit.make_l1_way(day_hr_str)
    yao_budunit.add_fact(fcontext=day_hr_way, fstate=day_hr_way, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_way = yao_budunit.make_l1_way(day_min_str)
    yao_budunit.add_fact(fcontext=day_min_way, fstate=day_min_way, fopen=0, fnigh=59)
    mon_wk_str = "month_week"
    mon_wk_way = yao_budunit.make_l1_way(mon_wk_str)
    yao_budunit.add_fact(fcontext=mon_wk_way, fstate=mon_wk_way)
    nation_str = "Nation-States"
    nation_way = yao_budunit.make_l1_way(nation_str)
    yao_budunit.add_fact(fcontext=nation_way, fstate=nation_way)
    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fcontext=mood_way, fstate=mood_way)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_way = yao_budunit.make_l1_way(aaron_str)
    yao_budunit.add_fact(fcontext=aaron_way, fstate=aaron_way)
    inter_str = "Interweb"
    inter_way = yao_budunit.make_l1_way(inter_str)
    yao_budunit.add_fact(fcontext=inter_way, fstate=inter_way)
    yr_mon_str = "year_month"
    yr_mon_way = yao_budunit.make_l1_way(yr_mon_str)
    yao_budunit.add_fact(fcontext=yr_mon_way, fstate=yr_mon_way, fopen=0, fnigh=1000)

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
    mon_premise_x = premiseunit_shop(pstate=mon_way)
    mon_premise_x._status = False
    mon_premise_x._task = False
    tue_premise_x = premiseunit_shop(pstate=tue_way)
    tue_premise_x._status = False
    tue_premise_x._task = False
    mt_premises = {
        mon_premise_x.pstate: mon_premise_x,
        tue_premise_x.pstate: tue_premise_x,
    }
    mt_reasonunit = reasonunit_shop(week_way, premises=mt_premises)
    mt_reasonheir = reasonheir_shop(week_way, premises=mt_premises, _status=False)
    x_conceptroot = yao_budunit.get_concept_obj(to_way(yao_budunit.fisc_label))
    x_conceptroot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_budunit.reasonunits[week_way].rcontext=}")
    # print(f"{yao_budunit.reasonunits[week_way].premises[mon_way].pstate=}")
    # print(f"{yao_budunit.reasonunits[week_way].premises[tue_way].pstate=}")
    week_reasonunit = x_conceptroot.reasonunits[week_way]
    print(f"{week_reasonunit.premises=}")
    premise_mon = week_reasonunit.premises.get(mon_way)
    premise_tue = week_reasonunit.premises.get(tue_way)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.pstate]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.pstate]
    assert week_reasonunit == mt_reasonunit

    # WHEN
    concept_dict = yao_budunit.get_concept_dict()

    # THEN
    gen_week_reasonheir = x_conceptroot.get_reasonheir(week_way)
    gen_mon_premise = gen_week_reasonheir.premises.get(mon_way)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_way)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_way)
    assert gen_week_reasonheir.premises == mt_reasonheir.premises
    assert gen_week_reasonheir == mt_reasonheir

    casa_str = "casa"
    casa_way = yao_budunit.make_l1_way(casa_str)
    bird_str = "say hi to birds"
    bird_way = yao_budunit.make_way(casa_way, bird_str)
    assert from_list_get_active(bird_way, concept_dict) is False

    # yao_budunit.add_fact(fcontext=week_way, fstate=mon_way)
    # concept_dict = yao_budunit.get_concept_dict()
    # casa_concept = x_conceptroot._kids[casa_str]
    # twee_concept = casa_concept._kids[bird_str]
    # print(f"{len(x_conceptroot._reasonheirs)=}")
    # print(f"{len(casa_concept._reasonheirs)=}")
    # print(f"{len(twee_concept._reasonheirs)=}")

    # assert YR.get_active(way=bird_concept, concept_dict=concept_dict) is True

    # yao_budunit.add_fact(fcontext=f"{yao_budunit.fisc_label},weekdays", fstate=f"{yao_budunit.fisc_label},weekdays,Tuesday")
    # concept_dict = yao_budunit.get_concept_dict()
    # assert YR.get_active(way=bird_concept, concept_dict=concept_dict) is True

    # yao_budunit.add_fact(fcontext=f"{yao_budunit.fisc_label},weekdays", fstate=f"{yao_budunit.fisc_label},weekdays,Wednesday")
    # concept_dict = yao_budunit.get_concept_dict()
    # assert YR.get_active(way=bird_concept, concept_dict=concept_dict) is False


def test_BudUnit_settle_bud_CorrectlySetsConceptUnitsActiveWithEvery6WeeksReason_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    day_str = "day_hour"
    day_way = yao_budunit.make_l1_way(day_str)
    min_str = "day_minute"
    min_way = yao_budunit.make_l1_way(day_str)

    # WHEN
    yao_budunit.add_fact(fcontext=day_way, fstate=day_way, fopen=0, fnigh=23)
    yao_budunit.add_fact(fcontext=min_way, fstate=min_way, fopen=0, fnigh=59)
    yao_budunit.settle_bud()

    # THEN
    ced_week_rcontext = yao_budunit.make_l1_way("ced_week")

    pdivisor = None
    popen = None
    pnigh = None
    print(f"{len(yao_budunit._concept_dict)=}")

    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    clean_couch_way = yao_budunit.make_way(cleaning_way, "clean sheets couch blankets")
    clean_sheet_concept = yao_budunit.get_concept_obj(clean_couch_way)
    # print(f"{clean_sheet_concept.reasonunits.values()=}")
    ced_week_reason = clean_sheet_concept.reasonunits.get(ced_week_rcontext)
    ced_week_premise = ced_week_reason.premises.get(ced_week_rcontext)
    print(
        f"{clean_sheet_concept.concept_label=} {ced_week_reason.rcontext=} {ced_week_premise.pstate=}"
    )
    # print(f"{clean_sheet_concept.concept_label=} {ced_week_reason.rcontext=} {premise_x=}")
    pdivisor = ced_week_premise.pdivisor
    popen = ced_week_premise.popen
    pnigh = ced_week_premise.pnigh
    # print(f"{concept.reasonunits=}")
    assert clean_sheet_concept._active is False

    # for concept in concept_dict:
    #     # print(f"{concept.parent_way=}")
    #     if concept.concept_label == "clean sheets couch blankets":
    #         print(f"{concept.get_concept_way()=}")

    assert pdivisor == 6
    assert popen == 1
    print(
        f"There exists a concept with a reason_rcontext {ced_week_rcontext} that also has lemmet div =6 and popen/pnigh =1"
    )
    # print(f"{len(concept_dict)=}")
    ced_week_popen = 6001

    # WHEN
    yao_budunit.add_fact(
        ced_week_rcontext,
        fstate=ced_week_rcontext,
        fopen=ced_week_popen,
        fnigh=ced_week_popen,
    )
    nation_str = "Nation-States"
    nation_way = yao_budunit.make_l1_way(nation_str)
    yao_budunit.add_fact(fcontext=nation_way, fstate=nation_way)
    print(
        f"Nation set and also fact set: {ced_week_rcontext=} with {ced_week_popen=} and {ced_week_popen=}"
    )
    print(f"{yao_budunit.conceptroot.factunits=}")
    yao_budunit.settle_bud()

    # THEN
    week_str = "ced_week"
    week_way = yao_budunit.make_l1_way(week_str)
    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    clean_couch_str = "clean sheets couch blankets"
    clean_couch_way = yao_budunit.make_way(cleaning_way, clean_couch_str)
    clean_couch_concept = yao_budunit.get_concept_obj(way=clean_couch_way)
    week_reason = clean_couch_concept.reasonunits.get(week_way)
    week_premise = week_reason.premises.get(week_way)
    print(
        f"{clean_couch_concept.concept_label=} {week_reason.rcontext=} {week_premise=}"
    )
    assert week_premise.pdivisor == 6 and week_premise.popen == 1


def test_BudUnit_settle_bud_EveryConceptHasActiveStatus_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    print(f"{len(yao_budunit._concept_dict)=}")
    # first_concept_kid_count = 0
    # first_concept_kid_none_count = 0
    # first_concept_kid_true_count = 0
    # first_concept_kid_false_count = 0
    # for concept in concept_list:
    #     if str(type(concept)).find(".concept.ConceptUnit'>") > 0:
    #         first_concept_kid_count += 1
    #         if concept._active is None:
    #             first_concept_kid_none_count += 1
    #         elif concept._active:
    #             first_concept_kid_true_count += 1
    #         elif concept._active is False:
    #             first_concept_kid_false_count += 1

    # print(f"{first_concept_kid_count=}")
    # print(f"{first_concept_kid_none_count=}")
    # print(f"{first_concept_kid_true_count=}")
    # print(f"{first_concept_kid_false_count=}")

    # concept_kid_count = 0
    # for concept in concept_list_without_conceptroot:
    #     concept_kid_count += 1
    #     print(f"{concept.concept_label=} {concept_kid_count=}")
    #     assert concept._active is not None
    #     assert concept._active in (True, False)
    # assert concept_kid_count == len(concept_list_without_conceptroot)

    assert len(yao_budunit._concept_dict) == sum(
        concept._active is not None for concept in yao_budunit._concept_dict.values()
    )


def test_BudUnit_settle_bud_EveryTwoMonthReturnsObj_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    minute_str = "day_minute"
    minute_way = yao_budunit.make_l1_way(minute_str)
    yao_budunit.add_fact(fcontext=minute_way, fstate=minute_way, fopen=0, fnigh=1399)
    month_str = "month_week"
    month_way = yao_budunit.make_l1_way(month_str)
    yao_budunit.add_fact(fcontext=month_way, fstate=month_way)
    nations_str = "Nation-States"
    nations_way = yao_budunit.make_l1_way(nations_str)
    yao_budunit.add_fact(fcontext=nations_way, fstate=nations_way)
    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fcontext=mood_way, fstate=mood_way)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_way = yao_budunit.make_l1_way(aaron_str)
    yao_budunit.add_fact(fcontext=aaron_way, fstate=aaron_way)
    interweb_str = "Interweb"
    interweb_way = yao_budunit.make_l1_way(interweb_str)
    yao_budunit.add_fact(fcontext=interweb_way, fstate=interweb_way)
    weekdays_str = "weekdays"
    weekdays_way = yao_budunit.make_l1_way(weekdays_str)
    yao_budunit.add_fact(fcontext=weekdays_way, fstate=weekdays_way)
    concept_dict = yao_budunit.get_concept_dict()
    print(f"{len(concept_dict)=}")

    casa_str = "casa"
    casa_way = yao_budunit.make_l1_way(casa_str)
    clean_str = "cleaning"
    clean_way = yao_budunit.make_way(casa_way, clean_str)
    mat_concept_label = "deep clean play mat"
    mat_way = yao_budunit.make_way(clean_way, mat_concept_label)
    assert from_list_get_active(mat_way, concept_dict) is False

    year_month_rcontext = yao_budunit.make_l1_way("year_month")
    print(f"{year_month_rcontext=}, {year_month_rcontext=}")

    # WHEN
    yao_budunit.add_fact(
        year_month_rcontext, fstate=year_month_rcontext, fopen=0, fnigh=8
    )
    ced_week = yao_budunit.make_l1_way("ced_week")
    yao_budunit.add_fact(fcontext=ced_week, fstate=ced_week, fopen=0, fnigh=4)
    yao_budunit.settle_bud()

    # THEN
    print(f"{len(concept_dict)=}")
    print(f"{len(yao_budunit.conceptroot.factunits)=}")
    assert from_list_get_active(mat_way, yao_budunit._concept_dict)


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
    nation_way = sue_budunit.make_l1_way("nation")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_budunit.edit_concept_attr(
        oregon_way, problem_bool=True, healerlink=sue_healerlink
    )
    oregon_concept = sue_budunit.get_concept_obj(oregon_way)
    print(f"{oregon_concept._fund_ratio=}")
    assert sue_budunit._sum_healerlink_share == 0
    assert oregon_concept._healerlink_ratio == 0

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._sum_healerlink_share == 0.038461539 * default_fund_pool()
    assert oregon_concept._healerlink_ratio == 1

    # WHEN
    week_way = sue_budunit.make_l1_way("weekdays")
    sue_budunit.edit_concept_attr(week_way, problem_bool=True)
    mon_way = sue_budunit.make_way(week_way, "Monday")
    sue_budunit.edit_concept_attr(mon_way, healerlink=sue_healerlink)
    mon_concept = sue_budunit.get_concept_obj(mon_way)
    # print(f"{mon_concept.problem_bool=} {mon_concept._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._sum_healerlink_share != 0.038461539 * default_fund_pool()
    assert sue_budunit._sum_healerlink_share == 0.06923077 * default_fund_pool()
    assert oregon_concept._healerlink_ratio == 0.5555555571604938
    assert mon_concept._healerlink_ratio == 0.4444444428395062

    # WHEN
    tue_way = sue_budunit.make_way(week_way, "Tuesday")
    sue_budunit.edit_concept_attr(tue_way, healerlink=sue_healerlink)
    tue_concept = sue_budunit.get_concept_obj(tue_way)
    # print(f"{tue_concept.problem_bool=} {tue_concept._fund_ratio=}")
    # sat_way = sue_budunit.make_way(week_way, "Saturday")
    # sat_concept = sue_budunit.get_concept_obj(sat_way)
    # print(f"{sat_concept.problem_bool=} {sat_concept._fund_ratio=}")
    sue_budunit.settle_bud()

    # THEN
    assert (
        sue_budunit._sum_healerlink_share != 0.06923076923076923 * default_fund_pool()
    )
    assert sue_budunit._sum_healerlink_share == 0.100000001 * default_fund_pool()
    assert oregon_concept._healerlink_ratio == 0.38461538615384616
    assert mon_concept._healerlink_ratio == 0.3076923069230769
    assert tue_concept._healerlink_ratio == 0.3076923069230769

    # WHEN
    sue_budunit.edit_concept_attr(week_way, healerlink=sue_healerlink)
    week_concept = sue_budunit.get_concept_obj(week_way)
    print(
        f"{week_concept.concept_label=} {week_concept.problem_bool=} {week_concept._fund_ratio=}"
    )
    sue_budunit.settle_bud()
    # THEN
    display_concepttree(sue_budunit, "Keep", graphics_bool)
    assert sue_budunit._sum_healerlink_share == 0
    assert oregon_concept._healerlink_ratio == 0
    assert mon_concept._healerlink_ratio == 0
    assert tue_concept._healerlink_ratio == 0


def test_BudUnit_settle_bud_CorrectlySets_keep_dict_v1(graphics_bool):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    sue_budunit.add_acctunit("Sue")
    sue_budunit.settle_bud()
    nation_way = sue_budunit.make_l1_way("nation")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_budunit.edit_concept_attr(
        oregon_way, problem_bool=True, healerlink=sue_healerlink
    )
    assert len(sue_budunit._keep_dict) == 0
    assert sue_budunit._keep_dict.get(oregon_way) is None

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert len(sue_budunit._keep_dict) == 1
    assert sue_budunit._keep_dict.get(oregon_way) is not None

    # WHEN
    week_way = sue_budunit.make_l1_way("weekdays")
    sue_budunit.edit_concept_attr(week_way, problem_bool=True)
    mon_way = sue_budunit.make_way(week_way, "Monday")
    sue_budunit.edit_concept_attr(mon_way, healerlink=sue_healerlink)
    # mon_concept = sue_budunit.get_concept_obj(mon_way)
    # print(f"{mon_concept.problem_bool=} {mon_concept._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    assert len(sue_budunit._keep_dict) == 2
    assert sue_budunit._keep_dict.get(oregon_way) is not None
    assert sue_budunit._keep_dict.get(mon_way) is not None

    # WHEN
    tue_way = sue_budunit.make_way(week_way, "Tuesday")
    sue_budunit.edit_concept_attr(tue_way, healerlink=sue_healerlink)
    # tue_concept = sue_budunit.get_concept_obj(tue_way)
    # print(f"{tue_concept.problem_bool=} {tue_concept._fund_ratio=}")
    # sat_way = sue_budunit.make_way(week_way, "Saturday")
    # sat_concept = sue_budunit.get_concept_obj(sat_way)
    # print(f"{sat_concept.problem_bool=} {sat_concept._fund_ratio=}")
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._keep_dict) == 3
    assert sue_budunit._keep_dict.get(oregon_way) is not None
    assert sue_budunit._keep_dict.get(mon_way) is not None
    assert sue_budunit._keep_dict.get(tue_way) is not None

    # WHEN
    sue_budunit.edit_concept_attr(week_way, healerlink=sue_healerlink)
    week_concept = sue_budunit.get_concept_obj(week_way)
    print(
        f"{week_concept.concept_label=} {week_concept.problem_bool=} {week_concept._fund_ratio=}"
    )
    sue_budunit.settle_bud()
    # THEN
    display_concepttree(sue_budunit, "Keep", graphics_bool)
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
    nation_way = sue_budunit.make_l1_way("nation")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_concept_attr(
        oregon_way, problem_bool=True, healerlink=sue_healerlink
    )

    week_way = sue_budunit.make_l1_way("weekdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_budunit.edit_concept_attr(
        week_way, problem_bool=True, healerlink=bob_healerlink
    )
    assert sue_budunit._healers_dict == {}

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._healers_dict) == 2
    week_concept = sue_budunit.get_concept_obj(week_way)
    assert sue_budunit._healers_dict.get(bob_str) == {week_way: week_concept}
    oregon_concept = sue_budunit.get_concept_obj(oregon_way)
    assert sue_budunit._healers_dict.get(sue_str) == {oregon_way: oregon_concept}


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
    nation_way = sue_budunit.make_l1_way("nation")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_concept_attr(
        oregon_way, problem_bool=True, healerlink=sue_healerlink
    )

    week_way = sue_budunit.make_l1_way("weekdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_budunit.edit_concept_attr(
        week_way, problem_bool=True, healerlink=bob_healerlink
    )

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
    nation_way = sue_budunit.make_l1_way("nation")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    bend_str = "Be/nd"
    bend_way = sue_budunit.make_way(oregon_way, bend_str)
    sue_budunit.set_concept(conceptunit_shop(bend_str), oregon_way)
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_concept_attr(
        bend_way, problem_bool=True, healerlink=sue_healerlink
    )
    assert sue_budunit._keeps_buildable

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._keeps_buildable is False
