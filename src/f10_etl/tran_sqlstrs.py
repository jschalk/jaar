from sqlite3 import Connection as sqlite3_Connection


CREATE_BUD_ACCT_MEMBERSHIP_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_agg (fiscal_title TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"""
CREATE_BUD_ACCT_MEMBERSHIP_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL, error_message TEXT)"""
CREATE_BUD_ACCTUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_agg (fiscal_title TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"""
CREATE_BUD_ACCTUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL, error_message TEXT)"""
CREATE_BUD_ITEM_AWARDLINK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_agg (fiscal_title TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL)"""
CREATE_BUD_ITEM_AWARDLINK_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL, error_message TEXT)"""
CREATE_BUD_ITEM_FACTUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_agg (fiscal_title TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL)"""
CREATE_BUD_ITEM_FACTUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL, error_message TEXT)"""
CREATE_BUD_ITEM_HEALERLINK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_agg (fiscal_title TEXT, road TEXT, healer_name TEXT)"""
CREATE_BUD_ITEM_HEALERLINK_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, road TEXT, healer_name TEXT, error_message TEXT)"""
CREATE_BUD_ITEM_REASON_PREMISEUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_agg (fiscal_title TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor REAL)"""
CREATE_BUD_ITEM_REASON_PREMISEUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor REAL, error_message TEXT)"""
CREATE_BUD_ITEM_REASONUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_agg (fiscal_title TEXT, road TEXT, base TEXT, base_item_active_requisite TEXT)"""
CREATE_BUD_ITEM_REASONUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, road TEXT, base TEXT, base_item_active_requisite TEXT, error_message TEXT)"""
CREATE_BUD_ITEM_TEAMLINK_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_agg (fiscal_title TEXT, road TEXT, team_tag TEXT)"""
CREATE_BUD_ITEM_TEAMLINK_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, road TEXT, team_tag TEXT, error_message TEXT)"""
CREATE_BUD_ITEMUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_agg (fiscal_title TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor REAL, denom REAL, morph INTEGER, gogo_want REAL, stop_want REAL, mass REAL, pledge INTEGER, problem_bool INTEGER)"""
CREATE_BUD_ITEMUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor REAL, denom REAL, morph INTEGER, gogo_want REAL, stop_want REAL, mass REAL, pledge INTEGER, problem_bool INTEGER, error_message TEXT)"""
CREATE_BUDUNIT_AGG_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_agg (fiscal_title TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, deal_time_int INTEGER, tally REAL, fund_coin REAL, penny REAL, respect_bit REAL)"""
CREATE_BUDUNIT_STAGING_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_staging (idea_number TEXT, face_name TEXT, event_int INTEGER, fiscal_title TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, deal_time_int INTEGER, tally REAL, fund_coin REAL, penny REAL, respect_bit REAL, error_message TEXT)"""
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


def get_all_idea_create_table_sqlstrs() -> dict[str, str]:
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
FISCALDEAL_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, owner_name, time_int
FROM fiscal_deal_episode_staging
GROUP BY fiscal_title, owner_name, time_int
HAVING MIN(quota) != MAX(quota)
"""
FISCALCASH_INCONSISTENCY_SQLSTR = """SELECT acct_name, fiscal_title, owner_name, time_int
FROM fiscal_cashbook_staging
GROUP BY acct_name, fiscal_title, owner_name, time_int
HAVING MIN(amount) != MAX(amount)
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
BUDMEMB_INCONSISTENCY_SQLSTR = """SELECT acct_name, fiscal_title, group_label
FROM bud_acct_membership_staging
GROUP BY acct_name, fiscal_title, group_label
HAVING MIN(credit_vote) != MAX(credit_vote)
    OR MIN(debtit_vote) != MAX(debtit_vote)
"""
BUDACCT_INCONSISTENCY_SQLSTR = """SELECT acct_name, fiscal_title
FROM bud_acctunit_staging
GROUP BY acct_name, fiscal_title
HAVING MIN(credit_belief) != MAX(credit_belief)
    OR MIN(debtit_belief) != MAX(debtit_belief)
"""
BUDAWAR_INCONSISTENCY_SQLSTR = """SELECT awardee_tag, fiscal_title, road
FROM bud_item_awardlink_staging
GROUP BY awardee_tag, fiscal_title, road
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
"""
BUDFACT_INCONSISTENCY_SQLSTR = """SELECT base, fiscal_title, road
FROM bud_item_factunit_staging
GROUP BY base, fiscal_title, road
HAVING MIN(pick) != MAX(pick)
    OR MIN(fopen) != MAX(fopen)
    OR MIN(fnigh) != MAX(fnigh)
"""
BUDHEAL_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, healer_name, road
FROM bud_item_healerlink_staging
GROUP BY fiscal_title, healer_name, road
None
"""
BUDPREM_INCONSISTENCY_SQLSTR = """SELECT base, fiscal_title, need, road
FROM bud_item_reason_premiseunit_staging
GROUP BY base, fiscal_title, need, road
HAVING MIN(nigh) != MAX(nigh)
    OR MIN(open) != MAX(open)
    OR MIN(divisor) != MAX(divisor)
"""
BUDREAS_INCONSISTENCY_SQLSTR = """SELECT base, fiscal_title, road
FROM bud_item_reasonunit_staging
GROUP BY base, fiscal_title, road
HAVING MIN(base_item_active_requisite) != MAX(base_item_active_requisite)
"""
BUDTEAM_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, road, team_tag
FROM bud_item_teamlink_staging
GROUP BY fiscal_title, road, team_tag
None
"""
BUDITEM_INCONSISTENCY_SQLSTR = """SELECT fiscal_title, item_title, parent_road
FROM bud_itemunit_staging
GROUP BY fiscal_title, item_title, parent_road
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
BUDUNIT_INCONSISTENCY_SQLSTR = """SELECT fiscal_title
FROM budunit_staging
GROUP BY fiscal_title
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


def get_all_inconsistency_sqlstrs() -> dict[str, str]:
    return {
        "fiscalunit": FISCALUNIT_INCONSISTENCY_SQLSTR,
        "fiscal_deal_episode": FISCALDEAL_INCONSISTENCY_SQLSTR,
        "fiscal_cashbook": FISCALCASH_INCONSISTENCY_SQLSTR,
        "fiscal_timeline_hour": FISCALHOUR_INCONSISTENCY_SQLSTR,
        "fiscal_timeline_month": FISCALMONT_INCONSISTENCY_SQLSTR,
        "fiscal_timeline_weekday": FISCALWEEK_INCONSISTENCY_SQLSTR,
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


FISCALUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALUNIT_INCONSISTENCY_SQLSTR}
)
UPDATE fiscalunit_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscalunit_staging.fiscal_title
;
"""
FISCALDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALDEAL_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_deal_episode_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_deal_episode_staging.fiscal_title
    AND inconsistency_rows.owner_name = fiscal_deal_episode_staging.owner_name
    AND inconsistency_rows.time_int = fiscal_deal_episode_staging.time_int
;
"""
FISCALCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALCASH_INCONSISTENCY_SQLSTR}
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
FISCALHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALHOUR_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_timeline_hour_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_hour_staging.fiscal_title
    AND inconsistency_rows.hour_title = fiscal_timeline_hour_staging.hour_title
;
"""
FISCALMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALMONT_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_timeline_month_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_month_staging.fiscal_title
    AND inconsistency_rows.month_title = fiscal_timeline_month_staging.month_title
;
"""
FISCALWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = f"""
WITH inconsistency_rows AS (
    {FISCALWEEK_INCONSISTENCY_SQLSTR}
)
UPDATE fiscal_timeline_weekday_staging
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.fiscal_title = fiscal_timeline_weekday_staging.fiscal_title
    AND inconsistency_rows.weekday_title = fiscal_timeline_weekday_staging.weekday_title
;
"""


def get_set_inconsistency_error_message_sqlstrs() -> dict[str, str]:
    return {
        "fiscalunit": FISCALUNIT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_deal_episode": FISCALDEAL_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_cashbook": FISCALCASH_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_timeline_hour": FISCALHOUR_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_timeline_month": FISCALMONT_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
        "fiscal_timeline_weekday": FISCALWEEK_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,
    }
