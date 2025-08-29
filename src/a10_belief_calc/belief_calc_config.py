from os import getcwd as os_getcwd
from src.a00_data_toolbox.file_toolbox import create_path, open_json


def belief_calc_config_path() -> str:
    """src/belief_calc_module/belief_calc_config.json"""
    src_dir = create_path(os_getcwd(), "src")
    module_dir = create_path(src_dir, "a10_belief_calc")
    return create_path(module_dir, "belief_calc_config.json")


def get_belief_calc_config_dict() -> dict[str, dict]:
    return open_json(belief_calc_config_path())


def get_belief_calc_dimen_args(dimen: str) -> set:
    config_dict = get_belief_calc_config_dict()
    dimen_dict = config_dict.get(dimen)
    all_args = set(dimen_dict.get("jkeys").keys())
    all_args = all_args.union(set(dimen_dict.get("jvalues").keys()))
    all_args = all_args.union(set(dimen_dict.get("jmetrics").keys()))
    return all_args


def get_all_belief_calc_args() -> dict[str, set[str]]:
    belief_calc_config_dict = get_belief_calc_config_dict()
    all_args = {}
    for belief_calc_dimen, dimen_dict in belief_calc_config_dict.items():
        for dimen_key, arg_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg in arg_dict.keys():
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(belief_calc_dimen)
    return all_args


def get_belief_calc_args_type_dict() -> dict[str, str]:
    return {
        "voice_name": "NameTerm",
        "group_title": "TitleTerm",
        "credor_pool": "float",
        "debtor_pool": "float",
        "fund_agenda_give": "float",
        "fund_agenda_ratio_give": "float",
        "fund_agenda_ratio_take": "float",
        "fund_agenda_take": "float",
        "fund_give": "float",
        "fund_take": "float",
        "group_cred_points": "int",
        "group_debt_points": "int",
        "inallocable_voice_debt_points": "float",
        "irrational_voice_debt_points": "float",
        "voice_cred_points": "float",
        "voice_debt_points": "float",
        "addin": "float",
        "begin": "float",
        "close": "float",
        "denom": "int",
        "gogo_want": "float",
        "star": "int",
        "morph": "bool",
        "numor": "int",
        "task": "bool",
        "problem_bool": "bool",
        "stop_want": "float",
        "awardee_title": "TitleTerm",
        "plan_rope": "RopeTerm",
        "give_force": "float",
        "take_force": "float",
        "reason_context": "RopeTerm",
        "fact_upper": "float",
        "fact_lower": "float",
        "fact_state": "RopeTerm",
        "healer_name": "NameTerm",
        "reason_state": "RopeTerm",
        "status": "int",
        "chore": "int",
        "reason_divisor": "int",
        "reason_upper": "float",
        "reason_lower": "float",
        "_reason_active_heir": "int",
        "reason_active_requisite": "bool",
        "party_title": "TitleTerm",
        "_belief_name_is_labor": "int",
        "active": "int",
        "all_voice_cred": "int",
        "all_voice_debt": "int",
        "descendant_task_count": "int",
        "fund_cease": "float",
        "fund_onset": "float",
        "fund_ratio": "float",
        "gogo_calc": "float",
        "healerunit_ratio": "float",
        "level": "int",
        "range_evaluated": "int",
        "stop_calc": "float",
        "keeps_buildable": "int",
        "keeps_justified": "int",
        "offtrack_fund": "int",
        "rational": "bool",
        "sum_healerunit_share": "float",
        "tree_traverse_count": "int",
        "credor_respect": "float",
        "debtor_respect": "float",
        "fund_iota": "float",
        "fund_pool": "float",
        "max_tree_traverse": "int",
        "penny": "float",
        "respect_bit": "float",
        "tally": "int",
    }


def get_belief_calc_args_sqlite_datatype_dict() -> dict[str, str]:
    return {
        "voice_name": "TEXT",
        "group_title": "TEXT",
        "credor_pool": "REAL",
        "debtor_pool": "REAL",
        "fund_agenda_give": "REAL",
        "fund_agenda_ratio_give": "REAL",
        "fund_agenda_ratio_take": "REAL",
        "fund_agenda_take": "REAL",
        "fund_give": "REAL",
        "fund_take": "REAL",
        "group_cred_points": "REAL",
        "group_debt_points": "REAL",
        "inallocable_voice_debt_points": "REAL",
        "irrational_voice_debt_points": "REAL",
        "voice_cred_points": "REAL",
        "voice_debt_points": "REAL",
        "addin": "REAL",
        "begin": "REAL",
        "close": "REAL",
        "denom": "INTEGER",
        "gogo_want": "REAL",
        "star": "INTEGER",
        "morph": "INTEGER",
        "numor": "INTEGER",
        "task": "INTEGER",
        "problem_bool": "INTEGER",
        "stop_want": "REAL",
        "awardee_title": "TEXT",
        "plan_rope": "TEXT",
        "give_force": "REAL",
        "take_force": "REAL",
        "reason_context": "TEXT",
        "moment_label": "TEXT",
        "fact_context": "TEXT",
        "fact_state": "TEXT",
        "fact_upper": "REAL",
        "fact_lower": "REAL",
        "healer_name": "TEXT",
        "reason_state": "TEXT",
        "status": "INTEGER",
        "chore": "INTEGER",
        "reason_divisor": "INTEGER",
        "reason_upper": "REAL",
        "reason_lower": "REAL",
        "belief_name": "TEXT",
        "_reason_active_heir": "INTEGER",
        "reason_active_requisite": "INTEGER",
        "party_title": "TEXT",
        "knot": "TEXT",
        "_belief_name_is_labor": "INTEGER",
        "active": "INTEGER",
        "all_voice_cred": "INTEGER",
        "all_voice_debt": "INTEGER",
        "descendant_task_count": "INTEGER",
        "fund_cease": "REAL",
        "fund_onset": "REAL",
        "fund_ratio": "REAL",
        "gogo_calc": "REAL",
        "healerunit_ratio": "REAL",
        "level": "INTEGER",
        "range_evaluated": "INTEGER",
        "stop_calc": "REAL",
        "keeps_buildable": "INTEGER",
        "keeps_justified": "INTEGER",
        "offtrack_fund": "REAL",
        "rational": "INTEGER",
        "sum_healerunit_share": "REAL",
        "tree_traverse_count": "INTEGER",
        "credor_respect": "REAL",
        "debtor_respect": "REAL",
        "fund_iota": "REAL",
        "fund_pool": "REAL",
        "max_tree_traverse": "INTEGER",
        "penny": "REAL",
        "respect_bit": "REAL",
        "solo": "INTEGER",
        "tally": "INTEGER",
    }


def get_belief_calc_dimens() -> dict[str, str]:
    return {
        "beliefunit",
        "belief_voiceunit",
        "belief_voice_membership",
        "belief_planunit",
        "belief_plan_awardunit",
        "belief_plan_reasonunit",
        "belief_plan_reason_caseunit",
        "belief_plan_partyunit",
        "belief_plan_healerunit",
        "belief_plan_factunit",
        "belief_groupunit",
    }
