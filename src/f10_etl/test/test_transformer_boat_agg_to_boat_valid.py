from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_name_str, cmty_title_str
from src.f07_cmty.cmty_config import cumlative_minute_str, hour_title_str
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.pandas_tool import (
    sheet_exists,
    upsert_sheet,
    boat_agg_str,
    boat_valid_str,
)
from src.f10_etl.transformers import etl_boat_agg_to_boat_valid
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_boat_agg_to_boat_valid_CreatesSheets_Scenario0(
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
    br00003_columns = [
        face_name_str(),
        event_int_str(),
        cmty_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event1, accord23_str, hour7am, minute_420]
    row3 = [yao_str, event3, accord23_str, hour7am, minute_420]
    row4 = [yao_str, event9, accord23_str, hour7am, minute_420]
    boat_dir = create_path(get_test_etl_dir(), "boat")
    boat_file_path = create_path(boat_dir, "br00003.xlsx")
    boat_agg_df = DataFrame([row1, row2, row3, row4], columns=br00003_columns)
    upsert_sheet(boat_file_path, boat_agg_str(), boat_agg_df)
    legitimate_events = {event1, event9}
    assert sheet_exists(boat_file_path, boat_valid_str()) is False

    # WHEN
    etl_boat_agg_to_boat_valid(boat_dir, legitimate_events)

    # THEN
    assert sheet_exists(boat_file_path, boat_valid_str())
    gen_boat_valid_df = pandas_read_excel(boat_file_path, sheet_name=boat_valid_str())
    print(f"{gen_boat_valid_df.columns=}")
    example_boat_valid_df = DataFrame([row1, row2, row4], columns=br00003_columns)
    assert len(gen_boat_valid_df.columns) == len(example_boat_valid_df.columns)
    assert list(gen_boat_valid_df.columns) == list(example_boat_valid_df.columns)
    assert len(gen_boat_valid_df) > 0
    assert len(gen_boat_valid_df) == 3
    assert len(gen_boat_valid_df) == len(example_boat_valid_df)
    pandas_assert_frame_equal(gen_boat_valid_df, example_boat_valid_df)


# def test_WorldUnit_boat_agg_to_boat_valid_CreatesSheets_Scenario1(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_str = "fizz"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     bob_str = "Bob"
#     event1 = 1
#     event3 = 3
#     event9 = 9
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_file_name = "fizzbuzz.xlsx"
#     ocean_dir = create_path(get_test_etl_dir(), "ocean")
#     boat_dir = create_path(get_test_etl_dir(), "boat")
#     ocean_file_path = create_path(ocean_dir, ex_file_name)
#     boat_file_path = create_path(boat_dir, "br00003.xlsx")
#     idea_columns = [
#         face_name_str(),
#         event_int_str(),
#         cmty_title_str(),
#         hour_title_str(),
#         cumlative_minute_str(),
#     ]
#     accord23_str = "accord23"
#     row1 = [sue_str, event1, accord23_str, hour6am, minute_360]
#     row2 = [sue_str, event1, accord23_str, hour7am, minute_420]
#     row3 = [yao_str, event1, accord23_str, hour7am, minute_420]
#     row4 = [yao_str, event9, accord23_str, hour7am, minute_420]
#     row5 = [bob_str, event3, accord23_str, hour7am, minute_420]
#     df1 = DataFrame([row1, row2, row3, row4, row5], columns=idea_columns)
#     upsert_sheet(ocean_file_path, "example1_br00003", df1)
#     etl_ocean_to_boat_staging(ocean_dir, boat_dir)
#     etl_boat_staging_to_boat_agg(boat_dir)

#     # WHEN
#     etl_boat_agg_to_boat_valid(boat_dir)

#     # THEN
#     gen_otx_events_df = pandas_read_excel(boat_file_path, sheet_name="boat_valid")
#     print(f"{gen_otx_events_df.columns=}")
#     events_otx_columns = [face_name_str(), event_int_str(), "note"]
#     bob_row = [bob_str, event3, ""]
#     sue_row = [sue_str, event1, "invalid because of conflicting event_int"]
#     yao1_row = [yao_str, event1, "invalid because of conflicting event_int"]
#     yao9_row = [yao_str, event9, ""]
#     events_rows = [bob_row, sue_row, yao1_row, yao9_row]
#     ex_otx_events_df = DataFrame(events_rows, columns=events_otx_columns)
#     assert len(gen_otx_events_df.columns) == len(ex_otx_events_df.columns)
#     assert list(gen_otx_events_df.columns) == list(ex_otx_events_df.columns)
#     assert len(gen_otx_events_df) > 0
#     assert len(gen_otx_events_df) == 4
#     assert len(gen_otx_events_df) == len(ex_otx_events_df)
#     print(f"{gen_otx_events_df.to_csv(index=False)=}")
#     print(f" {ex_otx_events_df.to_csv(index=False)=}")
#     assert gen_otx_events_df.to_csv(index=False) == ex_otx_events_df.to_csv(index=False)
