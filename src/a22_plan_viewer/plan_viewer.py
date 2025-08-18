import dataclasses
from dataclasses import asdict as dataclasses_asdict
from src.a00_data_toolbox.dict_toolbox import make_dict_safe_for_json
from src.a05_plan_logic.plan import PlanUnit, planunit_shop
from typing import Any


def custom_asdict(obj: Any) -> dict:
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
            result["fund_share"] = obj.get_fund_share()
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
