from src.f00_instrument.file import create_path, save_file
from src.f04_gift.atom_config import (
    acct_id_str,
    face_id_str,
    fiscal_id_str,
    owner_id_str,
    type_AcctID_str,
    type_IdeaUnit_str,
)
from src.f08_pidgin.pidgin_config import event_id_str, pidgin_filename
from src.f08_pidgin.pidgin import pidginunit_shop
from src.f09_brick.pandas_tool import upsert_sheet, fish_valid_str, sheet_exists
from src.f10_etl.transformers import (
    etl_bow_event_bricks_to_inx_events,
    get_most_recent_event_id,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_get_most_recent_event_id_ReturnsObj():
    # ESTABLISH
    assert get_most_recent_event_id(set(), 5) is None
    assert get_most_recent_event_id({7}, 5) is None
    assert get_most_recent_event_id({2}, 5) == 2
    assert get_most_recent_event_id({1}, 5) == 1
    assert get_most_recent_event_id({0, 1}, 5) == 1
    assert get_most_recent_event_id({0, 1, 7}, 5) == 1


def test_etl_bow_event_bricks_to_fish_events_Scenario0_MultpleFaceIDs_CreatesEventInxSheets(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    zia_otx = "Zia"
    zia_inx = "Ziata"
    bob_otx = "Bob"
    yao_otx = "Yao"
    event3 = 3
    event7 = 7
    event9 = 9
    br00011_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
    ]
    music23_str = "music23"
    music55_otx = "music55"
    music55_inx = "musik5555"
    sue0 = [sue_otx, event3, music23_str, bob_otx, bob_otx]
    sue1 = [sue_otx, event3, music23_str, yao_otx, bob_otx]
    sue2 = [sue_otx, event3, music23_str, yao_otx, yao_otx]
    zia0 = [zia_otx, event7, music23_str, bob_otx, bob_otx]
    zia1 = [zia_otx, event9, music23_str, yao_otx, bob_otx]
    zia2 = [zia_otx, event9, music23_str, yao_otx, yao_otx]
    zia3 = [zia_otx, event9, music55_otx, bob_otx, yao_otx]
    bob0_inx = "Bobby"
    bob1_inx = "Bobito"
    bob2_inx = "Bobbie"
    yao0_inx = "Yaoy"
    yao1_inx = "Yaoito"
    yao2_inx = "Yaobie"
    e3_music23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    e7_music23_df = DataFrame([zia0], columns=br00011_columns)
    e9_music23_df = DataFrame([zia1, zia2, zia3], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    x_event_pidgins = {sue_otx: {event3}, zia_otx: {event7, event9}}
    x_bow_dir = create_path(get_test_etl_dir(), "faces_bow")
    sue_bow_dir = create_path(x_bow_dir, sue_otx)
    zia_bow_dir = create_path(x_bow_dir, zia_otx)
    bow_e3_dir = create_path(sue_bow_dir, event3)
    bow_e7_dir = create_path(zia_bow_dir, event7)
    bow_e9_dir = create_path(zia_bow_dir, event9)
    fish_e3_br00011_path = create_path(bow_e3_dir, br00011_filename)
    fish_e7_br00011_path = create_path(bow_e7_dir, br00011_filename)
    fish_e9_br00011_path = create_path(bow_e9_dir, br00011_filename)
    print(f"{fish_e3_br00011_path=}")
    print(f"{fish_e7_br00011_path=}")
    print(f"{fish_e9_br00011_path=}")
    upsert_sheet(fish_e3_br00011_path, fish_valid_str(), e3_music23_df)
    upsert_sheet(fish_e7_br00011_path, fish_valid_str(), e7_music23_df)
    upsert_sheet(fish_e9_br00011_path, fish_valid_str(), e9_music23_df)
    print(f"{fish_valid_str()=}")
    inx_str = "inx"
    e3_pidginunit = pidginunit_shop(sue_otx, event3)
    e7_pidginunit = pidginunit_shop(zia_otx, event7)
    e9_pidginunit = pidginunit_shop(zia_otx, event9)
    e3_pidginunit.set_otx2inx(type_AcctID_str(), sue_otx, sue_inx)
    e3_pidginunit.set_otx2inx(type_AcctID_str(), bob_otx, bob0_inx)
    e3_pidginunit.set_otx2inx(type_AcctID_str(), yao_otx, yao0_inx)
    e7_pidginunit.set_otx2inx(type_AcctID_str(), zia_otx, zia_inx)
    e7_pidginunit.set_otx2inx(type_AcctID_str(), bob_otx, bob1_inx)
    e7_pidginunit.set_otx2inx(type_AcctID_str(), yao_otx, yao1_inx)
    e9_pidginunit.set_otx2inx(type_AcctID_str(), zia_otx, zia_inx)
    e9_pidginunit.set_otx2inx(type_AcctID_str(), bob_otx, bob2_inx)
    e9_pidginunit.set_otx2inx(type_AcctID_str(), yao_otx, yao2_inx)
    e9_pidginunit.set_otx2inx(type_IdeaUnit_str(), music55_inx, music55_otx)
    save_file(bow_e3_dir, pidgin_filename(), e3_pidginunit.get_json())
    save_file(bow_e7_dir, pidgin_filename(), e7_pidginunit.get_json())
    save_file(bow_e9_dir, pidgin_filename(), e9_pidginunit.get_json())
    assert sheet_exists(fish_e3_br00011_path, inx_str) is False
    assert sheet_exists(fish_e7_br00011_path, inx_str) is False
    assert sheet_exists(fish_e9_br00011_path, inx_str) is False

    # WHEN
    etl_bow_event_bricks_to_inx_events(x_bow_dir, x_event_pidgins)

    # THEN
    assert sheet_exists(fish_e3_br00011_path, inx_str)
    assert sheet_exists(fish_e7_br00011_path, inx_str)
    assert sheet_exists(fish_e9_br00011_path, inx_str)
    e3_inx_df = pandas_read_excel(fish_e3_br00011_path, sheet_name=inx_str)
    e7_inx_df = pandas_read_excel(fish_e7_br00011_path, sheet_name=inx_str)
    e9_inx_df = pandas_read_excel(fish_e9_br00011_path, sheet_name=inx_str)
    sue_i0 = [sue_inx, event3, music23_str, bob0_inx, bob0_inx]
    sue_i1 = [sue_inx, event3, music23_str, yao0_inx, bob0_inx]
    sue_i2 = [sue_inx, event3, music23_str, yao0_inx, yao0_inx]
    zia_i0 = [zia_inx, event7, music23_str, bob1_inx, bob1_inx]
    zia_i1 = [zia_inx, event9, music23_str, yao2_inx, bob2_inx]
    zia_i2 = [zia_inx, event9, music23_str, yao2_inx, yao2_inx]
    zia_i3 = [zia_inx, event9, music55_otx, bob2_inx, yao2_inx]
    example_e3_inx_df = DataFrame([sue_i0, sue_i1, sue_i2], columns=br00011_columns)
    example_e7_inx_df = DataFrame([zia_i0], columns=br00011_columns)
    example_e9_inx_df = DataFrame([zia_i1, zia_i2, zia_i3], columns=br00011_columns)
    pandas_assert_frame_equal(e3_inx_df, example_e3_inx_df)
    pandas_assert_frame_equal(e7_inx_df, example_e7_inx_df)
    pandas_assert_frame_equal(e9_inx_df, example_e9_inx_df)
