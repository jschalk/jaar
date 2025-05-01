from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)
from src.a17_idea_logic._utils.str_a17 import brick_agg_str
from src.a17_idea_logic.idea_db_tool import get_sheet_names, upsert_sheet
from src.a18_etl_toolbox.tran_path import create_brick_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import etl_brick_agg_to_pidgin_road_raw
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_brick_agg_to_pidgin_road_raw_CreatesFile_Scenario0_SingleIdea(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    m_str = "accord23"
    event7 = 7
    x_brick_dir = get_module_temp_dir()
    br00117_file_path = create_path(x_brick_dir, "br00117.xlsx")
    br00117_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    sue0 = [event7, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event7, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, brick_agg_str(), br00117_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_brick_agg_to_pidgin_road_raw({event7}, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    road_raw_str = "road_raw"
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_raw_str)
    road_raw_columns = PidginPrimeColumns().pidgin_road_raw_columns
    assert list(gen_road_df.columns) == road_raw_columns
    assert len(gen_road_df) == 2
    bx = "br00117"
    e1_road0 = [bx, event7, sue_str, yao_str, yao_inx, None, None, None]
    e1_road1 = [bx, event7, sue_str, bob_str, bob_inx, None, None, None]
    e1_road_rows = [e1_road0, e1_road1]
    e1_road_df = DataFrame(e1_road_rows, columns=road_raw_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [road_raw_str]


def test_etl_brick_agg_to_pidgin_road_raw_CreatesFile_Scenario1_MultipleIdeasFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    m_str = "accord23"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    x_brick_dir = get_module_temp_dir()
    br00117_file_path = create_path(x_brick_dir, "br00117.xlsx")
    br00117_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(x_brick_dir, "br00045.xlsx")
    br00045_columns = [
        event_int_str(),
        face_name_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event7, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, brick_agg_str(), br00117_df)
    br00045_rows = [sue2, sue3, yao1]
    br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
    upsert_sheet(br00045_file_path, brick_agg_str(), br00045_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event5, event7}
    etl_brick_agg_to_pidgin_road_raw(legitimate_events, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    road_raw_str = "road_raw"
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_raw_str)
    road_raw_columns = PidginPrimeColumns().pidgin_road_raw_columns
    assert list(gen_road_df.columns) == road_raw_columns
    assert len(gen_road_df) == 5
    b3 = "br00117"
    b4 = "br00045"
    e1_road3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_road4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_road5 = [b4, event7, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    e1_road0 = [b3, event1, sue_str, yao_str, yao_inx, None, None, None]
    e1_road1 = [b3, event1, sue_str, bob_str, bob_inx, None, None, None]

    e1_road_rows = [e1_road3, e1_road4, e1_road5, e1_road0, e1_road1]
    e1_road_df = DataFrame(e1_road_rows, columns=road_raw_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [road_raw_str]


def test_etl_brick_agg_to_pidgin_road_raw_CreatesFile_Scenario2_WorldUnit_events_Filters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    m_str = "accord23"
    event1 = 1
    event2 = 2
    event5 = 5
    x_brick_dir = get_module_temp_dir()
    br00117_file_path = create_path(x_brick_dir, "br00117.xlsx")
    br00117_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(x_brick_dir, "br00045.xlsx")
    br00045_columns = [
        event_int_str(),
        face_name_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, brick_agg_str(), br00117_df)
    br00045_rows = [sue2, sue3, yao1]
    br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
    upsert_sheet(br00045_file_path, brick_agg_str(), br00045_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    legitimate_events = {event2, event5}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_brick_agg_to_pidgin_road_raw(legitimate_events, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    road_raw_str = "road_raw"
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_raw_str)
    road_raw_columns = PidginPrimeColumns().pidgin_road_raw_columns
    assert list(gen_road_df.columns) == road_raw_columns
    assert len(gen_road_df) == 2
    b3 = "br00117"
    b4 = "br00045"
    e1_road3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_road4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_road_rows = [e1_road3, e1_road4]
    e1_road_df = DataFrame(e1_road_rows, columns=road_raw_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [road_raw_str]
