from src.a00_data_toolbox.db_toolbox import (
    get_table_columns,
    create_update_inconsistency_error_query,
    create_table2table_agg_insert_query,
)
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
    "BUDTEAM",
    "BUDITEM",
    "BUDUNIT",
    "PIDLABE",
    "PIDNAME",
    "PIDROAD",
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
        "bud_item_awardlink": "BUDAWAR",
        "bud_item_factunit": "BUDFACT",
        "bud_item_healerlink": "BUDHEAL",
        "bud_item_reason_premiseunit": "BUDPREM",
        "bud_item_reasonunit": "BUDREAS",
        "bud_item_teamlink": "BUDTEAM",
        "bud_itemunit": "BUDITEM",
        "budunit": "BUDUNIT",
        "pidgin_label": "PIDLABE",
        "pidgin_name": "PIDNAME",
        "pidgin_road": "PIDROAD",
        "pidgin_tag": "PIDTAGG",
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
        "BUDAWAR": "bud_item_awardlink",
        "BUDFACT": "bud_item_factunit",
        "BUDHEAL": "bud_item_healerlink",
        "BUDPREM": "bud_item_reason_premiseunit",
        "BUDREAS": "bud_item_reasonunit",
        "BUDTEAM": "bud_item_teamlink",
        "BUDITEM": "bud_itemunit",
        "BUDUNIT": "budunit",
        "PIDLABE": "pidgin_label",
        "PIDNAME": "pidgin_name",
        "PIDROAD": "pidgin_road",
        "PIDTAGG": "pidgin_tag",
        "PIDCORE": "pidgin_core",
    }
    tablename = idea_dimen_or_abbv7
    if abbv_references.get(idea_dimen_or_abbv7.upper()):
        tablename = abbv_references.get(idea_dimen_or_abbv7.upper())
    if sound in {"s", "v"}:
        tablename = f"{tablename}_{sound}"

    return f"{tablename}_{put_del}_{stage}" if put_del else f"{tablename}_{stage}"


CREATE_PIDLABE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_agg (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_vld (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT)"""
CREATE_PIDNAME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_agg (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_vld (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT)"""
CREATE_PIDROAD_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_road_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_road TEXT, inx_road TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDROAD_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_road_s_agg (event_int INTEGER, face_name TEXT, otx_road TEXT, inx_road TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDROAD_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_road_s_vld (event_int INTEGER, face_name TEXT, otx_road TEXT, inx_road TEXT)"""
CREATE_PIDTAGG_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDTAGG_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_s_agg (event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDTAGG_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_s_vld (event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT)"""

CREATE_PIDCORE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_raw (source_dimen TEXT, face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDCORE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_agg (face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""
CREATE_PIDCORE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_vld (face_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""

CREATE_FISCASH_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISCASH_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISCASH_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_v_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISCASH_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_v_agg (fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISDEAL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISDEAL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISDEAL_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_v_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISDEAL_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_v_agg (fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISHOUR_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT, error_message TEXT)"""
CREATE_FISHOUR_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT)"""
CREATE_FISHOUR_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_v_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT, error_message TEXT)"""
CREATE_FISHOUR_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_v_agg (fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT)"""
CREATE_FISMONT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT, error_message TEXT)"""
CREATE_FISMONT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT)"""
CREATE_FISMONT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_v_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT, error_message TEXT)"""
CREATE_FISMONT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_v_agg (fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT)"""
CREATE_FISWEEK_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT, error_message TEXT)"""
CREATE_FISWEEK_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT)"""
CREATE_FISWEEK_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_v_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT, error_message TEXT)"""
CREATE_FISWEEK_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_v_agg (fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT)"""
CREATE_FISOFFI_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISOFFI_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, offi_time INTEGER)"""
CREATE_FISOFFI_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_v_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISOFFI_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_v_agg (fisc_tag TEXT, offi_time INTEGER)"""
CREATE_FISUNIT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_FISUNIT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_s_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""
CREATE_FISUNIT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_v_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_FISUNIT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_v_agg (fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""

CREATE_BUDMEMB_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"
CREATE_BUDMEMB_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"
CREATE_BUDMEMB_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"
CREATE_BUDMEMB_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"
CREATE_BUDMEMB_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"
CREATE_BUDMEMB_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acct_membership_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"
CREATE_BUDACCT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"
CREATE_BUDACCT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDACCT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDACCT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"
CREATE_BUDACCT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDACCT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_acctunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"
CREATE_BUDAWAR_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_awardlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_BUDAWAR_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_awardlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_awardlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title_ERASE TEXT)"
CREATE_BUDAWAR_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_awardlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title_ERASE TEXT)"
CREATE_BUDAWAR_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_awardlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_awardlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BUDAWAR_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_awardlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title_ERASE TEXT)"
CREATE_BUDAWAR_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_awardlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title_ERASE TEXT)"
CREATE_BUDFACT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_factunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase TEXT, fneed TEXT, fopen REAL, fnigh REAL, error_message TEXT)"
CREATE_BUDFACT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_factunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase TEXT, fneed TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_factunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase_ERASE TEXT)"
CREATE_BUDFACT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_factunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase_ERASE TEXT)"
CREATE_BUDFACT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_factunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase TEXT, fneed TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_factunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase TEXT, fneed TEXT, fopen REAL, fnigh REAL)"
CREATE_BUDFACT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_factunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase_ERASE TEXT)"
CREATE_BUDFACT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_factunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase_ERASE TEXT)"
CREATE_BUDHEAL_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_healerlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name TEXT, error_message TEXT)"
CREATE_BUDHEAL_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_healerlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name TEXT)"
CREATE_BUDHEAL_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_healerlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name_ERASE TEXT)"
CREATE_BUDHEAL_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_healerlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name_ERASE TEXT)"
CREATE_BUDHEAL_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_healerlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name TEXT)"
CREATE_BUDHEAL_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_healerlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name TEXT)"
CREATE_BUDHEAL_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_healerlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name_ERASE TEXT)"
CREATE_BUDHEAL_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_healerlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name_ERASE TEXT)"
CREATE_BUDPREM_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor INTEGER, error_message TEXT)"
CREATE_BUDPREM_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor INTEGER)"
CREATE_BUDPREM_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need_ERASE TEXT)"
CREATE_BUDPREM_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need_ERASE TEXT)"
CREATE_BUDPREM_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor INTEGER)"
CREATE_BUDPREM_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor INTEGER)"
CREATE_BUDPREM_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need_ERASE TEXT)"
CREATE_BUDPREM_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need_ERASE TEXT)"
CREATE_BUDREAS_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_reasonunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite INTEGER, error_message TEXT)"
CREATE_BUDREAS_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_reasonunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite INTEGER)"
CREATE_BUDREAS_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_reasonunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT)"
CREATE_BUDREAS_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_reasonunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT)"
CREATE_BUDREAS_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_reasonunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite INTEGER)"
CREATE_BUDREAS_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_reasonunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite INTEGER)"
CREATE_BUDREAS_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_reasonunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT)"
CREATE_BUDREAS_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_reasonunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT)"
CREATE_BUDTEAM_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_teamlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title TEXT, error_message TEXT)"
CREATE_BUDTEAM_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_teamlink_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title TEXT)"
CREATE_BUDTEAM_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_teamlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title_ERASE TEXT)"
CREATE_BUDTEAM_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_teamlink_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title_ERASE TEXT)"
CREATE_BUDTEAM_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_teamlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title TEXT)"
CREATE_BUDTEAM_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_teamlink_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title TEXT)"
CREATE_BUDTEAM_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_item_teamlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title_ERASE TEXT)"
CREATE_BUDTEAM_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_item_teamlink_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title_ERASE TEXT)"
CREATE_BUDITEM_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_itemunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_BUDITEM_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_itemunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDITEM_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_itemunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road_ERASE TEXT)"
CREATE_BUDITEM_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_itemunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road_ERASE TEXT)"
CREATE_BUDITEM_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_itemunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDITEM_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_itemunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BUDITEM_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS bud_itemunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road_ERASE TEXT)"
CREATE_BUDITEM_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS bud_itemunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road_ERASE TEXT)"
CREATE_BUDUNIT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"
CREATE_BUDUNIT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_s_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"
CREATE_BUDUNIT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_s_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"
CREATE_BUDUNIT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_v_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"
CREATE_BUDUNIT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS budunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"
CREATE_BUDUNIT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS budunit_v_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"


def get_prime_create_table_sqlstrs() -> dict[str:str]:
    return {
        "pidgin_label_s_raw": CREATE_PIDLABE_SOUND_RAW_SQLSTR,
        "pidgin_label_s_agg": CREATE_PIDLABE_SOUND_AGG_SQLSTR,
        "pidgin_label_s_vld": CREATE_PIDLABE_SOUND_VLD_SQLSTR,
        "pidgin_name_s_raw": CREATE_PIDNAME_SOUND_RAW_SQLSTR,
        "pidgin_name_s_agg": CREATE_PIDNAME_SOUND_AGG_SQLSTR,
        "pidgin_name_s_vld": CREATE_PIDNAME_SOUND_VLD_SQLSTR,
        "pidgin_road_s_raw": CREATE_PIDROAD_SOUND_RAW_SQLSTR,
        "pidgin_road_s_agg": CREATE_PIDROAD_SOUND_AGG_SQLSTR,
        "pidgin_road_s_vld": CREATE_PIDROAD_SOUND_VLD_SQLSTR,
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
        "bud_item_awardlink_s_put_raw": CREATE_BUDAWAR_SOUND_PUT_RAW_STR,
        "bud_item_awardlink_s_put_agg": CREATE_BUDAWAR_SOUND_PUT_AGG_STR,
        "bud_item_awardlink_s_del_raw": CREATE_BUDAWAR_SOUND_DEL_RAW_STR,
        "bud_item_awardlink_s_del_agg": CREATE_BUDAWAR_SOUND_DEL_AGG_STR,
        "bud_item_awardlink_v_put_raw": CREATE_BUDAWAR_VOICE_PUT_RAW_STR,
        "bud_item_awardlink_v_put_agg": CREATE_BUDAWAR_VOICE_PUT_AGG_STR,
        "bud_item_awardlink_v_del_raw": CREATE_BUDAWAR_VOICE_DEL_RAW_STR,
        "bud_item_awardlink_v_del_agg": CREATE_BUDAWAR_VOICE_DEL_AGG_STR,
        "bud_item_factunit_s_put_raw": CREATE_BUDFACT_SOUND_PUT_RAW_STR,
        "bud_item_factunit_s_put_agg": CREATE_BUDFACT_SOUND_PUT_AGG_STR,
        "bud_item_factunit_s_del_raw": CREATE_BUDFACT_SOUND_DEL_RAW_STR,
        "bud_item_factunit_s_del_agg": CREATE_BUDFACT_SOUND_DEL_AGG_STR,
        "bud_item_factunit_v_put_raw": CREATE_BUDFACT_VOICE_PUT_RAW_STR,
        "bud_item_factunit_v_put_agg": CREATE_BUDFACT_VOICE_PUT_AGG_STR,
        "bud_item_factunit_v_del_raw": CREATE_BUDFACT_VOICE_DEL_RAW_STR,
        "bud_item_factunit_v_del_agg": CREATE_BUDFACT_VOICE_DEL_AGG_STR,
        "bud_item_healerlink_s_put_raw": CREATE_BUDHEAL_SOUND_PUT_RAW_STR,
        "bud_item_healerlink_s_put_agg": CREATE_BUDHEAL_SOUND_PUT_AGG_STR,
        "bud_item_healerlink_s_del_raw": CREATE_BUDHEAL_SOUND_DEL_RAW_STR,
        "bud_item_healerlink_s_del_agg": CREATE_BUDHEAL_SOUND_DEL_AGG_STR,
        "bud_item_healerlink_v_put_raw": CREATE_BUDHEAL_VOICE_PUT_RAW_STR,
        "bud_item_healerlink_v_put_agg": CREATE_BUDHEAL_VOICE_PUT_AGG_STR,
        "bud_item_healerlink_v_del_raw": CREATE_BUDHEAL_VOICE_DEL_RAW_STR,
        "bud_item_healerlink_v_del_agg": CREATE_BUDHEAL_VOICE_DEL_AGG_STR,
        "bud_item_reason_premiseunit_s_put_raw": CREATE_BUDPREM_SOUND_PUT_RAW_STR,
        "bud_item_reason_premiseunit_s_put_agg": CREATE_BUDPREM_SOUND_PUT_AGG_STR,
        "bud_item_reason_premiseunit_s_del_raw": CREATE_BUDPREM_SOUND_DEL_RAW_STR,
        "bud_item_reason_premiseunit_s_del_agg": CREATE_BUDPREM_SOUND_DEL_AGG_STR,
        "bud_item_reason_premiseunit_v_put_raw": CREATE_BUDPREM_VOICE_PUT_RAW_STR,
        "bud_item_reason_premiseunit_v_put_agg": CREATE_BUDPREM_VOICE_PUT_AGG_STR,
        "bud_item_reason_premiseunit_v_del_raw": CREATE_BUDPREM_VOICE_DEL_RAW_STR,
        "bud_item_reason_premiseunit_v_del_agg": CREATE_BUDPREM_VOICE_DEL_AGG_STR,
        "bud_item_reasonunit_s_put_raw": CREATE_BUDREAS_SOUND_PUT_RAW_STR,
        "bud_item_reasonunit_s_put_agg": CREATE_BUDREAS_SOUND_PUT_AGG_STR,
        "bud_item_reasonunit_s_del_raw": CREATE_BUDREAS_SOUND_DEL_RAW_STR,
        "bud_item_reasonunit_s_del_agg": CREATE_BUDREAS_SOUND_DEL_AGG_STR,
        "bud_item_reasonunit_v_put_raw": CREATE_BUDREAS_VOICE_PUT_RAW_STR,
        "bud_item_reasonunit_v_put_agg": CREATE_BUDREAS_VOICE_PUT_AGG_STR,
        "bud_item_reasonunit_v_del_raw": CREATE_BUDREAS_VOICE_DEL_RAW_STR,
        "bud_item_reasonunit_v_del_agg": CREATE_BUDREAS_VOICE_DEL_AGG_STR,
        "bud_item_teamlink_s_put_raw": CREATE_BUDTEAM_SOUND_PUT_RAW_STR,
        "bud_item_teamlink_s_put_agg": CREATE_BUDTEAM_SOUND_PUT_AGG_STR,
        "bud_item_teamlink_s_del_raw": CREATE_BUDTEAM_SOUND_DEL_RAW_STR,
        "bud_item_teamlink_s_del_agg": CREATE_BUDTEAM_SOUND_DEL_AGG_STR,
        "bud_item_teamlink_v_put_raw": CREATE_BUDTEAM_VOICE_PUT_RAW_STR,
        "bud_item_teamlink_v_put_agg": CREATE_BUDTEAM_VOICE_PUT_AGG_STR,
        "bud_item_teamlink_v_del_raw": CREATE_BUDTEAM_VOICE_DEL_RAW_STR,
        "bud_item_teamlink_v_del_agg": CREATE_BUDTEAM_VOICE_DEL_AGG_STR,
        "bud_itemunit_s_put_raw": CREATE_BUDITEM_SOUND_PUT_RAW_STR,
        "bud_itemunit_s_put_agg": CREATE_BUDITEM_SOUND_PUT_AGG_STR,
        "bud_itemunit_s_del_raw": CREATE_BUDITEM_SOUND_DEL_RAW_STR,
        "bud_itemunit_s_del_agg": CREATE_BUDITEM_SOUND_DEL_AGG_STR,
        "bud_itemunit_v_put_raw": CREATE_BUDITEM_VOICE_PUT_RAW_STR,
        "bud_itemunit_v_put_agg": CREATE_BUDITEM_VOICE_PUT_AGG_STR,
        "bud_itemunit_v_del_raw": CREATE_BUDITEM_VOICE_DEL_RAW_STR,
        "bud_itemunit_v_del_agg": CREATE_BUDITEM_VOICE_DEL_AGG_STR,
        "budunit_s_put_raw": CREATE_BUDUNIT_SOUND_PUT_RAW_STR,
        "budunit_s_put_agg": CREATE_BUDUNIT_SOUND_PUT_AGG_STR,
        "budunit_s_del_raw": CREATE_BUDUNIT_SOUND_DEL_RAW_STR,
        "budunit_s_del_agg": CREATE_BUDUNIT_SOUND_DEL_AGG_STR,
        "budunit_v_put_raw": CREATE_BUDUNIT_VOICE_PUT_RAW_STR,
        "budunit_v_put_agg": CREATE_BUDUNIT_VOICE_PUT_AGG_STR,
        "budunit_v_del_raw": CREATE_BUDUNIT_VOICE_DEL_RAW_STR,
        "budunit_v_del_agg": CREATE_BUDUNIT_VOICE_DEL_AGG_STR,
    }


CREATE_PIDLABE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDLABE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_agg (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""
CREATE_PIDNAME_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDNAME_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_agg (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""
CREATE_PIDROAD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_road_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_road TEXT, inx_road TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDROAD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_road_agg (event_int INTEGER, face_name TEXT, otx_road TEXT, inx_road TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""
CREATE_PIDTAGG_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT, error_message TEXT)"""
CREATE_PIDTAGG_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_tag_agg (event_int INTEGER, face_name TEXT, otx_tag TEXT, inx_tag TEXT, otx_bridge TEXT, inx_bridge TEXT, unknown_word TEXT)"""

CREATE_FISCASH_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_agg (fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_FISCASH_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISDEAL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_agg (fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT)"""
CREATE_FISDEAL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_dealunit_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, deal_time INTEGER, quota REAL, celldepth INT, error_message TEXT)"""
CREATE_FISHOUR_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_agg (fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT)"""
CREATE_FISHOUR_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_minute INTEGER, hour_tag TEXT, error_message TEXT)"""
CREATE_FISMONT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_agg (fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT)"""
CREATE_FISMONT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, cumlative_day INTEGER, month_tag TEXT, error_message TEXT)"""
CREATE_FISWEEK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_agg (fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT)"""
CREATE_FISWEEK_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, weekday_order INTEGER, weekday_tag TEXT, error_message TEXT)"""
CREATE_FISOFFI_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_agg (fisc_tag TEXT, offi_time INTEGER)"""
CREATE_FISOFFI_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeoffi_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_FISUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_agg (fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER)"""
CREATE_FISUNIT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, timeline_tag TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, bridge TEXT, job_listen_rotations INTEGER, error_message TEXT)"""

CREATE_BUDMEMB_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"""
CREATE_BUDMEMB_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"""
CREATE_BUDMEMB_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"""
CREATE_BUDMEMB_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT, error_message TEXT)"""
CREATE_BUDACCT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"""
CREATE_BUDACCT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"""
CREATE_BUDACCT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT)"""
CREATE_BUDACCT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, acct_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDAWAR_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"""
CREATE_BUDAWAR_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"""
CREATE_BUDAWAR_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title_ERASE TEXT)"""
CREATE_BUDAWAR_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, awardee_title_ERASE TEXT, error_message TEXT)"""
CREATE_BUDFACT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase TEXT, fneed TEXT, fopen REAL, fnigh REAL)"""
CREATE_BUDFACT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase TEXT, fneed TEXT, fopen REAL, fnigh REAL, error_message TEXT)"""
CREATE_BUDFACT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase_ERASE TEXT)"""
CREATE_BUDFACT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, fbase_ERASE TEXT, error_message TEXT)"""
CREATE_BUDHEAL_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name TEXT)"""
CREATE_BUDHEAL_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name TEXT, error_message TEXT)"""
CREATE_BUDHEAL_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name_ERASE TEXT)"""
CREATE_BUDHEAL_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, healer_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDPREM_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor INTEGER)"""
CREATE_BUDPREM_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor INTEGER, error_message TEXT)"""
CREATE_BUDPREM_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need_ERASE TEXT)"""
CREATE_BUDPREM_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, need_ERASE TEXT, error_message TEXT)"""
CREATE_BUDREAS_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite INTEGER)"""
CREATE_BUDREAS_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite INTEGER, error_message TEXT)"""
CREATE_BUDREAS_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT)"""
CREATE_BUDREAS_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT, error_message TEXT)"""
CREATE_BUDTEAM_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title TEXT)"""
CREATE_BUDTEAM_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title TEXT, error_message TEXT)"""
CREATE_BUDTEAM_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title_ERASE TEXT)"""
CREATE_BUDTEAM_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, team_title_ERASE TEXT, error_message TEXT)"""
CREATE_BUDITEM_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER)"""
CREATE_BUDITEM_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"""
CREATE_BUDITEM_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road_ERASE TEXT)"""
CREATE_BUDITEM_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, road_ERASE TEXT, error_message TEXT)"""
CREATE_BUDUNIT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL)"""
CREATE_BUDUNIT_PUT_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"""
CREATE_BUDUNIT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_del_agg (event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT)"""
CREATE_BUDUNIT_DEL_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, fisc_tag TEXT, owner_name_ERASE TEXT, error_message TEXT)"""


def get_pidgin_prime_create_table_sqlstrs() -> dict[str, str]:
    return {
        "pidgin_label_raw": CREATE_PIDLABE_RAW_SQLSTR,
        "pidgin_label_agg": CREATE_PIDLABE_AGG_SQLSTR,
        "pidgin_name_raw": CREATE_PIDNAME_RAW_SQLSTR,
        "pidgin_name_agg": CREATE_PIDNAME_AGG_SQLSTR,
        "pidgin_road_raw": CREATE_PIDROAD_RAW_SQLSTR,
        "pidgin_road_agg": CREATE_PIDROAD_AGG_SQLSTR,
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
        "bud_item_awardlink_put_agg": CREATE_BUDAWAR_PUT_AGG_SQLSTR,
        "bud_item_awardlink_put_raw": CREATE_BUDAWAR_PUT_RAW_SQLSTR,
        "bud_item_awardlink_del_agg": CREATE_BUDAWAR_DEL_AGG_SQLSTR,
        "bud_item_awardlink_del_raw": CREATE_BUDAWAR_DEL_RAW_SQLSTR,
        "bud_item_factunit_put_agg": CREATE_BUDFACT_PUT_AGG_SQLSTR,
        "bud_item_factunit_put_raw": CREATE_BUDFACT_PUT_RAW_SQLSTR,
        "bud_item_factunit_del_agg": CREATE_BUDFACT_DEL_AGG_SQLSTR,
        "bud_item_factunit_del_raw": CREATE_BUDFACT_DEL_RAW_SQLSTR,
        "bud_item_healerlink_put_agg": CREATE_BUDHEAL_PUT_AGG_SQLSTR,
        "bud_item_healerlink_put_raw": CREATE_BUDHEAL_PUT_RAW_SQLSTR,
        "bud_item_healerlink_del_agg": CREATE_BUDHEAL_DEL_AGG_SQLSTR,
        "bud_item_healerlink_del_raw": CREATE_BUDHEAL_DEL_RAW_SQLSTR,
        "bud_item_reason_premiseunit_put_agg": CREATE_BUDPREM_PUT_AGG_SQLSTR,
        "bud_item_reason_premiseunit_put_raw": CREATE_BUDPREM_PUT_RAW_SQLSTR,
        "bud_item_reason_premiseunit_del_agg": CREATE_BUDPREM_DEL_AGG_SQLSTR,
        "bud_item_reason_premiseunit_del_raw": CREATE_BUDPREM_DEL_RAW_SQLSTR,
        "bud_item_reasonunit_put_agg": CREATE_BUDREAS_PUT_AGG_SQLSTR,
        "bud_item_reasonunit_put_raw": CREATE_BUDREAS_PUT_RAW_SQLSTR,
        "bud_item_reasonunit_del_agg": CREATE_BUDREAS_DEL_AGG_SQLSTR,
        "bud_item_reasonunit_del_raw": CREATE_BUDREAS_DEL_RAW_SQLSTR,
        "bud_item_teamlink_put_agg": CREATE_BUDTEAM_PUT_AGG_SQLSTR,
        "bud_item_teamlink_put_raw": CREATE_BUDTEAM_PUT_RAW_SQLSTR,
        "bud_item_teamlink_del_agg": CREATE_BUDTEAM_DEL_AGG_SQLSTR,
        "bud_item_teamlink_del_raw": CREATE_BUDTEAM_DEL_RAW_SQLSTR,
        "bud_itemunit_put_agg": CREATE_BUDITEM_PUT_AGG_SQLSTR,
        "bud_itemunit_put_raw": CREATE_BUDITEM_PUT_RAW_SQLSTR,
        "bud_itemunit_del_agg": CREATE_BUDITEM_DEL_AGG_SQLSTR,
        "bud_itemunit_del_raw": CREATE_BUDITEM_DEL_RAW_SQLSTR,
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
    if dimen[:4].lower() == "fisc":
        exclude_cols = {"idea_number", "event_int", "face_name", "error_message"}
    else:
        exclude_cols = {"idea_number", "error_message"}
    if dimen[:3].lower() == "bud":
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

    if dimen[:4].lower() == "fisc":
        exclude_cols = {"idea_number", "event_int", "face_name", "error_message"}
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns.remove("event_int")
        dimen_focus_columns.remove("face_name")
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    else:
        exclude_cols = {"idea_number", "error_message"}

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
SET error_message = 'Bridge cannot exist in TagUnit'
WHERE rowid IN (
    SELECT tagg_agg.rowid
    FROM {pidtagg_s_agg_tablename} tagg_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = tagg_agg.face_name
    WHERE tagg_agg.otx_tag LIKE '%' || core_vld.otx_bridge || '%'
      OR tagg_agg.inx_tag LIKE '%' || core_vld.inx_bridge || '%'
)
;
"""


def create_update_pidroad_sound_agg_bridge_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidroad_s_agg_tablename = create_prime_tablename("pidroad", "s", "agg")
    return f"""UPDATE {pidroad_s_agg_tablename}
SET error_message = 'Bridge must exist in RoadUnit'
WHERE rowid IN (
    SELECT road_agg.rowid
    FROM {pidroad_s_agg_tablename} road_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = road_agg.face_name
    WHERE NOT road_agg.otx_road LIKE core_vld.otx_bridge || '%'
        OR NOT road_agg.inx_road LIKE core_vld.inx_bridge || '%'
)
;
"""


def create_update_pidname_sound_agg_bridge_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidname_s_agg_tablename = create_prime_tablename("pidname", "s", "agg")
    return f"""UPDATE {pidname_s_agg_tablename}
SET error_message = 'Bridge cannot exist in NameUnit'
WHERE rowid IN (
    SELECT name_agg.rowid
    FROM {pidname_s_agg_tablename} name_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = name_agg.face_name
    WHERE name_agg.otx_name LIKE '%' || core_vld.otx_bridge || '%'
      OR name_agg.inx_name LIKE '%' || core_vld.inx_bridge || '%'
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
        "pidgin_road": "road",
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
PIDROAD_INCONSISTENCY_SQLSTR = """SELECT otx_road
FROM pidgin_road_raw
GROUP BY otx_road
HAVING MIN(inx_road) != MAX(inx_road)
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
BUDAWAR_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, road, awardee_title
FROM bud_item_awardlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
"""
BUDFACT_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, road, fbase
FROM bud_item_factunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, fbase
HAVING MIN(fneed) != MAX(fneed)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
"""
BUDHEAL_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, road, healer_name
FROM bud_item_healerlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, healer_name
HAVING 1=2
"""
BUDPREM_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, road, base, need
FROM bud_item_reason_premiseunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, base, need
HAVING MIN(nigh) != MAX(nigh)
    OR MIN(open) != MAX(open)
    OR MIN(divisor) != MAX(divisor)
"""
BUDREAS_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, road, base
FROM bud_item_reasonunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, base
HAVING MIN(base_item_active_requisite) != MAX(base_item_active_requisite)
"""
BUDTEAM_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, road, team_title
FROM bud_item_teamlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, team_title
HAVING 1=2
"""
BUDITEM_INCONSISTENCY_SQLSTR = """SELECT event_int, face_name, fisc_tag, owner_name, road
FROM bud_itemunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road
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
        "pidgin_road": PIDROAD_INCONSISTENCY_SQLSTR,
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
        "bud_item_awardlink": BUDAWAR_INCONSISTENCY_SQLSTR,
        "bud_item_factunit": BUDFACT_INCONSISTENCY_SQLSTR,
        "bud_item_healerlink": BUDHEAL_INCONSISTENCY_SQLSTR,
        "bud_item_reason_premiseunit": BUDPREM_INCONSISTENCY_SQLSTR,
        "bud_item_reasonunit": BUDREAS_INCONSISTENCY_SQLSTR,
        "bud_item_teamlink": BUDTEAM_INCONSISTENCY_SQLSTR,
        "bud_itemunit": BUDITEM_INCONSISTENCY_SQLSTR,
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
PIDROAD_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT otx_road
FROM pidgin_road_raw
GROUP BY otx_road
HAVING MIN(inx_road) != MAX(inx_road)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
)
UPDATE pidgin_road_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.otx_road = pidgin_road_raw.otx_road
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
SELECT event_int, face_name, fisc_tag, owner_name, road, awardee_title
FROM bud_item_awardlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE bud_item_awardlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_item_awardlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_item_awardlink_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_item_awardlink_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_item_awardlink_put_raw.owner_name
    AND inconsistency_rows.road = bud_item_awardlink_put_raw.road
    AND inconsistency_rows.awardee_title = bud_item_awardlink_put_raw.awardee_title
;
"""
BUDFACT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, road, fbase
FROM bud_item_factunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, fbase
HAVING MIN(fneed) != MAX(fneed)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
)
UPDATE bud_item_factunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_item_factunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_item_factunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_item_factunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_item_factunit_put_raw.owner_name
    AND inconsistency_rows.road = bud_item_factunit_put_raw.road
    AND inconsistency_rows.fbase = bud_item_factunit_put_raw.fbase
;
"""
BUDHEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, road, healer_name
FROM bud_item_healerlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, healer_name
HAVING 1=2
)
UPDATE bud_item_healerlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_item_healerlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_item_healerlink_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_item_healerlink_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_item_healerlink_put_raw.owner_name
    AND inconsistency_rows.road = bud_item_healerlink_put_raw.road
    AND inconsistency_rows.healer_name = bud_item_healerlink_put_raw.healer_name
;
"""
BUDPREM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, road, base, need
FROM bud_item_reason_premiseunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, base, need
HAVING MIN(nigh) != MAX(nigh)
    OR MIN(open) != MAX(open)
    OR MIN(divisor) != MAX(divisor)
)
UPDATE bud_item_reason_premiseunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_item_reason_premiseunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_item_reason_premiseunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_item_reason_premiseunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_item_reason_premiseunit_put_raw.owner_name
    AND inconsistency_rows.road = bud_item_reason_premiseunit_put_raw.road
    AND inconsistency_rows.base = bud_item_reason_premiseunit_put_raw.base
    AND inconsistency_rows.need = bud_item_reason_premiseunit_put_raw.need
;
"""
BUDREAS_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, road, base
FROM bud_item_reasonunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, base
HAVING MIN(base_item_active_requisite) != MAX(base_item_active_requisite)
)
UPDATE bud_item_reasonunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_item_reasonunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_item_reasonunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_item_reasonunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_item_reasonunit_put_raw.owner_name
    AND inconsistency_rows.road = bud_item_reasonunit_put_raw.road
    AND inconsistency_rows.base = bud_item_reasonunit_put_raw.base
;
"""
BUDTEAM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, road, team_title
FROM bud_item_teamlink_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, team_title
HAVING 1=2
)
UPDATE bud_item_teamlink_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_item_teamlink_put_raw.event_int
    AND inconsistency_rows.face_name = bud_item_teamlink_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_item_teamlink_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_item_teamlink_put_raw.owner_name
    AND inconsistency_rows.road = bud_item_teamlink_put_raw.road
    AND inconsistency_rows.team_title = bud_item_teamlink_put_raw.team_title
;
"""
BUDITEM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT event_int, face_name, fisc_tag, owner_name, road
FROM bud_itemunit_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road
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
UPDATE bud_itemunit_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_itemunit_put_raw.event_int
    AND inconsistency_rows.face_name = bud_itemunit_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_itemunit_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_itemunit_put_raw.owner_name
    AND inconsistency_rows.road = bud_itemunit_put_raw.road
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
BUDAWAR_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_awardlink_del_agg (event_int, face_name, fisc_tag, owner_name, road, awardee_title_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, road, awardee_title_ERASE
FROM bud_item_awardlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, awardee_title_ERASE
;
"""
BUDFACT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_factunit_del_agg (event_int, face_name, fisc_tag, owner_name, road, fbase_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, road, fbase_ERASE
FROM bud_item_factunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, fbase_ERASE
;
"""
BUDHEAL_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_healerlink_del_agg (event_int, face_name, fisc_tag, owner_name, road, healer_name_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, road, healer_name_ERASE
FROM bud_item_healerlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, healer_name_ERASE
;
"""
BUDPREM_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reason_premiseunit_del_agg (event_int, face_name, fisc_tag, owner_name, road, base, need_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, road, base, need_ERASE
FROM bud_item_reason_premiseunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, base, need_ERASE
;
"""
BUDREAS_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reasonunit_del_agg (event_int, face_name, fisc_tag, owner_name, road, base_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, road, base_ERASE
FROM bud_item_reasonunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, base_ERASE
;
"""
BUDTEAM_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_teamlink_del_agg (event_int, face_name, fisc_tag, owner_name, road, team_title_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, road, team_title_ERASE
FROM bud_item_teamlink_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, team_title_ERASE
;
"""
BUDITEM_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_itemunit_del_agg (event_int, face_name, fisc_tag, owner_name, road_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, road_ERASE
FROM bud_itemunit_del_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road_ERASE
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
        "pidgin_road": PIDROAD_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
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
        "bud_item_awardlink": BUDAWAR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_item_factunit": BUDFACT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_item_healerlink": BUDHEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_item_reason_premiseunit": BUDPREM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_item_reasonunit": BUDREAS_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_item_teamlink": BUDTEAM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "bud_itemunit": BUDITEM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "budunit": BUDUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
    }


def get_sound_pidgin_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    x_dict = {}
    for dimen, sqlstr in get_pidgin_update_inconsist_error_message_sqlstrs().items():
        old_raw_tablename = f"{dimen}_raw"
        new_raw_tablename = f"{dimen}_s_raw"
        x_dict[dimen] = sqlstr.replace(old_raw_tablename, new_raw_tablename)
    return x_dict


def get_sound_fisc_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    x_dict = {}
    for dimen, sqlstr in get_pidgin_update_inconsist_error_message_sqlstrs().items():
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
PIDROAD_AGG_INSERT_SQLSTR = """INSERT INTO pidgin_road_agg (otx_road, inx_road, otx_bridge, inx_bridge, unknown_word)
SELECT otx_road, MAX(inx_road), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_word)
FROM pidgin_road_raw
WHERE error_message IS NULL
GROUP BY otx_road
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
BUDAWAR_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_awardlink_put_agg (event_int, face_name, fisc_tag, owner_name, road, awardee_title, give_force, take_force)
SELECT event_int, face_name, fisc_tag, owner_name, road, awardee_title, MAX(give_force), MAX(take_force)
FROM bud_item_awardlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, awardee_title
;
"""
BUDFACT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_factunit_put_agg (event_int, face_name, fisc_tag, owner_name, road, fbase, fneed, fopen, fnigh)
SELECT event_int, face_name, fisc_tag, owner_name, road, fbase, MAX(fneed), MAX(fopen), MAX(fnigh)
FROM bud_item_factunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, fbase
;
"""
BUDHEAL_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_healerlink_put_agg (event_int, face_name, fisc_tag, owner_name, road, healer_name)
SELECT event_int, face_name, fisc_tag, owner_name, road, healer_name
FROM bud_item_healerlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, healer_name
;
"""
BUDPREM_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reason_premiseunit_put_agg (event_int, face_name, fisc_tag, owner_name, road, base, need, nigh, open, divisor)
SELECT event_int, face_name, fisc_tag, owner_name, road, base, need, MAX(nigh), MAX(open), MAX(divisor)
FROM bud_item_reason_premiseunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, base, need
;
"""
BUDREAS_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reasonunit_put_agg (event_int, face_name, fisc_tag, owner_name, road, base, base_item_active_requisite)
SELECT event_int, face_name, fisc_tag, owner_name, road, base, MAX(base_item_active_requisite)
FROM bud_item_reasonunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, base
;
"""
BUDTEAM_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_teamlink_put_agg (event_int, face_name, fisc_tag, owner_name, road, team_title)
SELECT event_int, face_name, fisc_tag, owner_name, road, team_title
FROM bud_item_teamlink_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, team_title
;
"""
BUDITEM_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_itemunit_put_agg (event_int, face_name, fisc_tag, owner_name, road, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool)
SELECT event_int, face_name, fisc_tag, owner_name, road, MAX(begin), MAX(close), MAX(addin), MAX(numor), MAX(denom), MAX(morph), MAX(gogo_want), MAX(stop_want), MAX(mass), MAX(pledge), MAX(problem_bool)
FROM bud_itemunit_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road
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
        "pidgin_road": PIDROAD_AGG_INSERT_SQLSTR,
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
        "bud_item_awardlink": BUDAWAR_PUT_AGG_INSERT_SQLSTR,
        "bud_item_factunit": BUDFACT_PUT_AGG_INSERT_SQLSTR,
        "bud_item_healerlink": BUDHEAL_PUT_AGG_INSERT_SQLSTR,
        "bud_item_reason_premiseunit": BUDPREM_PUT_AGG_INSERT_SQLSTR,
        "bud_item_reasonunit": BUDREAS_PUT_AGG_INSERT_SQLSTR,
        "bud_item_teamlink": BUDTEAM_PUT_AGG_INSERT_SQLSTR,
        "bud_itemunit": BUDITEM_PUT_AGG_INSERT_SQLSTR,
        "budunit": BUDUNIT_PUT_AGG_INSERT_SQLSTR,
    }


def get_bud_insert_del_agg_from_raw_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership": BUDMEMB_DEL_AGG_INSERT_SQLSTR,
        "bud_acctunit": BUDACCT_DEL_AGG_INSERT_SQLSTR,
        "bud_item_awardlink": BUDAWAR_DEL_AGG_INSERT_SQLSTR,
        "bud_item_factunit": BUDFACT_DEL_AGG_INSERT_SQLSTR,
        "bud_item_healerlink": BUDHEAL_DEL_AGG_INSERT_SQLSTR,
        "bud_item_reason_premiseunit": BUDPREM_DEL_AGG_INSERT_SQLSTR,
        "bud_item_reasonunit": BUDREAS_DEL_AGG_INSERT_SQLSTR,
        "bud_item_teamlink": BUDTEAM_DEL_AGG_INSERT_SQLSTR,
        "bud_itemunit": BUDITEM_DEL_AGG_INSERT_SQLSTR,
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
        "br00013": ["bud_itemunit", "budunit", "fiscunit"],
        "br00019": ["bud_itemunit", "budunit", "fiscunit"],
        "br00020": ["bud_acct_membership", "bud_acctunit", "budunit", "fiscunit"],
        "br00021": ["bud_acctunit", "budunit", "fiscunit"],
        "br00022": ["bud_item_awardlink", "bud_itemunit", "budunit", "fiscunit"],
        "br00023": ["bud_item_factunit", "bud_itemunit", "budunit", "fiscunit"],
        "br00024": ["bud_item_teamlink", "bud_itemunit", "budunit", "fiscunit"],
        "br00025": ["bud_item_healerlink", "bud_itemunit", "budunit", "fiscunit"],
        "br00026": [
            "bud_item_reason_premiseunit",
            "bud_item_reasonunit",
            "bud_itemunit",
            "budunit",
            "fiscunit",
        ],
        "br00027": ["bud_item_reasonunit", "bud_itemunit", "budunit", "fiscunit"],
        "br00028": ["bud_itemunit", "budunit", "fiscunit"],
        "br00029": ["budunit", "fiscunit"],
        "br00036": ["bud_item_healerlink", "bud_itemunit", "budunit", "fiscunit"],
        "br00042": [],
        "br00043": [],
        "br00044": [],
        "br00045": [],
        "br00050": ["bud_acctunit", "budunit", "fiscunit"],
        "br00051": ["budunit", "fiscunit"],
        "br00052": ["bud_itemunit", "budunit", "fiscunit"],
        "br00053": ["bud_itemunit", "budunit", "fiscunit"],
        "br00054": ["bud_itemunit", "budunit", "fiscunit"],
        "br00055": ["bud_itemunit", "budunit", "fiscunit"],
        "br00056": ["bud_item_reasonunit", "bud_itemunit", "budunit", "fiscunit"],
        "br00057": ["bud_itemunit", "budunit", "fiscunit"],
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
    "br00052": ["bud_item_awardlink"],
    "br00053": ["bud_item_factunit"],
    "br00054": ["bud_item_teamlink"],
    "br00055": ["bud_item_healerlink"],
    "br00056": ["bud_item_reason_premiseunit"],
    "br00057": ["bud_item_reasonunit"],
    "br00058": ["bud_itemunit"],
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
