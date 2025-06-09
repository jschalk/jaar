from src.a06_plan_logic.plan import planunit_shop
from src.a07_calendar_logic._test_util.a07_str import (
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
from src.a07_calendar_logic._test_util.calendar_examples import (
    add_time_creg_conceptunit,
    get_cregtime_str,
    get_fri,
    get_mon,
    get_sat,
    get_sun,
    get_thu,
    get_tue,
    get_wed,
)


def test_PlanUnit_set_concept_dict_SetsAll_range_inheritors():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    weeks_way = sue_planunit.make_way(creg_way, weeks_str())
    week_way = sue_planunit.make_way(creg_way, week_str())
    sun_way = sue_planunit.make_way(week_way, get_sun())
    day_way = sue_planunit.make_way(creg_way, day_str())
    c400_leap_way = sue_planunit.make_way(creg_way, c400_leap_str())
    c400_clean_way = sue_planunit.make_way(c400_leap_way, c400_clean_str())
    c100_clean_way = sue_planunit.make_way(c400_clean_way, c100_str())
    yr4_leap_way = sue_planunit.make_way(c100_clean_way, yr4_leap_str())
    yr4_clean_way = sue_planunit.make_way(yr4_leap_way, yr4_clean_str())
    year_way = sue_planunit.make_way(yr4_clean_way, year_str())
    jan_way = sue_planunit.make_way(year_way, "January")

    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    assert sue_planunit._range_inheritors == {}

    # WHEN
    sue_planunit._set_concept_dict()
    sue_planunit._set_concepttree_range_attrs()

    # THEN
    print(f"{sue_planunit._range_inheritors=}")
    assert sue_planunit._range_inheritors != {}
    assert day_way in sue_planunit._range_inheritors
    assert weeks_way in sue_planunit._range_inheritors
    assert week_way in sue_planunit._range_inheritors
    assert sun_way in sue_planunit._range_inheritors
    assert c400_leap_way in sue_planunit._range_inheritors
    assert c400_clean_way in sue_planunit._range_inheritors
    assert c100_clean_way in sue_planunit._range_inheritors
    assert yr4_leap_way in sue_planunit._range_inheritors
    assert yr4_clean_way in sue_planunit._range_inheritors
    assert year_way in sue_planunit._range_inheritors
    assert jan_way in sue_planunit._range_inheritors


def test_PlanUnit_set_concepttree_range_attrs_Sets_day_concept_gogo_calc_stop_calc():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    day_way = sue_planunit.make_way(creg_way, day_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    sue_planunit._set_concept_dict()
    assert sue_planunit.concept_exists(time_way)
    assert sue_planunit.concept_exists(creg_way)
    creg_concept = sue_planunit.get_concept_obj(creg_way)
    assert creg_concept.begin == 0
    assert creg_concept.close == 1472657760
    assert sue_planunit.concept_exists(day_way)
    day_concept = sue_planunit.get_concept_obj(day_way)
    assert day_concept.denom == 1440
    assert not day_concept._gogo_calc
    assert not day_concept._stop_calc

    # WHEN
    sue_planunit._set_concepttree_range_attrs()

    # THEN
    assert day_concept._gogo_calc == 0
    assert day_concept._stop_calc == 1440


def test_PlanUnit_set_concepttree_range_attrs_Sets_days_concept_gogo_calc_stop_calc():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    days_way = sue_planunit.make_way(creg_way, days_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    sue_planunit._set_concept_dict()
    assert sue_planunit.concept_exists(days_way)
    days_concept = sue_planunit.get_concept_obj(days_way)
    assert days_concept.denom == 1440
    assert not days_concept._gogo_calc
    assert not days_concept._stop_calc

    # WHEN
    sue_planunit._set_concepttree_range_attrs()

    # THEN
    assert days_concept.denom == 1440
    assert days_concept._gogo_calc == 0
    assert days_concept._stop_calc == 1022679


def test_PlanUnit_set_concepttree_range_attrs_Sets_weeks_concept_gogo_calc_stop_calc():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    weeks_way = sue_planunit.make_way(creg_way, weeks_str())
    week_way = sue_planunit.make_way(creg_way, week_str())
    sun_way = sue_planunit.make_way(week_way, get_sun())
    mon_way = sue_planunit.make_way(week_way, get_mon())
    tue_way = sue_planunit.make_way(week_way, get_tue())
    wed_way = sue_planunit.make_way(week_way, get_wed())
    thu_way = sue_planunit.make_way(week_way, get_thu())
    fri_way = sue_planunit.make_way(week_way, get_fri())
    sat_way = sue_planunit.make_way(week_way, get_sat())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    sue_planunit._set_concept_dict()
    assert sue_planunit.concept_exists(weeks_way)
    assert sue_planunit.concept_exists(sun_way)
    assert sue_planunit.concept_exists(mon_way)
    assert sue_planunit.concept_exists(tue_way)
    assert sue_planunit.concept_exists(wed_way)
    assert sue_planunit.concept_exists(thu_way)
    assert sue_planunit.concept_exists(fri_way)
    assert sue_planunit.concept_exists(sat_way)
    weeks_concept = sue_planunit.get_concept_obj(weeks_way)
    assert weeks_concept.denom == 10080
    assert not weeks_concept._gogo_calc
    assert not weeks_concept._stop_calc
    assert sue_planunit.concept_exists(week_way)
    week_concept = sue_planunit.get_concept_obj(week_way)
    assert week_concept.denom == 10080
    assert not week_concept._gogo_calc
    assert not week_concept._stop_calc

    # WHEN
    sue_planunit._set_concepttree_range_attrs()

    # THEN
    assert weeks_concept.denom == 10080
    assert weeks_concept._gogo_calc == 0
    assert weeks_concept._stop_calc == 146097
    assert week_concept._gogo_calc == 0
    assert week_concept._stop_calc == 10080
    assert sue_planunit.get_concept_obj(sun_way)._gogo_calc == 5760
    assert sue_planunit.get_concept_obj(mon_way)._gogo_calc == 7200
    assert sue_planunit.get_concept_obj(tue_way)._gogo_calc == 8640
    assert sue_planunit.get_concept_obj(wed_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(thu_way)._gogo_calc == 1440
    assert sue_planunit.get_concept_obj(fri_way)._gogo_calc == 2880
    assert sue_planunit.get_concept_obj(sat_way)._gogo_calc == 4320
    assert sue_planunit.get_concept_obj(sun_way)._stop_calc == 7200
    assert sue_planunit.get_concept_obj(mon_way)._stop_calc == 8640
    assert sue_planunit.get_concept_obj(tue_way)._stop_calc == 10080
    assert sue_planunit.get_concept_obj(wed_way)._stop_calc == 1440
    assert sue_planunit.get_concept_obj(thu_way)._stop_calc == 2880
    assert sue_planunit.get_concept_obj(fri_way)._stop_calc == 4320
    assert sue_planunit.get_concept_obj(sat_way)._stop_calc == 5760


def test_PlanUnit_set_concepttree_range_attrs_Sets_c400_concept_gogo_calc_stop_calc():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    c400_leap_way = sue_planunit.make_way(creg_way, c400_leap_str())
    # c400_clean_way = sue_planunit.make_way(c400_leap_way, c400_clean_str())
    # c100_clean_way = sue_planunit.make_way(c400_clean_way, c100_str())
    # yr4_leap_way = sue_planunit.make_way(c100_clean_way, yr4_leap_str())
    # yr4_clean_way = sue_planunit.make_way(yr4_leap_way, yr4_clean_str())
    # year_way = sue_planunit.make_way(yr4_clean_way, year_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    sue_planunit._set_concept_dict()
    print(f"    {c400_leap_way=}")
    assert sue_planunit.concept_exists(c400_leap_way)
    c400_leap_concept = sue_planunit.get_concept_obj(c400_leap_way)
    # assert year_concept.morph
    assert not c400_leap_concept._gogo_calc
    assert not c400_leap_concept._stop_calc

    # WHEN
    sue_planunit._set_concepttree_range_attrs()

    # THEN
    # assert year_concept.denom == 525600
    # assert year_concept._gogo_calc == 0
    # assert year_concept._stop_calc == 525600
    difference_between_mar1_jan1 = 86400
    assert sue_planunit.get_concept_obj(c400_leap_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(c400_leap_way)._stop_calc == 210379680
    assert 1472657760 % sue_planunit.get_concept_obj(c400_leap_way)._stop_calc == 0


def test_PlanUnit_set_concepttree_range_attrs_Sets_years_concept_gogo_calc_stop_calc():
    # ESTABLISH
    sue_planunit = planunit_shop("Sue")
    time_way = sue_planunit.make_l1_way(time_str())
    creg_way = sue_planunit.make_way(time_way, get_cregtime_str())
    c400_leap_way = sue_planunit.make_way(creg_way, c400_leap_str())
    c400_clean_way = sue_planunit.make_way(c400_leap_way, c400_clean_str())
    c100_clean_way = sue_planunit.make_way(c400_clean_way, c100_str())
    yr4_leap_way = sue_planunit.make_way(c100_clean_way, yr4_leap_str())
    yr4_clean_way = sue_planunit.make_way(yr4_leap_way, yr4_clean_str())
    year_way = sue_planunit.make_way(yr4_clean_way, year_str())
    sue_planunit = add_time_creg_conceptunit(sue_planunit)
    sue_planunit._set_concept_dict()
    print(f"    {year_way=}")
    assert sue_planunit.concept_exists(year_way)
    year_concept = sue_planunit.get_concept_obj(year_way)
    # assert year_concept.morph
    assert not year_concept._gogo_calc
    assert not year_concept._stop_calc

    # WHEN
    sue_planunit._set_concepttree_range_attrs()

    # THEN
    assert sue_planunit.get_concept_obj(creg_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(c400_leap_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(c400_clean_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(c100_clean_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(yr4_leap_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(yr4_clean_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(year_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(creg_way)._stop_calc == 1472657760
    assert sue_planunit.get_concept_obj(c400_leap_way)._stop_calc == 210379680
    assert sue_planunit.get_concept_obj(c400_clean_way)._stop_calc == 210378240
    assert sue_planunit.get_concept_obj(c100_clean_way)._stop_calc == 52594560
    assert sue_planunit.get_concept_obj(yr4_leap_way)._stop_calc == 2103840
    assert sue_planunit.get_concept_obj(yr4_clean_way)._stop_calc == 2102400
    assert sue_planunit.get_concept_obj(year_way)._stop_calc == 525600

    assert year_concept.denom == 525600
    assert year_concept._gogo_calc == 0
    assert year_concept._stop_calc == 525600

    jan_way = sue_planunit.make_way(year_way, "January")
    feb_way = sue_planunit.make_way(year_way, "February")
    mar_way = sue_planunit.make_way(year_way, "March")
    apr_way = sue_planunit.make_way(year_way, "April")
    may_way = sue_planunit.make_way(year_way, "May")
    jun_way = sue_planunit.make_way(year_way, "June")
    jul_way = sue_planunit.make_way(year_way, "July")
    aug_way = sue_planunit.make_way(year_way, "August")
    sep_way = sue_planunit.make_way(year_way, "September")
    oct_way = sue_planunit.make_way(year_way, "October")
    nov_way = sue_planunit.make_way(year_way, "November")
    dec_way = sue_planunit.make_way(year_way, "December")
    assert sue_planunit.get_concept_obj(jan_way)._gogo_calc == 440640
    assert sue_planunit.get_concept_obj(feb_way)._gogo_calc == 485280
    assert sue_planunit.get_concept_obj(mar_way)._gogo_calc == 0
    assert sue_planunit.get_concept_obj(apr_way)._gogo_calc == 44640
    assert sue_planunit.get_concept_obj(may_way)._gogo_calc == 87840
    assert sue_planunit.get_concept_obj(jun_way)._gogo_calc == 132480
    assert sue_planunit.get_concept_obj(jul_way)._gogo_calc == 175680
    assert sue_planunit.get_concept_obj(aug_way)._gogo_calc == 220320
    assert sue_planunit.get_concept_obj(sep_way)._gogo_calc == 264960
    assert sue_planunit.get_concept_obj(oct_way)._gogo_calc == 308160
    assert sue_planunit.get_concept_obj(nov_way)._gogo_calc == 352800
    assert sue_planunit.get_concept_obj(dec_way)._gogo_calc == 396000

    assert sue_planunit.get_concept_obj(jan_way)._stop_calc == 485280
    assert sue_planunit.get_concept_obj(feb_way)._stop_calc == 525600
    assert sue_planunit.get_concept_obj(mar_way)._stop_calc == 44640
    assert sue_planunit.get_concept_obj(apr_way)._stop_calc == 87840
    assert sue_planunit.get_concept_obj(may_way)._stop_calc == 132480
    assert sue_planunit.get_concept_obj(jun_way)._stop_calc == 175680
    assert sue_planunit.get_concept_obj(jul_way)._stop_calc == 220320
    assert sue_planunit.get_concept_obj(aug_way)._stop_calc == 264960
    assert sue_planunit.get_concept_obj(sep_way)._stop_calc == 308160
    assert sue_planunit.get_concept_obj(oct_way)._stop_calc == 352800
    assert sue_planunit.get_concept_obj(nov_way)._stop_calc == 396000
    assert sue_planunit.get_concept_obj(dec_way)._stop_calc == 440640
