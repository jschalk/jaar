from src.bud.bud import budunit_shop
from src.bud.bud_time import (
    get_time_min_from_dt,
    add_time_hreg_ideaunit,
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
    c400_leap_str,
    c400_clean_str,
    c100_str,
    yr4_leap_str,
    yr4_clean_str,
    year_str,
)
from datetime import datetime


def test_BudUnit_init_idea_tree_walk_SetsAll_range_inheritors():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    weeks_road = sue_budunit.make_road(jaja_road, weeks_str())
    week_road = sue_budunit.make_road(jaja_road, week_str())
    sun_road = sue_budunit.make_road(week_road, get_sun())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    c400_leap_road = sue_budunit.make_road(jaja_road, c400_leap_str())
    c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_clean_road = sue_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = sue_budunit.make_road(c100_clean_road, yr4_leap_str())
    yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = sue_budunit.make_road(yr4_clean_road, year_str())
    jan_road = sue_budunit.make_road(year_road, jan_str())

    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    assert sue_budunit._range_inheritors == {}

    # WHEN
    sue_budunit._init_idea_tree_walk()
    sue_budunit._set_ideaunits_range()

    # THEN
    print(f"{sue_budunit._range_inheritors=}")
    assert sue_budunit._range_inheritors != {}
    assert day_road in sue_budunit._range_inheritors
    assert weeks_road in sue_budunit._range_inheritors
    assert week_road in sue_budunit._range_inheritors
    assert sun_road in sue_budunit._range_inheritors
    assert c400_leap_road in sue_budunit._range_inheritors
    assert c400_clean_road in sue_budunit._range_inheritors
    assert c100_clean_road in sue_budunit._range_inheritors
    assert yr4_leap_road in sue_budunit._range_inheritors
    assert yr4_clean_road in sue_budunit._range_inheritors
    assert year_road in sue_budunit._range_inheritors
    assert jan_road in sue_budunit._range_inheritors


def test_BudUnit_set_ideaunits_range_Sets_day_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    day_road = sue_budunit.make_road(jaja_road, day_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(jaja_road)
    jaja_idea = sue_budunit.get_idea_obj(jaja_road)
    assert jaja_idea._begin == 0
    assert jaja_idea._close == 1472657760
    assert sue_budunit.idea_exists(day_road)
    day_idea = sue_budunit.get_idea_obj(day_road)
    assert day_idea._denom == 1440
    assert not day_idea._gogo_calc
    assert not day_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    assert day_idea._gogo_calc == 0
    assert day_idea._stop_calc == 1440


def test_BudUnit_set_ideaunits_range_Sets_days_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    days_road = sue_budunit.make_road(jaja_road, days_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    assert sue_budunit.idea_exists(days_road)
    days_idea = sue_budunit.get_idea_obj(days_road)
    assert days_idea._denom == 1440
    assert not days_idea._gogo_calc
    assert not days_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    assert days_idea._denom == 1440
    assert days_idea._gogo_calc == 0
    assert days_idea._stop_calc == 1022679


def test_BudUnit_set_ideaunits_range_Sets_weeks_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    weeks_road = sue_budunit.make_road(jaja_road, weeks_str())
    week_road = sue_budunit.make_road(jaja_road, week_str())
    sun_road = sue_budunit.make_road(week_road, get_sun())
    mon_road = sue_budunit.make_road(week_road, get_mon())
    tue_road = sue_budunit.make_road(week_road, get_tue())
    wed_road = sue_budunit.make_road(week_road, get_wed())
    thu_road = sue_budunit.make_road(week_road, get_thu())
    fri_road = sue_budunit.make_road(week_road, get_fri())
    sat_road = sue_budunit.make_road(week_road, get_sat())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    assert sue_budunit.idea_exists(weeks_road)
    assert sue_budunit.idea_exists(sun_road)
    assert sue_budunit.idea_exists(mon_road)
    assert sue_budunit.idea_exists(tue_road)
    assert sue_budunit.idea_exists(wed_road)
    assert sue_budunit.idea_exists(thu_road)
    assert sue_budunit.idea_exists(fri_road)
    assert sue_budunit.idea_exists(sat_road)
    weeks_idea = sue_budunit.get_idea_obj(weeks_road)
    assert weeks_idea._denom == 10080
    assert not weeks_idea._gogo_calc
    assert not weeks_idea._stop_calc
    assert sue_budunit.idea_exists(week_road)
    week_idea = sue_budunit.get_idea_obj(week_road)
    assert week_idea._denom == 10080
    assert not week_idea._gogo_calc
    assert not week_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    assert weeks_idea._denom == 10080
    assert weeks_idea._gogo_calc == 0
    assert weeks_idea._stop_calc == 146097
    assert week_idea._gogo_calc == 0
    assert week_idea._stop_calc == 10080
    assert sue_budunit.get_idea_obj(sun_road)._gogo_calc == 1440
    assert sue_budunit.get_idea_obj(mon_road)._gogo_calc == 2880
    assert sue_budunit.get_idea_obj(tue_road)._gogo_calc == 4320
    assert sue_budunit.get_idea_obj(wed_road)._gogo_calc == 5760
    assert sue_budunit.get_idea_obj(thu_road)._gogo_calc == 7200
    assert sue_budunit.get_idea_obj(fri_road)._gogo_calc == 8640
    assert sue_budunit.get_idea_obj(sat_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(sun_road)._stop_calc == 2880
    assert sue_budunit.get_idea_obj(mon_road)._stop_calc == 4320
    assert sue_budunit.get_idea_obj(tue_road)._stop_calc == 5760
    assert sue_budunit.get_idea_obj(wed_road)._stop_calc == 7200
    assert sue_budunit.get_idea_obj(thu_road)._stop_calc == 8640
    assert sue_budunit.get_idea_obj(fri_road)._stop_calc == 10080
    assert sue_budunit.get_idea_obj(sat_road)._stop_calc == 1440


def test_BudUnit_set_ideaunits_range_Sets_c400_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    c400_leap_road = sue_budunit.make_road(jaja_road, c400_leap_str())
    # c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    # c100_clean_road = sue_budunit.make_road(c400_clean_road, c100_str())
    # yr4_leap_road = sue_budunit.make_road(c100_clean_road, yr4_leap_str())
    # yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    # year_road = sue_budunit.make_road(yr4_clean_road, year_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    print(f"    {c400_leap_road=}")
    assert sue_budunit.idea_exists(c400_leap_road)
    c400_leap_idea = sue_budunit.get_idea_obj(c400_leap_road)
    # assert year_idea._morph
    assert not c400_leap_idea._gogo_calc
    assert not c400_leap_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    # assert year_idea._denom == 525600
    # assert year_idea._gogo_calc == 0
    # assert year_idea._stop_calc == 525600
    difference_between_mar1_jan1 = 86400
    assert sue_budunit.get_idea_obj(c400_leap_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(c400_leap_road)._stop_calc == 210379680
    assert 1472657760 % sue_budunit.get_idea_obj(c400_leap_road)._stop_calc == 0


def test_BudUnit_set_ideaunits_range_Sets_years_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
    c400_leap_road = sue_budunit.make_road(jaja_road, c400_leap_str())
    c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_clean_road = sue_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = sue_budunit.make_road(c100_clean_road, yr4_leap_str())
    yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = sue_budunit.make_road(yr4_clean_road, year_str())
    sue_budunit = add_time_hreg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    print(f"    {year_road=}")
    assert sue_budunit.idea_exists(year_road)
    year_idea = sue_budunit.get_idea_obj(year_road)
    # assert year_idea._morph
    assert not year_idea._gogo_calc
    assert not year_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    assert sue_budunit.get_idea_obj(jaja_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(c400_leap_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(c400_clean_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(c100_clean_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(yr4_leap_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(yr4_clean_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(year_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(jaja_road)._stop_calc == 1472657760
    assert sue_budunit.get_idea_obj(c400_leap_road)._stop_calc == 210379680
    assert sue_budunit.get_idea_obj(c400_clean_road)._stop_calc == 210378240
    assert sue_budunit.get_idea_obj(c100_clean_road)._stop_calc == 52594560
    assert sue_budunit.get_idea_obj(yr4_leap_road)._stop_calc == 2103840
    assert sue_budunit.get_idea_obj(yr4_clean_road)._stop_calc == 2102400
    assert sue_budunit.get_idea_obj(year_road)._stop_calc == 525600

    assert year_idea._denom == 525600
    assert year_idea._gogo_calc == 0
    assert year_idea._stop_calc == 525600

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
    assert sue_budunit.get_idea_obj(jan_road)._gogo_calc == 437760
    assert sue_budunit.get_idea_obj(feb_road)._gogo_calc == 480960
    assert sue_budunit.get_idea_obj(mar_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(apr_road)._gogo_calc == 44640
    assert sue_budunit.get_idea_obj(may_road)._gogo_calc == 84960
    assert sue_budunit.get_idea_obj(jun_road)._gogo_calc == 129600
    assert sue_budunit.get_idea_obj(jul_road)._gogo_calc == 172800
    assert sue_budunit.get_idea_obj(aug_road)._gogo_calc == 217440
    assert sue_budunit.get_idea_obj(sep_road)._gogo_calc == 260640
    assert sue_budunit.get_idea_obj(oct_road)._gogo_calc == 305280
    assert sue_budunit.get_idea_obj(nov_road)._gogo_calc == 349920
    assert sue_budunit.get_idea_obj(dec_road)._gogo_calc == 393120

    assert sue_budunit.get_idea_obj(jan_road)._stop_calc == 480960
    assert sue_budunit.get_idea_obj(feb_road)._stop_calc == 525600
    assert sue_budunit.get_idea_obj(mar_road)._stop_calc == 44640
    assert sue_budunit.get_idea_obj(apr_road)._stop_calc == 84960
    assert sue_budunit.get_idea_obj(may_road)._stop_calc == 129600
    assert sue_budunit.get_idea_obj(jun_road)._stop_calc == 172800
    assert sue_budunit.get_idea_obj(jul_road)._stop_calc == 217440
    assert sue_budunit.get_idea_obj(aug_road)._stop_calc == 260640
    assert sue_budunit.get_idea_obj(sep_road)._stop_calc == 305280
    assert sue_budunit.get_idea_obj(oct_road)._stop_calc == 349920
    assert sue_budunit.get_idea_obj(nov_road)._stop_calc == 393120
    assert sue_budunit.get_idea_obj(dec_road)._stop_calc == 437760


# def test_BudUnit_set_ideaunits_range_SyncsWeekDayAndYear():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     time_road = sue_budunit.make_l1_road(time_str())
#     jaja_road = sue_budunit.make_road(time_road, get_jajatime_text())
#     c400_leap_road = sue_budunit.make_road(jaja_road, c400_leap_str())
#     # c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
#     # c100_clean_road = sue_budunit.make_road(c400_clean_road, c100_str())
#     # yr4_leap_road = sue_budunit.make_road(c100_clean_road, yr4_leap_str())
#     # yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
#     # year_road = sue_budunit.make_road(yr4_clean_road, year_str())
#     sue_budunit = add_time_hreg_ideaunit(sue_budunit)
#     sue_budunit._init_idea_tree_walk()
#     print(f"    {c400_leap_road=}")
#     assert sue_budunit.idea_exists(c400_leap_road)
#     c400_leap_idea = sue_budunit.get_idea_obj(c400_leap_road)
#     # assert year_idea._morph
#     assert not c400_leap_idea._gogo_calc
#     assert not c400_leap_idea._stop_calc

#     # WHEN
#     sue_budunit._set_ideaunits_range()

#     # THEN
#     # assert year_idea._denom == 525600
#     # assert year_idea._gogo_calc == 0
#     # assert year_idea._stop_calc == 525600
#     difference_between_mar1_jan1 = 86400
#     assert sue_budunit.get_idea_obj(c400_leap_road)._gogo_calc == 0
#     assert sue_budunit.get_idea_obj(c400_leap_road)._stop_calc == 210379680
#     assert 1472657760 % sue_budunit.get_idea_obj(c400_leap_road)._stop_calc == 0
