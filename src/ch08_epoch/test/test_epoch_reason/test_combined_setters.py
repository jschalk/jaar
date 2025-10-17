from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
)
from src.ch08_epoch.epoch_reason_builder import (
    del_epoch_reason,
    set_epoch_base_case_datetime_range,
    set_epoch_cases_for_dayly,
    set_epoch_cases_for_monthly,
    set_epoch_cases_for_weekly,
    set_epoch_cases_for_yearly_monthday,
)
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as exx,
    get_bob_five_belief,
    get_creg_config,
    get_five_config,
    get_lizzy9_config,
)
from src.ref.keywords import Ch08Keywords as wx


def test_set_epoch_cases_for_dayly_SetsAttr_Scenario0_MiddleDayEvery3Days():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_dayly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: exx.day_rope,
        wx.reason_state: exx.day_rope,
    }
    mop_xdays_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: exx.days_rope,
        wx.reason_state: exx.days_rope,
    }
    mop_day_lower_min = 600
    mop_day_duration = 90
    mop_day_lower = 1
    mop_day_upper = 2
    mop_every_xdays = 3
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_xdays_args)

    # WHEN
    set_epoch_cases_for_dayly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=exx.five_str,
        day_lower_min=mop_day_lower_min,
        day_duration_min=mop_day_duration,
        day_lower=mop_day_lower,
        day_upper=mop_day_upper,
        every_x_days=mop_every_xdays,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_xdays_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_dayly_args)
    assert day_case.reason_state == exx.day_rope
    assert day_case.reason_lower == mop_day_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 1440


def test_set_epoch_cases_for_weekly_SetsAttr_Scenario0_ThirdDayEvery7Weeks():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_weekly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: exx.week_rope,
        wx.reason_state: exx.week_rope,
    }
    mop_xweeks_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: exx.weeks_rope,
        wx.reason_state: exx.weeks_rope,
    }
    mop_week_lower_min = 600
    mop_week_duration = 90
    mop_week_lower = 2
    mop_week_upper = 3
    mop_every_xweeks = 7
    assert not belief_plan_reasonunit_exists(bob_belief, mop_weekly_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_xweeks_args)

    # WHEN
    set_epoch_cases_for_weekly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=exx.five_str,
        lower_min=mop_week_lower_min,
        duration=mop_week_duration,
        weeks_lower=mop_week_lower,
        weeks_upper=mop_week_upper,
        every_x_weeks=mop_every_xweeks,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_weekly_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_xweeks_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)
    week_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_weekly_args)
    assert week_case.reason_state == exx.week_rope
    assert week_case.reason_lower == mop_week_lower_min
    assert week_case.reason_lower == 600
    assert week_case.reason_upper == 690
    assert week_case.reason_divisor == 7200


def test_set_epoch_cases_for_yearly_monthday_SetsAttr_Scenario0():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    month_geo_rope = bob_belief.make_rope(exx.five_year_rope, exx.Geo)
    mop_monthday_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: month_geo_rope,
        wx.reason_state: month_geo_rope,
    }
    mop_dayly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: exx.day_rope,
        wx.reason_state: exx.day_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    mop_day_lower_min = 600
    mop_day_duration = 90
    assert not belief_plan_reasonunit_exists(bob_belief, mop_monthday_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)

    # WHEN
    set_epoch_cases_for_yearly_monthday(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=exx.five_str,
        day_lower_min=mop_day_lower_min,
        day_duration_min=mop_day_duration,
        month_label=exx.Geo,
        monthday=mop_monthday,
        length_days=mop_length_days,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_monthday_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario0_AllDays_within_month_range():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_year_args = {wx.plan_rope: exx.mop_rope, wx.reason_context: exx.five_year_rope}
    mop_dayly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: exx.day_rope,
        wx.reason_state: exx.day_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    mop_day_lower_min = 600
    mop_day_duration = 90
    assert not belief_plan_reasonunit_exists(bob_belief, mop_year_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)

    # WHEN
    set_epoch_cases_for_monthly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=exx.five_str,
        monthday=mop_monthday,
        length_days=mop_length_days,
        day_lower_min=mop_day_lower_min,
        day_duration_min=mop_day_duration,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_year_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    year_reasonunit = belief_plan_reasonunit_get_obj(bob_belief, mop_year_args)
    year_cases = year_reasonunit.cases
    print(f"{year_cases.keys()=}")
    month_geo_rope = bob_belief.make_rope(exx.five_year_rope, exx.Geo)
    month_trump_rope = bob_belief.make_rope(exx.five_year_rope, exx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 15


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario1_OneDayNot_within_month_range():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_year_args = {wx.plan_rope: exx.mop_rope, wx.reason_context: exx.five_year_rope}
    mop_dayly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: exx.day_rope,
        wx.reason_state: exx.day_rope,
    }
    mop_monthday = 20
    mop_length_days = 4
    mop_day_lower_min = 600
    mop_day_duration = 90
    assert not belief_plan_reasonunit_exists(bob_belief, mop_year_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)

    # WHEN
    set_epoch_cases_for_monthly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=exx.five_str,
        monthday=mop_monthday,
        length_days=mop_length_days,
        day_lower_min=mop_day_lower_min,
        day_duration_min=mop_day_duration,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_year_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    year_reasonunit = belief_plan_reasonunit_get_obj(bob_belief, mop_year_args)
    year_cases = year_reasonunit.cases
    for month_case in year_cases.values():
        print(f"{month_case.reason_state} {month_case.reason_upper=}")
    month_geo_rope = bob_belief.make_rope(exx.five_year_rope, exx.Geo)
    month_trump_rope = bob_belief.make_rope(exx.five_year_rope, exx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert not year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 14
