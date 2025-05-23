from src.a00_data_toolbox.db_toolbox import (
    create_update_inconsistency_error_query,
    create_table2table_agg_insert_query,
)
from src.a17_idea_logic.idea_db_tool import (
    get_default_sorted_list,
    create_idea_sorted_table,
)
from src.a17_idea_logic.idea_config import (
    get_quick_ideas_column_ref,
    get_idea_config_dict,
)
from sqlite3 import Connection as sqlite3_Connection

ALL_DIMEN_ABBV7 = {
    "FISCASH",
    "FISDEAL",
    "FISHOUR",
    "FISMONT",
    "FISWEEK",
    "FISOFFI",
    "FISUNIT",
    "BUDMEMB",
    "BUDACCT",
    "BUDAWAR",
    "BUDFACT",
    "BUDHEAL",
    "BUDPREM",
    "BUDREAS",
    "BUDLABO",
    "BUDCONC",
    "BUDUNIT",
    "PIDTITL",
    "PIDNAME",
    "PIDWAYY",
    "PIDLABE",
}


def get_dimen_abbv7(dimen: str) -> str:
    return {
        "fisc_cashbook": "FISCASH",
        "fisc_dealunit": "FISDEAL",
        "fisc_timeline_hour": "FISHOUR",
        "fisc_timeline_month": "FISMONT",
        "fisc_timeline_weekday": "FISWEEK",
        "fisc_timeoffi": "FISOFFI",
        "fiscunit": "FISUNIT",
        "bud_acct_membership": "BUDMEMB",
        "bud_acctunit": "BUDACCT",
        "bud_concept_awardlink": "BUDAWAR",
        "bud_concept_factunit": "BUDFACT",
        "bud_concept_healerlink": "BUDHEAL",
        "bud_concept_reason_premiseunit": "BUDPREM",
        "bud_concept_reasonunit": "BUDREAS",
        "bud_concept_laborlink": "BUDLABO",
        "bud_conceptunit": "BUDCONC",
        "budunit": "BUDUNIT",
        "pidgin_title": "PIDTITL",
        "pidgin_name": "PIDNAME",
        "pidgin_way": "PIDWAYY",
        "pidgin_label": "PIDLABE",
        "pidgin_core": "PIDCORE",
    }.get(dimen)


def create_prime_tablename(
    idea_dimen_or_abbv7: str, sound: str, stage: str, put_del: str = None
) -> str:
    abbv_references = {
        "FISCASH": "fisc_cashbook",
        "FISDEAL": "fisc_dealunit",
        "FISHOUR": "fisc_timeline_hour",
        "FISMONT": "fisc_timeline_month",
        "FISWEEK": "fisc_timeline_weekday",
        "FISOFFI": "fisc_timeoffi",
        "FISUNIT": "fiscunit",
        "BUDMEMB": "bud_acct_membership",
        "BUDACCT": "bud_acctunit",
        "BUDAWAR": "bud_concept_awardlink",
        "BUDFACT": "bud_concept_factunit",
        "BUDHEAL": "bud_concept_healerlink",
        "BUDPREM": "bud_concept_reason_premiseunit",
        "BUDREAS": "bud_concept_reasonunit",
        "BUDLABO": "bud_concept_laborlink",
        "BUDCONC": "bud_conceptunit",
        "BUDUNIT": "budunit",
        "PIDTITL": "pidgin_title",
        "PIDNAME": "pidgin_name",
        "PIDWAYY": "pidgin_way",
        "PIDLABE": "pidgin_label",
        "PIDCORE": "pidgin_core",
    }
    tablename = idea_dimen_or_abbv7
    if abbv_references.get(idea_dimen_or_abbv7.upper()):
        tablename = abbv_references.get(idea_dimen_or_abbv7.upper())
    if sound in {"s", "v"}:
        tablename = f"{tablename}_{sound}"

    return f"{tablename}_{put_del}_{stage}" if put_del else f"{tablename}_{stage}"


CREATE_PIDTITL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDTITL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_agg (event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDTITL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_vld (event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT)"""
CREATE_PIDNAME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_agg (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_vld (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT)"""
CREATE_PIDWAYY_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDWAYY_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_agg (event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDWAYY_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_vld (event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT)"""
CREATE_PIDLABE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_agg (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_vld (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT)"""

CREATE_PIDCORE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_raw (source_dimen TEXT, face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDCORE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_agg (face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT)"""
CREATE_PIDCORE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_vld (face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT)"""

CREATE_FISCASH_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISCASH_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_s_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISCASH_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISCASH_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_v_agg (fisc_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISDEAL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISDEAL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_s_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISDEAL_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISDEAL_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_v_agg (fisc_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISHOUR_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, cumlative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_FISHOUR_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_s_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, cumlative_minute INTEGER, hour_label TEXT)"""
CREATE_FISHOUR_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, cumlative_minute INTEGER, hour_label_otx TEXT, hour_label_inx TEXT, error_message TEXT)"""
CREATE_FISHOUR_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_v_agg (fisc_label TEXT, cumlative_minute INTEGER, hour_label TEXT)"""
CREATE_FISMONT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, cumlative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_FISMONT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_s_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, cumlative_day INTEGER, month_label TEXT)"""
CREATE_FISMONT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, cumlative_day INTEGER, month_label_otx TEXT, month_label_inx TEXT, error_message TEXT)"""
CREATE_FISMONT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_v_agg (fisc_label TEXT, cumlative_day INTEGER, month_label TEXT)"""
CREATE_FISWEEK_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_FISWEEK_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_s_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_FISWEEK_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, weekday_order INTEGER, weekday_label_otx TEXT, weekday_label_inx TEXT, error_message TEXT)"""
CREATE_FISWEEK_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_v_agg (fisc_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_FISOFFI_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISOFFI_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_s_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, offi_time INTEGER)"""
CREATE_FISOFFI_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISOFFI_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_v_agg (fisc_label TEXT, offi_time INTEGER)"""
CREATE_FISUNIT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_FISUNIT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_s_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""
CREATE_FISUNIT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, timeline_label_otx TEXT, timeline_label_inx TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_FISUNIT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_v_agg (fisc_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""

CREATE_BUDMEMB_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"
CREATE_BUDMEMB_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT)"
CREATE_BUDMEMB_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT)"
CREATE_BUDMEMB_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, group_title_otx TEXT, group_title_inx TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, group_title_ERASE_otx TEXT, group_title_ERASE_inx TEXT)"
CREATE_BUDMEMB_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT)"
CREATE_BUDACCT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"
CREATE_BUDACCT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDACCT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDACCT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_ERASE_otx TEXT, acct_name_ERASE_inx TEXT)"
CREATE_BUDACCT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDAWAR_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_awardlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_BUDAWAR_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_awardlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_awardlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT)"
CREATE_BUDAWAR_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_awardlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT)"
CREATE_BUDAWAR_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_awardlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, awardee_title_otx TEXT, awardee_title_inx TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_awardlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_awardlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, awardee_title_ERASE_otx TEXT, awardee_title_ERASE_inx TEXT)"
CREATE_BUDAWAR_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_awardlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT)"
CREATE_BUDFACT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_factunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL, error_message TEXT)"
CREATE_BUDFACT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_factunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_factunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT)"
CREATE_BUDFACT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_factunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT)"
CREATE_BUDFACT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_factunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, fcontext_otx TEXT, fcontext_inx TEXT, fbranch_otx TEXT, fbranch_inx TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_factunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_factunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, fcontext_ERASE_otx TEXT, fcontext_ERASE_inx TEXT)"
CREATE_BUDFACT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_factunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT)"
CREATE_BUDHEAL_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_healerlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT, error_message TEXT)"
CREATE_BUDHEAL_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_healerlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT)"
CREATE_BUDHEAL_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_healerlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT)"
CREATE_BUDHEAL_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_healerlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT)"
CREATE_BUDHEAL_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_healerlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, healer_name_otx TEXT, healer_name_inx TEXT)"
CREATE_BUDHEAL_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_healerlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT)"
CREATE_BUDHEAL_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_healerlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, healer_name_ERASE_otx TEXT, healer_name_ERASE_inx TEXT)"
CREATE_BUDHEAL_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_healerlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT)"
CREATE_BUDPREM_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER, error_message TEXT)"
CREATE_BUDPREM_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_BUDPREM_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch_ERASE TEXT)"
CREATE_BUDPREM_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch_ERASE TEXT)"
CREATE_BUDPREM_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, pbranch_otx TEXT, pbranch_inx TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_BUDPREM_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_BUDPREM_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, pbranch_ERASE_otx TEXT, pbranch_ERASE_inx TEXT)"
CREATE_BUDPREM_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch_ERASE TEXT)"
CREATE_BUDREAS_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rcontext_concept_active_requisite INTEGER, error_message TEXT)"
CREATE_BUDREAS_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rcontext_concept_active_requisite INTEGER)"
CREATE_BUDREAS_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT)"
CREATE_BUDREAS_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT)"
CREATE_BUDREAS_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, rcontext_concept_active_requisite INTEGER)"
CREATE_BUDREAS_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rcontext_concept_active_requisite INTEGER)"
CREATE_BUDREAS_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, rcontext_ERASE_otx TEXT, rcontext_ERASE_inx TEXT)"
CREATE_BUDREAS_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT)"
CREATE_BUDLABOR_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_laborlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT, error_message TEXT)"
CREATE_BUDLABOR_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_laborlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT)"
CREATE_BUDLABOR_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_laborlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT)"
CREATE_BUDLABOR_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_laborlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT)"
CREATE_BUDLABOR_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_laborlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, labor_title_otx TEXT, labor_title_inx TEXT)"
CREATE_BUDLABOR_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_laborlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT)"
CREATE_BUDLABOR_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_concept_laborlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, labor_title_ERASE_otx TEXT, labor_title_ERASE_inx TEXT)"
CREATE_BUDLABOR_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_concept_laborlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT)"
CREATE_BUDCONC_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_conceptunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_BUDCONC_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_conceptunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDCONC_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_conceptunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way_ERASE TEXT)"
CREATE_BUDCONC_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_conceptunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way_ERASE TEXT)"
CREATE_BUDCONC_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_conceptunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_otx TEXT, concept_way_inx TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDCONC_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_conceptunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDCONC_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_conceptunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, concept_way_ERASE_otx TEXT, concept_way_ERASE_inx TEXT)"
CREATE_BUDCONC_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_conceptunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way_ERASE TEXT)"
CREATE_BUDUNIT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"
CREATE_BUDUNIT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name_ERASE TEXT)"
CREATE_BUDUNIT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name_ERASE TEXT)"
CREATE_BUDUNIT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_label_otx TEXT, fisc_label_inx TEXT, owner_name_ERASE_otx TEXT, owner_name_ERASE_inx TEXT)"
CREATE_BUDUNIT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name_ERASE TEXT)"


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
        "fisc_cashbook_s_raw": CREATE_FISCASH_SOUND_RAW_SQLSTR,
        "fisc_cashbook_s_agg": CREATE_FISCASH_SOUND_AGG_SQLSTR,
        "fisc_cashbook_v_raw": CREATE_FISCASH_VOICE_RAW_SQLSTR,
        "fisc_cashbook_v_agg": CREATE_FISCASH_VOICE_AGG_SQLSTR,
        "fisc_dealunit_s_raw": CREATE_FISDEAL_SOUND_RAW_SQLSTR,
        "fisc_dealunit_s_agg": CREATE_FISDEAL_SOUND_AGG_SQLSTR,
        "fisc_dealunit_v_raw": CREATE_FISDEAL_VOICE_RAW_SQLSTR,
        "fisc_dealunit_v_agg": CREATE_FISDEAL_VOICE_AGG_SQLSTR,
        "fisc_timeline_hour_s_raw": CREATE_FISHOUR_SOUND_RAW_SQLSTR,
        "fisc_timeline_hour_s_agg": CREATE_FISHOUR_SOUND_AGG_SQLSTR,
        "fisc_timeline_hour_v_raw": CREATE_FISHOUR_VOICE_RAW_SQLSTR,
        "fisc_timeline_hour_v_agg": CREATE_FISHOUR_VOICE_AGG_SQLSTR,
        "fisc_timeline_month_s_raw": CREATE_FISMONT_SOUND_RAW_SQLSTR,
        "fisc_timeline_month_s_agg": CREATE_FISMONT_SOUND_AGG_SQLSTR,
        "fisc_timeline_month_v_raw": CREATE_FISMONT_VOICE_RAW_SQLSTR,
        "fisc_timeline_month_v_agg": CREATE_FISMONT_VOICE_AGG_SQLSTR,
        "fisc_timeline_weekday_s_raw": CREATE_FISWEEK_SOUND_RAW_SQLSTR,
        "fisc_timeline_weekday_s_agg": CREATE_FISWEEK_SOUND_AGG_SQLSTR,
        "fisc_timeline_weekday_v_raw": CREATE_FISWEEK_VOICE_RAW_SQLSTR,
        "fisc_timeline_weekday_v_agg": CREATE_FISWEEK_VOICE_AGG_SQLSTR,
        "fisc_timeoffi_s_raw": CREATE_FISOFFI_SOUND_RAW_SQLSTR,
        "fisc_timeoffi_s_agg": CREATE_FISOFFI_SOUND_AGG_SQLSTR,
        "fisc_timeoffi_v_raw": CREATE_FISOFFI_VOICE_RAW_SQLSTR,
        "fisc_timeoffi_v_agg": CREATE_FISOFFI_VOICE_AGG_SQLSTR,
        "fiscunit_s_raw": CREATE_FISUNIT_SOUND_RAW_SQLSTR,
        "fiscunit_s_agg": CREATE_FISUNIT_SOUND_AGG_SQLSTR,
        "fiscunit_v_raw": CREATE_FISUNIT_VOICE_RAW_SQLSTR,
        "fiscunit_v_agg": CREATE_FISUNIT_VOICE_AGG_SQLSTR,
        "bud_acct_membership_s_put_raw": CREATE_BUDMEMB_SOUND_PUT_RAW_STR,
        "bud_acct_membership_s_put_agg": CREATE_BUDMEMB_SOUND_PUT_AGG_STR,
        "bud_acct_membership_s_del_raw": CREATE_BUDMEMB_SOUND_DEL_RAW_STR,
        "bud_acct_membership_s_del_agg": CREATE_BUDMEMB_SOUND_DEL_AGG_STR,
        "bud_acct_membership_v_put_raw": CREATE_BUDMEMB_VOICE_PUT_RAW_STR,
        "bud_acct_membership_v_put_agg": CREATE_BUDMEMB_VOICE_PUT_AGG_STR,
        "bud_acct_membership_v_del_raw": CREATE_BUDMEMB_VOICE_DEL_RAW_STR,
        "bud_acct_membership_v_del_agg": CREATE_BUDMEMB_VOICE_DEL_AGG_STR,
        "bud_acctunit_s_put_raw": CREATE_BUDACCT_SOUND_PUT_RAW_STR,
        "bud_acctunit_s_put_agg": CREATE_BUDACCT_SOUND_PUT_AGG_STR,
        "bud_acctunit_s_del_raw": CREATE_BUDACCT_SOUND_DEL_RAW_STR,
        "bud_acctunit_s_del_agg": CREATE_BUDACCT_SOUND_DEL_AGG_STR,
        "bud_acctunit_v_put_raw": CREATE_BUDACCT_VOICE_PUT_RAW_STR,
        "bud_acctunit_v_put_agg": CREATE_BUDACCT_VOICE_PUT_AGG_STR,
        "bud_acctunit_v_del_raw": CREATE_BUDACCT_VOICE_DEL_RAW_STR,
        "bud_acctunit_v_del_agg": CREATE_BUDACCT_VOICE_DEL_AGG_STR,
        "bud_concept_awardlink_s_put_raw": CREATE_BUDAWAR_SOUND_PUT_RAW_STR,
        "bud_concept_awardlink_s_put_agg": CREATE_BUDAWAR_SOUND_PUT_AGG_STR,
        "bud_concept_awardlink_s_del_raw": CREATE_BUDAWAR_SOUND_DEL_RAW_STR,
        "bud_concept_awardlink_s_del_agg": CREATE_BUDAWAR_SOUND_DEL_AGG_STR,
        "bud_concept_awardlink_v_put_raw": CREATE_BUDAWAR_VOICE_PUT_RAW_STR,
        "bud_concept_awardlink_v_put_agg": CREATE_BUDAWAR_VOICE_PUT_AGG_STR,
        "bud_concept_awardlink_v_del_raw": CREATE_BUDAWAR_VOICE_DEL_RAW_STR,
        "bud_concept_awardlink_v_del_agg": CREATE_BUDAWAR_VOICE_DEL_AGG_STR,
        "bud_concept_factunit_s_put_raw": CREATE_BUDFACT_SOUND_PUT_RAW_STR,
        "bud_concept_factunit_s_put_agg": CREATE_BUDFACT_SOUND_PUT_AGG_STR,
        "bud_concept_factunit_s_del_raw": CREATE_BUDFACT_SOUND_DEL_RAW_STR,
        "bud_concept_factunit_s_del_agg": CREATE_BUDFACT_SOUND_DEL_AGG_STR,
        "bud_concept_factunit_v_put_raw": CREATE_BUDFACT_VOICE_PUT_RAW_STR,
        "bud_concept_factunit_v_put_agg": CREATE_BUDFACT_VOICE_PUT_AGG_STR,
        "bud_concept_factunit_v_del_raw": CREATE_BUDFACT_VOICE_DEL_RAW_STR,
        "bud_concept_factunit_v_del_agg": CREATE_BUDFACT_VOICE_DEL_AGG_STR,
        "bud_concept_healerlink_s_put_raw": CREATE_BUDHEAL_SOUND_PUT_RAW_STR,
        "bud_concept_healerlink_s_put_agg": CREATE_BUDHEAL_SOUND_PUT_AGG_STR,
        "bud_concept_healerlink_s_del_raw": CREATE_BUDHEAL_SOUND_DEL_RAW_STR,
        "bud_concept_healerlink_s_del_agg": CREATE_BUDHEAL_SOUND_DEL_AGG_STR,
        "bud_concept_healerlink_v_put_raw": CREATE_BUDHEAL_VOICE_PUT_RAW_STR,
        "bud_concept_healerlink_v_put_agg": CREATE_BUDHEAL_VOICE_PUT_AGG_STR,
        "bud_concept_healerlink_v_del_raw": CREATE_BUDHEAL_VOICE_DEL_RAW_STR,
        "bud_concept_healerlink_v_del_agg": CREATE_BUDHEAL_VOICE_DEL_AGG_STR,
        "bud_concept_reason_premiseunit_s_put_raw": CREATE_BUDPREM_SOUND_PUT_RAW_STR,
        "bud_concept_reason_premiseunit_s_put_agg": CREATE_BUDPREM_SOUND_PUT_AGG_STR,
        "bud_concept_reason_premiseunit_s_del_raw": CREATE_BUDPREM_SOUND_DEL_RAW_STR,
        "bud_concept_reason_premiseunit_s_del_agg": CREATE_BUDPREM_SOUND_DEL_AGG_STR,
        "bud_concept_reason_premiseunit_v_put_raw": CREATE_BUDPREM_VOICE_PUT_RAW_STR,
        "bud_concept_reason_premiseunit_v_put_agg": CREATE_BUDPREM_VOICE_PUT_AGG_STR,
        "bud_concept_reason_premiseunit_v_del_raw": CREATE_BUDPREM_VOICE_DEL_RAW_STR,
        "bud_concept_reason_premiseunit_v_del_agg": CREATE_BUDPREM_VOICE_DEL_AGG_STR,
        "bud_concept_reasonunit_s_put_raw": CREATE_BUDREAS_SOUND_PUT_RAW_STR,
        "bud_concept_reasonunit_s_put_agg": CREATE_BUDREAS_SOUND_PUT_AGG_STR,
        "bud_concept_reasonunit_s_del_raw": CREATE_BUDREAS_SOUND_DEL_RAW_STR,
        "bud_concept_reasonunit_s_del_agg": CREATE_BUDREAS_SOUND_DEL_AGG_STR,
        "bud_concept_reasonunit_v_put_raw": CREATE_BUDREAS_VOICE_PUT_RAW_STR,
        "bud_concept_reasonunit_v_put_agg": CREATE_BUDREAS_VOICE_PUT_AGG_STR,
        "bud_concept_reasonunit_v_del_raw": CREATE_BUDREAS_VOICE_DEL_RAW_STR,
        "bud_concept_reasonunit_v_del_agg": CREATE_BUDREAS_VOICE_DEL_AGG_STR,
        "bud_concept_laborlink_s_put_raw": CREATE_BUDLABOR_SOUND_PUT_RAW_STR,
        "bud_concept_laborlink_s_put_agg": CREATE_BUDLABOR_SOUND_PUT_AGG_STR,
        "bud_concept_laborlink_s_del_raw": CREATE_BUDLABOR_SOUND_DEL_RAW_STR,
        "bud_concept_laborlink_s_del_agg": CREATE_BUDLABOR_SOUND_DEL_AGG_STR,
        "bud_concept_laborlink_v_put_raw": CREATE_BUDLABOR_VOICE_PUT_RAW_STR,
        "bud_concept_laborlink_v_put_agg": CREATE_BUDLABOR_VOICE_PUT_AGG_STR,
        "bud_concept_laborlink_v_del_raw": CREATE_BUDLABOR_VOICE_DEL_RAW_STR,
        "bud_concept_laborlink_v_del_agg": CREATE_BUDLABOR_VOICE_DEL_AGG_STR,
        "bud_conceptunit_s_put_raw": CREATE_BUDCONC_SOUND_PUT_RAW_STR,
        "bud_conceptunit_s_put_agg": CREATE_BUDCONC_SOUND_PUT_AGG_STR,
        "bud_conceptunit_s_del_raw": CREATE_BUDCONC_SOUND_DEL_RAW_STR,
        "bud_conceptunit_s_del_agg": CREATE_BUDCONC_SOUND_DEL_AGG_STR,
        "bud_conceptunit_v_put_raw": CREATE_BUDCONC_VOICE_PUT_RAW_STR,
        "bud_conceptunit_v_put_agg": CREATE_BUDCONC_VOICE_PUT_AGG_STR,
        "bud_conceptunit_v_del_raw": CREATE_BUDCONC_VOICE_DEL_RAW_STR,
        "bud_conceptunit_v_del_agg": CREATE_BUDCONC_VOICE_DEL_AGG_STR,
        "budunit_s_put_raw": CREATE_BUDUNIT_SOUND_PUT_RAW_STR,
        "budunit_s_put_agg": CREATE_BUDUNIT_SOUND_PUT_AGG_STR,
        "budunit_s_del_raw": CREATE_BUDUNIT_SOUND_DEL_RAW_STR,
        "budunit_s_del_agg": CREATE_BUDUNIT_SOUND_DEL_AGG_STR,
        "budunit_v_put_raw": CREATE_BUDUNIT_VOICE_PUT_RAW_STR,
        "budunit_v_put_agg": CREATE_BUDUNIT_VOICE_PUT_AGG_STR,
        "budunit_v_del_raw": CREATE_BUDUNIT_VOICE_DEL_RAW_STR,
        "budunit_v_del_agg": CREATE_BUDUNIT_VOICE_DEL_AGG_STR,
    }


def get_bud_voice_agg_tablenames() -> set[str]:
    return {
        "budunit_v_put_agg",
        "bud_concept_healerlink_v_put_agg",
        "bud_acctunit_v_put_agg",
        "bud_concept_reason_premiseunit_v_put_agg",
        "bud_concept_laborlink_v_put_agg",
        "bud_concept_reasonunit_v_put_agg",
        "bud_concept_factunit_v_put_agg",
        "bud_acct_membership_v_put_agg",
        "bud_conceptunit_v_put_agg",
        "bud_concept_awardlink_v_put_agg",
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
    if dimen.lower().startswith("fisc"):
        exclude_cols = {"idea_number", "event_int", "face_name", "error_message"}
    else:
        exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("bud"):
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

    if dimen.lower().startswith("fisc"):
        exclude_cols = {"idea_number", "event_int", "face_name", "error_message"}
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns.remove("event_int")
        dimen_focus_columns.remove("face_name")
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    else:
        exclude_cols = {"idea_number", "error_message"}

    if dimen.lower().startswith("bud"):
        agg_tablename = create_prime_tablename(dimen, "s", "agg", "put")
        raw_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        raw_tablename = create_prime_tablename(dimen, "s", "raw")
        agg_tablename = create_prime_tablename(dimen, "s", "agg")

    pidgin_fisc_bud_put_sqlstr = create_table2table_agg_insert_query(
        conn_or_cursor,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
    )
    sqlstrs = [pidgin_fisc_bud_put_sqlstr]
    if dimen.lower().startswith("bud"):
        del_raw_tablename = create_prime_tablename(dimen, "s", "raw", "del")
        del_agg_tablename = create_prime_tablename(dimen, "s", "agg", "del")
        bud_del_sqlstr = create_table2table_agg_insert_query(
            conn_or_cursor,
            src_table=del_raw_tablename,
            dst_table=del_agg_tablename,
            focus_cols=None,
            exclude_cols=exclude_cols,
            where_block="",
        )
        sqlstrs.append(bud_del_sqlstr)

    return sqlstrs


def create_insert_into_pidgin_core_raw_sqlstr(dimen: str) -> str:
    pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
    pidgin_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    return f"""INSERT INTO {pidgin_core_s_raw_tablename} (source_dimen, face_name, otx_bridge, inx_bridge, unknown_term)
SELECT '{pidgin_s_agg_tablename}', face_name, otx_bridge, inx_bridge, unknown_term
FROM {pidgin_s_agg_tablename}
GROUP BY face_name, otx_bridge, inx_bridge, unknown_term
;
"""


def create_insert_into_pidgin_core_vld_sqlstr(
    default_bridge: str, default_unknown: str
):
    return f"""INSERT INTO pidgin_core_s_vld (face_name, otx_bridge, inx_bridge, unknown_term)
SELECT
  face_name
, IFNULL(otx_bridge, '{default_bridge}')
, IFNULL(inx_bridge, '{default_bridge}')
, IFNULL(unknown_term, '{default_unknown}')
FROM pidgin_core_s_agg
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
SET error_message = 'Bridge cannot exist in LabelStr'
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
SET error_message = 'Bridge must exist in WayStr'
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
SET error_message = 'Bridge cannot exist in NameStr'
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


INSERT_FISCASH_VOICE_RAW_SQLSTR = "INSERT INTO fisc_cashbook_v_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, acct_name_otx, tran_time, amount) SELECT event_int, face_name, fisc_label, owner_name, acct_name, tran_time, amount FROM fisc_cashbook_s_agg "
INSERT_FISDEAL_VOICE_RAW_SQLSTR = "INSERT INTO fisc_dealunit_v_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, deal_time, quota, celldepth) SELECT event_int, face_name, fisc_label, owner_name, deal_time, quota, celldepth FROM fisc_dealunit_s_agg "
INSERT_FISHOUR_VOICE_RAW_SQLSTR = "INSERT INTO fisc_timeline_hour_v_raw (event_int, face_name_otx, fisc_label_otx, cumlative_minute, hour_label_otx) SELECT event_int, face_name, fisc_label, cumlative_minute, hour_label FROM fisc_timeline_hour_s_agg "
INSERT_FISMONT_VOICE_RAW_SQLSTR = "INSERT INTO fisc_timeline_month_v_raw (event_int, face_name_otx, fisc_label_otx, cumlative_day, month_label_otx) SELECT event_int, face_name, fisc_label, cumlative_day, month_label FROM fisc_timeline_month_s_agg "
INSERT_FISWEEK_VOICE_RAW_SQLSTR = "INSERT INTO fisc_timeline_weekday_v_raw (event_int, face_name_otx, fisc_label_otx, weekday_order, weekday_label_otx) SELECT event_int, face_name, fisc_label, weekday_order, weekday_label FROM fisc_timeline_weekday_s_agg "
INSERT_FISOFFI_VOICE_RAW_SQLSTR = "INSERT INTO fisc_timeoffi_v_raw (event_int, face_name_otx, fisc_label_otx, offi_time) SELECT event_int, face_name, fisc_label, offi_time FROM fisc_timeoffi_s_agg "
INSERT_FISUNIT_VOICE_RAW_SQLSTR = "INSERT INTO fiscunit_v_raw (event_int, face_name_otx, fisc_label_otx, timeline_label_otx, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations) SELECT event_int, face_name, fisc_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations FROM fiscunit_s_agg "

INSERT_BUDMEMB_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_acct_membership_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, acct_name_otx, group_title_otx, credit_vote, debtit_vote) SELECT event_int, face_name, fisc_label, owner_name, acct_name, group_title, credit_vote, debtit_vote FROM bud_acct_membership_s_put_agg "
INSERT_BUDMEMB_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_acct_membership_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, acct_name_otx, group_title_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, acct_name, group_title_ERASE FROM bud_acct_membership_s_del_agg "
INSERT_BUDACCT_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_acctunit_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, acct_name_otx, credit_belief, debtit_belief) SELECT event_int, face_name, fisc_label, owner_name, acct_name, credit_belief, debtit_belief FROM bud_acctunit_s_put_agg "
INSERT_BUDACCT_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_acctunit_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, acct_name_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, acct_name_ERASE FROM bud_acctunit_s_del_agg "
INSERT_BUDAWAR_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_concept_awardlink_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, awardee_title_otx, give_force, take_force) SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title, give_force, take_force FROM bud_concept_awardlink_s_put_agg "
INSERT_BUDAWAR_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_concept_awardlink_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, awardee_title_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title_ERASE FROM bud_concept_awardlink_s_del_agg "
INSERT_BUDFACT_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_concept_factunit_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, fcontext_otx, fbranch_otx, fopen, fnigh) SELECT event_int, face_name, fisc_label, owner_name, concept_way, fcontext, fbranch, fopen, fnigh FROM bud_concept_factunit_s_put_agg "
INSERT_BUDFACT_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_concept_factunit_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, fcontext_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way, fcontext_ERASE FROM bud_concept_factunit_s_del_agg "
INSERT_BUDHEAL_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_concept_healerlink_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, healer_name_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way, healer_name FROM bud_concept_healerlink_s_put_agg "
INSERT_BUDHEAL_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_concept_healerlink_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, healer_name_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way, healer_name_ERASE FROM bud_concept_healerlink_s_del_agg "
INSERT_BUDPREM_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_concept_reason_premiseunit_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, rcontext_otx, pbranch_otx, pnigh, popen, pdivisor) SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch, pnigh, popen, pdivisor FROM bud_concept_reason_premiseunit_s_put_agg "
INSERT_BUDPREM_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_concept_reason_premiseunit_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, rcontext_otx, pbranch_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch_ERASE FROM bud_concept_reason_premiseunit_s_del_agg "
INSERT_BUDREAS_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_concept_reasonunit_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, rcontext_otx, rcontext_concept_active_requisite) SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext, rcontext_concept_active_requisite FROM bud_concept_reasonunit_s_put_agg "
INSERT_BUDREAS_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_concept_reasonunit_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, rcontext_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext_ERASE FROM bud_concept_reasonunit_s_del_agg "
INSERT_BUDLABO_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_concept_laborlink_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, labor_title_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way, labor_title FROM bud_concept_laborlink_s_put_agg "
INSERT_BUDLABO_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_concept_laborlink_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, labor_title_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way, labor_title_ERASE FROM bud_concept_laborlink_s_del_agg "
INSERT_BUDCONC_VOICE_RAW_PUT_SQLSTR = "INSERT INTO bud_conceptunit_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_otx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool) SELECT event_int, face_name, fisc_label, owner_name, concept_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool FROM bud_conceptunit_s_put_agg "
INSERT_BUDCONC_VOICE_RAW_DEL_SQLSTR = "INSERT INTO bud_conceptunit_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, concept_way_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name, concept_way_ERASE FROM bud_conceptunit_s_del_agg "
INSERT_BUDUNIT_VOICE_RAW_PUT_SQLSTR = "INSERT INTO budunit_v_put_raw (event_int, face_name_otx, fisc_label_otx, owner_name_otx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit) SELECT event_int, face_name, fisc_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit FROM budunit_s_put_agg "
INSERT_BUDUNIT_VOICE_RAW_DEL_SQLSTR = "INSERT INTO budunit_v_del_raw (event_int, face_name_otx, fisc_label_otx, owner_name_ERASE_otx) SELECT event_int, face_name, fisc_label, owner_name_ERASE FROM budunit_s_del_agg "


def get_insert_into_voice_raw_sqlstrs() -> dict[str, str]:
    return {
        "fisc_cashbook_v_raw": INSERT_FISCASH_VOICE_RAW_SQLSTR,
        "fisc_dealunit_v_raw": INSERT_FISDEAL_VOICE_RAW_SQLSTR,
        "fisc_timeline_hour_v_raw": INSERT_FISHOUR_VOICE_RAW_SQLSTR,
        "fisc_timeline_month_v_raw": INSERT_FISMONT_VOICE_RAW_SQLSTR,
        "fisc_timeline_weekday_v_raw": INSERT_FISWEEK_VOICE_RAW_SQLSTR,
        "fisc_timeoffi_v_raw": INSERT_FISOFFI_VOICE_RAW_SQLSTR,
        "fiscunit_v_raw": INSERT_FISUNIT_VOICE_RAW_SQLSTR,
        "bud_acct_membership_v_put_raw": INSERT_BUDMEMB_VOICE_RAW_PUT_SQLSTR,
        "bud_acct_membership_v_del_raw": INSERT_BUDMEMB_VOICE_RAW_DEL_SQLSTR,
        "bud_acctunit_v_put_raw": INSERT_BUDACCT_VOICE_RAW_PUT_SQLSTR,
        "bud_acctunit_v_del_raw": INSERT_BUDACCT_VOICE_RAW_DEL_SQLSTR,
        "bud_concept_awardlink_v_put_raw": INSERT_BUDAWAR_VOICE_RAW_PUT_SQLSTR,
        "bud_concept_awardlink_v_del_raw": INSERT_BUDAWAR_VOICE_RAW_DEL_SQLSTR,
        "bud_concept_factunit_v_put_raw": INSERT_BUDFACT_VOICE_RAW_PUT_SQLSTR,
        "bud_concept_factunit_v_del_raw": INSERT_BUDFACT_VOICE_RAW_DEL_SQLSTR,
        "bud_concept_healerlink_v_put_raw": INSERT_BUDHEAL_VOICE_RAW_PUT_SQLSTR,
        "bud_concept_healerlink_v_del_raw": INSERT_BUDHEAL_VOICE_RAW_DEL_SQLSTR,
        "bud_concept_reason_premiseunit_v_put_raw": INSERT_BUDPREM_VOICE_RAW_PUT_SQLSTR,
        "bud_concept_reason_premiseunit_v_del_raw": INSERT_BUDPREM_VOICE_RAW_DEL_SQLSTR,
        "bud_concept_reasonunit_v_put_raw": INSERT_BUDREAS_VOICE_RAW_PUT_SQLSTR,
        "bud_concept_reasonunit_v_del_raw": INSERT_BUDREAS_VOICE_RAW_DEL_SQLSTR,
        "bud_concept_laborlink_v_put_raw": INSERT_BUDLABO_VOICE_RAW_PUT_SQLSTR,
        "bud_concept_laborlink_v_del_raw": INSERT_BUDLABO_VOICE_RAW_DEL_SQLSTR,
        "bud_conceptunit_v_put_raw": INSERT_BUDCONC_VOICE_RAW_PUT_SQLSTR,
        "bud_conceptunit_v_del_raw": INSERT_BUDCONC_VOICE_RAW_DEL_SQLSTR,
        "budunit_v_put_raw": INSERT_BUDUNIT_VOICE_RAW_PUT_SQLSTR,
        "budunit_v_del_raw": INSERT_BUDUNIT_VOICE_RAW_DEL_SQLSTR,
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


FISCASH_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO fisc_cashbook_v_agg (fisc_label, owner_name, acct_name, tran_time, amount)
SELECT fisc_label_inx, owner_name_inx, acct_name_inx, tran_time, amount
FROM fisc_cashbook_v_raw
GROUP BY fisc_label_inx, owner_name_inx, acct_name_inx, tran_time, amount
"""
FISDEAL_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO fisc_dealunit_v_agg (fisc_label, owner_name, deal_time, quota, celldepth)
SELECT fisc_label_inx, owner_name_inx, deal_time, quota, celldepth
FROM fisc_dealunit_v_raw
GROUP BY fisc_label_inx, owner_name_inx, deal_time, quota, celldepth
"""
FISHOUR_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO fisc_timeline_hour_v_agg (fisc_label, cumlative_minute, hour_label)
SELECT fisc_label_inx, cumlative_minute, hour_label_inx
FROM fisc_timeline_hour_v_raw
GROUP BY fisc_label_inx, cumlative_minute, hour_label_inx
"""
FISMONT_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO fisc_timeline_month_v_agg (fisc_label, cumlative_day, month_label)
SELECT fisc_label_inx, cumlative_day, month_label_inx
FROM fisc_timeline_month_v_raw
GROUP BY fisc_label_inx, cumlative_day, month_label_inx
"""
FISWEEK_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO fisc_timeline_weekday_v_agg (fisc_label, weekday_order, weekday_label)
SELECT fisc_label_inx, weekday_order, weekday_label_inx
FROM fisc_timeline_weekday_v_raw
GROUP BY fisc_label_inx, weekday_order, weekday_label_inx
"""
FISOFFI_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO fisc_timeoffi_v_agg (fisc_label, offi_time)
SELECT fisc_label_inx, offi_time
FROM fisc_timeoffi_v_raw
GROUP BY fisc_label_inx, offi_time
"""
FISUNIT_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO fiscunit_v_agg (fisc_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations)
SELECT fisc_label_inx, timeline_label_inx, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations
FROM fiscunit_v_raw
GROUP BY fisc_label_inx, timeline_label_inx, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations
"""

INSERT_BUDMEMB_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_acct_membership_v_put_agg (event_int, face_name, fisc_label, owner_name, acct_name, group_title, credit_vote, debtit_vote)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, acct_name_inx, group_title_inx, credit_vote, debtit_vote
FROM bud_acct_membership_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, acct_name_inx, group_title_inx, credit_vote, debtit_vote
"""
INSERT_BUDMEMB_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_acct_membership_v_del_agg (event_int, face_name, fisc_label, owner_name, acct_name, group_title_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, acct_name_inx, group_title_ERASE_inx
FROM bud_acct_membership_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, acct_name_inx, group_title_ERASE_inx
"""
INSERT_BUDACCT_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_acctunit_v_put_agg (event_int, face_name, fisc_label, owner_name, acct_name, credit_belief, debtit_belief)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, acct_name_inx, credit_belief, debtit_belief
FROM bud_acctunit_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, acct_name_inx, credit_belief, debtit_belief
"""
INSERT_BUDACCT_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_acctunit_v_del_agg (event_int, face_name, fisc_label, owner_name, acct_name_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, acct_name_ERASE_inx
FROM bud_acctunit_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, acct_name_ERASE_inx
"""
INSERT_BUDAWAR_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_concept_awardlink_v_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, awardee_title, give_force, take_force)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, awardee_title_inx, give_force, take_force
FROM bud_concept_awardlink_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, awardee_title_inx, give_force, take_force
"""
INSERT_BUDAWAR_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_concept_awardlink_v_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, awardee_title_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, awardee_title_ERASE_inx
FROM bud_concept_awardlink_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, awardee_title_ERASE_inx
"""
INSERT_BUDFACT_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_concept_factunit_v_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, fcontext, fbranch, fopen, fnigh)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, fcontext_inx, fbranch_inx, fopen, fnigh
FROM bud_concept_factunit_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, fcontext_inx, fbranch_inx, fopen, fnigh
"""
INSERT_BUDFACT_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_concept_factunit_v_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, fcontext_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, fcontext_ERASE_inx
FROM bud_concept_factunit_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, fcontext_ERASE_inx
"""
INSERT_BUDHEAL_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_concept_healerlink_v_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, healer_name)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, healer_name_inx
FROM bud_concept_healerlink_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, healer_name_inx
"""
INSERT_BUDHEAL_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_concept_healerlink_v_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, healer_name_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, healer_name_ERASE_inx
FROM bud_concept_healerlink_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, healer_name_ERASE_inx
"""
INSERT_BUDPREM_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_concept_reason_premiseunit_v_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch, pnigh, popen, pdivisor)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, pbranch_inx, pnigh, popen, pdivisor
FROM bud_concept_reason_premiseunit_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, pbranch_inx, pnigh, popen, pdivisor
"""
INSERT_BUDPREM_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_concept_reason_premiseunit_v_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, pbranch_ERASE_inx
FROM bud_concept_reason_premiseunit_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, pbranch_ERASE_inx
"""
INSERT_BUDREAS_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_concept_reasonunit_v_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, rcontext, rcontext_concept_active_requisite)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, rcontext_concept_active_requisite
FROM bud_concept_reasonunit_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, rcontext_inx, rcontext_concept_active_requisite
"""
INSERT_BUDREAS_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_concept_reasonunit_v_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, rcontext_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, rcontext_ERASE_inx
FROM bud_concept_reasonunit_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, rcontext_ERASE_inx
"""
INSERT_BUDLABO_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_concept_laborlink_v_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, labor_title)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, labor_title_inx
FROM bud_concept_laborlink_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, labor_title_inx
"""
INSERT_BUDLABO_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_concept_laborlink_v_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, labor_title_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, labor_title_ERASE_inx
FROM bud_concept_laborlink_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, labor_title_ERASE_inx
"""
INSERT_BUDCONC_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO bud_conceptunit_v_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool
FROM bud_conceptunit_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool
"""
INSERT_BUDCONC_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO bud_conceptunit_v_del_agg (event_int, face_name, fisc_label, owner_name, concept_way_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_ERASE_inx
FROM bud_conceptunit_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, concept_way_ERASE_inx
"""
INSERT_BUDUNIT_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO budunit_v_put_agg (event_int, face_name, fisc_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit
FROM budunit_v_put_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit
"""
INSERT_BUDUNIT_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO budunit_v_del_agg (event_int, face_name, fisc_label, owner_name_ERASE)
SELECT event_int, face_name_inx, fisc_label_inx, owner_name_ERASE_inx
FROM budunit_v_del_raw
GROUP BY event_int, face_name_inx, fisc_label_inx, owner_name_ERASE_inx
"""


def get_insert_voice_agg_sqlstrs() -> dict[str, str]:
    return {
        "fisc_cashbook": FISCASH_VOICE_AGG_INSERT_SQLSTR,
        "fisc_dealunit": FISDEAL_VOICE_AGG_INSERT_SQLSTR,
        "fisc_timeline_hour": FISHOUR_VOICE_AGG_INSERT_SQLSTR,
        "fisc_timeline_month": FISMONT_VOICE_AGG_INSERT_SQLSTR,
        "fisc_timeline_weekday": FISWEEK_VOICE_AGG_INSERT_SQLSTR,
        "fisc_timeoffi": FISOFFI_VOICE_AGG_INSERT_SQLSTR,
        "fiscunit": FISUNIT_VOICE_AGG_INSERT_SQLSTR,
        "bud_acct_membership_v_put_agg": INSERT_BUDMEMB_VOICE_AGG_PUT_SQLSTR,
        "bud_acct_membership_v_del_agg": INSERT_BUDMEMB_VOICE_AGG_DEL_SQLSTR,
        "bud_acctunit_v_put_agg": INSERT_BUDACCT_VOICE_AGG_PUT_SQLSTR,
        "bud_acctunit_v_del_agg": INSERT_BUDACCT_VOICE_AGG_DEL_SQLSTR,
        "bud_concept_awardlink_v_put_agg": INSERT_BUDAWAR_VOICE_AGG_PUT_SQLSTR,
        "bud_concept_awardlink_v_del_agg": INSERT_BUDAWAR_VOICE_AGG_DEL_SQLSTR,
        "bud_concept_factunit_v_put_agg": INSERT_BUDFACT_VOICE_AGG_PUT_SQLSTR,
        "bud_concept_factunit_v_del_agg": INSERT_BUDFACT_VOICE_AGG_DEL_SQLSTR,
        "bud_concept_healerlink_v_put_agg": INSERT_BUDHEAL_VOICE_AGG_PUT_SQLSTR,
        "bud_concept_healerlink_v_del_agg": INSERT_BUDHEAL_VOICE_AGG_DEL_SQLSTR,
        "bud_concept_reason_premiseunit_v_put_agg": INSERT_BUDPREM_VOICE_AGG_PUT_SQLSTR,
        "bud_concept_reason_premiseunit_v_del_agg": INSERT_BUDPREM_VOICE_AGG_DEL_SQLSTR,
        "bud_concept_reasonunit_v_put_agg": INSERT_BUDREAS_VOICE_AGG_PUT_SQLSTR,
        "bud_concept_reasonunit_v_del_agg": INSERT_BUDREAS_VOICE_AGG_DEL_SQLSTR,
        "bud_concept_laborlink_v_put_agg": INSERT_BUDLABO_VOICE_AGG_PUT_SQLSTR,
        "bud_concept_laborlink_v_del_agg": INSERT_BUDLABO_VOICE_AGG_DEL_SQLSTR,
        "bud_conceptunit_v_put_agg": INSERT_BUDCONC_VOICE_AGG_PUT_SQLSTR,
        "bud_conceptunit_v_del_agg": INSERT_BUDCONC_VOICE_AGG_DEL_SQLSTR,
        "budunit_v_put_agg": INSERT_BUDUNIT_VOICE_AGG_PUT_SQLSTR,
        "budunit_v_del_agg": INSERT_BUDUNIT_VOICE_AGG_DEL_SQLSTR,
    }


FISCASH_FU2_SELECT_SQLSTR = "SELECT fisc_label, owner_name, acct_name, tran_time, amount FROM fisc_cashbook_v_agg WHERE fisc_label = "
FISDEAL_FU2_SELECT_SQLSTR = "SELECT fisc_label, owner_name, deal_time, quota, celldepth FROM fisc_dealunit_v_agg WHERE fisc_label = "
FISHOUR_FU2_SELECT_SQLSTR = "SELECT fisc_label, cumlative_minute, hour_label FROM fisc_timeline_hour_v_agg WHERE fisc_label = "
FISMONT_FU2_SELECT_SQLSTR = "SELECT fisc_label, cumlative_day, month_label FROM fisc_timeline_month_v_agg WHERE fisc_label = "
FISWEEK_FU2_SELECT_SQLSTR = "SELECT fisc_label, weekday_order, weekday_label FROM fisc_timeline_weekday_v_agg WHERE fisc_label = "
FISOFFI_FU2_SELECT_SQLSTR = (
    "SELECT fisc_label, offi_time FROM fisc_timeoffi_v_agg WHERE fisc_label = "
)
FISUNIT_FU2_SELECT_SQLSTR = "SELECT fisc_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations FROM fiscunit_v_agg WHERE fisc_label = "


def get_fisc_voice_select1_sqlstrs(fisc_label: str) -> dict[str, str]:
    return {
        "fiscunit": f"{FISUNIT_FU2_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_dealunit": f"{FISDEAL_FU2_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_cashbook": f"{FISCASH_FU2_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_timeline_hour": f"{FISHOUR_FU2_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_timeline_month": f"{FISMONT_FU2_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_timeline_weekday": f"{FISWEEK_FU2_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_timeoffi": f"{FISOFFI_FU2_SELECT_SQLSTR}'{fisc_label}'",
    }


def get_idea_stageble_put_dimens() -> dict[str, list[str]]:
    return {
        "br00000": ["fiscunit"],
        "br00001": ["budunit", "fisc_dealunit", "fiscunit"],
        "br00002": ["bud_acctunit", "budunit", "fisc_cashbook", "fiscunit"],
        "br00003": ["fisc_timeline_hour", "fiscunit"],
        "br00004": ["fisc_timeline_month", "fiscunit"],
        "br00005": ["fisc_timeline_weekday", "fiscunit"],
        "br00006": ["fisc_timeoffi", "fiscunit"],
        "br00011": ["bud_acctunit", "budunit", "fiscunit"],
        "br00012": ["bud_acct_membership", "bud_acctunit", "budunit", "fiscunit"],
        "br00013": ["bud_conceptunit", "budunit", "fiscunit"],
        "br00019": ["bud_conceptunit", "budunit", "fiscunit"],
        "br00020": ["bud_acct_membership", "bud_acctunit", "budunit", "fiscunit"],
        "br00021": ["bud_acctunit", "budunit", "fiscunit"],
        "br00022": ["bud_concept_awardlink", "bud_conceptunit", "budunit", "fiscunit"],
        "br00023": ["bud_concept_factunit", "bud_conceptunit", "budunit", "fiscunit"],
        "br00024": ["bud_concept_laborlink", "bud_conceptunit", "budunit", "fiscunit"],
        "br00025": ["bud_concept_healerlink", "bud_conceptunit", "budunit", "fiscunit"],
        "br00026": [
            "bud_concept_reason_premiseunit",
            "bud_concept_reasonunit",
            "bud_conceptunit",
            "budunit",
            "fiscunit",
        ],
        "br00027": ["bud_concept_reasonunit", "bud_conceptunit", "budunit", "fiscunit"],
        "br00028": ["bud_conceptunit", "budunit", "fiscunit"],
        "br00029": ["budunit", "fiscunit"],
        "br00036": ["bud_concept_healerlink", "bud_conceptunit", "budunit", "fiscunit"],
        "br00042": [],
        "br00043": [],
        "br00044": [],
        "br00045": [],
        "br00050": ["bud_acctunit", "budunit", "fiscunit"],
        "br00051": ["budunit", "fiscunit"],
        "br00052": ["bud_conceptunit", "budunit", "fiscunit"],
        "br00053": ["bud_conceptunit", "budunit", "fiscunit"],
        "br00054": ["bud_conceptunit", "budunit", "fiscunit"],
        "br00055": ["bud_conceptunit", "budunit", "fiscunit"],
        "br00056": ["bud_concept_reasonunit", "bud_conceptunit", "budunit", "fiscunit"],
        "br00057": ["bud_conceptunit", "budunit", "fiscunit"],
        "br00058": ["budunit", "fiscunit"],
        "br00059": ["fiscunit"],
        "br00113": ["bud_acctunit", "budunit", "fiscunit"],
        "br00115": ["bud_acctunit", "budunit", "fiscunit"],
        "br00116": ["bud_acctunit", "budunit", "fiscunit"],
        "br00117": ["bud_acctunit", "budunit", "fiscunit"],
    }


IDEA_STAGEBLE_DEL_DIMENS = {
    "br00050": ["bud_acct_membership"],
    "br00051": ["bud_acctunit"],
    "br00052": ["bud_concept_awardlink"],
    "br00053": ["bud_concept_factunit"],
    "br00054": ["bud_concept_laborlink"],
    "br00055": ["bud_concept_healerlink"],
    "br00056": ["bud_concept_reason_premiseunit"],
    "br00057": ["bud_concept_reasonunit"],
    "br00058": ["bud_conceptunit"],
    "br00059": ["budunit"],
}


CREATE_FISC_EVENT_TIME_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
  fisc_label TEXT
, event_int INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
INSERT_FISC_EVENT_TIME_AGG_SQLSTR = """
INSERT INTO fisc_event_time_agg (fisc_label, event_int, agg_time)
SELECT fisc_label, event_int, agg_time
FROM (
    SELECT fisc_label, event_int, tran_time as agg_time
    FROM fisc_cashbook_raw
    GROUP BY fisc_label, event_int, tran_time
    UNION 
    SELECT fisc_label, event_int, deal_time as agg_time
    FROM fisc_dealunit_raw
    GROUP BY fisc_label, event_int, deal_time
)
ORDER BY fisc_label, event_int, agg_time
;
"""
UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR = """
WITH EventTimeOrdered AS (
    SELECT fisc_label, event_int, agg_time,
           LAG(agg_time) OVER (PARTITION BY fisc_label ORDER BY event_int) AS prev_agg_time
    FROM fisc_event_time_agg
)
UPDATE fisc_event_time_agg
SET error_message = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.event_int = fisc_event_time_agg.event_int
    AND EventTimeOrdered.fisc_label = fisc_event_time_agg.fisc_label
    AND EventTimeOrdered.agg_time = fisc_event_time_agg.agg_time
;
"""


CREATE_FISC_OTE1_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
  fisc_label TEXT
, owner_name TEXT
, event_int INTEGER
, deal_time INTEGER
, error_message TEXT
)
;
"""
INSERT_FISC_OTE1_AGG_FROM_VOICE_SQLSTR = """
INSERT INTO fisc_ote1_agg (fisc_label, owner_name, event_int, deal_time)
SELECT fisc_label, owner_name, event_int, deal_time
FROM (
    SELECT 
      fisc_label_inx fisc_label
    , owner_name_inx owner_name
    , event_int
    , deal_time
    FROM fisc_dealunit_v_raw
    GROUP BY fisc_label_inx, owner_name_inx, event_int, deal_time
)
ORDER BY fisc_label, owner_name, event_int, deal_time
;
"""
