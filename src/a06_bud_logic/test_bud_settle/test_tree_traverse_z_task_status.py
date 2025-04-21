from src.a00_data_toolboxs.plotly_toolbox import conditional_fig_show
from src.a02_finance_toolboxs.finance_config import default_fund_pool
from src.a06_bud_logic.bud_graphics import display_itemtree
from src.a06_bud_logic.bud import budunit_shop
from src.a05_item_logic.healer import healerlink_shop
from src.a06_bud_logic.examples.example_buds import (
    get_budunit_with_4_levels_and_2reasons,
    get_budunit_with7amCleanTableReason,
    budunit_v001,
    from_list_get_active,
)
from src.a05_item_logic.item import itemunit_shop
from src.a04_reason_logic.reason_item import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_settle_bud_SetsStatus_active_WhenFactSaysNo():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_road = sue_budunit.make_l1_road(week_str)
    sun_str = "Sunday"
    sun_road = sue_budunit.make_road(week_road, sun_str)

    # for item in sue_budunit._item_dict.values():
    #     print(f"{casa_road=} {item.get_road()=}")
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    assert sue_budunit.get_item_obj(casa_road)._active is None

    # WHEN
    sue_budunit.add_fact(base=week_road, pick=sun_road)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._item_dict != {}
    assert len(sue_budunit._item_dict) == 17

    # for item in sue_budunit._item_dict.values():
    #     print(f"{casa_road=} {item.get_road()=}")
    assert sue_budunit.get_item_obj(casa_road)._active is False


def test_BudUnit_settle_bud_SetsStatus_active_WhenFactModifies():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_road = sue_budunit.make_l1_road(week_str)
    sun_str = "Wednesday"
    sun_road = sue_budunit.make_road(week_road, sun_str)
    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)

    # WHEN
    sue_budunit.add_fact(base=week_road, pick=sun_road)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict
    assert len(sue_budunit._item_dict) == 17
    assert sue_budunit._item_dict.get(casa_road)._active is False

    # WHEN
    states_str = "nation-state"
    states_road = sue_budunit.make_l1_road(states_str)
    usa_str = "USA"
    usa_road = sue_budunit.make_road(states_road, usa_str)
    sue_budunit.add_fact(base=states_road, pick=usa_road)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict
    assert len(sue_budunit._item_dict) == 17
    assert sue_budunit._item_dict.get(casa_road)._active

    # WHEN
    france_str = "France"
    france_road = sue_budunit.make_road(states_road, france_str)
    sue_budunit.add_fact(base=states_road, pick=france_road)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict
    assert len(sue_budunit._item_dict) == 17
    assert sue_budunit._item_dict.get(casa_road)._active is False


def test_BudUnit_settle_bud_CorrectlySets_item_dict():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_road = sue_budunit.make_l1_road(week_str)
    wed_str = "Wednesday"
    wed_road = sue_budunit.make_road(week_road, wed_str)
    state_str = "nation-state"
    state_road = sue_budunit.make_l1_road(state_str)
    france_str = "France"
    france_road = sue_budunit.make_road(state_road, france_str)
    sue_budunit.add_fact(base=week_road, pick=wed_road)
    sue_budunit.add_fact(base=state_road, pick=france_road)

    casa_str = "casa"
    casa_road = sue_budunit.make_l1_road(casa_str)
    casa_item = sue_budunit.get_item_obj(casa_road)
    print(f"{sue_budunit.owner_name=} {len(casa_item.reasonunits)=}")
    # print(f"{casa_item.reasonunits=}")
    print(f"{sue_budunit.owner_name=} {len(sue_budunit.itemroot.factunits)=}")
    # print(f"{sue_budunit.itemroot.factunits=}")

    sue_budunit.settle_bud()
    assert sue_budunit._item_dict
    assert len(sue_budunit._item_dict) == 17

    usa_str = "USA"
    usa_road = sue_budunit.make_road(state_road, usa_str)
    oregon_str = "Oregon"
    oregon_road = sue_budunit.make_road(usa_road, oregon_str)

    wed = premiseunit_shop(need=wed_road)
    wed._status = True
    wed._task = False
    usa = premiseunit_shop(need=usa_road)
    usa._status = True
    usa._task = False

    wed_lu = reasonunit_shop(week_road, premises={wed.need: wed})
    sta_lu = reasonunit_shop(state_road, premises={usa.need: usa})
    wed_lh = reasonheir_shop(
        base=week_road,
        premises={wed.need: wed},
        _status=True,
        _task=False,
        _base_item_active_value=True,
    )
    sta_lh = reasonheir_shop(
        base=state_road,
        premises={usa.need: usa},
        _status=True,
        _task=False,
        _base_item_active_value=True,
    )

    x1_reasonunits = {
        wed_lu.base: wed_lu,
        sta_lu.base: sta_lu,
    }
    x1_reasonheirs = {
        wed_lh.base: wed_lh,
        sta_lh.base: sta_lh,
    }

    # WHEN
    sue_budunit.add_fact(base=state_road, pick=oregon_road)
    sue_budunit.settle_bud()

    # THEN
    casa_item = sue_budunit._item_dict.get(casa_road)
    print(f"\nlook at {casa_item.get_road()=}")
    assert casa_item.parent_road == sue_budunit.fisc_tag
    assert casa_item._kids == {}
    assert casa_item.mass == 30
    assert casa_item.item_tag == casa_str
    assert casa_item._level == 1
    assert casa_item._active
    assert casa_item.pledge
    # print(f"{casa_item._reasonheirs=}")
    x_reasonheir_state = casa_item._reasonheirs[state_road]
    print(f"  {x_reasonheir_state=}")
    print(f"  {x_reasonheir_state._status=}\n")
    # assert casa_item._reasonheirs == x1_reasonheirs

    assert len(casa_item._reasonheirs) == len(x1_reasonheirs)
    week_reasonheir = casa_item._reasonheirs.get(week_road)
    # usa_premise = week_reasonheir.premises.get(usa_road)
    print(f"    {casa_item.item_tag=}")
    # print(f"    {usa_premise.base=}")
    # print(f"    {usa_premise._task=}")
    # print(f"    {usa_premise._task=}")
    assert week_reasonheir._task is False
    # print(f"      premises: {w=}")
    # w_need = usa_premise.premises[wed_road].need
    # print(f"      {w_need=}")
    # assert usa_premise._task == w_need._task
    # assert usa_premise._status == w_need._status
    # assert week_reasonheir.premises == week_reasonheir.premises

    # assert casa_item.reasonunits == x1_reasonunits

    # print("iterate through every item...")
    # for x_item in item_dict:
    #     if str(type(x_item)).find(".item.ItemUnit'>") > 0:
    #         assert x_item._active is not None

    #     # print("")
    #     # print(f"{x_item.item_tag=}")
    #     # print(f"{len(x_item.reasonunits)=}")
    #     print(
    #         f"  {x_item.item_tag} iterate through every reasonheir... {len(x_item._reasonheirs)=} {x_item.item_tag=}"
    #     )
    #     # print(f"{x_item._reasonheirs=}")
    #     for reason in x_item._reasonheirs.values():
    #         assert str(type(reason)).find(".reason.ReasonHeir'>") > 0
    #         print(f"    {reason.base=}")
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
    house_road = sue_budunit.make_l1_road(house_str)
    clean_str = "clean table"
    clean_road = sue_budunit.make_road(house_road, clean_str)
    assert sue_budunit._item_dict.get(clean_road)._active is False

    # set facts as midnight to 8am
    time_str = "timetech"
    time_road = sue_budunit.make_l1_road(time_str)
    day24hr_str = "24hr day"
    day24hr_road = sue_budunit.make_road(time_road, day24hr_str)
    day24hr_base = day24hr_road
    day24hr_pick = day24hr_road
    day24hr_open = 0.0
    day24hr_nigh = 8.0

    # WHEN
    sue_budunit.add_fact(
        base=day24hr_base, pick=day24hr_pick, fopen=day24hr_open, fnigh=day24hr_nigh
    )

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict.get(clean_road)._active

    # WHEN
    # set facts as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(sue_budunit.itemroot.factunits[day24hr_road])
    sue_budunit.add_fact(
        base=day24hr_base, pick=day24hr_pick, fopen=day24hr_open, fnigh=day24hr_nigh
    )
    print(sue_budunit.itemroot.factunits[day24hr_road])
    print(sue_budunit.itemroot._kids[house_str]._kids[clean_str].reasonunits)
    # sue_budunit.itemroot._kids["housemanagement"]._kids[clean_str]._active = None

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict.get(clean_road)._active is False


def test_BudUnit_get_agenda_dict_ReturnsObj():
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()

    # WHEN
    pledge_items = sue_budunit.get_agenda_dict()

    # THEN
    assert pledge_items is not None
    assert len(pledge_items) > 0
    assert len(pledge_items) == 1


def test_BudUnit_settle_bud_CorrectlySetsData_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    print(f"{yao_budunit.get_reason_bases()=}")
    # day_hour = f"{yao_budunit.fisc_tag},day_hour"
    # yao_budunit.add_fact(base=day_hour, pick=day_hour, open=0, nigh=23)
    day_min_str = "day_minute"
    day_min_road = yao_budunit.make_l1_road(day_min_str)
    yao_budunit.add_fact(base=day_min_road, pick=day_min_road, fopen=0, fnigh=1439)

    mood_str = "Moods"
    mood_road = yao_budunit.make_l1_road(mood_str)
    yao_budunit.add_fact(base=mood_road, pick=mood_road)
    print(f"{yao_budunit.get_reason_bases()=}")

    yr_mon_str = "year_month"
    yr_mon_road = yao_budunit.make_l1_road(yr_mon_str)
    yao_budunit.add_fact(base=yr_mon_road, pick=yr_mon_road)
    inter_str = "Interweb"
    inter_road = yao_budunit.make_l1_road(inter_str)
    yao_budunit.add_fact(base=inter_road, pick=inter_road)
    assert yao_budunit is not None
    # print(f"{yao_budunit.owner_name=}")
    # print(f"{len(yao_budunit.itemroot._kids)=}")
    ulty_str = "Ultimate Frisbee"
    ulty_road = yao_budunit.make_l1_road(ulty_str)

    # if yao_budunit.itemroot._kids["Ultimate Frisbee"].item_tag == "Ultimate Frisbee":
    assert yao_budunit.itemroot._kids[ulty_str].reasonunits is not None
    assert yao_budunit.owner_name is not None

    # for fact in yao_budunit.itemroot.factunits.values():
    #     print(f"{fact=}")

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    # print(f"{str(type(item))=}")
    # print(f"{len(item_dict)=}")
    laundry_str = "laundry monday"
    casa_road = yao_budunit.make_l1_road("casa")
    cleaning_road = yao_budunit.make_road(casa_road, "cleaning")
    laundry_road = yao_budunit.make_road(cleaning_road, laundry_str)

    # for item in item_dict:
    #     assert (
    #         str(type(item)).find(".item.ItemUnit'>") > 0
    #         or str(type(item)).find(".item.ItemUnit'>") > 0
    #     )
    #     # print(f"{item.item_tag=}")
    #     if item.item_tag == laundry_str:
    #         for reason in item.reasonunits.values():
    #             print(f"{item.item_tag=} {reason.base=}")  # {reason.premises=}")
    # assert item._active is False
    assert yao_budunit._item_dict.get(laundry_road)._active is False

    # WHEN
    week_str = "weekdays"
    week_road = yao_budunit.make_l1_road(week_str)
    mon_str = "Monday"
    mon_road = yao_budunit.make_road(week_road, mon_str)
    yao_budunit.add_fact(base=week_road, pick=mon_road)
    yao_budunit.settle_bud()

    # THEN
    assert yao_budunit._item_dict.get(laundry_road)._active is False


def test_BudUnit_settle_bud_OptionWeekdaysReturnsObj_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()

    day_hr_str = "day_hour"
    day_hr_road = yao_budunit.make_l1_road(day_hr_str)
    yao_budunit.add_fact(base=day_hr_road, pick=day_hr_road, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_road = yao_budunit.make_l1_road(day_min_str)
    yao_budunit.add_fact(base=day_min_road, pick=day_min_road, fopen=0, fnigh=59)
    mon_wk_str = "month_week"
    mon_wk_road = yao_budunit.make_l1_road(mon_wk_str)
    yao_budunit.add_fact(base=mon_wk_road, pick=mon_wk_road)
    nation_str = "Nation-States"
    nation_road = yao_budunit.make_l1_road(nation_str)
    yao_budunit.add_fact(base=nation_road, pick=nation_road)
    mood_str = "Moods"
    mood_road = yao_budunit.make_l1_road(mood_str)
    yao_budunit.add_fact(base=mood_road, pick=mood_road)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_road = yao_budunit.make_l1_road(aaron_str)
    yao_budunit.add_fact(base=aaron_road, pick=aaron_road)
    inter_str = "Interweb"
    inter_road = yao_budunit.make_l1_road(inter_str)
    yao_budunit.add_fact(base=inter_road, pick=inter_road)
    yr_mon_str = "year_month"
    yr_mon_road = yao_budunit.make_l1_road(yr_mon_str)
    yao_budunit.add_fact(base=yr_mon_road, pick=yr_mon_road, fopen=0, fnigh=1000)

    yao_budunit.settle_bud()
    missing_facts = yao_budunit.get_missing_fact_bases()
    # for missing_fact, count in missing_facts.items():
    #     print(f"{missing_fact=} {count=}")

    week_str = "weekdays"
    week_road = yao_budunit.make_l1_road(week_str)
    mon_str = "Monday"
    mon_road = yao_budunit.make_road(week_road, mon_str)
    tue_str = "Tuesday"
    tue_road = yao_budunit.make_road(week_road, tue_str)
    mon_premise_x = premiseunit_shop(need=mon_road)
    mon_premise_x._status = False
    mon_premise_x._task = False
    tue_premise_x = premiseunit_shop(need=tue_road)
    tue_premise_x._status = False
    tue_premise_x._task = False
    mt_premises = {
        mon_premise_x.need: mon_premise_x,
        tue_premise_x.need: tue_premise_x,
    }
    mt_reasonunit = reasonunit_shop(week_road, premises=mt_premises)
    mt_reasonheir = reasonheir_shop(week_road, premises=mt_premises, _status=False)
    x_itemroot = yao_budunit.get_item_obj(yao_budunit.fisc_tag)
    x_itemroot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_budunit.reasonunits[week_road].base=}")
    # print(f"{yao_budunit.reasonunits[week_road].premises[mon_road].need=}")
    # print(f"{yao_budunit.reasonunits[week_road].premises[tue_road].need=}")
    week_reasonunit = x_itemroot.reasonunits[week_road]
    print(f"{week_reasonunit.premises=}")
    premise_mon = week_reasonunit.premises.get(mon_road)
    premise_tue = week_reasonunit.premises.get(tue_road)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.need]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.need]
    assert week_reasonunit == mt_reasonunit

    # WHEN
    item_dict = yao_budunit.get_item_dict()

    # THEN
    gen_week_reasonheir = x_itemroot.get_reasonheir(week_road)
    gen_mon_premise = gen_week_reasonheir.premises.get(mon_road)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_road)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_road)
    assert gen_week_reasonheir.premises == mt_reasonheir.premises
    assert gen_week_reasonheir == mt_reasonheir

    casa_str = "casa"
    casa_road = yao_budunit.make_l1_road(casa_str)
    bird_str = "say hi to birds"
    bird_road = yao_budunit.make_road(casa_road, bird_str)
    assert from_list_get_active(bird_road, item_dict) is False

    # yao_budunit.add_fact(base=week_road, pick=mon_road)
    # item_dict = yao_budunit.get_item_dict()
    # casa_item = x_itemroot._kids[casa_str]
    # twee_item = casa_item._kids[bird_str]
    # print(f"{len(x_itemroot._reasonheirs)=}")
    # print(f"{len(casa_item._reasonheirs)=}")
    # print(f"{len(twee_item._reasonheirs)=}")

    # assert YR.get_active(road=bird_item, item_dict=item_dict) is True

    # yao_budunit.add_fact(base=f"{yao_budunit.fisc_tag},weekdays", pick=f"{yao_budunit.fisc_tag},weekdays,Tuesday")
    # item_dict = yao_budunit.get_item_dict()
    # assert YR.get_active(road=bird_item, item_dict=item_dict) is True

    # yao_budunit.add_fact(base=f"{yao_budunit.fisc_tag},weekdays", pick=f"{yao_budunit.fisc_tag},weekdays,Wednesday")
    # item_dict = yao_budunit.get_item_dict()
    # assert YR.get_active(road=bird_item, item_dict=item_dict) is False


def test_BudUnit_settle_bud_CorrectlySetsItemUnitsActiveWithEvery6WeeksReason_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    day_str = "day_hour"
    day_road = yao_budunit.make_l1_road(day_str)
    min_str = "day_minute"
    min_road = yao_budunit.make_l1_road(day_str)

    # WHEN
    yao_budunit.add_fact(base=day_road, pick=day_road, fopen=0, fnigh=23)
    yao_budunit.add_fact(base=min_road, pick=min_road, fopen=0, fnigh=59)
    yao_budunit.settle_bud()

    # THEN
    ced_week_base = yao_budunit.make_l1_road("ced_week")

    premise_divisor = None
    premise_open = None
    premise_nigh = None
    print(f"{len(yao_budunit._item_dict)=}")

    casa_road = yao_budunit.make_l1_road("casa")
    cleaning_road = yao_budunit.make_road(casa_road, "cleaning")
    clean_couch_road = yao_budunit.make_road(
        cleaning_road, "clean sheets couch blankets"
    )
    clean_sheet_item = yao_budunit.get_item_obj(clean_couch_road)
    # print(f"{clean_sheet_item.reasonunits.values()=}")
    ced_week_reason = clean_sheet_item.reasonunits.get(ced_week_base)
    ced_week_premise = ced_week_reason.premises.get(ced_week_base)
    print(
        f"{clean_sheet_item.item_tag=} {ced_week_reason.base=} {ced_week_premise.need=}"
    )
    # print(f"{clean_sheet_item.item_tag=} {ced_week_reason.base=} {premise_x=}")
    premise_divisor = ced_week_premise.divisor
    premise_open = ced_week_premise.open
    premise_nigh = ced_week_premise.nigh
    # print(f"{item.reasonunits=}")
    assert clean_sheet_item._active is False

    # for item in item_dict:
    #     # print(f"{item.parent_road=}")
    #     if item.item_tag == "clean sheets couch blankets":
    #         print(f"{item.get_road()=}")

    assert premise_divisor == 6
    assert premise_open == 1
    print(
        f"There exists a item with a reason_base {ced_week_base} that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(item_dict)=}")
    ced_week_open = 6001

    # WHEN
    yao_budunit.add_fact(
        base=ced_week_base, pick=ced_week_base, fopen=ced_week_open, fnigh=ced_week_open
    )
    nation_str = "Nation-States"
    nation_road = yao_budunit.make_l1_road(nation_str)
    yao_budunit.add_fact(base=nation_road, pick=nation_road)
    print(
        f"Nation-states set and also fact set: {ced_week_base=} with {ced_week_open=} and {ced_week_open=}"
    )
    print(f"{yao_budunit.itemroot.factunits=}")
    yao_budunit.settle_bud()

    # THEN
    week_str = "ced_week"
    week_road = yao_budunit.make_l1_road(week_str)
    casa_road = yao_budunit.make_l1_road("casa")
    cleaning_road = yao_budunit.make_road(casa_road, "cleaning")
    clean_couch_str = "clean sheets couch blankets"
    clean_couch_road = yao_budunit.make_road(cleaning_road, clean_couch_str)
    clean_couch_item = yao_budunit.get_item_obj(road=clean_couch_road)
    week_reason = clean_couch_item.reasonunits.get(week_road)
    week_premise = week_reason.premises.get(week_road)
    print(f"{clean_couch_item.item_tag=} {week_reason.base=} {week_premise=}")
    assert week_premise.divisor == 6 and week_premise.open == 1


def test_BudUnit_settle_bud_EveryItemHasActiveStatus_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()

    # WHEN
    yao_budunit.settle_bud()

    # THEN
    print(f"{len(yao_budunit._item_dict)=}")
    # first_item_kid_count = 0
    # first_item_kid_none_count = 0
    # first_item_kid_true_count = 0
    # first_item_kid_false_count = 0
    # for item in item_list:
    #     if str(type(item)).find(".item.ItemUnit'>") > 0:
    #         first_item_kid_count += 1
    #         if item._active is None:
    #             first_item_kid_none_count += 1
    #         elif item._active:
    #             first_item_kid_true_count += 1
    #         elif item._active is False:
    #             first_item_kid_false_count += 1

    # print(f"{first_item_kid_count=}")
    # print(f"{first_item_kid_none_count=}")
    # print(f"{first_item_kid_true_count=}")
    # print(f"{first_item_kid_false_count=}")

    # item_kid_count = 0
    # for item in item_list_without_itemroot:
    #     item_kid_count += 1
    #     print(f"{item.item_tag=} {item_kid_count=}")
    #     assert item._active is not None
    #     assert item._active in (True, False)
    # assert item_kid_count == len(item_list_without_itemroot)

    assert len(yao_budunit._item_dict) == sum(
        item._active is not None for item in yao_budunit._item_dict.values()
    )


def test_BudUnit_settle_bud_EveryTwoMonthReturnsObj_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    minute_str = "day_minute"
    minute_road = yao_budunit.make_l1_road(minute_str)
    yao_budunit.add_fact(base=minute_road, pick=minute_road, fopen=0, fnigh=1399)
    month_str = "month_week"
    month_road = yao_budunit.make_l1_road(month_str)
    yao_budunit.add_fact(base=month_road, pick=month_road)
    nations_str = "Nation-States"
    nations_road = yao_budunit.make_l1_road(nations_str)
    yao_budunit.add_fact(base=nations_road, pick=nations_road)
    mood_str = "Moods"
    mood_road = yao_budunit.make_l1_road(mood_str)
    yao_budunit.add_fact(base=mood_road, pick=mood_road)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_road = yao_budunit.make_l1_road(aaron_str)
    yao_budunit.add_fact(base=aaron_road, pick=aaron_road)
    interweb_str = "Interweb"
    interweb_road = yao_budunit.make_l1_road(interweb_str)
    yao_budunit.add_fact(base=interweb_road, pick=interweb_road)
    weekdays_str = "weekdays"
    weekdays_road = yao_budunit.make_l1_road(weekdays_str)
    yao_budunit.add_fact(base=weekdays_road, pick=weekdays_road)
    item_dict = yao_budunit.get_item_dict()
    print(f"{len(item_dict)=}")

    casa_str = "casa"
    casa_road = yao_budunit.make_l1_road(casa_str)
    clean_str = "cleaning"
    clean_road = yao_budunit.make_road(casa_road, clean_str)
    mat_item_tag = "deep clean play mat"
    mat_road = yao_budunit.make_road(clean_road, mat_item_tag)
    assert from_list_get_active(mat_road, item_dict) is False

    year_month_base = yao_budunit.make_l1_road("year_month")
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    yao_budunit.add_fact(base=year_month_base, pick=year_month_base, fopen=0, fnigh=8)
    ced_week = yao_budunit.make_l1_road("ced_week")
    yao_budunit.add_fact(base=ced_week, pick=ced_week, fopen=0, fnigh=4)
    yao_budunit.settle_bud()

    # THEN
    print(f"{len(item_dict)=}")
    print(f"{len(yao_budunit.itemroot.factunits)=}")
    assert from_list_get_active(mat_road, yao_budunit._item_dict)


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
    nation_road = sue_budunit.make_l1_road("nation-state")
    usa_road = sue_budunit.make_road(nation_road, "USA")
    oregon_road = sue_budunit.make_road(usa_road, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_budunit.edit_item_attr(
        oregon_road, problem_bool=True, healerlink=sue_healerlink
    )
    oregon_item = sue_budunit.get_item_obj(oregon_road)
    print(f"{oregon_item._fund_ratio=}")
    assert sue_budunit._sum_healerlink_share == 0
    assert oregon_item._healerlink_ratio == 0

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._sum_healerlink_share == 0.038461539 * default_fund_pool()
    assert oregon_item._healerlink_ratio == 1

    # WHEN
    week_road = sue_budunit.make_l1_road("weekdays")
    sue_budunit.edit_item_attr(week_road, problem_bool=True)
    mon_road = sue_budunit.make_road(week_road, "Monday")
    sue_budunit.edit_item_attr(mon_road, healerlink=sue_healerlink)
    mon_item = sue_budunit.get_item_obj(mon_road)
    # print(f"{mon_item.problem_bool=} {mon_item._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._sum_healerlink_share != 0.038461539 * default_fund_pool()
    assert sue_budunit._sum_healerlink_share == 0.06923077 * default_fund_pool()
    assert oregon_item._healerlink_ratio == 0.5555555571604938
    assert mon_item._healerlink_ratio == 0.4444444428395062

    # WHEN
    tue_road = sue_budunit.make_road(week_road, "Tuesday")
    sue_budunit.edit_item_attr(tue_road, healerlink=sue_healerlink)
    tue_item = sue_budunit.get_item_obj(tue_road)
    # print(f"{tue_item.problem_bool=} {tue_item._fund_ratio=}")
    # sat_road = sue_budunit.make_road(week_road, "Saturday")
    # sat_item = sue_budunit.get_item_obj(sat_road)
    # print(f"{sat_item.problem_bool=} {sat_item._fund_ratio=}")
    sue_budunit.settle_bud()

    # THEN
    assert (
        sue_budunit._sum_healerlink_share != 0.06923076923076923 * default_fund_pool()
    )
    assert sue_budunit._sum_healerlink_share == 0.100000001 * default_fund_pool()
    assert oregon_item._healerlink_ratio == 0.38461538615384616
    assert mon_item._healerlink_ratio == 0.3076923069230769
    assert tue_item._healerlink_ratio == 0.3076923069230769

    # WHEN
    sue_budunit.edit_item_attr(week_road, healerlink=sue_healerlink)
    week_item = sue_budunit.get_item_obj(week_road)
    print(f"{week_item.item_tag=} {week_item.problem_bool=} {week_item._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    display_itemtree(sue_budunit, "Keep", graphics_bool)
    assert sue_budunit._sum_healerlink_share == 0
    assert oregon_item._healerlink_ratio == 0
    assert mon_item._healerlink_ratio == 0
    assert tue_item._healerlink_ratio == 0


def test_BudUnit_settle_bud_CorrectlySets_keep_dict_v1(graphics_bool):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels_and_2reasons()
    sue_budunit.add_acctunit("Sue")
    sue_budunit.settle_bud()
    nation_road = sue_budunit.make_l1_road("nation-state")
    usa_road = sue_budunit.make_road(nation_road, "USA")
    oregon_road = sue_budunit.make_road(usa_road, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_budunit.edit_item_attr(
        oregon_road, problem_bool=True, healerlink=sue_healerlink
    )
    assert len(sue_budunit._keep_dict) == 0
    assert sue_budunit._keep_dict.get(oregon_road) is None

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert len(sue_budunit._keep_dict) == 1
    assert sue_budunit._keep_dict.get(oregon_road) is not None

    # WHEN
    week_road = sue_budunit.make_l1_road("weekdays")
    sue_budunit.edit_item_attr(week_road, problem_bool=True)
    mon_road = sue_budunit.make_road(week_road, "Monday")
    sue_budunit.edit_item_attr(mon_road, healerlink=sue_healerlink)
    # mon_item = sue_budunit.get_item_obj(mon_road)
    # print(f"{mon_item.problem_bool=} {mon_item._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    assert len(sue_budunit._keep_dict) == 2
    assert sue_budunit._keep_dict.get(oregon_road) is not None
    assert sue_budunit._keep_dict.get(mon_road) is not None

    # WHEN
    tue_road = sue_budunit.make_road(week_road, "Tuesday")
    sue_budunit.edit_item_attr(tue_road, healerlink=sue_healerlink)
    # tue_item = sue_budunit.get_item_obj(tue_road)
    # print(f"{tue_item.problem_bool=} {tue_item._fund_ratio=}")
    # sat_road = sue_budunit.make_road(week_road, "Saturday")
    # sat_item = sue_budunit.get_item_obj(sat_road)
    # print(f"{sat_item.problem_bool=} {sat_item._fund_ratio=}")
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._keep_dict) == 3
    assert sue_budunit._keep_dict.get(oregon_road) is not None
    assert sue_budunit._keep_dict.get(mon_road) is not None
    assert sue_budunit._keep_dict.get(tue_road) is not None

    # WHEN
    sue_budunit.edit_item_attr(week_road, healerlink=sue_healerlink)
    week_item = sue_budunit.get_item_obj(week_road)
    print(f"{week_item.item_tag=} {week_item.problem_bool=} {week_item._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    display_itemtree(sue_budunit, "Keep", graphics_bool)
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
    nation_road = sue_budunit.make_l1_road("nation-state")
    usa_road = sue_budunit.make_road(nation_road, "USA")
    oregon_road = sue_budunit.make_road(usa_road, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_item_attr(
        oregon_road, problem_bool=True, healerlink=sue_healerlink
    )

    week_road = sue_budunit.make_l1_road("weekdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_budunit.edit_item_attr(week_road, problem_bool=True, healerlink=bob_healerlink)
    assert sue_budunit._healers_dict == {}

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._healers_dict) == 2
    week_item = sue_budunit.get_item_obj(week_road)
    assert sue_budunit._healers_dict.get(bob_str) == {week_road: week_item}
    oregon_item = sue_budunit.get_item_obj(oregon_road)
    assert sue_budunit._healers_dict.get(sue_str) == {oregon_road: oregon_item}


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
    nation_road = sue_budunit.make_l1_road("nation-state")
    usa_road = sue_budunit.make_road(nation_road, "USA")
    oregon_road = sue_budunit.make_road(usa_road, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_item_attr(
        oregon_road, problem_bool=True, healerlink=sue_healerlink
    )

    week_road = sue_budunit.make_l1_road("weekdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_budunit.edit_item_attr(week_road, problem_bool=True, healerlink=bob_healerlink)

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
    nation_road = sue_budunit.make_l1_road("nation-state")
    usa_road = sue_budunit.make_road(nation_road, "USA")
    oregon_road = sue_budunit.make_road(usa_road, "Oregon")
    bend_str = "Be/nd"
    bend_road = sue_budunit.make_road(oregon_road, bend_str)
    sue_budunit.set_item(itemunit_shop(bend_str), oregon_road)
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_item_attr(bend_road, problem_bool=True, healerlink=sue_healerlink)
    assert sue_budunit._keeps_buildable

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._keeps_buildable is False
