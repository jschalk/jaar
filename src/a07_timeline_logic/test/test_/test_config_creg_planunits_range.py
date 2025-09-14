from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a07_timeline_logic.test._util.a07_terms import (
    c100_str,
    c400_clean_str,
    c400_leap_str,
    day_str,
    days_str,
    time_str,
    week_str,
    weeks_str,
    year_str,
    yr4_clean_str,
    yr4_leap_str,
)
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_planunit,
    get_cregtime_str,
    get_fri,
    get_mon,
    get_sat,
    get_sun,
    get_thu,
    get_tue,
    get_wed,
)


def test_BeliefUnit_set_plan_dict_SetsAll_range_inheritors():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    weeks_rope = sue_beliefunit.make_rope(creg_rope, weeks_str())
    week_rope = sue_beliefunit.make_rope(creg_rope, week_str())
    sun_rope = sue_beliefunit.make_rope(week_rope, get_sun())
    day_rope = sue_beliefunit.make_rope(creg_rope, day_str())
    c400_leap_rope = sue_beliefunit.make_rope(creg_rope, c400_leap_str())
    c400_clean_rope = sue_beliefunit.make_rope(c400_leap_rope, c400_clean_str())
    c100_clean_rope = sue_beliefunit.make_rope(c400_clean_rope, c100_str())
    yr4_leap_rope = sue_beliefunit.make_rope(c100_clean_rope, yr4_leap_str())
    yr4_clean_rope = sue_beliefunit.make_rope(yr4_leap_rope, yr4_clean_str())
    year_rope = sue_beliefunit.make_rope(yr4_clean_rope, year_str())
    jan_rope = sue_beliefunit.make_rope(year_rope, "January")

    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    assert sue_beliefunit._range_inheritors == {}

    # WHEN
    sue_beliefunit._set_plan_dict()
    sue_beliefunit._set_plantree_range_attrs()

    # THEN
    print(f"{sue_beliefunit._range_inheritors=}")
    assert sue_beliefunit._range_inheritors != {}
    assert day_rope in sue_beliefunit._range_inheritors
    assert weeks_rope in sue_beliefunit._range_inheritors
    assert week_rope in sue_beliefunit._range_inheritors
    assert sun_rope in sue_beliefunit._range_inheritors
    assert c400_leap_rope in sue_beliefunit._range_inheritors
    assert c400_clean_rope in sue_beliefunit._range_inheritors
    assert c100_clean_rope in sue_beliefunit._range_inheritors
    assert yr4_leap_rope in sue_beliefunit._range_inheritors
    assert yr4_clean_rope in sue_beliefunit._range_inheritors
    assert year_rope in sue_beliefunit._range_inheritors
    assert jan_rope in sue_beliefunit._range_inheritors


def test_BeliefUnit_set_plantree_range_attrs_Sets_day_plan_gogo_calc_stop_calc():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_beliefunit.make_rope(creg_rope, day_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    sue_beliefunit._set_plan_dict()
    assert sue_beliefunit.plan_exists(time_rope)
    assert sue_beliefunit.plan_exists(creg_rope)
    creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    assert creg_plan.begin == 0
    assert creg_plan.close == 1472657760
    assert sue_beliefunit.plan_exists(day_rope)
    day_plan = sue_beliefunit.get_plan_obj(day_rope)
    assert day_plan.denom == 1440
    assert not day_plan.gogo_calc
    assert not day_plan.stop_calc

    # WHEN
    sue_beliefunit._set_plantree_range_attrs()

    # THEN
    assert day_plan.gogo_calc == 0
    assert day_plan.stop_calc == 1440


def test_BeliefUnit_set_plantree_range_attrs_Sets_days_plan_gogo_calc_stop_calc():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    days_rope = sue_beliefunit.make_rope(creg_rope, days_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    sue_beliefunit._set_plan_dict()
    assert sue_beliefunit.plan_exists(days_rope)
    days_plan = sue_beliefunit.get_plan_obj(days_rope)
    assert days_plan.denom == 1440
    assert not days_plan.gogo_calc
    assert not days_plan.stop_calc

    # WHEN
    sue_beliefunit._set_plantree_range_attrs()

    # THEN
    assert days_plan.denom == 1440
    assert days_plan.gogo_calc == 0
    assert days_plan.stop_calc == 1022679


def test_BeliefUnit_set_plantree_range_attrs_Sets_weeks_plan_gogo_calc_stop_calc():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    weeks_rope = sue_beliefunit.make_rope(creg_rope, weeks_str())
    week_rope = sue_beliefunit.make_rope(creg_rope, week_str())
    sun_rope = sue_beliefunit.make_rope(week_rope, get_sun())
    mon_rope = sue_beliefunit.make_rope(week_rope, get_mon())
    tue_rope = sue_beliefunit.make_rope(week_rope, get_tue())
    wed_rope = sue_beliefunit.make_rope(week_rope, get_wed())
    thu_rope = sue_beliefunit.make_rope(week_rope, get_thu())
    fri_rope = sue_beliefunit.make_rope(week_rope, get_fri())
    sat_rope = sue_beliefunit.make_rope(week_rope, get_sat())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    sue_beliefunit._set_plan_dict()
    assert sue_beliefunit.plan_exists(weeks_rope)
    assert sue_beliefunit.plan_exists(sun_rope)
    assert sue_beliefunit.plan_exists(mon_rope)
    assert sue_beliefunit.plan_exists(tue_rope)
    assert sue_beliefunit.plan_exists(wed_rope)
    assert sue_beliefunit.plan_exists(thu_rope)
    assert sue_beliefunit.plan_exists(fri_rope)
    assert sue_beliefunit.plan_exists(sat_rope)
    weeks_plan = sue_beliefunit.get_plan_obj(weeks_rope)
    assert weeks_plan.denom == 10080
    assert not weeks_plan.gogo_calc
    assert not weeks_plan.stop_calc
    assert sue_beliefunit.plan_exists(week_rope)
    week_plan = sue_beliefunit.get_plan_obj(week_rope)
    assert week_plan.denom == 10080
    assert not week_plan.gogo_calc
    assert not week_plan.stop_calc

    # WHEN
    sue_beliefunit._set_plantree_range_attrs()

    # THEN
    assert weeks_plan.denom == 10080
    assert weeks_plan.gogo_calc == 0
    assert weeks_plan.stop_calc == 146097
    assert week_plan.gogo_calc == 0
    assert week_plan.stop_calc == 10080
    assert sue_beliefunit.get_plan_obj(sun_rope).gogo_calc == 5760
    assert sue_beliefunit.get_plan_obj(mon_rope).gogo_calc == 7200
    assert sue_beliefunit.get_plan_obj(tue_rope).gogo_calc == 8640
    assert sue_beliefunit.get_plan_obj(wed_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(thu_rope).gogo_calc == 1440
    assert sue_beliefunit.get_plan_obj(fri_rope).gogo_calc == 2880
    assert sue_beliefunit.get_plan_obj(sat_rope).gogo_calc == 4320
    assert sue_beliefunit.get_plan_obj(sun_rope).stop_calc == 7200
    assert sue_beliefunit.get_plan_obj(mon_rope).stop_calc == 8640
    assert sue_beliefunit.get_plan_obj(tue_rope).stop_calc == 10080
    assert sue_beliefunit.get_plan_obj(wed_rope).stop_calc == 1440
    assert sue_beliefunit.get_plan_obj(thu_rope).stop_calc == 2880
    assert sue_beliefunit.get_plan_obj(fri_rope).stop_calc == 4320
    assert sue_beliefunit.get_plan_obj(sat_rope).stop_calc == 5760


def test_BeliefUnit_set_plantree_range_attrs_Sets_c400_plan_gogo_calc_stop_calc():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    c400_leap_rope = sue_beliefunit.make_rope(creg_rope, c400_leap_str())
    # c400_clean_rope = sue_beliefunit.make_rope(c400_leap_rope, c400_clean_str())
    # c100_clean_rope = sue_beliefunit.make_rope(c400_clean_rope, c100_str())
    # yr4_leap_rope = sue_beliefunit.make_rope(c100_clean_rope, yr4_leap_str())
    # yr4_clean_rope = sue_beliefunit.make_rope(yr4_leap_rope, yr4_clean_str())
    # year_rope = sue_beliefunit.make_rope(yr4_clean_rope, year_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    sue_beliefunit._set_plan_dict()
    print(f"    {c400_leap_rope=}")
    assert sue_beliefunit.plan_exists(c400_leap_rope)
    c400_leap_plan = sue_beliefunit.get_plan_obj(c400_leap_rope)
    # assert year_plan.morph
    assert not c400_leap_plan.gogo_calc
    assert not c400_leap_plan.stop_calc

    # WHEN
    sue_beliefunit._set_plantree_range_attrs()

    # THEN
    # assert year_plan.denom == 525600
    # assert year_plan.gogo_calc == 0
    # assert year_plan.stop_calc == 525600
    difference_between_mar1_jan1 = 86400
    assert sue_beliefunit.get_plan_obj(c400_leap_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(c400_leap_rope).stop_calc == 210379680
    assert 1472657760 % sue_beliefunit.get_plan_obj(c400_leap_rope).stop_calc == 0


def test_BeliefUnit_set_plantree_range_attrs_Sets_years_plan_gogo_calc_stop_calc():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    c400_leap_rope = sue_beliefunit.make_rope(creg_rope, c400_leap_str())
    c400_clean_rope = sue_beliefunit.make_rope(c400_leap_rope, c400_clean_str())
    c100_clean_rope = sue_beliefunit.make_rope(c400_clean_rope, c100_str())
    yr4_leap_rope = sue_beliefunit.make_rope(c100_clean_rope, yr4_leap_str())
    yr4_clean_rope = sue_beliefunit.make_rope(yr4_leap_rope, yr4_clean_str())
    year_rope = sue_beliefunit.make_rope(yr4_clean_rope, year_str())
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)
    sue_beliefunit._set_plan_dict()
    print(f"    {year_rope=}")
    assert sue_beliefunit.plan_exists(year_rope)
    year_plan = sue_beliefunit.get_plan_obj(year_rope)
    # assert year_plan.morph
    assert not year_plan.gogo_calc
    assert not year_plan.stop_calc

    # WHEN
    sue_beliefunit._set_plantree_range_attrs()

    # THEN
    assert sue_beliefunit.get_plan_obj(creg_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(c400_leap_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(c400_clean_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(c100_clean_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(yr4_leap_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(yr4_clean_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(year_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(creg_rope).stop_calc == 1472657760
    assert sue_beliefunit.get_plan_obj(c400_leap_rope).stop_calc == 210379680
    assert sue_beliefunit.get_plan_obj(c400_clean_rope).stop_calc == 210378240
    assert sue_beliefunit.get_plan_obj(c100_clean_rope).stop_calc == 52594560
    assert sue_beliefunit.get_plan_obj(yr4_leap_rope).stop_calc == 2103840
    assert sue_beliefunit.get_plan_obj(yr4_clean_rope).stop_calc == 2102400
    assert sue_beliefunit.get_plan_obj(year_rope).stop_calc == 525600

    assert year_plan.denom == 525600
    assert year_plan.gogo_calc == 0
    assert year_plan.stop_calc == 525600

    jan_rope = sue_beliefunit.make_rope(year_rope, "January")
    feb_rope = sue_beliefunit.make_rope(year_rope, "February")
    mar_rope = sue_beliefunit.make_rope(year_rope, "March")
    apr_rope = sue_beliefunit.make_rope(year_rope, "April")
    may_rope = sue_beliefunit.make_rope(year_rope, "May")
    jun_rope = sue_beliefunit.make_rope(year_rope, "June")
    jul_rope = sue_beliefunit.make_rope(year_rope, "July")
    aug_rope = sue_beliefunit.make_rope(year_rope, "August")
    sep_rope = sue_beliefunit.make_rope(year_rope, "September")
    oct_rope = sue_beliefunit.make_rope(year_rope, "October")
    nov_rope = sue_beliefunit.make_rope(year_rope, "November")
    dec_rope = sue_beliefunit.make_rope(year_rope, "December")
    assert sue_beliefunit.get_plan_obj(jan_rope).gogo_calc == 440640
    assert sue_beliefunit.get_plan_obj(feb_rope).gogo_calc == 485280
    assert sue_beliefunit.get_plan_obj(mar_rope).gogo_calc == 0
    assert sue_beliefunit.get_plan_obj(apr_rope).gogo_calc == 44640
    assert sue_beliefunit.get_plan_obj(may_rope).gogo_calc == 87840
    assert sue_beliefunit.get_plan_obj(jun_rope).gogo_calc == 132480
    assert sue_beliefunit.get_plan_obj(jul_rope).gogo_calc == 175680
    assert sue_beliefunit.get_plan_obj(aug_rope).gogo_calc == 220320
    assert sue_beliefunit.get_plan_obj(sep_rope).gogo_calc == 264960
    assert sue_beliefunit.get_plan_obj(oct_rope).gogo_calc == 308160
    assert sue_beliefunit.get_plan_obj(nov_rope).gogo_calc == 352800
    assert sue_beliefunit.get_plan_obj(dec_rope).gogo_calc == 396000

    assert sue_beliefunit.get_plan_obj(jan_rope).stop_calc == 485280
    assert sue_beliefunit.get_plan_obj(feb_rope).stop_calc == 525600
    assert sue_beliefunit.get_plan_obj(mar_rope).stop_calc == 44640
    assert sue_beliefunit.get_plan_obj(apr_rope).stop_calc == 87840
    assert sue_beliefunit.get_plan_obj(may_rope).stop_calc == 132480
    assert sue_beliefunit.get_plan_obj(jun_rope).stop_calc == 175680
    assert sue_beliefunit.get_plan_obj(jul_rope).stop_calc == 220320
    assert sue_beliefunit.get_plan_obj(aug_rope).stop_calc == 264960
    assert sue_beliefunit.get_plan_obj(sep_rope).stop_calc == 308160
    assert sue_beliefunit.get_plan_obj(oct_rope).stop_calc == 352800
    assert sue_beliefunit.get_plan_obj(nov_rope).stop_calc == 396000
    assert sue_beliefunit.get_plan_obj(dec_rope).stop_calc == 440640
