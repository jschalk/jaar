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
    unknown_word_str,
    inx_label_str,
    otx_label_str,
)
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet
from src.f10_world.transformers import etl_zoo_agg_to_nub_road_staging
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_etl_zoo_agg_to_nub_road_staging_CreatesFile_Scenario0_SingleBrick(
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
    x_zoo_dir = get_test_worlds_dir()
    br00114_file_path = create_path(x_zoo_dir, "br00114.xlsx")
    br00114_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
    br00114_rows = [sue0, sue1]
    br00114_df = DataFrame(br00114_rows, columns=br00114_columns)
    upsert_sheet(br00114_file_path, "zoo_agg", br00114_df)
    pidgin_path = create_path(x_zoo_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_zoo_agg_to_nub_road_staging({event7}, x_zoo_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    nub_staging_str = "nub_staging"
    gen_nub_df = pandas_read_excel(pidgin_path, sheet_name=nub_staging_str)
    nub_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_label_str(),
        inx_label_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_nub_df.columns) == nub_file_columns
    assert len(gen_nub_df) == 2
    bx = "br00114"
    e1_nub0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_nub1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_nub_rows = [e1_nub0, e1_nub1]
    e1_nub_df = DataFrame(e1_nub_rows, columns=nub_file_columns)
    assert len(gen_nub_df) == len(e1_nub_df)
    print(f"{gen_nub_df.to_csv()=}")
    print(f" {e1_nub_df.to_csv()=}")
    assert gen_nub_df.to_csv(index=False) == e1_nub_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [nub_staging_str]


def test_etl_zoo_agg_to_nub_road_staging_CreatesFile_Scenario1_MultipleBricksFiles(
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
    x_zoo_dir = get_test_worlds_dir()
    br00114_file_path = create_path(x_zoo_dir, "br00114.xlsx")
    br00114_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00041_file_path = create_path(x_zoo_dir, "br00041.xlsx")
    br00041_columns = [
        face_id_str(),
        event_id_str(),
        otx_label_str(),
        inx_label_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    br00114_rows = [sue0, sue1]
    br00114_df = DataFrame(br00114_rows, columns=br00114_columns)
    upsert_sheet(br00114_file_path, "zoo_agg", br00114_df)
    br00041_rows = [sue2, sue3, yao1]
    br00041_df = DataFrame(br00041_rows, columns=br00041_columns)
    upsert_sheet(br00041_file_path, "zoo_agg", br00041_df)
    pidgin_path = create_path(x_zoo_dir, "pidgin.xlsx")
    assert os_path_exists(pidgin_path) is False

    # WHEN
    legitimate_events = {event1, event2, event5, event7}
    etl_zoo_agg_to_nub_road_staging(legitimate_events, x_zoo_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    nub_staging_str = "nub_staging"
    gen_nub_df = pandas_read_excel(pidgin_path, sheet_name=nub_staging_str)
    nub_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_label_str(),
        inx_label_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_nub_df.columns) == nub_file_columns
    assert len(gen_nub_df) == 5
    b3 = "br00114"
    b4 = "br00041"
    e1_nub3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_nub4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_nub5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_nub0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_nub1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

    e1_nub_rows = [e1_nub3, e1_nub4, e1_nub5, e1_nub0, e1_nub1]
    e1_nub_df = DataFrame(e1_nub_rows, columns=nub_file_columns)
    assert len(gen_nub_df) == len(e1_nub_df)
    print(f"{gen_nub_df.to_csv()=}")
    print(f" {e1_nub_df.to_csv()=}")
    assert gen_nub_df.to_csv(index=False) == e1_nub_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [nub_staging_str]


def test_etl_zoo_agg_to_nub_road_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    x_zoo_dir = get_test_worlds_dir()
    br00114_file_path = create_path(x_zoo_dir, "br00114.xlsx")
    br00114_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00041_file_path = create_path(x_zoo_dir, "br00041.xlsx")
    br00041_columns = [
        face_id_str(),
        event_id_str(),
        otx_label_str(),
        inx_label_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00114_rows = [sue0, sue1]
    br00114_df = DataFrame(br00114_rows, columns=br00114_columns)
    upsert_sheet(br00114_file_path, "zoo_agg", br00114_df)
    br00041_rows = [sue2, sue3, yao1]
    br00041_df = DataFrame(br00041_rows, columns=br00041_columns)
    upsert_sheet(br00041_file_path, "zoo_agg", br00041_df)
    pidgin_path = create_path(x_zoo_dir, "pidgin.xlsx")
    legitimate_events = {event2, event5}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    etl_zoo_agg_to_nub_road_staging(legitimate_events, x_zoo_dir)

    # THEN
    assert os_path_exists(pidgin_path)
    nub_staging_str = "nub_staging"
    gen_nub_df = pandas_read_excel(pidgin_path, sheet_name=nub_staging_str)
    nub_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_label_str(),
        inx_label_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_nub_df.columns) == nub_file_columns
    assert len(gen_nub_df) == 2
    b3 = "br00114"
    b4 = "br00041"
    e1_nub3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_nub4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_nub_rows = [e1_nub3, e1_nub4]
    e1_nub_df = DataFrame(e1_nub_rows, columns=nub_file_columns)
    assert len(gen_nub_df) == len(e1_nub_df)
    print(f"{gen_nub_df.to_csv()=}")
    print(f" {e1_nub_df.to_csv()=}")
    assert gen_nub_df.to_csv(index=False) == e1_nub_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [nub_staging_str]
