from src.f00_instrument.file import save_json, get_level1_dirs
from src.f04_gift.atom_config import face_name_str, event_int_str
from src.f09_idea.idea_db_tool import upsert_sheet, sheet_exists
from src.f10_etl.tran_path import create_cart_events_path
from src.f10_etl.transformers import get_cart_events_max_event_int
from src.f10_etl.examples.etl_env import env_dir_setup_cleanup, get_test_etl_dir
from pathlib import Path
from os import mkdir as os_mkdir
from pytest import fixture as pytest_fixture, raises as pytest_raises
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_get_level1_dirs_EmptyDirectory(tmp_path):
    # ESTABLISH
    test_dir = tmp_path

    # WHEN
    result = get_level1_dirs(test_dir)

    # THEN
    expected_dirs = []
    assert_fail_str = f"Expected empty list for empty directory, but got {result}"
    assert result == expected_dirs, assert_fail_str


def test_get_level1_dirs_NonExistentDirectory():
    # ESTABLISH
    test_dir = Path("/non/existent/directory")

    # WHEN
    result = get_level1_dirs(test_dir)

    # WHEN/THEN
    expected_dirs = []
    assert_fail_str = f"Expected empty list for empty directory, but got {result}"
    assert result == expected_dirs, assert_fail_str


@pytest_fixture
def setup_test_directory(tmp_path):
    # Create a temporary directory structure
    os_mkdir((tmp_path / "dir2"))
    os_mkdir((tmp_path / "dir1"))
    os_mkdir((tmp_path / "dir3"))
    os_mkdir((tmp_path / "dir1" / "subdir1"))
    os_mkdir((tmp_path / "dir2" / "subdir2"))
    return tmp_path


def test_get_level1_dirs_ReturnsObjSorted(setup_test_directory):
    # ESTABLISH
    test_dir = setup_test_directory
    expected_dirs = ["dir1", "dir2", "dir3"]

    # WHEN
    result = get_level1_dirs(test_dir)

    # THEN
    assert result == expected_dirs, f"Expected {expected_dirs}, but got {result}"


def test_get_cart_events_max_event_int_ReturnsObj_Scenario0_NoFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH / WHEN
    cart_dir = get_test_etl_dir()
    max_event_int = get_cart_events_max_event_int(cart_dir)
    events_file_path = create_cart_events_path(cart_dir)
    assert os_path_exists(events_file_path) is False
    assert sheet_exists(events_file_path, "events_agg") is False

    # THEN
    assert max_event_int == 0


def test_get_cart_events_max_event_int_ReturnsObj_Scenario1_EmptyFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cart_dir = get_test_etl_dir()
    events_file_path = create_cart_events_path(cart_dir)
    events_agg_columns = [face_name_str(), event_int_str()]
    ex_events_agg_df = DataFrame([], columns=events_agg_columns)
    upsert_sheet(events_file_path, "events_agg", ex_events_agg_df)
    assert os_path_exists(events_file_path)
    assert sheet_exists(events_file_path, "events_agg")

    # WHEN
    max_event_int = get_cart_events_max_event_int(cart_dir)

    # THEN
    assert max_event_int == 0


def test_get_cart_events_max_event_int_ReturnsObj_Scenario2_FileWithRecords(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    cart_dir = get_test_etl_dir()
    events_file_path = create_cart_events_path(cart_dir)
    bob_str = "Bob"
    event3 = 3
    event9 = 9
    e3_row = [bob_str, event3]
    e9_row = [bob_str, event9]
    el_rows = [e3_row, e9_row]
    events_agg_columns = [face_name_str(), event_int_str()]
    ex_events_agg_df = DataFrame(el_rows, columns=events_agg_columns)
    upsert_sheet(events_file_path, "events_agg", ex_events_agg_df)

    # WHEN
    max_event_int = get_cart_events_max_event_int(cart_dir)

    # THEN
    assert max_event_int == 9
