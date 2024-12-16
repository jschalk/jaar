from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str
from src.f08_pidgin.pidgin_config import (
    event_id_str,
    inx_wall_str,
    otx_wall_str,
    inx_acct_id_str,
    otx_acct_id_str,
    inx_group_id_str,
    otx_group_id_str,
    inx_road_str,
    otx_road_str,
    inx_idea_str,
    otx_idea_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import upsert_sheet, sheet_exists
from src.f10_etl.transformers import etl_fish_pidgin_agg_to_bow_face_dirs
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_fish_pidgin_agg_to_bow_face_dirs_Scenario0_Two_face_ids(
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
    acct_agg_str = "acct_agg"

    acct_file_columns = [
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    x_nan = float("nan")
    acct0 = [sue_str, event7, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    acct1 = [sue_str, event7, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    acct2 = [zia_str, event7, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    acct3 = [zia_str, event7, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    acct_rows = [acct0, acct1, acct2, acct3]
    e1_acct_agg_df = DataFrame(acct_rows, columns=acct_file_columns)

    fish_dir = create_path(get_test_etl_dir(), "fish")
    agg_pidgin_path = create_path(fish_dir, "pidgin.xlsx")
    upsert_sheet(agg_pidgin_path, acct_agg_str, e1_acct_agg_df)

    faces_dir = create_path(get_test_etl_dir(), "faces_otx")

    # WHEN
    etl_fish_pidgin_agg_to_bow_face_dirs(fish_dir, faces_dir)

    # THEN
    sue_dir = create_path(faces_dir, sue_str)
    zia_dir = create_path(faces_dir, zia_str)
    assert os_path_exists(sue_dir)
    assert os_path_exists(zia_dir)
    sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
    zia_pidgin_file_path = create_path(zia_dir, "pidgin.xlsx")
    assert os_path_exists(sue_pidgin_file_path)
    assert os_path_exists(zia_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, acct_agg_str)
    assert sheet_exists(zia_pidgin_file_path, acct_agg_str)
    gen_sue_acct_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=acct_agg_str)
    gen_zia_acct_df = pandas_read_excel(zia_pidgin_file_path, sheet_name=acct_agg_str)

    e1_sue_acct_agg_df = DataFrame([acct0, acct1], columns=acct_file_columns)
    e1_zia_acct_agg_df = DataFrame([acct2, acct3], columns=acct_file_columns)

    pandas_testing_assert_frame_equal(gen_sue_acct_df, e1_sue_acct_agg_df)
    pandas_testing_assert_frame_equal(gen_zia_acct_df, e1_zia_acct_agg_df)


def test_etl_fish_pidgin_agg_to_bow_face_dirs_Scenario1_AllBridgeCategorys(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_otx = "Bob"
    sue_str = "Sue"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    event7 = 7
    acct_agg_str = "acct_agg"

    acct_file_columns = [
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    x_nan = float("nan")
    e1_acct0 = [sue_str, event7, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    e1_acct1 = [sue_str, event7, bob_otx, bob_inx, x_nan, x_nan, x_nan]
    e1_acct_rows = [e1_acct0, e1_acct1]
    e1_acct_agg_df = DataFrame(e1_acct_rows, columns=acct_file_columns)

    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    event7 = 7
    group_agg_str = "group_agg"
    group_file_columns = [
        face_id_str(),
        event_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    e1_group0 = [sue_str, event7, jog_str, jog_inx, x_nan, x_nan, x_nan]
    e1_group1 = [sue_str, event7, run_str, run_inx, x_nan, x_nan, x_nan]
    e1_group_rows = [e1_group0, e1_group1]
    e1_group_agg_df = DataFrame(e1_group_rows, columns=group_file_columns)

    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    road_agg_str = "road_agg"
    road_file_columns = [
        face_id_str(),
        event_id_str(),
        otx_road_str(),
        inx_road_str(),
        otx_wall_str(),
        inx_wall_str(),
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
    idea_agg_str = "idea_agg"
    idea_file_columns = [
        face_id_str(),
        event_id_str(),
        otx_idea_str(),
        inx_idea_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    e1_idea0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_idea1 = [sue_str, event7, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_idea_rows = [e1_idea0, e1_idea1]
    e1_idea_agg_df = DataFrame(e1_idea_rows, columns=idea_file_columns)

    fish_dir = create_path(get_test_etl_dir(), "fish")
    agg_pidgin_path = create_path(fish_dir, "pidgin.xlsx")
    upsert_sheet(agg_pidgin_path, acct_agg_str, e1_acct_agg_df)
    upsert_sheet(agg_pidgin_path, group_agg_str, e1_group_agg_df)
    upsert_sheet(agg_pidgin_path, road_agg_str, e1_road_agg_df)
    upsert_sheet(agg_pidgin_path, idea_agg_str, e1_idea_agg_df)

    faces_dir = create_path(get_test_etl_dir(), "faces_otx")

    # WHEN
    etl_fish_pidgin_agg_to_bow_face_dirs(fish_dir, faces_dir)

    # THEN
    sue_dir = create_path(faces_dir, sue_str)
    assert os_path_exists(sue_dir)
    sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, acct_agg_str)
    assert sheet_exists(sue_pidgin_file_path, group_agg_str)
    assert sheet_exists(sue_pidgin_file_path, idea_agg_str)
    assert sheet_exists(sue_pidgin_file_path, road_agg_str)
    gen_sue_acct_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=acct_agg_str)
    gen_sue_group_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=group_agg_str)
    gen_sue_idea_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=idea_agg_str)
    gen_sue_road_df = pandas_read_excel(sue_pidgin_file_path, sheet_name=road_agg_str)
    print(f"{gen_sue_idea_df=}")

    pandas_testing_assert_frame_equal(gen_sue_acct_df, e1_acct_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_group_df, e1_group_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_road_df, e1_road_agg_df)
    pandas_testing_assert_frame_equal(gen_sue_idea_df, e1_idea_agg_df)
