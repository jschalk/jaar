from os.path import exists as os_path_exists
from pandas import DataFrame
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.a00_data_toolbox.file_toolbox import count_dirs_files, create_path, save_file
from src.a02_finance_logic.test._util.a02_str import (
    amount_str,
    bud_time_str,
    celldepth_str,
    owner_name_str,
    quota_str,
    tran_time_str,
    vow_label_str,
)
from src.a06_plan_logic.test._util.a06_str import acct_name_str
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a12_hub_toolbox.hub_path import (
    create_bud_acct_mandate_ledger_path as bud_mandate,
    create_event_all_pack_path,
    create_event_expressed_pack_path as expressed_path,
    create_gut_path,
    create_job_path,
    create_vow_json_path,
    create_vow_ote1_csv_path,
)
from src.a12_hub_toolbox.test._util.a12_str import vow_ote1_agg_str
from src.a15_vow_logic.test._util.a15_str import cumulative_minute_str, hour_label_str
from src.a16_pidgin_logic.test._util.a16_str import inx_name_str, otx_name_str
from src.a17_idea_logic.idea_db_tool import upsert_sheet
from src.a18_etl_toolbox.test._util.a18_str import (
    events_brick_agg_str,
    events_brick_valid_str,
    vow_acct_nets_str,
    vow_event_time_agg_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a19_kpi_toolbox.test._util.a19_str import vow_kpi001_acct_nets_str
from src.a20_world_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.a20_world_logic.world import worldunit_shop


def test_WorldUnit_mud_to_clarity_with_cursor_Scenario0_br000113PopulatesTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH:
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    # delete_dir(fizz_world.worlds_dir)
    sue_str = "Sue"
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        vow_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    a23_str = "accord23"
    br00113_str = "br00113"
    br00113row0 = [sue_str, e3, a23_str, sue_str, sue_str, sue_str, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(mud_file_path, br00113_ex0_str, br00113_df)
    br00113_raw = f"{br00113_str}_brick_raw"
    br00113_agg = f"{br00113_str}_brick_agg"
    br00113_valid = f"{br00113_str}_brick_valid"
    events_brick_valid_tablename = events_brick_valid_str()
    pidname_sound_raw = create_prime_tablename("pidname", "s", "raw")
    pidname_sound_agg = create_prime_tablename("pidname", "s", "agg")
    pidname_sound_vld = create_prime_tablename("pidname", "s", "vld")
    pidcore_sound_raw = create_prime_tablename("pidcore", "s", "raw")
    pidcore_sound_agg = create_prime_tablename("pidcore", "s", "agg")
    pidcore_sound_vld = create_prime_tablename("pidcore", "s", "vld")
    vowunit_sound_raw = create_prime_tablename("vowunit", "s", "raw")
    vowunit_sound_agg = create_prime_tablename("vowunit", "s", "agg")
    vowunit_sound_vld = create_prime_tablename("vowunit", "s", "vld")
    plnunit_sound_put_raw = create_prime_tablename("planunit", "s", "raw", "put")
    plnunit_sound_put_agg = create_prime_tablename("planunit", "s", "agg", "put")
    plnunit_sound_put_vld = create_prime_tablename("planunit", "s", "vld", "put")
    plnacct_sound_put_raw = create_prime_tablename("plnacct", "s", "raw", "put")
    plnacct_sound_put_agg = create_prime_tablename("plnacct", "s", "agg", "put")
    plnacct_sound_put_vld = create_prime_tablename("plnacct", "s", "vld", "put")
    vowunit_voice_raw = create_prime_tablename("vowunit", "v", "raw")
    vowunit_voice_agg = create_prime_tablename("vowunit", "v", "agg")
    plnunit_voice_put_raw = create_prime_tablename("planunit", "v", "raw", "put")
    plnunit_voice_put_agg = create_prime_tablename("planunit", "v", "agg", "put")
    plnacct_voice_put_raw = create_prime_tablename("plnacct", "v", "raw", "put")
    plnacct_voice_put_agg = create_prime_tablename("plnacct", "v", "agg", "put")
    mstr_dir = fizz_world._vow_mstr_dir
    a23_json_path = create_vow_json_path(mstr_dir, a23_str)
    a23_e1_all_pack_path = create_event_all_pack_path(mstr_dir, a23_str, sue_inx, e3)
    a23_e1_expressed_pack_path = expressed_path(mstr_dir, a23_str, sue_inx, e3)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_str, sue_inx)
    a23_sue_job_path = create_job_path(mstr_dir, a23_str, sue_inx)
    plnacct_job = create_prime_tablename("plnacct", "job", None)

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert not db_table_exists(cursor, br00113_raw)
        assert not db_table_exists(cursor, br00113_agg)
        assert not db_table_exists(cursor, events_brick_agg_str())
        assert not db_table_exists(cursor, events_brick_valid_tablename)
        assert not db_table_exists(cursor, br00113_valid)
        assert not db_table_exists(cursor, pidname_sound_raw)
        assert not db_table_exists(cursor, pidname_sound_agg)
        assert not db_table_exists(cursor, vowunit_sound_raw)
        assert not db_table_exists(cursor, vowunit_sound_agg)
        assert not db_table_exists(cursor, vowunit_sound_vld)
        assert not db_table_exists(cursor, plnunit_sound_put_raw)
        assert not db_table_exists(cursor, plnunit_sound_put_agg)
        assert not db_table_exists(cursor, plnunit_sound_put_vld)
        assert not db_table_exists(cursor, pidcore_sound_raw)
        assert not db_table_exists(cursor, pidcore_sound_agg)
        assert not db_table_exists(cursor, pidcore_sound_vld)
        assert not db_table_exists(cursor, pidname_sound_vld)
        assert not db_table_exists(cursor, vowunit_voice_raw)
        assert not db_table_exists(cursor, vowunit_voice_agg)
        assert not db_table_exists(cursor, plnunit_voice_put_raw)
        assert not db_table_exists(cursor, plnunit_voice_put_agg)
        assert not db_table_exists(cursor, plnacct_voice_put_raw)
        assert not db_table_exists(cursor, plnacct_voice_put_agg)
        assert not os_path_exists(a23_json_path)
        assert not os_path_exists(a23_e1_all_pack_path)
        assert not os_path_exists(a23_e1_expressed_pack_path)
        assert not os_path_exists(a23_sue_gut_path)
        assert not os_path_exists(a23_sue_job_path)
        assert not db_table_exists(cursor, vow_event_time_agg_str())
        assert not db_table_exists(cursor, vow_ote1_agg_str())
        assert not db_table_exists(cursor, plnacct_job)
        assert not db_table_exists(cursor, vow_acct_nets_str())
        assert not db_table_exists(cursor, vow_kpi001_acct_nets_str())

        # # create planunits
        # self.plan_tables_to_event_plan_csvs(cursor)

        # # create all vow_job and mandate reports
        # self.calc_vow_bud_acct_mandate_net_ledgers()

        # WHEN
        fizz_world.mud_to_clarity_with_cursor(db_conn, cursor)

        # THEN
        # select_pidgin_core = f"SELECT * FROM {pidcore_sound_vld}"
        # select_planunit_put = f"SELECT * FROM {plnunit_sound_put_agg}"
        # select_plnacct_put = f"SELECT * FROM {plnacct_sound_put_agg}"
        # select_vowunit_put_raw = f"SELECT * FROM {vowunit_sound_raw}"
        # select_vowunit_put_agg = f"SELECT * FROM {vowunit_sound_agg}"
        # print(f"{cursor.execute(select_pidgin_core).fetchall()=}")
        # print(f"{cursor.execute(select_planunit_put).fetchall()=}")
        # print(f"{cursor.execute(select_plnacct_put).fetchall()=}")
        # print(f"{cursor.execute(select_vowunit_put_raw).fetchall()=}")
        # print(f"{cursor.execute(select_vowunit_put_agg).fetchall()=}")

        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, events_brick_agg_str()) == 1
        assert get_row_count(cursor, events_brick_valid_tablename) == 1
        assert get_row_count(cursor, br00113_valid) == 1
        assert get_row_count(cursor, pidname_sound_raw) == 1
        assert get_row_count(cursor, vowunit_sound_raw) == 1
        assert get_row_count(cursor, plnunit_sound_put_raw) == 1
        assert get_row_count(cursor, plnacct_sound_put_raw) == 1
        assert get_row_count(cursor, pidname_sound_agg) == 1
        assert get_row_count(cursor, vowunit_sound_agg) == 1
        assert get_row_count(cursor, plnunit_sound_put_agg) == 1
        assert get_row_count(cursor, plnacct_sound_put_agg) == 1
        assert get_row_count(cursor, pidcore_sound_raw) == 1
        assert get_row_count(cursor, pidcore_sound_agg) == 1
        assert get_row_count(cursor, pidcore_sound_vld) == 1
        assert get_row_count(cursor, pidname_sound_vld) == 1
        assert get_row_count(cursor, vowunit_sound_vld) == 1
        assert get_row_count(cursor, plnunit_sound_put_vld) == 1
        assert get_row_count(cursor, plnacct_sound_put_vld) == 1
        assert get_row_count(cursor, vowunit_voice_raw) == 1
        assert get_row_count(cursor, plnunit_voice_put_raw) == 1
        assert get_row_count(cursor, plnacct_voice_put_raw) == 1
        assert get_row_count(cursor, vowunit_voice_agg) == 1
        assert get_row_count(cursor, plnunit_voice_put_agg) == 1
        assert get_row_count(cursor, plnacct_voice_put_agg) == 1
        assert os_path_exists(a23_json_path)
        print(f"{a23_e1_all_pack_path=}")
        assert os_path_exists(a23_e1_all_pack_path)
        assert os_path_exists(a23_e1_expressed_pack_path)
        assert os_path_exists(a23_sue_gut_path)
        assert os_path_exists(a23_sue_job_path)
        assert get_row_count(cursor, plnacct_job) == 1
        assert get_row_count(cursor, vow_acct_nets_str()) == 0
        # assert get_row_count(cursor, vow_event_time_agg_str()) == 0
        # assert get_row_count(cursor, vow_ote1_agg_tablename) == 0
        assert get_row_count(cursor, vow_kpi001_acct_nets_str()) == 0


def test_WorldUnit_mud_to_clarity_with_cursor_Scenario1_PopulateBudPayRows(
    env_dir_setup_cleanup,
):
    # ESTABLISH:
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    # delete_dir(fizz_world.worlds_dir)
    sue_str = "Sue"
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        vow_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    a23_str = "accord23"
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [sue_str, e3, a23_str, sue_str, sue_str, sue_str, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(mud_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        event_int_str(),
        face_name_str(),
        vow_label_str(),
        owner_name_str(),
        bud_time_str(),
        quota_str(),
        celldepth_str(),
    ]
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [e3, sue_str, a23_str, sue_str, tp37, sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(mud_file_path, br00001_ex0_str, br00001_1df)

    # Names of tables
    br00113_raw = f"{br00113_str}_brick_raw"
    br00113_agg = f"{br00113_str}_brick_agg"
    br00113_valid = f"{br00113_str}_brick_valid"
    events_brick_valid_tablename = events_brick_valid_str()
    pidname_sound_raw = create_prime_tablename("pidname", "s", "raw")
    pidname_sound_agg = create_prime_tablename("pidname", "s", "agg")
    pidname_sound_vld = create_prime_tablename("pidname", "s", "vld")
    pidcore_sound_raw = create_prime_tablename("pidcore", "s", "raw")
    pidcore_sound_agg = create_prime_tablename("pidcore", "s", "agg")
    pidcore_sound_vld = create_prime_tablename("pidcore", "s", "vld")
    vowunit_sound_raw = create_prime_tablename("vowunit", "s", "raw")
    vowunit_sound_agg = create_prime_tablename("vowunit", "s", "agg")
    plnunit_sound_put_raw = create_prime_tablename("planunit", "s", "raw", "put")
    plnunit_sound_put_agg = create_prime_tablename("planunit", "s", "agg", "put")
    plnacct_sound_put_raw = create_prime_tablename("plnacct", "s", "raw", "put")
    plnacct_sound_put_agg = create_prime_tablename("plnacct", "s", "agg", "put")
    vowunit_voice_raw = create_prime_tablename("vowunit", "v", "raw")
    vowunit_voice_agg = create_prime_tablename("vowunit", "v", "agg")
    plnunit_voice_put_raw = create_prime_tablename("planunit", "v", "raw", "put")
    plnunit_voice_put_agg = create_prime_tablename("planunit", "v", "agg", "put")
    plnacct_voice_put_raw = create_prime_tablename("plnacct", "v", "raw", "put")
    plnacct_voice_put_agg = create_prime_tablename("plnacct", "v", "agg", "put")
    mstr_dir = fizz_world._vow_mstr_dir
    a23_json_path = create_vow_json_path(mstr_dir, a23_str)
    a23_e1_all_pack_path = create_event_all_pack_path(mstr_dir, a23_str, sue_inx, e3)
    a23_e1_expressed_pack_path = expressed_path(mstr_dir, a23_str, sue_inx, e3)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_str, sue_inx)
    a23_sue_job_path = create_job_path(mstr_dir, a23_str, sue_inx)
    sue37_mandate_path = bud_mandate(mstr_dir, a23_str, sue_inx, tp37)

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert not db_table_exists(cursor, br00113_raw)
        assert not db_table_exists(cursor, br00113_agg)
        assert not db_table_exists(cursor, events_brick_agg_str())
        assert not db_table_exists(cursor, events_brick_valid_tablename)
        assert not db_table_exists(cursor, br00113_valid)
        assert not db_table_exists(cursor, pidname_sound_raw)
        assert not db_table_exists(cursor, pidname_sound_agg)
        assert not db_table_exists(cursor, vowunit_sound_raw)
        assert not db_table_exists(cursor, vowunit_sound_agg)
        assert not db_table_exists(cursor, plnunit_sound_put_raw)
        assert not db_table_exists(cursor, plnunit_sound_put_agg)
        assert not db_table_exists(cursor, pidcore_sound_raw)
        assert not db_table_exists(cursor, pidcore_sound_agg)
        assert not db_table_exists(cursor, pidcore_sound_vld)
        assert not db_table_exists(cursor, pidname_sound_vld)
        assert not db_table_exists(cursor, vowunit_voice_raw)
        assert not db_table_exists(cursor, vowunit_voice_agg)
        assert not db_table_exists(cursor, plnunit_voice_put_raw)
        assert not db_table_exists(cursor, plnunit_voice_put_agg)
        assert not db_table_exists(cursor, plnacct_voice_put_raw)
        assert not db_table_exists(cursor, plnacct_voice_put_agg)
        assert not os_path_exists(a23_json_path)
        assert not os_path_exists(a23_e1_all_pack_path)
        assert not os_path_exists(a23_e1_expressed_pack_path)
        assert not os_path_exists(a23_sue_gut_path)
        assert not os_path_exists(a23_sue_job_path)
        assert not db_table_exists(cursor, vow_ote1_agg_str())
        assert not os_path_exists(sue37_mandate_path)
        assert not db_table_exists(cursor, vow_acct_nets_str())
        assert not db_table_exists(cursor, vow_kpi001_acct_nets_str())
        # self.vow_agg_tables_to_vow_ote1_agg(cursor)

        # # create planunits
        # self.plan_tables_to_event_plan_csvs(cursor)

        # # create all vow_job and mandate reports
        # self.calc_vow_bud_acct_mandate_net_ledgers()

        # WHEN
        fizz_world.mud_to_clarity_with_cursor(db_conn, cursor)

        # THEN
        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, events_brick_agg_str()) == 2
        assert get_row_count(cursor, events_brick_valid_tablename) == 2
        assert get_row_count(cursor, br00113_valid) == 2
        assert get_row_count(cursor, pidname_sound_raw) == 2
        assert get_row_count(cursor, vowunit_sound_raw) == 4
        assert get_row_count(cursor, plnunit_sound_put_raw) == 4
        assert get_row_count(cursor, plnacct_sound_put_raw) == 2
        assert get_row_count(cursor, pidname_sound_agg) == 1
        assert get_row_count(cursor, vowunit_sound_agg) == 1
        assert get_row_count(cursor, plnunit_sound_put_agg) == 1
        assert get_row_count(cursor, plnacct_sound_put_agg) == 1
        assert get_row_count(cursor, pidcore_sound_raw) == 1
        assert get_row_count(cursor, pidcore_sound_agg) == 1
        assert get_row_count(cursor, pidcore_sound_vld) == 1
        assert get_row_count(cursor, pidname_sound_vld) == 1
        assert get_row_count(cursor, vowunit_voice_raw) == 1
        assert get_row_count(cursor, plnunit_voice_put_raw) == 1
        assert get_row_count(cursor, plnacct_voice_put_raw) == 1
        assert get_row_count(cursor, vowunit_voice_agg) == 1
        assert get_row_count(cursor, plnunit_voice_put_agg) == 1
        assert get_row_count(cursor, plnacct_voice_put_agg) == 1
        assert os_path_exists(a23_json_path)
        assert os_path_exists(a23_e1_all_pack_path)
        assert os_path_exists(a23_e1_expressed_pack_path)
        assert os_path_exists(a23_sue_gut_path)
        assert os_path_exists(a23_sue_job_path)
        assert get_row_count(cursor, vow_ote1_agg_str()) == 1
        print(f"{sue37_mandate_path=}")
        assert os_path_exists(sue37_mandate_path)
        assert get_row_count(cursor, vow_acct_nets_str()) == 1
        assert get_row_count(cursor, vow_kpi001_acct_nets_str()) == 1


def test_WorldUnit_mud_to_clarity_with_cursor_Scenario2_PopulateVowTranBook(
    env_dir_setup_cleanup,
):
    # ESTABLISH:
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    # delete_dir(fizz_world.worlds_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    e3 = 3
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    br00002_columns = [
        event_int_str(),
        face_name_str(),
        vow_label_str(),
        owner_name_str(),
        acct_name_str(),
        tran_time_str(),
        amount_str(),
    ]
    a23_str = "accord23"
    br00002_str = "br00002"
    tp37 = 37
    sue_to_bob_amount = 200
    br00002row0 = [e3, sue_str, a23_str, sue_str, bob_str, tp37, sue_to_bob_amount]
    br00002_df = DataFrame([br00002row0], columns=br00002_columns)
    br00002_ex0_str = f"example0_{br00002_str}"
    upsert_sheet(mud_file_path, br00002_ex0_str, br00002_df)

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert not db_table_exists(cursor, vow_acct_nets_str())

        # WHEN
        fizz_world.mud_to_clarity_with_cursor(db_conn, cursor)

        # THEN
        assert get_row_count(cursor, vow_acct_nets_str()) == 1


def test_WorldUnit_mud_to_clarity_with_cursor_Scenario3_WhenNoVowIdeas_ote1_IsStillCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    sue_str = "Sue"
    event2 = 2
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    accord23_str = "accord23"
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        vow_label_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    br00011_rows = [[event2, sue_str, accord23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(mud_file_path, "br00011_ex3", br00011_df)
    vow_mstr = fizz_world._vow_mstr_dir
    a23_ote1_csv_path = create_vow_ote1_csv_path(vow_mstr, accord23_str)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert os_path_exists(a23_ote1_csv_path) is False

        # WHEN
        fizz_world.mud_to_clarity_with_cursor(db_conn, cursor)

    # THEN
    assert os_path_exists(a23_ote1_csv_path)


def test_WorldUnit_mud_to_clarity_with_cursor_Scenario4_DeletesPreviousFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    print(f"{fizz_world.worlds_dir=}")
    mstr_dir = fizz_world._vow_mstr_dir
    vows_dir = create_path(mstr_dir, "vows")
    testing2_filename = "testing2.txt"
    testing3_filename = "testing3.txt"
    save_file(fizz_world.worlds_dir, testing2_filename, "")
    save_file(vows_dir, testing3_filename, "")
    testing2_path = create_path(fizz_world.worlds_dir, testing2_filename)
    testing3_path = create_path(vows_dir, testing3_filename)
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path)
    print(f"{testing3_path=}")
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()

        # WHEN
        fizz_world.mud_to_clarity_with_cursor(db_conn, cursor)

    # THEN
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path) is False


def test_WorldUnit_mud_to_clarity_with_cursor_Scenario5_CreatesFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    # delete_dir(fizz_world.worlds_dir)
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    br00003_columns = [
        event_int_str(),
        face_name_str(),
        cumulative_minute_str(),
        vow_label_str(),
        hour_label_str(),
    ]
    br00001_columns = [
        event_int_str(),
        face_name_str(),
        vow_label_str(),
        owner_name_str(),
        bud_time_str(),
        quota_str(),
        celldepth_str(),
    ]
    accord23_str = "accord23"
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [event2, sue_str, accord23_str, sue_str, tp37, sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(mud_file_path, br00001_ex0_str, br00001_1df)

    br3row0 = [event1, sue_str, minute_360, accord23_str, hour6am]
    br3row1 = [event1, sue_str, minute_420, accord23_str, hour7am]
    br3row2 = [event2, sue_str, minute_420, accord23_str, hour7am]
    br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
    br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(mud_file_path, br00003_ex1_str, br00003_1df)
    upsert_sheet(mud_file_path, br00003_ex3_str, br00003_3df)
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        vow_label_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    br00011_rows = [[event2, sue_str, accord23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(mud_file_path, "br00011_ex3", br00011_df)
    mstr_dir = fizz_world._vow_mstr_dir
    wrong_a23_vow_dir = create_path(mstr_dir, accord23_str)
    assert os_path_exists(wrong_a23_vow_dir) is False
    a23_json_path = create_vow_json_path(mstr_dir, accord23_str)
    a23_sue_gut_path = create_gut_path(mstr_dir, accord23_str, sue_str)
    a23_sue_job_path = create_job_path(mstr_dir, accord23_str, sue_str)
    sue37_mandate_path = bud_mandate(mstr_dir, accord23_str, sue_str, tp37)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert os_path_exists(mud_file_path)
        assert not os_path_exists(a23_json_path)
        assert not os_path_exists(a23_sue_gut_path)
        assert not os_path_exists(a23_sue_job_path)
        assert not os_path_exists(sue37_mandate_path)
        assert count_dirs_files(fizz_world.worlds_dir) == 6

        # WHEN
        fizz_world.mud_to_clarity_with_cursor(db_conn, cursor)

        # THEN
        assert os_path_exists(wrong_a23_vow_dir) is False
        assert os_path_exists(mud_file_path)
        assert os_path_exists(a23_json_path)
        assert os_path_exists(a23_sue_gut_path)
        assert os_path_exists(a23_sue_job_path)
        assert os_path_exists(sue37_mandate_path)
        assert count_dirs_files(fizz_world.worlds_dir) == 43


def test_WorldUnit_mud_to_clarity_mstr_Scenario0_CreatesDatabaseFile(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-method
    # ESTABLISH:
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    # delete_dir(fizz_world.worlds_dir)
    sue_str = "Sue"
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        vow_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    a23_str = "accord23"
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [sue_str, e3, a23_str, sue_str, sue_str, sue_str, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(mud_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        event_int_str(),
        face_name_str(),
        vow_label_str(),
        owner_name_str(),
        bud_time_str(),
        quota_str(),
        celldepth_str(),
    ]
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [e3, sue_str, a23_str, sue_str, tp37, sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(mud_file_path, br00001_ex0_str, br00001_1df)
    fizz_db_path = fizz_world.get_db_path()
    assert not os_path_exists(fizz_db_path)

    # WHEN
    fizz_world.mud_to_clarity_mstr()

    # THEN
    assert os_path_exists(fizz_db_path)
    with sqlite3_connect(fizz_db_path) as db_conn:
        br00113_raw = f"{br00113_str}_brick_raw"
        br00113_agg = f"{br00113_str}_brick_agg"
        br00113_valid = f"{br00113_str}_brick_valid"
        events_brick_valid_tablename = events_brick_valid_str()
        pidname_sound_raw = create_prime_tablename("pidname", "s", "raw")
        pidname_sound_agg = create_prime_tablename("pidname", "s", "agg")
        pidname_sound_vld = create_prime_tablename("pidname", "s", "vld")
        pidcore_sound_raw = create_prime_tablename("pidcore", "s", "raw")
        pidcore_sound_agg = create_prime_tablename("pidcore", "s", "agg")
        pidcore_sound_vld = create_prime_tablename("pidcore", "s", "vld")
        vowunit_sound_raw = create_prime_tablename("vowunit", "s", "raw")
        vowunit_sound_agg = create_prime_tablename("vowunit", "s", "agg")
        plnunit_sound_put_raw = create_prime_tablename("planunit", "s", "raw", "put")
        plnunit_sound_put_agg = create_prime_tablename("planunit", "s", "agg", "put")
        plnacct_sound_put_raw = create_prime_tablename("plnacct", "s", "raw", "put")
        plnacct_sound_put_agg = create_prime_tablename("plnacct", "s", "agg", "put")
        vowunit_voice_raw = create_prime_tablename("vowunit", "v", "raw")
        vowunit_voice_agg = create_prime_tablename("vowunit", "v", "agg")
        plnunit_voice_put_raw = create_prime_tablename("planunit", "v", "raw", "put")
        plnunit_voice_put_agg = create_prime_tablename("planunit", "v", "agg", "put")
        plnacct_voice_put_raw = create_prime_tablename("plnacct", "v", "raw", "put")
        plnacct_voice_put_agg = create_prime_tablename("plnacct", "v", "agg", "put")

        cursor = db_conn.cursor()
        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, events_brick_agg_str()) == 2
        assert get_row_count(cursor, events_brick_valid_tablename) == 2
        assert get_row_count(cursor, br00113_valid) == 2
        assert get_row_count(cursor, pidname_sound_raw) == 2
        assert get_row_count(cursor, vowunit_sound_raw) == 4
        assert get_row_count(cursor, plnunit_sound_put_raw) == 4
        assert get_row_count(cursor, plnacct_sound_put_raw) == 2
        assert get_row_count(cursor, pidname_sound_agg) == 1
        assert get_row_count(cursor, vowunit_sound_agg) == 1
        assert get_row_count(cursor, plnunit_sound_put_agg) == 1
        assert get_row_count(cursor, plnacct_sound_put_agg) == 1
        assert get_row_count(cursor, pidcore_sound_raw) == 1
        assert get_row_count(cursor, pidcore_sound_agg) == 1
        assert get_row_count(cursor, pidcore_sound_vld) == 1
        assert get_row_count(cursor, pidname_sound_vld) == 1
        assert get_row_count(cursor, vowunit_voice_raw) == 1
        assert get_row_count(cursor, plnunit_voice_put_raw) == 1
        assert get_row_count(cursor, plnacct_voice_put_raw) == 1
        assert get_row_count(cursor, vowunit_voice_agg) == 1
        assert get_row_count(cursor, plnunit_voice_put_agg) == 1
        assert get_row_count(cursor, plnacct_voice_put_agg) == 1
        assert get_row_count(cursor, vow_ote1_agg_str()) == 1
