from src.a00_data_toolboxs.db_toolbox import create_table_from_columns
from src.a17_idea_logic.idea_db_tool import get_default_sorted_list
from src.a17_idea_logic.idea_config import (
    get_quick_ideas_column_ref,
    get_idea_sqlite_types,
)
from sqlite3 import Connection as sqlite3_Connection


CREATE_JOB_BUDMEMB_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL, _fund_agenda_ratio_give REAL, _fund_agenda_ratio_take REAL)"""
CREATE_JOB_BUDACCT_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL, _fund_agenda_ratio_give REAL, _fund_agenda_ratio_take REAL, _inallocable_debtit_belief REAL, _irrational_debtit_belief REAL)"""
CREATE_JOB_BUDGROU_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_groupunit_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, group_label TEXT, fund_coin REAL, bridge TEXT, _credor_pool REAL, _debtor_pool REAL, _fund_give REAL, _fund_take REAL, _fund_agenda_give REAL, _fund_agenda_take REAL)"""
CREATE_JOB_BUDAWAR_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL, _fund_give REAL, _fund_take REAL)"""
CREATE_JOB_BUDFACT_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL)"""
CREATE_JOB_BUDHEAL_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, road TEXT, healer_name TEXT)"""
CREATE_JOB_BUDPREM_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor INTEGER, _task INTEGER, _status INTEGER)"""
CREATE_JOB_BUDREAS_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite INTEGER, _task INTEGER, _status INTEGER, _base_item_active_value INTEGER)"""
CREATE_JOB_BUDTEAM_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, road TEXT, team_tag TEXT, _owner_name_team INTEGER)"""
CREATE_JOB_BUDITEM_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor INTEGER, denom INTEGER, morph INTEGER, gogo_want REAL, stop_want REAL, mass INTEGER, pledge INTEGER, problem_bool INTEGER, fund_coin REAL, _active INTEGER, _task INTEGER, _fund_onset REAL, _fund_cease REAL, _fund_ratio REAL, _gogo_calc REAL, _stop_calc REAL, _level INTEGER, _range_evaluated INTEGER, _descendant_pledge_count INTEGER, _healerlink_ratio REAL, _all_acct_cred INTEGER, _all_acct_debt INTEGER)"""
CREATE_JOB_BUDUNIT_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_job (world_id TEXT, fisc_title TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally INTEGER, fund_coin REAL, penny REAL, respect_bit REAL, _rational INTEGER, _keeps_justified INTEGER, _offtrack_fund REAL, _sum_healerlink_share REAL, _keeps_buildable INTEGER, _tree_traverse_count INTEGER)"""


def get_job_create_table_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership_job": CREATE_JOB_BUDMEMB_SQLSTR,
        "bud_acctunit_job": CREATE_JOB_BUDACCT_SQLSTR,
        "bud_groupunit_job": CREATE_JOB_BUDGROU_SQLSTR,
        "bud_item_awardlink_job": CREATE_JOB_BUDAWAR_SQLSTR,
        "bud_item_factunit_job": CREATE_JOB_BUDFACT_SQLSTR,
        "bud_item_healerlink_job": CREATE_JOB_BUDHEAL_SQLSTR,
        "bud_item_reason_premiseunit_job": CREATE_JOB_BUDPREM_SQLSTR,
        "bud_item_reasonunit_job": CREATE_JOB_BUDREAS_SQLSTR,
        "bud_item_teamlink_job": CREATE_JOB_BUDTEAM_SQLSTR,
        "bud_itemunit_job": CREATE_JOB_BUDITEM_SQLSTR,
        "budunit_job": CREATE_JOB_BUDUNIT_SQLSTR,
    }


def create_job_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_job_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)
