from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic._utils.str_a17 import brick_valid_str, brick_agg_str
from src.a17_idea_logic.idea_db_tool import sheet_exists, upsert_sheet
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_brick_agg_non_pidgin_ideas_to_brick_valid_CreatesSheets_Scenario0(
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
        fisc_tag_str(),
        hour_tag_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event1, accord23_str, hour7am, minute_420]
    row3 = [yao_str, event3, accord23_str, hour7am, minute_420]
    row4 = [yao_str, event9, accord23_str, hour7am, minute_420]
    fizz_world = worldunit_shop("fizz", worlds_dir())
    fizz_world.set_event(event1, sue_str)
    fizz_world.set_event(event9, yao_str)
    legitimate_events = {event1, event9}
    assert set(fizz_world._events.keys()) == legitimate_events
    brick_file_path = create_path(fizz_world._brick_dir, "br00003.xlsx")
    brick_agg_df = DataFrame([row1, row2, row3, row4], columns=br00003_columns)
    upsert_sheet(brick_file_path, brick_agg_str(), brick_agg_df)
    assert sheet_exists(brick_file_path, brick_valid_str()) is False

    # WHEN
    fizz_world.brick_agg_non_pidgin_ideas_to_brick_valid()

    # THEN
    assert sheet_exists(brick_file_path, brick_valid_str())
    gen_brick_valid_df = pandas_read_excel(
        brick_file_path, sheet_name=brick_valid_str()
    )
    print(f"{gen_brick_valid_df.columns=}")
    example_brick_valid_df = DataFrame([row1, row2, row4], columns=br00003_columns)
    assert len(gen_brick_valid_df.columns) == len(example_brick_valid_df.columns)
    assert list(gen_brick_valid_df.columns) == list(example_brick_valid_df.columns)
    assert len(gen_brick_valid_df) > 0
    assert len(gen_brick_valid_df) == 3
    assert len(gen_brick_valid_df) == len(example_brick_valid_df)
    pandas_assert_frame_equal(gen_brick_valid_df, example_brick_valid_df)


# def test_WorldUnit_brick_agg_non_pidgin_ideas_to_brick_valid_CreatesSheets_Scenario1(
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
#     ex_filename = "fizzbuzz.xlsx"
#     mud_dir = create_path(get_module_temp_dir(), "mud")
#     brick_dir = create_path(get_module_temp_dir(), "brick")
#     mud_file_path = create_path(mud_dir, ex_filename)
#     brick_file_path = create_path(brick_dir, "br00003.xlsx")
#     idea_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_tag_str(),
#         hour_tag_str(),
#         cumlative_minute_str(),
#     ]
#     accord23_str = "accord23"
#     row1 = [sue_str, event1, accord23_str, hour6am, minute_360]
#     row2 = [sue_str, event1, accord23_str, hour7am, minute_420]
#     row3 = [yao_str, event1, accord23_str, hour7am, minute_420]
#     row4 = [yao_str, event9, accord23_str, hour7am, minute_420]
#     row5 = [bob_str, event3, accord23_str, hour7am, minute_420]
#     df1 = DataFrame([row1, row2, row3, row4, row5], columns=idea_columns)
#     upsert_sheet(mud_file_path, "example1_br00003", df1)
#     etl_brick_raw_db_to_brick_agg_df(brick_dir)

#     # WHEN
#     etl_brick_agg_non_pidgin_ideas_to_brick_valid(brick_dir)

#     # THEN
#     gen_otx_events_df = pandas_read_excel(brick_file_path, sheet_name="brick_valid")
#     print(f"{gen_otx_events_df.columns=}")
#     events_otx_columns = [face_name_str(), event_int_str(), "error_message"]
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
