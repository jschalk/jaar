from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import get_row_count
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
    present_time_str,
    amount_str,
    hour_title_str,
    cumlative_minute_str,
    cumlative_day_str,
    month_title_str,
    weekday_order_str,
    weekday_title_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_config import idea_number_str, get_idea_sqlite_types
from src.f09_idea.pandas_tool import get_pragma_table_fetchall, get_custom_sorted_list
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f10_etl.transformers import (
    etl_aft_face_csv_files_to_fiscal_db,
    create_fiscal_tables,
    idea_staging_tables2fiscal_staging_tables,
    fiscal_staging_tables2fiscal_agg_tables,
    etl_fiscal_staging_tables_to_fiscal_csvs,
    etl_fiscal_agg_tables_to_fiscal_csvs,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_fiscal_staging_tables2fiscal_agg_tables_PassesOnly_fiscal_title():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)

        cursor = fiscal_db_conn.cursor()
        x_fis = FiscalPrimeObjsRef()
        insert_staging_sqlstr = f"""
INSERT INTO {x_fis.unit_stage_tablename} (idea_number, face_name, event_int, fiscal_title)
VALUES
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 4
        assert get_row_count(fiscal_db_conn, x_fis.unit_agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.unit_agg_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.unit_agg_tablename};")
        fiscalunit_agg_rows = cursor.fetchall()
        expected_row0 = (
            accord23_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # present_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        expected_row1 = (
            accord45_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # present_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        print(f"{fiscalunit_agg_rows[0]=}")
        print(f"      {expected_row0=}")
        assert fiscalunit_agg_rows == [expected_row0, expected_row1]


def test_fiscal_staging_tables2fiscal_agg_tables_Scenario0_fiscalunit_WithNo_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_fund_coin = 11
    a23_penny = 22
    a23_respect_bit = 33
    a23_present_time = 44
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_title = "accord23_timeline"
    x_objs = FiscalPrimeObjsRef()
    x_cols = FiscalPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        staging_tablename = x_objs.unit_stage_tablename
        insert_staging_sqlstr = f"""
INSERT INTO {staging_tablename} ({x_cols.unit_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
, ('br00555','{sue_inx}',{event7},'{accord45_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
, ('br00666','{sue_inx}',{event7},'{accord45_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
;
"""
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = x_objs.unit_agg_tablename
        assert get_row_count(fiscal_db_conn, agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, agg_tablename) != 0
        agg_columns = x_cols.unit_agg_csv_header
        select_agg_sqlstr = f"SELECT {agg_columns} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (
            accord23_str,
            a23_fund_coin,
            a23_penny,
            a23_respect_bit,
            a23_present_time,
            a23_bridge,
            a23_c400_number,
            a23_yr1_jan1_offset,
            a23_monthday_distortion,
            a23_timeline_title,
        )
        expected_agg_row1 = (
            accord45_str,
            a23_fund_coin,
            a23_penny,
            a23_respect_bit,
            a23_present_time,
            a23_bridge,
            a23_c400_number,
            a23_yr1_jan1_offset,
            a23_monthday_distortion,
            a23_timeline_title,
        )
        print(f"{rows}")
        assert get_row_count(fiscal_db_conn, agg_tablename) == 2
        assert rows == [expected_agg_row0, expected_agg_row1]


def test_fiscal_staging_tables2fiscal_agg_tables_Scenario1_fiscalunit_With_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_fund_coin = 11
    a23_penny = 22
    a23_respect_bit = 33
    a23_present_time = 44
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_title = "accord23_timeline"
    x_objs = FiscalPrimeObjsRef()
    x_cols = FiscalPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        staging_tablename = x_objs.unit_stage_tablename
        insert_staging_sqlstr = f"""
INSERT INTO {staging_tablename} ({x_cols.unit_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}','Inconsistent fiscal data')
, ('br00555','{sue_inx}',{event7},'{accord45_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}','Inconsistent fiscal data')
, ('br00666','{sue_inx}',{event7},'{accord45_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}','Inconsistent fiscal data')
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = x_objs.unit_agg_tablename
        assert get_row_count(fiscal_db_conn, agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, agg_tablename) != 0
        select_agg_sqlstr = f"SELECT {x_cols.unit_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (
            accord23_str,
            a23_fund_coin,
            a23_penny,
            a23_respect_bit,
            a23_present_time,
            a23_bridge,
            a23_c400_number,
            a23_yr1_jan1_offset,
            a23_monthday_distortion,
            a23_timeline_title,
        )
        # print(f"{rows}")
        assert get_row_count(fiscal_db_conn, agg_tablename) == 1
        assert rows == [expected_agg_row0]


def test_fiscal_staging_tables2fiscal_agg_tables_Scenario2_fiscalhour_Some_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    event9 = 9
    accord23_str = "accord23"
    accord45_str = "accord45"
    _4pm_str = "4pm"
    _8pm_str = "8pm"
    cumlative_minute_1 = 44
    cumlative_minute_2 = 77
    x_error_message = "Inconsistent fiscal data"
    x_objs = FiscalPrimeObjsRef()
    x_cols = FiscalPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        staging_tablename = x_objs.hour_stage_tablename
        insert_staging_sqlstr = f"""
INSERT INTO {staging_tablename} ({x_cols.hour_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{_4pm_str}',{cumlative_minute_1},NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{_4pm_str}',{cumlative_minute_1},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{_4pm_str}',{cumlative_minute_1},'{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord45_str}','{_4pm_str}',{cumlative_minute_2},'{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{_8pm_str}',{cumlative_minute_2},NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = x_objs.hour_agg_tablename
        assert get_row_count(fiscal_db_conn, agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, agg_tablename) == 2
        select_agg_sqlstr = f"SELECT {x_cols.hour_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, _4pm_str, cumlative_minute_1)
        expected_agg_row1 = (accord23_str, _8pm_str, cumlative_minute_2)
        assert rows == [expected_agg_row0, expected_agg_row1]


def test_fiscal_staging_tables2fiscal_agg_tables_Scenario3_fiscalmont_Some_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    event9 = 9
    accord23_str = "accord23"
    accord45_str = "accord45"
    apr_str = "Apr"
    aug_str = "Aug"
    cumlative_day_1 = 44
    cumlative_day_2 = 77
    x_error_message = "Inconsistent fiscal data"
    x_objs = FiscalPrimeObjsRef()
    x_cols = FiscalPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        insert_staging_sqlstr = f"""
INSERT INTO {x_objs.mont_stage_tablename} ({x_cols.mont_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{apr_str}',{cumlative_day_1},NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{apr_str}',{cumlative_day_1},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{aug_str}',{cumlative_day_1},'{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord45_str}','{aug_str}',{cumlative_day_2},'{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{aug_str}',{cumlative_day_2},NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = x_objs.mont_agg_tablename
        assert get_row_count(fiscal_db_conn, agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, agg_tablename) == 2
        select_agg_sqlstr = f"SELECT {x_cols.mont_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, apr_str, cumlative_day_1)
        expected_agg_row1 = (accord23_str, aug_str, cumlative_day_2)
        assert rows == [expected_agg_row0, expected_agg_row1]


def test_fiscal_staging_tables2fiscal_agg_tables_Scenario4_fiscalweek_Some_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    event9 = 9
    accord23_str = "accord23"
    accord45_str = "accord45"
    mon_str = "Mon"
    wed_str = "Wed"
    weekday_order_1 = 4
    weekday_order_2 = 7
    x_error_message = "Inconsistent fiscal data"
    x_objs = FiscalPrimeObjsRef()
    x_cols = FiscalPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        insert_staging_sqlstr = f"""
INSERT INTO {x_objs.week_stage_tablename} ({x_cols.week_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{mon_str}',{weekday_order_1},NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{mon_str}',{weekday_order_1},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{wed_str}',{weekday_order_1},'{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord45_str}','{wed_str}',{weekday_order_2},'{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{wed_str}',{weekday_order_2},NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = x_objs.week_agg_tablename
        assert get_row_count(fiscal_db_conn, agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, agg_tablename) == 2
        select_agg_sqlstr = f"SELECT {x_cols.week_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, mon_str, weekday_order_1)
        expected_agg_row1 = (accord23_str, wed_str, weekday_order_2)
        assert rows == [expected_agg_row0, expected_agg_row1]


def test_fiscal_staging_tables2fiscal_agg_tables_Scenario5_fiscaldeal_Some_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    event9 = 9
    accord23_str = "accord23"
    accord45_str = "accord45"
    bob_inx = "Bobby"
    t1_time_int = 33
    t1_quota_1 = 200
    t1_quota_2 = 300
    t2_time_int = 55
    t2_quota = 400
    x_error_message = "Inconsistent fiscal data"
    x_objs = FiscalPrimeObjsRef()
    x_cols = FiscalPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        insert_staging_sqlstr = f"""
INSERT INTO {x_objs.deal_stage_tablename} ({x_cols.deal_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{bob_inx}',{t1_time_int},{t1_quota_1},'{x_error_message}')
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{bob_inx}',{t1_time_int},{t1_quota_2},'{x_error_message}')
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{bob_inx}',{t2_time_int},{t2_quota},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{bob_inx}',{t2_time_int},{t2_quota},NULL)
, ('br00333','{sue_inx}',{event9},'{accord45_str}','{bob_inx}',{t1_time_int},{t1_quota_1},NULL)
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{bob_inx}',{t2_time_int},{t2_quota},NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = x_objs.deal_agg_tablename
        assert get_row_count(fiscal_db_conn, agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, agg_tablename) == 3
        select_agg_sqlstr = f"SELECT {x_cols.deal_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, bob_inx, t2_time_int, t2_quota)
        expected_agg_row1 = (accord45_str, bob_inx, t1_time_int, t1_quota_1)
        expected_agg_row2 = (accord45_str, bob_inx, t2_time_int, t2_quota)
        assert rows == [expected_agg_row0, expected_agg_row1, expected_agg_row2]


def test_fiscal_staging_tables2fiscal_agg_tables_Scenario6_fiscalcash_Some_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    event9 = 9
    accord23_str = "accord23"
    accord45_str = "accord45"
    bob_inx = "Bobby"
    yao_inx = "Yao"
    t1_time_int = 33
    t1_amount_1 = 200
    t1_amount_2 = 300
    t2_time_int = 55
    t2_amount = 400
    x_error_message = "Inconsistent fiscal data"
    x_objs = FiscalPrimeObjsRef()
    x_cols = FiscalPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        insert_staging_sqlstr = f"""
INSERT INTO {x_objs.cash_stage_tablename} ({x_cols.cash_staging_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',{t1_time_int},{t1_amount_1},'{x_error_message}')
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',{t1_time_int},{t1_amount_2},'{x_error_message}')
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',{t2_time_int},{t2_amount},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}',{t2_time_int},{t2_amount},NULL)
, ('br00333','{sue_inx}',{event9},'{accord45_str}','{bob_inx}','{yao_inx}',{t1_time_int},{t1_amount_1},NULL)
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{bob_inx}','{yao_inx}',{t2_time_int},{t2_amount},NULL)
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{bob_inx}','{yao_inx}',{t2_time_int},NULL,NULL)
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = x_objs.cash_agg_tablename
        assert get_row_count(fiscal_db_conn, agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, agg_tablename) == 3
        select_agg_sqlstr = f"SELECT {x_cols.cash_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, bob_inx, yao_inx, t2_time_int, t2_amount)
        expected_agg_row1 = (accord45_str, bob_inx, yao_inx, t1_time_int, t1_amount_1)
        expected_agg_row2 = (accord45_str, bob_inx, yao_inx, t2_time_int, t2_amount)
        assert rows == [expected_agg_row0, expected_agg_row1, expected_agg_row2]


def test_etl_fiscal_agg_tables_to_fiscal_csvs_CreateFiles():
    # sourcery skip: extract-method
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        cursor = fiscal_db_conn.cursor()
        fiscal_mstr_dir = get_test_etl_dir()
        x_fis = FiscalPrimeObjsRef(fiscal_mstr_dir)
        insert_agg_sqlstr = f"""
INSERT INTO {x_fis.unit_agg_tablename} ({fiscal_title_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_agg_sqlstr)
        assert os_path_exists(x_fis.unit_agg_csv_path) is False
        assert os_path_exists(x_fis.deal_agg_csv_path) is False
        assert os_path_exists(x_fis.cash_agg_csv_path) is False
        assert os_path_exists(x_fis.hour_agg_csv_path) is False
        assert os_path_exists(x_fis.mont_agg_csv_path) is False
        assert os_path_exists(x_fis.week_agg_csv_path) is False

        # WHEN
        etl_fiscal_agg_tables_to_fiscal_csvs(fiscal_db_conn, fiscal_mstr_dir)

        # THEN
        assert os_path_exists(x_fis.unit_agg_csv_path)
        assert os_path_exists(x_fis.deal_agg_csv_path)
        assert os_path_exists(x_fis.cash_agg_csv_path)
        assert os_path_exists(x_fis.hour_agg_csv_path)
        assert os_path_exists(x_fis.mont_agg_csv_path)
        assert os_path_exists(x_fis.week_agg_csv_path)
        unit_agg_csv_filename = x_fis.unit_agg_csv_filename
        generated_fiscalunit_csv = open_file(fiscal_mstr_dir, unit_agg_csv_filename)
        expected_fiscalunit_csv_str = f"""{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{present_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
        assert generated_fiscalunit_csv == expected_fiscalunit_csv_str
