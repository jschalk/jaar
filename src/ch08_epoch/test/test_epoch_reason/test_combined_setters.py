from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
)
from src.ch08_epoch.epoch_reason_builder import (
    del_epoch_reason,
    set_epoch_base_case_range,
    set_epoch_cases_for_dayly,
    set_epoch_cases_for_monthly,
    set_epoch_cases_for_weekly,
    set_epoch_cases_for_yearly_monthday,
)
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as wx,
    get_bob_five_belief,
    get_creg_config,
    get_five_config,
    get_lizzy9_config,
)
from src.ref.keywords import Ch08Keywords as kw


def test_set_epoch_cases_for_dayly_SetsAttr_Scenario0_MiddleDayEvery3Days():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.days_rope,
        kw.reason_state: wx.days_rope,
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
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
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
    assert day_case.reason_state == wx.day_rope
    assert day_case.reason_lower == mop_day_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 1440


def test_set_epoch_cases_for_dayly_SetsAttr_Scenario1_IncludeRange():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_xdays_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.days_rope,
        kw.reason_state: wx.days_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_day_lower_min = 600
    mop_day_duration = 90
    mop_day_lower = 1
    mop_day_upper = 2
    mop_every_xdays = 3
    mop_range_lower_min = 200
    mop_range_duration = 300
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_xdays_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_range_args)

    # WHEN
    set_epoch_cases_for_dayly(
        x_belief=bob_belief,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        day_lower_min=mop_day_lower_min,
        day_duration_min=mop_day_duration,
        day_lower=mop_day_lower,
        day_upper=mop_day_upper,
        every_x_days=mop_every_xdays,
        range_lower_min=mop_range_lower_min,
        range_duration=mop_range_duration,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_xdays_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_range_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)
    range_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)
    assert range_case.reason_state == wx.five_rope
    assert range_case.reason_lower == 200
    assert range_case.reason_upper == 500
    assert range_case.reason_divisor == 5259492000


def test_set_epoch_cases_for_weekly_SetsAttr_Scenario0_ThirdDayEvery7Weeks():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.week_rope,
        kw.reason_state: wx.week_rope,
    }
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.weeks_rope,
        kw.reason_state: wx.weeks_rope,
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
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
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
    assert week_case.reason_state == wx.week_rope
    assert week_case.reason_lower == mop_week_lower_min
    assert week_case.reason_lower == 600
    assert week_case.reason_upper == 690
    assert week_case.reason_divisor == 7200


def test_set_epoch_cases_for_weekly_SetsAttr_Scenario1_IncludeRange():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_weekly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.week_rope,
        kw.reason_state: wx.week_rope,
    }
    mop_xweeks_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.weeks_rope,
        kw.reason_state: wx.weeks_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_week_lower_min = 600
    mop_week_duration = 90
    mop_week_lower = 2
    mop_week_upper = 3
    mop_every_xweeks = 7
    mop_range_lower_min = 200
    mop_range_duration = 300
    assert not belief_plan_reasonunit_exists(bob_belief, mop_weekly_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_xweeks_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_range_args)

    # WHEN
    set_epoch_cases_for_weekly(
        x_belief=bob_belief,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        lower_min=mop_week_lower_min,
        duration=mop_week_duration,
        weeks_lower=mop_week_lower,
        weeks_upper=mop_week_upper,
        every_x_weeks=mop_every_xweeks,
        range_lower_min=mop_range_lower_min,
        range_duration=mop_range_duration,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_weekly_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_xweeks_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_range_args)
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)
    five_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)
    assert five_case.reason_state == wx.five_rope
    assert five_case.reason_lower == mop_range_lower_min
    assert five_case.reason_lower == 200
    assert five_case.reason_upper == mop_range_lower_min + mop_range_duration
    assert five_case.reason_upper == 500
    assert five_case.reason_divisor == 5259492000


def test_set_epoch_cases_for_yearly_monthday_SetsAttr_Scenario0_NoRange():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    month_geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
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
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        day_lower_min=mop_day_lower_min,
        day_duration_min=mop_day_duration,
        month_label=wx.Geo,
        monthday=mop_monthday,
        length_days=mop_length_days,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_monthday_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)


def test_set_epoch_cases_for_yearly_monthday_SetsAttr_Scenario1_IncludesRange():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    month_geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    mop_monthday_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: month_geo_rope,
        kw.reason_state: month_geo_rope,
    }
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    mop_day_lower_min = 600
    mop_day_duration = 90
    mop_range_lower_min = 200
    mop_range_duration = 300
    assert not belief_plan_reasonunit_exists(bob_belief, mop_monthday_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_range_args)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)

    # WHEN
    set_epoch_cases_for_yearly_monthday(
        x_belief=bob_belief,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        day_lower_min=mop_day_lower_min,
        day_duration_min=mop_day_duration,
        month_label=wx.Geo,
        monthday=mop_monthday,
        length_days=mop_length_days,
        range_lower_min=mop_range_lower_min,
        range_duration=mop_range_duration,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_monthday_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario0_AllDays_within_month_range():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
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
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
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
    month_geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_belief.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 15


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario1_OneDayNot_within_month_range():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
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
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
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
    month_geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_belief.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert not year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 14


def test_set_epoch_cases_for_monthly_SetsAttr_Scenario2_Include_epoch_five_range():
    # ESTABLISH
    bob_belief = get_bob_five_belief()
    mop_year_args = {kw.plan_rope: wx.mop_rope, kw.reason_context: wx.five_year_rope}
    mop_dayly_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.day_rope,
        kw.reason_state: wx.day_rope,
    }
    mop_range_args = {
        kw.plan_rope: wx.mop_rope,
        kw.reason_context: wx.five_rope,
        kw.reason_state: wx.five_rope,
    }
    mop_monthday = 20
    mop_length_days = 4
    mop_day_lower_min = 600
    mop_day_duration = 90
    mop_range_lower_min = 200
    mop_range_duration = 300
    assert not belief_plan_reasonunit_exists(bob_belief, mop_year_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_range_args)

    # WHEN
    set_epoch_cases_for_monthly(
        x_belief=bob_belief,
        plan_rope=wx.mop_rope,
        epoch_label=wx.five_str,
        monthday=mop_monthday,
        length_days=mop_length_days,
        day_lower_min=mop_day_lower_min,
        day_duration_min=mop_day_duration,
        range_lower_min=mop_range_lower_min,
        range_duration=mop_range_duration,
    )

    # THEN
    assert belief_plan_reasonunit_exists(bob_belief, mop_year_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
    assert belief_plan_reasonunit_exists(bob_belief, mop_range_args)
    year_reasonunit = belief_plan_reasonunit_get_obj(bob_belief, mop_year_args)
    year_cases = year_reasonunit.cases
    for month_case in year_cases.values():
        print(f"{month_case.reason_state} {month_case.reason_upper=}")
    month_geo_rope = bob_belief.make_rope(wx.five_year_rope, wx.Geo)
    month_trump_rope = bob_belief.make_rope(wx.five_year_rope, wx.Trump)
    assert year_reasonunit.case_exists(month_geo_rope)
    assert not year_reasonunit.case_exists(month_trump_rope)
    assert len(year_reasonunit.cases) == 14
    range_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_range_args)
    assert range_case.reason_state == wx.five_rope
    assert range_case.reason_lower == 200
    assert range_case.reason_upper == 500
    assert range_case.reason_divisor == 5259492000
