from src._instrument.file import open_file
from src._road.road import RoadUnit
from src.bud.idea import ideaunit_shop
from src.bud.reason_idea import factunit_shop, reasonunit_shop
from src.bud.bud import (
    BudUnit,
    budunit_shop,
    get_from_json as budunit_get_from_json,
)
from src.bud.reason_doer import doerunit_shop
from src.bud.examples.bud_env import get_bud_examples_dir as env_dir


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
    yao_bud.set_fact(ced_week_road, ced_week_road, open=0, nigh=53)
    yao_bud.set_fact(day_minute_road, day_minute_road, open=0, nigh=1399)
    # yao_bud.set_fact(internet, internet)
    yao_bud.set_fact(month_week_road, month_week_road, open=0, nigh=5)
    yao_bud.set_fact(mood_road, mood_road)
    # yao_bud.set_fact(movie, movie)
    yao_bud.set_fact(nations_road, nations_road)
    yao_bud.set_fact(season_road, season_road)
    yao_bud.set_fact(year_month_road, year_month_road, open=0, nigh=12)
    # yao_bud.set_fact(water, water)
    yao_bud.set_fact(weekdays_road, weekdays_road)
    return yao_bud


def budunit_v002() -> BudUnit:
    bob_bud = budunit_get_from_json(open_file(env_dir(), "example_bud2.json"))
    print(f"{bob_bud._real_id=} {bob_bud._road_delimiter=}")
    return bob_bud


def get_budunit_with_4_levels() -> BudUnit:
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    sue_bud.set_l1_idea(ideaunit_shop(casa_text, _mass=30, pledge=True))
    cat_text = "cat have dinner"
    sue_bud.set_l1_idea(ideaunit_shop(cat_text, _mass=30, pledge=True))

    week_text = "weekdays"
    week_road = sue_bud.make_l1_road(week_text)
    idea_kid_weekdays = ideaunit_shop(week_text, _mass=40)
    sue_bud.set_l1_idea(idea_kid_weekdays)
    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"
    sue_bud.set_idea(ideaunit_shop(sun_text, _mass=20), week_road)
    sue_bud.set_idea(ideaunit_shop(mon_text, _mass=20), week_road)
    sue_bud.set_idea(ideaunit_shop(tue_text, _mass=20), week_road)
    sue_bud.set_idea(ideaunit_shop(wed_text, _mass=20), week_road)
    sue_bud.set_idea(ideaunit_shop(thu_text, _mass=30), week_road)
    sue_bud.set_idea(ideaunit_shop(fri_text, _mass=40), week_road)
    sue_bud.set_idea(ideaunit_shop(sat_text, _mass=50), week_road)

    states_text = "nation-state"
    states_road = sue_bud.make_l1_road(states_text)
    idea_kid_states = ideaunit_shop(states_text, _mass=30)
    sue_bud.set_l1_idea(idea_kid_states)
    usa_text = "USA"
    usa_road = sue_bud.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    idea_grandkid_usa = ideaunit_shop(usa_text, _mass=50)
    idea_grandkid_france = ideaunit_shop(france_text, _mass=50)
    idea_grandkid_brazil = ideaunit_shop(brazil_text, _mass=50)
    sue_bud.set_idea(idea_grandkid_france, states_road)
    sue_bud.set_idea(idea_grandkid_brazil, states_road)
    sue_bud.set_idea(idea_grandkid_usa, states_road)
    texas_text = "Texas"
    oregon_text = "Oregon"
    idea_grandgrandkid_usa_texas = ideaunit_shop(texas_text, _mass=50)
    idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_text, _mass=50)
    sue_bud.set_idea(idea_grandgrandkid_usa_texas, usa_road)
    sue_bud.set_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return sue_bud


def get_budunit_with_4_levels_and_2reasons() -> BudUnit:
    sue_bud = get_budunit_with_4_levels()
    week_text = "weekdays"
    week_road = sue_bud.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_bud.make_road(week_road, wed_text)
    week_reason = reasonunit_shop(week_road)
    week_reason.set_premise(wed_road)

    nation_text = "nation-state"
    nation_road = sue_bud.make_l1_road(nation_text)
    usa_text = "USA"
    usa_road = sue_bud.make_road(nation_road, usa_text)
    nation_reason = reasonunit_shop(nation_road)
    nation_reason.set_premise(usa_road)

    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    sue_bud.edit_idea_attr(road=casa_road, reason=week_reason)
    sue_bud.edit_idea_attr(road=casa_road, reason=nation_reason)
    return sue_bud


def get_budunit_with_4_levels_and_2reasons_2facts() -> BudUnit:
    sue_bud = get_budunit_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_bud.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_bud.make_road(week_road, wed_text)
    states_text = "nation-state"
    states_road = sue_bud.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_bud.make_road(states_road, usa_text)
    sue_bud.set_fact(base=week_road, pick=wed_road)
    sue_bud.set_fact(base=states_road, pick=usa_road)
    return sue_bud


def get_budunit_with7amCleanTableReason() -> BudUnit:
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()

    time_text = "timetech"
    time_road = sue_bud.make_l1_road(time_text)
    time_idea = ideaunit_shop(time_text)

    day24hr_text = "24hr day"
    day24hr_road = sue_bud.make_road(time_road, day24hr_text)
    day24hr_idea = ideaunit_shop(day24hr_text, _begin=0.0, _close=24.0)

    am_text = "am"
    am_road = sue_bud.make_road(day24hr_road, am_text)
    pm_text = "pm"
    n1_text = "1"
    n2_text = "2"
    n3_text = "3"
    am_idea = ideaunit_shop(am_text, _gogo_want=0, _stop_want=12)
    pm_idea = ideaunit_shop(pm_text, _gogo_want=12, _stop_want=24)
    n1_idea = ideaunit_shop(n1_text, _gogo_want=1, _stop_want=2)
    n2_idea = ideaunit_shop(n2_text, _gogo_want=2, _stop_want=3)
    n3_idea = ideaunit_shop(n3_text, _gogo_want=3, _stop_want=4)

    sue_bud.set_l1_idea(time_idea)
    sue_bud.set_idea(day24hr_idea, time_road)
    sue_bud.set_idea(am_idea, day24hr_road)
    sue_bud.set_idea(pm_idea, day24hr_road)
    sue_bud.set_idea(n1_idea, am_road)  # idea_am
    sue_bud.set_idea(n2_idea, am_road)  # idea_am
    sue_bud.set_idea(n3_idea, am_road)  # idea_am

    house_text = "housemanagement"
    house_road = sue_bud.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = sue_bud.make_road(house_road, clean_text)
    dish_text = "remove dishs"
    soap_text = "get soap"
    soap_road = sue_bud.make_road(clean_road, soap_text)
    grab_text = "grab soap"
    grab_road = sue_bud.make_road(soap_road, grab_text)
    house_idea = ideaunit_shop(house_text)
    clean_idea = ideaunit_shop(clean_text, pledge=True)
    dish_idea = ideaunit_shop(dish_text, pledge=True)
    soap_idea = ideaunit_shop(soap_text, pledge=True)
    grab_idea = ideaunit_shop(grab_text, pledge=True)

    sue_bud.set_l1_idea(house_idea)
    sue_bud.set_idea(clean_idea, house_road)
    sue_bud.set_idea(dish_idea, clean_road)
    sue_bud.set_idea(soap_idea, clean_road)
    sue_bud.set_idea(grab_idea, soap_road)

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
    sue_bud.edit_idea_attr(clean_road, reason=clean_table_7am_reason)
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    sue_bud.edit_idea_attr(casa_road, reason=clean_table_7am_reason)
    return sue_bud


def get_budunit_1Task_1CE0MinutesReason_1Fact() -> BudUnit:
    yao_bud = budunit_shop("Yao")
    hour_min_text = "hour"
    hour_min_idea = ideaunit_shop(hour_min_text)
    hour_road = yao_bud.make_l1_road(hour_min_text)
    hour_reasonunit = reasonunit_shop(hour_road)
    hour_reasonunit.set_premise(hour_road, open=80, nigh=90)
    yao_bud.set_l1_idea(hour_min_idea)
    yao_bud.set_fact(hour_road, hour_road, 85, 95)
    mail_text = "obtain mail"
    mail_road = yao_bud.make_l1_road(mail_text)
    mail_idea = ideaunit_shop(mail_text, pledge=True)
    yao_bud.set_l1_idea(mail_idea)
    yao_bud.edit_idea_attr(mail_road, reason=hour_reasonunit)
    return yao_bud


def get_budunit_x1_3levels_1reason_1facts() -> BudUnit:
    tiger_text = "tiger"
    zia_bud = budunit_shop("Zia", _real_id=tiger_text)
    shave_text = "shave"
    shave_road = zia_bud.make_l1_road(shave_text)
    idea_kid_shave = ideaunit_shop(shave_text, _mass=30, pledge=True)
    zia_bud.set_l1_idea(idea_kid_shave)
    week_text = "weekdays"
    week_road = zia_bud.make_l1_road(week_text)
    week_idea = ideaunit_shop(week_text, _mass=40)
    zia_bud.set_l1_idea(week_idea)

    sun_text = "Sunday"
    sun_road = zia_bud.make_road(week_road, sun_text)
    church_text = "Church"
    church_road = zia_bud.make_road(sun_road, church_text)
    mon_text = "Monday"
    mon_road = zia_bud.make_road(week_road, mon_text)
    idea_grandkidU = ideaunit_shop(sun_text, _mass=20)
    idea_grandkidM = ideaunit_shop(mon_text, _mass=20)
    zia_bud.set_idea(idea_grandkidU, week_road)
    zia_bud.set_idea(idea_grandkidM, week_road)

    shave_reason = reasonunit_shop(week_road)
    shave_reason.set_premise(mon_road)

    zia_bud.edit_idea_attr(road=shave_road, reason=shave_reason)
    zia_bud.set_fact(base=week_road, pick=sun_road)
    factunit_x = factunit_shop(base=week_road, pick=church_road)
    zia_bud.edit_idea_attr(road=shave_road, factunit=factunit_x)
    return zia_bud


def get_budunit_base_time_example() -> BudUnit:
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
    # 2. hatter_bud._tree_traverse_count = hatter_bud._max_tree_traverse

    hatter_bud = budunit_shop("Mad Hatter")
    hatter_bud.set_max_tree_traverse(3)

    egg_text = "egg first"
    egg_road = hatter_bud.make_l1_road(egg_text)
    hatter_bud.set_l1_idea(ideaunit_shop(egg_text))

    chicken_text = "chicken first"
    chicken_road = hatter_bud.make_l1_road(chicken_text)
    hatter_bud.set_l1_idea(ideaunit_shop(chicken_text))

    # set egg pledge is True when chicken first is False
    hatter_bud.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_idea_active_requisite=True,
    )

    # set chick pledge is True when egg first is False
    hatter_bud.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_idea_active_requisite=False,
    )

    return hatter_bud


def get_budunit_mop_example1():
    sue_bud = budunit_shop("Sue")
    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = sue_bud.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, pledge=True)
    sue_bud.set_idea(floor_idea, casa_road)
    sue_bud.set_l1_idea(ideaunit_shop("unimportant"))

    status_text = "cleaniness status"
    status_road = sue_bud.make_road(casa_road, status_text)
    sue_bud.set_idea(ideaunit_shop(status_text), casa_road)

    clean_text = "clean"
    clean_road = sue_bud.make_road(status_road, clean_text)
    sue_bud.set_idea(ideaunit_shop(clean_text), status_road)
    sue_bud.set_idea(ideaunit_shop("very_much"), clean_road)
    sue_bud.set_idea(ideaunit_shop("moderately"), clean_road)
    sue_bud.set_idea(ideaunit_shop("dirty"), status_road)

    floor_reason = reasonunit_shop(status_road)
    floor_reason.set_premise(premise=status_road)
    sue_bud.edit_idea_attr(road=floor_road, reason=floor_reason)
    return sue_bud


def get_budunit_laundry_example1() -> BudUnit:
    amos_text = "Amos"
    amos_bud = budunit_shop(amos_text)
    cali_text = "Cali"
    amos_bud.add_acctunit(amos_text)
    amos_bud.add_acctunit(cali_text)

    casa_text = "casa"
    basket_text = "laundry basket status"
    b_full_text = "full"
    b_smel_text = "smelly"
    b_bare_text = "bare"
    b_fine_text = "fine"
    b_half_text = "half full"
    do_laundry_text = "do_laundry"
    casa_road = amos_bud.make_l1_road(casa_text)
    basket_road = amos_bud.make_road(casa_road, basket_text)
    b_full_road = amos_bud.make_road(basket_road, b_full_text)
    b_smel_road = amos_bud.make_road(basket_road, b_smel_text)
    laundry_task_road = amos_bud.make_road(casa_road, do_laundry_text)
    amos_bud.set_l1_idea(ideaunit_shop(casa_text))
    amos_bud.set_idea(ideaunit_shop(basket_text), casa_road)
    amos_bud.set_idea(ideaunit_shop(b_full_text), basket_road)
    amos_bud.set_idea(ideaunit_shop(b_smel_text), basket_road)
    amos_bud.set_idea(ideaunit_shop(b_bare_text), basket_road)
    amos_bud.set_idea(ideaunit_shop(b_fine_text), basket_road)
    amos_bud.set_idea(ideaunit_shop(b_half_text), basket_road)
    amos_bud.set_idea(ideaunit_shop(do_laundry_text, pledge=True), casa_road)

    # laundry requirement
    amos_bud.edit_idea_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_full_road
    )
    # laundry requirement
    amos_bud.edit_idea_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_smel_road
    )
    cali_doerunit = doerunit_shop()
    cali_doerunit.set_grouphold(cali_text)
    amos_bud.edit_idea_attr(road=laundry_task_road, doerunit=cali_doerunit)
    # print(f"{basket_road=}")
    # print(f"{amos_bud._real_id=}")
    amos_bud.set_fact(base=basket_road, pick=b_full_road)

    return amos_bud


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

    # if idea._reasonunits is not None:
    #     for lu in idea._reasonunits.values():
    #         print(f"  ReasonUnit   '{lu.base}' premises: {len(lu.premises)} ")
    if idea._reasonheirs is not None:
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
    # print(f"{(idea._factheirs is not None)=}")
    # print(f"{len(idea._factheirs)=} ")

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
                if hh.open is not None:
                    hh_open = f"\topen:{hh.open}"
                if hh.nigh is not None:
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
