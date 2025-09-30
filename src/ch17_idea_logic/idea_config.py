from os import getcwd as os_getcwd
from src.ch01_data_toolbox.db_toolbox import get_sorted_cols_only_list
from src.ch01_data_toolbox.file_toolbox import create_path, get_json_filename, open_json


def idea_config_path() -> str:
    "Returns path: a17_idea_logic/idea_config.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch17_idea_logic")
    return create_path(chapter_dir, "idea_config.json")


def get_idea_config_dict() -> dict:
    "Returns path: a17_idea_logic/idea_config.json"
    return open_json(idea_config_path())


def get_allowed_curds() -> set[str]:
    return {
        "insert_one_time",
        "insert_multiple",
        "delete_insert_update",
        "insert_update",
        "delete_insert",
        "delete_update",
        "UPDATE",
        "DELETE",
        "INSERT",
    }


def get_idea_formats_dir() -> str:
    idea_dir = create_path("src", "ch17_idea_logic")
    # return create_path(idea_dir, "idea_formats")
    return "src/ch17_idea_logic/idea_formats"


def get_idea_elements_sort_order() -> list[str]:
    """Contains the standard sort order for all idea and belief_calc columns"""
    return [
        "world_name",
        "idea_number",
        "source_dimen",
        "translate_event_int",
        "event_int",
        "face_name",
        "face_name_otx",
        "face_name_inx",
        "moment_label",
        "moment_label_otx",
        "moment_label_inx",
        "timeline_label",
        "timeline_label_otx",
        "timeline_label_inx",
        "offi_time",
        "c400_number",
        "yr1_jan1_offset",
        "monthday_index",
        "cumulative_day",
        "month_label",
        "month_label_otx",
        "month_label_inx",
        "cumulative_minute",
        "hour_label",
        "hour_label_otx",
        "hour_label_inx",
        "weekday_order",
        "weekday_label",
        "weekday_label_otx",
        "weekday_label_inx",
        "belief_name",
        "belief_name_otx",
        "belief_name_inx",
        "belief_name_ERASE",
        "belief_name_ERASE_otx",
        "belief_name_ERASE_inx",
        "voice_name",
        "voice_name_otx",
        "voice_name_inx",
        "voice_name_ERASE",
        "voice_name_ERASE_otx",
        "voice_name_ERASE_inx",
        "group_title",
        "group_title_otx",
        "group_title_inx",
        "group_title_ERASE",
        "group_title_ERASE_otx",
        "group_title_ERASE_inx",
        "plan_rope",
        "plan_rope_otx",
        "plan_rope_inx",
        "plan_rope_ERASE",
        "plan_rope_ERASE_otx",
        "plan_rope_ERASE_inx",
        "reason_context",
        "reason_context_otx",
        "reason_context_inx",
        "reason_context_ERASE",
        "reason_context_ERASE_otx",
        "reason_context_ERASE_inx",
        "fact_context",
        "fact_context_otx",
        "fact_context_inx",
        "fact_context_ERASE",
        "fact_context_ERASE_otx",
        "fact_context_ERASE_inx",
        "reason_state",
        "reason_state_otx",
        "reason_state_inx",
        "reason_state_ERASE",
        "reason_state_ERASE_otx",
        "reason_state_ERASE_inx",
        "fact_state",
        "fact_state_otx",
        "fact_state_inx",
        "party_title",
        "party_title_otx",
        "party_title_inx",
        "party_title_ERASE",
        "party_title_ERASE_otx",
        "party_title_ERASE_inx",
        "solo",
        "awardee_title",
        "awardee_title_otx",
        "awardee_title_inx",
        "awardee_title_ERASE",
        "awardee_title_ERASE_otx",
        "awardee_title_ERASE_inx",
        "healer_name",
        "healer_name_otx",
        "healer_name_inx",
        "healer_name_ERASE",
        "healer_name_ERASE_otx",
        "healer_name_ERASE_inx",
        "bud_time",
        "tran_time",
        "begin",
        "close",
        "addin",
        "numor",
        "denom",
        "morph",
        "gogo_want",
        "stop_want",
        "reason_active_requisite",
        "voice_cred_points",
        "voice_debt_points",
        "group_cred_points",
        "group_debt_points",
        "credor_respect",
        "debtor_respect",
        "fact_lower",
        "fact_upper",
        "fund_pool",
        "give_force",
        "star",
        "max_tree_traverse",
        "reason_upper",
        "reason_lower",
        "reason_divisor",
        "pledge",
        "problem_bool",
        "take_force",
        "tally",
        "fund_iota",
        "penny",
        "respect_bit",
        "amount",
        "otx_label",
        "inx_label",
        "otx_rope",
        "inx_rope",
        "otx_name",
        "inx_name",
        "otx_title",
        "inx_title",
        "otx_knot",
        "inx_knot",
        "knot",
        "unknown_str",
        "quota",
        "celldepth",
        "job_listen_rotations",
        "error_message",
        "_belief_name_is_labor",
        "active",
        "task",
        "status",
        "credor_pool",
        "debtor_pool",
        "rational",
        "fund_give",
        "fund_take",
        "fund_onset",
        "fund_cease",
        "fund_ratio",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
        "inallocable_voice_debt_points",
        "gogo_calc",
        "stop_calc",
        "tree_level",
        "range_evaluated",
        "descendant_pledge_count",
        "healerunit_ratio",
        "all_voice_cred",
        "keeps_justified",
        "offtrack_fund",
        "_reason_active_heir",
        "irrational_voice_debt_points",
        "sum_healerunit_share",
        "keeps_buildable",
        "all_voice_debt",
        "tree_traverse_count",
        "funds",
        "fund_rank",
        "pledges_count",
    ]


def get_default_sorted_list(
    existing_columns: set[str], sorting_columns: list[str] = None
) -> list[str]:
    if sorting_columns is None:
        sorting_columns = get_idea_elements_sort_order()
    return get_sorted_cols_only_list(existing_columns, sorting_columns)


def get_idea_sqlite_types() -> dict[str, str]:
    """Returns dictionary of sqlite_type for all idea elements (reference source: get_idea_elements_sort_order)"""

    return {
        "world_name": "TEXT",
        "idea_number": "TEXT",
        "face_name": "TEXT",
        "face_name_otx": "TEXT",
        "face_name_inx": "TEXT",
        "source_dimen": "TEXT",
        "translate_event_int": "INTEGER",
        "event_int": "INTEGER",
        "moment_label": "TEXT",
        "moment_label_otx": "TEXT",
        "moment_label_inx": "TEXT",
        "belief_name": "TEXT",
        "belief_name_otx": "TEXT",
        "belief_name_inx": "TEXT",
        "belief_name_ERASE": "TEXT",
        "belief_name_ERASE_otx": "TEXT",
        "belief_name_ERASE_inx": "TEXT",
        "voice_name": "TEXT",
        "voice_name_otx": "TEXT",
        "voice_name_inx": "TEXT",
        "voice_name_ERASE": "TEXT",
        "voice_name_ERASE_otx": "TEXT",
        "voice_name_ERASE_inx": "TEXT",
        "group_title": "TEXT",
        "group_title_otx": "TEXT",
        "group_title_inx": "TEXT",
        "group_title_ERASE": "TEXT",
        "group_title_ERASE_otx": "TEXT",
        "group_title_ERASE_inx": "TEXT",
        "plan_rope": "TEXT",
        "plan_rope_otx": "TEXT",
        "plan_rope_inx": "TEXT",
        "plan_rope_ERASE": "TEXT",
        "plan_rope_ERASE_otx": "TEXT",
        "plan_rope_ERASE_inx": "TEXT",
        "reason_context": "TEXT",
        "reason_context_otx": "TEXT",
        "reason_context_inx": "TEXT",
        "reason_context_ERASE": "TEXT",
        "reason_context_ERASE_otx": "TEXT",
        "reason_context_ERASE_inx": "TEXT",
        "fact_context": "TEXT",
        "fact_context_otx": "TEXT",
        "fact_context_inx": "TEXT",
        "fact_context_ERASE": "TEXT",
        "fact_context_ERASE_otx": "TEXT",
        "fact_context_ERASE_inx": "TEXT",
        "reason_state": "TEXT",
        "reason_state_otx": "TEXT",
        "reason_state_inx": "TEXT",
        "reason_state_ERASE": "TEXT",
        "reason_state_ERASE_otx": "TEXT",
        "reason_state_ERASE_inx": "TEXT",
        "fact_state": "TEXT",
        "fact_state_otx": "TEXT",
        "fact_state_inx": "TEXT",
        "party_title": "TEXT",
        "party_title_otx": "TEXT",
        "party_title_inx": "TEXT",
        "party_title_ERASE": "TEXT",
        "party_title_ERASE_otx": "TEXT",
        "party_title_ERASE_inx": "TEXT",
        "solo": "INTEGER",
        "awardee_title": "TEXT",
        "awardee_title_otx": "TEXT",
        "awardee_title_inx": "TEXT",
        "awardee_title_ERASE": "TEXT",
        "awardee_title_ERASE_otx": "TEXT",
        "awardee_title_ERASE_inx": "TEXT",
        "healer_name": "TEXT",
        "healer_name_otx": "TEXT",
        "healer_name_inx": "TEXT",
        "healer_name_ERASE": "TEXT",
        "healer_name_ERASE_otx": "TEXT",
        "healer_name_ERASE_inx": "TEXT",
        "bud_time": "INTEGER",
        "tran_time": "INTEGER",
        "offi_time": "INTEGER",
        "begin": "REAL",
        "close": "REAL",
        "addin": "REAL",
        "numor": "INTEGER",
        "denom": "INTEGER",
        "morph": "INTEGER",
        "gogo_want": "REAL",
        "stop_want": "REAL",
        "reason_active_requisite": "INTEGER",
        "voice_cred_points": "REAL",
        "voice_debt_points": "REAL",
        "group_cred_points": "REAL",
        "group_debt_points": "REAL",
        "credor_respect": "REAL",
        "debtor_respect": "REAL",
        "fact_lower": "REAL",
        "fact_upper": "REAL",
        "fund_pool": "REAL",
        "give_force": "REAL",
        "star": "INTEGER",
        "max_tree_traverse": "INTEGER",
        "reason_upper": "REAL",
        "reason_lower": "REAL",
        "reason_divisor": "INTEGER",
        "pledge": "INTEGER",
        "problem_bool": "INTEGER",
        "take_force": "REAL",
        "tally": "INTEGER",
        "penny": "REAL",
        "respect_bit": "REAL",
        "amount": "REAL",
        "month_label": "TEXT",
        "month_label_otx": "TEXT",
        "month_label_inx": "TEXT",
        "hour_label": "TEXT",
        "hour_label_otx": "TEXT",
        "hour_label_inx": "TEXT",
        "cumulative_minute": "INTEGER",
        "cumulative_day": "INTEGER",
        "weekday_label": "TEXT",
        "weekday_label_otx": "TEXT",
        "weekday_label_inx": "TEXT",
        "weekday_order": "INTEGER",
        "otx_knot": "TEXT",
        "inx_knot": "TEXT",
        "unknown_str": "TEXT",
        "otx_label": "TEXT",
        "inx_label": "TEXT",
        "otx_rope": "TEXT",
        "inx_rope": "TEXT",
        "otx_name": "TEXT",
        "inx_name": "TEXT",
        "otx_title": "TEXT",
        "inx_title": "TEXT",
        "knot": "TEXT",
        "c400_number": "INTEGER",
        "yr1_jan1_offset": "INTEGER",
        "quota": "REAL",
        "celldepth": "INTEGER",
        "monthday_index": "INTEGER",
        "job_listen_rotations": "INTEGER",
        "timeline_label": "TEXT",
        "timeline_label_otx": "TEXT",
        "timeline_label_inx": "TEXT",
        "error_message": "TEXT",
        "credor_pool": "REAL",
        "debtor_pool": "REAL",
        "fund_cease": "REAL",
        "fund_onset": "REAL",
        "fund_ratio": "REAL",
        "fund_iota": "REAL",
        "fund_agenda_give": "REAL",
        "fund_agenda_ratio_give": "REAL",
        "fund_agenda_ratio_take": "REAL",
        "fund_agenda_take": "REAL",
        "fund_give": "REAL",
        "fund_take": "REAL",
        "gogo_calc": "REAL",
        "stop_calc": "REAL",
        "all_voice_cred": "INTEGER",
        "all_voice_debt": "INTEGER",
        "_reason_active_heir": "INTEGER",
        "inallocable_voice_debt_points": "REAL",
        "irrational_voice_debt_points": "REAL",
        "status": "INTEGER",
        "task": "INTEGER",
        "_belief_name_is_labor": "INTEGER",
        "active": "INTEGER",
        "descendant_pledge_count": "INTEGER",
        "healerunit_ratio": "REAL",
        "tree_level": "INTEGER",
        "range_evaluated": "INTEGER",
        "keeps_buildable": "INTEGER",
        "keeps_justified": "INTEGER",
        "offtrack_fund": "REAL",
        "rational": "INTEGER",
        "sum_healerunit_share": "REAL",
        "tree_traverse_count": "INTEGER",
        "funds": "REAL",
        "fund_rank": "INTEGER",
        "pledges_count": "INTEGER",
    }


# def idea_format_00000_momentunit_v0_0_0()->str: return "idea_format_00000_momentunit_v0_0_0"
# def idea_format_00001_moment_budunit_v0_0_0()->str: return "idea_format_00001_moment_budunit_v0_0_0"
# def idea_format_00002_moment_paybook_v0_0_0()->str: return "idea_format_00002_moment_paybook_v0_0_0"
# def idea_format_00003_moment_timeline_hour_v0_0_0()->str: return "idea_format_00003_moment_timeline_hour_v0_0_0"
# def idea_format_00004_moment_timeline_month_v0_0_0()->str: return "idea_format_00004_moment_timeline_month_v0_0_0"
# def idea_format_00005_moment_timeline_weekday_v0_0_0()->str: return "idea_format_00005_moment_timeline_weekday_v0_0_0"


def idea_format_00000_momentunit_v0_0_0() -> str:
    return "idea_format_00000_momentunit_v0_0_0"


def idea_format_00001_moment_budunit_v0_0_0() -> str:
    return "idea_format_00001_moment_budunit_v0_0_0"


def idea_format_00002_moment_paybook_v0_0_0() -> str:
    return "idea_format_00002_moment_paybook_v0_0_0"


def idea_format_00003_moment_timeline_hour_v0_0_0() -> str:
    return "idea_format_00003_moment_timeline_hour_v0_0_0"


def idea_format_00004_moment_timeline_month_v0_0_0() -> str:
    return "idea_format_00004_moment_timeline_month_v0_0_0"


def idea_format_00005_moment_timeline_weekday_v0_0_0() -> str:
    return "idea_format_00005_moment_timeline_weekday_v0_0_0"


def idea_format_00006_moment_timeoffi_v0_0_0() -> str:
    return "idea_format_00006_moment_timeoffi_v0_0_0"


def idea_format_00011_voice_v0_0_0() -> str:
    return "idea_format_00011_voice_v0_0_0"


def idea_format_00012_membership_v0_0_0() -> str:
    return "idea_format_00012_membership_v0_0_0"


def idea_format_00013_planunit_v0_0_0() -> str:
    return "idea_format_00013_planunit_v0_0_0"


def idea_format_00019_planunit_v0_0_0() -> str:
    return "idea_format_00019_planunit_v0_0_0"


# def idea_format_00020_belief_voice_membership_v0_0_0()-> str: return "idea_format_00020_belief_voice_membership_v0_0_0"
# def idea_format_00021_belief_voiceunit_v0_0_0()-> str: return "idea_format_00021_belief_voiceunit_v0_0_0"
# def idea_format_00022_belief_plan_awardunit_v0_0_0()-> str: return "idea_format_00022_belief_plan_awardunit_v0_0_0"
# def idea_format_00023_belief_plan_factunit_v0_0_0()-> str: return "idea_format_00023_belief_plan_factunit_v0_0_0"
# def idea_format_00024_belief_plan_partyunit_v0_0_0()-> str: return "idea_format_00024_belief_plan_partyunit_v0_0_0"
# def idea_format_00025_belief_plan_healerunit_v0_0_0()-> str: return "idea_format_00025_belief_plan_healerunit_v0_0_0"
# def idea_format_00026_belief_plan_reason_caseunit_v0_0_0()-> str: return "idea_format_00026_belief_plan_reason_caseunit_v0_0_0"
# def idea_format_00027_belief_plan_reasonunit_v0_0_0()-> str: return "idea_format_00027_belief_plan_reasonunit_v0_0_0"
# def idea_format_00028_belief_planunit_v0_0_0()-> str: return "idea_format_00028_belief_planunit_v0_0_0"
# def idea_format_00029_beliefunit_v0_0_0()-> str: return "idea_format_00029_beliefunit_v0_0_0"


def idea_format_00020_belief_voice_membership_v0_0_0() -> str:
    return "idea_format_00020_belief_voice_membership_v0_0_0"


def idea_format_00021_belief_voiceunit_v0_0_0() -> str:
    return "idea_format_00021_belief_voiceunit_v0_0_0"


def idea_format_00022_belief_plan_awardunit_v0_0_0() -> str:
    return "idea_format_00022_belief_plan_awardunit_v0_0_0"


def idea_format_00023_belief_plan_factunit_v0_0_0() -> str:
    return "idea_format_00023_belief_plan_factunit_v0_0_0"


def idea_format_00024_belief_plan_partyunit_v0_0_0() -> str:
    return "idea_format_00024_belief_plan_partyunit_v0_0_0"


def idea_format_00025_belief_plan_healerunit_v0_0_0() -> str:
    return "idea_format_00025_belief_plan_healerunit_v0_0_0"


def idea_format_00026_belief_plan_reason_caseunit_v0_0_0() -> str:
    return "idea_format_00026_belief_plan_reason_caseunit_v0_0_0"


def idea_format_00027_belief_plan_reasonunit_v0_0_0() -> str:
    return "idea_format_00027_belief_plan_reasonunit_v0_0_0"


def idea_format_00028_belief_planunit_v0_0_0() -> str:
    return "idea_format_00028_belief_planunit_v0_0_0"


def idea_format_00029_beliefunit_v0_0_0() -> str:
    return "idea_format_00029_beliefunit_v0_0_0"


def idea_format_00036_problem_healer_v0_0_0() -> str:
    return "idea_format_00036_problem_healer_v0_0_0"


def idea_format_00040_map_otx2inx_v0_0_0() -> str:
    return "idea_format_00040_map_otx2inx_v0_0_0"


def idea_format_00042_translate_title_v0_0_0() -> str:
    return "idea_format_00042_translate_title_v0_0_0"


def idea_format_00043_translate_name_v0_0_0() -> str:
    return "idea_format_00043_translate_name_v0_0_0"


def idea_format_00044_translate_label_v0_0_0() -> str:
    return "idea_format_00044_translate_label_v0_0_0"


def idea_format_00045_translate_rope_v0_0_0() -> str:
    return "idea_format_00045_translate_rope_v0_0_0"


def idea_format_00050_delete_belief_voice_membership_v0_0_0() -> str:
    return "idea_format_00050_delete_belief_voice_membership_v0_0_0"


def idea_format_00051_delete_belief_voiceunit_v0_0_0() -> str:
    return "idea_format_00051_delete_belief_voiceunit_v0_0_0"


def idea_format_00052_delete_belief_plan_awardunit_v0_0_0() -> str:
    return "idea_format_00052_delete_belief_plan_awardunit_v0_0_0"


def idea_format_00053_delete_belief_plan_factunit_v0_0_0() -> str:
    return "idea_format_00053_delete_belief_plan_factunit_v0_0_0"


def idea_format_00054_delete_belief_plan_partyunit_v0_0_0() -> str:
    return "idea_format_00054_delete_belief_plan_partyunit_v0_0_0"


def idea_format_00055_delete_belief_plan_healerunit_v0_0_0() -> str:
    return "idea_format_00055_delete_belief_plan_healerunit_v0_0_0"


def idea_format_00056_delete_belief_plan_reason_caseunit_v0_0_0() -> str:
    return "idea_format_00056_delete_belief_plan_reason_caseunit_v0_0_0"


def idea_format_00057_delete_belief_plan_reasonunit_v0_0_0() -> str:
    return "idea_format_00057_delete_belief_plan_reasonunit_v0_0_0"


def idea_format_00058_delete_belief_planunit_v0_0_0() -> str:
    return "idea_format_00058_delete_belief_planunit_v0_0_0"


def idea_format_00059_delete_beliefunit_v0_0_0() -> str:
    return "idea_format_00059_delete_beliefunit_v0_0_0"


def idea_format_00113_voice_map1_v0_0_0() -> str:
    return "idea_format_00113_voice_map1_v0_0_0"


def idea_format_00115_group_map1_v0_0_0() -> str:
    return "idea_format_00115_group_map1_v0_0_0"


def idea_format_00116_label_map1_v0_0_0() -> str:
    return "idea_format_00116_label_map1_v0_0_0"


def idea_format_00117_rope_map1_v0_0_0() -> str:
    return "idea_format_00117_rope_map1_v0_0_0"


def get_idea_format_filenames() -> set[str]:
    return {
        idea_format_00000_momentunit_v0_0_0(),
        idea_format_00001_moment_budunit_v0_0_0(),
        idea_format_00002_moment_paybook_v0_0_0(),
        idea_format_00003_moment_timeline_hour_v0_0_0(),
        idea_format_00004_moment_timeline_month_v0_0_0(),
        idea_format_00005_moment_timeline_weekday_v0_0_0(),
        idea_format_00006_moment_timeoffi_v0_0_0(),
        idea_format_00011_voice_v0_0_0(),
        idea_format_00012_membership_v0_0_0(),
        idea_format_00013_planunit_v0_0_0(),
        idea_format_00019_planunit_v0_0_0(),
        idea_format_00020_belief_voice_membership_v0_0_0(),
        idea_format_00021_belief_voiceunit_v0_0_0(),
        idea_format_00022_belief_plan_awardunit_v0_0_0(),
        idea_format_00023_belief_plan_factunit_v0_0_0(),
        idea_format_00024_belief_plan_partyunit_v0_0_0(),
        idea_format_00025_belief_plan_healerunit_v0_0_0(),
        idea_format_00026_belief_plan_reason_caseunit_v0_0_0(),
        idea_format_00027_belief_plan_reasonunit_v0_0_0(),
        idea_format_00028_belief_planunit_v0_0_0(),
        idea_format_00029_beliefunit_v0_0_0(),
        idea_format_00036_problem_healer_v0_0_0(),
        idea_format_00042_translate_title_v0_0_0(),
        idea_format_00043_translate_name_v0_0_0(),
        idea_format_00044_translate_label_v0_0_0(),
        idea_format_00045_translate_rope_v0_0_0(),
        idea_format_00050_delete_belief_voice_membership_v0_0_0(),
        idea_format_00051_delete_belief_voiceunit_v0_0_0(),
        idea_format_00052_delete_belief_plan_awardunit_v0_0_0(),
        idea_format_00053_delete_belief_plan_factunit_v0_0_0(),
        idea_format_00054_delete_belief_plan_partyunit_v0_0_0(),
        idea_format_00055_delete_belief_plan_healerunit_v0_0_0(),
        idea_format_00056_delete_belief_plan_reason_caseunit_v0_0_0(),
        idea_format_00057_delete_belief_plan_reasonunit_v0_0_0(),
        idea_format_00058_delete_belief_planunit_v0_0_0(),
        idea_format_00059_delete_beliefunit_v0_0_0(),
        idea_format_00113_voice_map1_v0_0_0(),
        idea_format_00115_group_map1_v0_0_0(),
        idea_format_00116_label_map1_v0_0_0(),
        idea_format_00117_rope_map1_v0_0_0(),
    }


def get_idea_numbers() -> set[str]:
    return {
        "br00000",
        "br00001",
        "br00002",
        "br00003",
        "br00004",
        "br00005",
        "br00006",
        "br00011",
        "br00012",
        "br00013",
        "br00019",
        "br00020",
        "br00021",
        "br00022",
        "br00023",
        "br00024",
        "br00025",
        "br00026",
        "br00027",
        "br00028",
        "br00029",
        "br00036",
        "br00042",
        "br00043",
        "br00044",
        "br00045",
        "br00050",
        "br00051",
        "br00052",
        "br00053",
        "br00054",
        "br00055",
        "br00056",
        "br00057",
        "br00058",
        "br00059",
        "br00113",
        "br00115",
        "br00116",
        "br00117",
    }


def get_idea_format_filename(idea_number: str) -> str:
    idea_number_substring = idea_number[2:]
    for idea_format_filename in get_idea_format_filenames():
        if idea_format_filename[12:17] == idea_number_substring:
            return idea_format_filename


def get_idea_format_headers() -> dict[str, list[str]]:
    return {
        "moment_label,timeline_label,c400_number,yr1_jan1_offset,monthday_index,fund_iota,penny,respect_bit,knot,job_listen_rotations": idea_format_00000_momentunit_v0_0_0(),
        "moment_label,belief_name,bud_time,quota,celldepth": idea_format_00001_moment_budunit_v0_0_0(),
        "moment_label,belief_name,voice_name,tran_time,amount": idea_format_00002_moment_paybook_v0_0_0(),
        "moment_label,cumulative_minute,hour_label": idea_format_00003_moment_timeline_hour_v0_0_0(),
        "moment_label,cumulative_day,month_label": idea_format_00004_moment_timeline_month_v0_0_0(),
        "moment_label,weekday_order,weekday_label": idea_format_00005_moment_timeline_weekday_v0_0_0(),
        "moment_label,offi_time": idea_format_00006_moment_timeoffi_v0_0_0(),
        "moment_label,belief_name,voice_name": idea_format_00011_voice_v0_0_0(),
        "moment_label,belief_name,voice_name,group_title": idea_format_00012_membership_v0_0_0(),
        "moment_label,belief_name,plan_rope,star,pledge": idea_format_00013_planunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want": idea_format_00019_planunit_v0_0_0(),
        "moment_label,belief_name,voice_name,group_title,group_cred_points,group_debt_points": idea_format_00020_belief_voice_membership_v0_0_0(),
        "moment_label,belief_name,voice_name,voice_cred_points,voice_debt_points": idea_format_00021_belief_voiceunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,awardee_title,give_force,take_force": idea_format_00022_belief_plan_awardunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,fact_context,fact_state,fact_lower,fact_upper": idea_format_00023_belief_plan_factunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,party_title,solo": idea_format_00024_belief_plan_partyunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,healer_name": idea_format_00025_belief_plan_healerunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,reason_context,reason_state,reason_upper,reason_lower,reason_divisor": idea_format_00026_belief_plan_reason_caseunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,reason_context,reason_active_requisite": idea_format_00027_belief_plan_reasonunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want,star,pledge,problem_bool": idea_format_00028_belief_planunit_v0_0_0(),
        "moment_label,belief_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_iota,penny,respect_bit": idea_format_00029_beliefunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,healer_name,problem_bool": idea_format_00036_problem_healer_v0_0_0(),
        "otx_title,inx_title,otx_knot,inx_knot,unknown_str": idea_format_00042_translate_title_v0_0_0(),
        "otx_name,inx_name,otx_knot,inx_knot,unknown_str": idea_format_00043_translate_name_v0_0_0(),
        "otx_label,inx_label,otx_knot,inx_knot,unknown_str": idea_format_00044_translate_label_v0_0_0(),
        "otx_rope,inx_rope,otx_knot,inx_knot,unknown_str": idea_format_00045_translate_rope_v0_0_0(),
        "moment_label,belief_name,voice_name,group_title_ERASE": idea_format_00050_delete_belief_voice_membership_v0_0_0(),
        "moment_label,belief_name,voice_name_ERASE": idea_format_00051_delete_belief_voiceunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,awardee_title_ERASE": idea_format_00052_delete_belief_plan_awardunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,fact_context_ERASE": idea_format_00053_delete_belief_plan_factunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,party_title_ERASE": idea_format_00054_delete_belief_plan_partyunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,healer_name_ERASE": idea_format_00055_delete_belief_plan_healerunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,reason_context,reason_state_ERASE": idea_format_00056_delete_belief_plan_reason_caseunit_v0_0_0(),
        "moment_label,belief_name,plan_rope,reason_context_ERASE": idea_format_00057_delete_belief_plan_reasonunit_v0_0_0(),
        "moment_label,belief_name,plan_rope_ERASE": idea_format_00058_delete_belief_planunit_v0_0_0(),
        "moment_label,belief_name_ERASE": idea_format_00059_delete_beliefunit_v0_0_0(),
        "moment_label,belief_name,voice_name,otx_name,inx_name": idea_format_00113_voice_map1_v0_0_0(),
        "moment_label,belief_name,voice_name,otx_title,inx_title": idea_format_00115_group_map1_v0_0_0(),
        "moment_label,belief_name,voice_name,otx_label,inx_label": idea_format_00116_label_map1_v0_0_0(),
        "moment_label,belief_name,voice_name,otx_rope,inx_rope": idea_format_00117_rope_map1_v0_0_0(),
    }


def get_idearef_from_file(idea_format_filename: str) -> dict:
    idearef_filename = get_json_filename(idea_format_filename)
    return open_json(get_idea_formats_dir(), idearef_filename)


def get_quick_ideas_column_ref() -> dict[str, set[str]]:
    idea_number_dict = {}
    for idea_format_filename in get_idea_format_filenames():
        idearef_dict = get_idearef_from_file(idea_format_filename)
        idea_number = idearef_dict.get("idea_number")
        idea_number_dict[idea_number] = set(idearef_dict.get("attributes").keys())
    return idea_number_dict


def get_idea_dimen_ref() -> dict[str, set[str]]:
    """dictionary with key=dimen and value=set of all idea_numbers with that dimen's data"""
    return {
        "belief_voice_membership": {"br00012", "br00020", "br00050"},
        "belief_voiceunit": {
            "br00002",
            "br00011",
            "br00012",
            "br00020",
            "br00021",
            "br00050",
            "br00051",
            "br00113",
            "br00115",
            "br00116",
            "br00117",
        },
        "belief_plan_awardunit": {"br00022", "br00052"},
        "belief_plan_factunit": {"br00023", "br00053"},
        "belief_plan_healerunit": {"br00025", "br00036", "br00055"},
        "belief_plan_reason_caseunit": {"br00026", "br00056"},
        "belief_plan_reasonunit": {"br00026", "br00027", "br00056", "br00057"},
        "belief_plan_partyunit": {"br00024", "br00054"},
        "belief_planunit": {
            "br00013",
            "br00019",
            "br00022",
            "br00023",
            "br00024",
            "br00025",
            "br00026",
            "br00027",
            "br00028",
            "br00036",
            "br00052",
            "br00053",
            "br00054",
            "br00055",
            "br00056",
            "br00057",
            "br00058",
        },
        "beliefunit": {
            "br00001",
            "br00002",
            "br00011",
            "br00012",
            "br00013",
            "br00019",
            "br00020",
            "br00021",
            "br00022",
            "br00023",
            "br00024",
            "br00025",
            "br00026",
            "br00027",
            "br00028",
            "br00029",
            "br00036",
            "br00050",
            "br00051",
            "br00052",
            "br00053",
            "br00054",
            "br00055",
            "br00056",
            "br00057",
            "br00058",
            "br00059",
            "br00113",
            "br00115",
            "br00116",
            "br00117",
        },
        "moment_paybook": {"br00002"},
        "moment_budunit": {"br00001"},
        "moment_timeline_hour": {"br00003"},
        "moment_timeline_month": {"br00004"},
        "moment_timeline_weekday": {"br00005"},
        "moment_timeoffi": {"br00006"},
        "momentunit": {
            "br00000",
            "br00001",
            "br00002",
            "br00003",
            "br00004",
            "br00005",
            "br00006",
            "br00011",
            "br00012",
            "br00013",
            "br00019",
            "br00020",
            "br00021",
            "br00022",
            "br00023",
            "br00024",
            "br00025",
            "br00026",
            "br00027",
            "br00028",
            "br00029",
            "br00036",
            "br00050",
            "br00051",
            "br00052",
            "br00053",
            "br00054",
            "br00055",
            "br00056",
            "br00057",
            "br00058",
            "br00059",
            "br00113",
            "br00115",
            "br00116",
            "br00117",
        },
        "translate_title": {"br00042", "br00115"},
        "translate_name": {"br00043", "br00113"},
        "translate_rope": {"br00045", "br00117"},
        "translate_label": {"br00044", "br00116"},
    }
