from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import (
    sheet_exists,
    upsert_sheet,
    zoo_agg_str,
    zoo_valid_str,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_zoo_agg_to_zoo_valid_CreatesSheets_Scenario0(
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
    fizz_world = worldunit_shop("fizz")
    fizz_world.set_event(event1, sue_str)
    fizz_world.set_event(event9, yao_str)
    legitimate_events = {event1, event9}
    assert fizz_world.legitimate_events() == legitimate_events
    zoo_file_path = create_path(fizz_world._zoo_dir, "br00003.xlsx")
    zoo_agg_df = DataFrame([row1, row2, row3, row4], columns=br00003_columns)
    upsert_sheet(zoo_file_path, zoo_agg_str(), zoo_agg_df)
    assert sheet_exists(zoo_file_path, zoo_valid_str()) is False

    # WHEN
    fizz_world.zoo_agg_to_zoo_valid()

    # THEN
    assert sheet_exists(zoo_file_path, zoo_valid_str())
    gen_zoo_valid_df = pandas_read_excel(zoo_file_path, sheet_name=zoo_valid_str())
    print(f"{gen_zoo_valid_df.columns=}")
    example_zoo_valid_df = DataFrame([row1, row2, row4], columns=br00003_columns)
    assert len(gen_zoo_valid_df.columns) == len(example_zoo_valid_df.columns)
    assert list(gen_zoo_valid_df.columns) == list(example_zoo_valid_df.columns)
    assert len(gen_zoo_valid_df) > 0
    assert len(gen_zoo_valid_df) == 3
    assert len(gen_zoo_valid_df) == len(example_zoo_valid_df)
    pandas_assert_frame_equal(gen_zoo_valid_df, example_zoo_valid_df)


# def test_WorldUnit_zoo_agg_to_zoo_valid_CreatesSheets_Scenario1(
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
#     jungle_dir = create_path(get_test_etl_dir(), "jungle")
#     zoo_dir = create_path(get_test_etl_dir(), "zoo")
#     jungle_file_path = create_path(jungle_dir, ex_file_name)
#     zoo_file_path = create_path(zoo_dir, "br00003.xlsx")
#     brick_columns = [
#         face_id_str(),
#         event_id_str(),
#         fiscal_id_str(),
#         hour_label_str(),
#         cumlative_minute_str(),
#     ]
#     music23_str = "music23"
#     row1 = [sue_str, event1, music23_str, hour6am, minute_360]
#     row2 = [sue_str, event1, music23_str, hour7am, minute_420]
#     row3 = [yao_str, event1, music23_str, hour7am, minute_420]
#     row4 = [yao_str, event9, music23_str, hour7am, minute_420]
#     row5 = [bob_str, event3, music23_str, hour7am, minute_420]
#     df1 = DataFrame([row1, row2, row3, row4, row5], columns=brick_columns)
#     upsert_sheet(jungle_file_path, "example1_br00003", df1)
#     etl_jungle_to_zoo_staging(jungle_dir, zoo_dir)
#     etl_zoo_staging_to_zoo_agg(zoo_dir)

#     # WHEN
#     etl_zoo_agg_to_zoo_valid(zoo_dir)

#     # THEN
#     gen_otx_events_df = pandas_read_excel(zoo_file_path, sheet_name="zoo_valid")
#     print(f"{gen_otx_events_df.columns=}")
#     events_otx_columns = [face_id_str(), event_id_str(), "note"]
#     bob_row = [bob_str, event3, ""]
#     sue_row = [sue_str, event1, "invalid because of conflicting event_id"]
#     yao1_row = [yao_str, event1, "invalid because of conflicting event_id"]
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
