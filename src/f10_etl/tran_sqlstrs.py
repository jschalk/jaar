from src.f00_instrument.db_toolbox import create_table_from_columns
from src.f09_idea.idea_db_tool import get_custom_sorted_list
from src.f09_idea.idea_config import get_quick_ideas_column_ref, get_idea_sqlite_types
from sqlite3 import Connection as sqlite3_Connection


CREATE_BUD_ACCT_MEMBERSHIP_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"""
CREATE_BUD_ACCT_MEMBERSHIP_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"""
CREATE_BUD_ACCTUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"""
CREATE_BUD_ACCTUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"""
CREATE_BUD_ITEM_AWARDLINK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL)"""
CREATE_BUD_ITEM_AWARDLINK_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL, error_message TEXT)"""
CREATE_BUD_ITEM_FACTUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL)"""
CREATE_BUD_ITEM_FACTUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL, error_message TEXT)"""
CREATE_BUD_ITEM_HEALERLINK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, healer_name TEXT)"""
CREATE_BUD_ITEM_HEALERLINK_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, healer_name TEXT, error_message TEXT)"""
CREATE_BUD_ITEM_REASON_PREMISEUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor REAL)"""
CREATE_BUD_ITEM_REASON_PREMISEUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor REAL, error_message TEXT)"""
CREATE_BUD_ITEM_REASONUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite TEXT)"""
CREATE_BUD_ITEM_REASONUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite TEXT, error_message TEXT)"""
CREATE_BUD_ITEM_TEAMLINK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, team_tag TEXT)"""
CREATE_BUD_ITEM_TEAMLINK_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, road TEXT, team_tag TEXT, error_message TEXT)"""
CREATE_BUD_ITEMUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor REAL, denom REAL, morph INTEGER, gogo_want REAL, stop_want REAL, mass REAL, pledge INTEGER, problem_bool INTEGER)"""
CREATE_BUD_ITEMUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor REAL, denom REAL, morph INTEGER, gogo_want REAL, stop_want REAL, mass REAL, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"""
CREATE_BUDUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_agg (face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, deal_time_int INTEGER, tally REAL, fund_coin REAL, penny REAL, respect_bit REAL)"""
CREATE_BUDUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, deal_time_int INTEGER, tally REAL, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"""

CREATE_FISCAL_CASHBOOK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_cashbook_agg (fiscal_title TEXT, owner_name TEXT, acct_name TEXT, time_int INTEGER, amount REAL)"""
CREATE_FISCAL_CASHBOOK_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_cashbook_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, acct_name TEXT, time_int INTEGER, amount REAL, error_message TEXT)"""
CREATE_FISCAL_DEAL_EPISODE_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_deal_episode_agg (fiscal_title TEXT, owner_name TEXT, time_int INTEGER, quota REAL)"""
CREATE_FISCAL_DEAL_EPISODE_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_deal_episode_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, owner_name TEXT, time_int INTEGER, quota REAL, error_message TEXT)"""
CREATE_FISCAL_TIMELINE_HOUR_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_timeline_hour_agg (fiscal_title TEXT, hour_title TEXT, cumlative_minute INTEGER)"""
CREATE_FISCAL_TIMELINE_HOUR_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_timeline_hour_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, hour_title TEXT, cumlative_minute INTEGER, error_message TEXT)"""
CREATE_FISCAL_TIMELINE_MONTH_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_timeline_month_agg (fiscal_title TEXT, month_title TEXT, cumlative_day INTEGER)"""
CREATE_FISCAL_TIMELINE_MONTH_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_timeline_month_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, month_title TEXT, cumlative_day INTEGER, error_message TEXT)"""
CREATE_FISCAL_TIMELINE_WEEKDAY_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_timeline_weekday_agg (fiscal_title TEXT, weekday_title TEXT, weekday_order INTEGER)"""
CREATE_FISCAL_TIMELINE_WEEKDAY_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscal_timeline_weekday_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, weekday_title TEXT, weekday_order INTEGER, error_message TEXT)"""
CREATE_FISCALUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscalunit_agg (fiscal_title TEXT, fund_coin REAL, penny REAL, respect_bit REAL, present_time INTEGER, bridge TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, timeline_title TEXT)"""
CREATE_FISCALUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS fiscalunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, fund_coin REAL, penny REAL, respect_bit REAL, present_time INTEGER, bridge TEXT, c400_number INTEGER, yr1_jan1_offset INTEGER, monthday_distortion INTEGER, timeline_title TEXT, error_message TEXT)"""


def get_fiscal_create_table_sqlstrs() -> dict[str, str]:
    return {
        "fiscal_cashbook_agg": CREATE_FISCAL_CASHBOOK_AGG_SQLSTR,
        "fiscal_cashbook_staging": CREATE_FISCAL_CASHBOOK_STAGING_SQLSTR,
        "fiscal_deal_episode_agg": CREATE_FISCAL_DEAL_EPISODE_AGG_SQLSTR,
        "fiscal_deal_episode_staging": CREATE_FISCAL_DEAL_EPISODE_STAGING_SQLSTR,
        "fiscal_timeline_hour_agg": CREATE_FISCAL_TIMELINE_HOUR_AGG_SQLSTR,
        "fiscal_timeline_hour_staging": CREATE_FISCAL_TIMELINE_HOUR_STAGING_SQLSTR,
        "fiscal_timeline_month_agg": CREATE_FISCAL_TIMELINE_MONTH_AGG_SQLSTR,
        "fiscal_timeline_month_staging": CREATE_FISCAL_TIMELINE_MONTH_STAGING_SQLSTR,
        "fiscal_timeline_weekday_agg": CREATE_FISCAL_TIMELINE_WEEKDAY_AGG_SQLSTR,
        "fiscal_timeline_weekday_staging": CREATE_FISCAL_TIMELINE_WEEKDAY_STAGING_SQLSTR,
        "fiscalunit_agg": CREATE_FISCALUNIT_AGG_SQLSTR,
        "fiscalunit_staging": CREATE_FISCALUNIT_STAGING_SQLSTR,
    }


def get_bud_create_table_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership_agg": CREATE_BUD_ACCT_MEMBERSHIP_AGG_SQLSTR,
        "bud_acct_membership_staging": CREATE_BUD_ACCT_MEMBERSHIP_STAGING_SQLSTR,
        "bud_acctunit_agg": CREATE_BUD_ACCTUNIT_AGG_SQLSTR,
        "bud_acctunit_staging": CREATE_BUD_ACCTUNIT_STAGING_SQLSTR,
        "bud_item_awardlink_agg": CREATE_BUD_ITEM_AWARDLINK_AGG_SQLSTR,
        "bud_item_awardlink_staging": CREATE_BUD_ITEM_AWARDLINK_STAGING_SQLSTR,
        "bud_item_factunit_agg": CREATE_BUD_ITEM_FACTUNIT_AGG_SQLSTR,
        "bud_item_factunit_staging": CREATE_BUD_ITEM_FACTUNIT_STAGING_SQLSTR,
        "bud_item_healerlink_agg": CREATE_BUD_ITEM_HEALERLINK_AGG_SQLSTR,
        "bud_item_healerlink_staging": CREATE_BUD_ITEM_HEALERLINK_STAGING_SQLSTR,
        "bud_item_reason_premiseunit_agg": CREATE_BUD_ITEM_REASON_PREMISEUNIT_AGG_SQLSTR,
        "bud_item_reason_premiseunit_staging": CREATE_BUD_ITEM_REASON_PREMISEUNIT_STAGING_SQLSTR,
        "bud_item_reasonunit_agg": CREATE_BUD_ITEM_REASONUNIT_AGG_SQLSTR,
        "bud_item_reasonunit_staging": CREATE_BUD_ITEM_REASONUNIT_STAGING_SQLSTR,
        "bud_item_teamlink_agg": CREATE_BUD_ITEM_TEAMLINK_AGG_SQLSTR,
        "bud_item_teamlink_staging": CREATE_BUD_ITEM_TEAMLINK_STAGING_SQLSTR,
        "bud_itemunit_agg": CREATE_BUD_ITEMUNIT_AGG_SQLSTR,
        "bud_itemunit_staging": CREATE_BUD_ITEMUNIT_STAGING_SQLSTR,
        "budunit_agg": CREATE_BUDUNIT_AGG_SQLSTR,
        "budunit_staging": CREATE_BUDUNIT_STAGING_SQLSTR,
    }


def create_fiscal_tables(conn_or_cursor: sqlite3_Connection):
    for create_table_sqlstr in get_fiscal_create_table_sqlstrs().values():
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


BUDMEMB_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, acct_name, group_label
FROM bud_acct_membership_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, acct_name, group_label
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
"""
BUDACCT_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, acct_name
FROM bud_acctunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, acct_name
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
"""
BUDAWAR_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, road, awardee_tag
FROM bud_item_awardlink_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, awardee_tag
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
"""
BUDFACT_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, road, base
FROM bud_item_factunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base
HAVING MIN(pick) != MAX(pick)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
"""
BUDHEAL_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, road, healer_name
FROM bud_item_healerlink_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, healer_name

"""
BUDPREM_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, road, base, need
FROM bud_item_reason_premiseunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base, need
HAVING MIN(nigh) != MAX(nigh)
    OR MIN(open) != MAX(open)
    OR MIN(divisor) != MAX(divisor)
"""
BUDREAS_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, road, base
FROM bud_item_reasonunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base
HAVING MIN(base_item_active_requisite) != MAX(base_item_active_requisite)
"""
BUDTEAM_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, road, team_tag
FROM bud_item_teamlink_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, team_tag

"""
BUDITEM_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name, parent_road, item_title
FROM bud_itemunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, parent_road, item_title
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
BUDUNIT_INCONSISTENCY_SQLSTR = """SELECT face_name, event_int, fiscal_title, owner_name
FROM budunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name
HAVING MIN(credor_respect) != MAX(credor_respect)
    OR MIN(debtor_respect) != MAX(debtor_respect)
    OR MIN(fund_pool) != MAX(fund_pool)
    OR MIN(max_tree_traverse) != MAX(max_tree_traverse)
    OR MIN(deal_time_int) != MAX(deal_time_int)
    OR MIN(tally) != MAX(tally)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
"""

FISCALCASH_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, owner_name, acct_name, time_int
FROM fiscal_cashbook_staging
GROUP BY fiscal_title, owner_name, acct_name, time_int
HAVING MIN(amount) != MAX(amount)
"""
FISCALDEAL_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, owner_name, time_int
FROM fiscal_deal_episode_staging
GROUP BY fiscal_title, owner_name, time_int
HAVING MIN(quota) != MAX(quota)
"""
FISCALHOUR_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, hour_title
FROM fiscal_timeline_hour_staging
GROUP BY fiscal_title, hour_title
HAVING MIN(cumlative_minute) != MAX(cumlative_minute)
"""
FISCALMONT_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, month_title
FROM fiscal_timeline_month_staging
GROUP BY fiscal_title, month_title
HAVING MIN(cumlative_day) != MAX(cumlative_day)
"""
FISCALWEEK_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, weekday_title
FROM fiscal_timeline_weekday_staging
GROUP BY fiscal_title, weekday_title
HAVING MIN(weekday_order) != MAX(weekday_order)
"""
FISCALUNIT_INCONSISTENCY_SQLSTR = """SELECT fiscal_title
FROM fiscalunit_staging
GROUP BY fiscal_title
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


def get_fiscal_inconsistency_sqlstrs() -> dict[str, str]:
    return {
        "fiscalunit": FISCALUNIT_INCONSISTENCY_SQLSTR,
        "fiscal_deal_episode": FISCALDEAL_INCONSISTENCY_SQLSTR,
        "fiscal_cashbook": FISCALCASH_INCONSISTENCY_SQLSTR,
        "fiscal_timeline_hour": FISCALHOUR_INCONSISTENCY_SQLSTR,
        "fiscal_timeline_month": FISCALMONT_INCONSISTENCY_SQLSTR,
        "fiscal_timeline_weekday": FISCALWEEK_INCONSISTENCY_SQLSTR,
    }


BUDMEMB_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, acct_name, group_label
FROM bud_acct_membership_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, acct_name, group_label
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
)
UPDATE bud_acct_membership_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_acct_membership_staging.face_name
    AND inconsistency_rows.event_int = bud_acct_membership_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_acct_membership_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_acct_membership_staging.owner_name
    AND inconsistency_rows.acct_name = bud_acct_membership_staging.acct_name
    AND inconsistency_rows.group_label = bud_acct_membership_staging.group_label
;
"""
BUDACCT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, acct_name
FROM bud_acctunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, acct_name
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
)
UPDATE bud_acctunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_acctunit_staging.face_name
    AND inconsistency_rows.event_int = bud_acctunit_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_acctunit_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_acctunit_staging.owner_name
    AND inconsistency_rows.acct_name = bud_acctunit_staging.acct_name
;
"""
BUDAWAR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, road, awardee_tag
FROM bud_item_awardlink_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, awardee_tag
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE bud_item_awardlink_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_awardlink_staging.face_name
    AND inconsistency_rows.event_int = bud_item_awardlink_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_item_awardlink_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_item_awardlink_staging.owner_name
    AND inconsistency_rows.road = bud_item_awardlink_staging.road
    AND inconsistency_rows.awardee_tag = bud_item_awardlink_staging.awardee_tag
;
"""
BUDFACT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, road, base
FROM bud_item_factunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base
HAVING MIN(pick) != MAX(pick)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
)
UPDATE bud_item_factunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_factunit_staging.face_name
    AND inconsistency_rows.event_int = bud_item_factunit_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_item_factunit_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_item_factunit_staging.owner_name
    AND inconsistency_rows.road = bud_item_factunit_staging.road
    AND inconsistency_rows.base = bud_item_factunit_staging.base
;
"""
BUDHEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, road, healer_name
FROM bud_item_healerlink_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, healer_name

)
UPDATE bud_item_healerlink_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_healerlink_staging.face_name
    AND inconsistency_rows.event_int = bud_item_healerlink_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_item_healerlink_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_item_healerlink_staging.owner_name
    AND inconsistency_rows.road = bud_item_healerlink_staging.road
    AND inconsistency_rows.healer_name = bud_item_healerlink_staging.healer_name
;
"""
BUDPREM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, road, base, need
FROM bud_item_reason_premiseunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base, need
HAVING MIN(nigh) != MAX(nigh)
    OR MIN(open) != MAX(open)
    OR MIN(divisor) != MAX(divisor)
)
UPDATE bud_item_reason_premiseunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_reason_premiseunit_staging.face_name
    AND inconsistency_rows.event_int = bud_item_reason_premiseunit_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_item_reason_premiseunit_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_item_reason_premiseunit_staging.owner_name
    AND inconsistency_rows.road = bud_item_reason_premiseunit_staging.road
    AND inconsistency_rows.base = bud_item_reason_premiseunit_staging.base
    AND inconsistency_rows.need = bud_item_reason_premiseunit_staging.need
;
"""
BUDREAS_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, road, base
FROM bud_item_reasonunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base
HAVING MIN(base_item_active_requisite) != MAX(base_item_active_requisite)
)
UPDATE bud_item_reasonunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_reasonunit_staging.face_name
    AND inconsistency_rows.event_int = bud_item_reasonunit_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_item_reasonunit_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_item_reasonunit_staging.owner_name
    AND inconsistency_rows.road = bud_item_reasonunit_staging.road
    AND inconsistency_rows.base = bud_item_reasonunit_staging.base
;
"""
BUDTEAM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, road, team_tag
FROM bud_item_teamlink_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, road, team_tag

)
UPDATE bud_item_teamlink_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_item_teamlink_staging.face_name
    AND inconsistency_rows.event_int = bud_item_teamlink_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_item_teamlink_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_item_teamlink_staging.owner_name
    AND inconsistency_rows.road = bud_item_teamlink_staging.road
    AND inconsistency_rows.team_tag = bud_item_teamlink_staging.team_tag
;
"""
BUDITEM_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name, parent_road, item_title
FROM bud_itemunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name, parent_road, item_title
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
UPDATE bud_itemunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = bud_itemunit_staging.face_name
    AND inconsistency_rows.event_int = bud_itemunit_staging.event_int
    AND inconsistency_rows.fiscal_title = bud_itemunit_staging.fiscal_title
    AND inconsistency_rows.owner_name = bud_itemunit_staging.owner_name
    AND inconsistency_rows.parent_road = bud_itemunit_staging.parent_road
    AND inconsistency_rows.item_title = bud_itemunit_staging.item_title
;
"""
BUDUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT face_name, event_int, fiscal_title, owner_name
FROM budunit_staging
GROUP BY face_name, event_int, fiscal_title, owner_name
HAVING MIN(credor_respect) != MAX(credor_respect)
    OR MIN(debtor_respect) != MAX(debtor_respect)
    OR MIN(fund_pool) != MAX(fund_pool)
    OR MIN(max_tree_traverse) != MAX(max_tree_traverse)
    OR MIN(deal_time_int) != MAX(deal_time_int)
    OR MIN(tally) != MAX(tally)
    OR MIN(fund_coin) != MAX(fund_coin)
    OR MIN(penny) != MAX(penny)
    OR MIN(respect_bit) != MAX(respect_bit)
)
UPDATE budunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.face_name = budunit_staging.face_name
    AND inconsistency_rows.event_int = budunit_staging.event_int
    AND inconsistency_rows.fiscal_title = budunit_staging.fiscal_title
    AND inconsistency_rows.owner_name = budunit_staging.owner_name
;
"""

FISCALCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fiscal_title, owner_name, acct_name, time_int
FROM fiscal_cashbook_staging
GROUP BY fiscal_title, owner_name, acct_name, time_int
HAVING MIN(amount) != MAX(amount)
)
UPDATE fiscal_cashbook_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_cashbook_staging.fiscal_title
    AND inconsistency_rows.owner_name = fiscal_cashbook_staging.owner_name
    AND inconsistency_rows.acct_name = fiscal_cashbook_staging.acct_name
    AND inconsistency_rows.time_int = fiscal_cashbook_staging.time_int
;
"""
FISCALDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fiscal_title, owner_name, time_int
FROM fiscal_deal_episode_staging
GROUP BY fiscal_title, owner_name, time_int
HAVING MIN(quota) != MAX(quota)
)
UPDATE fiscal_deal_episode_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_deal_episode_staging.fiscal_title
    AND inconsistency_rows.owner_name = fiscal_deal_episode_staging.owner_name
    AND inconsistency_rows.time_int = fiscal_deal_episode_staging.time_int
;
"""
FISCALHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fiscal_title, hour_title
FROM fiscal_timeline_hour_staging
GROUP BY fiscal_title, hour_title
HAVING MIN(cumlative_minute) != MAX(cumlative_minute)
)
UPDATE fiscal_timeline_hour_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_hour_staging.fiscal_title
    AND inconsistency_rows.hour_title = fiscal_timeline_hour_staging.hour_title
;
"""
FISCALMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fiscal_title, month_title
FROM fiscal_timeline_month_staging
GROUP BY fiscal_title, month_title
HAVING MIN(cumlative_day) != MAX(cumlative_day)
)
UPDATE fiscal_timeline_month_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_month_staging.fiscal_title
    AND inconsistency_rows.month_title = fiscal_timeline_month_staging.month_title
;
"""
FISCALWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fiscal_title, weekday_title
FROM fiscal_timeline_weekday_staging
GROUP BY fiscal_title, weekday_title
HAVING MIN(weekday_order) != MAX(weekday_order)
)
UPDATE fiscal_timeline_weekday_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_weekday_staging.fiscal_title
    AND inconsistency_rows.weekday_title = fiscal_timeline_weekday_staging.weekday_title
;
"""
FISCALUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = """WITH inconsistency_rows AS (
SELECT fiscal_title
FROM fiscalunit_staging
GROUP BY fiscal_title
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
UPDATE fiscalunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscalunit_staging.fiscal_title
;
"""


def get_bud_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
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


def get_fiscal_update_inconsist_error_message_sqlstrs() -> dict[str, str]:
    return {
        "fiscalunit": FISCALUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_deal_episode": FISCALDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_cashbook": FISCALCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_timeline_hour": FISCALHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_timeline_month": FISCALMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_timeline_weekday": FISCALWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
    }


BUDMEMB_AGG_INSERT_SQLSTR = """INSERT INTO bud_acct_membership_agg (face_name, event_int, fiscal_title, owner_name, acct_name, group_label, credit_vote, debtit_vote)
SELECT face_name, event_int, fiscal_title, owner_name, acct_name, group_label, MAX(credit_vote), MAX(debtit_vote)
FROM bud_acct_membership_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, acct_name, group_label
;
"""
BUDACCT_AGG_INSERT_SQLSTR = """INSERT INTO bud_acctunit_agg (face_name, event_int, fiscal_title, owner_name, acct_name, credit_belief, debtit_belief)
SELECT face_name, event_int, fiscal_title, owner_name, acct_name, MAX(credit_belief), MAX(debtit_belief)
FROM bud_acctunit_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, acct_name
;
"""
BUDAWAR_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_awardlink_agg (face_name, event_int, fiscal_title, owner_name, road, awardee_tag, give_force, take_force)
SELECT face_name, event_int, fiscal_title, owner_name, road, awardee_tag, MAX(give_force), MAX(take_force)
FROM bud_item_awardlink_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, road, awardee_tag
;
"""
BUDFACT_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_factunit_agg (face_name, event_int, fiscal_title, owner_name, road, base, pick, fopen, fnigh)
SELECT face_name, event_int, fiscal_title, owner_name, road, base, MAX(pick), MAX(fopen), MAX(fnigh)
FROM bud_item_factunit_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base
;
"""
BUDHEAL_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_healerlink_agg (face_name, event_int, fiscal_title, owner_name, road, healer_name)
SELECT face_name, event_int, fiscal_title, owner_name, road, healer_name
FROM bud_item_healerlink_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, road, healer_name
;
"""
BUDPREM_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reason_premiseunit_agg (face_name, event_int, fiscal_title, owner_name, road, base, need, nigh, open, divisor)
SELECT face_name, event_int, fiscal_title, owner_name, road, base, need, MAX(nigh), MAX(open), MAX(divisor)
FROM bud_item_reason_premiseunit_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base, need
;
"""
BUDREAS_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_reasonunit_agg (face_name, event_int, fiscal_title, owner_name, road, base, base_item_active_requisite)
SELECT face_name, event_int, fiscal_title, owner_name, road, base, MAX(base_item_active_requisite)
FROM bud_item_reasonunit_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, road, base
;
"""
BUDTEAM_AGG_INSERT_SQLSTR = """INSERT INTO bud_item_teamlink_agg (face_name, event_int, fiscal_title, owner_name, road, team_tag)
SELECT face_name, event_int, fiscal_title, owner_name, road, team_tag
FROM bud_item_teamlink_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, road, team_tag
;
"""
BUDITEM_AGG_INSERT_SQLSTR = """INSERT INTO bud_itemunit_agg (face_name, event_int, fiscal_title, owner_name, parent_road, item_title, begin, close, addin, numor, denom, morph, gogo_want, stop_want, mass, pledge, problem_bool)
SELECT face_name, event_int, fiscal_title, owner_name, parent_road, item_title, MAX(begin), MAX(close), MAX(addin), MAX(numor), MAX(denom), MAX(morph), MAX(gogo_want), MAX(stop_want), MAX(mass), MAX(pledge), MAX(problem_bool)
FROM bud_itemunit_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name, parent_road, item_title
;
"""
BUDUNIT_AGG_INSERT_SQLSTR = """INSERT INTO budunit_agg (face_name, event_int, fiscal_title, owner_name, credor_respect, debtor_respect, fund_pool, max_tree_traverse, deal_time_int, tally, fund_coin, penny, respect_bit)
SELECT face_name, event_int, fiscal_title, owner_name, MAX(credor_respect), MAX(debtor_respect), MAX(fund_pool), MAX(max_tree_traverse), MAX(deal_time_int), MAX(tally), MAX(fund_coin), MAX(penny), MAX(respect_bit)
FROM budunit_staging
WHERE error_message IS NULL
GROUP BY face_name, event_int, fiscal_title, owner_name
;
"""

FISCALCASH_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_cashbook_agg (fiscal_title, owner_name, acct_name, time_int, amount)
SELECT fiscal_title, owner_name, acct_name, time_int, MAX(amount)
FROM fiscal_cashbook_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, owner_name, acct_name, time_int
;
"""
FISCALDEAL_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_deal_episode_agg (fiscal_title, owner_name, time_int, quota)
SELECT fiscal_title, owner_name, time_int, MAX(quota)
FROM fiscal_deal_episode_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, owner_name, time_int
;
"""
FISCALHOUR_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_timeline_hour_agg (fiscal_title, hour_title, cumlative_minute)
SELECT fiscal_title, hour_title, MAX(cumlative_minute)
FROM fiscal_timeline_hour_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, hour_title
;
"""
FISCALMONT_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_timeline_month_agg (fiscal_title, month_title, cumlative_day)
SELECT fiscal_title, month_title, MAX(cumlative_day)
FROM fiscal_timeline_month_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, month_title
;
"""
FISCALWEEK_AGG_INSERT_SQLSTR = """INSERT INTO fiscal_timeline_weekday_agg (fiscal_title, weekday_title, weekday_order)
SELECT fiscal_title, weekday_title, MAX(weekday_order)
FROM fiscal_timeline_weekday_staging
WHERE error_message IS NULL
GROUP BY fiscal_title, weekday_title
;
"""
FISCALUNIT_AGG_INSERT_SQLSTR = """INSERT INTO fiscalunit_agg (fiscal_title, fund_coin, penny, respect_bit, present_time, bridge, c400_number, yr1_jan1_offset, monthday_distortion, timeline_title)
SELECT fiscal_title, MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(present_time), MAX(bridge), MAX(c400_number), MAX(yr1_jan1_offset), MAX(monthday_distortion), MAX(timeline_title)
FROM fiscalunit_staging
WHERE error_message IS NULL
GROUP BY fiscal_title
;
"""


def get_bud_insert_agg_from_staging_sqlstrs() -> dict[str, str]:
    return {
        "bud_acct_membership": BUDMEMB_AGG_INSERT_SQLSTR,
        "bud_acctunit": BUDACCT_AGG_INSERT_SQLSTR,
        "bud_item_awardlink": BUDAWAR_AGG_INSERT_SQLSTR,
        "bud_item_factunit": BUDFACT_AGG_INSERT_SQLSTR,
        "bud_item_healerlink": BUDHEAL_AGG_INSERT_SQLSTR,
        "bud_item_reason_premiseunit": BUDPREM_AGG_INSERT_SQLSTR,
        "bud_item_reasonunit": BUDREAS_AGG_INSERT_SQLSTR,
        "bud_item_teamlink": BUDTEAM_AGG_INSERT_SQLSTR,
        "bud_itemunit": BUDITEM_AGG_INSERT_SQLSTR,
        "budunit": BUDUNIT_AGG_INSERT_SQLSTR,
    }


def get_fiscal_insert_agg_from_staging_sqlstrs() -> dict[str, str]:
    return {
        "fiscal_cashbook": FISCALCASH_AGG_INSERT_SQLSTR,
        "fiscal_deal_episode": FISCALDEAL_AGG_INSERT_SQLSTR,
        "fiscal_timeline_hour": FISCALHOUR_AGG_INSERT_SQLSTR,
        "fiscal_timeline_month": FISCALMONT_AGG_INSERT_SQLSTR,
        "fiscal_timeline_weekday": FISCALWEEK_AGG_INSERT_SQLSTR,
        "fiscalunit": FISCALUNIT_AGG_INSERT_SQLSTR,
    }


IDEA_STAGEABLE_DIMENS = {
    "br00000": ["fiscalunit"],
    "br00001": ["budunit", "fiscal_deal_episode", "fiscalunit"],
    "br00002": [
        "bud_acctunit",
        "budunit",
        "fiscal_cashbook",
        "fiscal_deal_episode",
        "fiscalunit",
    ],
    "br00003": ["fiscal_timeline_hour", "fiscalunit"],
    "br00004": ["fiscal_timeline_month", "fiscalunit"],
    "br00005": ["fiscal_timeline_weekday", "fiscalunit"],
    "br00011": ["bud_acctunit", "budunit", "fiscalunit"],
    "br00012": ["bud_acct_membership", "bud_acctunit", "budunit", "fiscalunit"],
    "br00013": ["bud_itemunit", "budunit", "fiscalunit"],
    "br00019": ["bud_itemunit", "budunit", "fiscalunit"],
    "br00020": ["bud_acct_membership", "bud_acctunit", "budunit", "fiscalunit"],
    "br00021": ["bud_acctunit", "budunit", "fiscalunit"],
    "br00022": ["bud_item_awardlink", "budunit", "fiscalunit"],
    "br00023": ["bud_item_factunit", "bud_item_reasonunit", "budunit", "fiscalunit"],
    "br00024": ["bud_item_teamlink", "budunit", "fiscalunit"],
    "br00025": ["bud_item_healerlink", "budunit", "fiscalunit"],
    "br00026": [
        "bud_item_factunit",
        "bud_item_reason_premiseunit",
        "bud_item_reasonunit",
        "budunit",
        "fiscalunit",
    ],
    "br00027": ["bud_item_factunit", "bud_item_reasonunit", "budunit", "fiscalunit"],
    "br00028": ["bud_itemunit", "budunit", "fiscalunit"],
    "br00029": ["budunit", "fiscalunit"],
    "br00036": ["bud_itemunit", "budunit", "fiscalunit"],
    "br00042": [],
    "br00043": [],
    "br00044": [],
    "br00045": [],
    "br00113": ["bud_acctunit", "budunit", "fiscalunit"],
    "br00115": ["bud_acctunit", "budunit", "fiscalunit"],
    "br00116": ["bud_acctunit", "budunit", "fiscalunit"],
    "br00117": ["bud_acctunit", "budunit", "fiscalunit"],
}
