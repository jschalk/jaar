from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet, forge_staging_str
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_mine_to_forge_staging_CreatesZooFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    event_1 = 1
    event_2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    mine_file_path = create_path(fizz_world._mine_dir, ex_file_name)
    forge_file_path = create_path(fizz_world._forge_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        event_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
        hour_label_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event_1, minute_360, music23_str, hour6am]
    row2 = [sue_str, event_1, minute_420, music23_str, hour7am]
    row3 = [sue_str, event_2, minute_420, music23_str, hour7am]
    incomplete_brick_columns = [
        face_id_str(),
        event_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
    ]
    incom_row1 = [sue_str, event_1, minute_360, music23_str]
    incom_row2 = [sue_str, event_1, minute_420, music23_str]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_brick_columns)
    df3 = DataFrame([row2, row1, row3], columns=brick_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(mine_file_path, br00003_ex1_str, df1)
    upsert_sheet(mine_file_path, br00003_ex2_str, df2)
    upsert_sheet(mine_file_path, br00003_ex3_str, df3)
    assert os_path_exists(forge_file_path) is False

    # WHEN
    fizz_world.mine_to_forge_staging()

    # THEN
    print(f"{forge_file_path=}")
    assert os_path_exists(forge_file_path)
    x_df = pandas_read_excel(forge_file_path, sheet_name=forge_staging_str())
    assert set(brick_columns).issubset(set(x_df.columns))
    file_dir_str = "file_dir"
    file_name_str = "file_name"
    sheet_name_str = "sheet_name"
    assert file_dir_str in set(x_df.columns)
    assert file_name_str in set(x_df.columns)
    assert sheet_name_str in set(x_df.columns)
    assert len(x_df) == 5
    assert get_sheet_names(forge_file_path) == [forge_staging_str()]
