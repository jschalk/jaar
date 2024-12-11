from src.f00_instrument.file import create_path, set_dir
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import upsert_sheet, forge_valid_str, sheet_exists
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_world_event_bricks_to_fiscal_bricks_CreatesFaceBrickSheets_Scenario0_MultpleFaceIDs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    event3 = 3
    event7 = 7
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    br00003_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    music55_str = "music55"
    sue0 = [sue_str, event3, music23_str, hour6am, minute_360]
    sue1 = [sue_str, event3, music23_str, hour7am, minute_420]
    zia0 = [zia_str, event7, music23_str, hour7am, minute_420]
    zia1 = [zia_str, event9, music23_str, hour6am, minute_360]
    zia2 = [zia_str, event9, music23_str, hour7am, minute_420]
    zia3 = [zia_str, event9, music55_str, hour7am, minute_420]
    example_event3_df = DataFrame([sue0, sue1], columns=br00003_columns)
    example_event7_df = DataFrame([zia0], columns=br00003_columns)
    example_event9_df = DataFrame([zia1, zia2, zia3], columns=br00003_columns)
    br00003_filename = "br00003.xlsx"
    fizz_world = worldunit_shop("fizz")
    sue_dir = create_path(fizz_world._faces_dir, sue_str)
    zia_dir = create_path(fizz_world._faces_dir, zia_str)
    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(zia_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    event3_br00003_filepath = create_path(event3_dir, br00003_filename)
    event7_br00003_filepath = create_path(event7_dir, br00003_filename)
    event9_br00003_filepath = create_path(event9_dir, br00003_filename)
    upsert_sheet(event3_br00003_filepath, forge_valid_str(), example_event3_df)
    upsert_sheet(event7_br00003_filepath, forge_valid_str(), example_event7_df)
    upsert_sheet(event9_br00003_filepath, forge_valid_str(), example_event9_df)
    e3_music23_dir = create_path(event3_dir, music23_str)
    e7_music23_dir = create_path(event7_dir, music23_str)
    e9_music23_dir = create_path(event9_dir, music23_str)
    e9_music55_dir = create_path(event9_dir, music55_str)
    e3_music23_br00003_filepath = create_path(e3_music23_dir, br00003_filename)
    e7_music23_br00003_filepath = create_path(e7_music23_dir, br00003_filename)
    e9_music23_br00003_filepath = create_path(e9_music23_dir, br00003_filename)
    e9_music55_br00003_filepath = create_path(e9_music55_dir, br00003_filename)
    print(f"{e3_music23_br00003_filepath=}")
    print(f"{e7_music23_br00003_filepath=}")
    print(f"{e9_music23_br00003_filepath=}")
    print(f"{e9_music55_br00003_filepath=}")
    assert sheet_exists(e3_music23_br00003_filepath, forge_valid_str()) is False
    assert sheet_exists(e7_music23_br00003_filepath, forge_valid_str()) is False
    assert sheet_exists(e9_music23_br00003_filepath, forge_valid_str()) is False
    assert sheet_exists(e9_music55_br00003_filepath, forge_valid_str()) is False

    # WHEN
    fizz_world.event_bricks_to_fiscal_bricks()

    # THEN
    assert sheet_exists(e7_music23_br00003_filepath, forge_valid_str())
    assert sheet_exists(e3_music23_br00003_filepath, forge_valid_str())
    assert sheet_exists(e9_music23_br00003_filepath, forge_valid_str())
    assert sheet_exists(e9_music55_br00003_filepath, forge_valid_str())
    gen_e3_music23_df = pandas_read_excel(
        e3_music23_br00003_filepath, forge_valid_str()
    )
    gen_e7_music23_df = pandas_read_excel(
        e7_music23_br00003_filepath, forge_valid_str()
    )
    gen_e9_music23_df = pandas_read_excel(
        e9_music23_br00003_filepath, forge_valid_str()
    )
    gen_e9_music55_df = pandas_read_excel(
        e9_music55_br00003_filepath, forge_valid_str()
    )
    expected_e9_music23_df = DataFrame([zia1, zia2], columns=br00003_columns)
    expected_e9_music55_df = DataFrame([zia3], columns=br00003_columns)
    print("gen_e9_music55_df")
    print(f"{gen_e9_music55_df}")
    print("expected_e9_music55_df")
    print(f"{expected_e9_music55_df}")
    pandas_assert_frame_equal(gen_e3_music23_df, example_event3_df)
    pandas_assert_frame_equal(gen_e7_music23_df, example_event7_df)
    pandas_assert_frame_equal(gen_e9_music23_df, expected_e9_music23_df)
    pandas_assert_frame_equal(gen_e9_music55_df, expected_e9_music55_df)


def test_WorldUnit_set_fiscal_events_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    event3 = 3
    event7 = 7
    event9 = 9
    music23_str = "music23"
    music55_str = "music55"
    fizz_world = worldunit_shop("fizz")
    sue_dir = create_path(fizz_world._faces_dir, sue_str)
    zia_dir = create_path(fizz_world._faces_dir, zia_str)
    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(zia_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    e3_music23_dir = create_path(event3_dir, music23_str)
    e7_music23_dir = create_path(event7_dir, music23_str)
    e9_music23_dir = create_path(event9_dir, music23_str)
    e9_music55_dir = create_path(event9_dir, music55_str)
    set_dir(e3_music23_dir)
    set_dir(e7_music23_dir)
    set_dir(e9_music23_dir)
    set_dir(e9_music55_dir)
    print(f"{e3_music23_dir=}")
    print(f"{e7_music23_dir=}")
    print(f"{e9_music23_dir=}")
    print(f"{e9_music55_dir=}")
    assert os_path_exists(e3_music23_dir)
    assert os_path_exists(e7_music23_dir)
    assert os_path_exists(e9_music23_dir)
    assert os_path_exists(e9_music55_dir)

    assert fizz_world._fiscal_events == {}

    # WHEN
    fizz_world._set_fiscal_events()

    # THEN
    assert fizz_world._fiscal_events == {
        music23_str: {event3, event7, event9},
        music55_str: {event9},
    }


def test_WorldUnit_event_bricks_to_fiscal_bricks_Sets_fiscal_events(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    event3 = 3
    event7 = 7
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    br00003_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    music55_str = "music55"
    sue0 = [sue_str, event3, music23_str, hour6am, minute_360]
    sue1 = [sue_str, event3, music23_str, hour7am, minute_420]
    zia0 = [zia_str, event7, music23_str, hour7am, minute_420]
    zia1 = [zia_str, event9, music23_str, hour6am, minute_360]
    zia2 = [zia_str, event9, music23_str, hour7am, minute_420]
    zia3 = [zia_str, event9, music55_str, hour7am, minute_420]
    example_event3_df = DataFrame([sue0, sue1], columns=br00003_columns)
    example_event7_df = DataFrame([zia0], columns=br00003_columns)
    example_event9_df = DataFrame([zia1, zia2, zia3], columns=br00003_columns)
    br00003_filename = "br00003.xlsx"
    fizz_world = worldunit_shop("fizz")
    sue_dir = create_path(fizz_world._faces_dir, sue_str)
    zia_dir = create_path(fizz_world._faces_dir, zia_str)
    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(zia_dir, event7)
    event9_dir = create_path(zia_dir, event9)
    event3_br00003_filepath = create_path(event3_dir, br00003_filename)
    event7_br00003_filepath = create_path(event7_dir, br00003_filename)
    event9_br00003_filepath = create_path(event9_dir, br00003_filename)
    upsert_sheet(event3_br00003_filepath, forge_valid_str(), example_event3_df)
    upsert_sheet(event7_br00003_filepath, forge_valid_str(), example_event7_df)
    upsert_sheet(event9_br00003_filepath, forge_valid_str(), example_event9_df)
    e3_music23_dir = create_path(event3_dir, music23_str)
    e7_music23_dir = create_path(event7_dir, music23_str)
    e9_music23_dir = create_path(event9_dir, music23_str)
    e9_music55_dir = create_path(event9_dir, music55_str)
    e3_music23_br00003_filepath = create_path(e3_music23_dir, br00003_filename)
    e7_music23_br00003_filepath = create_path(e7_music23_dir, br00003_filename)
    e9_music23_br00003_filepath = create_path(e9_music23_dir, br00003_filename)
    e9_music55_br00003_filepath = create_path(e9_music55_dir, br00003_filename)
    print(f"{e3_music23_br00003_filepath=}")
    print(f"{e7_music23_br00003_filepath=}")
    print(f"{e9_music23_br00003_filepath=}")
    print(f"{e9_music55_br00003_filepath=}")
    assert sheet_exists(e3_music23_br00003_filepath, forge_valid_str()) is False
    assert sheet_exists(e7_music23_br00003_filepath, forge_valid_str()) is False
    assert sheet_exists(e9_music23_br00003_filepath, forge_valid_str()) is False
    assert sheet_exists(e9_music55_br00003_filepath, forge_valid_str()) is False
    assert fizz_world._fiscal_events == {}

    # WHEN
    fizz_world.event_bricks_to_fiscal_bricks()

    # THEN
    assert sheet_exists(e7_music23_br00003_filepath, forge_valid_str())
    assert sheet_exists(e3_music23_br00003_filepath, forge_valid_str())
    assert sheet_exists(e9_music23_br00003_filepath, forge_valid_str())
    assert sheet_exists(e9_music55_br00003_filepath, forge_valid_str())
    assert fizz_world._fiscal_events == {
        music23_str: {event3, event7, event9},
        music55_str: {event9},
    }
