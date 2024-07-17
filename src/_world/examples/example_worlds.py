from src._instrument.file import open_file
from src._road.road import RoadUnit
from src._world.idea import ideaunit_shop
from src._world.reason_idea import (
    factunit_shop,
    premiseunit_shop,
    reasonunit_shop,
    factunit_shop,
)
from src._world.world import (
    WorldUnit,
    worldunit_shop,
    get_from_json as worldunit_get_from_json,
)
from src._world.reason_doer import doerunit_shop
from src._world.examples.world_env import get_world_examples_dir as env_dir


def world_v001() -> WorldUnit:
    return worldunit_get_from_json(open_file(env_dir(), "example_world1.json"))


def world_v001_with_large_agenda() -> WorldUnit:
    yao_world = world_v001()
    day_minute_road = yao_world.make_l1_road("day_minute")
    month_week_road = yao_world.make_l1_road("month_week")
    nations_road = yao_world.make_l1_road("Nation-States")
    mood_road = yao_world.make_l1_road("Moods")
    aaron_road = yao_world.make_l1_road("Aaron Donald things effected by him")
    year_month_road = yao_world.make_l1_road("year_month")
    season_road = yao_world.make_l1_road("Seasons")
    ced_week_road = yao_world.make_l1_road("ced_week")
    weekdays_road = yao_world.make_l1_road("weekdays")

    yao_world.set_fact(base=aaron_road, pick=aaron_road)
    yao_world.set_fact(base=ced_week_road, pick=ced_week_road, open=0, nigh=53)
    yao_world.set_fact(base=day_minute_road, pick=day_minute_road, open=0, nigh=1399)
    # yao_world.set_fact(base=internet, pick=internet)
    yao_world.set_fact(base=month_week_road, pick=month_week_road, open=0, nigh=5)
    yao_world.set_fact(base=mood_road, pick=mood_road)
    # yao_world.set_fact(base=movie, pick=movie)
    yao_world.set_fact(base=nations_road, pick=nations_road)
    yao_world.set_fact(base=season_road, pick=season_road)
    yao_world.set_fact(base=year_month_road, pick=year_month_road, open=0, nigh=12)
    # yao_world.set_fact(base=water, pick=water)
    yao_world.set_fact(base=weekdays_road, pick=weekdays_road)
    return yao_world


def world_v002() -> WorldUnit:
    bob_world = worldunit_get_from_json(open_file(env_dir(), "example_world2.json"))
    print(f"{bob_world._real_id=} {bob_world._road_delimiter=}")
    return bob_world


def get_world_with_4_levels() -> WorldUnit:
    sue_world = worldunit_shop(_owner_id="Sue", _weight=10)

    casa = "casa"
    idea_kid_casa = ideaunit_shop(casa, _weight=30, pledge=True)
    sue_world.add_l1_idea(idea_kid_casa)

    cat = "feed cat"
    idea_kid_feedcat = ideaunit_shop(cat, _weight=30, pledge=True)
    sue_world.add_l1_idea(idea_kid_feedcat)

    week_text = "weekdays"
    week_road = sue_world.make_l1_road(week_text)
    idea_kid_weekdays = ideaunit_shop(week_text, _weight=40)
    sue_world.add_l1_idea(idea_kid_weekdays)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    idea_grandkidU = ideaunit_shop(sun_text, _weight=20)
    idea_grandkidM = ideaunit_shop(mon_text, _weight=20)
    idea_grandkidT = ideaunit_shop(tue_text, _weight=20)
    idea_grandkidW = ideaunit_shop(wed_text, _weight=20)
    idea_grandkidR = ideaunit_shop(thu_text, _weight=30)
    idea_grandkidF = ideaunit_shop(fri_text, _weight=40)
    idea_grandkidA = ideaunit_shop(sat_text, _weight=50)

    sue_world.add_idea(idea_grandkidU, week_road)
    sue_world.add_idea(idea_grandkidM, week_road)
    sue_world.add_idea(idea_grandkidT, week_road)
    sue_world.add_idea(idea_grandkidW, week_road)
    sue_world.add_idea(idea_grandkidR, week_road)
    sue_world.add_idea(idea_grandkidF, week_road)
    sue_world.add_idea(idea_grandkidA, week_road)

    states_text = "nation-state"
    states_road = sue_world.make_l1_road(states_text)
    idea_kid_states = ideaunit_shop(states_text, _weight=30)
    sue_world.add_l1_idea(idea_kid_states)

    usa_text = "USA"
    usa_road = sue_world.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    idea_grandkid_usa = ideaunit_shop(usa_text, _weight=50)
    idea_grandkid_france = ideaunit_shop(france_text, _weight=50)
    idea_grandkid_brazil = ideaunit_shop(brazil_text, _weight=50)
    sue_world.add_idea(idea_grandkid_france, states_road)
    sue_world.add_idea(idea_grandkid_brazil, states_road)
    sue_world.add_idea(idea_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    idea_grandgrandkid_usa_texas = ideaunit_shop(texas_text, _weight=50)
    idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_text, _weight=50)
    sue_world.add_idea(idea_grandgrandkid_usa_texas, usa_road)
    sue_world.add_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return sue_world


def get_world_with_4_levels_and_2reasons() -> WorldUnit:
    sue_world = get_world_with_4_levels()
    week_text = "weekdays"
    week_road = sue_world.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_world.make_road(week_road, wed_text)
    week_reason = reasonunit_shop(week_road)
    week_reason.set_premise(wed_road)

    nation_text = "nation-state"
    nation_road = sue_world.make_l1_road(nation_text)
    usa_text = "USA"
    usa_road = sue_world.make_road(nation_road, usa_text)
    nation_reason = reasonunit_shop(nation_road)
    nation_reason.set_premise(usa_road)

    casa_text = "casa"
    casa_road = sue_world.make_l1_road(casa_text)
    sue_world.edit_idea_attr(road=casa_road, reason=week_reason)
    sue_world.edit_idea_attr(road=casa_road, reason=nation_reason)
    return sue_world


def get_world_with_4_levels_and_2reasons_2facts() -> WorldUnit:
    sue_world = get_world_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_world.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_world.make_road(week_road, wed_text)
    states_text = "nation-state"
    states_road = sue_world.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_world.make_road(states_road, usa_text)
    sue_world.set_fact(base=week_road, pick=wed_road)
    sue_world.set_fact(base=states_road, pick=usa_road)
    return sue_world


def get_world_with7amCleanTableReason() -> WorldUnit:
    sue_world = get_world_with_4_levels_and_2reasons_2facts()

    time_text = "timetech"
    time_road = sue_world.make_l1_road(time_text)
    time_idea = ideaunit_shop(time_text)

    day24hr_text = "24hr day"
    day24hr_road = sue_world.make_road(time_road, day24hr_text)
    day24hr_idea = ideaunit_shop(day24hr_text, _begin=0.0, _close=24.0)

    am_text = "am"
    am_road = sue_world.make_road(day24hr_road, am_text)
    pm_text = "pm"
    n1_text = "1"
    n2_text = "2"
    n3_text = "3"
    am_idea = ideaunit_shop(am_text, _begin=0, _close=12)
    pm_idea = ideaunit_shop(pm_text, _begin=12, _close=24)
    n1_idea = ideaunit_shop(n1_text, _begin=1, _close=2)
    n2_idea = ideaunit_shop(n2_text, _begin=2, _close=3)
    n3_idea = ideaunit_shop(n3_text, _begin=3, _close=4)

    sue_world.add_l1_idea(time_idea)
    sue_world.add_idea(day24hr_idea, time_road)
    sue_world.add_idea(am_idea, day24hr_road)
    sue_world.add_idea(pm_idea, day24hr_road)
    sue_world.add_idea(n1_idea, am_road)  # idea_am
    sue_world.add_idea(n2_idea, am_road)  # idea_am
    sue_world.add_idea(n3_idea, am_road)  # idea_am

    house_text = "housemanagement"
    house_road = sue_world.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = sue_world.make_road(house_road, clean_text)
    dish_text = "remove dishs"
    soap_text = "get soap"
    soap_road = sue_world.make_road(clean_road, soap_text)
    grab_text = "grab soap"
    grab_road = sue_world.make_road(soap_road, grab_text)
    house_idea = ideaunit_shop(house_text)
    clean_idea = ideaunit_shop(clean_text, pledge=True)
    dish_idea = ideaunit_shop(dish_text, pledge=True)
    soap_idea = ideaunit_shop(soap_text, pledge=True)
    grab_idea = ideaunit_shop(grab_text, pledge=True)

    sue_world.add_l1_idea(house_idea)
    sue_world.add_idea(clean_idea, house_road)
    sue_world.add_idea(dish_idea, clean_road)
    sue_world.add_idea(soap_idea, clean_road)
    sue_world.add_idea(grab_idea, soap_road)

    clean_table_7am_base = day24hr_road
    clean_table_7am_premise_road = day24hr_road
    clean_table_7am_premise_open = 7.0
    clean_table_7am_premise_nigh = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_base)
    clean_table_7am_reason.set_premise(
        premise=clean_table_7am_premise_road,
        open=clean_table_7am_premise_open,
        nigh=clean_table_7am_premise_nigh,
    )
    sue_world.edit_idea_attr(road=clean_road, reason=clean_table_7am_reason)
    casa_text = "casa"
    casa_road = sue_world.make_l1_road(casa_text)
    sue_world.edit_idea_attr(road=casa_road, reason=clean_table_7am_reason)
    return sue_world


def get_world_1Task_1CE0MinutesReason_1Fact() -> WorldUnit:
    bob_world = worldunit_shop(_owner_id="Bob", _weight=10)
    ced_min_label = "CE0_minutes"
    ced_minutes = ideaunit_shop(ced_min_label)
    ced_road = bob_world.make_l1_road(ced_min_label)
    bob_world.add_l1_idea(ced_minutes)
    mail_label = "obtain mail"
    mail_task = ideaunit_shop(mail_label, pledge=True)
    bob_world.add_l1_idea(mail_task)

    premise_x = premiseunit_shop(need=ced_road, open=80, nigh=90)
    x_task_reason = reasonunit_shop(premise_x.need, {premise_x.need: premise_x})
    mail_road = bob_world.make_l1_road(mail_label)
    bob_world.edit_idea_attr(road=mail_road, reason=x_task_reason)

    x_fact = factunit_shop(base=ced_road, pick=ced_road, open=85, nigh=95)
    # print(
    #     f"1Task_1CE0MinutesReason_1Fact 2. {len(bob_world._idearoot._kids)=} {x_fact.base=}"
    # )
    bob_world.set_fact(x_fact.base, x_fact.pick, x_fact.open, x_fact.nigh)
    # print(f"1Task_1CE0MinutesReason_1Fact 3. {len(bob_world._idearoot._kids)=}")
    return bob_world


def get_world_x1_3levels_1reason_1facts() -> WorldUnit:
    zia_world = worldunit_shop(_owner_id="Zia", _weight=10)
    shave_text = "shave"
    shave_road = zia_world.make_l1_road(shave_text)
    idea_kid_shave = ideaunit_shop(shave_text, _weight=30, pledge=True)
    zia_world.add_l1_idea(idea_kid_shave)
    week_text = "weekdays"
    week_road = zia_world.make_l1_road(week_text)
    week_idea = ideaunit_shop(week_text, _weight=40)
    zia_world.add_l1_idea(week_idea)

    sun_text = "Sunday"
    sun_road = zia_world.make_road(week_road, sun_text)
    church_text = "Church"
    church_road = zia_world.make_road(sun_road, church_text)
    mon_text = "Monday"
    mon_road = zia_world.make_road(week_road, mon_text)
    idea_grandkidU = ideaunit_shop(sun_text, _weight=20)
    idea_grandkidM = ideaunit_shop(mon_text, _weight=20)
    zia_world.add_idea(idea_grandkidU, week_road)
    zia_world.add_idea(idea_grandkidM, week_road)

    shave_reason = reasonunit_shop(week_road)
    shave_reason.set_premise(mon_road)

    zia_world.edit_idea_attr(road=shave_road, reason=shave_reason)
    zia_world.set_fact(base=week_road, pick=sun_road)
    factunit_x = factunit_shop(base=week_road, pick=church_road)
    zia_world.edit_idea_attr(road=shave_road, factunit=factunit_x)
    return zia_world


def get_world_base_time_example() -> WorldUnit:
    sue_world = worldunit_shop(_owner_id="Sue")
    sue_world.add_l1_idea(ideaunit_shop("casa"))
    return sue_world


def get_world_irrational_example() -> WorldUnit:
    # this world has no conclusive agenda because 2 pledge ideas are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active == True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active == True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_world.calc_world_metrics these should be true:
    # 1. hatter_world._irrational == True
    # 2. hatter_world._tree_traverse_count = hatter_world._max_tree_traverse

    hatter_world = worldunit_shop(_owner_id="Mad Hatter", _weight=10)
    hatter_world.set_max_tree_traverse(3)

    egg_text = "egg first"
    egg_road = hatter_world.make_l1_road(egg_text)
    hatter_world.add_l1_idea(ideaunit_shop(egg_text))

    chicken_text = "chicken first"
    chicken_road = hatter_world.make_l1_road(chicken_text)
    hatter_world.add_l1_idea(ideaunit_shop(chicken_text))

    # set egg pledge is True when chicken first is False
    hatter_world.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_idea_active_requisite=True,
    )

    # set chick pledge is True when egg first is False
    hatter_world.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_idea_active_requisite=False,
    )

    return hatter_world


def get_world_mop_example1():
    neo_world = worldunit_shop("Neo")
    casa_text = "casa"
    casa_road = neo_world.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = neo_world.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, pledge=True)
    neo_world.add_idea(floor_idea, casa_road)
    neo_world.add_l1_idea(ideaunit_shop("unimportant"))

    status_text = "cleaniness status"
    status_road = neo_world.make_road(casa_road, status_text)
    neo_world.add_idea(ideaunit_shop(status_text), casa_road)

    clean_text = "clean"
    clean_road = neo_world.make_road(status_road, clean_text)
    neo_world.add_idea(ideaunit_shop(clean_text), status_road)
    neo_world.add_idea(ideaunit_shop("very_much"), clean_road)
    neo_world.add_idea(ideaunit_shop("moderately"), clean_road)
    neo_world.add_idea(ideaunit_shop("dirty"), status_road)

    floor_reason = reasonunit_shop(status_road)
    floor_reason.set_premise(premise=status_road)
    neo_world.edit_idea_attr(road=floor_road, reason=floor_reason)
    return neo_world


def get_world_laundry_example1() -> WorldUnit:
    amos_text = "Amos"
    amos_world = worldunit_shop(_owner_id=amos_text)
    cali_text = "Cali"
    amos_world.add_charunit(amos_text)
    amos_world.add_charunit(cali_text)

    casa_text = "casa"
    basket_text = "laundry basket status"
    b_full_text = "full"
    b_smel_text = "smelly"
    b_bare_text = "bare"
    b_fine_text = "fine"
    b_half_text = "half full"
    do_laundry_text = "do_laundry"
    casa_road = amos_world.make_l1_road(casa_text)
    basket_road = amos_world.make_road(casa_road, basket_text)
    b_full_road = amos_world.make_road(basket_road, b_full_text)
    b_smel_road = amos_world.make_road(basket_road, b_smel_text)
    laundry_task_road = amos_world.make_road(casa_road, do_laundry_text)
    amos_world.add_l1_idea(ideaunit_shop(casa_text))
    amos_world.add_idea(ideaunit_shop(basket_text), casa_road)
    amos_world.add_idea(ideaunit_shop(b_full_text), basket_road)
    amos_world.add_idea(ideaunit_shop(b_smel_text), basket_road)
    amos_world.add_idea(ideaunit_shop(b_bare_text), basket_road)
    amos_world.add_idea(ideaunit_shop(b_fine_text), basket_road)
    amos_world.add_idea(ideaunit_shop(b_half_text), basket_road)
    amos_world.add_idea(ideaunit_shop(do_laundry_text, pledge=True), casa_road)

    # laundry requirement
    amos_world.edit_idea_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_full_road
    )
    # laundry requirement
    amos_world.edit_idea_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_smel_road
    )
    cali_doerunit = doerunit_shop()
    cali_doerunit.set_lobbyhold(cali_text)
    amos_world.edit_idea_attr(road=laundry_task_road, doerunit=cali_doerunit)
    # print(f"{basket_road=}")
    # print(f"{amos_world._real_id=}")
    amos_world.set_fact(base=basket_road, pick=b_full_road)

    return amos_world


def get_world_with_tuesday_cleaning_task() -> WorldUnit:
    bob_world = worldunit_shop("Bob")
    bob_world.set_time_hreg_ideas(7)

    casa_text = "casa"
    casa_road = bob_world.make_l1_road(casa_text)
    laundry_text = "do_laundry"
    laundry_road = bob_world.make_road(casa_road, laundry_text)
    chill_text = "chill"
    chill_road = bob_world.make_road(casa_road, chill_text)
    bob_world.add_l1_idea(ideaunit_shop(casa_text))
    jajatime_road = bob_world.make_road(bob_world.make_l1_road("time"), "jajatime")
    bob_world.set_fact(jajatime_road, jajatime_road, 1064131200, 1064136133)

    bob_world.add_idea(ideaunit_shop(laundry_text, pledge=True), casa_road)
    bob_world.edit_idea_attr(
        road=laundry_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=5760.0,
        reason_premise_nigh=5760.0,
        reason_premise_divisor=10080.0,
    )
    bob_world.add_idea(ideaunit_shop(chill_text, pledge=True), casa_road)
    bob_world.edit_idea_attr(
        road=chill_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=5760.0,
        reason_premise_nigh=7160.0,
        reason_premise_divisor=10080.0,
    )
    # # print(f"{bob_world._idearoot._factunits.values()=}")
    # laundry_reasonunit = bob_world.get_idea_obj(laundry_road).get_reasonunit(
    #     jajatime_road
    # )
    # laundry_premise = laundry_reasonunit.get_premise(jajatime_road)
    # # print(f"{laundry_reasonunit.base=} {laundry_premise=}")
    # bob_world.calc_world_metrics()
    # for x_ideaunit in bob_world._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    # print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    # print(f"{x_ideaunit._kids.keys()=}")
    # jaja_factheir = x_ideaunit._factheirs.get(jajatime_road)
    # print(f"{jaja_factheir.open % 10080=}")
    # print(f"{jaja_factheir.nigh % 10080=}")

    # print(f"{bob_world.get_agenda_dict().keys()=}")

    return bob_world


# class YR:
def from_list_get_active(
    road: RoadUnit, idea_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_idea = None

    active_true_count = 0
    active_false_count = 0
    for idea in idea_dict.values():
        if idea.get_road() == road:
            temp_idea = idea
            print(
                f"searched for IdeaUnit {temp_idea.get_road()} found {temp_idea._active=}"
            )

        if idea._active:
            active_true_count += 1
        elif idea._active is False:
            active_false_count += 1

    active = temp_idea._active
    print(
        f"Set active: {idea._label=} {active} {active_true_count=} {active_false_count=}"
    )

    if asse_bool in {True, False}:
        if active != asse_bool:
            yr_elucidation(temp_idea)

        assert active == asse_bool
    else:
        yr_elucidation(temp_idea)
    return active


def yr_print_idea_base_info(idea, filter: bool):
    for l in idea._reasonheirs.values():
        if l._status == filter:
            print(
                f"  ReasonHeir '{l.base}' Base LH:{l._status} W:{len(l.premises)}"  # \t_task {l._task}"
            )
            if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
                yr_print_fact(
                    lh_base=l.base,
                    lh_status=l._status,
                    premises=l.premises,
                    factheirs=idea._factheirs,
                )


def yr_elucidation(idea):
    str1 = f"'{yr_d(idea._parent_road)}' idea"
    str2 = f" has ReasonU:{yr_x(idea._reasonunits)} LH:{yr_x(idea._reasonheirs)}"
    str3 = f" {str(type(idea))}"
    str4 = " "
    if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
        str3 = f" Facts:{yr_x(idea._factheirs)} Status: {idea._active}"

        print(f"\n{str1}{str2}{str3}")
        hh_wo_matched_reason = []
        for hh in idea._factheirs.values():
            hh_wo_matched_reason = []
            try:
                idea._reasonheirs[hh.base]
            except Exception:
                hh_wo_matched_reason.append(hh.base)

        for base in hh_wo_matched_reason:
            print(f"Facts that don't matter to this Idea: {base}")

    # if idea._reasonunits != None:
    #     for lu in idea._reasonunits.values():
    #         print(f"  ReasonUnit   '{lu.base}' premises: {len(lu.premises)} ")
    if idea._reasonheirs != None:
        filter_x = True
        yr_print_idea_base_info(idea=idea, filter=True)

        filter_x = False
        print("\nReasons that failed:")

        for l in idea._reasonheirs.values():
            if l._status == filter_x:
                print(
                    f"  ReasonHeir '{l.base}' Base LH:{l._status} W:{len(l.premises)}"  # \t_task {l._task}"
                )
                if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
                    yr_print_fact(
                        lh_base=l.base,
                        lh_status=l._status,
                        premises=l.premises,
                        factheirs=idea._factheirs,
                    )
                print("")
    # print(idea._factheirs)
    # print(f"{(idea._factheirs != None)=}")
    # print(f"{len(idea._factheirs)=} ")

    print("")


def yr_print_fact(lh_base, lh_status, premises, factheirs):
    for ww in premises.values():
        ww_open = ""
        ww_open = f"\topen:{ww.open}" if ww.open != None else ""
        ww_nigh = ""
        ww_nigh = f"\tnigh:{ww.nigh}" if ww.nigh != None else ""
        ww_task = f" Task: {ww._task}"
        hh_open = ""
        hh_nigh = ""
        hh_pick = ""
        print(
            f"\t    '{lh_base}' Premise LH:{lh_status} W:{ww._status}\tneed:{ww.need}{ww_open}{ww_nigh}"
        )

        for hh in factheirs.values():
            if hh.base == lh_base:
                if hh.open != None:
                    hh_open = f"\topen:{hh.open}"
                if hh.nigh != None:
                    hh_nigh = f"\tnigh:{hh.nigh}"
                hh_pick = hh.pick
                # if hh_pick != "":
                print(
                    f"\t    '{hh.base}' Fact LH:{lh_status} W:{ww._status}\tFact:{hh_pick}{hh_open}{hh_nigh}"
                )
        if hh_pick == "":
            print(f"\t    Base: No Fact")


def yr_d(self):
    return "no road" if self is None else self[self.find(",") + 1 :]


def yr_x(self):
    return 0 if self is None else len(self)
