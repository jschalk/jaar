from src._prime.road import RoadUnit
from src.agenda.idea import ideaunit_shop
from src.agenda.required_idea import (
    acptfactunit_shop,
    sufffactunit_shop,
    requiredunit_shop,
    acptfactunit_shop,
)
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agenda_get_from_json,
)
from src.agenda.required_assign import assigned_unit_shop
from src.tools.file import open_file
from src.agenda.examples.agenda_env import agenda_env


def agenda_v001() -> AgendaUnit:
    return agenda_get_from_json(
        open_file(dest_dir=agenda_env(), file_name="example_agenda1.json")
    )


def agenda_v001_with_large_intent() -> AgendaUnit:
    x_agenda = agenda_v001()
    day_minute_text = "day_minute"
    day_minute_road = x_agenda.make_l1_road(day_minute_text)
    month_week_text = "month_week"
    month_week_road = x_agenda.make_l1_road(month_week_text)
    nations_text = "Nation-States"
    nations_road = x_agenda.make_l1_road(nations_text)
    mood_text = "Moods"
    mood_road = x_agenda.make_l1_road(mood_text)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = x_agenda.make_l1_road(aaron_text)
    # internet_text = "Internet"
    # internet_road = x_agenda.make_road(x_agenda._economy_id,internet_text)
    year_month_text = "year_month"
    year_month_road = x_agenda.make_l1_road(year_month_text)
    season_text = "Seasons"
    season_road = x_agenda.make_l1_road(season_text)
    ced_week_text = "ced_week"
    ced_week_road = x_agenda.make_l1_road(ced_week_text)
    # water_text = "WaterBeing"
    # water_road = x_agenda.make_road(x_agenda._economy_id,water_text)
    weekdays_text = "weekdays"
    weekdays_road = x_agenda.make_l1_road(weekdays_text)
    # movie_text = "No Movie playing"
    # movie_road = x_agenda.make_road(x_agenda._economy_id,movie_text)

    x_agenda.set_acptfact(base=aaron_road, pick=aaron_road)
    x_agenda.set_acptfact(base=ced_week_road, pick=ced_week_road, open=0, nigh=53)
    x_agenda.set_acptfact(base=day_minute_road, pick=day_minute_road, open=0, nigh=1399)
    # x_agenda.set_acptfact(base=internet, pick=internet)
    x_agenda.set_acptfact(base=month_week_road, pick=month_week_road, open=0, nigh=5)
    x_agenda.set_acptfact(base=mood_road, pick=mood_road)
    # x_agenda.set_acptfact(base=movie, pick=movie)
    x_agenda.set_acptfact(base=nations_road, pick=nations_road)
    x_agenda.set_acptfact(base=season_road, pick=season_road)
    x_agenda.set_acptfact(base=year_month_road, pick=year_month_road, open=0, nigh=12)
    # x_agenda.set_acptfact(base=water, pick=water)
    x_agenda.set_acptfact(base=weekdays_road, pick=weekdays_road)

    return x_agenda


def agenda_v002() -> AgendaUnit:
    x_agenda = agenda_get_from_json(
        open_file(
            dest_dir=agenda_env(),
            file_name="example_agenda2.json",
        )
    )
    print(f"{x_agenda._economy_id=} {x_agenda._road_delimiter=}")
    return x_agenda


def get_agenda_with_4_levels() -> AgendaUnit:
    sue_agenda = agendaunit_shop(_healer="Sue", _weight=10)
    # print(f"{sue_agenda._auto_output_to_public=}")

    work = "work"
    idea_kid_work = ideaunit_shop(work, _weight=30, promise=True)
    sue_agenda.add_idea(idea_kid_work, parent_road=sue_agenda._economy_id)

    cat = "feed cat"
    idea_kid_feedcat = ideaunit_shop(cat, _weight=30, promise=True)
    sue_agenda.add_idea(idea_kid_feedcat, parent_road=sue_agenda._economy_id)

    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    idea_kid_weekdays = ideaunit_shop(week_text, _weight=40)
    sue_agenda.add_idea(idea_kid_weekdays, parent_road=sue_agenda._economy_id)

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

    sue_agenda.add_idea(idea_grandkidU, parent_road=week_road)
    sue_agenda.add_idea(idea_grandkidM, parent_road=week_road)
    sue_agenda.add_idea(idea_grandkidT, parent_road=week_road)
    sue_agenda.add_idea(idea_grandkidW, parent_road=week_road)
    sue_agenda.add_idea(idea_grandkidR, parent_road=week_road)
    sue_agenda.add_idea(idea_grandkidF, parent_road=week_road)
    sue_agenda.add_idea(idea_grandkidA, parent_road=week_road)

    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    idea_kid_states = ideaunit_shop(states_text, _weight=30)
    sue_agenda.add_idea(idea_kid_states, parent_road=sue_agenda._economy_id)

    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    idea_grandkid_usa = ideaunit_shop(usa_text, _weight=50)
    idea_grandkid_france = ideaunit_shop(france_text, _weight=50)
    idea_grandkid_brazil = ideaunit_shop(brazil_text, _weight=50)
    sue_agenda.add_idea(idea_grandkid_france, states_road)
    sue_agenda.add_idea(idea_grandkid_brazil, states_road)
    sue_agenda.add_idea(idea_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    idea_grandgrandkid_usa_texas = ideaunit_shop(texas_text, _weight=50)
    idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_text, _weight=50)
    sue_agenda.add_idea(idea_grandgrandkid_usa_texas, usa_road)
    sue_agenda.add_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return sue_agenda


def get_agenda_with_4_levels_and_2requireds() -> AgendaUnit:
    sue_agenda = get_agenda_with_4_levels()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_agenda.make_road(week_road, wed_text)
    week_required = requiredunit_shop(week_road)
    week_required.set_sufffact(wed_road)

    nation_text = "nation-state"
    nation_road = sue_agenda.make_l1_road(nation_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(nation_road, usa_text)
    nation_required = requiredunit_shop(nation_road)
    nation_required.set_sufffact(usa_road)

    work_text = "work"
    work_road = sue_agenda.make_l1_road(work_text)
    sue_agenda.edit_idea_attr(road=work_road, required=week_required)
    sue_agenda.edit_idea_attr(road=work_road, required=nation_required)
    return sue_agenda


def get_agenda_with_4_levels_and_2requireds_2acptfacts() -> AgendaUnit:
    sue_agenda = get_agenda_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_agenda.make_road(week_road, wed_text)
    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    sue_agenda.set_acptfact(base=week_road, pick=wed_road)
    sue_agenda.set_acptfact(base=states_road, pick=usa_road)
    return sue_agenda


def get_agenda_with7amCleanTableRequired() -> AgendaUnit:
    sue_agenda = get_agenda_with_4_levels_and_2requireds_2acptfacts()

    time_text = "timetech"
    time_road = sue_agenda.make_l1_road(time_text)
    time_idea = ideaunit_shop(time_text)

    day24hr_text = "24hr day"
    day24hr_road = sue_agenda.make_road(time_road, day24hr_text)
    day24hr_idea = ideaunit_shop(day24hr_text, _begin=0.0, _close=24.0)

    am_text = "am"
    am_road = sue_agenda.make_road(day24hr_road, am_text)
    pm_text = "pm"
    n1_text = "1"
    n2_text = "2"
    n3_text = "3"
    am_idea = ideaunit_shop(am_text, _begin=0, _close=12)
    pm_idea = ideaunit_shop(pm_text, _begin=12, _close=24)
    n1_idea = ideaunit_shop(n1_text, _begin=1, _close=2)
    n2_idea = ideaunit_shop(n2_text, _begin=2, _close=3)
    n3_idea = ideaunit_shop(n3_text, _begin=3, _close=4)

    sue_agenda.add_idea(time_idea, sue_agenda._economy_id)
    sue_agenda.add_idea(day24hr_idea, time_road)
    sue_agenda.add_idea(am_idea, day24hr_road)
    sue_agenda.add_idea(pm_idea, day24hr_road)
    sue_agenda.add_idea(n1_idea, am_road)  # idea_am
    sue_agenda.add_idea(n2_idea, am_road)  # idea_am
    sue_agenda.add_idea(n3_idea, am_road)  # idea_am

    house_text = "housework"
    house_road = sue_agenda.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = sue_agenda.make_road(house_road, clean_text)
    dish_text = "remove dishs"
    soap_text = "get soap"
    soap_road = sue_agenda.make_road(clean_road, soap_text)
    grab_text = "grab soap"
    grab_road = sue_agenda.make_road(soap_road, grab_text)
    house_idea = ideaunit_shop(house_text)
    clean_idea = ideaunit_shop(clean_text, promise=True)
    dish_idea = ideaunit_shop(dish_text, promise=True)
    soap_idea = ideaunit_shop(soap_text, promise=True)
    grab_idea = ideaunit_shop(grab_text, promise=True)

    sue_agenda.add_idea(house_idea, parent_road=sue_agenda._economy_id)
    sue_agenda.add_idea(clean_idea, parent_road=house_road)
    sue_agenda.add_idea(dish_idea, parent_road=clean_road)
    sue_agenda.add_idea(soap_idea, parent_road=clean_road)
    sue_agenda.add_idea(grab_idea, parent_road=soap_road)

    clean_table_7am_base = day24hr_road
    clean_table_7am_sufffact_road = day24hr_road
    clean_table_7am_sufffact_open = 7.0
    clean_table_7am_sufffact_nigh = 7.0
    clean_table_7am_required = requiredunit_shop(clean_table_7am_base)
    clean_table_7am_required.set_sufffact(
        sufffact=clean_table_7am_sufffact_road,
        open=clean_table_7am_sufffact_open,
        nigh=clean_table_7am_sufffact_nigh,
    )
    sue_agenda.edit_idea_attr(road=clean_road, required=clean_table_7am_required)
    work_text = "work"
    work_road = sue_agenda.make_l1_road(work_text)
    sue_agenda.edit_idea_attr(road=work_road, required=clean_table_7am_required)
    return sue_agenda


def get_agenda_1Task_1CE0MinutesRequired_1AcptFact() -> AgendaUnit:
    bob_agenda = agendaunit_shop(_healer="Bob", _weight=10)
    ced_min_label = "CE0_minutes"
    ced_minutes = ideaunit_shop(ced_min_label)
    ced_road = bob_agenda.make_l1_road(ced_min_label)
    bob_agenda.add_idea(ced_minutes, parent_road=bob_agenda._economy_id)
    mail_label = "obtain mail"
    mail_task = ideaunit_shop(mail_label, promise=True)
    bob_agenda.add_idea(mail_task, parent_road=bob_agenda._economy_id)

    sufffact_x = sufffactunit_shop(need=ced_road, open=80, nigh=90)
    x_task_required = requiredunit_shop(
        base=sufffact_x.need, sufffacts={sufffact_x.need: sufffact_x}
    )
    mail_road = bob_agenda.make_l1_road(mail_label)
    bob_agenda.edit_idea_attr(road=mail_road, required=x_task_required)

    x_acptfact = acptfactunit_shop(base=ced_road, pick=ced_road, open=85, nigh=95)
    # print(
    #     f"1Task_1CE0MinutesRequired_1AcptFact 2. {len(bob_agenda._idearoot._kids)=} {x_acptfact.base=}"
    # )
    bob_agenda.set_acptfact(
        base=x_acptfact.base,
        pick=x_acptfact.pick,
        open=x_acptfact.open,
        nigh=x_acptfact.nigh,
    )
    # print(f"1Task_1CE0MinutesRequired_1AcptFact 3. {len(bob_agenda._idearoot._kids)=}")

    return bob_agenda


def get_agenda_x1_3levels_1required_1acptfacts() -> AgendaUnit:
    kol_agenda = agendaunit_shop(_healer="Kol", _weight=10)
    shave_text = "shave"
    shave_road = kol_agenda.make_l1_road(shave_text)
    idea_kid_shave = ideaunit_shop(shave_text, _weight=30, promise=True)
    kol_agenda.add_idea(idea_kid_shave, parent_road=kol_agenda._economy_id)
    week_text = "weekdays"
    week_road = kol_agenda.make_l1_road(week_text)
    week_idea = ideaunit_shop(week_text, _weight=40)
    kol_agenda.add_idea(week_idea, parent_road=kol_agenda._economy_id)

    sun_text = "Sunday"
    sun_road = kol_agenda.make_road(week_road, sun_text)
    church_text = "Church"
    church_road = kol_agenda.make_road(sun_road, church_text)
    mon_text = "Monday"
    mon_road = kol_agenda.make_road(week_road, mon_text)
    idea_grandkidU = ideaunit_shop(sun_text, _weight=20)
    idea_grandkidM = ideaunit_shop(mon_text, _weight=20)
    kol_agenda.add_idea(idea_grandkidU, parent_road=week_road)
    kol_agenda.add_idea(idea_grandkidM, parent_road=week_road)

    shave_required = requiredunit_shop(week_road)
    shave_required.set_sufffact(mon_road)

    kol_agenda.edit_idea_attr(road=shave_road, required=shave_required)
    kol_agenda.set_acptfact(base=week_road, pick=sun_road)
    acptfactunit_x = acptfactunit_shop(base=week_road, pick=church_road)
    kol_agenda.edit_idea_attr(road=shave_road, acptfactunit=acptfactunit_x)
    return kol_agenda


def get_agenda_base_time_example() -> AgendaUnit:
    sue_agenda = agendaunit_shop(_healer="Sue")
    plant_idea = ideaunit_shop("plant")
    sue_agenda.add_idea(plant_idea, parent_road=sue_agenda._economy_id)
    return sue_agenda


def get_agenda_irrational_example() -> AgendaUnit:
    # this agenda has no conclusive intent because 2 promise ideas are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active_status == True, egg._active_status is set to False
    # Step 1: if egg._active_status == False, chicken._active_status is set to False
    # Step 2: if chicken._active_status == False, egg._active_status is set to True
    # Step 3: if egg._active_status == True, chicken._active_status is set to True
    # Step 4: back to step 0.
    # after hatter_agenda.set_agenda_metrics these should be true:
    # 1. hatter_agenda._irrational == True
    # 2. hatter_agenda._tree_traverse_count = hatter_agenda._max_tree_traverse

    hatter_agenda = agendaunit_shop(_healer="Mad Hatter", _weight=10)
    hatter_agenda.set_max_tree_traverse(3)

    egg_text = "egg first"
    egg_road = hatter_agenda.make_l1_road(egg_text)
    hatter_agenda.add_idea(
        ideaunit_shop(egg_text), parent_road=hatter_agenda._economy_id
    )

    chicken_text = "chicken first"
    chicken_road = hatter_agenda.make_l1_road(chicken_text)
    hatter_agenda.add_idea(
        ideaunit_shop(chicken_text), parent_road=hatter_agenda._economy_id
    )

    # set egg promise is True when chicken first is False
    hatter_agenda.edit_idea_attr(
        road=egg_road,
        promise=True,
        required_base=chicken_road,
        required_suff_idea_active_status=True,
    )

    # set chick promise is True when egg first is False
    hatter_agenda.edit_idea_attr(
        road=chicken_road,
        promise=True,
        required_base=egg_road,
        required_suff_idea_active_status=False,
    )

    return hatter_agenda


def get_assignment_agenda_example1():
    neo_agenda = agendaunit_shop("Neo")
    casa_text = "casa"
    casa_road = neo_agenda.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = neo_agenda.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, promise=True)
    neo_agenda.add_idea(floor_idea, parent_road=casa_road)

    neo_agenda.add_idea(
        ideaunit_shop("unimportant"), parent_road=neo_agenda._economy_id
    )

    status_text = "cleaniness status"
    status_road = neo_agenda.make_road(casa_road, status_text)
    neo_agenda.add_idea(ideaunit_shop(status_text), parent_road=casa_road)

    clean_text = "clean"
    clean_road = neo_agenda.make_road(status_road, clean_text)
    neo_agenda.add_idea(ideaunit_shop(clean_text), parent_road=status_road)
    neo_agenda.add_idea(ideaunit_shop("very_much"), parent_road=clean_road)
    neo_agenda.add_idea(ideaunit_shop("moderately"), parent_road=clean_road)
    neo_agenda.add_idea(ideaunit_shop("dirty"), parent_road=status_road)

    floor_required = requiredunit_shop(status_road)
    floor_required.set_sufffact(sufffact=status_road)
    neo_agenda.edit_idea_attr(road=floor_road, required=floor_required)

    return neo_agenda


def get_agenda_assignment_laundry_example1() -> AgendaUnit:
    amer_text = "Amer"
    amer_agenda = agendaunit_shop(_healer=amer_text)
    cali_text = "Cali"
    amer_agenda.add_partyunit(amer_text)
    amer_agenda.add_partyunit(cali_text)

    root_road = amer_agenda._economy_id
    casa_text = "casa"
    basket_text = "laundry basket status"
    b_full_text = "full"
    b_smel_text = "smelly"
    b_bare_text = "bare"
    b_fine_text = "fine"
    b_half_text = "half full"
    do_laundry_text = "do_laundry"
    casa_road = amer_agenda.make_road(root_road, casa_text)
    basket_road = amer_agenda.make_road(casa_road, basket_text)
    b_full_road = amer_agenda.make_road(basket_road, b_full_text)
    b_smel_road = amer_agenda.make_road(basket_road, b_smel_text)
    laundry_task_road = amer_agenda.make_road(casa_road, do_laundry_text)
    amer_agenda.add_idea(ideaunit_shop(casa_text), root_road)
    amer_agenda.add_idea(ideaunit_shop(basket_text), casa_road)
    amer_agenda.add_idea(ideaunit_shop(b_full_text), basket_road)
    amer_agenda.add_idea(ideaunit_shop(b_smel_text), basket_road)
    amer_agenda.add_idea(ideaunit_shop(b_bare_text), basket_road)
    amer_agenda.add_idea(ideaunit_shop(b_fine_text), basket_road)
    amer_agenda.add_idea(ideaunit_shop(b_half_text), basket_road)
    amer_agenda.add_idea(ideaunit_shop(do_laundry_text, promise=True), casa_road)

    # laundry requirement
    amer_agenda.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_full_road
    )
    # laundry requirement
    amer_agenda.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_smel_road
    )
    # assign Cali to task
    cali_assignunit = assigned_unit_shop()
    cali_assignunit.set_suffgroup(cali_text)
    amer_agenda.edit_idea_attr(road=laundry_task_road, assignedunit=cali_assignunit)
    # print(f"{basket_road=}")
    # print(f"{amer_agenda._economy_id=}")
    amer_agenda.set_acptfact(base=basket_road, pick=b_full_road)

    return amer_agenda


# class YR:
def from_list_get_active_status(
    road: RoadUnit, idea_list: list, asse_bool: bool = None
) -> bool:
    active_status = None
    temp_idea = None

    active_true_count = 0
    active_false_count = 0
    for idea in idea_list:
        if idea.get_road() == road:
            temp_idea = idea
            print(
                f"searched for IdeaUnit {temp_idea.get_road()} found {temp_idea._active_status=}"
            )

        if idea._active_status:
            active_true_count += 1
        elif idea._active_status == False:
            active_false_count += 1

    active_status = temp_idea._active_status
    print(
        f"Set Active_status: {idea._label=} {active_status} {active_true_count=} {active_false_count=}"
    )

    if asse_bool in {True, False}:
        if active_status != asse_bool:
            yr_explanation(temp_idea)

        assert active_status == asse_bool
    else:
        yr_explanation(temp_idea)
    return active_status


def yr_print_idea_base_info(idea, filter: bool):
    for l in idea._requiredheirs.values():
        if l._status == filter:
            print(
                f"  RequiredHeir '{l.base}' Base LH:{l._status} W:{len(l.sufffacts)}"  # \t_task {l._task}"
            )
            if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
                yr_print_acptfact(
                    lh_base=l.base,
                    lh_status=l._status,
                    sufffacts=l.sufffacts,
                    acptfactheirs=idea._acptfactheirs,
                )


def yr_explanation(idea):
    str1 = f"'{yr_d(idea._parent_road)}' idea"
    str2 = f" has RequiredU:{yr_x(idea._requiredunits)} LH:{yr_x(idea._requiredheirs)}"
    str3 = f" {str(type(idea))}"
    str4 = " "
    if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
        str3 = f" AcptFacts:{yr_x(idea._acptfactheirs)} Status: {idea._active_status}"

        print(f"\n{str1}{str2}{str3}")
        hh_wo_matched_required = []
        for hh in idea._acptfactheirs.values():
            hh_wo_matched_required = []
            try:
                idea._requiredheirs[hh.base]
            except Exception:
                hh_wo_matched_required.append(hh.base)

        for base in hh_wo_matched_required:
            print(f"AcptFacts that don't matter to this Idea: {base}")

    # if idea._requiredunits != None:
    #     for lu in idea._requiredunits.values():
    #         print(f"  RequiredUnit   '{lu.base}' sufffacts: {len(lu.sufffacts)} ")
    if idea._requiredheirs != None:
        filter_x = True
        yr_print_idea_base_info(idea=idea, filter=True)

        filter_x = False
        print("\nRequireds that failed:")

        for l in idea._requiredheirs.values():
            if l._status == filter_x:
                print(
                    f"  RequiredHeir '{l.base}' Base LH:{l._status} W:{len(l.sufffacts)}"  # \t_task {l._task}"
                )
                if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
                    yr_print_acptfact(
                        lh_base=l.base,
                        lh_status=l._status,
                        sufffacts=l.sufffacts,
                        acptfactheirs=idea._acptfactheirs,
                    )
                print("")
    # print(idea._acptfactheirs)
    # print(f"{(idea._acptfactheirs != None)=}")
    # print(f"{len(idea._acptfactheirs)=} ")

    print("")


def yr_print_acptfact(lh_base, lh_status, sufffacts, acptfactheirs):
    for ww in sufffacts.values():
        ww_open = ""
        ww_open = f"\topen:{ww.open}" if ww.open != None else ""
        ww_nigh = ""
        ww_nigh = f"\tnigh:{ww.nigh}" if ww.nigh != None else ""
        ww_task = f" Task: {ww._task}"
        hh_open = ""
        hh_nigh = ""
        hh_pick = ""
        print(
            f"\t    '{lh_base}' SuffFact LH:{lh_status} W:{ww._status}\tneed:{ww.need}{ww_open}{ww_nigh}"
        )

        for hh in acptfactheirs.values():
            if hh.base == lh_base:
                if hh.open != None:
                    hh_open = f"\topen:{hh.open}"
                if hh.nigh != None:
                    hh_nigh = f"\tnigh:{hh.nigh}"
                hh_pick = hh.pick
                # if hh_pick != "":
                print(
                    f"\t    '{hh.base}' AcptFact LH:{lh_status} W:{ww._status}\tAcptFact:{hh_pick}{hh_open}{hh_nigh}"
                )
        if hh_pick == "":
            print(f"\t    Base: No AcptFact")


def yr_d(self):
    return "no road" if self is None else self[self.find(",") + 1 :]


def yr_x(self):
    return 0 if self is None else len(self)
