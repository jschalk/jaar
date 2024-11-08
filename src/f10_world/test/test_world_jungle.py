from src.f00_instrument.file import create_file_path, create_dir
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_filter.filter_config import eon_id_str
from src.f10_world.world import worldunit_shop, WorldUnit
from src.f10_world.world_tool import get_all_brick_dataframes
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, ExcelWriter, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_jungle_to_zoo_CreatesZooFiles(env_dir_setup_cleanup):
    # ESTABLISH
    music23_str = "music23"
    music_world = worldunit_shop(music23_str)
    sue_str = "Sue"
    eon_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    jungle_file_path = create_file_path(music_world._jungle_dir, ex_file_name)
    zoo_file_path = create_file_path(music_world._zoo_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        eon_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
        hour_label_str(),
    ]
    row1 = [sue_str, eon_1, minute_360, music23_str, hour6am]
    row2 = [sue_str, eon_1, minute_420, music23_str, hour7am]
    incomplete_brick_columns = [
        face_id_str(),
        eon_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
    ]
    incom_row1 = [sue_str, eon_1, minute_360, music23_str]
    incom_row2 = [sue_str, eon_1, minute_420, music23_str]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_brick_columns)
    df3 = DataFrame([row2, row1], columns=brick_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name=br00003_ex1_str, index=False)
        df2.to_excel(writer, sheet_name=br00003_ex2_str, index=False)
        df3.to_excel(writer, sheet_name=br00003_ex3_str, index=False)
    assert os_path_exists(zoo_file_path) is False

    # WHEN
    music_world.jungle_to_zoo()

    # THEN
    print(f"{zoo_file_path=}")
    assert os_path_exists(zoo_file_path)
    df = pandas_read_excel(zoo_file_path, sheet_name="br00003")
    assert set(brick_columns).issubset(set(df.columns))
    file_dir_str = "file_dir"
    file_name_str = "file_name"
    sheet_name_str = "sheet_name"
    assert file_dir_str in set(df.columns)
    assert file_name_str in set(df.columns)
    assert sheet_name_str in set(df.columns)
