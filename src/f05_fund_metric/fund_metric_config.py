from src.f00_instrument.file import open_json, save_json, create_path
from src.f00_instrument.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd


def jmetrics_str() -> str:
    return "jmetrics"


def fund_take_str() -> str:
    return "fund_take"


def fund_give_str() -> str:
    return "fund_give"


def get_fund_metric_config_filename() -> str:
    return "fund_metric_config.json"


def config_file_path() -> str:
    src_dir = create_path(os_getcwd(), "src")
    config_file_dir = create_path(src_dir, "f05_fund_metric")
    return create_path(config_file_dir, get_fund_metric_config_filename())


def get_fund_metric_config_dict() -> dict[str, dict]:
    return open_json(config_file_path())


def get_fund_metric_dimen_args(dimen: str) -> set:
    config_dict = get_fund_metric_config_dict()
    dimen_dict = config_dict.get(dimen)
    all_args = set(dimen_dict.get("jkeys").keys())
    all_args = all_args.union(set(dimen_dict.get("jvalues").keys()))
    all_args = all_args.union(set(dimen_dict.get("jmetrics").keys()))
    return all_args


def get_all_fund_metric_args() -> dict[str, set[str]]:
    fund_metric_config_dict = get_fund_metric_config_dict()
    all_args = {}
    for fund_metric_dimen, dimen_dict in fund_metric_config_dict.items():
        for dimen_key, arg_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg in arg_dict.keys():
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(fund_metric_dimen)
    return all_args


def get_fund_metric_args_type_dict() -> dict[str, str]:
    return {
        "acct_name": "NameUnit",
        "group_label": "LabelUnit",
        "_credor_pool": "float",
        "_debtor_pool": "float",
        "_fund_agenda_give": "float",
        "_fund_agenda_ratio_give": "float",
        "_fund_agenda_ratio_take": "float",
        "_fund_agenda_take": "float",
        "_fund_give": "float",
        "_fund_take": "float",
        "credit_vote": "int",
        "debtit_vote": "int",
        "_inallocable_debtit_belief": "float",
        "_irrational_debtit_belief": "float",
        "credit_belief": "float",
        "debtit_belief": "float",
        "item_title": "TitleUnit",
        "parent_road": "RoadUnit",
        "_fund_coin": "float",
        "addin": "float",
        "begin": "float",
        "close": "float",
        "denom": "int",
        "gogo_want": "float",
        "mass": "int",
        "morph": "bool",
        "numor": "int",
        "pledge": "bool",
        "problem_bool": "bool",
        "stop_want": "float",
        "awardee_tag": "LabelUnit",
        "road": "RoadUnit",
        "give_force": "float",
        "take_force": "float",
        "base": "RoadUnit",
        "fnigh": "float",
        "fopen": "float",
        "pick": "RoadUnit",
        "healer_name": "NameUnit",
        "need": "RoadUnit",
        "_status": "int",
        "_task": "int",
        "divisor": "int",
        "nigh": "float",
        "open": "float",
        "_base_item_active_value": "int",
        "base_item_active_requisite": "bool",
        "team_tag": "LabelUnit",
        "_owner_name_team": "int",
        "_active": "int",
        "_all_acct_cred": "int",
        "_all_acct_debt": "int",
        "_descendant_pledge_count": "int",
        "_fund_cease": "float",
        "_fund_onset": "float",
        "_fund_ratio": "float",
        "_gogo_calc": "float",
        "_healerlink_ratio": "float",
        "_level": "int",
        "_range_evaluated": "int",
        "_stop_calc": "float",
        "_keeps_buildable": "int",
        "_keeps_justified": "int",
        "_offtrack_fund": "int",
        "_rational": "bool",
        "_sum_healerlink_share": "float",
        "_tree_traverse_count": "int",
        "credor_respect": "float",
        "debtor_respect": "float",
        "fund_coin": "float",
        "fund_pool": "float",
        "max_tree_traverse": "int",
        "penny": "float",
        "respect_bit": "float",
        "tally": "int",
    }
