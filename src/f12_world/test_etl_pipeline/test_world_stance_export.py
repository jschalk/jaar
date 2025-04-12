from src.f00_instrument.file import create_path, set_dir
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f04_kick.atom_config import face_name_str, event_int_str, acct_name_str
from src.f10_idea.idea_db_tool import upsert_sheet, get_sheet_names
from src.f11_etl.tran_path import create_stances_dir_path, create_stance0001_path
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal
from os.path import exists as os_path_exists
from shutil import copy2 as shutil_copy2


def test_WorldUnit_create_stances_Senario0_EmptyWorld_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    fizz_world.mine_to_burdens()
    fizz_stance0001_path = create_stance0001_path(fizz_world._fisc_mstr_dir)
    assert os_path_exists(fizz_stance0001_path) is False

    # WHEN
    fizz_world.create_stances()

    # THEN
    assert os_path_exists(fizz_stance0001_path)


def test_WorldUnit_create_stances_Senario1_Add_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    event_2 = 2
    ex_filename = "fizzbuzz.xlsx"
    mine_file_path = create_path(fizz_world._mine_dir, ex_filename)
    accord23_str = "accord23"
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    br00011_rows = [[sue_str, event_2, accord23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(mine_file_path, "br00011_ex3", br00011_df)
    fizz_world.mine_to_burdens()
    fizz_stance0001_path = create_stance0001_path(fizz_world._fisc_mstr_dir)
    assert os_path_exists(fizz_stance0001_path) is False

    # WHEN
    fizz_world.create_stances()

    # THEN
    assert os_path_exists(fizz_stance0001_path)


def test_WorldUnit_create_stances_Senario2_CreatedStanceCanBeMinedByOtherWorldUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    event_2 = 2
    ex_filename = "fizzbuzz.xlsx"
    mine_file_path = create_path(fizz_world._mine_dir, ex_filename)
    accord23_str = "accord23"
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    br00011_rows = [[sue_str, event_2, accord23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(mine_file_path, "br00011_ex3", br00011_df)
    fizz_world.mine_to_burdens()
    fizz_stance0001_path = create_stance0001_path(fizz_world._fisc_mstr_dir)
    fizz_world.create_stances()
    buzz_world = worldunit_shop("buzz")
    buzz_mine_st0001_path = create_path(buzz_world._fisc_mstr_dir, "buzz_mine.xlsx")
    set_dir(create_stances_dir_path(buzz_world._fisc_mstr_dir))
    shutil_copy2(fizz_stance0001_path, dst=buzz_mine_st0001_path)
    # print(f" {pandas_read_excel(fizz_stance0001_path)=}")
    # print(f"{pandas_read_excel(buzz_mine_st0001_path)=}")
    print(f"{buzz_mine_st0001_path=}")
    print(f"{get_sheet_names(buzz_mine_st0001_path)=}")
    buzz_world.mine_to_burdens()
    buzz_stance0001_path = create_stance0001_path(buzz_world._fisc_mstr_dir)
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


# def test_WorldUnit_mine_to_burdens_CreatesFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_str = "fizz"
#     fizz_world = worldunit_shop(fizz_str)
#     # delete_dir(fizz_world.worlds_dir)
#     sue_str = "Sue"
#     event_1 = 1
#     event_2 = 2
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "fizzbuzz.xlsx"
#     mine_file_path = create_path(fizz_world._mine_dir, ex_filename)
#     br00003_columns = [
#         face_name_str(),
#         event_int_str(),
#         cumlative_minute_str(),
#         fisc_title_str(),
#         hour_title_str(),
#     ]
#     br00001_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_title_str(),
#         owner_name_str(),
#         deal_time(),
#         quota_str(),
#         celldepth_str(),
#     ]
#     accord23_str = "accord23"
#     tp37 = 37
#     sue_quota = 235
#     sue_celldepth = 3
#     br1row0 = [sue_str, event_2, accord23_str, sue_str, tp37, sue_quota, sue_celldepth]
#     br00001_1df = DataFrame([br1row0], columns=br00001_columns)
#     br00001_ex0_str = "example0_br00001"
#     upsert_sheet(mine_file_path, br00001_ex0_str, br00001_1df)

#     br3row0 = [sue_str, event_1, minute_360, accord23_str, hour6am]
#     br3row1 = [sue_str, event_1, minute_420, accord23_str, hour7am]
#     br3row2 = [sue_str, event_2, minute_420, accord23_str, hour7am]
#     br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
#     br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
#     br00003_ex1_str = "example1_br00003"
#     br00003_ex3_str = "example3_br00003"
#     upsert_sheet(mine_file_path, br00003_ex1_str, br00003_1df)
#     upsert_sheet(mine_file_path, br00003_ex3_str, br00003_3df)
#     br00011_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#     ]
#     br00011_rows = [[sue_str, event_2, accord23_str, sue_str, sue_str]]
#     br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
#     upsert_sheet(mine_file_path, "br00011_ex3", br00011_df)
#     mstr_dir = fizz_world._fisc_mstr_dir
#     wrong_a23_fisc_dir = create_path(mstr_dir, accord23_str)
#     assert os_path_exists(wrong_a23_fisc_dir) is False
#     a23_json_path = create_fisc_json_path(mstr_dir, accord23_str)
#     a23_sue_voice_path = create_voice_path(mstr_dir, accord23_str, sue_str)
#     a23_sue_plan_path = create_plan_path(mstr_dir, accord23_str, sue_str)
#     sue37_mandate_path = deal_mandate(mstr_dir, accord23_str, sue_str, tp37)
#     assert os_path_exists(mine_file_path)
#     assert os_path_exists(a23_json_path) is False
#     assert os_path_exists(a23_sue_voice_path) is False
#     assert os_path_exists(a23_sue_plan_path) is False
#     assert os_path_exists(sue37_mandate_path) is False
#     assert count_dirs_files(fizz_world.worlds_dir) == 7

#     # WHEN
#     fizz_world.mine_to_burdens()

#     # THEN
#     assert os_path_exists(wrong_a23_fisc_dir) is False
#     cart_file_path = create_path(fizz_world._cart_dir, "br00003.xlsx")
#     assert os_path_exists(mine_file_path)
#     assert os_path_exists(cart_file_path)
#     assert os_path_exists(a23_json_path)
#     assert os_path_exists(a23_sue_voice_path)
#     assert os_path_exists(a23_sue_plan_path)
#     assert os_path_exists(sue37_mandate_path)
#     assert count_dirs_files(fizz_world.worlds_dir) == 91
