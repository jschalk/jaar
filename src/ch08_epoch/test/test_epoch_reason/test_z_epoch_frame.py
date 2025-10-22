from src.ch06_plan.test._util.ch06_examples import get_range_attrs
from src.ch07_belief_logic.belief_main import beliefunit_shop, get_sorted_plan_list
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reasonunit_get_obj,
    belief_planunit_get_obj,
    get_belief_root_facts_dict,
)
from src.ch08_epoch.epoch_reason import (
    add_epoch_frame_to_beliefunit,
    add_epoch_frame_to_caseunit_dayly,
    add_epoch_frame_to_caseunit_monthday,
    add_epoch_frame_to_caseunit_monthly,
    add_epoch_frame_to_caseunit_obj,
    add_epoch_frame_to_caseunit_range,
    add_epoch_frame_to_caseunit_weekly,
    add_epoch_frame_to_caseunit_xdays,
    add_epoch_frame_to_caseunit_xweeks,
    add_epoch_frame_to_factunit,
    add_epoch_frame_to_planunit,
    apply_epoch_frame,
    del_epoch_reason,
    set_epoch_cases_by_args_dict,
)
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as wx,
    get_bob_five_belief,
)
from src.ref.keywords import Ch08Keywords as kw


def test_apply_epoch_frame_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert apply_epoch_frame(x_min=1000, epoch_frame=500, denom=1440) == 60
    assert apply_epoch_frame(1000, 500, 1440) == 60
    assert apply_epoch_frame(1000, 1200, 1200) == 1000
    assert apply_epoch_frame(1000, 200, 1200) == 0
    assert apply_epoch_frame(1000, -2000, 1200) == 200


def test_add_epoch_frame_to_caseunit_dayly_SetsAttr_Scenario0_adds_epoch_frame_NoWrap_dayly():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
        kw.epoch_label: wx.five_str,
        kw.dayly_lower_min: 600,
        kw.dayly_duration_min: 90,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_dayly_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_dayly_args)
    x_epoch_frame = 100
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690

    # WHEN
    add_epoch_frame_to_caseunit_dayly(day_case, x_epoch_frame)

    # THEN
    assert day_case.reason_lower != 600
    assert day_case.reason_upper != 690
    assert day_case.reason_lower == 600 + 100
    assert day_case.reason_upper == 690 + 100


def test_add_epoch_frame_to_caseunit_dayly_SetsAttr_Scenario1_adds_epoch_frame_Wrap_dayly():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
        kw.epoch_label: wx.five_str,
        kw.dayly_lower_min: 600,
        kw.dayly_duration_min: 90,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_dayly_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_dayly_args)
    x_epoch_frame = 1000
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690

    # WHEN
    add_epoch_frame_to_caseunit_dayly(day_case, x_epoch_frame)

    # THEN
    assert day_case.reason_lower != 600
    assert day_case.reason_upper != 690
    assert day_case.reason_lower == (600 + x_epoch_frame) % day_case.reason_divisor
    assert day_case.reason_upper == (690 + x_epoch_frame) % day_case.reason_divisor


def test_add_epoch_frame_to_caseunit_xdays_SetsAttr_Scenario0_adds_epoch_frame_NoWarp_xdays():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_days_lower_day = 3
    mop_days_upper_day = 4
    mop_every_xdays = 13
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.days_rope,
        kw.reason_state: wx.days_rope,
        kw.epoch_label: wx.five_str,
        kw.days_lower_day: mop_days_lower_day,
        kw.days_upper_day: mop_days_upper_day,
        kw.every_xdays: mop_every_xdays,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_xdays_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_xdays_args)
    xdays_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xdays_args)
    x_epoch_frame = 5000
    assert xdays_case.reason_lower == mop_days_lower_day
    assert xdays_case.reason_upper == mop_days_upper_day

    # WHEN
    add_epoch_frame_to_caseunit_xdays(xdays_case, x_epoch_frame)

    # THEN
    assert xdays_case.reason_lower != mop_days_lower_day
    assert xdays_case.reason_upper != mop_days_upper_day
    assert xdays_case.reason_lower == mop_days_lower_day + 3
    assert xdays_case.reason_upper == mop_days_upper_day + 3


def test_add_epoch_frame_to_caseunit_xdays_SetsAttr_Scenario1_adds_epoch_frame_Wrap_xdays():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_days_lower_day = 3
    mop_days_upper_day = 4
    mop_every_xdays = 13
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.days_rope,
        kw.reason_state: wx.days_rope,
        kw.epoch_label: wx.five_str,
        kw.days_lower_day: mop_days_lower_day,
        kw.days_upper_day: mop_days_upper_day,
        kw.every_xdays: mop_every_xdays,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_xdays_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_xdays_args)
    xdays_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xdays_args)
    x_epoch_frame_min = 50000
    assert xdays_case.reason_lower == mop_days_lower_day
    assert xdays_case.reason_upper == mop_days_upper_day

    # WHEN
    add_epoch_frame_to_caseunit_xdays(xdays_case, x_epoch_frame_min)

    # THEN
    assert xdays_case.reason_lower != mop_days_lower_day
    assert xdays_case.reason_upper != mop_days_upper_day
    print(f"{x_epoch_frame_min//1440=}")
    print(f"{mop_days_lower_day + (x_epoch_frame_min//1440)=}")
    ex_lower = (mop_days_lower_day + (x_epoch_frame_min // 1440)) % mop_every_xdays
    ex_upper = (mop_days_upper_day + (x_epoch_frame_min // 1440)) % mop_every_xdays
    assert xdays_case.reason_lower == ex_lower
    assert xdays_case.reason_upper == ex_upper


def test_add_epoch_frame_to_caseunit_weekly_SetsAttr_Scenario0_adds_epoch_frame_NoWrap():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.week_rope,
        kw.reason_state: wx.week_rope,
        kw.epoch_label: wx.five_str,
        kw.weekly_lower_min: 600,
        kw.weekly_duration_min: 90,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_weekly_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)
    week_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_weekly_args)
    x_epoch_frame = 100
    assert week_case.reason_lower == 600
    assert week_case.reason_upper == 690

    # WHEN
    add_epoch_frame_to_caseunit_weekly(week_case, x_epoch_frame)

    # THEN
    assert week_case.reason_lower != 600
    assert week_case.reason_upper != 690
    assert week_case.reason_lower == 600 + 100
    assert week_case.reason_upper == 690 + 100


def test_add_epoch_frame_to_caseunit_weekly_SetsAttr_Scenario1_adds_epoch_frame_Wrap_weekly():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.week_rope,
        kw.reason_state: wx.week_rope,
        kw.epoch_label: wx.five_str,
        kw.weekly_lower_min: 600,
        kw.weekly_duration_min: 90,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_weekly_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)
    week_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_weekly_args)
    x_epoch_frame = 10000
    assert week_case.reason_lower == 600
    assert week_case.reason_upper == 690

    # WHEN
    add_epoch_frame_to_caseunit_weekly(week_case, x_epoch_frame)

    # THEN
    assert week_case.reason_lower != 600
    assert week_case.reason_upper != 690
    assert week_case.reason_lower == (600 + x_epoch_frame) % week_case.reason_divisor
    assert week_case.reason_upper == (690 + x_epoch_frame) % week_case.reason_divisor


def test_add_epoch_frame_to_caseunit_xweeks_SetsAttr_Scenario0_adds_epoch_frame_NoWrap_xweeks():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_weeks_lower_week = 3
    mop_weeks_upper_week = 4
    mop_every_xweeks = 13
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.weeks_rope,
        kw.reason_state: wx.weeks_rope,
        kw.epoch_label: wx.five_str,
        kw.weeks_lower_week: mop_weeks_lower_week,
        kw.weeks_upper_week: mop_weeks_upper_week,
        kw.every_xweeks: mop_every_xweeks,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_xweeks_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_xweeks_args)
    xweeks_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xweeks_args)
    x_epoch_frame = 24000
    assert xweeks_case.reason_lower == mop_weeks_lower_week
    assert xweeks_case.reason_upper == mop_weeks_upper_week

    # WHEN
    add_epoch_frame_to_caseunit_xweeks(xweeks_case, x_epoch_frame)

    # THEN
    assert xweeks_case.reason_lower != mop_weeks_lower_week
    assert xweeks_case.reason_upper != mop_weeks_upper_week
    assert xweeks_case.reason_lower == mop_weeks_lower_week + 2
    assert xweeks_case.reason_upper == mop_weeks_upper_week + 2


def test_add_epoch_frame_to_caseunit_xweeks_SetsAttr_Scenario1_adds_epoch_frame_Wraps_every_xweeks():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_weeks_lower_week = 3
    mop_weeks_upper_week = 4
    mop_every_xweeks = 13
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.weeks_rope,
        kw.reason_state: wx.weeks_rope,
        kw.epoch_label: wx.five_str,
        kw.weeks_lower_week: mop_weeks_lower_week,
        kw.weeks_upper_week: mop_weeks_upper_week,
        kw.every_xweeks: mop_every_xweeks,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_xweeks_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_xweeks_args)
    xweeks_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xweeks_args)
    x_epoch_frame_min = 50000
    assert xweeks_case.reason_lower == mop_weeks_lower_week
    assert xweeks_case.reason_upper == mop_weeks_upper_week

    # WHEN
    add_epoch_frame_to_caseunit_xweeks(xweeks_case, x_epoch_frame_min)

    # THEN
    assert xweeks_case.reason_lower != mop_weeks_lower_week
    assert xweeks_case.reason_upper != mop_weeks_upper_week
    print(f"{x_epoch_frame_min//10080=}")
    print(f"{mop_weeks_lower_week + (x_epoch_frame_min//10080)=}")
    ex_lower = (mop_weeks_lower_week + (x_epoch_frame_min // 10080)) % mop_every_xweeks
    ex_upper = (mop_weeks_upper_week + (x_epoch_frame_min // 10080)) % mop_every_xweeks
    assert xweeks_case.reason_lower == ex_lower
    assert xweeks_case.reason_upper == ex_upper


def test_add_epoch_frame_to_caseunit_monthday_SetsAttr_Scenario0_adds_epoch_frame_NoWrapYear():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.reason_context: geo_rope,
        kw.reason_state: geo_rope,
        kw.month_label: wx.Geo,
        kw.year_monthday_lower: 5,
        kw.year_monthday_duration_days: 3,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_monthday_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)
    year_reason = belief_plan_reasonunit_get_obj(bob_belief, mop_monthday_args)
    monthday_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_monthday_args)

    print(f"{monthday_case.reason_divisor=}")
    x_epoch_frame = 500
    geo_5_epochpoint = 43200
    geo_8_epochpoint = 47520
    assert monthday_case.reason_lower == geo_5_epochpoint
    assert monthday_case.reason_upper == geo_8_epochpoint

    # WHEN
    add_epoch_frame_to_caseunit_monthday(monthday_case, x_epoch_frame)

    # THEN
    assert monthday_case.reason_lower != geo_5_epochpoint
    assert monthday_case.reason_upper != geo_8_epochpoint
    assert monthday_case.reason_lower == geo_5_epochpoint + x_epoch_frame
    assert monthday_case.reason_upper == geo_8_epochpoint + x_epoch_frame


def test_add_epoch_frame_to_caseunit_monthday_SetsAttr_Scenario1_adds_epoch_frame_WrapsYear():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.reason_context: geo_rope,
        kw.reason_state: geo_rope,
        kw.month_label: wx.Geo,
        kw.year_monthday_lower: 5,
        kw.year_monthday_duration_days: 3,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_monthday_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_monthday_args)
    x_epoch_frame_min = 5000000
    geo_5_epochpoint = 43200
    geo_8_epochpoint = 47520
    assert day_case.reason_lower == geo_5_epochpoint
    assert day_case.reason_upper == geo_8_epochpoint

    # WHEN
    add_epoch_frame_to_caseunit_monthday(day_case, x_epoch_frame_min)

    # THEN
    assert day_case.reason_lower != geo_5_epochpoint
    assert day_case.reason_upper != geo_8_epochpoint
    print(f"{(geo_5_epochpoint + x_epoch_frame_min) % 525600=}")
    print(f"{(geo_8_epochpoint + x_epoch_frame_min) % 525600=}")
    assert day_case.reason_lower == (geo_5_epochpoint + x_epoch_frame_min) % 525600
    assert day_case.reason_upper == (geo_8_epochpoint + x_epoch_frame_min) % 525600


def test_add_epoch_frame_to_caseunit_monthly_SetsAttr_Scenario0_adds_epoch_frame_NoWrapYear():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.monthly_monthday_lower: 5,
        kw.monthly_duration_days: 3,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_monthly_args)
    geo_month_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.reason_context: wx.five_year_rope,
        kw.reason_state: geo_rope,
    }
    assert belief_plan_reason_caseunit_exists(bob_belief, geo_month_args)
    geo_case = belief_plan_reason_caseunit_get_obj(bob_belief, geo_month_args)

    print(f"{geo_case.reason_divisor=}")
    x_epoch_frame = 500
    geo_5_epochpoint = 43200
    geo_8_epochpoint = 47520
    assert geo_case.reason_lower == geo_5_epochpoint
    assert geo_case.reason_upper == geo_8_epochpoint

    # WHEN
    add_epoch_frame_to_caseunit_monthly(geo_case, x_epoch_frame)

    # THEN
    assert geo_case.reason_lower != geo_5_epochpoint
    assert geo_case.reason_upper != geo_8_epochpoint
    assert geo_case.reason_lower == geo_5_epochpoint + x_epoch_frame
    assert geo_case.reason_upper == geo_8_epochpoint + x_epoch_frame


def test_add_epoch_frame_to_caseunit_monthly_SetsAttr_Scenario1_adds_epoch_frame_WrapsYear():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.monthly_monthday_lower: 5,
        kw.monthly_duration_days: 3,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_monthly_args)
    geo_month_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.reason_context: wx.five_year_rope,
        kw.reason_state: geo_rope,
    }
    assert belief_plan_reason_caseunit_exists(bob_belief, geo_month_args)
    geo_case = belief_plan_reason_caseunit_get_obj(bob_belief, geo_month_args)
    x_epoch_frame_min = 5000000
    geo_5_epochpoint = 43200
    geo_8_epochpoint = 47520
    assert geo_case.reason_lower == geo_5_epochpoint
    assert geo_case.reason_upper == geo_8_epochpoint

    # WHEN
    add_epoch_frame_to_caseunit_monthly(geo_case, x_epoch_frame_min)

    # THEN
    assert geo_case.reason_lower != geo_5_epochpoint
    assert geo_case.reason_upper != geo_8_epochpoint
    print(f"{(geo_5_epochpoint + x_epoch_frame_min) % 525600=}")
    print(f"{(geo_8_epochpoint + x_epoch_frame_min) % 525600=}")
    assert geo_case.reason_lower == (geo_5_epochpoint + x_epoch_frame_min) % 525600
    assert geo_case.reason_upper == (geo_8_epochpoint + x_epoch_frame_min) % 525600


def test_add_epoch_frame_to_caseunit_range_SetsAttr_Scenario0_adds_epoch_frame_NoWrapYear():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    x_range_lower_min = 7777
    x_range_duration = 2000
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
        kw.range_lower_min: x_range_lower_min,
        kw.range_duration: x_range_duration,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_range_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_range_args)
    epoch_args = {kw.plan_rope: wx.five_rope}
    epoch_plan = belief_planunit_get_obj(bob_belief, epoch_args)
    epoch_length_min = epoch_plan.close
    print(f"{get_range_attrs(epoch_plan)=}")
    epoch_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)

    x_epoch_frame = 500
    x_range_upper_min = x_range_lower_min + x_range_duration
    assert epoch_case.reason_lower == x_range_lower_min
    assert epoch_case.reason_upper == x_range_upper_min

    # WHEN
    add_epoch_frame_to_caseunit_range(epoch_case, epoch_length_min, x_epoch_frame)

    # THEN
    assert epoch_case.reason_lower != x_range_lower_min
    assert epoch_case.reason_upper != x_range_duration
    assert epoch_case.reason_lower == x_range_lower_min + x_epoch_frame
    assert epoch_case.reason_upper == x_range_upper_min + x_epoch_frame


def test_add_epoch_frame_to_caseunit_range_SetsAttr_Scenario1_adds_epoch_frame_WrapsYear():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    x_range_lower_min = 7777
    x_range_duration = 2000
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.epoch_label: wx.five_str,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
        kw.range_lower_min: x_range_lower_min,
        kw.range_duration: x_range_duration,
    }
    set_epoch_cases_by_args_dict(bob_belief, mop_range_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_range_args)
    epoch_args = {kw.plan_rope: wx.five_rope}
    epoch_plan = belief_planunit_get_obj(bob_belief, epoch_args)
    print(f"{get_range_attrs(epoch_plan)=}")
    epoch_length_min = epoch_plan.close
    epoch_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)

    x_epoch_frame = epoch_length_min + 10005
    x_range_upper_min = x_range_lower_min + x_range_duration
    assert epoch_case.reason_lower == x_range_lower_min
    assert epoch_case.reason_upper == x_range_upper_min

    # WHEN
    add_epoch_frame_to_caseunit_range(epoch_case, epoch_length_min, x_epoch_frame)

    # THEN
    assert epoch_case.reason_lower != x_range_lower_min
    assert epoch_case.reason_upper != x_range_duration
    print(
        f"{x_range_lower_min + x_epoch_frame=} vs {epoch_length_min} (epoch_length_min)"
    )
    expected_lower = (x_range_lower_min + x_epoch_frame) % epoch_length_min
    expected_upper = (x_range_upper_min + x_epoch_frame) % epoch_length_min
    assert epoch_case.reason_lower == expected_lower
    assert epoch_case.reason_upper == expected_upper


# # set_epoch_base_case_monthly
# # "reason_state": change reason_state month to correct month
# # "reason_lower": add_epoch_frame_then_modular_reason_year_525600_Then check what month new reason_lower is in.
# # There can be only one caseunit per month, If there is a conflict take younger date or raise exception
# # "reason_upper": add_epoch_frame_then_modular_reason_year_525600_Then check what month new reason_upper is in.
# # There can be only one caseunit per month, If there is a conflict take younger date or raise exception


# def test_add_epoch_frame_to_caseunit_range_ReturnsObj():
#     assert 1 == 2


# def test_add_epoch_frame_to_factunit_ReturnsObj():
#     assert 1 == 2


# def test_add_epoch_frame_to_planunit_ReturnsObj():
#     assert 1 == 2


# def test_add_epoch_frame_to_beliefunit_ReturnsObj():
#     assert 1 == 2
