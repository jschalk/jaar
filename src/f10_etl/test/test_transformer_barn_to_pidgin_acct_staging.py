from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    face_id_str,
    fiscal_id_str,
    acct_id_str,
    owner_id_str,
)
from src.f08_pidgin.pidgin_config import (
    event_id_str,
    inx_wall_str,
    otx_wall_str,
    inx_acct_id_str,
    otx_acct_id_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet, barn_agg_str
from src.f10_etl.transformers import etl_barn_agg_to_pidgin_acct_staging
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_barn_agg_to_pidgin_acct_staging_CreatesFile_Scenario0_SingleBrick(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    m_str = "music23"
    event7 = 7
    x_barn_dir = get_test_etl_dir()
    br00113_file_path = create_path(x_barn_dir, "br00113.xlsx")
    br00113_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, barn_agg_str(), br00113_df)
    pidgin_path = create_path(x_barn_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event7}
    etl_barn_agg_to_pidgin_acct_staging(legitimate_events, x_barn_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    acct_staging_str = "acct_staging"
    gen_acct_df = pandas_read_excel(pidgin_path, sheet_name=acct_staging_str)
    acct_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_acct_df.columns) == acct_file_columns
    assert len(gen_acct_df) == 2
    bx = "br00113"
    e1_acct0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_acct1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_acct_rows = [e1_acct0, e1_acct1]
    e1_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
    assert len(gen_acct_df) == len(e1_acct_df)
    print(f"{gen_acct_df.to_csv()=}")
    print(f" {e1_acct_df.to_csv()=}")
    assert gen_acct_df.to_csv(index=False) == e1_acct_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [acct_staging_str]


def test_etl_barn_agg_to_pidgin_acct_staging_CreatesFile_Scenario1_MultipleBricksFiles(
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
    m_str = "music23"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    x_barn_dir = get_test_etl_dir()
    br00113_file_path = create_path(x_barn_dir, "br00113.xlsx")
    br00113_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
    ]
    br00043_file_path = create_path(x_barn_dir, "br00043.xlsx")
    br00043_columns = [
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, barn_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, barn_agg_str(), br00043_df)
    pidgin_path = create_path(x_barn_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event7, event5}
    etl_barn_agg_to_pidgin_acct_staging(legitimate_events, x_barn_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    acct_staging_str = "acct_staging"
    gen_acct_df = pandas_read_excel(pidgin_path, sheet_name=acct_staging_str)
    acct_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_acct_df.columns) == acct_file_columns
    assert len(gen_acct_df) == 5
    b3 = "br00113"
    b4 = "br00043"
    e1_acct3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_acct4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_acct5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_acct0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_acct1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

    e1_acct_rows = [e1_acct3, e1_acct4, e1_acct5, e1_acct0, e1_acct1]
    e1_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
    assert len(gen_acct_df) == len(e1_acct_df)
    print(f"{gen_acct_df.to_csv()=}")
    print(f" {e1_acct_df.to_csv()=}")
    assert gen_acct_df.to_csv(index=False) == e1_acct_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [acct_staging_str]


def test_etl_barn_agg_to_pidgin_acct_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    m_str = "music23"
    event1 = 1
    event2 = 2
    event5 = 5
    x_barn_dir = get_test_etl_dir()
    br00113_file_path = create_path(x_barn_dir, "br00113.xlsx")
    br00113_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
    ]
    br00043_file_path = create_path(x_barn_dir, "br00043.xlsx")
    br00043_columns = [
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, barn_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, barn_agg_str(), br00043_df)
    pidgin_path = create_path(x_barn_dir, "pidgin.xlsx")
    legitimate_events = {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_barn_agg_to_pidgin_acct_staging(legitimate_events, x_barn_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    acct_staging_str = "acct_staging"
    gen_acct_df = pandas_read_excel(pidgin_path, sheet_name=acct_staging_str)
    acct_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_acct_df.columns) == acct_file_columns
    assert len(gen_acct_df) == 2
    b3 = "br00113"
    b4 = "br00043"
    e1_acct3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_acct4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_acct_rows = [e1_acct3, e1_acct4]
    e1_acct_df = DataFrame(e1_acct_rows, columns=acct_file_columns)
    assert len(gen_acct_df) == len(e1_acct_df)
    print(f"{gen_acct_df.to_csv()=}")
    print(f" {e1_acct_df.to_csv()=}")
    assert gen_acct_df.to_csv(index=False) == e1_acct_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [acct_staging_str]
