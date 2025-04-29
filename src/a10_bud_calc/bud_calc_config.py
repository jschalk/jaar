from src.a00_data_toolbox.file_toolbox import open_json, create_path
from os import getcwd as os_getcwd


def jmetrics_str() -> str:
    return "jmetrics"


def fund_take_str() -> str:
    return "fund_take"


def fund_give_str() -> str:
    return "fund_give"


def get_bud_calc_config_filename() -> str:
    return "bud_calc_config.json"


def config_file_path() -> str:
    src_dir = create_path(os_getcwd(), "src")
    config_file_dir = create_path(src_dir, "a10_bud_calc")
    return create_path(config_file_dir, get_bud_calc_config_filename())


def get_bud_calc_config_dict() -> dict[str, dict]:
    return open_json(config_file_path())


def get_bud_calc_dimen_args(dimen: str) -> set:
    config_dict = get_bud_calc_config_dict()
    dimen_dict = config_dict.get(dimen)
    all_args = set(dimen_dict.get("jkeys").keys())
    all_args = all_args.union(set(dimen_dict.get("jvalues").keys()))
    all_args = all_args.union(set(dimen_dict.get("jmetrics").keys()))
    return all_args


def get_all_bud_calc_args() -> dict[str, set[str]]:
    bud_calc_config_dict = get_bud_calc_config_dict()
    all_args = {}
    for bud_calc_dimen, dimen_dict in bud_calc_config_dict.items():
        for dimen_key, arg_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg in arg_dict.keys():
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(bud_calc_dimen)
    return all_args


def get_bud_calc_args_type_dict() -> dict[str, str]:
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
        "item_tag": "TagUnit",
        "parent_road": "RoadUnit",
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
        "awardee_title": "LabelUnit",
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
        "team_title": "LabelUnit",
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


def get_bud_calc_args_sqlite_datatype_dict() -> dict[str, str]:
    return {
        "acct_name": "TEXT",
        "group_label": "TEXT",
        "_credor_pool": "REAL",
        "_debtor_pool": "REAL",
        "_fund_agenda_give": "REAL",
        "_fund_agenda_ratio_give": "REAL",
        "_fund_agenda_ratio_take": "REAL",
        "_fund_agenda_take": "REAL",
        "_fund_give": "REAL",
        "_fund_take": "REAL",
        "credit_vote": "REAL",
        "debtit_vote": "REAL",
        "_inallocable_debtit_belief": "REAL",
        "_irrational_debtit_belief": "REAL",
        "credit_belief": "REAL",
        "debtit_belief": "REAL",
        "item_tag": "TEXT",
        "parent_road": "TEXT",
        "addin": "REAL",
        "begin": "REAL",
        "close": "REAL",
        "denom": "INTEGER",
        "gogo_want": "REAL",
        "mass": "INTEGER",
        "morph": "INTEGER",
        "numor": "INTEGER",
        "pledge": "INTEGER",
        "problem_bool": "INTEGER",
        "stop_want": "REAL",
        "awardee_title": "TEXT",
        "road": "TEXT",
        "give_force": "REAL",
        "take_force": "REAL",
        "base": "TEXT",
        "fisc_tag": "TEXT",
        "fnigh": "REAL",
        "fopen": "REAL",
        "pick": "TEXT",
        "healer_name": "TEXT",
        "need": "TEXT",
        "_status": "INTEGER",
        "_task": "INTEGER",
        "divisor": "INTEGER",
        "nigh": "REAL",
        "open": "REAL",
        "owner_name": "TEXT",
        "_base_item_active_value": "INTEGER",
        "base_item_active_requisite": "INTEGER",
        "team_title": "TEXT",
        "bridge": "TEXT",
        "_owner_name_team": "INTEGER",
        "_active": "INTEGER",
        "_all_acct_cred": "INTEGER",
        "_all_acct_debt": "INTEGER",
        "_descendant_pledge_count": "INTEGER",
        "_fund_cease": "REAL",
        "_fund_onset": "REAL",
        "_fund_ratio": "REAL",
        "_gogo_calc": "REAL",
        "_healerlink_ratio": "REAL",
        "_level": "INTEGER",
        "_range_evaluated": "INTEGER",
        "_stop_calc": "REAL",
        "_keeps_buildable": "INTEGER",
        "_keeps_justified": "INTEGER",
        "_offtrack_fund": "REAL",
        "_rational": "INTEGER",
        "_sum_healerlink_share": "REAL",
        "_tree_traverse_count": "INTEGER",
        "credor_respect": "REAL",
        "debtor_respect": "REAL",
        "fund_coin": "REAL",
        "fund_pool": "REAL",
        "max_tree_traverse": "INTEGER",
        "penny": "REAL",
        "respect_bit": "REAL",
        "tally": "INTEGER",
        "world_id": "TEXT",
    }


def get_bud_calc_dimens() -> dict[str, str]:
    return {
        "budunit",
        "bud_acctunit",
        "bud_acct_membership",
        "bud_itemunit",
        "bud_item_awardlink",
        "bud_item_reasonunit",
        "bud_item_reason_premiseunit",
        "bud_item_teamlink",
        "bud_item_healerlink",
        "bud_item_factunit",
        "bud_groupunit",
    }
