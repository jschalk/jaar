from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.str_helpers import owner_name_str, fisc_tag_str
from src.a08_bud_atom_logic.atom_config import (
    acct_name_str,
    face_name_str,
    event_int_str,
)
from src.a17_idea_logic.idea_db_tool import upsert_sheet, sheet_exists
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_utils import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_otz_inx_event_ideas_to_inz_faces_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    accord23_str = "accord23"
    sue0 = [sue_inx, event3, accord23_str, bob_inx, bob_inx]
    sue1 = [sue_inx, event3, accord23_str, yao_inx, bob_inx]
    sue2 = [sue_inx, event3, accord23_str, yao_inx, yao_inx]
    e3_accord23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    otz_sue_dir = create_path(fizz_world._syntax_otz_dir, sue_otx)
    otz_e3_dir = create_path(otz_sue_dir, event3)
    otz_e3_br00011_path = create_path(otz_e3_dir, br00011_filename)
    inx_str = "inx"
    upsert_sheet(otz_e3_br00011_path, inx_str, e3_accord23_df)
    assert sheet_exists(otz_e3_br00011_path, inx_str)
    inz_sue_dir = create_path(fizz_world._syntax_inz_dir, sue_inx)
    inz_br00011_path = create_path(inz_sue_dir, br00011_filename)
    print(f"{otz_e3_br00011_path=}")
    print(f"{inz_br00011_path=}")
    assert sheet_exists(inz_br00011_path, inx_str) is False

    # WHEN
    fizz_world.otz_inx_event_ideas_to_inz_faces()

    # THEN
    assert sheet_exists(inz_br00011_path, inx_str)
    inz_e3_df = pandas_read_excel(inz_br00011_path, sheet_name=inx_str)
    pandas_assert_frame_equal(inz_e3_df, e3_accord23_df)


def test_otz_inx_event_ideas_to_inz_faces_Scenario1(env_dir_setup_cleanup):
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
        fisc_tag_str(),
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
    fizz_world = worldunit_shop("fizz", worlds_dir())
    otz_sue_dir = create_path(fizz_world._syntax_otz_dir, sue_otx)
    otz_e3_dir = create_path(otz_sue_dir, event3)
    otz_e7_dir = create_path(otz_sue_dir, event7)
    otz_e3_br00011_path = create_path(otz_e3_dir, br00011_filename)
    otz_e7_br00011_path = create_path(otz_e7_dir, br00011_filename)
    inx_str = "inx"
    upsert_sheet(otz_e3_br00011_path, inx_str, e3_accord23_df)
    upsert_sheet(otz_e7_br00011_path, inx_str, e7_accord23_df)
    assert sheet_exists(otz_e3_br00011_path, inx_str)
    assert sheet_exists(otz_e7_br00011_path, inx_str)
    sue_inz_dir = create_path(fizz_world._syntax_inz_dir, sue_inx)
    inz_br00011_path = create_path(sue_inz_dir, br00011_filename)
    print(f"{otz_e3_br00011_path=}")
    print(f"{inz_br00011_path=}")
    assert sheet_exists(inz_br00011_path, inx_str) is False

    # WHEN
    fizz_world.otz_inx_event_ideas_to_inz_faces()

    # THEN
    assert sheet_exists(inz_br00011_path, inx_str)
    sue_accord23_df = DataFrame([sue0, sue1, sue2, sue3], columns=br00011_columns)
    inz_sue_df = pandas_read_excel(inz_br00011_path, sheet_name=inx_str)
    print(f"{inz_sue_df=}")
    pandas_assert_frame_equal(inz_sue_df, sue_accord23_df)
