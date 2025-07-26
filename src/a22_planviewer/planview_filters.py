from src.a00_data_toolbox.dict_toolbox import change_nested_key, set_in_nested_dict
from src.a01_term_logic.rope import RopeTerm, get_all_rope_labels
from src.a05_plan_logic.plan import PlanUnit
from src.a06_believer_logic.believer import get_from_dict as get_believerunit_from_dict


def mark_keys(
    x_dict: dict, marking_key: str, mark_text: str = None, max_depth=None, _depth=0
):
    """
    Recursively renames keys in nested dictionaries if their value is a dict containing `marking_key`.
    Appends ' (MARK)' to the key name and removes the `marking_key` from the inner dict.

    Args:
        x_dict (dict): The dictionary to process.
        marking_key (str): The key to detect in nested dictionaries.
        mark_text (str or None): Optional override for the mark text. Defaults to value of `marking_key`.
        max_depth (int or None): How deep to go. None means unlimited.
        _depth (int): Used internally for recursion tracking.

    Returns:
        dict: The transformed dictionary.
    """
    if not isinstance(x_dict, dict):
        return x_dict  # Safety check, shouldn't happen if inputs are valid

    new_dict = {}

    for key, value in x_dict.items():
        new_key = key
        new_value = value

        if isinstance(value, dict):
            if marking_key in value:
                if not mark_text:
                    new_key = f"{key} ({value.get(marking_key)})"
                else:
                    new_key = f"{key} ({mark_text})"

                # Remove the 'task' key
                value = {k: v for k, v in value.items() if k != marking_key}

            # Recurse if within depth
            if max_depth is None or _depth + 1 < max_depth:
                new_value = mark_keys(
                    value, marking_key, mark_text, max_depth, _depth + 1
                )
            else:
                new_value = value

        new_dict[new_key] = new_value

    return new_dict


def get_planunits_list(believerunit_dict: dict) -> list[PlanUnit]:
    x_believerunit = get_believerunit_from_dict(believerunit_dict)
    x_believerunit.settle_believer()
    return x_believerunit._plan_dict.values()


def plan_label(believerunit_dict: dict) -> dict:
    result = {}
    for planunit in get_planunits_list(believerunit_dict):
        plan_labels = get_all_rope_labels(planunit.get_plan_rope())
        if planunit.is_kidless():
            set_in_nested_dict(result, plan_labels, "")
        else:
            set_in_nested_dict(result, plan_labels, {})
    return result


def plan_tasks(believerunit_dict: dict) -> dict:
    result = {}
    for planunit in get_planunits_list(believerunit_dict):
        plan_labels = get_all_rope_labels(planunit.get_plan_rope())
        if planunit.task:
            set_in_nested_dict(result, plan_labels, {"task": "True"})
    return mark_keys(result, marking_key="task", mark_text="TASK")


def plan_fund(believerunit_dict: dict) -> dict:
    result = {}
    for planunit in get_planunits_list(believerunit_dict):
        plan_labels = get_all_rope_labels(planunit.get_plan_rope())
        set_in_nested_dict(
            result, plan_labels, {"fund_share": f"fund {planunit.get_fund_share():,}"}
        )
    return mark_keys(result, marking_key="fund_share")


def plan_awardees(believerunit_dict: dict) -> dict:
    result = {}
    for planunit in get_planunits_list(believerunit_dict):
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


def plan_reasons(believerunit_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_facts(believerunit_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_time(believerunit_dict: dict) -> dict:
    view_dict = {}
    return view_dict
