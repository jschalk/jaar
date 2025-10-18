from sqlite3 import Connection as sqlite3_Connection
from src.ch01_py.db_toolbox import (
    create_table2table_agg_insert_query,
    create_update_inconsistency_error_query,
)
from src.ch17_idea.idea_config import get_idea_config_dict, get_quick_ideas_column_ref
from src.ch17_idea.idea_db_tool import create_idea_sorted_table, get_default_sorted_list

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
    "TRLTITL",
    "TRLNAME",
    "TRLROPE",
    "TRLLABE",
}


def get_dimen_abbv7(dimen: str) -> str:
    return {
        "moment_paybook": "BLFPAYY",
        "moment_budunit": "BLFBUDD",
        "moment_epoch_hour": "BLFHOUR",
        "moment_epoch_month": "BLFMONT",
        "moment_epoch_weekday": "BLFWEEK",
        "moment_timeoffi": "BLFOFFI",
        "momentunit": "BLFUNIT",
        "belief_voice_membership": "BLRMEMB",
        "belief_voiceunit": "BLRPERN",
        "belief_plan_awardunit": "BLRAWAR",
        "belief_plan_factunit": "BLRFACT",
        "belief_plan_healerunit": "BLRHEAL",
        "belief_plan_reason_caseunit": "BLRPREM",
        "belief_plan_reasonunit": "BLRREAS",
        "belief_plan_partyunit": "BLRLABO",
        "belief_planunit": "BLRPLAN",
        "beliefunit": "BLRUNIT",
        "translate_title": "TRLTITL",
        "translate_name": "TRLNAME",
        "translate_rope": "TRLROPE",
        "translate_label": "TRLLABE",
        "translate_core": "TRLCORE",
    }.get(dimen)


class prime_tablenameException(Exception):
    pass


def create_prime_tablename(
    idea_dimen_or_abbv7: str, phase: str, stage: str, put_del: str = None
) -> str:
    """
    phase must be one: 's', 'h', 'job'
    stage must be one: 'raw', 'agg', 'vld'
    """

    abbv_references = {
        "BLFPAYY": "moment_paybook",
        "BLFBUDD": "moment_budunit",
        "BLFHOUR": "moment_epoch_hour",
        "BLFMONT": "moment_epoch_month",
        "BLFWEEK": "moment_epoch_weekday",
        "BLFOFFI": "moment_timeoffi",
        "BLFUNIT": "momentunit",
        "BLRMEMB": "belief_voice_membership",
        "BLRPERN": "belief_voiceunit",
        "BLRAWAR": "belief_plan_awardunit",
        "BLRFACT": "belief_plan_factunit",
        "BLRGROU": "belief_groupunit",
        "BLRHEAL": "belief_plan_healerunit",
        "BLRPREM": "belief_plan_reason_caseunit",
        "BLRREAS": "belief_plan_reasonunit",
        "BLRLABO": "belief_plan_partyunit",
        "BLRPLAN": "belief_planunit",
        "BLRUNIT": "beliefunit",
        "TRLTITL": "translate_title",
        "TRLNAME": "translate_name",
        "TRLROPE": "translate_rope",
        "TRLLABE": "translate_label",
        "TRLCORE": "translate_core",
    }
    tablename = idea_dimen_or_abbv7
    if abbv_references.get(idea_dimen_or_abbv7.upper()):
        tablename = abbv_references.get(idea_dimen_or_abbv7.upper())
    if phase in {"s", "h", "job"}:
        tablename = f"{tablename}_{phase}"
    if stage is None:
        return tablename
    if stage not in {"raw", "agg", "vld"}:
        raise prime_tablenameException(f"'{stage}' is not a valid stage")

    return f"{tablename}_{put_del}_{stage}" if put_del else f"{tablename}_{stage}"


CREATE_TRLTITL_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLTITL_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_agg (spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLTITL_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_title_s_vld (spark_num INTEGER, face_name TEXT, otx_title TEXT, inx_title TEXT)"""
CREATE_TRLNAME_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLNAME_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_agg (spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLNAME_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_name_s_vld (spark_num INTEGER, face_name TEXT, otx_name TEXT, inx_name TEXT)"""
CREATE_TRLROPE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLROPE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_agg (spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLROPE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_rope_s_vld (spark_num INTEGER, face_name TEXT, otx_rope TEXT, inx_rope TEXT)"""
CREATE_TRLLABE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLLABE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_agg (spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLLABE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_label_s_vld (spark_num INTEGER, face_name TEXT, otx_label TEXT, inx_label TEXT)"""

CREATE_TRLCORE_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_raw (source_dimen TEXT, face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT, error_message TEXT)"""
CREATE_TRLCORE_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_agg (face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT)"""
CREATE_TRLCORE_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS translate_core_s_vld (face_name TEXT, otx_knot TEXT, inx_knot TEXT, unknown_str TEXT)"""

CREATE_BLFPAYY_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_BLFPAYY_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_BLFPAYY_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_s_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_BLFPAYY_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, voice_name_otx TEXT, voice_name_inx TEXT, tran_time INTEGER, amount REAL, error_message TEXT)"""
CREATE_BLFPAYY_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_paybook_h_agg (moment_label TEXT, belief_name TEXT, voice_name TEXT, tran_time INTEGER, amount REAL)"""
CREATE_BLFBUDD_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_BLFBUDD_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_BLFBUDD_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_s_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER)"""
CREATE_BLFBUDD_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER, error_message TEXT)"""
CREATE_BLFBUDD_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_budunit_h_agg (moment_label TEXT, belief_name TEXT, bud_time INTEGER, quota REAL, celldepth INTEGER)"""
CREATE_BLFHOUR_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, cumulative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_BLFHOUR_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, cumulative_minute INTEGER, hour_label TEXT, error_message TEXT)"""
CREATE_BLFHOUR_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_s_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, cumulative_minute INTEGER, hour_label TEXT)"""
CREATE_BLFHOUR_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, cumulative_minute INTEGER, hour_label_otx TEXT, hour_label_inx TEXT, error_message TEXT)"""
CREATE_BLFHOUR_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_hour_h_agg (moment_label TEXT, cumulative_minute INTEGER, hour_label TEXT)"""
CREATE_BLFMONT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, cumulative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_BLFMONT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, cumulative_day INTEGER, month_label TEXT, error_message TEXT)"""
CREATE_BLFMONT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_s_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, cumulative_day INTEGER, month_label TEXT)"""
CREATE_BLFMONT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, cumulative_day INTEGER, month_label_otx TEXT, month_label_inx TEXT, error_message TEXT)"""
CREATE_BLFMONT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_month_h_agg (moment_label TEXT, cumulative_day INTEGER, month_label TEXT)"""
CREATE_BLFWEEK_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_BLFWEEK_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, weekday_order INTEGER, weekday_label TEXT, error_message TEXT)"""
CREATE_BLFWEEK_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_s_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_BLFWEEK_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, weekday_order INTEGER, weekday_label_otx TEXT, weekday_label_inx TEXT, error_message TEXT)"""
CREATE_BLFWEEK_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_epoch_weekday_h_agg (moment_label TEXT, weekday_order INTEGER, weekday_label TEXT)"""
CREATE_BLFOFFI_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_BLFOFFI_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_BLFOFFI_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_s_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, offi_time INTEGER)"""
CREATE_BLFOFFI_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, offi_time INTEGER, error_message TEXT)"""
CREATE_BLFOFFI_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS moment_timeoffi_h_agg (moment_label TEXT, offi_time INTEGER)"""
CREATE_BLFUNIT_SOUND_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_BLFUNIT_SOUND_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_BLFUNIT_SOUND_VLD_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_s_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER)"""
CREATE_BLFUNIT_HEARD_RAW_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_h_raw (spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, epoch_label_otx TEXT, epoch_label_inx TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER, error_message TEXT)"""
CREATE_BLFUNIT_HEARD_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS momentunit_h_agg (moment_label TEXT, epoch_label TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_index INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL, knot TEXT, job_listen_rotations INTEGER)"""

CREATE_BLRMEMB_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, error_message TEXT)"
CREATE_BLRMEMB_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, error_message TEXT)"
CREATE_BLRMEMB_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL)"
CREATE_BLRMEMB_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title_ERASE TEXT)"
CREATE_BLRMEMB_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title_ERASE TEXT, error_message TEXT)"
CREATE_BLRMEMB_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title_ERASE TEXT)"
CREATE_BLRMEMB_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, voice_name_otx TEXT, voice_name_inx TEXT, group_title_otx TEXT, group_title_inx TEXT, group_cred_lumen REAL, group_debt_lumen REAL)"
CREATE_BLRMEMB_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL)"
CREATE_BLRMEMB_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, voice_name_otx TEXT, voice_name_inx TEXT, group_title_ERASE_otx TEXT, group_title_ERASE_inx TEXT)"
CREATE_BLRMEMB_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_voice_membership_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title_ERASE TEXT)"
CREATE_BLRPERN_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, voice_cred_lumen REAL, voice_debt_lumen REAL, error_message TEXT)"
CREATE_BLRPERN_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, voice_cred_lumen REAL, voice_debt_lumen REAL, error_message TEXT)"
CREATE_BLRPERN_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, voice_cred_lumen REAL, voice_debt_lumen REAL)"
CREATE_BLRPERN_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name_ERASE TEXT)"
CREATE_BLRPERN_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name_ERASE TEXT, error_message TEXT)"
CREATE_BLRPERN_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name_ERASE TEXT)"
CREATE_BLRPERN_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, voice_name_otx TEXT, voice_name_inx TEXT, voice_cred_lumen REAL, voice_debt_lumen REAL)"
CREATE_BLRPERN_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name TEXT, voice_cred_lumen REAL, voice_debt_lumen REAL)"
CREATE_BLRPERN_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, voice_name_ERASE_otx TEXT, voice_name_ERASE_inx TEXT)"
CREATE_BLRPERN_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_voiceunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, voice_name_ERASE TEXT)"
CREATE_BLRAWAR_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_BLRAWAR_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, error_message TEXT)"
CREATE_BLRAWAR_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BLRAWAR_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"
CREATE_BLRAWAR_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT, error_message TEXT)"
CREATE_BLRAWAR_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"
CREATE_BLRAWAR_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, awardee_title_otx TEXT, awardee_title_inx TEXT, give_force REAL, take_force REAL)"
CREATE_BLRAWAR_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL)"
CREATE_BLRAWAR_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, awardee_title_ERASE_otx TEXT, awardee_title_ERASE_inx TEXT)"
CREATE_BLRAWAR_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_awardunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title_ERASE TEXT)"
CREATE_BLRFACT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, error_message TEXT)"
CREATE_BLRFACT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL, error_message TEXT)"
CREATE_BLRFACT_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"
CREATE_BLRFACT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"
CREATE_BLRFACT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT, error_message TEXT)"
CREATE_BLRFACT_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"
CREATE_BLRFACT_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, fact_context_otx TEXT, fact_context_inx TEXT, fact_state_otx TEXT, fact_state_inx TEXT, fact_lower REAL, fact_upper REAL)"
CREATE_BLRFACT_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"
CREATE_BLRFACT_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, fact_context_ERASE_otx TEXT, fact_context_ERASE_inx TEXT)"
CREATE_BLRFACT_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_factunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context_ERASE TEXT)"
CREATE_BLRHEAL_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name TEXT, error_message TEXT)"
CREATE_BLRHEAL_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name TEXT, error_message TEXT)"
CREATE_BLRHEAL_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name TEXT)"
CREATE_BLRHEAL_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"
CREATE_BLRHEAL_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT, error_message TEXT)"
CREATE_BLRHEAL_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"
CREATE_BLRHEAL_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, healer_name_otx TEXT, healer_name_inx TEXT)"
CREATE_BLRHEAL_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name TEXT)"
CREATE_BLRHEAL_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, healer_name_ERASE_otx TEXT, healer_name_ERASE_inx TEXT)"
CREATE_BLRHEAL_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_healerunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name_ERASE TEXT)"
CREATE_BLRPREM_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER, error_message TEXT)"
CREATE_BLRPREM_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER, error_message TEXT)"
CREATE_BLRPREM_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER)"
CREATE_BLRPREM_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"
CREATE_BLRPREM_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT, error_message TEXT)"
CREATE_BLRPREM_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"
CREATE_BLRPREM_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_state_otx TEXT, reason_state_inx TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER)"
CREATE_BLRPREM_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER)"
CREATE_BLRPREM_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, reason_state_ERASE_otx TEXT, reason_state_ERASE_inx TEXT)"
CREATE_BLRPREM_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state_ERASE TEXT)"
CREATE_BLRREAS_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, error_message TEXT)"
CREATE_BLRREAS_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, error_message TEXT)"
CREATE_BLRREAS_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER)"
CREATE_BLRREAS_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"
CREATE_BLRREAS_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT, error_message TEXT)"
CREATE_BLRREAS_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"
CREATE_BLRREAS_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_otx TEXT, reason_context_inx TEXT, active_requisite INTEGER)"
CREATE_BLRREAS_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER)"
CREATE_BLRREAS_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, reason_context_ERASE_otx TEXT, reason_context_ERASE_inx TEXT)"
CREATE_BLRREAS_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context_ERASE TEXT)"
CREATE_BLRLABO_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title TEXT, solo INTEGER, error_message TEXT)"
CREATE_BLRLABO_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title TEXT, solo INTEGER, error_message TEXT)"
CREATE_BLRLABO_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title TEXT, solo INTEGER)"
CREATE_BLRLABO_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title_ERASE TEXT)"
CREATE_BLRLABO_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title_ERASE TEXT, error_message TEXT)"
CREATE_BLRLABO_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title_ERASE TEXT)"
CREATE_BLRLABO_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, party_title_otx TEXT, party_title_inx TEXT, solo INTEGER)"
CREATE_BLRLABO_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title TEXT, solo INTEGER)"
CREATE_BLRLABO_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, party_title_ERASE_otx TEXT, party_title_ERASE_inx TEXT)"
CREATE_BLRLABO_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_plan_partyunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title_ERASE TEXT)"
CREATE_BLRPLAN_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_BLRPLAN_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"
CREATE_BLRPLAN_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BLRPLAN_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope_ERASE TEXT)"
CREATE_BLRPLAN_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope_ERASE TEXT, error_message TEXT)"
CREATE_BLRPLAN_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope_ERASE TEXT)"
CREATE_BLRPLAN_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_otx TEXT, plan_rope_inx TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BLRPLAN_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER)"
CREATE_BLRPLAN_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, plan_rope_ERASE_otx TEXT, plan_rope_ERASE_inx TEXT)"
CREATE_BLRPLAN_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS belief_planunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, plan_rope_ERASE TEXT)"
CREATE_BLRUNIT_SOUND_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS beliefunit_s_put_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL, error_message TEXT)"
CREATE_BLRUNIT_SOUND_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS beliefunit_s_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL, error_message TEXT)"
CREATE_BLRUNIT_SOUND_PUT_VLD_STR = "CREATE TABLE IF NOT EXISTS beliefunit_s_put_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL)"
CREATE_BLRUNIT_SOUND_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS beliefunit_s_del_raw (idea_number TEXT, spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name_ERASE TEXT)"
CREATE_BLRUNIT_SOUND_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS beliefunit_s_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name_ERASE TEXT, error_message TEXT)"
CREATE_BLRUNIT_SOUND_DEL_VLD_STR = "CREATE TABLE IF NOT EXISTS beliefunit_s_del_vld (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name_ERASE TEXT)"
CREATE_BLRUNIT_HEARD_PUT_RAW_STR = "CREATE TABLE IF NOT EXISTS beliefunit_h_put_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_otx TEXT, belief_name_inx TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL)"
CREATE_BLRUNIT_HEARD_PUT_AGG_STR = "CREATE TABLE IF NOT EXISTS beliefunit_h_put_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL)"
CREATE_BLRUNIT_HEARD_DEL_RAW_STR = "CREATE TABLE IF NOT EXISTS beliefunit_h_del_raw (translate_spark_num INTEGER, spark_num INTEGER, face_name_otx TEXT, face_name_inx TEXT, moment_label_otx TEXT, moment_label_inx TEXT, belief_name_ERASE_otx TEXT, belief_name_ERASE_inx TEXT)"
CREATE_BLRUNIT_HEARD_DEL_AGG_STR = "CREATE TABLE IF NOT EXISTS beliefunit_h_del_agg (spark_num INTEGER, face_name TEXT, moment_label TEXT, belief_name_ERASE TEXT)"


def get_prime_create_table_sqlstrs() -> dict[str, str]:
    return {
        "translate_title_s_raw": CREATE_TRLTITL_SOUND_RAW_SQLSTR,
        "translate_title_s_agg": CREATE_TRLTITL_SOUND_AGG_SQLSTR,
        "translate_title_s_vld": CREATE_TRLTITL_SOUND_VLD_SQLSTR,
        "translate_name_s_raw": CREATE_TRLNAME_SOUND_RAW_SQLSTR,
        "translate_name_s_agg": CREATE_TRLNAME_SOUND_AGG_SQLSTR,
        "translate_name_s_vld": CREATE_TRLNAME_SOUND_VLD_SQLSTR,
        "translate_rope_s_raw": CREATE_TRLROPE_SOUND_RAW_SQLSTR,
        "translate_rope_s_agg": CREATE_TRLROPE_SOUND_AGG_SQLSTR,
        "translate_rope_s_vld": CREATE_TRLROPE_SOUND_VLD_SQLSTR,
        "translate_label_s_raw": CREATE_TRLLABE_SOUND_RAW_SQLSTR,
        "translate_label_s_agg": CREATE_TRLLABE_SOUND_AGG_SQLSTR,
        "translate_label_s_vld": CREATE_TRLLABE_SOUND_VLD_SQLSTR,
        "translate_core_s_raw": CREATE_TRLCORE_SOUND_RAW_SQLSTR,
        "translate_core_s_agg": CREATE_TRLCORE_SOUND_AGG_SQLSTR,
        "translate_core_s_vld": CREATE_TRLCORE_SOUND_VLD_SQLSTR,
        "moment_paybook_s_raw": CREATE_BLFPAYY_SOUND_RAW_SQLSTR,
        "moment_paybook_s_agg": CREATE_BLFPAYY_SOUND_AGG_SQLSTR,
        "moment_paybook_s_vld": CREATE_BLFPAYY_SOUND_VLD_SQLSTR,
        "moment_paybook_h_raw": CREATE_BLFPAYY_HEARD_RAW_SQLSTR,
        "moment_paybook_h_agg": CREATE_BLFPAYY_HEARD_AGG_SQLSTR,
        "moment_budunit_s_raw": CREATE_BLFBUDD_SOUND_RAW_SQLSTR,
        "moment_budunit_s_agg": CREATE_BLFBUDD_SOUND_AGG_SQLSTR,
        "moment_budunit_s_vld": CREATE_BLFBUDD_SOUND_VLD_SQLSTR,
        "moment_budunit_h_raw": CREATE_BLFBUDD_HEARD_RAW_SQLSTR,
        "moment_budunit_h_agg": CREATE_BLFBUDD_HEARD_AGG_SQLSTR,
        "moment_epoch_hour_s_raw": CREATE_BLFHOUR_SOUND_RAW_SQLSTR,
        "moment_epoch_hour_s_agg": CREATE_BLFHOUR_SOUND_AGG_SQLSTR,
        "moment_epoch_hour_s_vld": CREATE_BLFHOUR_SOUND_VLD_SQLSTR,
        "moment_epoch_hour_h_raw": CREATE_BLFHOUR_HEARD_RAW_SQLSTR,
        "moment_epoch_hour_h_agg": CREATE_BLFHOUR_HEARD_AGG_SQLSTR,
        "moment_epoch_month_s_raw": CREATE_BLFMONT_SOUND_RAW_SQLSTR,
        "moment_epoch_month_s_agg": CREATE_BLFMONT_SOUND_AGG_SQLSTR,
        "moment_epoch_month_s_vld": CREATE_BLFMONT_SOUND_VLD_SQLSTR,
        "moment_epoch_month_h_raw": CREATE_BLFMONT_HEARD_RAW_SQLSTR,
        "moment_epoch_month_h_agg": CREATE_BLFMONT_HEARD_AGG_SQLSTR,
        "moment_epoch_weekday_s_raw": CREATE_BLFWEEK_SOUND_RAW_SQLSTR,
        "moment_epoch_weekday_s_agg": CREATE_BLFWEEK_SOUND_AGG_SQLSTR,
        "moment_epoch_weekday_s_vld": CREATE_BLFWEEK_SOUND_VLD_SQLSTR,
        "moment_epoch_weekday_h_raw": CREATE_BLFWEEK_HEARD_RAW_SQLSTR,
        "moment_epoch_weekday_h_agg": CREATE_BLFWEEK_HEARD_AGG_SQLSTR,
        "moment_timeoffi_s_raw": CREATE_BLFOFFI_SOUND_RAW_SQLSTR,
        "moment_timeoffi_s_agg": CREATE_BLFOFFI_SOUND_AGG_SQLSTR,
        "moment_timeoffi_s_vld": CREATE_BLFOFFI_SOUND_VLD_SQLSTR,
        "moment_timeoffi_h_raw": CREATE_BLFOFFI_HEARD_RAW_SQLSTR,
        "moment_timeoffi_h_agg": CREATE_BLFOFFI_HEARD_AGG_SQLSTR,
        "momentunit_s_raw": CREATE_BLFUNIT_SOUND_RAW_SQLSTR,
        "momentunit_s_agg": CREATE_BLFUNIT_SOUND_AGG_SQLSTR,
        "momentunit_s_vld": CREATE_BLFUNIT_SOUND_VLD_SQLSTR,
        "momentunit_h_raw": CREATE_BLFUNIT_HEARD_RAW_SQLSTR,
        "momentunit_h_agg": CREATE_BLFUNIT_HEARD_AGG_SQLSTR,
        "belief_voice_membership_s_put_raw": CREATE_BLRMEMB_SOUND_PUT_RAW_STR,
        "belief_voice_membership_s_put_agg": CREATE_BLRMEMB_SOUND_PUT_AGG_STR,
        "belief_voice_membership_s_put_vld": CREATE_BLRMEMB_SOUND_PUT_VLD_STR,
        "belief_voice_membership_s_del_raw": CREATE_BLRMEMB_SOUND_DEL_RAW_STR,
        "belief_voice_membership_s_del_agg": CREATE_BLRMEMB_SOUND_DEL_AGG_STR,
        "belief_voice_membership_s_del_vld": CREATE_BLRMEMB_SOUND_DEL_VLD_STR,
        "belief_voice_membership_h_put_raw": CREATE_BLRMEMB_HEARD_PUT_RAW_STR,
        "belief_voice_membership_h_put_agg": CREATE_BLRMEMB_HEARD_PUT_AGG_STR,
        "belief_voice_membership_h_del_raw": CREATE_BLRMEMB_HEARD_DEL_RAW_STR,
        "belief_voice_membership_h_del_agg": CREATE_BLRMEMB_HEARD_DEL_AGG_STR,
        "belief_voiceunit_s_put_raw": CREATE_BLRPERN_SOUND_PUT_RAW_STR,
        "belief_voiceunit_s_put_agg": CREATE_BLRPERN_SOUND_PUT_AGG_STR,
        "belief_voiceunit_s_put_vld": CREATE_BLRPERN_SOUND_PUT_VLD_STR,
        "belief_voiceunit_s_del_raw": CREATE_BLRPERN_SOUND_DEL_RAW_STR,
        "belief_voiceunit_s_del_agg": CREATE_BLRPERN_SOUND_DEL_AGG_STR,
        "belief_voiceunit_s_del_vld": CREATE_BLRPERN_SOUND_DEL_VLD_STR,
        "belief_voiceunit_h_put_raw": CREATE_BLRPERN_HEARD_PUT_RAW_STR,
        "belief_voiceunit_h_put_agg": CREATE_BLRPERN_HEARD_PUT_AGG_STR,
        "belief_voiceunit_h_del_raw": CREATE_BLRPERN_HEARD_DEL_RAW_STR,
        "belief_voiceunit_h_del_agg": CREATE_BLRPERN_HEARD_DEL_AGG_STR,
        "belief_plan_awardunit_s_put_raw": CREATE_BLRAWAR_SOUND_PUT_RAW_STR,
        "belief_plan_awardunit_s_put_agg": CREATE_BLRAWAR_SOUND_PUT_AGG_STR,
        "belief_plan_awardunit_s_put_vld": CREATE_BLRAWAR_SOUND_PUT_VLD_STR,
        "belief_plan_awardunit_s_del_raw": CREATE_BLRAWAR_SOUND_DEL_RAW_STR,
        "belief_plan_awardunit_s_del_agg": CREATE_BLRAWAR_SOUND_DEL_AGG_STR,
        "belief_plan_awardunit_s_del_vld": CREATE_BLRAWAR_SOUND_DEL_VLD_STR,
        "belief_plan_awardunit_h_put_raw": CREATE_BLRAWAR_HEARD_PUT_RAW_STR,
        "belief_plan_awardunit_h_put_agg": CREATE_BLRAWAR_HEARD_PUT_AGG_STR,
        "belief_plan_awardunit_h_del_raw": CREATE_BLRAWAR_HEARD_DEL_RAW_STR,
        "belief_plan_awardunit_h_del_agg": CREATE_BLRAWAR_HEARD_DEL_AGG_STR,
        "belief_plan_factunit_s_put_raw": CREATE_BLRFACT_SOUND_PUT_RAW_STR,
        "belief_plan_factunit_s_put_agg": CREATE_BLRFACT_SOUND_PUT_AGG_STR,
        "belief_plan_factunit_s_put_vld": CREATE_BLRFACT_SOUND_PUT_VLD_STR,
        "belief_plan_factunit_s_del_raw": CREATE_BLRFACT_SOUND_DEL_RAW_STR,
        "belief_plan_factunit_s_del_agg": CREATE_BLRFACT_SOUND_DEL_AGG_STR,
        "belief_plan_factunit_s_del_vld": CREATE_BLRFACT_SOUND_DEL_VLD_STR,
        "belief_plan_factunit_h_put_raw": CREATE_BLRFACT_HEARD_PUT_RAW_STR,
        "belief_plan_factunit_h_put_agg": CREATE_BLRFACT_HEARD_PUT_AGG_STR,
        "belief_plan_factunit_h_del_raw": CREATE_BLRFACT_HEARD_DEL_RAW_STR,
        "belief_plan_factunit_h_del_agg": CREATE_BLRFACT_HEARD_DEL_AGG_STR,
        "belief_plan_healerunit_s_put_raw": CREATE_BLRHEAL_SOUND_PUT_RAW_STR,
        "belief_plan_healerunit_s_put_agg": CREATE_BLRHEAL_SOUND_PUT_AGG_STR,
        "belief_plan_healerunit_s_put_vld": CREATE_BLRHEAL_SOUND_PUT_VLD_STR,
        "belief_plan_healerunit_s_del_raw": CREATE_BLRHEAL_SOUND_DEL_RAW_STR,
        "belief_plan_healerunit_s_del_agg": CREATE_BLRHEAL_SOUND_DEL_AGG_STR,
        "belief_plan_healerunit_s_del_vld": CREATE_BLRHEAL_SOUND_DEL_VLD_STR,
        "belief_plan_healerunit_h_put_raw": CREATE_BLRHEAL_HEARD_PUT_RAW_STR,
        "belief_plan_healerunit_h_put_agg": CREATE_BLRHEAL_HEARD_PUT_AGG_STR,
        "belief_plan_healerunit_h_del_raw": CREATE_BLRHEAL_HEARD_DEL_RAW_STR,
        "belief_plan_healerunit_h_del_agg": CREATE_BLRHEAL_HEARD_DEL_AGG_STR,
        "belief_plan_reason_caseunit_s_put_raw": CREATE_BLRPREM_SOUND_PUT_RAW_STR,
        "belief_plan_reason_caseunit_s_put_agg": CREATE_BLRPREM_SOUND_PUT_AGG_STR,
        "belief_plan_reason_caseunit_s_put_vld": CREATE_BLRPREM_SOUND_PUT_VLD_STR,
        "belief_plan_reason_caseunit_s_del_raw": CREATE_BLRPREM_SOUND_DEL_RAW_STR,
        "belief_plan_reason_caseunit_s_del_agg": CREATE_BLRPREM_SOUND_DEL_AGG_STR,
        "belief_plan_reason_caseunit_s_del_vld": CREATE_BLRPREM_SOUND_DEL_VLD_STR,
        "belief_plan_reason_caseunit_h_put_raw": CREATE_BLRPREM_HEARD_PUT_RAW_STR,
        "belief_plan_reason_caseunit_h_put_agg": CREATE_BLRPREM_HEARD_PUT_AGG_STR,
        "belief_plan_reason_caseunit_h_del_raw": CREATE_BLRPREM_HEARD_DEL_RAW_STR,
        "belief_plan_reason_caseunit_h_del_agg": CREATE_BLRPREM_HEARD_DEL_AGG_STR,
        "belief_plan_reasonunit_s_put_raw": CREATE_BLRREAS_SOUND_PUT_RAW_STR,
        "belief_plan_reasonunit_s_put_agg": CREATE_BLRREAS_SOUND_PUT_AGG_STR,
        "belief_plan_reasonunit_s_put_vld": CREATE_BLRREAS_SOUND_PUT_VLD_STR,
        "belief_plan_reasonunit_s_del_raw": CREATE_BLRREAS_SOUND_DEL_RAW_STR,
        "belief_plan_reasonunit_s_del_agg": CREATE_BLRREAS_SOUND_DEL_AGG_STR,
        "belief_plan_reasonunit_s_del_vld": CREATE_BLRREAS_SOUND_DEL_VLD_STR,
        "belief_plan_reasonunit_h_put_raw": CREATE_BLRREAS_HEARD_PUT_RAW_STR,
        "belief_plan_reasonunit_h_put_agg": CREATE_BLRREAS_HEARD_PUT_AGG_STR,
        "belief_plan_reasonunit_h_del_raw": CREATE_BLRREAS_HEARD_DEL_RAW_STR,
        "belief_plan_reasonunit_h_del_agg": CREATE_BLRREAS_HEARD_DEL_AGG_STR,
        "belief_plan_partyunit_s_put_raw": CREATE_BLRLABO_SOUND_PUT_RAW_STR,
        "belief_plan_partyunit_s_put_agg": CREATE_BLRLABO_SOUND_PUT_AGG_STR,
        "belief_plan_partyunit_s_put_vld": CREATE_BLRLABO_SOUND_PUT_VLD_STR,
        "belief_plan_partyunit_s_del_raw": CREATE_BLRLABO_SOUND_DEL_RAW_STR,
        "belief_plan_partyunit_s_del_agg": CREATE_BLRLABO_SOUND_DEL_AGG_STR,
        "belief_plan_partyunit_s_del_vld": CREATE_BLRLABO_SOUND_DEL_VLD_STR,
        "belief_plan_partyunit_h_put_raw": CREATE_BLRLABO_HEARD_PUT_RAW_STR,
        "belief_plan_partyunit_h_put_agg": CREATE_BLRLABO_HEARD_PUT_AGG_STR,
        "belief_plan_partyunit_h_del_raw": CREATE_BLRLABO_HEARD_DEL_RAW_STR,
        "belief_plan_partyunit_h_del_agg": CREATE_BLRLABO_HEARD_DEL_AGG_STR,
        "belief_planunit_s_put_raw": CREATE_BLRPLAN_SOUND_PUT_RAW_STR,
        "belief_planunit_s_put_agg": CREATE_BLRPLAN_SOUND_PUT_AGG_STR,
        "belief_planunit_s_put_vld": CREATE_BLRPLAN_SOUND_PUT_VLD_STR,
        "belief_planunit_s_del_raw": CREATE_BLRPLAN_SOUND_DEL_RAW_STR,
        "belief_planunit_s_del_agg": CREATE_BLRPLAN_SOUND_DEL_AGG_STR,
        "belief_planunit_s_del_vld": CREATE_BLRPLAN_SOUND_DEL_VLD_STR,
        "belief_planunit_h_put_raw": CREATE_BLRPLAN_HEARD_PUT_RAW_STR,
        "belief_planunit_h_put_agg": CREATE_BLRPLAN_HEARD_PUT_AGG_STR,
        "belief_planunit_h_del_raw": CREATE_BLRPLAN_HEARD_DEL_RAW_STR,
        "belief_planunit_h_del_agg": CREATE_BLRPLAN_HEARD_DEL_AGG_STR,
        "beliefunit_s_put_raw": CREATE_BLRUNIT_SOUND_PUT_RAW_STR,
        "beliefunit_s_put_agg": CREATE_BLRUNIT_SOUND_PUT_AGG_STR,
        "beliefunit_s_put_vld": CREATE_BLRUNIT_SOUND_PUT_VLD_STR,
        "beliefunit_s_del_raw": CREATE_BLRUNIT_SOUND_DEL_RAW_STR,
        "beliefunit_s_del_agg": CREATE_BLRUNIT_SOUND_DEL_AGG_STR,
        "beliefunit_s_del_vld": CREATE_BLRUNIT_SOUND_DEL_VLD_STR,
        "beliefunit_h_put_raw": CREATE_BLRUNIT_HEARD_PUT_RAW_STR,
        "beliefunit_h_put_agg": CREATE_BLRUNIT_HEARD_PUT_AGG_STR,
        "beliefunit_h_del_raw": CREATE_BLRUNIT_HEARD_DEL_RAW_STR,
        "beliefunit_h_del_agg": CREATE_BLRUNIT_HEARD_DEL_AGG_STR,
    }


def get_moment_belief_sound_agg_tablenames():
    return {
        "belief_voice_membership_s_del_agg",
        "belief_voice_membership_s_put_agg",
        "belief_voiceunit_s_del_agg",
        "belief_voiceunit_s_put_agg",
        "belief_plan_awardunit_s_del_agg",
        "belief_plan_awardunit_s_put_agg",
        "belief_plan_factunit_s_del_agg",
        "belief_plan_factunit_s_put_agg",
        "belief_plan_healerunit_s_del_agg",
        "belief_plan_healerunit_s_put_agg",
        "belief_plan_partyunit_s_del_agg",
        "belief_plan_partyunit_s_put_agg",
        "belief_plan_reason_caseunit_s_del_agg",
        "belief_plan_reason_caseunit_s_put_agg",
        "belief_plan_reasonunit_s_del_agg",
        "belief_plan_reasonunit_s_put_agg",
        "belief_planunit_s_del_agg",
        "belief_planunit_s_put_agg",
        "beliefunit_s_del_agg",
        "beliefunit_s_put_agg",
        "moment_paybook_s_agg",
        "moment_budunit_s_agg",
        "moment_epoch_hour_s_agg",
        "moment_epoch_month_s_agg",
        "moment_epoch_weekday_s_agg",
        "moment_timeoffi_s_agg",
        "momentunit_s_agg",
    }


def get_belief_heard_agg_tablenames() -> set[str]:
    return {
        "beliefunit_h_put_agg",
        "belief_plan_healerunit_h_put_agg",
        "belief_voiceunit_h_put_agg",
        "belief_plan_reason_caseunit_h_put_agg",
        "belief_plan_partyunit_h_put_agg",
        "belief_plan_reasonunit_h_put_agg",
        "belief_plan_factunit_h_put_agg",
        "belief_voice_membership_h_put_agg",
        "belief_planunit_h_put_agg",
        "belief_plan_awardunit_h_put_agg",
    }


def create_sound_and_heard_tables(conn_or_cursor: sqlite3_Connection):
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
    if dimen.lower().startswith("moment"):
        exclude_cols = {"idea_number", "spark_num", "face_name", "error_message"}
    else:
        exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("belief"):
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

    if dimen.lower().startswith("moment"):
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
    exclude_cols = {"idea_number", "error_message"}
    if dimen.lower().startswith("belief"):
        agg_tablename = create_prime_tablename(dimen, "s", "agg", "put")
        raw_tablename = create_prime_tablename(dimen, "s", "raw", "put")
    else:
        raw_tablename = create_prime_tablename(dimen, "s", "raw")
        agg_tablename = create_prime_tablename(dimen, "s", "agg")

    translate_moment_belief_put_sqlstr = create_table2table_agg_insert_query(
        conn_or_cursor,
        src_table=raw_tablename,
        dst_table=agg_tablename,
        focus_cols=dimen_focus_columns,
        exclude_cols=exclude_cols,
        where_block="WHERE error_message IS NULL",
    )
    sqlstrs = [translate_moment_belief_put_sqlstr]
    if dimen.lower().startswith("belief"):
        del_raw_tablename = create_prime_tablename(dimen, "s", "raw", "del")
        del_agg_tablename = create_prime_tablename(dimen, "s", "agg", "del")
        dimen_focus_columns = get_default_sorted_list(set(dimen_focus_columns))
        last_element = dimen_focus_columns.pop(-1)
        dimen_focus_columns.append(f"{last_element}_ERASE")
        belief_del_sqlstr = create_table2table_agg_insert_query(
            conn_or_cursor,
            src_table=del_raw_tablename,
            dst_table=del_agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
            where_block="",
        )
        sqlstrs.append(belief_del_sqlstr)

    return sqlstrs


def create_insert_into_translate_core_raw_sqlstr(dimen: str) -> str:
    translate_core_s_raw_tablename = create_prime_tablename("trlcore", "s", "raw")
    translate_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    return f"""INSERT INTO {translate_core_s_raw_tablename} (source_dimen, face_name, otx_knot, inx_knot, unknown_str)
SELECT '{translate_s_agg_tablename}', face_name, otx_knot, inx_knot, unknown_str
FROM {translate_s_agg_tablename}
GROUP BY face_name, otx_knot, inx_knot, unknown_str
;
"""


def create_insert_translate_core_agg_into_vld_sqlstr(
    default_knot: str, default_unknown: str
):
    return f"""INSERT INTO translate_core_s_vld (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  face_name
, IFNULL(otx_knot, '{default_knot}')
, IFNULL(inx_knot, '{default_knot}')
, IFNULL(unknown_str, '{default_unknown}')
FROM translate_core_s_agg
;
"""


def create_insert_missing_face_name_into_translate_core_vld_sqlstr(
    default_knot: str, default_unknown: str, moment_belief_sound_agg_tablename: str
):
    return f"""INSERT INTO translate_core_s_vld (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  {moment_belief_sound_agg_tablename}.face_name
, '{default_knot}'
, '{default_knot}'
, '{default_unknown}'
FROM {moment_belief_sound_agg_tablename} 
LEFT JOIN translate_core_s_vld ON translate_core_s_vld.face_name = {moment_belief_sound_agg_tablename}.face_name
WHERE translate_core_s_vld.face_name IS NULL
GROUP BY {moment_belief_sound_agg_tablename}.face_name
;
"""


def create_update_translate_sound_agg_inconsist_sqlstr(dimen: str) -> str:
    translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    translate_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    return f"""UPDATE {translate_s_agg_tablename}
SET error_message = 'Inconsistent translate core data'
WHERE face_name IN (
    SELECT {translate_s_agg_tablename}.face_name
    FROM {translate_s_agg_tablename} 
    LEFT JOIN {translate_core_s_vld_tablename} ON {translate_core_s_vld_tablename}.face_name = {translate_s_agg_tablename}.face_name
    WHERE {translate_core_s_vld_tablename}.face_name IS NULL
)
;
"""


def create_update_trllabe_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    trllabe_s_agg_tablename = create_prime_tablename("trllabe", "s", "agg")
    return f"""UPDATE {trllabe_s_agg_tablename}
SET error_message = 'Knot cannot exist in LabelTerm'
WHERE rowid IN (
    SELECT label_agg.rowid
    FROM {trllabe_s_agg_tablename} label_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = label_agg.face_name
    WHERE label_agg.otx_label LIKE '%' || core_vld.otx_knot || '%'
      OR label_agg.inx_label LIKE '%' || core_vld.inx_knot || '%'
)
;
"""


def create_update_trlrope_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    trlrope_s_agg_tablename = create_prime_tablename("trlrope", "s", "agg")
    return f"""UPDATE {trlrope_s_agg_tablename}
SET error_message = 'Knot must exist in RopeTerm'
WHERE rowid IN (
    SELECT rope_agg.rowid
    FROM {trlrope_s_agg_tablename} rope_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = rope_agg.face_name
    WHERE NOT rope_agg.otx_rope LIKE core_vld.otx_knot || '%'
        OR NOT rope_agg.inx_rope LIKE core_vld.inx_knot || '%'
)
;
"""


def create_update_trlname_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    trlname_s_agg_tablename = create_prime_tablename("trlname", "s", "agg")
    return f"""UPDATE {trlname_s_agg_tablename}
SET error_message = 'Knot cannot exist in NameTerm'
WHERE rowid IN (
    SELECT name_agg.rowid
    FROM {trlname_s_agg_tablename} name_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = name_agg.face_name
    WHERE name_agg.otx_name LIKE '%' || core_vld.otx_knot || '%'
      OR name_agg.inx_name LIKE '%' || core_vld.inx_knot || '%'
)
;
"""


def create_update_trltitl_sound_agg_knot_error_sqlstr() -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    trltitl_s_agg_tablename = create_prime_tablename("trltitl", "s", "agg")
    return f"""UPDATE {trltitl_s_agg_tablename}
SET error_message = 'Otx and inx titles must match knot.'
WHERE rowid IN (
  SELECT title_agg.rowid
  FROM {trltitl_s_agg_tablename} title_agg
  JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = title_agg.face_name
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


def create_insert_translate_sound_vld_table_sqlstr(dimen: str) -> str:
    translate_s_agg_tablename = create_prime_tablename(dimen, "s", "agg")
    translate_s_vld_tablename = create_prime_tablename(dimen, "s", "vld")
    dimen_otx_inx_obj_names = {
        "translate_name": "name",
        "translate_title": "title",
        "translate_label": "label",
        "translate_rope": "rope",
    }
    otx_str = f"otx_{dimen_otx_inx_obj_names.get(dimen, dimen)}"
    inx_str = f"inx_{dimen_otx_inx_obj_names.get(dimen, dimen)}"
    return f"""
INSERT INTO {translate_s_vld_tablename} (spark_num, face_name, {otx_str}, {inx_str})
SELECT spark_num, face_name, MAX({otx_str}), MAX({inx_str})
FROM {translate_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY spark_num, face_name
;
"""


def create_knot_exists_in_name_error_update_sqlstr(table: str, column: str) -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    return f"""UPDATE {table}
SET error_message = 'Knot cannot exist in NameTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_knot || '%'
)
;
"""


def create_knot_exists_in_label_error_update_sqlstr(table: str, column: str) -> str:
    trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
    return f"""UPDATE {table}
SET error_message = 'Knot cannot exist in LabelTerm column {column}'
WHERE rowid IN (
    SELECT sound_agg.rowid
    FROM {table} sound_agg
    JOIN {trlcore_s_vld_tablename} core_vld ON core_vld.face_name = sound_agg.face_name
    WHERE sound_agg.{column} LIKE '%' || core_vld.otx_knot || '%'
)
;
"""


INSERT_BLRMEMB_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_voice_membership_s_put_vld (spark_num, face_name, moment_label, belief_name, voice_name, group_title, group_cred_lumen, group_debt_lumen) SELECT spark_num, face_name, moment_label, belief_name, voice_name, group_title, group_cred_lumen, group_debt_lumen FROM belief_voice_membership_s_put_agg WHERE error_message IS NULL"
INSERT_BLRMEMB_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_voice_membership_s_del_vld (spark_num, face_name, moment_label, belief_name, voice_name, group_title_ERASE) SELECT spark_num, face_name, moment_label, belief_name, voice_name, group_title_ERASE FROM belief_voice_membership_s_del_agg WHERE error_message IS NULL"
INSERT_BLRPERN_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_voiceunit_s_put_vld (spark_num, face_name, moment_label, belief_name, voice_name, voice_cred_lumen, voice_debt_lumen) SELECT spark_num, face_name, moment_label, belief_name, voice_name, voice_cred_lumen, voice_debt_lumen FROM belief_voiceunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRPERN_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_voiceunit_s_del_vld (spark_num, face_name, moment_label, belief_name, voice_name_ERASE) SELECT spark_num, face_name, moment_label, belief_name, voice_name_ERASE FROM belief_voiceunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRAWAR_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_plan_awardunit_s_put_vld (spark_num, face_name, moment_label, belief_name, plan_rope, awardee_title, give_force, take_force) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, awardee_title, give_force, take_force FROM belief_plan_awardunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRAWAR_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_plan_awardunit_s_del_vld (spark_num, face_name, moment_label, belief_name, plan_rope, awardee_title_ERASE) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, awardee_title_ERASE FROM belief_plan_awardunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRFACT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_plan_factunit_s_put_vld (spark_num, face_name, moment_label, belief_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper FROM belief_plan_factunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRFACT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_plan_factunit_s_del_vld (spark_num, face_name, moment_label, belief_name, plan_rope, fact_context_ERASE) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, fact_context_ERASE FROM belief_plan_factunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRHEAL_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_plan_healerunit_s_put_vld (spark_num, face_name, moment_label, belief_name, plan_rope, healer_name) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, healer_name FROM belief_plan_healerunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRHEAL_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_plan_healerunit_s_del_vld (spark_num, face_name, moment_label, belief_name, plan_rope, healer_name_ERASE) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, healer_name_ERASE FROM belief_plan_healerunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRPREM_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_plan_reason_caseunit_s_put_vld (spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor FROM belief_plan_reason_caseunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRPREM_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_plan_reason_caseunit_s_del_vld (spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, reason_state_ERASE) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, reason_state_ERASE FROM belief_plan_reason_caseunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRREAS_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_plan_reasonunit_s_put_vld (spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, active_requisite) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, active_requisite FROM belief_plan_reasonunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRREAS_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_plan_reasonunit_s_del_vld (spark_num, face_name, moment_label, belief_name, plan_rope, reason_context_ERASE) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, reason_context_ERASE FROM belief_plan_reasonunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRLABO_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_plan_partyunit_s_put_vld (spark_num, face_name, moment_label, belief_name, plan_rope, party_title, solo) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, party_title, solo FROM belief_plan_partyunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRLABO_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_plan_partyunit_s_del_vld (spark_num, face_name, moment_label, belief_name, plan_rope, party_title_ERASE) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, party_title_ERASE FROM belief_plan_partyunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRPLAN_SOUND_VLD_PUT_SQLSTR = "INSERT INTO belief_planunit_s_put_vld (spark_num, face_name, moment_label, belief_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool FROM belief_planunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRPLAN_SOUND_VLD_DEL_SQLSTR = "INSERT INTO belief_planunit_s_del_vld (spark_num, face_name, moment_label, belief_name, plan_rope_ERASE) SELECT spark_num, face_name, moment_label, belief_name, plan_rope_ERASE FROM belief_planunit_s_del_agg WHERE error_message IS NULL"
INSERT_BLRUNIT_SOUND_VLD_PUT_SQLSTR = "INSERT INTO beliefunit_s_put_vld (spark_num, face_name, moment_label, belief_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_grain, money_grain, respect_grain) SELECT spark_num, face_name, moment_label, belief_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_grain, money_grain, respect_grain FROM beliefunit_s_put_agg WHERE error_message IS NULL"
INSERT_BLRUNIT_SOUND_VLD_DEL_SQLSTR = "INSERT INTO beliefunit_s_del_vld (spark_num, face_name, moment_label, belief_name_ERASE) SELECT spark_num, face_name, moment_label, belief_name_ERASE FROM beliefunit_s_del_agg WHERE error_message IS NULL"

INSERT_BLFPAYY_SOUND_VLD_SQLSTR = "INSERT INTO moment_paybook_s_vld (spark_num, face_name, moment_label, belief_name, voice_name, tran_time, amount) SELECT spark_num, face_name, moment_label, belief_name, voice_name, tran_time, amount FROM moment_paybook_s_agg WHERE error_message IS NULL"
INSERT_BLFBUDD_SOUND_VLD_SQLSTR = "INSERT INTO moment_budunit_s_vld (spark_num, face_name, moment_label, belief_name, bud_time, quota, celldepth) SELECT spark_num, face_name, moment_label, belief_name, bud_time, quota, celldepth FROM moment_budunit_s_agg WHERE error_message IS NULL"
INSERT_BLFHOUR_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_hour_s_vld (spark_num, face_name, moment_label, cumulative_minute, hour_label) SELECT spark_num, face_name, moment_label, cumulative_minute, hour_label FROM moment_epoch_hour_s_agg WHERE error_message IS NULL"
INSERT_BLFMONT_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_month_s_vld (spark_num, face_name, moment_label, cumulative_day, month_label) SELECT spark_num, face_name, moment_label, cumulative_day, month_label FROM moment_epoch_month_s_agg WHERE error_message IS NULL"
INSERT_BLFWEEK_SOUND_VLD_SQLSTR = "INSERT INTO moment_epoch_weekday_s_vld (spark_num, face_name, moment_label, weekday_order, weekday_label) SELECT spark_num, face_name, moment_label, weekday_order, weekday_label FROM moment_epoch_weekday_s_agg WHERE error_message IS NULL"
INSERT_BLFOFFI_SOUND_VLD_SQLSTR = "INSERT INTO moment_timeoffi_s_vld (spark_num, face_name, moment_label, offi_time) SELECT spark_num, face_name, moment_label, offi_time FROM moment_timeoffi_s_agg WHERE error_message IS NULL"
INSERT_BLFUNIT_SOUND_VLD_SQLSTR = "INSERT INTO momentunit_s_vld (spark_num, face_name, moment_label, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, money_grain, respect_grain, knot, job_listen_rotations) SELECT spark_num, face_name, moment_label, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, money_grain, respect_grain, knot, job_listen_rotations FROM momentunit_s_agg WHERE error_message IS NULL"


def get_insert_into_sound_vld_sqlstrs() -> dict[str, str]:
    return {
        "belief_voice_membership_s_put_vld": INSERT_BLRMEMB_SOUND_VLD_PUT_SQLSTR,
        "belief_voice_membership_s_del_vld": INSERT_BLRMEMB_SOUND_VLD_DEL_SQLSTR,
        "belief_voiceunit_s_put_vld": INSERT_BLRPERN_SOUND_VLD_PUT_SQLSTR,
        "belief_voiceunit_s_del_vld": INSERT_BLRPERN_SOUND_VLD_DEL_SQLSTR,
        "belief_plan_awardunit_s_put_vld": INSERT_BLRAWAR_SOUND_VLD_PUT_SQLSTR,
        "belief_plan_awardunit_s_del_vld": INSERT_BLRAWAR_SOUND_VLD_DEL_SQLSTR,
        "belief_plan_factunit_s_put_vld": INSERT_BLRFACT_SOUND_VLD_PUT_SQLSTR,
        "belief_plan_factunit_s_del_vld": INSERT_BLRFACT_SOUND_VLD_DEL_SQLSTR,
        "belief_plan_healerunit_s_put_vld": INSERT_BLRHEAL_SOUND_VLD_PUT_SQLSTR,
        "belief_plan_healerunit_s_del_vld": INSERT_BLRHEAL_SOUND_VLD_DEL_SQLSTR,
        "belief_plan_reason_caseunit_s_put_vld": INSERT_BLRPREM_SOUND_VLD_PUT_SQLSTR,
        "belief_plan_reason_caseunit_s_del_vld": INSERT_BLRPREM_SOUND_VLD_DEL_SQLSTR,
        "belief_plan_reasonunit_s_put_vld": INSERT_BLRREAS_SOUND_VLD_PUT_SQLSTR,
        "belief_plan_reasonunit_s_del_vld": INSERT_BLRREAS_SOUND_VLD_DEL_SQLSTR,
        "belief_plan_partyunit_s_put_vld": INSERT_BLRLABO_SOUND_VLD_PUT_SQLSTR,
        "belief_plan_partyunit_s_del_vld": INSERT_BLRLABO_SOUND_VLD_DEL_SQLSTR,
        "belief_planunit_s_put_vld": INSERT_BLRPLAN_SOUND_VLD_PUT_SQLSTR,
        "belief_planunit_s_del_vld": INSERT_BLRPLAN_SOUND_VLD_DEL_SQLSTR,
        "beliefunit_s_put_vld": INSERT_BLRUNIT_SOUND_VLD_PUT_SQLSTR,
        "beliefunit_s_del_vld": INSERT_BLRUNIT_SOUND_VLD_DEL_SQLSTR,
        "moment_paybook_s_vld": INSERT_BLFPAYY_SOUND_VLD_SQLSTR,
        "moment_budunit_s_vld": INSERT_BLFBUDD_SOUND_VLD_SQLSTR,
        "moment_epoch_hour_s_vld": INSERT_BLFHOUR_SOUND_VLD_SQLSTR,
        "moment_epoch_month_s_vld": INSERT_BLFMONT_SOUND_VLD_SQLSTR,
        "moment_epoch_weekday_s_vld": INSERT_BLFWEEK_SOUND_VLD_SQLSTR,
        "moment_timeoffi_s_vld": INSERT_BLFOFFI_SOUND_VLD_SQLSTR,
        "momentunit_s_vld": INSERT_BLFUNIT_SOUND_VLD_SQLSTR,
    }


INSERT_BLFPAYY_HEARD_RAW_SQLSTR = "INSERT INTO moment_paybook_h_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, voice_name_otx, tran_time, amount) SELECT spark_num, face_name, moment_label, belief_name, voice_name, tran_time, amount FROM moment_paybook_s_vld "
INSERT_BLFBUDD_HEARD_RAW_SQLSTR = "INSERT INTO moment_budunit_h_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, bud_time, quota, celldepth) SELECT spark_num, face_name, moment_label, belief_name, bud_time, quota, celldepth FROM moment_budunit_s_vld "
INSERT_BLFHOUR_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_hour_h_raw (spark_num, face_name_otx, moment_label_otx, cumulative_minute, hour_label_otx) SELECT spark_num, face_name, moment_label, cumulative_minute, hour_label FROM moment_epoch_hour_s_vld "
INSERT_BLFMONT_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_month_h_raw (spark_num, face_name_otx, moment_label_otx, cumulative_day, month_label_otx) SELECT spark_num, face_name, moment_label, cumulative_day, month_label FROM moment_epoch_month_s_vld "
INSERT_BLFWEEK_HEARD_RAW_SQLSTR = "INSERT INTO moment_epoch_weekday_h_raw (spark_num, face_name_otx, moment_label_otx, weekday_order, weekday_label_otx) SELECT spark_num, face_name, moment_label, weekday_order, weekday_label FROM moment_epoch_weekday_s_vld "
INSERT_BLFOFFI_HEARD_RAW_SQLSTR = "INSERT INTO moment_timeoffi_h_raw (spark_num, face_name_otx, moment_label_otx, offi_time) SELECT spark_num, face_name, moment_label, offi_time FROM moment_timeoffi_s_vld "
INSERT_BLFUNIT_HEARD_RAW_SQLSTR = "INSERT INTO momentunit_h_raw (spark_num, face_name_otx, moment_label_otx, epoch_label_otx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, money_grain, respect_grain, knot, job_listen_rotations) SELECT spark_num, face_name, moment_label, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, money_grain, respect_grain, knot, job_listen_rotations FROM momentunit_s_vld "

INSERT_BLRMEMB_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_voice_membership_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, voice_name_otx, group_title_otx, group_cred_lumen, group_debt_lumen) SELECT spark_num, face_name, moment_label, belief_name, voice_name, group_title, group_cred_lumen, group_debt_lumen FROM belief_voice_membership_s_put_vld "
INSERT_BLRMEMB_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_voice_membership_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, voice_name_otx, group_title_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, voice_name, group_title_ERASE FROM belief_voice_membership_s_del_vld "
INSERT_BLRPERN_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_voiceunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, voice_name_otx, voice_cred_lumen, voice_debt_lumen) SELECT spark_num, face_name, moment_label, belief_name, voice_name, voice_cred_lumen, voice_debt_lumen FROM belief_voiceunit_s_put_vld "
INSERT_BLRPERN_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_voiceunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, voice_name_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, voice_name_ERASE FROM belief_voiceunit_s_del_vld "
INSERT_BLRAWAR_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_plan_awardunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, awardee_title_otx, give_force, take_force) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, awardee_title, give_force, take_force FROM belief_plan_awardunit_s_put_vld "
INSERT_BLRAWAR_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_plan_awardunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, awardee_title_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, awardee_title_ERASE FROM belief_plan_awardunit_s_del_vld "
INSERT_BLRFACT_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_plan_factunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, fact_context_otx, fact_state_otx, fact_lower, fact_upper) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper FROM belief_plan_factunit_s_put_vld "
INSERT_BLRFACT_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_plan_factunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, fact_context_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, fact_context_ERASE FROM belief_plan_factunit_s_del_vld "
INSERT_BLRHEAL_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_plan_healerunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, healer_name_otx) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, healer_name FROM belief_plan_healerunit_s_put_vld "
INSERT_BLRHEAL_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_plan_healerunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, healer_name_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, healer_name_ERASE FROM belief_plan_healerunit_s_del_vld "
INSERT_BLRPREM_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_plan_reason_caseunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, reason_context_otx, reason_state_otx, reason_upper, reason_lower, reason_divisor) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor FROM belief_plan_reason_caseunit_s_put_vld "
INSERT_BLRPREM_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_plan_reason_caseunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, reason_context_otx, reason_state_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, reason_state_ERASE FROM belief_plan_reason_caseunit_s_del_vld "
INSERT_BLRREAS_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_plan_reasonunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, reason_context_otx, active_requisite) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, active_requisite FROM belief_plan_reasonunit_s_put_vld "
INSERT_BLRREAS_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_plan_reasonunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, reason_context_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, reason_context_ERASE FROM belief_plan_reasonunit_s_del_vld "
INSERT_BLRLABO_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_plan_partyunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, party_title_otx, solo) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, party_title, solo FROM belief_plan_partyunit_s_put_vld "
INSERT_BLRLABO_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_plan_partyunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, party_title_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, party_title_ERASE FROM belief_plan_partyunit_s_del_vld "
INSERT_BLRPLAN_HEARD_RAW_PUT_SQLSTR = "INSERT INTO belief_planunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_otx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool) SELECT spark_num, face_name, moment_label, belief_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool FROM belief_planunit_s_put_vld "
INSERT_BLRPLAN_HEARD_RAW_DEL_SQLSTR = "INSERT INTO belief_planunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, plan_rope_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name, plan_rope_ERASE FROM belief_planunit_s_del_vld "
INSERT_BLRUNIT_HEARD_RAW_PUT_SQLSTR = "INSERT INTO beliefunit_h_put_raw (spark_num, face_name_otx, moment_label_otx, belief_name_otx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_grain, money_grain, respect_grain) SELECT spark_num, face_name, moment_label, belief_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_grain, money_grain, respect_grain FROM beliefunit_s_put_vld "
INSERT_BLRUNIT_HEARD_RAW_DEL_SQLSTR = "INSERT INTO beliefunit_h_del_raw (spark_num, face_name_otx, moment_label_otx, belief_name_ERASE_otx) SELECT spark_num, face_name, moment_label, belief_name_ERASE FROM beliefunit_s_del_vld "


def get_insert_into_heard_raw_sqlstrs() -> dict[str, str]:
    return {
        "moment_paybook_h_raw": INSERT_BLFPAYY_HEARD_RAW_SQLSTR,
        "moment_budunit_h_raw": INSERT_BLFBUDD_HEARD_RAW_SQLSTR,
        "moment_epoch_hour_h_raw": INSERT_BLFHOUR_HEARD_RAW_SQLSTR,
        "moment_epoch_month_h_raw": INSERT_BLFMONT_HEARD_RAW_SQLSTR,
        "moment_epoch_weekday_h_raw": INSERT_BLFWEEK_HEARD_RAW_SQLSTR,
        "moment_timeoffi_h_raw": INSERT_BLFOFFI_HEARD_RAW_SQLSTR,
        "momentunit_h_raw": INSERT_BLFUNIT_HEARD_RAW_SQLSTR,
        "belief_voice_membership_h_put_raw": INSERT_BLRMEMB_HEARD_RAW_PUT_SQLSTR,
        "belief_voice_membership_h_del_raw": INSERT_BLRMEMB_HEARD_RAW_DEL_SQLSTR,
        "belief_voiceunit_h_put_raw": INSERT_BLRPERN_HEARD_RAW_PUT_SQLSTR,
        "belief_voiceunit_h_del_raw": INSERT_BLRPERN_HEARD_RAW_DEL_SQLSTR,
        "belief_plan_awardunit_h_put_raw": INSERT_BLRAWAR_HEARD_RAW_PUT_SQLSTR,
        "belief_plan_awardunit_h_del_raw": INSERT_BLRAWAR_HEARD_RAW_DEL_SQLSTR,
        "belief_plan_factunit_h_put_raw": INSERT_BLRFACT_HEARD_RAW_PUT_SQLSTR,
        "belief_plan_factunit_h_del_raw": INSERT_BLRFACT_HEARD_RAW_DEL_SQLSTR,
        "belief_plan_healerunit_h_put_raw": INSERT_BLRHEAL_HEARD_RAW_PUT_SQLSTR,
        "belief_plan_healerunit_h_del_raw": INSERT_BLRHEAL_HEARD_RAW_DEL_SQLSTR,
        "belief_plan_reason_caseunit_h_put_raw": INSERT_BLRPREM_HEARD_RAW_PUT_SQLSTR,
        "belief_plan_reason_caseunit_h_del_raw": INSERT_BLRPREM_HEARD_RAW_DEL_SQLSTR,
        "belief_plan_reasonunit_h_put_raw": INSERT_BLRREAS_HEARD_RAW_PUT_SQLSTR,
        "belief_plan_reasonunit_h_del_raw": INSERT_BLRREAS_HEARD_RAW_DEL_SQLSTR,
        "belief_plan_partyunit_h_put_raw": INSERT_BLRLABO_HEARD_RAW_PUT_SQLSTR,
        "belief_plan_partyunit_h_del_raw": INSERT_BLRLABO_HEARD_RAW_DEL_SQLSTR,
        "belief_planunit_h_put_raw": INSERT_BLRPLAN_HEARD_RAW_PUT_SQLSTR,
        "belief_planunit_h_del_raw": INSERT_BLRPLAN_HEARD_RAW_DEL_SQLSTR,
        "beliefunit_h_put_raw": INSERT_BLRUNIT_HEARD_RAW_PUT_SQLSTR,
        "beliefunit_h_del_raw": INSERT_BLRUNIT_HEARD_RAW_DEL_SQLSTR,
    }


def create_update_heard_raw_existing_inx_col_sqlstr(
    translate_type_abbv: str, table: str, column_prefix: str
) -> str:
    return f"""
WITH trl_face_otx_spark AS (
    SELECT 
      raw_dim.rowid raw_rowid
    , raw_dim.spark_num
    , raw_dim.face_name_otx
    , raw_dim.{column_prefix}_otx
    , MAX(trl.spark_num) translate_spark_num
    FROM {table} raw_dim
    LEFT JOIN translate_{translate_type_abbv}_s_vld trl ON trl.face_name = raw_dim.face_name_otx
        AND trl.otx_{translate_type_abbv} = raw_dim.{column_prefix}_otx
        AND raw_dim.spark_num >= trl.spark_num
    GROUP BY 
      raw_dim.rowid
    , raw_dim.spark_num
    , raw_dim.face_name_otx
    , raw_dim.{column_prefix}_otx
),
trl_inx_strs AS (
    SELECT trl_foe.raw_rowid, trl_vld.inx_{translate_type_abbv}
    FROM trl_face_otx_spark trl_foe
    LEFT JOIN translate_{translate_type_abbv}_s_vld trl_vld
        ON trl_vld.face_name = trl_foe.face_name_otx
        AND trl_vld.otx_{translate_type_abbv} = trl_foe.{column_prefix}_otx
        AND trl_vld.spark_num = trl_foe.translate_spark_num
)
UPDATE {table} as dim_h_raw
SET {column_prefix}_inx = (
    SELECT trl_inx_strs.inx_{translate_type_abbv}
    FROM trl_inx_strs
    WHERE dim_h_raw.rowid = trl_inx_strs.raw_rowid
)
;
"""


def create_update_heard_raw_empty_inx_col_sqlstr(table: str, column_prefix: str) -> str:
    return f"""
UPDATE {table} as dim_h_raw
SET {column_prefix}_inx = {column_prefix}_otx
WHERE {column_prefix}_inx IS NULL
;
"""


BLFPAYY_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_paybook_h_agg (moment_label, belief_name, voice_name, tran_time, amount)
SELECT moment_label_inx, belief_name_inx, voice_name_inx, tran_time, amount
FROM moment_paybook_h_raw
GROUP BY moment_label_inx, belief_name_inx, voice_name_inx, tran_time, amount
"""
BLFBUDD_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_budunit_h_agg (moment_label, belief_name, bud_time, quota, celldepth)
SELECT moment_label_inx, belief_name_inx, bud_time, quota, celldepth
FROM moment_budunit_h_raw
GROUP BY moment_label_inx, belief_name_inx, bud_time, quota, celldepth
"""
BLFHOUR_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_hour_h_agg (moment_label, cumulative_minute, hour_label)
SELECT moment_label_inx, cumulative_minute, hour_label_inx
FROM moment_epoch_hour_h_raw
GROUP BY moment_label_inx, cumulative_minute, hour_label_inx
"""
BLFMONT_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_month_h_agg (moment_label, cumulative_day, month_label)
SELECT moment_label_inx, cumulative_day, month_label_inx
FROM moment_epoch_month_h_raw
GROUP BY moment_label_inx, cumulative_day, month_label_inx
"""
BLFWEEK_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_epoch_weekday_h_agg (moment_label, weekday_order, weekday_label)
SELECT moment_label_inx, weekday_order, weekday_label_inx
FROM moment_epoch_weekday_h_raw
GROUP BY moment_label_inx, weekday_order, weekday_label_inx
"""
BLFOFFI_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO moment_timeoffi_h_agg (moment_label, offi_time)
SELECT moment_label_inx, offi_time
FROM moment_timeoffi_h_raw
GROUP BY moment_label_inx, offi_time
"""
BLFUNIT_HEARD_AGG_INSERT_SQLSTR = """
INSERT INTO momentunit_h_agg (moment_label, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, money_grain, respect_grain, knot, job_listen_rotations)
SELECT moment_label_inx, epoch_label_inx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, money_grain, respect_grain, knot, job_listen_rotations
FROM momentunit_h_raw
GROUP BY moment_label_inx, epoch_label_inx, c400_number, yr1_jan1_offset, monthday_index, fund_grain, money_grain, respect_grain, knot, job_listen_rotations
"""

INSERT_BLRMEMB_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_voice_membership_h_put_agg (spark_num, face_name, moment_label, belief_name, voice_name, group_title, group_cred_lumen, group_debt_lumen)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, voice_name_inx, group_title_inx, group_cred_lumen, group_debt_lumen
FROM belief_voice_membership_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, voice_name_inx, group_title_inx, group_cred_lumen, group_debt_lumen
"""
INSERT_BLRMEMB_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_voice_membership_h_del_agg (spark_num, face_name, moment_label, belief_name, voice_name, group_title_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, voice_name_inx, group_title_ERASE_inx
FROM belief_voice_membership_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, voice_name_inx, group_title_ERASE_inx
"""
INSERT_BLRPERN_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_voiceunit_h_put_agg (spark_num, face_name, moment_label, belief_name, voice_name, voice_cred_lumen, voice_debt_lumen)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, voice_name_inx, voice_cred_lumen, voice_debt_lumen
FROM belief_voiceunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, voice_name_inx, voice_cred_lumen, voice_debt_lumen
"""
INSERT_BLRPERN_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_voiceunit_h_del_agg (spark_num, face_name, moment_label, belief_name, voice_name_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, voice_name_ERASE_inx
FROM belief_voiceunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, voice_name_ERASE_inx
"""
INSERT_BLRAWAR_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_plan_awardunit_h_put_agg (spark_num, face_name, moment_label, belief_name, plan_rope, awardee_title, give_force, take_force)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, awardee_title_inx, give_force, take_force
FROM belief_plan_awardunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, awardee_title_inx, give_force, take_force
"""
INSERT_BLRAWAR_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_plan_awardunit_h_del_agg (spark_num, face_name, moment_label, belief_name, plan_rope, awardee_title_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, awardee_title_ERASE_inx
FROM belief_plan_awardunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, awardee_title_ERASE_inx
"""
INSERT_BLRFACT_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_plan_factunit_h_put_agg (spark_num, face_name, moment_label, belief_name, plan_rope, fact_context, fact_state, fact_lower, fact_upper)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper
FROM belief_plan_factunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, fact_context_inx, fact_state_inx, fact_lower, fact_upper
"""
INSERT_BLRFACT_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_plan_factunit_h_del_agg (spark_num, face_name, moment_label, belief_name, plan_rope, fact_context_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, fact_context_ERASE_inx
FROM belief_plan_factunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, fact_context_ERASE_inx
"""
INSERT_BLRHEAL_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_plan_healerunit_h_put_agg (spark_num, face_name, moment_label, belief_name, plan_rope, healer_name)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, healer_name_inx
FROM belief_plan_healerunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, healer_name_inx
"""
INSERT_BLRHEAL_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_plan_healerunit_h_del_agg (spark_num, face_name, moment_label, belief_name, plan_rope, healer_name_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, healer_name_ERASE_inx
FROM belief_plan_healerunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, healer_name_ERASE_inx
"""
INSERT_BLRPREM_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_plan_reason_caseunit_h_put_agg (spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, reason_state, reason_upper, reason_lower, reason_divisor)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, reason_context_inx, reason_state_inx, reason_upper, reason_lower, reason_divisor
FROM belief_plan_reason_caseunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, reason_context_inx, reason_state_inx, reason_upper, reason_lower, reason_divisor
"""
INSERT_BLRPREM_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_plan_reason_caseunit_h_del_agg (spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, reason_state_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, reason_context_inx, reason_state_ERASE_inx
FROM belief_plan_reason_caseunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, reason_context_inx, reason_state_ERASE_inx
"""
INSERT_BLRREAS_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_plan_reasonunit_h_put_agg (spark_num, face_name, moment_label, belief_name, plan_rope, reason_context, active_requisite)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, reason_context_inx, active_requisite
FROM belief_plan_reasonunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, reason_context_inx, active_requisite
"""
INSERT_BLRREAS_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_plan_reasonunit_h_del_agg (spark_num, face_name, moment_label, belief_name, plan_rope, reason_context_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, reason_context_ERASE_inx
FROM belief_plan_reasonunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, reason_context_ERASE_inx
"""
INSERT_BLRLABO_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_plan_partyunit_h_put_agg (spark_num, face_name, moment_label, belief_name, plan_rope, party_title, solo)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, party_title_inx, solo
FROM belief_plan_partyunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, party_title_inx, solo
"""
INSERT_BLRLABO_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_plan_partyunit_h_del_agg (spark_num, face_name, moment_label, belief_name, plan_rope, party_title_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, party_title_ERASE_inx
FROM belief_plan_partyunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, party_title_ERASE_inx
"""
INSERT_BLRPLAN_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO belief_planunit_h_put_agg (spark_num, face_name, moment_label, belief_name, plan_rope, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool
FROM belief_planunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_inx, begin, close, addin, numor, denom, morph, gogo_want, stop_want, star, pledge, problem_bool
"""
INSERT_BLRPLAN_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO belief_planunit_h_del_agg (spark_num, face_name, moment_label, belief_name, plan_rope_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_ERASE_inx
FROM belief_planunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, plan_rope_ERASE_inx
"""
INSERT_BLRUNIT_HEARD_AGG_PUT_SQLSTR = """
INSERT INTO beliefunit_h_put_agg (spark_num, face_name, moment_label, belief_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_grain, money_grain, respect_grain)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_grain, money_grain, respect_grain
FROM beliefunit_h_put_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_inx, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_grain, money_grain, respect_grain
"""
INSERT_BLRUNIT_HEARD_AGG_DEL_SQLSTR = """
INSERT INTO beliefunit_h_del_agg (spark_num, face_name, moment_label, belief_name_ERASE)
SELECT spark_num, face_name_inx, moment_label_inx, belief_name_ERASE_inx
FROM beliefunit_h_del_raw
GROUP BY spark_num, face_name_inx, moment_label_inx, belief_name_ERASE_inx
"""


def get_insert_heard_agg_sqlstrs() -> dict[str, str]:
    return {
        "moment_paybook": BLFPAYY_HEARD_AGG_INSERT_SQLSTR,
        "moment_budunit": BLFBUDD_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_hour": BLFHOUR_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_month": BLFMONT_HEARD_AGG_INSERT_SQLSTR,
        "moment_epoch_weekday": BLFWEEK_HEARD_AGG_INSERT_SQLSTR,
        "moment_timeoffi": BLFOFFI_HEARD_AGG_INSERT_SQLSTR,
        "momentunit": BLFUNIT_HEARD_AGG_INSERT_SQLSTR,
        "belief_voice_membership_h_put_agg": INSERT_BLRMEMB_HEARD_AGG_PUT_SQLSTR,
        "belief_voice_membership_h_del_agg": INSERT_BLRMEMB_HEARD_AGG_DEL_SQLSTR,
        "belief_voiceunit_h_put_agg": INSERT_BLRPERN_HEARD_AGG_PUT_SQLSTR,
        "belief_voiceunit_h_del_agg": INSERT_BLRPERN_HEARD_AGG_DEL_SQLSTR,
        "belief_plan_awardunit_h_put_agg": INSERT_BLRAWAR_HEARD_AGG_PUT_SQLSTR,
        "belief_plan_awardunit_h_del_agg": INSERT_BLRAWAR_HEARD_AGG_DEL_SQLSTR,
        "belief_plan_factunit_h_put_agg": INSERT_BLRFACT_HEARD_AGG_PUT_SQLSTR,
        "belief_plan_factunit_h_del_agg": INSERT_BLRFACT_HEARD_AGG_DEL_SQLSTR,
        "belief_plan_healerunit_h_put_agg": INSERT_BLRHEAL_HEARD_AGG_PUT_SQLSTR,
        "belief_plan_healerunit_h_del_agg": INSERT_BLRHEAL_HEARD_AGG_DEL_SQLSTR,
        "belief_plan_reason_caseunit_h_put_agg": INSERT_BLRPREM_HEARD_AGG_PUT_SQLSTR,
        "belief_plan_reason_caseunit_h_del_agg": INSERT_BLRPREM_HEARD_AGG_DEL_SQLSTR,
        "belief_plan_reasonunit_h_put_agg": INSERT_BLRREAS_HEARD_AGG_PUT_SQLSTR,
        "belief_plan_reasonunit_h_del_agg": INSERT_BLRREAS_HEARD_AGG_DEL_SQLSTR,
        "belief_plan_partyunit_h_put_agg": INSERT_BLRLABO_HEARD_AGG_PUT_SQLSTR,
        "belief_plan_partyunit_h_del_agg": INSERT_BLRLABO_HEARD_AGG_DEL_SQLSTR,
        "belief_planunit_h_put_agg": INSERT_BLRPLAN_HEARD_AGG_PUT_SQLSTR,
        "belief_planunit_h_del_agg": INSERT_BLRPLAN_HEARD_AGG_DEL_SQLSTR,
        "beliefunit_h_put_agg": INSERT_BLRUNIT_HEARD_AGG_PUT_SQLSTR,
        "beliefunit_h_del_agg": INSERT_BLRUNIT_HEARD_AGG_DEL_SQLSTR,
    }


BLFPAYY_FU2_SELECT_SQLSTR = "SELECT moment_label, belief_name, voice_name, tran_time, amount FROM moment_paybook_h_agg WHERE moment_label = "
BLFBUDD_FU2_SELECT_SQLSTR = "SELECT moment_label, belief_name, bud_time, quota, celldepth FROM moment_budunit_h_agg WHERE moment_label = "
BLFHOUR_FU2_SELECT_SQLSTR = "SELECT moment_label, cumulative_minute, hour_label FROM moment_epoch_hour_h_agg WHERE moment_label = "
BLFMONT_FU2_SELECT_SQLSTR = "SELECT moment_label, cumulative_day, month_label FROM moment_epoch_month_h_agg WHERE moment_label = "
BLFWEEK_FU2_SELECT_SQLSTR = "SELECT moment_label, weekday_order, weekday_label FROM moment_epoch_weekday_h_agg WHERE moment_label = "
BLFOFFI_FU2_SELECT_SQLSTR = (
    "SELECT moment_label, offi_time FROM moment_timeoffi_h_agg WHERE moment_label = "
)
BLFUNIT_FU2_SELECT_SQLSTR = "SELECT moment_label, epoch_label, c400_number, yr1_jan1_offset, monthday_index, fund_grain, money_grain, respect_grain, knot, job_listen_rotations FROM momentunit_h_agg WHERE moment_label = "


def get_moment_heard_select1_sqlstrs(moment_label: str) -> dict[str, str]:
    return {
        "momentunit": f"{BLFUNIT_FU2_SELECT_SQLSTR}'{moment_label}'",
        "moment_budunit": f"{BLFBUDD_FU2_SELECT_SQLSTR}'{moment_label}'",
        "moment_paybook": f"{BLFPAYY_FU2_SELECT_SQLSTR}'{moment_label}'",
        "moment_epoch_hour": f"{BLFHOUR_FU2_SELECT_SQLSTR}'{moment_label}'",
        "moment_epoch_month": f"{BLFMONT_FU2_SELECT_SQLSTR}'{moment_label}'",
        "moment_epoch_weekday": f"{BLFWEEK_FU2_SELECT_SQLSTR}'{moment_label}'",
        "moment_timeoffi": f"{BLFOFFI_FU2_SELECT_SQLSTR}'{moment_label}'",
    }


def get_idea_stageble_put_dimens() -> dict[str, list[str]]:
    return {
        "br00000": ["momentunit"],
        "br00001": ["beliefunit", "moment_budunit", "momentunit"],
        "br00002": ["belief_voiceunit", "beliefunit", "moment_paybook", "momentunit"],
        "br00003": ["moment_epoch_hour", "momentunit"],
        "br00004": ["moment_epoch_month", "momentunit"],
        "br00005": ["moment_epoch_weekday", "momentunit"],
        "br00006": ["moment_timeoffi", "momentunit"],
        "br00011": ["belief_voiceunit", "beliefunit", "momentunit"],
        "br00012": [
            "belief_voice_membership",
            "belief_voiceunit",
            "beliefunit",
            "momentunit",
        ],
        "br00013": ["belief_planunit", "beliefunit", "momentunit"],
        "br00019": ["belief_planunit", "beliefunit", "momentunit"],
        "br00020": [
            "belief_voice_membership",
            "belief_voiceunit",
            "beliefunit",
            "momentunit",
        ],
        "br00021": ["belief_voiceunit", "beliefunit", "momentunit"],
        "br00022": [
            "belief_plan_awardunit",
            "belief_planunit",
            "beliefunit",
            "momentunit",
        ],
        "br00023": [
            "belief_plan_factunit",
            "belief_planunit",
            "beliefunit",
            "momentunit",
        ],
        "br00024": [
            "belief_plan_partyunit",
            "belief_planunit",
            "beliefunit",
            "momentunit",
        ],
        "br00025": [
            "belief_plan_healerunit",
            "belief_planunit",
            "beliefunit",
            "momentunit",
        ],
        "br00026": [
            "belief_plan_reason_caseunit",
            "belief_plan_reasonunit",
            "belief_planunit",
            "beliefunit",
            "momentunit",
        ],
        "br00027": [
            "belief_plan_reasonunit",
            "belief_planunit",
            "beliefunit",
            "momentunit",
        ],
        "br00028": ["belief_planunit", "beliefunit", "momentunit"],
        "br00029": ["beliefunit", "momentunit"],
        "br00036": [
            "belief_plan_healerunit",
            "belief_planunit",
            "beliefunit",
            "momentunit",
        ],
        "br00042": [],
        "br00043": [],
        "br00044": [],
        "br00045": [],
        "br00050": ["belief_voiceunit", "beliefunit", "momentunit"],
        "br00051": ["beliefunit", "momentunit"],
        "br00052": ["belief_planunit", "beliefunit", "momentunit"],
        "br00053": ["belief_planunit", "beliefunit", "momentunit"],
        "br00054": ["belief_planunit", "beliefunit", "momentunit"],
        "br00055": ["belief_planunit", "beliefunit", "momentunit"],
        "br00056": [
            "belief_plan_reasonunit",
            "belief_planunit",
            "beliefunit",
            "momentunit",
        ],
        "br00057": ["belief_planunit", "beliefunit", "momentunit"],
        "br00058": ["beliefunit", "momentunit"],
        "br00059": ["momentunit"],
        "br00113": ["belief_voiceunit", "beliefunit", "momentunit"],
        "br00115": ["belief_voiceunit", "beliefunit", "momentunit"],
        "br00116": ["belief_voiceunit", "beliefunit", "momentunit"],
        "br00117": ["belief_voiceunit", "beliefunit", "momentunit"],
    }


IDEA_STAGEBLE_DEL_DIMENS = {
    "br00050": ["belief_voice_membership"],
    "br00051": ["belief_voiceunit"],
    "br00052": ["belief_plan_awardunit"],
    "br00053": ["belief_plan_factunit"],
    "br00054": ["belief_plan_partyunit"],
    "br00055": ["belief_plan_healerunit"],
    "br00056": ["belief_plan_reason_caseunit"],
    "br00057": ["belief_plan_reasonunit"],
    "br00058": ["belief_planunit"],
    "br00059": ["beliefunit"],
}


CREATE_MOMENT_SPARK_TIME_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS moment_spark_time_agg (
  moment_label TEXT
, spark_num INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
INSERT_MOMENT_SPARK_TIME_AGG_SQLSTR = """
INSERT INTO moment_spark_time_agg (moment_label, spark_num, agg_time)
SELECT moment_label, spark_num, agg_time
FROM (
    SELECT moment_label, spark_num, tran_time as agg_time
    FROM moment_paybook_raw
    GROUP BY moment_label, spark_num, tran_time
    UNION 
    SELECT moment_label, spark_num, bud_time as agg_time
    FROM moment_budunit_raw
    GROUP BY moment_label, spark_num, bud_time
)
ORDER BY moment_label, spark_num, agg_time
;
"""
UPDATE_ERROR_MESSAGE_MOMENT_SPARK_TIME_AGG_SQLSTR = """
WITH SparkTimeOrdered AS (
    SELECT moment_label, spark_num, agg_time,
           LAG(agg_time) OVER (PARTITION BY moment_label ORDER BY spark_num) AS prev_agg_time
    FROM moment_spark_time_agg
)
UPDATE moment_spark_time_agg
SET error_message = CASE 
         WHEN SparkTimeOrdered.prev_agg_time > SparkTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM SparkTimeOrdered
WHERE SparkTimeOrdered.spark_num = moment_spark_time_agg.spark_num
    AND SparkTimeOrdered.moment_label = moment_spark_time_agg.moment_label
    AND SparkTimeOrdered.agg_time = moment_spark_time_agg.agg_time
;
"""


CREATE_MOMENT_OTE1_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS moment_ote1_agg (
  moment_label TEXT
, belief_name TEXT
, spark_num INTEGER
, bud_time INTEGER
, error_message TEXT
)
;
"""
INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR = """
INSERT INTO moment_ote1_agg (moment_label, belief_name, spark_num, bud_time)
SELECT moment_label, belief_name, spark_num, bud_time
FROM (
    SELECT 
      moment_label_inx moment_label
    , belief_name_inx belief_name
    , spark_num
    , bud_time
    FROM moment_budunit_h_raw
    GROUP BY moment_label_inx, belief_name_inx, spark_num, bud_time
)
ORDER BY moment_label, belief_name, spark_num, bud_time
;
"""


CREATE_JOB_BLRMEMB_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_voice_membership_job (moment_label TEXT, belief_name TEXT, voice_name TEXT, group_title TEXT, group_cred_lumen REAL, group_debt_lumen REAL, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL, fund_agenda_ratio_give REAL, fund_agenda_ratio_take REAL)"""
CREATE_JOB_BLRPERN_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_voiceunit_job (moment_label TEXT, belief_name TEXT, voice_name TEXT, voice_cred_lumen REAL, voice_debt_lumen REAL, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL, fund_agenda_ratio_give REAL, fund_agenda_ratio_take REAL, inallocable_voice_debt_lumen REAL, irrational_voice_debt_lumen REAL)"""
CREATE_JOB_BLRGROU_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_groupunit_job (moment_label TEXT, belief_name TEXT, group_title TEXT, fund_grain REAL, knot TEXT, credor_pool REAL, debtor_pool REAL, fund_give REAL, fund_take REAL, fund_agenda_give REAL, fund_agenda_take REAL)"""
CREATE_JOB_BLRAWAR_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_plan_awardunit_job (moment_label TEXT, belief_name TEXT, plan_rope TEXT, awardee_title TEXT, give_force REAL, take_force REAL, fund_give REAL, fund_take REAL)"""
CREATE_JOB_BLRFACT_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_plan_factunit_job (moment_label TEXT, belief_name TEXT, plan_rope TEXT, fact_context TEXT, fact_state TEXT, fact_lower REAL, fact_upper REAL)"""
CREATE_JOB_BLRHEAL_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_plan_healerunit_job (moment_label TEXT, belief_name TEXT, plan_rope TEXT, healer_name TEXT)"""
CREATE_JOB_BLRPREM_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_plan_reason_caseunit_job (moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, reason_state TEXT, reason_upper REAL, reason_lower REAL, reason_divisor INTEGER, task INTEGER, case_active INTEGER)"""
CREATE_JOB_BLRREAS_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_plan_reasonunit_job (moment_label TEXT, belief_name TEXT, plan_rope TEXT, reason_context TEXT, active_requisite INTEGER, task INTEGER, status INTEGER, parent_heir_active INTEGER)"""
CREATE_JOB_BLRLABO_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_plan_partyunit_job (moment_label TEXT, belief_name TEXT, plan_rope TEXT, party_title TEXT, solo INTEGER, _belief_name_is_labor INTEGER)"""
CREATE_JOB_BLRPLAN_SQLSTR = """CREATE TABLE IF NOT EXISTS belief_planunit_job (moment_label TEXT, belief_name TEXT, plan_rope TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, star INTEGER, pledge INTEGER, problem_bool INTEGER, fund_grain REAL, active INTEGER, task INTEGER, fund_onset REAL, fund_cease REAL, fund_ratio REAL, gogo_calc REAL, stop_calc REAL, tree_level INTEGER, range_evaluated INTEGER, descendant_pledge_count INTEGER, healerunit_ratio REAL, all_voice_cred INTEGER, all_voice_debt INTEGER)"""
CREATE_JOB_BLRUNIT_SQLSTR = """CREATE TABLE IF NOT EXISTS beliefunit_job (moment_label TEXT, belief_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_grain REAL, money_grain REAL, respect_grain REAL, rational INTEGER, keeps_justified INTEGER, offtrack_fund REAL, sum_healerunit_plans_fund_total REAL, keeps_buildable INTEGER, tree_traverse_count INTEGER)"""


def get_job_create_table_sqlstrs() -> dict[str, str]:
    return {
        "belief_voice_membership_job": CREATE_JOB_BLRMEMB_SQLSTR,
        "belief_voiceunit_job": CREATE_JOB_BLRPERN_SQLSTR,
        "belief_groupunit_job": CREATE_JOB_BLRGROU_SQLSTR,
        "belief_plan_awardunit_job": CREATE_JOB_BLRAWAR_SQLSTR,
        "belief_plan_factunit_job": CREATE_JOB_BLRFACT_SQLSTR,
        "belief_plan_healerunit_job": CREATE_JOB_BLRHEAL_SQLSTR,
        "belief_plan_reason_caseunit_job": CREATE_JOB_BLRPREM_SQLSTR,
        "belief_plan_reasonunit_job": CREATE_JOB_BLRREAS_SQLSTR,
        "belief_plan_partyunit_job": CREATE_JOB_BLRLABO_SQLSTR,
        "belief_planunit_job": CREATE_JOB_BLRPLAN_SQLSTR,
        "beliefunit_job": CREATE_JOB_BLRUNIT_SQLSTR,
    }


def create_job_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_job_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


CREATE_MOMENT_VOICE_NETS_SQLSTR = "CREATE TABLE IF NOT EXISTS moment_voice_nets (moment_label TEXT, belief_name TEXT, belief_net_amount REAL)"
