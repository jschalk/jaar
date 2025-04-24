from src.a00_data_toolboxs.file_toolbox import create_path
from src.a17_idea_logic.idea_db_tool import upsert_sheet, sheet_exists
from src.a18_etl_toolbox.tran_path import (
    create_yell_pidgin_path,
    create_syntax_otx_pidgin_path,
)
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import (
    etl_yell_pidgin_agg_to_otz_face_pidgin_agg,
)
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_yell_pidgin_agg_to_otz_face_pidgin_agg_Scenario0_Two_face_names(
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

    name_agg_columns = PidginPrimeColumns().map_name_agg_columns
    x_nan = float("nan")
    name0 = [sue_str, event7, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    name1 = [sue_str, event7, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    name2 = [zia_str, event7, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    name3 = [zia_str, event7, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    name_rows = [name0, name1, name2, name3]
    e1_name_agg_df = DataFrame(name_rows, columns=name_agg_columns)

    yell_dir = create_path(get_test_etl_dir(), "yell")
    agg_pidgin_path = create_yell_pidgin_path(yell_dir)
    upsert_sheet(agg_pidgin_path, name_agg_str, e1_name_agg_df)

    faces_dir = create_path(get_test_etl_dir(), "syntax_otz")

    # WHEN
    etl_yell_pidgin_agg_to_otz_face_pidgin_agg(yell_dir, faces_dir)

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


def test_etl_yell_pidgin_agg_to_otz_face_pidgin_agg_Scenario1_AllMapDimens(
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
    label_agg_columns = PidginPrimeColumns().map_label_agg_columns
    e1_label0 = [sue_str, event7, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_label1 = [sue_str, event7, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_agg_columns)

    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    road_agg_str = "road_agg"
    road_agg_columns = PidginPrimeColumns().map_road_agg_columns
    e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road_rows = [e1_road0, e1_road1]
    e1_road_agg_df = DataFrame(e1_road_rows, columns=road_agg_columns)

    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    tag_agg_str = "tag_agg"
    tag_agg_columns = PidginPrimeColumns().map_tag_agg_columns
    e1_tag0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_tag1 = [sue_str, event7, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_tag_rows = [e1_tag0, e1_tag1]
    e1_tag_agg_df = DataFrame(e1_tag_rows, columns=tag_agg_columns)

    yell_dir = create_path(get_test_etl_dir(), "yell")
    agg_pidgin_path = create_yell_pidgin_path(yell_dir)
    upsert_sheet(agg_pidgin_path, name_agg_str, e1_name_agg_df)
    upsert_sheet(agg_pidgin_path, label_agg_str, e1_label_agg_df)
    upsert_sheet(agg_pidgin_path, road_agg_str, e1_road_agg_df)
    upsert_sheet(agg_pidgin_path, tag_agg_str, e1_tag_agg_df)

    faces_dir = create_path(get_test_etl_dir(), "syntax_otz")

    # WHEN
    etl_yell_pidgin_agg_to_otz_face_pidgin_agg(yell_dir, faces_dir)

    # THEN
    sue_dir = create_path(faces_dir, sue_str)
    assert os_path_exists(sue_dir)
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
    print(f"{sue_pidgin_file_path=}")

    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, name_agg_str)
    assert sheet_exists(sue_pidgin_file_path, label_agg_str)
    assert sheet_exists(sue_pidgin_file_path, tag_agg_str)
    assert sheet_exists(sue_pidgin_file_path, road_agg_str)
    gen_sue_name_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=name_agg_str)
    gen_sue_label_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=label_agg_str)
    gen_sue_tag_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=tag_agg_str)
    gen_sue_road_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=road_agg_str)
    print(f"{gen_sue_tag_df=}")

    pandas_testing_assert_frame_equal(gen_sue_name_df, e1_name_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_label_df, e1_label_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_road_df, e1_road_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_tag_df, e1_tag_agg_df)
