from datetime import datetime
from src.a00_data_toolbox.plotly_toolbox import conditional_fig_show
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import reasonunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a07_calendar_logic._test_util.a07_str import (
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
from src.a07_calendar_logic._test_util.calendar_examples import (
    add_time_creg_conceptunit,
    add_time_five_conceptunit,
    creg_hour_int_label,
    creg_str,
    creg_weekday_conceptunits,
    cregtime_conceptunit,
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
from src.a07_calendar_logic.chrono import (
    get_c400_constants,
    get_min_from_dt,
    get_timeline_min_difference,
    get_year_way,
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


def test_cregtime_conceptunit_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert cregtime_conceptunit().begin == 0
    assert cregtime_conceptunit().close == 1472657760
    assert cregtime_conceptunit().close == get_c400_constants().c400_leap_length * 7


def test_creg_weekday_conceptunits_ReturnsObj():
    assert creg_weekday_conceptunits().get(get_wed()).gogo_want == 0
    assert creg_weekday_conceptunits().get(get_thu()).gogo_want == 1440
    assert creg_weekday_conceptunits().get(get_fri()).gogo_want == 2880
    assert creg_weekday_conceptunits().get(get_sat()).gogo_want == 4320
    assert creg_weekday_conceptunits().get(get_sun()).gogo_want == 5760
    assert creg_weekday_conceptunits().get(get_mon()).gogo_want == 7200
    assert creg_weekday_conceptunits().get(get_tue()).gogo_want == 8640
    assert creg_weekday_conceptunits().get(get_wed()).stop_want == 1440
    assert creg_weekday_conceptunits().get(get_thu()).stop_want == 2880
    assert creg_weekday_conceptunits().get(get_fri()).stop_want == 4320
    assert creg_weekday_conceptunits().get(get_sat()).stop_want == 5760
    assert creg_weekday_conceptunits().get(get_sun()).stop_want == 7200
    assert creg_weekday_conceptunits().get(get_mon()).stop_want == 8640
    assert creg_weekday_conceptunits().get(get_tue()).stop_want == 10080


def test_add_time_creg_conceptunit_ReturnsObjWith_days():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_way = sue_budunit.make_l1_way(time_str())
    creg_way = sue_budunit.make_way(time_way, get_cregtime_str())
    day_way = sue_budunit.make_way(creg_way, day_str())
    days_way = sue_budunit.make_way(creg_way, days_str())
    print(f"{time_way=}")
    print(f"{creg_way=}")
    print(f"{day_way=}")
    assert not sue_budunit.concept_exists(time_way)
    assert not sue_budunit.concept_exists(creg_way)
    assert not sue_budunit.concept_exists(day_way)
    assert not sue_budunit.concept_exists(days_way)

    # WHEN
    sue_budunit = add_time_creg_conceptunit(sue_budunit)

    # THEN
    assert sue_budunit.concept_exists(time_way)
    assert sue_budunit.concept_exists(creg_way)
    assert sue_budunit.concept_exists(day_way)
    assert sue_budunit.concept_exists(days_way)
    assert sue_budunit.get_concept_obj(creg_way).begin == 0
    assert sue_budunit.get_concept_obj(creg_way).close == 1472657760
    assert sue_budunit.get_concept_obj(day_way).denom == 1440
    assert sue_budunit.get_concept_obj(day_way).morph
    assert sue_budunit.get_concept_obj(days_way).denom == 1440
    assert sue_budunit.get_concept_obj(days_way).morph is None


def test_add_time_creg_conceptunit_ReturnsObjWith_weeks():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_way = sue_budunit.make_l1_way(time_str())
    creg_way = sue_budunit.make_way(time_way, get_cregtime_str())
    week_way = sue_budunit.make_way(creg_way, week_str())
    sun_way = sue_budunit.make_way(week_way, get_sun())
    mon_way = sue_budunit.make_way(week_way, get_mon())
    tue_way = sue_budunit.make_way(week_way, get_tue())
    wed_way = sue_budunit.make_way(week_way, get_wed())
    thu_way = sue_budunit.make_way(week_way, get_thu())
    fri_way = sue_budunit.make_way(week_way, get_fri())
    sat_way = sue_budunit.make_way(week_way, get_sat())
    weeks_way = sue_budunit.make_way(creg_way, weeks_str())

    assert not sue_budunit.concept_exists(week_way)
    assert not sue_budunit.concept_exists(sun_way)
    assert not sue_budunit.concept_exists(mon_way)
    assert not sue_budunit.concept_exists(tue_way)
    assert not sue_budunit.concept_exists(wed_way)
    assert not sue_budunit.concept_exists(thu_way)
    assert not sue_budunit.concept_exists(fri_way)
    assert not sue_budunit.concept_exists(sat_way)
    assert not sue_budunit.concept_exists(weeks_way)

    # WHEN
    sue_budunit = add_time_creg_conceptunit(sue_budunit)

    # THEN
    assert sue_budunit.concept_exists(week_way)
    assert sue_budunit.get_concept_obj(week_way).gogo_want is None
    assert sue_budunit.get_concept_obj(week_way).stop_want is None
    assert sue_budunit.get_concept_obj(week_way).denom == 10080
    assert sue_budunit.get_concept_obj(week_way).morph
    assert sue_budunit.concept_exists(sun_way)
    assert sue_budunit.concept_exists(mon_way)
    assert sue_budunit.concept_exists(tue_way)
    assert sue_budunit.concept_exists(wed_way)
    assert sue_budunit.concept_exists(thu_way)
    assert sue_budunit.concept_exists(fri_way)
    assert sue_budunit.concept_exists(sat_way)
    assert sue_budunit.concept_exists(weeks_way)
    assert sue_budunit.get_concept_obj(weeks_way).denom == 10080
    assert sue_budunit.get_concept_obj(weeks_way).morph is None


def test_add_time_creg_conceptunit_ReturnsObjWith_c400_leap_way():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_way = sue_budunit.make_l1_way(time_str())
    creg_way = sue_budunit.make_way(time_way, get_cregtime_str())
    c400_leap_way = sue_budunit.make_way(creg_way, c400_leap_str())
    c400_clean_way = sue_budunit.make_way(c400_leap_way, c400_clean_str())
    c100_way = sue_budunit.make_way(c400_clean_way, c100_str())
    yr4_leap_way = sue_budunit.make_way(c100_way, yr4_leap_str())
    yr4_clean_way = sue_budunit.make_way(yr4_leap_way, yr4_clean_str())
    year_way = sue_budunit.make_way(yr4_clean_way, year_str())

    assert not sue_budunit.concept_exists(c400_leap_way)

    # WHEN
    sue_budunit = add_time_creg_conceptunit(sue_budunit)

    # THEN
    assert sue_budunit.concept_exists(c400_leap_way)
    c400_leap_concept = sue_budunit.get_concept_obj(c400_leap_way)
    assert not c400_leap_concept.gogo_want
    assert not c400_leap_concept.stop_want
    assert c400_leap_concept.denom == 210379680
    assert c400_leap_concept.morph

    assert sue_budunit.concept_exists(c400_clean_way)
    c400_clean_concept = sue_budunit.get_concept_obj(c400_clean_way)
    assert not c400_clean_concept.gogo_want
    assert not c400_clean_concept.stop_want
    assert c400_clean_concept.denom == 210378240
    assert c400_clean_concept.morph

    assert sue_budunit.concept_exists(c100_way)
    c100_concept = sue_budunit.get_concept_obj(c100_way)
    assert not c100_concept.gogo_want
    assert not c100_concept.stop_want
    assert c100_concept.denom == 52594560
    assert c100_concept.morph

    assert sue_budunit.concept_exists(yr4_leap_way)
    yr4_leap_concept = sue_budunit.get_concept_obj(yr4_leap_way)
    assert not yr4_leap_concept.gogo_want
    assert not yr4_leap_concept.stop_want
    assert yr4_leap_concept.denom == 2103840
    assert yr4_leap_concept.morph

    assert sue_budunit.concept_exists(yr4_clean_way)
    yr4_clean_concept = sue_budunit.get_concept_obj(yr4_clean_way)
    assert not yr4_clean_concept.gogo_want
    assert not yr4_clean_concept.stop_want
    assert yr4_clean_concept.denom == 2102400
    assert yr4_clean_concept.morph

    assert sue_budunit.concept_exists(year_way)
    year_concept = sue_budunit.get_concept_obj(year_way)
    assert not year_concept.gogo_want
    assert not year_concept.stop_want
    assert year_concept.denom == 525600
    assert year_concept.morph


def test_add_time_creg_conceptunit_ReturnsObjWith_years():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_way = sue_budunit.make_l1_way(time_str())
    creg_way = sue_budunit.make_way(time_way, get_cregtime_str())
    year_way = get_year_way(sue_budunit, creg_way)

    assert not sue_budunit.concept_exists(creg_way)
    assert not sue_budunit.concept_exists(year_way)

    jan_way = sue_budunit.make_way(year_way, "January")
    feb_way = sue_budunit.make_way(year_way, "February")
    mar_way = sue_budunit.make_way(year_way, "March")
    apr_way = sue_budunit.make_way(year_way, "April")
    may_way = sue_budunit.make_way(year_way, "May")
    jun_way = sue_budunit.make_way(year_way, "June")
    jul_way = sue_budunit.make_way(year_way, "July")
    aug_way = sue_budunit.make_way(year_way, "August")
    sep_way = sue_budunit.make_way(year_way, "September")
    oct_way = sue_budunit.make_way(year_way, "October")
    nov_way = sue_budunit.make_way(year_way, "November")
    dec_way = sue_budunit.make_way(year_way, "December")
    assert not sue_budunit.concept_exists(jan_way)
    assert not sue_budunit.concept_exists(feb_way)
    assert not sue_budunit.concept_exists(mar_way)
    assert not sue_budunit.concept_exists(apr_way)
    assert not sue_budunit.concept_exists(may_way)
    assert not sue_budunit.concept_exists(jun_way)
    assert not sue_budunit.concept_exists(jul_way)
    assert not sue_budunit.concept_exists(aug_way)
    assert not sue_budunit.concept_exists(sep_way)
    assert not sue_budunit.concept_exists(oct_way)
    assert not sue_budunit.concept_exists(nov_way)
    assert not sue_budunit.concept_exists(dec_way)
    assert not sue_budunit.concept_exists(year_way)

    # WHEN
    sue_budunit = add_time_creg_conceptunit(sue_budunit)

    # THEN
    assert sue_budunit.concept_exists(creg_way)
    assert sue_budunit.concept_exists(year_way)

    year_concept = sue_budunit.get_concept_obj(year_way)
    # assert year_concept.morph
    assert sue_budunit.concept_exists(jan_way)
    assert sue_budunit.concept_exists(feb_way)
    assert sue_budunit.concept_exists(mar_way)
    assert sue_budunit.concept_exists(apr_way)
    assert sue_budunit.concept_exists(may_way)
    assert sue_budunit.concept_exists(jun_way)
    assert sue_budunit.concept_exists(jul_way)
    assert sue_budunit.concept_exists(aug_way)
    assert sue_budunit.concept_exists(sep_way)
    assert sue_budunit.concept_exists(oct_way)
    assert sue_budunit.concept_exists(nov_way)
    assert sue_budunit.concept_exists(dec_way)
    assert sue_budunit.get_concept_obj(jan_way).addin == 1440
    assert sue_budunit.get_concept_obj(feb_way).addin == 1440
    assert sue_budunit.get_concept_obj(mar_way).addin == 1440
    assert sue_budunit.get_concept_obj(apr_way).addin == 1440
    assert sue_budunit.get_concept_obj(may_way).addin == 1440
    assert sue_budunit.get_concept_obj(jun_way).addin == 1440
    assert sue_budunit.get_concept_obj(jul_way).addin == 1440
    assert sue_budunit.get_concept_obj(aug_way).addin == 1440
    assert sue_budunit.get_concept_obj(sep_way).addin == 1440
    assert sue_budunit.get_concept_obj(oct_way).addin == 1440
    assert sue_budunit.get_concept_obj(nov_way).addin == 1440
    assert sue_budunit.get_concept_obj(dec_way).addin == 1440

    assert sue_budunit.get_concept_obj(jan_way).gogo_want == 440640
    assert sue_budunit.get_concept_obj(feb_way).gogo_want == 485280
    assert sue_budunit.get_concept_obj(mar_way).gogo_want == 0
    assert sue_budunit.get_concept_obj(apr_way).gogo_want == 44640
    assert sue_budunit.get_concept_obj(may_way).gogo_want == 87840
    assert sue_budunit.get_concept_obj(jun_way).gogo_want == 132480
    assert sue_budunit.get_concept_obj(jul_way).gogo_want == 175680
    assert sue_budunit.get_concept_obj(aug_way).gogo_want == 220320
    assert sue_budunit.get_concept_obj(sep_way).gogo_want == 264960
    assert sue_budunit.get_concept_obj(oct_way).gogo_want == 308160
    assert sue_budunit.get_concept_obj(nov_way).gogo_want == 352800
    assert sue_budunit.get_concept_obj(dec_way).gogo_want == 396000

    assert sue_budunit.get_concept_obj(jan_way).stop_want == 485280
    assert sue_budunit.get_concept_obj(feb_way).stop_want == 525600
    assert sue_budunit.get_concept_obj(mar_way).stop_want == 44640
    assert sue_budunit.get_concept_obj(apr_way).stop_want == 87840
    assert sue_budunit.get_concept_obj(may_way).stop_want == 132480
    assert sue_budunit.get_concept_obj(jun_way).stop_want == 175680
    assert sue_budunit.get_concept_obj(jul_way).stop_want == 220320
    assert sue_budunit.get_concept_obj(aug_way).stop_want == 264960
    assert sue_budunit.get_concept_obj(sep_way).stop_want == 308160
    assert sue_budunit.get_concept_obj(oct_way).stop_want == 352800
    assert sue_budunit.get_concept_obj(nov_way).stop_want == 396000
    assert sue_budunit.get_concept_obj(dec_way).stop_want == 440640


def test_add_time_creg_conceptunit_ReturnsObjWith_c400_leap():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_way = sue_budunit.make_l1_way(time_str())
    creg_way = sue_budunit.make_way(time_way, get_cregtime_str())
    day_way = sue_budunit.make_way(creg_way, day_str())
    days_way = sue_budunit.make_way(creg_way, days_str())
    print(f"{time_way=}")
    print(f"{creg_way=}")
    print(f"{day_way=}")
    assert not sue_budunit.concept_exists(time_way)
    assert not sue_budunit.concept_exists(creg_way)
    assert not sue_budunit.concept_exists(day_way)
    assert not sue_budunit.concept_exists(days_way)

    # WHEN
    sue_budunit = add_time_creg_conceptunit(sue_budunit)

    # THEN
    assert sue_budunit.concept_exists(time_way)
    assert sue_budunit.concept_exists(creg_way)
    creg_concept = sue_budunit.get_concept_obj(creg_way)
    assert creg_concept.begin == 0
    assert creg_concept.close == 1472657760
    assert sue_budunit.concept_exists(day_way)
    day_concept = sue_budunit.get_concept_obj(day_way)
    assert day_concept.denom == 1440
    assert day_concept.morph
    assert sue_budunit.concept_exists(days_way)
    days_concept = sue_budunit.get_concept_obj(days_way)
    assert days_concept.denom == 1440
    assert not days_concept.morph


def test_add_time_creg_conceptunit_ReturnsObjWith_hours():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_way = sue_budunit.make_l1_way(time_str())
    creg_way = sue_budunit.make_way(time_way, get_cregtime_str())
    day_way = sue_budunit.make_way(creg_way, day_str())
    hour_way = sue_budunit.make_way(day_way, hour_str())
    hr_00_way = sue_budunit.make_way(day_way, creg_hour_int_label(0))
    hr_01_way = sue_budunit.make_way(day_way, creg_hour_int_label(1))
    hr_02_way = sue_budunit.make_way(day_way, creg_hour_int_label(2))
    hr_03_way = sue_budunit.make_way(day_way, creg_hour_int_label(3))
    hr_04_way = sue_budunit.make_way(day_way, creg_hour_int_label(4))
    hr_05_way = sue_budunit.make_way(day_way, creg_hour_int_label(5))
    hr_06_way = sue_budunit.make_way(day_way, creg_hour_int_label(6))
    hr_07_way = sue_budunit.make_way(day_way, creg_hour_int_label(7))
    hr_08_way = sue_budunit.make_way(day_way, creg_hour_int_label(8))
    hr_09_way = sue_budunit.make_way(day_way, creg_hour_int_label(9))
    hr_10_way = sue_budunit.make_way(day_way, creg_hour_int_label(10))
    hr_11_way = sue_budunit.make_way(day_way, creg_hour_int_label(11))
    hr_12_way = sue_budunit.make_way(day_way, creg_hour_int_label(12))
    hr_13_way = sue_budunit.make_way(day_way, creg_hour_int_label(13))
    hr_14_way = sue_budunit.make_way(day_way, creg_hour_int_label(14))
    hr_15_way = sue_budunit.make_way(day_way, creg_hour_int_label(15))
    hr_16_way = sue_budunit.make_way(day_way, creg_hour_int_label(16))
    hr_17_way = sue_budunit.make_way(day_way, creg_hour_int_label(17))
    hr_18_way = sue_budunit.make_way(day_way, creg_hour_int_label(18))
    hr_19_way = sue_budunit.make_way(day_way, creg_hour_int_label(19))
    hr_20_way = sue_budunit.make_way(day_way, creg_hour_int_label(20))
    hr_21_way = sue_budunit.make_way(day_way, creg_hour_int_label(21))
    hr_22_way = sue_budunit.make_way(day_way, creg_hour_int_label(22))
    hr_23_way = sue_budunit.make_way(day_way, creg_hour_int_label(23))

    print(f"{day_way=}")
    print(f"{hr_00_way=}")
    assert not sue_budunit.concept_exists(time_way)
    assert not sue_budunit.concept_exists(creg_way)
    assert not sue_budunit.concept_exists(day_way)
    assert not sue_budunit.concept_exists(hr_00_way)
    assert not sue_budunit.concept_exists(hr_01_way)
    assert not sue_budunit.concept_exists(hr_02_way)
    assert not sue_budunit.concept_exists(hr_03_way)
    assert not sue_budunit.concept_exists(hr_04_way)
    assert not sue_budunit.concept_exists(hr_05_way)
    assert not sue_budunit.concept_exists(hr_06_way)
    assert not sue_budunit.concept_exists(hr_07_way)
    assert not sue_budunit.concept_exists(hr_08_way)
    assert not sue_budunit.concept_exists(hr_09_way)
    assert not sue_budunit.concept_exists(hr_10_way)
    assert not sue_budunit.concept_exists(hr_11_way)
    assert not sue_budunit.concept_exists(hr_12_way)
    assert not sue_budunit.concept_exists(hr_13_way)
    assert not sue_budunit.concept_exists(hr_14_way)
    assert not sue_budunit.concept_exists(hr_15_way)
    assert not sue_budunit.concept_exists(hr_16_way)
    assert not sue_budunit.concept_exists(hr_17_way)
    assert not sue_budunit.concept_exists(hr_18_way)
    assert not sue_budunit.concept_exists(hr_19_way)
    assert not sue_budunit.concept_exists(hr_20_way)
    assert not sue_budunit.concept_exists(hr_21_way)
    assert not sue_budunit.concept_exists(hr_22_way)
    assert not sue_budunit.concept_exists(hr_23_way)

    # WHEN
    sue_budunit = add_time_creg_conceptunit(sue_budunit)

    # THEN
    day_concept = sue_budunit.get_concept_obj(day_way)
    print(f"{day_concept._kids.keys()=}")
    assert sue_budunit.concept_exists(time_way)
    assert sue_budunit.concept_exists(creg_way)
    assert sue_budunit.concept_exists(day_way)
    # assert sue_budunit.get_concept_obj(hour_way).denom == 60
    # assert sue_budunit.get_concept_obj(hour_way).morph
    # assert not sue_budunit.get_concept_obj(hour_way).gogo_want
    # assert not sue_budunit.get_concept_obj(hour_way).stop_want
    assert sue_budunit.concept_exists(hr_00_way)
    assert sue_budunit.concept_exists(hr_01_way)
    assert sue_budunit.concept_exists(hr_02_way)
    assert sue_budunit.concept_exists(hr_03_way)
    assert sue_budunit.concept_exists(hr_04_way)
    assert sue_budunit.concept_exists(hr_05_way)
    assert sue_budunit.concept_exists(hr_06_way)
    assert sue_budunit.concept_exists(hr_07_way)
    assert sue_budunit.concept_exists(hr_08_way)
    assert sue_budunit.concept_exists(hr_09_way)
    assert sue_budunit.concept_exists(hr_10_way)
    assert sue_budunit.concept_exists(hr_11_way)
    assert sue_budunit.concept_exists(hr_12_way)
    assert sue_budunit.concept_exists(hr_13_way)
    assert sue_budunit.concept_exists(hr_14_way)
    assert sue_budunit.concept_exists(hr_15_way)
    assert sue_budunit.concept_exists(hr_16_way)
    assert sue_budunit.concept_exists(hr_17_way)
    assert sue_budunit.concept_exists(hr_18_way)
    assert sue_budunit.concept_exists(hr_19_way)
    assert sue_budunit.concept_exists(hr_20_way)
    assert sue_budunit.concept_exists(hr_21_way)
    assert sue_budunit.concept_exists(hr_22_way)
    assert sue_budunit.concept_exists(hr_23_way)
    assert sue_budunit.get_concept_obj(hr_00_way).gogo_want == 0
    assert sue_budunit.get_concept_obj(hr_01_way).gogo_want == 60
    assert sue_budunit.get_concept_obj(hr_02_way).gogo_want == 120
    assert sue_budunit.get_concept_obj(hr_03_way).gogo_want == 180
    assert sue_budunit.get_concept_obj(hr_04_way).gogo_want == 240
    assert sue_budunit.get_concept_obj(hr_05_way).gogo_want == 300
    assert sue_budunit.get_concept_obj(hr_06_way).gogo_want == 360
    assert sue_budunit.get_concept_obj(hr_07_way).gogo_want == 420
    assert sue_budunit.get_concept_obj(hr_08_way).gogo_want == 480
    assert sue_budunit.get_concept_obj(hr_09_way).gogo_want == 540
    assert sue_budunit.get_concept_obj(hr_10_way).gogo_want == 600
    assert sue_budunit.get_concept_obj(hr_11_way).gogo_want == 660
    assert sue_budunit.get_concept_obj(hr_12_way).gogo_want == 720
    assert sue_budunit.get_concept_obj(hr_13_way).gogo_want == 780
    assert sue_budunit.get_concept_obj(hr_14_way).gogo_want == 840
    assert sue_budunit.get_concept_obj(hr_15_way).gogo_want == 900
    assert sue_budunit.get_concept_obj(hr_16_way).gogo_want == 960
    assert sue_budunit.get_concept_obj(hr_17_way).gogo_want == 1020
    assert sue_budunit.get_concept_obj(hr_18_way).gogo_want == 1080
    assert sue_budunit.get_concept_obj(hr_19_way).gogo_want == 1140
    assert sue_budunit.get_concept_obj(hr_20_way).gogo_want == 1200
    assert sue_budunit.get_concept_obj(hr_21_way).gogo_want == 1260
    assert sue_budunit.get_concept_obj(hr_22_way).gogo_want == 1320
    assert sue_budunit.get_concept_obj(hr_23_way).gogo_want == 1380
    assert sue_budunit.get_concept_obj(hr_00_way).stop_want == 60
    assert sue_budunit.get_concept_obj(hr_01_way).stop_want == 120
    assert sue_budunit.get_concept_obj(hr_02_way).stop_want == 180
    assert sue_budunit.get_concept_obj(hr_03_way).stop_want == 240
    assert sue_budunit.get_concept_obj(hr_04_way).stop_want == 300
    assert sue_budunit.get_concept_obj(hr_05_way).stop_want == 360
    assert sue_budunit.get_concept_obj(hr_06_way).stop_want == 420
    assert sue_budunit.get_concept_obj(hr_07_way).stop_want == 480
    assert sue_budunit.get_concept_obj(hr_08_way).stop_want == 540
    assert sue_budunit.get_concept_obj(hr_09_way).stop_want == 600
    assert sue_budunit.get_concept_obj(hr_10_way).stop_want == 660
    assert sue_budunit.get_concept_obj(hr_11_way).stop_want == 720
    assert sue_budunit.get_concept_obj(hr_12_way).stop_want == 780
    assert sue_budunit.get_concept_obj(hr_13_way).stop_want == 840
    assert sue_budunit.get_concept_obj(hr_14_way).stop_want == 900
    assert sue_budunit.get_concept_obj(hr_15_way).stop_want == 960
    assert sue_budunit.get_concept_obj(hr_16_way).stop_want == 1020
    assert sue_budunit.get_concept_obj(hr_17_way).stop_want == 1080
    assert sue_budunit.get_concept_obj(hr_18_way).stop_want == 1140
    assert sue_budunit.get_concept_obj(hr_19_way).stop_want == 1200
    assert sue_budunit.get_concept_obj(hr_20_way).stop_want == 1260
    assert sue_budunit.get_concept_obj(hr_21_way).stop_want == 1320
    assert sue_budunit.get_concept_obj(hr_22_way).stop_want == 1380
    assert sue_budunit.get_concept_obj(hr_23_way).stop_want == 1440


def test_add_time_creg_conceptunit_ReturnsObjWith_offset_ConceptUnits():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_conceptunit(sue_bud)
    sue_bud.settle_bud()
    time_way = sue_bud.make_l1_way(time_str())
    creg_way = sue_bud.make_way(time_way, creg_str())
    five_way = sue_bud.make_way(time_way, five_str())
    creg_yr1_jan1_offset_way = sue_bud.make_way(creg_way, yr1_jan1_offset_str())
    five_yr1_jan1_offset_way = sue_bud.make_way(five_way, yr1_jan1_offset_str())

    assert sue_bud.concept_exists(creg_yr1_jan1_offset_way)
    creg_yr1_offset_concept = sue_bud.get_concept_obj(creg_yr1_jan1_offset_way)
    assert creg_yr1_offset_concept.addin == get_creg_config().get(yr1_jan1_offset_str())
    assert not sue_bud.concept_exists(five_yr1_jan1_offset_way)

    # WHEN
    sue_bud = add_time_five_conceptunit(sue_bud)

    # THEN
    assert sue_bud.concept_exists(creg_yr1_jan1_offset_way)
    assert sue_bud.concept_exists(five_yr1_jan1_offset_way)
    five_yr1_offset_concept = sue_bud.get_concept_obj(five_yr1_jan1_offset_way)
    assert five_yr1_offset_concept.addin == get_five_config().get(yr1_jan1_offset_str())


# def test_BudUnit_get_concept_ranged_kids_ReturnsSomeChildrenScenario2():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_creg_concepts(c400_number=7)

#     # WHEN THEN
#     time_way = sue_budunit.make_l1_way("time")
#     tech_way = sue_budunit.make_way(time_way, "tech")
#     week_way = sue_budunit.make_way(tech_way, "week")
#     assert len(sue_budunit.get_concept_ranged_kids(week_way, begin=0, close=1440)) == 1
#     assert len(sue_budunit.get_concept_ranged_kids(week_way, begin=0, close=2000)) == 2
#     assert len(sue_budunit.get_concept_ranged_kids(week_way, begin=0, close=3000)) == 3


# def test_BudUnit_get_concept_ranged_kids_ReturnsSomeChildrenScenario3():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_creg_concepts(c400_number=7)

#     # WHEN THEN
#     time_way = sue_budunit.make_l1_way("time")
#     tech_way = sue_budunit.make_way(time_way, "tech")
#     week_way = sue_budunit.make_way(tech_way, "week")
#     assert len(sue_budunit.get_concept_ranged_kids(concept_way=week_way, begin=0)) == 1
#     assert len(sue_budunit.get_concept_ranged_kids(concept_way=week_way, begin=1440)) == 1


def test_BudUnit_get_agenda_dict_DoesNotReturnTaskConceptsOutsideRange():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = add_time_creg_conceptunit(budunit_shop(sue_str))
    clean_str = "clean"
    clean_way = sue_bud.make_l1_way(clean_str)
    sue_bud.set_l1_concept(conceptunit_shop(clean_str, task=True))
    time_way = sue_bud.make_l1_way("time")
    cregtime_way = sue_bud.make_way(time_way, creg_str())
    day_way = sue_bud.make_way(cregtime_way, "day")

    sue_bud.edit_concept_attr(
        clean_way,
        reason_rcontext=day_way,
        reason_premise=day_way,
        popen=320,
        reason_pnigh=480,
    )

    # WHEN
    x_popen = 2063971110
    x_pnigh1 = 2063971523
    sue_bud.add_fact(cregtime_way, fstate=cregtime_way, fopen=x_popen, fnigh=x_pnigh1)

    # THEN
    agenda_dict = sue_bud.get_agenda_dict()
    print(f"{agenda_dict.keys()=}")
    assert len(agenda_dict) == 1
    assert clean_way in agenda_dict.keys()

    # WHEN
    # x_pnigh2 = 1063971923
    x_popen2 = 0
    x_pnigh2 = 0
    sue_bud.add_fact(cregtime_way, fstate=cregtime_way, fopen=x_popen2, fnigh=x_pnigh2)
    print(f"{sue_bud.conceptroot.factunits=}")

    # THEN
    agenda_dict = sue_bud.get_agenda_dict()
    assert len(agenda_dict) == 0


def test_BudUnit_create_agenda_concept_CorrectlyCreatesAllBudAttributes():
    # WHEN "I am cleaning the cookery since I'm in the flat and it's 8am and it's dirty and it's for my family"

    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    assert len(sue_bud.accts) == 0
    assert len(sue_bud.get_acctunit_group_titles_dict()) == 0

    clean_str = "cleanings"
    clean_way = sue_bud.make_l1_way(clean_str)
    sweep_str = "sweep"
    sweep_way = sue_bud.make_way(clean_way, sweep_str)
    sweep_concept = conceptunit_shop(sweep_str, parent_way=clean_way)
    print(f"{sweep_concept.get_concept_way()=}")
    house_str = "house"
    house_way = sue_bud.make_l1_way(house_str)
    cookery_room_str = "cookery room"
    cookery_room_way = sue_bud.make_way(house_way, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_way = sue_bud.make_way(cookery_room_way, cookery_dirty_str)

    # create gregorian timeline
    add_time_creg_conceptunit(sue_bud)
    time_way = sue_bud.make_l1_way("time")
    cregtime_way = sue_bud.make_way(time_way, creg_str())
    creg_concept = sue_bud.get_concept_obj(cregtime_way)
    print(f"{creg_concept._kids.keys()=}")
    daytime_way = sue_bud.make_way(cregtime_way, "day")
    popen_8am = 480
    pnigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_way)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_way)
    sweep_concept.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_way)
    daytime_reason.set_premise(premise=daytime_way, popen=popen_8am, pnigh=pnigh_8am)
    sweep_concept.set_reasonunit(reason=daytime_reason)

    family_str = ",family"
    awardlink_z = awardlink_shop(awardee_title=family_str)
    sweep_concept.set_awardlink(awardlink_z)

    assert len(sue_bud.accts) == 0
    assert len(sue_bud.get_acctunit_group_titles_dict()) == 0
    assert len(sue_bud.conceptroot._kids) == 1
    assert sue_bud.get_concept_obj(daytime_way).denom == 1440
    assert sue_bud.get_concept_obj(daytime_way).morph
    print(f"{sweep_concept.get_concept_way()=}")

    # ESTABLISH
    sue_bud.set_dominate_task_concept(concept_kid=sweep_concept)

    # THEN
    # for concept_kid in sue_bud.conceptroot._kids.keys():
    #     print(f"  {concept_kid=}")

    print(f"{sweep_concept.get_concept_way()=}")
    assert sue_bud.get_concept_obj(sweep_way) is not None
    assert sue_bud.get_concept_obj(sweep_way).concept_label == sweep_str
    assert sue_bud.get_concept_obj(sweep_way).task
    assert len(sue_bud.get_concept_obj(sweep_way).reasonunits) == 2
    assert sue_bud.get_concept_obj(clean_way) is not None
    assert sue_bud.get_concept_obj(cookery_room_way) is not None
    assert sue_bud.get_concept_obj(cookery_dirty_way) is not None
    assert len(sue_bud.get_acctunit_group_titles_dict()) == 0
    assert sue_bud.get_acctunit_group_titles_dict().get(family_str) is None

    assert len(sue_bud.conceptroot._kids) == 3


def test_ConceptCore_get_agenda_dict_ReturnsObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    add_time_creg_conceptunit(sue_bud)

    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    laundry_str = "do_laundry"
    laundry_way = sue_bud.make_way(casa_way, laundry_str)
    sue_bud.set_l1_concept(conceptunit_shop(casa_str))
    sue_bud.set_concept(conceptunit_shop(laundry_str, task=True), casa_way)
    time_way = sue_bud.make_l1_way("time")
    cregtime_way = sue_bud.make_way(time_way, creg_str())
    sue_bud.edit_concept_attr(
        laundry_way,
        reason_rcontext=cregtime_way,
        reason_premise=cregtime_way,
        popen=3420.0,
        reason_pnigh=3420.0,
        pdivisor=10080.0,
    )
    print("set first fact")

    sue_bud.add_fact(cregtime_way, cregtime_way, 1064131200, fnigh=1064135133)
    print("get 1st agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")
    assert sue_agenda_dict == {}

    laundry_concept = sue_bud.get_concept_obj(laundry_way)
    laundry_reasonheir = laundry_concept.get_reasonheir(cregtime_way)
    laundry_premise = laundry_reasonheir.get_premise(cregtime_way)
    laundry_factheir = laundry_concept._factheirs.get(cregtime_way)
    # print(
    #     f"{laundry_concept._active=} {laundry_premise.popen=} {laundry_factheir.fopen % 10080=}"
    # )
    # print(
    #     f"{laundry_concept._active=} {laundry_premise.pnigh=} {laundry_factheir.fnigh % 10080=}"
    # )
    # print(f"{laundry_reasonheir.rcontext=} {laundry_premise=}")
    # for x_conceptunit in sue_bud._concept_dict.values():
    #     if x_conceptunit.concept_label in [laundry_str]:
    #         print(f"{x_conceptunit.concept_label=} {x_conceptunit.begin=} {x_conceptunit.close=}")
    #         print(f"{x_conceptunit._kids.keys()=}")

    # WHEN
    print("set 2nd fact")
    sue_bud.add_fact(cregtime_way, cregtime_way, 1064131200, fnigh=1064136133)
    print("get 2nd agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")

    laundry_concept = sue_bud.get_concept_obj(laundry_way)
    laundry_reasonheir = laundry_concept.get_reasonheir(cregtime_way)
    laundry_premise = laundry_reasonheir.get_premise(cregtime_way)
    laundry_factheir = laundry_concept._factheirs.get(cregtime_way)
    # print(
    #     f"{laundry_concept._active=} {laundry_premise.popen=} {laundry_factheir.fopen % 10080=}"
    # )
    # print(
    #     f"{laundry_concept._active=} {laundry_premise.pnigh=} {laundry_factheir.fnigh % 10080=}"
    # )
    # for x_conceptunit in sue_bud._concept_dict.values():
    #     if x_conceptunit.concept_label in [laundry_str]:
    #         print(f"{x_conceptunit.concept_label=} {x_conceptunit.begin=} {x_conceptunit.close=}")
    #         print(f"{x_conceptunit._kids.keys()=}")
    #         creg_factheir = x_conceptunit._factheirs.get(cregtime_way)
    #         print(f"{creg_factheir.fopen % 10080=}")
    #         print(f"{creg_factheir.fnigh % 10080=}")

    # THEN
    assert sue_agenda_dict == {}


def test_add_newtimeline_conceptunit_CorrectlyAddsMultiple_timelines():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_conceptunit(sue_bud)
    sue_bud.settle_bud()
    time_way = sue_bud.make_l1_way(time_str())
    creg_way = sue_bud.make_way(time_way, creg_str())
    five_way = sue_bud.make_way(time_way, five_str())
    creg_yr1_jan1_offset_way = sue_bud.make_way(creg_way, yr1_jan1_offset_str())
    five_yr1_jan1_offset_way = sue_bud.make_way(five_way, yr1_jan1_offset_str())
    creg_year_way = get_year_way(sue_bud, creg_way)
    five_year_way = get_year_way(sue_bud, five_way)
    print(f"{creg_year_way=}")
    print(f"{five_year_way=}")
    # print(f"{sue_bud._concept_dict.keys()=}")

    assert not sue_bud.concept_exists(five_year_way)
    assert sue_bud.concept_exists(creg_year_way)
    assert sue_bud.concept_exists(creg_yr1_jan1_offset_way)
    creg_offset_concept = sue_bud.get_concept_obj(creg_yr1_jan1_offset_way)
    assert creg_offset_concept.addin == get_creg_config().get(yr1_jan1_offset_str())
    assert not sue_bud.concept_exists(five_yr1_jan1_offset_way)

    # WHEN
    sue_bud = add_time_five_conceptunit(sue_bud)

    # THEN
    assert sue_bud.concept_exists(five_year_way)
    assert sue_bud.concept_exists(creg_year_way)
    assert sue_bud.concept_exists(creg_yr1_jan1_offset_way)
    assert sue_bud.concept_exists(five_yr1_jan1_offset_way)
    five_offset_concept = sue_bud.get_concept_obj(five_yr1_jan1_offset_way)
    assert five_offset_concept.addin == get_five_config().get(yr1_jan1_offset_str())


def test_get_creg_min_from_dt_ReturnsObj():
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
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_conceptunit(sue_bud)
    sue_bud.settle_bud()
    x_datetime = datetime(2022, 10, 30, 0, 0)
    time_way = sue_bud.make_l1_way(time_str())
    creg_way = sue_bud.make_way(time_way, creg_str())

    # WHEN
    creg_min = get_min_from_dt(sue_bud, creg_way, x_datetime)

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
