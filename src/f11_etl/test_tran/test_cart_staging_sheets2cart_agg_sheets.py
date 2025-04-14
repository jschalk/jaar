from src.f00_data_toolboxs.file_toolbox import create_path
from src.f02_finance_toolboxs.deal import fisc_title_str
from src.f04_pack.atom_config import face_name_str, event_int_str
from src.f08_fisc.fisc_config import cumlative_minute_str, hour_title_str
from src.f10_idea.idea_db_tool import (
    get_sheet_names,
    upsert_sheet,
    cart_staging_str,
    cart_agg_str,
)
from src.f11_etl.transformers import (
    etl_mine_to_cart_staging,
    etl_cart_staging_to_cart_agg,
)
from src.f11_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_cart_staging_to_cart_agg_CreatesOtxSheets_Scenario0_GroupByWorks(
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
    cart_dir = create_path(get_test_etl_dir(), "cart")
    mine_file_path = create_path(mine_dir, ex_filename)
    cart_file_path = create_path(cart_dir, "br00003.xlsx")
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        cumlative_minute_str(),
        hour_title_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, accord23_str, minute_360, hour6am]
    row2 = [sue_str, event_1, accord23_str, minute_420, hour7am]
    row3 = [sue_str, event_1, accord23_str, minute_420, hour7am]
    df1 = DataFrame([row1, row2, row3], columns=idea_columns)
    upsert_sheet(mine_file_path, "example1_br00003", df1)
    etl_mine_to_cart_staging(mine_dir, cart_dir)
    cart__staging_df = pandas_read_excel(cart_file_path, sheet_name=cart_staging_str())
    assert len(cart__staging_df) == 3

    # WHEN
    etl_cart_staging_to_cart_agg(cart_dir)

    # THEN
    gen_otx_df = pandas_read_excel(cart_file_path, sheet_name=cart_agg_str())
    ex_otx_df = DataFrame([row1, row2], columns=idea_columns)
    print(f"{gen_otx_df.columns=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 2
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(cart_file_path) == [cart_staging_str(), cart_agg_str()]


def test_etl_cart_staging_to_cart_agg_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    hour8am = "8am"
    ex_filename = "fizzbuzz.xlsx"
    mine_dir = create_path(get_test_etl_dir(), "mine")
    cart_dir = create_path(get_test_etl_dir(), "cart")
    mine_file_path = create_path(mine_dir, ex_filename)
    cart_file_path = create_path(cart_dir, "br00003.xlsx")
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        cumlative_minute_str(),
        hour_title_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event_1, accord23_str, minute_360, hour6am]
    row2 = [sue_str, event_1, accord23_str, minute_420, hour7am]
    row3 = [sue_str, event_1, accord23_str, minute_420, hour8am]
    df1 = DataFrame([row1, row2, row3], columns=idea_columns)
    upsert_sheet(mine_file_path, "example1_br00003", df1)
    etl_mine_to_cart_staging(mine_dir, cart_dir)
    cart_df = pandas_read_excel(cart_file_path, sheet_name=cart_staging_str())
    assert len(cart_df) == 3

    # WHEN
    etl_cart_staging_to_cart_agg(cart_dir)

    # THEN
    gen_otx_df = pandas_read_excel(cart_file_path, sheet_name=cart_agg_str())
    ex_otx_df = DataFrame([row1], columns=idea_columns)
    # print(f"{gen_otx_df.columns=}")
    print(f"{gen_otx_df=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 1
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(cart_file_path) == [cart_staging_str(), cart_agg_str()]
