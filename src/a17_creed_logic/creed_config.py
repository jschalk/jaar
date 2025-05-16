from src.a00_data_toolbox.file_toolbox import (
    open_json,
    create_path,
    get_json_filename,
)
from src.a00_data_toolbox.db_toolbox import get_sorted_intersection_list
from os import getcwd as os_getcwd


def get_creed_config_filename() -> str:
    return "creed_config.json"


def config_file_dir() -> str:
    src_dir = create_path(os_getcwd(), "src")
    return create_path(src_dir, "a17_creed_logic")


def get_creed_config_dict() -> dict:
    return open_json(config_file_dir(), get_creed_config_filename())


def get_allowed_curds() -> set[str]:
    return {
        "INSERT_ONE_TIME",
        "INSERT_MULITPLE",
        "DELETE_INSERT_UPDATE",
        "INSERT_UPDATE",
        "DELETE_INSERT",
        "DELETE_UPDATE",
        "UPDATE",
        "DELETE",
        "INSERT",
    }


def get_creed_formats_dir() -> str:
    creed_dir = create_path("src", "a17_creed_logic")
    # return create_path(creed_dir, "creed_formats")
    return "src/a17_creed_logic/creed_formats"


def get_creed_elements_sort_order() -> list[str]:
    """Contains the standard sort order for all creed and bud_calc columns"""
    return [
        "world_id",
        "creed_number",
        "source_dimen",
        "pidgin_event_int",
        "event_int",
        "face_name",
        "face_name_otx",
        "face_name_inx",
        "fisc_word",
        "fisc_word_otx",
        "fisc_word_inx",
        "timeline_word",
        "timeline_word_otx",
        "timeline_word_inx",
        "offi_time",
        "c400_number",
        "yr1_jan1_offset",
        "monthday_distortion",
        "cumlative_day",
        "month_word",
        "month_word_otx",
        "month_word_inx",
        "cumlative_minute",
        "hour_word",
        "hour_word_otx",
        "hour_word_inx",
        "weekday_order",
        "weekday_word",
        "weekday_word_otx",
        "weekday_word_inx",
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
        "group_label",
        "group_label_otx",
        "group_label_inx",
        "group_label_ERASE",
        "group_label_ERASE_otx",
        "group_label_ERASE_inx",
        "idea_way",
        "idea_way_otx",
        "idea_way_inx",
        "idea_way_ERASE",
        "idea_way_ERASE_otx",
        "idea_way_ERASE_inx",
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
        "pbranch",
        "pbranch_otx",
        "pbranch_inx",
        "pbranch_ERASE",
        "pbranch_ERASE_otx",
        "pbranch_ERASE_inx",
        "fbranch",
        "fbranch_otx",
        "fbranch_inx",
        "labor_label",
        "labor_label_otx",
        "labor_label_inx",
        "labor_label_ERASE",
        "labor_label_ERASE_otx",
        "labor_label_ERASE_inx",
        "awardee_label",
        "awardee_label_otx",
        "awardee_label_inx",
        "awardee_label_ERASE",
        "awardee_label_ERASE_otx",
        "awardee_label_ERASE_inx",
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
        "rcontext_idea_active_requisite",
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
        "otx_word",
        "inx_word",
        "otx_way",
        "inx_way",
        "otx_name",
        "inx_name",
        "otx_label",
        "inx_label",
        "otx_bridge",
        "inx_bridge",
        "bridge",
        "unknown_term",
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
        "_rcontext_idea_active_value",
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
        sorting_columns = get_creed_elements_sort_order()
    return get_sorted_intersection_list(existing_columns, sorting_columns)


def get_creed_sqlite_types() -> dict[str, str]:
    """Contains the sqlite_type for all creed and bud_calc columns"""

    return {
        "world_id": "TEXT",
        "creed_number": "TEXT",
        "face_name": "TEXT",
        "face_name_otx": "TEXT",
        "face_name_inx": "TEXT",
        "source_dimen": "TEXT",
        "pidgin_event_int": "INTEGER",
        "event_int": "INTEGER",
        "fisc_word": "TEXT",
        "fisc_word_otx": "TEXT",
        "fisc_word_inx": "TEXT",
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
        "group_label": "TEXT",
        "group_label_otx": "TEXT",
        "group_label_inx": "TEXT",
        "group_label_ERASE": "TEXT",
        "group_label_ERASE_otx": "TEXT",
        "group_label_ERASE_inx": "TEXT",
        "idea_way": "TEXT",
        "idea_way_otx": "TEXT",
        "idea_way_inx": "TEXT",
        "idea_way_ERASE": "TEXT",
        "idea_way_ERASE_otx": "TEXT",
        "idea_way_ERASE_inx": "TEXT",
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
        "pbranch": "TEXT",
        "pbranch_otx": "TEXT",
        "pbranch_inx": "TEXT",
        "pbranch_ERASE": "TEXT",
        "pbranch_ERASE_otx": "TEXT",
        "pbranch_ERASE_inx": "TEXT",
        "fbranch": "TEXT",
        "fbranch_otx": "TEXT",
        "fbranch_inx": "TEXT",
        "labor_label": "TEXT",
        "labor_label_otx": "TEXT",
        "labor_label_inx": "TEXT",
        "labor_label_ERASE": "TEXT",
        "labor_label_ERASE_otx": "TEXT",
        "labor_label_ERASE_inx": "TEXT",
        "awardee_label": "TEXT",
        "awardee_label_otx": "TEXT",
        "awardee_label_inx": "TEXT",
        "awardee_label_ERASE": "TEXT",
        "awardee_label_ERASE_otx": "TEXT",
        "awardee_label_ERASE_inx": "TEXT",
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
        "rcontext_idea_active_requisite": "INTEGER",
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
        "month_word": "TEXT",
        "month_word_otx": "TEXT",
        "month_word_inx": "TEXT",
        "hour_word": "TEXT",
        "hour_word_otx": "TEXT",
        "hour_word_inx": "TEXT",
        "cumlative_minute": "INTEGER",
        "cumlative_day": "INTEGER",
        "weekday_word": "TEXT",
        "weekday_word_otx": "TEXT",
        "weekday_word_inx": "TEXT",
        "weekday_order": "INTEGER",
        "otx_bridge": "TEXT",
        "inx_bridge": "TEXT",
        "unknown_term": "TEXT",
        "otx_word": "TEXT",
        "inx_word": "TEXT",
        "otx_way": "TEXT",
        "inx_way": "TEXT",
        "otx_name": "TEXT",
        "inx_name": "TEXT",
        "otx_label": "TEXT",
        "inx_label": "TEXT",
        "bridge": "TEXT",
        "c400_number": "INTEGER",
        "yr1_jan1_offset": "INTEGER",
        "quota": "REAL",
        "celldepth": "INT",
        "monthday_distortion": "INTEGER",
        "job_listen_rotations": "INTEGER",
        "timeline_word": "TEXT",
        "timeline_word_otx": "TEXT",
        "timeline_word_inx": "TEXT",
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
        "_rcontext_idea_active_value": "INTEGER",
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


# def creed_format_00000_fiscunit_v0_0_0()->str: return "creed_format_00000_fiscunit_v0_0_0"
# def creed_format_00001_fisc_dealunit_v0_0_0()->str: return "creed_format_00001_fisc_dealunit_v0_0_0"
# def creed_format_00002_fisc_cashbook_v0_0_0()->str: return "creed_format_00002_fisc_cashbook_v0_0_0"
# def creed_format_00003_fisc_timeline_hour_v0_0_0()->str: return "creed_format_00003_fisc_timeline_hour_v0_0_0"
# def creed_format_00004_fisc_timeline_month_v0_0_0()->str: return "creed_format_00004_fisc_timeline_month_v0_0_0"
# def creed_format_00005_fisc_timeline_weekday_v0_0_0()->str: return "creed_format_00005_fisc_timeline_weekday_v0_0_0"


def creed_format_00000_fiscunit_v0_0_0() -> str:
    return "creed_format_00000_fiscunit_v0_0_0"


def creed_format_00001_fisc_dealunit_v0_0_0() -> str:
    return "creed_format_00001_fisc_dealunit_v0_0_0"


def creed_format_00002_fisc_cashbook_v0_0_0() -> str:
    return "creed_format_00002_fisc_cashbook_v0_0_0"


def creed_format_00003_fisc_timeline_hour_v0_0_0() -> str:
    return "creed_format_00003_fisc_timeline_hour_v0_0_0"


def creed_format_00004_fisc_timeline_month_v0_0_0() -> str:
    return "creed_format_00004_fisc_timeline_month_v0_0_0"


def creed_format_00005_fisc_timeline_weekday_v0_0_0() -> str:
    return "creed_format_00005_fisc_timeline_weekday_v0_0_0"


def creed_format_00006_fisc_timeoffi_v0_0_0() -> str:
    return "creed_format_00006_fisc_timeoffi_v0_0_0"


def creed_format_00011_acct_v0_0_0() -> str:
    return "creed_format_00011_acct_v0_0_0"


def creed_format_00012_membership_v0_0_0() -> str:
    return "creed_format_00012_membership_v0_0_0"


def creed_format_00013_ideaunit_v0_0_0() -> str:
    return "creed_format_00013_ideaunit_v0_0_0"


def creed_format_00019_ideaunit_v0_0_0() -> str:
    return "creed_format_00019_ideaunit_v0_0_0"


# def creed_format_00020_bud_acct_membership_v0_0_0()-> str: return "creed_format_00020_bud_acct_membership_v0_0_0"
# def creed_format_00021_bud_acctunit_v0_0_0()-> str: return "creed_format_00021_bud_acctunit_v0_0_0"
# def creed_format_00022_bud_idea_awardlink_v0_0_0()-> str: return "creed_format_00022_bud_idea_awardlink_v0_0_0"
# def creed_format_00023_bud_idea_factunit_v0_0_0()-> str: return "creed_format_00023_bud_idea_factunit_v0_0_0"
# def creed_format_00024_bud_idea_laborlink_v0_0_0()-> str: return "creed_format_00024_bud_idea_laborlink_v0_0_0"
# def creed_format_00025_bud_idea_healerlink_v0_0_0()-> str: return "creed_format_00025_bud_idea_healerlink_v0_0_0"
# def creed_format_00026_bud_idea_reason_premiseunit_v0_0_0()-> str: return "creed_format_00026_bud_idea_reason_premiseunit_v0_0_0"
# def creed_format_00027_bud_idea_reasonunit_v0_0_0()-> str: return "creed_format_00027_bud_idea_reasonunit_v0_0_0"
# def creed_format_00028_bud_ideaunit_v0_0_0()-> str: return "creed_format_00028_bud_ideaunit_v0_0_0"
# def creed_format_00029_budunit_v0_0_0()-> str: return "creed_format_00029_budunit_v0_0_0"


def creed_format_00020_bud_acct_membership_v0_0_0() -> str:
    return "creed_format_00020_bud_acct_membership_v0_0_0"


def creed_format_00021_bud_acctunit_v0_0_0() -> str:
    return "creed_format_00021_bud_acctunit_v0_0_0"


def creed_format_00022_bud_idea_awardlink_v0_0_0() -> str:
    return "creed_format_00022_bud_idea_awardlink_v0_0_0"


def creed_format_00023_bud_idea_factunit_v0_0_0() -> str:
    return "creed_format_00023_bud_idea_factunit_v0_0_0"


def creed_format_00024_bud_idea_laborlink_v0_0_0() -> str:
    return "creed_format_00024_bud_idea_laborlink_v0_0_0"


def creed_format_00025_bud_idea_healerlink_v0_0_0() -> str:
    return "creed_format_00025_bud_idea_healerlink_v0_0_0"


def creed_format_00026_bud_idea_reason_premiseunit_v0_0_0() -> str:
    return "creed_format_00026_bud_idea_reason_premiseunit_v0_0_0"


def creed_format_00027_bud_idea_reasonunit_v0_0_0() -> str:
    return "creed_format_00027_bud_idea_reasonunit_v0_0_0"


def creed_format_00028_bud_ideaunit_v0_0_0() -> str:
    return "creed_format_00028_bud_ideaunit_v0_0_0"


def creed_format_00029_budunit_v0_0_0() -> str:
    return "creed_format_00029_budunit_v0_0_0"


def creed_format_00036_problem_healer_v0_0_0() -> str:
    return "creed_format_00036_problem_healer_v0_0_0"


def creed_format_00040_map_otx2inx_v0_0_0() -> str:
    return "creed_format_00040_map_otx2inx_v0_0_0"


def creed_format_00042_pidgin_label_v0_0_0() -> str:
    return "creed_format_00042_pidgin_label_v0_0_0"


def creed_format_00043_pidgin_name_v0_0_0() -> str:
    return "creed_format_00043_pidgin_name_v0_0_0"


def creed_format_00044_pidgin_word_v0_0_0() -> str:
    return "creed_format_00044_pidgin_word_v0_0_0"


def creed_format_00045_pidgin_way_v0_0_0() -> str:
    return "creed_format_00045_pidgin_way_v0_0_0"


def creed_format_00050_delete_bud_acct_membership_v0_0_0() -> str:
    return "creed_format_00050_delete_bud_acct_membership_v0_0_0"


def creed_format_00051_delete_bud_acctunit_v0_0_0() -> str:
    return "creed_format_00051_delete_bud_acctunit_v0_0_0"


def creed_format_00052_delete_bud_idea_awardlink_v0_0_0() -> str:
    return "creed_format_00052_delete_bud_idea_awardlink_v0_0_0"


def creed_format_00053_delete_bud_idea_factunit_v0_0_0() -> str:
    return "creed_format_00053_delete_bud_idea_factunit_v0_0_0"


def creed_format_00054_delete_bud_idea_laborlink_v0_0_0() -> str:
    return "creed_format_00054_delete_bud_idea_laborlink_v0_0_0"


def creed_format_00055_delete_bud_idea_healerlink_v0_0_0() -> str:
    return "creed_format_00055_delete_bud_idea_healerlink_v0_0_0"


def creed_format_00056_delete_bud_idea_reason_premiseunit_v0_0_0() -> str:
    return "creed_format_00056_delete_bud_idea_reason_premiseunit_v0_0_0"


def creed_format_00057_delete_bud_idea_reasonunit_v0_0_0() -> str:
    return "creed_format_00057_delete_bud_idea_reasonunit_v0_0_0"


def creed_format_00058_delete_bud_ideaunit_v0_0_0() -> str:
    return "creed_format_00058_delete_bud_ideaunit_v0_0_0"


def creed_format_00059_delete_budunit_v0_0_0() -> str:
    return "creed_format_00059_delete_budunit_v0_0_0"


def creed_format_00050_delete_bud_acct_membership_v0_0_0() -> str:
    return "creed_format_00050_delete_bud_acct_membership_v0_0_0"


def creed_format_00113_acct_map1_v0_0_0() -> str:
    return "creed_format_00113_acct_map1_v0_0_0"


def creed_format_00115_group_map1_v0_0_0() -> str:
    return "creed_format_00115_group_map1_v0_0_0"


def creed_format_00116_word_map1_v0_0_0() -> str:
    return "creed_format_00116_word_map1_v0_0_0"


def creed_format_00117_way_map1_v0_0_0() -> str:
    return "creed_format_00117_way_map1_v0_0_0"


def get_creed_format_filenames() -> set[str]:
    return {
        creed_format_00000_fiscunit_v0_0_0(),
        creed_format_00001_fisc_dealunit_v0_0_0(),
        creed_format_00002_fisc_cashbook_v0_0_0(),
        creed_format_00003_fisc_timeline_hour_v0_0_0(),
        creed_format_00004_fisc_timeline_month_v0_0_0(),
        creed_format_00005_fisc_timeline_weekday_v0_0_0(),
        creed_format_00006_fisc_timeoffi_v0_0_0(),
        creed_format_00011_acct_v0_0_0(),
        creed_format_00012_membership_v0_0_0(),
        creed_format_00013_ideaunit_v0_0_0(),
        creed_format_00019_ideaunit_v0_0_0(),
        creed_format_00020_bud_acct_membership_v0_0_0(),
        creed_format_00021_bud_acctunit_v0_0_0(),
        creed_format_00022_bud_idea_awardlink_v0_0_0(),
        creed_format_00023_bud_idea_factunit_v0_0_0(),
        creed_format_00024_bud_idea_laborlink_v0_0_0(),
        creed_format_00025_bud_idea_healerlink_v0_0_0(),
        creed_format_00026_bud_idea_reason_premiseunit_v0_0_0(),
        creed_format_00027_bud_idea_reasonunit_v0_0_0(),
        creed_format_00028_bud_ideaunit_v0_0_0(),
        creed_format_00029_budunit_v0_0_0(),
        creed_format_00036_problem_healer_v0_0_0(),
        creed_format_00042_pidgin_label_v0_0_0(),
        creed_format_00043_pidgin_name_v0_0_0(),
        creed_format_00044_pidgin_word_v0_0_0(),
        creed_format_00045_pidgin_way_v0_0_0(),
        creed_format_00050_delete_bud_acct_membership_v0_0_0(),
        creed_format_00051_delete_bud_acctunit_v0_0_0(),
        creed_format_00052_delete_bud_idea_awardlink_v0_0_0(),
        creed_format_00053_delete_bud_idea_factunit_v0_0_0(),
        creed_format_00054_delete_bud_idea_laborlink_v0_0_0(),
        creed_format_00055_delete_bud_idea_healerlink_v0_0_0(),
        creed_format_00056_delete_bud_idea_reason_premiseunit_v0_0_0(),
        creed_format_00057_delete_bud_idea_reasonunit_v0_0_0(),
        creed_format_00058_delete_bud_ideaunit_v0_0_0(),
        creed_format_00059_delete_budunit_v0_0_0(),
        creed_format_00113_acct_map1_v0_0_0(),
        creed_format_00115_group_map1_v0_0_0(),
        creed_format_00116_word_map1_v0_0_0(),
        creed_format_00117_way_map1_v0_0_0(),
    }


def get_creed_numbers() -> set[str]:
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


def get_creed_format_filename(creed_number: str) -> str:
    creed_number_substring = creed_number[2:]
    for creed_format_filename in get_creed_format_filenames():
        if creed_format_filename[13:18] == creed_number_substring:
            return creed_format_filename


def get_creed_format_headers() -> dict[str, list[str]]:
    return {
        "fisc_word,timeline_word,c400_number,yr1_jan1_offset,monthday_distortion,fund_coin,penny,respect_bit,bridge,job_listen_rotations": creed_format_00000_fiscunit_v0_0_0(),
        "fisc_word,owner_name,deal_time,quota,celldepth": creed_format_00001_fisc_dealunit_v0_0_0(),
        "fisc_word,owner_name,acct_name,tran_time,amount": creed_format_00002_fisc_cashbook_v0_0_0(),
        "fisc_word,cumlative_minute,hour_word": creed_format_00003_fisc_timeline_hour_v0_0_0(),
        "fisc_word,cumlative_day,month_word": creed_format_00004_fisc_timeline_month_v0_0_0(),
        "fisc_word,weekday_order,weekday_word": creed_format_00005_fisc_timeline_weekday_v0_0_0(),
        "fisc_word,offi_time": creed_format_00006_fisc_timeoffi_v0_0_0(),
        "fisc_word,owner_name,acct_name": creed_format_00011_acct_v0_0_0(),
        "fisc_word,owner_name,acct_name,group_label": creed_format_00012_membership_v0_0_0(),
        "fisc_word,owner_name,idea_way,mass,pledge": creed_format_00013_ideaunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,begin,close,addin,numor,denom,morph,gogo_want,stop_want": creed_format_00019_ideaunit_v0_0_0(),
        "fisc_word,owner_name,acct_name,group_label,credit_vote,debtit_vote": creed_format_00020_bud_acct_membership_v0_0_0(),
        "fisc_word,owner_name,acct_name,credit_belief,debtit_belief": creed_format_00021_bud_acctunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,awardee_label,give_force,take_force": creed_format_00022_bud_idea_awardlink_v0_0_0(),
        "fisc_word,owner_name,idea_way,fcontext,fbranch,fopen,fnigh": creed_format_00023_bud_idea_factunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,labor_label": creed_format_00024_bud_idea_laborlink_v0_0_0(),
        "fisc_word,owner_name,idea_way,healer_name": creed_format_00025_bud_idea_healerlink_v0_0_0(),
        "fisc_word,owner_name,idea_way,rcontext,pbranch,pnigh,popen,pdivisor": creed_format_00026_bud_idea_reason_premiseunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,rcontext,rcontext_idea_active_requisite": creed_format_00027_bud_idea_reasonunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,begin,close,addin,numor,denom,morph,gogo_want,stop_want,mass,pledge,problem_bool": creed_format_00028_bud_ideaunit_v0_0_0(),
        "fisc_word,owner_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_coin,penny,respect_bit": creed_format_00029_budunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,healer_name,problem_bool": creed_format_00036_problem_healer_v0_0_0(),
        "otx_label,inx_label,otx_bridge,inx_bridge,unknown_term": creed_format_00042_pidgin_label_v0_0_0(),
        "otx_name,inx_name,otx_bridge,inx_bridge,unknown_term": creed_format_00043_pidgin_name_v0_0_0(),
        "otx_word,inx_word,otx_bridge,inx_bridge,unknown_term": creed_format_00044_pidgin_word_v0_0_0(),
        "otx_way,inx_way,otx_bridge,inx_bridge,unknown_term": creed_format_00045_pidgin_way_v0_0_0(),
        "fisc_word,owner_name,acct_name,group_label_ERASE": creed_format_00050_delete_bud_acct_membership_v0_0_0(),
        "fisc_word,owner_name,acct_name_ERASE": creed_format_00051_delete_bud_acctunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,awardee_label_ERASE": creed_format_00052_delete_bud_idea_awardlink_v0_0_0(),
        "fisc_word,owner_name,idea_way,fcontext_ERASE": creed_format_00053_delete_bud_idea_factunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,labor_label_ERASE": creed_format_00054_delete_bud_idea_laborlink_v0_0_0(),
        "fisc_word,owner_name,idea_way,healer_name_ERASE": creed_format_00055_delete_bud_idea_healerlink_v0_0_0(),
        "fisc_word,owner_name,idea_way,rcontext,pbranch_ERASE": creed_format_00056_delete_bud_idea_reason_premiseunit_v0_0_0(),
        "fisc_word,owner_name,idea_way,rcontext_ERASE": creed_format_00057_delete_bud_idea_reasonunit_v0_0_0(),
        "fisc_word,owner_name,idea_way_ERASE": creed_format_00058_delete_bud_ideaunit_v0_0_0(),
        "fisc_word,owner_name_ERASE": creed_format_00059_delete_budunit_v0_0_0(),
        "fisc_word,owner_name,acct_name,otx_name,inx_name": creed_format_00113_acct_map1_v0_0_0(),
        "fisc_word,owner_name,acct_name,otx_label,inx_label": creed_format_00115_group_map1_v0_0_0(),
        "fisc_word,owner_name,acct_name,otx_word,inx_word": creed_format_00116_word_map1_v0_0_0(),
        "fisc_word,owner_name,acct_name,otx_way,inx_way": creed_format_00117_way_map1_v0_0_0(),
    }


def get_creedref_from_file(creed_format_filename: str) -> dict:
    creedref_filename = get_json_filename(creed_format_filename)
    return open_json(get_creed_formats_dir(), creedref_filename)


def get_quick_creeds_column_ref() -> dict[str, set[str]]:
    creed_number_dict = {}
    for creed_format_filename in get_creed_format_filenames():
        creedref_dict = get_creedref_from_file(creed_format_filename)
        creed_number = creedref_dict.get("creed_number")
        creed_number_dict[creed_number] = set(creedref_dict.get("attributes").keys())
    return creed_number_dict


def get_creed_dimen_ref() -> dict[str, set[str]]:
    """dictionary with key=dimen and value=set of all creed_numbers with that dimen's data"""
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
        "bud_idea_awardlink": {"br00022", "br00052"},
        "bud_idea_factunit": {"br00023", "br00053"},
        "bud_idea_healerlink": {"br00025", "br00036", "br00055"},
        "bud_idea_reason_premiseunit": {"br00026", "br00056"},
        "bud_idea_reasonunit": {"br00026", "br00027", "br00056", "br00057"},
        "bud_idea_laborlink": {"br00024", "br00054"},
        "bud_ideaunit": {
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
        "pidgin_label": {"br00042", "br00115"},
        "pidgin_name": {"br00043", "br00113"},
        "pidgin_way": {"br00045", "br00117"},
        "pidgin_word": {"br00044", "br00116"},
    }
