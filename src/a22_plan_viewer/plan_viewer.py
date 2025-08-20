import dataclasses
from src.a00_data_toolbox.dict_toolbox import make_dict_safe_for_json
from src.a04_reason_logic.reason_plan import ReasonUnit
from src.a05_plan_logic.plan import (
    AwardHeir,
    AwardLine,
    AwardUnit,
    FactHeir,
    FactUnit,
    PlanUnit,
    ReasonHeir,
    ReasonUnit,
)
from src.a06_belief_logic.belief_main import BeliefUnit
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from typing import Any


def add_small_dot(x_str: str) -> str:
    return f"&nbsp;&nbsp;<small>� {x_str}</small>"


def readable_percent(value: float) -> str:
    # if value is None:
    #     return 0
    pct = value * 100
    if abs(pct) >= 1:  # show as integer percent
        return f"{pct:.0f}%"
    elif abs(pct) >= 0.01:  # show with 2 decimal places
        return f"{pct:.2f}%"
    else:  # very small -> show in scientific-like format
        return f"{pct:.5f}%".rstrip("0").rstrip(".")


def jaar_objs_asdict(obj: Any) -> dict:
    """
    Convert a dataclass-like object to dict,
    including extra keys defined in a custom attribute.
    """
    current_belief = None
    current_reasonunit = None
    if dataclasses.is_dataclass(obj):
        result = {}
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            result[field.name] = jaar_objs_asdict(value)
        if isinstance(obj, BeliefUnit):
            current_belief = obj
        if isinstance(obj, PlanUnit):
            set_readable_plan_values(obj, result)
        elif isinstance(obj, AwardUnit):
            readable_str = (
                f"{obj.awardee_title}: Take {obj.take_force}, Give {obj.give_force}"
            )
            result["readable"] = add_small_dot(readable_str)
        elif isinstance(obj, AwardHeir):
            readable_str = f"{obj.awardee_title}: Take {obj.take_force} ({obj._fund_take}), Give {obj.give_force} ({obj._fund_give})"
            result["readable"] = add_small_dot(readable_str)
        elif isinstance(obj, AwardLine):
            readable_str = f"{obj.awardee_title}: take_fund ({obj._fund_take}), give_fund ({obj._fund_give})"
            result["readable"] = add_small_dot(readable_str)
        elif isinstance(obj, (FactUnit, FactHeir)):
            readable_str = get_fact_state_readable_str(obj, None, current_belief)
            result["readable"] = add_small_dot(readable_str)
        elif isinstance(obj, ReasonUnit):
            current_reasonunit = obj
        elif isinstance(obj, ReasonUnit):
            current_reasonunit = obj

        return result
    elif isinstance(obj, (list, tuple)):
        return [jaar_objs_asdict(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: jaar_objs_asdict(v) for k, v in obj.items()}
    else:
        return obj


def set_readable_plan_values(x_plan: PlanUnit, result: dict):
    result["parent_rope"] = (
        add_small_dot(x_plan.parent_rope)
        if result.get("parent_rope") != ""
        else add_small_dot("Root Plan parent_rope is empty str")
    )
    result["fund_share"] = x_plan.get_fund_share()
    _all_partner_cred_str = f"all_partner_cred = {x_plan._all_partner_cred}"
    _all_partner_debt_str = f"all_partner_debt = {x_plan._all_partner_debt}"
    _all_partner_cred_str = add_small_dot(_all_partner_cred_str)
    _all_partner_debt_str = add_small_dot(_all_partner_debt_str)
    result["_all_partner_cred"] = _all_partner_cred_str
    result["_all_partner_debt"] = _all_partner_debt_str
    result["_fund_ratio"] = readable_percent(result.get("_fund_ratio"))
    result_gogo_want = result.get("gogo_want")
    result_stop_want = result.get("stop_want")
    result_gogo_calc = result.get("_gogo_calc")
    result_stop_calc = result.get("_stop_calc")
    result["gogo_want"] = add_small_dot(f"gogo_want: {result_gogo_want}")
    result["stop_want"] = add_small_dot(f"stop_want: {result_stop_want}")
    result["_gogo_calc"] = add_small_dot(f"gogo_calc: {result_gogo_calc}")
    result["_stop_calc"] = add_small_dot(f"stop_calc: {result_stop_calc}")
    result_addin = result.get("addin")
    result_begin = result.get("begin")
    result_close = result.get("close")
    result_denom = result.get("denom")
    result_morph = result.get("morph")
    result_numor = result.get("numor")
    result["addin"] = add_small_dot(f"addin: {result_addin}")
    result["begin"] = add_small_dot(f"begin: {result_begin}")
    result["close"] = add_small_dot(f"close: {result_close}")
    result["denom"] = add_small_dot(f"denom: {result_denom}")
    result["morph"] = add_small_dot(f"morph: {result_morph}")
    result["numor"] = add_small_dot(f"numor: {result_numor}")
    result["_active_hx"] = add_small_dot(f"active_hx: {x_plan._active_hx}")


def get_plan_view_dict(x_plan: PlanUnit) -> dict[str,]:
    """Returns a dictionary of only base value types and dictionarys"""

    # return make_dict_safe_for_json(dataclasses_asdict(x_plan))
    return make_dict_safe_for_json(jaar_objs_asdict(x_plan))
