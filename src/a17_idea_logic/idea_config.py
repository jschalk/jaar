from src.a00_data_toolbox.file_toolbox import (
    open_json,
    create_path,
    get_json_filename,
)
from src.a00_data_toolbox.db_toolbox import get_sorted_intersection_list
from os import getcwd as os_getcwd


def get_idea_config_filename() -> str:
    return "idea_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "a17_idea_logic")


def get_idea_config_dict() -> dict:
    return open_json(config_file_dir(), get_idea_config_filename())


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
    idea_dir = create_path("src", "a17_idea_logic")
    # return create_path(idea_dir, "idea_formats")
    return "src/a17_idea_logic/idea_formats"


def get_idea_elements_sort_order() -> list[str]:
    """Contains the standard sort order for all idea and bud_calc columns"""
    return [
        "world_id",
        "idea_number",
        "source_dimen",
        "pidgin_event_int",
        "event_int",
        "face_name",
        "face_name_otx",
        "face_name_inx",
        "fisc_label",
        "fisc_label_otx",
        "fisc_label_inx",
        "timeline_label",
        "timeline_label_otx",
        "timeline_label_inx",
        "offi_time",
        "c400_number",
        "yr1_jan1_offset",
        "monthday_distortion",
        "cumlative_day",
        "month_label",
        "month_label_otx",
        "month_label_inx",
        "cumlative_minute",
        "hour_label",
        "hour_label_otx",
        "hour_label_inx",
        "weekday_order",
        "weekday_label",
        "weekday_label_otx",
        "weekday_label_inx",
        "owner_name",
        "owner_name_otx",
        "owner_name_inx",
        "owner_name_ERASE",
        "owner_name_ERASE_otx",
        "owner_name_ERASE_inx",
        "acct_name",
        "acct_name_otx",
        "acct_name_inx",
        "acct_name_ERASE",
        "acct_name_ERASE_otx",
        "acct_name_ERASE_inx",
        "group_title",
        "group_title_otx",
        "group_title_inx",
        "group_title_ERASE",
        "group_title_ERASE_otx",
        "group_title_ERASE_inx",
        "concept_way",
        "concept_way_otx",
        "concept_way_inx",
        "concept_way_ERASE",
        "concept_way_ERASE_otx",
        "concept_way_ERASE_inx",
        "rcontext",
        "rcontext_otx",
        "rcontext_inx",
        "rcontext_ERASE",
        "rcontext_ERASE_otx",
        "rcontext_ERASE_inx",
        "fcontext",
        "fcontext_otx",
        "fcontext_inx",
        "fcontext_ERASE",
        "fcontext_ERASE_otx",
        "fcontext_ERASE_inx",
        "pstate",
        "pstate_otx",
        "pstate_inx",
        "pstate_ERASE",
        "pstate_ERASE_otx",
        "pstate_ERASE_inx",
        "fstate",
        "fstate_otx",
        "fstate_inx",
        "labor_title",
        "labor_title_otx",
        "labor_title_inx",
        "labor_title_ERASE",
        "labor_title_ERASE_otx",
        "labor_title_ERASE_inx",
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
        "deal_time",
        "tran_time",
        "begin",
        "close",
        "addin",
        "numor",
        "denom",
        "morph",
        "gogo_want",
        "stop_want",
        "rconcept_active_requisite",
        "credit_belief",
        "debtit_belief",
        "credit_vote",
        "debtit_vote",
        "credor_respect",
        "debtor_respect",
        "fopen",
        "fnigh",
        "fund_pool",
        "give_force",
        "mass",
        "max_tree_traverse",
        "pnigh",
        "popen",
        "pdivisor",
        "pledge",
        "problem_bool",
        "take_force",
        "tally",
        "fund_coin",
        "penny",
        "respect_bit",
        "amount",
        "otx_label",
        "inx_label",
        "otx_way",
        "inx_way",
        "otx_name",
        "inx_name",
        "otx_title",
        "inx_title",
        "otx_bridge",
        "inx_bridge",
        "bridge",
        "unknown_str",
        "quota",
        "celldepth",
        "job_listen_rotations",
        "error_message",
        "_owner_name_labor",
        "_active",
        "_task",
        "_status",
        "_credor_pool",
        "_debtor_pool",
        "_rational",
        "_fund_give",
        "_fund_take",
        "_fund_onset",
        "_fund_cease",
        "_fund_ratio",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
        "_inallocable_debtit_belief",
        "_gogo_calc",
        "_stop_calc",
        "_level",
        "_range_evaluated",
        "_descendant_pledge_count",
        "_healerlink_ratio",
        "_all_acct_cred",
        "_keeps_justified",
        "_offtrack_fund",
        "_rcontext_concept_active_value",
        "_irrational_debtit_belief",
        "_sum_healerlink_share",
        "_keeps_buildable",
        "_all_acct_debt",
        "_tree_traverse_count",
    ]


def get_default_sorted_list(
    existing_columns: set[str], sorting_columns: list[str] = None
) -> list[str]:
    if sorting_columns is None:
        sorting_columns = get_idea_elements_sort_order()
    return get_sorted_intersection_list(existing_columns, sorting_columns)


def get_idea_sqlite_types() -> dict[str, str]:
    """Contains the sqlite_type for all idea and bud_calc columns"""

    return {
        "world_id": "TEXT",
        "idea_number": "TEXT",
        "face_name": "TEXT",
        "face_name_otx": "TEXT",
        "face_name_inx": "TEXT",
        "source_dimen": "TEXT",
        "pidgin_event_int": "INTEGER",
        "event_int": "INTEGER",
        "fisc_label": "TEXT",
        "fisc_label_otx": "TEXT",
        "fisc_label_inx": "TEXT",
        "owner_name": "TEXT",
        "owner_name_otx": "TEXT",
        "owner_name_inx": "TEXT",
        "owner_name_ERASE": "TEXT",
        "owner_name_ERASE_otx": "TEXT",
        "owner_name_ERASE_inx": "TEXT",
        "acct_name": "TEXT",
        "acct_name_otx": "TEXT",
        "acct_name_inx": "TEXT",
        "acct_name_ERASE": "TEXT",
        "acct_name_ERASE_otx": "TEXT",
        "acct_name_ERASE_inx": "TEXT",
        "group_title": "TEXT",
        "group_title_otx": "TEXT",
        "group_title_inx": "TEXT",
        "group_title_ERASE": "TEXT",
        "group_title_ERASE_otx": "TEXT",
        "group_title_ERASE_inx": "TEXT",
        "concept_way": "TEXT",
        "concept_way_otx": "TEXT",
        "concept_way_inx": "TEXT",
        "concept_way_ERASE": "TEXT",
        "concept_way_ERASE_otx": "TEXT",
        "concept_way_ERASE_inx": "TEXT",
        "rcontext": "TEXT",
        "rcontext_otx": "TEXT",
        "rcontext_inx": "TEXT",
        "rcontext_ERASE": "TEXT",
        "rcontext_ERASE_otx": "TEXT",
        "rcontext_ERASE_inx": "TEXT",
        "fcontext": "TEXT",
        "fcontext_otx": "TEXT",
        "fcontext_inx": "TEXT",
        "fcontext_ERASE": "TEXT",
        "fcontext_ERASE_otx": "TEXT",
        "fcontext_ERASE_inx": "TEXT",
        "pstate": "TEXT",
        "pstate_otx": "TEXT",
        "pstate_inx": "TEXT",
        "pstate_ERASE": "TEXT",
        "pstate_ERASE_otx": "TEXT",
        "pstate_ERASE_inx": "TEXT",
        "fstate": "TEXT",
        "fstate_otx": "TEXT",
        "fstate_inx": "TEXT",
        "labor_title": "TEXT",
        "labor_title_otx": "TEXT",
        "labor_title_inx": "TEXT",
        "labor_title_ERASE": "TEXT",
        "labor_title_ERASE_otx": "TEXT",
        "labor_title_ERASE_inx": "TEXT",
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
        "deal_time": "INTEGER",
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
        "rconcept_active_requisite": "INTEGER",
        "credit_belief": "REAL",
        "debtit_belief": "REAL",
        "credit_vote": "REAL",
        "debtit_vote": "REAL",
        "credor_respect": "REAL",
        "debtor_respect": "REAL",
        "fopen": "REAL",
        "fnigh": "REAL",
        "fund_pool": "REAL",
        "give_force": "REAL",
        "mass": "INTEGER",
        "max_tree_traverse": "INTEGER",
        "pnigh": "REAL",
        "popen": "REAL",
        "pdivisor": "INTEGER",
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
        "cumlative_minute": "INTEGER",
        "cumlative_day": "INTEGER",
        "weekday_label": "TEXT",
        "weekday_label_otx": "TEXT",
        "weekday_label_inx": "TEXT",
        "weekday_order": "INTEGER",
        "otx_bridge": "TEXT",
        "inx_bridge": "TEXT",
        "unknown_str": "TEXT",
        "otx_label": "TEXT",
        "inx_label": "TEXT",
        "otx_way": "TEXT",
        "inx_way": "TEXT",
        "otx_name": "TEXT",
        "inx_name": "TEXT",
        "otx_title": "TEXT",
        "inx_title": "TEXT",
        "bridge": "TEXT",
        "c400_number": "INTEGER",
        "yr1_jan1_offset": "INTEGER",
        "quota": "REAL",
        "celldepth": "INT",
        "monthday_distortion": "INTEGER",
        "job_listen_rotations": "INTEGER",
        "timeline_label": "TEXT",
        "timeline_label_otx": "TEXT",
        "timeline_label_inx": "TEXT",
        "error_message": "TEXT",
        "_credor_pool": "REAL",
        "_debtor_pool": "REAL",
        "_fund_cease": "REAL",
        "_fund_onset": "REAL",
        "_fund_ratio": "REAL",
        "fund_coin": "REAL",
        "_fund_agenda_give": "REAL",
        "_fund_agenda_ratio_give": "REAL",
        "_fund_agenda_ratio_take": "REAL",
        "_fund_agenda_take": "REAL",
        "_fund_give": "REAL",
        "_fund_take": "REAL",
        "_gogo_calc": "REAL",
        "_stop_calc": "REAL",
        "_all_acct_cred": "INTEGER",
        "_all_acct_debt": "INTEGER",
        "_rcontext_concept_active_value": "INTEGER",
        "_inallocable_debtit_belief": "REAL",
        "_irrational_debtit_belief": "REAL",
        "_status": "INTEGER",
        "_task": "INTEGER",
        "_owner_name_labor": "INTEGER",
        "_active": "INTEGER",
        "_descendant_pledge_count": "INTEGER",
        "_healerlink_ratio": "REAL",
        "_level": "INTEGER",
        "_range_evaluated": "INTEGER",
        "_keeps_buildable": "INTEGER",
        "_keeps_justified": "INTEGER",
        "_offtrack_fund": "REAL",
        "_rational": "INTEGER",
        "_sum_healerlink_share": "REAL",
        "_tree_traverse_count": "INTEGER",
    }


# def idea_format_00000_fiscunit_v0_0_0()->str: return "idea_format_00000_fiscunit_v0_0_0"
# def idea_format_00001_fisc_dealunit_v0_0_0()->str: return "idea_format_00001_fisc_dealunit_v0_0_0"
# def idea_format_00002_fisc_cashbook_v0_0_0()->str: return "idea_format_00002_fisc_cashbook_v0_0_0"
# def idea_format_00003_fisc_timeline_hour_v0_0_0()->str: return "idea_format_00003_fisc_timeline_hour_v0_0_0"
# def idea_format_00004_fisc_timeline_month_v0_0_0()->str: return "idea_format_00004_fisc_timeline_month_v0_0_0"
# def idea_format_00005_fisc_timeline_weekday_v0_0_0()->str: return "idea_format_00005_fisc_timeline_weekday_v0_0_0"


def idea_format_00000_fiscunit_v0_0_0() -> str:
    return "idea_format_00000_fiscunit_v0_0_0"


def idea_format_00001_fisc_dealunit_v0_0_0() -> str:
    return "idea_format_00001_fisc_dealunit_v0_0_0"


def idea_format_00002_fisc_cashbook_v0_0_0() -> str:
    return "idea_format_00002_fisc_cashbook_v0_0_0"


def idea_format_00003_fisc_timeline_hour_v0_0_0() -> str:
    return "idea_format_00003_fisc_timeline_hour_v0_0_0"


def idea_format_00004_fisc_timeline_month_v0_0_0() -> str:
    return "idea_format_00004_fisc_timeline_month_v0_0_0"


def idea_format_00005_fisc_timeline_weekday_v0_0_0() -> str:
    return "idea_format_00005_fisc_timeline_weekday_v0_0_0"


def idea_format_00006_fisc_timeoffi_v0_0_0() -> str:
    return "idea_format_00006_fisc_timeoffi_v0_0_0"


def idea_format_00011_acct_v0_0_0() -> str:
    return "idea_format_00011_acct_v0_0_0"


def idea_format_00012_membership_v0_0_0() -> str:
    return "idea_format_00012_membership_v0_0_0"


def idea_format_00013_conceptunit_v0_0_0() -> str:
    return "idea_format_00013_conceptunit_v0_0_0"


def idea_format_00019_conceptunit_v0_0_0() -> str:
    return "idea_format_00019_conceptunit_v0_0_0"


# def idea_format_00020_bud_acct_membership_v0_0_0()-> str: return "idea_format_00020_bud_acct_membership_v0_0_0"
# def idea_format_00021_bud_acctunit_v0_0_0()-> str: return "idea_format_00021_bud_acctunit_v0_0_0"
# def idea_format_00022_bud_concept_awardlink_v0_0_0()-> str: return "idea_format_00022_bud_concept_awardlink_v0_0_0"
# def idea_format_00023_bud_concept_factunit_v0_0_0()-> str: return "idea_format_00023_bud_concept_factunit_v0_0_0"
# def idea_format_00024_bud_concept_laborlink_v0_0_0()-> str: return "idea_format_00024_bud_concept_laborlink_v0_0_0"
# def idea_format_00025_bud_concept_healerlink_v0_0_0()-> str: return "idea_format_00025_bud_concept_healerlink_v0_0_0"
# def idea_format_00026_bud_concept_reason_premiseunit_v0_0_0()-> str: return "idea_format_00026_bud_concept_reason_premiseunit_v0_0_0"
# def idea_format_00027_bud_concept_reasonunit_v0_0_0()-> str: return "idea_format_00027_bud_concept_reasonunit_v0_0_0"
# def idea_format_00028_bud_conceptunit_v0_0_0()-> str: return "idea_format_00028_bud_conceptunit_v0_0_0"
# def idea_format_00029_budunit_v0_0_0()-> str: return "idea_format_00029_budunit_v0_0_0"


def idea_format_00020_bud_acct_membership_v0_0_0() -> str:
    return "idea_format_00020_bud_acct_membership_v0_0_0"


def idea_format_00021_bud_acctunit_v0_0_0() -> str:
    return "idea_format_00021_bud_acctunit_v0_0_0"


def idea_format_00022_bud_concept_awardlink_v0_0_0() -> str:
    return "idea_format_00022_bud_concept_awardlink_v0_0_0"


def idea_format_00023_bud_concept_factunit_v0_0_0() -> str:
    return "idea_format_00023_bud_concept_factunit_v0_0_0"


def idea_format_00024_bud_concept_laborlink_v0_0_0() -> str:
    return "idea_format_00024_bud_concept_laborlink_v0_0_0"


def idea_format_00025_bud_concept_healerlink_v0_0_0() -> str:
    return "idea_format_00025_bud_concept_healerlink_v0_0_0"


def idea_format_00026_bud_concept_reason_premiseunit_v0_0_0() -> str:
    return "idea_format_00026_bud_concept_reason_premiseunit_v0_0_0"


def idea_format_00027_bud_concept_reasonunit_v0_0_0() -> str:
    return "idea_format_00027_bud_concept_reasonunit_v0_0_0"


def idea_format_00028_bud_conceptunit_v0_0_0() -> str:
    return "idea_format_00028_bud_conceptunit_v0_0_0"


def idea_format_00029_budunit_v0_0_0() -> str:
    return "idea_format_00029_budunit_v0_0_0"


def idea_format_00036_problem_healer_v0_0_0() -> str:
    return "idea_format_00036_problem_healer_v0_0_0"


def idea_format_00040_map_otx2inx_v0_0_0() -> str:
    return "idea_format_00040_map_otx2inx_v0_0_0"


def idea_format_00042_pidgin_title_v0_0_0() -> str:
    return "idea_format_00042_pidgin_title_v0_0_0"


def idea_format_00043_pidgin_name_v0_0_0() -> str:
    return "idea_format_00043_pidgin_name_v0_0_0"


def idea_format_00044_pidgin_label_v0_0_0() -> str:
    return "idea_format_00044_pidgin_label_v0_0_0"


def idea_format_00045_pidgin_way_v0_0_0() -> str:
    return "idea_format_00045_pidgin_way_v0_0_0"


def idea_format_00050_delete_bud_acct_membership_v0_0_0() -> str:
    return "idea_format_00050_delete_bud_acct_membership_v0_0_0"


def idea_format_00051_delete_bud_acctunit_v0_0_0() -> str:
    return "idea_format_00051_delete_bud_acctunit_v0_0_0"


def idea_format_00052_delete_bud_concept_awardlink_v0_0_0() -> str:
    return "idea_format_00052_delete_bud_concept_awardlink_v0_0_0"


def idea_format_00053_delete_bud_concept_factunit_v0_0_0() -> str:
    return "idea_format_00053_delete_bud_concept_factunit_v0_0_0"


def idea_format_00054_delete_bud_concept_laborlink_v0_0_0() -> str:
    return "idea_format_00054_delete_bud_concept_laborlink_v0_0_0"


def idea_format_00055_delete_bud_concept_healerlink_v0_0_0() -> str:
    return "idea_format_00055_delete_bud_concept_healerlink_v0_0_0"


def idea_format_00056_delete_bud_concept_reason_premiseunit_v0_0_0() -> str:
    return "idea_format_00056_delete_bud_concept_reason_premiseunit_v0_0_0"


def idea_format_00057_delete_bud_concept_reasonunit_v0_0_0() -> str:
    return "idea_format_00057_delete_bud_concept_reasonunit_v0_0_0"


def idea_format_00058_delete_bud_conceptunit_v0_0_0() -> str:
    return "idea_format_00058_delete_bud_conceptunit_v0_0_0"


def idea_format_00059_delete_budunit_v0_0_0() -> str:
    return "idea_format_00059_delete_budunit_v0_0_0"


def idea_format_00050_delete_bud_acct_membership_v0_0_0() -> str:
    return "idea_format_00050_delete_bud_acct_membership_v0_0_0"


def idea_format_00113_acct_map1_v0_0_0() -> str:
    return "idea_format_00113_acct_map1_v0_0_0"


def idea_format_00115_group_map1_v0_0_0() -> str:
    return "idea_format_00115_group_map1_v0_0_0"


def idea_format_00116_label_map1_v0_0_0() -> str:
    return "idea_format_00116_label_map1_v0_0_0"


def idea_format_00117_way_map1_v0_0_0() -> str:
    return "idea_format_00117_way_map1_v0_0_0"


def get_idea_format_filenames() -> set[str]:
    return {
        idea_format_00000_fiscunit_v0_0_0(),
        idea_format_00001_fisc_dealunit_v0_0_0(),
        idea_format_00002_fisc_cashbook_v0_0_0(),
        idea_format_00003_fisc_timeline_hour_v0_0_0(),
        idea_format_00004_fisc_timeline_month_v0_0_0(),
        idea_format_00005_fisc_timeline_weekday_v0_0_0(),
        idea_format_00006_fisc_timeoffi_v0_0_0(),
        idea_format_00011_acct_v0_0_0(),
        idea_format_00012_membership_v0_0_0(),
        idea_format_00013_conceptunit_v0_0_0(),
        idea_format_00019_conceptunit_v0_0_0(),
        idea_format_00020_bud_acct_membership_v0_0_0(),
        idea_format_00021_bud_acctunit_v0_0_0(),
        idea_format_00022_bud_concept_awardlink_v0_0_0(),
        idea_format_00023_bud_concept_factunit_v0_0_0(),
        idea_format_00024_bud_concept_laborlink_v0_0_0(),
        idea_format_00025_bud_concept_healerlink_v0_0_0(),
        idea_format_00026_bud_concept_reason_premiseunit_v0_0_0(),
        idea_format_00027_bud_concept_reasonunit_v0_0_0(),
        idea_format_00028_bud_conceptunit_v0_0_0(),
        idea_format_00029_budunit_v0_0_0(),
        idea_format_00036_problem_healer_v0_0_0(),
        idea_format_00042_pidgin_title_v0_0_0(),
        idea_format_00043_pidgin_name_v0_0_0(),
        idea_format_00044_pidgin_label_v0_0_0(),
        idea_format_00045_pidgin_way_v0_0_0(),
        idea_format_00050_delete_bud_acct_membership_v0_0_0(),
        idea_format_00051_delete_bud_acctunit_v0_0_0(),
        idea_format_00052_delete_bud_concept_awardlink_v0_0_0(),
        idea_format_00053_delete_bud_concept_factunit_v0_0_0(),
        idea_format_00054_delete_bud_concept_laborlink_v0_0_0(),
        idea_format_00055_delete_bud_concept_healerlink_v0_0_0(),
        idea_format_00056_delete_bud_concept_reason_premiseunit_v0_0_0(),
        idea_format_00057_delete_bud_concept_reasonunit_v0_0_0(),
        idea_format_00058_delete_bud_conceptunit_v0_0_0(),
        idea_format_00059_delete_budunit_v0_0_0(),
        idea_format_00113_acct_map1_v0_0_0(),
        idea_format_00115_group_map1_v0_0_0(),
        idea_format_00116_label_map1_v0_0_0(),
        idea_format_00117_way_map1_v0_0_0(),
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
        "fisc_label,timeline_label,c400_number,yr1_jan1_offset,monthday_distortion,fund_coin,penny,respect_bit,bridge,job_listen_rotations": idea_format_00000_fiscunit_v0_0_0(),
        "fisc_label,owner_name,deal_time,quota,celldepth": idea_format_00001_fisc_dealunit_v0_0_0(),
        "fisc_label,owner_name,acct_name,tran_time,amount": idea_format_00002_fisc_cashbook_v0_0_0(),
        "fisc_label,cumlative_minute,hour_label": idea_format_00003_fisc_timeline_hour_v0_0_0(),
        "fisc_label,cumlative_day,month_label": idea_format_00004_fisc_timeline_month_v0_0_0(),
        "fisc_label,weekday_order,weekday_label": idea_format_00005_fisc_timeline_weekday_v0_0_0(),
        "fisc_label,offi_time": idea_format_00006_fisc_timeoffi_v0_0_0(),
        "fisc_label,owner_name,acct_name": idea_format_00011_acct_v0_0_0(),
        "fisc_label,owner_name,acct_name,group_title": idea_format_00012_membership_v0_0_0(),
        "fisc_label,owner_name,concept_way,mass,pledge": idea_format_00013_conceptunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,begin,close,addin,numor,denom,morph,gogo_want,stop_want": idea_format_00019_conceptunit_v0_0_0(),
        "fisc_label,owner_name,acct_name,group_title,credit_vote,debtit_vote": idea_format_00020_bud_acct_membership_v0_0_0(),
        "fisc_label,owner_name,acct_name,credit_belief,debtit_belief": idea_format_00021_bud_acctunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,awardee_title,give_force,take_force": idea_format_00022_bud_concept_awardlink_v0_0_0(),
        "fisc_label,owner_name,concept_way,fcontext,fstate,fopen,fnigh": idea_format_00023_bud_concept_factunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,labor_title": idea_format_00024_bud_concept_laborlink_v0_0_0(),
        "fisc_label,owner_name,concept_way,healer_name": idea_format_00025_bud_concept_healerlink_v0_0_0(),
        "fisc_label,owner_name,concept_way,rcontext,pstate,pnigh,popen,pdivisor": idea_format_00026_bud_concept_reason_premiseunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,rcontext,rconcept_active_requisite": idea_format_00027_bud_concept_reasonunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,begin,close,addin,numor,denom,morph,gogo_want,stop_want,mass,pledge,problem_bool": idea_format_00028_bud_conceptunit_v0_0_0(),
        "fisc_label,owner_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_coin,penny,respect_bit": idea_format_00029_budunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,healer_name,problem_bool": idea_format_00036_problem_healer_v0_0_0(),
        "otx_title,inx_title,otx_bridge,inx_bridge,unknown_str": idea_format_00042_pidgin_title_v0_0_0(),
        "otx_name,inx_name,otx_bridge,inx_bridge,unknown_str": idea_format_00043_pidgin_name_v0_0_0(),
        "otx_label,inx_label,otx_bridge,inx_bridge,unknown_str": idea_format_00044_pidgin_label_v0_0_0(),
        "otx_way,inx_way,otx_bridge,inx_bridge,unknown_str": idea_format_00045_pidgin_way_v0_0_0(),
        "fisc_label,owner_name,acct_name,group_title_ERASE": idea_format_00050_delete_bud_acct_membership_v0_0_0(),
        "fisc_label,owner_name,acct_name_ERASE": idea_format_00051_delete_bud_acctunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,awardee_title_ERASE": idea_format_00052_delete_bud_concept_awardlink_v0_0_0(),
        "fisc_label,owner_name,concept_way,fcontext_ERASE": idea_format_00053_delete_bud_concept_factunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,labor_title_ERASE": idea_format_00054_delete_bud_concept_laborlink_v0_0_0(),
        "fisc_label,owner_name,concept_way,healer_name_ERASE": idea_format_00055_delete_bud_concept_healerlink_v0_0_0(),
        "fisc_label,owner_name,concept_way,rcontext,pstate_ERASE": idea_format_00056_delete_bud_concept_reason_premiseunit_v0_0_0(),
        "fisc_label,owner_name,concept_way,rcontext_ERASE": idea_format_00057_delete_bud_concept_reasonunit_v0_0_0(),
        "fisc_label,owner_name,concept_way_ERASE": idea_format_00058_delete_bud_conceptunit_v0_0_0(),
        "fisc_label,owner_name_ERASE": idea_format_00059_delete_budunit_v0_0_0(),
        "fisc_label,owner_name,acct_name,otx_name,inx_name": idea_format_00113_acct_map1_v0_0_0(),
        "fisc_label,owner_name,acct_name,otx_title,inx_title": idea_format_00115_group_map1_v0_0_0(),
        "fisc_label,owner_name,acct_name,otx_label,inx_label": idea_format_00116_label_map1_v0_0_0(),
        "fisc_label,owner_name,acct_name,otx_way,inx_way": idea_format_00117_way_map1_v0_0_0(),
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
        "bud_acct_membership": {"br00012", "br00020", "br00050"},
        "bud_acctunit": {
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
        "bud_concept_awardlink": {"br00022", "br00052"},
        "bud_concept_factunit": {"br00023", "br00053"},
        "bud_concept_healerlink": {"br00025", "br00036", "br00055"},
        "bud_concept_reason_premiseunit": {"br00026", "br00056"},
        "bud_concept_reasonunit": {"br00026", "br00027", "br00056", "br00057"},
        "bud_concept_laborlink": {"br00024", "br00054"},
        "bud_conceptunit": {
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
        "budunit": {
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
        "fisc_cashbook": {"br00002"},
        "fisc_dealunit": {"br00001"},
        "fisc_timeline_hour": {"br00003"},
        "fisc_timeline_month": {"br00004"},
        "fisc_timeline_weekday": {"br00005"},
        "fisc_timeoffi": {"br00006"},
        "fiscunit": {
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
        "pidgin_title": {"br00042", "br00115"},
        "pidgin_name": {"br00043", "br00113"},
        "pidgin_way": {"br00045", "br00117"},
        "pidgin_label": {"br00044", "br00116"},
    }
