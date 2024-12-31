from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    face_name_str,
    gov_idea_str,
    acct_name_str,
    owner_name_str,
)
from src.f08_pidgin.pidgin_config import (
    event_int_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet, boat_agg_str
from src.f10_etl.transformers import etl_boat_agg_to_pidgin_road_staging
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_boat_agg_to_pidgin_road_staging_CreatesFile_Scenario0_SingleBrick(
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
    br00117_file_path = create_path(x_boat_dir, "br00117.xlsx")
    br00117_columns = [
        face_name_str(),
        event_int_str(),
        gov_idea_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, boat_agg_str(), br00117_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_boat_agg_to_pidgin_road_staging({event7}, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    road_staging_str = "road_staging"
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)
    road_file_columns = [
        "src_brick",
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_road_df.columns) == road_file_columns
    assert len(gen_road_df) == 2
    bx = "br00117"
    e1_road0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_road1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_road_rows = [e1_road0, e1_road1]
    e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [road_staging_str]


def test_etl_boat_agg_to_pidgin_road_staging_CreatesFile_Scenario1_MultipleBricksFiles(
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
    br00117_file_path = create_path(x_boat_dir, "br00117.xlsx")
    br00117_columns = [
        face_name_str(),
        event_int_str(),
        gov_idea_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(x_boat_dir, "br00045.xlsx")
    br00045_columns = [
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, boat_agg_str(), br00117_df)
    br00045_rows = [sue2, sue3, yao1]
    br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
    upsert_sheet(br00045_file_path, boat_agg_str(), br00045_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event5, event7}
    etl_boat_agg_to_pidgin_road_staging(legitimate_events, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    road_staging_str = "road_staging"
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)
    road_file_columns = [
        "src_brick",
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_road_df.columns) == road_file_columns
    assert len(gen_road_df) == 5
    b3 = "br00117"
    b4 = "br00045"
    e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_road5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_road0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_road1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

    e1_road_rows = [e1_road3, e1_road4, e1_road5, e1_road0, e1_road1]
    e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [road_staging_str]


def test_etl_boat_agg_to_pidgin_road_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    br00117_file_path = create_path(x_boat_dir, "br00117.xlsx")
    br00117_columns = [
        face_name_str(),
        event_int_str(),
        gov_idea_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(x_boat_dir, "br00045.xlsx")
    br00045_columns = [
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, boat_agg_str(), br00117_df)
    br00045_rows = [sue2, sue3, yao1]
    br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
    upsert_sheet(br00045_file_path, boat_agg_str(), br00045_df)
    pidgin_path = create_path(x_boat_dir, "pidgin.xlsx")
    legitimate_events = {event2, event5}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_boat_agg_to_pidgin_road_staging(legitimate_events, x_boat_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    road_staging_str = "road_staging"
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)
    road_file_columns = [
        "src_brick",
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_road_df.columns) == road_file_columns
    assert len(gen_road_df) == 2
    b3 = "br00117"
    b4 = "br00045"
    e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_road_rows = [e1_road3, e1_road4]
    e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [road_staging_str]
