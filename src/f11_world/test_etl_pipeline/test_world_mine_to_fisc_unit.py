from src.f00_instrument.file import create_path, count_dirs_files, delete_dir, save_file
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f04_gift.atom_config import face_name_str, event_int_str, acct_name_str
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_forecast_path,
    create_voice_path,
)
from src.f07_fisc.fisc_config import cumlative_minute_str, hour_title_str
from src.f09_idea.idea_db_tool import upsert_sheet
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from pandas import DataFrame
from os.path import exists as os_path_exists


def test_WorldUnit_mine_to_forecasts_DeletesPreviousFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    print(f"{fizz_world.worlds_dir=}")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    testing2_filename = "testing2.txt"
    testing3_filename = "testing3.txt"
    save_file(fizz_world.worlds_dir, testing2_filename, "")
    save_file(fiscs_dir, testing3_filename, "")
    testing2_path = create_path(fizz_world.worlds_dir, testing2_filename)
    testing3_path = create_path(fiscs_dir, testing3_filename)
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path)
    print(f"{testing3_path=}")
    assert count_dirs_files(fizz_world.worlds_dir) == 9

    # WHEN
    fizz_world.mine_to_forecasts()

    # THEN
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path) is False
    assert count_dirs_files(fizz_world.worlds_dir) == 27


# TODO add deal to
def test_WorldUnit_mine_to_forecasts_CreatesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    # delete_dir(fizz_world.worlds_dir)
    sue_str = "Sue"
    event_1 = 1
    event_2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    mine_file_path = create_path(fizz_world._mine_dir, ex_filename)
    br00003_columns = [
        face_name_str(),
        event_int_str(),
        cumlative_minute_str(),
        fisc_title_str(),
        hour_title_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, minute_360, accord23_str, hour6am]
    row2 = [sue_str, event_1, minute_420, accord23_str, hour7am]
    row3 = [sue_str, event_2, minute_420, accord23_str, hour7am]
    df1 = DataFrame([row1, row2], columns=br00003_columns)
    df3 = DataFrame([row2, row1, row3], columns=br00003_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(mine_file_path, br00003_ex1_str, df1)
    upsert_sheet(mine_file_path, br00003_ex3_str, df3)
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
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    wrong_a23_fisc_dir = create_path(fisc_mstr_dir, accord23_str)
    assert os_path_exists(wrong_a23_fisc_dir) is False
    a23_json_path = create_fisc_json_path(fisc_mstr_dir, accord23_str)
    a23_sue_voice_path = create_voice_path(fisc_mstr_dir, accord23_str, sue_str)
    a23_sue_forecast_path = create_forecast_path(fisc_mstr_dir, accord23_str, sue_str)
    assert os_path_exists(mine_file_path)
    assert os_path_exists(a23_json_path) is False
    assert os_path_exists(a23_sue_voice_path) is False
    assert os_path_exists(a23_sue_forecast_path) is False
    assert count_dirs_files(fizz_world.worlds_dir) == 7

    # WHEN
    fizz_world.mine_to_forecasts()

    # THEN
    assert os_path_exists(wrong_a23_fisc_dir) is False
    train_file_path = create_path(fizz_world._train_dir, "br00003.xlsx")
    assert os_path_exists(mine_file_path)
    assert os_path_exists(train_file_path)
    assert os_path_exists(a23_json_path)
    assert os_path_exists(a23_sue_voice_path)
    assert os_path_exists(a23_sue_forecast_path)
    assert count_dirs_files(fizz_world.worlds_dir) == 67


# def test_WorldUnit_mine_to_forecasts_CreatestrainFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_str = "fizz"
#     fizz_world = worldunit_shop(fizz_str)
#     delete_dir(fizz_world.worlds_dir)
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
#     accord23_str = "accord23"
#     row1 = [sue_str, event_1, minute_360, accord23_str, hour6am]
#     row2 = [sue_str, event_1, minute_420, accord23_str, hour7am]
#     row3 = [sue_str, event_2, minute_420, accord23_str, hour7am]
#     df1 = DataFrame([row1, row2], columns=br00003_columns)
#     df3 = DataFrame([row2, row1, row3], columns=br00003_columns)
#     br00003_ex1_str = "example1_br00003"
#     br00003_ex3_str = "example3_br00003"
#     upsert_sheet(mine_file_path, br00003_ex1_str, df1)
#     upsert_sheet(mine_file_path, br00003_ex3_str, df3)
#     br00011_columns = [
#         face_name_str(),
#         event_int_str(),
#         "fisc_title",
#         "owner_name",
#         "acct_name",
#     ]
#     br00011_rows = [[sue_str, event_2, accord23_str, sue_str, sue_str]]
#     br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
#     upsert_sheet(mine_file_path, "br00011_ex3", br00011_df)
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
#     a23_json_path = create_fisc_json_path(fisc_mstr_dir, accord23_str)
#     a23_sue_voice_path = create_voice_path(fiscs_dir, accord23_str, sue_str)
#     a23_sue_forecast_path = create_forecast_path(fiscs_dir, accord23_str, sue_str)
#     assert os_path_exists(mine_file_path)
#     assert os_path_exists(a23_json_path) is False
#     assert os_path_exists(a23_sue_voice_path) is False
#     assert os_path_exists(a23_sue_forecast_path) is False

#     # WHEN
#     fizz_world.mine_to_forecasts()

#     # THEN
#     train_file_path = create_path(fizz_world._train_dir, "br00003.xlsx")
#     assert os_path_exists(mine_file_path)
#     assert os_path_exists(train_file_path)
#     assert os_path_exists(a23_json_path)
#     assert os_path_exists(a23_sue_voice_path)
#     assert os_path_exists(a23_sue_forecast_path)
