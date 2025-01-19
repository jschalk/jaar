from src.f00_instrument.file import create_path
from src.f09_idea.pandas_tool import upsert_sheet, sheet_exists
from src.f10_etl.pidgin_agg import PidginPrimeColumns
from src.f10_etl.transformers import etl_boat_pidgin_agg_to_bow_face_dirs
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_boat_pidgin_agg_to_bow_face_dirs_Scenario0_Two_face_names(
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

    boat_dir = create_path(get_test_etl_dir(), "boat")
    agg_pidgin_path = create_path(boat_dir, "pidgin.xlsx")
    upsert_sheet(agg_pidgin_path, name_agg_str, e1_name_agg_df)

    faces_dir = create_path(get_test_etl_dir(), "faces_bow")

    # WHEN
    etl_boat_pidgin_agg_to_bow_face_dirs(boat_dir, faces_dir)

    # THEN
    sue_dir = create_path(faces_dir, sue_str)
    zia_dir = create_path(faces_dir, zia_str)
    assert os_path_exists(sue_dir)
    assert os_path_exists(zia_dir)
    sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
    zia_pidgin_file_path = create_path(zia_dir, "pidgin.xlsx")
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


def test_etl_boat_pidgin_agg_to_bow_face_dirs_Scenario1_AllMapCategorys(
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
    title_agg_str = "title_agg"
    title_agg_columns = PidginPrimeColumns().map_title_agg_columns
    e1_title0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_title1 = [sue_str, event7, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_title_rows = [e1_title0, e1_title1]
    e1_title_agg_df = DataFrame(e1_title_rows, columns=title_agg_columns)

    boat_dir = create_path(get_test_etl_dir(), "boat")
    agg_pidgin_path = create_path(boat_dir, "pidgin.xlsx")
    upsert_sheet(agg_pidgin_path, name_agg_str, e1_name_agg_df)
    upsert_sheet(agg_pidgin_path, label_agg_str, e1_label_agg_df)
    upsert_sheet(agg_pidgin_path, road_agg_str, e1_road_agg_df)
    upsert_sheet(agg_pidgin_path, title_agg_str, e1_title_agg_df)

    faces_dir = create_path(get_test_etl_dir(), "faces_bow")

    # WHEN
    etl_boat_pidgin_agg_to_bow_face_dirs(boat_dir, faces_dir)

    # THEN
    sue_dir = create_path(faces_dir, sue_str)
    assert os_path_exists(sue_dir)
    sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
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
