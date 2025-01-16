from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import db_table_exists, get_row_count
from src.f01_road.finance_tran import bridge_str
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
    current_time_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_config import idea_number_str
from src.f09_idea.pandas_tool import get_pragma_table_fetchall, get_sorting_columns
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f10_etl.transformers import (
    etl_aft_face_csv_files_to_fiscal_db,
    create_fiscal_tables,
    populate_fiscal_staging_tables,
    populate_fiscal_agg_tables,
    etl_fiscal_staging_tables_to_fiscal_csvs,
    etl_fiscal_agg_tables_to_fiscal_csvs,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_etl_aft_face_csv_files_to_fiscal_db_DBChanges(
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
    br00011_staging_tablename = f"{br00011_str}_staging"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        assert db_table_exists(fiscal_db_conn, br00011_staging_tablename) is False

        # ESTABLISH
        etl_aft_face_csv_files_to_fiscal_db(fiscal_db_conn, aft_faces_dir)

        # THEN
        assert db_table_exists(fiscal_db_conn, br00011_staging_tablename)
        print(f"{type(fiscal_db_conn)=}")
        assert fiscal_db_conn != None
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"PRAGMA table_info({br00011_staging_tablename})")
        br00011_db_columns = cursor.fetchall()
        br00011_expected_columns = [
            (0, face_name_str(), "TEXT", 0, None, 0),
            (1, event_int_str(), "INTEGER", 0, None, 0),
            (2, fiscal_title_str(), "TEXT", 0, None, 0),
            (3, owner_name_str(), "TEXT", 0, None, 0),
            (4, acct_name_str(), "TEXT", 0, None, 0),
        ]
        print(f"      {br00011_db_columns=}")
        print(f"{br00011_expected_columns=}")
        assert br00011_db_columns == br00011_expected_columns
        cursor.execute(f"SELECT * FROM {br00011_staging_tablename}")
        br00011_db_rows = cursor.fetchall()
        expected_data = [
            (sue_inx, event3, accord23_str, bob_inx, bob_inx),
            (sue_inx, event3, accord23_str, yao_inx, bob_inx),
            (sue_inx, event3, accord23_str, yao_inx, yao_inx),
            (sue_inx, event7, accord23_str, yao_inx, yao_inx),
        ]
        assert br00011_db_rows == expected_data


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


def test_populate_fiscal_staging_tables_Scenario0_PopulatesFiscalStagingTables(
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

    fiscalunit_tablename = f"{fiscalunit_str()}_staging"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        etl_aft_face_csv_files_to_fiscal_db(fiscal_db_conn, aft_faces_dir)
        create_fiscal_tables(fiscal_db_conn)
        assert get_row_count(fiscal_db_conn, fiscalunit_tablename) == 0

        # WHEN
        populate_fiscal_staging_tables(fiscal_db_conn)

        # THEN
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"SELECT * FROM {fiscalunit_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row0 = (
            br00011_str,  # idea_number
            sue_inx,  # face_name
            event3,  # event_int
            accord23_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # current_time
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
            None,  # current_time
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


def test_populate_fiscal_agg_tables_PopulatesFiscalAggTables(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    fiscalunit_stage_tablename = f"{fiscalunit_str()}_staging"
    fiscalunit_agg_tablename = f"{fiscalunit_str()}_agg"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)

        cursor = fiscal_db_conn.cursor()
        insert_staging_sqlstr = f"""
INSERT INTO fiscalunit_staging (idea_number, face_name, event_int, fiscal_title)
VALUES 
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        cursor.execute(f"SELECT * FROM {fiscalunit_stage_tablename};")
        fiscalunit_stage_rows = cursor.fetchall()
        assert len(fiscalunit_stage_rows) == 4
        cursor.execute(f"SELECT * FROM {fiscalunit_agg_tablename};")
        fiscalunit_agg_rows = cursor.fetchall()
        assert fiscalunit_agg_rows == []

        # WHEN
        populate_fiscal_agg_tables(fiscal_db_conn)

        # THEN
        cursor.execute(f"SELECT * FROM {fiscalunit_agg_tablename};")
        fiscalunit_agg_rows = cursor.fetchall()
        expected_row1 = (
            accord23_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # current_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        expected_row2 = (
            accord45_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # current_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        print(f"{fiscalunit_agg_rows=}")
        print(f"      {expected_row1=}")
        assert fiscalunit_agg_rows == [expected_row1, expected_row2]


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
        cursor = fiscal_db_conn.cursor()
        insert_staging_sqlstr = f"""
INSERT INTO fiscalunit_staging ({idea_number_str()}, {face_name_str()}, {event_int_str()}, {fiscal_title_str()})
VALUES 
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        fiscal_mstr_dir = get_test_etl_dir()
        fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
        fiscalref = FiscalPrimeObjsRef(fiscals_dir)
        fis_cols = FiscalPrimeColumnsRef()
        assert os_path_exists(fiscalref.unit_stage_csv_path) is False
        assert os_path_exists(fiscalref.deal_stage_csv_path) is False
        assert os_path_exists(fiscalref.cash_stage_csv_path) is False
        assert os_path_exists(fiscalref.hour_stage_csv_path) is False
        assert os_path_exists(fiscalref.mont_stage_csv_path) is False
        assert os_path_exists(fiscalref.week_stage_csv_path) is False

        # WHEN
        etl_fiscal_staging_tables_to_fiscal_csvs(fiscal_db_conn, fiscals_dir)

        # THEN
        assert os_path_exists(fiscalref.unit_stage_csv_path)
        assert os_path_exists(fiscalref.deal_stage_csv_path)
        assert os_path_exists(fiscalref.cash_stage_csv_path)
        assert os_path_exists(fiscalref.hour_stage_csv_path)
        assert os_path_exists(fiscalref.mont_stage_csv_path)
        assert os_path_exists(fiscalref.week_stage_csv_path)
        unit_stage_csv_filename = fiscalref.unit_stage_csv_filename
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
        assert len(open_file(fiscalref.deal_stage_csv_path)) == 76
        assert len(open_file(fiscalref.cash_stage_csv_path)) == 87
        assert len(open_file(fiscalref.hour_stage_csv_path)) == 78
        assert len(open_file(fiscalref.mont_stage_csv_path)) == 76
        assert len(open_file(fiscalref.week_stage_csv_path)) == 78


def test_etl_fiscal_agg_tables_to_fiscal_csvs_CreateFiles(env_dir_setup_cleanup):
    # sourcery skip: extract-method
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        cursor = fiscal_db_conn.cursor()
        fiscal_mstr_dir = get_test_etl_dir()
        fiscalref = FiscalPrimeObjsRef(fiscal_mstr_dir)
        insert_agg_sqlstr = f"""
INSERT INTO {fiscalref.unit_agg_tablename} ({fiscal_title_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_agg_sqlstr)
        assert os_path_exists(fiscalref.unit_agg_csv_path) is False
        assert os_path_exists(fiscalref.deal_agg_csv_path) is False
        assert os_path_exists(fiscalref.cash_agg_csv_path) is False
        assert os_path_exists(fiscalref.hour_agg_csv_path) is False
        assert os_path_exists(fiscalref.mont_agg_csv_path) is False
        assert os_path_exists(fiscalref.week_agg_csv_path) is False

        # WHEN
        etl_fiscal_agg_tables_to_fiscal_csvs(fiscal_db_conn, fiscal_mstr_dir)

        # THEN
        assert os_path_exists(fiscalref.unit_agg_csv_path)
        assert os_path_exists(fiscalref.deal_agg_csv_path)
        assert os_path_exists(fiscalref.cash_agg_csv_path)
        assert os_path_exists(fiscalref.hour_agg_csv_path)
        assert os_path_exists(fiscalref.mont_agg_csv_path)
        assert os_path_exists(fiscalref.week_agg_csv_path)
        unit_agg_csv_filename = fiscalref.unit_agg_csv_filename
        generated_fiscalunit_csv = open_file(fiscal_mstr_dir, unit_agg_csv_filename)
        expected_fiscalunit_csv_str = f"""{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{current_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
        assert generated_fiscalunit_csv == expected_fiscalunit_csv_str
