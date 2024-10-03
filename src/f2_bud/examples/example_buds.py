from src.f0_instrument.file import open_file
from src.f1_road.road import RoadUnit
from src.f2_bud.item import itemunit_shop
from src.f2_bud.reason_item import factunit_shop, reasonunit_shop
from src.f2_bud.bud import (
    BudUnit,
    budunit_shop,
    get_from_json as budunit_get_from_json,
)
from src.f2_bud.reason_team import teamunit_shop
from src.f2_bud.examples.bud_env import get_bud_examples_dir as env_dir


def budunit_v001() -> BudUnit:
    return budunit_get_from_json(open_file(env_dir(), "example_bud1.json"))


def budunit_v001_with_large_agenda() -> BudUnit:
    yao_bud = budunit_v001()
    day_minute_road = yao_bud.make_l1_road("day_minute")
    month_week_road = yao_bud.make_l1_road("month_week")
    nations_road = yao_bud.make_l1_road("Nation-States")
    mood_road = yao_bud.make_l1_road("Moods")
    aaron_road = yao_bud.make_l1_road("Aaron Donald things effected by him")
    year_month_road = yao_bud.make_l1_road("year_month")
    season_road = yao_bud.make_l1_road("Seasons")
    ced_week_road = yao_bud.make_l1_road("ced_week")
    weekdays_road = yao_bud.make_l1_road("weekdays")

    yao_bud.set_fact(aaron_road, aaron_road)
    yao_bud.set_fact(ced_week_road, ced_week_road, fopen=0, fnigh=53)
    yao_bud.set_fact(day_minute_road, day_minute_road, fopen=0, fnigh=1399)
    # yao_bud.set_fact(interweb, interweb)
    yao_bud.set_fact(month_week_road, month_week_road, fopen=0, fnigh=5)
    yao_bud.set_fact(mood_road, mood_road)
    # yao_bud.set_fact(movie, movie)
    yao_bud.set_fact(nations_road, nations_road)
    yao_bud.set_fact(season_road, season_road)
    yao_bud.set_fact(year_month_road, year_month_road, fopen=0, fnigh=12)
    # yao_bud.set_fact(water, water)
    yao_bud.set_fact(weekdays_road, weekdays_road)
    return yao_bud


def budunit_v002() -> BudUnit:
    bob_bud = budunit_get_from_json(open_file(env_dir(), "example_bud2.json"))
    print(f"{bob_bud._fiscal_id=} {bob_bud._road_delimiter=}")
    return bob_bud


def get_budunit_with_4_levels() -> BudUnit:
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    sue_bud.set_l1_item(itemunit_shop(casa_str, mass=30, pledge=True))
    cat_str = "cat have dinner"
    sue_bud.set_l1_item(itemunit_shop(cat_str, mass=30, pledge=True))

    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    item_kid_weekdays = itemunit_shop(week_str, mass=40)
    sue_bud.set_l1_item(item_kid_weekdays)
    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sue_bud.set_item(itemunit_shop(sun_str, mass=20), week_road)
    sue_bud.set_item(itemunit_shop(mon_str, mass=20), week_road)
    sue_bud.set_item(itemunit_shop(tue_str, mass=20), week_road)
    sue_bud.set_item(itemunit_shop(wed_str, mass=20), week_road)
    sue_bud.set_item(itemunit_shop(thu_str, mass=30), week_road)
    sue_bud.set_item(itemunit_shop(fri_str, mass=40), week_road)
    sue_bud.set_item(itemunit_shop(sat_str, mass=50), week_road)

    states_str = "nation-state"
    states_road = sue_bud.make_l1_road(states_str)
    item_kid_states = itemunit_shop(states_str, mass=30)
    sue_bud.set_l1_item(item_kid_states)
    usa_str = "USA"
    usa_road = sue_bud.make_road(states_road, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    item_grandkid_usa = itemunit_shop(usa_str, mass=50)
    item_grandkid_france = itemunit_shop(france_str, mass=50)
    item_grandkid_brazil = itemunit_shop(brazil_str, mass=50)
    sue_bud.set_item(item_grandkid_france, states_road)
    sue_bud.set_item(item_grandkid_brazil, states_road)
    sue_bud.set_item(item_grandkid_usa, states_road)
    texas_str = "Texas"
    oregon_str = "Oregon"
    item_grandgrandkid_usa_texas = itemunit_shop(texas_str, mass=50)
    item_grandgrandkid_usa_oregon = itemunit_shop(oregon_str, mass=50)
    sue_bud.set_item(item_grandgrandkid_usa_texas, usa_road)
    sue_bud.set_item(item_grandgrandkid_usa_oregon, usa_road)
    return sue_bud


def get_budunit_with_4_levels_and_2reasons() -> BudUnit:
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    wed_str = "Wednesday"
    wed_road = sue_bud.make_road(week_road, wed_str)
    week_reason = reasonunit_shop(week_road)
    week_reason.set_premise(wed_road)

    nation_str = "nation-state"
    nation_road = sue_bud.make_l1_road(nation_str)
    usa_str = "USA"
    usa_road = sue_bud.make_road(nation_road, usa_str)
    nation_reason = reasonunit_shop(nation_road)
    nation_reason.set_premise(usa_road)

    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.edit_item_attr(road=casa_road, reason=week_reason)
    sue_bud.edit_item_attr(road=casa_road, reason=nation_reason)
    return sue_bud


def get_budunit_with_4_levels_and_2reasons_2facts() -> BudUnit:
    sue_bud = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    wed_str = "Wednesday"
    wed_road = sue_bud.make_road(week_road, wed_str)
    states_str = "nation-state"
    states_road = sue_bud.make_l1_road(states_str)
    usa_str = "USA"
    usa_road = sue_bud.make_road(states_road, usa_str)
    sue_bud.set_fact(base=week_road, pick=wed_road)
    sue_bud.set_fact(base=states_road, pick=usa_road)
    return sue_bud


def get_budunit_with7amCleanTableReason() -> BudUnit:
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()

    time_str = "timetech"
    time_road = sue_bud.make_l1_road(time_str)
    time_item = itemunit_shop(time_str)

    day24hr_str = "24hr day"
    day24hr_road = sue_bud.make_road(time_road, day24hr_str)
    day24hr_item = itemunit_shop(day24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_road = sue_bud.make_road(day24hr_road, am_str)
    pm_str = "pm"
    n1_str = "1"
    n2_str = "2"
    n3_str = "3"
    am_item = itemunit_shop(am_str, gogo_want=0, stop_want=12)
    pm_item = itemunit_shop(pm_str, gogo_want=12, stop_want=24)
    n1_item = itemunit_shop(n1_str, gogo_want=1, stop_want=2)
    n2_item = itemunit_shop(n2_str, gogo_want=2, stop_want=3)
    n3_item = itemunit_shop(n3_str, gogo_want=3, stop_want=4)

    sue_bud.set_l1_item(time_item)
    sue_bud.set_item(day24hr_item, time_road)
    sue_bud.set_item(am_item, day24hr_road)
    sue_bud.set_item(pm_item, day24hr_road)
    sue_bud.set_item(n1_item, am_road)  # item_am
    sue_bud.set_item(n2_item, am_road)  # item_am
    sue_bud.set_item(n3_item, am_road)  # item_am

    house_str = "housemanagement"
    house_road = sue_bud.make_l1_road(house_str)
    clean_str = "clean table"
    clean_road = sue_bud.make_road(house_road, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_road = sue_bud.make_road(clean_road, soap_str)
    grab_str = "grab soap"
    grab_road = sue_bud.make_road(soap_road, grab_str)
    house_item = itemunit_shop(house_str)
    clean_item = itemunit_shop(clean_str, pledge=True)
    dish_item = itemunit_shop(dish_str, pledge=True)
    soap_item = itemunit_shop(soap_str, pledge=True)
    grab_item = itemunit_shop(grab_str, pledge=True)

    sue_bud.set_l1_item(house_item)
    sue_bud.set_item(clean_item, house_road)
    sue_bud.set_item(dish_item, clean_road)
    sue_bud.set_item(soap_item, clean_road)
    sue_bud.set_item(grab_item, soap_road)

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
    sue_bud.edit_item_attr(clean_road, reason=clean_table_7am_reason)
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    sue_bud.edit_item_attr(casa_road, reason=clean_table_7am_reason)
    return sue_bud


def get_budunit_1Task_1CE0MinutesReason_1Fact() -> BudUnit:
    yao_bud = budunit_shop("Yao")
    hour_min_str = "hour"
    hour_min_item = itemunit_shop(hour_min_str)
    hour_road = yao_bud.make_l1_road(hour_min_str)
    hour_reasonunit = reasonunit_shop(hour_road)
    hour_reasonunit.set_premise(hour_road, open=80, nigh=90)
    yao_bud.set_l1_item(hour_min_item)
    yao_bud.set_fact(hour_road, hour_road, 85, 95)
    mail_str = "obtain mail"
    mail_road = yao_bud.make_l1_road(mail_str)
    mail_item = itemunit_shop(mail_str, pledge=True)
    yao_bud.set_l1_item(mail_item)
    yao_bud.edit_item_attr(mail_road, reason=hour_reasonunit)
    return yao_bud


def get_budunit_x1_3levels_1reason_1facts() -> BudUnit:
    tiger_str = "tiger"
    zia_bud = budunit_shop("Zia", _fiscal_id=tiger_str)
    shave_str = "shave"
    shave_road = zia_bud.make_l1_road(shave_str)
    item_kid_shave = itemunit_shop(shave_str, mass=30, pledge=True)
    zia_bud.set_l1_item(item_kid_shave)
    week_str = "weekdays"
    week_road = zia_bud.make_l1_road(week_str)
    week_item = itemunit_shop(week_str, mass=40)
    zia_bud.set_l1_item(week_item)

    sun_str = "Sunday"
    sun_road = zia_bud.make_road(week_road, sun_str)
    church_str = "Church"
    church_road = zia_bud.make_road(sun_road, church_str)
    mon_str = "Monday"
    mon_road = zia_bud.make_road(week_road, mon_str)
    item_grandkidU = itemunit_shop(sun_str, mass=20)
    item_grandkidM = itemunit_shop(mon_str, mass=20)
    zia_bud.set_item(item_grandkidU, week_road)
    zia_bud.set_item(item_grandkidM, week_road)

    shave_reason = reasonunit_shop(week_road)
    shave_reason.set_premise(mon_road)

    zia_bud.edit_item_attr(road=shave_road, reason=shave_reason)
    zia_bud.set_fact(base=week_road, pick=sun_road)
    factunit_x = factunit_shop(base=week_road, pick=church_road)
    zia_bud.edit_item_attr(road=shave_road, factunit=factunit_x)
    return zia_bud


def get_budunit_base_time_example() -> BudUnit:
    sue_bud = budunit_shop("Sue")
    sue_bud.set_l1_item(itemunit_shop("casa"))
    return sue_bud


def get_budunit_irrational_example() -> BudUnit:
    # this bud has no conclusive agenda because 2 pledge items are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active is True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active is True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_bud.settle_bud these should be true:
    # 1. hatter_bud._irrational is True
    # 2. hatter_bud._tree_traverse_count = hatter_bud.max_tree_traverse

    hatter_bud = budunit_shop("Mad Hatter")
    hatter_bud.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_road = hatter_bud.make_l1_road(egg_str)
    hatter_bud.set_l1_item(itemunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_road = hatter_bud.make_l1_road(chicken_str)
    hatter_bud.set_l1_item(itemunit_shop(chicken_str))

    # set egg pledge is True when chicken first is False
    hatter_bud.edit_item_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_item_active_requisite=True,
    )

    # set chick pledge is True when egg first is False
    hatter_bud.edit_item_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_item_active_requisite=False,
    )

    return hatter_bud


def get_budunit_mop_example1():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    floor_str = "mop floor"
    floor_road = sue_bud.make_road(casa_road, floor_str)
    floor_item = itemunit_shop(floor_str, pledge=True)
    sue_bud.set_item(floor_item, casa_road)
    sue_bud.set_l1_item(itemunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_road = sue_bud.make_road(casa_road, status_str)
    sue_bud.set_item(itemunit_shop(status_str), casa_road)

    clean_str = "clean"
    clean_road = sue_bud.make_road(status_road, clean_str)
    sue_bud.set_item(itemunit_shop(clean_str), status_road)
    sue_bud.set_item(itemunit_shop("very_much"), clean_road)
    sue_bud.set_item(itemunit_shop("moderately"), clean_road)
    sue_bud.set_item(itemunit_shop("dirty"), status_road)

    floor_reason = reasonunit_shop(status_road)
    floor_reason.set_premise(premise=status_road)
    sue_bud.edit_item_attr(road=floor_road, reason=floor_reason)
    return sue_bud


def get_budunit_laundry_example1() -> BudUnit:
    amos_str = "Amos"
    amos_bud = budunit_shop(amos_str)
    cali_str = "Cali"
    amos_bud.add_acctunit(amos_str)
    amos_bud.add_acctunit(cali_str)

    casa_str = "casa"
    basket_str = "laundry basket status"
    b_full_str = "full"
    b_smel_str = "smelly"
    b_bare_str = "bare"
    b_fine_str = "fine"
    b_half_str = "half full"
    do_laundry_str = "do_laundry"
    casa_road = amos_bud.make_l1_road(casa_str)
    basket_road = amos_bud.make_road(casa_road, basket_str)
    b_full_road = amos_bud.make_road(basket_road, b_full_str)
    b_smel_road = amos_bud.make_road(basket_road, b_smel_str)
    laundry_task_road = amos_bud.make_road(casa_road, do_laundry_str)
    amos_bud.set_l1_item(itemunit_shop(casa_str))
    amos_bud.set_item(itemunit_shop(basket_str), casa_road)
    amos_bud.set_item(itemunit_shop(b_full_str), basket_road)
    amos_bud.set_item(itemunit_shop(b_smel_str), basket_road)
    amos_bud.set_item(itemunit_shop(b_bare_str), basket_road)
    amos_bud.set_item(itemunit_shop(b_fine_str), basket_road)
    amos_bud.set_item(itemunit_shop(b_half_str), basket_road)
    amos_bud.set_item(itemunit_shop(do_laundry_str, pledge=True), casa_road)

    # laundry requirement
    amos_bud.edit_item_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_full_road
    )
    # laundry requirement
    amos_bud.edit_item_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_smel_road
    )
    cali_teamunit = teamunit_shop()
    cali_teamunit.set_teamlink(cali_str)
    amos_bud.edit_item_attr(road=laundry_task_road, teamunit=cali_teamunit)
    # print(f"{basket_road=}")
    # print(f"{amos_bud._fiscal_id=}")
    amos_bud.set_fact(base=basket_road, pick=b_full_road)

    return amos_bud


# class YR:
def from_list_get_active(
    road: RoadUnit, item_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_item = None

    active_true_count = 0
    active_false_count = 0
    for item in item_dict.values():
        if item.get_road() == road:
            temp_item = item
            print(
                f"searched for ItemUnit {temp_item.get_road()} found {temp_item._active=}"
            )

        if item._active:
            active_true_count += 1
        elif item._active is False:
            active_false_count += 1

    active = temp_item._active
    print(
        f"Set active: {item._label=} {active} {active_true_count=} {active_false_count=}"
    )

    if asse_bool in {True, False}:
        if active != asse_bool:
            yr_elucidation(temp_item)

        assert active == asse_bool
    else:
        yr_elucidation(temp_item)
    return active


def yr_print_item_base_info(item, filter: bool):
    for l in item._reasonheirs.values():
        if l._status == filter:
            print(
                f"  ReasonHeir '{l.base}' Base LH:{l._status} W:{len(l.premises)}"  # \t_task {l._task}"
            )
            if str(type(item)).find(".item.ItemUnit'>") > 0:
                yr_print_fact(
                    lh_base=l.base,
                    lh_status=l._status,
                    premises=l.premises,
                    factheirs=item._factheirs,
                )


def yr_elucidation(item):
    str1 = f"'{yr_d(item._parent_road)}' item"
    str2 = f" has ReasonU:{yr_x(item.reasonunits)} LH:{yr_x(item._reasonheirs)}"
    str3 = f" {str(type(item))}"
    str4 = " "
    if str(type(item)).find(".item.ItemUnit'>") > 0:
        str3 = f" Facts:{yr_x(item._factheirs)} Status: {item._active}"

        print(f"\n{str1}{str2}{str3}")
        hh_wo_matched_reason = []
        for hh in item._factheirs.values():
            hh_wo_matched_reason = []
            try:
                item._reasonheirs[hh.base]
            except Exception:
                hh_wo_matched_reason.append(hh.base)

        for base in hh_wo_matched_reason:
            print(f"Facts that don't matter to this Item: {base}")

    # if item.reasonunits is not None:
    #     for lu in item.reasonunits.values():
    #         print(f"  ReasonUnit   '{lu.base}' premises: {len(lu.premises)} ")
    if item._reasonheirs is not None:
        filter_x = True
        yr_print_item_base_info(item=item, filter=True)

        filter_x = False
        print("\nReasons that failed:")

        for l in item._reasonheirs.values():
            if l._status == filter_x:
                print(
                    f"  ReasonHeir '{l.base}' Base LH:{l._status} W:{len(l.premises)}"  # \t_task {l._task}"
                )
                if str(type(item)).find(".item.ItemUnit'>") > 0:
                    yr_print_fact(
                        lh_base=l.base,
                        lh_status=l._status,
                        premises=l.premises,
                        factheirs=item._factheirs,
                    )
                print("")
    # print(item._factheirs)
    # print(f"{(item._factheirs is not None)=}")
    # print(f"{len(item._factheirs)=} ")

    print("")


def yr_print_fact(lh_base, lh_status, premises, factheirs):
    for ww in premises.values():
        ww_open = ""
        ww_open = f"\topen:{ww.open}" if ww.open is not None else ""
        ww_nigh = ""
        ww_nigh = f"\tnigh:{ww.nigh}" if ww.nigh is not None else ""
        ww_task = f" Task: {ww._task}"
        hh_open = ""
        hh_nigh = ""
        hh_pick = ""
        print(
            f"\t    '{lh_base}' Premise LH:{lh_status} W:{ww._status}\tneed:{ww.need}{ww_open}{ww_nigh}"
        )

        for hh in factheirs.values():
            if hh.base == lh_base:
                if hh.fopen is not None:
                    hh_open = f"\topen:{hh.fopen}"
                if hh.fnigh is not None:
                    hh_nigh = f"\tnigh:{hh.fnigh}"
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
