from src.f00_instrument.file import create_path
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f04_kick.atom_config import face_name_str, acct_name_str, event_int_str
from src.f09_pidgin.pidgin_config import (
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    unknown_word_str,
)
from src.f10_idea.idea_db_tool import get_sheet_names, upsert_sheet, cart_agg_str
from src.f11_etl.tran_path import create_cart_pidgin_path
from src.f11_etl.pidgin_agg import PidginPrimeColumns
from src.f11_etl.transformers import etl_cart_agg_to_pidgin_name_staging
from src.f11_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_cart_agg_to_pidgin_name_staging_CreatesFile_Scenario0_SingleIdea(
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
    x_cart_dir = get_test_etl_dir()
    br00113_file_path = create_path(x_cart_dir, "br00113.xlsx")
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, cart_agg_str(), br00113_df)
    pidgin_path = create_cart_pidgin_path(x_cart_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event7}
    etl_cart_agg_to_pidgin_name_staging(legitimate_events, x_cart_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    name_staging_str = "name_staging"
    gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_staging_str)
    name_staging_columns = PidginPrimeColumns().map_name_staging_columns
    assert list(gen_name_df.columns) == name_staging_columns
    assert len(gen_name_df) == 2
    bx = "br00113"
    e1_name0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_name1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_name_rows = [e1_name0, e1_name1]
    e1_name_df = DataFrame(e1_name_rows, columns=name_staging_columns)
    assert len(gen_name_df) == len(e1_name_df)
    print(f"{gen_name_df.to_csv()=}")
    print(f" {e1_name_df.to_csv()=}")
    assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [name_staging_str]


def test_etl_cart_agg_to_pidgin_name_staging_CreatesFile_Scenario1_MultipleIdeasFiles(
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
    x_cart_dir = get_test_etl_dir()
    br00113_file_path = create_path(x_cart_dir, "br00113.xlsx")
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    br00043_file_path = create_path(x_cart_dir, "br00043.xlsx")
    br00043_columns = [
        face_name_str(),
        event_int_str(),
        otx_name_str(),
        inx_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, cart_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, cart_agg_str(), br00043_df)
    pidgin_path = create_cart_pidgin_path(x_cart_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event7, event5}
    etl_cart_agg_to_pidgin_name_staging(legitimate_events, x_cart_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    name_staging_str = "name_staging"
    gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_staging_str)
    name_staging_columns = PidginPrimeColumns().map_name_staging_columns
    assert list(gen_name_df.columns) == name_staging_columns
    assert len(gen_name_df) == 5
    b3 = "br00113"
    b4 = "br00043"
    e1_name3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_name4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_name5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_name0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_name1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

    e1_name_rows = [e1_name3, e1_name4, e1_name5, e1_name0, e1_name1]
    e1_name_df = DataFrame(e1_name_rows, columns=name_staging_columns)
    assert len(gen_name_df) == len(e1_name_df)
    print(f"{gen_name_df.to_csv()=}")
    print(f" {e1_name_df.to_csv()=}")
    assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [name_staging_str]


def test_etl_cart_agg_to_pidgin_name_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    x_cart_dir = get_test_etl_dir()
    br00113_file_path = create_path(x_cart_dir, "br00113.xlsx")
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    br00043_file_path = create_path(x_cart_dir, "br00043.xlsx")
    br00043_columns = [
        face_name_str(),
        event_int_str(),
        otx_name_str(),
        inx_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, cart_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, cart_agg_str(), br00043_df)
    pidgin_path = create_cart_pidgin_path(x_cart_dir)
    legitimate_events = {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_cart_agg_to_pidgin_name_staging(legitimate_events, x_cart_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    name_staging_str = "name_staging"
    gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_staging_str)
    name_staging_columns = PidginPrimeColumns().map_name_staging_columns
    assert list(gen_name_df.columns) == name_staging_columns
    assert len(gen_name_df) == 2
    b3 = "br00113"
    b4 = "br00043"
    e1_name3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_name4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_name_rows = [e1_name3, e1_name4]
    e1_name_df = DataFrame(e1_name_rows, columns=name_staging_columns)
    assert len(gen_name_df) == len(e1_name_df)
    print(f"{gen_name_df.to_csv()=}")
    print(f" {e1_name_df.to_csv()=}")
    assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [name_staging_str]
