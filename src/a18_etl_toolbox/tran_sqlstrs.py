from sqlite3 import Connection as sqlite3_Connection
from src.a00_data_toolbox.db_toolbox import (
    create_table2table_agg_insert_query,
    create_update_inconsistency_error_query,
)
from src.a17_idea_logic.idea_config import (
    get_idea_config_dict,
    get_quick_ideas_column_ref,
)
from src.a17_idea_logic.idea_db_tool import (
    create_idea_sorted_table,
    get_default_sorted_list,
)

ALL_DIMEN_ABBV7 = {
    "VOWPAYY",
    "VOWDEAL",
    "VOWHOUR",
    "VOWMONT",
    "VOWWEEK",
    "VOWOFFI",
    "VOWUNIT",
    "PLNMEMB",
    "PLNACCT",
    "PLNAWAR",
    "PLNFACT",
    "PLNHEAL",
    "PLNPREM",
    "PLNREAS",
    "PLNLABO",
    "PLNCONC",
    "PLANUNIT",
    "PIDTITL",
    "PIDNAME",
    "PIDWAYY",
    "PIDLABE",
}


def get_dimen_abbv7(dimen: str) -> str:
    return {
        "vow_paybook": "VOWPAYY",
        "vow_dealunit": "VOWDEAL",
        "vow_timeline_hour": "VOWHOUR",
        "vow_timeline_month": "VOWMONT",
        "vow_timeline_weekday": "VOWWEEK",
        "vow_timeoffi": "VOWOFFI",
        "vowunit": "VOWUNIT",
        "plan_acct_membership": "PLNMEMB",
        "plan_acctunit": "PLNACCT",
        "plan_concept_awardlink": "PLNAWAR",
        "plan_concept_factunit": "PLNFACT",
        "plan_concept_healerlink": "PLNHEAL",
        "plan_concept_reason_premiseunit": "PLNPREM",
        "plan_concept_reasonunit": "PLNREAS",
        "plan_concept_laborlink": "PLNLABO",
        "plan_conceptunit": "PLNCONC",
        "planunit": "PLANUNIT",
        "pidgin_title": "PIDTITL",
        "pidgin_name": "PIDNAME",
        "pidgin_way": "PIDWAYY",
        "pidgin_label": "PIDLABE",
        "pidgin_core": "PIDCORE",
    }.get(dimen)


class prime_tablenameException(Exception):
    pass


def create_prime_tablename(
    idea_dimen_or_abbv7: str, phase: str, stage: str, put_del: str = None
) -> str:
    """
    phase must be one: 's', 'v', 'job'
    stage must be one: 'raw', 'agg', 'vld'
    """

    abbv_references = {
        "VOWPAYY": "vow_paybook",
        "VOWDEAL": "vow_dealunit",
        "VOWHOUR": "vow_timeline_hour",
        "VOWMONT": "vow_timeline_month",
        "VOWWEEK": "vow_timeline_weekday",
        "VOWOFFI": "vow_timeoffi",
        "VOWUNIT": "vowunit",
        "PLNMEMB": "plan_acct_membership",
        "PLNACCT": "plan_acctunit",
        "PLNAWAR": "plan_concept_awardlink",
        "PLNFACT": "plan_concept_factunit",
        "PLNGROU": "plan_groupunit",
        "PLNHEAL": "plan_concept_healerlink",
        "PLNPREM": "plan_concept_reason_premiseunit",
        "PLNREAS": "plan_concept_reasonunit",
        "PLNLABO": "plan_concept_laborlink",
        "PLNCONC": "plan_conceptunit",
        "PLANUNIT": "planunit",
        "PIDTITL": "pidgin_title",
        "PIDNAME": "pidgin_name",
        "PIDWAYY": "pidgin_way",
        "PIDLABE": "pidgin_label",
        "PIDCORE": "pidgin_core",
    }
    tablename = idea_dimen_or_abbv7
    if abbv_references.get(idea_dimen_or_abbv7.upper()):
        tablename = abbv_references.get(idea_dimen_or_abbv7.upper())
    if phase in {"s", "v", "job"}:
        tablename = f"{tablename}_{phase}"
    if stage is None:
        return tablename
    if stage not in {"raw", "agg", "vld"}:
        raise prime_tablenameException(f"'{stage}' is not a valid stage")

    return f"{tablename}_{put_del}_{stage}" if put_del else f"{tablename}_{stage}"


CREATE_PIDTITL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDTITL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_agg (event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDTITL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_vld (event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT)"""
CREATE_PIDNAME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_agg (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_vld (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT)"""
CREATE_PIDWAYY_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDWAYY_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_agg (event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDWAYY_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_vld (event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT)"""
CREATE_PIDLABE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_agg (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_vld (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT)"""

CREATE_PIDCORE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_raw (source_dimen TEXT, face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDCORE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_agg (face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT)"""
CREATE_PIDCORE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_vld (face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_str TEXT)"""

CREATE_VOWPAYY_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_paybook_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_VOWPAYY_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_paybook_s_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_VOWPAYY_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_paybook_s_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_VOWPAYY_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_paybook_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_VOWPAYY_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_paybook_v_agg (vow_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_VOWDEAL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_dealunit_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_VOWDEAL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_dealunit_s_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_VOWDEAL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_dealunit_s_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_VOWDEAL_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_dealunit_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_VOWDEAL_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_dealunit_v_agg (vow_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_VOWHOUR_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_hour_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, cumlative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_VOWHOUR_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_hour_s_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, cumlative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_VOWHOUR_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_hour_s_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, cumlative_minute INTEGER, hour_label TEXT)"""
CREATE_VOWHOUR_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_hour_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, cumlative_minute INTEGER, hour_label_otx TEXT, hour_label_inx TEXT, error_message TEXT)"""
CREATE_VOWHOUR_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_hour_v_agg (vow_label TEXT, cumlative_minute INTEGER, hour_label TEXT)"""
CREATE_VOWMONT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_month_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, cumlative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_VOWMONT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_month_s_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, cumlative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_VOWMONT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_month_s_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, cumlative_day INTEGER, month_label TEXT)"""
CREATE_VOWMONT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_month_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, cumlative_day INTEGER, month_label_otx TEXT, month_label_inx TEXT, error_message TEXT)"""
CREATE_VOWMONT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_month_v_agg (vow_label TEXT, cumlative_day INTEGER, month_label TEXT)"""
CREATE_VOWWEEK_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_weekday_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_VOWWEEK_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_weekday_s_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_VOWWEEK_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_weekday_s_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_VOWWEEK_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_weekday_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, weekday_order INTEGER, weekday_label_otx TEXT, weekday_label_inx TEXT, error_message TEXT)"""
CREATE_VOWWEEK_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeline_weekday_v_agg (vow_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_VOWOFFI_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeoffi_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_VOWOFFI_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeoffi_s_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_VOWOFFI_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeoffi_s_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, offi_time INTEGER)"""
CREATE_VOWOFFI_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeoffi_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_VOWOFFI_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vow_timeoffi_v_agg (vow_label TEXT, offi_time INTEGER)"""
CREATE_VOWUNIT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vowunit_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_VOWUNIT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vowunit_s_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_VOWUNIT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS vowunit_s_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""
CREATE_VOWUNIT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS vowunit_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, timeline_label_otx TEXT, timeline_label_inx TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_VOWUNIT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS vowunit_v_agg (vow_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""

CREATE_PLNMEMB_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debt_vote REAL, error_message TEXT)"
CREATE_PLNMEMB_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debt_vote REAL, error_message TEXT)"
CREATE_PLNMEMB_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debt_vote REAL)"
CREATE_PLNMEMB_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT)"
CREATE_PLNMEMB_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT, error_message TEXT)"
CREATE_PLNMEMB_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT)"
CREATE_PLNMEMB_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, group_title_otx TEXT, group_title_inx TEXT, credit_vote REAL, debt_vote REAL)"
CREATE_PLNMEMB_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debt_vote REAL)"
CREATE_PLNMEMB_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, group_title_ERASE_otx TEXT, group_title_ERASE_inx TEXT)"
CREATE_PLNMEMB_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_acct_membership_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT)"
CREATE_PLNACCT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, credit_score REAL, debt_score REAL, error_message TEXT)"
CREATE_PLNACCT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, credit_score REAL, debt_score REAL, error_message TEXT)"
CREATE_PLNACCT_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, credit_score REAL, debt_score REAL)"
CREATE_PLNACCT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_PLNACCT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name_ERASE TEXT, error_message TEXT)"
CREATE_PLNACCT_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_PLNACCT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, credit_score REAL, debt_score REAL)"
CREATE_PLNACCT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name TEXT, credit_score REAL, debt_score REAL)"
CREATE_PLNACCT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_ERASE_otx TEXT, acct_name_ERASE_inx TEXT)"
CREATE_PLNACCT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_acctunit_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_PLNAWAR_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_PLNAWAR_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_PLNAWAR_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_PLNAWAR_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT)"
CREATE_PLNAWAR_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT, error_message TEXT)"
CREATE_PLNAWAR_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT)"
CREATE_PLNAWAR_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, awardee_title_otx TEXT, awardee_title_inx TEXT, give_force REAL, take_force REAL)"
CREATE_PLNAWAR_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_PLNAWAR_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, awardee_title_ERASE_otx TEXT, awardee_title_ERASE_inx TEXT)"
CREATE_PLNAWAR_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_awardlink_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT)"
CREATE_PLNFACT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fstate TEXT, fopen REAL, fnigh REAL, error_message TEXT)"
CREATE_PLNFACT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fstate TEXT, fopen REAL, fnigh REAL, error_message TEXT)"
CREATE_PLNFACT_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fstate TEXT, fopen REAL, fnigh REAL)"
CREATE_PLNFACT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT)"
CREATE_PLNFACT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT, error_message TEXT)"
CREATE_PLNFACT_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT)"
CREATE_PLNFACT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, fcontext_otx TEXT, fcontext_inx TEXT, fstate_otx TEXT, fstate_inx TEXT, fopen REAL, fnigh REAL)"
CREATE_PLNFACT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fstate TEXT, fopen REAL, fnigh REAL)"
CREATE_PLNFACT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, fcontext_ERASE_otx TEXT, fcontext_ERASE_inx TEXT)"
CREATE_PLNFACT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_factunit_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT)"
CREATE_PLNHEAL_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT, error_message TEXT)"
CREATE_PLNHEAL_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT, error_message TEXT)"
CREATE_PLNHEAL_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT)"
CREATE_PLNHEAL_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT)"
CREATE_PLNHEAL_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT, error_message TEXT)"
CREATE_PLNHEAL_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT)"
CREATE_PLNHEAL_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, healer_name_otx TEXT, healer_name_inx TEXT)"
CREATE_PLNHEAL_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT)"
CREATE_PLNHEAL_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, healer_name_ERASE_otx TEXT, healer_name_ERASE_inx TEXT)"
CREATE_PLNHEAL_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_healerlink_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT)"
CREATE_PLNPREM_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate TEXT, pnigh REAL, popen REAL, pdivisor INTEGER, error_message TEXT)"
CREATE_PLNPREM_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate TEXT, pnigh REAL, popen REAL, pdivisor INTEGER, error_message TEXT)"
CREATE_PLNPREM_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_PLNPREM_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate_ERASE TEXT)"
CREATE_PLNPREM_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate_ERASE TEXT, error_message TEXT)"
CREATE_PLNPREM_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate_ERASE TEXT)"
CREATE_PLNPREM_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, pstate_otx TEXT, pstate_inx TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_PLNPREM_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_PLNPREM_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, pstate_ERASE_otx TEXT, pstate_ERASE_inx TEXT)"
CREATE_PLNPREM_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate_ERASE TEXT)"
CREATE_PLNREAS_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rconcept_active_requisite INTEGER, error_message TEXT)"
CREATE_PLNREAS_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rconcept_active_requisite INTEGER, error_message TEXT)"
CREATE_PLNREAS_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rconcept_active_requisite INTEGER)"
CREATE_PLNREAS_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT)"
CREATE_PLNREAS_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT, error_message TEXT)"
CREATE_PLNREAS_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT)"
CREATE_PLNREAS_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, rconcept_active_requisite INTEGER)"
CREATE_PLNREAS_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rconcept_active_requisite INTEGER)"
CREATE_PLNREAS_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, rcontext_ERASE_otx TEXT, rcontext_ERASE_inx TEXT)"
CREATE_PLNREAS_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT)"
CREATE_PLNLABO_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT, error_message TEXT)"
CREATE_PLNLABO_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT, error_message TEXT)"
CREATE_PLNLABO_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT)"
CREATE_PLNLABO_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT)"
CREATE_PLNLABO_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT, error_message TEXT)"
CREATE_PLNLABO_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT)"
CREATE_PLNLABO_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, labor_title_otx TEXT, labor_title_inx TEXT)"
CREATE_PLNLABO_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT)"
CREATE_PLNLABO_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, labor_title_ERASE_otx TEXT, labor_title_ERASE_inx TEXT)"
CREATE_PLNLABO_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_concept_laborlink_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT)"
CREATE_PLNCONC_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, task INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_PLNCONC_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, task INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_PLNCONC_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, task INTEGER, problem_bool INTEGER)"
CREATE_PLNCONC_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way_ERASE TEXT)"
CREATE_PLNCONC_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way_ERASE TEXT, error_message TEXT)"
CREATE_PLNCONC_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way_ERASE TEXT)"
CREATE_PLNCONC_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, task INTEGER, problem_bool INTEGER)"
CREATE_PLNCONC_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, task INTEGER, problem_bool INTEGER)"
CREATE_PLNCONC_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_ERASE_otx TEXT, concept_way_ERASE_inx TEXT)"
CREATE_PLNCONC_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS plan_conceptunit_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, concept_way_ERASE TEXT)"
CREATE_PLANUNIT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS planunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, error_message TEXT)"
CREATE_PLANUNIT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS planunit_s_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, error_message TEXT)"
CREATE_PLANUNIT_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS planunit_s_put_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL)"
CREATE_PLANUNIT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS planunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name_ERASE TEXT)"
CREATE_PLANUNIT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS planunit_s_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name_ERASE TEXT, error_message TEXT)"
CREATE_PLANUNIT_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS planunit_s_del_vld (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name_ERASE TEXT)"
CREATE_PLANUNIT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS planunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL)"
CREATE_PLANUNIT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS planunit_v_put_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL)"
CREATE_PLANUNIT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS planunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, vow_label_otx TEXT, vow_label_inx TEXT, owner_name_ERASE_otx TEXT, owner_name_ERASE_inx TEXT)"
CREATE_PLANUNIT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS planunit_v_del_agg (event_int INTEGER, face_name TEXT, vow_label TEXT, owner_name_ERASE TEXT)"


def get_prime_create_table_sqlstrs() -> dict[str:str]:
    return {
        "pidgin_title_s_raw": CREATE_PIDTITL_SOUND_RAW_SQLSTR,
        "pidgin_title_s_agg": CREATE_PIDTITL_SOUND_AGG_SQLSTR,
        "pidgin_title_s_vld": CREATE_PIDTITL_SOUND_VLD_SQLSTR,
        "pidgin_name_s_raw": CREATE_PIDNAME_SOUND_RAW_SQLSTR,
        "pidgin_name_s_agg": CREATE_PIDNAME_SOUND_AGG_SQLSTR,
        "pidgin_name_s_vld": CREATE_PIDNAME_SOUND_VLD_SQLSTR,
        "pidgin_way_s_raw": CREATE_PIDWAYY_SOUND_RAW_SQLSTR,
        "pidgin_way_s_agg": CREATE_PIDWAYY_SOUND_AGG_SQLSTR,
        "pidgin_way_s_vld": CREATE_PIDWAYY_SOUND_VLD_SQLSTR,
        "pidgin_label_s_raw": CREATE_PIDLABE_SOUND_RAW_SQLSTR,
        "pidgin_label_s_agg": CREATE_PIDLABE_SOUND_AGG_SQLSTR,
        "pidgin_label_s_vld": CREATE_PIDLABE_SOUND_VLD_SQLSTR,
        "pidgin_core_s_raw": CREATE_PIDCORE_SOUND_RAW_SQLSTR,
        "pidgin_core_s_agg": CREATE_PIDCORE_SOUND_AGG_SQLSTR,
        "pidgin_core_s_vld": CREATE_PIDCORE_SOUND_VLD_SQLSTR,
        "vow_paybook_s_raw": CREATE_VOWPAYY_SOUND_RAW_SQLSTR,
        "vow_paybook_s_agg": CREATE_VOWPAYY_SOUND_AGG_SQLSTR,
        "vow_paybook_s_vld": CREATE_VOWPAYY_SOUND_VLD_SQLSTR,
        "vow_paybook_v_raw": CREATE_VOWPAYY_VOICE_RAW_SQLSTR,
        "vow_paybook_v_agg": CREATE_VOWPAYY_VOICE_AGG_SQLSTR,
        "vow_dealunit_s_raw": CREATE_VOWDEAL_SOUND_RAW_SQLSTR,
        "vow_dealunit_s_agg": CREATE_VOWDEAL_SOUND_AGG_SQLSTR,
        "vow_dealunit_s_vld": CREATE_VOWDEAL_SOUND_VLD_SQLSTR,
        "vow_dealunit_v_raw": CREATE_VOWDEAL_VOICE_RAW_SQLSTR,
        "vow_dealunit_v_agg": CREATE_VOWDEAL_VOICE_AGG_SQLSTR,
        "vow_timeline_hour_s_raw": CREATE_VOWHOUR_SOUND_RAW_SQLSTR,
        "vow_timeline_hour_s_agg": CREATE_VOWHOUR_SOUND_AGG_SQLSTR,
        "vow_timeline_hour_s_vld": CREATE_VOWHOUR_SOUND_VLD_SQLSTR,
        "vow_timeline_hour_v_raw": CREATE_VOWHOUR_VOICE_RAW_SQLSTR,
        "vow_timeline_hour_v_agg": CREATE_VOWHOUR_VOICE_AGG_SQLSTR,
        "vow_timeline_month_s_raw": CREATE_VOWMONT_SOUND_RAW_SQLSTR,
        "vow_timeline_month_s_agg": CREATE_VOWMONT_SOUND_AGG_SQLSTR,
        "vow_timeline_month_s_vld": CREATE_VOWMONT_SOUND_VLD_SQLSTR,
        "vow_timeline_month_v_raw": CREATE_VOWMONT_VOICE_RAW_SQLSTR,
        "vow_timeline_month_v_agg": CREATE_VOWMONT_VOICE_AGG_SQLSTR,
        "vow_timeline_weekday_s_raw": CREATE_VOWWEEK_SOUND_RAW_SQLSTR,
        "vow_timeline_weekday_s_agg": CREATE_VOWWEEK_SOUND_AGG_SQLSTR,
        "vow_timeline_weekday_s_vld": CREATE_VOWWEEK_SOUND_VLD_SQLSTR,
        "vow_timeline_weekday_v_raw": CREATE_VOWWEEK_VOICE_RAW_SQLSTR,
        "vow_timeline_weekday_v_agg": CREATE_VOWWEEK_VOICE_AGG_SQLSTR,
        "vow_timeoffi_s_raw": CREATE_VOWOFFI_SOUND_RAW_SQLSTR,
        "vow_timeoffi_s_agg": CREATE_VOWOFFI_SOUND_AGG_SQLSTR,
        "vow_timeoffi_s_vld": CREATE_VOWOFFI_SOUND_VLD_SQLSTR,
        "vow_timeoffi_v_raw": CREATE_VOWOFFI_VOICE_RAW_SQLSTR,
        "vow_timeoffi_v_agg": CREATE_VOWOFFI_VOICE_AGG_SQLSTR,
        "vowunit_s_raw": CREATE_VOWUNIT_SOUND_RAW_SQLSTR,
        "vowunit_s_agg": CREATE_VOWUNIT_SOUND_AGG_SQLSTR,
        "vowunit_s_vld": CREATE_VOWUNIT_SOUND_VLD_SQLSTR,
        "vowunit_v_raw": CREATE_VOWUNIT_VOICE_RAW_SQLSTR,
        "vowunit_v_agg": CREATE_VOWUNIT_VOICE_AGG_SQLSTR,
        "plan_acct_membership_s_put_raw": CREATE_PLNMEMB_SOUND_PUT_RAW_STR,
        "plan_acct_membership_s_put_agg": CREATE_PLNMEMB_SOUND_PUT_AGG_STR,
        "plan_acct_membership_s_put_vld": CREATE_PLNMEMB_SOUND_PUT_VLD_STR,
        "plan_acct_membership_s_del_raw": CREATE_PLNMEMB_SOUND_DEL_RAW_STR,
        "plan_acct_membership_s_del_agg": CREATE_PLNMEMB_SOUND_DEL_AGG_STR,
        "plan_acct_membership_s_del_vld": CREATE_PLNMEMB_SOUND_DEL_VLD_STR,
        "plan_acct_membership_v_put_raw": CREATE_PLNMEMB_VOICE_PUT_RAW_STR,
        "plan_acct_membership_v_put_agg": CREATE_PLNMEMB_VOICE_PUT_AGG_STR,
        "plan_acct_membership_v_del_raw": CREATE_PLNMEMB_VOICE_DEL_RAW_STR,
        "plan_acct_membership_v_del_agg": CREATE_PLNMEMB_VOICE_DEL_AGG_STR,
        "plan_acctunit_s_put_raw": CREATE_PLNACCT_SOUND_PUT_RAW_STR,
        "plan_acctunit_s_put_agg": CREATE_PLNACCT_SOUND_PUT_AGG_STR,
        "plan_acctunit_s_put_vld": CREATE_PLNACCT_SOUND_PUT_VLD_STR,
        "plan_acctunit_s_del_raw": CREATE_PLNACCT_SOUND_DEL_RAW_STR,
        "plan_acctunit_s_del_agg": CREATE_PLNACCT_SOUND_DEL_AGG_STR,
        "plan_acctunit_s_del_vld": CREATE_PLNACCT_SOUND_DEL_VLD_STR,
        "plan_acctunit_v_put_raw": CREATE_PLNACCT_VOICE_PUT_RAW_STR,
        "plan_acctunit_v_put_agg": CREATE_PLNACCT_VOICE_PUT_AGG_STR,
        "plan_acctunit_v_del_raw": CREATE_PLNACCT_VOICE_DEL_RAW_STR,
        "plan_acctunit_v_del_agg": CREATE_PLNACCT_VOICE_DEL_AGG_STR,
        "plan_concept_awardlink_s_put_raw": CREATE_PLNAWAR_SOUND_PUT_RAW_STR,
        "plan_concept_awardlink_s_put_agg": CREATE_PLNAWAR_SOUND_PUT_AGG_STR,
        "plan_concept_awardlink_s_put_vld": CREATE_PLNAWAR_SOUND_PUT_VLD_STR,
        "plan_concept_awardlink_s_del_raw": CREATE_PLNAWAR_SOUND_DEL_RAW_STR,
        "plan_concept_awardlink_s_del_agg": CREATE_PLNAWAR_SOUND_DEL_AGG_STR,
        "plan_concept_awardlink_s_del_vld": CREATE_PLNAWAR_SOUND_DEL_VLD_STR,
        "plan_concept_awardlink_v_put_raw": CREATE_PLNAWAR_VOICE_PUT_RAW_STR,
        "plan_concept_awardlink_v_put_agg": CREATE_PLNAWAR_VOICE_PUT_AGG_STR,
        "plan_concept_awardlink_v_del_raw": CREATE_PLNAWAR_VOICE_DEL_RAW_STR,
        "plan_concept_awardlink_v_del_agg": CREATE_PLNAWAR_VOICE_DEL_AGG_STR,
        "plan_concept_factunit_s_put_raw": CREATE_PLNFACT_SOUND_PUT_RAW_STR,
        "plan_concept_factunit_s_put_agg": CREATE_PLNFACT_SOUND_PUT_AGG_STR,
        "plan_concept_factunit_s_put_vld": CREATE_PLNFACT_SOUND_PUT_VLD_STR,
        "plan_concept_factunit_s_del_raw": CREATE_PLNFACT_SOUND_DEL_RAW_STR,
        "plan_concept_factunit_s_del_agg": CREATE_PLNFACT_SOUND_DEL_AGG_STR,
        "plan_concept_factunit_s_del_vld": CREATE_PLNFACT_SOUND_DEL_VLD_STR,
        "plan_concept_factunit_v_put_raw": CREATE_PLNFACT_VOICE_PUT_RAW_STR,
        "plan_concept_factunit_v_put_agg": CREATE_PLNFACT_VOICE_PUT_AGG_STR,
        "plan_concept_factunit_v_del_raw": CREATE_PLNFACT_VOICE_DEL_RAW_STR,
        "plan_concept_factunit_v_del_agg": CREATE_PLNFACT_VOICE_DEL_AGG_STR,
        "plan_concept_healerlink_s_put_raw": CREATE_PLNHEAL_SOUND_PUT_RAW_STR,
        "plan_concept_healerlink_s_put_agg": CREATE_PLNHEAL_SOUND_PUT_AGG_STR,
        "plan_concept_healerlink_s_put_vld": CREATE_PLNHEAL_SOUND_PUT_VLD_STR,
        "plan_concept_healerlink_s_del_raw": CREATE_PLNHEAL_SOUND_DEL_RAW_STR,
        "plan_concept_healerlink_s_del_agg": CREATE_PLNHEAL_SOUND_DEL_AGG_STR,
        "plan_concept_healerlink_s_del_vld": CREATE_PLNHEAL_SOUND_DEL_VLD_STR,
        "plan_concept_healerlink_v_put_raw": CREATE_PLNHEAL_VOICE_PUT_RAW_STR,
        "plan_concept_healerlink_v_put_agg": CREATE_PLNHEAL_VOICE_PUT_AGG_STR,
        "plan_concept_healerlink_v_del_raw": CREATE_PLNHEAL_VOICE_DEL_RAW_STR,
        "plan_concept_healerlink_v_del_agg": CREATE_PLNHEAL_VOICE_DEL_AGG_STR,
        "plan_concept_reason_premiseunit_s_put_raw": CREATE_PLNPREM_SOUND_PUT_RAW_STR,
        "plan_concept_reason_premiseunit_s_put_agg": CREATE_PLNPREM_SOUND_PUT_AGG_STR,
        "plan_concept_reason_premiseunit_s_put_vld": CREATE_PLNPREM_SOUND_PUT_VLD_STR,
        "plan_concept_reason_premiseunit_s_del_raw": CREATE_PLNPREM_SOUND_DEL_RAW_STR,
        "plan_concept_reason_premiseunit_s_del_agg": CREATE_PLNPREM_SOUND_DEL_AGG_STR,
        "plan_concept_reason_premiseunit_s_del_vld": CREATE_PLNPREM_SOUND_DEL_VLD_STR,
        "plan_concept_reason_premiseunit_v_put_raw": CREATE_PLNPREM_VOICE_PUT_RAW_STR,
        "plan_concept_reason_premiseunit_v_put_agg": CREATE_PLNPREM_VOICE_PUT_AGG_STR,
        "plan_concept_reason_premiseunit_v_del_raw": CREATE_PLNPREM_VOICE_DEL_RAW_STR,
        "plan_concept_reason_premiseunit_v_del_agg": CREATE_PLNPREM_VOICE_DEL_AGG_STR,
        "plan_concept_reasonunit_s_put_raw": CREATE_PLNREAS_SOUND_PUT_RAW_STR,
        "plan_concept_reasonunit_s_put_agg": CREATE_PLNREAS_SOUND_PUT_AGG_STR,
        "plan_concept_reasonunit_s_put_vld": CREATE_PLNREAS_SOUND_PUT_VLD_STR,
        "plan_concept_reasonunit_s_del_raw": CREATE_PLNREAS_SOUND_DEL_RAW_STR,
        "plan_concept_reasonunit_s_del_agg": CREATE_PLNREAS_SOUND_DEL_AGG_STR,
        "plan_concept_reasonunit_s_del_vld": CREATE_PLNREAS_SOUND_DEL_VLD_STR,
        "plan_concept_reasonunit_v_put_raw": CREATE_PLNREAS_VOICE_PUT_RAW_STR,
        "plan_concept_reasonunit_v_put_agg": CREATE_PLNREAS_VOICE_PUT_AGG_STR,
        "plan_concept_reasonunit_v_del_raw": CREATE_PLNREAS_VOICE_DEL_RAW_STR,
        "plan_concept_reasonunit_v_del_agg": CREATE_PLNREAS_VOICE_DEL_AGG_STR,
        "plan_concept_laborlink_s_put_raw": CREATE_PLNLABO_SOUND_PUT_RAW_STR,
        "plan_concept_laborlink_s_put_agg": CREATE_PLNLABO_SOUND_PUT_AGG_STR,
        "plan_concept_laborlink_s_put_vld": CREATE_PLNLABO_SOUND_PUT_VLD_STR,
        "plan_concept_laborlink_s_del_raw": CREATE_PLNLABO_SOUND_DEL_RAW_STR,
        "plan_concept_laborlink_s_del_agg": CREATE_PLNLABO_SOUND_DEL_AGG_STR,
        "plan_concept_laborlink_s_del_vld": CREATE_PLNLABO_SOUND_DEL_VLD_STR,
        "plan_concept_laborlink_v_put_raw": CREATE_PLNLABO_VOICE_PUT_RAW_STR,
        "plan_concept_laborlink_v_put_agg": CREATE_PLNLABO_VOICE_PUT_AGG_STR,
        "plan_concept_laborlink_v_del_raw": CREATE_PLNLABO_VOICE_DEL_RAW_STR,
        "plan_concept_laborlink_v_del_agg": CREATE_PLNLABO_VOICE_DEL_AGG_STR,
        "plan_conceptunit_s_put_raw": CREATE_PLNCONC_SOUND_PUT_RAW_STR,
        "plan_conceptunit_s_put_agg": CREATE_PLNCONC_SOUND_PUT_AGG_STR,
        "plan_conceptunit_s_put_vld": CREATE_PLNCONC_SOUND_PUT_VLD_STR,
        "plan_conceptunit_s_del_raw": CREATE_PLNCONC_SOUND_DEL_RAW_STR,
        "plan_conceptunit_s_del_agg": CREATE_PLNCONC_SOUND_DEL_AGG_STR,
        "plan_conceptunit_s_del_vld": CREATE_PLNCONC_SOUND_DEL_VLD_STR,
        "plan_conceptunit_v_put_raw": CREATE_PLNCONC_VOICE_PUT_RAW_STR,
        "plan_conceptunit_v_put_agg": CREATE_PLNCONC_VOICE_PUT_AGG_STR,
        "plan_conceptunit_v_del_raw": CREATE_PLNCONC_VOICE_DEL_RAW_STR,
        "plan_conceptunit_v_del_agg": CREATE_PLNCONC_VOICE_DEL_AGG_STR,
        "planunit_s_put_raw": CREATE_PLANUNIT_SOUND_PUT_RAW_STR,
        "planunit_s_put_agg": CREATE_PLANUNIT_SOUND_PUT_AGG_STR,
        "planunit_s_put_vld": CREATE_PLANUNIT_SOUND_PUT_VLD_STR,
        "planunit_s_del_raw": CREATE_PLANUNIT_SOUND_DEL_RAW_STR,
        "planunit_s_del_agg": CREATE_PLANUNIT_SOUND_DEL_AGG_STR,
        "planunit_s_del_vld": CREATE_PLANUNIT_SOUND_DEL_VLD_STR,
        "planunit_v_put_raw": CREATE_PLANUNIT_VOICE_PUT_RAW_STR,
        "planunit_v_put_agg": CREATE_PLANUNIT_VOICE_PUT_AGG_STR,
        "planunit_v_del_raw": CREATE_PLANUNIT_VOICE_DEL_RAW_STR,
        "planunit_v_del_agg": CREATE_PLANUNIT_VOICE_DEL_AGG_STR,
    }


def get_vow_plan_sound_agg_tablenames():
    return {
        "plan_acct_membership_s_del_agg",
        "plan_acct_membership_s_put_agg",
        "plan_acctunit_s_del_agg",
        "plan_acctunit_s_put_agg",
        "plan_concept_awardlink_s_del_agg",
        "plan_concept_awardlink_s_put_agg",
        "plan_concept_factunit_s_del_agg",
        "plan_concept_factunit_s_put_agg",
        "plan_concept_healerlink_s_del_agg",
        "plan_concept_healerlink_s_put_agg",
        "plan_concept_laborlink_s_del_agg",
        "plan_concept_laborlink_s_put_agg",
        "plan_concept_reason_premiseunit_s_del_agg",
        "plan_concept_reason_premiseunit_s_put_agg",
        "plan_concept_reasonunit_s_del_agg",
        "plan_concept_reasonunit_s_put_agg",
        "plan_conceptunit_s_del_agg",
        "plan_conceptunit_s_put_agg",
        "planunit_s_del_agg",
        "planunit_s_put_agg",
        "vow_paybook_s_agg",
        "vow_dealunit_s_agg",
        "vow_timeline_hour_s_agg",
        "vow_timeline_month_s_agg",
        "vow_timeline_weekday_s_agg",
        "vow_timeoffi_s_agg",
        "vowunit_s_agg",
    }


def get_plan_voice_agg_tablenames() -> set[str]:
    return {
        "planunit_v_put_agg",
        "plan_concept_healerlink_v_put_agg",
        "plan_acctunit_v_put_agg",
        "plan_concept_reason_premiseunit_v_put_agg",
        "plan_concept_laborlink_v_put_agg",
        "plan_concept_reasonunit_v_put_agg",
        "plan_concept_factunit_v_put_agg",
        "plan_acct_membership_v_put_agg",
        "plan_conceptunit_v_put_agg",
        "plan_concept_awardlink_v_put_agg",
    }


def create_sound_and_voice_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_prime_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_all_idea_tables(conn_or_cursor: sqlite3_Connection):
    idea_refs = get_quick_ideas_column_ref()
    for idea_number, idea_columns in idea_refs.items():
        x_tablename = f"{idea_number}_raw"
        create_idea_sorted_table(conn_or_cursor, x_tablename, idea_columns)


def create_sound_raw_update_inconsist_error_message_sqlstr(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    if dimen.lower().startswith("vow"):
        exclude_cols = {"idea_number", "event_int", "face_name", "error_message"}
    else:
        exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("plan"):
        x_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        x_tablename = create_prime_tablename(dimen, "s", "raw")
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())
    return create_update_inconsistency_error_query(
        conn_or_cursor, x_tablename, dimen_focus_columns, exclude_cols
    )


def create_sound_agg_insert_sqlstrs(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())

    if dimen.lower().startswith("vow"):
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("plan"):
        agg_tablename = create_prime_tablename(dimen, "s", "agg", "put")
        raw_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        raw_tablename = create_prime_tablename(dimen, "s", "raw")
        agg_tablename = create_prime_tablename(dimen, "s", "agg")

    pidgin_vow_plan_put_sqlstr = create_table2table_agg_insert_query(
        conn_or_cursor,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
    )
    sqlstrs = [pidgin_vow_plan_put_sqlstr]
    if dimen.lower().startswith("plan"):
        del_raw_tablename = create_prime_tablename(dimen, "s", "raw", "del")
        del_agg_tablename = create_prime_tablename(dimen, "s", "agg", "del")
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
        last_element = dimen_focus_columns.pop(-1)
        dimen_focus_columns.append(f"{last_element}_ERASE")
        plan_del_sqlstr = create_table2table_agg_insert_query(
            conn_or_cursor,
            src_table=del_raw_tablename,
            dst_table=del_agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
            where_block="",
        )
        sqlstrs.append(plan_del_sqlstr)

    return sqlstrs


def create_insert_into_pidgin_core_raw_sqlstr(dimen: str) -> str:
    pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
    pidgin_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    return f"""INSERT INTO {pidgin_core_s_raw_tablename} (source_dimen, face_name, otx_bridge, inx_bridge, unknown_str)
SELECT '{pidgin_s_agg_tablename}', face_name, otx_bridge, inx_bridge, unknown_str
FROM {pidgin_s_agg_tablename}
GROUP BY face_name, otx_bridge, inx_bridge, unknown_str
;
"""


def create_insert_pidgin_core_agg_into_vld_sqlstr(
    default_bridge: str, default_unknown: str
):
    return f"""INSERT INTO pidgin_core_s_vld (face_name, otx_bridge, inx_bridge, unknown_str)
SELECT
  face_name
, IFNULL(otx_bridge, '{default_bridge}')
, IFNULL(inx_bridge, '{default_bridge}')
, IFNULL(unknown_str, '{default_unknown}')
FROM pidgin_core_s_agg
;
"""


def create_insert_missing_face_name_into_pidgin_core_vld_sqlstr(
    default_bridge: str, default_unknown: str, vow_plan_sound_agg_tablename: str
):
    return f"""INSERT INTO pidgin_core_s_vld (face_name, otx_bridge, inx_bridge, unknown_str)
SELECT
  {vow_plan_sound_agg_tablename}.face_name
, '{default_bridge}'
, '{default_bridge}'
, '{default_unknown}'
FROM {vow_plan_sound_agg_tablename} 
LEFT JOIN pidgin_core_s_vld ON pidgin_core_s_vld.face_name = {vow_plan_sound_agg_tablename}.face_name
WHERE pidgin_core_s_vld.face_name IS NULL
GROUP BY {vow_plan_sound_agg_tablename}.face_name
;
"""


def create_update_pidgin_sound_agg_inconsist_sqlstr(dimen: str) -> str:
    pidgin_core_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidgin_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    return f"""UPDATE {pidgin_s_agg_tablename}
SET error_message = 'Inconsistent pidgin core data'
WHERE face_name IN (
    SELECT {pidgin_s_agg_tablename}.face_name
    FROM {pidgin_s_agg_tablename} 
    LEFT JOIN {pidgin_core_s_vld_tablename} ON {pidgin_core_s_vld_tablename}.face_name = {pidgin_s_agg_tablename}.face_name
    WHERE {pidgin_core_s_vld_tablename}.face_name IS NULL
)
;
"""


def create_update_pidlabe_sound_agg_bridge_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidlabe_s_agg_tablename = create_prime_tablename("pidlabe", "s", "agg")
    return f"""UPDATE {pidlabe_s_agg_tablename}
SET error_message = 'Bridge cannot exist in LabelTerm'
WHERE rowid IN (
    SELECT label_agg.rowid
    FROM {pidlabe_s_agg_tablename} label_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = label_agg.face_name
    WHERE label_agg.otx_label LIKE '%' || core_vld.otx_bridge || '%'
      OR label_agg.inx_label LIKE '%' || core_vld.inx_bridge || '%'
)
;
"""


def create_update_pidwayy_sound_agg_bridge_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidwayy_s_agg_tablename = create_prime_tablename("pidwayy", "s", "agg")
    return f"""UPDATE {pidwayy_s_agg_tablename}
SET error_message = 'Bridge must exist in WayTerm'
WHERE rowid IN (
    SELECT way_agg.rowid
    FROM {pidwayy_s_agg_tablename} way_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = way_agg.face_name
    WHERE NOT way_agg.otx_way LIKE core_vld.otx_bridge || '%'
        OR NOT way_agg.inx_way LIKE core_vld.inx_bridge || '%'
)
;
"""


def create_update_pidname_sound_agg_bridge_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidname_s_agg_tablename = create_prime_tablename("pidname", "s", "agg")
    return f"""UPDATE {pidname_s_agg_tablename}
SET error_message = 'Bridge cannot exist in NameTerm'
WHERE rowid IN (
    SELECT name_agg.rowid
    FROM {pidname_s_agg_tablename} name_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = name_agg.face_name
    WHERE name_agg.otx_name LIKE '%' || core_vld.otx_bridge || '%'
      OR name_agg.inx_name LIKE '%' || core_vld.inx_bridge || '%'
)
;
"""


def create_update_pidtitl_sound_agg_bridge_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidtitl_s_agg_tablename = create_prime_tablename("pidtitl", "s", "agg")
    return f"""UPDATE {pidtitl_s_agg_tablename}
SET error_message = 'Otx and inx titles must match bridge property.'
WHERE rowid IN (
  SELECT title_agg.rowid
  FROM {pidtitl_s_agg_tablename} title_agg
  JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = title_agg.face_name
  WHERE NOT ((
            title_agg.otx_title LIKE core_vld.otx_bridge || '%' 
        AND title_agg.inx_title LIKE core_vld.inx_bridge || '%') 
      OR (
            NOT title_agg.otx_title LIKE core_vld.otx_bridge || '%'
        AND NOT title_agg.inx_title LIKE core_vld.inx_bridge || '%'
        ))
)
;
"""


def create_insert_pidgin_sound_vld_table_sqlstr(dimen: str) -> str:
    pidgin_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    pidgin_s_vld_tablename = create_prime_tablename(dimen, "s", "vld")
    dimen_otx_inx_obj_names = {
        "pidgin_name": "name",
        "pidgin_title": "title",
        "pidgin_label": "label",
        "pidgin_way": "way",
    }
    otx_str = f"otx_{dimen_otx_inx_obj_names.get(dimen, dimen)}"
    inx_str = f"inx_{dimen_otx_inx_obj_names.get(dimen, dimen)}"
    return f"""
INSERT INTO {pidgin_s_vld_tablename} (event_int, face_name, {otx_str}, {inx_str})
SELECT event_int, face_name, MAX({otx_str}), MAX({inx_str})
FROM {pidgin_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY event_int, face_name
;
"""


def create_bridge_exists_in_name_error_update_sqlstr(table: str, column: str) -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    return f"""UPDATE {table}
SET error_message = 'Bridge cannot exist in NameTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_bridge || '%'
)
;
"""


def create_bridge_exists_in_label_error_update_sqlstr(table: str, column: str) -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    return f"""UPDATE {table}
SET error_message = 'Bridge cannot exist in LabelTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_bridge || '%'
)
;
"""


INSERT_PLNMEMB_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_acct_membership_s_put_vld (event_int, face_name, vow_label, owner_name, acct_name, group_title, credit_vote, debt_vote) SELECT event_int, face_name, vow_label, owner_name, acct_name, group_title, credit_vote, debt_vote FROM plan_acct_membership_s_put_agg WHERE error_message IS NULL"
INSERT_PLNMEMB_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_acct_membership_s_del_vld (event_int, face_name, vow_label, owner_name, acct_name, group_title_ERASE) SELECT event_int, face_name, vow_label, owner_name, acct_name, group_title_ERASE FROM plan_acct_membership_s_del_agg WHERE error_message IS NULL"
INSERT_PLNACCT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_acctunit_s_put_vld (event_int, face_name, vow_label, owner_name, acct_name, credit_score, debt_score) SELECT event_int, face_name, vow_label, owner_name, acct_name, credit_score, debt_score FROM plan_acctunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNACCT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_acctunit_s_del_vld (event_int, face_name, vow_label, owner_name, acct_name_ERASE) SELECT event_int, face_name, vow_label, owner_name, acct_name_ERASE FROM plan_acctunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNAWAR_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_concept_awardlink_s_put_vld (event_int, face_name, vow_label, owner_name, concept_way, awardee_title, give_force, take_force) SELECT event_int, face_name, vow_label, owner_name, concept_way, awardee_title, give_force, take_force FROM plan_concept_awardlink_s_put_agg WHERE error_message IS NULL"
INSERT_PLNAWAR_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_concept_awardlink_s_del_vld (event_int, face_name, vow_label, owner_name, concept_way, awardee_title_ERASE) SELECT event_int, face_name, vow_label, owner_name, concept_way, awardee_title_ERASE FROM plan_concept_awardlink_s_del_agg WHERE error_message IS NULL"
INSERT_PLNFACT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_concept_factunit_s_put_vld (event_int, face_name, vow_label, owner_name, concept_way, fcontext, fstate, fopen, fnigh) SELECT event_int, face_name, vow_label, owner_name, concept_way, fcontext, fstate, fopen, fnigh FROM plan_concept_factunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNFACT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_concept_factunit_s_del_vld (event_int, face_name, vow_label, owner_name, concept_way, fcontext_ERASE) SELECT event_int, face_name, vow_label, owner_name, concept_way, fcontext_ERASE FROM plan_concept_factunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNHEAL_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_concept_healerlink_s_put_vld (event_int, face_name, vow_label, owner_name, concept_way, healer_name) SELECT event_int, face_name, vow_label, owner_name, concept_way, healer_name FROM plan_concept_healerlink_s_put_agg WHERE error_message IS NULL"
INSERT_PLNHEAL_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_concept_healerlink_s_del_vld (event_int, face_name, vow_label, owner_name, concept_way, healer_name_ERASE) SELECT event_int, face_name, vow_label, owner_name, concept_way, healer_name_ERASE FROM plan_concept_healerlink_s_del_agg WHERE error_message IS NULL"
INSERT_PLNPREM_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_concept_reason_premiseunit_s_put_vld (event_int, face_name, vow_label, owner_name, concept_way, rcontext, pstate, pnigh, popen, pdivisor) SELECT event_int, face_name, vow_label, owner_name, concept_way, rcontext, pstate, pnigh, popen, pdivisor FROM plan_concept_reason_premiseunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNPREM_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_concept_reason_premiseunit_s_del_vld (event_int, face_name, vow_label, owner_name, concept_way, rcontext, pstate_ERASE) SELECT event_int, face_name, vow_label, owner_name, concept_way, rcontext, pstate_ERASE FROM plan_concept_reason_premiseunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNREAS_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_concept_reasonunit_s_put_vld (event_int, face_name, vow_label, owner_name, concept_way, rcontext, rconcept_active_requisite) SELECT event_int, face_name, vow_label, owner_name, concept_way, rcontext, rconcept_active_requisite FROM plan_concept_reasonunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNREAS_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_concept_reasonunit_s_del_vld (event_int, face_name, vow_label, owner_name, concept_way, rcontext_ERASE) SELECT event_int, face_name, vow_label, owner_name, concept_way, rcontext_ERASE FROM plan_concept_reasonunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLNLABO_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_concept_laborlink_s_put_vld (event_int, face_name, vow_label, owner_name, concept_way, labor_title) SELECT event_int, face_name, vow_label, owner_name, concept_way, labor_title FROM plan_concept_laborlink_s_put_agg WHERE error_message IS NULL"
INSERT_PLNLABO_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_concept_laborlink_s_del_vld (event_int, face_name, vow_label, owner_name, concept_way, labor_title_ERASE) SELECT event_int, face_name, vow_label, owner_name, concept_way, labor_title_ERASE FROM plan_concept_laborlink_s_del_agg WHERE error_message IS NULL"
INSERT_PLNCONC_SOUND_VLD_PUT_SQLSTR = "INSERT INTO plan_conceptunit_s_put_vld (event_int, face_name, vow_label, owner_name, concept_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool) SELECT event_int, face_name, vow_label, owner_name, concept_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool FROM plan_conceptunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLNCONC_SOUND_VLD_DEL_SQLSTR = "INSERT INTO plan_conceptunit_s_del_vld (event_int, face_name, vow_label, owner_name, concept_way_ERASE) SELECT event_int, face_name, vow_label, owner_name, concept_way_ERASE FROM plan_conceptunit_s_del_agg WHERE error_message IS NULL"
INSERT_PLANUNIT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO planunit_s_put_vld (event_int, face_name, vow_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit) SELECT event_int, face_name, vow_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit FROM planunit_s_put_agg WHERE error_message IS NULL"
INSERT_PLANUNIT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO planunit_s_del_vld (event_int, face_name, vow_label, owner_name_ERASE) SELECT event_int, face_name, vow_label, owner_name_ERASE FROM planunit_s_del_agg WHERE error_message IS NULL"

INSERT_VOWPAYY_SOUND_VLD_SQLSTR = "INSERT INTO vow_paybook_s_vld (event_int, face_name, vow_label, owner_name, acct_name, tran_time, amount) SELECT event_int, face_name, vow_label, owner_name, acct_name, tran_time, amount FROM vow_paybook_s_agg WHERE error_message IS NULL"
INSERT_VOWDEAL_SOUND_VLD_SQLSTR = "INSERT INTO vow_dealunit_s_vld (event_int, face_name, vow_label, owner_name, deal_time, quota, celldepth) SELECT event_int, face_name, vow_label, owner_name, deal_time, quota, celldepth FROM vow_dealunit_s_agg WHERE error_message IS NULL"
INSERT_VOWHOUR_SOUND_VLD_SQLSTR = "INSERT INTO vow_timeline_hour_s_vld (event_int, face_name, vow_label, cumlative_minute, hour_label) SELECT event_int, face_name, vow_label, cumlative_minute, hour_label FROM vow_timeline_hour_s_agg WHERE error_message IS NULL"
INSERT_VOWMONT_SOUND_VLD_SQLSTR = "INSERT INTO vow_timeline_month_s_vld (event_int, face_name, vow_label, cumlative_day, month_label) SELECT event_int, face_name, vow_label, cumlative_day, month_label FROM vow_timeline_month_s_agg WHERE error_message IS NULL"
INSERT_VOWWEEK_SOUND_VLD_SQLSTR = "INSERT INTO vow_timeline_weekday_s_vld (event_int, face_name, vow_label, weekday_order, weekday_label) SELECT event_int, face_name, vow_label, weekday_order, weekday_label FROM vow_timeline_weekday_s_agg WHERE error_message IS NULL"
INSERT_VOWOFFI_SOUND_VLD_SQLSTR = "INSERT INTO vow_timeoffi_s_vld (event_int, face_name, vow_label, offi_time) SELECT event_int, face_name, vow_label, offi_time FROM vow_timeoffi_s_agg WHERE error_message IS NULL"
INSERT_VOWUNIT_SOUND_VLD_SQLSTR = "INSERT INTO vowunit_s_vld (event_int, face_name, vow_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations) SELECT event_int, face_name, vow_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations FROM vowunit_s_agg WHERE error_message IS NULL"


def get_insert_into_sound_vld_sqlstrs() -> dict[str, str]:
    return {
        "plan_acct_membership_s_put_vld": INSERT_PLNMEMB_SOUND_VLD_PUT_SQLSTR,
        "plan_acct_membership_s_del_vld": INSERT_PLNMEMB_SOUND_VLD_DEL_SQLSTR,
        "plan_acctunit_s_put_vld": INSERT_PLNACCT_SOUND_VLD_PUT_SQLSTR,
        "plan_acctunit_s_del_vld": INSERT_PLNACCT_SOUND_VLD_DEL_SQLSTR,
        "plan_concept_awardlink_s_put_vld": INSERT_PLNAWAR_SOUND_VLD_PUT_SQLSTR,
        "plan_concept_awardlink_s_del_vld": INSERT_PLNAWAR_SOUND_VLD_DEL_SQLSTR,
        "plan_concept_factunit_s_put_vld": INSERT_PLNFACT_SOUND_VLD_PUT_SQLSTR,
        "plan_concept_factunit_s_del_vld": INSERT_PLNFACT_SOUND_VLD_DEL_SQLSTR,
        "plan_concept_healerlink_s_put_vld": INSERT_PLNHEAL_SOUND_VLD_PUT_SQLSTR,
        "plan_concept_healerlink_s_del_vld": INSERT_PLNHEAL_SOUND_VLD_DEL_SQLSTR,
        "plan_concept_reason_premiseunit_s_put_vld": INSERT_PLNPREM_SOUND_VLD_PUT_SQLSTR,
        "plan_concept_reason_premiseunit_s_del_vld": INSERT_PLNPREM_SOUND_VLD_DEL_SQLSTR,
        "plan_concept_reasonunit_s_put_vld": INSERT_PLNREAS_SOUND_VLD_PUT_SQLSTR,
        "plan_concept_reasonunit_s_del_vld": INSERT_PLNREAS_SOUND_VLD_DEL_SQLSTR,
        "plan_concept_laborlink_s_put_vld": INSERT_PLNLABO_SOUND_VLD_PUT_SQLSTR,
        "plan_concept_laborlink_s_del_vld": INSERT_PLNLABO_SOUND_VLD_DEL_SQLSTR,
        "plan_conceptunit_s_put_vld": INSERT_PLNCONC_SOUND_VLD_PUT_SQLSTR,
        "plan_conceptunit_s_del_vld": INSERT_PLNCONC_SOUND_VLD_DEL_SQLSTR,
        "planunit_s_put_vld": INSERT_PLANUNIT_SOUND_VLD_PUT_SQLSTR,
        "planunit_s_del_vld": INSERT_PLANUNIT_SOUND_VLD_DEL_SQLSTR,
        "vow_paybook_s_vld": INSERT_VOWPAYY_SOUND_VLD_SQLSTR,
        "vow_dealunit_s_vld": INSERT_VOWDEAL_SOUND_VLD_SQLSTR,
        "vow_timeline_hour_s_vld": INSERT_VOWHOUR_SOUND_VLD_SQLSTR,
        "vow_timeline_month_s_vld": INSERT_VOWMONT_SOUND_VLD_SQLSTR,
        "vow_timeline_weekday_s_vld": INSERT_VOWWEEK_SOUND_VLD_SQLSTR,
        "vow_timeoffi_s_vld": INSERT_VOWOFFI_SOUND_VLD_SQLSTR,
        "vowunit_s_vld": INSERT_VOWUNIT_SOUND_VLD_SQLSTR,
    }


INSERT_VOWPAYY_VOICE_RAW_SQLSTR = "INSERT INTO vow_paybook_v_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, acct_name_otx, tran_time, amount) SELECT event_int, face_name, vow_label, owner_name, acct_name, tran_time, amount FROM vow_paybook_s_vld "
INSERT_VOWDEAL_VOICE_RAW_SQLSTR = "INSERT INTO vow_dealunit_v_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, deal_time, quota, celldepth) SELECT event_int, face_name, vow_label, owner_name, deal_time, quota, celldepth FROM vow_dealunit_s_vld "
INSERT_VOWHOUR_VOICE_RAW_SQLSTR = "INSERT INTO vow_timeline_hour_v_raw (event_int, face_name_otx, vow_label_otx, cumlative_minute, hour_label_otx) SELECT event_int, face_name, vow_label, cumlative_minute, hour_label FROM vow_timeline_hour_s_vld "
INSERT_VOWMONT_VOICE_RAW_SQLSTR = "INSERT INTO vow_timeline_month_v_raw (event_int, face_name_otx, vow_label_otx, cumlative_day, month_label_otx) SELECT event_int, face_name, vow_label, cumlative_day, month_label FROM vow_timeline_month_s_vld "
INSERT_VOWWEEK_VOICE_RAW_SQLSTR = "INSERT INTO vow_timeline_weekday_v_raw (event_int, face_name_otx, vow_label_otx, weekday_order, weekday_label_otx) SELECT event_int, face_name, vow_label, weekday_order, weekday_label FROM vow_timeline_weekday_s_vld "
INSERT_VOWOFFI_VOICE_RAW_SQLSTR = "INSERT INTO vow_timeoffi_v_raw (event_int, face_name_otx, vow_label_otx, offi_time) SELECT event_int, face_name, vow_label, offi_time FROM vow_timeoffi_s_vld "
INSERT_VOWUNIT_VOICE_RAW_SQLSTR = "INSERT INTO vowunit_v_raw (event_int, face_name_otx, vow_label_otx, timeline_label_otx, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations) SELECT event_int, face_name, vow_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations FROM vowunit_s_vld "

INSERT_PLNMEMB_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_acct_membership_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, acct_name_otx, group_title_otx, credit_vote, debt_vote) SELECT event_int, face_name, vow_label, owner_name, acct_name, group_title, credit_vote, debt_vote FROM plan_acct_membership_s_put_vld "
INSERT_PLNMEMB_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_acct_membership_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, acct_name_otx, group_title_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, acct_name, group_title_ERASE FROM plan_acct_membership_s_del_vld "
INSERT_PLNACCT_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_acctunit_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, acct_name_otx, credit_score, debt_score) SELECT event_int, face_name, vow_label, owner_name, acct_name, credit_score, debt_score FROM plan_acctunit_s_put_vld "
INSERT_PLNACCT_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_acctunit_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, acct_name_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, acct_name_ERASE FROM plan_acctunit_s_del_vld "
INSERT_PLNAWAR_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_concept_awardlink_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, awardee_title_otx, give_force, take_force) SELECT event_int, face_name, vow_label, owner_name, concept_way, awardee_title, give_force, take_force FROM plan_concept_awardlink_s_put_vld "
INSERT_PLNAWAR_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_concept_awardlink_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, awardee_title_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way, awardee_title_ERASE FROM plan_concept_awardlink_s_del_vld "
INSERT_PLNFACT_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_concept_factunit_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, fcontext_otx, fstate_otx, fopen, fnigh) SELECT event_int, face_name, vow_label, owner_name, concept_way, fcontext, fstate, fopen, fnigh FROM plan_concept_factunit_s_put_vld "
INSERT_PLNFACT_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_concept_factunit_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, fcontext_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way, fcontext_ERASE FROM plan_concept_factunit_s_del_vld "
INSERT_PLNHEAL_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_concept_healerlink_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, healer_name_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way, healer_name FROM plan_concept_healerlink_s_put_vld "
INSERT_PLNHEAL_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_concept_healerlink_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, healer_name_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way, healer_name_ERASE FROM plan_concept_healerlink_s_del_vld "
INSERT_PLNPREM_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_concept_reason_premiseunit_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, rcontext_otx, pstate_otx, pnigh, popen, pdivisor) SELECT event_int, face_name, vow_label, owner_name, concept_way, rcontext, pstate, pnigh, popen, pdivisor FROM plan_concept_reason_premiseunit_s_put_vld "
INSERT_PLNPREM_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_concept_reason_premiseunit_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, rcontext_otx, pstate_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way, rcontext, pstate_ERASE FROM plan_concept_reason_premiseunit_s_del_vld "
INSERT_PLNREAS_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_concept_reasonunit_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, rcontext_otx, rconcept_active_requisite) SELECT event_int, face_name, vow_label, owner_name, concept_way, rcontext, rconcept_active_requisite FROM plan_concept_reasonunit_s_put_vld "
INSERT_PLNREAS_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_concept_reasonunit_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, rcontext_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way, rcontext_ERASE FROM plan_concept_reasonunit_s_del_vld "
INSERT_PLNLABO_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_concept_laborlink_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, labor_title_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way, labor_title FROM plan_concept_laborlink_s_put_vld "
INSERT_PLNLABO_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_concept_laborlink_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, labor_title_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way, labor_title_ERASE FROM plan_concept_laborlink_s_del_vld "
INSERT_PLNCONC_VOICE_RAW_PUT_SQLSTR = "INSERT INTO plan_conceptunit_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_otx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool) SELECT event_int, face_name, vow_label, owner_name, concept_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool FROM plan_conceptunit_s_put_vld "
INSERT_PLNCONC_VOICE_RAW_DEL_SQLSTR = "INSERT INTO plan_conceptunit_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, concept_way_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name, concept_way_ERASE FROM plan_conceptunit_s_del_vld "
INSERT_PLANUNIT_VOICE_RAW_PUT_SQLSTR = "INSERT INTO planunit_v_put_raw (event_int, face_name_otx, vow_label_otx, owner_name_otx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit) SELECT event_int, face_name, vow_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit FROM planunit_s_put_vld "
INSERT_PLANUNIT_VOICE_RAW_DEL_SQLSTR = "INSERT INTO planunit_v_del_raw (event_int, face_name_otx, vow_label_otx, owner_name_ERASE_otx) SELECT event_int, face_name, vow_label, owner_name_ERASE FROM planunit_s_del_vld "


def get_insert_into_voice_raw_sqlstrs() -> dict[str, str]:
    return {
        "vow_paybook_v_raw": INSERT_VOWPAYY_VOICE_RAW_SQLSTR,
        "vow_dealunit_v_raw": INSERT_VOWDEAL_VOICE_RAW_SQLSTR,
        "vow_timeline_hour_v_raw": INSERT_VOWHOUR_VOICE_RAW_SQLSTR,
        "vow_timeline_month_v_raw": INSERT_VOWMONT_VOICE_RAW_SQLSTR,
        "vow_timeline_weekday_v_raw": INSERT_VOWWEEK_VOICE_RAW_SQLSTR,
        "vow_timeoffi_v_raw": INSERT_VOWOFFI_VOICE_RAW_SQLSTR,
        "vowunit_v_raw": INSERT_VOWUNIT_VOICE_RAW_SQLSTR,
        "plan_acct_membership_v_put_raw": INSERT_PLNMEMB_VOICE_RAW_PUT_SQLSTR,
        "plan_acct_membership_v_del_raw": INSERT_PLNMEMB_VOICE_RAW_DEL_SQLSTR,
        "plan_acctunit_v_put_raw": INSERT_PLNACCT_VOICE_RAW_PUT_SQLSTR,
        "plan_acctunit_v_del_raw": INSERT_PLNACCT_VOICE_RAW_DEL_SQLSTR,
        "plan_concept_awardlink_v_put_raw": INSERT_PLNAWAR_VOICE_RAW_PUT_SQLSTR,
        "plan_concept_awardlink_v_del_raw": INSERT_PLNAWAR_VOICE_RAW_DEL_SQLSTR,
        "plan_concept_factunit_v_put_raw": INSERT_PLNFACT_VOICE_RAW_PUT_SQLSTR,
        "plan_concept_factunit_v_del_raw": INSERT_PLNFACT_VOICE_RAW_DEL_SQLSTR,
        "plan_concept_healerlink_v_put_raw": INSERT_PLNHEAL_VOICE_RAW_PUT_SQLSTR,
        "plan_concept_healerlink_v_del_raw": INSERT_PLNHEAL_VOICE_RAW_DEL_SQLSTR,
        "plan_concept_reason_premiseunit_v_put_raw": INSERT_PLNPREM_VOICE_RAW_PUT_SQLSTR,
        "plan_concept_reason_premiseunit_v_del_raw": INSERT_PLNPREM_VOICE_RAW_DEL_SQLSTR,
        "plan_concept_reasonunit_v_put_raw": INSERT_PLNREAS_VOICE_RAW_PUT_SQLSTR,
        "plan_concept_reasonunit_v_del_raw": INSERT_PLNREAS_VOICE_RAW_DEL_SQLSTR,
        "plan_concept_laborlink_v_put_raw": INSERT_PLNLABO_VOICE_RAW_PUT_SQLSTR,
        "plan_concept_laborlink_v_del_raw": INSERT_PLNLABO_VOICE_RAW_DEL_SQLSTR,
        "plan_conceptunit_v_put_raw": INSERT_PLNCONC_VOICE_RAW_PUT_SQLSTR,
        "plan_conceptunit_v_del_raw": INSERT_PLNCONC_VOICE_RAW_DEL_SQLSTR,
        "planunit_v_put_raw": INSERT_PLANUNIT_VOICE_RAW_PUT_SQLSTR,
        "planunit_v_del_raw": INSERT_PLANUNIT_VOICE_RAW_DEL_SQLSTR,
    }


def create_update_voice_raw_existing_inx_col_sqlstr(
    pidgin_type_abbv: str, table: str, column_prefix: str
) -> str:
    return f"""
WITH pid_face_otx_event AS (
    SELECT 
      raw_dim.rowid raw_rowid
    , raw_dim.event_int
    , raw_dim.face_name_otx
    , raw_dim.{column_prefix}_otx
    , MAX(pid.event_int) pidgin_event_int
    FROM {table} raw_dim
    LEFT JOIN pidgin_{pidgin_type_abbv}_s_vld pid ON pid.face_name = raw_dim.face_name_otx
        AND pid.otx_{pidgin_type_abbv} = raw_dim.{column_prefix}_otx
        AND raw_dim.event_int >= pid.event_int
    GROUP BY 
      raw_dim.rowid
    , raw_dim.event_int
    , raw_dim.face_name_otx
    , raw_dim.{column_prefix}_otx
),
pid_inx_strs AS (
    SELECT pid_foe.raw_rowid, pid_vld.inx_{pidgin_type_abbv}
    FROM pid_face_otx_event pid_foe
    LEFT JOIN pidgin_{pidgin_type_abbv}_s_vld pid_vld
        ON pid_vld.face_name = pid_foe.face_name_otx
        AND pid_vld.otx_{pidgin_type_abbv} = pid_foe.{column_prefix}_otx
        AND pid_vld.event_int = pid_foe.pidgin_event_int
)
UPDATE {table} as dim_v_raw
SET {column_prefix}_inx = (
    SELECT pid_inx_strs.inx_{pidgin_type_abbv}
    FROM pid_inx_strs
    WHERE dim_v_raw.rowid = pid_inx_strs.raw_rowid
)
;
"""


def create_update_voice_raw_empty_inx_col_sqlstr(table: str, column_prefix: str) -> str:
    return f"""
UPDATE {table} as dim_v_raw
SET {column_prefix}_inx = {column_prefix}_otx
WHERE {column_prefix}_inx IS NULL
;
"""


VOWPAYY_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO vow_paybook_v_agg (vow_label, owner_name, acct_name, tran_time, amount)
SELECT vow_label_inx, owner_name_inx, acct_name_inx, tran_time, amount
FROM vow_paybook_v_raw
GROUP BY vow_label_inx, owner_name_inx, acct_name_inx, tran_time, amount
"""
VOWDEAL_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO vow_dealunit_v_agg (vow_label, owner_name, deal_time, quota, celldepth)
SELECT vow_label_inx, owner_name_inx, deal_time, quota, celldepth
FROM vow_dealunit_v_raw
GROUP BY vow_label_inx, owner_name_inx, deal_time, quota, celldepth
"""
VOWHOUR_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO vow_timeline_hour_v_agg (vow_label, cumlative_minute, hour_label)
SELECT vow_label_inx, cumlative_minute, hour_label_inx
FROM vow_timeline_hour_v_raw
GROUP BY vow_label_inx, cumlative_minute, hour_label_inx
"""
VOWMONT_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO vow_timeline_month_v_agg (vow_label, cumlative_day, month_label)
SELECT vow_label_inx, cumlative_day, month_label_inx
FROM vow_timeline_month_v_raw
GROUP BY vow_label_inx, cumlative_day, month_label_inx
"""
VOWWEEK_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO vow_timeline_weekday_v_agg (vow_label, weekday_order, weekday_label)
SELECT vow_label_inx, weekday_order, weekday_label_inx
FROM vow_timeline_weekday_v_raw
GROUP BY vow_label_inx, weekday_order, weekday_label_inx
"""
VOWOFFI_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO vow_timeoffi_v_agg (vow_label, offi_time)
SELECT vow_label_inx, offi_time
FROM vow_timeoffi_v_raw
GROUP BY vow_label_inx, offi_time
"""
VOWUNIT_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO vowunit_v_agg (vow_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations)
SELECT vow_label_inx, timeline_label_inx, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations
FROM vowunit_v_raw
GROUP BY vow_label_inx, timeline_label_inx, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations
"""

INSERT_PLNMEMB_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_acct_membership_v_put_agg (event_int, face_name, vow_label, owner_name, acct_name, group_title, credit_vote, debt_vote)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, acct_name_inx, group_title_inx, credit_vote, debt_vote
FROM plan_acct_membership_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, acct_name_inx, group_title_inx, credit_vote, debt_vote
"""
INSERT_PLNMEMB_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_acct_membership_v_del_agg (event_int, face_name, vow_label, owner_name, acct_name, group_title_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, acct_name_inx, group_title_ERASE_inx
FROM plan_acct_membership_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, acct_name_inx, group_title_ERASE_inx
"""
INSERT_PLNACCT_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_acctunit_v_put_agg (event_int, face_name, vow_label, owner_name, acct_name, credit_score, debt_score)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, acct_name_inx, credit_score, debt_score
FROM plan_acctunit_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, acct_name_inx, credit_score, debt_score
"""
INSERT_PLNACCT_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_acctunit_v_del_agg (event_int, face_name, vow_label, owner_name, acct_name_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, acct_name_ERASE_inx
FROM plan_acctunit_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, acct_name_ERASE_inx
"""
INSERT_PLNAWAR_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_concept_awardlink_v_put_agg (event_int, face_name, vow_label, owner_name, concept_way, awardee_title, give_force, take_force)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, awardee_title_inx, give_force, take_force
FROM plan_concept_awardlink_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, awardee_title_inx, give_force, take_force
"""
INSERT_PLNAWAR_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_concept_awardlink_v_del_agg (event_int, face_name, vow_label, owner_name, concept_way, awardee_title_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, awardee_title_ERASE_inx
FROM plan_concept_awardlink_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, awardee_title_ERASE_inx
"""
INSERT_PLNFACT_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_concept_factunit_v_put_agg (event_int, face_name, vow_label, owner_name, concept_way, fcontext, fstate, fopen, fnigh)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, fcontext_inx, fstate_inx, fopen, fnigh
FROM plan_concept_factunit_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, fcontext_inx, fstate_inx, fopen, fnigh
"""
INSERT_PLNFACT_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_concept_factunit_v_del_agg (event_int, face_name, vow_label, owner_name, concept_way, fcontext_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, fcontext_ERASE_inx
FROM plan_concept_factunit_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, fcontext_ERASE_inx
"""
INSERT_PLNHEAL_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_concept_healerlink_v_put_agg (event_int, face_name, vow_label, owner_name, concept_way, healer_name)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, healer_name_inx
FROM plan_concept_healerlink_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, healer_name_inx
"""
INSERT_PLNHEAL_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_concept_healerlink_v_del_agg (event_int, face_name, vow_label, owner_name, concept_way, healer_name_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, healer_name_ERASE_inx
FROM plan_concept_healerlink_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, healer_name_ERASE_inx
"""
INSERT_PLNPREM_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_concept_reason_premiseunit_v_put_agg (event_int, face_name, vow_label, owner_name, concept_way, rcontext, pstate, pnigh, popen, pdivisor)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, pstate_inx, pnigh, popen, pdivisor
FROM plan_concept_reason_premiseunit_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, pstate_inx, pnigh, popen, pdivisor
"""
INSERT_PLNPREM_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_concept_reason_premiseunit_v_del_agg (event_int, face_name, vow_label, owner_name, concept_way, rcontext, pstate_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, pstate_ERASE_inx
FROM plan_concept_reason_premiseunit_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, pstate_ERASE_inx
"""
INSERT_PLNREAS_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_concept_reasonunit_v_put_agg (event_int, face_name, vow_label, owner_name, concept_way, rcontext, rconcept_active_requisite)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, rconcept_active_requisite
FROM plan_concept_reasonunit_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, rconcept_active_requisite
"""
INSERT_PLNREAS_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_concept_reasonunit_v_del_agg (event_int, face_name, vow_label, owner_name, concept_way, rcontext_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, rcontext_ERASE_inx
FROM plan_concept_reasonunit_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, rcontext_ERASE_inx
"""
INSERT_PLNLABO_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_concept_laborlink_v_put_agg (event_int, face_name, vow_label, owner_name, concept_way, labor_title)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, labor_title_inx
FROM plan_concept_laborlink_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, labor_title_inx
"""
INSERT_PLNLABO_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_concept_laborlink_v_del_agg (event_int, face_name, vow_label, owner_name, concept_way, labor_title_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, labor_title_ERASE_inx
FROM plan_concept_laborlink_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, labor_title_ERASE_inx
"""
INSERT_PLNCONC_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO plan_conceptunit_v_put_agg (event_int, face_name, vow_label, owner_name, concept_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool
FROM plan_conceptunit_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, task, problem_bool
"""
INSERT_PLNCONC_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO plan_conceptunit_v_del_agg (event_int, face_name, vow_label, owner_name, concept_way_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_ERASE_inx
FROM plan_conceptunit_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, concept_way_ERASE_inx
"""
INSERT_PLANUNIT_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO planunit_v_put_agg (event_int, face_name, vow_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit
FROM planunit_v_put_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit
"""
INSERT_PLANUNIT_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO planunit_v_del_agg (event_int, face_name, vow_label, owner_name_ERASE)
SELECT event_int, face_name_inx, vow_label_inx, owner_name_ERASE_inx
FROM planunit_v_del_raw
GROUP BY event_int, face_name_inx, vow_label_inx, owner_name_ERASE_inx
"""


def get_insert_voice_agg_sqlstrs() -> dict[str, str]:
    return {
        "vow_paybook": VOWPAYY_VOICE_AGG_INSERT_SQLSTR,
        "vow_dealunit": VOWDEAL_VOICE_AGG_INSERT_SQLSTR,
        "vow_timeline_hour": VOWHOUR_VOICE_AGG_INSERT_SQLSTR,
        "vow_timeline_month": VOWMONT_VOICE_AGG_INSERT_SQLSTR,
        "vow_timeline_weekday": VOWWEEK_VOICE_AGG_INSERT_SQLSTR,
        "vow_timeoffi": VOWOFFI_VOICE_AGG_INSERT_SQLSTR,
        "vowunit": VOWUNIT_VOICE_AGG_INSERT_SQLSTR,
        "plan_acct_membership_v_put_agg": INSERT_PLNMEMB_VOICE_AGG_PUT_SQLSTR,
        "plan_acct_membership_v_del_agg": INSERT_PLNMEMB_VOICE_AGG_DEL_SQLSTR,
        "plan_acctunit_v_put_agg": INSERT_PLNACCT_VOICE_AGG_PUT_SQLSTR,
        "plan_acctunit_v_del_agg": INSERT_PLNACCT_VOICE_AGG_DEL_SQLSTR,
        "plan_concept_awardlink_v_put_agg": INSERT_PLNAWAR_VOICE_AGG_PUT_SQLSTR,
        "plan_concept_awardlink_v_del_agg": INSERT_PLNAWAR_VOICE_AGG_DEL_SQLSTR,
        "plan_concept_factunit_v_put_agg": INSERT_PLNFACT_VOICE_AGG_PUT_SQLSTR,
        "plan_concept_factunit_v_del_agg": INSERT_PLNFACT_VOICE_AGG_DEL_SQLSTR,
        "plan_concept_healerlink_v_put_agg": INSERT_PLNHEAL_VOICE_AGG_PUT_SQLSTR,
        "plan_concept_healerlink_v_del_agg": INSERT_PLNHEAL_VOICE_AGG_DEL_SQLSTR,
        "plan_concept_reason_premiseunit_v_put_agg": INSERT_PLNPREM_VOICE_AGG_PUT_SQLSTR,
        "plan_concept_reason_premiseunit_v_del_agg": INSERT_PLNPREM_VOICE_AGG_DEL_SQLSTR,
        "plan_concept_reasonunit_v_put_agg": INSERT_PLNREAS_VOICE_AGG_PUT_SQLSTR,
        "plan_concept_reasonunit_v_del_agg": INSERT_PLNREAS_VOICE_AGG_DEL_SQLSTR,
        "plan_concept_laborlink_v_put_agg": INSERT_PLNLABO_VOICE_AGG_PUT_SQLSTR,
        "plan_concept_laborlink_v_del_agg": INSERT_PLNLABO_VOICE_AGG_DEL_SQLSTR,
        "plan_conceptunit_v_put_agg": INSERT_PLNCONC_VOICE_AGG_PUT_SQLSTR,
        "plan_conceptunit_v_del_agg": INSERT_PLNCONC_VOICE_AGG_DEL_SQLSTR,
        "planunit_v_put_agg": INSERT_PLANUNIT_VOICE_AGG_PUT_SQLSTR,
        "planunit_v_del_agg": INSERT_PLANUNIT_VOICE_AGG_DEL_SQLSTR,
    }


VOWPAYY_FU2_SELECT_SQLSTR = "SELECT vow_label, owner_name, acct_name, tran_time, amount FROM vow_paybook_v_agg WHERE vow_label = "
VOWDEAL_FU2_SELECT_SQLSTR = "SELECT vow_label, owner_name, deal_time, quota, celldepth FROM vow_dealunit_v_agg WHERE vow_label = "
VOWHOUR_FU2_SELECT_SQLSTR = "SELECT vow_label, cumlative_minute, hour_label FROM vow_timeline_hour_v_agg WHERE vow_label = "
VOWMONT_FU2_SELECT_SQLSTR = "SELECT vow_label, cumlative_day, month_label FROM vow_timeline_month_v_agg WHERE vow_label = "
VOWWEEK_FU2_SELECT_SQLSTR = "SELECT vow_label, weekday_order, weekday_label FROM vow_timeline_weekday_v_agg WHERE vow_label = "
VOWOFFI_FU2_SELECT_SQLSTR = (
    "SELECT vow_label, offi_time FROM vow_timeoffi_v_agg WHERE vow_label = "
)
VOWUNIT_FU2_SELECT_SQLSTR = "SELECT vow_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations FROM vowunit_v_agg WHERE vow_label = "


def get_vow_voice_select1_sqlstrs(vow_label: str) -> dict[str, str]:
    return {
        "vowunit": f"{VOWUNIT_FU2_SELECT_SQLSTR}'{vow_label}'",
        "vow_dealunit": f"{VOWDEAL_FU2_SELECT_SQLSTR}'{vow_label}'",
        "vow_paybook": f"{VOWPAYY_FU2_SELECT_SQLSTR}'{vow_label}'",
        "vow_timeline_hour": f"{VOWHOUR_FU2_SELECT_SQLSTR}'{vow_label}'",
        "vow_timeline_month": f"{VOWMONT_FU2_SELECT_SQLSTR}'{vow_label}'",
        "vow_timeline_weekday": f"{VOWWEEK_FU2_SELECT_SQLSTR}'{vow_label}'",
        "vow_timeoffi": f"{VOWOFFI_FU2_SELECT_SQLSTR}'{vow_label}'",
    }


def get_idea_stageble_put_dimens() -> dict[str, list[str]]:
    return {
        "br00000": ["vowunit"],
        "br00001": ["planunit", "vow_dealunit", "vowunit"],
        "br00002": ["plan_acctunit", "planunit", "vow_paybook", "vowunit"],
        "br00003": ["vow_timeline_hour", "vowunit"],
        "br00004": ["vow_timeline_month", "vowunit"],
        "br00005": ["vow_timeline_weekday", "vowunit"],
        "br00006": ["vow_timeoffi", "vowunit"],
        "br00011": ["plan_acctunit", "planunit", "vowunit"],
        "br00012": ["plan_acct_membership", "plan_acctunit", "planunit", "vowunit"],
        "br00013": ["plan_conceptunit", "planunit", "vowunit"],
        "br00019": ["plan_conceptunit", "planunit", "vowunit"],
        "br00020": ["plan_acct_membership", "plan_acctunit", "planunit", "vowunit"],
        "br00021": ["plan_acctunit", "planunit", "vowunit"],
        "br00022": [
            "plan_concept_awardlink",
            "plan_conceptunit",
            "planunit",
            "vowunit",
        ],
        "br00023": ["plan_concept_factunit", "plan_conceptunit", "planunit", "vowunit"],
        "br00024": [
            "plan_concept_laborlink",
            "plan_conceptunit",
            "planunit",
            "vowunit",
        ],
        "br00025": [
            "plan_concept_healerlink",
            "plan_conceptunit",
            "planunit",
            "vowunit",
        ],
        "br00026": [
            "plan_concept_reason_premiseunit",
            "plan_concept_reasonunit",
            "plan_conceptunit",
            "planunit",
            "vowunit",
        ],
        "br00027": [
            "plan_concept_reasonunit",
            "plan_conceptunit",
            "planunit",
            "vowunit",
        ],
        "br00028": ["plan_conceptunit", "planunit", "vowunit"],
        "br00029": ["planunit", "vowunit"],
        "br00036": [
            "plan_concept_healerlink",
            "plan_conceptunit",
            "planunit",
            "vowunit",
        ],
        "br00042": [],
        "br00043": [],
        "br00044": [],
        "br00045": [],
        "br00050": ["plan_acctunit", "planunit", "vowunit"],
        "br00051": ["planunit", "vowunit"],
        "br00052": ["plan_conceptunit", "planunit", "vowunit"],
        "br00053": ["plan_conceptunit", "planunit", "vowunit"],
        "br00054": ["plan_conceptunit", "planunit", "vowunit"],
        "br00055": ["plan_conceptunit", "planunit", "vowunit"],
        "br00056": [
            "plan_concept_reasonunit",
            "plan_conceptunit",
            "planunit",
            "vowunit",
        ],
        "br00057": ["plan_conceptunit", "planunit", "vowunit"],
        "br00058": ["planunit", "vowunit"],
        "br00059": ["vowunit"],
        "br00113": ["plan_acctunit", "planunit", "vowunit"],
        "br00115": ["plan_acctunit", "planunit", "vowunit"],
        "br00116": ["plan_acctunit", "planunit", "vowunit"],
        "br00117": ["plan_acctunit", "planunit", "vowunit"],
    }


IDEA_STAGEBLE_DEL_DIMENS = {
    "br00050": ["plan_acct_membership"],
    "br00051": ["plan_acctunit"],
    "br00052": ["plan_concept_awardlink"],
    "br00053": ["plan_concept_factunit"],
    "br00054": ["plan_concept_laborlink"],
    "br00055": ["plan_concept_healerlink"],
    "br00056": ["plan_concept_reason_premiseunit"],
    "br00057": ["plan_concept_reasonunit"],
    "br00058": ["plan_conceptunit"],
    "br00059": ["planunit"],
}


CREATE_VOW_EVENT_TIME_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS vow_event_time_agg (
  vow_label TEXT
, event_int INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
INSERT_VOW_EVENT_TIME_AGG_SQLSTR = """
INSERT INTO vow_event_time_agg (vow_label, event_int, agg_time)
SELECT vow_label, event_int, agg_time
FROM (
    SELECT vow_label, event_int, tran_time as agg_time
    FROM vow_paybook_raw
    GROUP BY vow_label, event_int, tran_time
    UNION 
    SELECT vow_label, event_int, deal_time as agg_time
    FROM vow_dealunit_raw
    GROUP BY vow_label, event_int, deal_time
)
ORDER BY vow_label, event_int, agg_time
;
"""
UPDATE_ERROR_MESSAGE_VOW_EVENT_TIME_AGG_SQLSTR = """
WITH EventTimeOrdered AS (
    SELECT vow_label, event_int, agg_time,
           LAG(agg_time) OVER (PARTITION BY vow_label ORDER BY event_int) AS prev_agg_time
    FROM vow_event_time_agg
)
UPDATE vow_event_time_agg
SET error_message = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.event_int = vow_event_time_agg.event_int
    AND EventTimeOrdered.vow_label = vow_event_time_agg.vow_label
    AND EventTimeOrdered.agg_time = vow_event_time_agg.agg_time
;
"""


CREATE_VOW_OTE1_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS vow_ote1_agg (
  vow_label TEXT
, owner_name TEXT
, event_int INTEGER
, deal_time INTEGER
, error_message TEXT
)
;
"""
INSERT_VOW_OTE1_AGG_FROM_VOICE_SQLSTR = """
INSERT INTO vow_ote1_agg (vow_label, owner_name, event_int, deal_time)
SELECT vow_label, owner_name, event_int, deal_time
FROM (
    SELECT 
      vow_label_inx vow_label
    , owner_name_inx owner_name
    , event_int
    , deal_time
    FROM vow_dealunit_v_raw
    GROUP BY vow_label_inx, owner_name_inx, event_int, deal_time
)
ORDER BY vow_label, owner_name, event_int, deal_time
;
"""


CREATE_JOB_PLNMEMB_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_acct_membership_job (vow_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debt_vote REAL, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL, _fund_agenda_ratio_give REAL, _fund_agenda_ratio_take REAL)"""
CREATE_JOB_PLNACCT_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_acctunit_job (vow_label TEXT, owner_name TEXT, acct_name TEXT, credit_score REAL, debt_score REAL, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL, _fund_agenda_ratio_give REAL, _fund_agenda_ratio_take REAL, _inallocable_debt_score REAL, _irrational_debt_score REAL)"""
CREATE_JOB_PLNGROU_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_groupunit_job (vow_label TEXT, owner_name TEXT, group_title TEXT, fund_iota REAL, bridge TEXT, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL)"""
CREATE_JOB_PLNAWAR_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_concept_awardlink_job (vow_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL, _fund_give REAL, _fund_take REAL)"""
CREATE_JOB_PLNFACT_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_concept_factunit_job (vow_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fstate TEXT, fopen REAL, fnigh REAL)"""
CREATE_JOB_PLNHEAL_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_concept_healerlink_job (vow_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT)"""
CREATE_JOB_PLNPREM_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_concept_reason_premiseunit_job (vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pstate TEXT, pnigh REAL, popen REAL, pdivisor INTEGER, _chore INTEGER, _status INTEGER)"""
CREATE_JOB_PLNREAS_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_concept_reasonunit_job (vow_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rconcept_active_requisite INTEGER, _chore INTEGER, _status INTEGER, _rconcept_active_value INTEGER)"""
CREATE_JOB_PLNLABO_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_concept_laborlink_job (vow_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT, _owner_name_labor INTEGER)"""
CREATE_JOB_PLNCONC_SQLSTR = """CREATE TABLE IF NOT EXISTS plan_conceptunit_job (vow_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, task INTEGER, problem_bool INTEGER, fund_iota REAL, _active INTEGER, _chore INTEGER, _fund_onset REAL, _fund_cease REAL, _fund_ratio REAL, _gogo_calc REAL, _stop_calc REAL, _level INTEGER, _range_evaluated INTEGER, _descendant_task_count INTEGER, _healerlink_ratio REAL, _all_acct_cred INTEGER, _all_acct_debt INTEGER)"""
CREATE_JOB_PLANUNIT_SQLSTR = """CREATE TABLE IF NOT EXISTS planunit_job (vow_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, _rational INTEGER, _keeps_justified INTEGER, _offtrack_fund REAL, _sum_healerlink_share REAL, _keeps_buildable INTEGER, _tree_traverse_count INTEGER)"""


def get_job_create_table_sqlstrs() -> dict[str, str]:
    return {
        "plan_acct_membership_job": CREATE_JOB_PLNMEMB_SQLSTR,
        "plan_acctunit_job": CREATE_JOB_PLNACCT_SQLSTR,
        "plan_groupunit_job": CREATE_JOB_PLNGROU_SQLSTR,
        "plan_concept_awardlink_job": CREATE_JOB_PLNAWAR_SQLSTR,
        "plan_concept_factunit_job": CREATE_JOB_PLNFACT_SQLSTR,
        "plan_concept_healerlink_job": CREATE_JOB_PLNHEAL_SQLSTR,
        "plan_concept_reason_premiseunit_job": CREATE_JOB_PLNPREM_SQLSTR,
        "plan_concept_reasonunit_job": CREATE_JOB_PLNREAS_SQLSTR,
        "plan_concept_laborlink_job": CREATE_JOB_PLNLABO_SQLSTR,
        "plan_conceptunit_job": CREATE_JOB_PLNCONC_SQLSTR,
        "planunit_job": CREATE_JOB_PLANUNIT_SQLSTR,
    }


def create_job_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_job_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)
