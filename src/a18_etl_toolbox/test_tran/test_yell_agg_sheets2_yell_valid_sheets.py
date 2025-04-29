from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic._utils.str_a17 import yell_valid_str, yell_agg_str
from src.a17_idea_logic.idea_db_tool import sheet_exists, upsert_sheet
from src.a18_etl_toolbox.transformers import (
    etl_yell_agg_non_pidgin_ideas_to_yell_valid,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_yell_agg_non_pidgin_ideas_to_yell_valid_CreatesSheets_Scenario0(
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
    yell_dir = create_path(get_module_temp_dir(), "yell")
    yell_file_path = create_path(yell_dir, "br00003.xlsx")
    yell_agg_df = DataFrame([row1, row2, row3, row4], columns=br00003_columns)
    upsert_sheet(yell_file_path, yell_agg_str(), yell_agg_df)
    legitimate_events = {event1, event9}
    assert sheet_exists(yell_file_path, yell_valid_str()) is False

    # WHEN
    etl_yell_agg_non_pidgin_ideas_to_yell_valid(yell_dir, legitimate_events)

    # THEN
    assert sheet_exists(yell_file_path, yell_valid_str())
    gen_yell_valid_df = pandas_read_excel(yell_file_path, sheet_name=yell_valid_str())
    print(f"{gen_yell_valid_df.columns=}")
    example_yell_valid_df = DataFrame([row1, row2, row4], columns=br00003_columns)
    assert len(gen_yell_valid_df.columns) == len(example_yell_valid_df.columns)
    assert list(gen_yell_valid_df.columns) == list(example_yell_valid_df.columns)
    assert len(gen_yell_valid_df) > 0
    assert len(gen_yell_valid_df) == 3
    assert len(gen_yell_valid_df) == len(example_yell_valid_df)
    pandas_assert_frame_equal(gen_yell_valid_df, example_yell_valid_df)
