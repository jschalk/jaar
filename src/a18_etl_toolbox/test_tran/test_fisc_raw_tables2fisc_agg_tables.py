from src.a00_data_toolboxs.file_toolbox import open_file
from src.a00_data_toolboxs.db_toolbox import get_row_count
from src.a02_finance_toolboxs.deal import bridge_str, fisc_tag_str
from src.a07_calendar_logic.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_tag_str,
)
from src.a08_bud_atom_logic.atom_config import fund_coin_str, penny_str, respect_bit_str
from src.a18_etl_toolbox.fisc_etl_tool import FiscPrimeObjsRef, FiscPrimeColumnsRef
from src.a18_etl_toolbox.transformers import (
    create_fisc_tables,
    fisc_raw_tables2fisc_agg_tables,
    etl_fisc_agg_tables_to_fisc_csvs,
)
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir
from sqlite3 import connect as sqlite3_connect
from os.path import exists as os_path_exists


def test_fisc_raw_tables2fisc_agg_tables_PassesOnly_fisc_tag():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)

        x_fisc = FiscPrimeObjsRef()
        insert_raw_sqlstr = f"""
INSERT INTO {x_fisc.unit_raw_tablename} (idea_number, face_name, event_int, fisc_tag)
VALUES
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, x_fisc.unit_raw_tablename) == 4
        assert get_row_count(cursor, x_fisc.unit_agg_tablename) == 0

        # WHEN
        fisc_raw_tables2fisc_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, x_fisc.unit_agg_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fisc.unit_agg_tablename};")
        fiscunit_agg_rows = cursor.fetchall()
        expected_row0 = (
            accord23_str,  # fisc_tag
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_tag
            None,  # job_listen_rotations
        )
        expected_row1 = (
            accord45_str,  # fisc_tag
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            # None,  # _offi_time_max
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_tag
            None,  # job_listen_rotations
        )
        print(f"{fiscunit_agg_rows[0]=}")
        print(f"      {expected_row0=}")
        assert fiscunit_agg_rows == [expected_row0, expected_row1]


def test_fisc_raw_tables2fisc_agg_tables_Scenario0_fiscunit_WithNo_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_fund_coin = 11
    a23_penny = 22
    a23_respect_bit = 33
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_tag = "accord23_timeline"
    a23_job_listen_rotations = 900
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        raw_tablename = x_objs.unit_raw_tablename
        insert_raw_sqlstr = f"""
INSERT INTO {raw_tablename} ({x_cols.unit_raw_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}',NULL)
, ('br00555','{sue_inx}',{event7},'{accord45_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}',NULL)
, ('br00666','{sue_inx}',{event7},'{accord45_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}',NULL)
;
"""
        cursor.execute(insert_raw_sqlstr)
        print(f"{x_objs.unit_raw_tablename=}")
        agg_tablename = x_objs.unit_agg_tablename
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fisc_raw_tables2fisc_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) != 0
        agg_columns = x_cols.unit_agg_csv_header
        select_agg_sqlstr = f"SELECT {agg_columns} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (
            accord23_str,
            a23_timeline_tag,
            a23_c400_number,
            a23_yr1_jan1_offset,
            a23_monthday_distortion,
            a23_fund_coin,
            a23_penny,
            a23_respect_bit,
            a23_bridge,
            a23_job_listen_rotations,
        )
        expected_agg_row1 = (
            accord45_str,
            a23_timeline_tag,
            a23_c400_number,
            a23_yr1_jan1_offset,
            a23_monthday_distortion,
            a23_fund_coin,
            a23_penny,
            a23_respect_bit,
            a23_bridge,
            a23_job_listen_rotations,
        )
        print(f"{rows}")
        assert get_row_count(cursor, agg_tablename) == 2
        assert rows == [expected_agg_row0, expected_agg_row1]


def test_fisc_raw_tables2fisc_agg_tables_Scenario1_fiscunit_With_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    a23_fund_coin = 11
    a23_penny = 22
    a23_respect_bit = 33
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_tag = "accord23_timeline"
    a23_job_listen_rotations = 900
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        raw_tablename = x_objs.unit_raw_tablename
        insert_raw_sqlstr = f"""
INSERT INTO {raw_tablename} ({x_cols.unit_raw_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}','Inconsistent data')
, ('br00555','{sue_inx}',{event7},'{accord45_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}','Inconsistent data')
, ('br00666','{sue_inx}',{event7},'{accord45_str}','{a23_timeline_tag}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},{a23_fund_coin},{a23_penny},{a23_respect_bit},'{a23_bridge}','{a23_job_listen_rotations}','Inconsistent data')
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        agg_tablename = x_objs.unit_agg_tablename
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fisc_raw_tables2fisc_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) != 0
        select_agg_sqlstr = f"SELECT {x_cols.unit_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (
            accord23_str,
            a23_timeline_tag,
            a23_c400_number,
            a23_yr1_jan1_offset,
            a23_monthday_distortion,
            a23_fund_coin,
            a23_penny,
            a23_respect_bit,
            a23_bridge,
            a23_job_listen_rotations,
        )
        # print(f"{rows}")
        assert get_row_count(cursor, agg_tablename) == 1
        assert rows == [expected_agg_row0]


def test_fisc_raw_tables2fisc_agg_tables_Scenario2_fischour_Some_error_message():
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
    x_error_message = "Inconsistent data"
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        raw_tablename = x_objs.hour_raw_tablename
        insert_raw_sqlstr = f"""
INSERT INTO {raw_tablename} ({x_cols.hour_raw_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{cumlative_minute_1},'{_4pm_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{cumlative_minute_1},'{_4pm_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{cumlative_minute_1},'{_4pm_str}','{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord45_str}',{cumlative_minute_2},'{_4pm_str}','{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord23_str}',{cumlative_minute_2},'{_8pm_str}',NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        agg_tablename = x_objs.hour_agg_tablename
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fisc_raw_tables2fisc_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 2
        select_agg_sqlstr = f"SELECT {x_cols.hour_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, cumlative_minute_1, _4pm_str)
        expected_agg_row1 = (accord23_str, cumlative_minute_2, _8pm_str)
        assert rows == [expected_agg_row0, expected_agg_row1]


def test_fisc_raw_tables2fisc_agg_tables_Scenario3_fiscmont_Some_error_message():
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
    x_error_message = "Inconsistent data"
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        insert_raw_sqlstr = f"""
INSERT INTO {x_objs.mont_raw_tablename} ({x_cols.mont_raw_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{cumlative_day_1},'{apr_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{cumlative_day_1},'{apr_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{cumlative_day_1},'{aug_str}','{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord45_str}',{cumlative_day_2},'{aug_str}','{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord23_str}',{cumlative_day_2},'{aug_str}',NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        agg_tablename = x_objs.mont_agg_tablename
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fisc_raw_tables2fisc_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 2
        select_agg_sqlstr = f"SELECT {x_cols.mont_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, cumlative_day_1, apr_str)
        expected_agg_row1 = (accord23_str, cumlative_day_2, aug_str)
        assert rows == [expected_agg_row0, expected_agg_row1]


def test_fisc_raw_tables2fisc_agg_tables_Scenario4_fiscweek_Some_error_message():
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
    x_error_message = "Inconsistent data"
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        insert_raw_sqlstr = f"""
INSERT INTO {x_objs.week_raw_tablename} ({x_cols.week_raw_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}',{weekday_order_1},'{mon_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord23_str}',{weekday_order_1},'{mon_str}',NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}',{weekday_order_1},'{wed_str}','{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord45_str}',{weekday_order_2},'{wed_str}','{x_error_message}')
, ('br00333','{sue_inx}',{event9},'{accord23_str}',{weekday_order_2},'{wed_str}',NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        agg_tablename = x_objs.week_agg_tablename
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fisc_raw_tables2fisc_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 2
        select_agg_sqlstr = f"SELECT {x_cols.week_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, weekday_order_1, mon_str)
        expected_agg_row1 = (accord23_str, weekday_order_2, wed_str)
        assert rows == [expected_agg_row0, expected_agg_row1]


def test_fisc_raw_tables2fisc_agg_tables_Scenario5_fiscdeal_Some_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    event9 = 9
    accord23_str = "accord23"
    accord45_str = "accord45"
    bob_inx = "Bobby"
    t1_deal_time = 33
    t1_quota_1 = 200
    t1_quota_2 = 300
    t2_deal_time = 55
    t2_quota = 400
    x_error_message = "Inconsistent data"
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        insert_raw_sqlstr = f"""
INSERT INTO {x_objs.deal_raw_tablename} ({x_cols.deal_raw_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{bob_inx}',{t1_deal_time},{t1_quota_1},NULL,'{x_error_message}')
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{bob_inx}',{t1_deal_time},{t1_quota_2},NULL,'{x_error_message}')
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{bob_inx}',{t2_deal_time},{t2_quota},NULL,NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{bob_inx}',{t2_deal_time},{t2_quota},NULL,NULL)
, ('br00333','{sue_inx}',{event9},'{accord45_str}','{bob_inx}',{t1_deal_time},{t1_quota_1},NULL,NULL)
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{bob_inx}',{t2_deal_time},{t2_quota},NULL,NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        agg_tablename = x_objs.deal_agg_tablename
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fisc_raw_tables2fisc_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 3
        select_agg_sqlstr = f"SELECT {x_cols.deal_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, bob_inx, t2_deal_time, t2_quota, None)
        expected_agg_row1 = (accord45_str, bob_inx, t1_deal_time, t1_quota_1, None)
        expected_agg_row2 = (accord45_str, bob_inx, t2_deal_time, t2_quota, None)
        assert rows == [expected_agg_row0, expected_agg_row1, expected_agg_row2]


def test_fisc_raw_tables2fisc_agg_tables_Scenario6_fisccash_Some_error_message():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    event9 = 9
    accord23_str = "accord23"
    accord45_str = "accord45"
    bob_inx = "Bobby"
    yao_inx = "Yao"
    t1_tran_time = 33
    t1_amount_1 = 200
    t1_amount_2 = 300
    t2_tran_time = 55
    t2_amount = 400
    x_error_message = "Inconsistent data"
    x_objs = FiscPrimeObjsRef()
    x_cols = FiscPrimeColumnsRef()

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        insert_raw_sqlstr = f"""
INSERT INTO {x_objs.cash_raw_tablename} ({x_cols.cash_raw_csv_header})
VALUES
  ('br00333','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',{t1_tran_time},{t1_amount_1},'{x_error_message}')
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',{t1_tran_time},{t1_amount_2},'{x_error_message}')
, ('br00333','{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',{t2_tran_time},{t2_amount},NULL)
, ('br00333','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}',{t2_tran_time},{t2_amount},NULL)
, ('br00333','{sue_inx}',{event9},'{accord45_str}','{bob_inx}','{yao_inx}',{t1_tran_time},{t1_amount_1},NULL)
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{bob_inx}','{yao_inx}',{t2_tran_time},{t2_amount},NULL)
, ('br00333','{sue_inx}',{event9},'{accord23_str}','{bob_inx}','{yao_inx}',{t2_tran_time},NULL,NULL)
;
"""
        print(f"{insert_raw_sqlstr=}")
        cursor.execute(insert_raw_sqlstr)
        agg_tablename = x_objs.cash_agg_tablename
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fisc_raw_tables2fisc_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 3
        select_agg_sqlstr = f"SELECT {x_cols.cash_agg_csv_header} FROM {agg_tablename};"
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        expected_agg_row0 = (accord23_str, bob_inx, yao_inx, t2_tran_time, t2_amount)
        expected_agg_row1 = (accord45_str, bob_inx, yao_inx, t1_tran_time, t1_amount_1)
        expected_agg_row2 = (accord45_str, bob_inx, yao_inx, t2_tran_time, t2_amount)
        assert rows == [expected_agg_row0, expected_agg_row1, expected_agg_row2]


def test_etl_fisc_agg_tables_to_fisc_csvs_CreateFiles():
    # sourcery skip: extract-method
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        fisc_mstr_dir = get_test_etl_dir()
        x_fisc = FiscPrimeObjsRef(fisc_mstr_dir)
        insert_agg_sqlstr = f"""
INSERT INTO {x_fisc.unit_agg_tablename} ({fisc_tag_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_agg_sqlstr)
        assert os_path_exists(x_fisc.unit_agg_csv_path) is False
        assert os_path_exists(x_fisc.deal_agg_csv_path) is False
        assert os_path_exists(x_fisc.cash_agg_csv_path) is False
        assert os_path_exists(x_fisc.hour_agg_csv_path) is False
        assert os_path_exists(x_fisc.mont_agg_csv_path) is False
        assert os_path_exists(x_fisc.week_agg_csv_path) is False

        # WHEN
        etl_fisc_agg_tables_to_fisc_csvs(cursor, fisc_mstr_dir)

        # THEN
        assert os_path_exists(x_fisc.unit_agg_csv_path)
        assert os_path_exists(x_fisc.deal_agg_csv_path)
        assert os_path_exists(x_fisc.cash_agg_csv_path)
        assert os_path_exists(x_fisc.hour_agg_csv_path)
        assert os_path_exists(x_fisc.mont_agg_csv_path)
        assert os_path_exists(x_fisc.week_agg_csv_path)
        unit_agg_csv_filename = x_fisc.unit_agg_csv_filename
        generated_fiscunit_csv = open_file(fisc_mstr_dir, unit_agg_csv_filename)
        expected_fiscunit_csv_str = f"""{fisc_tag_str()},{timeline_tag_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{bridge_str()},job_listen_rotations
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
        assert generated_fiscunit_csv == expected_fiscunit_csv_str
