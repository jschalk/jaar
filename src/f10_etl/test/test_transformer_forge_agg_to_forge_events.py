from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import (
    get_sheet_names,
    upsert_sheet,
    forge_staging_str,
    forge_agg_str,
)
from src.f10_etl.transformers import (
    etl_mine_to_forge_staging,
    etl_forge_staging_to_forge_agg,
    etl_forge_agg_to_forge_events,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_forge_agg_to_forge_events_CreatesSheets_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    mine_dir = create_path(get_test_etl_dir(), "mine")
    forge_dir = create_path(get_test_etl_dir(), "forge")
    mine_file_path = create_path(mine_dir, ex_file_name)
    forge_file_path = create_path(forge_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event1, music23_str, hour7am, minute_420]
    row3 = [yao_str, event3, music23_str, hour7am, minute_420]
    row4 = [yao_str, event9, music23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4], columns=brick_columns)
    upsert_sheet(mine_file_path, "example1_br00003", df1)
    etl_mine_to_forge_staging(mine_dir, forge_dir)
    etl_forge_staging_to_forge_agg(forge_dir)

    # WHEN
    etl_forge_agg_to_forge_events(forge_dir)

    # THEN
    gen_otx_events_df = pandas_read_excel(forge_file_path, sheet_name="forge_events")
    print(f"{gen_otx_events_df.columns=}")
    events_otx_columns = [face_id_str(), event_id_str(), "note"]
    sue_r = [sue_str, event1, ""]
    yao3_r = [yao_str, event3, ""]
    yao9_r = [yao_str, event9, ""]
    ex_otx_events_df = DataFrame([sue_r, yao3_r, yao9_r], columns=events_otx_columns)
    assert len(gen_otx_events_df.columns) == len(ex_otx_events_df.columns)
    assert list(gen_otx_events_df.columns) == list(ex_otx_events_df.columns)
    assert len(gen_otx_events_df) > 0
    assert len(gen_otx_events_df) == 3
    assert len(gen_otx_events_df) == len(ex_otx_events_df)
    assert gen_otx_events_df.to_csv(index=False) == ex_otx_events_df.to_csv(index=False)
    assert get_sheet_names(forge_file_path) == [
        forge_staging_str(),
        forge_agg_str(),
        "forge_events",
    ]


def test_WorldUnit_forge_agg_to_forge_events_CreatesSheets_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    mine_dir = create_path(get_test_etl_dir(), "mine")
    forge_dir = create_path(get_test_etl_dir(), "forge")
    mine_file_path = create_path(mine_dir, ex_file_name)
    forge_file_path = create_path(forge_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event1, music23_str, hour7am, minute_420]
    row3 = [yao_str, event1, music23_str, hour7am, minute_420]
    row4 = [yao_str, event9, music23_str, hour7am, minute_420]
    row5 = [bob_str, event3, music23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4, row5], columns=brick_columns)
    upsert_sheet(mine_file_path, "example1_br00003", df1)
    etl_mine_to_forge_staging(mine_dir, forge_dir)
    etl_forge_staging_to_forge_agg(forge_dir)

    # WHEN
    etl_forge_agg_to_forge_events(forge_dir)

    # THEN
    gen_otx_events_df = pandas_read_excel(forge_file_path, sheet_name="forge_events")
    print(f"{gen_otx_events_df.columns=}")
    events_otx_columns = [face_id_str(), event_id_str(), "note"]
    bob_row = [bob_str, event3, ""]
    sue_row = [sue_str, event1, "invalid because of conflicting event_id"]
    yao1_row = [yao_str, event1, "invalid because of conflicting event_id"]
    yao9_row = [yao_str, event9, ""]
    events_rows = [bob_row, sue_row, yao1_row, yao9_row]
    ex_otx_events_df = DataFrame(events_rows, columns=events_otx_columns)
    assert len(gen_otx_events_df.columns) == len(ex_otx_events_df.columns)
    assert list(gen_otx_events_df.columns) == list(ex_otx_events_df.columns)
    assert len(gen_otx_events_df) > 0
    assert len(gen_otx_events_df) == 4
    assert len(gen_otx_events_df) == len(ex_otx_events_df)
    print(f"{gen_otx_events_df.to_csv(index=False)=}")
    print(f" {ex_otx_events_df.to_csv(index=False)=}")
    assert gen_otx_events_df.to_csv(index=False) == ex_otx_events_df.to_csv(index=False)
