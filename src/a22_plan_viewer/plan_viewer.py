import dataclasses
from dataclasses import asdict as dataclasses_asdict
from src.a00_data_toolbox.dict_toolbox import make_dict_safe_for_json
from src.a05_plan_logic.plan import PlanUnit, planunit_shop
from typing import Any


def add_small_dot(x_str: str) -> str:
    return f"&nbsp;&nbsp;<small>• {x_str}</small>"


def custom_asdict(obj: Any) -> dict:
    # sourcery skip: extract-method
    """
    Convert a dataclass-like object to dict,
    including extra keys defined in a custom attribute.
    """
    if dataclasses.is_dataclass(obj):
        result = {}
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            result[field.name] = custom_asdict(value)
        # Include your extra attributes if present
        if isinstance(obj, PlanUnit):
            if result.get("parent_rope") != "":
                result["parent_rope"] = add_small_dot(obj.parent_rope)
            else:
                root_parent_rope_str = "Root Plan parent_rope is empty str"
                result["parent_rope"] = add_small_dot(root_parent_rope_str)
            result["fund_share"] = obj.get_fund_share()
            _all_partner_cred_str = f"all_partner_cred = {obj._all_partner_cred}"
            _all_partner_debt_str = f"all_partner_debt = {obj._all_partner_debt}"
            _all_partner_cred_str = add_small_dot(_all_partner_cred_str)
            _all_partner_debt_str = add_small_dot(_all_partner_debt_str)
            result["_all_partner_cred"] = _all_partner_cred_str
            result["_all_partner_debt"] = _all_partner_debt_str

        return result
    elif isinstance(obj, (list, tuple)):
        return [custom_asdict(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: custom_asdict(v) for k, v in obj.items()}
    else:
        return obj


def get_plan_view_dict(x_plan: PlanUnit) -> dict[str,]:
    """Returns a dictionary of only base value types and dictionarys"""

    # return make_dict_safe_for_json(dataclasses_asdict(x_plan))
    return make_dict_safe_for_json(custom_asdict(x_plan))
