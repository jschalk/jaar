from src.f00_instrument.file import create_path, set_dir, save_file
from src.f04_gift.atom_config import (
    acct_id_str,
    face_id_str,
    fiscal_id_str,
    owner_id_str,
    type_AcctID_str,
)
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str, pidgin_filename
from src.f08_pidgin.pidgin import pidginunit_shop
from src.f09_brick.pandas_tool import upsert_sheet, forge_valid_str, sheet_exists
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_WorldUnit_fiscal_bricks_to_fiscal_inx_Scenario0_MultpleFaceIDs_CreatesFiscalInxSheets(
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
    event8 = 8
    event9 = 9
    br00011_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
    ]
    music23_str = "music23"
    music55_str = "music55"
    sue0 = [sue_otx, event3, music23_str, bob_otx, bob_otx]
    sue1 = [sue_otx, event3, music23_str, yao_otx, bob_otx]
    sue2 = [sue_otx, event3, music23_str, yao_otx, yao_otx]
    zia0 = [zia_otx, event7, music23_str, bob_otx, bob_otx]
    zia1 = [zia_otx, event9, music23_str, yao_otx, bob_otx]
    zia2 = [zia_otx, event9, music23_str, yao_otx, yao_otx]
    zia3 = [zia_otx, event9, music55_str, bob_otx, yao_otx]
    bob0_inx = "Bobby"
    bob1_inx = "Bobito"
    bob2_inx = "Bobbie"
    yao0_inx = "Yaoy"
    yao1_inx = "Yaoito"
    yao2_inx = "Yaobie"
    e3_music23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    e7_music23_df = DataFrame([zia0], columns=br00011_columns)
    e9_music23_df = DataFrame([zia1, zia2], columns=br00011_columns)
    e9_music55_df = DataFrame([zia3], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    fizz_world = worldunit_shop("fizz")
    fizz_world.events = {
        event3: sue_otx,
        event7: zia_otx,
        event8: zia_otx,
        event9: zia_otx,
    }
    fizz_world._fiscal_pidgins = {
        music23_str: {event3: event3, event7: event7, event9: event8},
        music55_str: {event9: event8},
    }
    sue_dir = create_path(fizz_world._faces_otx_dir, sue_otx)
    zia_dir = create_path(fizz_world._faces_otx_dir, zia_otx)
    event3_dir = create_path(sue_dir, event3)
    event7_dir = create_path(zia_dir, event7)
    event8_dir = create_path(zia_dir, event8)
    event9_dir = create_path(zia_dir, event9)
    e3_music23_dir = create_path(event3_dir, music23_str)
    e7_music23_dir = create_path(event7_dir, music23_str)
    e9_music23_dir = create_path(event9_dir, music23_str)
    e9_music55_dir = create_path(event9_dir, music55_str)
    e3_music23_br00011_path = create_path(e3_music23_dir, br00011_filename)
    e7_music23_br00011_path = create_path(e7_music23_dir, br00011_filename)
    e9_music23_br00011_path = create_path(e9_music23_dir, br00011_filename)
    e9_music55_br00011_path = create_path(e9_music55_dir, br00011_filename)
    print(f"{e3_music23_br00011_path=}")
    print(f"{e7_music23_br00011_path=}")
    print(f"{e9_music23_br00011_path=}")
    print(f"{e9_music55_br00011_path=}")
    upsert_sheet(e3_music23_br00011_path, forge_valid_str(), e3_music23_df)
    upsert_sheet(e7_music23_br00011_path, forge_valid_str(), e7_music23_df)
    upsert_sheet(e9_music23_br00011_path, forge_valid_str(), e9_music23_df)
    upsert_sheet(e9_music55_br00011_path, forge_valid_str(), e9_music55_df)
    forge_inx_str = "forge_inx"
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
    save_file(event3_dir, pidgin_filename(), e3_pidginunit.get_json())
    save_file(event7_dir, pidgin_filename(), e7_pidginunit.get_json())
    save_file(event8_dir, pidgin_filename(), e9_pidginunit.get_json())
    assert sheet_exists(e7_music23_br00011_path, forge_inx_str) is False
    assert sheet_exists(e3_music23_br00011_path, forge_inx_str) is False
    assert sheet_exists(e9_music23_br00011_path, forge_inx_str) is False
    assert sheet_exists(e9_music55_br00011_path, forge_inx_str) is False

    # WHEN
    fizz_world.fiscal_bricks_to_fiscal_inx()

    # THEN
    assert sheet_exists(e7_music23_br00011_path, forge_inx_str)
    assert sheet_exists(e3_music23_br00011_path, forge_inx_str)
    assert sheet_exists(e9_music23_br00011_path, forge_inx_str)
    assert sheet_exists(e9_music55_br00011_path, forge_inx_str)
    e3_m23_inx_df = pandas_read_excel(e3_music23_br00011_path, sheet_name=forge_inx_str)
    e7_m23_inx_df = pandas_read_excel(e7_music23_br00011_path, sheet_name=forge_inx_str)
    e9_m23_inx_df = pandas_read_excel(e9_music23_br00011_path, sheet_name=forge_inx_str)
    e9_m55_inx_df = pandas_read_excel(e9_music55_br00011_path, sheet_name=forge_inx_str)
    sue_i0 = [sue_inx, event3, music23_str, bob0_inx, bob0_inx]
    sue_i1 = [sue_inx, event3, music23_str, yao0_inx, bob0_inx]
    sue_i2 = [sue_inx, event3, music23_str, yao0_inx, yao0_inx]
    zia_i0 = [zia_inx, event7, music23_str, bob1_inx, bob1_inx]
    zia_i1 = [zia_inx, event9, music23_str, yao2_inx, bob2_inx]
    zia_i2 = [zia_inx, event9, music23_str, yao2_inx, yao2_inx]
    zia_i3 = [zia_inx, event9, music55_str, bob2_inx, yao2_inx]
    example_e3_m23_inx_df = DataFrame([sue_i0, sue_i1, sue_i2], columns=br00011_columns)
    example_e7_m23_inx_df = DataFrame([zia_i0], columns=br00011_columns)
    example_e9_m23_inx_df = DataFrame([zia_i1, zia_i2], columns=br00011_columns)
    example_e9_m55_inx_df = DataFrame([zia_i3], columns=br00011_columns)
    pandas_assert_frame_equal(e3_m23_inx_df, example_e3_m23_inx_df)
    pandas_assert_frame_equal(e7_m23_inx_df, example_e7_m23_inx_df)
    pandas_assert_frame_equal(e9_m23_inx_df, example_e9_m23_inx_df)
    pandas_assert_frame_equal(e9_m55_inx_df, example_e9_m55_inx_df)
