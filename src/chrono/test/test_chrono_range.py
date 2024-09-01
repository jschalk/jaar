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
    ChronoPoint,
    chronopoint_shop,
    ChronoRange,
    chronorange_shop,
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


def test_ChronoPoint_Exists():
    # ESTABLISH / WHEN
    x_chronopoint = ChronoPoint()

    # THEN
    assert not x_chronopoint.timeline_min
    assert not x_chronopoint.weekday_label
    assert not x_chronopoint.month_label
    assert not x_chronopoint.monthday_num
    assert not x_chronopoint.c400_leap_count
    assert not x_chronopoint.c100_count
    assert not x_chronopoint.yr4_leap_count
    assert not x_chronopoint.yr_count
    assert not x_chronopoint.year_num
    assert not x_chronopoint.hour_label
    assert not x_chronopoint.minute_num


def test_chronopoint_shop_ReturnsObj():
    # ESTABLISH
    x_timeline_min = 890000

    # WHEN
    x_chronopoint = chronopoint_shop(x_timeline_min)

    # THEN
    assert x_chronopoint.timeline_min == x_timeline_min


def test_ChronoRange_Exists():
    # ESTABLISH / WHEN
    x_chronorange = ChronoRange()

    # THEN
    assert not x_chronorange.x_budunit
    assert not x_chronorange.time_range_root_road
    assert not x_chronorange.copen
    assert not x_chronorange.cnigh
    assert not x_chronorange._timeline_idea
    assert not x_chronorange._copen_weekday
    assert not x_chronorange._cnigh_weekday
    assert not x_chronorange._copen_monthday
    assert not x_chronorange._cnigh_monthday
    assert not x_chronorange._copen_month
    assert not x_chronorange._cnigh_month
    assert not x_chronorange._copen_hour
    assert not x_chronorange._cnigh_hour
    assert not x_chronorange._copen_minute
    assert not x_chronorange._cnigh_minute


def test_ChronoRange_shop_ReturnsObj():
    # ESTABLISH
    x_time_range_root_road = "fizz07"
    x_timeline_min_copen = 890000
    x_timeline_min_cnigh = 5000000
    sue_bud = budunit_shop("Sue")

    # WHEN
    x_chronorange = chronorange_shop(
        x_budunit=sue_bud,
        time_range_root_road=x_time_range_root_road,
        copen=x_timeline_min_copen,
        cnigh=x_timeline_min_cnigh,
    )

    # THEN
    assert x_chronorange.x_budunit == sue_bud
    assert x_chronorange.time_range_root_road == x_time_range_root_road
    assert x_chronorange.copen == x_timeline_min_copen
    assert x_chronorange.cnigh == x_timeline_min_cnigh


def test_ChronoRange_set_timeline_idea_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronorange = chronorange_shop(sue_bud, creg_road, 10000000, 10001440)
    assert not x_chronorange._timeline_idea

    # WHEN
    x_chronorange._set_timeline_idea()

    # THEN
    assert x_chronorange._timeline_idea


def test_ChronoRange_set_weekday_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronorange = chronorange_shop(sue_bud, creg_road, 10001440, 10002880)
    x_chronorange._set_timeline_idea()
    assert not x_chronorange._copen_weekday
    assert not x_chronorange._cnigh_weekday

    # WHEN
    x_chronorange._set_weekday()

    # THEN
    assert x_chronorange._copen_weekday == "Thursday"
    assert x_chronorange._cnigh_weekday == "Friday"


def test_ChronoRange_set_month_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronorange = chronorange_shop(sue_bud, creg_road, 10060000, 10120000)
    x_chronorange._set_timeline_idea()
    assert not x_chronorange._copen_month
    assert not x_chronorange._cnigh_month
    assert not x_chronorange._copen_monthday
    assert not x_chronorange._cnigh_monthday

    # WHEN
    x_chronorange._set_month()

    # THEN
    assert x_chronorange._copen_month == "apr"
    assert x_chronorange._cnigh_month == "may"
    assert x_chronorange._copen_monthday == 16
    assert x_chronorange._cnigh_monthday == 29


def test_ChronoRange_set_hour_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_ideaunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronorange = chronorange_shop(sue_bud, creg_road, 10000001, 10000062)
    x_chronorange._set_timeline_idea()
    assert not x_chronorange._copen_hour
    assert not x_chronorange._copen_hour
    assert not x_chronorange._copen_minute
    assert not x_chronorange._cnigh_minute

    # WHEN
    x_chronorange._set_hour()

    # THEN
    assert x_chronorange._copen_hour == "10-10am"
    assert x_chronorange._cnigh_hour == "11-11am"
    assert x_chronorange._copen_minute == 41
    assert x_chronorange._cnigh_minute == 42
