from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.str_helpers import fisc_tag_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic.idea_db_tool import (
    get_sheet_names,
    upsert_sheet,
    yell_valid_str,
    sheet_exists,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_utils import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_yell_ideas_to_otz_face_ideas_CreatesOtxSheets_Scenario0_GroupByWorks(
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
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        hour_tag_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event3, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event3, accord23_str, hour7am, minute_420]
    br00003_yell_agg_df = DataFrame([row1, row2], columns=idea_columns)
    br00003_agg_file_path = create_path(fizz_world._yell_dir, "br00003.xlsx")
    upsert_sheet(br00003_agg_file_path, yell_valid_str(), br00003_yell_agg_df)
    assert sheet_exists(br00003_agg_file_path, yell_valid_str())
    sue_dir = create_path(fizz_world._syntax_otz_dir, sue_str)
    sue_br00003_filepath = create_path(sue_dir, "br00003.xlsx")
    assert sheet_exists(sue_br00003_filepath, yell_valid_str()) is False

    # WHEN
    fizz_world.yell_ideas_to_otz_face_ideas()

    # THEN
    assert sheet_exists(sue_br00003_filepath, yell_valid_str())
    assert get_sheet_names(sue_br00003_filepath) == [yell_valid_str()]
    sue_br3_agg_df = pandas_read_excel(
        br00003_agg_file_path, sheet_name=yell_valid_str()
    )
    print(f"{sue_br3_agg_df.columns=}")

    assert len(sue_br3_agg_df.columns) == len(br00003_yell_agg_df.columns)
    assert list(sue_br3_agg_df.columns) == list(br00003_yell_agg_df.columns)
    assert len(sue_br3_agg_df) > 0
    assert len(sue_br3_agg_df) == len(br00003_yell_agg_df)
    assert len(sue_br3_agg_df) == 2
    assert sue_br3_agg_df.to_csv() == br00003_yell_agg_df.to_csv()
