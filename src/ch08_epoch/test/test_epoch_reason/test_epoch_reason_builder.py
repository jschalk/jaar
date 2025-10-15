from src.ch07_belief_logic.belief_main import beliefunit_shop, get_sorted_plan_list
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reason_caseunit_set_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
)
from src.ch08_epoch.epoch_main import add_epoch_planunit
from src.ch08_epoch.epoch_reason_builder import set_plan_reason_daily
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as exx,
    get_creg_config,
    get_five_config,
    get_lizzy9_config,
)
from src.ref.keywords import Ch08Keywords as wx


def test_set_plan_reason_daily_SetsAttr_Scenario0_Simple():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    bob_belief.cashout()
    epoch_time_rope = bob_belief.make_l1_rope(wx.time)
    epoch_five_rope = bob_belief.make_rope(epoch_time_rope, five_label)
    epoch_day_rope = bob_belief.make_rope(epoch_five_rope, wx.day)
    mop_daily_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: epoch_five_rope,
        wx.reason_state: epoch_five_rope,
    }
    mop_day_lower_min = 600
    mop_day_duration = 90
    assert bob_belief.plan_exists(epoch_five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)

    # WHEN
    set_plan_reason_daily(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    print(f"{epoch_day_rope=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_daily_args)
    assert day_case.reason_state == epoch_five_rope
    assert day_case.reason_lower == mop_day_lower_min
    assert day_case.reason_lower == 600
    assert day_case.reason_upper == 690
    assert day_case.reason_divisor == 1440


def test_set_plan_reason_daily_SetsAttr_Scenario1_WarpAround():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    bob_belief.cashout()
    epoch_time_rope = bob_belief.make_l1_rope(wx.time)
    epoch_five_rope = bob_belief.make_rope(epoch_time_rope, five_label)
    epoch_day_rope = bob_belief.make_rope(epoch_five_rope, wx.day)
    mop_daily_args = {
        wx.plan_rope: exx.mop_rope,
        wx.reason_context: epoch_five_rope,
        wx.reason_state: epoch_five_rope,
    }
    mop_day_lower_min = 1400
    mop_day_duration = 95
    assert bob_belief.plan_exists(epoch_five_rope)
    assert not belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)

    # WHEN
    set_plan_reason_daily(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    print(f"{epoch_day_rope=}")
    assert belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)
    day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_daily_args)
    assert day_case.reason_state == epoch_five_rope
    assert day_case.reason_lower == mop_day_lower_min
    assert day_case.reason_lower == 1400
    assert day_case.reason_upper == 55
    assert day_case.reason_divisor == 1440
    # for x_plan in get_sorted_plan_list(bob_belief._plan_dict):
    #     print(f"{x_plan.get_plan_rope()=}")


# create exception if set_plan_reason_daily plan_rope,beginning time + duration is greater then 1440 (must stay within day)

# create function del_plan_reason_daily given BeliefUnit, plan_rope,beginning time, duration

# create test with multiple set_plan_reason_daily added to single plan

# create test with multiple daily reasons added and del_plan_reason_daily only deletes the correct one
