from src.bud.bud import budunit_shop
from src.chrono.examples.chrono_examples import (
    get_creg_config,
    get_squirt_config,
    chrono_examples_dir,
    get_example_timeline_config,
    cinco_str,
)
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
from copy import deepcopy as copy_deepcopy


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
    assert not x_chronorange.timeline_label
    assert not x_chronorange.copen
    assert not x_chronorange.cnigh


def test_ChronoRange_shop_ReturnsObj():
    # ESTABLISH
    x_timeline_label = "fizz07"
    x_timeline_min_copen = 890000
    x_timeline_min_cnigh = 5000000

    # WHEN
    x_chronorange = chronorange_shop(
        timeline_label=x_timeline_label,
        copen=x_timeline_min_copen,
        cnigh=x_timeline_min_cnigh,
    )

    # THEN
    assert x_chronorange.timeline_label == x_timeline_label
    assert x_chronorange.copen == x_timeline_min_copen
    assert x_chronorange.cnigh == x_timeline_min_cnigh
