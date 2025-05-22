from src.a00_data_toolbox.db_toolbox import (
    create_update_inconsistency_error_query,
    create_table2table_agg_insert_query,
)
from src.a16_pidgin_logic.pidgin_config import find_set_otx_inx_args
from src.a17_idea_logic.idea_db_tool import (
    get_default_sorted_list,
    create_idea_sorted_table,
)
from src.a17_idea_logic.idea_config import (
    get_quick_ideas_column_ref,
    get_idea_sqlite_types,
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


CREATE_PIDTITL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDTITL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_agg (event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT)"""
CREATE_PIDNAME_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDNAME_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_agg (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT)"""
CREATE_PIDWAYY_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDWAYY_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_agg (event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT)"""
CREATE_PIDLABE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT, error_message TEXT)"""
CREATE_PIDLABE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_agg (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_term TEXT)"""

CREATE_FISCASH_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_agg (fisc_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISCASH_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISDEAL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_agg (fisc_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISDEAL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISHOUR_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_agg (fisc_label TEXT, cumlative_minute INTEGER, hour_label TEXT)"""
CREATE_FISHOUR_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, cumlative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_FISMONT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_agg (fisc_label TEXT, cumlative_day INTEGER, month_label TEXT)"""
CREATE_FISMONT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, cumlative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_FISWEEK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_agg (fisc_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_FISWEEK_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_FISOFFI_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_agg (fisc_label TEXT, offi_time INTEGER)"""
CREATE_FISOFFI_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_agg (fisc_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""
CREATE_FISUNIT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""

CREATE_BUDMEMB_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"""
CREATE_BUDMEMB_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title TEXT, credit_vote REAL, debtit_vote REAL)"""
CREATE_BUDMEMB_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT, error_message TEXT)"""
CREATE_BUDMEMB_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, group_title_ERASE TEXT)"""
CREATE_BUDACCT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"""
CREATE_BUDACCT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"""
CREATE_BUDACCT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDACCT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, acct_name_ERASE TEXT)"""
CREATE_BUDAWAR_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_awardlink_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"""
CREATE_BUDAWAR_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_awardlink_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"""
CREATE_BUDAWAR_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_awardlink_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT, error_message TEXT)"""
CREATE_BUDAWAR_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_awardlink_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, awardee_title_ERASE TEXT)"""
CREATE_BUDFACT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_factunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL, error_message TEXT)"""
CREATE_BUDFACT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_factunit_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL)"""
CREATE_BUDFACT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_factunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT, error_message TEXT)"""
CREATE_BUDFACT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_factunit_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, fcontext_ERASE TEXT)"""
CREATE_BUDHEAL_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_healerlink_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT, error_message TEXT)"""
CREATE_BUDHEAL_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_healerlink_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name TEXT)"""
CREATE_BUDHEAL_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_healerlink_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDHEAL_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_healerlink_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, healer_name_ERASE TEXT)"""
CREATE_BUDPREM_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER, error_message TEXT)"""
CREATE_BUDPREM_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"""
CREATE_BUDPREM_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch_ERASE TEXT, error_message TEXT)"""
CREATE_BUDPREM_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_reason_premiseunit_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, pbranch_ERASE TEXT)"""
CREATE_BUDREAS_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rcontext_concept_active_requisite INTEGER, error_message TEXT)"""
CREATE_BUDREAS_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext TEXT, rcontext_concept_active_requisite INTEGER)"""
CREATE_BUDREAS_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT, error_message TEXT)"""
CREATE_BUDREAS_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_reasonunit_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, rcontext_ERASE TEXT)"""
CREATE_BUDLABOR_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_laborlink_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT, error_message TEXT)"""
CREATE_BUDLABOR_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_laborlink_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title TEXT)"""
CREATE_BUDLABOR_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_laborlink_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT, error_message TEXT)"""
CREATE_BUDLABOR_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_concept_laborlink_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, labor_title_ERASE TEXT)"""
CREATE_BUDCONC_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_conceptunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"""
CREATE_BUDCONC_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_conceptunit_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"""
CREATE_BUDCONC_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_conceptunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way_ERASE TEXT, error_message TEXT)"""
CREATE_BUDCONC_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_conceptunit_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, concept_way_ERASE TEXT)"""
CREATE_BUDUNIT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"""
CREATE_BUDUNIT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"""
CREATE_BUDUNIT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDUNIT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_del_agg (event_int INTEGER, face_name TEXT, fisc_label TEXT, owner_name_ERASE TEXT)"""


def get_pidgin_prime_create_table_sqlstrs() -> dict[str, str]:
    return {
        "pidgin_title_raw": CREATE_PIDTITL_RAW_SQLSTR,
        "pidgin_title_agg": CREATE_PIDTITL_AGG_SQLSTR,
        "pidgin_name_raw": CREATE_PIDNAME_RAW_SQLSTR,
        "pidgin_name_agg": CREATE_PIDNAME_AGG_SQLSTR,
        "pidgin_way_raw": CREATE_PIDWAYY_RAW_SQLSTR,
        "pidgin_way_agg": CREATE_PIDWAYY_AGG_SQLSTR,
        "pidgin_label_raw": CREATE_PIDLABE_RAW_SQLSTR,
        "pidgin_label_agg": CREATE_PIDLABE_AGG_SQLSTR,
    }


def get_fisc_prime_create_table_sqlstrs() -> dict[str, str]:
    return {
        "fisc_cashbook_agg": CREATE_FISCASH_AGG_SQLSTR,
        "fisc_cashbook_raw": CREATE_FISCASH_RAW_SQLSTR,
        "fisc_dealunit_agg": CREATE_FISDEAL_AGG_SQLSTR,
        "fisc_dealunit_raw": CREATE_FISDEAL_RAW_SQLSTR,
        "fisc_timeline_hour_agg": CREATE_FISHOUR_AGG_SQLSTR,
        "fisc_timeline_hour_raw": CREATE_FISHOUR_RAW_SQLSTR,
        "fisc_timeline_month_agg": CREATE_FISMONT_AGG_SQLSTR,
        "fisc_timeline_month_raw": CREATE_FISMONT_RAW_SQLSTR,
        "fisc_timeline_weekday_agg": CREATE_FISWEEK_AGG_SQLSTR,
        "fisc_timeline_weekday_raw": CREATE_FISWEEK_RAW_SQLSTR,
        "fisc_timeoffi_agg": CREATE_FISOFFI_AGG_SQLSTR,
        "fisc_timeoffi_raw": CREATE_FISOFFI_RAW_SQLSTR,
        "fiscunit_agg": CREATE_FISUNIT_AGG_SQLSTR,
        "fiscunit_raw": CREATE_FISUNIT_RAW_SQLSTR,
    }


def get_bud_prime_create_table_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership_put_agg": CREATE_BUDMEMB_PUT_AGG_SQLSTR,
        "bud_acct_membership_put_raw": CREATE_BUDMEMB_PUT_RAW_SQLSTR,
        "bud_acct_membership_del_agg": CREATE_BUDMEMB_DEL_AGG_SQLSTR,
        "bud_acct_membership_del_raw": CREATE_BUDMEMB_DEL_RAW_SQLSTR,
        "bud_acctunit_put_agg": CREATE_BUDACCT_PUT_AGG_SQLSTR,
        "bud_acctunit_put_raw": CREATE_BUDACCT_PUT_RAW_SQLSTR,
        "bud_acctunit_del_agg": CREATE_BUDACCT_DEL_AGG_SQLSTR,
        "bud_acctunit_del_raw": CREATE_BUDACCT_DEL_RAW_SQLSTR,
        "bud_concept_awardlink_put_agg": CREATE_BUDAWAR_PUT_AGG_SQLSTR,
        "bud_concept_awardlink_put_raw": CREATE_BUDAWAR_PUT_RAW_SQLSTR,
        "bud_concept_awardlink_del_agg": CREATE_BUDAWAR_DEL_AGG_SQLSTR,
        "bud_concept_awardlink_del_raw": CREATE_BUDAWAR_DEL_RAW_SQLSTR,
        "bud_concept_factunit_put_agg": CREATE_BUDFACT_PUT_AGG_SQLSTR,
        "bud_concept_factunit_put_raw": CREATE_BUDFACT_PUT_RAW_SQLSTR,
        "bud_concept_factunit_del_agg": CREATE_BUDFACT_DEL_AGG_SQLSTR,
        "bud_concept_factunit_del_raw": CREATE_BUDFACT_DEL_RAW_SQLSTR,
        "bud_concept_healerlink_put_agg": CREATE_BUDHEAL_PUT_AGG_SQLSTR,
        "bud_concept_healerlink_put_raw": CREATE_BUDHEAL_PUT_RAW_SQLSTR,
        "bud_concept_healerlink_del_agg": CREATE_BUDHEAL_DEL_AGG_SQLSTR,
        "bud_concept_healerlink_del_raw": CREATE_BUDHEAL_DEL_RAW_SQLSTR,
        "bud_concept_reason_premiseunit_put_agg": CREATE_BUDPREM_PUT_AGG_SQLSTR,
        "bud_concept_reason_premiseunit_put_raw": CREATE_BUDPREM_PUT_RAW_SQLSTR,
        "bud_concept_reason_premiseunit_del_agg": CREATE_BUDPREM_DEL_AGG_SQLSTR,
        "bud_concept_reason_premiseunit_del_raw": CREATE_BUDPREM_DEL_RAW_SQLSTR,
        "bud_concept_reasonunit_put_agg": CREATE_BUDREAS_PUT_AGG_SQLSTR,
        "bud_concept_reasonunit_put_raw": CREATE_BUDREAS_PUT_RAW_SQLSTR,
        "bud_concept_reasonunit_del_agg": CREATE_BUDREAS_DEL_AGG_SQLSTR,
        "bud_concept_reasonunit_del_raw": CREATE_BUDREAS_DEL_RAW_SQLSTR,
        "bud_concept_laborlink_put_agg": CREATE_BUDLABOR_PUT_AGG_SQLSTR,
        "bud_concept_laborlink_put_raw": CREATE_BUDLABOR_PUT_RAW_SQLSTR,
        "bud_concept_laborlink_del_agg": CREATE_BUDLABOR_DEL_AGG_SQLSTR,
        "bud_concept_laborlink_del_raw": CREATE_BUDLABOR_DEL_RAW_SQLSTR,
        "bud_conceptunit_put_agg": CREATE_BUDCONC_PUT_AGG_SQLSTR,
        "bud_conceptunit_put_raw": CREATE_BUDCONC_PUT_RAW_SQLSTR,
        "bud_conceptunit_del_agg": CREATE_BUDCONC_DEL_AGG_SQLSTR,
        "bud_conceptunit_del_raw": CREATE_BUDCONC_DEL_RAW_SQLSTR,
        "budunit_put_agg": CREATE_BUDUNIT_PUT_AGG_SQLSTR,
        "budunit_put_raw": CREATE_BUDUNIT_PUT_RAW_SQLSTR,
        "budunit_del_agg": CREATE_BUDUNIT_DEL_AGG_SQLSTR,
        "budunit_del_raw": CREATE_BUDUNIT_DEL_RAW_SQLSTR,
    }


def create_sound_and_voice_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_prime_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_pidgin_prime_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_pidgin_prime_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_fisc_prime_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_fisc_prime_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_bud_prime_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_bud_prime_create_table_sqlstrs().values():
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


def create_pidgin_face_otx_event_sqlstr(
    pidgin_type_abbv: str, table: str, column_prefix: str
) -> str:
    return f"""
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
"""


def create_pidname_face_otx_event_sqlstr(table: str, column_prefix: str) -> str:
    return create_pidgin_face_otx_event_sqlstr("name", table, column_prefix)


def create_pidtitl_face_otx_event_sqlstr(table: str, column_prefix: str) -> str:
    return create_pidgin_face_otx_event_sqlstr("title", table, column_prefix)


def create_pidlabe_face_otx_event_sqlstr(table: str, column_prefix: str) -> str:
    return create_pidgin_face_otx_event_sqlstr("label", table, column_prefix)


def create_pidwayy_face_otx_event_sqlstr(table: str, column_prefix: str) -> str:
    return create_pidgin_face_otx_event_sqlstr("way", table, column_prefix)


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


PIDTITL_INCONSISTENCY_SQLSTR = """SELECT otx_title
FROM pidgin_title_raw
GROUP BY otx_title
HAVING MIN(inx_title) != MAX(inx_title)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_term) != MAX(unknown_term)
"""
PIDNAME_INCONSISTENCY_SQLSTR = """SELECT otx_name
FROM pidgin_name_raw
GROUP BY otx_name
HAVING MIN(inx_name) != MAX(inx_name)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_term) != MAX(unknown_term)
"""
PIDWAYY_INCONSISTENCY_SQLSTR = """SELECT otx_way
FROM pidgin_way_raw
GROUP BY otx_way
HAVING MIN(inx_way) != MAX(inx_way)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_term) != MAX(unknown_term)
"""
PIDLABE_INCONSISTENCY_SQLSTR = """SELECT otx_label
FROM pidgin_label_raw
GROUP BY otx_label
HAVING MIN(inx_label) != MAX(inx_label)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_term) != MAX(unknown_term)
"""

FISCASH_INCONSISTENCY_SQLSTR = """SELECT fisc_label, owner_name, acct_name, tran_time
FROM fisc_cashbook_raw
GROUP BY fisc_label, owner_name, acct_name, tran_time
HAVING MIN(amount) != MAX(amount)
"""
FISDEAL_INCONSISTENCY_SQLSTR = """SELECT fisc_label, owner_name, deal_time
FROM fisc_dealunit_raw
GROUP BY fisc_label, owner_name, deal_time
HAVING MIN(quota) != MAX(quota)
    OR MIN(celldepth) != MAX(celldepth)
"""
FISHOUR_INCONSISTENCY_SQLSTR = """SELECT fisc_label, cumlative_minute
FROM fisc_timeline_hour_raw
GROUP BY fisc_label, cumlative_minute
HAVING MIN(hour_label) != MAX(hour_label)
"""
FISMONT_INCONSISTENCY_SQLSTR = """SELECT fisc_label, cumlative_day
FROM fisc_timeline_month_raw
GROUP BY fisc_label, cumlative_day
HAVING MIN(month_label) != MAX(month_label)
"""
FISWEEK_INCONSISTENCY_SQLSTR = """SELECT fisc_label, weekday_order
FROM fisc_timeline_weekday_raw
GROUP BY fisc_label, weekday_order
HAVING MIN(weekday_label) != MAX(weekday_label)
"""
FISOFFI_INCONSISTENCY_SQLSTR = """SELECT fisc_label, offi_time
FROM fisc_timeoffi_raw
GROUP BY fisc_label, offi_time
HAVING 1=2
"""
FISUNIT_INCONSISTENCY_SQLSTR = """SELECT fisc_label
FROM fiscunit_raw
GROUP BY fisc_label
HAVING MIN(timeline_label) != MAX(timeline_label)
    OR MIN(c400_number) != MAX(c400_number)
    OR MIN(yr1_jan1_offset) != MAX(yr1_jan1_offset)
    OR MIN(monthday_distortion) != MAX(monthday_distortion)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
    OR MIN(bridge) != MAX(bridge)
    OR MIN(job_listen_rotations) != MAX(job_listen_rotations)
"""

BUDMEMB_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, acct_name, group_title
FROM bud_acct_membership_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, acct_name, group_title
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
"""
BUDACCT_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, acct_name
FROM bud_acctunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, acct_name
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
"""
BUDAWAR_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title
FROM bud_concept_awardlink_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
"""
BUDFACT_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, concept_way, fcontext
FROM bud_concept_factunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, fcontext
HAVING MIN(fbranch) != MAX(fbranch)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
"""
BUDHEAL_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, concept_way, healer_name
FROM bud_concept_healerlink_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, healer_name
HAVING 1=2
"""
BUDPREM_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch
FROM bud_concept_reason_premiseunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch
HAVING MIN(pnigh) != MAX(pnigh)
    OR MIN(popen) != MAX(popen)
    OR MIN(pdivisor) != MAX(pdivisor)
"""
BUDREAS_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext
FROM bud_concept_reasonunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, rcontext
HAVING MIN(rcontext_concept_active_requisite) != MAX(rcontext_concept_active_requisite)
"""
BUDLABOR_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, concept_way, labor_title
FROM bud_concept_laborlink_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, labor_title
HAVING 1=2
"""
BUDCONC_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name, concept_way
FROM bud_conceptunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way
HAVING MIN(begin) != MAX(begin)
    OR MIN(close) != MAX(close)
    OR MIN(addin) != MAX(addin)
    OR MIN(numor) != MAX(numor)
    OR MIN(denom) != MAX(denom)
    OR MIN(morph) != MAX(morph)
    OR MIN(gogo_want) != MAX(gogo_want)
    OR MIN(stop_want) != MAX(stop_want)
    OR MIN(mass) != MAX(mass)
    OR MIN(pledge) != MAX(pledge)
    OR MIN(problem_bool) != MAX(problem_bool)
"""
BUDUNIT_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_label, owner_name
FROM budunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name
HAVING MIN(credor_respect) != MAX(credor_respect)
    OR MIN(debtor_respect) != MAX(debtor_respect)
    OR MIN(fund_pool) != MAX(fund_pool)
    OR MIN(max_tree_traverse) != MAX(max_tree_traverse)
    OR MIN(tally) != MAX(tally)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
"""


def get_pidgin_inconsistency_sqlstrs() -> dict[str, str]:
    return {
        "pidgin_title": PIDTITL_INCONSISTENCY_SQLSTR,
        "pidgin_name": PIDNAME_INCONSISTENCY_SQLSTR,
        "pidgin_way": PIDWAYY_INCONSISTENCY_SQLSTR,
        "pidgin_label": PIDLABE_INCONSISTENCY_SQLSTR,
    }


def get_fisc_inconsistency_sqlstrs() -> dict[str, str]:
    return {
        "fiscunit": FISUNIT_INCONSISTENCY_SQLSTR,
        "fisc_dealunit": FISDEAL_INCONSISTENCY_SQLSTR,
        "fisc_cashbook": FISCASH_INCONSISTENCY_SQLSTR,
        "fisc_timeline_hour": FISHOUR_INCONSISTENCY_SQLSTR,
        "fisc_timeline_month": FISMONT_INCONSISTENCY_SQLSTR,
        "fisc_timeline_weekday": FISWEEK_INCONSISTENCY_SQLSTR,
        "fisc_timeoffi": FISOFFI_INCONSISTENCY_SQLSTR,
    }


def get_bud_inconsistency_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership": BUDMEMB_INCONSISTENCY_SQLSTR,
        "bud_acctunit": BUDACCT_INCONSISTENCY_SQLSTR,
        "bud_concept_awardlink": BUDAWAR_INCONSISTENCY_SQLSTR,
        "bud_concept_factunit": BUDFACT_INCONSISTENCY_SQLSTR,
        "bud_concept_healerlink": BUDHEAL_INCONSISTENCY_SQLSTR,
        "bud_concept_reason_premiseunit": BUDPREM_INCONSISTENCY_SQLSTR,
        "bud_concept_reasonunit": BUDREAS_INCONSISTENCY_SQLSTR,
        "bud_concept_laborlink": BUDLABOR_INCONSISTENCY_SQLSTR,
        "bud_conceptunit": BUDCONC_INCONSISTENCY_SQLSTR,
        "budunit": BUDUNIT_INCONSISTENCY_SQLSTR,
    }


PIDTITL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT otx_title
FROM pidgin_title_raw
GROUP BY otx_title
HAVING MIN(inx_title) != MAX(inx_title)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_term) != MAX(unknown_term)
)
UPDATE pidgin_title_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.otx_title = pidgin_title_raw.otx_title
;
"""
PIDNAME_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT otx_name
FROM pidgin_name_raw
GROUP BY otx_name
HAVING MIN(inx_name) != MAX(inx_name)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_term) != MAX(unknown_term)
)
UPDATE pidgin_name_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.otx_name = pidgin_name_raw.otx_name
;
"""
PIDWAYY_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT otx_way
FROM pidgin_way_raw
GROUP BY otx_way
HAVING MIN(inx_way) != MAX(inx_way)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_term) != MAX(unknown_term)
)
UPDATE pidgin_way_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.otx_way = pidgin_way_raw.otx_way
;
"""
PIDLABE_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT otx_label
FROM pidgin_label_raw
GROUP BY otx_label
HAVING MIN(inx_label) != MAX(inx_label)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_term) != MAX(unknown_term)
)
UPDATE pidgin_label_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.otx_label = pidgin_label_raw.otx_label
;
"""

FISCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_label, owner_name, acct_name, tran_time
FROM fisc_cashbook_raw
GROUP BY fisc_label, owner_name, acct_name, tran_time
HAVING MIN(amount) != MAX(amount)
)
UPDATE fisc_cashbook_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_label = fisc_cashbook_raw.fisc_label
    AND inconsistency_rows.owner_name = fisc_cashbook_raw.owner_name
    AND inconsistency_rows.acct_name = fisc_cashbook_raw.acct_name
    AND inconsistency_rows.tran_time = fisc_cashbook_raw.tran_time
;
"""
FISDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_label, owner_name, deal_time
FROM fisc_dealunit_raw
GROUP BY fisc_label, owner_name, deal_time
HAVING MIN(quota) != MAX(quota)
    OR MIN(celldepth) != MAX(celldepth)
)
UPDATE fisc_dealunit_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_label = fisc_dealunit_raw.fisc_label
    AND inconsistency_rows.owner_name = fisc_dealunit_raw.owner_name
    AND inconsistency_rows.deal_time = fisc_dealunit_raw.deal_time
;
"""
FISHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_label, cumlative_minute
FROM fisc_timeline_hour_raw
GROUP BY fisc_label, cumlative_minute
HAVING MIN(hour_label) != MAX(hour_label)
)
UPDATE fisc_timeline_hour_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_label = fisc_timeline_hour_raw.fisc_label
    AND inconsistency_rows.cumlative_minute = fisc_timeline_hour_raw.cumlative_minute
;
"""
FISMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_label, cumlative_day
FROM fisc_timeline_month_raw
GROUP BY fisc_label, cumlative_day
HAVING MIN(month_label) != MAX(month_label)
)
UPDATE fisc_timeline_month_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_label = fisc_timeline_month_raw.fisc_label
    AND inconsistency_rows.cumlative_day = fisc_timeline_month_raw.cumlative_day
;
"""
FISWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_label, weekday_order
FROM fisc_timeline_weekday_raw
GROUP BY fisc_label, weekday_order
HAVING MIN(weekday_label) != MAX(weekday_label)
)
UPDATE fisc_timeline_weekday_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_label = fisc_timeline_weekday_raw.fisc_label
    AND inconsistency_rows.weekday_order = fisc_timeline_weekday_raw.weekday_order
;
"""
FISOFFI_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_label, offi_time
FROM fisc_timeoffi_raw
GROUP BY fisc_label, offi_time
HAVING 1=2
)
UPDATE fisc_timeoffi_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_label = fisc_timeoffi_raw.fisc_label
    AND inconsistency_rows.offi_time = fisc_timeoffi_raw.offi_time
;
"""
FISUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_label
FROM fiscunit_raw
GROUP BY fisc_label
HAVING MIN(timeline_label) != MAX(timeline_label)
    OR MIN(c400_number) != MAX(c400_number)
    OR MIN(yr1_jan1_offset) != MAX(yr1_jan1_offset)
    OR MIN(monthday_distortion) != MAX(monthday_distortion)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
    OR MIN(bridge) != MAX(bridge)
    OR MIN(job_listen_rotations) != MAX(job_listen_rotations)
)
UPDATE fiscunit_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_label = fiscunit_raw.fisc_label
;
"""

BUDMEMB_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, acct_name, group_title
FROM bud_acct_membership_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, acct_name, group_title
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
)
UPDATE bud_acct_membership_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_acct_membership_put_raw.event_int
    AND inconsistency_rows.face_name = bud_acct_membership_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_acct_membership_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_acct_membership_put_raw.owner_name
    AND inconsistency_rows.acct_name = bud_acct_membership_put_raw.acct_name
    AND inconsistency_rows.group_title = bud_acct_membership_put_raw.group_title
;
"""
BUDACCT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, acct_name
FROM bud_acctunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, acct_name
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
)
UPDATE bud_acctunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_acctunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_acctunit_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_acctunit_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_acctunit_put_raw.owner_name
    AND inconsistency_rows.acct_name = bud_acctunit_put_raw.acct_name
;
"""
BUDAWAR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title
FROM bud_concept_awardlink_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE bud_concept_awardlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_concept_awardlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_concept_awardlink_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_concept_awardlink_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_concept_awardlink_put_raw.owner_name
    AND inconsistency_rows.concept_way = bud_concept_awardlink_put_raw.concept_way
    AND inconsistency_rows.awardee_title = bud_concept_awardlink_put_raw.awardee_title
;
"""
BUDFACT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, concept_way, fcontext
FROM bud_concept_factunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, fcontext
HAVING MIN(fbranch) != MAX(fbranch)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
)
UPDATE bud_concept_factunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_concept_factunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_concept_factunit_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_concept_factunit_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_concept_factunit_put_raw.owner_name
    AND inconsistency_rows.concept_way = bud_concept_factunit_put_raw.concept_way
    AND inconsistency_rows.fcontext = bud_concept_factunit_put_raw.fcontext
;
"""
BUDHEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, concept_way, healer_name
FROM bud_concept_healerlink_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, healer_name
HAVING 1=2
)
UPDATE bud_concept_healerlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_concept_healerlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_concept_healerlink_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_concept_healerlink_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_concept_healerlink_put_raw.owner_name
    AND inconsistency_rows.concept_way = bud_concept_healerlink_put_raw.concept_way
    AND inconsistency_rows.healer_name = bud_concept_healerlink_put_raw.healer_name
;
"""
BUDPREM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch
FROM bud_concept_reason_premiseunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch
HAVING MIN(pnigh) != MAX(pnigh)
    OR MIN(popen) != MAX(popen)
    OR MIN(pdivisor) != MAX(pdivisor)
)
UPDATE bud_concept_reason_premiseunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_concept_reason_premiseunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_concept_reason_premiseunit_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_concept_reason_premiseunit_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_concept_reason_premiseunit_put_raw.owner_name
    AND inconsistency_rows.concept_way = bud_concept_reason_premiseunit_put_raw.concept_way
    AND inconsistency_rows.rcontext = bud_concept_reason_premiseunit_put_raw.rcontext
    AND inconsistency_rows.pbranch = bud_concept_reason_premiseunit_put_raw.pbranch
;
"""
BUDREAS_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext
FROM bud_concept_reasonunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, rcontext
HAVING MIN(rcontext_concept_active_requisite) != MAX(rcontext_concept_active_requisite)
)
UPDATE bud_concept_reasonunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_concept_reasonunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_concept_reasonunit_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_concept_reasonunit_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_concept_reasonunit_put_raw.owner_name
    AND inconsistency_rows.concept_way = bud_concept_reasonunit_put_raw.concept_way
    AND inconsistency_rows.rcontext = bud_concept_reasonunit_put_raw.rcontext
;
"""
BUDLABOR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, concept_way, labor_title
FROM bud_concept_laborlink_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, labor_title
HAVING 1=2
)
UPDATE bud_concept_laborlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_concept_laborlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_concept_laborlink_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_concept_laborlink_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_concept_laborlink_put_raw.owner_name
    AND inconsistency_rows.concept_way = bud_concept_laborlink_put_raw.concept_way
    AND inconsistency_rows.labor_title = bud_concept_laborlink_put_raw.labor_title
;
"""
BUDCONC_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name, concept_way
FROM bud_conceptunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way
HAVING MIN(begin) != MAX(begin)
    OR MIN(close) != MAX(close)
    OR MIN(addin) != MAX(addin)
    OR MIN(numor) != MAX(numor)
    OR MIN(denom) != MAX(denom)
    OR MIN(morph) != MAX(morph)
    OR MIN(gogo_want) != MAX(gogo_want)
    OR MIN(stop_want) != MAX(stop_want)
    OR MIN(mass) != MAX(mass)
    OR MIN(pledge) != MAX(pledge)
    OR MIN(problem_bool) != MAX(problem_bool)
)
UPDATE bud_conceptunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_conceptunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_conceptunit_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_conceptunit_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_conceptunit_put_raw.owner_name
    AND inconsistency_rows.concept_way = bud_conceptunit_put_raw.concept_way
;
"""
BUDUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_label, owner_name
FROM budunit_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name
HAVING MIN(credor_respect) != MAX(credor_respect)
    OR MIN(debtor_respect) != MAX(debtor_respect)
    OR MIN(fund_pool) != MAX(fund_pool)
    OR MIN(max_tree_traverse) != MAX(max_tree_traverse)
    OR MIN(tally) != MAX(tally)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
)
UPDATE budunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = budunit_put_raw.event_int
    AND inconsistency_rows.face_name = budunit_put_raw.face_name
    AND inconsistency_rows.fisc_label = budunit_put_raw.fisc_label
    AND inconsistency_rows.owner_name = budunit_put_raw.owner_name
;
"""
BUDMEMB_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_acct_membership_del_agg (event_int, face_name, fisc_label, owner_name, acct_name, group_title_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, acct_name, group_title_ERASE
FROM bud_acct_membership_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, acct_name, group_title_ERASE
;
"""
BUDACCT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_acctunit_del_agg (event_int, face_name, fisc_label, owner_name, acct_name_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, acct_name_ERASE
FROM bud_acctunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, acct_name_ERASE
;
"""
BUDAWAR_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_awardlink_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, awardee_title_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title_ERASE
FROM bud_concept_awardlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, awardee_title_ERASE
;
"""
BUDFACT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_factunit_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, fcontext_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, fcontext_ERASE
FROM bud_concept_factunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, fcontext_ERASE
;
"""
BUDHEAL_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_healerlink_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, healer_name_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, healer_name_ERASE
FROM bud_concept_healerlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, healer_name_ERASE
;
"""
BUDPREM_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_reason_premiseunit_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch_ERASE
FROM bud_concept_reason_premiseunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch_ERASE
;
"""
BUDREAS_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_reasonunit_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, rcontext_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext_ERASE
FROM bud_concept_reasonunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, rcontext_ERASE
;
"""
BUDLABOR_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_laborlink_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, labor_title_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, labor_title_ERASE
FROM bud_concept_laborlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, labor_title_ERASE
;
"""
BUDCONC_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_conceptunit_del_agg (event_int, face_name, fisc_label, owner_name, concept_way_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, concept_way_ERASE
FROM bud_conceptunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way_ERASE
;
"""
BUDUNIT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO budunit_del_agg (event_int, face_name, fisc_label, owner_name_ERASE)
SELECT event_int, face_name, fisc_label, owner_name_ERASE
FROM budunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name_ERASE
;
"""


def get_pidgin_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    return {
        "pidgin_title": PIDTITL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "pidgin_name": PIDNAME_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "pidgin_way": PIDWAYY_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "pidgin_label": PIDLABE_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
    }


def get_fisc_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    return {
        "fiscunit": FISUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_dealunit": FISDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_cashbook": FISCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_timeline_hour": FISHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_timeline_month": FISMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_timeline_weekday": FISWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_timeoffi": FISOFFI_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
    }


def get_bud_put_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership": BUDMEMB_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_acctunit": BUDACCT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_concept_awardlink": BUDAWAR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_concept_factunit": BUDFACT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_concept_healerlink": BUDHEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_concept_reason_premiseunit": BUDPREM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_concept_reasonunit": BUDREAS_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_concept_laborlink": BUDLABOR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_conceptunit": BUDCONC_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "budunit": BUDUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
    }


def get_sound_pidgin_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    x_dict = {}
    for (
        dimen,
        sqlstr,
    ) in get_pidgin_update_inconsist_error_message_sqlstrs().items():
        old_raw_tablename = f"{dimen}_raw"
        new_raw_tablename = f"{dimen}_s_raw"
        x_dict[dimen] = sqlstr.replace(old_raw_tablename, new_raw_tablename)
    return x_dict


def get_sound_fisc_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    x_dict = {}
    for (
        dimen,
        sqlstr,
    ) in get_pidgin_update_inconsist_error_message_sqlstrs().items():
        old_raw_tablename = f"{dimen}_raw"
        new_raw_tablename = f"{dimen}_s_raw"
        x_dict[dimen] = sqlstr.replace(old_raw_tablename, new_raw_tablename)
    return x_dict


PIDTITL_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_title_agg (otx_title, inx_title, otx_bridge, inx_bridge, unknown_term)
SELECT otx_title, MAX(inx_title), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_term)
FROM pidgin_title_raw
WHERE error_message IS NULL
GROUP BY otx_title
;
"""
PIDNAME_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_name_agg (otx_name, inx_name, otx_bridge, inx_bridge, unknown_term)
SELECT otx_name, MAX(inx_name), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_term)
FROM pidgin_name_raw
WHERE error_message IS NULL
GROUP BY otx_name
;
"""
PIDWAYY_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_way_agg (otx_way, inx_way, otx_bridge, inx_bridge, unknown_term)
SELECT otx_way, MAX(inx_way), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_term)
FROM pidgin_way_raw
WHERE error_message IS NULL
GROUP BY otx_way
;
"""
PIDLABE_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_label_agg (otx_label, inx_label, otx_bridge, inx_bridge, unknown_term)
SELECT otx_label, MAX(inx_label), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_term)
FROM pidgin_label_raw
WHERE error_message IS NULL
GROUP BY otx_label
;
"""

FISCASH_AGG_INSERT_SQLSTR = """INSERT INTO fisc_cashbook_agg (fisc_label, owner_name, acct_name, tran_time, amount)
SELECT fisc_label, owner_name, acct_name, tran_time, MAX(amount)
FROM fisc_cashbook_raw
WHERE error_message IS NULL
GROUP BY fisc_label, owner_name, acct_name, tran_time
;
"""
FISDEAL_AGG_INSERT_SQLSTR = """INSERT INTO fisc_dealunit_agg (fisc_label, owner_name, deal_time, quota, celldepth)
SELECT fisc_label, owner_name, deal_time, MAX(quota), MAX(celldepth)
FROM fisc_dealunit_raw
WHERE error_message IS NULL
GROUP BY fisc_label, owner_name, deal_time
;
"""
FISHOUR_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_hour_agg (fisc_label, cumlative_minute, hour_label)
SELECT fisc_label, cumlative_minute, MAX(hour_label)
FROM fisc_timeline_hour_raw
WHERE error_message IS NULL
GROUP BY fisc_label, cumlative_minute
;
"""
FISMONT_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_month_agg (fisc_label, cumlative_day, month_label)
SELECT fisc_label, cumlative_day, MAX(month_label)
FROM fisc_timeline_month_raw
WHERE error_message IS NULL
GROUP BY fisc_label, cumlative_day
;
"""
FISWEEK_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_weekday_agg (fisc_label, weekday_order, weekday_label)
SELECT fisc_label, weekday_order, MAX(weekday_label)
FROM fisc_timeline_weekday_raw
WHERE error_message IS NULL
GROUP BY fisc_label, weekday_order
;
"""
FISOFFI_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeoffi_agg (fisc_label, offi_time)
SELECT fisc_label, offi_time
FROM fisc_timeoffi_raw
WHERE error_message IS NULL
GROUP BY fisc_label, offi_time
;
"""
FISUNIT_AGG_INSERT_SQLSTR = """INSERT INTO fiscunit_agg (fisc_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations)
SELECT fisc_label, MAX(timeline_label), MAX(c400_number), MAX(yr1_jan1_offset), MAX(monthday_distortion), MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(bridge), MAX(job_listen_rotations)
FROM fiscunit_raw
WHERE error_message IS NULL
GROUP BY fisc_label
;
"""

BUDMEMB_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_acct_membership_put_agg (event_int, face_name, fisc_label, owner_name, acct_name, group_title, credit_vote, debtit_vote)
SELECT event_int, face_name, fisc_label, owner_name, acct_name, group_title, MAX(credit_vote), MAX(debtit_vote)
FROM bud_acct_membership_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, acct_name, group_title
;
"""
BUDACCT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_acctunit_put_agg (event_int, face_name, fisc_label, owner_name, acct_name, credit_belief, debtit_belief)
SELECT event_int, face_name, fisc_label, owner_name, acct_name, MAX(credit_belief), MAX(debtit_belief)
FROM bud_acctunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, acct_name
;
"""
BUDAWAR_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_awardlink_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, awardee_title, give_force, take_force)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title, MAX(give_force), MAX(take_force)
FROM bud_concept_awardlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, awardee_title
;
"""
BUDFACT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_factunit_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, fcontext, fbranch, fopen, fnigh)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, fcontext, MAX(fbranch), MAX(fopen), MAX(fnigh)
FROM bud_concept_factunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, fcontext
;
"""
BUDHEAL_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_healerlink_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, healer_name)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, healer_name
FROM bud_concept_healerlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, healer_name
;
"""
BUDPREM_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_reason_premiseunit_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch, pnigh, popen, pdivisor)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch, MAX(pnigh), MAX(popen), MAX(pdivisor)
FROM bud_concept_reason_premiseunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, rcontext, pbranch
;
"""
BUDREAS_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_reasonunit_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, rcontext, rcontext_concept_active_requisite)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, rcontext, MAX(rcontext_concept_active_requisite)
FROM bud_concept_reasonunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, rcontext
;
"""
BUDLABOR_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_concept_laborlink_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, labor_title)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, labor_title
FROM bud_concept_laborlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, labor_title
;
"""
BUDCONC_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_conceptunit_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, MAX(begin), MAX(close), MAX(addin), MAX(numor), MAX(denom), MAX(morph), MAX(gogo_want), MAX(stop_want), MAX(mass), MAX(pledge), MAX(problem_bool)
FROM bud_conceptunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way
;
"""
BUDUNIT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO budunit_put_agg (event_int, face_name, fisc_label, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit)
SELECT event_int, face_name, fisc_label, owner_name, MAX(credor_respect), MAX(debtor_respect), MAX(fund_pool), MAX(max_tree_traverse), MAX(tally), MAX(fund_coin), MAX(penny), MAX(respect_bit)
FROM budunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name
;
"""


def get_pidgin_insert_agg_from_raw_sqlstrs() -> dict[str, str]:
    return {
        "pidgin_title": PIDTITL_AGG_INSERT_SQLSTR,
        "pidgin_name": PIDNAME_AGG_INSERT_SQLSTR,
        "pidgin_way": PIDWAYY_AGG_INSERT_SQLSTR,
        "pidgin_label": PIDLABE_AGG_INSERT_SQLSTR,
    }


def get_fisc_insert_agg_from_raw_sqlstrs() -> dict[str, str]:
    return {
        "fisc_cashbook": FISCASH_AGG_INSERT_SQLSTR,
        "fisc_dealunit": FISDEAL_AGG_INSERT_SQLSTR,
        "fisc_timeline_hour": FISHOUR_AGG_INSERT_SQLSTR,
        "fisc_timeline_month": FISMONT_AGG_INSERT_SQLSTR,
        "fisc_timeline_weekday": FISWEEK_AGG_INSERT_SQLSTR,
        "fisc_timeoffi": FISOFFI_AGG_INSERT_SQLSTR,
        "fiscunit": FISUNIT_AGG_INSERT_SQLSTR,
    }


def get_bud_insert_put_agg_from_raw_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership": BUDMEMB_PUT_AGG_INSERT_SQLSTR,
        "bud_acctunit": BUDACCT_PUT_AGG_INSERT_SQLSTR,
        "bud_concept_awardlink": BUDAWAR_PUT_AGG_INSERT_SQLSTR,
        "bud_concept_factunit": BUDFACT_PUT_AGG_INSERT_SQLSTR,
        "bud_concept_healerlink": BUDHEAL_PUT_AGG_INSERT_SQLSTR,
        "bud_concept_reason_premiseunit": BUDPREM_PUT_AGG_INSERT_SQLSTR,
        "bud_concept_reasonunit": BUDREAS_PUT_AGG_INSERT_SQLSTR,
        "bud_concept_laborlink": BUDLABOR_PUT_AGG_INSERT_SQLSTR,
        "bud_conceptunit": BUDCONC_PUT_AGG_INSERT_SQLSTR,
        "budunit": BUDUNIT_PUT_AGG_INSERT_SQLSTR,
    }


def get_bud_insert_del_agg_from_raw_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership": BUDMEMB_DEL_AGG_INSERT_SQLSTR,
        "bud_acctunit": BUDACCT_DEL_AGG_INSERT_SQLSTR,
        "bud_concept_awardlink": BUDAWAR_DEL_AGG_INSERT_SQLSTR,
        "bud_concept_factunit": BUDFACT_DEL_AGG_INSERT_SQLSTR,
        "bud_concept_healerlink": BUDHEAL_DEL_AGG_INSERT_SQLSTR,
        "bud_concept_reason_premiseunit": BUDPREM_DEL_AGG_INSERT_SQLSTR,
        "bud_concept_reasonunit": BUDREAS_DEL_AGG_INSERT_SQLSTR,
        "bud_concept_laborlink": BUDLABOR_DEL_AGG_INSERT_SQLSTR,
        "bud_conceptunit": BUDCONC_DEL_AGG_INSERT_SQLSTR,
        "budunit": BUDUNIT_DEL_AGG_INSERT_SQLSTR,
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

FISCASH_FU1_SELECT_SQLSTR = "SELECT fisc_label, owner_name, acct_name, tran_time, amount FROM fisc_cashbook_agg WHERE fisc_label = "
FISDEAL_FU1_SELECT_SQLSTR = "SELECT fisc_label, owner_name, deal_time, quota, celldepth FROM fisc_dealunit_agg WHERE fisc_label = "
FISHOUR_FU1_SELECT_SQLSTR = "SELECT fisc_label, cumlative_minute, hour_label FROM fisc_timeline_hour_agg WHERE fisc_label = "
FISMONT_FU1_SELECT_SQLSTR = "SELECT fisc_label, cumlative_day, month_label FROM fisc_timeline_month_agg WHERE fisc_label = "
FISWEEK_FU1_SELECT_SQLSTR = "SELECT fisc_label, weekday_order, weekday_label FROM fisc_timeline_weekday_agg WHERE fisc_label = "
FISOFFI_FU1_SELECT_SQLSTR = (
    "SELECT fisc_label, offi_time FROM fisc_timeoffi_agg WHERE fisc_label = "
)
FISUNIT_FU1_SELECT_SQLSTR = "SELECT fisc_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations FROM fiscunit_agg WHERE fisc_label = "


def get_fisc_fu1_select_sqlstrs(fisc_label: str) -> dict[str, str]:
    return {
        "fiscunit": f"{FISUNIT_FU1_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_dealunit": f"{FISDEAL_FU1_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_cashbook": f"{FISCASH_FU1_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_timeline_hour": f"{FISHOUR_FU1_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_timeline_month": f"{FISMONT_FU1_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_timeline_weekday": f"{FISWEEK_FU1_SELECT_SQLSTR}'{fisc_label}'",
        "fisc_timeoffi": f"{FISOFFI_FU1_SELECT_SQLSTR}'{fisc_label}'",
    }
