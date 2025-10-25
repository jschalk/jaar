from os import getcwd as os_getcwd
from src.ch01_py.file_toolbox import create_path, open_json


def max_tree_traverse_default() -> int:
    return 20


def belief_config_path() -> str:
    """src/ch07_belief_logic/belief_config.json"""
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch07_belief_logic")
    return create_path(chapter_dir, "belief_config.json")


def get_belief_config_dict() -> dict[str, dict]:
    return open_json(belief_config_path())


def get_belief_calc_dimen_args(dimen: str) -> set:
    config_dict = get_belief_config_dict()
    dimen_dict = config_dict.get(dimen)
    all_args = set(dimen_dict.get("jkeys").keys())
    all_args = all_args.union(set(dimen_dict.get("jvalues").keys()))
    return all_args


def get_all_belief_calc_args() -> dict[str, set[str]]:
    belief_config_dict = get_belief_config_dict()
    all_args = {}
    for belief_calc_dimen, dimen_dict in belief_config_dict.items():
        for dimen_key, arg_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg in arg_dict.keys():
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(belief_calc_dimen)
    return all_args


def get_belief_calc_args_type_dict() -> dict[str, str]:
    return {
        "case_active": "int",
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
        "group_cred_lumen": "int",
        "group_debt_lumen": "int",
        "inallocable_voice_debt_lumen": "float",
        "irrational_voice_debt_lumen": "float",
        "voice_cred_lumen": "float",
        "voice_debt_lumen": "float",
        "addin": "float",
        "begin": "float",
        "close": "float",
        "denom": "int",
        "gogo_want": "float",
        "star": "int",
        "morph": "bool",
        "numor": "int",
        "pledge": "bool",
        "problem_bool": "bool",
        "stop_want": "float",
        "awardee_title": "TitleTerm",
        "plan_rope": "RopeTerm",
        "give_force": "float",
        "take_force": "float",
        "reason_context": "RopeTerm",
        "fact_upper": "ContextNum",
        "fact_lower": "ContextNum",
        "fact_state": "RopeTerm",
        "healer_name": "NameTerm",
        "reason_state": "RopeTerm",
        "reason_active": "int",
        "task": "int",
        "reason_divisor": "int",
        "reason_upper": "ContextNum",
        "reason_lower": "ContextNum",
        "parent_heir_active": "int",
        "active_requisite": "bool",
        "party_title": "TitleTerm",
        "belief_name_is_labor": "int",
        "plan_active": "int",
        "all_voice_cred": "int",
        "all_voice_debt": "int",
        "descendant_pledge_count": "int",
        "fund_cease": "float",
        "fund_onset": "float",
        "fund_ratio": "float",
        "gogo_calc": "float",
        "healerunit_ratio": "float",
        "tree_level": "int",
        "range_evaluated": "int",
        "stop_calc": "float",
        "keeps_buildable": "int",
        "keeps_justified": "int",
        "offtrack_fund": "int",
        "rational": "bool",
        "sum_healerunit_plans_fund_total": "float",
        "tree_traverse_count": "int",
        "credor_respect": "float",
        "debtor_respect": "float",
        "fund_grain": "float",
        "fund_pool": "float",
        "max_tree_traverse": "int",
        "mana_grain": "float",
        "respect_grain": "float",
        "tally": "int",
    }


def get_belief_calc_args_sqlite_datatype_dict() -> dict[str, str]:
    return {
        "case_active": "INTEGER",
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
        "group_cred_lumen": "REAL",
        "group_debt_lumen": "REAL",
        "groupmark": "TEXT",
        "inallocable_voice_debt_lumen": "REAL",
        "irrational_voice_debt_lumen": "REAL",
        "voice_cred_lumen": "REAL",
        "voice_debt_lumen": "REAL",
        "addin": "REAL",
        "begin": "REAL",
        "close": "REAL",
        "denom": "INTEGER",
        "gogo_want": "REAL",
        "star": "INTEGER",
        "morph": "INTEGER",
        "numor": "INTEGER",
        "pledge": "INTEGER",
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
        "reason_active": "INTEGER",
        "task": "INTEGER",
        "reason_divisor": "INTEGER",
        "reason_upper": "REAL",
        "reason_lower": "REAL",
        "belief_name": "TEXT",
        "parent_heir_active": "INTEGER",
        "active_requisite": "INTEGER",
        "party_title": "TEXT",
        "knot": "TEXT",
        "belief_name_is_labor": "INTEGER",
        "plan_active": "INTEGER",
        "all_voice_cred": "INTEGER",
        "all_voice_debt": "INTEGER",
        "descendant_pledge_count": "INTEGER",
        "fund_cease": "REAL",
        "fund_onset": "REAL",
        "fund_ratio": "REAL",
        "gogo_calc": "REAL",
        "healerunit_ratio": "REAL",
        "tree_level": "INTEGER",
        "range_evaluated": "INTEGER",
        "stop_calc": "REAL",
        "keeps_buildable": "INTEGER",
        "keeps_justified": "INTEGER",
        "offtrack_fund": "REAL",
        "rational": "INTEGER",
        "sum_healerunit_plans_fund_total": "REAL",
        "tree_traverse_count": "INTEGER",
        "credor_respect": "REAL",
        "debtor_respect": "REAL",
        "fund_grain": "REAL",
        "fund_pool": "REAL",
        "max_tree_traverse": "INTEGER",
        "mana_grain": "REAL",
        "respect_grain": "REAL",
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
