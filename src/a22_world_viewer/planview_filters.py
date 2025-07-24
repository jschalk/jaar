from src.a00_data_toolbox.dict_toolbox import set_in_nested_dict
from src.a01_term_logic.rope import get_all_rope_labels
from src.a06_believer_logic.believer import get_from_dict as get_believerunit_from_dict


def plan_label(x_dict: dict) -> dict:

    x_believerunit = get_believerunit_from_dict(x_dict)
    x_believerunit.settle_believer()

    result = {}
    for planunit in x_believerunit._plan_dict.values():
        plan_labels = get_all_rope_labels(planunit.get_plan_rope())
        set_in_nested_dict(result, plan_labels, {})

    return result


def plan_tasks(x_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_fund(x_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_awardees(x_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_reasons(x_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_facts(x_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_time(x_dict: dict) -> dict:
    view_dict = {}
    return view_dict
