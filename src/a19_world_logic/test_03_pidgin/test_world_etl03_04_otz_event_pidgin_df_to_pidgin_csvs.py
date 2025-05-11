from src.a00_data_toolbox.file_toolbox import create_path
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_way_str,
    otx_way_str,
    unknown_word_str,
)
from src.a17_idea_logic.idea_db_tool import sheet_exists, upsert_sheet, open_csv
from src.a18_etl_toolbox.tran_path import (
    create_otx_event_pidgin_path as otx_event_pidgin_path,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_otz_event_pidgins_to_otz_pidgin_csv_files_Scenario0_3Event_way(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event3 = 3
    event7 = 7
    event9 = 9
    way_file_columns = [
        event_int_str(),
        face_name_str(),
        otx_way_str(),
        inx_way_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    x_nan = float("nan")
    e3_way0 = [event3, bob_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e3_way1 = [event3, bob_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e3_way_rows = [e3_way0, e3_way1]
    e3_way_df = DataFrame(e3_way_rows, columns=way_file_columns)

    e7_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e7_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e7_way_rows = [e7_way0, e7_way1]
    e7_way_df = DataFrame(e7_way_rows, columns=way_file_columns)

    e9_way0 = [event9, zia_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e9_way1 = [event9, zia_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e9_way_rows = [e9_way0, e9_way1]
    e9_way_df = DataFrame(e9_way_rows, columns=way_file_columns)

    fizz_world = worldunit_shop("fizz", worlds_dir())
    bob_dir = create_path(fizz_world._syntax_otz_dir, bob_str)
    sue_dir = create_path(fizz_world._syntax_otz_dir, sue_str)
    zia_dir = create_path(fizz_world._syntax_otz_dir, zia_str)
    event3_dir = create_path(bob_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    syntax_otz_dir = fizz_world._syntax_otz_dir
    event3_pidgin_file_path = otx_event_pidgin_path(syntax_otz_dir, bob_str, event3)
    event7_pidgin_file_path = otx_event_pidgin_path(syntax_otz_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(syntax_otz_dir, zia_str, event9)
    event3_way_csv_file_path = create_path(event3_dir, "way.csv")
    event7_way_csv_file_path = create_path(event7_dir, "way.csv")
    event9_way_csv_file_path = create_path(event9_dir, "way.csv")
    way_agg_str = "way_agg"
    upsert_sheet(event3_pidgin_file_path, way_agg_str, e3_way_df)
    upsert_sheet(event7_pidgin_file_path, way_agg_str, e7_way_df)
    upsert_sheet(event9_pidgin_file_path, way_agg_str, e9_way_df)
    assert sheet_exists(event3_pidgin_file_path, way_agg_str)
    assert sheet_exists(event7_pidgin_file_path, way_agg_str)
    assert sheet_exists(event9_pidgin_file_path, way_agg_str)
    assert os_path_exists(event3_way_csv_file_path) is False
    assert os_path_exists(event7_way_csv_file_path) is False
    assert os_path_exists(event9_way_csv_file_path) is False

    # WHEN
    fizz_world.otz_event_pidgins_to_otz_pidgin_csv_files()

    # THEN
    assert os_path_exists(event3_way_csv_file_path)
    assert os_path_exists(event7_way_csv_file_path)
    assert os_path_exists(event9_way_csv_file_path)
    gen_csv_event3_df = open_csv(event7_dir, "way.csv")
    print(f"{gen_csv_event3_df=}")
    pandas_testing_assert_frame_equal(gen_csv_event3_df, e7_way_df)
