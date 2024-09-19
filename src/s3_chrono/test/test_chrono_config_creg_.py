from src.s0_instrument.plotly_tool import conditional_fig_show
from src.s2_bud.group import awardlink_shop
from src.s2_bud.reason_idea import reasonunit_shop
from src.s2_bud.idea import ideaunit_shop
from src.s2_bud.bud import budunit_shop
from src.s3_chrono.chrono import (
    time_str,
    year_str,
    get_year_road,
    day_str,
    days_str,
    c400_leap_str,
    c400_clean_str,
    c100_str,
    yr4_leap_str,
    yr4_clean_str,
    year_str,
    hour_str,
    weeks_str,
    week_str,
    get_c400_constants,
    get_timeline_min_difference,
    yr1_jan1_offset_str,
    get_min_from_dt,
)
from src.s3_chrono.examples.chrono_examples import (
    add_time_creg_ideaunit,
    add_time_five_ideaunit,
    get_creg_min_from_dt,
    get_five_min_from_dt,
    get_cregtime_str,
    get_sun,
    get_mon,
    get_tue,
    get_wed,
    get_thu,
    get_fri,
    get_sat,
    creg_hour_label,
    cregtime_ideaunit,
    creg_weekday_ideaunits,
    creg_str,
    five_str,
    get_creg_config,
    get_five_config,
    display_current_creg_five_min,
)
from datetime import datetime


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


def test_cregtime_ideaunit_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert cregtime_ideaunit().begin == 0
    assert cregtime_ideaunit().close == 1472657760
    assert cregtime_ideaunit().close == get_c400_constants().c400_leap_length * 7


def test_creg_weekday_ideaunits_ReturnsObj():
    assert creg_weekday_ideaunits().get(get_wed()).gogo_want == 0
    assert creg_weekday_ideaunits().get(get_thu()).gogo_want == 1440
    assert creg_weekday_ideaunits().get(get_fri()).gogo_want == 2880
    assert creg_weekday_ideaunits().get(get_sat()).gogo_want == 4320
    assert creg_weekday_ideaunits().get(get_sun()).gogo_want == 5760
    assert creg_weekday_ideaunits().get(get_mon()).gogo_want == 7200
    assert creg_weekday_ideaunits().get(get_tue()).gogo_want == 8640
    assert creg_weekday_ideaunits().get(get_wed()).stop_want == 1440
    assert creg_weekday_ideaunits().get(get_thu()).stop_want == 2880
    assert creg_weekday_ideaunits().get(get_fri()).stop_want == 4320
    assert creg_weekday_ideaunits().get(get_sat()).stop_want == 5760
    assert creg_weekday_ideaunits().get(get_sun()).stop_want == 7200
    assert creg_weekday_ideaunits().get(get_mon()).stop_want == 8640
    assert creg_weekday_ideaunits().get(get_tue()).stop_want == 10080


def test_add_time_creg_ideaunit_ReturnsObjWith_days():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    day_road = sue_budunit.make_road(creg_road, day_str())
    days_road = sue_budunit.make_road(creg_road, days_str())
    print(f"{time_road=}")
    print(f"{creg_road=}")
    print(f"{day_road=}")
    assert not sue_budunit.idea_exists(time_road)
    assert not sue_budunit.idea_exists(creg_road)
    assert not sue_budunit.idea_exists(day_road)
    assert not sue_budunit.idea_exists(days_road)

    # WHEN
    sue_budunit = add_time_creg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(creg_road)
    creg_idea = sue_budunit.get_idea_obj(creg_road)
    assert creg_idea.begin == 0
    assert creg_idea.close == 1472657760
    assert sue_budunit.idea_exists(day_road)
    day_idea = sue_budunit.get_idea_obj(day_road)
    assert day_idea.denom == 1440
    assert day_idea.morph
    assert sue_budunit.idea_exists(days_road)
    days_idea = sue_budunit.get_idea_obj(days_road)
    assert days_idea.denom == 1440
    assert not days_idea.morph


def test_add_time_creg_ideaunit_ReturnsObjWith_weeks():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    week_road = sue_budunit.make_road(creg_road, week_str())
    sun_road = sue_budunit.make_road(week_road, get_sun())
    mon_road = sue_budunit.make_road(week_road, get_mon())
    tue_road = sue_budunit.make_road(week_road, get_tue())
    wed_road = sue_budunit.make_road(week_road, get_wed())
    thu_road = sue_budunit.make_road(week_road, get_thu())
    fri_road = sue_budunit.make_road(week_road, get_fri())
    sat_road = sue_budunit.make_road(week_road, get_sat())
    weeks_road = sue_budunit.make_road(creg_road, weeks_str())

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
    sue_budunit = add_time_creg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(week_road)
    week_idea = sue_budunit.get_idea_obj(week_road)
    assert not week_idea.gogo_want
    assert not week_idea.stop_want
    assert week_idea.denom == 10080
    assert week_idea.morph
    assert sue_budunit.idea_exists(sun_road)
    assert sue_budunit.idea_exists(mon_road)
    assert sue_budunit.idea_exists(tue_road)
    assert sue_budunit.idea_exists(wed_road)
    assert sue_budunit.idea_exists(thu_road)
    assert sue_budunit.idea_exists(fri_road)
    assert sue_budunit.idea_exists(sat_road)
    assert sue_budunit.idea_exists(weeks_road)
    weeks_idea = sue_budunit.get_idea_obj(weeks_road)
    assert weeks_idea.denom == 10080
    assert not weeks_idea.morph


def test_add_time_creg_ideaunit_ReturnsObjWith_c400_leap_road():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    c400_leap_road = sue_budunit.make_road(creg_road, c400_leap_str())
    c400_clean_road = sue_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = sue_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = sue_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = sue_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = sue_budunit.make_road(yr4_clean_road, year_str())

    assert not sue_budunit.idea_exists(c400_leap_road)

    # WHEN
    sue_budunit = add_time_creg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(c400_leap_road)
    c400_leap_idea = sue_budunit.get_idea_obj(c400_leap_road)
    assert not c400_leap_idea.gogo_want
    assert not c400_leap_idea.stop_want
    assert c400_leap_idea.denom == 210379680
    assert c400_leap_idea.morph

    assert sue_budunit.idea_exists(c400_clean_road)
    c400_clean_idea = sue_budunit.get_idea_obj(c400_clean_road)
    assert not c400_clean_idea.gogo_want
    assert not c400_clean_idea.stop_want
    assert c400_clean_idea.denom == 210378240
    assert c400_clean_idea.morph

    assert sue_budunit.idea_exists(c100_road)
    c100_idea = sue_budunit.get_idea_obj(c100_road)
    assert not c100_idea.gogo_want
    assert not c100_idea.stop_want
    assert c100_idea.denom == 52594560
    assert c100_idea.morph

    assert sue_budunit.idea_exists(yr4_leap_road)
    yr4_leap_idea = sue_budunit.get_idea_obj(yr4_leap_road)
    assert not yr4_leap_idea.gogo_want
    assert not yr4_leap_idea.stop_want
    assert yr4_leap_idea.denom == 2103840
    assert yr4_leap_idea.morph

    assert sue_budunit.idea_exists(yr4_clean_road)
    yr4_clean_idea = sue_budunit.get_idea_obj(yr4_clean_road)
    assert not yr4_clean_idea.gogo_want
    assert not yr4_clean_idea.stop_want
    assert yr4_clean_idea.denom == 2102400
    assert yr4_clean_idea.morph

    assert sue_budunit.idea_exists(year_road)
    year_idea = sue_budunit.get_idea_obj(year_road)
    assert not year_idea.gogo_want
    assert not year_idea.stop_want
    assert year_idea.denom == 525600
    assert year_idea.morph


def test_add_time_creg_ideaunit_ReturnsObjWith_years():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    year_road = get_year_road(sue_budunit, creg_road)

    assert not sue_budunit.idea_exists(creg_road)
    assert not sue_budunit.idea_exists(year_road)

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
    sue_budunit = add_time_creg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(creg_road)
    assert sue_budunit.idea_exists(year_road)

    year_idea = sue_budunit.get_idea_obj(year_road)
    # assert year_idea.morph
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
    assert sue_budunit.get_idea_obj(jan_road).gogo_want == 440640
    assert sue_budunit.get_idea_obj(feb_road).gogo_want == 485280
    assert sue_budunit.get_idea_obj(mar_road).gogo_want == 0
    assert sue_budunit.get_idea_obj(apr_road).gogo_want == 44640
    assert sue_budunit.get_idea_obj(may_road).gogo_want == 87840
    assert sue_budunit.get_idea_obj(jun_road).gogo_want == 132480
    assert sue_budunit.get_idea_obj(jul_road).gogo_want == 175680
    assert sue_budunit.get_idea_obj(aug_road).gogo_want == 220320
    assert sue_budunit.get_idea_obj(sep_road).gogo_want == 264960
    assert sue_budunit.get_idea_obj(oct_road).gogo_want == 308160
    assert sue_budunit.get_idea_obj(nov_road).gogo_want == 352800
    assert sue_budunit.get_idea_obj(dec_road).gogo_want == 396000

    assert sue_budunit.get_idea_obj(jan_road).stop_want == 485280
    assert sue_budunit.get_idea_obj(feb_road).stop_want == 525600
    assert sue_budunit.get_idea_obj(mar_road).stop_want == 44640
    assert sue_budunit.get_idea_obj(apr_road).stop_want == 87840
    assert sue_budunit.get_idea_obj(may_road).stop_want == 132480
    assert sue_budunit.get_idea_obj(jun_road).stop_want == 175680
    assert sue_budunit.get_idea_obj(jul_road).stop_want == 220320
    assert sue_budunit.get_idea_obj(aug_road).stop_want == 264960
    assert sue_budunit.get_idea_obj(sep_road).stop_want == 308160
    assert sue_budunit.get_idea_obj(oct_road).stop_want == 352800
    assert sue_budunit.get_idea_obj(nov_road).stop_want == 396000
    assert sue_budunit.get_idea_obj(dec_road).stop_want == 440640


def test_add_time_creg_ideaunit_ReturnsObjWith_c400_leap():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    day_road = sue_budunit.make_road(creg_road, day_str())
    days_road = sue_budunit.make_road(creg_road, days_str())
    print(f"{time_road=}")
    print(f"{creg_road=}")
    print(f"{day_road=}")
    assert not sue_budunit.idea_exists(time_road)
    assert not sue_budunit.idea_exists(creg_road)
    assert not sue_budunit.idea_exists(day_road)
    assert not sue_budunit.idea_exists(days_road)

    # WHEN
    sue_budunit = add_time_creg_ideaunit(sue_budunit)

    # THEN
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(creg_road)
    creg_idea = sue_budunit.get_idea_obj(creg_road)
    assert creg_idea.begin == 0
    assert creg_idea.close == 1472657760
    assert sue_budunit.idea_exists(day_road)
    day_idea = sue_budunit.get_idea_obj(day_road)
    assert day_idea.denom == 1440
    assert day_idea.morph
    assert sue_budunit.idea_exists(days_road)
    days_idea = sue_budunit.get_idea_obj(days_road)
    assert days_idea.denom == 1440
    assert not days_idea.morph


def test_add_time_creg_ideaunit_ReturnsObjWith_c400_leap():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    day_road = sue_budunit.make_road(creg_road, day_str())
    hour_road = sue_budunit.make_road(day_road, hour_str())
    hr_00_road = sue_budunit.make_road(day_road, creg_hour_label(0))
    hr_01_road = sue_budunit.make_road(day_road, creg_hour_label(1))
    hr_02_road = sue_budunit.make_road(day_road, creg_hour_label(2))
    hr_03_road = sue_budunit.make_road(day_road, creg_hour_label(3))
    hr_04_road = sue_budunit.make_road(day_road, creg_hour_label(4))
    hr_05_road = sue_budunit.make_road(day_road, creg_hour_label(5))
    hr_06_road = sue_budunit.make_road(day_road, creg_hour_label(6))
    hr_07_road = sue_budunit.make_road(day_road, creg_hour_label(7))
    hr_08_road = sue_budunit.make_road(day_road, creg_hour_label(8))
    hr_09_road = sue_budunit.make_road(day_road, creg_hour_label(9))
    hr_10_road = sue_budunit.make_road(day_road, creg_hour_label(10))
    hr_11_road = sue_budunit.make_road(day_road, creg_hour_label(11))
    hr_12_road = sue_budunit.make_road(day_road, creg_hour_label(12))
    hr_13_road = sue_budunit.make_road(day_road, creg_hour_label(13))
    hr_14_road = sue_budunit.make_road(day_road, creg_hour_label(14))
    hr_15_road = sue_budunit.make_road(day_road, creg_hour_label(15))
    hr_16_road = sue_budunit.make_road(day_road, creg_hour_label(16))
    hr_17_road = sue_budunit.make_road(day_road, creg_hour_label(17))
    hr_18_road = sue_budunit.make_road(day_road, creg_hour_label(18))
    hr_19_road = sue_budunit.make_road(day_road, creg_hour_label(19))
    hr_20_road = sue_budunit.make_road(day_road, creg_hour_label(20))
    hr_21_road = sue_budunit.make_road(day_road, creg_hour_label(21))
    hr_22_road = sue_budunit.make_road(day_road, creg_hour_label(22))
    hr_23_road = sue_budunit.make_road(day_road, creg_hour_label(23))

    print(f"{day_road=}")
    print(f"{hr_00_road=}")
    assert not sue_budunit.idea_exists(time_road)
    assert not sue_budunit.idea_exists(creg_road)
    assert not sue_budunit.idea_exists(day_road)
    assert not sue_budunit.idea_exists(hr_00_road)
    assert not sue_budunit.idea_exists(hr_01_road)
    assert not sue_budunit.idea_exists(hr_02_road)
    assert not sue_budunit.idea_exists(hr_03_road)
    assert not sue_budunit.idea_exists(hr_04_road)
    assert not sue_budunit.idea_exists(hr_05_road)
    assert not sue_budunit.idea_exists(hr_06_road)
    assert not sue_budunit.idea_exists(hr_07_road)
    assert not sue_budunit.idea_exists(hr_08_road)
    assert not sue_budunit.idea_exists(hr_09_road)
    assert not sue_budunit.idea_exists(hr_10_road)
    assert not sue_budunit.idea_exists(hr_11_road)
    assert not sue_budunit.idea_exists(hr_12_road)
    assert not sue_budunit.idea_exists(hr_13_road)
    assert not sue_budunit.idea_exists(hr_14_road)
    assert not sue_budunit.idea_exists(hr_15_road)
    assert not sue_budunit.idea_exists(hr_16_road)
    assert not sue_budunit.idea_exists(hr_17_road)
    assert not sue_budunit.idea_exists(hr_18_road)
    assert not sue_budunit.idea_exists(hr_19_road)
    assert not sue_budunit.idea_exists(hr_20_road)
    assert not sue_budunit.idea_exists(hr_21_road)
    assert not sue_budunit.idea_exists(hr_22_road)
    assert not sue_budunit.idea_exists(hr_23_road)

    # WHEN
    sue_budunit = add_time_creg_ideaunit(sue_budunit)

    # THEN
    day_idea = sue_budunit.get_idea_obj(day_road)
    print(f"{day_idea._kids.keys()=}")
    assert sue_budunit.idea_exists(time_road)
    assert sue_budunit.idea_exists(creg_road)
    assert sue_budunit.idea_exists(day_road)
    # assert sue_budunit.get_idea_obj(hour_road).denom == 60
    # assert sue_budunit.get_idea_obj(hour_road).morph
    # assert not sue_budunit.get_idea_obj(hour_road).gogo_want
    # assert not sue_budunit.get_idea_obj(hour_road).stop_want
    assert sue_budunit.idea_exists(hr_00_road)
    assert sue_budunit.idea_exists(hr_01_road)
    assert sue_budunit.idea_exists(hr_02_road)
    assert sue_budunit.idea_exists(hr_03_road)
    assert sue_budunit.idea_exists(hr_04_road)
    assert sue_budunit.idea_exists(hr_05_road)
    assert sue_budunit.idea_exists(hr_06_road)
    assert sue_budunit.idea_exists(hr_07_road)
    assert sue_budunit.idea_exists(hr_08_road)
    assert sue_budunit.idea_exists(hr_09_road)
    assert sue_budunit.idea_exists(hr_10_road)
    assert sue_budunit.idea_exists(hr_11_road)
    assert sue_budunit.idea_exists(hr_12_road)
    assert sue_budunit.idea_exists(hr_13_road)
    assert sue_budunit.idea_exists(hr_14_road)
    assert sue_budunit.idea_exists(hr_15_road)
    assert sue_budunit.idea_exists(hr_16_road)
    assert sue_budunit.idea_exists(hr_17_road)
    assert sue_budunit.idea_exists(hr_18_road)
    assert sue_budunit.idea_exists(hr_19_road)
    assert sue_budunit.idea_exists(hr_20_road)
    assert sue_budunit.idea_exists(hr_21_road)
    assert sue_budunit.idea_exists(hr_22_road)
    assert sue_budunit.idea_exists(hr_23_road)
    assert sue_budunit.get_idea_obj(hr_00_road).gogo_want == 0
    assert sue_budunit.get_idea_obj(hr_01_road).gogo_want == 60
    assert sue_budunit.get_idea_obj(hr_02_road).gogo_want == 120
    assert sue_budunit.get_idea_obj(hr_03_road).gogo_want == 180
    assert sue_budunit.get_idea_obj(hr_04_road).gogo_want == 240
    assert sue_budunit.get_idea_obj(hr_05_road).gogo_want == 300
    assert sue_budunit.get_idea_obj(hr_06_road).gogo_want == 360
    assert sue_budunit.get_idea_obj(hr_07_road).gogo_want == 420
    assert sue_budunit.get_idea_obj(hr_08_road).gogo_want == 480
    assert sue_budunit.get_idea_obj(hr_09_road).gogo_want == 540
    assert sue_budunit.get_idea_obj(hr_10_road).gogo_want == 600
    assert sue_budunit.get_idea_obj(hr_11_road).gogo_want == 660
    assert sue_budunit.get_idea_obj(hr_12_road).gogo_want == 720
    assert sue_budunit.get_idea_obj(hr_13_road).gogo_want == 780
    assert sue_budunit.get_idea_obj(hr_14_road).gogo_want == 840
    assert sue_budunit.get_idea_obj(hr_15_road).gogo_want == 900
    assert sue_budunit.get_idea_obj(hr_16_road).gogo_want == 960
    assert sue_budunit.get_idea_obj(hr_17_road).gogo_want == 1020
    assert sue_budunit.get_idea_obj(hr_18_road).gogo_want == 1080
    assert sue_budunit.get_idea_obj(hr_19_road).gogo_want == 1140
    assert sue_budunit.get_idea_obj(hr_20_road).gogo_want == 1200
    assert sue_budunit.get_idea_obj(hr_21_road).gogo_want == 1260
    assert sue_budunit.get_idea_obj(hr_22_road).gogo_want == 1320
    assert sue_budunit.get_idea_obj(hr_23_road).gogo_want == 1380
    assert sue_budunit.get_idea_obj(hr_00_road).stop_want == 60
    assert sue_budunit.get_idea_obj(hr_01_road).stop_want == 120
    assert sue_budunit.get_idea_obj(hr_02_road).stop_want == 180
    assert sue_budunit.get_idea_obj(hr_03_road).stop_want == 240
    assert sue_budunit.get_idea_obj(hr_04_road).stop_want == 300
    assert sue_budunit.get_idea_obj(hr_05_road).stop_want == 360
    assert sue_budunit.get_idea_obj(hr_06_road).stop_want == 420
    assert sue_budunit.get_idea_obj(hr_07_road).stop_want == 480
    assert sue_budunit.get_idea_obj(hr_08_road).stop_want == 540
    assert sue_budunit.get_idea_obj(hr_09_road).stop_want == 600
    assert sue_budunit.get_idea_obj(hr_10_road).stop_want == 660
    assert sue_budunit.get_idea_obj(hr_11_road).stop_want == 720
    assert sue_budunit.get_idea_obj(hr_12_road).stop_want == 780
    assert sue_budunit.get_idea_obj(hr_13_road).stop_want == 840
    assert sue_budunit.get_idea_obj(hr_14_road).stop_want == 900
    assert sue_budunit.get_idea_obj(hr_15_road).stop_want == 960
    assert sue_budunit.get_idea_obj(hr_16_road).stop_want == 1020
    assert sue_budunit.get_idea_obj(hr_17_road).stop_want == 1080
    assert sue_budunit.get_idea_obj(hr_18_road).stop_want == 1140
    assert sue_budunit.get_idea_obj(hr_19_road).stop_want == 1200
    assert sue_budunit.get_idea_obj(hr_20_road).stop_want == 1260
    assert sue_budunit.get_idea_obj(hr_21_road).stop_want == 1320
    assert sue_budunit.get_idea_obj(hr_22_road).stop_want == 1380
    assert sue_budunit.get_idea_obj(hr_23_road).stop_want == 1440


# def test_BudUnit_get_idea_ranged_kids_ReturnsSomeChildrenScenario2():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_creg_ideas(c400_count=7)

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
#     sue_budunit.set_time_creg_ideas(c400_count=7)

#     # WHEN THEN
#     time_road = sue_budunit.make_l1_road("time")
#     tech_road = sue_budunit.make_road(time_road, "tech")
#     week_road = sue_budunit.make_road(tech_road, "week")
#     assert len(sue_budunit.get_idea_ranged_kids(idea_road=week_road, begin=0)) == 1
#     assert len(sue_budunit.get_idea_ranged_kids(idea_road=week_road, begin=1440)) == 1


def test_BudUnit_get_agenda_dict_DoesNotReturnPledgeItemsOutsideRange():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = add_time_creg_ideaunit(budunit_shop(sue_str))
    clean_str = "clean"
    clean_road = sue_bud.make_l1_road(clean_str)
    sue_bud.set_l1_idea(ideaunit_shop(clean_str, pledge=True))
    time_road = sue_bud.make_l1_road("time")
    cregtime_road = sue_bud.make_road(time_road, creg_str())
    day_road = sue_bud.make_road(cregtime_road, "day")

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
    sue_bud.set_fact(
        base=cregtime_road, pick=cregtime_road, fopen=open_x, fnigh=nigh_x1
    )

    # THEN
    agenda_dict = sue_bud.get_agenda_dict()
    print(f"{agenda_dict.keys()=}")
    assert len(agenda_dict) == 1
    assert clean_road in agenda_dict.keys()

    # WHEN
    # nigh_x2 = 1063971923
    open_x2 = 0
    nigh_x2 = 0
    sue_bud.set_fact(
        base=cregtime_road, pick=cregtime_road, fopen=open_x2, fnigh=nigh_x2
    )
    print(f"YAYA {sue_bud._idearoot.factunits=}")

    # THEN
    agenda_dict = sue_bud.get_agenda_dict()
    assert len(agenda_dict) == 0


def test_BudUnit_create_agenda_item_CorrectlyCreatesAllBudAttributes():
    # WHEN "I am cleaning the cookery since I'm in the flat and it's 8am and it's dirty and it's for my family"

    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    assert len(sue_bud._accts) == 0
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0

    clean_things_str = "cleaning things"
    clean_things_road = sue_bud.make_l1_road(clean_things_str)
    sweep_str = "sweep"
    sweep_road = sue_bud.make_road(clean_things_road, sweep_str)
    sweep_idea = ideaunit_shop(sweep_str, _parent_road=clean_things_road)
    print(f"{sweep_idea.get_road()=}")
    house_str = "house"
    house_road = sue_bud.make_l1_road(house_str)
    cookery_room_str = "cookery room"
    cookery_room_road = sue_bud.make_road(house_road, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_road = sue_bud.make_road(cookery_room_road, cookery_dirty_str)

    # create gregorian timeline
    add_time_creg_ideaunit(sue_bud)
    time_road = sue_bud.make_l1_road("time")
    cregtime_road = sue_bud.make_road(time_road, creg_str())
    creg_idea = sue_bud.get_idea_obj(cregtime_road)
    print(f"{creg_idea._kids.keys()=}")
    daytime_road = sue_bud.make_road(cregtime_road, "day")
    open_8am = 480
    nigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_road)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
    sweep_idea.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_road)
    daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
    sweep_idea.set_reasonunit(reason=daytime_reason)

    family_str = ",family"
    awardlink_z = awardlink_shop(group_id=family_str)
    sweep_idea.set_awardlink(awardlink_z)

    assert len(sue_bud._accts) == 0
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert len(sue_bud._idearoot._kids) == 1
    assert sue_bud.get_idea_obj(daytime_road).denom == 1440
    assert sue_bud.get_idea_obj(daytime_road).morph
    print(f"{sweep_idea.get_road()=}")

    # ESTABLISH
    sue_bud.set_dominate_pledge_idea(idea_kid=sweep_idea)

    # THEN
    # for idea_kid in sue_bud._idearoot._kids.keys():
    #     print(f"  {idea_kid=}")

    print(f"{sweep_idea.get_road()=}")
    assert sue_bud.get_idea_obj(sweep_road) is not None
    assert sue_bud.get_idea_obj(sweep_road)._label == sweep_str
    assert sue_bud.get_idea_obj(sweep_road).pledge
    assert len(sue_bud.get_idea_obj(sweep_road).reasonunits) == 2
    assert sue_bud.get_idea_obj(clean_things_road) is not None
    assert sue_bud.get_idea_obj(cookery_room_road) is not None
    assert sue_bud.get_idea_obj(cookery_dirty_road) is not None
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert sue_bud.get_acctunit_group_ids_dict().get(family_str) is None

    assert len(sue_bud._idearoot._kids) == 3


def test_IdeaCore_get_agenda_dict_ReturnsCorrectObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    add_time_creg_ideaunit(sue_bud)

    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    laundry_str = "do_laundry"
    laundry_road = sue_bud.make_road(casa_road, laundry_str)
    sue_bud.set_l1_idea(ideaunit_shop(casa_str))
    sue_bud.set_idea(ideaunit_shop(laundry_str, pledge=True), casa_road)
    time_road = sue_bud.make_l1_road("time")
    cregtime_road = sue_bud.make_road(time_road, creg_str())
    sue_bud.edit_idea_attr(
        road=laundry_road,
        reason_base=cregtime_road,
        reason_premise=cregtime_road,
        reason_premise_open=3420.0,
        reason_premise_nigh=3420.0,
        reason_premise_divisor=10080.0,
    )
    print("set first fact")

    sue_bud.set_fact(cregtime_road, cregtime_road, 1064131200, fnigh=1064135133)
    print("get 1st agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")
    assert sue_agenda_dict == {}

    laundry_idea = sue_bud.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(cregtime_road)
    laundry_premise = laundry_reasonheir.get_premise(cregtime_road)
    laundry_factheir = laundry_idea._factheirs.get(cregtime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.fopen % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.fnigh % 10080=}"
    # )
    # print(f"{laundry_reasonheir.base=} {laundry_premise=}")
    # for x_ideaunit in sue_bud._idea_dict.values():
    #     if x_ideaunit._label in [laundry_str]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit.begin=} {x_ideaunit.close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")

    # WHEN
    print("set 2nd fact")
    sue_bud.set_fact(cregtime_road, cregtime_road, 1064131200, fnigh=1064136133)
    print("get 2nd agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")

    laundry_idea = sue_bud.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(cregtime_road)
    laundry_premise = laundry_reasonheir.get_premise(cregtime_road)
    laundry_factheir = laundry_idea._factheirs.get(cregtime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_factheir.fopen % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_factheir.fnigh % 10080=}"
    # )
    # for x_ideaunit in sue_bud._idea_dict.values():
    #     if x_ideaunit._label in [laundry_str]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit.begin=} {x_ideaunit.close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")
    #         creg_factheir = x_ideaunit._factheirs.get(cregtime_road)
    #         print(f"{creg_factheir.fopen % 10080=}")
    #         print(f"{creg_factheir.fnigh % 10080=}")

    # THEN
    assert sue_agenda_dict == {}


def test_add_newtimeline_ideaunit_CorrectlyAddsMultiple_timelines():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road(time_str())
    creg_road = sue_bud.make_road(time_road, creg_str())
    five_road = sue_bud.make_road(time_road, five_str())
    creg_yr1_jan1_offset_road = sue_bud.make_road(creg_road, yr1_jan1_offset_str())
    five_yr1_jan1_offset_road = sue_bud.make_road(five_road, yr1_jan1_offset_str())
    creg_year_road = get_year_road(sue_bud, creg_road)
    five_year_road = get_year_road(sue_bud, five_road)
    print(f"{creg_year_road=}")
    print(f"{five_year_road=}")
    # print(f"{sue_bud._idea_dict.keys()=}")

    assert not sue_bud.idea_exists(five_year_road)
    assert sue_bud.idea_exists(creg_year_road)
    assert sue_bud.idea_exists(creg_yr1_jan1_offset_road)
    creg_offset_idea = sue_bud.get_idea_obj(creg_yr1_jan1_offset_road)
    assert creg_offset_idea.addin == get_creg_config().get(yr1_jan1_offset_str())
    assert not sue_bud.idea_exists(five_yr1_jan1_offset_road)

    # WHEN
    sue_bud = add_time_five_ideaunit(sue_bud)

    # THEN
    assert sue_bud.idea_exists(five_year_road)
    assert sue_bud.idea_exists(creg_year_road)
    assert sue_bud.idea_exists(creg_yr1_jan1_offset_road)
    assert sue_bud.idea_exists(five_yr1_jan1_offset_road)
    five_offset_idea = sue_bud.get_idea_obj(five_yr1_jan1_offset_road)
    assert five_offset_idea.addin == get_five_config().get(yr1_jan1_offset_str())


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
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    x_datetime = datetime(2022, 10, 30, 0, 0)
    time_road = sue_bud.make_l1_road(time_str())
    creg_road = sue_bud.make_road(time_road, creg_str())

    # WHEN
    creg_min = get_min_from_dt(sue_bud, creg_road, x_datetime)

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
