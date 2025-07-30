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
    "BLFPAYY",
    "BLFBUDD",
    "BLFHOUR",
    "BLFMONT",
    "BLFWEEK",
    "BLFOFFI",
    "BLFUNIT",
    "BLRMEMB",
    "BLRPERN",
    "BLRAWAR",
    "BLRFACT",
    "BLRHEAL",
    "BLRPREM",
    "BLRREAS",
    "BLRLABO",
    "BLRPLAN",
    "BLRUNIT",
    "PIDTITL",
    "PIDNAME",
    "PIDROPE",
    "PIDLABE",
}


def get_dimen_abbv7(dimen: str) -> str:
    return {
        "belief_paybook": "BLFPAYY",
        "belief_budunit": "BLFBUDD",
        "belief_timeline_hour": "BLFHOUR",
        "belief_timeline_month": "BLFMONT",
        "belief_timeline_weekday": "BLFWEEK",
        "belief_timeoffi": "BLFOFFI",
        "beliefunit": "BLFUNIT",
        "believer_partner_membership": "BLRMEMB",
        "believer_partnerunit": "BLRPERN",
        "believer_plan_awardlink": "BLRAWAR",
        "believer_plan_factunit": "BLRFACT",
        "believer_plan_healerlink": "BLRHEAL",
        "believer_plan_reason_caseunit": "BLRPREM",
        "believer_plan_reasonunit": "BLRREAS",
        "believer_plan_laborlink": "BLRLABO",
        "believer_planunit": "BLRPLAN",
        "believerunit": "BLRUNIT",
        "pidgin_title": "PIDTITL",
        "pidgin_name": "PIDNAME",
        "pidgin_rope": "PIDROPE",
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
        "BLFPAYY": "belief_paybook",
        "BLFBUDD": "belief_budunit",
        "BLFHOUR": "belief_timeline_hour",
        "BLFMONT": "belief_timeline_month",
        "BLFWEEK": "belief_timeline_weekday",
        "BLFOFFI": "belief_timeoffi",
        "BLFUNIT": "beliefunit",
        "BLRMEMB": "believer_partner_membership",
        "BLRPERN": "believer_partnerunit",
        "BLRAWAR": "believer_plan_awardlink",
        "BLRFACT": "believer_plan_factunit",
        "BLRGROU": "believer_groupunit",
        "BLRHEAL": "believer_plan_healerlink",
        "BLRPREM": "believer_plan_reason_caseunit",
        "BLRREAS": "believer_plan_reasonunit",
        "BLRLABO": "believer_plan_laborlink",
        "BLRPLAN": "believer_planunit",
        "BLRUNIT": "believerunit",
        "PIDTITL": "pidgin_title",
        "PIDNAME": "pidgin_name",
        "PIDROPE": "pidgin_rope",
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


CREATE_PIDTITL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDTITL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_agg (event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDTITL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_title_s_vld (event_int INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT)"""
CREATE_PIDNAME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_agg (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDNAME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_name_s_vld (event_int INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT)"""
CREATE_PIDROPE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_rope_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDROPE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_rope_s_agg (event_int INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDROPE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_rope_s_vld (event_int INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT)"""
CREATE_PIDLABE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_agg (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDLABE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_label_s_vld (event_int INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT)"""

CREATE_PIDCORE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_raw (source_dimen TEXT, face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_PIDCORE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_agg (face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT)"""
CREATE_PIDCORE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS pidgin_core_s_vld (face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT)"""

CREATE_BLFPAYY_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_paybook_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_BLFPAYY_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_paybook_s_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_BLFPAYY_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_paybook_s_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_BLFPAYY_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_paybook_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, partner_name_otx TEXT, partner_name_inx TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_BLFPAYY_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_paybook_v_agg (belief_label TEXT, believer_name TEXT, partner_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_BLFBUDD_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_budunit_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_BLFBUDD_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_budunit_s_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_BLFBUDD_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_budunit_s_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER)"""
CREATE_BLFBUDD_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_budunit_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_BLFBUDD_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_budunit_v_agg (belief_label TEXT, believer_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER)"""
CREATE_BLFHOUR_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_hour_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, cumulative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_BLFHOUR_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_hour_s_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, cumulative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_BLFHOUR_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_hour_s_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, cumulative_minute INTEGER, hour_label TEXT)"""
CREATE_BLFHOUR_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_hour_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, cumulative_minute INTEGER, hour_label_otx TEXT, hour_label_inx TEXT, error_message TEXT)"""
CREATE_BLFHOUR_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_hour_v_agg (belief_label TEXT, cumulative_minute INTEGER, hour_label TEXT)"""
CREATE_BLFMONT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_month_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, cumulative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_BLFMONT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_month_s_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, cumulative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_BLFMONT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_month_s_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, cumulative_day INTEGER, month_label TEXT)"""
CREATE_BLFMONT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_month_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, cumulative_day INTEGER, month_label_otx TEXT, month_label_inx TEXT, error_message TEXT)"""
CREATE_BLFMONT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_month_v_agg (belief_label TEXT, cumulative_day INTEGER, month_label TEXT)"""
CREATE_BLFWEEK_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_weekday_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_BLFWEEK_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_weekday_s_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_BLFWEEK_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_weekday_s_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_BLFWEEK_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_weekday_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, weekday_order INTEGER, weekday_label_otx TEXT, weekday_label_inx TEXT, error_message TEXT)"""
CREATE_BLFWEEK_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeline_weekday_v_agg (belief_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_BLFOFFI_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeoffi_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_BLFOFFI_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeoffi_s_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_BLFOFFI_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeoffi_s_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, offi_time INTEGER)"""
CREATE_BLFOFFI_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeoffi_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_BLFOFFI_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_timeoffi_v_agg (belief_label TEXT, offi_time INTEGER)"""
CREATE_BLFUNIT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS beliefunit_s_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_BLFUNIT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS beliefunit_s_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_BLFUNIT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS beliefunit_s_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, knot TEXT, job_listen_rotations INTEGER)"""
CREATE_BLFUNIT_VOICE_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS beliefunit_v_raw (event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, timeline_label_otx TEXT, timeline_label_inx TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_BLFUNIT_VOICE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS beliefunit_v_agg (belief_label TEXT, timeline_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, knot TEXT, job_listen_rotations INTEGER)"""

CREATE_BLRMEMB_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title TEXT, group_cred_points REAL, group_debt_points REAL, error_message TEXT)"
CREATE_BLRMEMB_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title TEXT, group_cred_points REAL, group_debt_points REAL, error_message TEXT)"
CREATE_BLRMEMB_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title TEXT, group_cred_points REAL, group_debt_points REAL)"
CREATE_BLRMEMB_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title_ERASE TEXT)"
CREATE_BLRMEMB_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title_ERASE TEXT, error_message TEXT)"
CREATE_BLRMEMB_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title_ERASE TEXT)"
CREATE_BLRMEMB_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, partner_name_otx TEXT, partner_name_inx TEXT, group_title_otx TEXT, group_title_inx TEXT, group_cred_points REAL, group_debt_points REAL)"
CREATE_BLRMEMB_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title TEXT, group_cred_points REAL, group_debt_points REAL)"
CREATE_BLRMEMB_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, partner_name_otx TEXT, partner_name_inx TEXT, group_title_ERASE_otx TEXT, group_title_ERASE_inx TEXT)"
CREATE_BLRMEMB_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_partner_membership_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title_ERASE TEXT)"
CREATE_BLRPERN_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, partner_cred_points REAL, partner_debt_points REAL, error_message TEXT)"
CREATE_BLRPERN_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, partner_cred_points REAL, partner_debt_points REAL, error_message TEXT)"
CREATE_BLRPERN_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, partner_cred_points REAL, partner_debt_points REAL)"
CREATE_BLRPERN_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name_ERASE TEXT)"
CREATE_BLRPERN_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name_ERASE TEXT, error_message TEXT)"
CREATE_BLRPERN_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name_ERASE TEXT)"
CREATE_BLRPERN_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, partner_name_otx TEXT, partner_name_inx TEXT, partner_cred_points REAL, partner_debt_points REAL)"
CREATE_BLRPERN_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name TEXT, partner_cred_points REAL, partner_debt_points REAL)"
CREATE_BLRPERN_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, partner_name_ERASE_otx TEXT, partner_name_ERASE_inx TEXT)"
CREATE_BLRPERN_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_partnerunit_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, partner_name_ERASE TEXT)"
CREATE_BLRAWAR_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_BLRAWAR_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_BLRAWAR_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BLRAWAR_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"
CREATE_BLRAWAR_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT, error_message TEXT)"
CREATE_BLRAWAR_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"
CREATE_BLRAWAR_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, awardee_title_otx TEXT, awardee_title_inx TEXT, give_force REAL, take_force REAL)"
CREATE_BLRAWAR_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BLRAWAR_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, awardee_title_ERASE_otx TEXT, awardee_title_ERASE_inx TEXT)"
CREATE_BLRAWAR_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_awardlink_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"
CREATE_BLRFACT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, error_message TEXT)"
CREATE_BLRFACT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, error_message TEXT)"
CREATE_BLRFACT_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"
CREATE_BLRFACT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"
CREATE_BLRFACT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT, error_message TEXT)"
CREATE_BLRFACT_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"
CREATE_BLRFACT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, fact_context_otx TEXT, fact_context_inx TEXT, fact_state_otx TEXT, fact_state_inx TEXT, fact_lower REAL, fact_upper REAL)"
CREATE_BLRFACT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"
CREATE_BLRFACT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, fact_context_ERASE_otx TEXT, fact_context_ERASE_inx TEXT)"
CREATE_BLRFACT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_factunit_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"
CREATE_BLRHEAL_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name TEXT, error_message TEXT)"
CREATE_BLRHEAL_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name TEXT, error_message TEXT)"
CREATE_BLRHEAL_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name TEXT)"
CREATE_BLRHEAL_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"
CREATE_BLRHEAL_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT, error_message TEXT)"
CREATE_BLRHEAL_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"
CREATE_BLRHEAL_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, healer_name_otx TEXT, healer_name_inx TEXT)"
CREATE_BLRHEAL_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name TEXT)"
CREATE_BLRHEAL_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, healer_name_ERASE_otx TEXT, healer_name_ERASE_inx TEXT)"
CREATE_BLRHEAL_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_healerlink_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"
CREATE_BLRPREM_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER, error_message TEXT)"
CREATE_BLRPREM_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER, error_message TEXT)"
CREATE_BLRPREM_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER)"
CREATE_BLRPREM_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"
CREATE_BLRPREM_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT, error_message TEXT)"
CREATE_BLRPREM_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"
CREATE_BLRPREM_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_state_otx TEXT, reason_state_inx TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER)"
CREATE_BLRPREM_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER)"
CREATE_BLRPREM_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_state_ERASE_otx TEXT, reason_state_ERASE_inx TEXT)"
CREATE_BLRPREM_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"
CREATE_BLRREAS_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_active_requisite INTEGER, error_message TEXT)"
CREATE_BLRREAS_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_active_requisite INTEGER, error_message TEXT)"
CREATE_BLRREAS_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_active_requisite INTEGER)"
CREATE_BLRREAS_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"
CREATE_BLRREAS_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT, error_message TEXT)"
CREATE_BLRREAS_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"
CREATE_BLRREAS_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_active_requisite INTEGER)"
CREATE_BLRREAS_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_active_requisite INTEGER)"
CREATE_BLRREAS_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_ERASE_otx TEXT, reason_context_ERASE_inx TEXT)"
CREATE_BLRREAS_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"
CREATE_BLRLABO_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title TEXT, error_message TEXT)"
CREATE_BLRLABO_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title TEXT, error_message TEXT)"
CREATE_BLRLABO_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title TEXT)"
CREATE_BLRLABO_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT)"
CREATE_BLRLABO_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT, error_message TEXT)"
CREATE_BLRLABO_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT)"
CREATE_BLRLABO_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, labor_title_otx TEXT, labor_title_inx TEXT)"
CREATE_BLRLABO_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title TEXT)"
CREATE_BLRLABO_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, labor_title_ERASE_otx TEXT, labor_title_ERASE_inx TEXT)"
CREATE_BLRLABO_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_plan_laborlink_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title_ERASE TEXT)"
CREATE_BLRPLAN_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, task INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_BLRPLAN_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, task INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_BLRPLAN_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, task INTEGER, problem_bool INTEGER)"
CREATE_BLRPLAN_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope_ERASE TEXT)"
CREATE_BLRPLAN_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope_ERASE TEXT, error_message TEXT)"
CREATE_BLRPLAN_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope_ERASE TEXT)"
CREATE_BLRPLAN_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, task INTEGER, problem_bool INTEGER)"
CREATE_BLRPLAN_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, task INTEGER, problem_bool INTEGER)"
CREATE_BLRPLAN_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, plan_rope_ERASE_otx TEXT, plan_rope_ERASE_inx TEXT)"
CREATE_BLRPLAN_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believer_planunit_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, plan_rope_ERASE TEXT)"
CREATE_BLRUNIT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believerunit_s_put_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, error_message TEXT)"
CREATE_BLRUNIT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believerunit_s_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, error_message TEXT)"
CREATE_BLRUNIT_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS believerunit_s_put_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL)"
CREATE_BLRUNIT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believerunit_s_del_raw (idea_number TEXT, event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name_ERASE TEXT)"
CREATE_BLRUNIT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believerunit_s_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name_ERASE TEXT, error_message TEXT)"
CREATE_BLRUNIT_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS believerunit_s_del_vld (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name_ERASE TEXT)"
CREATE_BLRUNIT_VOICE_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS believerunit_v_put_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_otx TEXT, believer_name_inx TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL)"
CREATE_BLRUNIT_VOICE_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS believerunit_v_put_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL)"
CREATE_BLRUNIT_VOICE_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS believerunit_v_del_raw (pidgin_event_int INTEGER, event_int INTEGER, face_name_otx TEXT, face_name_inx TEXT, belief_label_otx TEXT, belief_label_inx TEXT, believer_name_ERASE_otx TEXT, believer_name_ERASE_inx TEXT)"
CREATE_BLRUNIT_VOICE_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS believerunit_v_del_agg (event_int INTEGER, face_name TEXT, belief_label TEXT, believer_name_ERASE TEXT)"


def get_prime_create_table_sqlstrs() -> dict[str:str]:
    return {
        "pidgin_title_s_raw": CREATE_PIDTITL_SOUND_RAW_SQLSTR,
        "pidgin_title_s_agg": CREATE_PIDTITL_SOUND_AGG_SQLSTR,
        "pidgin_title_s_vld": CREATE_PIDTITL_SOUND_VLD_SQLSTR,
        "pidgin_name_s_raw": CREATE_PIDNAME_SOUND_RAW_SQLSTR,
        "pidgin_name_s_agg": CREATE_PIDNAME_SOUND_AGG_SQLSTR,
        "pidgin_name_s_vld": CREATE_PIDNAME_SOUND_VLD_SQLSTR,
        "pidgin_rope_s_raw": CREATE_PIDROPE_SOUND_RAW_SQLSTR,
        "pidgin_rope_s_agg": CREATE_PIDROPE_SOUND_AGG_SQLSTR,
        "pidgin_rope_s_vld": CREATE_PIDROPE_SOUND_VLD_SQLSTR,
        "pidgin_label_s_raw": CREATE_PIDLABE_SOUND_RAW_SQLSTR,
        "pidgin_label_s_agg": CREATE_PIDLABE_SOUND_AGG_SQLSTR,
        "pidgin_label_s_vld": CREATE_PIDLABE_SOUND_VLD_SQLSTR,
        "pidgin_core_s_raw": CREATE_PIDCORE_SOUND_RAW_SQLSTR,
        "pidgin_core_s_agg": CREATE_PIDCORE_SOUND_AGG_SQLSTR,
        "pidgin_core_s_vld": CREATE_PIDCORE_SOUND_VLD_SQLSTR,
        "belief_paybook_s_raw": CREATE_BLFPAYY_SOUND_RAW_SQLSTR,
        "belief_paybook_s_agg": CREATE_BLFPAYY_SOUND_AGG_SQLSTR,
        "belief_paybook_s_vld": CREATE_BLFPAYY_SOUND_VLD_SQLSTR,
        "belief_paybook_v_raw": CREATE_BLFPAYY_VOICE_RAW_SQLSTR,
        "belief_paybook_v_agg": CREATE_BLFPAYY_VOICE_AGG_SQLSTR,
        "belief_budunit_s_raw": CREATE_BLFBUDD_SOUND_RAW_SQLSTR,
        "belief_budunit_s_agg": CREATE_BLFBUDD_SOUND_AGG_SQLSTR,
        "belief_budunit_s_vld": CREATE_BLFBUDD_SOUND_VLD_SQLSTR,
        "belief_budunit_v_raw": CREATE_BLFBUDD_VOICE_RAW_SQLSTR,
        "belief_budunit_v_agg": CREATE_BLFBUDD_VOICE_AGG_SQLSTR,
        "belief_timeline_hour_s_raw": CREATE_BLFHOUR_SOUND_RAW_SQLSTR,
        "belief_timeline_hour_s_agg": CREATE_BLFHOUR_SOUND_AGG_SQLSTR,
        "belief_timeline_hour_s_vld": CREATE_BLFHOUR_SOUND_VLD_SQLSTR,
        "belief_timeline_hour_v_raw": CREATE_BLFHOUR_VOICE_RAW_SQLSTR,
        "belief_timeline_hour_v_agg": CREATE_BLFHOUR_VOICE_AGG_SQLSTR,
        "belief_timeline_month_s_raw": CREATE_BLFMONT_SOUND_RAW_SQLSTR,
        "belief_timeline_month_s_agg": CREATE_BLFMONT_SOUND_AGG_SQLSTR,
        "belief_timeline_month_s_vld": CREATE_BLFMONT_SOUND_VLD_SQLSTR,
        "belief_timeline_month_v_raw": CREATE_BLFMONT_VOICE_RAW_SQLSTR,
        "belief_timeline_month_v_agg": CREATE_BLFMONT_VOICE_AGG_SQLSTR,
        "belief_timeline_weekday_s_raw": CREATE_BLFWEEK_SOUND_RAW_SQLSTR,
        "belief_timeline_weekday_s_agg": CREATE_BLFWEEK_SOUND_AGG_SQLSTR,
        "belief_timeline_weekday_s_vld": CREATE_BLFWEEK_SOUND_VLD_SQLSTR,
        "belief_timeline_weekday_v_raw": CREATE_BLFWEEK_VOICE_RAW_SQLSTR,
        "belief_timeline_weekday_v_agg": CREATE_BLFWEEK_VOICE_AGG_SQLSTR,
        "belief_timeoffi_s_raw": CREATE_BLFOFFI_SOUND_RAW_SQLSTR,
        "belief_timeoffi_s_agg": CREATE_BLFOFFI_SOUND_AGG_SQLSTR,
        "belief_timeoffi_s_vld": CREATE_BLFOFFI_SOUND_VLD_SQLSTR,
        "belief_timeoffi_v_raw": CREATE_BLFOFFI_VOICE_RAW_SQLSTR,
        "belief_timeoffi_v_agg": CREATE_BLFOFFI_VOICE_AGG_SQLSTR,
        "beliefunit_s_raw": CREATE_BLFUNIT_SOUND_RAW_SQLSTR,
        "beliefunit_s_agg": CREATE_BLFUNIT_SOUND_AGG_SQLSTR,
        "beliefunit_s_vld": CREATE_BLFUNIT_SOUND_VLD_SQLSTR,
        "beliefunit_v_raw": CREATE_BLFUNIT_VOICE_RAW_SQLSTR,
        "beliefunit_v_agg": CREATE_BLFUNIT_VOICE_AGG_SQLSTR,
        "believer_partner_membership_s_put_raw": CREATE_BLRMEMB_SOUND_PUT_RAW_STR,
        "believer_partner_membership_s_put_agg": CREATE_BLRMEMB_SOUND_PUT_AGG_STR,
        "believer_partner_membership_s_put_vld": CREATE_BLRMEMB_SOUND_PUT_VLD_STR,
        "believer_partner_membership_s_del_raw": CREATE_BLRMEMB_SOUND_DEL_RAW_STR,
        "believer_partner_membership_s_del_agg": CREATE_BLRMEMB_SOUND_DEL_AGG_STR,
        "believer_partner_membership_s_del_vld": CREATE_BLRMEMB_SOUND_DEL_VLD_STR,
        "believer_partner_membership_v_put_raw": CREATE_BLRMEMB_VOICE_PUT_RAW_STR,
        "believer_partner_membership_v_put_agg": CREATE_BLRMEMB_VOICE_PUT_AGG_STR,
        "believer_partner_membership_v_del_raw": CREATE_BLRMEMB_VOICE_DEL_RAW_STR,
        "believer_partner_membership_v_del_agg": CREATE_BLRMEMB_VOICE_DEL_AGG_STR,
        "believer_partnerunit_s_put_raw": CREATE_BLRPERN_SOUND_PUT_RAW_STR,
        "believer_partnerunit_s_put_agg": CREATE_BLRPERN_SOUND_PUT_AGG_STR,
        "believer_partnerunit_s_put_vld": CREATE_BLRPERN_SOUND_PUT_VLD_STR,
        "believer_partnerunit_s_del_raw": CREATE_BLRPERN_SOUND_DEL_RAW_STR,
        "believer_partnerunit_s_del_agg": CREATE_BLRPERN_SOUND_DEL_AGG_STR,
        "believer_partnerunit_s_del_vld": CREATE_BLRPERN_SOUND_DEL_VLD_STR,
        "believer_partnerunit_v_put_raw": CREATE_BLRPERN_VOICE_PUT_RAW_STR,
        "believer_partnerunit_v_put_agg": CREATE_BLRPERN_VOICE_PUT_AGG_STR,
        "believer_partnerunit_v_del_raw": CREATE_BLRPERN_VOICE_DEL_RAW_STR,
        "believer_partnerunit_v_del_agg": CREATE_BLRPERN_VOICE_DEL_AGG_STR,
        "believer_plan_awardlink_s_put_raw": CREATE_BLRAWAR_SOUND_PUT_RAW_STR,
        "believer_plan_awardlink_s_put_agg": CREATE_BLRAWAR_SOUND_PUT_AGG_STR,
        "believer_plan_awardlink_s_put_vld": CREATE_BLRAWAR_SOUND_PUT_VLD_STR,
        "believer_plan_awardlink_s_del_raw": CREATE_BLRAWAR_SOUND_DEL_RAW_STR,
        "believer_plan_awardlink_s_del_agg": CREATE_BLRAWAR_SOUND_DEL_AGG_STR,
        "believer_plan_awardlink_s_del_vld": CREATE_BLRAWAR_SOUND_DEL_VLD_STR,
        "believer_plan_awardlink_v_put_raw": CREATE_BLRAWAR_VOICE_PUT_RAW_STR,
        "believer_plan_awardlink_v_put_agg": CREATE_BLRAWAR_VOICE_PUT_AGG_STR,
        "believer_plan_awardlink_v_del_raw": CREATE_BLRAWAR_VOICE_DEL_RAW_STR,
        "believer_plan_awardlink_v_del_agg": CREATE_BLRAWAR_VOICE_DEL_AGG_STR,
        "believer_plan_factunit_s_put_raw": CREATE_BLRFACT_SOUND_PUT_RAW_STR,
        "believer_plan_factunit_s_put_agg": CREATE_BLRFACT_SOUND_PUT_AGG_STR,
        "believer_plan_factunit_s_put_vld": CREATE_BLRFACT_SOUND_PUT_VLD_STR,
        "believer_plan_factunit_s_del_raw": CREATE_BLRFACT_SOUND_DEL_RAW_STR,
        "believer_plan_factunit_s_del_agg": CREATE_BLRFACT_SOUND_DEL_AGG_STR,
        "believer_plan_factunit_s_del_vld": CREATE_BLRFACT_SOUND_DEL_VLD_STR,
        "believer_plan_factunit_v_put_raw": CREATE_BLRFACT_VOICE_PUT_RAW_STR,
        "believer_plan_factunit_v_put_agg": CREATE_BLRFACT_VOICE_PUT_AGG_STR,
        "believer_plan_factunit_v_del_raw": CREATE_BLRFACT_VOICE_DEL_RAW_STR,
        "believer_plan_factunit_v_del_agg": CREATE_BLRFACT_VOICE_DEL_AGG_STR,
        "believer_plan_healerlink_s_put_raw": CREATE_BLRHEAL_SOUND_PUT_RAW_STR,
        "believer_plan_healerlink_s_put_agg": CREATE_BLRHEAL_SOUND_PUT_AGG_STR,
        "believer_plan_healerlink_s_put_vld": CREATE_BLRHEAL_SOUND_PUT_VLD_STR,
        "believer_plan_healerlink_s_del_raw": CREATE_BLRHEAL_SOUND_DEL_RAW_STR,
        "believer_plan_healerlink_s_del_agg": CREATE_BLRHEAL_SOUND_DEL_AGG_STR,
        "believer_plan_healerlink_s_del_vld": CREATE_BLRHEAL_SOUND_DEL_VLD_STR,
        "believer_plan_healerlink_v_put_raw": CREATE_BLRHEAL_VOICE_PUT_RAW_STR,
        "believer_plan_healerlink_v_put_agg": CREATE_BLRHEAL_VOICE_PUT_AGG_STR,
        "believer_plan_healerlink_v_del_raw": CREATE_BLRHEAL_VOICE_DEL_RAW_STR,
        "believer_plan_healerlink_v_del_agg": CREATE_BLRHEAL_VOICE_DEL_AGG_STR,
        "believer_plan_reason_caseunit_s_put_raw": CREATE_BLRPREM_SOUND_PUT_RAW_STR,
        "believer_plan_reason_caseunit_s_put_agg": CREATE_BLRPREM_SOUND_PUT_AGG_STR,
        "believer_plan_reason_caseunit_s_put_vld": CREATE_BLRPREM_SOUND_PUT_VLD_STR,
        "believer_plan_reason_caseunit_s_del_raw": CREATE_BLRPREM_SOUND_DEL_RAW_STR,
        "believer_plan_reason_caseunit_s_del_agg": CREATE_BLRPREM_SOUND_DEL_AGG_STR,
        "believer_plan_reason_caseunit_s_del_vld": CREATE_BLRPREM_SOUND_DEL_VLD_STR,
        "believer_plan_reason_caseunit_v_put_raw": CREATE_BLRPREM_VOICE_PUT_RAW_STR,
        "believer_plan_reason_caseunit_v_put_agg": CREATE_BLRPREM_VOICE_PUT_AGG_STR,
        "believer_plan_reason_caseunit_v_del_raw": CREATE_BLRPREM_VOICE_DEL_RAW_STR,
        "believer_plan_reason_caseunit_v_del_agg": CREATE_BLRPREM_VOICE_DEL_AGG_STR,
        "believer_plan_reasonunit_s_put_raw": CREATE_BLRREAS_SOUND_PUT_RAW_STR,
        "believer_plan_reasonunit_s_put_agg": CREATE_BLRREAS_SOUND_PUT_AGG_STR,
        "believer_plan_reasonunit_s_put_vld": CREATE_BLRREAS_SOUND_PUT_VLD_STR,
        "believer_plan_reasonunit_s_del_raw": CREATE_BLRREAS_SOUND_DEL_RAW_STR,
        "believer_plan_reasonunit_s_del_agg": CREATE_BLRREAS_SOUND_DEL_AGG_STR,
        "believer_plan_reasonunit_s_del_vld": CREATE_BLRREAS_SOUND_DEL_VLD_STR,
        "believer_plan_reasonunit_v_put_raw": CREATE_BLRREAS_VOICE_PUT_RAW_STR,
        "believer_plan_reasonunit_v_put_agg": CREATE_BLRREAS_VOICE_PUT_AGG_STR,
        "believer_plan_reasonunit_v_del_raw": CREATE_BLRREAS_VOICE_DEL_RAW_STR,
        "believer_plan_reasonunit_v_del_agg": CREATE_BLRREAS_VOICE_DEL_AGG_STR,
        "believer_plan_laborlink_s_put_raw": CREATE_BLRLABO_SOUND_PUT_RAW_STR,
        "believer_plan_laborlink_s_put_agg": CREATE_BLRLABO_SOUND_PUT_AGG_STR,
        "believer_plan_laborlink_s_put_vld": CREATE_BLRLABO_SOUND_PUT_VLD_STR,
        "believer_plan_laborlink_s_del_raw": CREATE_BLRLABO_SOUND_DEL_RAW_STR,
        "believer_plan_laborlink_s_del_agg": CREATE_BLRLABO_SOUND_DEL_AGG_STR,
        "believer_plan_laborlink_s_del_vld": CREATE_BLRLABO_SOUND_DEL_VLD_STR,
        "believer_plan_laborlink_v_put_raw": CREATE_BLRLABO_VOICE_PUT_RAW_STR,
        "believer_plan_laborlink_v_put_agg": CREATE_BLRLABO_VOICE_PUT_AGG_STR,
        "believer_plan_laborlink_v_del_raw": CREATE_BLRLABO_VOICE_DEL_RAW_STR,
        "believer_plan_laborlink_v_del_agg": CREATE_BLRLABO_VOICE_DEL_AGG_STR,
        "believer_planunit_s_put_raw": CREATE_BLRPLAN_SOUND_PUT_RAW_STR,
        "believer_planunit_s_put_agg": CREATE_BLRPLAN_SOUND_PUT_AGG_STR,
        "believer_planunit_s_put_vld": CREATE_BLRPLAN_SOUND_PUT_VLD_STR,
        "believer_planunit_s_del_raw": CREATE_BLRPLAN_SOUND_DEL_RAW_STR,
        "believer_planunit_s_del_agg": CREATE_BLRPLAN_SOUND_DEL_AGG_STR,
        "believer_planunit_s_del_vld": CREATE_BLRPLAN_SOUND_DEL_VLD_STR,
        "believer_planunit_v_put_raw": CREATE_BLRPLAN_VOICE_PUT_RAW_STR,
        "believer_planunit_v_put_agg": CREATE_BLRPLAN_VOICE_PUT_AGG_STR,
        "believer_planunit_v_del_raw": CREATE_BLRPLAN_VOICE_DEL_RAW_STR,
        "believer_planunit_v_del_agg": CREATE_BLRPLAN_VOICE_DEL_AGG_STR,
        "believerunit_s_put_raw": CREATE_BLRUNIT_SOUND_PUT_RAW_STR,
        "believerunit_s_put_agg": CREATE_BLRUNIT_SOUND_PUT_AGG_STR,
        "believerunit_s_put_vld": CREATE_BLRUNIT_SOUND_PUT_VLD_STR,
        "believerunit_s_del_raw": CREATE_BLRUNIT_SOUND_DEL_RAW_STR,
        "believerunit_s_del_agg": CREATE_BLRUNIT_SOUND_DEL_AGG_STR,
        "believerunit_s_del_vld": CREATE_BLRUNIT_SOUND_DEL_VLD_STR,
        "believerunit_v_put_raw": CREATE_BLRUNIT_VOICE_PUT_RAW_STR,
        "believerunit_v_put_agg": CREATE_BLRUNIT_VOICE_PUT_AGG_STR,
        "believerunit_v_del_raw": CREATE_BLRUNIT_VOICE_DEL_RAW_STR,
        "believerunit_v_del_agg": CREATE_BLRUNIT_VOICE_DEL_AGG_STR,
    }


def get_belief_believer_sound_agg_tablenames():
    return {
        "believer_partner_membership_s_del_agg",
        "believer_partner_membership_s_put_agg",
        "believer_partnerunit_s_del_agg",
        "believer_partnerunit_s_put_agg",
        "believer_plan_awardlink_s_del_agg",
        "believer_plan_awardlink_s_put_agg",
        "believer_plan_factunit_s_del_agg",
        "believer_plan_factunit_s_put_agg",
        "believer_plan_healerlink_s_del_agg",
        "believer_plan_healerlink_s_put_agg",
        "believer_plan_laborlink_s_del_agg",
        "believer_plan_laborlink_s_put_agg",
        "believer_plan_reason_caseunit_s_del_agg",
        "believer_plan_reason_caseunit_s_put_agg",
        "believer_plan_reasonunit_s_del_agg",
        "believer_plan_reasonunit_s_put_agg",
        "believer_planunit_s_del_agg",
        "believer_planunit_s_put_agg",
        "believerunit_s_del_agg",
        "believerunit_s_put_agg",
        "belief_paybook_s_agg",
        "belief_budunit_s_agg",
        "belief_timeline_hour_s_agg",
        "belief_timeline_month_s_agg",
        "belief_timeline_weekday_s_agg",
        "belief_timeoffi_s_agg",
        "beliefunit_s_agg",
    }


def get_believer_voice_agg_tablenames() -> set[str]:
    return {
        "believerunit_v_put_agg",
        "believer_plan_healerlink_v_put_agg",
        "believer_partnerunit_v_put_agg",
        "believer_plan_reason_caseunit_v_put_agg",
        "believer_plan_laborlink_v_put_agg",
        "believer_plan_reasonunit_v_put_agg",
        "believer_plan_factunit_v_put_agg",
        "believer_partner_membership_v_put_agg",
        "believer_planunit_v_put_agg",
        "believer_plan_awardlink_v_put_agg",
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
    if dimen.lower().startswith("belief"):
        exclude_cols = {"idea_number", "event_int", "face_name", "error_message"}
    else:
        exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("believer"):
        x_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        x_tablename = create_prime_tablename(dimen, "s", "raw")
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())
    return create_update_inconsistency_error_query(
        conn_or_cursor=conn_or_cursor,
        x_tablename=x_tablename,
        focus_columns=dimen_focus_columns,
        exclude_columns=exclude_cols,
        error_holder_column="error_message",
        error_str="Inconsistent data",
    )


def create_sound_agg_insert_sqlstrs(
    conn_or_cursor: sqlite3_Connection, dimen: str
) -> str:
    dimen_config = get_idea_config_dict().get(dimen)
    dimen_focus_columns = set(dimen_config.get("jkeys").keys())

    if dimen.lower().startswith("belief"):
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("believer"):
        agg_tablename = create_prime_tablename(dimen, "s", "agg", "put")
        raw_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        raw_tablename = create_prime_tablename(dimen, "s", "raw")
        agg_tablename = create_prime_tablename(dimen, "s", "agg")

    pidgin_belief_believer_put_sqlstr = create_table2table_agg_insert_query(
        conn_or_cursor,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
        where_block="WHERE error_message IS NULL",
    )
    sqlstrs = [pidgin_belief_believer_put_sqlstr]
    if dimen.lower().startswith("believer"):
        del_raw_tablename = create_prime_tablename(dimen, "s", "raw", "del")
        del_agg_tablename = create_prime_tablename(dimen, "s", "agg", "del")
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
        last_element = dimen_focus_columns.pop(-1)
        dimen_focus_columns.append(f"{last_element}_ERASE")
        believer_del_sqlstr = create_table2table_agg_insert_query(
            conn_or_cursor,
            src_table=del_raw_tablename,
            dst_table=del_agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
            where_block="",
        )
        sqlstrs.append(believer_del_sqlstr)

    return sqlstrs


def create_insert_into_pidgin_core_raw_sqlstr(dimen: str) -> str:
    pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
    pidgin_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    return f"""INSERT INTO {pidgin_core_s_raw_tablename} (source_dimen, face_name, otx_knot, inx_knot, unknown_str)
SELECT '{pidgin_s_agg_tablename}', face_name, otx_knot, inx_knot, unknown_str
FROM {pidgin_s_agg_tablename}
GROUP BY face_name, otx_knot, inx_knot, unknown_str
;
"""


def create_insert_pidgin_core_agg_into_vld_sqlstr(
    default_knot: str, default_unknown: str
):
    return f"""INSERT INTO pidgin_core_s_vld (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  face_name
, IFNULL(otx_knot, '{default_knot}')
, IFNULL(inx_knot, '{default_knot}')
, IFNULL(unknown_str, '{default_unknown}')
FROM pidgin_core_s_agg
;
"""


def create_insert_missing_face_name_into_pidgin_core_vld_sqlstr(
    default_knot: str, default_unknown: str, belief_believer_sound_agg_tablename: str
):
    return f"""INSERT INTO pidgin_core_s_vld (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  {belief_believer_sound_agg_tablename}.face_name
, '{default_knot}'
, '{default_knot}'
, '{default_unknown}'
FROM {belief_believer_sound_agg_tablename} 
LEFT JOIN pidgin_core_s_vld ON pidgin_core_s_vld.face_name = {belief_believer_sound_agg_tablename}.face_name
WHERE pidgin_core_s_vld.face_name IS NULL
GROUP BY {belief_believer_sound_agg_tablename}.face_name
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


def create_update_pidlabe_sound_agg_knot_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidlabe_s_agg_tablename = create_prime_tablename("pidlabe", "s", "agg")
    return f"""UPDATE {pidlabe_s_agg_tablename}
SET error_message = 'Knot cannot exist in LabelTerm'
WHERE rowid IN (
    SELECT label_agg.rowid
    FROM {pidlabe_s_agg_tablename} label_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = label_agg.face_name
    WHERE label_agg.otx_label LIKE '%' || core_vld.otx_knot || '%'
      OR label_agg.inx_label LIKE '%' || core_vld.inx_knot || '%'
)
;
"""


def create_update_pidrope_sound_agg_knot_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidrope_s_agg_tablename = create_prime_tablename("pidrope", "s", "agg")
    return f"""UPDATE {pidrope_s_agg_tablename}
SET error_message = 'Knot must exist in RopeTerm'
WHERE rowid IN (
    SELECT rope_agg.rowid
    FROM {pidrope_s_agg_tablename} rope_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = rope_agg.face_name
    WHERE NOT rope_agg.otx_rope LIKE core_vld.otx_knot || '%'
        OR NOT rope_agg.inx_rope LIKE core_vld.inx_knot || '%'
)
;
"""


def create_update_pidname_sound_agg_knot_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidname_s_agg_tablename = create_prime_tablename("pidname", "s", "agg")
    return f"""UPDATE {pidname_s_agg_tablename}
SET error_message = 'Knot cannot exist in NameTerm'
WHERE rowid IN (
    SELECT name_agg.rowid
    FROM {pidname_s_agg_tablename} name_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = name_agg.face_name
    WHERE name_agg.otx_name LIKE '%' || core_vld.otx_knot || '%'
      OR name_agg.inx_name LIKE '%' || core_vld.inx_knot || '%'
)
;
"""


def create_update_pidtitl_sound_agg_knot_error_sqlstr() -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    pidtitl_s_agg_tablename = create_prime_tablename("pidtitl", "s", "agg")
    return f"""UPDATE {pidtitl_s_agg_tablename}
SET error_message = 'Otx and inx titles must match knot.'
WHERE rowid IN (
  SELECT title_agg.rowid
  FROM {pidtitl_s_agg_tablename} title_agg
  JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = title_agg.face_name
  WHERE NOT ((
            title_agg.otx_title LIKE core_vld.otx_knot || '%' 
        AND title_agg.inx_title LIKE core_vld.inx_knot || '%') 
      OR (
            NOT title_agg.otx_title LIKE core_vld.otx_knot || '%'
        AND NOT title_agg.inx_title LIKE core_vld.inx_knot || '%'
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
        "pidgin_rope": "rope",
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


def create_knot_exists_in_name_error_update_sqlstr(table: str, column: str) -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    return f"""UPDATE {table}
SET error_message = 'Knot cannot exist in NameTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_knot || '%'
)
;
"""


def create_knot_exists_in_label_error_update_sqlstr(table: str, column: str) -> str:
    pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
    return f"""UPDATE {table}
SET error_message = 'Knot cannot exist in LabelTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {pidcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_knot || '%'
)
;
"""


INSERT_BLRMEMB_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_partner_membership_s_put_vld (event_int, face_name, belief_label, believer_name, partner_name, group_title, group_cred_points, group_debt_points) SELECT event_int, face_name, belief_label, believer_name, partner_name, group_title, group_cred_points, group_debt_points FROM believer_partner_membership_s_put_agg WHERE error_message IS NULL"
INSERT_BLRMEMB_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_partner_membership_s_del_vld (event_int, face_name, belief_label, believer_name, partner_name, group_title_ERASE) SELECT event_int, face_name, belief_label, believer_name, partner_name, group_title_ERASE FROM believer_partner_membership_s_del_agg WHERE error_message IS NULL"
INSERT_BLRPERN_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_partnerunit_s_put_vld (event_int, face_name, belief_label, believer_name, partner_name, partner_cred_points, partner_debt_points) SELECT event_int, face_name, belief_label, believer_name, partner_name, partner_cred_points, partner_debt_points FROM believer_partnerunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRPERN_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_partnerunit_s_del_vld (event_int, face_name, belief_label, believer_name, partner_name_ERASE) SELECT event_int, face_name, belief_label, believer_name, partner_name_ERASE FROM believer_partnerunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRAWAR_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_plan_awardlink_s_put_vld (event_int, face_name, belief_label, believer_name, plan_rope, awardee_title, give_force, take_force) SELECT event_int, face_name, belief_label, believer_name, plan_rope, awardee_title, give_force, take_force FROM believer_plan_awardlink_s_put_agg WHERE error_message IS NULL"
INSERT_BLRAWAR_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_plan_awardlink_s_del_vld (event_int, face_name, belief_label, believer_name, plan_rope, awardee_title_ERASE) SELECT event_int, face_name, belief_label, believer_name, plan_rope, awardee_title_ERASE FROM believer_plan_awardlink_s_del_agg WHERE error_message IS NULL"
INSERT_BLRFACT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_plan_factunit_s_put_vld (event_int, face_name, belief_label, believer_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper) SELECT event_int, face_name, belief_label, believer_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper FROM believer_plan_factunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRFACT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_plan_factunit_s_del_vld (event_int, face_name, belief_label, believer_name, plan_rope, fact_context_ERASE) SELECT event_int, face_name, belief_label, believer_name, plan_rope, fact_context_ERASE FROM believer_plan_factunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRHEAL_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_plan_healerlink_s_put_vld (event_int, face_name, belief_label, believer_name, plan_rope, healer_name) SELECT event_int, face_name, belief_label, believer_name, plan_rope, healer_name FROM believer_plan_healerlink_s_put_agg WHERE error_message IS NULL"
INSERT_BLRHEAL_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_plan_healerlink_s_del_vld (event_int, face_name, belief_label, believer_name, plan_rope, healer_name_ERASE) SELECT event_int, face_name, belief_label, believer_name, plan_rope, healer_name_ERASE FROM believer_plan_healerlink_s_del_agg WHERE error_message IS NULL"
INSERT_BLRPREM_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_plan_reason_caseunit_s_put_vld (event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor) SELECT event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor FROM believer_plan_reason_caseunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRPREM_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_plan_reason_caseunit_s_del_vld (event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_state_ERASE) SELECT event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_state_ERASE FROM believer_plan_reason_caseunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRREAS_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_plan_reasonunit_s_put_vld (event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_active_requisite) SELECT event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_active_requisite FROM believer_plan_reasonunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRREAS_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_plan_reasonunit_s_del_vld (event_int, face_name, belief_label, believer_name, plan_rope, reason_context_ERASE) SELECT event_int, face_name, belief_label, believer_name, plan_rope, reason_context_ERASE FROM believer_plan_reasonunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRLABO_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_plan_laborlink_s_put_vld (event_int, face_name, belief_label, believer_name, plan_rope, labor_title) SELECT event_int, face_name, belief_label, believer_name, plan_rope, labor_title FROM believer_plan_laborlink_s_put_agg WHERE error_message IS NULL"
INSERT_BLRLABO_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_plan_laborlink_s_del_vld (event_int, face_name, belief_label, believer_name, plan_rope, labor_title_ERASE) SELECT event_int, face_name, belief_label, believer_name, plan_rope, labor_title_ERASE FROM believer_plan_laborlink_s_del_agg WHERE error_message IS NULL"
INSERT_BLRPLAN_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believer_planunit_s_put_vld (event_int, face_name, belief_label, believer_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, task, problem_bool) SELECT event_int, face_name, belief_label, believer_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, task, problem_bool FROM believer_planunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRPLAN_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believer_planunit_s_del_vld (event_int, face_name, belief_label, believer_name, plan_rope_ERASE) SELECT event_int, face_name, belief_label, believer_name, plan_rope_ERASE FROM believer_planunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRUNIT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO believerunit_s_put_vld (event_int, face_name, belief_label, believer_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit) SELECT event_int, face_name, belief_label, believer_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit FROM believerunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRUNIT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO believerunit_s_del_vld (event_int, face_name, belief_label, believer_name_ERASE) SELECT event_int, face_name, belief_label, believer_name_ERASE FROM believerunit_s_del_agg WHERE error_message IS NULL"

INSERT_BLFPAYY_SOUND_VLD_SQLSTR = "INSERT INTO belief_paybook_s_vld (event_int, face_name, belief_label, believer_name, partner_name, tran_time, amount) SELECT event_int, face_name, belief_label, believer_name, partner_name, tran_time, amount FROM belief_paybook_s_agg WHERE error_message IS NULL"
INSERT_BLFBUDD_SOUND_VLD_SQLSTR = "INSERT INTO belief_budunit_s_vld (event_int, face_name, belief_label, believer_name, bud_time, quota, celldepth) SELECT event_int, face_name, belief_label, believer_name, bud_time, quota, celldepth FROM belief_budunit_s_agg WHERE error_message IS NULL"
INSERT_BLFHOUR_SOUND_VLD_SQLSTR = "INSERT INTO belief_timeline_hour_s_vld (event_int, face_name, belief_label, cumulative_minute, hour_label) SELECT event_int, face_name, belief_label, cumulative_minute, hour_label FROM belief_timeline_hour_s_agg WHERE error_message IS NULL"
INSERT_BLFMONT_SOUND_VLD_SQLSTR = "INSERT INTO belief_timeline_month_s_vld (event_int, face_name, belief_label, cumulative_day, month_label) SELECT event_int, face_name, belief_label, cumulative_day, month_label FROM belief_timeline_month_s_agg WHERE error_message IS NULL"
INSERT_BLFWEEK_SOUND_VLD_SQLSTR = "INSERT INTO belief_timeline_weekday_s_vld (event_int, face_name, belief_label, weekday_order, weekday_label) SELECT event_int, face_name, belief_label, weekday_order, weekday_label FROM belief_timeline_weekday_s_agg WHERE error_message IS NULL"
INSERT_BLFOFFI_SOUND_VLD_SQLSTR = "INSERT INTO belief_timeoffi_s_vld (event_int, face_name, belief_label, offi_time) SELECT event_int, face_name, belief_label, offi_time FROM belief_timeoffi_s_agg WHERE error_message IS NULL"
INSERT_BLFUNIT_SOUND_VLD_SQLSTR = "INSERT INTO beliefunit_s_vld (event_int, face_name, belief_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations) SELECT event_int, face_name, belief_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations FROM beliefunit_s_agg WHERE error_message IS NULL"


def get_insert_into_sound_vld_sqlstrs() -> dict[str, str]:
    return {
        "believer_partner_membership_s_put_vld": INSERT_BLRMEMB_SOUND_VLD_PUT_SQLSTR,
        "believer_partner_membership_s_del_vld": INSERT_BLRMEMB_SOUND_VLD_DEL_SQLSTR,
        "believer_partnerunit_s_put_vld": INSERT_BLRPERN_SOUND_VLD_PUT_SQLSTR,
        "believer_partnerunit_s_del_vld": INSERT_BLRPERN_SOUND_VLD_DEL_SQLSTR,
        "believer_plan_awardlink_s_put_vld": INSERT_BLRAWAR_SOUND_VLD_PUT_SQLSTR,
        "believer_plan_awardlink_s_del_vld": INSERT_BLRAWAR_SOUND_VLD_DEL_SQLSTR,
        "believer_plan_factunit_s_put_vld": INSERT_BLRFACT_SOUND_VLD_PUT_SQLSTR,
        "believer_plan_factunit_s_del_vld": INSERT_BLRFACT_SOUND_VLD_DEL_SQLSTR,
        "believer_plan_healerlink_s_put_vld": INSERT_BLRHEAL_SOUND_VLD_PUT_SQLSTR,
        "believer_plan_healerlink_s_del_vld": INSERT_BLRHEAL_SOUND_VLD_DEL_SQLSTR,
        "believer_plan_reason_caseunit_s_put_vld": INSERT_BLRPREM_SOUND_VLD_PUT_SQLSTR,
        "believer_plan_reason_caseunit_s_del_vld": INSERT_BLRPREM_SOUND_VLD_DEL_SQLSTR,
        "believer_plan_reasonunit_s_put_vld": INSERT_BLRREAS_SOUND_VLD_PUT_SQLSTR,
        "believer_plan_reasonunit_s_del_vld": INSERT_BLRREAS_SOUND_VLD_DEL_SQLSTR,
        "believer_plan_laborlink_s_put_vld": INSERT_BLRLABO_SOUND_VLD_PUT_SQLSTR,
        "believer_plan_laborlink_s_del_vld": INSERT_BLRLABO_SOUND_VLD_DEL_SQLSTR,
        "believer_planunit_s_put_vld": INSERT_BLRPLAN_SOUND_VLD_PUT_SQLSTR,
        "believer_planunit_s_del_vld": INSERT_BLRPLAN_SOUND_VLD_DEL_SQLSTR,
        "believerunit_s_put_vld": INSERT_BLRUNIT_SOUND_VLD_PUT_SQLSTR,
        "believerunit_s_del_vld": INSERT_BLRUNIT_SOUND_VLD_DEL_SQLSTR,
        "belief_paybook_s_vld": INSERT_BLFPAYY_SOUND_VLD_SQLSTR,
        "belief_budunit_s_vld": INSERT_BLFBUDD_SOUND_VLD_SQLSTR,
        "belief_timeline_hour_s_vld": INSERT_BLFHOUR_SOUND_VLD_SQLSTR,
        "belief_timeline_month_s_vld": INSERT_BLFMONT_SOUND_VLD_SQLSTR,
        "belief_timeline_weekday_s_vld": INSERT_BLFWEEK_SOUND_VLD_SQLSTR,
        "belief_timeoffi_s_vld": INSERT_BLFOFFI_SOUND_VLD_SQLSTR,
        "beliefunit_s_vld": INSERT_BLFUNIT_SOUND_VLD_SQLSTR,
    }


INSERT_BLFPAYY_VOICE_RAW_SQLSTR = "INSERT INTO belief_paybook_v_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, partner_name_otx, tran_time, amount) SELECT event_int, face_name, belief_label, believer_name, partner_name, tran_time, amount FROM belief_paybook_s_vld "
INSERT_BLFBUDD_VOICE_RAW_SQLSTR = "INSERT INTO belief_budunit_v_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, bud_time, quota, celldepth) SELECT event_int, face_name, belief_label, believer_name, bud_time, quota, celldepth FROM belief_budunit_s_vld "
INSERT_BLFHOUR_VOICE_RAW_SQLSTR = "INSERT INTO belief_timeline_hour_v_raw (event_int, face_name_otx, belief_label_otx, cumulative_minute, hour_label_otx) SELECT event_int, face_name, belief_label, cumulative_minute, hour_label FROM belief_timeline_hour_s_vld "
INSERT_BLFMONT_VOICE_RAW_SQLSTR = "INSERT INTO belief_timeline_month_v_raw (event_int, face_name_otx, belief_label_otx, cumulative_day, month_label_otx) SELECT event_int, face_name, belief_label, cumulative_day, month_label FROM belief_timeline_month_s_vld "
INSERT_BLFWEEK_VOICE_RAW_SQLSTR = "INSERT INTO belief_timeline_weekday_v_raw (event_int, face_name_otx, belief_label_otx, weekday_order, weekday_label_otx) SELECT event_int, face_name, belief_label, weekday_order, weekday_label FROM belief_timeline_weekday_s_vld "
INSERT_BLFOFFI_VOICE_RAW_SQLSTR = "INSERT INTO belief_timeoffi_v_raw (event_int, face_name_otx, belief_label_otx, offi_time) SELECT event_int, face_name, belief_label, offi_time FROM belief_timeoffi_s_vld "
INSERT_BLFUNIT_VOICE_RAW_SQLSTR = "INSERT INTO beliefunit_v_raw (event_int, face_name_otx, belief_label_otx, timeline_label_otx, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations) SELECT event_int, face_name, belief_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations FROM beliefunit_s_vld "

INSERT_BLRMEMB_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_partner_membership_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, partner_name_otx, group_title_otx, group_cred_points, group_debt_points) SELECT event_int, face_name, belief_label, believer_name, partner_name, group_title, group_cred_points, group_debt_points FROM believer_partner_membership_s_put_vld "
INSERT_BLRMEMB_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_partner_membership_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, partner_name_otx, group_title_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, partner_name, group_title_ERASE FROM believer_partner_membership_s_del_vld "
INSERT_BLRPERN_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_partnerunit_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, partner_name_otx, partner_cred_points, partner_debt_points) SELECT event_int, face_name, belief_label, believer_name, partner_name, partner_cred_points, partner_debt_points FROM believer_partnerunit_s_put_vld "
INSERT_BLRPERN_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_partnerunit_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, partner_name_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, partner_name_ERASE FROM believer_partnerunit_s_del_vld "
INSERT_BLRAWAR_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_plan_awardlink_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, awardee_title_otx, give_force, take_force) SELECT event_int, face_name, belief_label, believer_name, plan_rope, awardee_title, give_force, take_force FROM believer_plan_awardlink_s_put_vld "
INSERT_BLRAWAR_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_plan_awardlink_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, awardee_title_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope, awardee_title_ERASE FROM believer_plan_awardlink_s_del_vld "
INSERT_BLRFACT_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_plan_factunit_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, fact_context_otx, fact_state_otx, fact_lower, fact_upper) SELECT event_int, face_name, belief_label, believer_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper FROM believer_plan_factunit_s_put_vld "
INSERT_BLRFACT_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_plan_factunit_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, fact_context_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope, fact_context_ERASE FROM believer_plan_factunit_s_del_vld "
INSERT_BLRHEAL_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_plan_healerlink_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, healer_name_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope, healer_name FROM believer_plan_healerlink_s_put_vld "
INSERT_BLRHEAL_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_plan_healerlink_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, healer_name_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope, healer_name_ERASE FROM believer_plan_healerlink_s_del_vld "
INSERT_BLRPREM_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_plan_reason_caseunit_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, reason_context_otx, reason_state_otx, reason_upper, reason_lower, reason_divisor) SELECT event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor FROM believer_plan_reason_caseunit_s_put_vld "
INSERT_BLRPREM_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_plan_reason_caseunit_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, reason_context_otx, reason_state_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_state_ERASE FROM believer_plan_reason_caseunit_s_del_vld "
INSERT_BLRREAS_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_plan_reasonunit_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, reason_context_otx, reason_active_requisite) SELECT event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_active_requisite FROM believer_plan_reasonunit_s_put_vld "
INSERT_BLRREAS_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_plan_reasonunit_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, reason_context_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope, reason_context_ERASE FROM believer_plan_reasonunit_s_del_vld "
INSERT_BLRLABO_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_plan_laborlink_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, labor_title_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope, labor_title FROM believer_plan_laborlink_s_put_vld "
INSERT_BLRLABO_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_plan_laborlink_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, labor_title_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope, labor_title_ERASE FROM believer_plan_laborlink_s_del_vld "
INSERT_BLRPLAN_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believer_planunit_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_otx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, task, problem_bool) SELECT event_int, face_name, belief_label, believer_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, task, problem_bool FROM believer_planunit_s_put_vld "
INSERT_BLRPLAN_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believer_planunit_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, plan_rope_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name, plan_rope_ERASE FROM believer_planunit_s_del_vld "
INSERT_BLRUNIT_VOICE_RAW_PUT_SQLSTR = "INSERT INTO believerunit_v_put_raw (event_int, face_name_otx, belief_label_otx, believer_name_otx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit) SELECT event_int, face_name, belief_label, believer_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit FROM believerunit_s_put_vld "
INSERT_BLRUNIT_VOICE_RAW_DEL_SQLSTR = "INSERT INTO believerunit_v_del_raw (event_int, face_name_otx, belief_label_otx, believer_name_ERASE_otx) SELECT event_int, face_name, belief_label, believer_name_ERASE FROM believerunit_s_del_vld "


def get_insert_into_voice_raw_sqlstrs() -> dict[str, str]:
    return {
        "belief_paybook_v_raw": INSERT_BLFPAYY_VOICE_RAW_SQLSTR,
        "belief_budunit_v_raw": INSERT_BLFBUDD_VOICE_RAW_SQLSTR,
        "belief_timeline_hour_v_raw": INSERT_BLFHOUR_VOICE_RAW_SQLSTR,
        "belief_timeline_month_v_raw": INSERT_BLFMONT_VOICE_RAW_SQLSTR,
        "belief_timeline_weekday_v_raw": INSERT_BLFWEEK_VOICE_RAW_SQLSTR,
        "belief_timeoffi_v_raw": INSERT_BLFOFFI_VOICE_RAW_SQLSTR,
        "beliefunit_v_raw": INSERT_BLFUNIT_VOICE_RAW_SQLSTR,
        "believer_partner_membership_v_put_raw": INSERT_BLRMEMB_VOICE_RAW_PUT_SQLSTR,
        "believer_partner_membership_v_del_raw": INSERT_BLRMEMB_VOICE_RAW_DEL_SQLSTR,
        "believer_partnerunit_v_put_raw": INSERT_BLRPERN_VOICE_RAW_PUT_SQLSTR,
        "believer_partnerunit_v_del_raw": INSERT_BLRPERN_VOICE_RAW_DEL_SQLSTR,
        "believer_plan_awardlink_v_put_raw": INSERT_BLRAWAR_VOICE_RAW_PUT_SQLSTR,
        "believer_plan_awardlink_v_del_raw": INSERT_BLRAWAR_VOICE_RAW_DEL_SQLSTR,
        "believer_plan_factunit_v_put_raw": INSERT_BLRFACT_VOICE_RAW_PUT_SQLSTR,
        "believer_plan_factunit_v_del_raw": INSERT_BLRFACT_VOICE_RAW_DEL_SQLSTR,
        "believer_plan_healerlink_v_put_raw": INSERT_BLRHEAL_VOICE_RAW_PUT_SQLSTR,
        "believer_plan_healerlink_v_del_raw": INSERT_BLRHEAL_VOICE_RAW_DEL_SQLSTR,
        "believer_plan_reason_caseunit_v_put_raw": INSERT_BLRPREM_VOICE_RAW_PUT_SQLSTR,
        "believer_plan_reason_caseunit_v_del_raw": INSERT_BLRPREM_VOICE_RAW_DEL_SQLSTR,
        "believer_plan_reasonunit_v_put_raw": INSERT_BLRREAS_VOICE_RAW_PUT_SQLSTR,
        "believer_plan_reasonunit_v_del_raw": INSERT_BLRREAS_VOICE_RAW_DEL_SQLSTR,
        "believer_plan_laborlink_v_put_raw": INSERT_BLRLABO_VOICE_RAW_PUT_SQLSTR,
        "believer_plan_laborlink_v_del_raw": INSERT_BLRLABO_VOICE_RAW_DEL_SQLSTR,
        "believer_planunit_v_put_raw": INSERT_BLRPLAN_VOICE_RAW_PUT_SQLSTR,
        "believer_planunit_v_del_raw": INSERT_BLRPLAN_VOICE_RAW_DEL_SQLSTR,
        "believerunit_v_put_raw": INSERT_BLRUNIT_VOICE_RAW_PUT_SQLSTR,
        "believerunit_v_del_raw": INSERT_BLRUNIT_VOICE_RAW_DEL_SQLSTR,
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


BLFPAYY_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO belief_paybook_v_agg (belief_label, believer_name, partner_name, tran_time, amount)
SELECT belief_label_inx, believer_name_inx, partner_name_inx, tran_time, amount
FROM belief_paybook_v_raw
GROUP BY belief_label_inx, believer_name_inx, partner_name_inx, tran_time, amount
"""
BLFBUDD_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO belief_budunit_v_agg (belief_label, believer_name, bud_time, quota, celldepth)
SELECT belief_label_inx, believer_name_inx, bud_time, quota, celldepth
FROM belief_budunit_v_raw
GROUP BY belief_label_inx, believer_name_inx, bud_time, quota, celldepth
"""
BLFHOUR_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO belief_timeline_hour_v_agg (belief_label, cumulative_minute, hour_label)
SELECT belief_label_inx, cumulative_minute, hour_label_inx
FROM belief_timeline_hour_v_raw
GROUP BY belief_label_inx, cumulative_minute, hour_label_inx
"""
BLFMONT_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO belief_timeline_month_v_agg (belief_label, cumulative_day, month_label)
SELECT belief_label_inx, cumulative_day, month_label_inx
FROM belief_timeline_month_v_raw
GROUP BY belief_label_inx, cumulative_day, month_label_inx
"""
BLFWEEK_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO belief_timeline_weekday_v_agg (belief_label, weekday_order, weekday_label)
SELECT belief_label_inx, weekday_order, weekday_label_inx
FROM belief_timeline_weekday_v_raw
GROUP BY belief_label_inx, weekday_order, weekday_label_inx
"""
BLFOFFI_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO belief_timeoffi_v_agg (belief_label, offi_time)
SELECT belief_label_inx, offi_time
FROM belief_timeoffi_v_raw
GROUP BY belief_label_inx, offi_time
"""
BLFUNIT_VOICE_AGG_INSERT_SQLSTR = """
INSERT INTO beliefunit_v_agg (belief_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations)
SELECT belief_label_inx, timeline_label_inx, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations
FROM beliefunit_v_raw
GROUP BY belief_label_inx, timeline_label_inx, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations
"""

INSERT_BLRMEMB_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_partner_membership_v_put_agg (event_int, face_name, belief_label, believer_name, partner_name, group_title, group_cred_points, group_debt_points)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, partner_name_inx, group_title_inx, group_cred_points, group_debt_points
FROM believer_partner_membership_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, partner_name_inx, group_title_inx, group_cred_points, group_debt_points
"""
INSERT_BLRMEMB_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_partner_membership_v_del_agg (event_int, face_name, belief_label, believer_name, partner_name, group_title_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, partner_name_inx, group_title_ERASE_inx
FROM believer_partner_membership_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, partner_name_inx, group_title_ERASE_inx
"""
INSERT_BLRPERN_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_partnerunit_v_put_agg (event_int, face_name, belief_label, believer_name, partner_name, partner_cred_points, partner_debt_points)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, partner_name_inx, partner_cred_points, partner_debt_points
FROM believer_partnerunit_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, partner_name_inx, partner_cred_points, partner_debt_points
"""
INSERT_BLRPERN_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_partnerunit_v_del_agg (event_int, face_name, belief_label, believer_name, partner_name_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, partner_name_ERASE_inx
FROM believer_partnerunit_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, partner_name_ERASE_inx
"""
INSERT_BLRAWAR_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_plan_awardlink_v_put_agg (event_int, face_name, belief_label, believer_name, plan_rope, awardee_title, give_force, take_force)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, awardee_title_inx, give_force, take_force
FROM believer_plan_awardlink_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, awardee_title_inx, give_force, take_force
"""
INSERT_BLRAWAR_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_plan_awardlink_v_del_agg (event_int, face_name, belief_label, believer_name, plan_rope, awardee_title_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, awardee_title_ERASE_inx
FROM believer_plan_awardlink_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, awardee_title_ERASE_inx
"""
INSERT_BLRFACT_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_plan_factunit_v_put_agg (event_int, face_name, belief_label, believer_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper
FROM believer_plan_factunit_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper
"""
INSERT_BLRFACT_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_plan_factunit_v_del_agg (event_int, face_name, belief_label, believer_name, plan_rope, fact_context_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, fact_context_ERASE_inx
FROM believer_plan_factunit_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, fact_context_ERASE_inx
"""
INSERT_BLRHEAL_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_plan_healerlink_v_put_agg (event_int, face_name, belief_label, believer_name, plan_rope, healer_name)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, healer_name_inx
FROM believer_plan_healerlink_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, healer_name_inx
"""
INSERT_BLRHEAL_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_plan_healerlink_v_del_agg (event_int, face_name, belief_label, believer_name, plan_rope, healer_name_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, healer_name_ERASE_inx
FROM believer_plan_healerlink_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, healer_name_ERASE_inx
"""
INSERT_BLRPREM_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_plan_reason_caseunit_v_put_agg (event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, reason_context_inx, reason_state_inx, reason_upper, reason_lower, reason_divisor
FROM believer_plan_reason_caseunit_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, reason_context_inx, reason_state_inx, reason_upper, reason_lower, reason_divisor
"""
INSERT_BLRPREM_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_plan_reason_caseunit_v_del_agg (event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_state_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, reason_context_inx, reason_state_ERASE_inx
FROM believer_plan_reason_caseunit_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, reason_context_inx, reason_state_ERASE_inx
"""
INSERT_BLRREAS_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_plan_reasonunit_v_put_agg (event_int, face_name, belief_label, believer_name, plan_rope, reason_context, reason_active_requisite)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, reason_context_inx, reason_active_requisite
FROM believer_plan_reasonunit_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, reason_context_inx, reason_active_requisite
"""
INSERT_BLRREAS_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_plan_reasonunit_v_del_agg (event_int, face_name, belief_label, believer_name, plan_rope, reason_context_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, reason_context_ERASE_inx
FROM believer_plan_reasonunit_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, reason_context_ERASE_inx
"""
INSERT_BLRLABO_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_plan_laborlink_v_put_agg (event_int, face_name, belief_label, believer_name, plan_rope, labor_title)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, labor_title_inx
FROM believer_plan_laborlink_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, labor_title_inx
"""
INSERT_BLRLABO_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_plan_laborlink_v_del_agg (event_int, face_name, belief_label, believer_name, plan_rope, labor_title_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, labor_title_ERASE_inx
FROM believer_plan_laborlink_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, labor_title_ERASE_inx
"""
INSERT_BLRPLAN_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believer_planunit_v_put_agg (event_int, face_name, belief_label, believer_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, task, problem_bool)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, task, problem_bool
FROM believer_planunit_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, task, problem_bool
"""
INSERT_BLRPLAN_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believer_planunit_v_del_agg (event_int, face_name, belief_label, believer_name, plan_rope_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_ERASE_inx
FROM believer_planunit_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, plan_rope_ERASE_inx
"""
INSERT_BLRUNIT_VOICE_AGG_PUT_SQLSTR = """
INSERT INTO believerunit_v_put_agg (event_int, face_name, belief_label, believer_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit
FROM believerunit_v_put_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_iota, penny, respect_bit
"""
INSERT_BLRUNIT_VOICE_AGG_DEL_SQLSTR = """
INSERT INTO believerunit_v_del_agg (event_int, face_name, belief_label, believer_name_ERASE)
SELECT event_int, face_name_inx, belief_label_inx, believer_name_ERASE_inx
FROM believerunit_v_del_raw
GROUP BY event_int, face_name_inx, belief_label_inx, believer_name_ERASE_inx
"""


def get_insert_voice_agg_sqlstrs() -> dict[str, str]:
    return {
        "belief_paybook": BLFPAYY_VOICE_AGG_INSERT_SQLSTR,
        "belief_budunit": BLFBUDD_VOICE_AGG_INSERT_SQLSTR,
        "belief_timeline_hour": BLFHOUR_VOICE_AGG_INSERT_SQLSTR,
        "belief_timeline_month": BLFMONT_VOICE_AGG_INSERT_SQLSTR,
        "belief_timeline_weekday": BLFWEEK_VOICE_AGG_INSERT_SQLSTR,
        "belief_timeoffi": BLFOFFI_VOICE_AGG_INSERT_SQLSTR,
        "beliefunit": BLFUNIT_VOICE_AGG_INSERT_SQLSTR,
        "believer_partner_membership_v_put_agg": INSERT_BLRMEMB_VOICE_AGG_PUT_SQLSTR,
        "believer_partner_membership_v_del_agg": INSERT_BLRMEMB_VOICE_AGG_DEL_SQLSTR,
        "believer_partnerunit_v_put_agg": INSERT_BLRPERN_VOICE_AGG_PUT_SQLSTR,
        "believer_partnerunit_v_del_agg": INSERT_BLRPERN_VOICE_AGG_DEL_SQLSTR,
        "believer_plan_awardlink_v_put_agg": INSERT_BLRAWAR_VOICE_AGG_PUT_SQLSTR,
        "believer_plan_awardlink_v_del_agg": INSERT_BLRAWAR_VOICE_AGG_DEL_SQLSTR,
        "believer_plan_factunit_v_put_agg": INSERT_BLRFACT_VOICE_AGG_PUT_SQLSTR,
        "believer_plan_factunit_v_del_agg": INSERT_BLRFACT_VOICE_AGG_DEL_SQLSTR,
        "believer_plan_healerlink_v_put_agg": INSERT_BLRHEAL_VOICE_AGG_PUT_SQLSTR,
        "believer_plan_healerlink_v_del_agg": INSERT_BLRHEAL_VOICE_AGG_DEL_SQLSTR,
        "believer_plan_reason_caseunit_v_put_agg": INSERT_BLRPREM_VOICE_AGG_PUT_SQLSTR,
        "believer_plan_reason_caseunit_v_del_agg": INSERT_BLRPREM_VOICE_AGG_DEL_SQLSTR,
        "believer_plan_reasonunit_v_put_agg": INSERT_BLRREAS_VOICE_AGG_PUT_SQLSTR,
        "believer_plan_reasonunit_v_del_agg": INSERT_BLRREAS_VOICE_AGG_DEL_SQLSTR,
        "believer_plan_laborlink_v_put_agg": INSERT_BLRLABO_VOICE_AGG_PUT_SQLSTR,
        "believer_plan_laborlink_v_del_agg": INSERT_BLRLABO_VOICE_AGG_DEL_SQLSTR,
        "believer_planunit_v_put_agg": INSERT_BLRPLAN_VOICE_AGG_PUT_SQLSTR,
        "believer_planunit_v_del_agg": INSERT_BLRPLAN_VOICE_AGG_DEL_SQLSTR,
        "believerunit_v_put_agg": INSERT_BLRUNIT_VOICE_AGG_PUT_SQLSTR,
        "believerunit_v_del_agg": INSERT_BLRUNIT_VOICE_AGG_DEL_SQLSTR,
    }


BLFPAYY_FU2_SELECT_SQLSTR = "SELECT belief_label, believer_name, partner_name, tran_time, amount FROM belief_paybook_v_agg WHERE belief_label = "
BLFBUDD_FU2_SELECT_SQLSTR = "SELECT belief_label, believer_name, bud_time, quota, celldepth FROM belief_budunit_v_agg WHERE belief_label = "
BLFHOUR_FU2_SELECT_SQLSTR = "SELECT belief_label, cumulative_minute, hour_label FROM belief_timeline_hour_v_agg WHERE belief_label = "
BLFMONT_FU2_SELECT_SQLSTR = "SELECT belief_label, cumulative_day, month_label FROM belief_timeline_month_v_agg WHERE belief_label = "
BLFWEEK_FU2_SELECT_SQLSTR = "SELECT belief_label, weekday_order, weekday_label FROM belief_timeline_weekday_v_agg WHERE belief_label = "
BLFOFFI_FU2_SELECT_SQLSTR = (
    "SELECT belief_label, offi_time FROM belief_timeoffi_v_agg WHERE belief_label = "
)
BLFUNIT_FU2_SELECT_SQLSTR = "SELECT belief_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations FROM beliefunit_v_agg WHERE belief_label = "


def get_belief_voice_select1_sqlstrs(belief_label: str) -> dict[str, str]:
    return {
        "beliefunit": f"{BLFUNIT_FU2_SELECT_SQLSTR}'{belief_label}'",
        "belief_budunit": f"{BLFBUDD_FU2_SELECT_SQLSTR}'{belief_label}'",
        "belief_paybook": f"{BLFPAYY_FU2_SELECT_SQLSTR}'{belief_label}'",
        "belief_timeline_hour": f"{BLFHOUR_FU2_SELECT_SQLSTR}'{belief_label}'",
        "belief_timeline_month": f"{BLFMONT_FU2_SELECT_SQLSTR}'{belief_label}'",
        "belief_timeline_weekday": f"{BLFWEEK_FU2_SELECT_SQLSTR}'{belief_label}'",
        "belief_timeoffi": f"{BLFOFFI_FU2_SELECT_SQLSTR}'{belief_label}'",
    }


def get_idea_stageble_put_dimens() -> dict[str, list[str]]:
    return {
        "br00000": ["beliefunit"],
        "br00001": ["belief_budunit", "beliefunit", "believerunit"],
        "br00002": [
            "belief_paybook",
            "beliefunit",
            "believer_partnerunit",
            "believerunit",
        ],
        "br00003": ["belief_timeline_hour", "beliefunit"],
        "br00004": ["belief_timeline_month", "beliefunit"],
        "br00005": ["belief_timeline_weekday", "beliefunit"],
        "br00006": ["belief_timeoffi", "beliefunit"],
        "br00011": ["beliefunit", "believer_partnerunit", "believerunit"],
        "br00012": [
            "beliefunit",
            "believer_partner_membership",
            "believer_partnerunit",
            "believerunit",
        ],
        "br00013": ["beliefunit", "believer_planunit", "believerunit"],
        "br00019": ["beliefunit", "believer_planunit", "believerunit"],
        "br00020": [
            "beliefunit",
            "believer_partner_membership",
            "believer_partnerunit",
            "believerunit",
        ],
        "br00021": ["beliefunit", "believer_partnerunit", "believerunit"],
        "br00022": [
            "beliefunit",
            "believer_plan_awardlink",
            "believer_planunit",
            "believerunit",
        ],
        "br00023": [
            "beliefunit",
            "believer_plan_factunit",
            "believer_planunit",
            "believerunit",
        ],
        "br00024": [
            "beliefunit",
            "believer_plan_laborlink",
            "believer_planunit",
            "believerunit",
        ],
        "br00025": [
            "beliefunit",
            "believer_plan_healerlink",
            "believer_planunit",
            "believerunit",
        ],
        "br00026": [
            "beliefunit",
            "believer_plan_reason_caseunit",
            "believer_plan_reasonunit",
            "believer_planunit",
            "believerunit",
        ],
        "br00027": [
            "beliefunit",
            "believer_plan_reasonunit",
            "believer_planunit",
            "believerunit",
        ],
        "br00028": ["beliefunit", "believer_planunit", "believerunit"],
        "br00029": ["beliefunit", "believerunit"],
        "br00036": [
            "beliefunit",
            "believer_plan_healerlink",
            "believer_planunit",
            "believerunit",
        ],
        "br00042": [],
        "br00043": [],
        "br00044": [],
        "br00045": [],
        "br00050": ["beliefunit", "believer_partnerunit", "believerunit"],
        "br00051": ["beliefunit", "believerunit"],
        "br00052": ["beliefunit", "believer_planunit", "believerunit"],
        "br00053": ["beliefunit", "believer_planunit", "believerunit"],
        "br00054": ["beliefunit", "believer_planunit", "believerunit"],
        "br00055": ["beliefunit", "believer_planunit", "believerunit"],
        "br00056": [
            "beliefunit",
            "believer_plan_reasonunit",
            "believer_planunit",
            "believerunit",
        ],
        "br00057": ["beliefunit", "believer_planunit", "believerunit"],
        "br00058": ["beliefunit", "believerunit"],
        "br00059": ["beliefunit"],
        "br00113": ["beliefunit", "believer_partnerunit", "believerunit"],
        "br00115": ["beliefunit", "believer_partnerunit", "believerunit"],
        "br00116": ["beliefunit", "believer_partnerunit", "believerunit"],
        "br00117": ["beliefunit", "believer_partnerunit", "believerunit"],
    }


IDEA_STAGEBLE_DEL_DIMENS = {
    "br00050": ["believer_partner_membership"],
    "br00051": ["believer_partnerunit"],
    "br00052": ["believer_plan_awardlink"],
    "br00053": ["believer_plan_factunit"],
    "br00054": ["believer_plan_laborlink"],
    "br00055": ["believer_plan_healerlink"],
    "br00056": ["believer_plan_reason_caseunit"],
    "br00057": ["believer_plan_reasonunit"],
    "br00058": ["believer_planunit"],
    "br00059": ["believerunit"],
}


CREATE_BELIEF_EVENT_TIME_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS belief_event_time_agg (
  belief_label TEXT
, event_int INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
INSERT_BELIEF_EVENT_TIME_AGG_SQLSTR = """
INSERT INTO belief_event_time_agg (belief_label, event_int, agg_time)
SELECT belief_label, event_int, agg_time
FROM (
    SELECT belief_label, event_int, tran_time as agg_time
    FROM belief_paybook_raw
    GROUP BY belief_label, event_int, tran_time
    UNION 
    SELECT belief_label, event_int, bud_time as agg_time
    FROM belief_budunit_raw
    GROUP BY belief_label, event_int, bud_time
)
ORDER BY belief_label, event_int, agg_time
;
"""
UPDATE_ERROR_MESSAGE_BELIEF_EVENT_TIME_AGG_SQLSTR = """
WITH EventTimeOrdered AS (
    SELECT belief_label, event_int, agg_time,
           LAG(agg_time) OVER (PARTITION BY belief_label ORDER BY event_int) AS prev_agg_time
    FROM belief_event_time_agg
)
UPDATE belief_event_time_agg
SET error_message = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.event_int = belief_event_time_agg.event_int
    AND EventTimeOrdered.belief_label = belief_event_time_agg.belief_label
    AND EventTimeOrdered.agg_time = belief_event_time_agg.agg_time
;
"""


CREATE_BELIEF_OTE1_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS belief_ote1_agg (
  belief_label TEXT
, believer_name TEXT
, event_int INTEGER
, bud_time INTEGER
, error_message TEXT
)
;
"""
INSERT_BELIEF_OTE1_AGG_FROM_VOICE_SQLSTR = """
INSERT INTO belief_ote1_agg (belief_label, believer_name, event_int, bud_time)
SELECT belief_label, believer_name, event_int, bud_time
FROM (
    SELECT 
      belief_label_inx belief_label
    , believer_name_inx believer_name
    , event_int
    , bud_time
    FROM belief_budunit_v_raw
    GROUP BY belief_label_inx, believer_name_inx, event_int, bud_time
)
ORDER BY belief_label, believer_name, event_int, bud_time
;
"""


CREATE_JOB_BLRMEMB_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_partner_membership_job (belief_label TEXT, believer_name TEXT, partner_name TEXT, group_title TEXT, group_cred_points REAL, group_debt_points REAL, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL, _fund_agenda_ratio_give REAL, _fund_agenda_ratio_take REAL)"""
CREATE_JOB_BLRPERN_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_partnerunit_job (belief_label TEXT, believer_name TEXT, partner_name TEXT, partner_cred_points REAL, partner_debt_points REAL, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL, _fund_agenda_ratio_give REAL, _fund_agenda_ratio_take REAL, _inallocable_partner_debt_points REAL, _irrational_partner_debt_points REAL)"""
CREATE_JOB_BLRGROU_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_groupunit_job (belief_label TEXT, believer_name TEXT, group_title TEXT, fund_iota REAL, knot TEXT, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL)"""
CREATE_JOB_BLRAWAR_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_plan_awardlink_job (belief_label TEXT, believer_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, _fund_give REAL, _fund_take REAL)"""
CREATE_JOB_BLRFACT_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_plan_factunit_job (belief_label TEXT, believer_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"""
CREATE_JOB_BLRHEAL_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_plan_healerlink_job (belief_label TEXT, believer_name TEXT, plan_rope TEXT, healer_name TEXT)"""
CREATE_JOB_BLRPREM_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_plan_reason_caseunit_job (belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER, _chore INTEGER, _status INTEGER)"""
CREATE_JOB_BLRREAS_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_plan_reasonunit_job (belief_label TEXT, believer_name TEXT, plan_rope TEXT, reason_context TEXT, reason_active_requisite INTEGER, _chore INTEGER, _status INTEGER, _rplan_active_value INTEGER)"""
CREATE_JOB_BLRLABO_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_plan_laborlink_job (belief_label TEXT, believer_name TEXT, plan_rope TEXT, labor_title TEXT, _believer_name_labor INTEGER)"""
CREATE_JOB_BLRPLAN_SQLSTR = """CREATE TABLE IF NOT EXISTS believer_planunit_job (belief_label TEXT, believer_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, task INTEGER, problem_bool INTEGER, fund_iota REAL, _active INTEGER, _chore INTEGER, _fund_onset REAL, _fund_cease REAL, _fund_ratio REAL, _gogo_calc REAL, _stop_calc REAL, _level INTEGER, _range_evaluated INTEGER, _descendant_task_count INTEGER, _healerlink_ratio REAL, _all_partner_cred INTEGER, _all_partner_debt INTEGER)"""
CREATE_JOB_BLRUNIT_SQLSTR = """CREATE TABLE IF NOT EXISTS believerunit_job (belief_label TEXT, believer_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_iota REAL, penny REAL, respect_bit REAL, _rational INTEGER, _keeps_justified INTEGER, _offtrack_fund REAL, _sum_healerlink_share REAL, _keeps_buildable INTEGER, _tree_traverse_count INTEGER)"""


def get_job_create_table_sqlstrs() -> dict[str, str]:
    return {
        "believer_partner_membership_job": CREATE_JOB_BLRMEMB_SQLSTR,
        "believer_partnerunit_job": CREATE_JOB_BLRPERN_SQLSTR,
        "believer_groupunit_job": CREATE_JOB_BLRGROU_SQLSTR,
        "believer_plan_awardlink_job": CREATE_JOB_BLRAWAR_SQLSTR,
        "believer_plan_factunit_job": CREATE_JOB_BLRFACT_SQLSTR,
        "believer_plan_healerlink_job": CREATE_JOB_BLRHEAL_SQLSTR,
        "believer_plan_reason_caseunit_job": CREATE_JOB_BLRPREM_SQLSTR,
        "believer_plan_reasonunit_job": CREATE_JOB_BLRREAS_SQLSTR,
        "believer_plan_laborlink_job": CREATE_JOB_BLRLABO_SQLSTR,
        "believer_planunit_job": CREATE_JOB_BLRPLAN_SQLSTR,
        "believerunit_job": CREATE_JOB_BLRUNIT_SQLSTR,
    }


def create_job_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_job_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


CREATE_BELIEF_PARTNER_NETS_SQLSTR = "CREATE TABLE IF NOT EXISTS belief_partner_nets (belief_label TEXT, believer_name TEXT, believer_net_amount REAL)"
