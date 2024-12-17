from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import (
    get_sheet_names,
    upsert_sheet,
    fish_staging_str,
    fish_agg_str,
)
from src.f10_etl.transformers import (
    etl_ocean_to_fish_staging,
    etl_fish_staging_to_fish_agg,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_fish_staging_to_fish_agg_CreatesOtxSheets_Scenario0_GroupByWorks(
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
    fish_dir = create_path(get_test_etl_dir(), "fish")
    ocean_file_path = create_path(ocean_dir, ex_file_name)
    fish_file_path = create_path(fish_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event_1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event_1, music23_str, hour7am, minute_420]
    row3 = [sue_str, event_1, music23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3], columns=brick_columns)
    upsert_sheet(ocean_file_path, "example1_br00003", df1)
    etl_ocean_to_fish_staging(ocean_dir, fish_dir)
    fish__staging_df = pandas_read_excel(fish_file_path, sheet_name=fish_staging_str())
    assert len(fish__staging_df) == 3

    # WHEN
    etl_fish_staging_to_fish_agg(fish_dir)

    # THEN
    gen_otx_df = pandas_read_excel(fish_file_path, sheet_name=fish_agg_str())
    ex_otx_df = DataFrame([row1, row2], columns=brick_columns)
    print(f"{gen_otx_df.columns=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 2
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(fish_file_path) == [fish_staging_str(), fish_agg_str()]


def test_WorldUnit_fish_staging_to_fish_agg_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
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
    fish_dir = create_path(get_test_etl_dir(), "fish")
    ocean_file_path = create_path(ocean_dir, ex_file_name)
    fish_file_path = create_path(fish_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event_1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event_1, music23_str, hour7am, minute_420]
    row3 = [sue_str, event_1, music23_str, hour7am, minute_480]
    df1 = DataFrame([row1, row2, row3], columns=brick_columns)
    upsert_sheet(ocean_file_path, "example1_br00003", df1)
    etl_ocean_to_fish_staging(ocean_dir, fish_dir)
    fish_df = pandas_read_excel(fish_file_path, sheet_name=fish_staging_str())
    assert len(fish_df) == 3

    # WHEN
    etl_fish_staging_to_fish_agg(fish_dir)

    # THEN
    gen_otx_df = pandas_read_excel(fish_file_path, sheet_name=fish_agg_str())
    ex_otx_df = DataFrame([row1], columns=brick_columns)
    # print(f"{gen_otx_df.columns=}")
    print(f"{gen_otx_df=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 1
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(fish_file_path) == [fish_staging_str(), fish_agg_str()]
