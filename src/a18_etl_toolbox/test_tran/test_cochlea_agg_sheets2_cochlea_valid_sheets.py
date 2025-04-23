from src.a00_data_toolboxs.file_toolbox import create_path
from src.a02_finance_toolboxs.deal import fisc_tag_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic.idea_db_tool import (
    sheet_exists,
    upsert_sheet,
    cochlea_agg_str,
    cochlea_valid_str,
)
from src.a18_etl_toolbox.transformers import (
    etl_cochlea_agg_non_pidgin_ideas_to_cochlea_valid,
)
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_cochlea_agg_non_pidgin_ideas_to_cochlea_valid_CreatesSheets_Scenario0(
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
    cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
    cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
    cochlea_agg_df = DataFrame([row1, row2, row3, row4], columns=br00003_columns)
    upsert_sheet(cochlea_file_path, cochlea_agg_str(), cochlea_agg_df)
    legitimate_events = {event1, event9}
    assert sheet_exists(cochlea_file_path, cochlea_valid_str()) is False

    # WHEN
    etl_cochlea_agg_non_pidgin_ideas_to_cochlea_valid(cochlea_dir, legitimate_events)

    # THEN
    assert sheet_exists(cochlea_file_path, cochlea_valid_str())
    gen_cochlea_valid_df = pandas_read_excel(
        cochlea_file_path, sheet_name=cochlea_valid_str()
    )
    print(f"{gen_cochlea_valid_df.columns=}")
    example_cochlea_valid_df = DataFrame([row1, row2, row4], columns=br00003_columns)
    assert len(gen_cochlea_valid_df.columns) == len(example_cochlea_valid_df.columns)
    assert list(gen_cochlea_valid_df.columns) == list(example_cochlea_valid_df.columns)
    assert len(gen_cochlea_valid_df) > 0
    assert len(gen_cochlea_valid_df) == 3
    assert len(gen_cochlea_valid_df) == len(example_cochlea_valid_df)
    pandas_assert_frame_equal(gen_cochlea_valid_df, example_cochlea_valid_df)


# def test_etl_cochlea_agg_non_pidgin_ideas_to_cochlea_valid_CreatesSheets_Scenario1(
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
#     sound_dir = create_path(get_test_etl_dir(), "sound")
#     cochlea_dir = create_path(get_test_etl_dir(), "cochlea")
#     sound_file_path = create_path(sound_dir, ex_filename)
#     cochlea_file_path = create_path(cochlea_dir, "br00003.xlsx")
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
#     upsert_sheet(sound_file_path, "example1_br00003", df1)
#     etl_sound_df_to_cochlea_raw_df(sound_dir, cochlea_dir)
#     etl_cochlea_raw_df_to_cochlea_agg_df(cochlea_dir)

#     # WHEN
#     etl_cochlea_agg_non_pidgin_ideas_to_cochlea_valid(cochlea_dir)

#     # THEN
#     gen_otx_events_df = pandas_read_excel(cochlea_file_path, sheet_name="cochlea_valid")
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
