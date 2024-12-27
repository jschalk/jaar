from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    face_id_str,
    deal_id_str,
    acct_id_str,
    owner_id_str,
)
from src.f08_pidgin.pidgin_config import (
    event_id_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_idea_str,
    otx_idea_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet, boat_agg_str
from src.f10_etl.transformers import etl_boat_agg_to_pidgin_idea_staging
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_boat_agg_to_pidgin_idea_staging_CreatesFile_Scenario0_SingleBrick(
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
    x_boat_dir = get_test_etl_dir()
    br00116_file_path = create_path(x_boat_dir, "br00116.xlsx")
    br00116_columns = [
        face_id_str(),
        event_id_str(),
        deal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_idea_str(),
        inx_idea_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, boat_agg_str(), br00116_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_boat_agg_to_pidgin_idea_staging({event7}, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    idea_staging_str = "idea_staging"
    gen_idea_df = pandas_read_excel(pidgin_path, sheet_name=idea_staging_str)
    idea_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_idea_str(),
        inx_idea_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_idea_df.columns) == idea_file_columns
    assert len(gen_idea_df) == 2
    bx = "br00116"
    e1_idea0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_idea1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_idea_rows = [e1_idea0, e1_idea1]
    e1_idea_df = DataFrame(e1_idea_rows, columns=idea_file_columns)
    assert len(gen_idea_df) == len(e1_idea_df)
    print(f"{gen_idea_df.to_csv()=}")
    print(f" {e1_idea_df.to_csv()=}")
    assert gen_idea_df.to_csv(index=False) == e1_idea_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [idea_staging_str]


def test_etl_boat_agg_to_pidgin_idea_staging_CreatesFile_Scenario1_MultipleBricksFiles(
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
    x_boat_dir = get_test_etl_dir()
    br00116_file_path = create_path(x_boat_dir, "br00116.xlsx")
    br00116_columns = [
        face_id_str(),
        event_id_str(),
        deal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_idea_str(),
        inx_idea_str(),
    ]
    br00044_file_path = create_path(x_boat_dir, "br00044.xlsx")
    br00044_columns = [
        face_id_str(),
        event_id_str(),
        otx_idea_str(),
        inx_idea_str(),
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
    upsert_sheet(br00116_file_path, boat_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, boat_agg_str(), br00044_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event5, event7}
    etl_boat_agg_to_pidgin_idea_staging(legitimate_events, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    idea_staging_str = "idea_staging"
    gen_idea_df = pandas_read_excel(pidgin_path, sheet_name=idea_staging_str)
    idea_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_idea_str(),
        inx_idea_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_idea_df.columns) == idea_file_columns
    assert len(gen_idea_df) == 5
    b3 = "br00116"
    b4 = "br00044"
    e1_idea3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_idea4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_idea5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_idea0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_idea1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

    e1_idea_rows = [e1_idea3, e1_idea4, e1_idea5, e1_idea0, e1_idea1]
    e1_idea_df = DataFrame(e1_idea_rows, columns=idea_file_columns)
    assert len(gen_idea_df) == len(e1_idea_df)
    print(f"{gen_idea_df.to_csv()=}")
    print(f" {e1_idea_df.to_csv()=}")
    assert gen_idea_df.to_csv(index=False) == e1_idea_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [idea_staging_str]


def test_etl_boat_agg_to_pidgin_idea_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    x_boat_dir = get_test_etl_dir()
    br00116_file_path = create_path(x_boat_dir, "br00116.xlsx")
    br00116_columns = [
        face_id_str(),
        event_id_str(),
        deal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_idea_str(),
        inx_idea_str(),
    ]
    br00044_file_path = create_path(x_boat_dir, "br00044.xlsx")
    br00044_columns = [
        face_id_str(),
        event_id_str(),
        otx_idea_str(),
        inx_idea_str(),
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
    upsert_sheet(br00116_file_path, boat_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, boat_agg_str(), br00044_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    legitimate_events = {event2, event5}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_boat_agg_to_pidgin_idea_staging(legitimate_events, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    idea_staging_str = "idea_staging"
    gen_idea_df = pandas_read_excel(pidgin_path, sheet_name=idea_staging_str)
    idea_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_idea_str(),
        inx_idea_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_idea_df.columns) == idea_file_columns
    assert len(gen_idea_df) == 2
    b3 = "br00116"
    b4 = "br00044"
    e1_idea3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_idea4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_idea_rows = [e1_idea3, e1_idea4]
    e1_idea_df = DataFrame(e1_idea_rows, columns=idea_file_columns)
    assert len(gen_idea_df) == len(e1_idea_df)
    print(f"{gen_idea_df.to_csv()=}")
    print(f" {e1_idea_df.to_csv()=}")
    assert gen_idea_df.to_csv(index=False) == e1_idea_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [idea_staging_str]
