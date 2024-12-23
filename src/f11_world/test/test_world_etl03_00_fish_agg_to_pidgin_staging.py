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
    inx_idea_str,
    otx_idea_str,
    inx_road_str,
    otx_road_str,
    inx_group_id_str,
    otx_group_id_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import (
    upsert_sheet,
    sheet_exists,
    _get_pidgen_brick_format_filenames,
    fish_agg_str,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_get_pidgen_brick_format_filenames_ReturnsObj():
    # ESTABLISH / WHEN
    pidgen_brick_filenames = _get_pidgen_brick_format_filenames()

    # THEN
    print(f"need examples for {pidgen_brick_filenames=}")
    assert pidgen_brick_filenames == {
        "br00042.xlsx",
        "br00043.xlsx",
        "br00044.xlsx",
        "br00045.xlsx",
        "br00113.xlsx",
        "br00115.xlsx",
        "br00116.xlsx",
        "br00117.xlsx",
    }


def test_WorldUnit_fish_agg_to_pidgin_staging_CreatesFile(env_dir_setup_cleanup):
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
    br00113_file_path = create_path(fizz_world._fish_dir, "br00113.xlsx")
    br00113_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_acct_id_str(),
        inx_acct_id_str(),
    ]
    br00043_file_path = create_path(fizz_world._fish_dir, "br00043.xlsx")
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
    upsert_sheet(br00113_file_path, fish_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, fish_agg_str(), br00043_df)
    pidgin_path = create_path(fizz_world._fish_dir, "pidgin.xlsx")

    br00115_file_path = create_path(fizz_world._fish_dir, "br00115.xlsx")
    br00115_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_group_id_str(),
        inx_group_id_str(),
    ]
    br00042_file_path = create_path(fizz_world._fish_dir, "br00042.xlsx")
    br00042_columns = [
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
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, fish_agg_str(), br00115_df)
    b40_rows = [sue2, sue3, yao1]
    br00042_df = DataFrame(b40_rows, columns=br00042_columns)
    upsert_sheet(br00042_file_path, fish_agg_str(), br00042_df)

    br00116_file_path = create_path(fizz_world._fish_dir, "br00116.xlsx")
    br00116_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_idea_str(),
        inx_idea_str(),
    ]
    br00044_file_path = create_path(fizz_world._fish_dir, "br00044.xlsx")
    br00044_columns = [
        face_id_str(),
        event_id_str(),
        otx_idea_str(),
        inx_idea_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, fish_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, fish_agg_str(), br00044_df)

    br00117_file_path = create_path(fizz_world._fish_dir, "br00117.xlsx")
    br00117_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(fizz_world._fish_dir, "br00045.xlsx")
    br00045_columns = [
        face_id_str(),
        event_id_str(),
        otx_road_str(),
        inx_road_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, fish_agg_str(), br00117_df)
    br00045_rows = [sue2, sue3, yao1]
    br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
    upsert_sheet(br00045_file_path, fish_agg_str(), br00045_df)

    assert fizz_world.events == {}
    fizz_world.fish_agg_to_fish_events()
    fizz_world.fish_events_to_events_log()
    fizz_world.fish_events_log_to_events_agg()
    fizz_world.set_events_from_events_agg_file()
    assert fizz_world.events == {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.fish_agg_to_pidgin_staging()

    # THEN
    assert os_path_exists(pidgin_path)
    group_staging_str = "group_staging"
    acct_staging_str = "acct_staging"
    idea_staging_str = "idea_staging"
    road_staging_str = "road_staging"
    assert sheet_exists(pidgin_path, acct_staging_str)
    assert sheet_exists(pidgin_path, group_staging_str)
    assert sheet_exists(pidgin_path, idea_staging_str)
    assert sheet_exists(pidgin_path, road_staging_str)

    gen_group_df = pandas_read_excel(pidgin_path, sheet_name=group_staging_str)
    gen_acct_df = pandas_read_excel(pidgin_path, sheet_name=acct_staging_str)
    gen_idea_df = pandas_read_excel(pidgin_path, sheet_name=idea_staging_str)
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)

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
    b4 = "br00042"
    e1_group3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_group4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_group_rows = [e1_group3, e1_group4]
    e1_group_df = DataFrame(e1_group_rows, columns=group_file_columns)
    assert len(gen_group_df) == len(e1_group_df)
    print(f"{gen_group_df.to_csv()=}")
    print(f" {e1_group_df.to_csv()=}")
    assert gen_group_df.to_csv(index=False) == e1_group_df.to_csv(index=False)

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

    idea_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_idea_str(),
        inx_idea_str(),
        otx_wall_str(),
        inx_wall_str(),
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

    road_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        otx_road_str(),
        inx_road_str(),
        otx_wall_str(),
        inx_wall_str(),
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
