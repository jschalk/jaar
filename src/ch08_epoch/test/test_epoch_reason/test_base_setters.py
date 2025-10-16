from src.ch07_belief_logic.belief_main import beliefunit_shop, get_sorted_plan_list
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reasonunit_exists,
    get_belief_root_facts_dict,
)
from src.ch08_epoch.epoch_main import add_epoch_planunit
from src.ch08_epoch.epoch_reason_builder import (
    del_epoch_reason,
    set_epoch_base_case_dayly,
    set_epoch_base_case_monthday,
    set_epoch_base_case_once,
    set_epoch_base_case_weekly,
    set_epoch_base_case_xdays,
    set_epoch_base_case_xweeks,
)
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as exx,
    get_five_config,
)
from src.ref.keywords import Ch08Keywords as wx


def test_set_epoch_base_case_dayly_SetsAttr_Scenario0_NoWarppingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    day_rope = bob_belief.make_rope(five_rope, wx.day)
    mop_dayly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: day_rope,
        wx.reason_state: day_rope,
    }
    mop_day_lower_min = 600
    mop_day_duration = 90
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)

    # WHEN
    set_epoch_base_case_dayly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    print(f"{get_belief_root_facts_dict(bob_belief)=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_dayly_args)
    assert day_case.reason_state == day_rope
    assert day_case.reason_lower == mop_day_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 1440


def test_set_epoch_base_case_dayly_SetsAttr_Scenario1_WarppingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    bob_belief.cashout()
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    day_rope = bob_belief.make_rope(five_rope, wx.day)
    mop_dayly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: day_rope,
        wx.reason_state: day_rope,
    }
    mop_day_lower_min = 1400
    mop_day_duration = 95
    assert bob_belief.plan_exists(day_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)

    # WHEN
    set_epoch_base_case_dayly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    print(f"{day_rope=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_dayly_args)
    assert day_case.reason_state == day_rope
    assert day_case.reason_lower == mop_day_lower_min
    assert day_case.reason_lower == 1400
    assert day_case.reason_upper == 55
    assert day_case.reason_divisor == 1440
    # for x_plan in get_sorted_plan_list(bob_belief._plan_dict):
    #     print(f"{x_plan.get_plan_rope()=}")


def test_set_epoch_base_case_xdays_SetsAttr_Scenario0_NoWarppingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    days_rope = bob_belief.make_rope(five_rope, wx.days)
    mop_xdays_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: days_rope,
        wx.reason_state: days_rope,
    }
    mop_every_xdays = 7
    mop_day_lower = 3
    mop_day_upper = 5
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_xdays_args)
    bob_belief.cashout()
    for x_plan in get_sorted_plan_list(bob_belief._plan_dict):
        print(f"{x_plan.get_plan_rope()=}")

    # WHEN
    set_epoch_base_case_xdays(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        day_lower=mop_day_lower,
        day_upper=mop_day_upper,
        every_x_days=mop_every_xdays,
    )

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_xdays_args)
    xdays_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xdays_args)
    assert xdays_case.reason_state == days_rope
    assert xdays_case.reason_lower == mop_day_lower
    assert xdays_case.reason_upper == mop_day_upper
    assert xdays_case.reason_upper == 5
    assert xdays_case.reason_divisor == mop_every_xdays


def test_set_epoch_base_case_xdays_SetsAttr_Scenario1_WarppingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    days_rope = bob_belief.make_rope(five_rope, wx.days)
    mop_xdays_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: days_rope,
        wx.reason_state: days_rope,
    }
    mop_every_xdays = 7
    mop_day_lower = 30
    mop_day_upper = 56
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_xdays_args)

    # WHEN
    set_epoch_base_case_xdays(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        day_lower=mop_day_lower,
        day_upper=mop_day_upper,
        every_x_days=mop_every_xdays,
    )

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_xdays_args)
    xdays_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xdays_args)
    assert xdays_case.reason_state == days_rope
    assert xdays_case.reason_lower == mop_day_lower % 7
    assert xdays_case.reason_upper == mop_day_upper % 7
    assert xdays_case.reason_upper == 0
    assert xdays_case.reason_divisor == mop_every_xdays


def test_set_epoch_base_case_weekly_SetsAttr_Scenario0_NoWrapingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    week_rope = bob_belief.make_rope(five_rope, wx.week)
    mop_weekly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: week_rope,
        wx.reason_state: week_rope,
    }
    mop_weekly_lower_min = 600
    mop_weekly_duration = 90
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)

    # WHEN
    set_epoch_base_case_weekly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_weekly_lower_min,
        duration=mop_weekly_duration,
    )

    # THEN
    print(f"{week_rope=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_weekly_args)
    assert day_case.reason_state == week_rope
    assert day_case.reason_lower == mop_weekly_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 7200


def test_set_epoch_base_case_weekly_SetsAttr_Scenario1_WrapingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    week_rope = bob_belief.make_rope(five_rope, wx.week)
    mop_weekly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: week_rope,
        wx.reason_state: week_rope,
    }
    mop_weekly_lower_min = 7000
    mop_weekly_duration = 800
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)

    # WHEN
    set_epoch_base_case_weekly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_weekly_lower_min,
        duration=mop_weekly_duration,
    )

    # THEN
    print(f"{week_rope=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_weekly_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_weekly_args)
    assert day_case.reason_state == week_rope
    assert day_case.reason_lower == mop_weekly_lower_min
    assert day_case.reason_lower == 7000
    assert day_case.reason_upper == 600
    assert day_case.reason_divisor == 7200


def test_set_epoch_base_case_xweeks_SetsAttr_Scenario0_NoWrapingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    weeks_rope = bob_belief.make_rope(five_rope, wx.weeks)
    mop_xweeks_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: weeks_rope,
        wx.reason_state: weeks_rope,
    }
    mop_every_xweeks = 7
    mop_week_lower = 3
    mop_week_upper = 5
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_xweeks_args)

    # WHEN
    set_epoch_base_case_xweeks(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        week_lower=mop_week_lower,
        week_upper=mop_week_upper,
        every_x_weeks=mop_every_xweeks,
    )

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_xweeks_args)
    xweeks_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xweeks_args)
    assert xweeks_case.reason_state == weeks_rope
    assert xweeks_case.reason_lower == mop_week_lower
    assert xweeks_case.reason_upper == mop_week_upper
    assert xweeks_case.reason_upper == 5
    assert xweeks_case.reason_divisor == mop_every_xweeks


def test_set_epoch_base_case_xweeks_SetsAttr_Scenario1_WrapingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    weeks_rope = bob_belief.make_rope(five_rope, wx.weeks)
    mop_xweeks_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: weeks_rope,
        wx.reason_state: weeks_rope,
    }
    mop_every_xweeks = 7
    mop_week_lower = 30
    mop_week_upper = 56
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_xweeks_args)

    # WHEN
    set_epoch_base_case_xweeks(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        week_lower=mop_week_lower,
        week_upper=mop_week_upper,
        every_x_weeks=mop_every_xweeks,
    )

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_xweeks_args)
    xweeks_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_xweeks_args)
    assert xweeks_case.reason_state == weeks_rope
    assert xweeks_case.reason_lower == mop_week_lower % 7
    assert xweeks_case.reason_upper == mop_week_upper % 7
    assert xweeks_case.reason_upper == 0
    assert xweeks_case.reason_divisor == mop_every_xweeks


def test_set_epoch_base_case_once_SetsAttr_Scenario0_NoWrapingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    mop_once_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: five_rope,
        wx.reason_state: five_rope,
    }
    mop_once_lower_min = 600
    mop_once_duration = 90
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_once_args)

    # WHEN
    set_epoch_base_case_once(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_once_lower_min,
        duration=mop_once_duration,
    )

    # THEN
    print(f"{five_rope=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_once_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_once_args)
    assert day_case.reason_state == five_rope
    assert day_case.reason_lower == mop_once_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 5259492000
    assert day_case.reason_divisor == bob_belief.get_plan_obj(five_rope).close


def test_set_epoch_base_case_once_SetsAttr_Scenario1_WrapingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    week_rope = bob_belief.make_rope(five_rope, wx.week)
    mop_once_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: five_rope,
        wx.reason_state: five_rope,
    }
    mop_once_lower_min = 5259490000
    mop_once_duration = 8000
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_once_args)

    # WHEN
    set_epoch_base_case_once(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_once_lower_min,
        duration=mop_once_duration,
    )

    # THEN
    print(f"{week_rope=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_once_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_once_args)
    assert day_case.reason_state == five_rope
    assert day_case.reason_lower == mop_once_lower_min
    assert day_case.reason_lower == 5259490000
    assert day_case.reason_upper == 6000
    assert day_case.reason_divisor == 5259492000


def test_set_epoch_base_case_monthday_SetsAttr_Scenario0_NoWrapingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    month_fred_rope = bob_belief.make_rope(exx.five_year_rope, exx.Fredrick)
    month_geo_rope = bob_belief.make_rope(exx.five_year_rope, exx.Geo)
    mop_monthday_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: month_geo_rope,
        wx.reason_state: month_geo_rope,
    }
    mop_monthday = 3
    mop_length_days = 4
    print(f"geo rope  ='{month_geo_rope}")
    # bob_belief.cashout()
    # for x_plan in get_sorted_plan_list(bob_belief._plan_dict):
    #     print(f"{x_plan.get_plan_rope()=}")
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)

    # WHEN
    set_epoch_base_case_monthday(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        month_label=exx.Geo,
        monthday=mop_monthday,
        length_days=mop_length_days,
    )

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_monthday_args)
    assert day_case.reason_state == month_geo_rope
    month_geo_plan = bob_belief.get_plan_obj(month_geo_rope)
    print(f"{month_geo_plan.gogo_want=} {month_geo_plan.stop_want=}")
    expected_monthday_lower_min = mop_monthday * 1440 + month_geo_plan.gogo_want
    expected_monthday_upper_min = day_case.reason_lower + (mop_length_days * 1440)
    assert day_case.reason_lower == expected_monthday_lower_min
    assert day_case.reason_lower == 40320
    assert day_case.reason_upper == expected_monthday_upper_min
    assert day_case.reason_divisor is None


def test_set_epoch_base_case_monthday_SetsAttr_Scenario1_WrapingParameters():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    month_trump_rope = bob_belief.make_rope(exx.five_year_rope, exx.Trump)
    mop_monthday_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: month_trump_rope,
        wx.reason_state: month_trump_rope,
    }
    mop_monthday = 40
    mop_length_days = 3
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)

    # WHEN
    set_epoch_base_case_monthday(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        month_label=exx.Trump,
        monthday=mop_monthday,
        length_days=mop_length_days,
    )

    # THEN
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_monthday_args)
    monthday_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_monthday_args)
    month_trump_plan = bob_belief.get_plan_obj(month_trump_rope)
    year_plan = bob_belief.get_plan_obj(exx.five_year_rope)
    expected_lower = month_trump_plan.gogo_want + (mop_monthday * 1440)
    expected_upper = monthday_case.reason_lower + (mop_length_days * 1440)
    expected_lower = expected_lower % year_plan.denom
    expected_upper = expected_upper % year_plan.denom

    print(f"{month_trump_plan.gogo_want=} {month_trump_plan.stop_want=}")
    print(f"{monthday_case.reason_lower=} {monthday_case.reason_upper=}")
    print(f"            {expected_lower=}             {expected_upper=}")
    # print(f"{get_range_attrs(year_plan)=}")
    print(f"{year_plan.denom=}")
    assert monthday_case.reason_state == month_trump_rope
    assert monthday_case.reason_lower == expected_lower
    assert monthday_case.reason_lower == 36000
    assert monthday_case.reason_upper == expected_upper
    assert monthday_case.reason_upper == 40320
    assert monthday_case.reason_divisor is None


def test_del_epoch_reason_SetsAttr_Scenario0_NoReasonUnitExists():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, exx.five_str)
    day_rope = bob_belief.make_rope(five_rope, wx.day)
    mop_dayly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: day_rope,
        wx.reason_state: day_rope,
    }
    assert bob_belief.plan_exists(exx.mop_rope)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)

    # WHEN
    del_epoch_reason(bob_belief, exx.mop_rope, epoch_label=exx.five_str)

    # THEN
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)


def test_del_epoch_reason_SetsAttr_Scenario1_ReasonUnitExists():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    add_epoch_planunit(bob_belief, five_config)
    bob_belief.cashout()
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_label = five_config.get(wx.epoch_label)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    day_rope = bob_belief.make_rope(five_rope, wx.day)
    mop_dayly_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: day_rope,
        wx.reason_state: day_rope,
    }
    mop_day_lower_min = 600
    mop_day_duration = 90
    # WHEN
    set_epoch_base_case_dayly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )
    assert belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)

    # WHEN
    del_epoch_reason(bob_belief, exx.mop_rope, epoch_label=exx.five_str)

    # THEN
    assert not belief_plan_reasonunit_exists(bob_belief, mop_dayly_args)
