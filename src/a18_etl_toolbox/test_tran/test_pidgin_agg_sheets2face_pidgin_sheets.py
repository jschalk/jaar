from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_creed_logic.creed_db_tool import upsert_sheet, sheet_exists
from src.a18_etl_toolbox.tran_path import (
    create_brick_pidgin_path,
    create_syntax_otx_pidgin_path,
)
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import (
    etl_brick_pidgin_agg_df_to_otz_face_pidgin_agg_df,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_brick_pidgin_agg_df_to_otz_face_pidgin_agg_df_Scenario0_Two_face_names(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    bob_otx = "Bob"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    event7 = 7
    name_agg_str = "name_agg"

    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    x_nan = float("nan")
    name0 = [event7, sue_str, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    name1 = [event7, sue_str, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    name2 = [event7, zia_str, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    name3 = [event7, zia_str, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    name_rows = [name0, name1, name2, name3]
    e1_name_agg_df = DataFrame(name_rows, columns=name_agg_columns)

    brick_dir = create_path(get_module_temp_dir(), "brick")
    agg_pidgin_path = create_brick_pidgin_path(brick_dir)
    upsert_sheet(agg_pidgin_path, name_agg_str, e1_name_agg_df)

    faces_dir = create_path(get_module_temp_dir(), "syntax_otz")

    # WHEN
    etl_brick_pidgin_agg_df_to_otz_face_pidgin_agg_df(brick_dir, faces_dir)

    # THEN
    sue_dir = create_path(faces_dir, sue_str)
    zia_dir = create_path(faces_dir, zia_str)
    assert os_path_exists(sue_dir)
    assert os_path_exists(zia_dir)
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
    zia_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, zia_str)
    assert os_path_exists(sue_pidgin_file_path)
    assert os_path_exists(zia_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, name_agg_str)
    assert sheet_exists(zia_pidgin_file_path, name_agg_str)
    gen_sue_name_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=name_agg_str)
    gen_zia_name_df = pandas_read_excel(zia_pidgin_file_path, sheet_name=name_agg_str)

    e1_sue_name_agg_df = DataFrame([name0, name1], columns=name_agg_columns)
    e1_zia_name_agg_df = DataFrame([name2, name3], columns=name_agg_columns)

    pandas_testing_assert_frame_equal(gen_sue_name_df, e1_sue_name_agg_df)
    pandas_testing_assert_frame_equal(gen_zia_name_df, e1_zia_name_agg_df)


def test_etl_brick_pidgin_agg_df_to_otz_face_pidgin_agg_df_Scenario1_AllMapDimens(
    env_dir_setup_cleanup,
):
    # ESTABLISH
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
    title_agg_str = "title_agg"
    title_agg_columns = PidginPrimeColumns().pidgin_title_agg_columns
    e1_title0 = [event7, sue_str, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_title1 = [event7, sue_str, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_title_rows = [e1_title0, e1_title1]
    e1_title_agg_df = DataFrame(e1_title_rows, columns=title_agg_columns)

    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    way_agg_str = "way_agg"
    way_agg_columns = PidginPrimeColumns().pidgin_way_agg_columns
    e1_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way_rows = [e1_way0, e1_way1]
    e1_way_agg_df = DataFrame(e1_way_rows, columns=way_agg_columns)

    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    word_agg_str = "word_agg"
    word_agg_columns = PidginPrimeColumns().pidgin_word_agg_columns
    e1_word0 = [event7, sue_str, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_word1 = [event7, sue_str, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_word_rows = [e1_word0, e1_word1]
    e1_word_agg_df = DataFrame(e1_word_rows, columns=word_agg_columns)

    brick_dir = create_path(get_module_temp_dir(), "brick")
    agg_pidgin_path = create_brick_pidgin_path(brick_dir)
    upsert_sheet(agg_pidgin_path, name_agg_str, e1_name_agg_df)
    upsert_sheet(agg_pidgin_path, title_agg_str, e1_title_agg_df)
    upsert_sheet(agg_pidgin_path, way_agg_str, e1_way_agg_df)
    upsert_sheet(agg_pidgin_path, word_agg_str, e1_word_agg_df)

    faces_dir = create_path(get_module_temp_dir(), "syntax_otz")

    # WHEN
    etl_brick_pidgin_agg_df_to_otz_face_pidgin_agg_df(brick_dir, faces_dir)

    # THEN
    sue_dir = create_path(faces_dir, sue_str)
    assert os_path_exists(sue_dir)
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
    print(f"{sue_pidgin_file_path=}")

    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, name_agg_str)
    assert sheet_exists(sue_pidgin_file_path, title_agg_str)
    assert sheet_exists(sue_pidgin_file_path, word_agg_str)
    assert sheet_exists(sue_pidgin_file_path, way_agg_str)
    gen_sue_name_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=name_agg_str)
    gen_sue_title_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=title_agg_str)
    gen_sue_word_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=word_agg_str)
    gen_sue_way_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=way_agg_str)
    print(f"{gen_sue_word_df=}")

    pandas_testing_assert_frame_equal(gen_sue_name_df, e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_title_df, e1_title_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_way_df, e1_way_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_word_df, e1_word_agg_df)
