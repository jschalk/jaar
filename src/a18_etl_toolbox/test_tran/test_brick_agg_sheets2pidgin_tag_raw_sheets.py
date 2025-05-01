from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a16_pidgin_logic._utils.str_a16 import (
    inx_bridge_str,
    otx_bridge_str,
    inx_tag_str,
    otx_tag_str,
    unknown_word_str,
)
from src.a17_idea_logic._utils.str_a17 import brick_agg_str
from src.a17_idea_logic.idea_db_tool import get_sheet_names, upsert_sheet
from src.a18_etl_toolbox.tran_path import create_brick_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import etl_brick_agg_to_pidgin_tag_raw
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_brick_agg_to_pidgin_tag_raw_CreatesFile_Scenario0_SingleIdea(
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
    br00116_file_path = create_path(x_brick_dir, "br00116.xlsx")
    br00116_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_tag_str(),
        inx_tag_str(),
    ]
    sue0 = [event7, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event7, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, brick_agg_str(), br00116_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_brick_agg_to_pidgin_tag_raw({event7}, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    tag_raw_str = "tag_raw"
    gen_tag_df = pandas_read_excel(pidgin_path, sheet_name=tag_raw_str)
    tag_raw_columns = PidginPrimeColumns().pidgin_tag_raw_columns
    assert list(gen_tag_df.columns) == tag_raw_columns
    assert len(gen_tag_df) == 2
    bx = "br00116"
    e1_tag0 = [bx, event7, sue_str, yao_str, yao_inx, None, None, None]
    e1_tag1 = [bx, event7, sue_str, bob_str, bob_inx, None, None, None]
    e1_tag_rows = [e1_tag0, e1_tag1]
    e1_tag_df = DataFrame(e1_tag_rows, columns=tag_raw_columns)
    assert len(gen_tag_df) == len(e1_tag_df)
    print(f"{gen_tag_df.to_csv()=}")
    print(f" {e1_tag_df.to_csv()=}")
    assert gen_tag_df.to_csv(index=False) == e1_tag_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [tag_raw_str]


def test_etl_brick_agg_to_pidgin_tag_raw_CreatesFile_Scenario1_MultipleIdeasFiles(
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
    br00116_file_path = create_path(x_brick_dir, "br00116.xlsx")
    br00116_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_tag_str(),
        inx_tag_str(),
    ]
    br00044_file_path = create_path(x_brick_dir, "br00044.xlsx")
    br00044_columns = [
        event_int_str(),
        face_name_str(),
        otx_tag_str(),
        inx_tag_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event7, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, brick_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, brick_agg_str(), br00044_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event5, event7}
    etl_brick_agg_to_pidgin_tag_raw(legitimate_events, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    tag_raw_str = "tag_raw"
    gen_tag_df = pandas_read_excel(pidgin_path, sheet_name=tag_raw_str)
    tag_raw_columns = PidginPrimeColumns().pidgin_tag_raw_columns
    assert list(gen_tag_df.columns) == tag_raw_columns
    assert len(gen_tag_df) == 5
    b3 = "br00116"
    b4 = "br00044"
    e1_tag3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_tag4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_tag5 = [b4, event7, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    e1_tag0 = [b3, event1, sue_str, yao_str, yao_inx, None, None, None]
    e1_tag1 = [b3, event1, sue_str, bob_str, bob_inx, None, None, None]

    e1_tag_rows = [e1_tag3, e1_tag4, e1_tag5, e1_tag0, e1_tag1]
    e1_tag_df = DataFrame(e1_tag_rows, columns=tag_raw_columns)
    assert len(gen_tag_df) == len(e1_tag_df)
    print(f"{gen_tag_df.to_csv()=}")
    print(f" {e1_tag_df.to_csv()=}")
    assert gen_tag_df.to_csv(index=False) == e1_tag_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [tag_raw_str]


def test_etl_brick_agg_to_pidgin_tag_raw_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    br00116_file_path = create_path(x_brick_dir, "br00116.xlsx")
    br00116_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_tag_str(),
        inx_tag_str(),
    ]
    br00044_file_path = create_path(x_brick_dir, "br00044.xlsx")
    br00044_columns = [
        event_int_str(),
        face_name_str(),
        otx_tag_str(),
        inx_tag_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [event1, sue_str, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [event1, sue_str, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [event1, yao_str, yao_str, yao_inx, rdx, rdx, ukx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, brick_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, brick_agg_str(), br00044_df)
    pidgin_path = create_brick_pidgin_path(x_brick_dir)
    legitimate_events = {event2, event5}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_brick_agg_to_pidgin_tag_raw(legitimate_events, x_brick_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    tag_raw_str = "tag_raw"
    gen_tag_df = pandas_read_excel(pidgin_path, sheet_name=tag_raw_str)
    tag_raw_columns = PidginPrimeColumns().pidgin_tag_raw_columns
    assert list(gen_tag_df.columns) == tag_raw_columns
    assert len(gen_tag_df) == 2
    b3 = "br00116"
    b4 = "br00044"
    e1_tag3 = [b4, event2, sue_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_tag4 = [b4, event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_tag_rows = [e1_tag3, e1_tag4]
    e1_tag_df = DataFrame(e1_tag_rows, columns=tag_raw_columns)
    assert len(gen_tag_df) == len(e1_tag_df)
    print(f"{gen_tag_df.to_csv()=}")
    print(f" {e1_tag_df.to_csv()=}")
    assert gen_tag_df.to_csv(index=False) == e1_tag_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [tag_raw_str]
