from src.a00_data_toolbox.db_toolbox import (
    get_table_columns,
    create_update_inconsistency_error_query,
    create_table2table_agg_insert_query,
)
from src.a16_pidgin_logic.pidgin_config import find_set_otx_inx_args
from src.a17_creed_logic.creed_db_tool import (
    get_default_sorted_list,
    create_creed_sorted_table,
)
from src.a17_creed_logic.creed_config import (
    get_quick_creeds_column_ref,
    get_creed_sqlite_types,
    get_creed_config_dict,
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
    "BUDIDEA",
    "BUDUNIT",
    "PIDLABE",
    "PIDNAME",
    "PIDWAYY",
    "PIDTAGG",
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
        "bud_idea_awardlink": "BUDAWAR",
        "bud_idea_factunit": "BUDFACT",
        "bud_idea_healerlink": "BUDHEAL",
        "bud_idea_reason_premiseunit": "BUDPREM",
        "bud_idea_reasonunit": "BUDREAS",
        "bud_idea_laborlink": "BUDLABO",
        "bud_ideaunit": "BUDIDEA",
        "budunit": "BUDUNIT",
        "pidgin_label": "PIDLABE",
        "pidgin_name": "PIDNAME",
        "pidgin_way": "PIDWAYY",
        "pidgin_tag": "PIDTAGG",
        "pidgin_core": "PIDCORE",
    }.get(dimen)


def create_prime_tablename(
    creed_dimen_or_abbv7: str, sound: str, stage: str, put_del: str = None
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
        "BUDAWAR": "bud_idea_awardlink",
        "BUDFACT": "bud_idea_factunit",
        "BUDHEAL": "bud_idea_healerlink",
        "BUDPREM": "bud_idea_reason_premiseunit",
        "BUDREAS": "bud_idea_reasonunit",
        "BUDLABO": "bud_idea_laborlink",
        "BUDIDEA": "bud_ideaunit",
        "BUDUNIT": "budunit",
        "PIDLABE": "pidgin_label",
        "PIDNAME": "pidgin_name",
        "PIDWAYY": "pidgin_way",
        "PIDTAGG": "pidgin_tag",
        "PIDCORE": "pidgin_core",
    }
    tablename = creed_dimen_or_abbv7
    if abbv_references.get(creed_dimen_or_abbv7.upper()):
        tablename = abbv_references.get(creed_dimen_or_abbv7.upper())
    if sound in {"s", "v"}:
        tablename = f"{tablename}_{sound}"

    return f"{tablename}_{put_del}_{stage}" if put_del else f"{tablename}_{stage}"


CREATE_PIDLABE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_agg (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_vld (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT)"""
CREATE_PIDNAME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_agg (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_vld (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT)"""
CREATE_PIDWAYY_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDWAYY_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_agg (event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDWAYY_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_s_vld (event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT)"""
CREATE_PIDTAGG_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDTAGG_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_s_agg (event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDTAGG_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_s_vld (event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT)"""

CREATE_PIDCORE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_raw (source_dimen TEXT, face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDCORE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_agg (face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""
CREATE_PIDCORE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_vld (face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""

CREATE_FISCASH_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISCASH_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISCASH_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISCASH_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_v_agg (fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISDEAL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISDEAL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISDEAL_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISDEAL_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_v_agg (fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISHOUR_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT, error_message TEXT)"""
CREATE_FISHOUR_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT)"""
CREATE_FISHOUR_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, cumlative_minute INTEGER, hour_tag_otx TEXT, hour_tag_inx TEXT, error_message TEXT)"""
CREATE_FISHOUR_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_v_agg (fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT)"""
CREATE_FISMONT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT, error_message TEXT)"""
CREATE_FISMONT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT)"""
CREATE_FISMONT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, cumlative_day INTEGER, month_tag_otx TEXT, month_tag_inx TEXT, error_message TEXT)"""
CREATE_FISMONT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_v_agg (fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT)"""
CREATE_FISWEEK_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT, error_message TEXT)"""
CREATE_FISWEEK_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT)"""
CREATE_FISWEEK_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, weekday_order INTEGER, weekday_tag_otx TEXT, weekday_tag_inx TEXT, error_message TEXT)"""
CREATE_FISWEEK_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_v_agg (fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT)"""
CREATE_FISOFFI_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISOFFI_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, offi_time INTEGER)"""
CREATE_FISOFFI_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISOFFI_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_v_agg (fisc_tag TEXT, offi_time INTEGER)"""
CREATE_FISUNIT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_s_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_FISUNIT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""
CREATE_FISUNIT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, timeline_tag_otx TEXT, timeline_tag_inx TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_FISUNIT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_v_agg (fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""

CREATE_BUDMEMB_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"
CREATE_BUDMEMB_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"
CREATE_BUDMEMB_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"
CREATE_BUDMEMB_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, group_label_otx TEXT, group_label_inx TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, group_label_ERASE_otx TEXT, group_label_ERASE_inx TEXT)"
CREATE_BUDMEMB_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"
CREATE_BUDACCT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"
CREATE_BUDACCT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDACCT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDACCT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_otx TEXT, acct_name_inx TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, acct_name_ERASE_otx TEXT, acct_name_ERASE_inx TEXT)"
CREATE_BUDACCT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDAWAR_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_awardlink_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_BUDAWAR_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_awardlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_awardlink_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label_ERASE TEXT)"
CREATE_BUDAWAR_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_awardlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label_ERASE TEXT)"
CREATE_BUDAWAR_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_awardlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, awardee_label_otx TEXT, awardee_label_inx TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_awardlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_awardlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, awardee_label_ERASE_otx TEXT, awardee_label_ERASE_inx TEXT)"
CREATE_BUDAWAR_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_awardlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label_ERASE TEXT)"
CREATE_BUDFACT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_factunit_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL, error_message TEXT)"
CREATE_BUDFACT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_factunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_factunit_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext_ERASE TEXT)"
CREATE_BUDFACT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_factunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext_ERASE TEXT)"
CREATE_BUDFACT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_factunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, fcontext_otx TEXT, fcontext_inx TEXT, fbranch_otx TEXT, fbranch_inx TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_factunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_factunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, fcontext_ERASE_otx TEXT, fcontext_ERASE_inx TEXT)"
CREATE_BUDFACT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_factunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext_ERASE TEXT)"
CREATE_BUDHEAL_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_healerlink_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name TEXT, error_message TEXT)"
CREATE_BUDHEAL_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_healerlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name TEXT)"
CREATE_BUDHEAL_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_healerlink_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name_ERASE TEXT)"
CREATE_BUDHEAL_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_healerlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name_ERASE TEXT)"
CREATE_BUDHEAL_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_healerlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, healer_name_otx TEXT, healer_name_inx TEXT)"
CREATE_BUDHEAL_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_healerlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name TEXT)"
CREATE_BUDHEAL_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_healerlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, healer_name_ERASE_otx TEXT, healer_name_ERASE_inx TEXT)"
CREATE_BUDHEAL_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_healerlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name_ERASE TEXT)"
CREATE_BUDPREM_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER, error_message TEXT)"
CREATE_BUDPREM_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_BUDPREM_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch_ERASE TEXT)"
CREATE_BUDPREM_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch_ERASE TEXT)"
CREATE_BUDPREM_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, pbranch_otx TEXT, pbranch_inx TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_BUDPREM_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"
CREATE_BUDPREM_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, pbranch_ERASE_otx TEXT, pbranch_ERASE_inx TEXT)"
CREATE_BUDPREM_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch_ERASE TEXT)"
CREATE_BUDREAS_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, rcontext_idea_active_requisite INTEGER, error_message TEXT)"
CREATE_BUDREAS_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, rcontext_idea_active_requisite INTEGER)"
CREATE_BUDREAS_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext_ERASE TEXT)"
CREATE_BUDREAS_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext_ERASE TEXT)"
CREATE_BUDREAS_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, rcontext_otx TEXT, rcontext_inx TEXT, rcontext_idea_active_requisite INTEGER)"
CREATE_BUDREAS_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, rcontext_idea_active_requisite INTEGER)"
CREATE_BUDREAS_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, rcontext_ERASE_otx TEXT, rcontext_ERASE_inx TEXT)"
CREATE_BUDREAS_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext_ERASE TEXT)"
CREATE_BUDLABOR_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_laborlink_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label TEXT, error_message TEXT)"
CREATE_BUDLABOR_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_laborlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label TEXT)"
CREATE_BUDLABOR_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_laborlink_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label_ERASE TEXT)"
CREATE_BUDLABOR_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_laborlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label_ERASE TEXT)"
CREATE_BUDLABOR_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_laborlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, labor_label_otx TEXT, labor_label_inx TEXT)"
CREATE_BUDLABOR_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_laborlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label TEXT)"
CREATE_BUDLABOR_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_idea_laborlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, labor_label_ERASE_otx TEXT, labor_label_ERASE_inx TEXT)"
CREATE_BUDLABOR_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_idea_laborlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label_ERASE TEXT)"
CREATE_BUDIDEA_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_ideaunit_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_BUDIDEA_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_ideaunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDIDEA_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_ideaunit_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way_ERASE TEXT)"
CREATE_BUDIDEA_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_ideaunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way_ERASE TEXT)"
CREATE_BUDIDEA_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_ideaunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_otx TEXT, idea_way_inx TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDIDEA_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_ideaunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDIDEA_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_ideaunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, idea_way_ERASE_otx TEXT, idea_way_ERASE_inx TEXT)"
CREATE_BUDIDEA_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_ideaunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way_ERASE TEXT)"
CREATE_BUDUNIT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_s_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"
CREATE_BUDUNIT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_s_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"
CREATE_BUDUNIT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"
CREATE_BUDUNIT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_otx TEXT, owner_name_inx TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, fisc_tag_otx TEXT, fisc_tag_inx TEXT, owner_name_ERASE_otx TEXT, owner_name_ERASE_inx TEXT)"
CREATE_BUDUNIT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"


def get_prime_create_table_sqlstrs() -> dict[str:str]:
    return {
        "pidgin_label_s_raw": CREATE_PIDLABE_SOUND_RAW_SQLSTR,
        "pidgin_label_s_agg": CREATE_PIDLABE_SOUND_AGG_SQLSTR,
        "pidgin_label_s_vld": CREATE_PIDLABE_SOUND_VLD_SQLSTR,
        "pidgin_name_s_raw": CREATE_PIDNAME_SOUND_RAW_SQLSTR,
        "pidgin_name_s_agg": CREATE_PIDNAME_SOUND_AGG_SQLSTR,
        "pidgin_name_s_vld": CREATE_PIDNAME_SOUND_VLD_SQLSTR,
        "pidgin_way_s_raw": CREATE_PIDWAYY_SOUND_RAW_SQLSTR,
        "pidgin_way_s_agg": CREATE_PIDWAYY_SOUND_AGG_SQLSTR,
        "pidgin_way_s_vld": CREATE_PIDWAYY_SOUND_VLD_SQLSTR,
        "pidgin_tag_s_raw": CREATE_PIDTAGG_SOUND_RAW_SQLSTR,
        "pidgin_tag_s_agg": CREATE_PIDTAGG_SOUND_AGG_SQLSTR,
        "pidgin_tag_s_vld": CREATE_PIDTAGG_SOUND_VLD_SQLSTR,
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
        "bud_idea_awardlink_s_put_raw": CREATE_BUDAWAR_SOUND_PUT_RAW_STR,
        "bud_idea_awardlink_s_put_agg": CREATE_BUDAWAR_SOUND_PUT_AGG_STR,
        "bud_idea_awardlink_s_del_raw": CREATE_BUDAWAR_SOUND_DEL_RAW_STR,
        "bud_idea_awardlink_s_del_agg": CREATE_BUDAWAR_SOUND_DEL_AGG_STR,
        "bud_idea_awardlink_v_put_raw": CREATE_BUDAWAR_VOICE_PUT_RAW_STR,
        "bud_idea_awardlink_v_put_agg": CREATE_BUDAWAR_VOICE_PUT_AGG_STR,
        "bud_idea_awardlink_v_del_raw": CREATE_BUDAWAR_VOICE_DEL_RAW_STR,
        "bud_idea_awardlink_v_del_agg": CREATE_BUDAWAR_VOICE_DEL_AGG_STR,
        "bud_idea_factunit_s_put_raw": CREATE_BUDFACT_SOUND_PUT_RAW_STR,
        "bud_idea_factunit_s_put_agg": CREATE_BUDFACT_SOUND_PUT_AGG_STR,
        "bud_idea_factunit_s_del_raw": CREATE_BUDFACT_SOUND_DEL_RAW_STR,
        "bud_idea_factunit_s_del_agg": CREATE_BUDFACT_SOUND_DEL_AGG_STR,
        "bud_idea_factunit_v_put_raw": CREATE_BUDFACT_VOICE_PUT_RAW_STR,
        "bud_idea_factunit_v_put_agg": CREATE_BUDFACT_VOICE_PUT_AGG_STR,
        "bud_idea_factunit_v_del_raw": CREATE_BUDFACT_VOICE_DEL_RAW_STR,
        "bud_idea_factunit_v_del_agg": CREATE_BUDFACT_VOICE_DEL_AGG_STR,
        "bud_idea_healerlink_s_put_raw": CREATE_BUDHEAL_SOUND_PUT_RAW_STR,
        "bud_idea_healerlink_s_put_agg": CREATE_BUDHEAL_SOUND_PUT_AGG_STR,
        "bud_idea_healerlink_s_del_raw": CREATE_BUDHEAL_SOUND_DEL_RAW_STR,
        "bud_idea_healerlink_s_del_agg": CREATE_BUDHEAL_SOUND_DEL_AGG_STR,
        "bud_idea_healerlink_v_put_raw": CREATE_BUDHEAL_VOICE_PUT_RAW_STR,
        "bud_idea_healerlink_v_put_agg": CREATE_BUDHEAL_VOICE_PUT_AGG_STR,
        "bud_idea_healerlink_v_del_raw": CREATE_BUDHEAL_VOICE_DEL_RAW_STR,
        "bud_idea_healerlink_v_del_agg": CREATE_BUDHEAL_VOICE_DEL_AGG_STR,
        "bud_idea_reason_premiseunit_s_put_raw": CREATE_BUDPREM_SOUND_PUT_RAW_STR,
        "bud_idea_reason_premiseunit_s_put_agg": CREATE_BUDPREM_SOUND_PUT_AGG_STR,
        "bud_idea_reason_premiseunit_s_del_raw": CREATE_BUDPREM_SOUND_DEL_RAW_STR,
        "bud_idea_reason_premiseunit_s_del_agg": CREATE_BUDPREM_SOUND_DEL_AGG_STR,
        "bud_idea_reason_premiseunit_v_put_raw": CREATE_BUDPREM_VOICE_PUT_RAW_STR,
        "bud_idea_reason_premiseunit_v_put_agg": CREATE_BUDPREM_VOICE_PUT_AGG_STR,
        "bud_idea_reason_premiseunit_v_del_raw": CREATE_BUDPREM_VOICE_DEL_RAW_STR,
        "bud_idea_reason_premiseunit_v_del_agg": CREATE_BUDPREM_VOICE_DEL_AGG_STR,
        "bud_idea_reasonunit_s_put_raw": CREATE_BUDREAS_SOUND_PUT_RAW_STR,
        "bud_idea_reasonunit_s_put_agg": CREATE_BUDREAS_SOUND_PUT_AGG_STR,
        "bud_idea_reasonunit_s_del_raw": CREATE_BUDREAS_SOUND_DEL_RAW_STR,
        "bud_idea_reasonunit_s_del_agg": CREATE_BUDREAS_SOUND_DEL_AGG_STR,
        "bud_idea_reasonunit_v_put_raw": CREATE_BUDREAS_VOICE_PUT_RAW_STR,
        "bud_idea_reasonunit_v_put_agg": CREATE_BUDREAS_VOICE_PUT_AGG_STR,
        "bud_idea_reasonunit_v_del_raw": CREATE_BUDREAS_VOICE_DEL_RAW_STR,
        "bud_idea_reasonunit_v_del_agg": CREATE_BUDREAS_VOICE_DEL_AGG_STR,
        "bud_idea_laborlink_s_put_raw": CREATE_BUDLABOR_SOUND_PUT_RAW_STR,
        "bud_idea_laborlink_s_put_agg": CREATE_BUDLABOR_SOUND_PUT_AGG_STR,
        "bud_idea_laborlink_s_del_raw": CREATE_BUDLABOR_SOUND_DEL_RAW_STR,
        "bud_idea_laborlink_s_del_agg": CREATE_BUDLABOR_SOUND_DEL_AGG_STR,
        "bud_idea_laborlink_v_put_raw": CREATE_BUDLABOR_VOICE_PUT_RAW_STR,
        "bud_idea_laborlink_v_put_agg": CREATE_BUDLABOR_VOICE_PUT_AGG_STR,
        "bud_idea_laborlink_v_del_raw": CREATE_BUDLABOR_VOICE_DEL_RAW_STR,
        "bud_idea_laborlink_v_del_agg": CREATE_BUDLABOR_VOICE_DEL_AGG_STR,
        "bud_ideaunit_s_put_raw": CREATE_BUDIDEA_SOUND_PUT_RAW_STR,
        "bud_ideaunit_s_put_agg": CREATE_BUDIDEA_SOUND_PUT_AGG_STR,
        "bud_ideaunit_s_del_raw": CREATE_BUDIDEA_SOUND_DEL_RAW_STR,
        "bud_ideaunit_s_del_agg": CREATE_BUDIDEA_SOUND_DEL_AGG_STR,
        "bud_ideaunit_v_put_raw": CREATE_BUDIDEA_VOICE_PUT_RAW_STR,
        "bud_ideaunit_v_put_agg": CREATE_BUDIDEA_VOICE_PUT_AGG_STR,
        "bud_ideaunit_v_del_raw": CREATE_BUDIDEA_VOICE_DEL_RAW_STR,
        "bud_ideaunit_v_del_agg": CREATE_BUDIDEA_VOICE_DEL_AGG_STR,
        "budunit_s_put_raw": CREATE_BUDUNIT_SOUND_PUT_RAW_STR,
        "budunit_s_put_agg": CREATE_BUDUNIT_SOUND_PUT_AGG_STR,
        "budunit_s_del_raw": CREATE_BUDUNIT_SOUND_DEL_RAW_STR,
        "budunit_s_del_agg": CREATE_BUDUNIT_SOUND_DEL_AGG_STR,
        "budunit_v_put_raw": CREATE_BUDUNIT_VOICE_PUT_RAW_STR,
        "budunit_v_put_agg": CREATE_BUDUNIT_VOICE_PUT_AGG_STR,
        "budunit_v_del_raw": CREATE_BUDUNIT_VOICE_DEL_RAW_STR,
        "budunit_v_del_agg": CREATE_BUDUNIT_VOICE_DEL_AGG_STR,
    }


CREATE_PIDLABE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDLABE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_agg (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""
CREATE_PIDNAME_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDNAME_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_agg (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""
CREATE_PIDWAYY_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDWAYY_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_way_agg (event_int INTEGER, face_name TEXT, otx_way TEXT, inx_way TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""
CREATE_PIDTAGG_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDTAGG_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_agg (event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""

CREATE_FISCASH_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_agg (fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISCASH_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISDEAL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_agg (fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISDEAL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISHOUR_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_agg (fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT)"""
CREATE_FISHOUR_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT, error_message TEXT)"""
CREATE_FISMONT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_agg (fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT)"""
CREATE_FISMONT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT, error_message TEXT)"""
CREATE_FISWEEK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_agg (fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT)"""
CREATE_FISWEEK_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT, error_message TEXT)"""
CREATE_FISOFFI_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_agg (fisc_tag TEXT, offi_time INTEGER)"""
CREATE_FISOFFI_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_agg (fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""
CREATE_FISUNIT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""

CREATE_BUDMEMB_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"""
CREATE_BUDMEMB_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"""
CREATE_BUDMEMB_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT, error_message TEXT)"""
CREATE_BUDMEMB_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"""
CREATE_BUDACCT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"""
CREATE_BUDACCT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"""
CREATE_BUDACCT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDACCT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"""
CREATE_BUDAWAR_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_awardlink_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label TEXT, give_force REAL, take_force REAL, error_message TEXT)"""
CREATE_BUDAWAR_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_awardlink_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label TEXT, give_force REAL, take_force REAL)"""
CREATE_BUDAWAR_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_awardlink_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label_ERASE TEXT, error_message TEXT)"""
CREATE_BUDAWAR_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_awardlink_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, awardee_label_ERASE TEXT)"""
CREATE_BUDFACT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_factunit_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL, error_message TEXT)"""
CREATE_BUDFACT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_factunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext TEXT, fbranch TEXT, fopen REAL, fnigh REAL)"""
CREATE_BUDFACT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_factunit_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext_ERASE TEXT, error_message TEXT)"""
CREATE_BUDFACT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_factunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, fcontext_ERASE TEXT)"""
CREATE_BUDHEAL_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_healerlink_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name TEXT, error_message TEXT)"""
CREATE_BUDHEAL_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_healerlink_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name TEXT)"""
CREATE_BUDHEAL_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_healerlink_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDHEAL_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_healerlink_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, healer_name_ERASE TEXT)"""
CREATE_BUDPREM_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER, error_message TEXT)"""
CREATE_BUDPREM_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch TEXT, pnigh REAL, popen REAL, pdivisor INTEGER)"""
CREATE_BUDPREM_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch_ERASE TEXT, error_message TEXT)"""
CREATE_BUDPREM_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reason_premiseunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, pbranch_ERASE TEXT)"""
CREATE_BUDREAS_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, rcontext_idea_active_requisite INTEGER, error_message TEXT)"""
CREATE_BUDREAS_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext TEXT, rcontext_idea_active_requisite INTEGER)"""
CREATE_BUDREAS_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext_ERASE TEXT, error_message TEXT)"""
CREATE_BUDREAS_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_reasonunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, rcontext_ERASE TEXT)"""
CREATE_BUDLABOR_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_laborlink_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label TEXT, error_message TEXT)"""
CREATE_BUDLABOR_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_laborlink_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label TEXT)"""
CREATE_BUDLABOR_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_laborlink_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label_ERASE TEXT, error_message TEXT)"""
CREATE_BUDLABOR_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_idea_laborlink_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, labor_label_ERASE TEXT)"""
CREATE_BUDIDEA_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_ideaunit_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"""
CREATE_BUDIDEA_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_ideaunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"""
CREATE_BUDIDEA_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_ideaunit_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way_ERASE TEXT, error_message TEXT)"""
CREATE_BUDIDEA_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_ideaunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, idea_way_ERASE TEXT)"""
CREATE_BUDUNIT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"""
CREATE_BUDUNIT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"""
CREATE_BUDUNIT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_del_raw (creed_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDUNIT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"""


def get_pidgin_prime_create_table_sqlstrs() -> dict[str, str]:
    return {
        "pidgin_label_raw": CREATE_PIDLABE_RAW_SQLSTR,
        "pidgin_label_agg": CREATE_PIDLABE_AGG_SQLSTR,
        "pidgin_name_raw": CREATE_PIDNAME_RAW_SQLSTR,
        "pidgin_name_agg": CREATE_PIDNAME_AGG_SQLSTR,
        "pidgin_way_raw": CREATE_PIDWAYY_RAW_SQLSTR,
        "pidgin_way_agg": CREATE_PIDWAYY_AGG_SQLSTR,
        "pidgin_tag_raw": CREATE_PIDTAGG_RAW_SQLSTR,
        "pidgin_tag_agg": CREATE_PIDTAGG_AGG_SQLSTR,
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
        "bud_idea_awardlink_put_agg": CREATE_BUDAWAR_PUT_AGG_SQLSTR,
        "bud_idea_awardlink_put_raw": CREATE_BUDAWAR_PUT_RAW_SQLSTR,
        "bud_idea_awardlink_del_agg": CREATE_BUDAWAR_DEL_AGG_SQLSTR,
        "bud_idea_awardlink_del_raw": CREATE_BUDAWAR_DEL_RAW_SQLSTR,
        "bud_idea_factunit_put_agg": CREATE_BUDFACT_PUT_AGG_SQLSTR,
        "bud_idea_factunit_put_raw": CREATE_BUDFACT_PUT_RAW_SQLSTR,
        "bud_idea_factunit_del_agg": CREATE_BUDFACT_DEL_AGG_SQLSTR,
        "bud_idea_factunit_del_raw": CREATE_BUDFACT_DEL_RAW_SQLSTR,
        "bud_idea_healerlink_put_agg": CREATE_BUDHEAL_PUT_AGG_SQLSTR,
        "bud_idea_healerlink_put_raw": CREATE_BUDHEAL_PUT_RAW_SQLSTR,
        "bud_idea_healerlink_del_agg": CREATE_BUDHEAL_DEL_AGG_SQLSTR,
        "bud_idea_healerlink_del_raw": CREATE_BUDHEAL_DEL_RAW_SQLSTR,
        "bud_idea_reason_premiseunit_put_agg": CREATE_BUDPREM_PUT_AGG_SQLSTR,
        "bud_idea_reason_premiseunit_put_raw": CREATE_BUDPREM_PUT_RAW_SQLSTR,
        "bud_idea_reason_premiseunit_del_agg": CREATE_BUDPREM_DEL_AGG_SQLSTR,
        "bud_idea_reason_premiseunit_del_raw": CREATE_BUDPREM_DEL_RAW_SQLSTR,
        "bud_idea_reasonunit_put_agg": CREATE_BUDREAS_PUT_AGG_SQLSTR,
        "bud_idea_reasonunit_put_raw": CREATE_BUDREAS_PUT_RAW_SQLSTR,
        "bud_idea_reasonunit_del_agg": CREATE_BUDREAS_DEL_AGG_SQLSTR,
        "bud_idea_reasonunit_del_raw": CREATE_BUDREAS_DEL_RAW_SQLSTR,
        "bud_idea_laborlink_put_agg": CREATE_BUDLABOR_PUT_AGG_SQLSTR,
        "bud_idea_laborlink_put_raw": CREATE_BUDLABOR_PUT_RAW_SQLSTR,
        "bud_idea_laborlink_del_agg": CREATE_BUDLABOR_DEL_AGG_SQLSTR,
        "bud_idea_laborlink_del_raw": CREATE_BUDLABOR_DEL_RAW_SQLSTR,
        "bud_ideaunit_put_agg": CREATE_BUDIDEA_PUT_AGG_SQLSTR,
        "bud_ideaunit_put_raw": CREATE_BUDIDEA_PUT_RAW_SQLSTR,
        "bud_ideaunit_del_agg": CREATE_BUDIDEA_DEL_AGG_SQLSTR,
        "bud_ideaunit_del_raw": CREATE_BUDIDEA_DEL_RAW_SQLSTR,
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


def create_all_creed_tables(conn_or_cursor: sqlite3_Connection):
    creed_refs = get_quick_creeds_column_ref()
    for creed_number, creed_columns in creed_refs.items():
        x_tablename = f"{creed_number}_raw"
        create_creed_sorted_table(conn_or_cursor, x_tablename, creed_columns)


def create_sound_raw_update_inconsist_error_message_sqlstr(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    if dimen[:4].lower() == "fisc":
        exclude_cols = {"creed_number", "event_int", "face_name", "error_message"}
    else:
        exclude_cols = {"creed_number", "error_message"}
    if dimen[:3].lower() == "bud":
        x_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        x_tablename = create_prime_tablename(dimen, "s", "raw")
    dimen_config = get_creed_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())
    return create_update_inconsistency_error_query(
        conn_or_cursor, x_tablename, dimen_focus_columns, exclude_cols
    )


def create_sound_agg_insert_sqlstrs(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    dimen_config = get_creed_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())

    if dimen[:4].lower() == "fisc":
        exclude_cols = {"creed_number", "event_int", "face_name", "error_message"}
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns.remove("event_int")
        dimen_focus_columns.remove("face_name")
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    else:
        exclude_cols = {"creed_number", "error_message"}

    if dimen[:3].lower() == "bud":
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
    if dimen[:3].lower() == "bud":
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
    return f"""INSERT INTO {pidgin_core_s_raw_tablename} (source_dimen, face_name, otx_bridge, inx_bridge, unknown_word)
SELECT '{pidgin_s_agg_tablename}', face_name, otx_bridge, inx_bridge, unknown_word
FROM {pidgin_s_agg_tablename}
GROUP BY face_name, otx_bridge, inx_bridge, unknown_word
;
"""


def create_insert_into_pidgin_core_vld_sqlstr(
    default_bridge: str, default_unknown: str
):
    return f"""INSERT INTO pidgin_core_s_vld (face_name, otx_bridge, inx_bridge, unknown_word)
SELECT
  face_name
, IFNULL(otx_bridge, '{default_bridge}')
, IFNULL(inx_bridge, '{default_bridge}')
, IFNULL(unknown_word, '{default_unknown}')
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


def create_update_pidtagg_sound_agg_bridge_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidtagg_s_agg_tablename = create_prime_tablename("pidtagg", "s", "agg")
    return f"""UPDATE {pidtagg_s_agg_tablename}
SET error_message = 'Bridge cannot exist in TagStr'
WHERE rowid IN (
    SELECT tagg_agg.rowid
    FROM {pidtagg_s_agg_tablename} tagg_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = tagg_agg.face_name
    WHERE tagg_agg.otx_tag LIKE '%' || core_vld.otx_bridge || '%'
      OR tagg_agg.inx_tag LIKE '%' || core_vld.inx_bridge || '%'
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


def create_update_pidlabe_sound_agg_bridge_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidlabe_s_agg_tablename = create_prime_tablename("pidlabe", "s", "agg")
    return f"""UPDATE {pidlabe_s_agg_tablename}
SET error_message = 'Otx and inx labels must match bridge property.'
WHERE rowid IN (
  SELECT label_agg.rowid
  FROM {pidlabe_s_agg_tablename} label_agg
  JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = label_agg.face_name
  WHERE NOT ((
            label_agg.otx_label LIKE core_vld.otx_bridge || '%' 
        AND label_agg.inx_label LIKE core_vld.inx_bridge || '%') 
      OR (
            NOT label_agg.otx_label LIKE core_vld.otx_bridge || '%'
        AND NOT label_agg.inx_label LIKE core_vld.inx_bridge || '%'
        ))
)
;
"""


def create_insert_pidgin_sound_vld_table_sqlstr(dimen: str) -> str:
    pidgin_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    pidgin_s_vld_tablename = create_prime_tablename(dimen, "s", "vld")
    dimen_otx_inx_obj_names = {
        "pidgin_name": "name",
        "pidgin_label": "label",
        "pidgin_tag": "tag",
        "pidgin_way": "way",
    }
    otx_str = f"otx_{dimen_otx_inx_obj_names[dimen]}"
    inx_str = f"inx_{dimen_otx_inx_obj_names[dimen]}"
    return f"""
INSERT INTO {pidgin_s_vld_tablename} (event_int, face_name, {otx_str}, {inx_str})
SELECT event_int, face_name, MAX({otx_str}), MAX({inx_str})
FROM {pidgin_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY event_int, face_name
;
"""


INSERT_FISCASH_VOICE_RAW_SQLSTR = "INSERT INTO fisc_cashbook_v_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, acct_name_otx, tran_time, amount) SELECT event_int, face_name, fisc_tag, owner_name, acct_name, tran_time, amount FROM fisc_cashbook_s_agg "
INSERT_FISDEAL_VOICE_RAW_SQLSTR = "INSERT INTO fisc_dealunit_v_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, deal_time, quota, celldepth) SELECT event_int, face_name, fisc_tag, owner_name, deal_time, quota, celldepth FROM fisc_dealunit_s_agg "
INSERT_FISHOUR_VOICE_RAW_SQLSTR = "INSERT INTO fisc_timeline_hour_v_raw (event_int, face_name_otx, fisc_tag_otx, cumlative_minute, hour_tag_otx) SELECT event_int, face_name, fisc_tag, cumlative_minute, hour_tag FROM fisc_timeline_hour_s_agg "
INSERT_FISMONT_VOICE_RAW_SQLSTR = "INSERT INTO fisc_timeline_month_v_raw (event_int, face_name_otx, fisc_tag_otx, cumlative_day, month_tag_otx) SELECT event_int, face_name, fisc_tag, cumlative_day, month_tag FROM fisc_timeline_month_s_agg "
INSERT_FISWEEK_VOICE_RAW_SQLSTR = "INSERT INTO fisc_timeline_weekday_v_raw (event_int, face_name_otx, fisc_tag_otx, weekday_order, weekday_tag_otx) SELECT event_int, face_name, fisc_tag, weekday_order, weekday_tag FROM fisc_timeline_weekday_s_agg "
INSERT_FISOFFI_VOICE_RAW_SQLSTR = "INSERT INTO fisc_timeoffi_v_raw (event_int, face_name_otx, fisc_tag_otx, offi_time) SELECT event_int, face_name, fisc_tag, offi_time FROM fisc_timeoffi_s_agg "
INSERT_FISUNIT_VOICE_RAW_SQLSTR = "INSERT INTO fiscunit_v_raw (event_int, face_name_otx, fisc_tag_otx, timeline_tag_otx, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations) SELECT event_int, face_name, fisc_tag, timeline_tag, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations FROM fiscunit_s_agg "

INSERT_BUDMEMB_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_acct_membership_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, acct_name_otx, group_label_otx, credit_vote, debtit_vote) SELECT event_int, face_name, fisc_tag, owner_name, acct_name, group_label, credit_vote, debtit_vote FROM bud_acct_membership_s_put_agg "
INSERT_BUDMEMB_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_acct_membership_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, acct_name_otx, group_label_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, acct_name, group_label_ERASE FROM bud_acct_membership_s_del_agg "
INSERT_BUDACCT_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_acctunit_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, acct_name_otx, credit_belief, debtit_belief) SELECT event_int, face_name, fisc_tag, owner_name, acct_name, credit_belief, debtit_belief FROM bud_acctunit_s_put_agg "
INSERT_BUDACCT_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_acctunit_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, acct_name_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, acct_name_ERASE FROM bud_acctunit_s_del_agg "
INSERT_BUDAWAR_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_idea_awardlink_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, awardee_label_otx, give_force, take_force) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label, give_force, take_force FROM bud_idea_awardlink_s_put_agg "
INSERT_BUDAWAR_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_idea_awardlink_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, awardee_label_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label_ERASE FROM bud_idea_awardlink_s_del_agg "
INSERT_BUDFACT_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_idea_factunit_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, fcontext_otx, fbranch_otx, fopen, fnigh) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, fcontext, fbranch, fopen, fnigh FROM bud_idea_factunit_s_put_agg "
INSERT_BUDFACT_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_idea_factunit_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, fcontext_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, fcontext_ERASE FROM bud_idea_factunit_s_del_agg "
INSERT_BUDHEAL_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_idea_healerlink_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, healer_name_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, healer_name FROM bud_idea_healerlink_s_put_agg "
INSERT_BUDHEAL_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_idea_healerlink_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, healer_name_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, healer_name_ERASE FROM bud_idea_healerlink_s_del_agg "
INSERT_BUDPREM_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_idea_reason_premiseunit_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, rcontext_otx, pbranch_otx, pnigh, popen, pdivisor) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch, pnigh, popen, pdivisor FROM bud_idea_reason_premiseunit_s_put_agg "
INSERT_BUDPREM_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_idea_reason_premiseunit_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, rcontext_otx, pbranch_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch_ERASE FROM bud_idea_reason_premiseunit_s_del_agg "
INSERT_BUDREAS_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_idea_reasonunit_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, rcontext_otx, rcontext_idea_active_requisite) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, rcontext_idea_active_requisite FROM bud_idea_reasonunit_s_put_agg "
INSERT_BUDREAS_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_idea_reasonunit_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, rcontext_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext_ERASE FROM bud_idea_reasonunit_s_del_agg "
INSERT_BUDLABO_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_idea_laborlink_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, labor_label_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, labor_label FROM bud_idea_laborlink_s_put_agg "
INSERT_BUDLABO_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_idea_laborlink_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, labor_label_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, labor_label_ERASE FROM bud_idea_laborlink_s_del_agg "
INSERT_BUDIDEA_VOICE_PUT_RAW_SQLSTR = "INSERT INTO bud_ideaunit_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_otx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool) SELECT event_int, face_name, fisc_tag, owner_name, idea_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool FROM bud_ideaunit_s_put_agg "
INSERT_BUDIDEA_VOICE_DEL_RAW_SQLSTR = "INSERT INTO bud_ideaunit_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, idea_way_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name, idea_way_ERASE FROM bud_ideaunit_s_del_agg "
INSERT_BUDUNIT_VOICE_PUT_RAW_SQLSTR = "INSERT INTO budunit_v_put_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_otx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit) SELECT event_int, face_name, fisc_tag, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit FROM budunit_s_put_agg "
INSERT_BUDUNIT_VOICE_DEL_RAW_SQLSTR = "INSERT INTO budunit_v_del_raw (event_int, face_name_otx, fisc_tag_otx, owner_name_ERASE_otx) SELECT event_int, face_name, fisc_tag, owner_name_ERASE FROM budunit_s_del_agg "


def get_insert_into_voice_raw_sqlstrs() -> dict[str, str]:
    return {
        "fisc_cashbook_v_raw": INSERT_FISCASH_VOICE_RAW_SQLSTR,
        "fisc_dealunit_v_raw": INSERT_FISDEAL_VOICE_RAW_SQLSTR,
        "fisc_timeline_hour_v_raw": INSERT_FISHOUR_VOICE_RAW_SQLSTR,
        "fisc_timeline_month_v_raw": INSERT_FISMONT_VOICE_RAW_SQLSTR,
        "fisc_timeline_weekday_v_raw": INSERT_FISWEEK_VOICE_RAW_SQLSTR,
        "fisc_timeoffi_v_raw": INSERT_FISOFFI_VOICE_RAW_SQLSTR,
        "fiscunit_v_raw": INSERT_FISUNIT_VOICE_RAW_SQLSTR,
        "bud_acct_membership_v_put_raw": INSERT_BUDMEMB_VOICE_PUT_RAW_SQLSTR,
        "bud_acct_membership_v_del_raw": INSERT_BUDMEMB_VOICE_DEL_RAW_SQLSTR,
        "bud_acctunit_v_put_raw": INSERT_BUDACCT_VOICE_PUT_RAW_SQLSTR,
        "bud_acctunit_v_del_raw": INSERT_BUDACCT_VOICE_DEL_RAW_SQLSTR,
        "bud_idea_awardlink_v_put_raw": INSERT_BUDAWAR_VOICE_PUT_RAW_SQLSTR,
        "bud_idea_awardlink_v_del_raw": INSERT_BUDAWAR_VOICE_DEL_RAW_SQLSTR,
        "bud_idea_factunit_v_put_raw": INSERT_BUDFACT_VOICE_PUT_RAW_SQLSTR,
        "bud_idea_factunit_v_del_raw": INSERT_BUDFACT_VOICE_DEL_RAW_SQLSTR,
        "bud_idea_healerlink_v_put_raw": INSERT_BUDHEAL_VOICE_PUT_RAW_SQLSTR,
        "bud_idea_healerlink_v_del_raw": INSERT_BUDHEAL_VOICE_DEL_RAW_SQLSTR,
        "bud_idea_reason_premiseunit_v_put_raw": INSERT_BUDPREM_VOICE_PUT_RAW_SQLSTR,
        "bud_idea_reason_premiseunit_v_del_raw": INSERT_BUDPREM_VOICE_DEL_RAW_SQLSTR,
        "bud_idea_reasonunit_v_put_raw": INSERT_BUDREAS_VOICE_PUT_RAW_SQLSTR,
        "bud_idea_reasonunit_v_del_raw": INSERT_BUDREAS_VOICE_DEL_RAW_SQLSTR,
        "bud_idea_laborlink_v_put_raw": INSERT_BUDLABO_VOICE_PUT_RAW_SQLSTR,
        "bud_idea_laborlink_v_del_raw": INSERT_BUDLABO_VOICE_DEL_RAW_SQLSTR,
        "bud_ideaunit_v_put_raw": INSERT_BUDIDEA_VOICE_PUT_RAW_SQLSTR,
        "bud_ideaunit_v_del_raw": INSERT_BUDIDEA_VOICE_DEL_RAW_SQLSTR,
        "budunit_v_put_raw": INSERT_BUDUNIT_VOICE_PUT_RAW_SQLSTR,
        "budunit_v_del_raw": INSERT_BUDUNIT_VOICE_DEL_RAW_SQLSTR,
    }


PIDLABE_INCONSISTENCY_SQLSTR = """SELECT otx_label
FROM pidgin_label_raw
GROUP BY otx_label
HAVING MIN(inx_label) != MAX(inx_label)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
"""
PIDNAME_INCONSISTENCY_SQLSTR = """SELECT otx_name
FROM pidgin_name_raw
GROUP BY otx_name
HAVING MIN(inx_name) != MAX(inx_name)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
"""
PIDWAYY_INCONSISTENCY_SQLSTR = """SELECT otx_way
FROM pidgin_way_raw
GROUP BY otx_way
HAVING MIN(inx_way) != MAX(inx_way)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
"""
PIDTAGG_INCONSISTENCY_SQLSTR = """SELECT otx_tag
FROM pidgin_tag_raw
GROUP BY otx_tag
HAVING MIN(inx_tag) != MAX(inx_tag)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
"""

FISCASH_INCONSISTENCY_SQLSTR = """SELECT fisc_tag, owner_name, acct_name, tran_time
FROM fisc_cashbook_raw
GROUP BY fisc_tag, owner_name, acct_name, tran_time
HAVING MIN(amount) != MAX(amount)
"""
FISDEAL_INCONSISTENCY_SQLSTR = """SELECT fisc_tag, owner_name, deal_time
FROM fisc_dealunit_raw
GROUP BY fisc_tag, owner_name, deal_time
HAVING MIN(quota) != MAX(quota)
    OR MIN(celldepth) != MAX(celldepth)
"""
FISHOUR_INCONSISTENCY_SQLSTR = """SELECT fisc_tag, cumlative_minute
FROM fisc_timeline_hour_raw
GROUP BY fisc_tag, cumlative_minute
HAVING MIN(hour_tag) != MAX(hour_tag)
"""
FISMONT_INCONSISTENCY_SQLSTR = """SELECT fisc_tag, cumlative_day
FROM fisc_timeline_month_raw
GROUP BY fisc_tag, cumlative_day
HAVING MIN(month_tag) != MAX(month_tag)
"""
FISWEEK_INCONSISTENCY_SQLSTR = """SELECT fisc_tag, weekday_order
FROM fisc_timeline_weekday_raw
GROUP BY fisc_tag, weekday_order
HAVING MIN(weekday_tag) != MAX(weekday_tag)
"""
FISOFFI_INCONSISTENCY_SQLSTR = """SELECT fisc_tag, offi_time
FROM fisc_timeoffi_raw
GROUP BY fisc_tag, offi_time
HAVING 1=2
"""
FISUNIT_INCONSISTENCY_SQLSTR = """SELECT fisc_tag
FROM fiscunit_raw
GROUP BY fisc_tag
HAVING MIN(timeline_tag) != MAX(timeline_tag)
    OR MIN(c400_number) != MAX(c400_number)
    OR MIN(yr1_jan1_offset) != MAX(yr1_jan1_offset)
    OR MIN(monthday_distortion) != MAX(monthday_distortion)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
    OR MIN(bridge) != MAX(bridge)
    OR MIN(job_listen_rotations) != MAX(job_listen_rotations)
"""

BUDMEMB_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, acct_name, group_label
FROM bud_acct_membership_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, acct_name, group_label
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
"""
BUDACCT_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, acct_name
FROM bud_acctunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, acct_name
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
"""
BUDAWAR_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label
FROM bud_idea_awardlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
"""
BUDFACT_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, idea_way, fcontext
FROM bud_idea_factunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, fcontext
HAVING MIN(fbranch) != MAX(fbranch)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
"""
BUDHEAL_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, idea_way, healer_name
FROM bud_idea_healerlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, healer_name
HAVING 1=2
"""
BUDPREM_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch
FROM bud_idea_reason_premiseunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch
HAVING MIN(pnigh) != MAX(pnigh)
    OR MIN(popen) != MAX(popen)
    OR MIN(pdivisor) != MAX(pdivisor)
"""
BUDREAS_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext
FROM bud_idea_reasonunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, rcontext
HAVING MIN(rcontext_idea_active_requisite) != MAX(rcontext_idea_active_requisite)
"""
BUDLABOR_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, idea_way, labor_label
FROM bud_idea_laborlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, labor_label
HAVING 1=2
"""
BUDIDEA_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, idea_way
FROM bud_ideaunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way
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
BUDUNIT_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name
FROM budunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name
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
        "pidgin_label": PIDLABE_INCONSISTENCY_SQLSTR,
        "pidgin_name": PIDNAME_INCONSISTENCY_SQLSTR,
        "pidgin_way": PIDWAYY_INCONSISTENCY_SQLSTR,
        "pidgin_tag": PIDTAGG_INCONSISTENCY_SQLSTR,
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
        "bud_idea_awardlink": BUDAWAR_INCONSISTENCY_SQLSTR,
        "bud_idea_factunit": BUDFACT_INCONSISTENCY_SQLSTR,
        "bud_idea_healerlink": BUDHEAL_INCONSISTENCY_SQLSTR,
        "bud_idea_reason_premiseunit": BUDPREM_INCONSISTENCY_SQLSTR,
        "bud_idea_reasonunit": BUDREAS_INCONSISTENCY_SQLSTR,
        "bud_idea_laborlink": BUDLABOR_INCONSISTENCY_SQLSTR,
        "bud_ideaunit": BUDIDEA_INCONSISTENCY_SQLSTR,
        "budunit": BUDUNIT_INCONSISTENCY_SQLSTR,
    }


PIDLABE_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT otx_label
FROM pidgin_label_raw
GROUP BY otx_label
HAVING MIN(inx_label) != MAX(inx_label)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
)
UPDATE pidgin_label_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.otx_label = pidgin_label_raw.otx_label
;
"""
PIDNAME_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT otx_name
FROM pidgin_name_raw
GROUP BY otx_name
HAVING MIN(inx_name) != MAX(inx_name)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
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
    OR MIN(unknown_word) != MAX(unknown_word)
)
UPDATE pidgin_way_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.otx_way = pidgin_way_raw.otx_way
;
"""
PIDTAGG_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT otx_tag
FROM pidgin_tag_raw
GROUP BY otx_tag
HAVING MIN(inx_tag) != MAX(inx_tag)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
)
UPDATE pidgin_tag_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.otx_tag = pidgin_tag_raw.otx_tag
;
"""

FISCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_tag, owner_name, acct_name, tran_time
FROM fisc_cashbook_raw
GROUP BY fisc_tag, owner_name, acct_name, tran_time
HAVING MIN(amount) != MAX(amount)
)
UPDATE fisc_cashbook_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_tag = fisc_cashbook_raw.fisc_tag
    AND inconsistency_rows.owner_name = fisc_cashbook_raw.owner_name
    AND inconsistency_rows.acct_name = fisc_cashbook_raw.acct_name
    AND inconsistency_rows.tran_time = fisc_cashbook_raw.tran_time
;
"""
FISDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_tag, owner_name, deal_time
FROM fisc_dealunit_raw
GROUP BY fisc_tag, owner_name, deal_time
HAVING MIN(quota) != MAX(quota)
    OR MIN(celldepth) != MAX(celldepth)
)
UPDATE fisc_dealunit_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_tag = fisc_dealunit_raw.fisc_tag
    AND inconsistency_rows.owner_name = fisc_dealunit_raw.owner_name
    AND inconsistency_rows.deal_time = fisc_dealunit_raw.deal_time
;
"""
FISHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_tag, cumlative_minute
FROM fisc_timeline_hour_raw
GROUP BY fisc_tag, cumlative_minute
HAVING MIN(hour_tag) != MAX(hour_tag)
)
UPDATE fisc_timeline_hour_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_tag = fisc_timeline_hour_raw.fisc_tag
    AND inconsistency_rows.cumlative_minute = fisc_timeline_hour_raw.cumlative_minute
;
"""
FISMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_tag, cumlative_day
FROM fisc_timeline_month_raw
GROUP BY fisc_tag, cumlative_day
HAVING MIN(month_tag) != MAX(month_tag)
)
UPDATE fisc_timeline_month_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_tag = fisc_timeline_month_raw.fisc_tag
    AND inconsistency_rows.cumlative_day = fisc_timeline_month_raw.cumlative_day
;
"""
FISWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_tag, weekday_order
FROM fisc_timeline_weekday_raw
GROUP BY fisc_tag, weekday_order
HAVING MIN(weekday_tag) != MAX(weekday_tag)
)
UPDATE fisc_timeline_weekday_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_tag = fisc_timeline_weekday_raw.fisc_tag
    AND inconsistency_rows.weekday_order = fisc_timeline_weekday_raw.weekday_order
;
"""
FISOFFI_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_tag, offi_time
FROM fisc_timeoffi_raw
GROUP BY fisc_tag, offi_time
HAVING 1=2
)
UPDATE fisc_timeoffi_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_tag = fisc_timeoffi_raw.fisc_tag
    AND inconsistency_rows.offi_time = fisc_timeoffi_raw.offi_time
;
"""
FISUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_tag
FROM fiscunit_raw
GROUP BY fisc_tag
HAVING MIN(timeline_tag) != MAX(timeline_tag)
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
WHERE inconsistency_rows.fisc_tag = fiscunit_raw.fisc_tag
;
"""

BUDMEMB_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, acct_name, group_label
FROM bud_acct_membership_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, acct_name, group_label
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
)
UPDATE bud_acct_membership_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_acct_membership_put_raw.event_int
    AND inconsistency_rows.face_name = bud_acct_membership_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_acct_membership_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_acct_membership_put_raw.owner_name
    AND inconsistency_rows.acct_name = bud_acct_membership_put_raw.acct_name
    AND inconsistency_rows.group_label = bud_acct_membership_put_raw.group_label
;
"""
BUDACCT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, acct_name
FROM bud_acctunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, acct_name
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
)
UPDATE bud_acctunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_acctunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_acctunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_acctunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_acctunit_put_raw.owner_name
    AND inconsistency_rows.acct_name = bud_acctunit_put_raw.acct_name
;
"""
BUDAWAR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label
FROM bud_idea_awardlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE bud_idea_awardlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_idea_awardlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_idea_awardlink_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_idea_awardlink_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_idea_awardlink_put_raw.owner_name
    AND inconsistency_rows.idea_way = bud_idea_awardlink_put_raw.idea_way
    AND inconsistency_rows.awardee_label = bud_idea_awardlink_put_raw.awardee_label
;
"""
BUDFACT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, fcontext
FROM bud_idea_factunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, fcontext
HAVING MIN(fbranch) != MAX(fbranch)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
)
UPDATE bud_idea_factunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_idea_factunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_idea_factunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_idea_factunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_idea_factunit_put_raw.owner_name
    AND inconsistency_rows.idea_way = bud_idea_factunit_put_raw.idea_way
    AND inconsistency_rows.fcontext = bud_idea_factunit_put_raw.fcontext
;
"""
BUDHEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, healer_name
FROM bud_idea_healerlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, healer_name
HAVING 1=2
)
UPDATE bud_idea_healerlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_idea_healerlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_idea_healerlink_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_idea_healerlink_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_idea_healerlink_put_raw.owner_name
    AND inconsistency_rows.idea_way = bud_idea_healerlink_put_raw.idea_way
    AND inconsistency_rows.healer_name = bud_idea_healerlink_put_raw.healer_name
;
"""
BUDPREM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch
FROM bud_idea_reason_premiseunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch
HAVING MIN(pnigh) != MAX(pnigh)
    OR MIN(popen) != MAX(popen)
    OR MIN(pdivisor) != MAX(pdivisor)
)
UPDATE bud_idea_reason_premiseunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_idea_reason_premiseunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_idea_reason_premiseunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_idea_reason_premiseunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_idea_reason_premiseunit_put_raw.owner_name
    AND inconsistency_rows.idea_way = bud_idea_reason_premiseunit_put_raw.idea_way
    AND inconsistency_rows.rcontext = bud_idea_reason_premiseunit_put_raw.rcontext
    AND inconsistency_rows.pbranch = bud_idea_reason_premiseunit_put_raw.pbranch
;
"""
BUDREAS_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext
FROM bud_idea_reasonunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, rcontext
HAVING MIN(rcontext_idea_active_requisite) != MAX(rcontext_idea_active_requisite)
)
UPDATE bud_idea_reasonunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_idea_reasonunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_idea_reasonunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_idea_reasonunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_idea_reasonunit_put_raw.owner_name
    AND inconsistency_rows.idea_way = bud_idea_reasonunit_put_raw.idea_way
    AND inconsistency_rows.rcontext = bud_idea_reasonunit_put_raw.rcontext
;
"""
BUDLABOR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, labor_label
FROM bud_idea_laborlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, labor_label
HAVING 1=2
)
UPDATE bud_idea_laborlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_idea_laborlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_idea_laborlink_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_idea_laborlink_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_idea_laborlink_put_raw.owner_name
    AND inconsistency_rows.idea_way = bud_idea_laborlink_put_raw.idea_way
    AND inconsistency_rows.labor_label = bud_idea_laborlink_put_raw.labor_label
;
"""
BUDIDEA_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, idea_way
FROM bud_ideaunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way
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
UPDATE bud_ideaunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_ideaunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_ideaunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_ideaunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_ideaunit_put_raw.owner_name
    AND inconsistency_rows.idea_way = bud_ideaunit_put_raw.idea_way
;
"""
BUDUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name
FROM budunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name
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
    AND inconsistency_rows.fisc_tag = budunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = budunit_put_raw.owner_name
;
"""
BUDMEMB_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_acct_membership_del_agg (event_int, face_name, fisc_tag, owner_name, acct_name, group_label_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, acct_name, group_label_ERASE
FROM bud_acct_membership_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, acct_name, group_label_ERASE
;
"""
BUDACCT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_acctunit_del_agg (event_int, face_name, fisc_tag, owner_name, acct_name_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, acct_name_ERASE
FROM bud_acctunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, acct_name_ERASE
;
"""
BUDAWAR_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_awardlink_del_agg (event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label_ERASE
FROM bud_idea_awardlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label_ERASE
;
"""
BUDFACT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_factunit_del_agg (event_int, face_name, fisc_tag, owner_name, idea_way, fcontext_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, fcontext_ERASE
FROM bud_idea_factunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, fcontext_ERASE
;
"""
BUDHEAL_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_healerlink_del_agg (event_int, face_name, fisc_tag, owner_name, idea_way, healer_name_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, healer_name_ERASE
FROM bud_idea_healerlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, healer_name_ERASE
;
"""
BUDPREM_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_reason_premiseunit_del_agg (event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch_ERASE
FROM bud_idea_reason_premiseunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch_ERASE
;
"""
BUDREAS_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_reasonunit_del_agg (event_int, face_name, fisc_tag, owner_name, idea_way, rcontext_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext_ERASE
FROM bud_idea_reasonunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, rcontext_ERASE
;
"""
BUDLABOR_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_laborlink_del_agg (event_int, face_name, fisc_tag, owner_name, idea_way, labor_label_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, labor_label_ERASE
FROM bud_idea_laborlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, labor_label_ERASE
;
"""
BUDIDEA_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_ideaunit_del_agg (event_int, face_name, fisc_tag, owner_name, idea_way_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way_ERASE
FROM bud_ideaunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way_ERASE
;
"""
BUDUNIT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO budunit_del_agg (event_int, face_name, fisc_tag, owner_name_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name_ERASE
FROM budunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name_ERASE
;
"""


def get_pidgin_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    return {
        "pidgin_label": PIDLABE_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "pidgin_name": PIDNAME_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "pidgin_way": PIDWAYY_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "pidgin_tag": PIDTAGG_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
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
        "bud_idea_awardlink": BUDAWAR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_idea_factunit": BUDFACT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_idea_healerlink": BUDHEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_idea_reason_premiseunit": BUDPREM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_idea_reasonunit": BUDREAS_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_idea_laborlink": BUDLABOR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_ideaunit": BUDIDEA_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
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


PIDLABE_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_label_agg (otx_label, inx_label, otx_bridge, inx_bridge, unknown_word)
SELECT otx_label, MAX(inx_label), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_word)
FROM pidgin_label_raw
WHERE error_message IS NULL
GROUP BY otx_label
;
"""
PIDNAME_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_name_agg (otx_name, inx_name, otx_bridge, inx_bridge, unknown_word)
SELECT otx_name, MAX(inx_name), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_word)
FROM pidgin_name_raw
WHERE error_message IS NULL
GROUP BY otx_name
;
"""
PIDWAYY_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_way_agg (otx_way, inx_way, otx_bridge, inx_bridge, unknown_word)
SELECT otx_way, MAX(inx_way), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_word)
FROM pidgin_way_raw
WHERE error_message IS NULL
GROUP BY otx_way
;
"""
PIDTAGG_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_tag_agg (otx_tag, inx_tag, otx_bridge, inx_bridge, unknown_word)
SELECT otx_tag, MAX(inx_tag), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_word)
FROM pidgin_tag_raw
WHERE error_message IS NULL
GROUP BY otx_tag
;
"""

FISCASH_AGG_INSERT_SQLSTR = """INSERT INTO fisc_cashbook_agg (fisc_tag, owner_name, acct_name, tran_time, amount)
SELECT fisc_tag, owner_name, acct_name, tran_time, MAX(amount)
FROM fisc_cashbook_raw
WHERE error_message IS NULL
GROUP BY fisc_tag, owner_name, acct_name, tran_time
;
"""
FISDEAL_AGG_INSERT_SQLSTR = """INSERT INTO fisc_dealunit_agg (fisc_tag, owner_name, deal_time, quota, celldepth)
SELECT fisc_tag, owner_name, deal_time, MAX(quota), MAX(celldepth)
FROM fisc_dealunit_raw
WHERE error_message IS NULL
GROUP BY fisc_tag, owner_name, deal_time
;
"""
FISHOUR_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_hour_agg (fisc_tag, cumlative_minute, hour_tag)
SELECT fisc_tag, cumlative_minute, MAX(hour_tag)
FROM fisc_timeline_hour_raw
WHERE error_message IS NULL
GROUP BY fisc_tag, cumlative_minute
;
"""
FISMONT_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_month_agg (fisc_tag, cumlative_day, month_tag)
SELECT fisc_tag, cumlative_day, MAX(month_tag)
FROM fisc_timeline_month_raw
WHERE error_message IS NULL
GROUP BY fisc_tag, cumlative_day
;
"""
FISWEEK_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_weekday_agg (fisc_tag, weekday_order, weekday_tag)
SELECT fisc_tag, weekday_order, MAX(weekday_tag)
FROM fisc_timeline_weekday_raw
WHERE error_message IS NULL
GROUP BY fisc_tag, weekday_order
;
"""
FISOFFI_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeoffi_agg (fisc_tag, offi_time)
SELECT fisc_tag, offi_time
FROM fisc_timeoffi_raw
WHERE error_message IS NULL
GROUP BY fisc_tag, offi_time
;
"""
FISUNIT_AGG_INSERT_SQLSTR = """INSERT INTO fiscunit_agg (fisc_tag, timeline_tag, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations)
SELECT fisc_tag, MAX(timeline_tag), MAX(c400_number), MAX(yr1_jan1_offset), MAX(monthday_distortion), MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(bridge), MAX(job_listen_rotations)
FROM fiscunit_raw
WHERE error_message IS NULL
GROUP BY fisc_tag
;
"""

BUDMEMB_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_acct_membership_put_agg (event_int, face_name, fisc_tag, owner_name, acct_name, group_label, credit_vote, debtit_vote)
SELECT event_int, face_name, fisc_tag, owner_name, acct_name, group_label, MAX(credit_vote), MAX(debtit_vote)
FROM bud_acct_membership_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, acct_name, group_label
;
"""
BUDACCT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_acctunit_put_agg (event_int, face_name, fisc_tag, owner_name, acct_name, credit_belief, debtit_belief)
SELECT event_int, face_name, fisc_tag, owner_name, acct_name, MAX(credit_belief), MAX(debtit_belief)
FROM bud_acctunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, acct_name
;
"""
BUDAWAR_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_awardlink_put_agg (event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label, give_force, take_force)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label, MAX(give_force), MAX(take_force)
FROM bud_idea_awardlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, awardee_label
;
"""
BUDFACT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_factunit_put_agg (event_int, face_name, fisc_tag, owner_name, idea_way, fcontext, fbranch, fopen, fnigh)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, fcontext, MAX(fbranch), MAX(fopen), MAX(fnigh)
FROM bud_idea_factunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, fcontext
;
"""
BUDHEAL_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_healerlink_put_agg (event_int, face_name, fisc_tag, owner_name, idea_way, healer_name)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, healer_name
FROM bud_idea_healerlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, healer_name
;
"""
BUDPREM_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_reason_premiseunit_put_agg (event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch, pnigh, popen, pdivisor)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch, MAX(pnigh), MAX(popen), MAX(pdivisor)
FROM bud_idea_reason_premiseunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, pbranch
;
"""
BUDREAS_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_reasonunit_put_agg (event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, rcontext_idea_active_requisite)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, rcontext, MAX(rcontext_idea_active_requisite)
FROM bud_idea_reasonunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, rcontext
;
"""
BUDLABOR_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_idea_laborlink_put_agg (event_int, face_name, fisc_tag, owner_name, idea_way, labor_label)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, labor_label
FROM bud_idea_laborlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way, labor_label
;
"""
BUDIDEA_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_ideaunit_put_agg (event_int, face_name, fisc_tag, owner_name, idea_way, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool)
SELECT event_int, face_name, fisc_tag, owner_name, idea_way, MAX(begin), MAX(close), MAX(addin), MAX(numor), MAX(denom), MAX(morph), MAX(gogo_want), MAX(stop_want), MAX(mass), MAX(pledge), MAX(problem_bool)
FROM bud_ideaunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, idea_way
;
"""
BUDUNIT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO budunit_put_agg (event_int, face_name, fisc_tag, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit)
SELECT event_int, face_name, fisc_tag, owner_name, MAX(credor_respect), MAX(debtor_respect), MAX(fund_pool), MAX(max_tree_traverse), MAX(tally), MAX(fund_coin), MAX(penny), MAX(respect_bit)
FROM budunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name
;
"""


def get_pidgin_insert_agg_from_raw_sqlstrs() -> dict[str, str]:
    return {
        "pidgin_label": PIDLABE_AGG_INSERT_SQLSTR,
        "pidgin_name": PIDNAME_AGG_INSERT_SQLSTR,
        "pidgin_way": PIDWAYY_AGG_INSERT_SQLSTR,
        "pidgin_tag": PIDTAGG_AGG_INSERT_SQLSTR,
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
        "bud_idea_awardlink": BUDAWAR_PUT_AGG_INSERT_SQLSTR,
        "bud_idea_factunit": BUDFACT_PUT_AGG_INSERT_SQLSTR,
        "bud_idea_healerlink": BUDHEAL_PUT_AGG_INSERT_SQLSTR,
        "bud_idea_reason_premiseunit": BUDPREM_PUT_AGG_INSERT_SQLSTR,
        "bud_idea_reasonunit": BUDREAS_PUT_AGG_INSERT_SQLSTR,
        "bud_idea_laborlink": BUDLABOR_PUT_AGG_INSERT_SQLSTR,
        "bud_ideaunit": BUDIDEA_PUT_AGG_INSERT_SQLSTR,
        "budunit": BUDUNIT_PUT_AGG_INSERT_SQLSTR,
    }


def get_bud_insert_del_agg_from_raw_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership": BUDMEMB_DEL_AGG_INSERT_SQLSTR,
        "bud_acctunit": BUDACCT_DEL_AGG_INSERT_SQLSTR,
        "bud_idea_awardlink": BUDAWAR_DEL_AGG_INSERT_SQLSTR,
        "bud_idea_factunit": BUDFACT_DEL_AGG_INSERT_SQLSTR,
        "bud_idea_healerlink": BUDHEAL_DEL_AGG_INSERT_SQLSTR,
        "bud_idea_reason_premiseunit": BUDPREM_DEL_AGG_INSERT_SQLSTR,
        "bud_idea_reasonunit": BUDREAS_DEL_AGG_INSERT_SQLSTR,
        "bud_idea_laborlink": BUDLABOR_DEL_AGG_INSERT_SQLSTR,
        "bud_ideaunit": BUDIDEA_DEL_AGG_INSERT_SQLSTR,
        "budunit": BUDUNIT_DEL_AGG_INSERT_SQLSTR,
    }


def get_creed_stageble_put_dimens() -> dict[str, list[str]]:
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
        "br00013": ["bud_ideaunit", "budunit", "fiscunit"],
        "br00019": ["bud_ideaunit", "budunit", "fiscunit"],
        "br00020": ["bud_acct_membership", "bud_acctunit", "budunit", "fiscunit"],
        "br00021": ["bud_acctunit", "budunit", "fiscunit"],
        "br00022": ["bud_idea_awardlink", "bud_ideaunit", "budunit", "fiscunit"],
        "br00023": ["bud_idea_factunit", "bud_ideaunit", "budunit", "fiscunit"],
        "br00024": ["bud_idea_laborlink", "bud_ideaunit", "budunit", "fiscunit"],
        "br00025": ["bud_idea_healerlink", "bud_ideaunit", "budunit", "fiscunit"],
        "br00026": [
            "bud_idea_reason_premiseunit",
            "bud_idea_reasonunit",
            "bud_ideaunit",
            "budunit",
            "fiscunit",
        ],
        "br00027": ["bud_idea_reasonunit", "bud_ideaunit", "budunit", "fiscunit"],
        "br00028": ["bud_ideaunit", "budunit", "fiscunit"],
        "br00029": ["budunit", "fiscunit"],
        "br00036": ["bud_idea_healerlink", "bud_ideaunit", "budunit", "fiscunit"],
        "br00042": [],
        "br00043": [],
        "br00044": [],
        "br00045": [],
        "br00050": ["bud_acctunit", "budunit", "fiscunit"],
        "br00051": ["budunit", "fiscunit"],
        "br00052": ["bud_ideaunit", "budunit", "fiscunit"],
        "br00053": ["bud_ideaunit", "budunit", "fiscunit"],
        "br00054": ["bud_ideaunit", "budunit", "fiscunit"],
        "br00055": ["bud_ideaunit", "budunit", "fiscunit"],
        "br00056": ["bud_idea_reasonunit", "bud_ideaunit", "budunit", "fiscunit"],
        "br00057": ["bud_ideaunit", "budunit", "fiscunit"],
        "br00058": ["budunit", "fiscunit"],
        "br00059": ["fiscunit"],
        "br00113": ["bud_acctunit", "budunit", "fiscunit"],
        "br00115": ["bud_acctunit", "budunit", "fiscunit"],
        "br00116": ["bud_acctunit", "budunit", "fiscunit"],
        "br00117": ["bud_acctunit", "budunit", "fiscunit"],
    }


CREED_STAGEBLE_DEL_DIMENS = {
    "br00050": ["bud_acct_membership"],
    "br00051": ["bud_acctunit"],
    "br00052": ["bud_idea_awardlink"],
    "br00053": ["bud_idea_factunit"],
    "br00054": ["bud_idea_laborlink"],
    "br00055": ["bud_idea_healerlink"],
    "br00056": ["bud_idea_reason_premiseunit"],
    "br00057": ["bud_idea_reasonunit"],
    "br00058": ["bud_ideaunit"],
    "br00059": ["budunit"],
}


CREATE_FISC_EVENT_TIME_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
  fisc_tag TEXT
, event_int INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
INSERT_FISC_EVENT_TIME_AGG_SQLSTR = """
INSERT INTO fisc_event_time_agg (fisc_tag, event_int, agg_time)
SELECT fisc_tag, event_int, agg_time
FROM (
    SELECT fisc_tag, event_int, tran_time as agg_time
    FROM fisc_cashbook_raw
    GROUP BY fisc_tag, event_int, tran_time
    UNION 
    SELECT fisc_tag, event_int, deal_time as agg_time
    FROM fisc_dealunit_raw
    GROUP BY fisc_tag, event_int, deal_time
)
ORDER BY fisc_tag, event_int, agg_time
;
"""
UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR = """
WITH EventTimeOrdered AS (
    SELECT fisc_tag, event_int, agg_time,
           LAG(agg_time) OVER (PARTITION BY fisc_tag ORDER BY event_int) AS prev_agg_time
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
    AND EventTimeOrdered.fisc_tag = fisc_event_time_agg.fisc_tag
    AND EventTimeOrdered.agg_time = fisc_event_time_agg.agg_time
;
"""


CREATE_FISC_OTE1_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
  fisc_tag TEXT
, owner_name TEXT
, event_int INTEGER
, deal_time INTEGER
, error_message TEXT
)
;
"""
INSERT_FISC_OTE1_AGG_SQLSTR = """
INSERT INTO fisc_ote1_agg (fisc_tag, owner_name, event_int, deal_time)
SELECT fisc_tag, owner_name, event_int, deal_time
FROM (
    SELECT fisc_tag, owner_name, event_int, deal_time
    FROM fisc_dealunit_raw
    GROUP BY fisc_tag, owner_name, event_int, deal_time
)
ORDER BY fisc_tag, owner_name, event_int, deal_time
;
"""


FISCASH_FU1_SELECT_SQLSTR = "SELECT fisc_tag, owner_name, acct_name, tran_time, amount FROM fisc_cashbook_agg WHERE fisc_tag = "
FISDEAL_FU1_SELECT_SQLSTR = "SELECT fisc_tag, owner_name, deal_time, quota, celldepth FROM fisc_dealunit_agg WHERE fisc_tag = "
FISHOUR_FU1_SELECT_SQLSTR = "SELECT fisc_tag, cumlative_minute, hour_tag FROM fisc_timeline_hour_agg WHERE fisc_tag = "
FISMONT_FU1_SELECT_SQLSTR = "SELECT fisc_tag, cumlative_day, month_tag FROM fisc_timeline_month_agg WHERE fisc_tag = "
FISWEEK_FU1_SELECT_SQLSTR = "SELECT fisc_tag, weekday_order, weekday_tag FROM fisc_timeline_weekday_agg WHERE fisc_tag = "
FISOFFI_FU1_SELECT_SQLSTR = (
    "SELECT fisc_tag, offi_time FROM fisc_timeoffi_agg WHERE fisc_tag = "
)
FISUNIT_FU1_SELECT_SQLSTR = "SELECT fisc_tag, timeline_tag, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations FROM fiscunit_agg WHERE fisc_tag = "


def get_fisc_fu1_select_sqlstrs(fisc_tag: str) -> dict[str, str]:
    return {
        "fiscunit": f"{FISUNIT_FU1_SELECT_SQLSTR}'{fisc_tag}'",
        "fisc_dealunit": f"{FISDEAL_FU1_SELECT_SQLSTR}'{fisc_tag}'",
        "fisc_cashbook": f"{FISCASH_FU1_SELECT_SQLSTR}'{fisc_tag}'",
        "fisc_timeline_hour": f"{FISHOUR_FU1_SELECT_SQLSTR}'{fisc_tag}'",
        "fisc_timeline_month": f"{FISMONT_FU1_SELECT_SQLSTR}'{fisc_tag}'",
        "fisc_timeline_weekday": f"{FISWEEK_FU1_SELECT_SQLSTR}'{fisc_tag}'",
        "fisc_timeoffi": f"{FISOFFI_FU1_SELECT_SQLSTR}'{fisc_tag}'",
    }
