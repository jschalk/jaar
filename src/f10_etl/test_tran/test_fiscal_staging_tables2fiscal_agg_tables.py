from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import get_row_count, create_agg_insert_query
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
    get_fiscal_config_args,
    fiscalunit_str,
    fiscal_deal_episode_str,
    fiscal_cashbook_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
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
    FISCALUNIT_AGG_INSERT_SQLSTR,
    FISCALDEAL_AGG_INSERT_SQLSTR,
    FISCALCASH_AGG_INSERT_SQLSTR,
    FISCALHOUR_AGG_INSERT_SQLSTR,
    FISCALMONT_AGG_INSERT_SQLSTR,
    FISCALWEEK_AGG_INSERT_SQLSTR,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_GlobalVairableAGG_INSERT_SQLSTR_ReturnsObj():
    # ESTABLISH
    x_objs = FiscalPrimeObjsRef()
    x_exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)

        # WHEN
        generated_fiscalunit_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.unit_stage_tablename,
            dst_table=x_objs.unit_agg_tablename,
            exclude_cols=x_exclude_cols,
        )

        # THEN
        print(f" {generated_fiscalunit_sqlstr=}")
        print(f"{FISCALUNIT_AGG_INSERT_SQLSTR=}")
        assert FISCALUNIT_AGG_INSERT_SQLSTR == generated_fiscalunit_sqlstr

        columns_header = """fiscal_title, fund_coin, penny, respect_bit, present_time, bridge, c400_number, yr1_jan1_offset, monthday_distortion, timeline_title"""
        tablename = "fiscalunit"
        expected_ficsalunit_sqlstr = f"""INSERT INTO {tablename}_agg ({columns_header})
SELECT {columns_header}
FROM {tablename}_staging
WHERE error_message IS NULL
GROUP BY {columns_header}
;
"""
        assert FISCALUNIT_AGG_INSERT_SQLSTR == expected_ficsalunit_sqlstr

        # WHEN / THEN
        generated_fiscaldeal_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.deal_stage_tablename,
            dst_table=x_objs.deal_agg_tablename,
            exclude_cols=x_exclude_cols,
        )
        assert FISCALDEAL_AGG_INSERT_SQLSTR == generated_fiscaldeal_sqlstr

        # WHEN / THEN
        generated_fiscalcash_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.cash_stage_tablename,
            dst_table=x_objs.cash_agg_tablename,
            exclude_cols=x_exclude_cols,
        )
        assert FISCALCASH_AGG_INSERT_SQLSTR == generated_fiscalcash_sqlstr

        # WHEN / THEN
        generated_fiscalhour_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.hour_stage_tablename,
            dst_table=x_objs.hour_agg_tablename,
            exclude_cols=x_exclude_cols,
        )
        assert FISCALHOUR_AGG_INSERT_SQLSTR == generated_fiscalhour_sqlstr

        # WHEN / THEN
        generated_fiscalmont_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.mont_stage_tablename,
            dst_table=x_objs.mont_agg_tablename,
            exclude_cols=x_exclude_cols,
        )
        assert FISCALMONT_AGG_INSERT_SQLSTR == generated_fiscalmont_sqlstr

        # WHEN / THEN
        generated_fiscalweek_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.week_stage_tablename,
            dst_table=x_objs.week_agg_tablename,
            exclude_cols=x_exclude_cols,
        )
        assert FISCALWEEK_AGG_INSERT_SQLSTR == generated_fiscalweek_sqlstr


def test_fiscal_staging_tables2fiscal_agg_tables_PassesOnly_fiscal_title(
    env_dir_setup_cleanup,
):
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


def test_fiscal_staging_tables2fiscal_agg_tables_Scenario0_fiscalunit_WithNo_error_message(
    env_dir_setup_cleanup,
):
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


# def test_fiscal_staging_tables2fiscal_agg_tables_Scenario1_fiscalunit_Some_error_message(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     a23_fund_coin = 11
#     a23_penny_1 = 22
#     a23_penny_2 = 99
#     a23_respect_bit = 33
#     a23_present_time = 44
#     a23_bridge = ";"
#     a23_c400_number = 55
#     a23_yr1_jan1_offset = 66
#     a23_monthday_distortion = 77
#     a23_timeline_title = "accord23_timeline"
#     x_objs = FiscalPrimeObjsRef()
#     x_cols = FiscalPrimeColumnsRef()

#     with sqlite3_connect(":memory:") as fiscal_db_conn:
#         create_fiscal_tables(fiscal_db_conn)
#         x_tablename = x_objs.unit_stage_tablename
#         assert db_table_exists(fiscal_db_conn, x_tablename)
#         insert_staging_sqlstr = f"""
# INSERT INTO {x_tablename} ({x_cols.unit_staging_csv_header})
# VALUES
#   ('br00333','{sue_inx}',{event3},'{accord23_str}',{a23_fund_coin},{a23_penny_1},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
# , ('br00333','{sue_inx}',{event7},'{accord23_str}',{a23_fund_coin},{a23_penny_2},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
# , ('br00333','{sue_inx}',{event7},'{accord45_str}',{a23_fund_coin},{a23_penny_2},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}',NULL)
# ;
# """
#         print(f"{insert_staging_sqlstr=}")
#         cursor = fiscal_db_conn.cursor()
#         cursor.execute(insert_staging_sqlstr)
#         assert get_row_count(fiscal_db_conn, x_tablename) == 3
#         select_sqlstr = f"SELECT {event_int_str()}, {fiscal_title_str()}, error_message FROM {x_tablename};"
#         # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
#         cursor.execute(select_sqlstr)
#         # print(f"{select_sqlstr=}")
#         rows = cursor.fetchall()
#         # print(f"{rows=}")
#         assert rows == [
#             (event3, accord23_str, None),
#             (event7, accord23_str, None),
#             (event7, accord45_str, None),
#         ]

#         # WHEN
#         fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

#         # THEN
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         x_error_message = "Inconsistent fiscal data"
#         assert rows == [
#             (event3, accord23_str, x_error_message),
#             (event7, accord23_str, x_error_message),
#             (event7, accord45_str, None),
#         ]


# def test_fiscal_staging_tables2fiscal_agg_tables_Scenario2_fiscalhour_Some_error_message(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     a23_hour_title = "4pm"
#     a23_cumlative_minute_1 = 44
#     a23_cumlative_minute_2 = 77
#     x_objs = FiscalPrimeObjsRef()
#     x_cols = FiscalPrimeColumnsRef()

#     with sqlite3_connect(":memory:") as fiscal_db_conn:
#         create_fiscal_tables(fiscal_db_conn)
#         x_tablename = x_objs.hour_stage_tablename
#         assert db_table_exists(fiscal_db_conn, x_tablename)
#         insert_staging_sqlstr = f"""
# INSERT INTO {x_tablename} ({x_cols.hour_staging_csv_header})
# VALUES
#   ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_hour_title}',{a23_cumlative_minute_1},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_hour_title}',{a23_cumlative_minute_2},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_hour_title}',{a23_cumlative_minute_1},NULL)
# ;
# """
#         print(f"{insert_staging_sqlstr=}")
#         cursor = fiscal_db_conn.cursor()
#         cursor.execute(insert_staging_sqlstr)
#         assert get_row_count(fiscal_db_conn, x_tablename) == 3
#         select_sqlstr = f"SELECT {event_int_str()}, {fiscal_title_str()}, error_message FROM {x_tablename};"
#         # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
#         cursor.execute(select_sqlstr)
#         # print(f"{select_sqlstr=}")
#         rows = cursor.fetchall()
#         # print(f"{rows=}")
#         assert rows == [
#             (event3, accord23_str, None),
#             (event7, accord23_str, None),
#             (event7, accord45_str, None),
#         ]

#         # WHEN
#         fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

#         # THEN
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         x_error_message = "Inconsistent fiscal data"
#         assert rows == [
#             (event3, accord23_str, x_error_message),
#             (event7, accord23_str, x_error_message),
#             (event7, accord45_str, None),
#         ]


# def test_fiscal_staging_tables2fiscal_agg_tables_Scenario3_fiscalhour_Some_error_message(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     a23_month_title_1 = "March"
#     a23_month_title_2 = "Marche"
#     a23_cumlative_day = 44
#     x_objs = FiscalPrimeObjsRef()
#     x_cols = FiscalPrimeColumnsRef()

#     with sqlite3_connect(":memory:") as fiscal_db_conn:
#         create_fiscal_tables(fiscal_db_conn)
#         x_tablename = x_objs.mont_stage_tablename
#         assert db_table_exists(fiscal_db_conn, x_tablename)
#         insert_staging_sqlstr = f"""
# INSERT INTO {x_tablename} ({x_cols.mont_staging_csv_header})
# VALUES
#   ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_month_title_1}',{a23_cumlative_day},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_month_title_2}',{a23_cumlative_day},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_month_title_2}',{a23_cumlative_day},NULL)
# ;
# """
#         print(f"{insert_staging_sqlstr=}")
#         cursor = fiscal_db_conn.cursor()
#         cursor.execute(insert_staging_sqlstr)
#         assert get_row_count(fiscal_db_conn, x_tablename) == 3
#         select_sqlstr = f"SELECT {event_int_str()}, {fiscal_title_str()}, error_message FROM {x_tablename};"
#         # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
#         cursor.execute(select_sqlstr)
#         # print(f"{select_sqlstr=}")
#         rows = cursor.fetchall()
#         # print(f"{rows=}")
#         assert rows == [
#             (event3, accord23_str, None),
#             (event7, accord23_str, None),
#             (event7, accord45_str, None),
#         ]

#         # WHEN
#         fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

#         # THEN
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         x_error_message = "Inconsistent fiscal data"
#         assert rows == [
#             (event3, accord23_str, x_error_message),
#             (event7, accord23_str, x_error_message),
#             (event7, accord45_str, None),
#         ]


# def test_fiscal_staging_tables2fiscal_agg_tables_Scenario4_fiscalweek_Some_error_message(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     a23_weekday_title_1 = "Wednesday"
#     a23_weekday_title_2 = "Tuesday"
#     a23_weekday_order = 7
#     x_objs = FiscalPrimeObjsRef()
#     x_cols = FiscalPrimeColumnsRef()

#     with sqlite3_connect(":memory:") as fiscal_db_conn:
#         create_fiscal_tables(fiscal_db_conn)
#         x_tablename = x_objs.week_stage_tablename
#         assert db_table_exists(fiscal_db_conn, x_tablename)
#         insert_staging_sqlstr = f"""
# INSERT INTO {x_tablename} ({x_cols.week_staging_csv_header})
# VALUES
#   ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_weekday_title_1}',{a23_weekday_order},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_weekday_title_2}',{a23_weekday_order},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_weekday_title_1}',{a23_weekday_order},NULL)
# ;
# """
#         print(f"{insert_staging_sqlstr=}")
#         cursor = fiscal_db_conn.cursor()
#         cursor.execute(insert_staging_sqlstr)
#         assert get_row_count(fiscal_db_conn, x_tablename) == 3
#         select_sqlstr = f"SELECT {event_int_str()}, {fiscal_title_str()}, error_message FROM {x_tablename};"
#         # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
#         cursor.execute(select_sqlstr)
#         # print(f"{select_sqlstr=}")
#         rows = cursor.fetchall()
#         # print(f"{rows=}")
#         assert rows == [
#             (event3, accord23_str, None),
#             (event7, accord23_str, None),
#             (event7, accord45_str, None),
#         ]

#         # WHEN
#         fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

#         # THEN
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         x_error_message = "Inconsistent fiscal data"
#         assert rows == [
#             (event3, accord23_str, x_error_message),
#             (event7, accord23_str, x_error_message),
#             (event7, accord45_str, None),
#         ]


# def test_fiscal_staging_tables2fiscal_agg_tables_Scenario5_fiscaldeal_Some_error_message(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     bob_inx = "Bobby"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     a23_owner_name = bob_inx
#     t1_time_int = 33
#     t1_quota_1 = 200
#     t1_quota_2 = 300
#     t2_time_int = 55
#     t2_quota = 400
#     x_objs = FiscalPrimeObjsRef()
#     x_cols = FiscalPrimeColumnsRef()

#     with sqlite3_connect(":memory:") as fiscal_db_conn:
#         create_fiscal_tables(fiscal_db_conn)
#         x_tablename = x_objs.deal_stage_tablename
#         assert db_table_exists(fiscal_db_conn, x_tablename)
#         insert_staging_sqlstr = f"""
# INSERT INTO {x_tablename} ({x_cols.deal_staging_csv_header})
# VALUES
#   ('br00333','{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}',{t1_time_int},{t1_quota_1},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{t1_time_int},{t1_quota_2},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{t2_time_int},{t2_quota},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_owner_name}',{t1_time_int},{t1_quota_1},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord45_str}','{a23_owner_name}',{t2_time_int},{t2_quota},NULL)
# ;
# """
#         print(f"{insert_staging_sqlstr=}")
#         cursor = fiscal_db_conn.cursor()
#         cursor.execute(insert_staging_sqlstr)
#         assert get_row_count(fiscal_db_conn, x_tablename) == 5
#         select_sqlstr = f"SELECT {event_int_str()}, {fiscal_title_str()}, {time_int_str()}, error_message FROM {x_tablename};"
#         # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
#         cursor.execute(select_sqlstr)
#         # print(f"{select_sqlstr=}")
#         rows = cursor.fetchall()
#         # print(f"{rows=}")
#         assert rows == [
#             (event3, accord23_str, t1_time_int, None),
#             (event7, accord23_str, t1_time_int, None),
#             (event7, accord23_str, t2_time_int, None),
#             (event7, accord45_str, t1_time_int, None),
#             (event7, accord45_str, t2_time_int, None),
#         ]

#         # WHEN
#         fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

#         # THEN
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         print(f"{rows=}")
#         x_error_message = "Inconsistent fiscal data"
#         assert rows == [
#             (event3, accord23_str, t1_time_int, x_error_message),
#             (event7, accord23_str, t1_time_int, x_error_message),
#             (event7, accord23_str, t2_time_int, None),
#             (event7, accord45_str, t1_time_int, None),
#             (event7, accord45_str, t2_time_int, None),
#         ]


# def test_fiscal_staging_tables2fiscal_agg_tables_Scenario6_fiscalcash_Some_error_message(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_inx = "Suzy"
#     bob_inx = "Bobby"
#     yao_inx = "Yao"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     t1_time_int = 33
#     t2_time_int = 55
#     t1_amount_1 = 200
#     t1_amount_2 = 300
#     t2_amount = 400
#     x_objs = FiscalPrimeObjsRef()
#     x_cols = FiscalPrimeColumnsRef()

#     with sqlite3_connect(":memory:") as fiscal_db_conn:
#         create_fiscal_tables(fiscal_db_conn)
#         x_tablename = x_objs.cash_stage_tablename
#         assert db_table_exists(fiscal_db_conn, x_tablename)
#         insert_staging_sqlstr = f"""
# INSERT INTO {x_tablename} ({x_cols.cash_staging_csv_header})
# VALUES
#   ('br00333','{sue_inx}',{event3},'{accord23_str}','{yao_inx}','{bob_inx}',{t1_time_int},{t1_amount_1},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord23_str}','{yao_inx}','{bob_inx}',{t1_time_int},{t1_amount_2},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord23_str}','{yao_inx}','{bob_inx}',{t2_time_int},{t2_amount},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord45_str}','{yao_inx}','{bob_inx}',{t1_time_int},{t1_amount_1},NULL)
# , ('br00333','{sue_inx}',{event7},'{accord45_str}','{yao_inx}','{bob_inx}',{t2_time_int},{t2_amount},NULL)
# ;
# """
#         print(f"{insert_staging_sqlstr=}")
#         cursor = fiscal_db_conn.cursor()
#         cursor.execute(insert_staging_sqlstr)
#         assert get_row_count(fiscal_db_conn, x_tablename) == 5
#         select_sqlstr = f"SELECT {event_int_str()}, {fiscal_title_str()}, {time_int_str()}, error_message FROM {x_tablename};"
#         # # select_sqlstr = f"SELECT {event_int_str()} FROM {x_tablename};"
#         cursor.execute(select_sqlstr)
#         # print(f"{select_sqlstr=}")
#         rows = cursor.fetchall()
#         # print(f"{rows=}")
#         assert rows == [
#             (event3, accord23_str, t1_time_int, None),
#             (event7, accord23_str, t1_time_int, None),
#             (event7, accord23_str, t2_time_int, None),
#             (event7, accord45_str, t1_time_int, None),
#             (event7, accord45_str, t2_time_int, None),
#         ]

#         # WHEN
#         fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

#         # THEN
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         print(f"{rows=}")
#         x_error_message = "Inconsistent fiscal data"
#         assert rows == [
#             (event3, accord23_str, t1_time_int, x_error_message),
#             (event7, accord23_str, t1_time_int, x_error_message),
#             (event7, accord23_str, t2_time_int, None),
#             (event7, accord45_str, t1_time_int, None),
#             (event7, accord45_str, t2_time_int, None),
#         ]


def test_etl_fiscal_agg_tables_to_fiscal_csvs_CreateFiles(env_dir_setup_cleanup):
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
