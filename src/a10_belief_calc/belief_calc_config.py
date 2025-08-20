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
        "partner_name": "NameTerm",
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
        "_inallocable_partner_debt_points": "float",
        "_irrational_partner_debt_points": "float",
        "partner_cred_points": "float",
        "partner_debt_points": "float",
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
        "_status": "int",
        "_chore": "int",
        "reason_divisor": "int",
        "reason_upper": "float",
        "reason_lower": "float",
        "_rplan_active_value": "int",
        "reason_active_requisite": "bool",
        "party_title": "TitleTerm",
        "_belief_name_is_labor": "int",
        "_active": "int",
        "_all_partner_cred": "int",
        "_all_partner_debt": "int",
        "_descendant_task_count": "int",
        "_fund_cease": "float",
        "_fund_onset": "float",
        "_fund_ratio": "float",
        "_gogo_calc": "float",
        "_healerunit_ratio": "float",
        "_level": "int",
        "_range_evaluated": "int",
        "_stop_calc": "float",
        "_keeps_buildable": "int",
        "_keeps_justified": "int",
        "_offtrack_fund": "int",
        "_rational": "bool",
        "_sum_healerunit_share": "float",
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


def get_belief_calc_args_sqlite_datatype_dict() -> dict[str, str]:
    return {
        "partner_name": "TEXT",
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
        "_inallocable_partner_debt_points": "REAL",
        "_irrational_partner_debt_points": "REAL",
        "partner_cred_points": "REAL",
        "partner_debt_points": "REAL",
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
        "coin_label": "TEXT",
        "fact_context": "TEXT",
        "fact_state": "TEXT",
        "fact_upper": "REAL",
        "fact_lower": "REAL",
        "healer_name": "TEXT",
        "reason_state": "TEXT",
        "_status": "INTEGER",
        "_chore": "INTEGER",
        "reason_divisor": "INTEGER",
        "reason_upper": "REAL",
        "reason_lower": "REAL",
        "belief_name": "TEXT",
        "_rplan_active_value": "INTEGER",
        "reason_active_requisite": "INTEGER",
        "party_title": "TEXT",
        "knot": "TEXT",
        "_belief_name_is_labor": "INTEGER",
        "_active": "INTEGER",
        "_all_partner_cred": "INTEGER",
        "_all_partner_debt": "INTEGER",
        "_descendant_task_count": "INTEGER",
        "_fund_cease": "REAL",
        "_fund_onset": "REAL",
        "_fund_ratio": "REAL",
        "_gogo_calc": "REAL",
        "_healerunit_ratio": "REAL",
        "_level": "INTEGER",
        "_range_evaluated": "INTEGER",
        "_stop_calc": "REAL",
        "_keeps_buildable": "INTEGER",
        "_keeps_justified": "INTEGER",
        "_offtrack_fund": "REAL",
        "_rational": "INTEGER",
        "_sum_healerunit_share": "REAL",
        "_tree_traverse_count": "INTEGER",
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
        "belief_partnerunit",
        "belief_partner_membership",
        "belief_planunit",
        "belief_plan_awardunit",
        "belief_plan_reasonunit",
        "belief_plan_reason_caseunit",
        "belief_plan_partyunit",
        "belief_plan_healerunit",
        "belief_plan_factunit",
        "belief_groupunit",
    }
