from src.bud.bud import budunit_shop
from src.chrono.chrono import (
    C400Constants,
    get_c400_constants,
    day_length,
    hours_config_text,
    weekdays_config_text,
    months_config_text,
    timeline_label_text,
    c400_config_text,
    yr1_jan1_offset_text,
    validate_timeline_config,
    create_timeline_config,
    ChronoUnit,
    chronounit_shop,
    week_str,
    year_str,
    day_str,
    get_year_road,
    get_week_road,
    get_day_road,
    time_str,
    c400_leap_str,
    c400_clean_str,
    c100_str,
    yr4_leap_str,
    yr4_clean_str,
)
from src.chrono.examples.chrono_examples import (
    get_creg_config,
    get_squirt_config,
    chrono_examples_dir,
    get_example_timeline_config,
    five_str,
    add_time_creg_ideaunit,
    creg_str,
    get_creg_min_from_dt,
)


def test_ChronoUnit_Exists():
    # ESTABLISH / WHEN
    x_chronounit = ChronoUnit()

    # THEN
    assert not x_chronounit.x_budunit
    assert not x_chronounit.time_range_root_road
    assert not x_chronounit.x_min
    assert not x_chronounit._timeline_idea
    assert not x_chronounit._weekday
    assert not x_chronounit._monthday
    assert not x_chronounit._month
    assert not x_chronounit._hour
    assert not x_chronounit._minute
    assert not x_chronounit._c400_count
    assert not x_chronounit._c100_count
    assert not x_chronounit._yr4_count
    assert not x_chronounit._year_count
    assert not x_chronounit._year_num


def test_ChronoUnit_shop_ReturnsObj():
    # ESTABLISH
    x_time_range_root_road = "fizz07"
    x_timeline_min = 890000
    sue_bud = budunit_shop("Sue")

    # WHEN
    x_chronounit = chronounit_shop(
        x_budunit=sue_bud,
        time_range_root_road=x_time_range_root_road,
        x_min=x_timeline_min,
    )

    # THEN
    assert x_chronounit.x_budunit == sue_bud
    assert x_chronounit.time_range_root_road == x_time_range_root_road
    assert x_chronounit.x_min == x_timeline_min


def test_ChronoUnit_set_timeline_idea_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 10000000)
    assert not x_chronounit._timeline_idea

    # WHEN
    x_chronounit._set_timeline_idea()

    # THEN
    assert x_chronounit._timeline_idea


def test_ChronoUnit_set_weekday_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 10001440)
    x_chronounit._set_timeline_idea()
    assert not x_chronounit._weekday

    # WHEN
    x_chronounit._set_weekday()

    # THEN
    assert x_chronounit._weekday == "Thursday"


def test_ChronoUnit_set_month_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 10060000)
    x_chronounit._set_timeline_idea()
    assert not x_chronounit._month
    assert not x_chronounit._monthday

    # WHEN
    x_chronounit._set_month()

    # THEN
    assert x_chronounit._month == "apr"
    assert x_chronounit._monthday == 16


def test_ChronoUnit_set_hour_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 10000001)
    x_chronounit._set_timeline_idea()
    assert not x_chronounit._hour
    assert not x_chronounit._hour
    assert not x_chronounit._minute

    # WHEN
    x_chronounit._set_hour()

    # THEN
    assert x_chronounit._hour == "10-10am"
    assert x_chronounit._minute == 41


def test_ChronoUnit_set_year_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 1030600100)
    x_chronounit._set_timeline_idea()
    assert not x_chronounit._c400_count
    assert not x_chronounit._c100_count
    assert not x_chronounit._yr4_count
    assert not x_chronounit._year_count
    assert not x_chronounit._year_num

    # WHEN
    x_chronounit._set_year()

    # THEN
    print(f"{x_chronounit._year_num=}")
    assert x_chronounit._c400_count == 4
    assert x_chronounit._c100_count == 3
    assert x_chronounit._yr4_count == 14
    assert x_chronounit._year_count == 3
    assert x_chronounit._year_num == 1959


def test_ChronoUnit_calc_timeline_SetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 1030600102)
    assert not x_chronounit._timeline_idea
    assert not x_chronounit._weekday
    assert not x_chronounit._monthday
    assert not x_chronounit._month
    assert not x_chronounit._hour
    assert not x_chronounit._minute
    assert not x_chronounit._year_num

    # WHEN
    x_chronounit.calc_timeline()

    # THEN
    assert x_chronounit._timeline_idea
    assert x_chronounit._weekday
    assert x_chronounit._monthday
    assert x_chronounit._month
    assert x_chronounit._hour
    assert x_chronounit._minute
    assert x_chronounit._year_num
