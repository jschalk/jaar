from src.a00_data_toolbox.file_toolbox import create_path, set_dir, get_dir_filenames
from src.a17_idea_logic.idea_db_tool import upsert_sheet, sheet_exists, open_csv
from src.a18_etl_toolbox.tran_path import (
    create_otx_event_pidgin_path as otx_event_pidgin_path,
)
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import (
    event_pidgin_to_pidgin_csv_files,
    etl_otz_event_pidgins_to_otz_pidgin_csv_files,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from os.path import exists as os_path_exists


def test_etl_event_pidgin_to_pidgin_csv_files_Scenario0_Nofile(env_dir_setup_cleanup):
    # ESTABLISH
    faces_dir = get_module_temp_dir()
    sue_str = "Sue"
    sue_face_dir = create_path(faces_dir, sue_str)
    event3 = 3
    event3_dir = create_path(sue_face_dir, event3)
    name_agg_str = "name_agg"
    event3_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event3)
    print(f"{event3_pidgin_file_path=}")

    assert os_path_exists(sue_face_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, name_agg_str) is False
    assert len(get_dir_filenames(event3_dir)) == 0

    # WHEN
    event_pidgin_to_pidgin_csv_files(sue_face_dir)
    # THEN no changes
    assert os_path_exists(sue_face_dir) is False
    assert os_path_exists(event3_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, name_agg_str) is False
    assert len(get_dir_filenames(event3_dir)) == 0

    set_dir(sue_face_dir)
    assert os_path_exists(sue_face_dir)
    # WHEN
    event_pidgin_to_pidgin_csv_files(sue_face_dir)
    # THEN no changes
    assert os_path_exists(sue_face_dir)
    assert os_path_exists(event3_pidgin_file_path) is False
    assert sheet_exists(event3_pidgin_file_path, name_agg_str) is False
    assert len(get_dir_filenames(event3_dir)) == 0

    upsert_sheet(event3_pidgin_file_path, "irrelvant_sheet", DataFrame(columns=["a"]))
    assert os_path_exists(event3_pidgin_file_path)
    # WHEN
    event_pidgin_to_pidgin_csv_files(sue_face_dir)
    # THEN no changes
    assert os_path_exists(sue_face_dir)
    assert os_path_exists(event3_pidgin_file_path)
    assert sheet_exists(event3_pidgin_file_path, name_agg_str) is False
    assert len(get_dir_filenames(event3_dir)) == 1


def test_event_pidgin_to_pidgin_csv_files_Scenario1_1Event_name(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    bob_otx = "Bob"
    bob2_inx = "Bobby"
    event3 = 3
    name_agg_columns = PidginPrimeColumns().pidgin_name_agg_columns
    x_nan = float("nan")
    e3_name_row = [event3, sue_str, bob_otx, bob2_inx, x_nan, x_nan, x_nan]
    e3_name_df = DataFrame([e3_name_row], columns=name_agg_columns)

    faces_dir = get_module_temp_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event3_dir = create_path(sue_dir, event3)
    event3_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event3)
    event3_name_csv_file_path = create_path(event3_dir, "name.csv")
    name_agg_str = "name_agg"
    upsert_sheet(event3_pidgin_file_path, name_agg_str, e3_name_df)
    assert sheet_exists(event3_pidgin_file_path, name_agg_str)
    assert os_path_exists(event3_name_csv_file_path) is False

    # WHEN
    event_pidgin_to_pidgin_csv_files(event3_dir)

    # THEN
    assert os_path_exists(event3_name_csv_file_path)
    gen_event3_csv_df = open_csv(event3_dir, "name.csv")
    print(f"{gen_event3_csv_df=}")
    pandas_testing_assert_frame_equal(gen_event3_csv_df, e3_name_df)


def test_event_pidgin_to_pidgin_csv_files_Scenario2_1Event_way(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    casa_otx = "fizz,casa"
    casa_inx = "fizz,casaita"
    clean_otx = "fizz,casa,clean"
    clean_inx = "fizz,casaita,limpio"
    event7 = 7
    way_agg_columns = PidginPrimeColumns().pidgin_way_agg_columns
    x_nan = float("nan")
    e7_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e7_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e7_way_rows = [e7_way0, e7_way1]
    e7_way_df = DataFrame(e7_way_rows, columns=way_agg_columns)

    faces_dir = get_module_temp_dir()
    sue_dir = create_path(faces_dir, sue_str)
    event7_dir = create_path(sue_dir, event7)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    print(f"{event7_pidgin_file_path=}")
    event7_way_csv_file_path = create_path(event7_dir, "way.csv")
    way_agg_str = "way_agg"
    upsert_sheet(event7_pidgin_file_path, way_agg_str, e7_way_df)
    assert sheet_exists(event7_pidgin_file_path, way_agg_str)
    assert os_path_exists(event7_way_csv_file_path) is False

    # WHEN
    event_pidgin_to_pidgin_csv_files(event7_dir)

    # THEN
    assert os_path_exists(event7_way_csv_file_path)
    gen_event3_csv_df = open_csv(event7_dir, "way.csv")
    print(f"{gen_event3_csv_df=}")
    pandas_testing_assert_frame_equal(gen_event3_csv_df, e7_way_df)


def test_etl_otz_event_pidgins_to_otz_pidgin_csv_files_Scenario0_3Event_way(
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
    way_agg_columns = PidginPrimeColumns().pidgin_way_agg_columns
    x_nan = float("nan")
    e3_way0 = [event3, bob_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e3_way1 = [event3, bob_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e3_way_rows = [e3_way0, e3_way1]
    e3_way_df = DataFrame(e3_way_rows, columns=way_agg_columns)

    e7_way0 = [event7, sue_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e7_way1 = [event7, sue_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e7_way_rows = [e7_way0, e7_way1]
    e7_way_df = DataFrame(e7_way_rows, columns=way_agg_columns)

    e9_way0 = [event9, zia_str, casa_otx, casa_inx, x_nan, x_nan, x_nan]
    e9_way1 = [event9, zia_str, clean_otx, clean_inx, x_nan, x_nan, x_nan]
    e9_way_rows = [e9_way0, e9_way1]
    e9_way_df = DataFrame(e9_way_rows, columns=way_agg_columns)

    faces_dir = get_module_temp_dir()
    bob_dir = create_path(faces_dir, bob_str)
    sue_dir = create_path(faces_dir, sue_str)
    zia_dir = create_path(faces_dir, zia_str)
    event3_dir = create_path(bob_dir, event3)
    event7_dir = create_path(sue_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    event3_pidgin_file_path = otx_event_pidgin_path(faces_dir, bob_str, event3)
    event7_pidgin_file_path = otx_event_pidgin_path(faces_dir, sue_str, event7)
    event9_pidgin_file_path = otx_event_pidgin_path(faces_dir, zia_str, event9)
    event3_way_csv_file_path = create_path(event3_dir, "way.csv")
    event7_way_csv_file_path = create_path(event7_dir, "way.csv")
    event9_way_csv_file_path = create_path(event9_dir, "way.csv")
    way_agg_str = "way_agg"
    upsert_sheet(event3_pidgin_file_path, way_agg_str, e3_way_df)
    upsert_sheet(event7_pidgin_file_path, way_agg_str, e7_way_df)
    upsert_sheet(event9_pidgin_file_path, way_agg_str, e9_way_df)
    assert sheet_exists(event3_pidgin_file_path, way_agg_str)
    assert sheet_exists(event7_pidgin_file_path, way_agg_str)
    assert sheet_exists(event9_pidgin_file_path, way_agg_str)
    assert os_path_exists(event3_way_csv_file_path) is False
    assert os_path_exists(event7_way_csv_file_path) is False
    assert os_path_exists(event9_way_csv_file_path) is False

    # WHEN
    etl_otz_event_pidgins_to_otz_pidgin_csv_files(faces_dir)

    # THEN
    assert os_path_exists(event3_way_csv_file_path)
    assert os_path_exists(event7_way_csv_file_path)
    assert os_path_exists(event9_way_csv_file_path)
    gen_event3_csv_df = open_csv(event7_dir, "way.csv")
    print(f"{gen_event3_csv_df=}")
    pandas_testing_assert_frame_equal(gen_event3_csv_df, e7_way_df)
