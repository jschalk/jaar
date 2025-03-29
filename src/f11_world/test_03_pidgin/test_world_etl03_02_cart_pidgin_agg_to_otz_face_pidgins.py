from src.f00_instrument.file import create_path
from src.f04_stand.atom_config import face_name_str, event_int_str
from src.f08_pidgin.pidgin_config import (
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_label_str,
    otx_label_str,
    inx_title_str,
    otx_title_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)
from src.f09_idea.idea_db_tool import sheet_exists, upsert_sheet
from src.f10_etl.tran_path import create_cart_pidgin_path, create_otx_face_pidgin_path
from src.f10_etl.pidgin_agg import PidginPrimeColumns
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_cart_pidgin_agg_to_otz_face_dirs_Scenario1_AllMapDimens(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_otx = "Bob"
    sue_str = "Sue"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    event7 = 7
    name_agg_str = "name_agg"

    name_agg_columns = PidginPrimeColumns().map_name_agg_columns
    x_nan = float("nan")
    e1_name0 = [sue_str, event7, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    e1_name1 = [sue_str, event7, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_agg_df = DataFrame(e1_name_rows, columns=name_agg_columns)

    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    event7 = 7
    label_agg_str = "label_agg"
    label_file_columns = PidginPrimeColumns().map_label_agg_columns
    e1_label0 = [sue_str, event7, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_label1 = [sue_str, event7, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_file_columns)

    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    road_agg_str = "road_agg"
    road_file_columns = [
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road_rows = [e1_road0, e1_road1]
    e1_road_agg_df = DataFrame(e1_road_rows, columns=road_file_columns)

    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    title_agg_str = "title_agg"
    title_file_columns = [
        face_name_str(),
        event_int_str(),
        otx_title_str(),
        inx_title_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    e1_title0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_title1 = [sue_str, event7, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_title_rows = [e1_title0, e1_title1]
    e1_title_agg_df = DataFrame(e1_title_rows, columns=title_file_columns)

    agg_pidgin_path = create_cart_pidgin_path(fizz_world._cart_dir)
    upsert_sheet(agg_pidgin_path, name_agg_str, e1_name_agg_df)
    upsert_sheet(agg_pidgin_path, label_agg_str, e1_label_agg_df)
    upsert_sheet(agg_pidgin_path, road_agg_str, e1_road_agg_df)
    upsert_sheet(agg_pidgin_path, title_agg_str, e1_title_agg_df)
    sue_dir = create_path(fizz_world._faces_otz_dir, sue_str)
    faces_otz_dir = fizz_world._faces_otz_dir
    sue_pidgin_file_path = create_otx_face_pidgin_path(faces_otz_dir, sue_str)
    assert os_path_exists(sue_pidgin_file_path) is False

    # WHEN
    fizz_world.cart_pidgin_agg_to_otz_face_dirs()

    # THEN
    assert os_path_exists(sue_dir)
    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, name_agg_str)
    assert sheet_exists(sue_pidgin_file_path, label_agg_str)
    assert sheet_exists(sue_pidgin_file_path, title_agg_str)
    assert sheet_exists(sue_pidgin_file_path, road_agg_str)
    gen_sue_name_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=name_agg_str)
    gen_sue_label_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=label_agg_str)
    gen_sue_title_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=title_agg_str)
    gen_sue_road_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=road_agg_str)
    print(f"{gen_sue_title_df=}")

    pandas_testing_assert_frame_equal(gen_sue_name_df, e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_label_df, e1_label_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_road_df, e1_road_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_title_df, e1_title_agg_df)
