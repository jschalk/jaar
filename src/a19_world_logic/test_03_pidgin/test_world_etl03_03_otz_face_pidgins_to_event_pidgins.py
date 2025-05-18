from src.a00_data_toolbox.file_toolbox import create_path, get_dir_filenames
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_title_str,
    otx_title_str,
    inx_label_str,
    otx_label_str,
    inx_way_str,
    otx_way_str,
    unknown_term_str,
)
from src.a17_creed_logic.creed_db_tool import sheet_exists, upsert_sheet
from src.a18_etl_toolbox.tran_path import (
    create_syntax_otx_pidgin_path,
    create_otx_event_pidgin_path as otx_event_pidgin_path,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_otz_face_pidgins_df_to_otz_event_pidgins_df_Scenario0_way_Two_face_names(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
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
        unknown_term_str(),
    ]
    x_nan = float("nan")
    e1_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way2 = [event9, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way_rows = [e1_way0, e1_way1, e1_way2]
    sue_way_agg_df = DataFrame(e1_way_rows, columns=way_file_columns)
    z1_way3 = [event3, zia_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    zia_way_agg_df = DataFrame([z1_way3], columns=way_file_columns)

    fizz_world = worldunit_shop("fizz", worlds_dir())
    sue_dir = create_path(fizz_world._syntax_otz_dir, sue_str)
    zia_dir = create_path(fizz_world._syntax_otz_dir, zia_str)
    event3_dir = create_path(zia_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    syntax_otz_dir = fizz_world._syntax_otz_dir
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(syntax_otz_dir, sue_str)
    zia_pidgin_file_path = create_syntax_otx_pidgin_path(syntax_otz_dir, zia_str)
    event3_pidgin_file_path = otx_event_pidgin_path(syntax_otz_dir, zia_str, event3)
    event7_pidgin_file_path = otx_event_pidgin_path(syntax_otz_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(syntax_otz_dir, sue_str, event9)
    way_agg_str = "way_agg"
    upsert_sheet(sue_pidgin_file_path, way_agg_str, sue_way_agg_df)
    upsert_sheet(zia_pidgin_file_path, way_agg_str, zia_way_agg_df)
    assert sheet_exists(sue_pidgin_file_path, way_agg_str)
    assert sheet_exists(zia_pidgin_file_path, way_agg_str)

    assert os_path_exists(event3_dir) is False
    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, way_agg_str) is False
    assert sheet_exists(event7_pidgin_file_path, way_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, way_agg_str) is False

    # WHEN
    fizz_world.otz_face_pidgins_df_to_otz_event_pidgins_df()

    # THEN
    assert os_path_exists(event3_dir)
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event3_pidgin_file_path)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event3_pidgin_file_path, way_agg_str)
    assert sheet_exists(event7_pidgin_file_path, way_agg_str)
    assert sheet_exists(event9_pidgin_file_path, way_agg_str)
    e3_pidgin_way_df = pandas_read_excel(event3_pidgin_file_path, way_agg_str)
    e7_pidgin_way_df = pandas_read_excel(event7_pidgin_file_path, way_agg_str)
    e9_pidgin_way_df = pandas_read_excel(event9_pidgin_file_path, way_agg_str)

    expected7_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    expected7_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    expected7_way_rows = [expected7_way0, expected7_way1]
    expected7_agg_df = DataFrame(expected7_way_rows, columns=way_file_columns)

    expected9_way0 = [event9, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    expected9_way_rows = [expected9_way0]
    expected9_agg_df = DataFrame(expected9_way_rows, columns=way_file_columns)

    pandas_testing_assert_frame_equal(e3_pidgin_way_df, zia_way_agg_df)
    pandas_testing_assert_frame_equal(e7_pidgin_way_df, expected7_agg_df)
    pandas_testing_assert_frame_equal(e9_pidgin_way_df, expected9_agg_df)
