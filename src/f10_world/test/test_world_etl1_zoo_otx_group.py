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
    inx_group_id_str,
    otx_group_id_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet
from src.f10_world.world import worldunit_shop
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_zoo_agg_to_group_staging_CreatesFile_Scenario0_SingleBrick(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    m_str = "music23"
    event7 = 7
    br00115_file_path = create_path(fizz_world._zoo_dir, "br00115.xlsx")
    br00115_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, bob_str, bob_inx]
    b115_rows = [sue0, sue1]
    br00115_df = DataFrame(b115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, "zoo_agg", br00115_df)
    pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
    fizz_world.zoo_agg_to_zoo_events()
    fizz_world.zoo_events_to_events_log()
    fizz_world.events_log_to_events_agg()
    fizz_world.set_events_from_events_agg()
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.zoo_agg_to_group_staging()

    # THEN
    assert os_path_exists(pidgin_path)
    group_staging_str = "group_staging"
    gen_group_df = pandas_read_excel(pidgin_path, sheet_name=group_staging_str)
    group_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_group_df.columns) == group_file_columns
    assert len(gen_group_df) == 2
    bx = "br00115"
    e1_group0 = [bx, sue_str, event7, yao_str, yao_inx, None, None, None]
    e1_group1 = [bx, sue_str, event7, bob_str, bob_inx, None, None, None]
    e1_group_rows = [e1_group0, e1_group1]
    e1_group_df = DataFrame(e1_group_rows, columns=group_file_columns)
    assert len(gen_group_df) == len(e1_group_df)
    print(f"{gen_group_df.to_csv()=}")
    print(f" {e1_group_df.to_csv()=}")
    assert gen_group_df.to_csv(index=False) == e1_group_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [group_staging_str]


def test_WorldUnit_zoo_agg_to_group_staging_CreatesFile_Scenario1_MultipleBricksFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
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
    br00115_file_path = create_path(fizz_world._zoo_dir, "br00115.xlsx")
    br00115_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
    ]
    br00043_file_path = create_path(fizz_world._zoo_dir, "br00043.xlsx")
    br00043_columns = [
        face_id_str(),
        event_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    b115_rows = [sue0, sue1]
    br00115_df = DataFrame(b115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, "zoo_agg", br00115_df)
    b40_rows = [sue2, sue3, yao1]
    br00043_df = DataFrame(b40_rows, columns=br00043_columns)
    upsert_sheet(br00043_file_path, "zoo_agg", br00043_df)
    pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
    fizz_world.zoo_agg_to_zoo_events()
    fizz_world.zoo_events_to_events_log()
    fizz_world.events_log_to_events_agg()
    fizz_world.set_events_from_events_agg()
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.zoo_agg_to_group_staging()

    # THEN
    assert os_path_exists(pidgin_path)
    group_staging_str = "group_staging"
    gen_group_df = pandas_read_excel(pidgin_path, sheet_name=group_staging_str)
    group_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_group_df.columns) == group_file_columns
    assert len(gen_group_df) == 5
    b3 = "br00115"
    b4 = "br00043"
    e1_group3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_group4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_group5 = [b4, yao_str, event7, yao_str, yao_inx, rdx, rdx, ukx]
    e1_group0 = [b3, sue_str, event1, yao_str, yao_inx, None, None, None]
    e1_group1 = [b3, sue_str, event1, bob_str, bob_inx, None, None, None]

    e1_group_rows = [e1_group3, e1_group4, e1_group5, e1_group0, e1_group1]
    e1_group_df = DataFrame(e1_group_rows, columns=group_file_columns)
    assert len(gen_group_df) == len(e1_group_df)
    print(f"{gen_group_df.to_csv()=}")
    print(f" {e1_group_df.to_csv()=}")
    assert gen_group_df.to_csv(index=False) == e1_group_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [group_staging_str]


def test_WorldUnit_zoo_agg_to_group_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
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
    br00115_file_path = create_path(fizz_world._zoo_dir, "br00115.xlsx")
    br00115_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
    ]
    br00043_file_path = create_path(fizz_world._zoo_dir, "br00043.xlsx")
    br00043_columns = [
        face_id_str(),
        event_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    b115_rows = [sue0, sue1]
    br00115_df = DataFrame(b115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, "zoo_agg", br00115_df)
    b40_rows = [sue2, sue3, yao1]
    br00043_df = DataFrame(b40_rows, columns=br00043_columns)
    upsert_sheet(br00043_file_path, "zoo_agg", br00043_df)
    pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
    assert fizz_world.events == {}
    fizz_world.zoo_agg_to_zoo_events()
    fizz_world.zoo_events_to_events_log()
    fizz_world.events_log_to_events_agg()
    fizz_world.set_events_from_events_agg()
    assert fizz_world.events == {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.zoo_agg_to_group_staging()

    # THEN
    assert os_path_exists(pidgin_path)
    group_staging_str = "group_staging"
    gen_group_df = pandas_read_excel(pidgin_path, sheet_name=group_staging_str)
    group_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    assert list(gen_group_df.columns) == group_file_columns
    assert len(gen_group_df) == 2
    b3 = "br00115"
    b4 = "br00043"
    e1_group3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_group4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_group_rows = [e1_group3, e1_group4]
    e1_group_df = DataFrame(e1_group_rows, columns=group_file_columns)
    assert len(gen_group_df) == len(e1_group_df)
    print(f"{gen_group_df.to_csv()=}")
    print(f" {e1_group_df.to_csv()=}")
    assert gen_group_df.to_csv(index=False) == e1_group_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [group_staging_str]
