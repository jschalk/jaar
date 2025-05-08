from src.a06_bud_logic.bud import BudUnit, budunit_shop
from src.a07_calendar_logic.chrono import ChronoUnit, chronounit_shop
from src.a07_calendar_logic._utils.calendar_examples import (
    five_str,
    add_time_creg_itemunit,
    add_time_five_itemunit,
    creg_str,
    get_creg_min_from_dt,
    get_five_min_from_dt,
    display_current_creg_five_time_attrs,
    display_creg_five_squirt_time_attrs,
)
from datetime import datetime


def test_ChronoUnit_Exists():
    # ESTABLISH / WHEN
    x_chronounit = ChronoUnit()

    # THEN
    assert not x_chronounit.x_budunit
    assert not x_chronounit.time_range_root_road
    assert not x_chronounit.x_min
    assert not x_chronounit._timeline_item
    assert not x_chronounit._weekday
    assert not x_chronounit._monthday
    assert not x_chronounit._month
    assert not x_chronounit._hour
    assert not x_chronounit._minute
    assert not x_chronounit._c400_number
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


def test_ChronoUnit_set_timeline_item_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 10000000)
    assert not x_chronounit._timeline_item

    # WHEN
    x_chronounit._set_timeline_item()

    # THEN
    assert x_chronounit._timeline_item


def test_ChronoUnit_set_weekday_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 10001440)
    x_chronounit._set_timeline_item()
    assert not x_chronounit._weekday

    # WHEN
    x_chronounit._set_weekday()

    # THEN
    assert x_chronounit._weekday == "Thursday"


def test_ChronoUnit_set_month_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 10060000)
    x_chronounit._set_timeline_item()
    assert not x_chronounit._month
    assert not x_chronounit._monthday

    # WHEN
    x_chronounit._set_month()

    # THEN
    assert x_chronounit._month == "April"
    # assert x_chronounit._monthday == 16
    assert x_chronounit._monthday == 17


def test_ChronoUnit_set_hour_SetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 10000001)
    x_chronounit._set_timeline_item()
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
    sue_bud = add_time_creg_itemunit(sue_bud)
    sue_bud.settle_bud()
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 1030600100)
    x_chronounit._set_timeline_item()
    assert not x_chronounit._c400_number
    assert not x_chronounit._c100_count
    assert not x_chronounit._yr4_count
    assert not x_chronounit._year_count
    assert not x_chronounit._year_num

    # WHEN
    x_chronounit._set_year()

    # THEN
    print(f"{x_chronounit._year_num=}")
    assert x_chronounit._c400_number == 4
    assert x_chronounit._c100_count == 3
    assert x_chronounit._yr4_count == 14
    assert x_chronounit._year_count == 3
    assert x_chronounit._year_num == 1959


def test_ChronoUnit_calc_timeline_SetsAttrs():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 1030600102)
    assert not x_chronounit._timeline_item
    assert not x_chronounit._weekday
    assert not x_chronounit._monthday
    assert not x_chronounit._month
    assert not x_chronounit._hour
    assert not x_chronounit._minute
    assert not x_chronounit._year_num

    # WHEN
    x_chronounit.calc_timeline()

    # THEN
    assert x_chronounit._timeline_item
    assert x_chronounit._weekday
    assert x_chronounit._monthday
    assert x_chronounit._month
    assert x_chronounit._hour
    assert x_chronounit._minute
    assert x_chronounit._year_num


def test_ChronoUnit_get_blurb_ReturnsObj():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    x_chronounit = chronounit_shop(sue_bud, creg_road, 1030600102)
    x_chronounit.calc_timeline()
    assert x_chronounit._timeline_item
    assert x_chronounit._weekday
    assert x_chronounit._monthday
    assert x_chronounit._month
    assert x_chronounit._hour
    assert x_chronounit._minute
    assert x_chronounit._year_num

    # WHEN
    timeline_blurb = x_chronounit.get_blurb()

    # THEN
    x_str = f"{x_chronounit._hour}"
    x_str += f":{x_chronounit._minute}"
    x_str += f", {x_chronounit._weekday}"
    x_str += f", {x_chronounit._monthday}"
    x_str += f" {x_chronounit._month}"
    x_str += f", {x_chronounit._year_num}"
    assert timeline_blurb == x_str


def test_calc_timeline_SetsAttrFiveTimeLine(graphics_bool):
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    sue_bud = add_time_five_itemunit(sue_bud)
    time_road = sue_bud.make_l1_road("time")
    creg_road = sue_bud.make_road(time_road, creg_str())
    five_road = sue_bud.make_road(time_road, five_str())
    mar1_2000_datetime = datetime(2000, 3, 1)
    creg_min = get_creg_min_from_dt(mar1_2000_datetime)
    five_min = get_five_min_from_dt(mar1_2000_datetime)
    creg_chronounit = chronounit_shop(sue_bud, creg_road, creg_min)
    five_chronounit = chronounit_shop(sue_bud, five_road, five_min)
    assert not creg_chronounit._weekday
    assert not creg_chronounit._monthday
    assert not creg_chronounit._month
    assert not creg_chronounit._hour
    assert not creg_chronounit._minute
    assert not creg_chronounit._year_num
    assert not five_chronounit._weekday
    assert not five_chronounit._monthday
    assert not five_chronounit._month
    assert not five_chronounit._hour
    assert not five_chronounit._minute
    assert not five_chronounit._year_num

    # WHEN
    creg_chronounit.calc_timeline()
    five_chronounit.calc_timeline()

    # THEN
    assert creg_chronounit._weekday == "Wednesday"
    assert creg_chronounit._month == "March"
    assert creg_chronounit._monthday == 1
    assert creg_chronounit._hour == "0-12am"
    assert creg_chronounit._minute == 0
    assert creg_chronounit._year_num == 2000
    assert five_chronounit._weekday == "Baileyday"
    assert five_chronounit._monthday == 0
    assert five_chronounit._month == "Fredrick"
    assert five_chronounit._hour == "0hr"
    assert five_chronounit._minute == 0
    assert five_chronounit._year_num == 5200

    display_current_creg_five_time_attrs(graphics_bool)
    display_creg_five_squirt_time_attrs(graphics_bool)


def check_creg_timeline_attr(x_bud: BudUnit, x_datetime: datetime):
    time_road = x_bud.make_l1_road("time")
    creg_road = x_bud.make_road(time_road, creg_str())
    creg_min = get_creg_min_from_dt(x_datetime)
    creg_chronounit = chronounit_shop(x_bud, creg_road, creg_min)
    creg_chronounit.calc_timeline()
    dt_hour = x_datetime.strftime("%H")
    dt_minute = x_datetime.strftime("%M")
    dt_weekday = x_datetime.strftime("%A")
    dt_month = x_datetime.strftime("%B")
    dt_monthday = x_datetime.strftime("%d")
    dt_year = x_datetime.strftime("%Y")
    hour_str = ""
    hour_int = int(dt_hour)
    if hour_int == 0:
        hour_str = f"{hour_int}-12am"
    elif hour_int < 12:
        hour_str = f"{hour_int}-{hour_int}am"
    elif hour_int == 12:
        hour_str = f"{hour_int}-12pm"
    else:
        hour_str = f"{hour_int}-{hour_int%12}pm"
    print(x_datetime.strftime("%H:%M, %A, %d %B, %Y"))
    if creg_chronounit._month in {"January", "February"}:
        dt_year = int(dt_year) - 1
    assert creg_chronounit._weekday == dt_weekday
    assert creg_chronounit._month == dt_month
    # assert creg_chronounit._monthday == int(dt_monthday) - 1
    assert creg_chronounit._monthday == int(dt_monthday)
    assert creg_chronounit._hour == hour_str
    assert creg_chronounit._minute == int(dt_minute)
    assert creg_chronounit._year_num == int(dt_year)


def test_check_creg_timeline():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    sue_bud = add_time_creg_itemunit(sue_bud)
    check_creg_timeline_attr(sue_bud, datetime(2000, 3, 1, 0, 21))
    check_creg_timeline_attr(sue_bud, datetime(2000, 3, 1, 3, 21))
    check_creg_timeline_attr(sue_bud, datetime(2000, 3, 1, 12, 00))
    check_creg_timeline_attr(sue_bud, datetime(2000, 3, 1, 13, 00))
    check_creg_timeline_attr(sue_bud, datetime(2000, 4, 1, 13, 00))
    check_creg_timeline_attr(sue_bud, datetime(2000, 4, 20, 13, 00))
    check_creg_timeline_attr(sue_bud, datetime(2000, 4, 28, 13, 00))
    check_creg_timeline_attr(sue_bud, datetime(2000, 4, 29, 13, 00))
    check_creg_timeline_attr(sue_bud, datetime(2000, 4, 30, 13, 00))
    check_creg_timeline_attr(sue_bud, datetime(2000, 5, 1, 13, 00))
    check_creg_timeline_attr(sue_bud, datetime(2000, 7, 1, 13, 56))
    check_creg_timeline_attr(sue_bud, datetime(2003, 12, 28, 17, 56))
    check_creg_timeline_attr(sue_bud, datetime(2003, 2, 28, 17, 56))
    check_creg_timeline_attr(sue_bud, datetime(432, 3, 4, 2, 0))
