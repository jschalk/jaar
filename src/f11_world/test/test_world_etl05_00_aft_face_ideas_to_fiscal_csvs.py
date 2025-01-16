from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import db_table_exists, get_row_count
from src.f01_road.finance_tran import bridge_str, time_int_str, quota_str
from src.f03_chrono.chrono import (
    c400_number_str,
    monthday_distortion_str,
    timeline_title_str,
    yr1_jan1_offset_str,
)
from src.f04_gift.atom_config import (
    face_name_str,
    fiscal_title_str,
    acct_name_str,
    owner_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f07_fiscal.fiscal_config import (
    current_time_str,
    amount_str,
    month_title_str,
    hour_title_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_title_str,
    weekday_order_str,
    fiscalunit_str,
    fiscal_deal_episode_str,
    fiscal_cashbook_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
    get_fiscal_config_args,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_config import (
    get_idea_sqlite_types,
    get_idea_format_filename,
    get_idearef_from_file,
    idea_number_str,
)
from src.f09_idea.pandas_tool import (
    _get_fiscal_idea_format_filenames,
    boat_agg_str,
    get_sorting_columns,
    get_pragma_table_fetchall,
)
from src.f10_etl.fiscal_agg import FiscalPrimeColumns, FiscalPrimeFilePaths
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists
from copy import copy as copy_copy
from platform import system as platform_system
from sqlite3 import connect as sqlite3_connect

# def test_WorldUnit_memory_fiscal_db_conn_ReturnsDBConnection(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")

#     # WHEN / THEN
#     with fizz_world.memory_fiscal_db_conn() as fiscal_db_conn:
#         assert fiscal_db_conn != None
#         cursor = fiscal_db_conn.cursor()
#         x_tablename = "random_name_table"
#         cursor.execute(f"PRAGMA table_info({x_tablename})")
#         columns = cursor.fetchall()
#         assert columns == []  # implication is database exists


def test_WorldUnit_aft_face_csv_files_to_fiscal_db_HasIdeaDataFromCSV_aft_face_csv_files_to_fiscal_db(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    fizz_world = worldunit_shop("fizz")
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    print(f"{sue_aft_dir=}")
    fizz_world = worldunit_shop("fizz")

    # WHEN / THEN
    br00011_staging_tablename = f"{br00011_str}_staging"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fizz_world.aft_face_csv_files_to_fiscal_db(fiscal_db_conn)
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
        print(f"{type(fiscal_db_conn)=}")
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


def test_WorldUnit_idea_staging_to_fiscal_tables_CreatesFiscalStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")

    # WHEN / THEN
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
        fizz_world.idea_staging_to_fiscal_tables(fiscal_db_conn)
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


def test_WorldUnit_idea_staging_to_fiscal_tables_Bud_category_idea_PopulatesFiscalStagingTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    fizz_world = worldunit_shop("fizz")
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord23_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")
    fiscalunit_tablename = f"{fiscalunit_str()}_staging"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fizz_world.aft_face_csv_files_to_fiscal_db(fiscal_db_conn)
        assert not db_table_exists(fiscal_db_conn, fiscalunit_tablename)

        # WHEN
        fizz_world.idea_staging_to_fiscal_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, fiscalunit_tablename) == 2
        cursor = fiscal_db_conn.cursor()
        cursor.execute(f"SELECT * FROM {fiscalunit_tablename}")
        fiscalunit_db_rows = cursor.fetchall()
        expected_row1 = (
            br00011_str,
            sue_inx,
            event3,
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
            br00011_str,
            sue_inx,
            event7,
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


def test_WorldUnit_idea_staging_to_fiscal_tables_PopulatesFiscalAggTables(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-method

    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    fizz_world = worldunit_shop("fizz")
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    br00011_str = "br00011"
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord45_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")

    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fizz_world.aft_face_csv_files_to_fiscal_db(fiscal_db_conn)
        fiscalunit_agg_tablename = f"{fiscalunit_str()}_agg"
        assert not db_table_exists(fiscal_db_conn, fiscalunit_agg_tablename)

        # WHEN
        fizz_world.idea_staging_to_fiscal_tables(fiscal_db_conn)

        # THEN
        assert db_table_exists(fiscal_db_conn, fiscalunit_agg_tablename)
        cursor = fiscal_db_conn.cursor()
        # fiscalunit_stage_tablename = f"{fiscalunit_str()}_staging"
        # cursor.execute(f"SELECT * FROM {fiscalunit_stage_tablename};")
        # fiscalunit_stage_rows = cursor.fetchall()
        # assert len(fiscalunit_stage_rows) == 4
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


def test_WorldUnit_aft_faces_ideas_to_fiscal_mstr_csvs_CreateStagingFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    fizz_world = worldunit_shop("fizz")
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")
    fiscalunit_staging_csv_filename = "fiscalunit_staging.csv"
    fiscalunit_staging_csv_path = create_path(
        fizz_world._fiscal_mstr_dir, fiscalunit_staging_csv_filename
    )
    fizz_world.aft_face_ideas_to_csv_files()
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fizz_world.aft_face_csv_files_to_fiscal_db(fiscal_db_conn)
        fizz_world.idea_staging_to_fiscal_tables(fiscal_db_conn)
        assert os_path_exists(fiscalunit_staging_csv_path) is False

        # WHEN
        fizz_world.aft_faces_ideas_to_fiscal_mstr_csvs(fiscal_db_conn)

        # THEN
        # print(f"{fiscalunit_staging_csv_path=}")
        assert os_path_exists(fiscalunit_staging_csv_path)
        generated_fiscalunit_csv = open_file(
            fizz_world._fiscal_mstr_dir, fiscalunit_staging_csv_filename
        )
        expected_fiscalunit_csv_str = f"""{idea_number_str()},{face_name_str()},{event_int_str()},{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{current_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{br00011_str},{sue_inx},{event3},{accord23_str},,,,,,,,,
{br00011_str},{sue_inx},{event7},{accord45_str},,,,,,,,,
"""
        print(f"   {expected_fiscalunit_csv_str=}")
        assert generated_fiscalunit_csv == expected_fiscalunit_csv_str


def test_WorldUnit_aft_faces_ideas_to_fiscal_mstr_csvs_CreateAggFiles(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    fizz_world = worldunit_shop("fizz")
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{face_name_str()},{event_int_str()},{fiscal_title_str()},{owner_name_str()},{acct_name_str()}
{sue_inx},{event3},{accord23_str},{bob_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{bob_inx}
{sue_inx},{event3},{accord23_str},{yao_inx},{yao_inx}
{sue_inx},{event7},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_aft_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz")
    fiscalunit_csv_filename = "fiscalunit_agg.csv"
    fiscalunit_csv_path = create_path(
        fizz_world._fiscal_mstr_dir, fiscalunit_csv_filename
    )

    fizz_world.aft_face_ideas_to_csv_files()
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        fizz_world.aft_face_csv_files_to_fiscal_db(fiscal_db_conn)
        fizz_world.idea_staging_to_fiscal_tables(fiscal_db_conn)
        assert os_path_exists(fiscalunit_csv_path) is False

        # WHEN
        fizz_world.aft_faces_ideas_to_fiscal_mstr_csvs(fiscal_db_conn)

        # THEN
        # print(f"{fiscalunit_csv_path=}")
        assert os_path_exists(fiscalunit_csv_path)
        generated_fiscalunit_csv = open_file(fiscalunit_csv_path)
        expected_fiscalunit_csv_str = f"""{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{current_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
        print(f"{expected_fiscalunit_csv_str=}")
        print(f"   {generated_fiscalunit_csv=}")
        assert generated_fiscalunit_csv == expected_fiscalunit_csv_str


# def test_WorldUnit_aft_faces_ideas_to_fiscal_staging_CreatesCorrectTables(
#     env_dir_setup_cleanup,
# ):

#     # THEN
#     staging_str = "staging"
#     br00000_path = create_path(fizz_world._faces_aft_dir, "br00000.xlsx")
#     br00001_path = create_path(fizz_world._faces_aft_dir, "br00001.xlsx")
#     br00002_path = create_path(fizz_world._faces_aft_dir, "br00002.xlsx")
#     br00003_path = create_path(fizz_world._faces_aft_dir, "br00003.xlsx")
#     br00004_path = create_path(fizz_world._faces_aft_dir, "br00004.xlsx")
#     br00005_path = create_path(fizz_world._faces_aft_dir, "br00005.xlsx")

#     br00000_df = pandas_read_excel(br00000_path, sheet_name=staging_str)
#     br00001_df = pandas_read_excel(br00001_path, sheet_name=staging_str)
#     br00002_df = pandas_read_excel(br00002_path, sheet_name=staging_str)
#     br00003_df = pandas_read_excel(br00003_path, sheet_name=staging_str)
#     br00004_df = pandas_read_excel(br00004_path, sheet_name=staging_str)
#     br00005_df = pandas_read_excel(br00005_path, sheet_name=staging_str)

#     common_cols = [face_name_str(), event_int_str(), fiscal_title_str()]
#     expected_br0_columns = copy_copy(common_cols)
#     expected_br1_columns = copy_copy(common_cols)
#     expected_br2_columns = copy_copy(common_cols)
#     expected_br3_columns = copy_copy(common_cols)
#     expected_br4_columns = copy_copy(common_cols)
#     expected_br5_columns = copy_copy(common_cols)
#     expected_br0_columns.extend(
#         [
#             c400_number_str(),
#             current_time_str(),
#             fund_coin_str(),
#             monthday_distortion_str(),
#             penny_str(),
#             respect_bit_str(),
#             bridge_str(),
#             timeline_title_str(),
#             yr1_jan1_offset_str(),
#         ]
#     )
#     expected_br1_columns.extend(
#         [owner_name_str(), acct_name_str(), time_int_str(), quota_str()]
#     )
#     expected_br2_columns.extend(
#         [owner_name_str(), acct_name_str(), time_int_str(), amount_str()]
#     )
#     expected_br3_columns.extend([hour_title_str(), cumlative_minute_str()])
#     expected_br4_columns.extend([month_title_str(), cumlative_day_str()])
#     expected_br5_columns.extend([weekday_title_str(), weekday_order_str()])

#     print(f"{list(br00000_df.columns)=}")
#     assert list(br00000_df.columns) == expected_br0_columns
#     assert list(br00001_df.columns) == expected_br1_columns
#     assert list(br00002_df.columns) == expected_br2_columns
#     assert list(br00003_df.columns) == expected_br3_columns
#     assert list(br00004_df.columns) == expected_br4_columns
#     assert list(br00005_df.columns) == expected_br5_columns


# def test_WorldUnit_boat_agg_to_pidgin_staging_CreatesFile(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     rdx = ":"
#     ukx = "Unknown"
#     m_str = "accord23"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     br00113_file_path = create_path(fizz_world._boat_dir, "br00113.xlsx")
#     br00113_columns = [
#         face_name_str(),
#         event_int_str(),
#         fiscal_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_name_str(),
#         inx_name_str(),
#     ]
#     br00043_file_path = create_path(fizz_world._boat_dir, "br00043.xlsx")
#     br00043_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_name_str(),
#         inx_name_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00113_rows = [sue0, sue1]
#     br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
#     upsert_sheet(br00113_file_path, boat_agg_str(), br00113_df)
#     br00043_df = [sue2, sue3, yao1]
#     br00043_df = DataFrame(br00043_df, columns=br00043_columns)
#     upsert_sheet(br00043_file_path, boat_agg_str(), br00043_df)
#     pidgin_path = create_path(fizz_world._boat_dir, "pidgin.xlsx")

#     br00115_file_path = create_path(fizz_world._boat_dir, "br00115.xlsx")
#     br00115_columns = [
#         face_name_str(),
#         event_int_str(),
#         fiscal_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_label_str(),
#         inx_label_str(),
#     ]
#     br00042_file_path = create_path(fizz_world._boat_dir, "br00042.xlsx")
#     br00042_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_label_str(),
#         inx_label_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00115_rows = [sue0, sue1]
#     br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
#     upsert_sheet(br00115_file_path, boat_agg_str(), br00115_df)
#     b40_rows = [sue2, sue3, yao1]
#     br00042_df = DataFrame(b40_rows, columns=br00042_columns)
#     upsert_sheet(br00042_file_path, boat_agg_str(), br00042_df)

#     br00116_file_path = create_path(fizz_world._boat_dir, "br00116.xlsx")
#     br00116_columns = [
#         face_name_str(),
#         event_int_str(),
#         fiscal_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_title_str(),
#         inx_title_str(),
#     ]
#     br00044_file_path = create_path(fizz_world._boat_dir, "br00044.xlsx")
#     br00044_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_title_str(),
#         inx_title_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     br00116_rows = [sue0, sue1]
#     br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
#     upsert_sheet(br00116_file_path, boat_agg_str(), br00116_df)
#     br00044_rows = [sue2, sue3, yao1]
#     br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
#     upsert_sheet(br00044_file_path, boat_agg_str(), br00044_df)

#     br00117_file_path = create_path(fizz_world._boat_dir, "br00117.xlsx")
#     br00117_columns = [
#         face_name_str(),
#         event_int_str(),
#         fiscal_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_road_str(),
#         inx_road_str(),
#     ]
#     br00045_file_path = create_path(fizz_world._boat_dir, "br00045.xlsx")
#     br00045_columns = [
#         face_name_str(),
#         event_int_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
#     sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
#     b117_rows = [sue0, sue1]
#     br00117_df = DataFrame(b117_rows, columns=br00117_columns)
#     upsert_sheet(br00117_file_path, boat_agg_str(), br00117_df)
#     br00045_rows = [sue2, sue3, yao1]
#     br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
#     upsert_sheet(br00045_file_path, boat_agg_str(), br00045_df)

#     assert fizz_world.events == {}
#     fizz_world.boat_agg_to_boat_events()
#     fizz_world.boat_events_to_events_log()
#     fizz_world.boat_events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg_file()
#     assert fizz_world.events == {event2: sue_str, event5: sue_str}
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.boat_agg_to_pidgin_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     label_staging_str = "label_staging"
#     name_staging_str = "name_staging"
#     title_staging_str = "title_staging"
#     road_staging_str = "road_staging"
#     assert sheet_exists(pidgin_path, name_staging_str)
#     assert sheet_exists(pidgin_path, label_staging_str)
#     assert sheet_exists(pidgin_path, title_staging_str)
#     assert sheet_exists(pidgin_path, road_staging_str)

#     gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_staging_str)
#     gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_staging_str)
#     gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_staging_str)
#     gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)

#     label_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_label_str(),
#         inx_label_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_label_df.columns) == label_file_columns
#     assert len(gen_label_df) == 2
#     b3 = "br00115"
#     b4 = "br00042"
#     e1_label3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_label4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_label_rows = [e1_label3, e1_label4]
#     e1_label_df = DataFrame(e1_label_rows, columns=label_file_columns)
#     assert len(gen_label_df) == len(e1_label_df)
#     print(f"{gen_label_df.to_csv()=}")
#     print(f" {e1_label_df.to_csv()=}")
#     assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)

#     name_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_name_str(),
#         inx_name_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_name_df.columns) == name_file_columns
#     assert len(gen_name_df) == 2
#     b3 = "br00113"
#     b4 = "br00043"
#     e1_name3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_name4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_name_rows = [e1_name3, e1_name4]
#     e1_name_df = DataFrame(e1_name_rows, columns=name_file_columns)
#     assert len(gen_name_df) == len(e1_name_df)
#     print(f"{gen_name_df.to_csv()=}")
#     print(f" {e1_name_df.to_csv()=}")
#     assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)

#     title_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_title_str(),
#         inx_title_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_title_df.columns) == title_file_columns
#     assert len(gen_title_df) == 2
#     b3 = "br00116"
#     b4 = "br00044"
#     e1_title3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_title4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_title_rows = [e1_title3, e1_title4]
#     e1_title_df = DataFrame(e1_title_rows, columns=title_file_columns)
#     assert len(gen_title_df) == len(e1_title_df)
#     print(f"{gen_title_df.to_csv()=}")
#     print(f" {e1_title_df.to_csv()=}")
#     assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)

#     road_file_columns = [
#         "src_idea",
#         face_name_str(),
#         event_int_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_bridge_str(),
#         inx_bridge_str(),
#         unknown_word_str(),
#     ]
#     assert list(gen_road_df.columns) == road_file_columns
#     assert len(gen_road_df) == 2
#     b3 = "br00117"
#     b4 = "br00045"
#     e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
#     e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
#     e1_road_rows = [e1_road3, e1_road4]
#     e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
#     assert len(gen_road_df) == len(e1_road_df)
#     print(f"{gen_road_df.to_csv()=}")
#     print(f" {e1_road_df.to_csv()=}")
#     assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)


# def test_WorldUnit_aft_face_ideas_to_aft_event_ideas_CreatesFaceIdeaSheets_Scenario0_MultpleFaceNames(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     zia_str = "Zia"
#     event3 = 3
#     event7 = 7
#     event9 = 9
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     idea_columns = [
#         face_name_str(),
#         event_int_str(),
#         fiscal_title_str(),
#         hour_title_str(),
#         cumlative_minute_str(),
#     ]
#     accord23_str = "accord23"
#     sue0 = [sue_str, event3, accord23_str, hour6am, minute_360]
#     sue1 = [sue_str, event3, accord23_str, hour7am, minute_420]
#     zia0 = [zia_str, event7, accord23_str, hour7am, minute_420]
#     zia1 = [zia_str, event9, accord23_str, hour6am, minute_360]
#     zia2 = [zia_str, event9, accord23_str, hour7am, minute_420]
#     example_sue_df = DataFrame([sue0, sue1], columns=idea_columns)
#     example_zia_df = DataFrame([zia0, zia1, zia2], columns=idea_columns)
#     fizz_world = worldunit_shop("fizz")
#     br00003_filename = "br00003.xlsx"
#     sue_dir = create_path(fizz_world._faces_aft_dir, sue_str)
#     zia_dir = create_path(fizz_world._faces_aft_dir, zia_str)
#     sue_br00003_filepath = create_path(sue_dir, br00003_filename)
#     zia_br00003_filepath = create_path(zia_dir, br00003_filename)
#     upsert_sheet(sue_br00003_filepath, "inx", example_sue_df)
#     upsert_sheet(zia_br00003_filepath, "inx", example_zia_df)

#     event3_dir = create_path(sue_dir, event3)
#     event7_dir = create_path(zia_dir, event7)
#     event9_dir = create_path(zia_dir, event9)
#     event3_br00003_filepath = create_path(event3_dir, br00003_filename)
#     event7_br00003_filepath = create_path(event7_dir, br00003_filename)
#     event9_br00003_filepath = create_path(event9_dir, br00003_filename)
#     assert sheet_exists(event3_br00003_filepath, "inx") is False
#     assert sheet_exists(event7_br00003_filepath, "inx") is False
#     assert sheet_exists(event9_br00003_filepath, "inx") is False

#     # WHEN
#     fizz_world.aft_face_ideas_to_aft_event_ideas()

#     # THEN
#     assert sheet_exists(event3_br00003_filepath, "inx")
#     assert sheet_exists(event7_br00003_filepath, "inx")
#     assert sheet_exists(event9_br00003_filepath, "inx")
#     gen_event3_df = pandas_read_excel(event3_br00003_filepath, "inx")
#     gen_event7_df = pandas_read_excel(event7_br00003_filepath, "inx")
#     gen_event9_df = pandas_read_excel(event9_br00003_filepath, "inx")
#     example_event3_df = DataFrame([sue0, sue1], columns=idea_columns)
#     example_event7_df = DataFrame([zia0], columns=idea_columns)
#     example_event9_df = DataFrame([zia1, zia2], columns=idea_columns)
#     pandas_assert_frame_equal(gen_event3_df, example_event3_df)
#     pandas_assert_frame_equal(gen_event7_df, example_event7_df)
#     pandas_assert_frame_equal(gen_event9_df, example_event9_df)
