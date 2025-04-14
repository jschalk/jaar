from src.a00_data_toolboxs.file_toolbox import create_path
from src.a02_finance_toolboxs.deal import fisc_title_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.f08_fisc.fisc_config import cumlative_minute_str, hour_title_str
from src.f10_idea.idea_db_tool import get_sheet_names, upsert_sheet, cart_staging_str
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_mine_to_cart_staging_CreatescartFiles(env_dir_setup_cleanup):
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
    ex_filename = "fizzbuzz.xlsx"
    mine_file_path = create_path(fizz_world._mine_dir, ex_filename)
    cart_file_path = create_path(fizz_world._cart_dir, "br00003.xlsx")
    idea_columns = [
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
    incomplete_idea_columns = [
        face_name_str(),
        event_int_str(),
        cumlative_minute_str(),
        fisc_title_str(),
    ]
    incom_row1 = [sue_str, event_1, minute_360, accord23_str]
    incom_row2 = [sue_str, event_1, minute_420, accord23_str]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_idea_columns)
    df3 = DataFrame([row2, row1, row3], columns=idea_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(mine_file_path, br00003_ex1_str, df1)
    upsert_sheet(mine_file_path, br00003_ex2_str, df2)
    upsert_sheet(mine_file_path, br00003_ex3_str, df3)
    assert os_path_exists(cart_file_path) is False

    # WHEN
    fizz_world.mine_to_cart_staging()

    # THEN
    print(f"{cart_file_path=}")
    assert os_path_exists(cart_file_path)
    x_df = pandas_read_excel(cart_file_path, sheet_name=cart_staging_str())
    assert set(idea_columns).issubset(set(x_df.columns))
    file_dir_str = "file_dir"
    filename_str = "filename"
    sheet_name_str = "sheet_name"
    assert file_dir_str in set(x_df.columns)
    assert filename_str in set(x_df.columns)
    assert sheet_name_str in set(x_df.columns)
    assert len(x_df) == 5
    assert get_sheet_names(cart_file_path) == [cart_staging_str()]
