from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import fisc_label_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_label_str
from src.a17_creed_logic._utils.str_a17 import brick_valid_str
from src.a17_creed_logic.creed_db_tool import (
    get_sheet_names,
    upsert_sheet,
    sheet_exists,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_brick_creeds_to_otz_face_creeds_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    sue_str = "Sue"
    event3 = 3
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    creed_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [event3, sue_str, accord23_str, hour6am, minute_360]
    row2 = [event3, sue_str, accord23_str, hour7am, minute_420]
    br00003_brick_agg_df = DataFrame([row1, row2], columns=creed_columns)
    br00003_agg_file_path = create_path(fizz_world._brick_dir, "br00003.xlsx")
    upsert_sheet(br00003_agg_file_path, brick_valid_str(), br00003_brick_agg_df)
    assert sheet_exists(br00003_agg_file_path, brick_valid_str())
    sue_dir = create_path(fizz_world._syntax_otz_dir, sue_str)
    sue_br00003_filepath = create_path(sue_dir, "br00003.xlsx")
    assert sheet_exists(sue_br00003_filepath, brick_valid_str()) is False

    # WHEN
    fizz_world.brick_creeds_to_otz_face_creeds()

    # THEN
    assert sheet_exists(sue_br00003_filepath, brick_valid_str())
    assert get_sheet_names(sue_br00003_filepath) == [brick_valid_str()]
    sue_br3_agg_df = pandas_read_excel(
        br00003_agg_file_path, sheet_name=brick_valid_str()
    )
    print(f"{sue_br3_agg_df.columns=}")

    assert len(sue_br3_agg_df.columns) == len(br00003_brick_agg_df.columns)
    assert list(sue_br3_agg_df.columns) == list(br00003_brick_agg_df.columns)
    assert len(sue_br3_agg_df) > 0
    assert len(sue_br3_agg_df) == len(br00003_brick_agg_df)
    assert len(sue_br3_agg_df) == 2
    assert sue_br3_agg_df.to_csv() == br00003_brick_agg_df.to_csv()
