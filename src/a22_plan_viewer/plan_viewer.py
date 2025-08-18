from dataclasses import asdict as dataclasses_asdict
from src.a00_data_toolbox.dict_toolbox import make_dict_safe_for_json
from src.a05_plan_logic.plan import PlanUnit, planunit_shop


def get_plan_view_dict(x_plan: PlanUnit) -> dict[str,]:
    """Returns a dictionary of only base value types and dictionarys"""

    # return make_dict_safe_for_json(dataclasses_asdict(x_plan))
    return make_dict_safe_for_json(dataclasses_asdict(x_plan))
