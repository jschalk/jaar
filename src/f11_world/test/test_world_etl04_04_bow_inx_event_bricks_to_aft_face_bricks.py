from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    acct_id_str,
    face_id_str,
    deal_id_str,
    owner_id_str,
)
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import upsert_sheet, sheet_exists
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_bow_inx_event_bricks_to_aft_faces_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    br00011_columns = [
        face_id_str(),
        event_id_str(),
        deal_id_str(),
        owner_id_str(),
        acct_id_str(),
    ]
    music23_str = "music23"
    sue0 = [sue_inx, event3, music23_str, bob_inx, bob_inx]
    sue1 = [sue_inx, event3, music23_str, yao_inx, bob_inx]
    sue2 = [sue_inx, event3, music23_str, yao_inx, yao_inx]
    e3_music23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    fizz_world = worldunit_shop("fizz")
    bow_sue_dir = create_path(fizz_world._faces_bow_dir, sue_otx)
    bow_e3_dir = create_path(bow_sue_dir, event3)
    bow_e3_br00011_path = create_path(bow_e3_dir, br00011_filename)
    inx_str = "inx"
    upsert_sheet(bow_e3_br00011_path, inx_str, e3_music23_df)
    assert sheet_exists(bow_e3_br00011_path, inx_str)
    aft_sue_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    aft_br00011_path = create_path(aft_sue_dir, br00011_filename)
    print(f"{bow_e3_br00011_path=}")
    print(f"{aft_br00011_path=}")
    assert sheet_exists(aft_br00011_path, inx_str) is False

    # WHEN
    fizz_world.bow_inx_event_bricks_to_aft_faces()

    # THEN
    assert sheet_exists(aft_br00011_path, inx_str)
    aft_e3_df = pandas_read_excel(aft_br00011_path, sheet_name=inx_str)
    pandas_assert_frame_equal(aft_e3_df, e3_music23_df)


def test_bow_inx_event_bricks_to_aft_faces_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    br00011_columns = [
        face_id_str(),
        event_id_str(),
        deal_id_str(),
        owner_id_str(),
        acct_id_str(),
    ]
    music23_str = "music23"
    sue0 = [sue_inx, event3, music23_str, bob_inx, bob_inx]
    sue1 = [sue_inx, event3, music23_str, yao_inx, bob_inx]
    sue2 = [sue_inx, event3, music23_str, yao_inx, yao_inx]
    sue3 = [sue_inx, event7, music23_str, yao_inx, yao_inx]
    e3_music23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    e7_music23_df = DataFrame([sue3], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    fizz_world = worldunit_shop("fizz")
    bow_sue_dir = create_path(fizz_world._faces_bow_dir, sue_otx)
    bow_e3_dir = create_path(bow_sue_dir, event3)
    bow_e7_dir = create_path(bow_sue_dir, event7)
    bow_e3_br00011_path = create_path(bow_e3_dir, br00011_filename)
    bow_e7_br00011_path = create_path(bow_e7_dir, br00011_filename)
    inx_str = "inx"
    upsert_sheet(bow_e3_br00011_path, inx_str, e3_music23_df)
    upsert_sheet(bow_e7_br00011_path, inx_str, e7_music23_df)
    assert sheet_exists(bow_e3_br00011_path, inx_str)
    assert sheet_exists(bow_e7_br00011_path, inx_str)
    sue_aft_dir = create_path(fizz_world._faces_aft_dir, sue_inx)
    aft_br00011_path = create_path(sue_aft_dir, br00011_filename)
    print(f"{bow_e3_br00011_path=}")
    print(f"{aft_br00011_path=}")
    assert sheet_exists(aft_br00011_path, inx_str) is False

    # WHEN
    fizz_world.bow_inx_event_bricks_to_aft_faces()

    # THEN
    assert sheet_exists(aft_br00011_path, inx_str)
    sue_music23_df = DataFrame([sue0, sue1, sue2, sue3], columns=br00011_columns)
    aft_sue_df = pandas_read_excel(aft_br00011_path, sheet_name=inx_str)
    print(f"{aft_sue_df=}")
    pandas_assert_frame_equal(aft_sue_df, sue_music23_df)
