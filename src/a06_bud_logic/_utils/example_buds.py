from src.a00_data_toolbox.file_toolbox import open_file, create_path
from src.a01_way_logic.way import WayUnit
from src.a05_item_logic.item import itemunit_shop
from src.a04_reason_logic.reason_item import factunit_shop, reasonunit_shop
from src.a06_bud_logic.bud import (
    BudUnit,
    budunit_shop,
    get_from_json as budunit_get_from_json,
)
from src.a04_reason_logic.reason_team import teamunit_shop
from src.a06_bud_logic._utils.env_a06 import get_bud_examples_dir as env_dir
from os.path import exists as os_path_exists


def budunit_v001() -> BudUnit:
    bud1_path = "src/a06_bud_logic/_utils/example_bud1.json"
    bud1_json = open_file(bud1_path)
    return budunit_get_from_json(bud1_json)


def budunit_v001_with_large_agenda() -> BudUnit:
    yao_bud = budunit_v001()
    day_minute_way = yao_bud.make_l1_way("day_minute")
    month_week_way = yao_bud.make_l1_way("month_week")
    nations_way = yao_bud.make_l1_way("Nation-States")
    mood_way = yao_bud.make_l1_way("Moods")
    aaron_way = yao_bud.make_l1_way("Aaron Donald objects effected by him")
    year_month_way = yao_bud.make_l1_way("year_month")
    season_way = yao_bud.make_l1_way("Seasons")
    ced_week_way = yao_bud.make_l1_way("ced_week")
    weekdays_way = yao_bud.make_l1_way("weekdays")

    yao_bud.add_fact(aaron_way, aaron_way)
    yao_bud.add_fact(ced_week_way, ced_week_way, fopen=0, fnigh=53)
    yao_bud.add_fact(day_minute_way, day_minute_way, fopen=0, fnigh=1399)
    # yao_bud.add_fact(interweb, interweb)
    yao_bud.add_fact(month_week_way, month_week_way, fopen=0, fnigh=5)
    yao_bud.add_fact(mood_way, mood_way)
    # yao_bud.add_fact(movie, movie)
    yao_bud.add_fact(nations_way, nations_way)
    yao_bud.add_fact(season_way, season_way)
    yao_bud.add_fact(year_month_way, year_month_way, fopen=0, fnigh=12)
    # yao_bud.add_fact(water, water)
    yao_bud.add_fact(weekdays_way, weekdays_way)
    return yao_bud


def budunit_v002() -> BudUnit:
    bud2_path = "src/a06_bud_logic/_utils/example_bud2.json"
    return budunit_get_from_json(open_file(bud2_path))


def get_budunit_with_4_levels() -> BudUnit:
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    sue_bud.set_l1_item(itemunit_shop(casa_str, mass=30, pledge=True))
    cat_str = "cat have dinner"
    sue_bud.set_l1_item(itemunit_shop(cat_str, mass=30, pledge=True))

    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    item_kid_weekdays = itemunit_shop(week_str, mass=40)
    sue_bud.set_l1_item(item_kid_weekdays)
    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sue_bud.set_item(itemunit_shop(sun_str, mass=20), week_way)
    sue_bud.set_item(itemunit_shop(mon_str, mass=20), week_way)
    sue_bud.set_item(itemunit_shop(tue_str, mass=20), week_way)
    sue_bud.set_item(itemunit_shop(wed_str, mass=20), week_way)
    sue_bud.set_item(itemunit_shop(thu_str, mass=30), week_way)
    sue_bud.set_item(itemunit_shop(fri_str, mass=40), week_way)
    sue_bud.set_item(itemunit_shop(sat_str, mass=50), week_way)

    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    item_kid_states = itemunit_shop(states_str, mass=30)
    sue_bud.set_l1_item(item_kid_states)
    usa_str = "USA"
    usa_way = sue_bud.make_way(states_way, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    item_grandkid_usa = itemunit_shop(usa_str, mass=50)
    item_grandkid_france = itemunit_shop(france_str, mass=50)
    item_grandkid_brazil = itemunit_shop(brazil_str, mass=50)
    sue_bud.set_item(item_grandkid_france, states_way)
    sue_bud.set_item(item_grandkid_brazil, states_way)
    sue_bud.set_item(item_grandkid_usa, states_way)
    texas_str = "Texas"
    oregon_str = "Oregon"
    item_grandgrandkid_usa_texas = itemunit_shop(texas_str, mass=50)
    item_grandgrandkid_usa_oregon = itemunit_shop(oregon_str, mass=50)
    sue_bud.set_item(item_grandgrandkid_usa_texas, usa_way)
    sue_bud.set_item(item_grandgrandkid_usa_oregon, usa_way)
    return sue_bud


def get_budunit_with_4_levels_and_2reasons() -> BudUnit:
    sue_bud = get_budunit_with_4_levels()
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(week_way, wed_str)
    week_reason = reasonunit_shop(week_way)
    week_reason.set_premise(wed_way)

    nation_str = "nation-state"
    nation_way = sue_bud.make_l1_way(nation_str)
    usa_str = "USA"
    usa_way = sue_bud.make_way(nation_way, usa_str)
    nation_reason = reasonunit_shop(nation_way)
    nation_reason.set_premise(usa_way)

    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    sue_bud.edit_item_attr(casa_way, reason=week_reason)
    sue_bud.edit_item_attr(casa_way, reason=nation_reason)
    return sue_bud


def get_budunit_with_4_levels_and_2reasons_2facts() -> BudUnit:
    sue_bud = get_budunit_with_4_levels_and_2reasons()
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(week_way, wed_str)
    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    usa_str = "USA"
    usa_way = sue_bud.make_way(states_way, usa_str)
    sue_bud.add_fact(fbase=week_way, fneed=wed_way)
    sue_bud.add_fact(fbase=states_way, fneed=usa_way)
    return sue_bud


def get_budunit_with7amCleanTableReason() -> BudUnit:
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()

    time_str = "timetech"
    time_way = sue_bud.make_l1_way(time_str)
    time_item = itemunit_shop(time_str)

    day24hr_str = "24hr day"
    day24hr_way = sue_bud.make_way(time_way, day24hr_str)
    day24hr_item = itemunit_shop(day24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_way = sue_bud.make_way(day24hr_way, am_str)
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
    sue_bud.set_item(day24hr_item, time_way)
    sue_bud.set_item(am_item, day24hr_way)
    sue_bud.set_item(pm_item, day24hr_way)
    sue_bud.set_item(n1_item, am_way)  # item_am
    sue_bud.set_item(n2_item, am_way)  # item_am
    sue_bud.set_item(n3_item, am_way)  # item_am

    house_str = "housemanagement"
    house_way = sue_bud.make_l1_way(house_str)
    clean_str = "clean table"
    clean_way = sue_bud.make_way(house_way, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_way = sue_bud.make_way(clean_way, soap_str)
    grab_str = "grab soap"
    grab_way = sue_bud.make_way(soap_way, grab_str)
    house_item = itemunit_shop(house_str)
    clean_item = itemunit_shop(clean_str, pledge=True)
    dish_item = itemunit_shop(dish_str, pledge=True)
    soap_item = itemunit_shop(soap_str, pledge=True)
    grab_item = itemunit_shop(grab_str, pledge=True)

    sue_bud.set_l1_item(house_item)
    sue_bud.set_item(clean_item, house_way)
    sue_bud.set_item(dish_item, clean_way)
    sue_bud.set_item(soap_item, clean_way)
    sue_bud.set_item(grab_item, soap_way)

    clean_table_7am_base = day24hr_way
    clean_table_7am_premise_way = day24hr_way
    clean_table_7am_premise_open = 7.0
    clean_table_7am_premise_nigh = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_base)
    clean_table_7am_reason.set_premise(
        premise=clean_table_7am_premise_way,
        open=clean_table_7am_premise_open,
        nigh=clean_table_7am_premise_nigh,
    )
    sue_bud.edit_item_attr(clean_way, reason=clean_table_7am_reason)
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    sue_bud.edit_item_attr(casa_way, reason=clean_table_7am_reason)
    return sue_bud


def get_budunit_1Task_1CE0MinutesReason_1Fact() -> BudUnit:
    yao_bud = budunit_shop("Yao")
    hour_min_str = "hour"
    hour_min_item = itemunit_shop(hour_min_str)
    hour_way = yao_bud.make_l1_way(hour_min_str)
    hour_reasonunit = reasonunit_shop(hour_way)
    hour_reasonunit.set_premise(hour_way, open=80, nigh=90)
    yao_bud.set_l1_item(hour_min_item)
    yao_bud.add_fact(hour_way, hour_way, 85, 95)
    mail_str = "obtain mail"
    mail_way = yao_bud.make_l1_way(mail_str)
    mail_item = itemunit_shop(mail_str, pledge=True)
    yao_bud.set_l1_item(mail_item)
    yao_bud.edit_item_attr(mail_way, reason=hour_reasonunit)
    return yao_bud


def get_budunit_x1_3levels_1reason_1facts() -> BudUnit:
    tiger_str = "tiger"
    zia_bud = budunit_shop("Zia", fisc_tag=tiger_str)
    shave_str = "shave"
    shave_way = zia_bud.make_l1_way(shave_str)
    item_kid_shave = itemunit_shop(shave_str, mass=30, pledge=True)
    zia_bud.set_l1_item(item_kid_shave)
    week_str = "weekdays"
    week_way = zia_bud.make_l1_way(week_str)
    week_item = itemunit_shop(week_str, mass=40)
    zia_bud.set_l1_item(week_item)

    sun_str = "Sunday"
    sun_way = zia_bud.make_way(week_way, sun_str)
    church_str = "Church"
    church_way = zia_bud.make_way(sun_way, church_str)
    mon_str = "Monday"
    mon_way = zia_bud.make_way(week_way, mon_str)
    item_grandkidU = itemunit_shop(sun_str, mass=20)
    item_grandkidM = itemunit_shop(mon_str, mass=20)
    zia_bud.set_item(item_grandkidU, week_way)
    zia_bud.set_item(item_grandkidM, week_way)

    shave_reason = reasonunit_shop(week_way)
    shave_reason.set_premise(mon_way)

    zia_bud.edit_item_attr(shave_way, reason=shave_reason)
    zia_bud.add_fact(fbase=week_way, fneed=sun_way)
    x_factunit = factunit_shop(fbase=week_way, fneed=church_way)
    zia_bud.edit_item_attr(shave_way, factunit=x_factunit)
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
    egg_way = hatter_bud.make_l1_way(egg_str)
    hatter_bud.set_l1_item(itemunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_way = hatter_bud.make_l1_way(chicken_str)
    hatter_bud.set_l1_item(itemunit_shop(chicken_str))

    # set egg pledge is True when chicken first is False
    hatter_bud.edit_item_attr(
        egg_way,
        pledge=True,
        reason_base=chicken_way,
        reason_base_item_active_requisite=True,
    )

    # set chick pledge is True when egg first is False
    hatter_bud.edit_item_attr(
        chicken_way,
        pledge=True,
        reason_base=egg_way,
        reason_base_item_active_requisite=False,
    )

    return hatter_bud


def get_mop_with_reason_budunit_example1():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    floor_str = "mop floor"
    floor_way = sue_bud.make_way(casa_way, floor_str)
    floor_item = itemunit_shop(floor_str, pledge=True)
    sue_bud.set_item(floor_item, casa_way)
    sue_bud.set_l1_item(itemunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_way = sue_bud.make_way(casa_way, status_str)
    sue_bud.set_item(itemunit_shop(status_str), casa_way)

    clean_str = "clean"
    clean_way = sue_bud.make_way(status_way, clean_str)
    sue_bud.set_item(itemunit_shop(clean_str), status_way)
    sue_bud.set_item(itemunit_shop("very_much"), clean_way)
    sue_bud.set_item(itemunit_shop("moderately"), clean_way)
    sue_bud.set_item(itemunit_shop("dirty"), status_way)

    floor_reason = reasonunit_shop(status_way)
    floor_reason.set_premise(premise=status_way)
    sue_bud.edit_item_attr(floor_way, reason=floor_reason)
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
    casa_way = amos_bud.make_l1_way(casa_str)
    basket_way = amos_bud.make_way(casa_way, basket_str)
    b_full_way = amos_bud.make_way(basket_way, b_full_str)
    b_smel_way = amos_bud.make_way(basket_way, b_smel_str)
    laundry_task_way = amos_bud.make_way(casa_way, do_laundry_str)
    amos_bud.set_l1_item(itemunit_shop(casa_str))
    amos_bud.set_item(itemunit_shop(basket_str), casa_way)
    amos_bud.set_item(itemunit_shop(b_full_str), basket_way)
    amos_bud.set_item(itemunit_shop(b_smel_str), basket_way)
    amos_bud.set_item(itemunit_shop(b_bare_str), basket_way)
    amos_bud.set_item(itemunit_shop(b_fine_str), basket_way)
    amos_bud.set_item(itemunit_shop(b_half_str), basket_way)
    amos_bud.set_item(itemunit_shop(do_laundry_str, pledge=True), casa_way)

    # laundry requirement
    amos_bud.edit_item_attr(
        laundry_task_way, reason_base=basket_way, reason_premise=b_full_way
    )
    # laundry requirement
    amos_bud.edit_item_attr(
        laundry_task_way, reason_base=basket_way, reason_premise=b_smel_way
    )
    cali_teamunit = teamunit_shop()
    cali_teamunit.set_teamlink(cali_str)
    amos_bud.edit_item_attr(laundry_task_way, teamunit=cali_teamunit)
    amos_bud.add_fact(fbase=basket_way, fneed=b_full_way)

    return amos_bud


# class YR:
def from_list_get_active(way: WayUnit, item_dict: dict, asse_bool: bool = None) -> bool:
    active = None
    temp_item = None

    active_true_count = 0
    active_false_count = 0
    for item in item_dict.values():
        if item.get_item_way() == way:
            temp_item = item
            print(f"s for ItemUnit {temp_item.get_item_way()}  {temp_item._active=}")

        if item._active:
            active_true_count += 1
        elif item._active is False:
            active_false_count += 1

    active = temp_item._active
    print(
        f"Set active: {item.item_tag=} {active} {active_true_count=} {active_false_count=}"
    )

    return active
