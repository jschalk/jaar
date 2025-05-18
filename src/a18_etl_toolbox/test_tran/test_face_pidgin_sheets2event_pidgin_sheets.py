from src.a00_data_toolbox.file_toolbox import create_path, set_dir, get_dir_filenames
from src.a17_idea_logic.idea_db_tool import upsert_sheet, sheet_exists
from src.a18_etl_toolbox.tran_path import (
    create_syntax_otx_pidgin_path,
    create_otx_event_pidgin_path as otx_event_pidgin_path,
)
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import (
    etl_face_pidgin_to_event_pidgins,
    etl_otz_face_pidgins_df_to_otz_event_pidgins_df,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_face_pidgin_to_event_pidgins_Scenario0_Nofile(env_dir_setup_cleanup):
    # ESTABLISH
    faces_dir = get_module_temp_dir()
    sue_str = "Sue"
    sue_face_dir = create_path(faces_dir, sue_str)
    name_agg_str = "name_agg"
    face_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
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
    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    x_nan = float("nan")
    name0 = [event7, sue_str, yao_otx, yao_inx, x_nan, x_nan, x_nan]
    name1 = [event7, sue_str, bob_otx, bob1_inx, x_nan, x_nan, x_nan]
    name2 = [event9, sue_str, bob_otx, bob1_inx, x_nan, x_nan, x_nan]
    name3 = [event3, sue_str, bob_otx, bob2_inx, x_nan, x_nan, x_nan]
    name_rows = [name0, name1, name2, name3]
    sue_name_df = DataFrame(name_rows, columns=name_agg_columns)

    faces_dir = get_module_temp_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
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


def test_etl_face_pidgin_to_event_pidgins_Scenario2_title(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    event7 = 7
    event9 = 9
    jog_str = ";Jog"
    jog_inx = ";Yogging"
    run_str = ";Run"
    run_inx = ";Running"
    title_agg_columns = PidginPrimeColumns().pidgin_title_agg_columns
    x_nan = float("nan")
    title0 = [event7, sue_str, jog_str, jog_inx, x_nan, x_nan, x_nan]
    title1 = [event7, sue_str, run_str, run_inx, x_nan, x_nan, x_nan]
    title2 = [event9, sue_str, run_str, run_inx, x_nan, x_nan, x_nan]
    title_rows = [title0, title1, title2]
    sue_title_agg_df = DataFrame(title_rows, columns=title_agg_columns)

    faces_dir = get_module_temp_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    title_agg_str = "title_agg"
    upsert_sheet(sue_pidgin_file_path, title_agg_str, sue_title_agg_df)
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


def test_etl_face_pidgin_to_event_pidgins_Scenario3_label(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    t3am_otx = "t3am"
    t3am_inx = "t300"
    t6am_otx = "T6am"
    t6am_inx = "T600"
    event7 = 7
    event9 = 9
    label_agg_columns = PidginPrimeColumns().pidgin_label_agg_columns
    x_nan = float("nan")
    e1_label0 = [event7, sue_str, t3am_otx, t3am_inx, x_nan, x_nan, x_nan]
    e1_label1 = [event9, sue_str, t6am_otx, t6am_inx, x_nan, x_nan, x_nan]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_agg_df = DataFrame(e1_label_rows, columns=label_agg_columns)

    faces_dir = get_module_temp_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    label_agg_str = "label_agg"
    upsert_sheet(sue_pidgin_file_path, label_agg_str, e1_label_agg_df)
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


def test_etl_face_pidgin_to_event_pidgins_Scenario4_way(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    event9 = 9
    way_agg_columns = PidginPrimeColumns().pidgin_way_agg_columns
    x_nan = float("nan")
    e1_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way2 = [event9, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way_rows = [e1_way0, e1_way1, e1_way2]
    sue_way_agg_df = DataFrame(e1_way_rows, columns=way_agg_columns)

    faces_dir = get_module_temp_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    way_agg_str = "way_agg"
    upsert_sheet(sue_pidgin_file_path, way_agg_str, sue_way_agg_df)
    assert os_path_exists(sue_dir)
    assert os_path_exists(sue_pidgin_file_path)
    assert sheet_exists(sue_pidgin_file_path, way_agg_str)

    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event7_pidgin_file_path, way_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, way_agg_str) is False

    # WHEN
    etl_face_pidgin_to_event_pidgins(sue_dir)

    # THEN
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event7_pidgin_file_path, way_agg_str)
    assert sheet_exists(event9_pidgin_file_path, way_agg_str)


def test_etl_otz_face_pidgins_df_to_otz_event_pidgins_df_Scenario0_way_Two_face_names(
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
    way_agg_columns = PidginPrimeColumns().pidgin_way_agg_columns
    x_nan = float("nan")
    e1_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e1_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way2 = [event9, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e1_way_rows = [e1_way0, e1_way1, e1_way2]
    sue_way_agg_df = DataFrame(e1_way_rows, columns=way_agg_columns)
    z1_way3 = [event3, zia_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    zia_way_agg_df = DataFrame([z1_way3], columns=way_agg_columns)

    faces_dir = get_module_temp_dir()
    sue_dir = create_path(faces_dir, sue_str)
    zia_dir = create_path(faces_dir, zia_str)
    event3_dir = create_path(zia_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(sue_dir, event9)
    sue_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, sue_str)
    zia_pidgin_file_path = create_syntax_otx_pidgin_path(faces_dir, zia_str)
    event3_pidgin_file_path = otx_event_pidgin_path(faces_dir, zia_str, event3)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event9)
    way_agg_str = "way_agg"
    upsert_sheet(sue_pidgin_file_path, way_agg_str, sue_way_agg_df)
    upsert_sheet(zia_pidgin_file_path, way_agg_str, zia_way_agg_df)
    assert sheet_exists(sue_pidgin_file_path, way_agg_str)
    assert sheet_exists(zia_pidgin_file_path, way_agg_str)

    assert os_path_exists(event3_dir) is False
    assert os_path_exists(event7_dir) is False
    assert os_path_exists(event9_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert os_path_exists(event7_pidgin_file_path) is False
    assert os_path_exists(event9_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, way_agg_str) is False
    assert sheet_exists(event7_pidgin_file_path, way_agg_str) is False
    assert sheet_exists(event9_pidgin_file_path, way_agg_str) is False

    # WHEN
    etl_otz_face_pidgins_df_to_otz_event_pidgins_df(faces_dir)

    # THEN
    assert os_path_exists(event3_dir)
    assert os_path_exists(event7_dir)
    assert os_path_exists(event9_dir)
    assert os_path_exists(event3_pidgin_file_path)
    assert os_path_exists(event7_pidgin_file_path)
    assert os_path_exists(event9_pidgin_file_path)
    assert sheet_exists(event3_pidgin_file_path, way_agg_str)
    assert sheet_exists(event7_pidgin_file_path, way_agg_str)
    assert sheet_exists(event9_pidgin_file_path, way_agg_str)
    gen_e3 = pandas_read_excel(event3_pidgin_file_path, way_agg_str)
    gen_e7 = pandas_read_excel(event7_pidgin_file_path, way_agg_str)
    gen_e9 = pandas_read_excel(event9_pidgin_file_path, way_agg_str)
    pandas_testing_assert_frame_equal(gen_e3, zia_way_agg_df)
