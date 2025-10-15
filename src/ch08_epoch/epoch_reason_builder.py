from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reason_caseunit_set_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
)
from src.ch08_epoch._ref.ch08_semantic_types import LabelTerm, RopeTerm


def set_plan_reason_daily(
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
        "reason_context": epoch_rope,
        "reason_state": epoch_rope,
        "reason_lower": lower_min,
        "reason_upper": (lower_min + duration) % day_plan.denom,
        "reason_divisor": day_plan.denom,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)
