from src.ch07_belief_logic.belief_main import beliefunit_shop, get_sorted_plan_list
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reason_caseunit_set_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
    set_factunits_to_belief,
)
from src.ch08_epoch.epoch_main import add_epoch_planunit
from src.ch08_epoch.epoch_reason_builder import set_epoch_case_daily
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as exx,
    get_five_config,
)
from src.ref.keywords import Ch08Keywords as wx


def test_set_epoch_case_daily_ChangesBeliefUnit_agenda():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope, pledge=True)
    assert len(bob_belief.get_agenda_dict()) == 1
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    # beliefunit with pledge planunit that has reason set by set_epoch_case_daily
    # confirm different idearoot facts produce different outcomes
    add_epoch_planunit(bob_belief, five_config)
    bob_belief.cashout()
    time_rope = bob_belief.make_l1_rope(wx.time)
    five_rope = bob_belief.make_rope(time_rope, five_label)
    mop_day_lower_min = 600
    mop_day_duration = 90
    bob_belief.add_fact(five_rope, five_rope, 500, 500)
    assert len(bob_belief.get_agenda_dict()) == 1

    # WHEN
    set_epoch_case_daily(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    assert len(bob_belief.get_agenda_dict()) == 0
    # WHEN
    bob_belief.add_fact(five_rope, five_rope, 500, 1000)

    # THEN
    assert len(bob_belief.get_agenda_dict()) == 1


# def test_set_epoch_case_daily_SetsAttr_Scenario1_WarpAround():
#     # ESTABLISH
#     bob_belief = beliefunit_shop(exx.Bob)
#     bob_belief.add_plan(exx.mop_rope)
#     five_config = get_five_config()
#     five_label = five_config.get(wx.epoch_label)
#     add_epoch_planunit(bob_belief, five_config)
#     bob_belief.cashout()
#     time_rope = bob_belief.make_l1_rope(wx.time)
#     epoch_five_rope = bob_belief.make_rope(time_rope, five_label)
#     epoch_day_rope = bob_belief.make_rope(epoch_five_rope, wx.day)
#     mop_daily_args = {
#         wx.plan_rope: exx.mop_rope,
#         wx.reason_context: epoch_five_rope,
#         wx.reason_state: epoch_day_rope,
#     }
#     mop_day_lower_min = 1400
#     mop_day_duration = 95
#     assert bob_belief.plan_exists(epoch_five_rope)
#     assert not belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)

#     # WHEN
#     set_epoch_case_daily(
#         x_belief=bob_belief,
#         plan_rope=exx.mop_rope,
#         epoch_label=five_label,
#         lower_min=mop_day_lower_min,
#         duration=mop_day_duration,
#     )

#     # THEN
#     print(f"{epoch_day_rope=}")
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_daily_args)
#     day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_daily_args)
#     assert day_case.reason_state == epoch_day_rope
#     assert day_case.reason_lower == mop_day_lower_min
#     assert day_case.reason_lower == 1400
#     assert day_case.reason_upper == 55
#     assert day_case.reason_divisor == 1440
#     # for x_plan in get_sorted_plan_list(bob_belief._plan_dict):
#     #     print(f"{x_plan.get_plan_rope()=}")


# # create exception if set_epoch_case_daily plan_rope,beginning time + duration is greater then 1440 (must stay within day)

# # create function del_plan_reason_daily given BeliefUnit, plan_rope,beginning time, duration

# # create test with multiple set_epoch_case_daily added to single plan

# # create test with multiple daily reasons added and del_plan_reason_daily only deletes the correct one
