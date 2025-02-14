from src.f00_instrument.db_toolbox import create_table_from_columns
from src.f09_idea.idea_db_tool import get_custom_sorted_list
from src.f09_idea.idea_config import get_quick_ideas_column_ref, get_idea_sqlite_types
from sqlite3 import Connection as sqlite3_Connection


CREATE_BUDMEMB_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"""
CREATE_BUDMEMB_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"""
CREATE_BUDMEMB_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT)"""
CREATE_BUDMEMB_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, group_label_ERASE TEXT, error_message TEXT)"""
CREATE_BUDACCT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"""
CREATE_BUDACCT_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"""
CREATE_BUDACCT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name_ERASE TEXT)"""
CREATE_BUDACCT_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDAWAR_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL)"""
CREATE_BUDAWAR_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL, error_message TEXT)"""
CREATE_BUDAWAR_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, awardee_tag_ERASE TEXT)"""
CREATE_BUDAWAR_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, awardee_tag_ERASE TEXT, error_message TEXT)"""
CREATE_BUDFACT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL)"""
CREATE_BUDFACT_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL, error_message TEXT)"""
CREATE_BUDFACT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT)"""
CREATE_BUDFACT_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT, error_message TEXT)"""
CREATE_BUDHEAL_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, healer_name TEXT)"""
CREATE_BUDHEAL_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, healer_name TEXT, error_message TEXT)"""
CREATE_BUDHEAL_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, healer_name_ERASE TEXT)"""
CREATE_BUDHEAL_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, healer_name_ERASE TEXT, error_message TEXT)"""
CREATE_BUDPREM_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor REAL)"""
CREATE_BUDPREM_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor REAL, error_message TEXT)"""
CREATE_BUDPREM_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, need_ERASE TEXT)"""
CREATE_BUDPREM_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, need_ERASE TEXT, error_message TEXT)"""
CREATE_BUDREAS_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite TEXT)"""
CREATE_BUDREAS_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite TEXT, error_message TEXT)"""
CREATE_BUDREAS_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT)"""
CREATE_BUDREAS_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base_ERASE TEXT, error_message TEXT)"""
CREATE_BUDTEAM_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, team_tag TEXT)"""
CREATE_BUDTEAM_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, team_tag TEXT, error_message TEXT)"""
CREATE_BUDTEAM_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, team_tag_ERASE TEXT)"""
CREATE_BUDTEAM_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, team_tag_ERASE TEXT, error_message TEXT)"""
CREATE_BUDITEM_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor REAL, denom REAL, morph INTEGER, gogo_want REAL, stop_want REAL, mass REAL, pledge INTEGER, problem_bool INTEGER)"""
CREATE_BUDITEM_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor REAL, denom REAL, morph INTEGER, gogo_want REAL, stop_want REAL, mass REAL, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"""
CREATE_BUDITEM_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, parent_road TEXT, item_title_ERASE TEXT)"""
CREATE_BUDITEM_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, parent_road TEXT, item_title_ERASE TEXT, error_message TEXT)"""
CREATE_BUDUNIT_PUT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally REAL, fund_coin REAL, penny REAL, respect_bit REAL)"""
CREATE_BUDUNIT_PUT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally REAL, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"""
CREATE_BUDUNIT_DEL_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_del_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name_ERASE TEXT)"""
CREATE_BUDUNIT_DEL_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_del_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name_ERASE TEXT, error_message TEXT)"""

CREATE_FISC_CASHBOOK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_agg (fisc_title TEXT, owner_name TEXT, acct_name TEXT, time_int INTEGER, amount REAL)"""
CREATE_FISC_CASHBOOK_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_cashbook_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, time_int INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISC_DEAL_EPISODE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_deal_episode_agg (fisc_title TEXT, owner_name TEXT, time_int INTEGER, quota REAL, ledger_depth INT)"""
CREATE_FISC_DEAL_EPISODE_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_deal_episode_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, time_int INTEGER, quota REAL, ledger_depth INT, error_message TEXT)"""
CREATE_FISC_TIMELINE_HOUR_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_agg (fisc_title TEXT, hour_title TEXT, cumlative_minute INTEGER)"""
CREATE_FISC_TIMELINE_HOUR_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_hour_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, hour_title TEXT, cumlative_minute INTEGER, error_message TEXT)"""
CREATE_FISC_TIMELINE_MONTH_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_agg (fisc_title TEXT, month_title TEXT, cumlative_day INTEGER)"""
CREATE_FISC_TIMELINE_MONTH_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_month_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, month_title TEXT, cumlative_day INTEGER, error_message TEXT)"""
CREATE_FISC_TIMELINE_WEEKDAY_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_agg (fisc_title TEXT, weekday_title TEXT, weekday_order INTEGER)"""
CREATE_FISC_TIMELINE_WEEKDAY_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fisc_timeline_weekday_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, weekday_title TEXT, weekday_order INTEGER, error_message TEXT)"""
CREATE_FISCUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_agg (fisc_title TEXT, fund_coin REAL, penny REAL, respect_bit REAL, present_time INTEGER, bridge TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, timeline_title TEXT)"""
CREATE_FISCUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fisc_title TEXT, fund_coin REAL, penny REAL, respect_bit REAL, present_time INTEGER, bridge TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, timeline_title TEXT, error_message TEXT)"""


def get_fisc_create_table_sqlstrs() -> dict[str, str]:
    return {
        "fisc_cashbook_agg": CREATE_FISC_CASHBOOK_AGG_SQLSTR,
        "fisc_cashbook_staging": CREATE_FISC_CASHBOOK_STAGING_SQLSTR,
        "fisc_deal_episode_agg": CREATE_FISC_DEAL_EPISODE_AGG_SQLSTR,
        "fisc_deal_episode_staging": CREATE_FISC_DEAL_EPISODE_STAGING_SQLSTR,
        "fisc_timeline_hour_agg": CREATE_FISC_TIMELINE_HOUR_AGG_SQLSTR,
        "fisc_timeline_hour_staging": CREATE_FISC_TIMELINE_HOUR_STAGING_SQLSTR,
        "fisc_timeline_month_agg": CREATE_FISC_TIMELINE_MONTH_AGG_SQLSTR,
        "fisc_timeline_month_staging": CREATE_FISC_TIMELINE_MONTH_STAGING_SQLSTR,
        "fisc_timeline_weekday_agg": CREATE_FISC_TIMELINE_WEEKDAY_AGG_SQLSTR,
        "fisc_timeline_weekday_staging": CREATE_FISC_TIMELINE_WEEKDAY_STAGING_SQLSTR,
        "fiscunit_agg": CREATE_FISCUNIT_AGG_SQLSTR,
        "fiscunit_staging": CREATE_FISCUNIT_STAGING_SQLSTR,
    }


def get_bud_create_table_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership_put_agg": CREATE_BUDMEMB_PUT_AGG_SQLSTR,
        "bud_acct_membership_put_staging": CREATE_BUDMEMB_PUT_STAGING_SQLSTR,
        "bud_acct_membership_del_agg": CREATE_BUDMEMB_DEL_AGG_SQLSTR,
        "bud_acct_membership_del_staging": CREATE_BUDMEMB_DEL_STAGING_SQLSTR,
        "bud_acctunit_put_agg": CREATE_BUDACCT_PUT_AGG_SQLSTR,
        "bud_acctunit_put_staging": CREATE_BUDACCT_PUT_STAGING_SQLSTR,
        "bud_acctunit_del_agg": CREATE_BUDACCT_DEL_AGG_SQLSTR,
        "bud_acctunit_del_staging": CREATE_BUDACCT_DEL_STAGING_SQLSTR,
        "bud_item_awardlink_put_agg": CREATE_BUDAWAR_PUT_AGG_SQLSTR,
        "bud_item_awardlink_put_staging": CREATE_BUDAWAR_PUT_STAGING_SQLSTR,
        "bud_item_awardlink_del_agg": CREATE_BUDAWAR_DEL_AGG_SQLSTR,
        "bud_item_awardlink_del_staging": CREATE_BUDAWAR_DEL_STAGING_SQLSTR,
        "bud_item_factunit_put_agg": CREATE_BUDFACT_PUT_AGG_SQLSTR,
        "bud_item_factunit_put_staging": CREATE_BUDFACT_PUT_STAGING_SQLSTR,
        "bud_item_factunit_del_agg": CREATE_BUDFACT_DEL_AGG_SQLSTR,
        "bud_item_factunit_del_staging": CREATE_BUDFACT_DEL_STAGING_SQLSTR,
        "bud_item_healerlink_put_agg": CREATE_BUDHEAL_PUT_AGG_SQLSTR,
        "bud_item_healerlink_put_staging": CREATE_BUDHEAL_PUT_STAGING_SQLSTR,
        "bud_item_healerlink_del_agg": CREATE_BUDHEAL_DEL_AGG_SQLSTR,
        "bud_item_healerlink_del_staging": CREATE_BUDHEAL_DEL_STAGING_SQLSTR,
        "bud_item_reason_premiseunit_put_agg": CREATE_BUDPREM_PUT_AGG_SQLSTR,
        "bud_item_reason_premiseunit_put_staging": CREATE_BUDPREM_PUT_STAGING_SQLSTR,
        "bud_item_reason_premiseunit_del_agg": CREATE_BUDPREM_DEL_AGG_SQLSTR,
        "bud_item_reason_premiseunit_del_staging": CREATE_BUDPREM_DEL_STAGING_SQLSTR,
        "bud_item_reasonunit_put_agg": CREATE_BUDREAS_PUT_AGG_SQLSTR,
        "bud_item_reasonunit_put_staging": CREATE_BUDREAS_PUT_STAGING_SQLSTR,
        "bud_item_reasonunit_del_agg": CREATE_BUDREAS_DEL_AGG_SQLSTR,
        "bud_item_reasonunit_del_staging": CREATE_BUDREAS_DEL_STAGING_SQLSTR,
        "bud_item_teamlink_put_agg": CREATE_BUDTEAM_PUT_AGG_SQLSTR,
        "bud_item_teamlink_put_staging": CREATE_BUDTEAM_PUT_STAGING_SQLSTR,
        "bud_item_teamlink_del_agg": CREATE_BUDTEAM_DEL_AGG_SQLSTR,
        "bud_item_teamlink_del_staging": CREATE_BUDTEAM_DEL_STAGING_SQLSTR,
        "bud_itemunit_put_agg": CREATE_BUDITEM_PUT_AGG_SQLSTR,
        "bud_itemunit_put_staging": CREATE_BUDITEM_PUT_STAGING_SQLSTR,
        "bud_itemunit_del_agg": CREATE_BUDITEM_DEL_AGG_SQLSTR,
        "bud_itemunit_del_staging": CREATE_BUDITEM_DEL_STAGING_SQLSTR,
        "budunit_put_agg": CREATE_BUDUNIT_PUT_AGG_SQLSTR,
        "budunit_put_staging": CREATE_BUDUNIT_PUT_STAGING_SQLSTR,
        "budunit_del_agg": CREATE_BUDUNIT_DEL_AGG_SQLSTR,
        "budunit_del_staging": CREATE_BUDUNIT_DEL_STAGING_SQLSTR,
    }


def create_fisc_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_fisc_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_bud_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_bud_create_table_sqlstrs().values():
        conn_or_cursor.execute(create_table_sqlstr)


def create_all_idea_tables(conn_or_cursor: sqlite3_Connection):
    idea_refs = get_quick_ideas_column_ref()
    for idea_number, idea_columns in idea_refs.items():
        x_tablename = f"{idea_number}_staging"
        x_columns = get_custom_sorted_list(idea_columns)
        col_types = get_idea_sqlite_types()
        create_table_from_columns(conn_or_cursor, x_tablename, x_columns, col_types)


BUDMEMB_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, acct_name, group_label
FROM bud_acct_membership_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, acct_name, group_label
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
"""
BUDACCT_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, acct_name
FROM bud_acctunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, acct_name
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
"""
BUDAWAR_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, road, awardee_tag
FROM bud_item_awardlink_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, awardee_tag
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
"""
BUDFACT_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, road, base
FROM bud_item_factunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, base
HAVING MIN(pick) != MAX(pick)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
"""
BUDHEAL_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, road, healer_name
FROM bud_item_healerlink_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, healer_name

"""
BUDPREM_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, road, base, need
FROM bud_item_reason_premiseunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, base, need
HAVING MIN(nigh) != MAX(nigh)
    OR MIN(open) != MAX(open)
    OR MIN(divisor) != MAX(divisor)
"""
BUDREAS_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, road, base
FROM bud_item_reasonunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, base
HAVING MIN(base_item_active_requisite) != MAX(base_item_active_requisite)
"""
BUDTEAM_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, road, team_tag
FROM bud_item_teamlink_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, team_tag

"""
BUDITEM_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name, parent_road, item_title
FROM bud_itemunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, parent_road, item_title
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
BUDUNIT_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fisc_title, owner_name
FROM budunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name
HAVING MIN(credor_respect) != MAX(credor_respect)
    OR MIN(debtor_respect) != MAX(debtor_respect)
    OR MIN(fund_pool) != MAX(fund_pool)
    OR MIN(max_tree_traverse) != MAX(max_tree_traverse)
    OR MIN(tally) != MAX(tally)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
"""

FISCCASH_INCONSISTENCY_SQLSTR = """SELECT fisc_title, owner_name, acct_name, time_int
FROM fisc_cashbook_staging
GROUP BY fisc_title, owner_name, acct_name, time_int
HAVING MIN(amount) != MAX(amount)
"""
FISCDEAL_INCONSISTENCY_SQLSTR = """SELECT fisc_title, owner_name, time_int
FROM fisc_deal_episode_staging
GROUP BY fisc_title, owner_name, time_int
HAVING MIN(quota) != MAX(quota)
    OR MIN(ledger_depth) != MAX(ledger_depth)
"""
FISCHOUR_INCONSISTENCY_SQLSTR = """SELECT fisc_title, hour_title
FROM fisc_timeline_hour_staging
GROUP BY fisc_title, hour_title
HAVING MIN(cumlative_minute) != MAX(cumlative_minute)
"""
FISCMONT_INCONSISTENCY_SQLSTR = """SELECT fisc_title, month_title
FROM fisc_timeline_month_staging
GROUP BY fisc_title, month_title
HAVING MIN(cumlative_day) != MAX(cumlative_day)
"""
FISCWEEK_INCONSISTENCY_SQLSTR = """SELECT fisc_title, weekday_title
FROM fisc_timeline_weekday_staging
GROUP BY fisc_title, weekday_title
HAVING MIN(weekday_order) != MAX(weekday_order)
"""
FISCUNIT_INCONSISTENCY_SQLSTR = """SELECT fisc_title
FROM fiscunit_staging
GROUP BY fisc_title
HAVING MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
    OR MIN(present_time) != MAX(present_time)
    OR MIN(bridge) != MAX(bridge)
    OR MIN(c400_number) != MAX(c400_number)
    OR MIN(yr1_jan1_offset) != MAX(yr1_jan1_offset)
    OR MIN(monthday_distortion) != MAX(monthday_distortion)
    OR MIN(timeline_title) != MAX(timeline_title)
"""


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


def get_fisc_inconsistency_sqlstrs() -> dict[str, str]:
    return {
        "fiscunit": FISCUNIT_INCONSISTENCY_SQLSTR,
        "fisc_deal_episode": FISCDEAL_INCONSISTENCY_SQLSTR,
        "fisc_cashbook": FISCCASH_INCONSISTENCY_SQLSTR,
        "fisc_timeline_hour": FISCHOUR_INCONSISTENCY_SQLSTR,
        "fisc_timeline_month": FISCMONT_INCONSISTENCY_SQLSTR,
        "fisc_timeline_weekday": FISCWEEK_INCONSISTENCY_SQLSTR,
    }


BUDMEMB_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, acct_name, group_label
FROM bud_acct_membership_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, acct_name, group_label
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
)
UPDATE bud_acct_membership_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_acct_membership_put_staging.face_name
    AND inconsistency_rows.event_int = bud_acct_membership_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_acct_membership_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_acct_membership_put_staging.owner_name
    AND inconsistency_rows.acct_name = bud_acct_membership_put_staging.acct_name
    AND inconsistency_rows.group_label = bud_acct_membership_put_staging.group_label
;
"""
BUDACCT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, acct_name
FROM bud_acctunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, acct_name
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
)
UPDATE bud_acctunit_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_acctunit_put_staging.face_name
    AND inconsistency_rows.event_int = bud_acctunit_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_acctunit_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_acctunit_put_staging.owner_name
    AND inconsistency_rows.acct_name = bud_acctunit_put_staging.acct_name
;
"""
BUDAWAR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, road, awardee_tag
FROM bud_item_awardlink_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, awardee_tag
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE bud_item_awardlink_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_awardlink_put_staging.face_name
    AND inconsistency_rows.event_int = bud_item_awardlink_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_item_awardlink_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_item_awardlink_put_staging.owner_name
    AND inconsistency_rows.road = bud_item_awardlink_put_staging.road
    AND inconsistency_rows.awardee_tag = bud_item_awardlink_put_staging.awardee_tag
;
"""
BUDFACT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, road, base
FROM bud_item_factunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, base
HAVING MIN(pick) != MAX(pick)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
)
UPDATE bud_item_factunit_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_factunit_put_staging.face_name
    AND inconsistency_rows.event_int = bud_item_factunit_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_item_factunit_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_item_factunit_put_staging.owner_name
    AND inconsistency_rows.road = bud_item_factunit_put_staging.road
    AND inconsistency_rows.base = bud_item_factunit_put_staging.base
;
"""
BUDHEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, road, healer_name
FROM bud_item_healerlink_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, healer_name

)
UPDATE bud_item_healerlink_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_healerlink_put_staging.face_name
    AND inconsistency_rows.event_int = bud_item_healerlink_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_item_healerlink_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_item_healerlink_put_staging.owner_name
    AND inconsistency_rows.road = bud_item_healerlink_put_staging.road
    AND inconsistency_rows.healer_name = bud_item_healerlink_put_staging.healer_name
;
"""
BUDPREM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, road, base, need
FROM bud_item_reason_premiseunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, base, need
HAVING MIN(nigh) != MAX(nigh)
    OR MIN(open) != MAX(open)
    OR MIN(divisor) != MAX(divisor)
)
UPDATE bud_item_reason_premiseunit_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_reason_premiseunit_put_staging.face_name
    AND inconsistency_rows.event_int = bud_item_reason_premiseunit_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_item_reason_premiseunit_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_item_reason_premiseunit_put_staging.owner_name
    AND inconsistency_rows.road = bud_item_reason_premiseunit_put_staging.road
    AND inconsistency_rows.base = bud_item_reason_premiseunit_put_staging.base
    AND inconsistency_rows.need = bud_item_reason_premiseunit_put_staging.need
;
"""
BUDREAS_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, road, base
FROM bud_item_reasonunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, base
HAVING MIN(base_item_active_requisite) != MAX(base_item_active_requisite)
)
UPDATE bud_item_reasonunit_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_reasonunit_put_staging.face_name
    AND inconsistency_rows.event_int = bud_item_reasonunit_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_item_reasonunit_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_item_reasonunit_put_staging.owner_name
    AND inconsistency_rows.road = bud_item_reasonunit_put_staging.road
    AND inconsistency_rows.base = bud_item_reasonunit_put_staging.base
;
"""
BUDTEAM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, road, team_tag
FROM bud_item_teamlink_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, road, team_tag

)
UPDATE bud_item_teamlink_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_teamlink_put_staging.face_name
    AND inconsistency_rows.event_int = bud_item_teamlink_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_item_teamlink_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_item_teamlink_put_staging.owner_name
    AND inconsistency_rows.road = bud_item_teamlink_put_staging.road
    AND inconsistency_rows.team_tag = bud_item_teamlink_put_staging.team_tag
;
"""
BUDITEM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name, parent_road, item_title
FROM bud_itemunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name, parent_road, item_title
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
UPDATE bud_itemunit_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_itemunit_put_staging.face_name
    AND inconsistency_rows.event_int = bud_itemunit_put_staging.event_int
    AND inconsistency_rows.fisc_title = bud_itemunit_put_staging.fisc_title
    AND inconsistency_rows.owner_name = bud_itemunit_put_staging.owner_name
    AND inconsistency_rows.parent_road = bud_itemunit_put_staging.parent_road
    AND inconsistency_rows.item_title = bud_itemunit_put_staging.item_title
;
"""
BUDUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fisc_title, owner_name
FROM budunit_put_staging
GROUP BY face_name, event_int, fisc_title, owner_name
HAVING MIN(credor_respect) != MAX(credor_respect)
    OR MIN(debtor_respect) != MAX(debtor_respect)
    OR MIN(fund_pool) != MAX(fund_pool)
    OR MIN(max_tree_traverse) != MAX(max_tree_traverse)
    OR MIN(tally) != MAX(tally)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
)
UPDATE budunit_put_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = budunit_put_staging.face_name
    AND inconsistency_rows.event_int = budunit_put_staging.event_int
    AND inconsistency_rows.fisc_title = budunit_put_staging.fisc_title
    AND inconsistency_rows.owner_name = budunit_put_staging.owner_name
;
"""
BUDMEMB_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_acct_membership_del_agg (face_name, event_int, fisc_title, owner_name, acct_name, group_label_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, acct_name, group_label_ERASE
FROM bud_acct_membership_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, acct_name, group_label_ERASE
;
"""
BUDACCT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_acctunit_del_agg (face_name, event_int, fisc_title, owner_name, acct_name_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, acct_name_ERASE
FROM bud_acctunit_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, acct_name_ERASE
;
"""
BUDAWAR_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_awardlink_del_agg (face_name, event_int, fisc_title, owner_name, road, awardee_tag_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, road, awardee_tag_ERASE
FROM bud_item_awardlink_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, awardee_tag_ERASE
;
"""
BUDFACT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_factunit_del_agg (face_name, event_int, fisc_title, owner_name, road, base_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, road, base_ERASE
FROM bud_item_factunit_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, base_ERASE
;
"""
BUDHEAL_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_healerlink_del_agg (face_name, event_int, fisc_title, owner_name, road, healer_name_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, road, healer_name_ERASE
FROM bud_item_healerlink_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, healer_name_ERASE
;
"""
BUDPREM_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reason_premiseunit_del_agg (face_name, event_int, fisc_title, owner_name, road, base, need_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, road, base, need_ERASE
FROM bud_item_reason_premiseunit_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, base, need_ERASE
;
"""
BUDREAS_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reasonunit_del_agg (face_name, event_int, fisc_title, owner_name, road, base_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, road, base_ERASE
FROM bud_item_reasonunit_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, base_ERASE
;
"""
BUDTEAM_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_teamlink_del_agg (face_name, event_int, fisc_title, owner_name, road, team_tag_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, road, team_tag_ERASE
FROM bud_item_teamlink_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, team_tag_ERASE
;
"""
BUDITEM_DEL_AGG_INSERT_SQLSTR = """INSERT INTO bud_itemunit_del_agg (face_name, event_int, fisc_title, owner_name, parent_road, item_title_ERASE)
SELECT face_name, event_int, fisc_title, owner_name, parent_road, item_title_ERASE
FROM bud_itemunit_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, parent_road, item_title_ERASE
;
"""
BUDUNIT_DEL_AGG_INSERT_SQLSTR = """INSERT INTO budunit_del_agg (face_name, event_int, fisc_title, owner_name_ERASE)
SELECT face_name, event_int, fisc_title, owner_name_ERASE
FROM budunit_del_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name_ERASE
;
"""

FISCCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_title, owner_name, acct_name, time_int
FROM fisc_cashbook_staging
GROUP BY fisc_title, owner_name, acct_name, time_int
HAVING MIN(amount) != MAX(amount)
)
UPDATE fisc_cashbook_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_title = fisc_cashbook_staging.fisc_title
    AND inconsistency_rows.owner_name = fisc_cashbook_staging.owner_name
    AND inconsistency_rows.acct_name = fisc_cashbook_staging.acct_name
    AND inconsistency_rows.time_int = fisc_cashbook_staging.time_int
;
"""
FISCDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_title, owner_name, time_int
FROM fisc_deal_episode_staging
GROUP BY fisc_title, owner_name, time_int
HAVING MIN(quota) != MAX(quota)
    OR MIN(ledger_depth) != MAX(ledger_depth)
)
UPDATE fisc_deal_episode_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_title = fisc_deal_episode_staging.fisc_title
    AND inconsistency_rows.owner_name = fisc_deal_episode_staging.owner_name
    AND inconsistency_rows.time_int = fisc_deal_episode_staging.time_int
;
"""
FISCHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_title, hour_title
FROM fisc_timeline_hour_staging
GROUP BY fisc_title, hour_title
HAVING MIN(cumlative_minute) != MAX(cumlative_minute)
)
UPDATE fisc_timeline_hour_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_title = fisc_timeline_hour_staging.fisc_title
    AND inconsistency_rows.hour_title = fisc_timeline_hour_staging.hour_title
;
"""
FISCMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_title, month_title
FROM fisc_timeline_month_staging
GROUP BY fisc_title, month_title
HAVING MIN(cumlative_day) != MAX(cumlative_day)
)
UPDATE fisc_timeline_month_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_title = fisc_timeline_month_staging.fisc_title
    AND inconsistency_rows.month_title = fisc_timeline_month_staging.month_title
;
"""
FISCWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_title, weekday_title
FROM fisc_timeline_weekday_staging
GROUP BY fisc_title, weekday_title
HAVING MIN(weekday_order) != MAX(weekday_order)
)
UPDATE fisc_timeline_weekday_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_title = fisc_timeline_weekday_staging.fisc_title
    AND inconsistency_rows.weekday_title = fisc_timeline_weekday_staging.weekday_title
;
"""
FISCUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fisc_title
FROM fiscunit_staging
GROUP BY fisc_title
HAVING MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
    OR MIN(present_time) != MAX(present_time)
    OR MIN(bridge) != MAX(bridge)
    OR MIN(c400_number) != MAX(c400_number)
    OR MIN(yr1_jan1_offset) != MAX(yr1_jan1_offset)
    OR MIN(monthday_distortion) != MAX(monthday_distortion)
    OR MIN(timeline_title) != MAX(timeline_title)
)
UPDATE fiscunit_staging
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_title = fiscunit_staging.fisc_title
;
"""


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


def get_fisc_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    return {
        "fiscunit": FISCUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_deal_episode": FISCDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_cashbook": FISCCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_timeline_hour": FISCHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_timeline_month": FISCMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fisc_timeline_weekday": FISCWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
    }


BUDMEMB_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_acct_membership_put_agg (face_name, event_int, fisc_title, owner_name, acct_name, group_label, credit_vote, debtit_vote)
SELECT face_name, event_int, fisc_title, owner_name, acct_name, group_label, MAX(credit_vote), MAX(debtit_vote)
FROM bud_acct_membership_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, acct_name, group_label
;
"""
BUDACCT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_acctunit_put_agg (face_name, event_int, fisc_title, owner_name, acct_name, credit_belief, debtit_belief)
SELECT face_name, event_int, fisc_title, owner_name, acct_name, MAX(credit_belief), MAX(debtit_belief)
FROM bud_acctunit_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, acct_name
;
"""
BUDAWAR_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_awardlink_put_agg (face_name, event_int, fisc_title, owner_name, road, awardee_tag, give_force, take_force)
SELECT face_name, event_int, fisc_title, owner_name, road, awardee_tag, MAX(give_force), MAX(take_force)
FROM bud_item_awardlink_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, awardee_tag
;
"""
BUDFACT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_factunit_put_agg (face_name, event_int, fisc_title, owner_name, road, base, pick, fopen, fnigh)
SELECT face_name, event_int, fisc_title, owner_name, road, base, MAX(pick), MAX(fopen), MAX(fnigh)
FROM bud_item_factunit_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, base
;
"""
BUDHEAL_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_healerlink_put_agg (face_name, event_int, fisc_title, owner_name, road, healer_name)
SELECT face_name, event_int, fisc_title, owner_name, road, healer_name
FROM bud_item_healerlink_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, healer_name
;
"""
BUDPREM_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reason_premiseunit_put_agg (face_name, event_int, fisc_title, owner_name, road, base, need, nigh, open, divisor)
SELECT face_name, event_int, fisc_title, owner_name, road, base, need, MAX(nigh), MAX(open), MAX(divisor)
FROM bud_item_reason_premiseunit_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, base, need
;
"""
BUDREAS_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reasonunit_put_agg (face_name, event_int, fisc_title, owner_name, road, base, base_item_active_requisite)
SELECT face_name, event_int, fisc_title, owner_name, road, base, MAX(base_item_active_requisite)
FROM bud_item_reasonunit_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, base
;
"""
BUDTEAM_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_teamlink_put_agg (face_name, event_int, fisc_title, owner_name, road, team_tag)
SELECT face_name, event_int, fisc_title, owner_name, road, team_tag
FROM bud_item_teamlink_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, road, team_tag
;
"""
BUDITEM_PUT_AGG_INSERT_SQLSTR = """INSERT INTO bud_itemunit_put_agg (face_name, event_int, fisc_title, owner_name, parent_road, item_title, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool)
SELECT face_name, event_int, fisc_title, owner_name, parent_road, item_title, MAX(begin), MAX(close), MAX(addin), MAX(numor), MAX(denom), MAX(morph), MAX(gogo_want), MAX(stop_want), MAX(mass), MAX(pledge), MAX(problem_bool)
FROM bud_itemunit_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name, parent_road, item_title
;
"""
BUDUNIT_PUT_AGG_INSERT_SQLSTR = """INSERT INTO budunit_put_agg (face_name, event_int, fisc_title, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, tally, fund_coin, penny, respect_bit)
SELECT face_name, event_int, fisc_title, owner_name, MAX(credor_respect), MAX(debtor_respect), MAX(fund_pool), MAX(max_tree_traverse), MAX(tally), MAX(fund_coin), MAX(penny), MAX(respect_bit)
FROM budunit_put_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fisc_title, owner_name
;
"""

FISCCASH_AGG_INSERT_SQLSTR = """INSERT INTO fisc_cashbook_agg (fisc_title, owner_name, acct_name, time_int, amount)
SELECT fisc_title, owner_name, acct_name, time_int, MAX(amount)
FROM fisc_cashbook_staging
WHERE error_message IS NULL
GROUP BY fisc_title, owner_name, acct_name, time_int
;
"""
FISCDEAL_AGG_INSERT_SQLSTR = """INSERT INTO fisc_deal_episode_agg (fisc_title, owner_name, time_int, quota, ledger_depth)
SELECT fisc_title, owner_name, time_int, MAX(quota), MAX(ledger_depth)
FROM fisc_deal_episode_staging
WHERE error_message IS NULL
GROUP BY fisc_title, owner_name, time_int
;
"""
FISCHOUR_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_hour_agg (fisc_title, hour_title, cumlative_minute)
SELECT fisc_title, hour_title, MAX(cumlative_minute)
FROM fisc_timeline_hour_staging
WHERE error_message IS NULL
GROUP BY fisc_title, hour_title
;
"""
FISCMONT_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_month_agg (fisc_title, month_title, cumlative_day)
SELECT fisc_title, month_title, MAX(cumlative_day)
FROM fisc_timeline_month_staging
WHERE error_message IS NULL
GROUP BY fisc_title, month_title
;
"""
FISCWEEK_AGG_INSERT_SQLSTR = """INSERT INTO fisc_timeline_weekday_agg (fisc_title, weekday_title, weekday_order)
SELECT fisc_title, weekday_title, MAX(weekday_order)
FROM fisc_timeline_weekday_staging
WHERE error_message IS NULL
GROUP BY fisc_title, weekday_title
;
"""
FISCUNIT_AGG_INSERT_SQLSTR = """INSERT INTO fiscunit_agg (fisc_title, fund_coin, penny, respect_bit, present_time, bridge, c400_number, yr1_jan1_offset, monthday_distortion, timeline_title)
SELECT fisc_title, MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(present_time), MAX(bridge), MAX(c400_number), MAX(yr1_jan1_offset), MAX(monthday_distortion), MAX(timeline_title)
FROM fiscunit_staging
WHERE error_message IS NULL
GROUP BY fisc_title
;
"""


def get_bud_insert_put_agg_from_staging_sqlstrs() -> dict[str, str]:
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


def get_bud_insert_del_agg_from_staging_sqlstrs() -> dict[str, str]:
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


def get_fisc_insert_agg_from_staging_sqlstrs() -> dict[str, str]:
    return {
        "fisc_cashbook": FISCCASH_AGG_INSERT_SQLSTR,
        "fisc_deal_episode": FISCDEAL_AGG_INSERT_SQLSTR,
        "fisc_timeline_hour": FISCHOUR_AGG_INSERT_SQLSTR,
        "fisc_timeline_month": FISCMONT_AGG_INSERT_SQLSTR,
        "fisc_timeline_weekday": FISCWEEK_AGG_INSERT_SQLSTR,
        "fiscunit": FISCUNIT_AGG_INSERT_SQLSTR,
    }


IDEA_STAGEABLE_PUT_DIMENS = {
    "br00000": ["fiscunit"],
    "br00001": ["budunit", "fisc_deal_episode", "fiscunit"],
    "br00002": [
        "bud_acctunit",
        "budunit",
        "fisc_cashbook",
        "fisc_deal_episode",
        "fiscunit",
    ],
    "br00003": ["fisc_timeline_hour", "fiscunit"],
    "br00004": ["fisc_timeline_month", "fiscunit"],
    "br00005": ["fisc_timeline_weekday", "fiscunit"],
    "br00011": ["bud_acctunit", "budunit", "fiscunit"],
    "br00012": ["bud_acct_membership", "bud_acctunit", "budunit", "fiscunit"],
    "br00013": ["bud_itemunit", "budunit", "fiscunit"],
    "br00019": ["bud_itemunit", "budunit", "fiscunit"],
    "br00020": ["bud_acct_membership", "bud_acctunit", "budunit", "fiscunit"],
    "br00021": ["bud_acctunit", "budunit", "fiscunit"],
    "br00022": ["bud_item_awardlink", "budunit", "fiscunit"],
    "br00023": ["bud_item_factunit", "bud_item_reasonunit", "budunit", "fiscunit"],
    "br00024": ["bud_item_teamlink", "budunit", "fiscunit"],
    "br00025": ["bud_item_healerlink", "budunit", "fiscunit"],
    "br00026": [
        "bud_item_factunit",
        "bud_item_reason_premiseunit",
        "bud_item_reasonunit",
        "budunit",
        "fiscunit",
    ],
    "br00027": ["bud_item_factunit", "bud_item_reasonunit", "budunit", "fiscunit"],
    "br00028": ["bud_itemunit", "budunit", "fiscunit"],
    "br00029": ["budunit", "fiscunit"],
    "br00036": ["bud_itemunit", "budunit", "fiscunit"],
    "br00042": [],
    "br00043": [],
    "br00044": [],
    "br00045": [],
    "br00050": ["bud_acctunit", "budunit", "fiscunit"],
    "br00051": ["budunit", "fiscunit"],
    "br00052": ["budunit", "fiscunit"],
    "br00053": ["budunit", "fiscunit"],
    "br00054": ["budunit", "fiscunit"],
    "br00055": ["budunit", "fiscunit"],
    "br00056": ["bud_item_factunit", "bud_item_reasonunit", "budunit", "fiscunit"],
    "br00057": ["budunit", "fiscunit"],
    "br00058": ["budunit", "fiscunit"],
    "br00059": ["fiscunit"],
    "br00113": ["bud_acctunit", "budunit", "fiscunit"],
    "br00115": ["bud_acctunit", "budunit", "fiscunit"],
    "br00116": ["bud_acctunit", "budunit", "fiscunit"],
    "br00117": ["bud_acctunit", "budunit", "fiscunit"],
}

IDEA_STAGEABLE_DEL_DIMENS = {
    "br00050": ["bud_acct_membership"],
    "br00051": ["bud_acctunit"],
    "br00052": ["bud_item_awardlink"],
    "br00054": ["bud_item_teamlink"],
    "br00055": ["bud_item_healerlink"],
    "br00056": ["bud_item_reason_premiseunit"],
    "br00057": ["bud_item_factunit", "bud_item_reasonunit"],
    "br00058": ["bud_itemunit"],
    "br00059": ["budunit"],
}


CREATE_FISC_EVENT_TIME_AGG_SQLSTR = """
CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
  fisc_title TEXT
, event_int INTEGER
, time_int INTEGER
, error_message TEXT
)
;
"""
INSERT_FISC_EVENT_TIME_AGG_SQLSTR = """
INSERT INTO fisc_event_time_agg (fisc_title, event_int, time_int)
SELECT fisc_title, event_int, time_int
FROM (
    SELECT fisc_title, event_int, time_int
    FROM fisc_cashbook_staging
    GROUP BY fisc_title, event_int, time_int
    UNION 
    SELECT fisc_title, event_int, time_int
    FROM fisc_deal_episode_staging
    GROUP BY fisc_title, event_int, time_int
)
ORDER BY fisc_title, event_int, time_int
;
"""
UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR = """
WITH EventTimeOrdered AS (
    SELECT fisc_title, event_int, time_int,
           LAG(time_int) OVER (PARTITION BY fisc_title ORDER BY event_int) AS prev_time_int
    FROM fisc_event_time_agg
)
UPDATE fisc_event_time_agg
SET error_message = CASE 
         WHEN EventTimeOrdered.prev_time_int > EventTimeOrdered.time_int
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.event_int = fisc_event_time_agg.event_int
    AND EventTimeOrdered.fisc_title = fisc_event_time_agg.fisc_title
    AND EventTimeOrdered.time_int = fisc_event_time_agg.time_int
;
"""


CREATE_FISC_OWNER_DEAL_TIME_AGG1_SQLSTR = """
CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
  fisc_title TEXT
, owner_name TEXT
, event_int INTEGER
, time_int INTEGER
, error_message TEXT
)
;
"""
INSERT_FISC_OWNER_DEAL_TIME_AGG1_SQLSTR = """
INSERT INTO fisc_ote1_agg (fisc_title, owner_name, event_int, time_int)
SELECT fisc_title, owner_name, event_int, time_int
FROM (
    SELECT fisc_title, owner_name, event_int, time_int
    FROM fisc_deal_episode_staging
    GROUP BY fisc_title, owner_name, event_int, time_int
)
ORDER BY fisc_title, owner_name, event_int, time_int
;
"""
