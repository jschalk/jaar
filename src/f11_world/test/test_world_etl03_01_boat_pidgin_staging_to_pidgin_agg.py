from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_name_str
from src.f08_pidgin.pidgin_config import (
    event_int_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_label_str,
    otx_label_str,
    inx_road_str,
    otx_road_str,
    inx_idea_str,
    otx_idea_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import upsert_sheet, sheet_exists
from src.f10_etl.pidgin_agg import PidginPrimeColumns
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_pidgin_staging_to_name_agg_Scenario0_CreatesFileWithAllCategorys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    event7 = 7
    name_staging_str = "name_staging"
    name_agg_str = "name_agg"
    name_staging_columns = PidginPrimeColumns().map_name_staging_columns
    bx = "br00xxx"
    e1_name0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_name1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_name_rows = [e1_name0, e1_name1]
    staging_name_df = DataFrame(e1_name_rows, columns=name_staging_columns)

    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    event7 = 7
    label_staging_str = "label_staging"
    label_agg_str = "label_agg"
    label_file_columns = PidginPrimeColumns().map_label_staging_columns
    bx = "br00xxx"
    e1_label0 = [bx, sue_str, event7, jog_str, jog_inx, None, None, None]
    e1_label1 = [bx, sue_str, event7, run_str, run_inx, None, None, None]
    e1_label_rows = [e1_label0, e1_label1]
    staging_label_df = DataFrame(e1_label_rows, columns=label_file_columns)

    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    road_staging_str = "road_staging"
    road_agg_str = "road_agg"
    road_file_columns = [
        "src_brick",
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    bx = "br00xxx"
    e1_road0 = [bx, sue_str, event7, casa_otx, casa_inx, None, None, None]
    e1_road1 = [bx, sue_str, event7, clean_otx, clean_inx, None, None, None]
    e1_road_rows = [e1_road0, e1_road1]
    staging_road_df = DataFrame(e1_road_rows, columns=road_file_columns)

    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    idea_staging_str = "idea_staging"
    idea_agg_str = "idea_agg"
    idea_file_columns = [
        "src_brick",
        face_name_str(),
        event_int_str(),
        otx_idea_str(),
        inx_idea_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    bx = "br00xxx"
    e1_idea0 = [bx, sue_str, event7, t3am_otx, t3am_inx, None, None, None]
    e1_idea1 = [bx, sue_str, event7, t6am_otx, t6am_inx, None, None, None]
    e1_idea_rows = [e1_idea0, e1_idea1]
    staging_idea_df = DataFrame(e1_idea_rows, columns=idea_file_columns)

    pidgin_path = create_path(fizz_world._boat_dir, "pidgin.xlsx")
    upsert_sheet(pidgin_path, name_staging_str, staging_name_df)
    upsert_sheet(pidgin_path, label_staging_str, staging_label_df)
    upsert_sheet(pidgin_path, road_staging_str, staging_road_df)
    upsert_sheet(pidgin_path, idea_staging_str, staging_idea_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_staging_str)
    assert sheet_exists(pidgin_path, label_staging_str)
    assert sheet_exists(pidgin_path, road_staging_str)
    assert sheet_exists(pidgin_path, idea_staging_str)
    assert sheet_exists(pidgin_path, name_agg_str) is False
    assert sheet_exists(pidgin_path, label_agg_str) is False
    assert sheet_exists(pidgin_path, road_agg_str) is False
    assert sheet_exists(pidgin_path, idea_agg_str) is False

    # WHEN
    fizz_world.boat_pidgin_staging_to_agg()

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_agg_str)
    assert sheet_exists(pidgin_path, label_agg_str)
    assert sheet_exists(pidgin_path, road_agg_str)
    assert sheet_exists(pidgin_path, idea_agg_str)
    gen_name_agg_df = pandas_read_excel(pidgin_path, sheet_name=name_agg_str)
    gen_label_agg_df = pandas_read_excel(pidgin_path, sheet_name=label_agg_str)
    gen_road_agg_df = pandas_read_excel(pidgin_path, sheet_name=road_agg_str)
    gen_idea_agg_df = pandas_read_excel(pidgin_path, sheet_name=idea_agg_str)

    name_agg_columns = PidginPrimeColumns().map_name_agg_columns
    assert list(gen_name_agg_df.columns) == name_agg_columns
    assert len(gen_name_agg_df) == 2
    x_nan = float("nan")
    e1_name0 = [sue_str, event7, yao_str, yao_inx, x_nan, x_nan, x_nan]
    e1_name1 = [sue_str, event7, bob_str, bob_inx, x_nan, x_nan, x_nan]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_agg_df = DataFrame(e1_name_rows, columns=name_agg_columns)

    label_file_columns = PidginPrimeColumns().map_label_staging_columns
    assert list(gen_label_agg_df.columns) == label_file_columns
    assert len(gen_label_agg_df) == 2
    e1_label0 = [sue_str, event7, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_label1 = [sue_str, event7, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_file_columns)

    road_file_columns = [
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_road_agg_df.columns) == road_file_columns
    assert len(gen_road_agg_df) == 2
    e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road_rows = [e1_road0, e1_road1]
    e1_road_agg_df = DataFrame(e1_road_rows, columns=road_file_columns)

    idea_file_columns = [
        face_name_str(),
        event_int_str(),
        otx_idea_str(),
        inx_idea_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_idea_agg_df.columns) == idea_file_columns
    assert len(gen_idea_agg_df) == 2
    e1_idea0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_idea1 = [sue_str, event7, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_idea_rows = [e1_idea0, e1_idea1]
    e1_idea_agg_df = DataFrame(e1_idea_rows, columns=idea_file_columns)

    pandas_testing_assert_frame_equal(gen_name_agg_df, e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_label_agg_df, e1_label_agg_df)
    pandas_testing_assert_frame_equal(gen_road_agg_df, e1_road_agg_df)
    pandas_testing_assert_frame_equal(gen_idea_agg_df, e1_idea_agg_df)
