from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_label_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_title_str,
    otx_title_str,
    unknown_term_str,
)
from src.a17_idea_logic._utils.str_a17 import brick_agg_str
from src.a17_idea_logic.idea_db_tool import get_sheet_names, upsert_sheet
from src.a18_etl_toolbox.tran_path import create_brick_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import etl_brick_agg_dfs_to_pidgin_title_raw
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_brick_agg_dfs_to_pidgin_title_raw_CreatesFile_Scenario0_SingleIdea(
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
    br00115_file_path = create_path(x_brick_dir, "br00115.xlsx")
    br00115_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_title_str(),
        inx_title_str(),
    ]
    sue0 = [event7, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event7, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, brick_agg_str(), br00115_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event7}
    etl_brick_agg_dfs_to_pidgin_title_raw(legitimate_events, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    title_raw_str = "title_raw"
    gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_raw_str)
    title_raw_columns = PidginPrimeColumns().pidgin_title_raw_columns
    assert list(gen_title_df.columns) == title_raw_columns
    assert len(gen_title_df) == 2
    bx = "br00115"
    e1_title0 = [bx, event7, sue_str, yao_str, yao_inx, None, None, None]
    e1_title1 = [bx, event7, sue_str, bob_str, bob_inx, None, None, None]
    e1_title_rows = [e1_title0, e1_title1]
    e1_title_df = DataFrame(e1_title_rows, columns=title_raw_columns)
    assert len(gen_title_df) == len(e1_title_df)
    print(f"{gen_title_df.to_csv()=}")
    print(f" {e1_title_df.to_csv()=}")
    assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [title_raw_str]


def test_etl_brick_agg_dfs_to_pidgin_title_raw_CreatesFile_Scenario1_MultipleIdeasFiles(
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
    br00115_file_path = create_path(x_brick_dir, "br00115.xlsx")
    br00115_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_title_str(),
        inx_title_str(),
    ]
    br00042_file_path = create_path(x_brick_dir, "br00042.xlsx")
    br00042_columns = [
        event_int_str(),
        face_name_str(),
        otx_title_str(),
        inx_title_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event7, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, brick_agg_str(), br00115_df)
    br00042_rows = [sue2, sue3, yao1]
    br00042_df = DataFrame(br00042_rows, columns=br00042_columns)
    upsert_sheet(br00042_file_path, brick_agg_str(), br00042_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event5, event7}
    etl_brick_agg_dfs_to_pidgin_title_raw(legitimate_events, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    title_raw_str = "title_raw"
    gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_raw_str)
    title_raw_columns = PidginPrimeColumns().pidgin_title_raw_columns
    assert list(gen_title_df.columns) == title_raw_columns
    assert len(gen_title_df) == 5
    b3 = "br00115"
    b4 = "br00042"
    e1_title3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_title4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_title5 = [b4, event7, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    e1_title0 = [b3, event1, sue_str, yao_str, yao_inx, None, None, None]
    e1_title1 = [b3, event1, sue_str, bob_str, bob_inx, None, None, None]

    e1_title_rows = [e1_title3, e1_title4, e1_title5, e1_title0, e1_title1]
    e1_title_df = DataFrame(e1_title_rows, columns=title_raw_columns)
    assert len(gen_title_df) == len(e1_title_df)
    print(f"{gen_title_df.to_csv()=}")
    print(f" {e1_title_df.to_csv()=}")
    assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [title_raw_str]


def test_etl_brick_agg_dfs_to_pidgin_title_raw_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    br00115_file_path = create_path(x_brick_dir, "br00115.xlsx")
    br00115_columns = [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
        otx_title_str(),
        inx_title_str(),
    ]
    br00042_file_path = create_path(x_brick_dir, "br00042.xlsx")
    br00042_columns = [
        event_int_str(),
        face_name_str(),
        otx_title_str(),
        inx_title_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, brick_agg_str(), br00115_df)
    b40_rows = [sue2, sue3, yao1]
    br00042_df = DataFrame(b40_rows, columns=br00042_columns)
    upsert_sheet(br00042_file_path, brick_agg_str(), br00042_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event2, event5}
    etl_brick_agg_dfs_to_pidgin_title_raw(legitimate_events, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    title_raw_str = "title_raw"
    gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_raw_str)
    title_raw_columns = PidginPrimeColumns().pidgin_title_raw_columns
    assert list(gen_title_df.columns) == title_raw_columns
    assert len(gen_title_df) == 2
    b3 = "br00115"
    b4 = "br00042"
    e1_title3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_title4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_title_rows = [e1_title3, e1_title4]
    e1_title_df = DataFrame(e1_title_rows, columns=title_raw_columns)
    assert len(gen_title_df) == len(e1_title_df)
    print(f"{gen_title_df.to_csv()=}")
    print(f" {e1_title_df.to_csv()=}")
    assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [title_raw_str]
