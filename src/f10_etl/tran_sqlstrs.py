from src.f00_instrument.file import create_path, get_dir_file_strs, save_file, open_file
from src.f00_instrument.db_toolbox import (
    create_table_from_columns,
    db_table_exists,
    get_table_columns,
)
from src.f01_road.road import FaceName, EventInt
from src.f08_pidgin.pidgin import get_pidginunit_from_json, inherit_pidginunit
from src.f08_pidgin.pidgin_config import get_quick_pidgens_column_ref
from src.f09_idea.idea_config import (
    get_idea_numbers,
    get_idea_format_filename,
    get_idea_category_ref,
    get_idea_sqlite_types,
)
from sqlite3 import Connection as sqlite3_Connection
from copy import copy as copy_copy


def create_fiscal_tables(conn_or_cursor: sqlite3_Connection):
    conn = conn_or_cursor
    fiscalunit_agg_cols = [
        "fiscal_title",
        "fund_coin",
        "penny",
        "respect_bit",
        "present_time",
        "bridge",
        "c400_number",
        "yr1_jan1_offset",
        "monthday_distortion",
        "timeline_title",
    ]
    fiscaldeal_agg_cols = ["fiscal_title", "owner_name", "time_int", "quota"]
    fiscalcash_agg_cols = [
        "fiscal_title",
        "owner_name",
        "acct_name",
        "time_int",
        "amount",
    ]
    fiscalhour_agg_cols = ["fiscal_title", "hour_title", "cumlative_minute"]
    fiscalmont_agg_cols = ["fiscal_title", "month_title", "cumlative_day"]
    fiscalweek_agg_cols = ["fiscal_title", "weekday_title", "weekday_order"]
    fiscalunit_agg = "fiscalunit_agg"
    fiscaldeal_agg = "fiscal_deal_episode_agg"
    fiscalcash_agg = "fiscal_cashbook_agg"
    fiscalhour_agg = "fiscal_timeline_hour_agg"
    fiscalmont_agg = "fiscal_timeline_month_agg"
    fiscalweek_agg = "fiscal_timeline_weekday_agg"
    col_types = get_idea_sqlite_types()
    create_table_from_columns(conn, fiscalunit_agg, fiscalunit_agg_cols, col_types)
    create_table_from_columns(conn, fiscaldeal_agg, fiscaldeal_agg_cols, col_types)
    create_table_from_columns(conn, fiscalcash_agg, fiscalcash_agg_cols, col_types)
    create_table_from_columns(conn, fiscalhour_agg, fiscalhour_agg_cols, col_types)
    create_table_from_columns(conn, fiscalmont_agg, fiscalmont_agg_cols, col_types)
    create_table_from_columns(conn, fiscalweek_agg, fiscalweek_agg_cols, col_types)

    staging_columns = ["idea_number", "face_name", "event_int"]
    fiscalunit_stage_cols = copy_copy(staging_columns)
    fiscaldeal_stage_cols = copy_copy(staging_columns)
    fiscalcash_stage_cols = copy_copy(staging_columns)
    fiscalhour_stage_cols = copy_copy(staging_columns)
    fiscalmont_stage_cols = copy_copy(staging_columns)
    fiscalweek_stage_cols = copy_copy(staging_columns)
    fiscalunit_agg_cols.extend(["error_message"])
    fiscaldeal_agg_cols.extend(["error_message"])
    fiscalcash_agg_cols.extend(["error_message"])
    fiscalhour_agg_cols.extend(["error_message"])
    fiscalmont_agg_cols.extend(["error_message"])
    fiscalweek_agg_cols.extend(["error_message"])
    fiscalunit_stage_cols.extend(fiscalunit_agg_cols)
    fiscaldeal_stage_cols.extend(fiscaldeal_agg_cols)
    fiscalcash_stage_cols.extend(fiscalcash_agg_cols)
    fiscalhour_stage_cols.extend(fiscalhour_agg_cols)
    fiscalmont_stage_cols.extend(fiscalmont_agg_cols)
    fiscalweek_stage_cols.extend(fiscalweek_agg_cols)
    fiscalunit_stage = "fiscalunit_staging"
    fiscaldeal_stage = "fiscal_deal_episode_staging"
    fiscalcash_stage = "fiscal_cashbook_staging"
    fiscalhour_stage = "fiscal_timeline_hour_staging"
    fiscalmont_stage = "fiscal_timeline_month_staging"
    fiscalweek_stage = "fiscal_timeline_weekday_staging"
    create_table_from_columns(conn, fiscalunit_stage, fiscalunit_stage_cols, col_types)
    create_table_from_columns(conn, fiscaldeal_stage, fiscaldeal_stage_cols, col_types)
    create_table_from_columns(conn, fiscalcash_stage, fiscalcash_stage_cols, col_types)
    create_table_from_columns(conn, fiscalhour_stage, fiscalhour_stage_cols, col_types)
    create_table_from_columns(conn, fiscalmont_stage, fiscalmont_stage_cols, col_types)
    create_table_from_columns(conn, fiscalweek_stage, fiscalweek_stage_cols, col_types)


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


def get_inconsistency_sqlstrs() -> dict[str, str]:
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
