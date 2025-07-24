from src.a00_data_toolbox.dict_toolbox import set_in_nested_dict
from src.a01_term_logic.rope import RopeTerm, get_all_rope_labels
from src.a05_plan_logic.plan import PlanUnit
from src.a06_believer_logic.believer import get_from_dict as get_believerunit_from_dict


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
    return result


def plan_fund(believerunit_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_awardees(believerunit_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_reasons(believerunit_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_facts(believerunit_dict: dict) -> dict:
    view_dict = {}
    return view_dict


def plan_time(believerunit_dict: dict) -> dict:
    view_dict = {}
    return view_dict
