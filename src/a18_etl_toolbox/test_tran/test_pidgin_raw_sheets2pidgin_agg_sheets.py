from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_idea_logic.idea_db_tool import upsert_sheet, sheet_exists
from src.a18_etl_toolbox.tran_path import create_brick_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import (
    etl_pidgin_name_raw_to_name_agg,
    etl_pidgin_label_raw_to_label_agg,
    etl_pidgin_tag_raw_to_tag_agg,
    etl_pidgin_road_raw_to_road_agg,
    etl_brick_pidgin_raw_df_to_pidgin_agg_df,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_pidgin_name_raw_to_name_agg_Scenario0_CreatesEmptyFileBecauseOfConflict(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    event7 = 7
    name_raw_str = "name_raw"
    name_agg_str = "name_agg"
    colon_str = ":"
    slash_str = "/"
    name_raw_columns = PidginPrimeColumns().pidgin_name_raw_columns
    bx = "br00xxx"
    e1_name0 = [bx, sue_str, event7, yao_str, yao_inx, None, colon_str, None]
    e1_name1 = [bx, sue_str, event7, bob_str, bob_inx, None, slash_str, None]
    e1_name_rows = [e1_name0, e1_name1]
    raw_name_df = DataFrame(e1_name_rows, columns=name_raw_columns)
    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, name_raw_str, raw_name_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_raw_str)
    assert sheet_exists(pidgin_path, name_agg_str) is False

    # WHEN
    etl_pidgin_name_raw_to_name_agg(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_agg_str)
    gen_name_agg_df = pandas_read_excel(pidgin_path, sheet_name=name_agg_str)
    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    assert list(gen_name_agg_df.columns) == name_agg_columns
    assert len(gen_name_agg_df) == 0
    e1_name_agg_df = DataFrame([], columns=name_agg_columns)
    pandas_testing_assert_frame_equal(gen_name_agg_df, e1_name_agg_df)


def test_etl_pidgin_name_raw_to_name_agg_Scenario1_CreatesFileFromSingleIdea(
    env_dir_setup_cleanup,
):
    # ESTABLISH
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
    e1_name0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_name1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_name_rows = [e1_name0, e1_name1]
    raw_name_df = DataFrame(e1_name_rows, columns=name_raw_columns)
    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, name_raw_str, raw_name_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_raw_str)
    assert sheet_exists(pidgin_path, name_agg_str) is False

    # WHEN
    etl_pidgin_name_raw_to_name_agg(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_agg_str)
    gen_name_agg_df = pandas_read_excel(pidgin_path, sheet_name=name_agg_str)
    print(f"{gen_name_agg_df=}")
    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    assert list(gen_name_agg_df.columns) == name_agg_columns
    assert len(gen_name_agg_df) == 2
    x_nan = float("nan")
    e1_name0 = [sue_str, event7, yao_str, yao_inx, x_nan, x_nan, x_nan]
    e1_name1 = [sue_str, event7, bob_str, bob_inx, x_nan, x_nan, x_nan]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_agg_df = DataFrame(e1_name_rows, columns=name_agg_columns)
    pandas_testing_assert_frame_equal(gen_name_agg_df, e1_name_agg_df)


def test_etl_pidgin_label_raw_to_label_agg_Scenario0_CreatesFileFromSingleIdea(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    event7 = 7
    label_raw_str = "label_raw"
    label_agg_str = "label_agg"
    label_raw_columns = PidginPrimeColumns().pidgin_label_raw_columns
    bx = "br00xxx"
    e1_label0 = [bx, sue_str, event7, jog_str, jog_inx, None, None, None]
    e1_label1 = [bx, sue_str, event7, run_str, run_inx, None, None, None]
    e1_label_rows = [e1_label0, e1_label1]
    raw_label_df = DataFrame(e1_label_rows, columns=label_raw_columns)
    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, label_raw_str, raw_label_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, label_raw_str)
    assert sheet_exists(pidgin_path, label_agg_str) is False

    # WHEN
    etl_pidgin_label_raw_to_label_agg(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, label_agg_str)
    gen_label_agg_df = pandas_read_excel(pidgin_path, sheet_name=label_agg_str)
    print(f"{gen_label_agg_df=}")
    label_agg_columns = PidginPrimeColumns().pidgin_label_agg_columns
    assert list(gen_label_agg_df.columns) == label_agg_columns
    assert len(gen_label_agg_df) == 2
    x_nan = float("nan")
    e1_label0 = [sue_str, event7, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_label1 = [sue_str, event7, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_agg_columns)
    pandas_testing_assert_frame_equal(gen_label_agg_df, e1_label_agg_df)


def test_etl_pidgin_road_raw_to_road_agg_Scenario0_CreatesFileFromSingleIdea(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    road_raw_str = "road_raw"
    road_agg_str = "road_agg"
    road_raw_columns = PidginPrimeColumns().pidgin_road_raw_columns
    bx = "br00xxx"
    e1_road0 = [bx, sue_str, event7, casa_otx, casa_inx, None, None, None]
    e1_road1 = [bx, sue_str, event7, clean_otx, clean_inx, None, None, None]
    e1_road_rows = [e1_road0, e1_road1]
    raw_road_df = DataFrame(e1_road_rows, columns=road_raw_columns)
    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, road_raw_str, raw_road_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, road_raw_str)
    assert sheet_exists(pidgin_path, road_agg_str) is False

    # WHEN
    etl_pidgin_road_raw_to_road_agg(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, road_agg_str)
    gen_road_agg_df = pandas_read_excel(pidgin_path, sheet_name=road_agg_str)
    print(f"{gen_road_agg_df=}")
    road_agg_columns = PidginPrimeColumns().pidgin_road_agg_columns
    assert list(gen_road_agg_df.columns) == road_agg_columns
    assert len(gen_road_agg_df) == 2
    x_nan = float("nan")
    e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road_rows = [e1_road0, e1_road1]
    e1_road_agg_df = DataFrame(e1_road_rows, columns=road_agg_columns)
    pandas_testing_assert_frame_equal(gen_road_agg_df, e1_road_agg_df)


def test_etl_pidgin_tag_raw_to_tag_agg_Scenario0_CreatesFileFromSingleIdea(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    tag_raw_str = "tag_raw"
    tag_agg_str = "tag_agg"
    tag_raw_columns = PidginPrimeColumns().pidgin_tag_raw_columns
    bx = "br00xxx"
    e1_tag0 = [bx, sue_str, event7, t3am_otx, t3am_inx, None, None, None]
    e1_tag1 = [bx, sue_str, event7, t6am_otx, t6am_inx, None, None, None]
    e1_tag_rows = [e1_tag0, e1_tag1]
    raw_tag_df = DataFrame(e1_tag_rows, columns=tag_raw_columns)
    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, tag_raw_str, raw_tag_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, tag_raw_str)
    assert sheet_exists(pidgin_path, tag_agg_str) is False

    # WHEN
    etl_pidgin_tag_raw_to_tag_agg(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, tag_agg_str)
    gen_tag_agg_df = pandas_read_excel(pidgin_path, sheet_name=tag_agg_str)
    print(f"{gen_tag_agg_df=}")
    tag_agg_columns = PidginPrimeColumns().pidgin_tag_agg_columns
    assert list(gen_tag_agg_df.columns) == tag_agg_columns
    assert len(gen_tag_agg_df) == 2
    x_nan = float("nan")
    e1_tag0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_tag1 = [sue_str, event7, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_tag_rows = [e1_tag0, e1_tag1]
    e1_tag_agg_df = DataFrame(e1_tag_rows, columns=tag_agg_columns)
    pandas_testing_assert_frame_equal(gen_tag_agg_df, e1_tag_agg_df)


def test_etl_brick_pidgin_raw_df_to_pidgin_agg_df_Scenario0_CreatesFileWithAllDimens(
    env_dir_setup_cleanup,
):
    # ESTABLISH
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
    e1_name0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_name1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_name_rows = [e1_name0, e1_name1]
    raw_name_df = DataFrame(e1_name_rows, columns=name_raw_columns)

    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    event7 = 7
    label_raw_str = "label_raw"
    label_agg_str = "label_agg"
    label_raw_columns = PidginPrimeColumns().pidgin_label_raw_columns
    bx = "br00xxx"
    e1_label0 = [bx, sue_str, event7, jog_str, jog_inx, None, None, None]
    e1_label1 = [bx, sue_str, event7, run_str, run_inx, None, None, None]
    e1_label_rows = [e1_label0, e1_label1]
    raw_label_df = DataFrame(e1_label_rows, columns=label_raw_columns)

    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    road_raw_str = "road_raw"
    road_agg_str = "road_agg"
    road_raw_columns = PidginPrimeColumns().pidgin_road_raw_columns
    bx = "br00xxx"
    e1_road0 = [bx, sue_str, event7, casa_otx, casa_inx, None, None, None]
    e1_road1 = [bx, sue_str, event7, clean_otx, clean_inx, None, None, None]
    e1_road_rows = [e1_road0, e1_road1]
    raw_road_df = DataFrame(e1_road_rows, columns=road_raw_columns)

    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    tag_raw_str = "tag_raw"
    tag_agg_str = "tag_agg"
    tag_raw_columns = PidginPrimeColumns().pidgin_tag_raw_columns
    bx = "br00xxx"
    e1_tag0 = [bx, sue_str, event7, t3am_otx, t3am_inx, None, None, None]
    e1_tag1 = [bx, sue_str, event7, t6am_otx, t6am_inx, None, None, None]
    e1_tag_rows = [e1_tag0, e1_tag1]
    raw_tag_df = DataFrame(e1_tag_rows, columns=tag_raw_columns)

    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, name_raw_str, raw_name_df)
    upsert_sheet(pidgin_path, label_raw_str, raw_label_df)
    upsert_sheet(pidgin_path, road_raw_str, raw_road_df)
    upsert_sheet(pidgin_path, tag_raw_str, raw_tag_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_raw_str)
    assert sheet_exists(pidgin_path, label_raw_str)
    assert sheet_exists(pidgin_path, road_raw_str)
    assert sheet_exists(pidgin_path, tag_raw_str)
    assert sheet_exists(pidgin_path, name_agg_str) is False
    assert sheet_exists(pidgin_path, label_agg_str) is False
    assert sheet_exists(pidgin_path, road_agg_str) is False
    assert sheet_exists(pidgin_path, tag_agg_str) is False

    # WHEN
    etl_brick_pidgin_raw_df_to_pidgin_agg_df(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_agg_str)
    assert sheet_exists(pidgin_path, label_agg_str)
    assert sheet_exists(pidgin_path, road_agg_str)
    assert sheet_exists(pidgin_path, tag_agg_str)
    gen_name_agg_df = pandas_read_excel(pidgin_path, sheet_name=name_agg_str)
    gen_label_agg_df = pandas_read_excel(pidgin_path, sheet_name=label_agg_str)
    gen_road_agg_df = pandas_read_excel(pidgin_path, sheet_name=road_agg_str)
    gen_tag_agg_df = pandas_read_excel(pidgin_path, sheet_name=tag_agg_str)

    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    assert list(gen_name_agg_df.columns) == name_agg_columns
    assert len(gen_name_agg_df) == 2
    x_nan = float("nan")
    e1_name0 = [sue_str, event7, yao_str, yao_inx, x_nan, x_nan, x_nan]
    e1_name1 = [sue_str, event7, bob_str, bob_inx, x_nan, x_nan, x_nan]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_agg_df = DataFrame(e1_name_rows, columns=name_agg_columns)

    label_agg_columns = PidginPrimeColumns().pidgin_label_agg_columns
    assert list(gen_label_agg_df.columns) == label_agg_columns
    assert len(gen_label_agg_df) == 2
    e1_label0 = [sue_str, event7, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_label1 = [sue_str, event7, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_agg_columns)

    road_agg_columns = PidginPrimeColumns().pidgin_road_agg_columns
    assert list(gen_road_agg_df.columns) == road_agg_columns
    assert len(gen_road_agg_df) == 2
    e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road_rows = [e1_road0, e1_road1]
    e1_road_agg_df = DataFrame(e1_road_rows, columns=road_agg_columns)

    tag_agg_columns = PidginPrimeColumns().pidgin_tag_agg_columns
    assert list(gen_tag_agg_df.columns) == tag_agg_columns
    assert len(gen_tag_agg_df) == 2
    e1_tag0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_tag1 = [sue_str, event7, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_tag_rows = [e1_tag0, e1_tag1]
    e1_tag_agg_df = DataFrame(e1_tag_rows, columns=tag_agg_columns)

    pandas_testing_assert_frame_equal(gen_name_agg_df, e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_label_agg_df, e1_label_agg_df)
    pandas_testing_assert_frame_equal(gen_road_agg_df, e1_road_agg_df)
    pandas_testing_assert_frame_equal(gen_tag_agg_df, e1_tag_agg_df)
