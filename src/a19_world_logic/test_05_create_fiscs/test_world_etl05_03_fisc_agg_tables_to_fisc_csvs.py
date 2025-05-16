from src.a00_data_toolbox.file_toolbox import create_path, save_file, open_file
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_word_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a17_creed_logic.creed_db_tool import get_pragma_table_fetchall
from src.a18_etl_toolbox.fisc_etl_tool import (
    FiscPrimeColumnsRef,
    FiscPrimeObjsRef,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_inz_faces_creeds_to_fisc_mstr_csvs_CreateRawFiles(
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
    fizz_world = worldunit_shop("fizz", worlds_dir())
    sue_inz_dir = create_path(fizz_world._syntax_inz_dir, sue_inx)
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{event_int_str()},{face_name_str()},{fisc_word_str()},{owner_name_str()},{acct_name_str()}
{event3},{sue_inx},{accord23_str},{bob_inx},{bob_inx}
{event3},{sue_inx},{accord23_str},{yao_inx},{bob_inx}
{event3},{sue_inx},{accord23_str},{yao_inx},{yao_inx}
{event7},{sue_inx},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz", worlds_dir())
    fisc_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
    fizz_world.inz_face_creeds_to_csv_files()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.inz_face_csv_files2creed_raw_tables(cursor)
        fizz_world.creed_raw_to_fisc_prime_tables(cursor)
        assert os_path_exists(fisc_objs.unit_raw_csv_path) is False

        # WHEN
        fizz_world.inz_faces_creeds_to_fisc_mstr_csvs(cursor)

        # THEN
        print(f"{fisc_objs.unit_raw_csv_path=}")
        assert os_path_exists(fisc_objs.unit_raw_csv_path)
        generated_fiscunit_csv = open_file(fisc_objs.unit_raw_csv_path)
        fisc_cols = FiscPrimeColumnsRef()
        expected_fiscunit_csv_str = f"""{fisc_cols.unit_raw_csv_header}
{br00011_str},{event3},{sue_inx},{accord23_str},,,,,,,,,,
{br00011_str},{event7},{sue_inx},{accord45_str},,,,,,,,,,
"""
        print(f"   {expected_fiscunit_csv_str=}")
        assert generated_fiscunit_csv == expected_fiscunit_csv_str


def test_WorldUnit_inz_faces_creeds_to_fisc_mstr_csvs_CreateAggFiles(
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
    br00011_str = "br00011"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    sue_inz_dir = create_path(fizz_world._syntax_inz_dir, sue_inx)
    br00011_csv_filename = f"{br00011_str}.csv"
    br00011_csv_str = f"""{event_int_str()},{face_name_str()},{fisc_word_str()},{owner_name_str()},{acct_name_str()}
{event3},{sue_inx},{accord23_str},{bob_inx},{bob_inx}
{event3},{sue_inx},{accord23_str},{yao_inx},{bob_inx}
{event3},{sue_inx},{accord23_str},{yao_inx},{yao_inx}
{event7},{sue_inx},{accord45_str},{yao_inx},{yao_inx}
"""
    save_file(sue_inz_dir, br00011_csv_filename, br00011_csv_str)
    fizz_world = worldunit_shop("fizz", worlds_dir())
    fizz_world.inz_face_creeds_to_csv_files()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fizz_world.inz_face_csv_files2creed_raw_tables(cursor)
        fizz_world.creed_raw_to_fisc_prime_tables(cursor)
        fiz_objs = FiscPrimeObjsRef(fizz_world._fisc_mstr_dir)
        assert os_path_exists(fiz_objs.unit_agg_csv_path) is False

        # WHEN
        fizz_world.inz_faces_creeds_to_fisc_mstr_csvs(cursor)

        # THEN
        # print(f"{fiscunit_csv_path=}")
        assert os_path_exists(fiz_objs.unit_agg_csv_path)
        generated_fiscunit_csv = open_file(fiz_objs.unit_agg_csv_path)
        fisc_cols = FiscPrimeColumnsRef()
        expected_fiscunit_csv_str = f"""{fisc_cols.unit_agg_csv_header}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
        print(f"{expected_fiscunit_csv_str=}")
        print(f"   {generated_fiscunit_csv=}")
        assert generated_fiscunit_csv == expected_fiscunit_csv_str
