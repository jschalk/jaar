from dataclasses import asdict as dataclasses_asdict
from src.a05_plan_logic.plan import PlanUnit, planunit_shop


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, set):
        return list(obj)
    else:
        return obj


def get_plan_view_dict(x_plan: PlanUnit) -> dict[str,]:
    """Returns a dictionary of only base value types and dictionarys"""

    # return make_json_safe(dataclasses_asdict(x_plan))
    return make_json_safe(dataclasses_asdict(x_plan))
