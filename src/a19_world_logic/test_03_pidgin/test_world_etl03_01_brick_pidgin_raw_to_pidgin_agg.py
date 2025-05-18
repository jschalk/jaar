from src.a17_idea_logic.idea_db_tool import upsert_sheet, sheet_exists
from src.a18_etl_toolbox.tran_path import create_brick_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_WorldUnit_pidgin_raw_to_name_agg_Scenario0_CreatesFileWithAllDimens(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    event7 = 7
    name_raw_str = "name_raw"
    name_agg_str = "name_agg"
    name_raw_columns = PidginPrimeColumns().pidgin_name_raw_columns
    bx = "br00xxx"
    e1_name0 = [bx, event7, sue_str, yao_str, yao_inx, None, None, None]
    e1_name1 = [bx, event7, sue_str, bob_str, bob_inx, None, None, None]
    e1_name_rows = [e1_name0, e1_name1]
    raw_name_df = DataFrame(e1_name_rows, columns=name_raw_columns)

    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    event7 = 7
    title_raw_str = "title_raw"
    title_agg_str = "title_agg"
    title_raw_columns = PidginPrimeColumns().pidgin_title_raw_columns
    bx = "br00xxx"
    e1_title0 = [bx, event7, sue_str, jog_str, jog_inx, None, None, None]
    e1_title1 = [bx, event7, sue_str, run_str, run_inx, None, None, None]
    e1_title_rows = [e1_title0, e1_title1]
    raw_title_df = DataFrame(e1_title_rows, columns=title_raw_columns)

    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    way_raw_str = "way_raw"
    way_agg_str = "way_agg"
    way_raw_columns = PidginPrimeColumns().pidgin_way_raw_columns
    bx = "br00xxx"
    e1_way0 = [bx, event7, sue_str, casa_otx, casa_inx, None, None, None]
    e1_way1 = [bx, event7, sue_str, clean_otx, clean_inx, None, None, None]
    e1_way_rows = [e1_way0, e1_way1]
    raw_way_df = DataFrame(e1_way_rows, columns=way_raw_columns)

    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    label_raw_str = "label_raw"
    label_agg_str = "label_agg"
    label_raw_columns = PidginPrimeColumns().pidgin_label_raw_columns
    bx = "br00xxx"
    e1_label0 = [bx, event7, sue_str, t3am_otx, t3am_inx, None, None, None]
    e1_label1 = [bx, event7, sue_str, t6am_otx, t6am_inx, None, None, None]
    e1_label_rows = [e1_label0, e1_label1]
    raw_label_df = DataFrame(e1_label_rows, columns=label_raw_columns)

    pidgin_path = create_brick_pidgin_path(fizz_world._brick_dir)
    upsert_sheet(pidgin_path, name_raw_str, raw_name_df)
    upsert_sheet(pidgin_path, title_raw_str, raw_title_df)
    upsert_sheet(pidgin_path, way_raw_str, raw_way_df)
    upsert_sheet(pidgin_path, label_raw_str, raw_label_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_raw_str)
    assert sheet_exists(pidgin_path, title_raw_str)
    assert sheet_exists(pidgin_path, way_raw_str)
    assert sheet_exists(pidgin_path, label_raw_str)
    assert sheet_exists(pidgin_path, name_agg_str) is False
    assert sheet_exists(pidgin_path, title_agg_str) is False
    assert sheet_exists(pidgin_path, way_agg_str) is False
    assert sheet_exists(pidgin_path, label_agg_str) is False

    # WHEN
    fizz_world.brick_pidgin_raw_df_to_pidgin_agg_df()

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_agg_str)
    assert sheet_exists(pidgin_path, title_agg_str)
    assert sheet_exists(pidgin_path, way_agg_str)
    assert sheet_exists(pidgin_path, label_agg_str)
    gen_name_agg_df = pandas_read_excel(pidgin_path, sheet_name=name_agg_str)
    gen_title_agg_df = pandas_read_excel(pidgin_path, sheet_name=title_agg_str)
    gen_way_agg_df = pandas_read_excel(pidgin_path, sheet_name=way_agg_str)
    gen_label_agg_df = pandas_read_excel(pidgin_path, sheet_name=label_agg_str)

    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    assert list(gen_name_agg_df.columns) == name_agg_columns
    assert len(gen_name_agg_df) == 2
    x_nan = float("nan")
    e1_name0 = [event7, sue_str, yao_str, yao_inx, x_nan, x_nan, x_nan]
    e1_name1 = [event7, sue_str, bob_str, bob_inx, x_nan, x_nan, x_nan]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_agg_df = DataFrame(e1_name_rows, columns=name_agg_columns)

    title_agg_columns = PidginPrimeColumns().pidgin_title_agg_columns
    assert list(gen_title_agg_df.columns) == title_agg_columns
    assert len(gen_title_agg_df) == 2
    e1_title0 = [event7, sue_str, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_title1 = [event7, sue_str, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_title_rows = [e1_title0, e1_title1]
    e1_title_agg_df = DataFrame(e1_title_rows, columns=title_agg_columns)

    way_agg_columns = PidginPrimeColumns().pidgin_way_agg_columns
    assert list(gen_way_agg_df.columns) == way_agg_columns
    assert len(gen_way_agg_df) == 2
    e1_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way_rows = [e1_way0, e1_way1]
    e1_way_agg_df = DataFrame(e1_way_rows, columns=way_agg_columns)
    label_agg_columns = PidginPrimeColumns().pidgin_label_agg_columns
    assert list(gen_label_agg_df.columns) == label_agg_columns
    assert len(gen_label_agg_df) == 2
    e1_label0 = [event7, sue_str, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_label1 = [event7, sue_str, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_agg_columns)

    pandas_testing_assert_frame_equal(gen_name_agg_df, e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_title_agg_df, e1_title_agg_df)
    pandas_testing_assert_frame_equal(gen_way_agg_df, e1_way_agg_df)
    pandas_testing_assert_frame_equal(gen_label_agg_df, e1_label_agg_df)
