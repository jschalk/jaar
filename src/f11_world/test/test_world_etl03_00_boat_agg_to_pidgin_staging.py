from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    face_name_str,
    cmty_title_str,
    acct_name_str,
    owner_name_str,
)
from src.f08_pidgin.pidgin_config import (
    event_int_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_title_str,
    otx_title_str,
    inx_road_str,
    otx_road_str,
    inx_label_str,
    otx_label_str,
    unknown_word_str,
)
from src.f09_brick.pandas_tool import (
    upsert_sheet,
    sheet_exists,
    _get_pidgen_brick_format_filenames,
    boat_agg_str,
)
from src.f10_etl.pidgin_agg import PidginPrimeColumns
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


def test_WorldUnit_boat_agg_to_pidgin_staging_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
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
    br00113_file_path = create_path(fizz_world._boat_dir, "br00113.xlsx")
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        cmty_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    br00043_file_path = create_path(fizz_world._boat_dir, "br00043.xlsx")
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
    upsert_sheet(br00113_file_path, boat_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, boat_agg_str(), br00043_df)
    pidgin_path = create_path(fizz_world._boat_dir, "pidgin.xlsx")

    br00115_file_path = create_path(fizz_world._boat_dir, "br00115.xlsx")
    br00115_columns = [
        face_name_str(),
        event_int_str(),
        cmty_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00042_file_path = create_path(fizz_world._boat_dir, "br00042.xlsx")
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

    br00116_file_path = create_path(fizz_world._boat_dir, "br00116.xlsx")
    br00116_columns = [
        face_name_str(),
        event_int_str(),
        cmty_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_title_str(),
        inx_title_str(),
    ]
    br00044_file_path = create_path(fizz_world._boat_dir, "br00044.xlsx")
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
    upsert_sheet(br00116_file_path, boat_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, boat_agg_str(), br00044_df)

    br00117_file_path = create_path(fizz_world._boat_dir, "br00117.xlsx")
    br00117_columns = [
        face_name_str(),
        event_int_str(),
        cmty_title_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(fizz_world._boat_dir, "br00045.xlsx")
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

    assert fizz_world.events == {}
    fizz_world.boat_agg_to_boat_events()
    fizz_world.boat_events_to_events_log()
    fizz_world.boat_events_log_to_events_agg()
    fizz_world.set_events_from_events_agg_file()
    assert fizz_world.events == {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.boat_agg_to_pidgin_staging()

    # THEN
    assert os_path_exists(pidgin_path)
    label_staging_str = "label_staging"
    name_staging_str = "name_staging"
    title_staging_str = "title_staging"
    road_staging_str = "road_staging"
    assert sheet_exists(pidgin_path, name_staging_str)
    assert sheet_exists(pidgin_path, label_staging_str)
    assert sheet_exists(pidgin_path, title_staging_str)
    assert sheet_exists(pidgin_path, road_staging_str)

    gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_staging_str)
    gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_staging_str)
    gen_title_df = pandas_read_excel(pidgin_path, sheet_name=title_staging_str)
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_staging_str)

    label_file_columns = PidginPrimeColumns().map_label_staging_columns
    assert list(gen_label_df.columns) == label_file_columns
    assert len(gen_label_df) == 2
    b3 = "br00115"
    b4 = "br00042"
    e1_label3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_label4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_label_rows = [e1_label3, e1_label4]
    e1_label_df = DataFrame(e1_label_rows, columns=label_file_columns)
    assert len(gen_label_df) == len(e1_label_df)
    print(f"{gen_label_df.to_csv()=}")
    print(f" {e1_label_df.to_csv()=}")
    assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)

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

    title_file_columns = [
        "src_brick",
        face_name_str(),
        event_int_str(),
        otx_title_str(),
        inx_title_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_title_df.columns) == title_file_columns
    assert len(gen_title_df) == 2
    b3 = "br00116"
    b4 = "br00044"
    e1_title3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_title4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_title_rows = [e1_title3, e1_title4]
    e1_title_df = DataFrame(e1_title_rows, columns=title_file_columns)
    assert len(gen_title_df) == len(e1_title_df)
    print(f"{gen_title_df.to_csv()=}")
    print(f" {e1_title_df.to_csv()=}")
    assert gen_title_df.to_csv(index=False) == e1_title_df.to_csv(index=False)

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
