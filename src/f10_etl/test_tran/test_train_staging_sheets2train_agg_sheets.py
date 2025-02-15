from src.f00_instrument.file import create_path
from src.f01_road.deal import fisc_title_str
from src.f04_gift.atom_config import face_name_str, event_int_str
from src.f07_fisc.fisc_config import cumlative_minute_str, hour_title_str

from src.f09_idea.idea_db_tool import (
    get_sheet_names,
    upsert_sheet,
    train_staging_str,
    train_agg_str,
)
from src.f10_etl.transformers import (
    etl_mine_to_train_staging,
    etl_train_staging_to_train_agg,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_train_staging_to_train_agg_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    mine_dir = create_path(get_test_etl_dir(), "mine")
    train_dir = create_path(get_test_etl_dir(), "train")
    mine_file_path = create_path(mine_dir, ex_filename)
    train_file_path = create_path(train_dir, "br00003.xlsx")
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event_1, accord23_str, hour7am, minute_420]
    row3 = [sue_str, event_1, accord23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3], columns=idea_columns)
    upsert_sheet(mine_file_path, "example1_br00003", df1)
    etl_mine_to_train_staging(mine_dir, train_dir)
    train__staging_df = pandas_read_excel(
        train_file_path, sheet_name=train_staging_str()
    )
    assert len(train__staging_df) == 3

    # WHEN
    etl_train_staging_to_train_agg(train_dir)

    # THEN
    gen_otx_df = pandas_read_excel(train_file_path, sheet_name=train_agg_str())
    ex_otx_df = DataFrame([row1, row2], columns=idea_columns)
    print(f"{gen_otx_df.columns=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 2
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(train_file_path) == [train_staging_str(), train_agg_str()]


def test_etl_train_staging_to_train_agg_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
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
    ex_filename = "fizzbuzz.xlsx"
    mine_dir = create_path(get_test_etl_dir(), "mine")
    train_dir = create_path(get_test_etl_dir(), "train")
    mine_file_path = create_path(mine_dir, ex_filename)
    train_file_path = create_path(train_dir, "br00003.xlsx")
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event_1, accord23_str, hour7am, minute_420]
    row3 = [sue_str, event_1, accord23_str, hour7am, minute_480]
    df1 = DataFrame([row1, row2, row3], columns=idea_columns)
    upsert_sheet(mine_file_path, "example1_br00003", df1)
    etl_mine_to_train_staging(mine_dir, train_dir)
    train_df = pandas_read_excel(train_file_path, sheet_name=train_staging_str())
    assert len(train_df) == 3

    # WHEN
    etl_train_staging_to_train_agg(train_dir)

    # THEN
    gen_otx_df = pandas_read_excel(train_file_path, sheet_name=train_agg_str())
    ex_otx_df = DataFrame([row1], columns=idea_columns)
    # print(f"{gen_otx_df.columns=}")
    print(f"{gen_otx_df=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 1
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(train_file_path) == [train_staging_str(), train_agg_str()]
