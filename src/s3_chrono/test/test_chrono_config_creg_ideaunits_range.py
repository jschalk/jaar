from src.s2_bud.bud import budunit_shop
from src.s3_chrono.examples.chrono_examples import (
    add_time_creg_ideaunit,
    get_cregtime_str,
    get_sun,
    get_mon,
    get_tue,
    get_wed,
    get_thu,
    get_fri,
    get_sat,
)
from src.s3_chrono.chrono import (
    time_str,
    day_str,
    days_str,
    c400_leap_str,
    c400_clean_str,
    c100_str,
    yr4_leap_str,
    yr4_clean_str,
    year_str,
    week_str,
    weeks_str,
)


def test_BudUnit_init_idea_tree_walk_SetsAll_range_inheritors():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    weeks_road = sue_budunit.make_road(creg_road, weeks_str())
    week_road = sue_budunit.make_road(creg_road, week_str())
    sun_road = sue_budunit.make_road(week_road, get_sun())
    day_road = sue_budunit.make_road(creg_road, day_str())
    c400_leap_road = sue_budunit.make_road(creg_road, c400_leap_str())
    c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_clean_road = sue_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = sue_budunit.make_road(c100_clean_road, yr4_leap_str())
    yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = sue_budunit.make_road(yr4_clean_road, year_str())
    jan_road = sue_budunit.make_road(year_road, "January")

    sue_budunit = add_time_creg_ideaunit(sue_budunit)
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
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    day_road = sue_budunit.make_road(creg_road, day_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(creg_road)
    creg_idea = sue_budunit.get_idea_obj(creg_road)
    assert creg_idea.begin == 0
    assert creg_idea.close == 1472657760
    assert sue_budunit.idea_exists(day_road)
    day_idea = sue_budunit.get_idea_obj(day_road)
    assert day_idea.denom == 1440
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
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    days_road = sue_budunit.make_road(creg_road, days_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    assert sue_budunit.idea_exists(days_road)
    days_idea = sue_budunit.get_idea_obj(days_road)
    assert days_idea.denom == 1440
    assert not days_idea._gogo_calc
    assert not days_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    assert days_idea.denom == 1440
    assert days_idea._gogo_calc == 0
    assert days_idea._stop_calc == 1022679


def test_BudUnit_set_ideaunits_range_Sets_weeks_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    weeks_road = sue_budunit.make_road(creg_road, weeks_str())
    week_road = sue_budunit.make_road(creg_road, week_str())
    sun_road = sue_budunit.make_road(week_road, get_sun())
    mon_road = sue_budunit.make_road(week_road, get_mon())
    tue_road = sue_budunit.make_road(week_road, get_tue())
    wed_road = sue_budunit.make_road(week_road, get_wed())
    thu_road = sue_budunit.make_road(week_road, get_thu())
    fri_road = sue_budunit.make_road(week_road, get_fri())
    sat_road = sue_budunit.make_road(week_road, get_sat())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
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
    assert weeks_idea.denom == 10080
    assert not weeks_idea._gogo_calc
    assert not weeks_idea._stop_calc
    assert sue_budunit.idea_exists(week_road)
    week_idea = sue_budunit.get_idea_obj(week_road)
    assert week_idea.denom == 10080
    assert not week_idea._gogo_calc
    assert not week_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    assert weeks_idea.denom == 10080
    assert weeks_idea._gogo_calc == 0
    assert weeks_idea._stop_calc == 146097
    assert week_idea._gogo_calc == 0
    assert week_idea._stop_calc == 10080
    assert sue_budunit.get_idea_obj(sun_road)._gogo_calc == 5760
    assert sue_budunit.get_idea_obj(mon_road)._gogo_calc == 7200
    assert sue_budunit.get_idea_obj(tue_road)._gogo_calc == 8640
    assert sue_budunit.get_idea_obj(wed_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(thu_road)._gogo_calc == 1440
    assert sue_budunit.get_idea_obj(fri_road)._gogo_calc == 2880
    assert sue_budunit.get_idea_obj(sat_road)._gogo_calc == 4320
    assert sue_budunit.get_idea_obj(sun_road)._stop_calc == 7200
    assert sue_budunit.get_idea_obj(mon_road)._stop_calc == 8640
    assert sue_budunit.get_idea_obj(tue_road)._stop_calc == 10080
    assert sue_budunit.get_idea_obj(wed_road)._stop_calc == 1440
    assert sue_budunit.get_idea_obj(thu_road)._stop_calc == 2880
    assert sue_budunit.get_idea_obj(fri_road)._stop_calc == 4320
    assert sue_budunit.get_idea_obj(sat_road)._stop_calc == 5760


def test_BudUnit_set_ideaunits_range_Sets_c400_idea_gogo_calc_stop_calc():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    c400_leap_road = sue_budunit.make_road(creg_road, c400_leap_str())
    # c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    # c100_clean_road = sue_budunit.make_road(c400_clean_road, c100_str())
    # yr4_leap_road = sue_budunit.make_road(c100_clean_road, yr4_leap_str())
    # yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    # year_road = sue_budunit.make_road(yr4_clean_road, year_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    print(f"    {c400_leap_road=}")
    assert sue_budunit.idea_exists(c400_leap_road)
    c400_leap_idea = sue_budunit.get_idea_obj(c400_leap_road)
    # assert year_idea.morph
    assert not c400_leap_idea._gogo_calc
    assert not c400_leap_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    # assert year_idea.denom == 525600
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
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    c400_leap_road = sue_budunit.make_road(creg_road, c400_leap_str())
    c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_clean_road = sue_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = sue_budunit.make_road(c100_clean_road, yr4_leap_str())
    yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = sue_budunit.make_road(yr4_clean_road, year_str())
    sue_budunit = add_time_creg_ideaunit(sue_budunit)
    sue_budunit._init_idea_tree_walk()
    print(f"    {year_road=}")
    assert sue_budunit.idea_exists(year_road)
    year_idea = sue_budunit.get_idea_obj(year_road)
    # assert year_idea.morph
    assert not year_idea._gogo_calc
    assert not year_idea._stop_calc

    # WHEN
    sue_budunit._set_ideaunits_range()

    # THEN
    assert sue_budunit.get_idea_obj(creg_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(c400_leap_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(c400_clean_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(c100_clean_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(yr4_leap_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(yr4_clean_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(year_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(creg_road)._stop_calc == 1472657760
    assert sue_budunit.get_idea_obj(c400_leap_road)._stop_calc == 210379680
    assert sue_budunit.get_idea_obj(c400_clean_road)._stop_calc == 210378240
    assert sue_budunit.get_idea_obj(c100_clean_road)._stop_calc == 52594560
    assert sue_budunit.get_idea_obj(yr4_leap_road)._stop_calc == 2103840
    assert sue_budunit.get_idea_obj(yr4_clean_road)._stop_calc == 2102400
    assert sue_budunit.get_idea_obj(year_road)._stop_calc == 525600

    assert year_idea.denom == 525600
    assert year_idea._gogo_calc == 0
    assert year_idea._stop_calc == 525600

    jan_road = sue_budunit.make_road(year_road, "January")
    feb_road = sue_budunit.make_road(year_road, "February")
    mar_road = sue_budunit.make_road(year_road, "March")
    apr_road = sue_budunit.make_road(year_road, "April")
    may_road = sue_budunit.make_road(year_road, "May")
    jun_road = sue_budunit.make_road(year_road, "June")
    jul_road = sue_budunit.make_road(year_road, "July")
    aug_road = sue_budunit.make_road(year_road, "August")
    sep_road = sue_budunit.make_road(year_road, "September")
    oct_road = sue_budunit.make_road(year_road, "October")
    nov_road = sue_budunit.make_road(year_road, "November")
    dec_road = sue_budunit.make_road(year_road, "December")
    assert sue_budunit.get_idea_obj(jan_road)._gogo_calc == 440640
    assert sue_budunit.get_idea_obj(feb_road)._gogo_calc == 485280
    assert sue_budunit.get_idea_obj(mar_road)._gogo_calc == 0
    assert sue_budunit.get_idea_obj(apr_road)._gogo_calc == 44640
    assert sue_budunit.get_idea_obj(may_road)._gogo_calc == 87840
    assert sue_budunit.get_idea_obj(jun_road)._gogo_calc == 132480
    assert sue_budunit.get_idea_obj(jul_road)._gogo_calc == 175680
    assert sue_budunit.get_idea_obj(aug_road)._gogo_calc == 220320
    assert sue_budunit.get_idea_obj(sep_road)._gogo_calc == 264960
    assert sue_budunit.get_idea_obj(oct_road)._gogo_calc == 308160
    assert sue_budunit.get_idea_obj(nov_road)._gogo_calc == 352800
    assert sue_budunit.get_idea_obj(dec_road)._gogo_calc == 396000

    assert sue_budunit.get_idea_obj(jan_road)._stop_calc == 485280
    assert sue_budunit.get_idea_obj(feb_road)._stop_calc == 525600
    assert sue_budunit.get_idea_obj(mar_road)._stop_calc == 44640
    assert sue_budunit.get_idea_obj(apr_road)._stop_calc == 87840
    assert sue_budunit.get_idea_obj(may_road)._stop_calc == 132480
    assert sue_budunit.get_idea_obj(jun_road)._stop_calc == 175680
    assert sue_budunit.get_idea_obj(jul_road)._stop_calc == 220320
    assert sue_budunit.get_idea_obj(aug_road)._stop_calc == 264960
    assert sue_budunit.get_idea_obj(sep_road)._stop_calc == 308160
    assert sue_budunit.get_idea_obj(oct_road)._stop_calc == 352800
    assert sue_budunit.get_idea_obj(nov_road)._stop_calc == 396000
    assert sue_budunit.get_idea_obj(dec_road)._stop_calc == 440640
