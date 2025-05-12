from src.a00_data_toolbox.file_toolbox import open_file, create_path
from src.a01_way_logic.way import WayStr
from src.a05_idea_logic.idea import ideaunit_shop
from src.a04_reason_logic.reason_idea import factunit_shop, reasonunit_shop
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
    sue_bud.set_l1_idea(ideaunit_shop(casa_str, mass=30, pledge=True))
    cat_str = "cat have dinner"
    sue_bud.set_l1_idea(ideaunit_shop(cat_str, mass=30, pledge=True))

    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    idea_kid_weekdays = ideaunit_shop(week_str, mass=40)
    sue_bud.set_l1_idea(idea_kid_weekdays)
    sun_str = "Sunday"
    mon_str = "Monday"
    tue_str = "Tuesday"
    wed_str = "Wednesday"
    thu_str = "Thursday"
    fri_str = "Friday"
    sat_str = "Saturday"
    sue_bud.set_idea(ideaunit_shop(sun_str, mass=20), week_way)
    sue_bud.set_idea(ideaunit_shop(mon_str, mass=20), week_way)
    sue_bud.set_idea(ideaunit_shop(tue_str, mass=20), week_way)
    sue_bud.set_idea(ideaunit_shop(wed_str, mass=20), week_way)
    sue_bud.set_idea(ideaunit_shop(thu_str, mass=30), week_way)
    sue_bud.set_idea(ideaunit_shop(fri_str, mass=40), week_way)
    sue_bud.set_idea(ideaunit_shop(sat_str, mass=50), week_way)

    states_str = "nation-state"
    states_way = sue_bud.make_l1_way(states_str)
    idea_kid_states = ideaunit_shop(states_str, mass=30)
    sue_bud.set_l1_idea(idea_kid_states)
    usa_str = "USA"
    usa_way = sue_bud.make_way(states_way, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    idea_grandkid_usa = ideaunit_shop(usa_str, mass=50)
    idea_grandkid_france = ideaunit_shop(france_str, mass=50)
    idea_grandkid_brazil = ideaunit_shop(brazil_str, mass=50)
    sue_bud.set_idea(idea_grandkid_france, states_way)
    sue_bud.set_idea(idea_grandkid_brazil, states_way)
    sue_bud.set_idea(idea_grandkid_usa, states_way)
    texas_str = "Texas"
    oregon_str = "Oregon"
    idea_grandgrandkid_usa_texas = ideaunit_shop(texas_str, mass=50)
    idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_str, mass=50)
    sue_bud.set_idea(idea_grandgrandkid_usa_texas, usa_way)
    sue_bud.set_idea(idea_grandgrandkid_usa_oregon, usa_way)
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
    sue_bud.edit_idea_attr(casa_way, reason=week_reason)
    sue_bud.edit_idea_attr(casa_way, reason=nation_reason)
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
    sue_bud.add_fact(fcontext=week_way, fbranch=wed_way)
    sue_bud.add_fact(fcontext=states_way, fbranch=usa_way)
    return sue_bud


def get_budunit_with7amCleanTableReason() -> BudUnit:
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()

    time_str = "timetech"
    time_way = sue_bud.make_l1_way(time_str)
    time_idea = ideaunit_shop(time_str)

    day24hr_str = "24hr day"
    day24hr_way = sue_bud.make_way(time_way, day24hr_str)
    day24hr_idea = ideaunit_shop(day24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_way = sue_bud.make_way(day24hr_way, am_str)
    pm_str = "pm"
    n1_str = "1"
    n2_str = "2"
    n3_str = "3"
    am_idea = ideaunit_shop(am_str, gogo_want=0, stop_want=12)
    pm_idea = ideaunit_shop(pm_str, gogo_want=12, stop_want=24)
    n1_idea = ideaunit_shop(n1_str, gogo_want=1, stop_want=2)
    n2_idea = ideaunit_shop(n2_str, gogo_want=2, stop_want=3)
    n3_idea = ideaunit_shop(n3_str, gogo_want=3, stop_want=4)

    sue_bud.set_l1_idea(time_idea)
    sue_bud.set_idea(day24hr_idea, time_way)
    sue_bud.set_idea(am_idea, day24hr_way)
    sue_bud.set_idea(pm_idea, day24hr_way)
    sue_bud.set_idea(n1_idea, am_way)  # idea_am
    sue_bud.set_idea(n2_idea, am_way)  # idea_am
    sue_bud.set_idea(n3_idea, am_way)  # idea_am

    house_str = "housemanagement"
    house_way = sue_bud.make_l1_way(house_str)
    clean_str = "clean table"
    clean_way = sue_bud.make_way(house_way, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_way = sue_bud.make_way(clean_way, soap_str)
    grab_str = "grab soap"
    grab_way = sue_bud.make_way(soap_way, grab_str)
    house_idea = ideaunit_shop(house_str)
    clean_idea = ideaunit_shop(clean_str, pledge=True)
    dish_idea = ideaunit_shop(dish_str, pledge=True)
    soap_idea = ideaunit_shop(soap_str, pledge=True)
    grab_idea = ideaunit_shop(grab_str, pledge=True)

    sue_bud.set_l1_idea(house_idea)
    sue_bud.set_idea(clean_idea, house_way)
    sue_bud.set_idea(dish_idea, clean_way)
    sue_bud.set_idea(soap_idea, clean_way)
    sue_bud.set_idea(grab_idea, soap_way)

    clean_table_7am_rcontext = day24hr_way
    clean_table_7am_premise_way = day24hr_way
    clean_table_7am_popen = 7.0
    clean_table_7am_pnigh = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_rcontext)
    clean_table_7am_reason.set_premise(
        premise=clean_table_7am_premise_way,
        popen=clean_table_7am_popen,
        pnigh=clean_table_7am_pnigh,
    )
    sue_bud.edit_idea_attr(clean_way, reason=clean_table_7am_reason)
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    sue_bud.edit_idea_attr(casa_way, reason=clean_table_7am_reason)
    return sue_bud


def get_budunit_1Task_1CE0MinutesReason_1Fact() -> BudUnit:
    yao_bud = budunit_shop("Yao")
    hour_min_str = "hour"
    hour_min_idea = ideaunit_shop(hour_min_str)
    hour_way = yao_bud.make_l1_way(hour_min_str)
    hour_reasonunit = reasonunit_shop(hour_way)
    hour_reasonunit.set_premise(hour_way, popen=80, pnigh=90)
    yao_bud.set_l1_idea(hour_min_idea)
    yao_bud.add_fact(hour_way, hour_way, 85, 95)
    mail_str = "obtain mail"
    mail_way = yao_bud.make_l1_way(mail_str)
    mail_idea = ideaunit_shop(mail_str, pledge=True)
    yao_bud.set_l1_idea(mail_idea)
    yao_bud.edit_idea_attr(mail_way, reason=hour_reasonunit)
    return yao_bud


def get_budunit_x1_3levels_1reason_1facts() -> BudUnit:
    tiger_str = "tiger"
    zia_bud = budunit_shop("Zia", fisc_tag=tiger_str)
    shave_str = "shave"
    shave_way = zia_bud.make_l1_way(shave_str)
    idea_kid_shave = ideaunit_shop(shave_str, mass=30, pledge=True)
    zia_bud.set_l1_idea(idea_kid_shave)
    week_str = "weekdays"
    week_way = zia_bud.make_l1_way(week_str)
    week_idea = ideaunit_shop(week_str, mass=40)
    zia_bud.set_l1_idea(week_idea)

    sun_str = "Sunday"
    sun_way = zia_bud.make_way(week_way, sun_str)
    church_str = "Church"
    church_way = zia_bud.make_way(sun_way, church_str)
    mon_str = "Monday"
    mon_way = zia_bud.make_way(week_way, mon_str)
    idea_grandkidU = ideaunit_shop(sun_str, mass=20)
    idea_grandkidM = ideaunit_shop(mon_str, mass=20)
    zia_bud.set_idea(idea_grandkidU, week_way)
    zia_bud.set_idea(idea_grandkidM, week_way)

    shave_reason = reasonunit_shop(week_way)
    shave_reason.set_premise(mon_way)

    zia_bud.edit_idea_attr(shave_way, reason=shave_reason)
    zia_bud.add_fact(fcontext=week_way, fbranch=sun_way)
    x_factunit = factunit_shop(fcontext=week_way, fbranch=church_way)
    zia_bud.edit_idea_attr(shave_way, factunit=x_factunit)
    return zia_bud


def get_budunit_rcontext_time_example() -> BudUnit:
    sue_bud = budunit_shop("Sue")
    sue_bud.set_l1_idea(ideaunit_shop("casa"))
    return sue_bud


def get_budunit_irrational_example() -> BudUnit:
    # this bud has no conclusive agenda because 2 pledge ideas are in contradiction
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
    hatter_bud.set_l1_idea(ideaunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_way = hatter_bud.make_l1_way(chicken_str)
    hatter_bud.set_l1_idea(ideaunit_shop(chicken_str))

    # set egg pledge is True when chicken first is False
    hatter_bud.edit_idea_attr(
        egg_way,
        pledge=True,
        reason_rcontext=chicken_way,
        reason_rcontext_idea_active_requisite=True,
    )

    # set chick pledge is True when egg first is False
    hatter_bud.edit_idea_attr(
        chicken_way,
        pledge=True,
        reason_rcontext=egg_way,
        reason_rcontext_idea_active_requisite=False,
    )

    return hatter_bud


def get_mop_with_reason_budunit_example1():
    sue_bud = budunit_shop("Sue")
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    floor_str = "mop floor"
    floor_way = sue_bud.make_way(casa_way, floor_str)
    floor_idea = ideaunit_shop(floor_str, pledge=True)
    sue_bud.set_idea(floor_idea, casa_way)
    sue_bud.set_l1_idea(ideaunit_shop("unimportant"))

    status_str = "cleaniness status"
    status_way = sue_bud.make_way(casa_way, status_str)
    sue_bud.set_idea(ideaunit_shop(status_str), casa_way)

    clean_str = "clean"
    clean_way = sue_bud.make_way(status_way, clean_str)
    sue_bud.set_idea(ideaunit_shop(clean_str), status_way)
    sue_bud.set_idea(ideaunit_shop("very_much"), clean_way)
    sue_bud.set_idea(ideaunit_shop("moderately"), clean_way)
    sue_bud.set_idea(ideaunit_shop("dirty"), status_way)

    floor_reason = reasonunit_shop(status_way)
    floor_reason.set_premise(premise=status_way)
    sue_bud.edit_idea_attr(floor_way, reason=floor_reason)
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
    amos_bud.set_l1_idea(ideaunit_shop(casa_str))
    amos_bud.set_idea(ideaunit_shop(basket_str), casa_way)
    amos_bud.set_idea(ideaunit_shop(b_full_str), basket_way)
    amos_bud.set_idea(ideaunit_shop(b_smel_str), basket_way)
    amos_bud.set_idea(ideaunit_shop(b_bare_str), basket_way)
    amos_bud.set_idea(ideaunit_shop(b_fine_str), basket_way)
    amos_bud.set_idea(ideaunit_shop(b_half_str), basket_way)
    amos_bud.set_idea(ideaunit_shop(do_laundry_str, pledge=True), casa_way)

    # laundry requirement
    amos_bud.edit_idea_attr(
        laundry_task_way, reason_rcontext=basket_way, reason_premise=b_full_way
    )
    # laundry requirement
    amos_bud.edit_idea_attr(
        laundry_task_way, reason_rcontext=basket_way, reason_premise=b_smel_way
    )
    cali_teamunit = teamunit_shop()
    cali_teamunit.set_teamlink(cali_str)
    amos_bud.edit_idea_attr(laundry_task_way, teamunit=cali_teamunit)
    amos_bud.add_fact(fcontext=basket_way, fbranch=b_full_way)

    return amos_bud


# class YR:
def from_list_get_active(way: WayStr, idea_dict: dict, asse_bool: bool = None) -> bool:
    active = None
    temp_idea = None

    active_true_count = 0
    active_false_count = 0
    for idea in idea_dict.values():
        if idea.get_idea_way() == way:
            temp_idea = idea
            print(f"s for IdeaUnit {temp_idea.get_idea_way()}  {temp_idea._active=}")

        if idea._active:
            active_true_count += 1
        elif idea._active is False:
            active_false_count += 1

    active = temp_idea._active
    print(
        f"Set active: {idea.idea_tag=} {active} {active_true_count=} {active_false_count=}"
    )

    return active
