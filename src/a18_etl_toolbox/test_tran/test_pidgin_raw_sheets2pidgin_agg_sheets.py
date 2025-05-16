from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_creed_logic.creed_db_tool import upsert_sheet, sheet_exists
from src.a18_etl_toolbox.tran_path import create_brick_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import (
    etl_pidgin_name_raw_to_name_agg,
    etl_pidgin_label_raw_to_label_agg,
    etl_pidgin_word_raw_to_word_agg,
    etl_pidgin_way_raw_to_way_agg,
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
    e1_name0 = [bx, event7, sue_str, yao_str, yao_inx, None, colon_str, None]
    e1_name1 = [bx, event7, sue_str, bob_str, bob_inx, None, slash_str, None]
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


def test_etl_pidgin_name_raw_to_name_agg_Scenario1_CreatesFileFromSingleCreed(
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
    e1_name0 = [bx, event7, sue_str, yao_str, yao_inx, None, None, None]
    e1_name1 = [bx, event7, sue_str, bob_str, bob_inx, None, None, None]
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
    assert len(gen_name_agg_df) == 2
    x_nan = float("nan")
    e1_name0 = [event7, sue_str, yao_str, yao_inx, x_nan, x_nan, x_nan]
    e1_name1 = [event7, sue_str, bob_str, bob_inx, x_nan, x_nan, x_nan]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_agg_df = DataFrame(e1_name_rows, columns=name_agg_columns)
    print(gen_name_agg_df)
    print(e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_name_agg_df, e1_name_agg_df)


def test_etl_pidgin_label_raw_to_label_agg_Scenario0_CreatesFileFromSingleCreed(
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
    e1_label0 = [bx, event7, sue_str, jog_str, jog_inx, None, None, None]
    e1_label1 = [bx, event7, sue_str, run_str, run_inx, None, None, None]
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
    e1_label0 = [event7, sue_str, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_label1 = [event7, sue_str, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_agg_columns)
    pandas_testing_assert_frame_equal(gen_label_agg_df, e1_label_agg_df)


def test_etl_pidgin_way_raw_to_way_agg_Scenario0_CreatesFileFromSingleCreed(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
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
    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, way_raw_str, raw_way_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, way_raw_str)
    assert sheet_exists(pidgin_path, way_agg_str) is False

    # WHEN
    etl_pidgin_way_raw_to_way_agg(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, way_agg_str)
    gen_way_agg_df = pandas_read_excel(pidgin_path, sheet_name=way_agg_str)
    print(f"{gen_way_agg_df=}")
    way_agg_columns = PidginPrimeColumns().pidgin_way_agg_columns
    assert list(gen_way_agg_df.columns) == way_agg_columns
    assert len(gen_way_agg_df) == 2
    x_nan = float("nan")
    e1_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way_rows = [e1_way0, e1_way1]
    e1_way_agg_df = DataFrame(e1_way_rows, columns=way_agg_columns)
    pandas_testing_assert_frame_equal(gen_way_agg_df, e1_way_agg_df)


def test_etl_pidgin_word_raw_to_word_agg_Scenario0_CreatesFileFromSingleCreed(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    word_raw_str = "word_raw"
    word_agg_str = "word_agg"
    word_raw_columns = PidginPrimeColumns().pidgin_word_raw_columns
    bx = "br00xxx"
    e1_word0 = [bx, event7, sue_str, t3am_otx, t3am_inx, None, None, None]
    e1_word1 = [bx, event7, sue_str, t6am_otx, t6am_inx, None, None, None]
    e1_word_rows = [e1_word0, e1_word1]
    raw_word_df = DataFrame(e1_word_rows, columns=word_raw_columns)
    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, word_raw_str, raw_word_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, word_raw_str)
    assert sheet_exists(pidgin_path, word_agg_str) is False

    # WHEN
    etl_pidgin_word_raw_to_word_agg(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, word_agg_str)
    gen_word_agg_df = pandas_read_excel(pidgin_path, sheet_name=word_agg_str)
    print(f"{gen_word_agg_df=}")
    word_agg_columns = PidginPrimeColumns().pidgin_word_agg_columns
    assert list(gen_word_agg_df.columns) == word_agg_columns
    assert len(gen_word_agg_df) == 2
    x_nan = float("nan")
    e1_word0 = [event7, sue_str, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_word1 = [event7, sue_str, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_word_rows = [e1_word0, e1_word1]
    e1_word_agg_df = DataFrame(e1_word_rows, columns=word_agg_columns)
    pandas_testing_assert_frame_equal(gen_word_agg_df, e1_word_agg_df)


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
    e1_name0 = [bx, event7, sue_str, yao_str, yao_inx, None, None, None]
    e1_name1 = [bx, event7, sue_str, bob_str, bob_inx, None, None, None]
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
    e1_label0 = [bx, event7, sue_str, jog_str, jog_inx, None, None, None]
    e1_label1 = [bx, event7, sue_str, run_str, run_inx, None, None, None]
    e1_label_rows = [e1_label0, e1_label1]
    raw_label_df = DataFrame(e1_label_rows, columns=label_raw_columns)

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
    word_raw_str = "word_raw"
    word_agg_str = "word_agg"
    word_raw_columns = PidginPrimeColumns().pidgin_word_raw_columns
    bx = "br00xxx"
    e1_word0 = [bx, event7, sue_str, t3am_otx, t3am_inx, None, None, None]
    e1_word1 = [bx, event7, sue_str, t6am_otx, t6am_inx, None, None, None]
    e1_word_rows = [e1_word0, e1_word1]
    raw_word_df = DataFrame(e1_word_rows, columns=word_raw_columns)

    x_brick_dir = get_module_temp_dir()
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    upsert_sheet(pidgin_path, name_raw_str, raw_name_df)
    upsert_sheet(pidgin_path, label_raw_str, raw_label_df)
    upsert_sheet(pidgin_path, way_raw_str, raw_way_df)
    upsert_sheet(pidgin_path, word_raw_str, raw_word_df)
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_raw_str)
    assert sheet_exists(pidgin_path, label_raw_str)
    assert sheet_exists(pidgin_path, way_raw_str)
    assert sheet_exists(pidgin_path, word_raw_str)
    assert sheet_exists(pidgin_path, name_agg_str) is False
    assert sheet_exists(pidgin_path, label_agg_str) is False
    assert sheet_exists(pidgin_path, way_agg_str) is False
    assert sheet_exists(pidgin_path, word_agg_str) is False

    # WHEN
    etl_brick_pidgin_raw_df_to_pidgin_agg_df(x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    assert sheet_exists(pidgin_path, name_agg_str)
    assert sheet_exists(pidgin_path, label_agg_str)
    assert sheet_exists(pidgin_path, way_agg_str)
    assert sheet_exists(pidgin_path, word_agg_str)
    gen_name_agg_df = pandas_read_excel(pidgin_path, sheet_name=name_agg_str)
    gen_label_agg_df = pandas_read_excel(pidgin_path, sheet_name=label_agg_str)
    gen_way_agg_df = pandas_read_excel(pidgin_path, sheet_name=way_agg_str)
    gen_word_agg_df = pandas_read_excel(pidgin_path, sheet_name=word_agg_str)

    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    assert list(gen_name_agg_df.columns) == name_agg_columns
    assert len(gen_name_agg_df) == 2
    x_nan = float("nan")
    e1_name0 = [event7, sue_str, yao_str, yao_inx, x_nan, x_nan, x_nan]
    e1_name1 = [event7, sue_str, bob_str, bob_inx, x_nan, x_nan, x_nan]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_agg_df = DataFrame(e1_name_rows, columns=name_agg_columns)

    label_agg_columns = PidginPrimeColumns().pidgin_label_agg_columns
    assert list(gen_label_agg_df.columns) == label_agg_columns
    assert len(gen_label_agg_df) == 2
    e1_label0 = [event7, sue_str, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_label1 = [event7, sue_str, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_agg_columns)

    way_agg_columns = PidginPrimeColumns().pidgin_way_agg_columns
    assert list(gen_way_agg_df.columns) == way_agg_columns
    assert len(gen_way_agg_df) == 2
    e1_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way_rows = [e1_way0, e1_way1]
    e1_way_agg_df = DataFrame(e1_way_rows, columns=way_agg_columns)

    word_agg_columns = PidginPrimeColumns().pidgin_word_agg_columns
    assert list(gen_word_agg_df.columns) == word_agg_columns
    assert len(gen_word_agg_df) == 2
    e1_word0 = [event7, sue_str, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_word1 = [event7, sue_str, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_word_rows = [e1_word0, e1_word1]
    e1_word_agg_df = DataFrame(e1_word_rows, columns=word_agg_columns)

    pandas_testing_assert_frame_equal(gen_name_agg_df, e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_label_agg_df, e1_label_agg_df)
    pandas_testing_assert_frame_equal(gen_way_agg_df, e1_way_agg_df)
    pandas_testing_assert_frame_equal(gen_word_agg_df, e1_word_agg_df)
