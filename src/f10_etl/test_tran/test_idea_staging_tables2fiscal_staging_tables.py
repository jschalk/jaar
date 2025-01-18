from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import (
    db_table_exists,
    get_row_count,
    create_table_from_columns,
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
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def create_idea_staging_table(
    conn: sqlite3_Connection, tablename: str, columns_list: list[str]
):
    create_table_from_columns(conn, tablename, columns_list, get_idea_sqlite_types())


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


def test_idea_staging_tables2fiscal_staging_tables_Scenario0_From_br00011_IdeaFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    aft_faces_dir = get_test_etl_dir()
    sue_aft_dir = create_path(aft_faces_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        etl_aft_face_csv_files_to_fiscal_db(fiscal_db_conn, aft_faces_dir)
        create_fiscal_tables(fiscal_db_conn)
        x_fis = FiscalPrimeObjsRef()
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 2
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"SELECT * FROM {x_fis.unit_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
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
            None,  # note
        )
        expected_row1 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
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
            None,  # note
        )
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fiscal_staging_tables_Scenario1_From_br00011_IdeaTable(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00011_str = "br00011"
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        br00011_tablename = f"{br00011_str}_staging"
        create_idea_staging_table(fiscal_db_conn, br00011_tablename, br00011_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00011_tablename} ({face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()})
VALUES 
  ('{sue_inx}', {event3}, '{accord23_str}', '{bob_inx}', '{bob_inx}')
, ('{sue_inx}', {event3}, '{accord23_str}', '{yao_inx}', '{bob_inx}')
, ('{sue_inx}', {event3}, '{accord23_str}', '{yao_inx}', '{yao_inx}')
, ('{sue_inx}', {event7}, '{accord23_str}', '{yao_inx}', '{yao_inx}')
;
"""
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        x_fis = FiscalPrimeObjsRef()
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.unit_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
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
            None,  # note
        )
        expected_row1 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
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
            None,  # note
        )
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fiscal_staging_tables_Scenario2_Idea_br00000_Table_WithEmptyAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00000_str = "br00000"
    br00000_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        fund_coin_str(),
        penny_str(),
        respect_bit_str(),
        present_time_str(),
        bridge_str(),
        c400_number_str(),
        yr1_jan1_offset_str(),
        monthday_distortion_str(),
        timeline_title_str(),
    ]
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        br00000_tablename = f"{br00000_str}_staging"
        create_idea_staging_table(fiscal_db_conn, br00000_tablename, br00000_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00000_tablename} ({face_name_str()},{event_int_str()},{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{present_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()})
VALUES
  ('{sue_inx}', {event3}, '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
, ('{sue_inx}', {event3}, '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
, ('{sue_inx}', {event7}, '{accord23_str}', NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)
;
"""
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        x_fis = FiscalPrimeObjsRef()
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.unit_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00000_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
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
            None,  # note
        )
        expected_row1 = (
            br00000_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
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
            None,  # note
        )
        print(f"{fiscalunit_db_rows[0]=}")
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fiscal_staging_tables_Scenario3_Idea_br00000_Table_WithAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00000_str = "br00000"
    br00000_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        fund_coin_str(),
        penny_str(),
        respect_bit_str(),
        present_time_str(),
        bridge_str(),
        c400_number_str(),
        yr1_jan1_offset_str(),
        monthday_distortion_str(),
        timeline_title_str(),
    ]
    a23_fund_coin = 11
    a23_penny = 22
    a23_respect_bit = 33
    a23_present_time = 44
    a23_bridge = ";"
    a23_c400_number = 55
    a23_yr1_jan1_offset = 66
    a23_monthday_distortion = 77
    a23_timeline_title = "accord23_timeline"

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        br00000_tablename = f"{br00000_str}_staging"
        create_idea_staging_table(fiscal_db_conn, br00000_tablename, br00000_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00000_tablename} ({face_name_str()},{event_int_str()},{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{present_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}')
, ('{sue_inx}',{event3},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}')
, ('{sue_inx}',{event7},'{accord23_str}',{a23_fund_coin},{a23_penny},{a23_respect_bit},{a23_present_time},'{a23_bridge}',{a23_c400_number},{a23_yr1_jan1_offset},{a23_monthday_distortion},'{a23_timeline_title}')
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        x_fis = FiscalPrimeObjsRef()
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.unit_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00000_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fiscal_title
            a23_fund_coin,  # fund_coin
            a23_penny,  # penny
            a23_respect_bit,  # respect_bit
            a23_present_time,  # present_time
            a23_bridge,  # bridge
            a23_c400_number,  # c400_number
            a23_yr1_jan1_offset,  # yr1_jan1_offset
            a23_monthday_distortion,  # monthday_distortion
            a23_timeline_title,  # timeline_title
            None,  # note
        )
        expected_row1 = (
            br00000_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fiscal_title
            a23_fund_coin,  # fund_coin
            a23_penny,  # penny
            a23_respect_bit,  # respect_bit
            a23_present_time,  # present_time
            a23_bridge,  # bridge
            a23_c400_number,  # c400_number
            a23_yr1_jan1_offset,  # yr1_jan1_offset
            a23_monthday_distortion,  # monthday_distortion
            a23_timeline_title,  # timeline_title
            None,  # note
        )
        print(f"{fiscalunit_db_rows[0]=}")
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fiscal_staging_tables_Scenario4_Idea_br00001_Table_WithAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00001_str = "br00001"
    br00001_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        owner_name_str(),
        time_int_str(),
        quota_str(),
    ]
    a23_owner_name = bob_inx
    a23_time_int = 22
    a23_quota = 33

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        br00001_tablename = f"{br00001_str}_staging"
        create_idea_staging_table(fiscal_db_conn, br00001_tablename, br00001_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00001_tablename} ({face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{time_int_str()},{quota_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}',{a23_time_int},{a23_quota})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}',{a23_time_int},{a23_quota})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}',{a23_time_int},{a23_quota})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        x_fis = FiscalPrimeObjsRef()
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, x_fis.deal_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.deal_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.deal_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00001_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fiscal_title
            a23_owner_name,
            a23_time_int,
            a23_quota,
            None,  # note
        )
        expected_row1 = (
            br00001_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fiscal_title
            a23_owner_name,
            a23_time_int,
            a23_quota,
            None,  # note
        )
        print(f"{fiscalunit_db_rows[0]=}")
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fiscal_staging_tables_Scenario5_Idea_br00002_Table_WithAttrs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00002_str = "br00002"
    br00002_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        owner_name_str(),
        acct_name_str(),
        time_int_str(),
        amount_str(),
    ]
    a23_owner_name = bob_inx
    a23_acct_name = "Yao"
    a23_time_int = 33
    a23_amount = 44

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        br00002_tablename = f"{br00002_str}_staging"
        create_idea_staging_table(fiscal_db_conn, br00002_tablename, br00002_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00002_tablename} ({face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()},{time_int_str()},{amount_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_time_int},{a23_amount})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_time_int},{a23_amount})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_owner_name}','{a23_acct_name}',{a23_time_int},{a23_amount})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        x_fis = FiscalPrimeObjsRef()
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, x_fis.cash_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.cash_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.cash_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00002_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fiscal_title
            a23_owner_name,
            a23_acct_name,
            a23_time_int,
            a23_amount,
            None,  # note
        )
        expected_row1 = (
            br00002_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fiscal_title
            a23_owner_name,
            a23_acct_name,
            a23_time_int,
            a23_amount,
            None,  # note
        )
        print(f"{fiscalunit_db_rows[0]=}")
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fiscal_staging_tables_Scenario6_Idea_br00003_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00003_str = "br00003"
    br00003_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    a23_hour_title = "4pm"
    a23_cumlative_minute = 44

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        br00003_tablename = f"{br00003_str}_staging"
        create_idea_staging_table(fiscal_db_conn, br00003_tablename, br00003_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00003_tablename} ({face_name_str()},{event_int_str()},{fiscal_title_str()},{hour_title_str()},{cumlative_minute_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_hour_title}',{a23_cumlative_minute})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_hour_title}',{a23_cumlative_minute})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_hour_title}',{a23_cumlative_minute})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        x_fis = FiscalPrimeObjsRef()
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, x_fis.hour_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.hour_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.hour_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00003_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fiscal_title
            a23_hour_title,
            a23_cumlative_minute,
            None,  # note
        )
        expected_row1 = (
            br00003_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fiscal_title
            a23_hour_title,
            a23_cumlative_minute,
            None,  # note
        )
        print(f"{fiscalunit_db_rows[0]=}")
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fiscal_staging_tables_Scenario7_Idea_br00004_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00004_str = "br00004"
    br00004_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        month_title_str(),
        cumlative_day_str(),
    ]
    a23_month_title = "4pm"
    a23_cumlative_day = 44

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        br00004_tablename = f"{br00004_str}_staging"
        create_idea_staging_table(fiscal_db_conn, br00004_tablename, br00004_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00004_tablename} ({face_name_str()},{event_int_str()},{fiscal_title_str()},{month_title_str()},{cumlative_day_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_month_title}',{a23_cumlative_day})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_month_title}',{a23_cumlative_day})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_month_title}',{a23_cumlative_day})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        x_fis = FiscalPrimeObjsRef()
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, x_fis.mont_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.mont_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.mont_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00004_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fiscal_title
            a23_month_title,
            a23_cumlative_day,
            None,  # note
        )
        expected_row1 = (
            br00004_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fiscal_title
            a23_month_title,
            a23_cumlative_day,
            None,  # note
        )
        print(f"{fiscalunit_db_rows[0]=}")
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_idea_staging_tables2fiscal_staging_tables_Scenario8_Idea_br00005_Table_WithAttrs(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    br00005_str = "br00005"
    br00005_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        weekday_title_str(),
        weekday_order_str(),
    ]
    a23_weekday_title = "4pm"
    a23_weekday_order = 44

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        br00005_tablename = f"{br00005_str}_staging"
        create_idea_staging_table(fiscal_db_conn, br00005_tablename, br00005_columns)
        insert_staging_sqlstr = f"""
INSERT INTO {br00005_tablename} ({face_name_str()},{event_int_str()},{fiscal_title_str()},{weekday_title_str()},{weekday_order_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{a23_weekday_title}',{a23_weekday_order})
, ('{sue_inx}',{event3},'{accord23_str}','{a23_weekday_title}',{a23_weekday_order})
, ('{sue_inx}',{event7},'{accord23_str}','{a23_weekday_title}',{a23_weekday_order})
;
"""
        print(f"{insert_staging_sqlstr=}")
        cursor = fiscal_db_conn.cursor()
        cursor.execute(insert_staging_sqlstr)
        x_fis = FiscalPrimeObjsRef()
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, x_fis.week_stage_tablename) == 0

        # WHEN
        idea_staging_tables2fiscal_staging_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.week_stage_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.week_stage_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00005_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fiscal_title
            a23_weekday_title,
            a23_weekday_order,
            None,  # note
        )
        expected_row1 = (
            br00005_str,  # idea_number
            sue_inx,  # face_name
            event7,  # event_int
            accord23_str,  # fiscal_title
            a23_weekday_title,
            a23_weekday_order,
            None,  # note
        )
        print(f"{fiscalunit_db_rows[0]=}")
        print(f"{fiscalunit_db_rows[1]=}")
        print(f"        {expected_row0=}")
        print(f"        {expected_row1=}")
        assert fiscalunit_db_rows[0] == expected_row0
        assert fiscalunit_db_rows[1] == expected_row1
        assert fiscalunit_db_rows == [expected_row0, expected_row1]


def test_etl_fiscal_staging_tables_to_fiscal_csvs_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        fiscal_mstr_dir = get_test_etl_dir()
        fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
        x_fis = FiscalPrimeObjsRef(fiscals_dir)
        fis_cols = FiscalPrimeColumnsRef()
        cursor = fiscal_db_conn.cursor()
        insert_staging_sqlstr = f"""
INSERT INTO {x_fis.unit_stage_tablename} ({idea_number_str()}, {face_name_str()}, {event_int_str()}, {fiscal_title_str()})
VALUES 
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert os_path_exists(x_fis.unit_stage_csv_path) is False
        assert os_path_exists(x_fis.deal_stage_csv_path) is False
        assert os_path_exists(x_fis.cash_stage_csv_path) is False
        assert os_path_exists(x_fis.hour_stage_csv_path) is False
        assert os_path_exists(x_fis.mont_stage_csv_path) is False
        assert os_path_exists(x_fis.week_stage_csv_path) is False

        # WHEN
        etl_fiscal_staging_tables_to_fiscal_csvs(fiscal_db_conn, fiscals_dir)

        # THEN
        assert os_path_exists(x_fis.unit_stage_csv_path)
        assert os_path_exists(x_fis.deal_stage_csv_path)
        assert os_path_exists(x_fis.cash_stage_csv_path)
        assert os_path_exists(x_fis.hour_stage_csv_path)
        assert os_path_exists(x_fis.mont_stage_csv_path)
        assert os_path_exists(x_fis.week_stage_csv_path)
        unit_stage_csv_filename = x_fis.unit_stage_csv_filename
        generated_fiscalunit_csv = open_file(fiscals_dir, unit_stage_csv_filename)
        expected_fiscalunit_csv_str = f"""{fis_cols.unit_staging_csv_header}
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord45_str},,,,,,,,,,
{br00011_str},{sue_inx},{event7},{accord45_str},,,,,,,,,,
"""
        print(f"   {generated_fiscalunit_csv=}")
        print(f"{expected_fiscalunit_csv_str=}")
        assert generated_fiscalunit_csv == expected_fiscalunit_csv_str
        # confirming file is non-zero length, has column headers
        assert len(open_file(x_fis.deal_stage_csv_path)) == 76
        assert len(open_file(x_fis.cash_stage_csv_path)) == 87
        assert len(open_file(x_fis.hour_stage_csv_path)) == 78
        assert len(open_file(x_fis.mont_stage_csv_path)) == 76
        assert len(open_file(x_fis.week_stage_csv_path)) == 78


def test_etl_fiscal_staging_tables_to_fiscal_csvs_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        fiscal_mstr_dir = get_test_etl_dir()
        fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
        x_fis = FiscalPrimeObjsRef(fiscals_dir)
        fis_cols = FiscalPrimeColumnsRef()
        cursor = fiscal_db_conn.cursor()
        insert_staging_sqlstr = f"""
INSERT INTO {x_fis.unit_stage_tablename} ({idea_number_str()}, {face_name_str()}, {event_int_str()}, {fiscal_title_str()})
VALUES 
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert os_path_exists(x_fis.unit_stage_csv_path) is False
        assert os_path_exists(x_fis.deal_stage_csv_path) is False
        assert os_path_exists(x_fis.cash_stage_csv_path) is False
        assert os_path_exists(x_fis.hour_stage_csv_path) is False
        assert os_path_exists(x_fis.mont_stage_csv_path) is False
        assert os_path_exists(x_fis.week_stage_csv_path) is False

        # WHEN
        etl_fiscal_staging_tables_to_fiscal_csvs(fiscal_db_conn, fiscals_dir)

        # THEN
        assert os_path_exists(x_fis.unit_stage_csv_path)
        assert os_path_exists(x_fis.deal_stage_csv_path)
        assert os_path_exists(x_fis.cash_stage_csv_path)
        assert os_path_exists(x_fis.hour_stage_csv_path)
        assert os_path_exists(x_fis.mont_stage_csv_path)
        assert os_path_exists(x_fis.week_stage_csv_path)
        unit_stage_csv_filename = x_fis.unit_stage_csv_filename
        generated_fiscalunit_csv = open_file(fiscals_dir, unit_stage_csv_filename)
        expected_fiscalunit_csv_str = f"""{fis_cols.unit_staging_csv_header}
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord45_str},,,,,,,,,,
{br00011_str},{sue_inx},{event7},{accord45_str},,,,,,,,,,
"""
        print(f"   {generated_fiscalunit_csv=}")
        print(f"{expected_fiscalunit_csv_str=}")
        assert generated_fiscalunit_csv == expected_fiscalunit_csv_str
        # confirming file is non-zero length, has column headers
        assert len(open_file(x_fis.deal_stage_csv_path)) == 76
        assert len(open_file(x_fis.cash_stage_csv_path)) == 87
        assert len(open_file(x_fis.hour_stage_csv_path)) == 78
        assert len(open_file(x_fis.mont_stage_csv_path)) == 76
        assert len(open_file(x_fis.week_stage_csv_path)) == 78
