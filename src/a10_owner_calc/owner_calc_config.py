from os import getcwd as os_getcwd
from src.a00_data_toolbox.file_toolbox import create_path, open_json


def get_owner_calc_config_filename() -> str:
    return "owner_calc_config.json"


def config_owner_calc_file_path() -> str:
    """src/owner_calc_module/owner_calc_config.json"""
    src_dir = create_path(os_getcwd(), "src")
    config_file_dir = create_path(src_dir, "a10_owner_calc")
    return create_path(config_file_dir, get_owner_calc_config_filename())


def get_owner_calc_config_dict() -> dict[str, dict]:
    return open_json(config_owner_calc_file_path())


def get_owner_calc_dimen_args(dimen: str) -> set:
    config_dict = get_owner_calc_config_dict()
    dimen_dict = config_dict.get(dimen)
    all_args = set(dimen_dict.get("jkeys").keys())
    all_args = all_args.union(set(dimen_dict.get("jvalues").keys()))
    all_args = all_args.union(set(dimen_dict.get("jmetrics").keys()))
    return all_args


def get_all_owner_calc_args() -> dict[str, set[str]]:
    owner_calc_config_dict = get_owner_calc_config_dict()
    all_args = {}
    for owner_calc_dimen, dimen_dict in owner_calc_config_dict.items():
        for dimen_key, arg_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg in arg_dict.keys():
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(owner_calc_dimen)
    return all_args


def get_owner_calc_args_type_dict() -> dict[str, str]:
    return {
        "acct_name": "NameTerm",
        "group_title": "TitleTerm",
        "_credor_pool": "float",
        "_debtor_pool": "float",
        "_fund_agenda_give": "float",
        "_fund_agenda_ratio_give": "float",
        "_fund_agenda_ratio_take": "float",
        "_fund_agenda_take": "float",
        "_fund_give": "float",
        "_fund_take": "float",
        "group_cred_points": "int",
        "group_debt_points": "int",
        "_inallocable_acct_debt_points": "float",
        "_irrational_acct_debt_points": "float",
        "acct_cred_points": "float",
        "acct_debt_points": "float",
        "addin": "float",
        "begin": "float",
        "close": "float",
        "denom": "int",
        "gogo_want": "float",
        "mass": "int",
        "morph": "bool",
        "numor": "int",
        "task": "bool",
        "problem_bool": "bool",
        "stop_want": "float",
        "awardee_title": "TitleTerm",
        "plan_rope": "RopeTerm",
        "give_force": "float",
        "take_force": "float",
        "rcontext": "RopeTerm",
        "fnigh": "float",
        "fopen": "float",
        "fstate": "RopeTerm",
        "healer_name": "NameTerm",
        "pstate": "RopeTerm",
        "_status": "int",
        "_chore": "int",
        "pdivisor": "int",
        "pnigh": "float",
        "popen": "float",
        "_rplan_active_value": "int",
        "rplan_active_requisite": "bool",
        "labor_title": "TitleTerm",
        "_owner_name_labor": "int",
        "_active": "int",
        "_all_acct_cred": "int",
        "_all_acct_debt": "int",
        "_descendant_task_count": "int",
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
        "fund_iota": "float",
        "fund_pool": "float",
        "max_tree_traverse": "int",
        "penny": "float",
        "respect_bit": "float",
        "tally": "int",
    }


def get_owner_calc_args_sqlite_datatype_dict() -> dict[str, str]:
    return {
        "acct_name": "TEXT",
        "group_title": "TEXT",
        "_credor_pool": "REAL",
        "_debtor_pool": "REAL",
        "_fund_agenda_give": "REAL",
        "_fund_agenda_ratio_give": "REAL",
        "_fund_agenda_ratio_take": "REAL",
        "_fund_agenda_take": "REAL",
        "_fund_give": "REAL",
        "_fund_take": "REAL",
        "group_cred_points": "REAL",
        "group_debt_points": "REAL",
        "_inallocable_acct_debt_points": "REAL",
        "_irrational_acct_debt_points": "REAL",
        "acct_cred_points": "REAL",
        "acct_debt_points": "REAL",
        "addin": "REAL",
        "begin": "REAL",
        "close": "REAL",
        "denom": "INTEGER",
        "gogo_want": "REAL",
        "mass": "INTEGER",
        "morph": "INTEGER",
        "numor": "INTEGER",
        "task": "INTEGER",
        "problem_bool": "INTEGER",
        "stop_want": "REAL",
        "awardee_title": "TEXT",
        "plan_rope": "TEXT",
        "give_force": "REAL",
        "take_force": "REAL",
        "rcontext": "TEXT",
        "belief_label": "TEXT",
        "fcontext": "TEXT",
        "fstate": "TEXT",
        "fnigh": "REAL",
        "fopen": "REAL",
        "healer_name": "TEXT",
        "pstate": "TEXT",
        "_status": "INTEGER",
        "_chore": "INTEGER",
        "pdivisor": "INTEGER",
        "pnigh": "REAL",
        "popen": "REAL",
        "owner_name": "TEXT",
        "_rplan_active_value": "INTEGER",
        "rplan_active_requisite": "INTEGER",
        "labor_title": "TEXT",
        "knot": "TEXT",
        "_owner_name_labor": "INTEGER",
        "_active": "INTEGER",
        "_all_acct_cred": "INTEGER",
        "_all_acct_debt": "INTEGER",
        "_descendant_task_count": "INTEGER",
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
        "fund_iota": "REAL",
        "fund_pool": "REAL",
        "max_tree_traverse": "INTEGER",
        "penny": "REAL",
        "respect_bit": "REAL",
        "tally": "INTEGER",
    }


def get_owner_calc_dimens() -> dict[str, str]:
    return {
        "ownerunit",
        "owner_acctunit",
        "owner_acct_membership",
        "owner_planunit",
        "owner_plan_awardlink",
        "owner_plan_reasonunit",
        "owner_plan_reason_premiseunit",
        "owner_plan_laborlink",
        "owner_plan_healerlink",
        "owner_plan_factunit",
        "owner_groupunit",
    }
