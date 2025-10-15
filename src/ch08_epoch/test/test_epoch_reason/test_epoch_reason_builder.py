from src.ch07_belief_logic.belief_main import beliefunit_shop, get_sorted_plan_list
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reason_caseunit_set_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
    get_belief_root_facts_dict,
)
from src.ch08_epoch.epoch_main import add_epoch_planunit
from src.ch08_epoch.epoch_reason_builder import (
    del_epoch_reason,
    set_epoch_case_daily,
    set_epoch_case_once,
    set_epoch_case_weekly,
)
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as exx,
    get_creg_config,
    get_five_config,
    get_lizzy9_config,
)
from src.ref.keywords import Ch08Keywords as wx


def test_set_epoch_case_daily_SetsAttr_Scenario0_Simple():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    day_rope = bob_belief.make_rope(five_rope, wx.day)
    mop_daily_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: day_rope,
        wx.reason_state: day_rope,
    }
    mop_day_lower_min = 600
    mop_day_duration = 90
    assert bob_belief.plan_exists(five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)

    # WHEN
    set_epoch_case_daily(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    print(f"{get_belief_root_facts_dict(bob_belief)=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_daily_args)
    assert day_case.reason_state == day_rope
    assert day_case.reason_lower == mop_day_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 1440


def test_set_epoch_case_daily_SetsAttr_Scenario1_WarpAround():
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
    mop_daily_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: day_rope,
        wx.reason_state: day_rope,
    }
    mop_day_lower_min = 1400
    mop_day_duration = 95
    assert bob_belief.plan_exists(day_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)

    # WHEN
    set_epoch_case_daily(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    print(f"{day_rope=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_daily_args)
    assert day_case.reason_state == day_rope
    assert day_case.reason_lower == mop_day_lower_min
    assert day_case.reason_lower == 1400
    assert day_case.reason_upper == 55
    assert day_case.reason_divisor == 1440
    # for x_plan in get_sorted_plan_list(bob_belief._plan_dict):
    #     print(f"{x_plan.get_plan_rope()=}")


def test_set_epoch_case_weekly_SetsAttr_Scenario0_Simple():
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
    set_epoch_case_weekly(
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


def test_set_epoch_case_weekly_SetsAttr_Scenario1_Wrap_upper():
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
    set_epoch_case_weekly(
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


def test_set_epoch_case_once_SetsAttr_Scenario0_Simple():
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
    set_epoch_case_once(
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


def test_set_epoch_case_once_SetsAttr_Scenario1_Wrap_upper():
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
    set_epoch_case_once(
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


# create test with multiple set_epoch_case_daily added to single plan

# create test with multiple daily reasons added and del_plan_reason_daily only deletes the correct one


def test_del_epoch_reason_SetsAttr_Scenario0_NoReasonUnitExists():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, exx.five_str)
    day_rope = bob_belief.make_rope(five_rope, wx.day)
    mop_daily_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: day_rope,
        wx.reason_state: day_rope,
    }
    assert bob_belief.plan_exists(exx.mop_rope)
    assert not belief_plan_reasonunit_exists(bob_belief, mop_daily_args)

    # WHEN
    del_epoch_reason(bob_belief, exx.mop_rope, epoch_label=exx.five_str)

    # THEN
    assert not belief_plan_reasonunit_exists(bob_belief, mop_daily_args)


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
    mop_daily_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: day_rope,
        wx.reason_state: day_rope,
    }
    mop_day_lower_min = 600
    mop_day_duration = 90
    # WHEN
    set_epoch_case_daily(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )
    assert belief_plan_reasonunit_exists(bob_belief, mop_daily_args)

    # WHEN
    del_epoch_reason(bob_belief, exx.mop_rope, epoch_label=exx.five_str)

    # THEN
    assert not belief_plan_reasonunit_exists(bob_belief, mop_daily_args)
