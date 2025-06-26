from datetime import datetime
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_conceptunit,
    add_time_five_conceptunit,
    creg_str,
    display_creg_five_squirt_time_attrs,
    display_current_creg_five_time_attrs,
    five_str,
    get_creg_min_from_dt,
    get_five_min_from_dt,
)
from src.a07_timeline_logic.timeline import PlanTimelinePoint, plantimelinepoint_shop


def test_PlanTimelinePoint_Exists():
    # ESTABLISH / WHEN
    x_timelinepoint = PlanTimelinePoint()

    # THEN
    assert not x_timelinepoint.x_planunit
    assert not x_timelinepoint.time_range_root_rope
    assert not x_timelinepoint.x_min
    assert not x_timelinepoint._timeline_concept
    assert not x_timelinepoint._weekday
    assert not x_timelinepoint._monthday
    assert not x_timelinepoint._month
    assert not x_timelinepoint._hour
    assert not x_timelinepoint._minute
    assert not x_timelinepoint._c400_number
    assert not x_timelinepoint._c100_count
    assert not x_timelinepoint._yr4_count
    assert not x_timelinepoint._year_count
    assert not x_timelinepoint._year_num


def test_PlanTimelinePoint_shop_ReturnsObj():
    # ESTABLISH
    x_time_range_root_rope = "Fay07"
    x_timeline_min = 890000
    sue_plan = planunit_shop("Sue")

    # WHEN
    x_timelinepoint = plantimelinepoint_shop(
        x_planunit=sue_plan,
        time_range_root_rope=x_time_range_root_rope,
        x_min=x_timeline_min,
    )

    # THEN
    assert x_timelinepoint.x_planunit == sue_plan
    assert x_timelinepoint.time_range_root_rope == x_time_range_root_rope
    assert x_timelinepoint.x_min == x_timeline_min


def test_PlanTimelinePoint_set_timeline_concept_SetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    sue_plan.settle_plan()
    time_rope = sue_plan.make_l1_rope("time")
    creg_rope = sue_plan.make_rope(time_rope, creg_str())
    x_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, 10000000)
    assert not x_timelinepoint._timeline_concept

    # WHEN
    x_timelinepoint._set_timeline_concept()

    # THEN
    assert x_timelinepoint._timeline_concept


def test_PlanTimelinePoint_set_weekday_SetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    sue_plan.settle_plan()
    time_rope = sue_plan.make_l1_rope("time")
    creg_rope = sue_plan.make_rope(time_rope, creg_str())
    x_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, 10001440)
    x_timelinepoint._set_timeline_concept()
    assert not x_timelinepoint._weekday

    # WHEN
    x_timelinepoint._set_weekday()

    # THEN
    assert x_timelinepoint._weekday == "Thursday"


def test_PlanTimelinePoint_set_month_SetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    sue_plan.settle_plan()
    time_rope = sue_plan.make_l1_rope("time")
    creg_rope = sue_plan.make_rope(time_rope, creg_str())
    x_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, 10060000)
    x_timelinepoint._set_timeline_concept()
    assert not x_timelinepoint._month
    assert not x_timelinepoint._monthday

    # WHEN
    x_timelinepoint._set_month()

    # THEN
    assert x_timelinepoint._month == "April"
    # assert x_timelinepoint._monthday == 16
    assert x_timelinepoint._monthday == 17


def test_PlanTimelinePoint_set_hour_SetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    sue_plan.settle_plan()
    time_rope = sue_plan.make_l1_rope("time")
    creg_rope = sue_plan.make_rope(time_rope, creg_str())
    x_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, 10000001)
    x_timelinepoint._set_timeline_concept()
    assert not x_timelinepoint._hour
    assert not x_timelinepoint._hour
    assert not x_timelinepoint._minute

    # WHEN
    x_timelinepoint._set_hour()

    # THEN
    assert x_timelinepoint._hour == "10-10am"
    assert x_timelinepoint._minute == 41


def test_PlanTimelinePoint_set_year_SetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    sue_plan.settle_plan()
    time_rope = sue_plan.make_l1_rope("time")
    creg_rope = sue_plan.make_rope(time_rope, creg_str())
    x_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, 1030600100)
    x_timelinepoint._set_timeline_concept()
    assert not x_timelinepoint._c400_number
    assert not x_timelinepoint._c100_count
    assert not x_timelinepoint._yr4_count
    assert not x_timelinepoint._year_count
    assert not x_timelinepoint._year_num

    # WHEN
    x_timelinepoint._set_year()

    # THEN
    print(f"{x_timelinepoint._year_num=}")
    assert x_timelinepoint._c400_number == 4
    assert x_timelinepoint._c100_count == 3
    assert x_timelinepoint._yr4_count == 14
    assert x_timelinepoint._year_count == 3
    assert x_timelinepoint._year_num == 1959


def test_PlanTimelinePoint_calc_timeline_SetsAttrs():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    time_rope = sue_plan.make_l1_rope("time")
    creg_rope = sue_plan.make_rope(time_rope, creg_str())
    x_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, 1030600102)
    assert not x_timelinepoint._timeline_concept
    assert not x_timelinepoint._weekday
    assert not x_timelinepoint._monthday
    assert not x_timelinepoint._month
    assert not x_timelinepoint._hour
    assert not x_timelinepoint._minute
    assert not x_timelinepoint._year_num

    # WHEN
    x_timelinepoint.calc_timeline()

    # THEN
    assert x_timelinepoint._timeline_concept
    assert x_timelinepoint._weekday
    assert x_timelinepoint._monthday
    assert x_timelinepoint._month
    assert x_timelinepoint._hour
    assert x_timelinepoint._minute
    assert x_timelinepoint._year_num


def test_PlanTimelinePoint_get_blurb_ReturnsObj():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    time_rope = sue_plan.make_l1_rope("time")
    creg_rope = sue_plan.make_rope(time_rope, creg_str())
    x_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, 1030600102)
    x_timelinepoint.calc_timeline()
    assert x_timelinepoint._timeline_concept
    assert x_timelinepoint._weekday
    assert x_timelinepoint._monthday
    assert x_timelinepoint._month
    assert x_timelinepoint._hour
    assert x_timelinepoint._minute
    assert x_timelinepoint._year_num

    # WHEN
    timeline_blurb = x_timelinepoint.get_blurb()

    # THEN
    x_str = f"{x_timelinepoint._hour}"
    x_str += f":{x_timelinepoint._minute}"
    x_str += f", {x_timelinepoint._weekday}"
    x_str += f", {x_timelinepoint._monthday}"
    x_str += f" {x_timelinepoint._month}"
    x_str += f", {x_timelinepoint._year_num}"
    assert timeline_blurb == x_str


def test_calc_timeline_SetsAttrFiveTimeLine(graphics_bool):
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    sue_plan = add_time_five_conceptunit(sue_plan)
    time_rope = sue_plan.make_l1_rope("time")
    creg_rope = sue_plan.make_rope(time_rope, creg_str())
    five_rope = sue_plan.make_rope(time_rope, five_str())
    mar1_2000_datetime = datetime(2000, 3, 1)
    creg_min = get_creg_min_from_dt(mar1_2000_datetime)
    five_min = get_five_min_from_dt(mar1_2000_datetime)
    creg_timelinepoint = plantimelinepoint_shop(sue_plan, creg_rope, creg_min)
    five_timelinepoint = plantimelinepoint_shop(sue_plan, five_rope, five_min)
    assert not creg_timelinepoint._weekday
    assert not creg_timelinepoint._monthday
    assert not creg_timelinepoint._month
    assert not creg_timelinepoint._hour
    assert not creg_timelinepoint._minute
    assert not creg_timelinepoint._year_num
    assert not five_timelinepoint._weekday
    assert not five_timelinepoint._monthday
    assert not five_timelinepoint._month
    assert not five_timelinepoint._hour
    assert not five_timelinepoint._minute
    assert not five_timelinepoint._year_num

    # WHEN
    creg_timelinepoint.calc_timeline()
    five_timelinepoint.calc_timeline()

    # THEN
    assert creg_timelinepoint._weekday == "Wednesday"
    assert creg_timelinepoint._month == "March"
    assert creg_timelinepoint._monthday == 1
    assert creg_timelinepoint._hour == "0-12am"
    assert creg_timelinepoint._minute == 0
    assert creg_timelinepoint._year_num == 2000
    assert five_timelinepoint._weekday == "Baileyday"
    assert five_timelinepoint._monthday == 0
    assert five_timelinepoint._month == "Fredrick"
    assert five_timelinepoint._hour == "0hr"
    assert five_timelinepoint._minute == 0
    assert five_timelinepoint._year_num == 5200

    display_current_creg_five_time_attrs(graphics_bool)
    display_creg_five_squirt_time_attrs(graphics_bool)


def check_creg_timeline_attr(x_plan: PlanUnit, x_datetime: datetime):
    time_rope = x_plan.make_l1_rope("time")
    creg_rope = x_plan.make_rope(time_rope, creg_str())
    creg_min = get_creg_min_from_dt(x_datetime)
    creg_timelinepoint = plantimelinepoint_shop(x_plan, creg_rope, creg_min)
    creg_timelinepoint.calc_timeline()
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
    if creg_timelinepoint._month in {"January", "February"}:
        dt_year = int(dt_year) - 1
    assert creg_timelinepoint._weekday == dt_weekday
    assert creg_timelinepoint._month == dt_month
    # assert creg_timelinepoint._monthday == int(dt_monthday) - 1
    assert creg_timelinepoint._monthday == int(dt_monthday)
    assert creg_timelinepoint._hour == hour_str
    assert creg_timelinepoint._minute == int(dt_minute)
    assert creg_timelinepoint._year_num == int(dt_year)


def test_check_creg_timeline():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    sue_plan = add_time_creg_conceptunit(sue_plan)
    check_creg_timeline_attr(sue_plan, datetime(2000, 3, 1, 0, 21))
    check_creg_timeline_attr(sue_plan, datetime(2000, 3, 1, 3, 21))
    check_creg_timeline_attr(sue_plan, datetime(2000, 3, 1, 12, 00))
    check_creg_timeline_attr(sue_plan, datetime(2000, 3, 1, 13, 00))
    check_creg_timeline_attr(sue_plan, datetime(2000, 4, 1, 13, 00))
    check_creg_timeline_attr(sue_plan, datetime(2000, 4, 20, 13, 00))
    check_creg_timeline_attr(sue_plan, datetime(2000, 4, 28, 13, 00))
    check_creg_timeline_attr(sue_plan, datetime(2000, 4, 29, 13, 00))
    check_creg_timeline_attr(sue_plan, datetime(2000, 4, 30, 13, 00))
    check_creg_timeline_attr(sue_plan, datetime(2000, 5, 1, 13, 00))
    check_creg_timeline_attr(sue_plan, datetime(2000, 7, 1, 13, 56))
    check_creg_timeline_attr(sue_plan, datetime(2003, 12, 28, 17, 56))
    check_creg_timeline_attr(sue_plan, datetime(2003, 2, 28, 17, 56))
    check_creg_timeline_attr(sue_plan, datetime(432, 3, 4, 2, 0))
