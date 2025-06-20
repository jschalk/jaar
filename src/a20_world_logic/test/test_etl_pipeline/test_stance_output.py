from os.path import exists as os_path_exists
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal
from shutil import copy2 as shutil_copy2
from src.a00_data_toolbox.file_toolbox import create_path, set_dir
from src.a02_finance_logic.test._util.a02_str import owner_name_str, vow_label_str
from src.a06_plan_logic.test._util.a06_str import acct_name_str
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a17_idea_logic.idea_db_tool import get_sheet_names, upsert_sheet
from src.a18_etl_toolbox.tran_path import (
    create_stance0001_path,
    create_stances_dir_path,
)
from src.a20_world_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.a20_world_logic.world import worldunit_shop


def test_WorldUnit_create_stances_Senario0_EmptyWorld_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    fizz_world.mud_to_clarity_mstr()
    fizz_stance0001_path = create_stance0001_path(fizz_world._vow_mstr_dir)
    assert os_path_exists(fizz_stance0001_path) is False

    # WHEN
    fizz_world.create_stances()

    # THEN
    assert os_path_exists(fizz_stance0001_path)


def test_WorldUnit_create_stances_Senario1_Add_CreatesFile(env_dir_setup_cleanup):
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
    fizz_world.mud_to_clarity_mstr()
    fizz_stance0001_path = create_stance0001_path(fizz_world._vow_mstr_dir)
    assert os_path_exists(fizz_stance0001_path) is False

    # WHEN
    fizz_world.create_stances()

    # THEN
    assert os_path_exists(fizz_stance0001_path)


def test_WorldUnit_create_stances_Senario2_CreatedStanceCanBeIdeasForOtherWorldUnit(
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
    fizz_world.mud_to_clarity_mstr()
    fizz_stance0001_path = create_stance0001_path(fizz_world._vow_mstr_dir)
    fizz_world.create_stances()
    buzz_world = worldunit_shop("buzz", worlds_dir())
    buzz_mud_st0001_path = create_path(buzz_world._vow_mstr_dir, "buzz_mud.xlsx")
    set_dir(create_stances_dir_path(buzz_world._vow_mstr_dir))
    shutil_copy2(fizz_stance0001_path, dst=buzz_mud_st0001_path)
    # print(f" {pandas_read_excel(fizz_stance0001_path)=}")
    # print(f"{pandas_read_excel(buzz_mud_st0001_path)=}")
    print(f"{buzz_mud_st0001_path=}")
    print(f"{get_sheet_names(buzz_mud_st0001_path)=}")
    buzz_world.mud_to_clarity_mstr()
    buzz_stance0001_path = create_stance0001_path(buzz_world._vow_mstr_dir)
    assert os_path_exists(buzz_stance0001_path) is False

    # WHEN
    buzz_world.create_stances()

    # THEN
    assert os_path_exists(buzz_stance0001_path)
    print(f"{get_sheet_names(buzz_stance0001_path)=}")
    for sheetname in get_sheet_names(buzz_stance0001_path):
        print(f"comparing {sheetname=}...")
        fizz_sheet_df = pandas_read_excel(fizz_stance0001_path, sheetname)
        buzz_sheet_df = pandas_read_excel(fizz_stance0001_path, sheetname)
        # if sheetname == "br00021":
        #     print(f"{fizz_sheet_df=}")
        #     print(f"{buzz_sheet_df=}")
        assert_frame_equal(fizz_sheet_df, buzz_sheet_df)


# def test_WorldUnit_mud_to_clarity_CreatesFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_str = "fizz"
#     fizz_world = worldunit_shop(fizz_str, worlds_dir())
#     # delete_dir(fizz_world.worlds_dir)
#     sue_str = "Sue"
#     event1 = 1
#     event2 = 2
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "fizzbuzz.xlsx"
#     mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
#     br00003_columns = [
#         face_name_str(),
#         event_int_str(),
#         cumulative_minute_str(),
#         vow_label_str(),
#         hour_label_str(),
#     ]
#     br00001_columns = [
#         face_name_str(),
#         event_int_str(),
#         vow_label_str(),
#         owner_name_str(),
#         bud_time(),
#         quota_str(),
#         celldepth_str(),
#     ]
#     accord23_str = "accord23"
#     tp37 = 37
#     sue_quota = 235
#     sue_celldepth = 3
#     br1row0 = [event2, sue_str, accord23_str, sue_str, tp37, sue_quota, sue_celldepth]
#     br00001_1df = DataFrame([br1row0], columns=br00001_columns)
#     br00001_ex0_str = "example0_br00001"
#     upsert_sheet(mud_file_path, br00001_ex0_str, br00001_1df)

#     br3row0 = [event1, sue_str,  minute_360, accord23_str, hour6am]
#     br3row1 = [event1, sue_str,  minute_420, accord23_str, hour7am]
#     br3row2 = [event2, sue_str, minute_420, accord23_str, hour7am]
#     br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
#     br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
#     br00003_ex1_str = "example1_br00003"
#     br00003_ex3_str = "example3_br00003"
#     upsert_sheet(mud_file_path, br00003_ex1_str, br00003_1df)
#     upsert_sheet(mud_file_path, br00003_ex3_str, br00003_3df)
#     br00011_columns = [
#         face_name_str(),
#         event_int_str(),
#         vow_label_str(),
#         owner_name_str(),
#         acct_name_str(),
#     ]
#     br00011_rows = [[event2, sue_str, accord23_str, sue_str, sue_str]]
#     br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
#     upsert_sheet(mud_file_path, "br00011_ex3", br00011_df)
#     mstr_dir = fizz_world._vow_mstr_dir
#     wrong_a23_vow_dir = create_path(mstr_dir, accord23_str)
#     assert os_path_exists(wrong_a23_vow_dir) is False
#     a23_json_path = create_vow_json_path(mstr_dir, accord23_str)
#     a23_sue_gut_path = create_gut_path(mstr_dir, accord23_str, sue_str)
#     a23_sue_job_path = create_job_path(mstr_dir, accord23_str, sue_str)
#     sue37_mandate_path = bud_mandate(mstr_dir, accord23_str, sue_str, tp37)
#     assert os_path_exists(mud_file_path)
#     assert os_path_exists(a23_json_path) is False
#     assert os_path_exists(a23_sue_gut_path) is False
#     assert os_path_exists(a23_sue_job_path) is False
#     assert os_path_exists(sue37_mandate_path) is False
#     assert count_dirs_files(fizz_world.worlds_dir) == 7

#     # WHEN
#     fizz_world.mud_to_clarity_mstr()

#     # THEN
#     assert os_path_exists(wrong_a23_vow_dir) is False
#     brick_file_path = create_path(fizz_world._brick_dir, "br00003.xlsx")
#     assert os_path_exists(mud_file_path)
#     assert os_path_exists(brick_file_path)
#     assert os_path_exists(a23_json_path)
#     assert os_path_exists(a23_sue_gut_path)
#     assert os_path_exists(a23_sue_job_path)
#     assert os_path_exists(sue37_mandate_path)
#     assert count_dirs_files(fizz_world.worlds_dir) == 91
