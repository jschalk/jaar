from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_name_str, gov_idea_str
from src.f07_gov.gov_config import cumlative_minute_str, hour_idea_str
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet, boat_staging_str
from src.f10_etl.transformers import etl_ocean_to_boat_staging
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_ocean_to_boat_staging_CreatesboatFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
    event_2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    ocean_dir = create_path(get_test_etl_dir(), "ocean")
    boat_dir = create_path(get_test_etl_dir(), "boat")
    ocean_file_path = create_path(ocean_dir, ex_file_name)
    brick_columns = [
        face_name_str(),
        event_int_str(),
        cumlative_minute_str(),
        gov_idea_str(),
        hour_idea_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, minute_360, accord23_str, hour6am]
    row2 = [sue_str, event_1, minute_420, accord23_str, hour7am]
    row3 = [sue_str, event_2, minute_420, accord23_str, hour7am]
    incomplete_brick_columns = [
        face_name_str(),
        event_int_str(),
        cumlative_minute_str(),
        gov_idea_str(),
    ]
    incom_row1 = [sue_str, event_1, minute_360, accord23_str]
    incom_row2 = [sue_str, event_1, minute_420, accord23_str]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_brick_columns)
    df3 = DataFrame([row2, row1, row3], columns=brick_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(ocean_file_path, br00003_ex1_str, df1)
    upsert_sheet(ocean_file_path, br00003_ex2_str, df2)
    upsert_sheet(ocean_file_path, br00003_ex3_str, df3)
    boat_file_path = create_path(boat_dir, "br00003.xlsx")
    assert os_path_exists(boat_file_path) is False

    # WHEN
    etl_ocean_to_boat_staging(ocean_dir, boat_dir)

    # THEN
    print(f"{boat_file_path=}")
    assert os_path_exists(boat_file_path)
    x_df = pandas_read_excel(boat_file_path, sheet_name=boat_staging_str())
    assert set(brick_columns).issubset(set(x_df.columns))
    file_dir_str = "file_dir"
    file_name_str = "file_name"
    sheet_name_str = "sheet_name"
    assert file_dir_str in set(x_df.columns)
    assert file_name_str in set(x_df.columns)
    assert sheet_name_str in set(x_df.columns)
    assert len(x_df) == 5
    assert get_sheet_names(boat_file_path) == [boat_staging_str()]
