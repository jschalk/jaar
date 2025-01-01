from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_name_str, cmty_idea_str
from src.f07_cmty.cmty_config import cumlative_minute_str, hour_idea_str
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_brick.pandas_tool import (
    get_sheet_names,
    upsert_sheet,
    boat_staging_str,
    boat_agg_str,
)
from src.f10_etl.transformers import (
    etl_ocean_to_boat_staging,
    etl_boat_staging_to_boat_agg,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_boat_staging_to_boat_agg_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    ocean_dir = create_path(get_test_etl_dir(), "ocean")
    boat_dir = create_path(get_test_etl_dir(), "boat")
    ocean_file_path = create_path(ocean_dir, ex_file_name)
    boat_file_path = create_path(boat_dir, "br00003.xlsx")
    brick_columns = [
        face_name_str(),
        event_int_str(),
        cmty_idea_str(),
        hour_idea_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event_1, accord23_str, hour7am, minute_420]
    row3 = [sue_str, event_1, accord23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3], columns=brick_columns)
    upsert_sheet(ocean_file_path, "example1_br00003", df1)
    etl_ocean_to_boat_staging(ocean_dir, boat_dir)
    boat__staging_df = pandas_read_excel(boat_file_path, sheet_name=boat_staging_str())
    assert len(boat__staging_df) == 3

    # WHEN
    etl_boat_staging_to_boat_agg(boat_dir)

    # THEN
    gen_otx_df = pandas_read_excel(boat_file_path, sheet_name=boat_agg_str())
    ex_otx_df = DataFrame([row1, row2], columns=brick_columns)
    print(f"{gen_otx_df.columns=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 2
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(boat_file_path) == [boat_staging_str(), boat_agg_str()]


def test_WorldUnit_boat_staging_to_boat_agg_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    minute_480 = 480
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    ocean_dir = create_path(get_test_etl_dir(), "ocean")
    boat_dir = create_path(get_test_etl_dir(), "boat")
    ocean_file_path = create_path(ocean_dir, ex_file_name)
    boat_file_path = create_path(boat_dir, "br00003.xlsx")
    brick_columns = [
        face_name_str(),
        event_int_str(),
        cmty_idea_str(),
        hour_idea_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event_1, accord23_str, hour7am, minute_420]
    row3 = [sue_str, event_1, accord23_str, hour7am, minute_480]
    df1 = DataFrame([row1, row2, row3], columns=brick_columns)
    upsert_sheet(ocean_file_path, "example1_br00003", df1)
    etl_ocean_to_boat_staging(ocean_dir, boat_dir)
    boat_df = pandas_read_excel(boat_file_path, sheet_name=boat_staging_str())
    assert len(boat_df) == 3

    # WHEN
    etl_boat_staging_to_boat_agg(boat_dir)

    # THEN
    gen_otx_df = pandas_read_excel(boat_file_path, sheet_name=boat_agg_str())
    ex_otx_df = DataFrame([row1], columns=brick_columns)
    # print(f"{gen_otx_df.columns=}")
    print(f"{gen_otx_df=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 1
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(boat_file_path) == [boat_staging_str(), boat_agg_str()]
