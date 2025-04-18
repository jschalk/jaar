from src.a00_data_toolboxs.file_toolbox import create_path
from src.a02_finance_toolboxs.deal import owner_name_str, fisc_title_str
from src.a08_bud_atom_logic.atom_config import (
    face_name_str,
    acct_name_str,
    event_int_str,
)
from src.a16_pidgin_logic.pidgin_config import (
    inx_bridge_str,
    otx_bridge_str,
    inx_title_str,
    otx_title_str,
    unknown_word_str,
)
from src.a17_idea_logic.idea_db_tool import get_sheet_names, upsert_sheet, cart_agg_str
from src.a18_etl_toolbox.tran_path import create_cart_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a18_etl_toolbox.transformers import etl_cart_agg_to_pidgin_title_staging
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_cart_agg_to_pidgin_title_staging_CreatesFile_Scenario0_SingleIdea(
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
    br00116_file_path = create_path(x_cart_dir, "br00116.xlsx")
    br00116_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_title_str(),
        inx_title_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, cart_agg_str(), br00116_df)
    pidgin_path = create_cart_pidgin_path(x_cart_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_cart_agg_to_pidgin_title_staging({event7}, x_cart_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    title_staging_str = "title_staging"
    gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_staging_str)
    title_staging_columns = PidginPrimeColumns().map_title_staging_columns
    assert list(gen_title_df.columns) == title_staging_columns
    assert len(gen_title_df) == 2
    bx = "br00116"
    e1_title0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_title1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_title_rows = [e1_title0, e1_title1]
    e1_title_df = DataFrame(e1_title_rows, columns=title_staging_columns)
    assert len(gen_title_df) == len(e1_title_df)
    print(f"{gen_title_df.to_csv()=}")
    print(f" {e1_title_df.to_csv()=}")
    assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [title_staging_str]


def test_etl_cart_agg_to_pidgin_title_staging_CreatesFile_Scenario1_MultipleIdeasFiles(
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
    br00116_file_path = create_path(x_cart_dir, "br00116.xlsx")
    br00116_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_title_str(),
        inx_title_str(),
    ]
    br00044_file_path = create_path(x_cart_dir, "br00044.xlsx")
    br00044_columns = [
        face_name_str(),
        event_int_str(),
        otx_title_str(),
        inx_title_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, cart_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, cart_agg_str(), br00044_df)
    pidgin_path = create_cart_pidgin_path(x_cart_dir)
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event5, event7}
    etl_cart_agg_to_pidgin_title_staging(legitimate_events, x_cart_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    title_staging_str = "title_staging"
    gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_staging_str)
    title_staging_columns = PidginPrimeColumns().map_title_staging_columns
    assert list(gen_title_df.columns) == title_staging_columns
    assert len(gen_title_df) == 5
    b3 = "br00116"
    b4 = "br00044"
    e1_title3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_title4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_title5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_title0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_title1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

    e1_title_rows = [e1_title3, e1_title4, e1_title5, e1_title0, e1_title1]
    e1_title_df = DataFrame(e1_title_rows, columns=title_staging_columns)
    assert len(gen_title_df) == len(e1_title_df)
    print(f"{gen_title_df.to_csv()=}")
    print(f" {e1_title_df.to_csv()=}")
    assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [title_staging_str]


def test_etl_cart_agg_to_pidgin_title_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    br00116_file_path = create_path(x_cart_dir, "br00116.xlsx")
    br00116_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_title_str(),
        inx_title_str(),
    ]
    br00044_file_path = create_path(x_cart_dir, "br00044.xlsx")
    br00044_columns = [
        face_name_str(),
        event_int_str(),
        otx_title_str(),
        inx_title_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, cart_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, cart_agg_str(), br00044_df)
    pidgin_path = create_cart_pidgin_path(x_cart_dir)
    legitimate_events = {event2, event5}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_cart_agg_to_pidgin_title_staging(legitimate_events, x_cart_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    title_staging_str = "title_staging"
    gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_staging_str)
    title_staging_columns = PidginPrimeColumns().map_title_staging_columns
    assert list(gen_title_df.columns) == title_staging_columns
    assert len(gen_title_df) == 2
    b3 = "br00116"
    b4 = "br00044"
    e1_title3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_title4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_title_rows = [e1_title3, e1_title4]
    e1_title_df = DataFrame(e1_title_rows, columns=title_staging_columns)
    assert len(gen_title_df) == len(e1_title_df)
    print(f"{gen_title_df.to_csv()=}")
    print(f" {e1_title_df.to_csv()=}")
    assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [title_staging_str]
