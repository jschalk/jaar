from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    face_name_str,
    fiscal_title_str,
    acct_name_str,
    owner_name_str,
)
from src.f08_pidgin.pidgin_config import (
    event_int_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_label_str,
    otx_label_str,
    unknown_word_str,
)
from src.f09_idea.pandas_tool import get_sheet_names, upsert_sheet, boat_agg_str
from src.f10_etl.pidgin_agg import PidginPrimeColumns
from src.f10_etl.transformers import etl_boat_agg_to_pidgin_label_staging
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_boat_agg_to_pidgin_label_staging_CreatesFile_Scenario0_SingleIdea(
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
    x_boat_dir = get_test_etl_dir()
    br00115_file_path = create_path(x_boat_dir, "br00115.xlsx")
    br00115_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, boat_agg_str(), br00115_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event7}
    etl_boat_agg_to_pidgin_label_staging(legitimate_events, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    label_staging_str = "label_staging"
    gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_staging_str)
    label_staging_columns = PidginPrimeColumns().map_label_staging_columns
    assert list(gen_label_df.columns) == label_staging_columns
    assert len(gen_label_df) == 2
    bx = "br00115"
    e1_label0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_label1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_label_rows = [e1_label0, e1_label1]
    e1_label_df = DataFrame(e1_label_rows, columns=label_staging_columns)
    assert len(gen_label_df) == len(e1_label_df)
    print(f"{gen_label_df.to_csv()=}")
    print(f" {e1_label_df.to_csv()=}")
    assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [label_staging_str]


def test_etl_boat_agg_to_pidgin_label_staging_CreatesFile_Scenario1_MultipleIdeasFiles(
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
    x_boat_dir = get_test_etl_dir()
    br00115_file_path = create_path(x_boat_dir, "br00115.xlsx")
    br00115_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00042_file_path = create_path(x_boat_dir, "br00042.xlsx")
    br00042_columns = [
        face_name_str(),
        event_int_str(),
        otx_label_str(),
        inx_label_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, boat_agg_str(), br00115_df)
    br00042_rows = [sue2, sue3, yao1]
    br00042_df = DataFrame(br00042_rows, columns=br00042_columns)
    upsert_sheet(br00042_file_path, boat_agg_str(), br00042_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event5, event7}
    etl_boat_agg_to_pidgin_label_staging(legitimate_events, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    label_staging_str = "label_staging"
    gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_staging_str)
    label_staging_columns = PidginPrimeColumns().map_label_staging_columns
    assert list(gen_label_df.columns) == label_staging_columns
    assert len(gen_label_df) == 5
    b3 = "br00115"
    b4 = "br00042"
    e1_label3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_label4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_label5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_label0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_label1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

    e1_label_rows = [e1_label3, e1_label4, e1_label5, e1_label0, e1_label1]
    e1_label_df = DataFrame(e1_label_rows, columns=label_staging_columns)
    assert len(gen_label_df) == len(e1_label_df)
    print(f"{gen_label_df.to_csv()=}")
    print(f" {e1_label_df.to_csv()=}")
    assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [label_staging_str]


def test_etl_boat_agg_to_pidgin_label_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    x_boat_dir = get_test_etl_dir()
    br00115_file_path = create_path(x_boat_dir, "br00115.xlsx")
    br00115_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00042_file_path = create_path(x_boat_dir, "br00042.xlsx")
    br00042_columns = [
        face_name_str(),
        event_int_str(),
        otx_label_str(),
        inx_label_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, boat_agg_str(), br00115_df)
    b40_rows = [sue2, sue3, yao1]
    br00042_df = DataFrame(b40_rows, columns=br00042_columns)
    upsert_sheet(br00042_file_path, boat_agg_str(), br00042_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event2, event5}
    etl_boat_agg_to_pidgin_label_staging(legitimate_events, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    label_staging_str = "label_staging"
    gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_staging_str)
    label_staging_columns = PidginPrimeColumns().map_label_staging_columns
    assert list(gen_label_df.columns) == label_staging_columns
    assert len(gen_label_df) == 2
    b3 = "br00115"
    b4 = "br00042"
    e1_label3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_label4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_label_rows = [e1_label3, e1_label4]
    e1_label_df = DataFrame(e1_label_rows, columns=label_staging_columns)
    assert len(gen_label_df) == len(e1_label_df)
    print(f"{gen_label_df.to_csv()=}")
    print(f" {e1_label_df.to_csv()=}")
    assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [label_staging_str]
