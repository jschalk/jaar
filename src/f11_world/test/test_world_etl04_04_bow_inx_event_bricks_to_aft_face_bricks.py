from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    acct_name_str,
    face_name_str,
    deal_idea_str,
    owner_name_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
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
        face_name_str(),
        event_int_str(),
        deal_idea_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    accord23_str = "accord23"
    sue0 = [sue_inx, event3, accord23_str, bob_inx, bob_inx]
    sue1 = [sue_inx, event3, accord23_str, yao_inx, bob_inx]
    sue2 = [sue_inx, event3, accord23_str, yao_inx, yao_inx]
    e3_accord23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    fizz_world = worldunit_shop("fizz")
    bow_sue_dir = create_path(fizz_world._faces_bow_dir, sue_otx)
    bow_e3_dir = create_path(bow_sue_dir, event3)
    bow_e3_br00011_path = create_path(bow_e3_dir, br00011_filename)
    inx_str = "inx"
    upsert_sheet(bow_e3_br00011_path, inx_str, e3_accord23_df)
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
    pandas_assert_frame_equal(aft_e3_df, e3_accord23_df)


def test_bow_inx_event_bricks_to_aft_faces_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    event7 = 7
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        deal_idea_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    accord23_str = "accord23"
    sue0 = [sue_inx, event3, accord23_str, bob_inx, bob_inx]
    sue1 = [sue_inx, event3, accord23_str, yao_inx, bob_inx]
    sue2 = [sue_inx, event3, accord23_str, yao_inx, yao_inx]
    sue3 = [sue_inx, event7, accord23_str, yao_inx, yao_inx]
    e3_accord23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    e7_accord23_df = DataFrame([sue3], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    fizz_world = worldunit_shop("fizz")
    bow_sue_dir = create_path(fizz_world._faces_bow_dir, sue_otx)
    bow_e3_dir = create_path(bow_sue_dir, event3)
    bow_e7_dir = create_path(bow_sue_dir, event7)
    bow_e3_br00011_path = create_path(bow_e3_dir, br00011_filename)
    bow_e7_br00011_path = create_path(bow_e7_dir, br00011_filename)
    inx_str = "inx"
    upsert_sheet(bow_e3_br00011_path, inx_str, e3_accord23_df)
    upsert_sheet(bow_e7_br00011_path, inx_str, e7_accord23_df)
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
    sue_accord23_df = DataFrame([sue0, sue1, sue2, sue3], columns=br00011_columns)
    aft_sue_df = pandas_read_excel(aft_br00011_path, sheet_name=inx_str)
    print(f"{aft_sue_df=}")
    pandas_assert_frame_equal(aft_sue_df, sue_accord23_df)
