from src.f00_instrument.db_toolbox import (
    db_table_exists,
    get_row_count,
    create_table_from_columns,
    create_inconsistency_query,
)
from src.f01_road.finance_tran import bridge_str, quota_str, time_int_str
from src.f03_chrono.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_title_str,
)
from src.f04_gift.atom_config import (
    acct_name_str,
    face_name_str,
    fiscal_title_str,
    owner_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f07_fiscal.fiscal_config import (
    fiscal_cashbook_str,
    fiscal_deal_episode_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
    fiscalunit_str,
    present_time_str,
    amount_str,
    hour_title_str,
    cumlative_minute_str,
    cumlative_day_str,
    month_title_str,
    weekday_order_str,
    weekday_title_str,
)
from src.f08_pidgin.pidgin_config import event_int_str, pidginunit_str
from src.f09_idea.idea_config import (
    idea_number_str,
    get_idea_sqlite_types,
    get_idea_config_dict,
    idea_type_str,
)
from src.f09_idea.pandas_tool import get_pragma_table_fetchall, get_custom_sorted_list
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f10_etl.tran_sqlstrs import create_fiscal_tables, get_inconsistency_sqlstrs
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_create_fiscal_tables_CreatesFiscalStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fis_objs = FiscalPrimeObjsRef()
        fis_cols = FiscalPrimeColumnsRef()
        assert db_table_exists(fiscal_db_conn, fis_objs.unit_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.deal_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.cash_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.hour_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.mont_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.week_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.unit_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.deal_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.cash_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.hour_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.mont_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fis_objs.week_stage_tablename) is False

        # WHEN
        create_fiscal_tables(fiscal_db_conn)

        # THEN
        assert db_table_exists(fiscal_db_conn, fis_objs.unit_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.deal_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.cash_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.hour_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.mont_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.week_agg_tablename)

        assert db_table_exists(fiscal_db_conn, fis_objs.unit_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.deal_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.cash_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.hour_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.mont_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fis_objs.week_stage_tablename)

        fis_unit_agg_pragma = get_pragma_table_fetchall(fis_cols.unit_agg_columns)
        fis_deal_agg_pragma = get_pragma_table_fetchall(fis_cols.deal_agg_columns)
        fis_cash_agg_pragma = get_pragma_table_fetchall(fis_cols.cash_agg_columns)
        fis_hour_agg_pragma = get_pragma_table_fetchall(fis_cols.hour_agg_columns)
        fis_mont_agg_pragma = get_pragma_table_fetchall(fis_cols.mont_agg_columns)
        fis_week_agg_pragma = get_pragma_table_fetchall(fis_cols.week_agg_columns)
        fis_unit_stage_pragma = get_pragma_table_fetchall(fis_cols.unit_staging_columns)
        fis_deal_stage_pragma = get_pragma_table_fetchall(fis_cols.deal_staging_columns)
        fis_cash_stage_pragma = get_pragma_table_fetchall(fis_cols.cash_staging_columns)
        fis_hour_stage_pragma = get_pragma_table_fetchall(fis_cols.hour_staging_columns)
        fis_mont_stage_pragma = get_pragma_table_fetchall(fis_cols.mont_staging_columns)
        fis_week_stage_pragma = get_pragma_table_fetchall(fis_cols.week_staging_columns)
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"PRAGMA table_info({fis_objs.unit_agg_tablename})")
        assert fis_unit_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.deal_agg_tablename})")
        assert fis_deal_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.cash_agg_tablename})")
        assert fis_cash_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.hour_agg_tablename})")
        assert fis_hour_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.mont_agg_tablename})")
        assert fis_mont_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.week_agg_tablename})")
        assert fis_week_agg_pragma == cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({fis_objs.unit_stage_tablename})")
        assert fis_unit_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.deal_stage_tablename})")
        assert fis_deal_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.cash_stage_tablename})")
        assert fis_cash_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.hour_stage_tablename})")
        assert fis_hour_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.mont_stage_tablename})")
        assert fis_mont_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.week_stage_tablename})")
        assert fis_week_stage_pragma == cursor.fetchall()


def test_GlobalVariablesForFiscal_inconsistency_queryReturns_sqlstrs():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    idea_config = {
        x_category: category_config
        for x_category, category_config in idea_config.items()
        # if category_config.get(idea_type_str()) != pidginunit_str()
        if category_config.get(idea_type_str()) == fiscalunit_str()
    }

    exclude_cols = {"idea_number", "face_name", "event_int", "error_message"}
    with sqlite3_connect(":memory:") as conn:
        create_fiscal_tables(conn)

        for x_category, x_sqlstr in get_inconsistency_sqlstrs().items():
            x_tablename = f"{x_category}_staging"
            cat_config = idea_config.get(x_category)
            cat_focus_columns = set(cat_config.get("jkeys").keys())
            cat_focus_columns.remove(event_int_str())
            cat_focus_columns.remove(face_name_str())
            generated_cat_sqlstr = create_inconsistency_query(
                conn, x_tablename, cat_focus_columns, exclude_cols
            )
            assert x_sqlstr == generated_cat_sqlstr
            print(f"{x_category} checked...")
