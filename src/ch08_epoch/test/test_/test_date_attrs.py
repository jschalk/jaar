from datetime import datetime
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch08_epoch.epoch_main import (
    BeliefEpochInstant,
    EpochInstant,
    beliefEpochInstant_shop,
)
from src.ch08_epoch.test._util.ch08_examples import (
    add_time_creg_planunit,
    add_time_five_planunit,
    display_creg_five_squirt_time_attrs,
    display_current_creg_five_time_attrs,
    get_creg_min_from_dt,
    get_five_min_from_dt,
)
from src.ref.keywords import Ch08Keywords as kw


def test_EpochInstant_Exists():
    # ESTABLISH / WHEN / THEN
    assert EpochInstant(8) == 8


def test_BeliefEpochInstant_Exists():
    # ESTABLISH / WHEN
    x_EpochInstant = BeliefEpochInstant()

    # THEN
    assert not x_EpochInstant.x_beliefunit
    assert not x_EpochInstant.epoch_label
    assert not x_EpochInstant.x_min
    assert not x_EpochInstant._epoch_plan
    assert not x_EpochInstant._weekday
    assert not x_EpochInstant._monthday
    assert not x_EpochInstant._month
    assert not x_EpochInstant._hour
    assert not x_EpochInstant._minute
    assert not x_EpochInstant._c400_number
    assert not x_EpochInstant._c100_count
    assert not x_EpochInstant._yr4_count
    assert not x_EpochInstant._year_count
    assert not x_EpochInstant._year_num


def test_BeliefEpochInstant_shop_ReturnsObj():
    # ESTABLISH
    x_epoch_label = "Fay07"
    x_epoch_min = 890000
    sue_belief = beliefunit_shop("Sue")

    # WHEN
    x_EpochInstant = beliefEpochInstant_shop(
        x_beliefunit=sue_belief,
        epoch_label=x_epoch_label,
        x_min=x_epoch_min,
    )

    # THEN
    assert x_EpochInstant.x_beliefunit == sue_belief
    assert x_EpochInstant.epoch_label == x_epoch_label
    assert x_EpochInstant.x_min == x_epoch_min


def test_BeliefEpochInstant_set_epoch_plan_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    x_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.creg, 10000000)
    assert not x_EpochInstant._epoch_plan

    # WHEN
    x_EpochInstant._set_epoch_plan()

    # THEN
    assert x_EpochInstant._epoch_plan


def test_BeliefEpochInstant_set_weekday_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    x_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.creg, 10001440)
    x_EpochInstant._set_epoch_plan()
    assert not x_EpochInstant._weekday

    # WHEN
    x_EpochInstant._set_weekday()

    # THEN
    assert x_EpochInstant._weekday == kw.Thursday


def test_BeliefEpochInstant_set_month_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    x_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.creg, 10060000)
    x_EpochInstant._set_epoch_plan()
    assert not x_EpochInstant._month
    assert not x_EpochInstant._monthday

    # WHEN
    x_EpochInstant._set_month()

    # THEN
    assert x_EpochInstant._month == "April"
    # assert x_EpochInstant._monthday == 16
    assert x_EpochInstant._monthday == 17


def test_BeliefEpochInstant_set_hour_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    x_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.creg, 10000001)
    x_EpochInstant._set_epoch_plan()
    assert not x_EpochInstant._hour
    assert not x_EpochInstant._hour
    assert not x_EpochInstant._minute

    # WHEN
    x_EpochInstant._set_hour()

    # THEN
    assert x_EpochInstant._hour == "10am"
    assert x_EpochInstant._minute == 41


def test_BeliefEpochInstant_set_year_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief.cashout()
    x_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.creg, 1030600100)
    x_EpochInstant._set_epoch_plan()
    assert not x_EpochInstant._c400_number
    assert not x_EpochInstant._c100_count
    assert not x_EpochInstant._yr4_count
    assert not x_EpochInstant._year_count
    assert not x_EpochInstant._year_num

    # WHEN
    x_EpochInstant._set_year()

    # THEN
    print(f"{x_EpochInstant._year_num=}")
    assert x_EpochInstant._c400_number == 4
    assert x_EpochInstant._c100_count == 3
    assert x_EpochInstant._yr4_count == 14
    assert x_EpochInstant._year_count == 3
    assert x_EpochInstant._year_num == 1959


def test_BeliefEpochInstant_calc_epoch_SetsAttrs():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    x_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.creg, 1030600102)
    assert not x_EpochInstant._epoch_plan
    assert not x_EpochInstant._weekday
    assert not x_EpochInstant._monthday
    assert not x_EpochInstant._month
    assert not x_EpochInstant._hour
    assert not x_EpochInstant._minute
    assert not x_EpochInstant._year_num

    # WHEN
    x_EpochInstant.calc_epoch()

    # THEN
    assert x_EpochInstant._epoch_plan
    assert x_EpochInstant._weekday
    assert x_EpochInstant._monthday
    assert x_EpochInstant._month
    assert x_EpochInstant._hour
    assert x_EpochInstant._minute
    assert x_EpochInstant._year_num


def test_BeliefEpochInstant_get_blurb_ReturnsObj():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    x_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.creg, 1030600102)
    x_EpochInstant.calc_epoch()
    assert x_EpochInstant._epoch_plan
    assert x_EpochInstant._weekday
    assert x_EpochInstant._monthday
    assert x_EpochInstant._month
    assert x_EpochInstant._hour
    assert x_EpochInstant._minute
    assert x_EpochInstant._year_num

    # WHEN
    epoch_blurb = x_EpochInstant.get_blurb()

    # THEN
    x_str = f"{x_EpochInstant._hour}"
    x_str += f":{x_EpochInstant._minute}"
    x_str += f", {x_EpochInstant._weekday}"
    x_str += f", {x_EpochInstant._monthday}"
    x_str += f" {x_EpochInstant._month}"
    x_str += f", {x_EpochInstant._year_num}"
    assert epoch_blurb == x_str


def test_calc_epoch_SetsAttrFiveEpoch(graphics_bool):
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_time_creg_planunit(sue_belief)
    sue_belief = add_time_five_planunit(sue_belief)
    mar1_2000_datetime = datetime(2000, 3, 1)
    creg_min = get_creg_min_from_dt(mar1_2000_datetime)
    five_min = get_five_min_from_dt(mar1_2000_datetime)
    creg_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.creg, creg_min)
    five_EpochInstant = beliefEpochInstant_shop(sue_belief, kw.five, five_min)
    assert not creg_EpochInstant._weekday
    assert not creg_EpochInstant._monthday
    assert not creg_EpochInstant._month
    assert not creg_EpochInstant._hour
    assert not creg_EpochInstant._minute
    assert not creg_EpochInstant._year_num
    assert not five_EpochInstant._weekday
    assert not five_EpochInstant._monthday
    assert not five_EpochInstant._month
    assert not five_EpochInstant._hour
    assert not five_EpochInstant._minute
    assert not five_EpochInstant._year_num

    # WHEN
    creg_EpochInstant.calc_epoch()
    five_EpochInstant.calc_epoch()

    # THEN
    assert creg_EpochInstant._weekday == kw.Wednesday
    assert creg_EpochInstant._month == "March"
    assert creg_EpochInstant._monthday == 1
    assert creg_EpochInstant._hour == "12am"
    assert creg_EpochInstant._minute == 0
    assert creg_EpochInstant._year_num == 2000
    assert five_EpochInstant._weekday == kw.Baileyday
    assert five_EpochInstant._monthday == 0
    assert five_EpochInstant._month == "Fredrick"
    assert five_EpochInstant._hour == "0hr"
    assert five_EpochInstant._minute == 0
    assert five_EpochInstant._year_num == 5200

    display_current_creg_five_time_attrs(graphics_bool)
    display_creg_five_squirt_time_attrs(graphics_bool)


def check_creg_epoch_attr(x_belief: BeliefUnit, x_datetime: datetime):
    creg_min = get_creg_min_from_dt(x_datetime)
    creg_EpochInstant = beliefEpochInstant_shop(x_belief, kw.creg, creg_min)
    creg_EpochInstant.calc_epoch()
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
    if creg_EpochInstant._month in {"January", "February"}:
        dt_year = int(dt_year) - 1
    assert creg_EpochInstant._weekday == dt_weekday
    assert creg_EpochInstant._month == dt_month
    # assert creg_EpochInstant._monthday == int(dt_monthday) - 1
    assert creg_EpochInstant._monthday == int(dt_monthday)
    assert creg_EpochInstant._hour == hour_str
    assert creg_EpochInstant._minute == int(dt_minute)
    assert creg_EpochInstant._year_num == int(dt_year)


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
