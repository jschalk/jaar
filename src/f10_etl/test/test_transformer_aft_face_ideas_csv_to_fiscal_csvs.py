from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import db_table_exists
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
    agg_str = "_agg"
    fiscalunit_agg_tablename = f"{fiscalunit_str()}{agg_str}"
    fiscaldeal_agg_tablename = f"{fiscal_deal_episode_str()}{agg_str}"
    fiscalcash_agg_tablename = f"{fiscal_cashbook_str()}{agg_str}"
    fiscalhour_agg_tablename = f"{fiscal_timeline_hour_str()}{agg_str}"
    fiscalmont_agg_tablename = f"{fiscal_timeline_month_str()}{agg_str}"
    fiscalweek_agg_tablename = f"{fiscal_timeline_weekday_str()}{agg_str}"
    staging_str = "_staging"
    fiscalunit_stage_tablename = f"{fiscalunit_str()}{staging_str}"
    fiscaldeal_stage_tablename = f"{fiscal_deal_episode_str()}{staging_str}"
    fiscalcash_stage_tablename = f"{fiscal_cashbook_str()}{staging_str}"
    fiscalhour_stage_tablename = f"{fiscal_timeline_hour_str()}{staging_str}"
    fiscalmont_stage_tablename = f"{fiscal_timeline_month_str()}{staging_str}"
    fiscalweek_stage_tablename = f"{fiscal_timeline_weekday_str()}{staging_str}"
    fiscalunit_args = get_fiscal_config_args(fiscalunit_str()).keys()
    fiscaldeal_args = get_fiscal_config_args(fiscal_deal_episode_str()).keys()
    fiscalcash_args = get_fiscal_config_args(fiscal_cashbook_str()).keys()
    fiscalhour_args = get_fiscal_config_args(fiscal_timeline_hour_str()).keys()
    fiscalmont_args = get_fiscal_config_args(fiscal_timeline_month_str()).keys()
    fiscalweek_args = get_fiscal_config_args(fiscal_timeline_weekday_str()).keys()
    staging_columns = ["idea_number", "face_name", "event_int"]
    fiscalunit_agg_columns = get_sorting_columns(fiscalunit_args)
    fiscaldeal_agg_columns = get_sorting_columns(fiscaldeal_args)
    fiscalcash_agg_columns = get_sorting_columns(fiscalcash_args)
    fiscalhour_agg_columns = get_sorting_columns(fiscalhour_args)
    fiscalmont_agg_columns = get_sorting_columns(fiscalmont_args)
    fiscalweek_agg_columns = get_sorting_columns(fiscalweek_args)
    fiscalunit_agg_pragma = get_pragma_table_fetchall(fiscalunit_agg_columns)
    fiscaldeal_agg_pragma = get_pragma_table_fetchall(fiscaldeal_agg_columns)
    fiscalcash_agg_pragma = get_pragma_table_fetchall(fiscalcash_agg_columns)
    fiscalhour_agg_pragma = get_pragma_table_fetchall(fiscalhour_agg_columns)
    fiscalmont_agg_pragma = get_pragma_table_fetchall(fiscalmont_agg_columns)
    fiscalweek_agg_pragma = get_pragma_table_fetchall(fiscalweek_agg_columns)

    fiscalunit_stage_columns = copy_copy(staging_columns)
    fiscaldeal_stage_columns = copy_copy(staging_columns)
    fiscalcash_stage_columns = copy_copy(staging_columns)
    fiscalhour_stage_columns = copy_copy(staging_columns)
    fiscalmont_stage_columns = copy_copy(staging_columns)
    fiscalweek_stage_columns = copy_copy(staging_columns)
    fiscalunit_stage_columns.extend(fiscalunit_agg_columns)
    fiscaldeal_stage_columns.extend(fiscaldeal_agg_columns)
    fiscalcash_stage_columns.extend(fiscalcash_agg_columns)
    fiscalhour_stage_columns.extend(fiscalhour_agg_columns)
    fiscalmont_stage_columns.extend(fiscalmont_agg_columns)
    fiscalweek_stage_columns.extend(fiscalweek_agg_columns)
    fiscalunit_stage_pragma = get_pragma_table_fetchall(fiscalunit_stage_columns)
    fiscaldeal_stage_pragma = get_pragma_table_fetchall(fiscaldeal_stage_columns)
    fiscalcash_stage_pragma = get_pragma_table_fetchall(fiscalcash_stage_columns)
    fiscalhour_stage_pragma = get_pragma_table_fetchall(fiscalhour_stage_columns)
    fiscalmont_stage_pragma = get_pragma_table_fetchall(fiscalmont_stage_columns)
    fiscalweek_stage_pragma = get_pragma_table_fetchall(fiscalweek_stage_columns)

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        assert db_table_exists(fiscal_db_conn, fiscalunit_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscaldeal_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalcash_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalhour_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalmont_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalweek_agg_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalunit_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscaldeal_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalcash_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalhour_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalmont_stage_tablename) is False
        assert db_table_exists(fiscal_db_conn, fiscalweek_stage_tablename) is False

        # WHEN
        create_fiscal_tables(fiscal_db_conn)

        # THEN
        assert db_table_exists(fiscal_db_conn, fiscalunit_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fiscaldeal_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fiscalcash_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fiscalhour_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fiscalmont_agg_tablename)
        assert db_table_exists(fiscal_db_conn, fiscalweek_agg_tablename)

        assert db_table_exists(fiscal_db_conn, fiscalunit_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fiscaldeal_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fiscalcash_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fiscalhour_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fiscalmont_stage_tablename)
        assert db_table_exists(fiscal_db_conn, fiscalweek_stage_tablename)
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"PRAGMA table_info({fiscalunit_agg_tablename})")
        assert fiscalunit_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscaldeal_agg_tablename})")
        assert fiscaldeal_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscalcash_agg_tablename})")
        assert fiscalcash_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscalhour_agg_tablename})")
        assert fiscalhour_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscalmont_agg_tablename})")
        assert fiscalmont_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscalweek_agg_tablename})")
        assert fiscalweek_agg_pragma == cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({fiscalunit_stage_tablename})")
        assert fiscalunit_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscaldeal_stage_tablename})")
        assert fiscaldeal_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscalcash_stage_tablename})")
        assert fiscalcash_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscalhour_stage_tablename})")
        assert fiscalhour_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscalmont_stage_tablename})")
        assert fiscalmont_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fiscalweek_stage_tablename})")
        assert fiscalweek_stage_pragma == cursor.fetchall()


def test_populate_fiscal_staging_tables_PopulatesFiscalStagingTables(
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
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"SELECT * FROM {fiscalunit_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        assert fiscalunit_db_rows == []

        # WHEN
        populate_fiscal_staging_tables(fiscal_db_conn)

        # THEN
        cursor.execute(f"SELECT * FROM {fiscalunit_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row1 = (
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
        )
        expected_row2 = (
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
        )
        assert fiscalunit_db_rows == [expected_row1, expected_row2]


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
        assert fiscalunit_agg_rows == [expected_row1, expected_row2]


def test_etl_fiscal_staging_tables_to_fiscal_csvs_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    fiscalunit_staging_tablename = f"{fiscalunit_str()}_staging"
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
        fiscal_mstr_dir = get_test_etl_dir()
        fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
        fiscalunit_csv_filename = f"{fiscalunit_staging_tablename}.csv"
        fiscalunit_csv_path = create_path(fiscals_dir, fiscalunit_csv_filename)
        assert os_path_exists(fiscalunit_csv_path) is False

        # WHEN
        etl_fiscal_staging_tables_to_fiscal_csvs(fiscal_db_conn, fiscals_dir)

        # THEN
        assert os_path_exists(fiscalunit_csv_path)
        generated_fiscalunit_csv = open_file(fiscals_dir, fiscalunit_csv_filename)
        expected_fiscalunit_csv_str = f"""{idea_number_str()},{face_name_str()},{event_int_str()},{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{current_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,
{br00011_str},{sue_inx},{event3},{accord45_str},,,,,,,,,
{br00011_str},{sue_inx},{event7},{accord45_str},,,,,,,,,
"""
        assert generated_fiscalunit_csv == expected_fiscalunit_csv_str


def test_etl_fiscal_agg_tables_to_fiscal_csvs_CreateFiles(env_dir_setup_cleanup):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    fiscalunit_agg_tablename = f"{fiscalunit_str()}_agg"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        check_etl_fiscal_agg_tables_to_fiscal_csvs_CreateFile(
            fiscal_db_conn, fiscalunit_agg_tablename, accord23_str, accord45_str
        )


def check_etl_fiscal_agg_tables_to_fiscal_csvs_CreateFile(
    fiscal_db_conn, fiscalunit_agg_tablename, accord23_str, accord45_str
):
    create_fiscal_tables(fiscal_db_conn)
    cursor = fiscal_db_conn.cursor()
    insert_agg_sqlstr = f"""
INSERT INTO {fiscalunit_agg_tablename} (fiscal_title)
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
    cursor.execute(insert_agg_sqlstr)
    fiscal_mstr_dir = get_test_etl_dir()
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    fiscalunit_csv_filename = f"{fiscalunit_agg_tablename}.csv"
    fiscalunit_csv_path = create_path(fiscals_dir, fiscalunit_csv_filename)
    assert os_path_exists(fiscalunit_csv_path) is False

    # WHEN
    etl_fiscal_agg_tables_to_fiscal_csvs(fiscal_db_conn, fiscals_dir)

    # THEN
    assert os_path_exists(fiscalunit_csv_path)
    generated_fiscalunit_csv = open_file(fiscals_dir, fiscalunit_csv_filename)
    expected_fiscalunit_csv_str = f"""{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{current_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
    assert generated_fiscalunit_csv == expected_fiscalunit_csv_str
