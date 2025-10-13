from os.path import exists as os_path_exists
from pandas import DataFrame
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count
from src.ch01_py.file_toolbox import count_dirs_files, create_path, save_file
from src.ch12_pack_file._ref.ch12_path import (
    create_event_all_pack_path,
    create_event_expressed_pack_path as expressed_path,
    create_gut_path,
    create_job_path,
    create_moment_json_path,
)
from src.ch12_pack_file.packfilehandler import open_gut_file
from src.ch15_moment._ref.ch15_path import (
    create_bud_voice_mandate_ledger_path as bud_mandate,
)
from src.ch17_idea.idea_db_tool import upsert_sheet
from src.ch18_world_etl._ref.ch18_path import (
    create_last_run_metrics_path,
    create_moment_ote1_csv_path,
)
from src.ch18_world_etl.tran_sqlstrs import create_prime_tablename as prime_tbl
from src.ch20_world_logic.test._util.ch20_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as worlds_dir,
)
from src.ch20_world_logic.world import worldunit_shop
from src.ref.ch20_keywords import Ch20Keywords as wx


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario0_br000113PopulatesTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_str = "Sue"
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        wx.face_name,
        wx.event_int,
        wx.moment_label,
        wx.belief_name,
        wx.voice_name,
        wx.otx_name,
        wx.inx_name,
    ]
    a23_str = "amy23"
    br00113_str = "br00113"
    br00113row0 = [sue_str, e3, a23_str, sue_str, sue_str, sue_str, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)
    br00113_raw = f"{br00113_str}_brick_raw"
    br00113_agg = f"{br00113_str}_brick_agg"
    br00113_valid = f"{br00113_str}_brick_valid"
    events_brick_valid_tablename = wx.events_brick_valid
    trlname_sound_raw = prime_tbl("trlname", "s", "raw")
    trlname_sound_agg = prime_tbl("trlname", "s", "agg")
    trlname_sound_vld = prime_tbl("trlname", "s", "vld")
    trlcore_sound_raw = prime_tbl("trlcore", "s", "raw")
    trlcore_sound_agg = prime_tbl("trlcore", "s", "agg")
    trlcore_sound_vld = prime_tbl("trlcore", "s", "vld")
    momentunit_sound_raw = prime_tbl("momentunit", "s", "raw")
    momentunit_sound_agg = prime_tbl("momentunit", "s", "agg")
    momentunit_sound_vld = prime_tbl("momentunit", "s", "vld")
    blrunit_sound_put_raw = prime_tbl("beliefunit", "s", "raw", "put")
    blrunit_sound_put_agg = prime_tbl("beliefunit", "s", "agg", "put")
    blrunit_sound_put_vld = prime_tbl("beliefunit", "s", "vld", "put")
    blrpern_sound_put_raw = prime_tbl("blrpern", "s", "raw", "put")
    blrpern_sound_put_agg = prime_tbl("blrpern", "s", "agg", "put")
    blrpern_sound_put_vld = prime_tbl("blrpern", "s", "vld", "put")
    momentunit_heard_raw = prime_tbl("momentunit", "h", "raw")
    momentunit_heard_agg = prime_tbl("momentunit", "h", "agg")
    blrunit_heard_put_raw = prime_tbl("beliefunit", "h", "raw", "put")
    blrunit_heard_put_agg = prime_tbl("beliefunit", "h", "agg", "put")
    blrpern_heard_put_raw = prime_tbl("blrpern", "h", "raw", "put")
    blrpern_heard_put_agg = prime_tbl("blrpern", "h", "agg", "put")
    mstr_dir = fay_world._moment_mstr_dir
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    a23_e1_all_pack_path = create_event_all_pack_path(mstr_dir, a23_str, sue_inx, e3)
    a23_e1_expressed_pack_path = expressed_path(mstr_dir, a23_str, sue_inx, e3)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_str, sue_inx)
    a23_sue_job_path = create_job_path(mstr_dir, a23_str, sue_inx)
    blrpern_job = prime_tbl("blrpern", "job", None)
    last_run_metrics_path = create_last_run_metrics_path(mstr_dir)

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert not db_table_exists(cursor, br00113_raw)
        assert not db_table_exists(cursor, br00113_agg)
        assert not db_table_exists(cursor, wx.events_brick_agg)
        assert not db_table_exists(cursor, events_brick_valid_tablename)
        assert not db_table_exists(cursor, br00113_valid)
        assert not db_table_exists(cursor, trlname_sound_raw)
        assert not db_table_exists(cursor, trlname_sound_agg)
        assert not db_table_exists(cursor, momentunit_sound_raw)
        assert not db_table_exists(cursor, momentunit_sound_agg)
        assert not db_table_exists(cursor, momentunit_sound_vld)
        assert not db_table_exists(cursor, blrunit_sound_put_raw)
        assert not db_table_exists(cursor, blrunit_sound_put_agg)
        assert not db_table_exists(cursor, blrunit_sound_put_vld)
        assert not db_table_exists(cursor, trlcore_sound_raw)
        assert not db_table_exists(cursor, trlcore_sound_agg)
        assert not db_table_exists(cursor, trlcore_sound_vld)
        assert not db_table_exists(cursor, trlname_sound_vld)
        assert not db_table_exists(cursor, momentunit_heard_raw)
        assert not db_table_exists(cursor, momentunit_heard_agg)
        assert not db_table_exists(cursor, blrunit_heard_put_raw)
        assert not db_table_exists(cursor, blrunit_heard_put_agg)
        assert not db_table_exists(cursor, blrpern_heard_put_raw)
        assert not db_table_exists(cursor, blrpern_heard_put_agg)
        assert not os_path_exists(a23_json_path)
        assert not os_path_exists(a23_e1_all_pack_path)
        assert not os_path_exists(a23_e1_expressed_pack_path)
        assert not os_path_exists(a23_sue_gut_path)
        assert not os_path_exists(a23_sue_job_path)
        assert not db_table_exists(cursor, wx.moment_event_time_agg)
        assert not db_table_exists(cursor, wx.moment_ote1_agg)
        assert not db_table_exists(cursor, blrpern_job)
        assert not db_table_exists(cursor, wx.moment_voice_nets)
        assert not db_table_exists(cursor, wx.moment_kpi001_voice_nets)
        assert not os_path_exists(last_run_metrics_path)

        # # create beliefunits
        # self.belief_tables_to_event_belief_csvs(cursor)

        # # create all moment_job and mandate reports
        # self.calc_moment_bud_voice_mandate_net_ledgers()

        # WHEN
        fay_world.sheets_input_to_clarity_with_cursor(cursor)

        # THEN
        # select_translate_core = f"SELECT * FROM {trlcore_sound_vld}"
        # select_beliefunit_put = f"SELECT * FROM {blrunit_sound_put_agg}"
        # select_blrpern_put = f"SELECT * FROM {blrpern_sound_put_agg}"
        # select_momentunit_put_raw = f"SELECT * FROM {momentunit_sound_raw}"
        # select_momentunit_put_agg = f"SELECT * FROM {momentunit_sound_agg}"
        # print(f"{cursor.execute(select_translate_core).fetchall()=}")
        # print(f"{cursor.execute(select_beliefunit_put).fetchall()=}")
        # print(f"{cursor.execute(select_blrpern_put).fetchall()=}")
        # print(f"{cursor.execute(select_momentunit_put_raw).fetchall()=}")
        # print(f"{cursor.execute(select_momentunit_put_agg).fetchall()=}")

        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, wx.events_brick_agg) == 1
        assert get_row_count(cursor, events_brick_valid_tablename) == 1
        assert get_row_count(cursor, br00113_valid) == 1
        assert get_row_count(cursor, trlname_sound_raw) == 1
        assert get_row_count(cursor, momentunit_sound_raw) == 1
        assert get_row_count(cursor, blrunit_sound_put_raw) == 1
        assert get_row_count(cursor, blrpern_sound_put_raw) == 1
        assert get_row_count(cursor, trlname_sound_agg) == 1
        assert get_row_count(cursor, momentunit_sound_agg) == 1
        assert get_row_count(cursor, blrunit_sound_put_agg) == 1
        assert get_row_count(cursor, blrpern_sound_put_agg) == 1
        assert get_row_count(cursor, trlcore_sound_raw) == 1
        assert get_row_count(cursor, trlcore_sound_agg) == 1
        assert get_row_count(cursor, trlcore_sound_vld) == 1
        assert get_row_count(cursor, trlname_sound_vld) == 1
        assert get_row_count(cursor, momentunit_sound_vld) == 1
        assert get_row_count(cursor, blrunit_sound_put_vld) == 1
        assert get_row_count(cursor, blrpern_sound_put_vld) == 1
        assert get_row_count(cursor, momentunit_heard_raw) == 1
        assert get_row_count(cursor, blrunit_heard_put_raw) == 1
        assert get_row_count(cursor, blrpern_heard_put_raw) == 1
        assert get_row_count(cursor, momentunit_heard_agg) == 1
        assert get_row_count(cursor, blrunit_heard_put_agg) == 1
        assert get_row_count(cursor, blrpern_heard_put_agg) == 1
        assert os_path_exists(a23_json_path)
        print(f"{a23_e1_all_pack_path=}")
        assert os_path_exists(a23_e1_all_pack_path)
        assert os_path_exists(a23_e1_expressed_pack_path)
        assert os_path_exists(a23_sue_gut_path)
        sue_gut = open_gut_file(mstr_dir, a23_str, sue_inx)
        time_rope = sue_gut.make_l1_rope(wx.time)
        creg_rope = sue_gut.make_rope(time_rope, wx.creg)
        assert sue_gut.plan_exists(creg_rope)
        assert os_path_exists(a23_sue_job_path)
        assert get_row_count(cursor, blrpern_job) == 1
        assert get_row_count(cursor, wx.moment_voice_nets) == 0
        # assert get_row_count(cursor, wx.moment_event_time_agg) == 0
        # assert get_row_count(cursor, moment_ote1_agg_tablename) == 0
        assert get_row_count(cursor, wx.moment_kpi001_voice_nets) == 0
        assert os_path_exists(last_run_metrics_path)


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario1_PopulateBudPayRows(
    env_dir_setup_cleanup,
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_str = "Sue"
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        wx.face_name,
        wx.event_int,
        wx.moment_label,
        wx.belief_name,
        wx.voice_name,
        wx.otx_name,
        wx.inx_name,
    ]
    a23_str = "amy23"
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [sue_str, e3, a23_str, sue_str, sue_str, sue_str, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        wx.event_int,
        wx.face_name,
        wx.moment_label,
        wx.belief_name,
        wx.bud_time,
        wx.quota,
        wx.celldepth,
    ]
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [e3, sue_str, a23_str, sue_str, tp37, sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)

    # Names of tables
    br00113_raw = f"{br00113_str}_brick_raw"
    br00113_agg = f"{br00113_str}_brick_agg"
    br00113_valid = f"{br00113_str}_brick_valid"
    events_brick_valid_tablename = wx.events_brick_valid
    trlname_sound_raw = prime_tbl("trlname", "s", "raw")
    trlname_sound_agg = prime_tbl("trlname", "s", "agg")
    trlname_sound_vld = prime_tbl("trlname", "s", "vld")
    trlcore_sound_raw = prime_tbl("trlcore", "s", "raw")
    trlcore_sound_agg = prime_tbl("trlcore", "s", "agg")
    trlcore_sound_vld = prime_tbl("trlcore", "s", "vld")
    momentunit_sound_raw = prime_tbl("momentunit", "s", "raw")
    momentunit_sound_agg = prime_tbl("momentunit", "s", "agg")
    blrunit_sound_put_raw = prime_tbl("beliefunit", "s", "raw", "put")
    blrunit_sound_put_agg = prime_tbl("beliefunit", "s", "agg", "put")
    blrpern_sound_put_raw = prime_tbl("blrpern", "s", "raw", "put")
    blrpern_sound_put_agg = prime_tbl("blrpern", "s", "agg", "put")
    momentunit_heard_raw = prime_tbl("momentunit", "h", "raw")
    momentunit_heard_agg = prime_tbl("momentunit", "h", "agg")
    blrunit_heard_put_raw = prime_tbl("beliefunit", "h", "raw", "put")
    blrunit_heard_put_agg = prime_tbl("beliefunit", "h", "agg", "put")
    blrpern_heard_put_raw = prime_tbl("blrpern", "h", "raw", "put")
    blrpern_heard_put_agg = prime_tbl("blrpern", "h", "agg", "put")
    mstr_dir = fay_world._moment_mstr_dir
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    a23_e1_all_pack_path = create_event_all_pack_path(mstr_dir, a23_str, sue_inx, e3)
    a23_e1_expressed_pack_path = expressed_path(mstr_dir, a23_str, sue_inx, e3)
    a23_sue_gut_path = create_gut_path(mstr_dir, a23_str, sue_inx)
    a23_sue_job_path = create_job_path(mstr_dir, a23_str, sue_inx)
    sue37_mandate_path = bud_mandate(mstr_dir, a23_str, sue_inx, tp37)

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert not db_table_exists(cursor, br00113_raw)
        assert not db_table_exists(cursor, br00113_agg)
        assert not db_table_exists(cursor, wx.events_brick_agg)
        assert not db_table_exists(cursor, events_brick_valid_tablename)
        assert not db_table_exists(cursor, br00113_valid)
        assert not db_table_exists(cursor, trlname_sound_raw)
        assert not db_table_exists(cursor, trlname_sound_agg)
        assert not db_table_exists(cursor, momentunit_sound_raw)
        assert not db_table_exists(cursor, momentunit_sound_agg)
        assert not db_table_exists(cursor, blrunit_sound_put_raw)
        assert not db_table_exists(cursor, blrunit_sound_put_agg)
        assert not db_table_exists(cursor, trlcore_sound_raw)
        assert not db_table_exists(cursor, trlcore_sound_agg)
        assert not db_table_exists(cursor, trlcore_sound_vld)
        assert not db_table_exists(cursor, trlname_sound_vld)
        assert not db_table_exists(cursor, momentunit_heard_raw)
        assert not db_table_exists(cursor, momentunit_heard_agg)
        assert not db_table_exists(cursor, blrunit_heard_put_raw)
        assert not db_table_exists(cursor, blrunit_heard_put_agg)
        assert not db_table_exists(cursor, blrpern_heard_put_raw)
        assert not db_table_exists(cursor, blrpern_heard_put_agg)
        assert not os_path_exists(a23_json_path)
        assert not os_path_exists(a23_e1_all_pack_path)
        assert not os_path_exists(a23_e1_expressed_pack_path)
        assert not os_path_exists(a23_sue_gut_path)
        assert not os_path_exists(a23_sue_job_path)
        assert not db_table_exists(cursor, wx.moment_ote1_agg)
        assert not os_path_exists(sue37_mandate_path)
        assert not db_table_exists(cursor, wx.moment_voice_nets)
        assert not db_table_exists(cursor, wx.moment_kpi001_voice_nets)
        # self.moment_agg_tables_to_moment_ote1_agg(cursor)

        # # create beliefunits
        # self.belief_tables_to_event_belief_csvs(cursor)

        # # create all moment_job and mandate reports
        # self.calc_moment_bud_voice_mandate_net_ledgers()

        # WHEN
        fay_world.sheets_input_to_clarity_with_cursor(cursor)

        # THEN
        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        print(cursor.execute(f"SELECT * FROM {wx.events_brick_agg}").fetchall())
        assert get_row_count(cursor, wx.events_brick_agg) == 2
        assert get_row_count(cursor, events_brick_valid_tablename) == 2
        assert get_row_count(cursor, br00113_valid) == 2
        assert get_row_count(cursor, trlname_sound_raw) == 2
        assert get_row_count(cursor, momentunit_sound_raw) == 4
        assert get_row_count(cursor, blrunit_sound_put_raw) == 4
        assert get_row_count(cursor, blrpern_sound_put_raw) == 2
        assert get_row_count(cursor, trlname_sound_agg) == 1
        assert get_row_count(cursor, momentunit_sound_agg) == 1
        assert get_row_count(cursor, blrunit_sound_put_agg) == 1
        assert get_row_count(cursor, blrpern_sound_put_agg) == 1
        assert get_row_count(cursor, trlcore_sound_raw) == 1
        assert get_row_count(cursor, trlcore_sound_agg) == 1
        assert get_row_count(cursor, trlcore_sound_vld) == 1
        assert get_row_count(cursor, trlname_sound_vld) == 1
        assert get_row_count(cursor, momentunit_heard_raw) == 1
        assert get_row_count(cursor, blrunit_heard_put_raw) == 1
        assert get_row_count(cursor, blrpern_heard_put_raw) == 1
        assert get_row_count(cursor, momentunit_heard_agg) == 1
        assert get_row_count(cursor, blrunit_heard_put_agg) == 1
        assert get_row_count(cursor, blrpern_heard_put_agg) == 1
        assert os_path_exists(a23_json_path)
        assert os_path_exists(a23_e1_all_pack_path)
        assert os_path_exists(a23_e1_expressed_pack_path)
        assert os_path_exists(a23_sue_gut_path)
        assert os_path_exists(a23_sue_job_path)
        assert get_row_count(cursor, wx.moment_ote1_agg) == 1
        print(f"{sue37_mandate_path=}")
        assert os_path_exists(sue37_mandate_path)
        assert get_row_count(cursor, wx.moment_voice_nets) == 1
        assert get_row_count(cursor, wx.moment_kpi001_voice_nets) == 1


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario2_PopulateMomentTranBook(
    env_dir_setup_cleanup,
):
    # ESTABLISH:
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00002_columns = [
        wx.event_int,
        wx.face_name,
        wx.moment_label,
        wx.belief_name,
        wx.voice_name,
        wx.tran_time,
        wx.amount,
    ]
    a23_str = "amy23"
    br00002_str = "br00002"
    tp37 = 37
    sue_to_bob_amount = 200
    br00002row0 = [e3, sue_str, a23_str, sue_str, bob_str, tp37, sue_to_bob_amount]
    br00002_df = DataFrame([br00002row0], columns=br00002_columns)
    br00002_ex0_str = f"example0_{br00002_str}"
    upsert_sheet(input_file_path, br00002_ex0_str, br00002_df)

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert not db_table_exists(cursor, wx.moment_voice_nets)

        # WHEN
        fay_world.sheets_input_to_clarity_with_cursor(cursor)

        # THEN
        assert get_row_count(cursor, wx.moment_voice_nets) == 1


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario3_WhenNoMomentIdeas_ote1_IsStillCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    sue_str = "Sue"
    event2 = 2
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    amy23_str = "amy23"
    br00011_columns = [
        wx.event_int,
        wx.face_name,
        wx.moment_label,
        wx.belief_name,
        wx.voice_name,
    ]
    br00011_rows = [[event2, sue_str, amy23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    moment_mstr = fay_world._moment_mstr_dir
    a23_ote1_csv_path = create_moment_ote1_csv_path(moment_mstr, amy23_str)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert os_path_exists(a23_ote1_csv_path) is False

        # WHEN
        fay_world.sheets_input_to_clarity_with_cursor(cursor)

    # THEN
    assert os_path_exists(a23_ote1_csv_path)


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario4_DeletesPreviousFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    print(f"{fay_world.worlds_dir=}")
    mstr_dir = fay_world._moment_mstr_dir
    moments_dir = create_path(mstr_dir, "moments")
    testing2_filename = "testing2.txt"
    testing3_filename = "testing3.txt"
    save_file(fay_world.worlds_dir, testing2_filename, "")
    save_file(moments_dir, testing3_filename, "")
    testing2_path = create_path(fay_world.worlds_dir, testing2_filename)
    testing3_path = create_path(moments_dir, testing3_filename)
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path)
    print(f"{testing3_path=}")
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()

        # WHEN
        fay_world.sheets_input_to_clarity_with_cursor(cursor)

    # THEN
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path) is False


def test_WorldUnit_sheets_input_to_clarity_with_cursor_Scenario5_CreatesFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00003_columns = [
        wx.event_int,
        wx.face_name,
        wx.cumulative_minute,
        wx.moment_label,
        wx.hour_label,
    ]
    br00001_columns = [
        wx.event_int,
        wx.face_name,
        wx.moment_label,
        wx.belief_name,
        wx.bud_time,
        wx.quota,
        wx.celldepth,
    ]
    amy23_str = "amy23"
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [event2, sue_str, amy23_str, sue_str, tp37, sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)

    br3row0 = [event1, sue_str, minute_360, amy23_str, hour6am]
    br3row1 = [event1, sue_str, minute_420, amy23_str, hour7am]
    br3row2 = [event2, sue_str, minute_420, amy23_str, hour7am]
    br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
    br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(input_file_path, br00003_ex1_str, br00003_1df)
    upsert_sheet(input_file_path, br00003_ex3_str, br00003_3df)
    br00011_columns = [
        wx.event_int,
        wx.face_name,
        wx.moment_label,
        wx.belief_name,
        wx.voice_name,
    ]
    br00011_rows = [[event2, sue_str, amy23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    mstr_dir = fay_world._moment_mstr_dir
    wrong_a23_moment_dir = create_path(mstr_dir, amy23_str)
    assert os_path_exists(wrong_a23_moment_dir) is False
    a23_json_path = create_moment_json_path(mstr_dir, amy23_str)
    a23_sue_gut_path = create_gut_path(mstr_dir, amy23_str, sue_str)
    a23_sue_job_path = create_job_path(mstr_dir, amy23_str, sue_str)
    sue37_mandate_path = bud_mandate(mstr_dir, amy23_str, sue_str, tp37)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        assert os_path_exists(input_file_path)
        assert not os_path_exists(a23_json_path)
        assert not os_path_exists(a23_sue_gut_path)
        assert not os_path_exists(a23_sue_job_path)
        assert not os_path_exists(sue37_mandate_path)
        assert count_dirs_files(fay_world.worlds_dir) == 5

        # WHEN
        fay_world.sheets_input_to_clarity_with_cursor(cursor)

        # THEN
        assert os_path_exists(wrong_a23_moment_dir) is False
        assert os_path_exists(input_file_path)
        assert os_path_exists(a23_json_path)
        assert os_path_exists(a23_sue_gut_path)
        assert os_path_exists(a23_sue_job_path)
        assert os_path_exists(sue37_mandate_path)
        assert count_dirs_files(fay_world.worlds_dir) == 42


def test_WorldUnit_sheets_input_to_clarity_mstr_Scenario0_CreatesDatabaseFile(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-method
    # ESTABLISH:
    fay_str = "Fay"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_str = "Sue"
    sue_inx = "Suzy"
    e3 = 3
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        wx.face_name,
        wx.event_int,
        wx.moment_label,
        wx.belief_name,
        wx.voice_name,
        wx.otx_name,
        wx.inx_name,
    ]
    a23_str = "amy23"
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [sue_str, e3, a23_str, sue_str, sue_str, sue_str, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        wx.event_int,
        wx.face_name,
        wx.moment_label,
        wx.belief_name,
        wx.bud_time,
        wx.quota,
        wx.celldepth,
    ]
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [e3, sue_str, a23_str, sue_str, tp37, sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)
    fay_db_path = fay_world.get_world_db_path()
    assert not os_path_exists(fay_db_path)

    # WHEN
    fay_world.sheets_input_to_clarity_mstr()

    # THEN
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn:
        br00113_raw = f"{br00113_str}_brick_raw"
        br00113_agg = f"{br00113_str}_brick_agg"
        br00113_valid = f"{br00113_str}_brick_valid"
        events_brick_valid_tablename = wx.events_brick_valid
        trlname_sound_raw = prime_tbl("trlname", "s", "raw")
        trlname_sound_agg = prime_tbl("trlname", "s", "agg")
        trlname_sound_vld = prime_tbl("trlname", "s", "vld")
        trlcore_sound_raw = prime_tbl("trlcore", "s", "raw")
        trlcore_sound_agg = prime_tbl("trlcore", "s", "agg")
        trlcore_sound_vld = prime_tbl("trlcore", "s", "vld")
        momentunit_sound_raw = prime_tbl("momentunit", "s", "raw")
        momentunit_sound_agg = prime_tbl("momentunit", "s", "agg")
        blrunit_sound_put_raw = prime_tbl("beliefunit", "s", "raw", "put")
        blrunit_sound_put_agg = prime_tbl("beliefunit", "s", "agg", "put")
        blrpern_sound_put_raw = prime_tbl("blrpern", "s", "raw", "put")
        blrpern_sound_put_agg = prime_tbl("blrpern", "s", "agg", "put")
        momentunit_heard_raw = prime_tbl("momentunit", "h", "raw")
        momentunit_heard_agg = prime_tbl("momentunit", "h", "agg")
        blrunit_heard_put_raw = prime_tbl("beliefunit", "h", "raw", "put")
        blrunit_heard_put_agg = prime_tbl("beliefunit", "h", "agg", "put")
        blrpern_heard_put_raw = prime_tbl("blrpern", "h", "raw", "put")
        blrpern_heard_put_agg = prime_tbl("blrpern", "h", "agg", "put")

        cursor = db_conn.cursor()
        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, wx.events_brick_agg) == 2
        assert get_row_count(cursor, events_brick_valid_tablename) == 2
        assert get_row_count(cursor, br00113_valid) == 2
        assert get_row_count(cursor, trlname_sound_raw) == 2
        assert get_row_count(cursor, momentunit_sound_raw) == 4
        assert get_row_count(cursor, blrunit_sound_put_raw) == 4
        assert get_row_count(cursor, blrpern_sound_put_raw) == 2
        assert get_row_count(cursor, trlname_sound_agg) == 1
        assert get_row_count(cursor, momentunit_sound_agg) == 1
        assert get_row_count(cursor, blrunit_sound_put_agg) == 1
        assert get_row_count(cursor, blrpern_sound_put_agg) == 1
        assert get_row_count(cursor, trlcore_sound_raw) == 1
        assert get_row_count(cursor, trlcore_sound_agg) == 1
        assert get_row_count(cursor, trlcore_sound_vld) == 1
        assert get_row_count(cursor, trlname_sound_vld) == 1
        assert get_row_count(cursor, momentunit_heard_raw) == 1
        assert get_row_count(cursor, blrunit_heard_put_raw) == 1
        assert get_row_count(cursor, blrpern_heard_put_raw) == 1
        assert get_row_count(cursor, momentunit_heard_agg) == 1
        assert get_row_count(cursor, blrunit_heard_put_agg) == 1
        assert get_row_count(cursor, blrpern_heard_put_agg) == 1
        assert get_row_count(cursor, wx.moment_ote1_agg) == 1
    db_conn.close()
