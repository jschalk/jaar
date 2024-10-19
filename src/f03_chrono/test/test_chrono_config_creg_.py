from src.f00_instrument.plotly_tool import conditional_fig_show
from src.f02_bud.group import awardlink_shop
from src.f02_bud.reason_item import reasonunit_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f03_chrono.chrono import (
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
    monthday_distortion_str,
    get_min_from_dt,
)
from src.f03_chrono.examples.chrono_examples import (
    add_time_creg_itemunit,
    add_time_five_itemunit,
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
    cregtime_itemunit,
    creg_weekday_itemunits,
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
    assert creg_config.get(monthday_distortion_str()) == 1
    assert five_config.get(monthday_distortion_str()) == 0


def test_cregtime_itemunit_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert cregtime_itemunit().begin == 0
    assert cregtime_itemunit().close == 1472657760
    assert cregtime_itemunit().close == get_c400_constants().c400_leap_length * 7


def test_creg_weekday_itemunits_ReturnsObj():
    assert creg_weekday_itemunits().get(get_wed()).gogo_want == 0
    assert creg_weekday_itemunits().get(get_thu()).gogo_want == 1440
    assert creg_weekday_itemunits().get(get_fri()).gogo_want == 2880
    assert creg_weekday_itemunits().get(get_sat()).gogo_want == 4320
    assert creg_weekday_itemunits().get(get_sun()).gogo_want == 5760
    assert creg_weekday_itemunits().get(get_mon()).gogo_want == 7200
    assert creg_weekday_itemunits().get(get_tue()).gogo_want == 8640
    assert creg_weekday_itemunits().get(get_wed()).stop_want == 1440
    assert creg_weekday_itemunits().get(get_thu()).stop_want == 2880
    assert creg_weekday_itemunits().get(get_fri()).stop_want == 4320
    assert creg_weekday_itemunits().get(get_sat()).stop_want == 5760
    assert creg_weekday_itemunits().get(get_sun()).stop_want == 7200
    assert creg_weekday_itemunits().get(get_mon()).stop_want == 8640
    assert creg_weekday_itemunits().get(get_tue()).stop_want == 10080


def test_add_time_creg_itemunit_ReturnsObjWith_days():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    day_road = sue_budunit.make_road(creg_road, day_str())
    days_road = sue_budunit.make_road(creg_road, days_str())
    print(f"{time_road=}")
    print(f"{creg_road=}")
    print(f"{day_road=}")
    assert not sue_budunit.item_exists(time_road)
    assert not sue_budunit.item_exists(creg_road)
    assert not sue_budunit.item_exists(day_road)
    assert not sue_budunit.item_exists(days_road)

    # WHEN
    sue_budunit = add_time_creg_itemunit(sue_budunit)

    # THEN
    assert sue_budunit.item_exists(time_road)
    assert sue_budunit.item_exists(creg_road)
    assert sue_budunit.item_exists(day_road)
    assert sue_budunit.item_exists(days_road)
    assert sue_budunit.get_item_obj(creg_road).begin == 0
    assert sue_budunit.get_item_obj(creg_road).close == 1472657760
    assert sue_budunit.get_item_obj(day_road).denom == 1440
    assert sue_budunit.get_item_obj(day_road).morph
    assert sue_budunit.get_item_obj(days_road).denom == 1440
    assert sue_budunit.get_item_obj(days_road).morph is None


def test_add_time_creg_itemunit_ReturnsObjWith_weeks():
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

    assert not sue_budunit.item_exists(week_road)
    assert not sue_budunit.item_exists(sun_road)
    assert not sue_budunit.item_exists(mon_road)
    assert not sue_budunit.item_exists(tue_road)
    assert not sue_budunit.item_exists(wed_road)
    assert not sue_budunit.item_exists(thu_road)
    assert not sue_budunit.item_exists(fri_road)
    assert not sue_budunit.item_exists(sat_road)
    assert not sue_budunit.item_exists(weeks_road)

    # WHEN
    sue_budunit = add_time_creg_itemunit(sue_budunit)

    # THEN
    assert sue_budunit.item_exists(week_road)
    assert sue_budunit.get_item_obj(week_road).gogo_want is None
    assert sue_budunit.get_item_obj(week_road).stop_want is None
    assert sue_budunit.get_item_obj(week_road).denom == 10080
    assert sue_budunit.get_item_obj(week_road).morph
    assert sue_budunit.item_exists(sun_road)
    assert sue_budunit.item_exists(mon_road)
    assert sue_budunit.item_exists(tue_road)
    assert sue_budunit.item_exists(wed_road)
    assert sue_budunit.item_exists(thu_road)
    assert sue_budunit.item_exists(fri_road)
    assert sue_budunit.item_exists(sat_road)
    assert sue_budunit.item_exists(weeks_road)
    assert sue_budunit.get_item_obj(weeks_road).denom == 10080
    assert sue_budunit.get_item_obj(weeks_road).morph is None


def test_add_time_creg_itemunit_ReturnsObjWith_c400_leap_road():
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

    assert not sue_budunit.item_exists(c400_leap_road)

    # WHEN
    sue_budunit = add_time_creg_itemunit(sue_budunit)

    # THEN
    assert sue_budunit.item_exists(c400_leap_road)
    c400_leap_item = sue_budunit.get_item_obj(c400_leap_road)
    assert not c400_leap_item.gogo_want
    assert not c400_leap_item.stop_want
    assert c400_leap_item.denom == 210379680
    assert c400_leap_item.morph

    assert sue_budunit.item_exists(c400_clean_road)
    c400_clean_item = sue_budunit.get_item_obj(c400_clean_road)
    assert not c400_clean_item.gogo_want
    assert not c400_clean_item.stop_want
    assert c400_clean_item.denom == 210378240
    assert c400_clean_item.morph

    assert sue_budunit.item_exists(c100_road)
    c100_item = sue_budunit.get_item_obj(c100_road)
    assert not c100_item.gogo_want
    assert not c100_item.stop_want
    assert c100_item.denom == 52594560
    assert c100_item.morph

    assert sue_budunit.item_exists(yr4_leap_road)
    yr4_leap_item = sue_budunit.get_item_obj(yr4_leap_road)
    assert not yr4_leap_item.gogo_want
    assert not yr4_leap_item.stop_want
    assert yr4_leap_item.denom == 2103840
    assert yr4_leap_item.morph

    assert sue_budunit.item_exists(yr4_clean_road)
    yr4_clean_item = sue_budunit.get_item_obj(yr4_clean_road)
    assert not yr4_clean_item.gogo_want
    assert not yr4_clean_item.stop_want
    assert yr4_clean_item.denom == 2102400
    assert yr4_clean_item.morph

    assert sue_budunit.item_exists(year_road)
    year_item = sue_budunit.get_item_obj(year_road)
    assert not year_item.gogo_want
    assert not year_item.stop_want
    assert year_item.denom == 525600
    assert year_item.morph


def test_add_time_creg_itemunit_ReturnsObjWith_years():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    year_road = get_year_road(sue_budunit, creg_road)

    assert not sue_budunit.item_exists(creg_road)
    assert not sue_budunit.item_exists(year_road)

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
    assert not sue_budunit.item_exists(jan_road)
    assert not sue_budunit.item_exists(feb_road)
    assert not sue_budunit.item_exists(mar_road)
    assert not sue_budunit.item_exists(apr_road)
    assert not sue_budunit.item_exists(may_road)
    assert not sue_budunit.item_exists(jun_road)
    assert not sue_budunit.item_exists(jul_road)
    assert not sue_budunit.item_exists(aug_road)
    assert not sue_budunit.item_exists(sep_road)
    assert not sue_budunit.item_exists(oct_road)
    assert not sue_budunit.item_exists(nov_road)
    assert not sue_budunit.item_exists(dec_road)
    assert not sue_budunit.item_exists(year_road)

    # WHEN
    sue_budunit = add_time_creg_itemunit(sue_budunit)

    # THEN
    assert sue_budunit.item_exists(creg_road)
    assert sue_budunit.item_exists(year_road)

    year_item = sue_budunit.get_item_obj(year_road)
    # assert year_item.morph
    assert sue_budunit.item_exists(jan_road)
    assert sue_budunit.item_exists(feb_road)
    assert sue_budunit.item_exists(mar_road)
    assert sue_budunit.item_exists(apr_road)
    assert sue_budunit.item_exists(may_road)
    assert sue_budunit.item_exists(jun_road)
    assert sue_budunit.item_exists(jul_road)
    assert sue_budunit.item_exists(aug_road)
    assert sue_budunit.item_exists(sep_road)
    assert sue_budunit.item_exists(oct_road)
    assert sue_budunit.item_exists(nov_road)
    assert sue_budunit.item_exists(dec_road)
    assert sue_budunit.get_item_obj(jan_road).addin == 1440
    assert sue_budunit.get_item_obj(feb_road).addin == 1440
    assert sue_budunit.get_item_obj(mar_road).addin == 1440
    assert sue_budunit.get_item_obj(apr_road).addin == 1440
    assert sue_budunit.get_item_obj(may_road).addin == 1440
    assert sue_budunit.get_item_obj(jun_road).addin == 1440
    assert sue_budunit.get_item_obj(jul_road).addin == 1440
    assert sue_budunit.get_item_obj(aug_road).addin == 1440
    assert sue_budunit.get_item_obj(sep_road).addin == 1440
    assert sue_budunit.get_item_obj(oct_road).addin == 1440
    assert sue_budunit.get_item_obj(nov_road).addin == 1440
    assert sue_budunit.get_item_obj(dec_road).addin == 1440

    assert sue_budunit.get_item_obj(jan_road).gogo_want == 440640
    assert sue_budunit.get_item_obj(feb_road).gogo_want == 485280
    assert sue_budunit.get_item_obj(mar_road).gogo_want == 0
    assert sue_budunit.get_item_obj(apr_road).gogo_want == 44640
    assert sue_budunit.get_item_obj(may_road).gogo_want == 87840
    assert sue_budunit.get_item_obj(jun_road).gogo_want == 132480
    assert sue_budunit.get_item_obj(jul_road).gogo_want == 175680
    assert sue_budunit.get_item_obj(aug_road).gogo_want == 220320
    assert sue_budunit.get_item_obj(sep_road).gogo_want == 264960
    assert sue_budunit.get_item_obj(oct_road).gogo_want == 308160
    assert sue_budunit.get_item_obj(nov_road).gogo_want == 352800
    assert sue_budunit.get_item_obj(dec_road).gogo_want == 396000

    assert sue_budunit.get_item_obj(jan_road).stop_want == 485280
    assert sue_budunit.get_item_obj(feb_road).stop_want == 525600
    assert sue_budunit.get_item_obj(mar_road).stop_want == 44640
    assert sue_budunit.get_item_obj(apr_road).stop_want == 87840
    assert sue_budunit.get_item_obj(may_road).stop_want == 132480
    assert sue_budunit.get_item_obj(jun_road).stop_want == 175680
    assert sue_budunit.get_item_obj(jul_road).stop_want == 220320
    assert sue_budunit.get_item_obj(aug_road).stop_want == 264960
    assert sue_budunit.get_item_obj(sep_road).stop_want == 308160
    assert sue_budunit.get_item_obj(oct_road).stop_want == 352800
    assert sue_budunit.get_item_obj(nov_road).stop_want == 396000
    assert sue_budunit.get_item_obj(dec_road).stop_want == 440640


def test_add_time_creg_itemunit_ReturnsObjWith_c400_leap():
    # ESTABLISH
    sue_budunit = budunit_shop("Sue")
    time_road = sue_budunit.make_l1_road(time_str())
    creg_road = sue_budunit.make_road(time_road, get_cregtime_str())
    day_road = sue_budunit.make_road(creg_road, day_str())
    days_road = sue_budunit.make_road(creg_road, days_str())
    print(f"{time_road=}")
    print(f"{creg_road=}")
    print(f"{day_road=}")
    assert not sue_budunit.item_exists(time_road)
    assert not sue_budunit.item_exists(creg_road)
    assert not sue_budunit.item_exists(day_road)
    assert not sue_budunit.item_exists(days_road)

    # WHEN
    sue_budunit = add_time_creg_itemunit(sue_budunit)

    # THEN
    assert sue_budunit.item_exists(time_road)
    assert sue_budunit.item_exists(creg_road)
    creg_item = sue_budunit.get_item_obj(creg_road)
    assert creg_item.begin == 0
    assert creg_item.close == 1472657760
    assert sue_budunit.item_exists(day_road)
    day_item = sue_budunit.get_item_obj(day_road)
    assert day_item.denom == 1440
    assert day_item.morph
    assert sue_budunit.item_exists(days_road)
    days_item = sue_budunit.get_item_obj(days_road)
    assert days_item.denom == 1440
    assert not days_item.morph


def test_add_time_creg_itemunit_ReturnsObjWith_hours():
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
    assert not sue_budunit.item_exists(time_road)
    assert not sue_budunit.item_exists(creg_road)
    assert not sue_budunit.item_exists(day_road)
    assert not sue_budunit.item_exists(hr_00_road)
    assert not sue_budunit.item_exists(hr_01_road)
    assert not sue_budunit.item_exists(hr_02_road)
    assert not sue_budunit.item_exists(hr_03_road)
    assert not sue_budunit.item_exists(hr_04_road)
    assert not sue_budunit.item_exists(hr_05_road)
    assert not sue_budunit.item_exists(hr_06_road)
    assert not sue_budunit.item_exists(hr_07_road)
    assert not sue_budunit.item_exists(hr_08_road)
    assert not sue_budunit.item_exists(hr_09_road)
    assert not sue_budunit.item_exists(hr_10_road)
    assert not sue_budunit.item_exists(hr_11_road)
    assert not sue_budunit.item_exists(hr_12_road)
    assert not sue_budunit.item_exists(hr_13_road)
    assert not sue_budunit.item_exists(hr_14_road)
    assert not sue_budunit.item_exists(hr_15_road)
    assert not sue_budunit.item_exists(hr_16_road)
    assert not sue_budunit.item_exists(hr_17_road)
    assert not sue_budunit.item_exists(hr_18_road)
    assert not sue_budunit.item_exists(hr_19_road)
    assert not sue_budunit.item_exists(hr_20_road)
    assert not sue_budunit.item_exists(hr_21_road)
    assert not sue_budunit.item_exists(hr_22_road)
    assert not sue_budunit.item_exists(hr_23_road)

    # WHEN
    sue_budunit = add_time_creg_itemunit(sue_budunit)

    # THEN
    day_item = sue_budunit.get_item_obj(day_road)
    print(f"{day_item._kids.keys()=}")
    assert sue_budunit.item_exists(time_road)
    assert sue_budunit.item_exists(creg_road)
    assert sue_budunit.item_exists(day_road)
    # assert sue_budunit.get_item_obj(hour_road).denom == 60
    # assert sue_budunit.get_item_obj(hour_road).morph
    # assert not sue_budunit.get_item_obj(hour_road).gogo_want
    # assert not sue_budunit.get_item_obj(hour_road).stop_want
    assert sue_budunit.item_exists(hr_00_road)
    assert sue_budunit.item_exists(hr_01_road)
    assert sue_budunit.item_exists(hr_02_road)
    assert sue_budunit.item_exists(hr_03_road)
    assert sue_budunit.item_exists(hr_04_road)
    assert sue_budunit.item_exists(hr_05_road)
    assert sue_budunit.item_exists(hr_06_road)
    assert sue_budunit.item_exists(hr_07_road)
    assert sue_budunit.item_exists(hr_08_road)
    assert sue_budunit.item_exists(hr_09_road)
    assert sue_budunit.item_exists(hr_10_road)
    assert sue_budunit.item_exists(hr_11_road)
    assert sue_budunit.item_exists(hr_12_road)
    assert sue_budunit.item_exists(hr_13_road)
    assert sue_budunit.item_exists(hr_14_road)
    assert sue_budunit.item_exists(hr_15_road)
    assert sue_budunit.item_exists(hr_16_road)
    assert sue_budunit.item_exists(hr_17_road)
    assert sue_budunit.item_exists(hr_18_road)
    assert sue_budunit.item_exists(hr_19_road)
    assert sue_budunit.item_exists(hr_20_road)
    assert sue_budunit.item_exists(hr_21_road)
    assert sue_budunit.item_exists(hr_22_road)
    assert sue_budunit.item_exists(hr_23_road)
    assert sue_budunit.get_item_obj(hr_00_road).gogo_want == 0
    assert sue_budunit.get_item_obj(hr_01_road).gogo_want == 60
    assert sue_budunit.get_item_obj(hr_02_road).gogo_want == 120
    assert sue_budunit.get_item_obj(hr_03_road).gogo_want == 180
    assert sue_budunit.get_item_obj(hr_04_road).gogo_want == 240
    assert sue_budunit.get_item_obj(hr_05_road).gogo_want == 300
    assert sue_budunit.get_item_obj(hr_06_road).gogo_want == 360
    assert sue_budunit.get_item_obj(hr_07_road).gogo_want == 420
    assert sue_budunit.get_item_obj(hr_08_road).gogo_want == 480
    assert sue_budunit.get_item_obj(hr_09_road).gogo_want == 540
    assert sue_budunit.get_item_obj(hr_10_road).gogo_want == 600
    assert sue_budunit.get_item_obj(hr_11_road).gogo_want == 660
    assert sue_budunit.get_item_obj(hr_12_road).gogo_want == 720
    assert sue_budunit.get_item_obj(hr_13_road).gogo_want == 780
    assert sue_budunit.get_item_obj(hr_14_road).gogo_want == 840
    assert sue_budunit.get_item_obj(hr_15_road).gogo_want == 900
    assert sue_budunit.get_item_obj(hr_16_road).gogo_want == 960
    assert sue_budunit.get_item_obj(hr_17_road).gogo_want == 1020
    assert sue_budunit.get_item_obj(hr_18_road).gogo_want == 1080
    assert sue_budunit.get_item_obj(hr_19_road).gogo_want == 1140
    assert sue_budunit.get_item_obj(hr_20_road).gogo_want == 1200
    assert sue_budunit.get_item_obj(hr_21_road).gogo_want == 1260
    assert sue_budunit.get_item_obj(hr_22_road).gogo_want == 1320
    assert sue_budunit.get_item_obj(hr_23_road).gogo_want == 1380
    assert sue_budunit.get_item_obj(hr_00_road).stop_want == 60
    assert sue_budunit.get_item_obj(hr_01_road).stop_want == 120
    assert sue_budunit.get_item_obj(hr_02_road).stop_want == 180
    assert sue_budunit.get_item_obj(hr_03_road).stop_want == 240
    assert sue_budunit.get_item_obj(hr_04_road).stop_want == 300
    assert sue_budunit.get_item_obj(hr_05_road).stop_want == 360
    assert sue_budunit.get_item_obj(hr_06_road).stop_want == 420
    assert sue_budunit.get_item_obj(hr_07_road).stop_want == 480
    assert sue_budunit.get_item_obj(hr_08_road).stop_want == 540
    assert sue_budunit.get_item_obj(hr_09_road).stop_want == 600
    assert sue_budunit.get_item_obj(hr_10_road).stop_want == 660
    assert sue_budunit.get_item_obj(hr_11_road).stop_want == 720
    assert sue_budunit.get_item_obj(hr_12_road).stop_want == 780
    assert sue_budunit.get_item_obj(hr_13_road).stop_want == 840
    assert sue_budunit.get_item_obj(hr_14_road).stop_want == 900
    assert sue_budunit.get_item_obj(hr_15_road).stop_want == 960
    assert sue_budunit.get_item_obj(hr_16_road).stop_want == 1020
    assert sue_budunit.get_item_obj(hr_17_road).stop_want == 1080
    assert sue_budunit.get_item_obj(hr_18_road).stop_want == 1140
    assert sue_budunit.get_item_obj(hr_19_road).stop_want == 1200
    assert sue_budunit.get_item_obj(hr_20_road).stop_want == 1260
    assert sue_budunit.get_item_obj(hr_21_road).stop_want == 1320
    assert sue_budunit.get_item_obj(hr_22_road).stop_want == 1380
    assert sue_budunit.get_item_obj(hr_23_road).stop_want == 1440


def test_add_time_creg_itemunit_ReturnsObjWith_offset_ItemUnits():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road(time_str())
    creg_road = sue_bud.make_road(time_road, creg_str())
    five_road = sue_bud.make_road(time_road, five_str())
    creg_yr1_jan1_offset_road = sue_bud.make_road(creg_road, yr1_jan1_offset_str())
    five_yr1_jan1_offset_road = sue_bud.make_road(five_road, yr1_jan1_offset_str())

    assert sue_bud.item_exists(creg_yr1_jan1_offset_road)
    creg_yr1_offset_item = sue_bud.get_item_obj(creg_yr1_jan1_offset_road)
    assert creg_yr1_offset_item.addin == get_creg_config().get(yr1_jan1_offset_str())
    assert not sue_bud.item_exists(five_yr1_jan1_offset_road)

    # WHEN
    sue_bud = add_time_five_itemunit(sue_bud)

    # THEN
    assert sue_bud.item_exists(creg_yr1_jan1_offset_road)
    assert sue_bud.item_exists(five_yr1_jan1_offset_road)
    five_yr1_offset_item = sue_bud.get_item_obj(five_yr1_jan1_offset_road)
    assert five_yr1_offset_item.addin == get_five_config().get(yr1_jan1_offset_str())


# def test_BudUnit_get_item_ranged_kids_ReturnsSomeChildrenScenario2():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_creg_items(c400_count=7)

#     # WHEN THEN
#     time_road = sue_budunit.make_l1_road("time")
#     tech_road = sue_budunit.make_road(time_road, "tech")
#     week_road = sue_budunit.make_road(tech_road, "week")
#     assert len(sue_budunit.get_item_ranged_kids(week_road, begin=0, close=1440)) == 1
#     assert len(sue_budunit.get_item_ranged_kids(week_road, begin=0, close=2000)) == 2
#     assert len(sue_budunit.get_item_ranged_kids(week_road, begin=0, close=3000)) == 3


# def test_BudUnit_get_item_ranged_kids_ReturnsSomeChildrenScenario3():
#     # ESTABLISH
#     sue_budunit = budunit_shop("Sue")
#     sue_budunit.set_time_creg_items(c400_count=7)

#     # WHEN THEN
#     time_road = sue_budunit.make_l1_road("time")
#     tech_road = sue_budunit.make_road(time_road, "tech")
#     week_road = sue_budunit.make_road(tech_road, "week")
#     assert len(sue_budunit.get_item_ranged_kids(item_road=week_road, begin=0)) == 1
#     assert len(sue_budunit.get_item_ranged_kids(item_road=week_road, begin=1440)) == 1


def test_BudUnit_get_agenda_dict_DoesNotReturnPledgeItemsOutsideRange():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = add_time_creg_itemunit(budunit_shop(sue_str))
    clean_str = "clean"
    clean_road = sue_bud.make_l1_road(clean_str)
    sue_bud.set_l1_item(itemunit_shop(clean_str, pledge=True))
    time_road = sue_bud.make_l1_road("time")
    cregtime_road = sue_bud.make_road(time_road, creg_str())
    day_road = sue_bud.make_road(cregtime_road, "day")

    sue_bud.edit_item_attr(
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
    print(f"YAYA {sue_bud._itemroot.factunits=}")

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
    sweep_item = itemunit_shop(sweep_str, _parent_road=clean_things_road)
    print(f"{sweep_item.get_road()=}")
    house_str = "house"
    house_road = sue_bud.make_l1_road(house_str)
    cookery_room_str = "cookery room"
    cookery_room_road = sue_bud.make_road(house_road, cookery_room_str)
    cookery_dirty_str = "dirty"
    cookery_dirty_road = sue_bud.make_road(cookery_room_road, cookery_dirty_str)

    # create gregorian timeline
    add_time_creg_itemunit(sue_bud)
    time_road = sue_bud.make_l1_road("time")
    cregtime_road = sue_bud.make_road(time_road, creg_str())
    creg_item = sue_bud.get_item_obj(cregtime_road)
    print(f"{creg_item._kids.keys()=}")
    daytime_road = sue_bud.make_road(cregtime_road, "day")
    open_8am = 480
    nigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_road)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
    sweep_item.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_road)
    daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
    sweep_item.set_reasonunit(reason=daytime_reason)

    family_str = ",family"
    awardlink_z = awardlink_shop(awardee_id=family_str)
    sweep_item.set_awardlink(awardlink_z)

    assert len(sue_bud._accts) == 0
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert len(sue_bud._itemroot._kids) == 1
    assert sue_bud.get_item_obj(daytime_road).denom == 1440
    assert sue_bud.get_item_obj(daytime_road).morph
    print(f"{sweep_item.get_road()=}")

    # ESTABLISH
    sue_bud.set_dominate_pledge_item(item_kid=sweep_item)

    # THEN
    # for item_kid in sue_bud._itemroot._kids.keys():
    #     print(f"  {item_kid=}")

    print(f"{sweep_item.get_road()=}")
    assert sue_bud.get_item_obj(sweep_road) is not None
    assert sue_bud.get_item_obj(sweep_road)._label == sweep_str
    assert sue_bud.get_item_obj(sweep_road).pledge
    assert len(sue_bud.get_item_obj(sweep_road).reasonunits) == 2
    assert sue_bud.get_item_obj(clean_things_road) is not None
    assert sue_bud.get_item_obj(cookery_room_road) is not None
    assert sue_bud.get_item_obj(cookery_dirty_road) is not None
    assert len(sue_bud.get_acctunit_group_ids_dict()) == 0
    assert sue_bud.get_acctunit_group_ids_dict().get(family_str) is None

    assert len(sue_bud._itemroot._kids) == 3


def test_ItemCore_get_agenda_dict_ReturnsCorrectObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    add_time_creg_itemunit(sue_bud)

    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    laundry_str = "do_laundry"
    laundry_road = sue_bud.make_road(casa_road, laundry_str)
    sue_bud.set_l1_item(itemunit_shop(casa_str))
    sue_bud.set_item(itemunit_shop(laundry_str, pledge=True), casa_road)
    time_road = sue_bud.make_l1_road("time")
    cregtime_road = sue_bud.make_road(time_road, creg_str())
    sue_bud.edit_item_attr(
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

    laundry_item = sue_bud.get_item_obj(laundry_road)
    laundry_reasonheir = laundry_item.get_reasonheir(cregtime_road)
    laundry_premise = laundry_reasonheir.get_premise(cregtime_road)
    laundry_factheir = laundry_item._factheirs.get(cregtime_road)
    # print(
    #     f"{laundry_item._active=} {laundry_premise.open=} {laundry_factheir.fopen % 10080=}"
    # )
    # print(
    #     f"{laundry_item._active=} {laundry_premise.nigh=} {laundry_factheir.fnigh % 10080=}"
    # )
    # print(f"{laundry_reasonheir.base=} {laundry_premise=}")
    # for x_itemunit in sue_bud._item_dict.values():
    #     if x_itemunit._label in [laundry_str]:
    #         print(f"{x_itemunit._label=} {x_itemunit.begin=} {x_itemunit.close=}")
    #         print(f"{x_itemunit._kids.keys()=}")

    # WHEN
    print("set 2nd fact")
    sue_bud.set_fact(cregtime_road, cregtime_road, 1064131200, fnigh=1064136133)
    print("get 2nd agenda dictionary")
    sue_agenda_dict = sue_bud.get_agenda_dict()
    print(f"{sue_agenda_dict.keys()=}")

    laundry_item = sue_bud.get_item_obj(laundry_road)
    laundry_reasonheir = laundry_item.get_reasonheir(cregtime_road)
    laundry_premise = laundry_reasonheir.get_premise(cregtime_road)
    laundry_factheir = laundry_item._factheirs.get(cregtime_road)
    # print(
    #     f"{laundry_item._active=} {laundry_premise.open=} {laundry_factheir.fopen % 10080=}"
    # )
    # print(
    #     f"{laundry_item._active=} {laundry_premise.nigh=} {laundry_factheir.fnigh % 10080=}"
    # )
    # for x_itemunit in sue_bud._item_dict.values():
    #     if x_itemunit._label in [laundry_str]:
    #         print(f"{x_itemunit._label=} {x_itemunit.begin=} {x_itemunit.close=}")
    #         print(f"{x_itemunit._kids.keys()=}")
    #         creg_factheir = x_itemunit._factheirs.get(cregtime_road)
    #         print(f"{creg_factheir.fopen % 10080=}")
    #         print(f"{creg_factheir.fnigh % 10080=}")

    # THEN
    assert sue_agenda_dict == {}


def test_add_newtimeline_itemunit_CorrectlyAddsMultiple_timelines():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
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
    # print(f"{sue_bud._item_dict.keys()=}")

    assert not sue_bud.item_exists(five_year_road)
    assert sue_bud.item_exists(creg_year_road)
    assert sue_bud.item_exists(creg_yr1_jan1_offset_road)
    creg_offset_item = sue_bud.get_item_obj(creg_yr1_jan1_offset_road)
    assert creg_offset_item.addin == get_creg_config().get(yr1_jan1_offset_str())
    assert not sue_bud.item_exists(five_yr1_jan1_offset_road)

    # WHEN
    sue_bud = add_time_five_itemunit(sue_bud)

    # THEN
    assert sue_bud.item_exists(five_year_road)
    assert sue_bud.item_exists(creg_year_road)
    assert sue_bud.item_exists(creg_yr1_jan1_offset_road)
    assert sue_bud.item_exists(five_yr1_jan1_offset_road)
    five_offset_item = sue_bud.get_item_obj(five_yr1_jan1_offset_road)
    assert five_offset_item.addin == get_five_config().get(yr1_jan1_offset_str())


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
    sue_bud = add_time_creg_itemunit(sue_bud)
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
