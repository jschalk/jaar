from src.ch01_py.dict_toolbox import get_False_if_None
from src.ch03_rope.rope import is_sub_rope
from src.ch06_plan.plan import PlanUnit
from src.ch07_belief_logic.belief_main import BeliefUnit
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
from src.ch08_epoch.epoch_main import get_day_rope, get_week_rope, get_year_rope


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


def calculate_day_lower_min(day_lower_min: int, day_plan_denom: int) -> int:
    return day_lower_min % day_plan_denom


def calculate_day_upper_min(
    day_lower_min: int, day_duration_min: int, day_plan_denom: int
) -> int:
    return (day_lower_min + day_duration_min) % day_plan_denom


def set_epoch_base_case_dayly(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    day_lower_min: int,
    day_duration_min: int,
):
    """Given an epoch_label set reason for a plan that would make it a dayly occurance
    Example:
    Given: sue_beliefunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, lower_min=600, duration=90
    Add a reason to mop_plan that indicates it's to be active between 10am and 11:30am in lizzy9 epoch
    """
    day_rope = get_day_rope(x_belief, epoch_label)
    day_plan = x_belief.get_plan_obj(day_rope)
    calc_day_lower_min = calculate_day_lower_min(day_lower_min, day_plan.denom)
    calc_day_upper_min = calculate_day_upper_min(
        day_lower_min, day_duration_min, day_plan.denom
    )
    case_args = {
        "plan_rope": plan_rope,
        "reason_context": day_rope,
        "reason_state": day_rope,
        "reason_lower": calc_day_lower_min,
        "reason_upper": calc_day_upper_min,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_base_case_weekly(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    week_lower_min: int,
    week_duration_min: int,
):
    """Given an epoch_label set reason for a plan that would make it a weekly occurance
    Example:
    Given: sue_beliefunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, lower_min=600, duration=90
    Add a reason to mop_plan that indicates it's to be active between minute 600 and minute 690 of the week
    """
    week_rope = get_week_rope(x_belief, epoch_label)
    week_plan = x_belief.get_plan_obj(week_rope)

    case_args = {
        "plan_rope": plan_rope,
        "reason_context": week_rope,
        "reason_state": week_rope,
        "reason_lower": week_lower_min,
        "reason_upper": (week_lower_min + week_duration_min) % week_plan.denom,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_base_case_range(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    range_lower_min: int,
    range_duration_min: int,
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
        "reason_lower": range_lower_min,
        "reason_upper": (range_lower_min + range_duration_min) % epoch_plan.close,
        "reason_divisor": epoch_plan.close,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_base_case_xweeks(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    weeks_lower: int,
    weeks_upper: int,
    every_x_weeks: int,
):
    time_rope = x_belief.make_l1_rope("time")
    epoch_rope = x_belief.make_rope(time_rope, epoch_label)
    weeks_rope = x_belief.make_rope(epoch_rope, "weeks")

    case_args = {
        "plan_rope": plan_rope,
        "reason_context": weeks_rope,
        "reason_state": weeks_rope,
        "reason_lower": weeks_lower % every_x_weeks,
        "reason_upper": weeks_upper % every_x_weeks,
        "reason_divisor": every_x_weeks,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_base_case_xdays(
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


def get_calc_year_lower_upper(
    month_plan: PlanUnit,
    monthday: int,
    length_days,
    range_must_be_within_month: bool,
    year_plan_denom: int,
):
    month_minutes = month_plan.stop_want - month_plan.gogo_want
    monthday_lower_minutes = monthday * 1440
    if range_must_be_within_month and month_minutes < monthday_lower_minutes:
        return None, None
    year_lower_min = monthday_lower_minutes + month_plan.gogo_want
    length_minutes = length_days * 1440
    year_upper_min = year_lower_min + length_minutes
    if range_must_be_within_month and year_upper_min > month_plan.stop_want:
        year_upper_min = month_plan.stop_want
    year_lower_min = year_lower_min % year_plan_denom
    year_upper_min = year_upper_min % year_plan_denom
    return year_lower_min, year_upper_min


def set_epoch_base_case_monthday(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    month_label: LabelTerm,
    monthday: int,
    length_days: int,
    range_must_be_within_month: bool = None,
):
    """Given an epoch_label set reason for a plan that would make it a occurance across entire week(s)
    Example:
    Given: sue_beliefunit, plan_rope=;amy23;casa;mop;, epoch_label=lizzy9, every_x_days=5, days_duration=3
    Add a reason to mop_plan that indicates it's to be active between every 5 days for a length of 3 days
    """
    range_must_be_within_month = get_False_if_None(range_must_be_within_month)
    year_rope = get_year_rope(x_belief, epoch_label)
    month_rope = x_belief.make_rope(year_rope, month_label)
    month_plan = x_belief.get_plan_obj(month_rope)
    year_plan = x_belief.get_plan_obj(year_rope)
    year_lower_min, year_upper_min = get_calc_year_lower_upper(
        month_plan, monthday, length_days, range_must_be_within_month, year_plan.denom
    )
    if year_lower_min is None:
        return

    case_args = {
        "plan_rope": plan_rope,
        "reason_context": month_rope,
        "reason_state": month_rope,
        "reason_lower": year_lower_min,
        "reason_upper": year_upper_min,
    }
    belief_plan_reason_caseunit_set_obj(x_belief, case_args)


def set_epoch_cases_for_dayly(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    day_lower_min: int,
    day_duration_min: int,
    day_lower: int,
    day_upper: int,
    every_x_days: int,
    range_lower_min: int = None,
    range_duration: int = None,
):
    set_epoch_base_case_dayly(
        x_belief, plan_rope, epoch_label, day_lower_min, day_duration_min
    )
    set_epoch_base_case_xdays(
        x_belief, plan_rope, epoch_label, day_lower, day_upper, every_x_days
    )
    if range_lower_min and range_duration:
        set_epoch_base_case_range(
            x_belief, plan_rope, epoch_label, range_lower_min, range_duration
        )


def set_epoch_cases_for_weekly(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    lower_min: int,
    duration: int,
    weeks_lower: int,
    weeks_upper: int,
    every_x_weeks: int,
    range_lower_min: int = None,
    range_duration: int = None,
):
    set_epoch_base_case_weekly(x_belief, plan_rope, epoch_label, lower_min, duration)
    set_epoch_base_case_xweeks(
        x_belief, plan_rope, epoch_label, weeks_lower, weeks_upper, every_x_weeks
    )
    if range_lower_min and range_duration:
        set_epoch_base_case_range(
            x_belief, plan_rope, epoch_label, range_lower_min, range_duration
        )


def set_epoch_cases_for_yearly_monthday(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    day_lower_min: int,
    day_duration_min: int,
    month_label: LabelTerm,
    monthday: int,
    length_days: int,
    range_lower_min: int = None,
    range_duration: int = None,
):
    set_epoch_base_case_dayly(
        x_belief, plan_rope, epoch_label, day_lower_min, day_duration_min
    )
    set_epoch_base_case_monthday(
        x_belief, plan_rope, epoch_label, month_label, monthday, length_days
    )
    if range_lower_min and range_duration:
        set_epoch_base_case_range(
            x_belief, plan_rope, epoch_label, range_lower_min, range_duration
        )


def set_epoch_cases_for_monthly(
    x_belief: BeliefUnit,
    plan_rope: RopeTerm,
    epoch_label: LabelTerm,
    day_lower_min: int,
    day_duration_min: int,
    monthday: int,
    length_days: int,
    range_lower_min: int = None,
    range_duration: int = None,
):
    year_rope = get_year_rope(x_belief, epoch_label)
    year_plan = x_belief.get_plan_obj(year_rope)
    for month_label, month_plan in year_plan.kids.items():
        month_rope = x_belief.make_rope(year_rope, month_label)
        year_lower_min, year_upper_min = get_calc_year_lower_upper(
            month_plan, monthday, length_days, True, year_plan.denom
        )
        if year_lower_min and year_upper_min:
            case_args = {
                "plan_rope": plan_rope,
                "reason_context": year_rope,
                "reason_state": month_rope,
                "reason_lower": year_lower_min,
                "reason_upper": year_upper_min,
            }
            belief_plan_reason_caseunit_set_obj(x_belief, case_args)
    set_epoch_base_case_dayly(
        x_belief, plan_rope, epoch_label, day_lower_min, day_duration_min
    )
    if range_lower_min and range_duration:
        set_epoch_base_case_range(
            x_belief, plan_rope, epoch_label, range_lower_min, range_duration
        )
