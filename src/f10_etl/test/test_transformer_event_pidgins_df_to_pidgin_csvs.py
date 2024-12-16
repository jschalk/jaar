from src.f00_instrument.file import create_path, set_dir, get_dir_filenames
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
from src.f09_brick.pandas_tool import upsert_sheet, sheet_exists, open_csv
from src.f10_etl.transformers import (
    event_pidgin_to_pidgin_csv_files,
    etl_bow_event_pidgins_to_bow_pidgin_csv_files,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_event_pidgin_to_pidgin_csv_files_Scenario0_Nofile(env_dir_setup_cleanup):
    # ESTABLISH
    faces_dir = get_test_etl_dir()
    sue_str = "Sue"
    sue_face_dir = create_path(faces_dir, sue_str)
    event3 = 3
    event3_dir = create_path(faces_dir, event3)
    acct_agg_str = "acct_agg"
    event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")

    assert os_path_exists(sue_face_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, acct_agg_str) is False
    assert len(get_dir_filenames(event3_dir)) == 0

    # WHEN
    event_pidgin_to_pidgin_csv_files(sue_face_dir)
    # THEN nothing changes
    assert os_path_exists(sue_face_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, acct_agg_str) is False
    assert len(get_dir_filenames(event3_dir)) == 0

    set_dir(sue_face_dir)
    assert os_path_exists(sue_face_dir)
    # WHEN
    event_pidgin_to_pidgin_csv_files(sue_face_dir)
    # THEN nothing changes
    assert os_path_exists(sue_face_dir)
    assert os_path_exists(event3_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, acct_agg_str) is False
    assert len(get_dir_filenames(event3_dir)) == 0

    upsert_sheet(event3_pidgin_file_path, "irrelvant_sheet", DataFrame(columns=["a"]))
    assert os_path_exists(event3_pidgin_file_path)
    # WHEN
    event_pidgin_to_pidgin_csv_files(sue_face_dir)
    # THEN nothing changes
    assert os_path_exists(sue_face_dir)
    assert os_path_exists(event3_pidgin_file_path)
    assert sheet_exists(event3_pidgin_file_path, acct_agg_str) is False
    assert len(get_dir_filenames(event3_dir)) == 1


def test_event_pidgin_to_pidgin_csv_files_Scenario1_1Event_acct(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_otx = "Bob"
    bob2_inx = "Bobby"
    event3 = 3
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
    e3_acct_row = [sue_str, event3, bob_otx, bob2_inx, x_nan, x_nan, x_nan]
    e3_acct_df = DataFrame([e3_acct_row], columns=acct_file_columns)

    faces_dir = get_test_etl_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event3_dir = create_path(sue_dir, event3)
    event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")
    event3_acct_csv_file_path = create_path(event3_dir, "acct.csv")
    acct_agg_str = "acct_agg"
    upsert_sheet(event3_pidgin_file_path, acct_agg_str, e3_acct_df)
    assert sheet_exists(event3_pidgin_file_path, acct_agg_str)
    assert os_path_exists(event3_acct_csv_file_path) is False

    # WHEN
    event_pidgin_to_pidgin_csv_files(event3_dir)

    # THEN
    assert os_path_exists(event3_acct_csv_file_path)
    gen_event3_csv_df = open_csv(event3_dir, "acct.csv")
    print(f"{gen_event3_csv_df=}")
    pandas_testing_assert_frame_equal(gen_event3_csv_df, e3_acct_df)


def test_event_pidgin_to_pidgin_csv_files_Scenario2_1Event_road(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    road_file_columns = [
        face_id_str(),
        event_id_str(),
        otx_road_str(),
        inx_road_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    x_nan = float("nan")
    e7_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e7_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e7_road_rows = [e7_road0, e7_road1]
    e7_road_df = DataFrame(e7_road_rows, columns=road_file_columns)

    faces_dir = get_test_etl_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event7_dir = create_path(sue_dir, event7)
    event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
    event7_road_csv_file_path = create_path(event7_dir, "road.csv")
    road_agg_str = "road_agg"
    upsert_sheet(event7_pidgin_file_path, road_agg_str, e7_road_df)
    assert sheet_exists(event7_pidgin_file_path, road_agg_str)
    assert os_path_exists(event7_road_csv_file_path) is False

    # WHEN
    event_pidgin_to_pidgin_csv_files(event7_dir)

    # THEN
    assert os_path_exists(event7_road_csv_file_path)
    gen_event3_csv_df = open_csv(event7_dir, "road.csv")
    print(f"{gen_event3_csv_df=}")
    pandas_testing_assert_frame_equal(gen_event3_csv_df, e7_road_df)


def test_etl_bow_event_pidgins_to_bow_pidgin_csv_files_Scenario0_3Event_road(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event3 = 3
    event7 = 7
    event9 = 9
    road_file_columns = [
        face_id_str(),
        event_id_str(),
        otx_road_str(),
        inx_road_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    x_nan = float("nan")
    e3_road0 = [bob_str, event3, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e3_road1 = [bob_str, event3, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e3_road_rows = [e3_road0, e3_road1]
    e3_road_df = DataFrame(e3_road_rows, columns=road_file_columns)

    e7_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e7_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e7_road_rows = [e7_road0, e7_road1]
    e7_road_df = DataFrame(e7_road_rows, columns=road_file_columns)

    e9_road0 = [zia_str, event9, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e9_road1 = [zia_str, event9, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e9_road_rows = [e9_road0, e9_road1]
    e9_road_df = DataFrame(e9_road_rows, columns=road_file_columns)

    faces_dir = get_test_etl_dir()
    bob_dir = create_path(faces_dir, bob_str)
    sue_dir = create_path(faces_dir, sue_str)
    zia_dir = create_path(faces_dir, zia_str)
    event3_dir = create_path(bob_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")
    event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
    event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
    event3_road_csv_file_path = create_path(event3_dir, "road.csv")
    event7_road_csv_file_path = create_path(event7_dir, "road.csv")
    event9_road_csv_file_path = create_path(event9_dir, "road.csv")
    road_agg_str = "road_agg"
    upsert_sheet(event3_pidgin_file_path, road_agg_str, e3_road_df)
    upsert_sheet(event7_pidgin_file_path, road_agg_str, e7_road_df)
    upsert_sheet(event9_pidgin_file_path, road_agg_str, e9_road_df)
    assert sheet_exists(event3_pidgin_file_path, road_agg_str)
    assert sheet_exists(event7_pidgin_file_path, road_agg_str)
    assert sheet_exists(event9_pidgin_file_path, road_agg_str)
    assert os_path_exists(event3_road_csv_file_path) is False
    assert os_path_exists(event7_road_csv_file_path) is False
    assert os_path_exists(event9_road_csv_file_path) is False

    # WHEN
    etl_bow_event_pidgins_to_bow_pidgin_csv_files(faces_dir)

    # THEN
    assert os_path_exists(event3_road_csv_file_path)
    assert os_path_exists(event7_road_csv_file_path)
    assert os_path_exists(event9_road_csv_file_path)
    gen_event3_csv_df = open_csv(event7_dir, "road.csv")
    print(f"{gen_event3_csv_df=}")
    pandas_testing_assert_frame_equal(gen_event3_csv_df, e7_road_df)


# def test_event_pidgin_to_pidgin_csv_files_Scenario2_3Events(env_dir_setup_cleanup):
#     # ESTABLISH
#     sue_str = "Sue"
#     bob_otx = "Bob"
#     yao_otx = "Yao"
#     yao_inx = "Yaoito"
#     bob1_inx = "Bobito"
#     bob2_inx = "Bobby"
#     event3 = 3
#     event7 = 7
#     event9 = 9
#     acct_file_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_acct_id_str(),
#         inx_acct_id_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     x_nan = float("nan")
#     e3_acct_row = [sue_str, event3, bob_otx, bob2_inx, x_nan, x_nan, x_nan]
#     e7_acct_row0 = [sue_str, event7, yao_otx, yao_inx, x_nan, x_nan, x_nan]
#     e7_acct_row1 = [sue_str, event7, bob_otx, bob1_inx, x_nan, x_nan, x_nan]
#     e9_acct_row = [sue_str, event9, bob_otx, bob1_inx, x_nan, x_nan, x_nan]
#     e3_acct_df = DataFrame([e3_acct_row], columns=acct_file_columns)
#     e7_acct_df = DataFrame([e7_acct_row0, e7_acct_row1], columns=acct_file_columns)
#     e9_acct_df = DataFrame([e9_acct_row], columns=acct_file_columns)

#     faces_dir = get_test_etl_dir()
#     sue_dir = create_path(faces_dir, sue_str)
#     event3_dir = create_path(sue_dir, event3)
#     event7_dir = create_path(sue_dir, event7)
#     event9_dir = create_path(sue_dir, event9)
#     event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")
#     event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
#     event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
#     event3_acct_csv_file_path = create_path(event3_dir, "acct.csv")
#     event7_road_csv_file_path = create_path(event7_dir, "acct.csv")
#     event9_acct_csv_file_path = create_path(event9_dir, "acct.csv")
#     acct_agg_str = "acct_agg"
#     upsert_sheet(event3_pidgin_file_path, acct_agg_str, e3_acct_df)
#     upsert_sheet(event7_pidgin_file_path, acct_agg_str, e7_acct_df)
#     upsert_sheet(event9_pidgin_file_path, acct_agg_str, e9_acct_df)
#     assert sheet_exists(event3_pidgin_file_path, acct_agg_str)
#     assert sheet_exists(event7_pidgin_file_path, acct_agg_str)
#     assert sheet_exists(event9_pidgin_file_path, acct_agg_str)

#     assert os_path_exists(event3_acct_csv_file_path) is False
#     assert os_path_exists(event7_road_csv_file_path) is False
#     assert os_path_exists(event9_acct_csv_file_path) is False

#     # WHEN
#     event_pidgin_to_pidgin_csv_files(sue_dir)

#     # THEN
#     assert os_path_exists(event3_acct_csv_file_path)
#     assert os_path_exists(event7_road_csv_file_path)
#     assert os_path_exists(event9_acct_csv_file_path)
#     event3_csv = open_csv(event3_acct_csv_file_path)
#     event7_csv = open_csv(event7_road_csv_file_path)
#     event9_csv = open_csv(event9_acct_csv_file_path)
#     assert event3_csv == "sv_file_path)"
#     assert event7_csv == "sv_file_path)"
#     assert event9_csv == "sv_file_path)"
#     assert 1 == 2


# def test_event_pidgin_to_pidgin_csv_files_Scenario3_group(env_dir_setup_cleanup):
#     # ESTABLISH
#     sue_str = "Sue"
#     event7 = 7
#     event9 = 9
#     jog_str = ";Jog"
#     jog_inx = ";Yogging"
#     run_str = ";Run"
#     run_inx = ";Running"
#     group_file_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_group_id_str(),
#         inx_group_id_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     x_nan = float("nan")
#     group0 = [sue_str, event7, jog_str, jog_inx, x_nan, x_nan, x_nan]
#     group1 = [sue_str, event7, run_str, run_inx, x_nan, x_nan, x_nan]
#     group2 = [sue_str, event9, run_str, run_inx, x_nan, x_nan, x_nan]
#     group_rows = [group0, group1, group2]
#     sue_group_agg_df = DataFrame(group_rows, columns=group_file_columns)

#     faces_dir = get_test_etl_dir()
#     sue_dir = create_path(faces_dir, sue_str)
#     event7_dir = create_path(sue_dir, event7)
#     event9_dir = create_path(sue_dir, event9)
#     sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
#     event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
#     event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
#     group_agg_str = "group_agg"
#     upsert_sheet(sue_pidgin_file_path, group_agg_str, sue_group_agg_df)
#     assert os_path_exists(sue_dir)
#     assert os_path_exists(sue_pidgin_file_path)
#     assert sheet_exists(sue_pidgin_file_path, group_agg_str)

#     assert os_path_exists(event7_dir) is False
#     assert os_path_exists(event9_dir) is False
#     assert os_path_exists(event7_pidgin_file_path) is False
#     assert os_path_exists(event9_pidgin_file_path) is False
#     assert sheet_exists(event7_pidgin_file_path, group_agg_str) is False
#     assert sheet_exists(event9_pidgin_file_path, group_agg_str) is False

#     # WHEN
#     event_pidgin_to_pidgin_csv_files(sue_dir)

#     # THEN
#     assert os_path_exists(event7_dir)
#     assert os_path_exists(event9_dir)
#     assert os_path_exists(event7_pidgin_file_path)
#     assert os_path_exists(event9_pidgin_file_path)
#     assert sheet_exists(event7_pidgin_file_path, group_agg_str)
#     assert sheet_exists(event9_pidgin_file_path, group_agg_str)


# def test_event_pidgin_to_pidgin_csv_files_Scenario3_idea(env_dir_setup_cleanup):
#     # ESTABLISH
#     sue_str = "Sue"
#     t3am_otx = "t3am"
#     t3am_inx = "t300"
#     t6am_otx = "T6am"
#     t6am_inx = "T600"
#     event7 = 7
#     event9 = 9
#     idea_file_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_idea_str(),
#         inx_idea_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     x_nan = float("nan")
#     e1_idea0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
#     e1_idea1 = [sue_str, event9, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
#     e1_idea_rows = [e1_idea0, e1_idea1]
#     e1_idea_agg_df = DataFrame(e1_idea_rows, columns=idea_file_columns)

#     faces_dir = get_test_etl_dir()
#     sue_dir = create_path(faces_dir, sue_str)
#     event7_dir = create_path(sue_dir, event7)
#     event9_dir = create_path(sue_dir, event9)
#     sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
#     event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
#     event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
#     idea_agg_str = "idea_agg"
#     upsert_sheet(sue_pidgin_file_path, idea_agg_str, e1_idea_agg_df)
#     assert os_path_exists(sue_dir)
#     assert os_path_exists(sue_pidgin_file_path)
#     assert sheet_exists(sue_pidgin_file_path, idea_agg_str)

#     assert os_path_exists(event7_dir) is False
#     assert os_path_exists(event9_dir) is False
#     assert os_path_exists(event7_pidgin_file_path) is False
#     assert os_path_exists(event9_pidgin_file_path) is False
#     assert sheet_exists(event7_pidgin_file_path, idea_agg_str) is False
#     assert sheet_exists(event9_pidgin_file_path, idea_agg_str) is False

#     # WHEN
#     event_pidgin_to_pidgin_csv_files(sue_dir)

#     # THEN
#     assert os_path_exists(event7_dir)
#     assert os_path_exists(event9_dir)
#     assert os_path_exists(event7_pidgin_file_path)
#     assert os_path_exists(event9_pidgin_file_path)
#     assert sheet_exists(event7_pidgin_file_path, idea_agg_str)
#     assert sheet_exists(event9_pidgin_file_path, idea_agg_str)


# def test_event_pidgin_to_pidgin_csv_files_Scenario3_road(env_dir_setup_cleanup):
#     # ESTABLISH
#     sue_str = "Sue"
#     casa_otx = "fizz,casa"
#     casa_inx = "fizz,casaita"
#     clean_otx = "fizz,casa,clean"
#     clean_inx = "fizz,casaita,limpio"
#     event7 = 7
#     event9 = 9
#     road_file_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     x_nan = float("nan")
#     e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
#     e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
#     e1_road2 = [sue_str, event9, clean_otx, clean_inx, x_nan, x_nan, x_nan]
#     e1_road_rows = [e1_road0, e1_road1, e1_road2]
#     sue_road_agg_df = DataFrame(e1_road_rows, columns=road_file_columns)

#     faces_dir = get_test_etl_dir()
#     sue_dir = create_path(faces_dir, sue_str)
#     event7_dir = create_path(sue_dir, event7)
#     event9_dir = create_path(sue_dir, event9)
#     sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
#     event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
#     event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
#     road_agg_str = "road_agg"
#     upsert_sheet(sue_pidgin_file_path, road_agg_str, sue_road_agg_df)
#     assert os_path_exists(sue_dir)
#     assert os_path_exists(sue_pidgin_file_path)
#     assert sheet_exists(sue_pidgin_file_path, road_agg_str)

#     assert os_path_exists(event7_dir) is False
#     assert os_path_exists(event9_dir) is False
#     assert os_path_exists(event7_pidgin_file_path) is False
#     assert os_path_exists(event9_pidgin_file_path) is False
#     assert sheet_exists(event7_pidgin_file_path, road_agg_str) is False
#     assert sheet_exists(event9_pidgin_file_path, road_agg_str) is False

#     # WHEN
#     event_pidgin_to_pidgin_csv_files(sue_dir)

#     # THEN
#     assert os_path_exists(event7_dir)
#     assert os_path_exists(event9_dir)
#     assert os_path_exists(event7_pidgin_file_path)
#     assert os_path_exists(event9_pidgin_file_path)
#     assert sheet_exists(event7_pidgin_file_path, road_agg_str)
#     assert sheet_exists(event9_pidgin_file_path, road_agg_str)


# def test_etl_bow_face_pidgins_to_bow_event_pidgins_Scenario0_road_Two_face_ids(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_str = "Sue"
#     zia_str = "Zia"
#     casa_otx = "fizz,casa"
#     casa_inx = "fizz,casaita"
#     clean_otx = "fizz,casa,clean"
#     clean_inx = "fizz,casaita,limpio"
#     event3 = 3
#     event7 = 7
#     event9 = 9
#     road_file_columns = [
#         face_id_str(),
#         event_id_str(),
#         otx_road_str(),
#         inx_road_str(),
#         otx_wall_str(),
#         inx_wall_str(),
#         unknown_word_str(),
#     ]
#     x_nan = float("nan")
#     e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
#     e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
#     e1_road2 = [sue_str, event9, clean_otx, clean_inx, x_nan, x_nan, x_nan]
#     e1_road_rows = [e1_road0, e1_road1, e1_road2]
#     sue_road_agg_df = DataFrame(e1_road_rows, columns=road_file_columns)
#     z1_road3 = [zia_str, event3, clean_otx, clean_inx, x_nan, x_nan, x_nan]
#     zia_road_agg_df = DataFrame([z1_road3], columns=road_file_columns)

#     faces_dir = get_test_etl_dir()
#     sue_dir = create_path(faces_dir, sue_str)
#     zia_dir = create_path(faces_dir, zia_str)
#     event3_dir = create_path(zia_dir, event3)
#     event7_dir = create_path(sue_dir, event7)
#     event9_dir = create_path(sue_dir, event9)
#     sue_pidgin_file_path = create_path(sue_dir, "pidgin.xlsx")
#     zia_pidgin_file_path = create_path(zia_dir, "pidgin.xlsx")
#     event3_pidgin_file_path = create_path(event3_dir, "pidgin.xlsx")
#     event7_pidgin_file_path = create_path(event7_dir, "pidgin.xlsx")
#     event9_pidgin_file_path = create_path(event9_dir, "pidgin.xlsx")
#     road_agg_str = "road_agg"
#     upsert_sheet(sue_pidgin_file_path, road_agg_str, sue_road_agg_df)
#     upsert_sheet(zia_pidgin_file_path, road_agg_str, zia_road_agg_df)
#     assert sheet_exists(sue_pidgin_file_path, road_agg_str)
#     assert sheet_exists(zia_pidgin_file_path, road_agg_str)

#     assert os_path_exists(event3_dir) is False
#     assert os_path_exists(event7_dir) is False
#     assert os_path_exists(event9_dir) is False
#     assert os_path_exists(event3_pidgin_file_path) is False
#     assert os_path_exists(event7_pidgin_file_path) is False
#     assert os_path_exists(event9_pidgin_file_path) is False
#     assert sheet_exists(event3_pidgin_file_path, road_agg_str) is False
#     assert sheet_exists(event7_pidgin_file_path, road_agg_str) is False
#     assert sheet_exists(event9_pidgin_file_path, road_agg_str) is False

#     # WHEN
#     etl_bow_face_pidgins_to_bow_event_pidgins(faces_dir)

#     # THEN
#     assert os_path_exists(event3_dir)
#     assert os_path_exists(event7_dir)
#     assert os_path_exists(event9_dir)
#     assert os_path_exists(event3_pidgin_file_path)
#     assert os_path_exists(event7_pidgin_file_path)
#     assert os_path_exists(event9_pidgin_file_path)
#     assert sheet_exists(event3_pidgin_file_path, road_agg_str)
#     assert sheet_exists(event7_pidgin_file_path, road_agg_str)
#     assert sheet_exists(event9_pidgin_file_path, road_agg_str)
