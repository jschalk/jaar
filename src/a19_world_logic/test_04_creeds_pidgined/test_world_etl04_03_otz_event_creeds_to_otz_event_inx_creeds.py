from src.a00_data_toolbox.file_toolbox import create_path, save_file
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_label_str
from src.a06_bud_logic._utils.str_a06 import (
    acct_name_str,
    face_name_str,
    event_int_str,
    type_NameStr_str,
    type_LabelStr_str,
)
from src.a16_pidgin_logic._utils.str_a16 import pidgin_filename
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from src.a17_creed_logic._utils.str_a17 import brick_valid_str
from src.a17_creed_logic.creed_db_tool import upsert_sheet, sheet_exists
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_otz_event_creeds_to_brick_events_Scenario0_NoPidginUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_otx = "Sue"
    bob_otx = "Bob"
    yao_otx = "Yao"
    event3 = 3
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    accord23_str = "accord23"
    sue0 = [event3, sue_otx, accord23_str, bob_otx, bob_otx]
    sue1 = [event3, sue_otx, accord23_str, yao_otx, bob_otx]
    sue2 = [event3, sue_otx, accord23_str, yao_otx, yao_otx]
    e3_accord23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    fizz_world._pidgin_events = {}
    sue_otz_dir = create_path(fizz_world._syntax_otz_dir, sue_otx)
    otz_e3_dir = create_path(sue_otz_dir, event3)
    brick_e3_br00011_path = create_path(otz_e3_dir, br00011_filename)
    print(f"{brick_e3_br00011_path=}")
    upsert_sheet(brick_e3_br00011_path, brick_valid_str(), e3_accord23_df)
    print(f"{brick_valid_str()=}")
    inx_str = "inx"
    assert sheet_exists(brick_e3_br00011_path, inx_str) is False

    # WHEN
    fizz_world.otz_event_creeds_to_inz_events()

    # THEN
    assert sheet_exists(brick_e3_br00011_path, inx_str)
    e3_inx_df = pandas_read_excel(brick_e3_br00011_path, sheet_name=inx_str)
    sue_i0 = [event3, sue_otx, accord23_str, bob_otx, bob_otx]
    sue_i1 = [event3, sue_otx, accord23_str, yao_otx, bob_otx]
    sue_i2 = [event3, sue_otx, accord23_str, yao_otx, yao_otx]
    example_e3_inx_df = DataFrame([sue_i0, sue_i1, sue_i2], columns=br00011_columns)
    pandas_assert_frame_equal(e3_inx_df, example_e3_inx_df)


def test_etl_otz_event_creeds_to_brick_events_Scenario1_MultpleFaceNames_CreatesEventInxSheets(
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
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    accord23_str = "accord23"
    accord55_otx = "accord55"
    accord55_inx = "musik5555"
    sue0 = [event3, sue_otx, accord23_str, bob_otx, bob_otx]
    sue1 = [event3, sue_otx, accord23_str, yao_otx, bob_otx]
    sue2 = [event3, sue_otx, accord23_str, yao_otx, yao_otx]
    zia0 = [event7, zia_otx, accord23_str, bob_otx, bob_otx]
    zia1 = [event9, zia_otx, accord23_str, yao_otx, bob_otx]
    zia2 = [event9, zia_otx, accord23_str, yao_otx, yao_otx]
    zia3 = [event9, zia_otx, accord55_otx, bob_otx, yao_otx]
    bob0_inx = "Bobby"
    bob1_inx = "Bobito"
    bob2_inx = "Bobbie"
    yao0_inx = "Yaoy"
    yao1_inx = "Yaoito"
    yao2_inx = "Yaobie"
    e3_accord23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    e7_accord23_df = DataFrame([zia0], columns=br00011_columns)
    e9_accord23_df = DataFrame([zia1, zia2, zia3], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    fizz_world._pidgin_events = {sue_otx: {event3}, zia_otx: {event7, event9}}
    sue_otz_dir = create_path(fizz_world._syntax_otz_dir, sue_otx)
    zia_otz_dir = create_path(fizz_world._syntax_otz_dir, zia_otx)
    otz_e3_dir = create_path(sue_otz_dir, event3)
    otz_e7_dir = create_path(zia_otz_dir, event7)
    otz_e9_dir = create_path(zia_otz_dir, event9)
    brick_e3_br00011_path = create_path(otz_e3_dir, br00011_filename)
    brick_e7_br00011_path = create_path(otz_e7_dir, br00011_filename)
    brick_e9_br00011_path = create_path(otz_e9_dir, br00011_filename)
    print(f"{brick_e3_br00011_path=}")
    print(f"{brick_e7_br00011_path=}")
    print(f"{brick_e9_br00011_path=}")
    upsert_sheet(brick_e3_br00011_path, brick_valid_str(), e3_accord23_df)
    upsert_sheet(brick_e7_br00011_path, brick_valid_str(), e7_accord23_df)
    upsert_sheet(brick_e9_br00011_path, brick_valid_str(), e9_accord23_df)
    print(f"{brick_valid_str()=}")
    inx_str = "inx"
    e3_pidginunit = pidginunit_shop(sue_otx, event3)
    e7_pidginunit = pidginunit_shop(zia_otx, event7)
    e9_pidginunit = pidginunit_shop(zia_otx, event9)
    e3_pidginunit.set_otx2inx(type_NameStr_str(), sue_otx, sue_inx)
    e3_pidginunit.set_otx2inx(type_NameStr_str(), bob_otx, bob0_inx)
    e3_pidginunit.set_otx2inx(type_NameStr_str(), yao_otx, yao0_inx)
    e7_pidginunit.set_otx2inx(type_NameStr_str(), zia_otx, zia_inx)
    e7_pidginunit.set_otx2inx(type_NameStr_str(), bob_otx, bob1_inx)
    e7_pidginunit.set_otx2inx(type_NameStr_str(), yao_otx, yao1_inx)
    e9_pidginunit.set_otx2inx(type_NameStr_str(), zia_otx, zia_inx)
    e9_pidginunit.set_otx2inx(type_NameStr_str(), bob_otx, bob2_inx)
    e9_pidginunit.set_otx2inx(type_NameStr_str(), yao_otx, yao2_inx)
    e9_pidginunit.set_otx2inx(type_LabelStr_str(), accord55_inx, accord55_otx)
    save_file(otz_e3_dir, pidgin_filename(), e3_pidginunit.get_json())
    save_file(otz_e7_dir, pidgin_filename(), e7_pidginunit.get_json())
    save_file(otz_e9_dir, pidgin_filename(), e9_pidginunit.get_json())
    assert sheet_exists(brick_e3_br00011_path, inx_str) is False
    assert sheet_exists(brick_e7_br00011_path, inx_str) is False
    assert sheet_exists(brick_e9_br00011_path, inx_str) is False

    # WHEN
    fizz_world.otz_event_creeds_to_inz_events()

    # THEN
    assert sheet_exists(brick_e3_br00011_path, inx_str)
    assert sheet_exists(brick_e7_br00011_path, inx_str)
    assert sheet_exists(brick_e9_br00011_path, inx_str)
    e3_inx_df = pandas_read_excel(brick_e3_br00011_path, sheet_name=inx_str)
    e7_inx_df = pandas_read_excel(brick_e7_br00011_path, sheet_name=inx_str)
    e9_inx_df = pandas_read_excel(brick_e9_br00011_path, sheet_name=inx_str)
    sue_i0 = [event3, sue_inx, accord23_str, bob0_inx, bob0_inx]
    sue_i1 = [event3, sue_inx, accord23_str, yao0_inx, bob0_inx]
    sue_i2 = [event3, sue_inx, accord23_str, yao0_inx, yao0_inx]
    zia_i0 = [event7, zia_inx, accord23_str, bob1_inx, bob1_inx]
    zia_i1 = [event9, zia_inx, accord23_str, yao2_inx, bob2_inx]
    zia_i2 = [event9, zia_inx, accord23_str, yao2_inx, yao2_inx]
    zia_i3 = [event9, zia_inx, accord55_otx, bob2_inx, yao2_inx]
    example_e3_inx_df = DataFrame([sue_i0, sue_i1, sue_i2], columns=br00011_columns)
    example_e7_inx_df = DataFrame([zia_i0], columns=br00011_columns)
    example_e9_inx_df = DataFrame([zia_i1, zia_i2, zia_i3], columns=br00011_columns)
    pandas_assert_frame_equal(e3_inx_df, example_e3_inx_df)
    pandas_assert_frame_equal(e7_inx_df, example_e7_inx_df)
    pandas_assert_frame_equal(e9_inx_df, example_e9_inx_df)
