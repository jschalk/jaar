from datetime import datetime
from src.ch00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.ch04_group_logic.group import awardunit_shop
from src.ch05_reason_logic.reason import reasonunit_shop
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_timeline_logic._ref.ch08_terms import (
    c100_str,
    c400_clean_str,
    c400_leap_str,
    day_str,
    days_str,
    hour_str,
    monthday_distortion_str,
    time_str,
    week_str,
    weeks_str,
    year_str,
    yr1_jan1_offset_str,
    yr4_clean_str,
    yr4_leap_str,
)
from src.ch08_timeline_logic.test._util.calendar_examples import (
    add_time_creg_planunit,
    add_time_five_planunit,
    creg_hour_int_label,
    creg_str,
    creg_weekday_planunits,
    cregtime_planunit,
    display_current_creg_five_min,
    five_str,
    get_creg_config,
    get_creg_min_from_dt,
    get_cregtime_str,
    get_five_config,
    get_five_min_from_dt,
    get_fri,
    get_mon,
    get_sat,
    get_sun,
    get_thu,
    get_tue,
    get_wed,
)
from src.ch08_timeline_logic.timeline_main import (
    add_newtimeline_planunit,
    get_c400_constants,
    get_min_from_dt,
    get_timeline_min_difference,
    get_year_rope,
)


def test_get_creg_config_ReturnsObj():
    # ESTABLISH
    creg_config = get_creg_config()
    five_config = get_five_config()

    # WHEN
    creg_offset = creg_config.get(yr1_jan1_offset_str())
    five_offset = five_config.get(yr1_jan1_offset_str())

    # THEN
    assert creg_offset == 440640
    assert five_offset == 1683478080
    c400_len = get_c400_constants().c400_leap_length
    assert five_offset == (c400_len * 8) + 440640
    assert creg_config.get(monthday_distortion_str()) == 1
    assert five_config.get(monthday_distortion_str()) == 0


def test_cregtime_planunit_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert cregtime_planunit().begin == 0
    assert cregtime_planunit().close == 1472657760
    assert cregtime_planunit().close == get_c400_constants().c400_leap_length * 7


def test_creg_weekday_planunits_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert creg_weekday_planunits().get(get_wed()).gogo_want == 0
    assert creg_weekday_planunits().get(get_thu()).gogo_want == 1440
    assert creg_weekday_planunits().get(get_fri()).gogo_want == 2880
    assert creg_weekday_planunits().get(get_sat()).gogo_want == 4320
    assert creg_weekday_planunits().get(get_sun()).gogo_want == 5760
    assert creg_weekday_planunits().get(get_mon()).gogo_want == 7200
    assert creg_weekday_planunits().get(get_tue()).gogo_want == 8640
    assert creg_weekday_planunits().get(get_wed()).stop_want == 1440
    assert creg_weekday_planunits().get(get_thu()).stop_want == 2880
    assert creg_weekday_planunits().get(get_fri()).stop_want == 4320
    assert creg_weekday_planunits().get(get_sat()).stop_want == 5760
    assert creg_weekday_planunits().get(get_sun()).stop_want == 7200
    assert creg_weekday_planunits().get(get_mon()).stop_want == 8640
    assert creg_weekday_planunits().get(get_tue()).stop_want == 10080


def test_add_time_creg_planunit_ReturnsObjWith_days():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_beliefunit.make_rope(creg_rope, day_str())
    days_rope = sue_beliefunit.make_rope(creg_rope, days_str())
    print(f"{time_rope=}")
    print(f"{creg_rope=}")
    print(f"{day_rope=}")
    assert not sue_beliefunit.plan_exists(time_rope)
    assert not sue_beliefunit.plan_exists(creg_rope)
    assert not sue_beliefunit.plan_exists(day_rope)
    assert not sue_beliefunit.plan_exists(days_rope)

    # WHEN
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)

    # THEN
    assert sue_beliefunit.plan_exists(time_rope)
    assert sue_beliefunit.plan_exists(creg_rope)
    assert sue_beliefunit.plan_exists(day_rope)
    assert sue_beliefunit.plan_exists(days_rope)
    assert sue_beliefunit.get_plan_obj(creg_rope).begin == 0
    assert sue_beliefunit.get_plan_obj(creg_rope).close == 1472657760
    assert sue_beliefunit.get_plan_obj(day_rope).denom == 1440
    assert sue_beliefunit.get_plan_obj(day_rope).morph
    assert sue_beliefunit.get_plan_obj(days_rope).denom == 1440
    assert sue_beliefunit.get_plan_obj(days_rope).morph is None


def test_add_time_creg_planunit_ReturnsObjWith_weeks():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    week_rope = sue_beliefunit.make_rope(creg_rope, week_str())
    sun_rope = sue_beliefunit.make_rope(week_rope, get_sun())
    mon_rope = sue_beliefunit.make_rope(week_rope, get_mon())
    tue_rope = sue_beliefunit.make_rope(week_rope, get_tue())
    wed_rope = sue_beliefunit.make_rope(week_rope, get_wed())
    thu_rope = sue_beliefunit.make_rope(week_rope, get_thu())
    fri_rope = sue_beliefunit.make_rope(week_rope, get_fri())
    sat_rope = sue_beliefunit.make_rope(week_rope, get_sat())
    weeks_rope = sue_beliefunit.make_rope(creg_rope, weeks_str())

    assert not sue_beliefunit.plan_exists(week_rope)
    assert not sue_beliefunit.plan_exists(sun_rope)
    assert not sue_beliefunit.plan_exists(mon_rope)
    assert not sue_beliefunit.plan_exists(tue_rope)
    assert not sue_beliefunit.plan_exists(wed_rope)
    assert not sue_beliefunit.plan_exists(thu_rope)
    assert not sue_beliefunit.plan_exists(fri_rope)
    assert not sue_beliefunit.plan_exists(sat_rope)
    assert not sue_beliefunit.plan_exists(weeks_rope)

    # WHEN
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)

    # THEN
    assert sue_beliefunit.plan_exists(week_rope)
    assert sue_beliefunit.get_plan_obj(week_rope).gogo_want is None
    assert sue_beliefunit.get_plan_obj(week_rope).stop_want is None
    assert sue_beliefunit.get_plan_obj(week_rope).denom == 10080
    assert sue_beliefunit.get_plan_obj(week_rope).morph
    assert sue_beliefunit.plan_exists(sun_rope)
    assert sue_beliefunit.plan_exists(mon_rope)
    assert sue_beliefunit.plan_exists(tue_rope)
    assert sue_beliefunit.plan_exists(wed_rope)
    assert sue_beliefunit.plan_exists(thu_rope)
    assert sue_beliefunit.plan_exists(fri_rope)
    assert sue_beliefunit.plan_exists(sat_rope)
    assert sue_beliefunit.plan_exists(weeks_rope)
    assert sue_beliefunit.get_plan_obj(weeks_rope).denom == 10080
    assert sue_beliefunit.get_plan_obj(weeks_rope).morph is None


def test_add_time_creg_planunit_ReturnsObjWith_c400_leap_rope():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    c400_leap_rope = sue_beliefunit.make_rope(creg_rope, c400_leap_str())
    c400_clean_rope = sue_beliefunit.make_rope(c400_leap_rope, c400_clean_str())
    c100_rope = sue_beliefunit.make_rope(c400_clean_rope, c100_str())
    yr4_leap_rope = sue_beliefunit.make_rope(c100_rope, yr4_leap_str())
    yr4_clean_rope = sue_beliefunit.make_rope(yr4_leap_rope, yr4_clean_str())
    year_rope = sue_beliefunit.make_rope(yr4_clean_rope, year_str())

    assert not sue_beliefunit.plan_exists(c400_leap_rope)

    # WHEN
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)

    # THEN
    assert sue_beliefunit.plan_exists(c400_leap_rope)
    c400_leap_plan = sue_beliefunit.get_plan_obj(c400_leap_rope)
    assert not c400_leap_plan.gogo_want
    assert not c400_leap_plan.stop_want
    assert c400_leap_plan.denom == 210379680
    assert c400_leap_plan.morph

    assert sue_beliefunit.plan_exists(c400_clean_rope)
    c400_clean_plan = sue_beliefunit.get_plan_obj(c400_clean_rope)
    assert not c400_clean_plan.gogo_want
    assert not c400_clean_plan.stop_want
    assert c400_clean_plan.denom == 210378240
    assert c400_clean_plan.morph

    assert sue_beliefunit.plan_exists(c100_rope)
    c100_plan = sue_beliefunit.get_plan_obj(c100_rope)
    assert not c100_plan.gogo_want
    assert not c100_plan.stop_want
    assert c100_plan.denom == 52594560
    assert c100_plan.morph

    assert sue_beliefunit.plan_exists(yr4_leap_rope)
    yr4_leap_plan = sue_beliefunit.get_plan_obj(yr4_leap_rope)
    assert not yr4_leap_plan.gogo_want
    assert not yr4_leap_plan.stop_want
    assert yr4_leap_plan.denom == 2103840
    assert yr4_leap_plan.morph

    assert sue_beliefunit.plan_exists(yr4_clean_rope)
    yr4_clean_plan = sue_beliefunit.get_plan_obj(yr4_clean_rope)
    assert not yr4_clean_plan.gogo_want
    assert not yr4_clean_plan.stop_want
    assert yr4_clean_plan.denom == 2102400
    assert yr4_clean_plan.morph

    assert sue_beliefunit.plan_exists(year_rope)
    year_plan = sue_beliefunit.get_plan_obj(year_rope)
    assert not year_plan.gogo_want
    assert not year_plan.stop_want
    assert year_plan.denom == 525600
    assert year_plan.morph


def test_add_time_creg_planunit_ReturnsObjWith_years():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    year_rope = get_year_rope(sue_beliefunit, creg_rope)

    assert not sue_beliefunit.plan_exists(creg_rope)
    assert not sue_beliefunit.plan_exists(year_rope)

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
    assert not sue_beliefunit.plan_exists(jan_rope)
    assert not sue_beliefunit.plan_exists(feb_rope)
    assert not sue_beliefunit.plan_exists(mar_rope)
    assert not sue_beliefunit.plan_exists(apr_rope)
    assert not sue_beliefunit.plan_exists(may_rope)
    assert not sue_beliefunit.plan_exists(jun_rope)
    assert not sue_beliefunit.plan_exists(jul_rope)
    assert not sue_beliefunit.plan_exists(aug_rope)
    assert not sue_beliefunit.plan_exists(sep_rope)
    assert not sue_beliefunit.plan_exists(oct_rope)
    assert not sue_beliefunit.plan_exists(nov_rope)
    assert not sue_beliefunit.plan_exists(dec_rope)
    assert not sue_beliefunit.plan_exists(year_rope)

    # WHEN
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)

    # THEN
    assert sue_beliefunit.plan_exists(creg_rope)
    assert sue_beliefunit.plan_exists(year_rope)

    year_plan = sue_beliefunit.get_plan_obj(year_rope)
    # assert year_plan.morph
    assert sue_beliefunit.plan_exists(jan_rope)
    assert sue_beliefunit.plan_exists(feb_rope)
    assert sue_beliefunit.plan_exists(mar_rope)
    assert sue_beliefunit.plan_exists(apr_rope)
    assert sue_beliefunit.plan_exists(may_rope)
    assert sue_beliefunit.plan_exists(jun_rope)
    assert sue_beliefunit.plan_exists(jul_rope)
    assert sue_beliefunit.plan_exists(aug_rope)
    assert sue_beliefunit.plan_exists(sep_rope)
    assert sue_beliefunit.plan_exists(oct_rope)
    assert sue_beliefunit.plan_exists(nov_rope)
    assert sue_beliefunit.plan_exists(dec_rope)
    assert sue_beliefunit.get_plan_obj(jan_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(feb_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(mar_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(apr_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(may_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(jun_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(jul_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(aug_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(sep_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(oct_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(nov_rope).addin == 1440
    assert sue_beliefunit.get_plan_obj(dec_rope).addin == 1440

    assert sue_beliefunit.get_plan_obj(jan_rope).gogo_want == 440640
    assert sue_beliefunit.get_plan_obj(feb_rope).gogo_want == 485280
    assert sue_beliefunit.get_plan_obj(mar_rope).gogo_want == 0
    assert sue_beliefunit.get_plan_obj(apr_rope).gogo_want == 44640
    assert sue_beliefunit.get_plan_obj(may_rope).gogo_want == 87840
    assert sue_beliefunit.get_plan_obj(jun_rope).gogo_want == 132480
    assert sue_beliefunit.get_plan_obj(jul_rope).gogo_want == 175680
    assert sue_beliefunit.get_plan_obj(aug_rope).gogo_want == 220320
    assert sue_beliefunit.get_plan_obj(sep_rope).gogo_want == 264960
    assert sue_beliefunit.get_plan_obj(oct_rope).gogo_want == 308160
    assert sue_beliefunit.get_plan_obj(nov_rope).gogo_want == 352800
    assert sue_beliefunit.get_plan_obj(dec_rope).gogo_want == 396000

    assert sue_beliefunit.get_plan_obj(jan_rope).stop_want == 485280
    assert sue_beliefunit.get_plan_obj(feb_rope).stop_want == 525600
    assert sue_beliefunit.get_plan_obj(mar_rope).stop_want == 44640
    assert sue_beliefunit.get_plan_obj(apr_rope).stop_want == 87840
    assert sue_beliefunit.get_plan_obj(may_rope).stop_want == 132480
    assert sue_beliefunit.get_plan_obj(jun_rope).stop_want == 175680
    assert sue_beliefunit.get_plan_obj(jul_rope).stop_want == 220320
    assert sue_beliefunit.get_plan_obj(aug_rope).stop_want == 264960
    assert sue_beliefunit.get_plan_obj(sep_rope).stop_want == 308160
    assert sue_beliefunit.get_plan_obj(oct_rope).stop_want == 352800
    assert sue_beliefunit.get_plan_obj(nov_rope).stop_want == 396000
    assert sue_beliefunit.get_plan_obj(dec_rope).stop_want == 440640


def test_add_time_creg_planunit_ReturnsObjWith_c400_leap():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_beliefunit.make_rope(creg_rope, day_str())
    days_rope = sue_beliefunit.make_rope(creg_rope, days_str())
    print(f"{time_rope=}")
    print(f"{creg_rope=}")
    print(f"{day_rope=}")
    assert not sue_beliefunit.plan_exists(time_rope)
    assert not sue_beliefunit.plan_exists(creg_rope)
    assert not sue_beliefunit.plan_exists(day_rope)
    assert not sue_beliefunit.plan_exists(days_rope)

    # WHEN
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)

    # THEN
    assert sue_beliefunit.plan_exists(time_rope)
    assert sue_beliefunit.plan_exists(creg_rope)
    creg_plan = sue_beliefunit.get_plan_obj(creg_rope)
    assert creg_plan.begin == 0
    assert creg_plan.close == 1472657760
    assert sue_beliefunit.plan_exists(day_rope)
    day_plan = sue_beliefunit.get_plan_obj(day_rope)
    assert day_plan.denom == 1440
    assert day_plan.morph
    assert sue_beliefunit.plan_exists(days_rope)
    days_plan = sue_beliefunit.get_plan_obj(days_rope)
    assert days_plan.denom == 1440
    assert not days_plan.morph


def test_add_time_creg_planunit_ReturnsObjWith_hours():
    # ESTABLISH
    sue_beliefunit = beliefunit_shop("Sue")
    time_rope = sue_beliefunit.make_l1_rope(time_str())
    creg_rope = sue_beliefunit.make_rope(time_rope, get_cregtime_str())
    day_rope = sue_beliefunit.make_rope(creg_rope, day_str())
    hour_rope = sue_beliefunit.make_rope(day_rope, hour_str())
    hr_00_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(0))
    hr_01_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(1))
    hr_02_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(2))
    hr_03_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(3))
    hr_04_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(4))
    hr_05_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(5))
    hr_06_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(6))
    hr_07_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(7))
    hr_08_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(8))
    hr_09_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(9))
    hr_10_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(10))
    hr_11_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(11))
    hr_12_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(12))
    hr_13_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(13))
    hr_14_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(14))
    hr_15_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(15))
    hr_16_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(16))
    hr_17_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(17))
    hr_18_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(18))
    hr_19_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(19))
    hr_20_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(20))
    hr_21_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(21))
    hr_22_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(22))
    hr_23_rope = sue_beliefunit.make_rope(day_rope, creg_hour_int_label(23))

    print(f"{day_rope=}")
    print(f"{hr_00_rope=}")
    assert not sue_beliefunit.plan_exists(time_rope)
    assert not sue_beliefunit.plan_exists(creg_rope)
    assert not sue_beliefunit.plan_exists(day_rope)
    assert not sue_beliefunit.plan_exists(hr_00_rope)
    assert not sue_beliefunit.plan_exists(hr_01_rope)
    assert not sue_beliefunit.plan_exists(hr_02_rope)
    assert not sue_beliefunit.plan_exists(hr_03_rope)
    assert not sue_beliefunit.plan_exists(hr_04_rope)
    assert not sue_beliefunit.plan_exists(hr_05_rope)
    assert not sue_beliefunit.plan_exists(hr_06_rope)
    assert not sue_beliefunit.plan_exists(hr_07_rope)
    assert not sue_beliefunit.plan_exists(hr_08_rope)
    assert not sue_beliefunit.plan_exists(hr_09_rope)
    assert not sue_beliefunit.plan_exists(hr_10_rope)
    assert not sue_beliefunit.plan_exists(hr_11_rope)
    assert not sue_beliefunit.plan_exists(hr_12_rope)
    assert not sue_beliefunit.plan_exists(hr_13_rope)
    assert not sue_beliefunit.plan_exists(hr_14_rope)
    assert not sue_beliefunit.plan_exists(hr_15_rope)
    assert not sue_beliefunit.plan_exists(hr_16_rope)
    assert not sue_beliefunit.plan_exists(hr_17_rope)
    assert not sue_beliefunit.plan_exists(hr_18_rope)
    assert not sue_beliefunit.plan_exists(hr_19_rope)
    assert not sue_beliefunit.plan_exists(hr_20_rope)
    assert not sue_beliefunit.plan_exists(hr_21_rope)
    assert not sue_beliefunit.plan_exists(hr_22_rope)
    assert not sue_beliefunit.plan_exists(hr_23_rope)

    # WHEN
    sue_beliefunit = add_time_creg_planunit(sue_beliefunit)

    # THEN
    day_plan = sue_beliefunit.get_plan_obj(day_rope)
    print(f"{day_plan.kids.keys()=}")
    assert sue_beliefunit.plan_exists(time_rope)
    assert sue_beliefunit.plan_exists(creg_rope)
    assert sue_beliefunit.plan_exists(day_rope)
    # assert sue_beliefunit.get_plan_obj(hour_rope).denom == 60
    # assert sue_beliefunit.get_plan_obj(hour_rope).morph
    # assert not sue_beliefunit.get_plan_obj(hour_rope).gogo_want
    # assert not sue_beliefunit.get_plan_obj(hour_rope).stop_want
    assert sue_beliefunit.plan_exists(hr_00_rope)
    assert sue_beliefunit.plan_exists(hr_01_rope)
    assert sue_beliefunit.plan_exists(hr_02_rope)
    assert sue_beliefunit.plan_exists(hr_03_rope)
    assert sue_beliefunit.plan_exists(hr_04_rope)
    assert sue_beliefunit.plan_exists(hr_05_rope)
    assert sue_beliefunit.plan_exists(hr_06_rope)
    assert sue_beliefunit.plan_exists(hr_07_rope)
    assert sue_beliefunit.plan_exists(hr_08_rope)
    assert sue_beliefunit.plan_exists(hr_09_rope)
    assert sue_beliefunit.plan_exists(hr_10_rope)
    assert sue_beliefunit.plan_exists(hr_11_rope)
    assert sue_beliefunit.plan_exists(hr_12_rope)
    assert sue_beliefunit.plan_exists(hr_13_rope)
    assert sue_beliefunit.plan_exists(hr_14_rope)
    assert sue_beliefunit.plan_exists(hr_15_rope)
    assert sue_beliefunit.plan_exists(hr_16_rope)
    assert sue_beliefunit.plan_exists(hr_17_rope)
    assert sue_beliefunit.plan_exists(hr_18_rope)
    assert sue_beliefunit.plan_exists(hr_19_rope)
    assert sue_beliefunit.plan_exists(hr_20_rope)
    assert sue_beliefunit.plan_exists(hr_21_rope)
    assert sue_beliefunit.plan_exists(hr_22_rope)
    assert sue_beliefunit.plan_exists(hr_23_rope)
    assert sue_beliefunit.get_plan_obj(hr_00_rope).gogo_want == 0
    assert sue_beliefunit.get_plan_obj(hr_01_rope).gogo_want == 60
    assert sue_beliefunit.get_plan_obj(hr_02_rope).gogo_want == 120
    assert sue_beliefunit.get_plan_obj(hr_03_rope).gogo_want == 180
    assert sue_beliefunit.get_plan_obj(hr_04_rope).gogo_want == 240
    assert sue_beliefunit.get_plan_obj(hr_05_rope).gogo_want == 300
    assert sue_beliefunit.get_plan_obj(hr_06_rope).gogo_want == 360
    assert sue_beliefunit.get_plan_obj(hr_07_rope).gogo_want == 420
    assert sue_beliefunit.get_plan_obj(hr_08_rope).gogo_want == 480
    assert sue_beliefunit.get_plan_obj(hr_09_rope).gogo_want == 540
    assert sue_beliefunit.get_plan_obj(hr_10_rope).gogo_want == 600
    assert sue_beliefunit.get_plan_obj(hr_11_rope).gogo_want == 660
    assert sue_beliefunit.get_plan_obj(hr_12_rope).gogo_want == 720
    assert sue_beliefunit.get_plan_obj(hr_13_rope).gogo_want == 780
    assert sue_beliefunit.get_plan_obj(hr_14_rope).gogo_want == 840
    assert sue_beliefunit.get_plan_obj(hr_15_rope).gogo_want == 900
    assert sue_beliefunit.get_plan_obj(hr_16_rope).gogo_want == 960
    assert sue_beliefunit.get_plan_obj(hr_17_rope).gogo_want == 1020
    assert sue_beliefunit.get_plan_obj(hr_18_rope).gogo_want == 1080
    assert sue_beliefunit.get_plan_obj(hr_19_rope).gogo_want == 1140
    assert sue_beliefunit.get_plan_obj(hr_20_rope).gogo_want == 1200
    assert sue_beliefunit.get_plan_obj(hr_21_rope).gogo_want == 1260
    assert sue_beliefunit.get_plan_obj(hr_22_rope).gogo_want == 1320
    assert sue_beliefunit.get_plan_obj(hr_23_rope).gogo_want == 1380
    assert sue_beliefunit.get_plan_obj(hr_00_rope).stop_want == 60
    assert sue_beliefunit.get_plan_obj(hr_01_rope).stop_want == 120
    assert sue_beliefunit.get_plan_obj(hr_02_rope).stop_want == 180
    assert sue_beliefunit.get_plan_obj(hr_03_rope).stop_want == 240
    assert sue_beliefunit.get_plan_obj(hr_04_rope).stop_want == 300
    assert sue_beliefunit.get_plan_obj(hr_05_rope).stop_want == 360
    assert sue_beliefunit.get_plan_obj(hr_06_rope).stop_want == 420
    assert sue_beliefunit.get_plan_obj(hr_07_rope).stop_want == 480
    assert sue_beliefunit.get_plan_obj(hr_08_rope).stop_want == 540
    assert sue_beliefunit.get_plan_obj(hr_09_rope).stop_want == 600
    assert sue_beliefunit.get_plan_obj(hr_10_rope).stop_want == 660
    assert sue_beliefunit.get_plan_obj(hr_11_rope).stop_want == 720
    assert sue_beliefunit.get_plan_obj(hr_12_rope).stop_want == 780
    assert sue_beliefunit.get_plan_obj(hr_13_rope).stop_want == 840
    assert sue_beliefunit.get_plan_obj(hr_14_rope).stop_want == 900
    assert sue_beliefunit.get_plan_obj(hr_15_rope).stop_want == 960
    assert sue_beliefunit.get_plan_obj(hr_16_rope).stop_want == 1020
    assert sue_beliefunit.get_plan_obj(hr_17_rope).stop_want == 1080
    assert sue_beliefunit.get_plan_obj(hr_18_rope).stop_want == 1140
    assert sue_beliefunit.get_plan_obj(hr_19_rope).stop_want == 1200
    assert sue_beliefunit.get_plan_obj(hr_20_rope).stop_want == 1260
    assert sue_beliefunit.get_plan_obj(hr_21_rope).stop_want == 1320
    assert sue_beliefunit.get_plan_obj(hr_22_rope).stop_want == 1380
    assert sue_beliefunit.get_plan_obj(hr_23_rope).stop_want == 1440


def test_add_time_creg_planunit_ReturnsObjWith_offset_PlanUnits():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    time_rope = sue_belief.make_l1_rope(time_str())
    creg_rope = sue_belief.make_rope(time_rope, creg_str())
    five_rope = sue_belief.make_rope(time_rope, five_str())
    creg_yr1_jan1_offset_rope = sue_belief.make_rope(creg_rope, yr1_jan1_offset_str())
    five_yr1_jan1_offset_rope = sue_belief.make_rope(five_rope, yr1_jan1_offset_str())

    assert sue_belief.plan_exists(creg_yr1_jan1_offset_rope)
    creg_yr1_offset_plan = sue_belief.get_plan_obj(creg_yr1_jan1_offset_rope)
    assert creg_yr1_offset_plan.addin == get_creg_config().get(yr1_jan1_offset_str())
    assert not sue_belief.plan_exists(five_yr1_jan1_offset_rope)

    # WHEN
    sue_belief = add_time_five_planunit(sue_belief)

    # THEN
    assert sue_belief.plan_exists(creg_yr1_jan1_offset_rope)
    assert sue_belief.plan_exists(five_yr1_jan1_offset_rope)
    five_yr1_offset_plan = sue_belief.get_plan_obj(five_yr1_jan1_offset_rope)
    assert five_yr1_offset_plan.addin == get_five_config().get(yr1_jan1_offset_str())


def test_add_newtimeline_planunit_SetsAttr_Scenario0():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief.cashout()
    time_rope = sue_belief.make_l1_rope(time_str())
    creg_rope = sue_belief.make_rope(time_rope, creg_str())
    creg_yr1_jan1_offset_rope = sue_belief.make_rope(creg_rope, yr1_jan1_offset_str())
    creg_year_rope = get_year_rope(sue_belief, creg_rope)
    print(f"{creg_year_rope=}")
    # print(f"{sue_belief._plan_dict.keys()=}")
    creg_config = get_creg_config()

    assert not sue_belief.plan_exists(creg_year_rope)
    assert not sue_belief.plan_exists(creg_yr1_jan1_offset_rope)

    # WHEN
    sue_belief = add_newtimeline_planunit(sue_belief, creg_config)

    # THEN
    assert sue_belief.plan_exists(creg_year_rope)
    assert sue_belief.plan_exists(creg_yr1_jan1_offset_rope)
    creg_offset_plan = sue_belief.get_plan_obj(creg_yr1_jan1_offset_rope)
    assert creg_offset_plan.addin == creg_config.get(yr1_jan1_offset_str())


# def test_BeliefUnit_get_plan_ranged_kids_ReturnsSomeChildrenScenario2():
#     # ESTABLISH
#     sue_beliefunit = beliefunit_shop("Sue")
#     sue_beliefunit.set_time_creg_plans(c400_number=7)

#     # WHEN THEN
#     time_rope = sue_beliefunit.make_l1_rope("time")
#     tech_rope = sue_beliefunit.make_rope(time_rope, "tech")
#     week_rope = sue_beliefunit.make_rope(tech_rope, "week")
#     assert len(sue_beliefunit.get_plan_ranged_kids(week_rope, begin=0, close=1440)) == 1
#     assert len(sue_beliefunit.get_plan_ranged_kids(week_rope, begin=0, close=2000)) == 2
#     assert len(sue_beliefunit.get_plan_ranged_kids(week_rope, begin=0, close=3000)) == 3


# def test_BeliefUnit_get_plan_ranged_kids_ReturnsSomeChildrenScenario3():
#     # ESTABLISH
#     sue_beliefunit = beliefunit_shop("Sue")
#     sue_beliefunit.set_time_creg_plans(c400_number=7)

#     # WHEN THEN
#     time_rope = sue_beliefunit.make_l1_rope("time")
#     tech_rope = sue_beliefunit.make_rope(time_rope, "tech")
#     week_rope = sue_beliefunit.make_rope(tech_rope, "week")
#     assert len(sue_beliefunit.get_plan_ranged_kids(plan_rope=week_rope, begin=0)) == 1
#     assert len(sue_beliefunit.get_plan_ranged_kids(plan_rope=week_rope, begin=1440)) == 1


def test_BeliefUnit_get_agenda_dict_DoesNotReturnTaskPlansOutsideRange():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    sue_belief = add_time_creg_planunit(beliefunit_shop(sue_str))
    clean_str = "clean"
    clean_rope = sue_belief.make_l1_rope(clean_str)
    sue_belief.set_l1_plan(planunit_shop(clean_str, task=True))
    time_rope = sue_belief.make_l1_rope("time")
    cregtime_rope = sue_belief.make_rope(time_rope, creg_str())
    day_rope = sue_belief.make_rope(cregtime_rope, "day")

    sue_belief.edit_plan_attr(
        clean_rope,
        reason_context=day_rope,
        reason_case=day_rope,
        reason_lower=320,
        reason_upper=480,
    )

    # WHEN
    x_reason_lower = 2063971110
    x_reason_upper1 = 2063971523
    sue_belief.add_fact(
        cregtime_rope,
        fact_state=cregtime_rope,
        fact_lower=x_reason_lower,
        fact_upper=x_reason_upper1,
    )

    # THEN
    agenda_dict = sue_belief.get_agenda_dict()
    print(f"{agenda_dict.keys()=}")
    assert len(agenda_dict) == 1
    assert clean_rope in agenda_dict.keys()

    # WHEN
    # x_reason_upper2 = 1063971923
    x_reason_lower2 = 0
    x_reason_upper2 = 0
    sue_belief.add_fact(
        cregtime_rope,
        fact_state=cregtime_rope,
        fact_lower=x_reason_lower2,
        fact_upper=x_reason_upper2,
    )
    print(f"{sue_belief.planroot.factunits=}")

    # THEN
    agenda_dict = sue_belief.get_agenda_dict()
    assert len(agenda_dict) == 0


def test_BeliefUnit_create_agenda_plan_CreatesAllBeliefAttributes():
    # WHEN "I am cleaning the cookery since I'm in the flat and its 8am and its dirty and its for my family"

    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    assert len(sue_belief.voices) == 0
    assert len(sue_belief.get_voiceunit_group_titles_dict()) == 0

    clean_str = "cleanings"
    clean_rope = sue_belief.make_l1_rope(clean_str)
    sweep_str = "sweep"
    sweep_rope = sue_belief.make_rope(clean_rope, sweep_str)
    sweep_plan = planunit_shop(sweep_str, parent_rope=clean_rope)
    print(f"{sweep_plan.get_plan_rope()=}")
    house_str = "house"
    house_rope = sue_belief.make_l1_rope(house_str)
    cookery_room_str = "cookery room"
    cookery_room_rope = sue_belief.make_rope(house_rope, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_rope = sue_belief.make_rope(cookery_room_rope, cookery_dirty_str)

    # create gregorian timeline
    add_time_creg_planunit(sue_belief)
    time_rope = sue_belief.make_l1_rope("time")
    cregtime_rope = sue_belief.make_rope(time_rope, creg_str())
    creg_plan = sue_belief.get_plan_obj(cregtime_rope)
    print(f"{creg_plan.kids.keys()=}")
    daytime_rope = sue_belief.make_rope(cregtime_rope, "day")
    reason_lower_8am = 480
    reason_upper_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_rope)
    dirty_cookery_reason.set_case(case=cookery_dirty_rope)
    sweep_plan.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_rope)
    daytime_reason.set_case(
        case=daytime_rope, reason_lower=reason_lower_8am, reason_upper=reason_upper_8am
    )
    sweep_plan.set_reasonunit(reason=daytime_reason)

    family_str = ",family"
    awardunit_z = awardunit_shop(awardee_title=family_str)
    sweep_plan.set_awardunit(awardunit_z)

    assert len(sue_belief.voices) == 0
    assert len(sue_belief.get_voiceunit_group_titles_dict()) == 0
    assert len(sue_belief.planroot.kids) == 1
    assert sue_belief.get_plan_obj(daytime_rope).denom == 1440
    assert sue_belief.get_plan_obj(daytime_rope).morph
    print(f"{sweep_plan.get_plan_rope()=}")

    # ESTABLISH
    sue_belief.set_dominate_task_plan(plan_kid=sweep_plan)

    # THEN
    # for plan_kid in sue_belief.planroot.kids.keys():
    #     print(f"  {plan_kid=}")

    print(f"{sweep_plan.get_plan_rope()=}")
    assert sue_belief.get_plan_obj(sweep_rope) is not None
    assert sue_belief.get_plan_obj(sweep_rope).plan_label == sweep_str
    assert sue_belief.get_plan_obj(sweep_rope).task
    assert len(sue_belief.get_plan_obj(sweep_rope).reasonunits) == 2
    assert sue_belief.get_plan_obj(clean_rope) is not None
    assert sue_belief.get_plan_obj(cookery_room_rope) is not None
    assert sue_belief.get_plan_obj(cookery_dirty_rope) is not None
    assert len(sue_belief.get_voiceunit_group_titles_dict()) == 0
    assert sue_belief.get_voiceunit_group_titles_dict().get(family_str) is None

    assert len(sue_belief.planroot.kids) == 3


def test_PlanCore_get_agenda_dict_ReturnsObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    add_time_creg_planunit(sue_belief)

    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    laundry_str = "do_laundry"
    laundry_rope = sue_belief.make_rope(casa_rope, laundry_str)
    sue_belief.set_l1_plan(planunit_shop(casa_str))
    sue_belief.set_plan(planunit_shop(laundry_str, task=True), casa_rope)
    time_rope = sue_belief.make_l1_rope("time")
    cregtime_rope = sue_belief.make_rope(time_rope, creg_str())
    sue_belief.edit_plan_attr(
        laundry_rope,
        reason_context=cregtime_rope,
        reason_case=cregtime_rope,
        reason_lower=3420.0,
        reason_upper=3420.0,
        reason_divisor=10080.0,
    )
    print("set first fact")

    sue_belief.add_fact(cregtime_rope, cregtime_rope, 1064131200, fact_upper=1064135133)
    print("get 1st agenda dictionary")
    sue_agenda_dict = sue_belief.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")
    assert sue_agenda_dict == {}

    laundry_plan = sue_belief.get_plan_obj(laundry_rope)
    laundry_reasonheir = laundry_plan.get_reasonheir(cregtime_rope)
    laundry_case = laundry_reasonheir.get_case(cregtime_rope)
    laundry_factheir = laundry_plan.factheirs.get(cregtime_rope)
    # print(
    #     f"{laundry_plan.active=} {laundry_case.reason_lower=} {laundry_factheir.fact_lower % 10080=}"
    # )
    # print(
    #     f"{laundry_plan.active=} {laundry_case.reason_upper=} {laundry_factheir.fact_upper % 10080=}"
    # )
    # print(f"{laundry_reasonheir.reason_context=} {laundry_case=}")
    # for x_planunit in sue_belief._plan_dict.values():
    #     if x_planunit.plan_label in [laundry_str]:
    #         print(f"{x_planunit.plan_label=} {x_planunit.begin=} {x_planunit.close=}")
    #         print(f"{x_planunit.kids.keys()=}")

    # WHEN
    print("set 2nd fact")
    sue_belief.add_fact(cregtime_rope, cregtime_rope, 1064131200, fact_upper=1064136133)
    print("get 2nd agenda dictionary")
    sue_agenda_dict = sue_belief.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")

    laundry_plan = sue_belief.get_plan_obj(laundry_rope)
    laundry_reasonheir = laundry_plan.get_reasonheir(cregtime_rope)
    laundry_case = laundry_reasonheir.get_case(cregtime_rope)
    laundry_factheir = laundry_plan.factheirs.get(cregtime_rope)
    # print(
    #     f"{laundry_plan.active=} {laundry_case.reason_lower=} {laundry_factheir.fact_lower % 10080=}"
    # )
    # print(
    #     f"{laundry_plan.active=} {laundry_case.reason_upper=} {laundry_factheir.fact_upper % 10080=}"
    # )
    # for x_planunit in sue_belief._plan_dict.values():
    #     if x_planunit.plan_label in [laundry_str]:
    #         print(f"{x_planunit.plan_label=} {x_planunit.begin=} {x_planunit.close=}")
    #         print(f"{x_planunit.kids.keys()=}")
    #         creg_factheir = x_planunit.factheirs.get(cregtime_rope)
    #         print(f"{creg_factheir.fact_lower % 10080=}")
    #         print(f"{creg_factheir.fact_upper % 10080=}")

    # THEN
    assert sue_agenda_dict == {}


def test_add_time_five_planunit_SetsAttr_Scenario0_AddsMultiple_timelines():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    time_rope = sue_belief.make_l1_rope(time_str())
    creg_rope = sue_belief.make_rope(time_rope, creg_str())
    five_rope = sue_belief.make_rope(time_rope, five_str())
    creg_yr1_jan1_offset_rope = sue_belief.make_rope(creg_rope, yr1_jan1_offset_str())
    five_yr1_jan1_offset_rope = sue_belief.make_rope(five_rope, yr1_jan1_offset_str())
    creg_year_rope = get_year_rope(sue_belief, creg_rope)
    five_year_rope = get_year_rope(sue_belief, five_rope)
    print(f"{creg_year_rope=}")
    print(f"{five_year_rope=}")
    # print(f"{sue_belief._plan_dict.keys()=}")

    assert not sue_belief.plan_exists(five_year_rope)
    assert sue_belief.plan_exists(creg_year_rope)
    assert sue_belief.plan_exists(creg_yr1_jan1_offset_rope)
    creg_offset_plan = sue_belief.get_plan_obj(creg_yr1_jan1_offset_rope)
    assert creg_offset_plan.addin == get_creg_config().get(yr1_jan1_offset_str())
    assert not sue_belief.plan_exists(five_yr1_jan1_offset_rope)

    # WHEN
    sue_belief = add_time_five_planunit(sue_belief)

    # THEN
    assert sue_belief.plan_exists(five_year_rope)
    assert sue_belief.plan_exists(creg_year_rope)
    assert sue_belief.plan_exists(creg_yr1_jan1_offset_rope)
    assert sue_belief.plan_exists(five_yr1_jan1_offset_rope)
    five_offset_plan = sue_belief.get_plan_obj(five_yr1_jan1_offset_rope)
    assert five_offset_plan.addin == get_five_config().get(yr1_jan1_offset_str())


def test_get_creg_min_from_dt_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_creg_min_from_dt(datetime(1938, 11, 10))
    assert get_creg_min_from_dt(datetime(1, 1, 1)) == 440640
    assert get_creg_min_from_dt(datetime(1, 1, 2)) == 440640 + 1440
    assert get_creg_min_from_dt(datetime(1938, 11, 10)) == 1019653920
    # assert g_lw.get_time_dt_from_min(
    #     min=g_lw.get_creg_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    # ) == datetime(2000, 1, 1, 0, 0)
    assert get_creg_min_from_dt(datetime(800, 1, 1, 0, 0)) == 420672960
    assert get_creg_min_from_dt(datetime(1200, 1, 1, 0, 0)) == 631052640
    assert get_creg_min_from_dt(datetime(1201, 3, 1, 0, 0)) == 631664640
    assert get_creg_min_from_dt(datetime(1201, 3, 1, 0, 20)) == 631664660

    x_minutes = 1063817280
    assert get_creg_min_from_dt(datetime(2022, 10, 29, 0, 0)) == x_minutes
    x_next_day = x_minutes + 1440
    assert get_creg_min_from_dt(datetime(2022, 10, 30, 0, 0)) == x_next_day


def test_get_min_from_dt_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    x_datetime = datetime(2022, 10, 30, 0, 0)
    time_rope = sue_belief.make_l1_rope(time_str())
    creg_rope = sue_belief.make_rope(time_rope, creg_str())

    # WHEN
    creg_min = get_min_from_dt(sue_belief, creg_rope, x_datetime)

    # THEN
    print(f"                        {creg_min=}")
    print(f"{get_creg_min_from_dt(x_datetime)=}")
    assert creg_min == get_creg_min_from_dt(x_datetime)


def test_get_timeline_min_difference_ReturnsObj():
    # ESTABLISH
    creg_config = get_creg_config()
    five_config = get_five_config()

    # WHEN
    five_creg_diff = get_timeline_min_difference(five_config, creg_config)
    creg_five_diff = get_timeline_min_difference(creg_config, five_config)

    # THEN
    c400_len = get_c400_constants().c400_leap_length
    c400_8x = c400_len * 8
    assert creg_five_diff == -c400_8x
    assert five_creg_diff == c400_8x


def test_get_creg_min_from_dt_ReturnsObj_get_five_min_from_dt_ReturnsObj(
    graphics_bool,
):
    # ESTABLISH
    mar1_2000_datetime = datetime(2000, 3, 1)

    # WHEN
    creg_mar1_2000_len = get_creg_min_from_dt(mar1_2000_datetime)
    five_mar1_2000_len = get_five_min_from_dt(mar1_2000_datetime)

    # THEN
    creg_config = get_creg_config()
    five_config = get_five_config()
    five_creg_diff = get_timeline_min_difference(five_config, creg_config)
    c400_len = get_c400_constants().c400_leap_length
    assert creg_mar1_2000_len == c400_len * 5
    assert five_mar1_2000_len == c400_len * 13
    assert five_mar1_2000_len - creg_mar1_2000_len == c400_len * 8
    assert five_mar1_2000_len - creg_mar1_2000_len == five_creg_diff

    display_current_creg_five_min(graphics_bool)
