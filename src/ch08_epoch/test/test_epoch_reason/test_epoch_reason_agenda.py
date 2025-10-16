from src.ch07_belief_logic.belief_main import beliefunit_shop, get_sorted_plan_list
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reason_caseunit_set_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
    get_belief_root_facts_dict,
    set_factunits_to_belief,
)
from src.ch08_epoch.epoch_main import add_epoch_planunit
from src.ch08_epoch.epoch_reason_builder import set_epoch_base_case_dayly
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as exx,
    get_five_config,
)
from src.ref.keywords import Ch08Keywords as wx


def test_set_epoch_base_case_dayly_ChangesBeliefUnit_agenda():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope, pledge=True)
    assert len(bob_belief.get_agenda_dict()) == 1
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    mop_day_lower_min = 600
    mop_day_duration = 90
    bob_belief.add_fact(exx.five_rope, exx.five_rope, 500, 500)
    assert len(bob_belief.get_agenda_dict()) == 1

    # WHEN
    set_epoch_base_case_dayly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    assert len(bob_belief.get_agenda_dict()) == 0
    # WHEN
    bob_belief.add_fact(exx.five_rope, exx.five_rope, 500, 1000)

    # THEN
    bob_belief.cashout()
    print(f"{bob_belief.planroot.factheirs.keys()=}")
    mop_plan = bob_belief.get_plan_obj(exx.mop_rope)
    day_factheir = mop_plan.factheirs.get(exx.day_rope)
    day_reasonheir = mop_plan.reasonheirs.get(exx.day_rope)
    day_heir_case = day_reasonheir.cases.get(exx.day_rope)
    print(f" {day_factheir=}")
    print(f"{day_heir_case=}")
    assert len(bob_belief.get_agenda_dict()) == 1


# def test_set_epoch_base_case_dayly_SetsAttr_Scenario1_WarpAround():
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
#     mop_dayly_args = {
#         wx.plan_rope: exx.mop_rope,
#         wx.reason_context: epoch_five_rope,
#         wx.reason_state: epoch_day_rope,
#     }
#     mop_day_lower_min = 1400
#     mop_day_duration = 95
#     assert bob_belief.plan_exists(epoch_five_rope)
#     assert not belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)

#     # WHEN
#     set_epoch_base_case_dayly(
#         x_belief=bob_belief,
#         plan_rope=exx.mop_rope,
#         epoch_label=five_label,
#         lower_min=mop_day_lower_min,
#         duration=mop_day_duration,
#     )

#     # THEN
#     print(f"{epoch_day_rope=}")
#     assert belief_plan_reason_caseunit_exists(bob_belief, mop_dayly_args)
#     day_case = belief_plan_reason_caseunit_get_obj(bob_belief, mop_dayly_args)
#     assert day_case.reason_state == epoch_day_rope
#     assert day_case.reason_lower == mop_day_lower_min
#     assert day_case.reason_lower == 1400
#     assert day_case.reason_upper == 55
#     assert day_case.reason_divisor == 1440
#     # for x_plan in get_sorted_plan_list(bob_belief._plan_dict):
#     #     print(f"{x_plan.get_plan_rope()=}")


# # create exception if set_epoch_base_case_dayly plan_rope,beginning time + duration is greater then 1440 (must stay within day)

# # create function del_plan_reason_dayly given BeliefUnit, plan_rope,beginning time, duration

# # create test with multiple set_epoch_base_case_dayly added to single plan

# # create test with multiple dayly reasons added and del_plan_reason_dayly only deletes the correct one
