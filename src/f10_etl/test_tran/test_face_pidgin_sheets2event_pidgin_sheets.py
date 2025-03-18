from src.f00_instrument.file import create_path, set_dir, get_dir_filenames
from src.f09_idea.idea_db_tool import upsert_sheet, sheet_exists
from src.f10_etl.tran_path import (
    create_otx_face_pidgin_path,
    create_otx_event_pidgin_path as otx_event_pidgin_path,
)
from src.f10_etl.pidgin_agg import PidginPrimeColumns
from src.f10_etl.transformers import (
    etl_face_pidgin_to_event_pidgins,
    etl_otz_face_pidgins_to_otz_event_pidgins,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_face_pidgin_to_event_pidgins_Scenario0_Nofile(env_dir_setup_cleanup):
    # ESTABLISH
    faces_dir = get_test_etl_dir()
    sue_str = "Sue"
    sue_face_dir = create_path(faces_dir, sue_str)
    name_agg_str = "name_agg"
    face_pidgin_file_path = create_otx_face_pidgin_path(faces_dir, sue_str)
    assert os_path_exists(sue_face_dir) is False
    assert os_path_exists(face_pidgin_file_path) is False
    assert sheet_exists(face_pidgin_file_path, name_agg_str) is False
    assert len(get_dir_filenames(sue_face_dir)) == 0

    # WHEN
    etl_face_pidgin_to_event_pidgins(sue_face_dir)
    # THEN no changes
    assert os_path_exists(sue_face_dir) is False
    assert os_path_exists(face_pidgin_file_path) is False
    assert sheet_exists(face_pidgin_file_path, name_agg_str) is False
    assert len(get_dir_filenames(sue_face_dir)) == 0

    set_dir(sue_face_dir)
    assert os_path_exists(sue_face_dir)
    # WHEN
    etl_face_pidgin_to_event_pidgins(sue_face_dir)
    # THEN no changes
    assert os_path_exists(sue_face_dir)
    assert os_path_exists(face_pidgin_file_path) is False
    assert sheet_exists(face_pidgin_file_path, name_agg_str) is False
    assert len(get_dir_filenames(sue_face_dir)) == 0

    upsert_sheet(face_pidgin_file_path, "irrelvant_sheet", DataFrame(columns=["a"]))
    assert os_path_exists(face_pidgin_file_path)
    # WHEN
    etl_face_pidgin_to_event_pidgins(sue_face_dir)
    # THEN no changes
    assert os_path_exists(sue_face_dir)
    assert os_path_exists(face_pidgin_file_path)
    assert sheet_exists(face_pidgin_file_path, name_agg_str) is False
    assert len(get_dir_filenames(sue_face_dir)) == 1


def test_etl_face_pidgin_to_event_pidgins_Scenario1_3Events(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_otx = "Bob"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    bob1_inx = "Bobito"
    bob2_inx = "Bobby"
    event3 = 3
    event7 = 7
    event9 = 9
    name_agg_columns = PidginPrimeColumns().map_name_agg_columns
    x_nan = float("nan")
    name0 = [sue_str, event7, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    name1 = [sue_str, event7, bob_otx, bob1_inx, x_nan, x_nan, x_nan]
    name2 = [sue_str, event9, bob_otx, bob1_inx, x_nan, x_nan, x_nan]
    name3 = [sue_str, event3, bob_otx, bob2_inx, x_nan, x_nan, x_nan]
    name_rows = [name0, name1, name2, name3]
    sue_name_df = DataFrame(name_rows, columns=name_agg_columns)

    faces_dir = get_test_etl_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_otx_face_pidgin_path(faces_dir, sue_str)
    event3_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event3)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    name_agg_str = "name_agg"
    upsert_sheet(sue_pidgin_file_path, name_agg_str, sue_name_df)
    assert os_path_exists(sue_dir)
    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, name_agg_str)

    assert os_path_exists(event3_dir) is False
    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, name_agg_str) is False
    assert sheet_exists(event7_pidgin_file_path, name_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, name_agg_str) is False

    # WHEN
    etl_face_pidgin_to_event_pidgins(sue_dir)

    # THEN
    assert os_path_exists(event3_dir)
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event3_pidgin_file_path)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event3_pidgin_file_path, name_agg_str)
    assert sheet_exists(event7_pidgin_file_path, name_agg_str)
    assert sheet_exists(event9_pidgin_file_path, name_agg_str)


def test_etl_face_pidgin_to_event_pidgins_Scenario2_label(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    event7 = 7
    event9 = 9
    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    label_agg_columns = PidginPrimeColumns().map_label_agg_columns
    x_nan = float("nan")
    label0 = [sue_str, event7, jog_str, jog_inx, x_nan, x_nan, x_nan]
    label1 = [sue_str, event7, run_str, run_inx, x_nan, x_nan, x_nan]
    label2 = [sue_str, event9, run_str, run_inx, x_nan, x_nan, x_nan]
    label_rows = [label0, label1, label2]
    sue_label_agg_df = DataFrame(label_rows, columns=label_agg_columns)

    faces_dir = get_test_etl_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_otx_face_pidgin_path(faces_dir, sue_str)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    label_agg_str = "label_agg"
    upsert_sheet(sue_pidgin_file_path, label_agg_str, sue_label_agg_df)
    assert os_path_exists(sue_dir)
    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, label_agg_str)

    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event7_pidgin_file_path, label_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, label_agg_str) is False

    # WHEN
    etl_face_pidgin_to_event_pidgins(sue_dir)

    # THEN
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event7_pidgin_file_path, label_agg_str)
    assert sheet_exists(event9_pidgin_file_path, label_agg_str)


def test_etl_face_pidgin_to_event_pidgins_Scenario3_title(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    event9 = 9
    title_agg_columns = PidginPrimeColumns().map_title_agg_columns
    x_nan = float("nan")
    e1_title0 = [sue_str, event7, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_title1 = [sue_str, event9, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_title_rows = [e1_title0, e1_title1]
    e1_title_agg_df = DataFrame(e1_title_rows, columns=title_agg_columns)

    faces_dir = get_test_etl_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_otx_face_pidgin_path(faces_dir, sue_str)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    title_agg_str = "title_agg"
    upsert_sheet(sue_pidgin_file_path, title_agg_str, e1_title_agg_df)
    assert os_path_exists(sue_dir)
    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, title_agg_str)

    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event7_pidgin_file_path, title_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, title_agg_str) is False

    # WHEN
    etl_face_pidgin_to_event_pidgins(sue_dir)

    # THEN
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event7_pidgin_file_path, title_agg_str)
    assert sheet_exists(event9_pidgin_file_path, title_agg_str)


def test_etl_face_pidgin_to_event_pidgins_Scenario4_road(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    event9 = 9
    road_agg_columns = PidginPrimeColumns().map_road_agg_columns
    x_nan = float("nan")
    e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road2 = [sue_str, event9, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road_rows = [e1_road0, e1_road1, e1_road2]
    sue_road_agg_df = DataFrame(e1_road_rows, columns=road_agg_columns)

    faces_dir = get_test_etl_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_otx_face_pidgin_path(faces_dir, sue_str)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    road_agg_str = "road_agg"
    upsert_sheet(sue_pidgin_file_path, road_agg_str, sue_road_agg_df)
    assert os_path_exists(sue_dir)
    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, road_agg_str)

    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event7_pidgin_file_path, road_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, road_agg_str) is False

    # WHEN
    etl_face_pidgin_to_event_pidgins(sue_dir)

    # THEN
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event7_pidgin_file_path, road_agg_str)
    assert sheet_exists(event9_pidgin_file_path, road_agg_str)


def test_etl_otz_face_pidgins_to_otz_event_pidgins_Scenario0_road_Two_face_names(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event3 = 3
    event7 = 7
    event9 = 9
    road_agg_columns = PidginPrimeColumns().map_road_agg_columns
    x_nan = float("nan")
    e1_road0 = [sue_str, event7, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_road1 = [sue_str, event7, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road2 = [sue_str, event9, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_road_rows = [e1_road0, e1_road1, e1_road2]
    sue_road_agg_df = DataFrame(e1_road_rows, columns=road_agg_columns)
    z1_road3 = [zia_str, event3, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    zia_road_agg_df = DataFrame([z1_road3], columns=road_agg_columns)

    faces_dir = get_test_etl_dir()
    sue_dir = create_path(faces_dir, sue_str)
    zia_dir = create_path(faces_dir, zia_str)
    event3_dir = create_path(zia_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_otx_face_pidgin_path(faces_dir, sue_str)
    zia_pidgin_file_path = create_otx_face_pidgin_path(faces_dir, zia_str)
    event3_pidgin_file_path = otx_event_pidgin_path(faces_dir, zia_str, event3)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    road_agg_str = "road_agg"
    upsert_sheet(sue_pidgin_file_path, road_agg_str, sue_road_agg_df)
    upsert_sheet(zia_pidgin_file_path, road_agg_str, zia_road_agg_df)
    assert sheet_exists(sue_pidgin_file_path, road_agg_str)
    assert sheet_exists(zia_pidgin_file_path, road_agg_str)

    assert os_path_exists(event3_dir) is False
    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, road_agg_str) is False
    assert sheet_exists(event7_pidgin_file_path, road_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, road_agg_str) is False

    # WHEN
    etl_otz_face_pidgins_to_otz_event_pidgins(faces_dir)

    # THEN
    assert os_path_exists(event3_dir)
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event3_pidgin_file_path)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event3_pidgin_file_path, road_agg_str)
    assert sheet_exists(event7_pidgin_file_path, road_agg_str)
    assert sheet_exists(event9_pidgin_file_path, road_agg_str)
    gen_e3 = pandas_read_excel(event3_pidgin_file_path, road_agg_str)
    gen_e7 = pandas_read_excel(event7_pidgin_file_path, road_agg_str)
    gen_e9 = pandas_read_excel(event9_pidgin_file_path, road_agg_str)
    pandas_testing_assert_frame_equal(gen_e3, zia_road_agg_df)
