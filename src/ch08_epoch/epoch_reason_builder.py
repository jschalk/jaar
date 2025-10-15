from src.ch02_rope.rope import is_sub_rope
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reason_caseunit_set_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
    belief_planunit_exists,
    belief_planunit_get_obj,
)
from src.ch08_epoch._ref.ch08_semantic_types import LabelTerm, RopeTerm


def del_epoch_reason(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
):
    time_rope = x_belief.make_l1_rope("time")
    epoch_rope = x_belief.make_rope(time_rope, epoch_label)
    plan_args = {"plan_rope": plan_rope}
    if belief_planunit_exists(x_belief, plan_args):
        x_plan = belief_planunit_get_obj(x_belief, plan_args)
        reason_contexts = set(x_plan.reasonunits.keys())
        for reason_context in reason_contexts:
            if is_sub_rope(reason_context, epoch_rope):
                x_plan.del_reasonunit_reason_context(reason_context)


def set_epoch_case_daily(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    lower_min: int,
    duration: int,
):
    """Given an epoch_label set reason for a plan that would make it a daily occurance
    Example:
    Given: sue_beliefunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, lower_min=600, duration=90
    Add a reason to mop_plan that indicates it's to be active between 10am and 11:30am in lizzy9 epoch
    """
    time_rope = x_belief.make_l1_rope("time")
    epoch_rope = x_belief.make_rope(time_rope, epoch_label)
    day_rope = x_belief.make_rope(epoch_rope, "day")
    day_plan = x_belief.get_plan_obj(day_rope)
    case_args = {
        "plan_rope": plan_rope,
        "reason_context": day_rope,
        "reason_state": day_rope,
        "reason_lower": lower_min,
        "reason_upper": (lower_min + duration) % day_plan.denom,
        "reason_divisor": day_plan.denom,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_case_weekly(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    lower_min: int,
    duration: int,
):
    """Given an epoch_label set reason for a plan that would make it a weekly occurance
    Example:
    Given: sue_beliefunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, lower_min=600, duration=90
    Add a reason to mop_plan that indicates it's to be active between minute 600 and minute 690 of the week
    """
    time_rope = x_belief.make_l1_rope("time")
    epoch_rope = x_belief.make_rope(time_rope, epoch_label)
    week_rope = x_belief.make_rope(epoch_rope, "week")
    week_plan = x_belief.get_plan_obj(week_rope)

    case_args = {
        "plan_rope": plan_rope,
        "reason_context": week_rope,
        "reason_state": week_rope,
        "reason_lower": lower_min,
        "reason_upper": (lower_min + duration) % week_plan.denom,
        "reason_divisor": week_plan.denom,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_case_once(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    lower_min: int,
    duration: int,
):
    """Given an epoch_label set reason for a plan that would make it a weekly occurance
    Example:
    Given: sue_beliefunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, lower_min=600, duration=90
    Add a reason to mop_plan that indicates it's to be active between minute 600 and minute 690 of the week
    """
    time_rope = x_belief.make_l1_rope("time")
    epoch_rope = x_belief.make_rope(time_rope, epoch_label)
    epoch_plan = x_belief.get_plan_obj(epoch_rope)

    case_args = {
        "plan_rope": plan_rope,
        "reason_context": epoch_rope,
        "reason_state": epoch_rope,
        "reason_lower": lower_min,
        "reason_upper": (lower_min + duration) % epoch_plan.close,
        "reason_divisor": epoch_plan.close,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_case_xweeks(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    week_lower: int,
    week_upper: int,
    every_x_weeks: int,
):
    time_rope = x_belief.make_l1_rope("time")
    epoch_rope = x_belief.make_rope(time_rope, epoch_label)
    weeks_rope = x_belief.make_rope(epoch_rope, "weeks")

    case_args = {
        "plan_rope": plan_rope,
        "reason_context": weeks_rope,
        "reason_state": weeks_rope,
        "reason_lower": week_lower % every_x_weeks,
        "reason_upper": week_upper % every_x_weeks,
        "reason_divisor": every_x_weeks,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_case_xdays(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    day_lower: int,
    day_upper: int,
    every_x_days: int,
):
    """Given an epoch_label set reason for a plan that would make it a occurance across entire week(s)
    Example:
    Given: sue_beliefunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, every_x_days=5, days_duration=3
    Add a reason to mop_plan that indicates it's to be active between every 5 days for a length of 3 days
    """
    time_rope = x_belief.make_l1_rope("time")
    epoch_rope = x_belief.make_rope(time_rope, epoch_label)
    days_rope = x_belief.make_rope(epoch_rope, "days")
    epoch_plan = x_belief.get_plan_obj(epoch_rope)
    days_plan = x_belief.get_plan_obj(days_rope)

    case_args = {
        "plan_rope": plan_rope,
        "reason_context": days_rope,
        "reason_state": days_rope,
        "reason_lower": day_lower % every_x_days,
        "reason_upper": day_upper % every_x_days,
        "reason_divisor": every_x_days,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)
