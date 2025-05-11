from src.a01_way_logic.way import to_way
from src.a02_finance_logic.finance_config import default_fund_pool
from src.a04_reason_logic.reason_item import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.a05_item_logic.item import itemunit_shop
from src.a05_item_logic.healer import healerlink_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic.bud_graphics import display_itemtree
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

    # for item in sue_budunit._item_dict.values():
    #     print(f"{casa_way=} {item.get_item_way()=}")
    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    assert sue_budunit.get_item_obj(casa_way)._active is None

    # WHEN
    sue_budunit.add_fact(fbase=week_way, fneed=sun_way)
    sue_budunit.settle_bud()

    # THEN
    assert sue_budunit._item_dict != {}
    assert len(sue_budunit._item_dict) == 17

    # for item in sue_budunit._item_dict.values():
    #     print(f"{casa_way=} {item.get_item_way()=}")
    assert sue_budunit.get_item_obj(casa_way)._active is False


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
    sue_budunit.add_fact(fbase=week_way, fneed=sun_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict
    assert len(sue_budunit._item_dict) == 17
    assert sue_budunit._item_dict.get(casa_way)._active is False

    # WHEN
    states_str = "nation-state"
    states_way = sue_budunit.make_l1_way(states_str)
    usa_str = "USA"
    usa_way = sue_budunit.make_way(states_way, usa_str)
    sue_budunit.add_fact(fbase=states_way, fneed=usa_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict
    assert len(sue_budunit._item_dict) == 17
    assert sue_budunit._item_dict.get(casa_way)._active

    # WHEN
    france_str = "France"
    france_way = sue_budunit.make_way(states_way, france_str)
    sue_budunit.add_fact(fbase=states_way, fneed=france_way)

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict
    assert len(sue_budunit._item_dict) == 17
    assert sue_budunit._item_dict.get(casa_way)._active is False


def test_BudUnit_settle_bud_CorrectlySets_item_dict():
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
    sue_budunit.add_fact(fbase=week_way, fneed=wed_way)
    sue_budunit.add_fact(fbase=state_way, fneed=france_way)

    casa_str = "casa"
    casa_way = sue_budunit.make_l1_way(casa_str)
    casa_item = sue_budunit.get_item_obj(casa_way)
    print(f"{sue_budunit.owner_name=} {len(casa_item.reasonunits)=}")
    # print(f"{casa_item.reasonunits=}")
    print(f"{sue_budunit.owner_name=} {len(sue_budunit.itemroot.factunits)=}")
    # print(f"{sue_budunit.itemroot.factunits=}")

    sue_budunit.settle_bud()
    assert sue_budunit._item_dict
    assert len(sue_budunit._item_dict) == 17

    usa_str = "USA"
    usa_way = sue_budunit.make_way(state_way, usa_str)
    oregon_str = "Oregon"
    oregon_way = sue_budunit.make_way(usa_way, oregon_str)

    wed = premiseunit_shop(need=wed_way)
    wed._status = True
    wed._task = False
    usa = premiseunit_shop(need=usa_way)
    usa._status = True
    usa._task = False

    wed_lu = reasonunit_shop(week_way, premises={wed.need: wed})
    sta_lu = reasonunit_shop(state_way, premises={usa.need: usa})
    wed_lh = reasonheir_shop(
        base=week_way,
        premises={wed.need: wed},
        _status=True,
        _task=False,
        _base_item_active_value=True,
    )
    sta_lh = reasonheir_shop(
        base=state_way,
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
    sue_budunit.add_fact(fbase=state_way, fneed=oregon_way)
    sue_budunit.settle_bud()

    # THEN
    casa_item = sue_budunit._item_dict.get(casa_way)
    print(f"\nlook at {casa_item.get_item_way()=}")
    assert casa_item.parent_way == to_way(sue_budunit.fisc_tag)
    assert casa_item._kids == {}
    assert casa_item.mass == 30
    assert casa_item.item_tag == casa_str
    assert casa_item._level == 1
    assert casa_item._active
    assert casa_item.pledge
    # print(f"{casa_item._reasonheirs=}")
    x_reasonheir_state = casa_item._reasonheirs[state_way]
    print(f"  {x_reasonheir_state=}")
    print(f"  {x_reasonheir_state._status=}\n")
    # assert casa_item._reasonheirs == x1_reasonheirs

    assert len(casa_item._reasonheirs) == len(x1_reasonheirs)
    week_reasonheir = casa_item._reasonheirs.get(week_way)
    # usa_premise = week_reasonheir.premises.get(usa_way)
    print(f"    {casa_item.item_tag=}")
    # print(f"    {usa_premise.base=}")
    # print(f"    {usa_premise._task=}")
    # print(f"    {usa_premise._task=}")
    assert week_reasonheir._task is False
    # print(f"      premises: {w=}")
    # w_need = usa_premise.premises[wed_way].need
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
    house_way = sue_budunit.make_l1_way(house_str)
    clean_str = "clean table"
    clean_way = sue_budunit.make_way(house_way, clean_str)
    assert sue_budunit._item_dict.get(clean_way)._active is False

    # set facts as midnight to 8am
    time_str = "timetech"
    time_way = sue_budunit.make_l1_way(time_str)
    day24hr_str = "24hr day"
    day24hr_way = sue_budunit.make_way(time_way, day24hr_str)
    day24hr_base = day24hr_way
    day24hr_fneed = day24hr_way
    day24hr_open = 0.0
    day24hr_nigh = 8.0

    # WHEN
    sue_budunit.add_fact(
        fbase=day24hr_base, fneed=day24hr_fneed, fopen=day24hr_open, fnigh=day24hr_nigh
    )

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict.get(clean_way)._active

    # WHEN
    # set facts as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(sue_budunit.itemroot.factunits[day24hr_way])
    sue_budunit.add_fact(
        fbase=day24hr_base, fneed=day24hr_fneed, fopen=day24hr_open, fnigh=day24hr_nigh
    )
    print(sue_budunit.itemroot.factunits[day24hr_way])
    print(sue_budunit.itemroot._kids[house_str]._kids[clean_str].reasonunits)
    # sue_budunit.itemroot._kids["housemanagement"]._kids[clean_str]._active = None

    # THEN
    sue_budunit.settle_bud()
    assert sue_budunit._item_dict.get(clean_way)._active is False


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
    # yao_budunit.add_fact(fbase=day_hour, fneed=day_hour, open=0, nigh=23)
    day_min_str = "day_minute"
    day_min_way = yao_budunit.make_l1_way(day_min_str)
    yao_budunit.add_fact(fbase=day_min_way, fneed=day_min_way, fopen=0, fnigh=1439)

    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fbase=mood_way, fneed=mood_way)
    print(f"{yao_budunit.get_reason_bases()=}")

    yr_mon_str = "year_month"
    yr_mon_way = yao_budunit.make_l1_way(yr_mon_str)
    yao_budunit.add_fact(fbase=yr_mon_way, fneed=yr_mon_way)
    inter_str = "Interweb"
    inter_way = yao_budunit.make_l1_way(inter_str)
    yao_budunit.add_fact(fbase=inter_way, fneed=inter_way)
    assert yao_budunit is not None
    # print(f"{yao_budunit.owner_name=}")
    # print(f"{len(yao_budunit.itemroot._kids)=}")
    ulty_str = "Ultimate Frisbee"
    ulty_way = yao_budunit.make_l1_way(ulty_str)

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
    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    laundry_way = yao_budunit.make_way(cleaning_way, laundry_str)

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
    assert yao_budunit._item_dict.get(laundry_way)._active is False

    # WHEN
    week_str = "weekdays"
    week_way = yao_budunit.make_l1_way(week_str)
    mon_str = "Monday"
    mon_way = yao_budunit.make_way(week_way, mon_str)
    yao_budunit.add_fact(fbase=week_way, fneed=mon_way)
    yao_budunit.settle_bud()

    # THEN
    assert yao_budunit._item_dict.get(laundry_way)._active is False


def test_BudUnit_settle_bud_OptionWeekdaysReturnsObj_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()

    day_hr_str = "day_hour"
    day_hr_way = yao_budunit.make_l1_way(day_hr_str)
    yao_budunit.add_fact(fbase=day_hr_way, fneed=day_hr_way, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_way = yao_budunit.make_l1_way(day_min_str)
    yao_budunit.add_fact(fbase=day_min_way, fneed=day_min_way, fopen=0, fnigh=59)
    mon_wk_str = "month_week"
    mon_wk_way = yao_budunit.make_l1_way(mon_wk_str)
    yao_budunit.add_fact(fbase=mon_wk_way, fneed=mon_wk_way)
    nation_str = "Nation-States"
    nation_way = yao_budunit.make_l1_way(nation_str)
    yao_budunit.add_fact(fbase=nation_way, fneed=nation_way)
    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fbase=mood_way, fneed=mood_way)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_way = yao_budunit.make_l1_way(aaron_str)
    yao_budunit.add_fact(fbase=aaron_way, fneed=aaron_way)
    inter_str = "Interweb"
    inter_way = yao_budunit.make_l1_way(inter_str)
    yao_budunit.add_fact(fbase=inter_way, fneed=inter_way)
    yr_mon_str = "year_month"
    yr_mon_way = yao_budunit.make_l1_way(yr_mon_str)
    yao_budunit.add_fact(fbase=yr_mon_way, fneed=yr_mon_way, fopen=0, fnigh=1000)

    yao_budunit.settle_bud()
    missing_facts = yao_budunit.get_missing_fact_bases()
    # for missing_fact, count in missing_facts.items():
    #     print(f"{missing_fact=} {count=}")

    week_str = "weekdays"
    week_way = yao_budunit.make_l1_way(week_str)
    mon_str = "Monday"
    mon_way = yao_budunit.make_way(week_way, mon_str)
    tue_str = "Tuesday"
    tue_way = yao_budunit.make_way(week_way, tue_str)
    mon_premise_x = premiseunit_shop(need=mon_way)
    mon_premise_x._status = False
    mon_premise_x._task = False
    tue_premise_x = premiseunit_shop(need=tue_way)
    tue_premise_x._status = False
    tue_premise_x._task = False
    mt_premises = {
        mon_premise_x.need: mon_premise_x,
        tue_premise_x.need: tue_premise_x,
    }
    mt_reasonunit = reasonunit_shop(week_way, premises=mt_premises)
    mt_reasonheir = reasonheir_shop(week_way, premises=mt_premises, _status=False)
    x_itemroot = yao_budunit.get_item_obj(to_way(yao_budunit.fisc_tag))
    x_itemroot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_budunit.reasonunits[week_way].base=}")
    # print(f"{yao_budunit.reasonunits[week_way].premises[mon_way].need=}")
    # print(f"{yao_budunit.reasonunits[week_way].premises[tue_way].need=}")
    week_reasonunit = x_itemroot.reasonunits[week_way]
    print(f"{week_reasonunit.premises=}")
    premise_mon = week_reasonunit.premises.get(mon_way)
    premise_tue = week_reasonunit.premises.get(tue_way)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.need]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.need]
    assert week_reasonunit == mt_reasonunit

    # WHEN
    item_dict = yao_budunit.get_item_dict()

    # THEN
    gen_week_reasonheir = x_itemroot.get_reasonheir(week_way)
    gen_mon_premise = gen_week_reasonheir.premises.get(mon_way)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_way)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_way)
    assert gen_week_reasonheir.premises == mt_reasonheir.premises
    assert gen_week_reasonheir == mt_reasonheir

    casa_str = "casa"
    casa_way = yao_budunit.make_l1_way(casa_str)
    bird_str = "say hi to birds"
    bird_way = yao_budunit.make_way(casa_way, bird_str)
    assert from_list_get_active(bird_way, item_dict) is False

    # yao_budunit.add_fact(fbase=week_way, fneed=mon_way)
    # item_dict = yao_budunit.get_item_dict()
    # casa_item = x_itemroot._kids[casa_str]
    # twee_item = casa_item._kids[bird_str]
    # print(f"{len(x_itemroot._reasonheirs)=}")
    # print(f"{len(casa_item._reasonheirs)=}")
    # print(f"{len(twee_item._reasonheirs)=}")

    # assert YR.get_active(way=bird_item, item_dict=item_dict) is True

    # yao_budunit.add_fact(fbase=f"{yao_budunit.fisc_tag},weekdays", fneed=f"{yao_budunit.fisc_tag},weekdays,Tuesday")
    # item_dict = yao_budunit.get_item_dict()
    # assert YR.get_active(way=bird_item, item_dict=item_dict) is True

    # yao_budunit.add_fact(fbase=f"{yao_budunit.fisc_tag},weekdays", fneed=f"{yao_budunit.fisc_tag},weekdays,Wednesday")
    # item_dict = yao_budunit.get_item_dict()
    # assert YR.get_active(way=bird_item, item_dict=item_dict) is False


def test_BudUnit_settle_bud_CorrectlySetsItemUnitsActiveWithEvery6WeeksReason_budunit_v001():
    # ESTABLISH
    yao_budunit = budunit_v001()
    day_str = "day_hour"
    day_way = yao_budunit.make_l1_way(day_str)
    min_str = "day_minute"
    min_way = yao_budunit.make_l1_way(day_str)

    # WHEN
    yao_budunit.add_fact(fbase=day_way, fneed=day_way, fopen=0, fnigh=23)
    yao_budunit.add_fact(fbase=min_way, fneed=min_way, fopen=0, fnigh=59)
    yao_budunit.settle_bud()

    # THEN
    ced_week_base = yao_budunit.make_l1_way("ced_week")

    premise_divisor = None
    premise_open = None
    premise_nigh = None
    print(f"{len(yao_budunit._item_dict)=}")

    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    clean_couch_way = yao_budunit.make_way(cleaning_way, "clean sheets couch blankets")
    clean_sheet_item = yao_budunit.get_item_obj(clean_couch_way)
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
    #     # print(f"{item.parent_way=}")
    #     if item.item_tag == "clean sheets couch blankets":
    #         print(f"{item.get_item_way()=}")

    assert premise_divisor == 6
    assert premise_open == 1
    print(
        f"There exists a item with a reason_base {ced_week_base} that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(item_dict)=}")
    ced_week_open = 6001

    # WHEN
    yao_budunit.add_fact(
        fbase=ced_week_base,
        fneed=ced_week_base,
        fopen=ced_week_open,
        fnigh=ced_week_open,
    )
    nation_str = "Nation-States"
    nation_way = yao_budunit.make_l1_way(nation_str)
    yao_budunit.add_fact(fbase=nation_way, fneed=nation_way)
    print(
        f"Nation-states set and also fact set: {ced_week_base=} with {ced_week_open=} and {ced_week_open=}"
    )
    print(f"{yao_budunit.itemroot.factunits=}")
    yao_budunit.settle_bud()

    # THEN
    week_str = "ced_week"
    week_way = yao_budunit.make_l1_way(week_str)
    casa_way = yao_budunit.make_l1_way("casa")
    cleaning_way = yao_budunit.make_way(casa_way, "cleaning")
    clean_couch_str = "clean sheets couch blankets"
    clean_couch_way = yao_budunit.make_way(cleaning_way, clean_couch_str)
    clean_couch_item = yao_budunit.get_item_obj(way=clean_couch_way)
    week_reason = clean_couch_item.reasonunits.get(week_way)
    week_premise = week_reason.premises.get(week_way)
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
    minute_way = yao_budunit.make_l1_way(minute_str)
    yao_budunit.add_fact(fbase=minute_way, fneed=minute_way, fopen=0, fnigh=1399)
    month_str = "month_week"
    month_way = yao_budunit.make_l1_way(month_str)
    yao_budunit.add_fact(fbase=month_way, fneed=month_way)
    nations_str = "Nation-States"
    nations_way = yao_budunit.make_l1_way(nations_str)
    yao_budunit.add_fact(fbase=nations_way, fneed=nations_way)
    mood_str = "Moods"
    mood_way = yao_budunit.make_l1_way(mood_str)
    yao_budunit.add_fact(fbase=mood_way, fneed=mood_way)
    aaron_str = "Aaron Donald objects effected by him"
    aaron_way = yao_budunit.make_l1_way(aaron_str)
    yao_budunit.add_fact(fbase=aaron_way, fneed=aaron_way)
    interweb_str = "Interweb"
    interweb_way = yao_budunit.make_l1_way(interweb_str)
    yao_budunit.add_fact(fbase=interweb_way, fneed=interweb_way)
    weekdays_str = "weekdays"
    weekdays_way = yao_budunit.make_l1_way(weekdays_str)
    yao_budunit.add_fact(fbase=weekdays_way, fneed=weekdays_way)
    item_dict = yao_budunit.get_item_dict()
    print(f"{len(item_dict)=}")

    casa_str = "casa"
    casa_way = yao_budunit.make_l1_way(casa_str)
    clean_str = "cleaning"
    clean_way = yao_budunit.make_way(casa_way, clean_str)
    mat_item_tag = "deep clean play mat"
    mat_way = yao_budunit.make_way(clean_way, mat_item_tag)
    assert from_list_get_active(mat_way, item_dict) is False

    year_month_base = yao_budunit.make_l1_way("year_month")
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    yao_budunit.add_fact(fbase=year_month_base, fneed=year_month_base, fopen=0, fnigh=8)
    ced_week = yao_budunit.make_l1_way("ced_week")
    yao_budunit.add_fact(fbase=ced_week, fneed=ced_week, fopen=0, fnigh=4)
    yao_budunit.settle_bud()

    # THEN
    print(f"{len(item_dict)=}")
    print(f"{len(yao_budunit.itemroot.factunits)=}")
    assert from_list_get_active(mat_way, yao_budunit._item_dict)


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
    sue_budunit.edit_item_attr(oregon_way, problem_bool=True, healerlink=sue_healerlink)
    oregon_item = sue_budunit.get_item_obj(oregon_way)
    print(f"{oregon_item._fund_ratio=}")
    assert sue_budunit._sum_healerlink_share == 0
    assert oregon_item._healerlink_ratio == 0

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._sum_healerlink_share == 0.038461539 * default_fund_pool()
    assert oregon_item._healerlink_ratio == 1

    # WHEN
    week_way = sue_budunit.make_l1_way("weekdays")
    sue_budunit.edit_item_attr(week_way, problem_bool=True)
    mon_way = sue_budunit.make_way(week_way, "Monday")
    sue_budunit.edit_item_attr(mon_way, healerlink=sue_healerlink)
    mon_item = sue_budunit.get_item_obj(mon_way)
    # print(f"{mon_item.problem_bool=} {mon_item._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._sum_healerlink_share != 0.038461539 * default_fund_pool()
    assert sue_budunit._sum_healerlink_share == 0.06923077 * default_fund_pool()
    assert oregon_item._healerlink_ratio == 0.5555555571604938
    assert mon_item._healerlink_ratio == 0.4444444428395062

    # WHEN
    tue_way = sue_budunit.make_way(week_way, "Tuesday")
    sue_budunit.edit_item_attr(tue_way, healerlink=sue_healerlink)
    tue_item = sue_budunit.get_item_obj(tue_way)
    # print(f"{tue_item.problem_bool=} {tue_item._fund_ratio=}")
    # sat_way = sue_budunit.make_way(week_way, "Saturday")
    # sat_item = sue_budunit.get_item_obj(sat_way)
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
    sue_budunit.edit_item_attr(week_way, healerlink=sue_healerlink)
    week_item = sue_budunit.get_item_obj(week_way)
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
    nation_way = sue_budunit.make_l1_way("nation-state")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({"Sue"})
    sue_budunit.edit_item_attr(oregon_way, problem_bool=True, healerlink=sue_healerlink)
    assert len(sue_budunit._keep_dict) == 0
    assert sue_budunit._keep_dict.get(oregon_way) is None

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert len(sue_budunit._keep_dict) == 1
    assert sue_budunit._keep_dict.get(oregon_way) is not None

    # WHEN
    week_way = sue_budunit.make_l1_way("weekdays")
    sue_budunit.edit_item_attr(week_way, problem_bool=True)
    mon_way = sue_budunit.make_way(week_way, "Monday")
    sue_budunit.edit_item_attr(mon_way, healerlink=sue_healerlink)
    # mon_item = sue_budunit.get_item_obj(mon_way)
    # print(f"{mon_item.problem_bool=} {mon_item._fund_ratio=}")
    sue_budunit.settle_bud()
    # THEN
    assert len(sue_budunit._keep_dict) == 2
    assert sue_budunit._keep_dict.get(oregon_way) is not None
    assert sue_budunit._keep_dict.get(mon_way) is not None

    # WHEN
    tue_way = sue_budunit.make_way(week_way, "Tuesday")
    sue_budunit.edit_item_attr(tue_way, healerlink=sue_healerlink)
    # tue_item = sue_budunit.get_item_obj(tue_way)
    # print(f"{tue_item.problem_bool=} {tue_item._fund_ratio=}")
    # sat_way = sue_budunit.make_way(week_way, "Saturday")
    # sat_item = sue_budunit.get_item_obj(sat_way)
    # print(f"{sat_item.problem_bool=} {sat_item._fund_ratio=}")
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._keep_dict) == 3
    assert sue_budunit._keep_dict.get(oregon_way) is not None
    assert sue_budunit._keep_dict.get(mon_way) is not None
    assert sue_budunit._keep_dict.get(tue_way) is not None

    # WHEN
    sue_budunit.edit_item_attr(week_way, healerlink=sue_healerlink)
    week_item = sue_budunit.get_item_obj(week_way)
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
    nation_way = sue_budunit.make_l1_way("nation-state")
    usa_way = sue_budunit.make_way(nation_way, "USA")
    oregon_way = sue_budunit.make_way(usa_way, "Oregon")
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_item_attr(oregon_way, problem_bool=True, healerlink=sue_healerlink)

    week_way = sue_budunit.make_l1_way("weekdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_budunit.edit_item_attr(week_way, problem_bool=True, healerlink=bob_healerlink)
    assert sue_budunit._healers_dict == {}

    # WHEN
    sue_budunit.settle_bud()

    # THEN
    assert len(sue_budunit._healers_dict) == 2
    week_item = sue_budunit.get_item_obj(week_way)
    assert sue_budunit._healers_dict.get(bob_str) == {week_way: week_item}
    oregon_item = sue_budunit.get_item_obj(oregon_way)
    assert sue_budunit._healers_dict.get(sue_str) == {oregon_way: oregon_item}


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
    sue_budunit.edit_item_attr(oregon_way, problem_bool=True, healerlink=sue_healerlink)

    week_way = sue_budunit.make_l1_way("weekdays")
    bob_healerlink = healerlink_shop({bob_str})
    sue_budunit.edit_item_attr(week_way, problem_bool=True, healerlink=bob_healerlink)

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
    sue_budunit.set_item(itemunit_shop(bend_str), oregon_way)
    sue_healerlink = healerlink_shop({sue_str})
    sue_budunit.edit_item_attr(bend_way, problem_bool=True, healerlink=sue_healerlink)
    assert sue_budunit._keeps_buildable

    # WHEN
    sue_budunit.settle_bud()
    # THEN
    assert sue_budunit._keeps_buildable is False
