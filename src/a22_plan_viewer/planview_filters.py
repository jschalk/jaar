from copy import copy as copy_copy
from src.a00_data_toolbox.dict_toolbox import mark_keys, set_in_nested_dict
from src.a01_term_logic.rope import get_all_rope_labels, get_tail_label
from src.a05_plan_logic.plan import PlanUnit
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)


def plan_label(planunits_list: list[PlanUnit]) -> dict:
    result = {}
    for planunit in planunits_list:
        plan_labels = get_all_rope_labels(planunit.get_plan_rope())
        if planunit.is_kidless():
            set_in_nested_dict(result, plan_labels, "")
        else:
            set_in_nested_dict(result, plan_labels, {})
    return result


def plan_tasks(planunits_list: list[PlanUnit]) -> dict:
    result = {}
    for planunit in planunits_list:
        plan_labels = get_all_rope_labels(planunit.get_plan_rope())
        if planunit.task:
            set_in_nested_dict(result, plan_labels, {"task": "True"})
    return mark_keys(result, marking_key="task", mark_text="TASK")


def plan_fund(planunits_list: list[PlanUnit]) -> dict:
    result = {}
    for planunit in planunits_list:
        plan_labels = get_all_rope_labels(planunit.get_plan_rope())
        set_in_nested_dict(
            result, plan_labels, {"fund_share": f"fund {planunit.get_fund_share():,}"}
        )
    return mark_keys(result, marking_key="fund_share")


def plan_awardees(planunits_list: list[PlanUnit]) -> dict:
    result = {}
    for planunit in planunits_list:
        fund_share_display = f"fund {planunit.get_fund_share():,}"
        plan_rope_labels = get_all_rope_labels(planunit.get_plan_rope())
        fund_share_keys = plan_rope_labels + ["fund_share"]
        set_in_nested_dict(result, fund_share_keys, fund_share_display)

        for awardline in planunit._awardheirs.values():
            awardline_display = (
                f"Give {awardline._fund_give:,}, Take {awardline._fund_take:,}"
            )
            awardline_keys = plan_rope_labels + [awardline.awardee_title]
            set_in_nested_dict(result, awardline_keys, awardline_display)

    return mark_keys(result, marking_key="fund_share")


def plan_reasons(planunits_list: list[PlanUnit]) -> dict:
    result = {}
    for planunit in planunits_list:
        plan_rope_labels = get_all_rope_labels(planunit.get_plan_rope())

        for reason in planunit.reasonunits.values():
            reason_label_str = f"Reason {get_tail_label(reason.reason_context)}"
            reason_keys = copy_copy(plan_rope_labels) + [reason_label_str]
            for case in reason.cases.values():
                case_line_display = get_reason_case_readable_str(
                    reason.reason_context, case
                )
                case_keys = copy_copy(reason_keys) + [case_line_display]
                set_in_nested_dict(result, case_keys, "")
    return result


def plan_facts(planunits_list: list[PlanUnit]) -> dict:
    result = {}
    for planunit in planunits_list:
        plan_rope_labels = get_all_rope_labels(planunit.get_plan_rope())
        plan_keys = copy_copy(plan_rope_labels) + [planunit.plan_label]

        for fact in planunit.factunits.values():
            fact_display_str = get_fact_state_readable_str(fact)
            fact_keys = copy_copy(plan_keys) + [fact_display_str]
            set_in_nested_dict(result, fact_keys, "")
    return result


def plan_time(planunits_list: list[PlanUnit]) -> dict:
    return {}
