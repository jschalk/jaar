from datetime import datetime
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch08_epoch_logic.epoch_main import (
    BeliefEpochPoint,
    EpochPoint,
    beliefepochpoint_shop,
)
from src.ch08_epoch_logic.test._util.ch08_examples import (
    add_time_creg_planunit,
    add_time_five_planunit,
    display_creg_five_squirt_time_attrs,
    display_current_creg_five_time_attrs,
    get_creg_min_from_dt,
    get_five_min_from_dt,
)
from src.ref.ch08_keywords import Ch08Keywords as wx


def test_EpochPoint_Exists():
    # ESTABLISH / WHEN / THEN
    assert EpochPoint(8) == 8


def test_BeliefEpochPoint_Exists():
    # ESTABLISH / WHEN
    x_epochpoint = BeliefEpochPoint()

    # THEN
    assert not x_epochpoint.x_beliefunit
    assert not x_epochpoint.time_range_root_rope
    assert not x_epochpoint.x_min
    assert not x_epochpoint._epoch_plan
    assert not x_epochpoint._weekday
    assert not x_epochpoint._monthday
    assert not x_epochpoint._month
    assert not x_epochpoint._hour
    assert not x_epochpoint._minute
    assert not x_epochpoint._c400_number
    assert not x_epochpoint._c100_count
    assert not x_epochpoint._yr4_count
    assert not x_epochpoint._year_count
    assert not x_epochpoint._year_num


def test_BeliefEpochPoint_shop_ReturnsObj():
    # ESTABLISH
    x_time_range_root_rope = "Fay07"
    x_epoch_min = 890000
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    x_epochpoint = beliefepochpoint_shop(
        x_beliefunit=sue_belief,
        time_range_root_rope=x_time_range_root_rope,
        x_min=x_epoch_min,
    )

    # THEN
    assert x_epochpoint.x_beliefunit == sue_belief
    assert x_epochpoint.time_range_root_rope == x_time_range_root_rope
    assert x_epochpoint.x_min == x_epoch_min


def test_BeliefEpochPoint_set_epoch_plan_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    time_rope = sue_belief.make_l1_rope("time")
    creg_rope = sue_belief.make_rope(time_rope, wx.creg)
    x_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, 10000000)
    assert not x_epochpoint._epoch_plan

    # WHEN
    x_epochpoint._set_epoch_plan()

    # THEN
    assert x_epochpoint._epoch_plan


def test_BeliefEpochPoint_set_weekday_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    time_rope = sue_belief.make_l1_rope("time")
    creg_rope = sue_belief.make_rope(time_rope, wx.creg)
    x_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, 10001440)
    x_epochpoint._set_epoch_plan()
    assert not x_epochpoint._weekday

    # WHEN
    x_epochpoint._set_weekday()

    # THEN
    assert x_epochpoint._weekday == "Thursday"


def test_BeliefEpochPoint_set_month_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    time_rope = sue_belief.make_l1_rope("time")
    creg_rope = sue_belief.make_rope(time_rope, wx.creg)
    x_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, 10060000)
    x_epochpoint._set_epoch_plan()
    assert not x_epochpoint._month
    assert not x_epochpoint._monthday

    # WHEN
    x_epochpoint._set_month()

    # THEN
    assert x_epochpoint._month == "April"
    # assert x_epochpoint._monthday == 16
    assert x_epochpoint._monthday == 17


def test_BeliefEpochPoint_set_hour_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    time_rope = sue_belief.make_l1_rope("time")
    creg_rope = sue_belief.make_rope(time_rope, wx.creg)
    x_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, 10000001)
    x_epochpoint._set_epoch_plan()
    assert not x_epochpoint._hour
    assert not x_epochpoint._hour
    assert not x_epochpoint._minute

    # WHEN
    x_epochpoint._set_hour()

    # THEN
    assert x_epochpoint._hour == "10am"
    assert x_epochpoint._minute == 41


def test_BeliefEpochPoint_set_year_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    time_rope = sue_belief.make_l1_rope("time")
    creg_rope = sue_belief.make_rope(time_rope, wx.creg)
    x_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, 1030600100)
    x_epochpoint._set_epoch_plan()
    assert not x_epochpoint._c400_number
    assert not x_epochpoint._c100_count
    assert not x_epochpoint._yr4_count
    assert not x_epochpoint._year_count
    assert not x_epochpoint._year_num

    # WHEN
    x_epochpoint._set_year()

    # THEN
    print(f"{x_epochpoint._year_num=}")
    assert x_epochpoint._c400_number == 4
    assert x_epochpoint._c100_count == 3
    assert x_epochpoint._yr4_count == 14
    assert x_epochpoint._year_count == 3
    assert x_epochpoint._year_num == 1959


def test_BeliefEpochPoint_calc_epoch_SetsAttrs():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    time_rope = sue_belief.make_l1_rope("time")
    creg_rope = sue_belief.make_rope(time_rope, wx.creg)
    x_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, 1030600102)
    assert not x_epochpoint._epoch_plan
    assert not x_epochpoint._weekday
    assert not x_epochpoint._monthday
    assert not x_epochpoint._month
    assert not x_epochpoint._hour
    assert not x_epochpoint._minute
    assert not x_epochpoint._year_num

    # WHEN
    x_epochpoint.calc_epoch()

    # THEN
    assert x_epochpoint._epoch_plan
    assert x_epochpoint._weekday
    assert x_epochpoint._monthday
    assert x_epochpoint._month
    assert x_epochpoint._hour
    assert x_epochpoint._minute
    assert x_epochpoint._year_num


def test_BeliefEpochPoint_get_blurb_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    time_rope = sue_belief.make_l1_rope("time")
    creg_rope = sue_belief.make_rope(time_rope, wx.creg)
    x_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, 1030600102)
    x_epochpoint.calc_epoch()
    assert x_epochpoint._epoch_plan
    assert x_epochpoint._weekday
    assert x_epochpoint._monthday
    assert x_epochpoint._month
    assert x_epochpoint._hour
    assert x_epochpoint._minute
    assert x_epochpoint._year_num

    # WHEN
    epoch_blurb = x_epochpoint.get_blurb()

    # THEN
    x_str = f"{x_epochpoint._hour}"
    x_str += f":{x_epochpoint._minute}"
    x_str += f", {x_epochpoint._weekday}"
    x_str += f", {x_epochpoint._monthday}"
    x_str += f" {x_epochpoint._month}"
    x_str += f", {x_epochpoint._year_num}"
    assert epoch_blurb == x_str


def test_calc_epoch_SetsAttrFiveEpoch(graphics_bool):
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief = add_time_five_planunit(sue_belief)
    time_rope = sue_belief.make_l1_rope("time")
    creg_rope = sue_belief.make_rope(time_rope, wx.creg)
    five_rope = sue_belief.make_rope(time_rope, wx.five)
    mar1_2000_datetime = datetime(2000, 3, 1)
    creg_min = get_creg_min_from_dt(mar1_2000_datetime)
    five_min = get_five_min_from_dt(mar1_2000_datetime)
    creg_epochpoint = beliefepochpoint_shop(sue_belief, creg_rope, creg_min)
    five_epochpoint = beliefepochpoint_shop(sue_belief, five_rope, five_min)
    assert not creg_epochpoint._weekday
    assert not creg_epochpoint._monthday
    assert not creg_epochpoint._month
    assert not creg_epochpoint._hour
    assert not creg_epochpoint._minute
    assert not creg_epochpoint._year_num
    assert not five_epochpoint._weekday
    assert not five_epochpoint._monthday
    assert not five_epochpoint._month
    assert not five_epochpoint._hour
    assert not five_epochpoint._minute
    assert not five_epochpoint._year_num

    # WHEN
    creg_epochpoint.calc_epoch()
    five_epochpoint.calc_epoch()

    # THEN
    assert creg_epochpoint._weekday == "Wednesday"
    assert creg_epochpoint._month == "March"
    assert creg_epochpoint._monthday == 1
    assert creg_epochpoint._hour == "12am"
    assert creg_epochpoint._minute == 0
    assert creg_epochpoint._year_num == 2000
    assert five_epochpoint._weekday == "Baileyday"
    assert five_epochpoint._monthday == 0
    assert five_epochpoint._month == "Fredrick"
    assert five_epochpoint._hour == "0hr"
    assert five_epochpoint._minute == 0
    assert five_epochpoint._year_num == 5200

    display_current_creg_five_time_attrs(graphics_bool)
    display_creg_five_squirt_time_attrs(graphics_bool)


def check_creg_epoch_attr(x_belief: BeliefUnit, x_datetime: datetime):
    time_rope = x_belief.make_l1_rope("time")
    creg_rope = x_belief.make_rope(time_rope, wx.creg)
    creg_min = get_creg_min_from_dt(x_datetime)
    creg_epochpoint = beliefepochpoint_shop(x_belief, creg_rope, creg_min)
    creg_epochpoint.calc_epoch()
    dt_hour = x_datetime.strftime("%H")
    dt_minute = x_datetime.strftime("%M")
    dt_weekday = x_datetime.strftime("%A")
    dt_month = x_datetime.strftime("%B")
    dt_monthday = x_datetime.strftime("%d")
    dt_year = x_datetime.strftime("%Y")
    hour_str = ""
    hour_int = int(dt_hour)
    if hour_int == 0:
        hour_str = "12am"
    elif hour_int < 12:
        hour_str = f"{hour_int}am"
    elif hour_int == 12:
        hour_str = "12pm"
    else:
        hour_str = f"{hour_int%12}pm"
    print(x_datetime.strftime("%H:%M, %A, %d %B, %Y"))
    if creg_epochpoint._month in {"January", "February"}:
        dt_year = int(dt_year) - 1
    assert creg_epochpoint._weekday == dt_weekday
    assert creg_epochpoint._month == dt_month
    # assert creg_epochpoint._monthday == int(dt_monthday) - 1
    assert creg_epochpoint._monthday == int(dt_monthday)
    assert creg_epochpoint._hour == hour_str
    assert creg_epochpoint._minute == int(dt_minute)
    assert creg_epochpoint._year_num == int(dt_year)


def test_check_creg_epoch():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    sue_belief = add_time_creg_planunit(sue_belief)

    # THEN
    check_creg_epoch_attr(sue_belief, datetime(2000, 3, 1, 0, 21))
    check_creg_epoch_attr(sue_belief, datetime(2000, 3, 1, 3, 21))
    check_creg_epoch_attr(sue_belief, datetime(2000, 3, 1, 12, 00))
    check_creg_epoch_attr(sue_belief, datetime(2000, 3, 1, 13, 00))
    check_creg_epoch_attr(sue_belief, datetime(2000, 4, 1, 13, 00))
    check_creg_epoch_attr(sue_belief, datetime(2000, 4, 20, 13, 00))
    check_creg_epoch_attr(sue_belief, datetime(2000, 4, 28, 13, 00))
    check_creg_epoch_attr(sue_belief, datetime(2000, 4, 29, 13, 00))
    check_creg_epoch_attr(sue_belief, datetime(2000, 4, 30, 13, 00))
    check_creg_epoch_attr(sue_belief, datetime(2000, 5, 1, 13, 00))
    check_creg_epoch_attr(sue_belief, datetime(2000, 7, 1, 13, 56))
    check_creg_epoch_attr(sue_belief, datetime(2003, 12, 28, 17, 56))
    check_creg_epoch_attr(sue_belief, datetime(2003, 2, 28, 17, 56))
    check_creg_epoch_attr(sue_belief, datetime(432, 3, 4, 2, 0))
