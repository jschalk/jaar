from src._road.finance import default_bud_pool
from src._world.graphic import display_ideatree
from src._world.char import charunit_shop
from src._world.lobby import awardlink_shop
from src._world.world import worldunit_shop
from src._world.healer import healerhold_shop
from src._world.examples.example_worlds import (
    get_world_with_4_levels_and_2reasons,
    get_world_with7amCleanTableReason,
    world_v001,
    from_list_get_active,
)
from src._world.idea import ideaunit_shop
from src._world.reason_idea import premiseunit_shop, reasonunit_shop, reasonheir_shop
from src._world.world import worldunit_shop


def test_WorldUnit_get_tree_metrics_TracksReasonsThatHaveNoFactBases():
    # ESTABLISH
    yao_worldunit = world_v001()

    # WHEN
    yao_world_metrics = yao_worldunit.get_tree_metrics()

    # THEN
    print(f"{yao_world_metrics.level_count=}")
    print(f"{yao_world_metrics.reason_bases=}")
    assert yao_world_metrics != None
    reason_bases_x = yao_world_metrics.reason_bases
    assert reason_bases_x != None
    assert len(reason_bases_x) > 0


def test_WorldUnit_get_missing_fact_bases_ReturnsAllBasesNotCoveredByFacts():
    # ESTABLISH
    yao_worldunit = world_v001()
    missing_bases = yao_worldunit.get_missing_fact_bases()
    assert missing_bases != None
    print(f"{missing_bases=}")
    print(f"{len(missing_bases)=}")
    assert len(missing_bases) == 11

    yao_worldunit.set_fact(
        base=yao_worldunit.make_l1_road("day_minute"),
        pick=yao_worldunit.make_l1_road("day_minute"),
        open=0,
        nigh=1439,
    )

    # WHEN
    missing_bases = yao_worldunit.get_missing_fact_bases()

    # THEN
    assert len(missing_bases) == 11


def test_WorldUnit_3AdvocatesNoideaunit_shop():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"

    zia_worldunit = worldunit_shop("Zia")
    yao_charunit = charunit_shop(char_id=yao_text)
    sue_charunit = charunit_shop(char_id=sue_text)
    zia_charunit = charunit_shop(char_id=zia_text)
    # print(f"{yao=}")
    zia_worldunit.set_charunit(yao_charunit)
    zia_worldunit.set_charunit(sue_charunit)
    zia_worldunit.set_charunit(zia_charunit)
    zia_worldunit._idearoot.set_awardlink(awardlink_shop(yao_text, give_weight=10))
    zia_worldunit._idearoot.set_awardlink(awardlink_shop(sue_text, give_weight=10))
    zia_worldunit._idearoot.set_awardlink(awardlink_shop(zia_text, give_weight=10))

    # WHEN
    assert zia_worldunit.get_awardlinks_metrics() != None
    chars_metrics = zia_worldunit.get_awardlinks_metrics()

    # THEN
    awardlink_yao = chars_metrics[yao_text]
    awardlink_sue = chars_metrics[sue_text]
    awardlink_zia = chars_metrics[zia_text]
    assert awardlink_yao.lobby_id != None
    assert awardlink_sue.lobby_id != None
    assert awardlink_zia.lobby_id != None
    assert awardlink_yao.lobby_id == yao_text
    assert awardlink_sue.lobby_id == sue_text
    assert awardlink_zia.lobby_id == zia_text


def test_WorldUnit_calc_world_metrics_CreatesFullyPopulated_idea_dict():
    # ESTABLISH
    sue_worldunit = get_world_with_4_levels_and_2reasons()

    # WHEN
    sue_worldunit.calc_world_metrics()

    # THEN
    assert len(sue_worldunit._idea_dict) == 17


def test_WorldUnit_calc_world_metrics_SetsSatiateStatusCorrectlyWhenFactSaysNo():
    # ESTABLISH
    sue_worldunit = get_world_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_worldunit.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = sue_worldunit.make_road(week_road, sun_text)

    # for idea in sue_worldunit._idea_dict.values():
    #     print(f"{casa_road=} {idea.get_road()=}")
    casa_text = "casa"
    casa_road = sue_worldunit.make_l1_road(casa_text)
    assert sue_worldunit.get_idea_obj(casa_road)._active is None

    # WHEN
    sue_worldunit.set_fact(base=week_road, pick=sun_road)
    sue_worldunit.calc_world_metrics()

    # THEN
    assert sue_worldunit._idea_dict != {}
    assert len(sue_worldunit._idea_dict) == 17

    # for idea in sue_worldunit._idea_dict.values():
    #     print(f"{casa_road=} {idea.get_road()=}")
    assert sue_worldunit.get_idea_obj(casa_road)._active is False


def test_WorldUnit_calc_world_metrics_SetsSatiateStatusCorrectlyWhenFactModifies():
    # ESTABLISH
    sue_worldunit = get_world_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_worldunit.make_l1_road(week_text)
    sun_text = "Wednesday"
    sun_road = sue_worldunit.make_road(week_road, sun_text)
    casa_text = "casa"
    casa_road = sue_worldunit.make_l1_road(casa_text)

    # WHEN
    sue_worldunit.set_fact(base=week_road, pick=sun_road)

    # THEN
    sue_worldunit.calc_world_metrics()
    assert sue_worldunit._idea_dict
    assert len(sue_worldunit._idea_dict) == 17
    assert sue_worldunit._idea_dict.get(casa_road)._active is False

    # WHEN
    states_text = "nation-state"
    states_road = sue_worldunit.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_worldunit.make_road(states_road, usa_text)
    sue_worldunit.set_fact(base=states_road, pick=usa_road)

    # THEN
    sue_worldunit.calc_world_metrics()
    assert sue_worldunit._idea_dict
    assert len(sue_worldunit._idea_dict) == 17
    assert sue_worldunit._idea_dict.get(casa_road)._active

    # WHEN
    france_text = "France"
    france_road = sue_worldunit.make_road(states_road, france_text)
    sue_worldunit.set_fact(base=states_road, pick=france_road)

    # THEN
    sue_worldunit.calc_world_metrics()
    assert sue_worldunit._idea_dict
    assert len(sue_worldunit._idea_dict) == 17
    assert sue_worldunit._idea_dict.get(casa_road)._active is False


def test_WorldUnit_calc_world_metrics_CorrectlySets_idea_dict():
    # ESTABLISH
    sue_worldunit = get_world_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_worldunit.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_worldunit.make_road(week_road, wed_text)
    state_text = "nation-state"
    state_road = sue_worldunit.make_l1_road(state_text)
    france_text = "France"
    france_road = sue_worldunit.make_road(state_road, france_text)
    sue_worldunit.set_fact(base=week_road, pick=wed_road)
    sue_worldunit.set_fact(base=state_road, pick=france_road)

    casa_text = "casa"
    casa_road = sue_worldunit.make_l1_road(casa_text)
    casa_idea = sue_worldunit.get_idea_obj(casa_road)
    print(f"{sue_worldunit._owner_id=} {len(casa_idea._reasonunits)=}")
    # print(f"{casa_idea._reasonunits=}")
    print(f"{sue_worldunit._owner_id=} {len(sue_worldunit._idearoot._factunits)=}")
    # print(f"{sue_worldunit._idearoot._factunits=}")

    sue_worldunit.calc_world_metrics()
    assert sue_worldunit._idea_dict
    assert len(sue_worldunit._idea_dict) == 17

    usa_text = "USA"
    usa_road = sue_worldunit.make_road(state_road, usa_text)
    oregon_text = "Oregon"
    oregon_road = sue_worldunit.make_road(usa_road, oregon_text)

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
        _base_idea_active_value=True,
    )
    sta_lh = reasonheir_shop(
        base=state_road,
        premises={usa.need: usa},
        _status=True,
        _task=False,
        _base_idea_active_value=True,
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
    sue_worldunit.set_fact(base=state_road, pick=oregon_road)

    # THEN
    casa_idea = sue_worldunit._idea_dict.get(casa_road)
    print(f"\nlook at {casa_idea.get_road()=}")
    assert casa_idea._parent_road == sue_worldunit._real_id
    assert casa_idea._kids == {}
    assert casa_idea._weight == 30
    assert casa_idea._label == casa_text
    assert casa_idea._level == 1
    assert casa_idea._active
    assert casa_idea.pledge
    # print(f"{casa_idea._reasonheirs=}")
    x_reasonheir_state = casa_idea._reasonheirs[state_road]
    print(f"  {x_reasonheir_state=}")
    print(f"  {x_reasonheir_state._status=}\n")
    # assert casa_idea._reasonheirs == x1_reasonheirs

    assert len(casa_idea._reasonheirs) == len(x1_reasonheirs)
    week_reasonheir = casa_idea._reasonheirs.get(week_road)
    # usa_premise = week_reasonheir.premises.get(usa_road)
    print(f"    {casa_idea._label=}")
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

    # assert casa_idea._reasonunits == x1_reasonunits

    # print("iterate through every idea...")
    # for x_idea in idea_dict:
    #     if str(type(x_idea)).find(".idea.IdeaUnit'>") > 0:
    #         assert x_idea._active != None

    #     # print("")
    #     # print(f"{x_idea._label=}")
    #     # print(f"{len(x_idea._reasonunits)=}")
    #     print(
    #         f"  {x_idea._label} iterate through every reasonheir... {len(x_idea._reasonheirs)=} {x_idea._label=}"
    #     )
    #     # print(f"{x_idea._reasonheirs=}")
    #     for reason in x_idea._reasonheirs.values():
    #         assert str(type(reason)).find(".reason.ReasonHeir'>") > 0
    #         print(f"    {reason.base=}")
    #         assert reason._status != None
    #         for premise_x in reason.premises.values():
    #             assert premise_x._status != None
    #         assert _check_all_objects_in_dict_are_correct_type(
    #             x_dict=reason.premises, type_str="src._worldunit.reason.PremiseUnit"
    #         )


# def _check_all_objects_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
#     bool_x = True
#     for x_value in x_dict.values():
#         if type_str not in str(type(x_value)):
#             bool_x = False
#         print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
#     return bool_x


def test_WorldUnit_calc_world_metrics_CorrectlyClears_bud_onset_bud_cease():
    # ESTABLISH
    x_worldunit = get_world_with7amCleanTableReason()
    casa_road = x_worldunit.make_l1_road("casa")
    catt_road = x_worldunit.make_l1_road("cat have dinner")
    week_road = x_worldunit.make_l1_road("weekdays")
    x_worldunit._idearoot._bud_onset = 13
    x_worldunit._idearoot._bud_cease = 13
    x_worldunit.get_idea_obj(casa_road)._bud_onset = 13
    x_worldunit.get_idea_obj(casa_road)._bud_cease = 13
    x_worldunit.get_idea_obj(catt_road)._bud_onset = 13
    x_worldunit.get_idea_obj(catt_road)._bud_cease = 13
    x_worldunit.get_idea_obj(week_road)._bud_onset = 13
    x_worldunit.get_idea_obj(week_road)._bud_cease = 13

    assert x_worldunit._idearoot._bud_onset == 13
    assert x_worldunit._idearoot._bud_cease == 13
    assert x_worldunit.get_idea_obj(casa_road)._bud_onset == 13
    assert x_worldunit.get_idea_obj(casa_road)._bud_cease == 13
    assert x_worldunit.get_idea_obj(catt_road)._bud_onset == 13
    assert x_worldunit.get_idea_obj(catt_road)._bud_cease == 13
    assert x_worldunit.get_idea_obj(week_road)._bud_onset == 13
    assert x_worldunit.get_idea_obj(week_road)._bud_cease == 13

    # WHEN
    x_worldunit.calc_world_metrics()

    # THEN
    assert x_worldunit._idearoot._bud_onset != 13
    assert x_worldunit._idearoot._bud_cease != 13
    assert x_worldunit.get_idea_obj(casa_road)._bud_onset != 13
    assert x_worldunit.get_idea_obj(casa_road)._bud_cease != 13
    assert x_worldunit.get_idea_obj(catt_road)._bud_onset != 13
    assert x_worldunit.get_idea_obj(catt_road)._bud_cease != 13
    assert x_worldunit.get_idea_obj(week_road)._bud_onset != 13
    assert x_worldunit.get_idea_obj(week_road)._bud_cease != 13


def test_WorldUnit_calc_world_metrics_CorrectlyCalculatesIdeaAttr_bud_onset_bud_cease():
    # ESTABLISH
    yao_worldunit = worldunit_shop("Yao", _weight=10)

    auto_text = "auto"
    auto_road = yao_worldunit.make_l1_road(auto_text)
    auto_idea = ideaunit_shop(auto_text, _weight=10)
    yao_worldunit.add_l1_idea(auto_idea)

    barn_text = "barn"
    barn_road = yao_worldunit.make_l1_road(barn_text)
    barn_idea = ideaunit_shop(barn_text, _weight=60)
    yao_worldunit.add_l1_idea(barn_idea)
    lamb_text = "lambs"
    lamb_road = yao_worldunit.make_road(barn_road, lamb_text)
    lamb_idea = ideaunit_shop(lamb_text, _weight=1)
    yao_worldunit.add_idea(lamb_idea, parent_road=barn_road)
    duck_text = "ducks"
    duck_road = yao_worldunit.make_road(barn_road, duck_text)
    duck_idea = ideaunit_shop(duck_text, _weight=2)
    yao_worldunit.add_idea(duck_idea, parent_road=barn_road)

    coal_text = "coal"
    coal_road = yao_worldunit.make_l1_road(coal_text)
    coal_idea = ideaunit_shop(coal_text, _weight=30)
    yao_worldunit.add_l1_idea(coal_idea)

    assert yao_worldunit._idearoot._bud_onset is None
    assert yao_worldunit._idearoot._bud_cease is None
    assert yao_worldunit.get_idea_obj(auto_road)._bud_onset is None
    assert yao_worldunit.get_idea_obj(auto_road)._bud_cease is None
    assert yao_worldunit.get_idea_obj(barn_road)._bud_onset is None
    assert yao_worldunit.get_idea_obj(barn_road)._bud_cease is None
    assert yao_worldunit.get_idea_obj(coal_road)._bud_onset is None
    assert yao_worldunit.get_idea_obj(coal_road)._bud_cease is None
    lamb_before = yao_worldunit.get_idea_obj(road=lamb_road)
    assert lamb_before._bud_onset is None
    assert lamb_before._bud_cease is None
    duck_before = yao_worldunit.get_idea_obj(road=duck_road)
    assert duck_before._bud_onset is None
    assert duck_before._bud_cease is None

    # WHEN
    yao_worldunit.calc_world_metrics()

    # THEN
    assert yao_worldunit._idearoot._bud_onset == 0.0
    assert yao_worldunit._idearoot._bud_cease == default_bud_pool()
    assert yao_worldunit.get_idea_obj(auto_road)._bud_onset == 0.0
    assert yao_worldunit.get_idea_obj(auto_road)._bud_cease == default_bud_pool() * 0.1
    assert yao_worldunit.get_idea_obj(barn_road)._bud_onset == default_bud_pool() * 0.1
    assert yao_worldunit.get_idea_obj(barn_road)._bud_cease == default_bud_pool() * 0.7
    assert yao_worldunit.get_idea_obj(coal_road)._bud_onset == default_bud_pool() * 0.7
    assert yao_worldunit.get_idea_obj(coal_road)._bud_cease == default_bud_pool() * 1.0

    duck_after = yao_worldunit.get_idea_obj(road=duck_road)
    assert duck_after._bud_onset == default_bud_pool() * 0.1
    assert duck_after._bud_cease == default_bud_pool() * 0.5
    lamb_after = yao_worldunit.get_idea_obj(road=lamb_road)
    assert lamb_after._bud_onset == default_bud_pool() * 0.5
    assert lamb_after._bud_cease == default_bud_pool() * 0.7


def test_WorldUnit_get_idea_list_without_root_CorrectlyCalculatesIdeaAttributes():
    # ESTABLISH
    x_worldunit = get_world_with7amCleanTableReason()

    # WHEN
    idea_list_without_idearoot = x_worldunit.get_idea_list_without_idearoot()
    idea_dict_with_idearoot = x_worldunit.get_idea_dict()

    # THEN
    assert len(idea_list_without_idearoot) == 28
    assert len(idea_list_without_idearoot) + 1 == len(idea_dict_with_idearoot)

    # for idea in x_worldunit.get_idea_list_without_idearoot():
    #     assert str(type(idea)).find(".idea.IdeaUnit'>") > 0

    # for idea in x_worldunit.get_idea_list_without_idearoot():
    #     print(f"{idea._label=}")


def test_WorldUnit_calc_world_metrics_CorrectlyCalculatesRangeAttributes():
    # ESTABLISH
    sue_worldunit = get_world_with7amCleanTableReason()
    sue_worldunit.calc_world_metrics()
    house_text = "housemanagement"
    house_road = sue_worldunit.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = sue_worldunit.make_road(house_road, clean_text)
    assert sue_worldunit._idea_dict.get(clean_road)._active is False

    # set facts as midnight to 8am
    time_text = "timetech"
    time_road = sue_worldunit.make_l1_road(time_text)
    day24hr_text = "24hr day"
    day24hr_road = sue_worldunit.make_road(time_road, day24hr_text)
    day24hr_base = day24hr_road
    day24hr_pick = day24hr_road
    day24hr_open = 0.0
    day24hr_nigh = 8.0

    # WHEN
    sue_worldunit.set_fact(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )

    # THEN
    sue_worldunit.calc_world_metrics()
    assert sue_worldunit._idea_dict.get(clean_road)._active

    # WHEN
    # set facts as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(sue_worldunit._idearoot._factunits[day24hr_road])
    sue_worldunit.set_fact(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )
    print(sue_worldunit._idearoot._factunits[day24hr_road])
    print(sue_worldunit._idearoot._kids[house_text]._kids[clean_text]._reasonunits)
    # sue_worldunit._idearoot._kids["housemanagement"]._kids[clean_text]._active = None

    # THEN
    sue_worldunit.calc_world_metrics()
    assert sue_worldunit._idea_dict.get(clean_road)._active is False


def test_get_agenda_dict_ReturnsCorrectObj():
    # ESTABLISH
    sue_worldunit = get_world_with_4_levels_and_2reasons()

    # WHEN
    pledge_items = sue_worldunit.get_agenda_dict()

    # THEN
    assert pledge_items != None
    assert len(pledge_items) > 0
    assert len(pledge_items) == 1


def test_WorldUnit_calc_world_metrics_CorrectlySetsData_world_v001():
    yao_worldunit = world_v001()
    print(f"{yao_worldunit.get_reason_bases()=}")
    # day_hour = f"{yao_worldunit._real_id},day_hour"
    # yao_worldunit.set_fact(base=day_hour, pick=day_hour, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_worldunit.make_l1_road(day_min_text)
    yao_worldunit.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=1439)

    mood_text = "Moods"
    mood_road = yao_worldunit.make_l1_road(mood_text)
    yao_worldunit.set_fact(base=mood_road, pick=mood_road)
    print(f"{yao_worldunit.get_reason_bases()=}")

    yr_mon_text = "year_month"
    yr_mon_road = yao_worldunit.make_l1_road(yr_mon_text)
    yao_worldunit.set_fact(base=yr_mon_road, pick=yr_mon_road)
    inter_text = "Internet"
    inter_road = yao_worldunit.make_l1_road(inter_text)
    yao_worldunit.set_fact(base=inter_road, pick=inter_road)
    assert yao_worldunit != None
    # print(f"{yao_worldunit._owner_id=}")
    # print(f"{len(yao_worldunit._idearoot._kids)=}")
    ulty_text = "Ultimate Frisbee"
    ulty_road = yao_worldunit.make_l1_road(ulty_text)

    # if yao_worldunit._idearoot._kids["Ultimate Frisbee"]._label == "Ultimate Frisbee":
    assert yao_worldunit._idearoot._kids[ulty_text]._reasonunits != None
    assert yao_worldunit._owner_id != None

    # for fact in yao_worldunit._idearoot._factunits.values():
    #     print(f"{fact=}")

    yao_worldunit.calc_world_metrics()
    # print(f"{str(type(idea))=}")
    # print(f"{len(idea_dict)=}")
    laundry_text = "laundry monday"
    casa_road = yao_worldunit.make_l1_road("casa")
    cleaning_road = yao_worldunit.make_road(casa_road, "cleaning")
    laundry_road = yao_worldunit.make_road(cleaning_road, laundry_text)

    # for idea in idea_dict:
    #     assert (
    #         str(type(idea)).find(".idea.IdeaUnit'>") > 0
    #         or str(type(idea)).find(".idea.IdeaUnit'>") > 0
    #     )
    #     # print(f"{idea._label=}")
    #     if idea._label == laundry_text:
    #         for reason in idea._reasonunits.values():
    #             print(f"{idea._label=} {reason.base=}")  # {reason.premises=}")
    # assert idea._active is False
    assert yao_worldunit._idea_dict.get(laundry_road)._active is False

    # WHEN
    week_text = "weekdays"
    week_road = yao_worldunit.make_l1_road(week_text)
    mon_text = "Monday"
    mon_road = yao_worldunit.make_road(week_road, mon_text)
    yao_worldunit.set_fact(base=week_road, pick=mon_road)
    yao_worldunit.calc_world_metrics()

    # THEN
    assert yao_worldunit._idea_dict.get(laundry_road)._active is False


def test_WorldUnit_calc_world_metrics_OptionWeekdaysReturnsCorrectObj_world_v001():
    # ESTABLISH
    yao_worldunit = world_v001()

    day_hr_text = "day_hour"
    day_hr_road = yao_worldunit.make_l1_road(day_hr_text)
    yao_worldunit.set_fact(base=day_hr_road, pick=day_hr_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_worldunit.make_l1_road(day_min_text)
    yao_worldunit.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    mon_wk_text = "month_week"
    mon_wk_road = yao_worldunit.make_l1_road(mon_wk_text)
    yao_worldunit.set_fact(base=mon_wk_road, pick=mon_wk_road)
    nation_text = "Nation-States"
    nation_road = yao_worldunit.make_l1_road(nation_text)
    yao_worldunit.set_fact(base=nation_road, pick=nation_road)
    mood_text = "Moods"
    mood_road = yao_worldunit.make_l1_road(mood_text)
    yao_worldunit.set_fact(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = yao_worldunit.make_l1_road(aaron_text)
    yao_worldunit.set_fact(base=aaron_road, pick=aaron_road)
    inter_text = "Internet"
    inter_road = yao_worldunit.make_l1_road(inter_text)
    yao_worldunit.set_fact(base=inter_road, pick=inter_road)
    yr_mon_text = "year_month"
    yr_mon_road = yao_worldunit.make_l1_road(yr_mon_text)
    yao_worldunit.set_fact(base=yr_mon_road, pick=yr_mon_road, open=0, nigh=1000)

    yao_worldunit.calc_world_metrics()
    missing_facts = yao_worldunit.get_missing_fact_bases()
    # for missing_fact, count in missing_facts.items():
    #     print(f"{missing_fact=} {count=}")

    week_text = "weekdays"
    week_road = yao_worldunit.make_l1_road(week_text)
    mon_text = "Monday"
    mon_road = yao_worldunit.make_road(week_road, mon_text)
    tue_text = "Tuesday"
    tue_road = yao_worldunit.make_road(week_road, tue_text)
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
    x_idearoot = yao_worldunit.get_idea_obj(yao_worldunit._real_id)
    x_idearoot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_worldunit._reasonunits[week_road].base=}")
    # print(f"{yao_worldunit._reasonunits[week_road].premises[mon_road].need=}")
    # print(f"{yao_worldunit._reasonunits[week_road].premises[tue_road].need=}")
    week_reasonunit = x_idearoot._reasonunits[week_road]
    print(f"{week_reasonunit.premises=}")
    premise_mon = week_reasonunit.premises.get(mon_road)
    premise_tue = week_reasonunit.premises.get(tue_road)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.need]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.need]
    assert week_reasonunit == mt_reasonunit

    # WHEN
    idea_dict = yao_worldunit.get_idea_dict()

    # THEN
    gen_week_reasonheir = x_idearoot.get_reasonheir(week_road)
    gen_mon_premise = gen_week_reasonheir.premises.get(mon_road)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_road)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_road)
    assert gen_week_reasonheir.premises == mt_reasonheir.premises
    assert gen_week_reasonheir == mt_reasonheir

    casa_text = "casa"
    casa_road = yao_worldunit.make_l1_road(casa_text)
    bird_text = "say hi to birds"
    bird_road = yao_worldunit.make_road(casa_road, bird_text)
    assert from_list_get_active(road=bird_road, idea_dict=idea_dict) is False

    # yao_worldunit.set_fact(base=week_road, pick=mon_road)
    # idea_dict = yao_worldunit.get_idea_dict()
    # casa_idea = x_idearoot._kids[casa_text]
    # twee_idea = casa_idea._kids[bird_text]
    # print(f"{len(x_idearoot._reasonheirs)=}")
    # print(f"{len(casa_idea._reasonheirs)=}")
    # print(f"{len(twee_idea._reasonheirs)=}")

    # assert YR.get_active(road=bird_idea, idea_dict=idea_dict) == True

    # yao_worldunit.set_fact(base=f"{yao_worldunit._real_id},weekdays", pick=f"{yao_worldunit._real_id},weekdays,Tuesday")
    # idea_dict = yao_worldunit.get_idea_dict()
    # assert YR.get_active(road=bird_idea, idea_dict=idea_dict) == True

    # yao_worldunit.set_fact(base=f"{yao_worldunit._real_id},weekdays", pick=f"{yao_worldunit._real_id},weekdays,Wednesday")
    # idea_dict = yao_worldunit.get_idea_dict()
    # assert YR.get_active(road=bird_idea, idea_dict=idea_dict) is False


def test_WorldUnit_calc_world_metrics_CorrectlySetsIdeaUnitsActiveWithEvery6WeeksReason_world_v001():
    # ESTABLISH
    yao_worldunit = world_v001()
    day_text = "day_hour"
    day_road = yao_worldunit.make_l1_road(day_text)
    min_text = "day_minute"
    min_road = yao_worldunit.make_l1_road(day_text)

    # WHEN
    yao_worldunit.set_fact(base=day_road, pick=day_road, open=0, nigh=23)
    yao_worldunit.set_fact(base=min_road, pick=min_road, open=0, nigh=59)
    yao_worldunit.calc_world_metrics()

    # THEN
    ced_week_base = yao_worldunit.make_l1_road("ced_week")

    premise_divisor = None
    premise_open = None
    premise_nigh = None
    print(f"{len(yao_worldunit._idea_dict)=}")

    casa_road = yao_worldunit.make_l1_road("casa")
    cleaning_road = yao_worldunit.make_road(casa_road, "cleaning")
    clean_couch_road = yao_worldunit.make_road(
        cleaning_road, "clean sheets couch blankets"
    )
    clean_sheet_idea = yao_worldunit.get_idea_obj(clean_couch_road)
    # print(f"{clean_sheet_idea._reasonunits.values()=}")
    ced_week_reason = clean_sheet_idea._reasonunits.get(ced_week_base)
    ced_week_premise = ced_week_reason.premises.get(ced_week_base)
    print(
        f"{clean_sheet_idea._label=} {ced_week_reason.base=} {ced_week_premise.need=}"
    )
    # print(f"{clean_sheet_idea._label=} {ced_week_reason.base=} {premise_x=}")
    premise_divisor = ced_week_premise.divisor
    premise_open = ced_week_premise.open
    premise_nigh = ced_week_premise.nigh
    # print(f"{idea._reasonunits=}")
    assert clean_sheet_idea._active is False

    # for idea in idea_dict:
    #     # print(f"{idea._parent_road=}")
    #     if idea._label == "clean sheets couch blankets":
    #         print(f"{idea.get_road()=}")

    assert premise_divisor == 6
    assert premise_open == 1
    print(
        f"There exists a idea with a reason_base {ced_week_base} that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(idea_dict)=}")
    ced_week_open = 6001

    # WHEN
    yao_worldunit.set_fact(
        base=ced_week_base, pick=ced_week_base, open=ced_week_open, nigh=ced_week_open
    )
    nation_text = "Nation-States"
    nation_road = yao_worldunit.make_l1_road(nation_text)
    yao_worldunit.set_fact(base=nation_road, pick=nation_road)
    print(
        f"Nation-states set and also fact set: {ced_week_base=} with {ced_week_open=} and {ced_week_open=}"
    )
    print(f"{yao_worldunit._idearoot._factunits=}")
    yao_worldunit.calc_world_metrics()

    # THEN
    week_text = "ced_week"
    week_road = yao_worldunit.make_l1_road(week_text)
    casa_road = yao_worldunit.make_l1_road("casa")
    cleaning_road = yao_worldunit.make_road(casa_road, "cleaning")
    clean_couch_text = "clean sheets couch blankets"
    clean_couch_road = yao_worldunit.make_road(cleaning_road, clean_couch_text)
    clean_couch_idea = yao_worldunit.get_idea_obj(road=clean_couch_road)
    week_reason = clean_couch_idea._reasonunits.get(week_road)
    week_premise = week_reason.premises.get(week_road)
    print(f"{clean_couch_idea._label=} {week_reason.base=} {week_premise=}")
    assert week_premise.divisor == 6 and week_premise.open == 1


def test_WorldUnit_calc_world_metrics_EveryIdeaHasActiveStatus_world_v001():
    # ESTABLISH
    yao_worldunit = world_v001()

    # WHEN
    yao_worldunit.calc_world_metrics()

    # THEN
    print(f"{len(yao_worldunit._idea_dict)=}")
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
    #     print(f"{idea._label=} {idea_kid_count=}")
    #     assert idea._active != None
    #     assert idea._active in (True, False)
    # assert idea_kid_count == len(idea_list_without_idearoot)

    assert len(yao_worldunit._idea_dict) == sum(
        idea._active != None for idea in yao_worldunit._idea_dict.values()
    )


def test_WorldUnit_calc_world_metrics_EveryTwoMonthReturnsCorrectObj_world_v001():
    # ESTABLISH
    yao_worldunit = world_v001()
    minute_text = "day_minute"
    minute_road = yao_worldunit.make_l1_road(minute_text)
    yao_worldunit.set_fact(base=minute_road, pick=minute_road, open=0, nigh=1399)
    month_text = "month_week"
    month_road = yao_worldunit.make_l1_road(month_text)
    yao_worldunit.set_fact(base=month_road, pick=month_road)
    nations_text = "Nation-States"
    nations_road = yao_worldunit.make_l1_road(nations_text)
    yao_worldunit.set_fact(base=nations_road, pick=nations_road)
    mood_text = "Moods"
    mood_road = yao_worldunit.make_l1_road(mood_text)
    yao_worldunit.set_fact(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = yao_worldunit.make_l1_road(aaron_text)
    yao_worldunit.set_fact(base=aaron_road, pick=aaron_road)
    internet_text = "Internet"
    internet_road = yao_worldunit.make_l1_road(internet_text)
    yao_worldunit.set_fact(base=internet_road, pick=internet_road)
    weekdays_text = "weekdays"
    weekdays_road = yao_worldunit.make_l1_road(weekdays_text)
    yao_worldunit.set_fact(base=weekdays_road, pick=weekdays_road)
    idea_dict = yao_worldunit.get_idea_dict()
    print(f"{len(idea_dict)=}")

    casa_text = "casa"
    casa_road = yao_worldunit.make_l1_road(casa_text)
    clean_text = "cleaning"
    clean_road = yao_worldunit.make_road(casa_road, clean_text)
    mat_label = "deep clean play mat"
    mat_road = yao_worldunit.make_road(clean_road, mat_label)
    assert from_list_get_active(road=mat_road, idea_dict=idea_dict) is False

    year_month_base = yao_worldunit.make_l1_road("year_month")
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    yao_worldunit.set_fact(base=year_month_base, pick=year_month_base, open=0, nigh=8)
    ced_week = yao_worldunit.make_l1_road("ced_week")
    yao_worldunit.set_fact(base=ced_week, pick=ced_week, open=0, nigh=4)
    yao_worldunit.calc_world_metrics()

    # THEN
    print(f"{len(idea_dict)=}")
    print(f"{len(yao_worldunit._idearoot._factunits)=}")
    # from_list_get_active(road=mat_road, idea_dict=idea_dict)
    assert from_list_get_active(road=mat_road, idea_dict=yao_worldunit._idea_dict)


def test_WorldUnit_calc_world_metrics_CorrectlySetsEmpty_sum_healerhold_share():
    # ESTABLISH
    sue_worldunit = worldunit_shop("Sue")
    assert sue_worldunit._sum_healerhold_share == 0
    assert sue_worldunit._econ_dict == {}

    # WHEN
    sue_worldunit.calc_world_metrics()

    # THEN
    assert sue_worldunit._sum_healerhold_share == 0
    assert sue_worldunit._econ_dict == {}


def test_WorldUnit_calc_world_metrics_CorrectlySets_sum_healerhold_share():
    # ESTABLISH
    sue_worldunit = get_world_with_4_levels_and_2reasons()
    sue_worldunit.add_charunit("Sue")
    sue_worldunit.calc_world_metrics()
    nation_road = sue_worldunit.make_l1_road("nation-state")
    usa_road = sue_worldunit.make_road(nation_road, "USA")
    oregon_road = sue_worldunit.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({"Sue"})
    sue_worldunit.edit_idea_attr(
        oregon_road, problem_bool=True, healerhold=sue_healerhold
    )
    oregon_idea = sue_worldunit.get_idea_obj(oregon_road)
    print(f"{oregon_idea._bud_ratio=}")
    assert sue_worldunit._sum_healerhold_share == 0
    assert oregon_idea._healerhold_ratio == 0

    # WHEN
    sue_worldunit.calc_world_metrics()
    # THEN
    assert sue_worldunit._sum_healerhold_share == 0.038461539 * default_bud_pool()
    assert oregon_idea._healerhold_ratio == 1

    # WHEN
    week_road = sue_worldunit.make_l1_road("weekdays")
    sue_worldunit.edit_idea_attr(week_road, problem_bool=True)
    mon_road = sue_worldunit.make_road(week_road, "Monday")
    sue_worldunit.edit_idea_attr(mon_road, healerhold=sue_healerhold)
    mon_idea = sue_worldunit.get_idea_obj(mon_road)
    # print(f"{mon_idea._problem_bool=} {mon_idea._bud_ratio=}")
    sue_worldunit.calc_world_metrics()
    # THEN
    assert sue_worldunit._sum_healerhold_share != 0.038461539 * default_bud_pool()
    assert sue_worldunit._sum_healerhold_share == 0.06923077 * default_bud_pool()
    assert oregon_idea._healerhold_ratio == 0.5555555571604938
    assert mon_idea._healerhold_ratio == 0.4444444428395062

    # WHEN
    tue_road = sue_worldunit.make_road(week_road, "Tuesday")
    sue_worldunit.edit_idea_attr(tue_road, healerhold=sue_healerhold)
    tue_idea = sue_worldunit.get_idea_obj(tue_road)
    # print(f"{tue_idea._problem_bool=} {tue_idea._bud_ratio=}")
    # sat_road = sue_worldunit.make_road(week_road, "Saturday")
    # sat_idea = sue_worldunit.get_idea_obj(sat_road)
    # print(f"{sat_idea._problem_bool=} {sat_idea._bud_ratio=}")
    sue_worldunit.calc_world_metrics()

    # THEN
    assert (
        sue_worldunit._sum_healerhold_share != 0.06923076923076923 * default_bud_pool()
    )
    assert sue_worldunit._sum_healerhold_share == 0.100000001 * default_bud_pool()
    assert oregon_idea._healerhold_ratio == 0.38461538615384616
    assert mon_idea._healerhold_ratio == 0.3076923069230769
    assert tue_idea._healerhold_ratio == 0.3076923069230769

    # WHEN
    sue_worldunit.edit_idea_attr(week_road, healerhold=sue_healerhold)
    week_idea = sue_worldunit.get_idea_obj(week_road)
    print(f"{week_idea._label=} {week_idea._problem_bool=} {week_idea._bud_ratio=}")
    sue_worldunit.calc_world_metrics()
    # THEN
    # display_ideatree(sue_world, "Econ").show()
    assert sue_worldunit._sum_healerhold_share == 0
    assert oregon_idea._healerhold_ratio == 0
    assert mon_idea._healerhold_ratio == 0
    assert tue_idea._healerhold_ratio == 0


def test_WorldUnit_calc_world_metrics_CorrectlySets_econ_dict_v1():
    # ESTABLISH
    sue_worldunit = get_world_with_4_levels_and_2reasons()
    sue_worldunit.add_charunit("Sue")
    sue_worldunit.calc_world_metrics()
    nation_road = sue_worldunit.make_l1_road("nation-state")
    usa_road = sue_worldunit.make_road(nation_road, "USA")
    oregon_road = sue_worldunit.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({"Sue"})
    sue_worldunit.edit_idea_attr(
        oregon_road, problem_bool=True, healerhold=sue_healerhold
    )
    assert len(sue_worldunit._econ_dict) == 0
    assert sue_worldunit._econ_dict.get(oregon_road) is None

    # WHEN
    sue_worldunit.calc_world_metrics()
    # THEN
    assert len(sue_worldunit._econ_dict) == 1
    assert sue_worldunit._econ_dict.get(oregon_road) != None

    # WHEN
    week_road = sue_worldunit.make_l1_road("weekdays")
    sue_worldunit.edit_idea_attr(week_road, problem_bool=True)
    mon_road = sue_worldunit.make_road(week_road, "Monday")
    sue_worldunit.edit_idea_attr(mon_road, healerhold=sue_healerhold)
    # mon_idea = sue_worldunit.get_idea_obj(mon_road)
    # print(f"{mon_idea._problem_bool=} {mon_idea._bud_ratio=}")
    sue_worldunit.calc_world_metrics()
    # THEN
    assert len(sue_worldunit._econ_dict) == 2
    assert sue_worldunit._econ_dict.get(oregon_road) != None
    assert sue_worldunit._econ_dict.get(mon_road) != None

    # WHEN
    tue_road = sue_worldunit.make_road(week_road, "Tuesday")
    sue_worldunit.edit_idea_attr(tue_road, healerhold=sue_healerhold)
    # tue_idea = sue_worldunit.get_idea_obj(tue_road)
    # print(f"{tue_idea._problem_bool=} {tue_idea._bud_ratio=}")
    # sat_road = sue_worldunit.make_road(week_road, "Saturday")
    # sat_idea = sue_worldunit.get_idea_obj(sat_road)
    # print(f"{sat_idea._problem_bool=} {sat_idea._bud_ratio=}")
    sue_worldunit.calc_world_metrics()

    # THEN
    assert len(sue_worldunit._econ_dict) == 3
    assert sue_worldunit._econ_dict.get(oregon_road) != None
    assert sue_worldunit._econ_dict.get(mon_road) != None
    assert sue_worldunit._econ_dict.get(tue_road) != None

    # WHEN
    sue_worldunit.edit_idea_attr(week_road, healerhold=sue_healerhold)
    week_idea = sue_worldunit.get_idea_obj(week_road)
    print(f"{week_idea._label=} {week_idea._problem_bool=} {week_idea._bud_ratio=}")
    sue_worldunit.calc_world_metrics()
    # THEN
    # display_ideatree(sue_world, "Econ").show()
    assert len(sue_worldunit._econ_dict) == 0
    assert sue_worldunit._econ_dict == {}


# def test_world_metrics_CorrectlySets_healers_dict():
#     # ESTABLISH
#     sue_text = "Sue"
#     bob_text = "Bob"
#     sue_worldunit = get_world_with_4_levels_and_2reasons()
#     sue_worldunit.add_charunit(sue_text)
#     sue_worldunit.add_charunit(bob_text)
#     assert sue_worldunit._healers_dict == {}

#     # WHEN
#     sue_worldunit.calc_world_metrics()
#     # THEN
#     assert sue_worldunit._healers_dict == {}

#     # ESTABLISH
#     nation_road = sue_worldunit.make_l1_road("nation-state")
#     usa_road = sue_worldunit.make_road(nation_road, "USA")
#     oregon_road = sue_worldunit.make_road(usa_road, "Oregon")
#     sue_healerhold = healerhold_shop({sue_text})
#     sue_worldunit.edit_idea_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)

#     week_road = sue_worldunit.make_l1_road("weekdays")
#     bob_healerhold = healerhold_shop({bob_text})
#     sue_worldunit.edit_idea_attr(week_road, problem_bool=True, healerhold=bob_healerhold)
#     assert sue_worldunit._healers_dict == {}

#     # WHEN
#     sue_worldunit.calc_world_metrics()

#     # THEN
#     assert len(sue_worldunit._healers_dict) == 2
#     week_idea = sue_worldunit.get_idea_obj(week_road)
#     assert sue_worldunit._healers_dict.get(bob_text) == {week_road: week_idea}
#     oregon_idea = sue_worldunit.get_idea_obj(oregon_road)
#     assert sue_worldunit._healers_dict.get(sue_text) == {oregon_road: oregon_idea}


def test_WorldUnit_calc_world_metrics_CorrectlySets_healers_dict():
    # ESTABLISH
    sue_text = "Sue"
    bob_text = "Bob"
    sue_worldunit = get_world_with_4_levels_and_2reasons()
    sue_worldunit.add_charunit(sue_text)
    sue_worldunit.add_charunit(bob_text)
    assert sue_worldunit._healers_dict == {}

    # WHEN
    sue_worldunit.calc_world_metrics()
    # THEN
    assert sue_worldunit._healers_dict == {}

    # ESTABLISH
    nation_road = sue_worldunit.make_l1_road("nation-state")
    usa_road = sue_worldunit.make_road(nation_road, "USA")
    oregon_road = sue_worldunit.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({sue_text})
    sue_worldunit.edit_idea_attr(
        oregon_road, problem_bool=True, healerhold=sue_healerhold
    )

    week_road = sue_worldunit.make_l1_road("weekdays")
    bob_healerhold = healerhold_shop({bob_text})
    sue_worldunit.edit_idea_attr(
        week_road, problem_bool=True, healerhold=bob_healerhold
    )
    assert sue_worldunit._healers_dict == {}

    # WHEN
    sue_worldunit.calc_world_metrics()

    # THEN
    assert len(sue_worldunit._healers_dict) == 2
    week_idea = sue_worldunit.get_idea_obj(week_road)
    assert sue_worldunit._healers_dict.get(bob_text) == {week_road: week_idea}
    oregon_idea = sue_worldunit.get_idea_obj(oregon_road)
    assert sue_worldunit._healers_dict.get(sue_text) == {oregon_road: oregon_idea}


def test_WorldUnit_calc_world_metrics_CorrectlySets_econs_buildable_True():
    # ESTABLISH
    sue_text = "Sue"
    bob_text = "Bob"
    sue_worldunit = get_world_with_4_levels_and_2reasons()
    sue_worldunit.add_charunit(sue_text)
    sue_worldunit.add_charunit(bob_text)
    assert sue_worldunit._econs_buildable is False

    # WHEN
    sue_worldunit.calc_world_metrics()
    # THEN
    assert sue_worldunit._econs_buildable

    # ESTABLISH
    nation_road = sue_worldunit.make_l1_road("nation-state")
    usa_road = sue_worldunit.make_road(nation_road, "USA")
    oregon_road = sue_worldunit.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({sue_text})
    sue_worldunit.edit_idea_attr(
        oregon_road, problem_bool=True, healerhold=sue_healerhold
    )

    week_road = sue_worldunit.make_l1_road("weekdays")
    bob_healerhold = healerhold_shop({bob_text})
    sue_worldunit.edit_idea_attr(
        week_road, problem_bool=True, healerhold=bob_healerhold
    )

    # WHEN
    sue_worldunit.calc_world_metrics()
    # THEN
    assert sue_worldunit._econs_buildable


def test_WorldUnit_calc_world_metrics_CorrectlySets_econs_buildable_False():
    # ESTABLISH
    sue_text = "Sue"
    bob_text = "Bob"
    sue_worldunit = get_world_with_4_levels_and_2reasons()
    sue_worldunit.add_charunit(sue_text)
    sue_worldunit.add_charunit(bob_text)
    assert sue_worldunit._econs_buildable is False

    # WHEN
    sue_worldunit.calc_world_metrics()
    # THEN
    assert sue_worldunit._econs_buildable

    # ESTABLISH
    nation_road = sue_worldunit.make_l1_road("nation-state")
    usa_road = sue_worldunit.make_road(nation_road, "USA")
    oregon_road = sue_worldunit.make_road(usa_road, "Oregon")
    bend_text = "Be/nd"
    bend_road = sue_worldunit.make_road(oregon_road, bend_text)
    sue_worldunit.add_idea(ideaunit_shop(bend_text), oregon_road)
    sue_healerhold = healerhold_shop({sue_text})
    sue_worldunit.edit_idea_attr(
        bend_road, problem_bool=True, healerhold=sue_healerhold
    )
    assert sue_worldunit._econs_buildable

    # WHEN
    sue_worldunit.calc_world_metrics()
    # THEN
    assert sue_worldunit._econs_buildable is False
