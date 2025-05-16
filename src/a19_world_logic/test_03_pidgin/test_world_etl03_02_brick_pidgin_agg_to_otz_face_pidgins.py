from src.a00_data_toolbox.file_toolbox import create_path
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_label_str,
    otx_label_str,
    inx_tag_str,
    otx_tag_str,
    inx_way_str,
    otx_way_str,
    unknown_term_str,
)
from src.a17_creed_logic.creed_db_tool import sheet_exists, upsert_sheet
from src.a18_etl_toolbox.tran_path import (
    create_brick_pidgin_path,
    create_syntax_otx_pidgin_path,
)
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_brick_pidgin_agg_df_to_otz_face_pidgin_agg_df_Scenario1_AllMapDimens(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    bob_otx = "Bob"
    sue_str = "Sue"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    event7 = 7
    name_agg_str = "name_agg"

    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    x_nan = float("nan")
    e1_name0 = [event7, sue_str, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    e1_name1 = [event7, sue_str, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_agg_df = DataFrame(e1_name_rows, columns=name_agg_columns)

    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    event7 = 7
    label_agg_str = "label_agg"
    label_file_columns = PidginPrimeColumns().pidgin_label_agg_columns
    e1_label0 = [event7, sue_str, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_label1 = [event7, sue_str, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_file_columns)

    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    way_agg_str = "way_agg"
    way_file_columns = [
        event_int_str(),
        face_name_str(),
        otx_way_str(),
        inx_way_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    e1_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way_rows = [e1_way0, e1_way1]
    e1_way_agg_df = DataFrame(e1_way_rows, columns=way_file_columns)

    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    tag_agg_str = "tag_agg"
    tag_file_columns = [
        event_int_str(),
        face_name_str(),
        otx_tag_str(),
        inx_tag_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    e1_tag0 = [event7, sue_str, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_tag1 = [event7, sue_str, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_tag_rows = [e1_tag0, e1_tag1]
    e1_tag_agg_df = DataFrame(e1_tag_rows, columns=tag_file_columns)

    agg_pidgin_path = create_brick_pidgin_path(fizz_world._brick_dir)
    upsert_sheet(agg_pidgin_path, name_agg_str, e1_name_agg_df)
    upsert_sheet(agg_pidgin_path, label_agg_str, e1_label_agg_df)
    upsert_sheet(agg_pidgin_path, way_agg_str, e1_way_agg_df)
    upsert_sheet(agg_pidgin_path, tag_agg_str, e1_tag_agg_df)
    sue_dir = create_path(fizz_world._syntax_otz_dir, sue_str)
    syntax_otz_dir = fizz_world._syntax_otz_dir
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(syntax_otz_dir, sue_str)
    assert os_path_exists(sue_pidgin_file_path) is False

    # WHEN
    fizz_world.brick_pidgin_agg_df_to_otz_face_pidgin_agg_df()

    # THEN
    assert os_path_exists(sue_dir)
    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, name_agg_str)
    assert sheet_exists(sue_pidgin_file_path, label_agg_str)
    assert sheet_exists(sue_pidgin_file_path, tag_agg_str)
    assert sheet_exists(sue_pidgin_file_path, way_agg_str)
    gen_sue_name_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=name_agg_str)
    gen_sue_label_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=label_agg_str)
    gen_sue_tag_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=tag_agg_str)
    gen_sue_way_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=way_agg_str)
    print(f"{gen_sue_tag_df=}")

    pandas_testing_assert_frame_equal(gen_sue_name_df, e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_label_df, e1_label_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_way_df, e1_way_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_tag_df, e1_tag_agg_df)
