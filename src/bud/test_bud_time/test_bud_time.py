from src._road.road import RoadUnit, is_string_in_road
from src.bud.group import awardlink_shop
from src.bud.reason_idea import reasonunit_shop
from src.bud.idea import IdeaUnit, ideaunit_shop
from src.bud.bud import budunit_shop, BudUnit
from src.bud.bud_time import (
    add_time_hreg_ideaunit,
    get_time_min_from_dt,
    # get_time_dt_from_min,
    time_str,  # "time"
    get_jajatime_text,  # "jajatime"
    get_sun,  # "Sunday"
    get_mon,  # "Monday"
    get_tue,  # "Tuesday"
    get_wed,  # "Wednesday"
    get_thu,  # "Thursday"
    get_fri,  # "Friday"
    get_sat,  # "Saturday"
    week_str,  # "week"
    weeks_str,  # f"{get_week()}s"
    day_str,  # "day"
    days_str,  # f"{get_day()}s"
    year_str,
    years_str,
    jan_str,
    feb_str,
    mar_str,
    apr_str,
    may_str,
    jun_str,
    jul_str,
    aug_str,
    sep_str,
    oct_str,
    nov_str,
    dec_str,
    year4_no__leap_str,
    year4_withleap_str,
    c400_leap_str,
    c400_clean_str,
    c100_str,
    yr4_leap_str,
    yr4_clean_str,
    year_str,
    month_str,
    hour_str,
    weekday_idea_str,
    year1_str,
    year2_str,
    year3_str,
    year4_str,
    node_0_100_str,
    node_1_4_str,
    node_1_96_str,
    node_2_4_str,
    node_2_96_str,
    node_3_4_str,
    node_3_96_str,
)
from datetime import datetime
from random import randint

# from src.bud.examples.example_time import get_budunit_sue_TimeExample
from copy import deepcopy as copy_deepcopy


def kidless(x_budunit: BudUnit, idea_road: RoadUnit) -> IdeaUnit:
    x_ideaunit = copy_deepcopy(x_budunit.get_idea_obj(idea_road))
    x_ideaunit._kids = {}
    x_ideaunit._fund_onset = None
    x_ideaunit._fund_cease = None
    x_ideaunit._fund_ratio = None
    x_ideaunit._fund_coin = None
    x_ideaunit._is_expanded = None
    return x_ideaunit


def kidlist(x_budunit: BudUnit, idea_road: RoadUnit) -> set[RoadUnit]:
    x_ideaunit = x_budunit.get_idea_obj(idea_road)
    return set(x_ideaunit._kids.keys())


def compare_kidless_ideas(src_budunit: BudUnit, x_budunit: BudUnit):
    # src_budunit.settle_bud()
    # x_budunit.settle_bud()

    for src_road in src_budunit._idea_dict.keys():
        # print(f"'{src_road}'")

        # TODO Fix these failures to pass assert that are skipped.
        if not is_string_in_road(
            "ZZ;time;jajatime;years;", src_road
        ) and src_road not in {
            "ZZ;time;tech;400 year segment;0-100-25 leap years;4year with leap",
            "ZZ;time;tech;400 year segment;100-104-0 leap years;4year wo leap",
            "ZZ;time;tech;400 year segment;104-200-24 leap years;4year with leap",
            "ZZ;time;tech;400 year segment;200-204-0 leap years;4year wo leap",
            "ZZ;time;tech;400 year segment;204-300-24 leap years;4year with leap",
        }:
            if kidless(src_budunit, src_road) != kidless(x_budunit, src_road):
                print(f"'{src_road}' failure")
                src_ideaunit = src_budunit.get_idea_obj(src_road)
                x_ideaunit = x_budunit.get_idea_obj(src_road)
                print(f"{src_ideaunit._begin=} \t\t {x_ideaunit._begin=}")
                print(f"{src_ideaunit._close=} \t\t {x_ideaunit._close=}")
                print(f"{src_ideaunit._numor=} \t\t {x_ideaunit._numor=}")
                print(f"{src_ideaunit._denom=} \t\t {x_ideaunit._denom=}")
                print(f"{src_ideaunit._addin=} \t\t {x_ideaunit._addin=}")
                print(f"{src_ideaunit._morph=} \t\t {x_ideaunit._morph=}")
                # print(f"{src_ideaunit._parent_road=} \t\t {x_ideaunit._parent_road=}")
            assert kidless(src_budunit, src_road) == kidless(x_budunit, src_road)


def compare_kidlists(src_budunit: BudUnit, x_budunit: BudUnit):
    for src_road in src_budunit._idea_dict.keys():
        if kidlist(src_budunit, src_road) != kidlist(x_budunit, src_road):
            print(f"   Kidlist failure at {src_road=}")
            print(f"{kidlist(src_budunit, src_road)=}")
        assert kidlist(src_budunit, src_road) == kidlist(x_budunit, src_road)


def test_get_time_min_from_dt_WorksCorrectly():
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_hreg_ideaunit(sue_bud)

    assert get_time_min_from_dt(datetime(1938, 11, 10))
    assert get_time_min_from_dt(datetime(1, 1, 1)) == 440640
    assert get_time_min_from_dt(datetime(1, 1, 2)) == 440640 + 1440
    assert get_time_min_from_dt(datetime(1938, 11, 10)) == 1019653920
    # assert g_lw.get_time_dt_from_min(
    #     min=g_lw.get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    # ) == datetime(2000, 1, 1, 0, 0)
    assert get_time_min_from_dt(datetime(800, 1, 1, 0, 0)) == 420672960
    assert get_time_min_from_dt(datetime(1200, 1, 1, 0, 0)) == 631052640
    assert get_time_min_from_dt(datetime(1201, 3, 1, 0, 0)) == 631664640
    assert get_time_min_from_dt(datetime(1201, 3, 1, 0, 20)) == 631664660

    x_minutes = 1063817280
    assert get_time_min_from_dt(datetime(2022, 10, 29, 0, 0)) == x_minutes
    x_next_day = x_minutes + 1440
    assert get_time_min_from_dt(datetime(2022, 10, 30, 0, 0)) == x_next_day


def test_add_time_hreg_ideaunit_ReturnsObjWith_days():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    days_road = sue_budunit.make_road(jaja_road, days_str())
    print(f"{time_road=}")
    print(f"{jaja_road=}")
    print(f"{day_road=}")
    assert not sue_budunit.idea_exists(time_road)
    assert not sue_budunit.idea_exists(jaja_road)
    assert not sue_budunit.idea_exists(day_road)
    assert not sue_budunit.idea_exists(days_road)

    # WHEN
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(jaja_road)
    jaja_idea = sue_budunit.get_idea_obj(jaja_road)
    assert jaja_idea._begin == 0
    assert jaja_idea._close == 1472657760
    assert sue_budunit.idea_exists(day_road)
    day_idea = sue_budunit.get_idea_obj(day_road)
    assert day_idea._gogo_want == 0
    assert day_idea._stop_want == 1440
    assert day_idea._denom == 1440
    assert day_idea._morph
    assert sue_budunit.idea_exists(days_road)
    days_idea = sue_budunit.get_idea_obj(days_road)
    assert days_idea._denom == 1440
    assert not days_idea._morph


def test_add_time_hreg_ideaunit_ReturnsObjWith_weeks():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    week_road = sue_budunit.make_road(jaja_road, week_str())
    sun_road = sue_budunit.make_road(week_road, get_sun())
    mon_road = sue_budunit.make_road(week_road, get_mon())
    tue_road = sue_budunit.make_road(week_road, get_tue())
    wed_road = sue_budunit.make_road(week_road, get_wed())
    thu_road = sue_budunit.make_road(week_road, get_thu())
    fri_road = sue_budunit.make_road(week_road, get_fri())
    sat_road = sue_budunit.make_road(week_road, get_sat())
    weeks_road = sue_budunit.make_road(jaja_road, weeks_str())

    assert not sue_budunit.idea_exists(week_road)
    assert not sue_budunit.idea_exists(sun_road)
    assert not sue_budunit.idea_exists(mon_road)
    assert not sue_budunit.idea_exists(tue_road)
    assert not sue_budunit.idea_exists(wed_road)
    assert not sue_budunit.idea_exists(thu_road)
    assert not sue_budunit.idea_exists(fri_road)
    assert not sue_budunit.idea_exists(sat_road)
    assert not sue_budunit.idea_exists(weeks_road)

    # WHEN
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(week_road)
    week_idea = sue_budunit.get_idea_obj(week_road)
    assert week_idea._gogo_want == 0
    assert week_idea._stop_want == 10080
    assert week_idea._denom == 10080
    assert week_idea._morph
    assert sue_budunit.idea_exists(sun_road)
    assert sue_budunit.idea_exists(mon_road)
    assert sue_budunit.idea_exists(tue_road)
    assert sue_budunit.idea_exists(wed_road)
    assert sue_budunit.idea_exists(thu_road)
    assert sue_budunit.idea_exists(fri_road)
    assert sue_budunit.idea_exists(sat_road)
    assert sue_budunit.idea_exists(weeks_road)
    weeks_idea = sue_budunit.get_idea_obj(weeks_road)
    assert weeks_idea._denom == 10080
    assert not weeks_idea._morph


def test_add_time_hreg_ideaunit_ReturnsObjWith_c400_leap_road():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    c400_leap_road = sue_budunit.make_road(jaja_road, c400_leap_str())
    c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = sue_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = sue_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = sue_budunit.make_road(yr4_clean_road, year_str())

    assert not sue_budunit.idea_exists(c400_leap_road)

    # WHEN
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(c400_leap_road)
    c400_leap_idea = sue_budunit.get_idea_obj(c400_leap_road)
    assert not c400_leap_idea._gogo_want
    assert not c400_leap_idea._stop_want
    assert c400_leap_idea._denom == 210379680
    assert c400_leap_idea._morph

    assert sue_budunit.idea_exists(c400_clean_road)
    c400_clean_idea = sue_budunit.get_idea_obj(c400_clean_road)
    assert not c400_clean_idea._gogo_want
    assert not c400_clean_idea._stop_want
    assert c400_clean_idea._denom == 210378240
    assert c400_clean_idea._morph

    assert sue_budunit.idea_exists(c100_road)
    c100_idea = sue_budunit.get_idea_obj(c100_road)
    assert not c100_idea._gogo_want
    assert not c100_idea._stop_want
    assert c100_idea._denom == 52594560
    assert c100_idea._morph

    assert sue_budunit.idea_exists(yr4_leap_road)
    yr4_leap_idea = sue_budunit.get_idea_obj(yr4_leap_road)
    assert not yr4_leap_idea._gogo_want
    assert not yr4_leap_idea._stop_want
    assert yr4_leap_idea._denom == 2103840
    assert yr4_leap_idea._morph

    assert sue_budunit.idea_exists(yr4_clean_road)
    yr4_clean_idea = sue_budunit.get_idea_obj(yr4_clean_road)
    assert not yr4_clean_idea._gogo_want
    assert not yr4_clean_idea._stop_want
    assert yr4_clean_idea._denom == 2102400
    assert yr4_clean_idea._morph

    assert sue_budunit.idea_exists(year_road)
    year_idea = sue_budunit.get_idea_obj(year_road)
    assert not year_idea._gogo_want
    assert not year_idea._stop_want
    assert year_idea._denom == 525600
    assert year_idea._morph


def test_add_time_hreg_ideaunit_ReturnsObjWith_years():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    c400_leap_road = sue_budunit.make_road(jaja_road, c400_leap_str())
    c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = sue_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = sue_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = sue_budunit.make_road(yr4_clean_road, year_str())

    assert not sue_budunit.idea_exists(jaja_road)
    assert not sue_budunit.idea_exists(c400_leap_road)
    assert not sue_budunit.idea_exists(c400_clean_road)
    assert not sue_budunit.idea_exists(c100_road)
    assert not sue_budunit.idea_exists(yr4_leap_road)
    assert not sue_budunit.idea_exists(yr4_clean_road)
    assert not sue_budunit.idea_exists(year_road)

    jan_road = sue_budunit.make_road(year_road, jan_str())
    feb_road = sue_budunit.make_road(year_road, feb_str())
    mar_road = sue_budunit.make_road(year_road, mar_str())
    apr_road = sue_budunit.make_road(year_road, apr_str())
    may_road = sue_budunit.make_road(year_road, may_str())
    jun_road = sue_budunit.make_road(year_road, jun_str())
    jul_road = sue_budunit.make_road(year_road, jul_str())
    aug_road = sue_budunit.make_road(year_road, aug_str())
    sep_road = sue_budunit.make_road(year_road, sep_str())
    oct_road = sue_budunit.make_road(year_road, oct_str())
    nov_road = sue_budunit.make_road(year_road, nov_str())
    dec_road = sue_budunit.make_road(year_road, dec_str())
    assert not sue_budunit.idea_exists(jan_road)
    assert not sue_budunit.idea_exists(feb_road)
    assert not sue_budunit.idea_exists(mar_road)
    assert not sue_budunit.idea_exists(apr_road)
    assert not sue_budunit.idea_exists(may_road)
    assert not sue_budunit.idea_exists(jun_road)
    assert not sue_budunit.idea_exists(jul_road)
    assert not sue_budunit.idea_exists(aug_road)
    assert not sue_budunit.idea_exists(sep_road)
    assert not sue_budunit.idea_exists(oct_road)
    assert not sue_budunit.idea_exists(nov_road)
    assert not sue_budunit.idea_exists(dec_road)
    assert not sue_budunit.idea_exists(year_road)

    # WHEN
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(jaja_road)
    print(f"     {year_road=}")
    assert sue_budunit.idea_exists(c400_leap_road)
    assert sue_budunit.idea_exists(c400_clean_road)
    assert sue_budunit.idea_exists(c100_road)
    assert sue_budunit.idea_exists(yr4_leap_road)
    assert sue_budunit.idea_exists(yr4_clean_road)
    assert sue_budunit.idea_exists(year_road)

    year_idea = sue_budunit.get_idea_obj(year_road)
    # assert year_idea._morph
    assert sue_budunit.idea_exists(jan_road)
    assert sue_budunit.idea_exists(feb_road)
    assert sue_budunit.idea_exists(mar_road)
    assert sue_budunit.idea_exists(apr_road)
    assert sue_budunit.idea_exists(may_road)
    assert sue_budunit.idea_exists(jun_road)
    assert sue_budunit.idea_exists(jul_road)
    assert sue_budunit.idea_exists(aug_road)
    assert sue_budunit.idea_exists(sep_road)
    assert sue_budunit.idea_exists(oct_road)
    assert sue_budunit.idea_exists(nov_road)
    assert sue_budunit.idea_exists(dec_road)
    assert sue_budunit.get_idea_obj(jan_road)._gogo_want == 437760
    assert sue_budunit.get_idea_obj(feb_road)._gogo_want == 480960
    assert sue_budunit.get_idea_obj(mar_road)._gogo_want == 0
    assert sue_budunit.get_idea_obj(apr_road)._gogo_want == 44640
    assert sue_budunit.get_idea_obj(may_road)._gogo_want == 84960
    assert sue_budunit.get_idea_obj(jun_road)._gogo_want == 129600
    assert sue_budunit.get_idea_obj(jul_road)._gogo_want == 172800
    assert sue_budunit.get_idea_obj(aug_road)._gogo_want == 217440
    assert sue_budunit.get_idea_obj(sep_road)._gogo_want == 260640
    assert sue_budunit.get_idea_obj(oct_road)._gogo_want == 305280
    assert sue_budunit.get_idea_obj(nov_road)._gogo_want == 349920
    assert sue_budunit.get_idea_obj(dec_road)._gogo_want == 393120

    assert sue_budunit.get_idea_obj(jan_road)._stop_want == 480960
    assert sue_budunit.get_idea_obj(feb_road)._stop_want == 525600
    assert sue_budunit.get_idea_obj(mar_road)._stop_want == 44640
    assert sue_budunit.get_idea_obj(apr_road)._stop_want == 84960
    assert sue_budunit.get_idea_obj(may_road)._stop_want == 129600
    assert sue_budunit.get_idea_obj(jun_road)._stop_want == 172800
    assert sue_budunit.get_idea_obj(jul_road)._stop_want == 217440
    assert sue_budunit.get_idea_obj(aug_road)._stop_want == 260640
    assert sue_budunit.get_idea_obj(sep_road)._stop_want == 305280
    assert sue_budunit.get_idea_obj(oct_road)._stop_want == 349920
    assert sue_budunit.get_idea_obj(nov_road)._stop_want == 393120
    assert sue_budunit.get_idea_obj(dec_road)._stop_want == 437760


def test_add_time_hreg_ideaunit_ReturnsObjWith_c400_():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    days_road = sue_budunit.make_road(jaja_road, days_str())
    print(f"{time_road=}")
    print(f"{jaja_road=}")
    print(f"{day_road=}")
    assert not sue_budunit.idea_exists(time_road)
    assert not sue_budunit.idea_exists(jaja_road)
    assert not sue_budunit.idea_exists(day_road)
    assert not sue_budunit.idea_exists(days_road)

    # WHEN
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(jaja_road)
    jaja_idea = sue_budunit.get_idea_obj(jaja_road)
    assert jaja_idea._begin == 0
    assert jaja_idea._close == 1472657760
    assert sue_budunit.idea_exists(day_road)
    day_idea = sue_budunit.get_idea_obj(day_road)
    assert day_idea._gogo_want == 0
    assert day_idea._stop_want == 1440
    assert day_idea._denom == 1440
    assert day_idea._morph
    assert sue_budunit.idea_exists(days_road)
    days_idea = sue_budunit.get_idea_obj(days_road)
    assert days_idea._denom == 1440
    assert not days_idea._morph

    # assert sue_budunit is not None
    # assert sue_budunit.idea_exists(time_road)
    # assert sue_budunit.idea_exists(tech_road)
    # assert sue_budunit.idea_exists(week_road)
    # assert sue_budunit.idea_exists(jaja_road)
    # assert kidlist(sue_budunit, time_road) == kidlist(ex1_budunit, time_road)
    # assert kidlist(sue_budunit, tech_road) == kidlist(ex1_budunit, tech_road)
    # assert kidlist(sue_budunit, year365_road) == kidlist(ex1_budunit, year365_road)
    # assert kidlist(sue_budunit, year366_road) == kidlist(ex1_budunit, year366_road)
    # assert kidlist(sue_budunit, day_road) == kidlist(ex1_budunit, day_road)
    # assert kidlist(sue_budunit, hour_road) == kidlist(ex1_budunit, hour_road)
    # assert kidlist(sue_budunit, month_road) == kidlist(ex1_budunit, month_road)
    # assert kidlist(sue_budunit, week_road) == kidlist(ex1_budunit, week_road)
    # assert kidlist(sue_budunit, jaja_road) == kidlist(ex1_budunit, jaja_road)
    # compare_kidlists(ex1_budunit, sue_budunit)

    # compare_kidless_ideas(ex1_budunit, sue_budunit)
    # # assert sue_budunit == ex1_budunit


# def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario2():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_hreg_ideas(c400_count=7)

#     # WHEN THEN
#     time_road = sue_budunit.make_l1_road("time")
#     tech_road = sue_budunit.make_road(time_road, "tech")
#     week_road = sue_budunit.make_road(tech_road, "week")
#     assert len(sue_budunit.get_idea_ranged_kids(week_road, begin=0, close=1440)) == 1
#     assert len(sue_budunit.get_idea_ranged_kids(week_road, begin=0, close=2000)) == 2
#     assert len(sue_budunit.get_idea_ranged_kids(week_road, begin=0, close=3000)) == 3


# def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario3():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_hreg_ideas(c400_count=7)

#     # WHEN THEN
#     time_road = sue_budunit.make_l1_road("time")
#     tech_road = sue_budunit.make_road(time_road, "tech")
#     week_road = sue_budunit.make_road(tech_road, "week")
#     assert len(sue_budunit.get_idea_ranged_kids(idea_road=week_road, begin=0)) == 1
#     assert len(sue_budunit.get_idea_ranged_kids(idea_road=week_road, begin=1440)) == 1


def test_BudUnit_get_agenda_dict_DoesNotReturnPledgeItemsOutsideRange():
    # ESTABLISH
    sue_text = "Sue"
    sue_bud = add_time_hreg_ideaunit(budunit_shop(sue_text))
    clean_text = "clean"
    clean_road = sue_bud.make_l1_road(clean_text)
    sue_bud.set_l1_idea(ideaunit_shop(clean_text, pledge=True))
    time_road = sue_bud.make_l1_road("time")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    day_road = sue_bud.make_road(jajatime_road, "day")

    sue_bud.edit_idea_attr(
        road=clean_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=320,
        reason_premise_nigh=480,
    )

    # WHEN
    open_x = 2063971110
    nigh_x1 = 2063971523
    sue_bud.set_fact(base=jajatime_road, pick=jajatime_road, open=open_x, nigh=nigh_x1)

    # THEN
    agenda_dict = sue_bud.get_agenda_dict()
    print(f"{agenda_dict.keys()=}")
    assert len(agenda_dict) == 1
    assert clean_road in agenda_dict.keys()

    # WHEN
    # nigh_x2 = 1063971923
    open_x2 = 0
    nigh_x2 = 0
    sue_bud.set_fact(base=jajatime_road, pick=jajatime_road, open=open_x2, nigh=nigh_x2)
    print(f"YAYA {sue_bud._idearoot._factunits=}")

    # THEN
    agenda_dict = sue_bud.get_agenda_dict()
    assert len(agenda_dict) == 0


def test_BudUnit_create_agenda_item_CorrectlyCreatesAllBudAttributes():
    # WHEN "I am cleaning the cookery since I'm in the flat and it's 8am and it's dirty and it's for my family"

    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    assert len(sue_bud._accts) == 0
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0

    clean_things_text = "cleaning things"
    clean_things_road = sue_bud.make_l1_road(clean_things_text)
    sweep_text = "sweep"
    sweep_road = sue_bud.make_road(clean_things_road, sweep_text)
    sweep_idea = ideaunit_shop(sweep_text, _parent_road=clean_things_road)
    print(f"{sweep_idea.get_road()=}")
    house_text = "house"
    house_road = sue_bud.make_l1_road(house_text)
    cookery_room_text = "cookery room"
    cookery_room_road = sue_bud.make_road(house_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = sue_bud.make_road(cookery_room_road, cookery_dirty_text)

    # create gregorian timeline
    add_time_hreg_ideaunit(sue_bud)
    time_road = sue_bud.make_l1_road("time")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    jaja_idea = sue_bud.get_idea_obj(jajatime_road)
    print(f"{jaja_idea._kids.keys()=}")
    daytime_road = sue_bud.make_road(jajatime_road, "day")
    open_8am = 480
    nigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_road)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
    sweep_idea.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_road)
    daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
    sweep_idea.set_reasonunit(reason=daytime_reason)

    family_text = ",family"
    awardlink_z = awardlink_shop(group_id=family_text)
    sweep_idea.set_awardlink(awardlink_z)

    assert len(sue_bud._accts) == 0
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert len(sue_bud._idearoot._kids) == 1
    assert sue_bud.get_idea_obj(daytime_road)._gogo_want == 0
    assert sue_bud.get_idea_obj(daytime_road)._stop_want == 1440
    print(f"{sweep_idea.get_road()=}")

    # ESTABLISH
    sue_bud.set_dominate_pledge_idea(idea_kid=sweep_idea)

    # THEN
    # for idea_kid in sue_bud._idearoot._kids.keys():
    #     print(f"  {idea_kid=}")

    print(f"{sweep_idea.get_road()=}")
    assert sue_bud.get_idea_obj(sweep_road) is not None
    assert sue_bud.get_idea_obj(sweep_road)._label == sweep_text
    assert sue_bud.get_idea_obj(sweep_road).pledge
    assert len(sue_bud.get_idea_obj(sweep_road)._reasonunits) == 2
    assert sue_bud.get_idea_obj(clean_things_road) is not None
    assert sue_bud.get_idea_obj(cookery_room_road) is not None
    assert sue_bud.get_idea_obj(cookery_dirty_road) is not None
    assert sue_bud.get_idea_obj(daytime_road)._gogo_want == 0
    assert sue_bud.get_idea_obj(daytime_road)._stop_want == 1440
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert sue_bud.get_acctunit_group_ids_dict().get(family_text) is None

    assert len(sue_bud._idearoot._kids) == 3


def test_IdeaCore_get_agenda_dict_ReturnsCorrectObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    add_time_hreg_ideaunit(sue_bud)

    casa_text = "casa"
    casa_road = sue_bud.make_l1_road(casa_text)
    laundry_text = "do_laundry"
    laundry_road = sue_bud.make_road(casa_road, laundry_text)
    sue_bud.set_l1_idea(ideaunit_shop(casa_text))
    sue_bud.set_idea(ideaunit_shop(laundry_text, pledge=True), casa_road)
    time_road = sue_bud.make_l1_road("time")
    jajatime_road = sue_bud.make_road(time_road, "jajatime")
    sue_bud.edit_idea_attr(
        road=laundry_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=3420.0,
        reason_premise_nigh=3420.0,
        reason_premise_divisor=10080.0,
    )
    print("set first fact")

    sue_bud.set_fact(jajatime_road, jajatime_road, 1064131200, nigh=1064135133)
    print("get 1st agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")
    assert sue_agenda_dict == {}

    laundry_idea = sue_bud.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_factheir = laundry_idea._factheirs.get(jajatime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.nigh % 10080=}"
    # )
    # print(f"{laundry_reasonheir.base=} {laundry_premise=}")
    # for x_ideaunit in sue_bud._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")

    # WHEN
    print("set 2nd fact")
    sue_bud.set_fact(jajatime_road, jajatime_road, 1064131200, nigh=1064136133)
    print("get 2nd agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")

    laundry_idea = sue_bud.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_factheir = laundry_idea._factheirs.get(jajatime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.nigh % 10080=}"
    # )
    # for x_ideaunit in sue_bud._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")
    #         jaja_factheir = x_ideaunit._factheirs.get(jajatime_road)
    #         print(f"{jaja_factheir.open % 10080=}")
    #         print(f"{jaja_factheir.nigh % 10080=}")

    # THEN
    assert sue_agenda_dict == {}


# def test_get_time_dt_from_min_WorksCorrectly():
#     sue_bud = budunit_shop("Sue")
#     sue_bud = add_time_hreg_ideaunit(sue_bud)
#     assert get_time_dt_from_min(5000000)
#     # assert g_lw.get_time_dt_from_min(
#     #     min=g_lw.get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
#     # ) == datetime(2000, 1, 1, 0, 0)
#     assert get_time_dt_from_min(420759360) == datetime(800, 1, 1, 0, 0)
#     assert get_time_dt_from_min(631139040) == datetime(1200, 1, 1, 0, 0)
#     assert get_time_dt_from_min(631751040) == datetime(1201, 3, 1, 0, 0)
#     assert get_time_dt_from_min(631751060) == datetime(1201, 3, 1, 0, 20)

#     x_minutes = 1063903680
#     assert get_time_dt_from_min(min=x_minutes) == datetime(2022, 10, 29, 0, 0)
#     x_next_day = x_minutes + 1440
#     assert get_time_dt_from_min(min=x_next_day) == datetime(2022, 10, 30, 0, 0)


# def _check_time_conversion_works_with_random_inputs():
#     py_dt = datetime(
#         year=randint(1, 2800),
#         month=randint(1, 12),
#         day=randint(1, 28),
#         hour=randint(0, 23),
#         minute=randint(0, 59),
#     )
#     print(f"Attempt {py_dt=}")
#     assert py_dt == get_time_dt_from_min(min=get_time_min_from_dt(dt=py_dt))


# def test_get_time_min_from_dt_WorksCorrectly():
#     _check_time_conversion_works_with_random_inputs()
#     _check_time_conversion_works_with_random_inputs()
#     _check_time_conversion_works_with_random_inputs()
