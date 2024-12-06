from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import (
    cumlative_minute_str,
    hour_label_str,
    weekday_label_str,
    weekday_order_str,
)
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet
from src.f10_world.world import worldunit_shop
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_zoo_agg_to_zoo_events_CreatesSheets_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    jungle_file_path = create_path(fizz_world._jungle_dir, ex_file_name)
    zoo_file_path = create_path(fizz_world._zoo_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event1, music23_str, hour7am, minute_420]
    row3 = [yao_str, event3, music23_str, hour7am, minute_420]
    row4 = [yao_str, event9, music23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4], columns=brick_columns)
    upsert_sheet(jungle_file_path, "example1_br00003", df1)
    fizz_world.jungle_to_zoo_staging()
    fizz_world.zoo_staging_to_zoo_agg()

    # WHEN
    fizz_world.zoo_agg_to_zoo_events()

    # THEN
    gen_otx_events_df = pandas_read_excel(zoo_file_path, sheet_name="zoo_events")
    print(f"{gen_otx_events_df.columns=}")
    events_otx_columns = [face_id_str(), event_id_str(), "note"]
    sue_r = [sue_str, event1, ""]
    yao3_r = [yao_str, event3, ""]
    yao9_r = [yao_str, event9, ""]
    ex_otx_events_df = DataFrame([sue_r, yao3_r, yao9_r], columns=events_otx_columns)
    assert len(gen_otx_events_df.columns) == len(ex_otx_events_df.columns)
    assert list(gen_otx_events_df.columns) == list(ex_otx_events_df.columns)
    assert len(gen_otx_events_df) > 0
    assert len(gen_otx_events_df) == 3
    assert len(gen_otx_events_df) == len(ex_otx_events_df)
    assert gen_otx_events_df.to_csv(index=False) == ex_otx_events_df.to_csv(index=False)
    assert get_sheet_names(zoo_file_path) == ["zoo_staging", "zoo_agg", "zoo_events"]


def test_WorldUnit_zoo_agg_to_zoo_events_CreatesSheets_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    jungle_file_path = create_path(fizz_world._jungle_dir, ex_file_name)
    zoo_file_path = create_path(fizz_world._zoo_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event1, music23_str, hour7am, minute_420]
    row3 = [yao_str, event1, music23_str, hour7am, minute_420]
    row4 = [yao_str, event9, music23_str, hour7am, minute_420]
    row5 = [bob_str, event3, music23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4, row5], columns=brick_columns)
    upsert_sheet(jungle_file_path, "example1_br00003", df1)
    fizz_world.jungle_to_zoo_staging()
    fizz_world.zoo_staging_to_zoo_agg()

    # WHEN
    fizz_world.zoo_agg_to_zoo_events()

    # THEN
    gen_otx_events_df = pandas_read_excel(zoo_file_path, sheet_name="zoo_events")
    print(f"{gen_otx_events_df.columns=}")
    events_otx_columns = [face_id_str(), event_id_str(), "note"]
    bob_row = [bob_str, event3, ""]
    sue_row = [sue_str, event1, "invalid because of conflicting event_id"]
    yao1_row = [yao_str, event1, "invalid because of conflicting event_id"]
    yao9_row = [yao_str, event9, ""]
    events_rows = [bob_row, sue_row, yao1_row, yao9_row]
    ex_otx_events_df = DataFrame(events_rows, columns=events_otx_columns)
    assert len(gen_otx_events_df.columns) == len(ex_otx_events_df.columns)
    assert list(gen_otx_events_df.columns) == list(ex_otx_events_df.columns)
    assert len(gen_otx_events_df) > 0
    assert len(gen_otx_events_df) == 4
    assert len(gen_otx_events_df) == len(ex_otx_events_df)
    print(f"{gen_otx_events_df.to_csv(index=False)=}")
    print(f" {ex_otx_events_df.to_csv(index=False)=}")
    assert gen_otx_events_df.to_csv(index=False) == ex_otx_events_df.to_csv(index=False)


def test_WorldUnit_zoo_events_to_events_log_CreatesSheets_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    jungle_file_path = create_path(fizz_world._jungle_dir, ex_file_name)
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event1, music23_str, hour7am, minute_420]
    row3 = [yao_str, event1, music23_str, hour7am, minute_420]
    row4 = [yao_str, event9, music23_str, hour7am, minute_420]
    row5 = [bob_str, event3, music23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4, row5], columns=brick_columns)
    upsert_sheet(jungle_file_path, "example1_br00003", df1)
    fizz_world.jungle_to_zoo_staging()
    fizz_world.zoo_staging_to_zoo_agg()
    fizz_world.zoo_agg_to_zoo_events()
    events_file_name = "events.xlsx"
    events_file_path = create_path(fizz_world._zoo_dir, events_file_name)
    assert os_path_exists(events_file_path) is False

    # WHEN
    fizz_world.zoo_events_to_events_log()

    # THEN
    assert os_path_exists(events_file_path)
    elog = "events_log"
    gen_events_log_df = pandas_read_excel(events_file_path, sheet_name=elog)
    print(f"{gen_events_log_df.columns=}")
    events_otx_columns = [
        "file_dir",
        "file_name",
        "sheet_name",
        face_id_str(),
        event_id_str(),
        "note",
    ]
    invalid_error_str = "invalid because of conflicting event_id"
    invalid_error_str = "invalid because of conflicting event_id"
    zoo_dir = fizz_world._zoo_dir
    src_file_name = "br00003.xlsx"
    oe_str = "zoo_events"
    bob_row = [zoo_dir, src_file_name, oe_str, bob_str, event3, ""]
    sue_row = [zoo_dir, src_file_name, oe_str, sue_str, event1, invalid_error_str]
    yao1_row = [zoo_dir, src_file_name, oe_str, yao_str, event1, invalid_error_str]
    yao9_row = [zoo_dir, src_file_name, oe_str, yao_str, event9, ""]
    # el_rows = [zoo_dir, events_file_name, elog, bob_row, sue_row, yao1_row, yao9_row]
    el_rows = [bob_row, sue_row, yao1_row, yao9_row]
    ex_otx_events_df = DataFrame(el_rows, columns=events_otx_columns)
    assert len(gen_events_log_df.columns) == len(ex_otx_events_df.columns)
    assert list(gen_events_log_df.columns) == list(ex_otx_events_df.columns)
    assert len(gen_events_log_df) > 0
    assert len(gen_events_log_df) == 4
    assert len(gen_events_log_df) == len(ex_otx_events_df)
    print(f"{gen_events_log_df.to_csv(index=False)=}")
    print(f" {ex_otx_events_df.to_csv(index=False)=}")
    assert gen_events_log_df.to_csv(index=False) == ex_otx_events_df.to_csv(index=False)
    assert get_sheet_names(events_file_path) == ["events_log"]


def test_WorldUnit_zoo_events_to_events_log_CreatesSheets_Scenario1_MultipleBricks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    jungle_file_path = create_path(fizz_world._jungle_dir, ex_file_name)
    brick3_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    brick5_columns = [
        event_id_str(),
        face_id_str(),
        fiscal_id_str(),
        weekday_label_str(),
        weekday_order_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event1, music23_str, hour7am, minute_420]
    row3 = [yao_str, event1, music23_str, hour7am, minute_420]
    row4 = [yao_str, event9, music23_str, hour7am, minute_420]
    row5 = [bob_str, event3, music23_str, hour7am, minute_420]
    b3_df = DataFrame([row1, row2, row3, row4, row5], columns=brick3_columns)
    b5_0_row = [event3, bob_str, music23_str, "thu", 1]
    b5_1_row = [event9, yao_str, music23_str, "wed", 0]
    b5_df = DataFrame([b5_0_row, b5_1_row], columns=brick5_columns)
    upsert_sheet(jungle_file_path, "example1_br00003", b3_df)
    upsert_sheet(jungle_file_path, "example1_br00005", b5_df)
    fizz_world.jungle_to_zoo_staging()
    fizz_world.zoo_staging_to_zoo_agg()
    fizz_world.zoo_agg_to_zoo_events()
    events_file_name = "events.xlsx"
    events_file_path = create_path(fizz_world._zoo_dir, events_file_name)
    assert os_path_exists(events_file_path) is False

    # WHEN
    fizz_world.zoo_events_to_events_log()

    # THEN
    assert os_path_exists(events_file_path)
    elog = "events_log"
    gen_events_log_df = pandas_read_excel(events_file_path, sheet_name=elog)
    print(f"{gen_events_log_df.columns=}")
    events_otx_columns = [
        "file_dir",
        "file_name",
        "sheet_name",
        face_id_str(),
        event_id_str(),
        "note",
    ]
    invalid_error_str = "invalid because of conflicting event_id"
    invalid_error_str = "invalid because of conflicting event_id"
    zoo_dir = fizz_world._zoo_dir
    src3_file_name = "br00003.xlsx"
    src5_file_name = "br00005.xlsx"
    oe_str = "zoo_events"
    bob_row = [zoo_dir, src3_file_name, oe_str, bob_str, event3, ""]
    sue_row = [zoo_dir, src3_file_name, oe_str, sue_str, event1, invalid_error_str]
    yao1_row = [zoo_dir, src3_file_name, oe_str, yao_str, event1, invalid_error_str]
    yao9_row = [zoo_dir, src3_file_name, oe_str, yao_str, event9, ""]
    s5_0_row = [zoo_dir, src5_file_name, oe_str, bob_str, event3, ""]
    s5_1_row = [zoo_dir, src5_file_name, oe_str, yao_str, event9, ""]
    # el_rows = [zoo_dir, events_file_name, elog, bob_row, sue_row, yao1_row, yao9_row]
    el_rows = [bob_row, sue_row, yao1_row, yao9_row, s5_0_row, s5_1_row]
    ex_events_log_df = DataFrame(el_rows, columns=events_otx_columns)
    assert len(gen_events_log_df.columns) == len(ex_events_log_df.columns)
    assert list(gen_events_log_df.columns) == list(ex_events_log_df.columns)
    assert len(gen_events_log_df) > 0
    assert len(gen_events_log_df) == 6
    assert len(gen_events_log_df) == len(ex_events_log_df)
    print(f"{gen_events_log_df.to_csv(index=False)=}")
    print(f" {ex_events_log_df.to_csv(index=False)=}")
    assert gen_events_log_df.to_csv(index=False) == ex_events_log_df.to_csv(index=False)
    assert get_sheet_names(events_file_path) == ["events_log"]


def test_WorldUnit_events_log_to_events_agg_CreatesSheets_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    events_otx_columns = [
        "file_dir",
        "file_name",
        "sheet_name",
        face_id_str(),
        event_id_str(),
        "note",
    ]
    invalid_error_str = "invalid because of conflicting event_id"
    invalid_error_str = "invalid because of conflicting event_id"
    zoo_dir = fizz_world._zoo_dir
    src3_file_name = "br00003.xlsx"
    src5_file_name = "br00005.xlsx"
    oe_str = "zoo_events"
    bob_row = [zoo_dir, src3_file_name, oe_str, bob_str, event3, ""]
    sue_row = [zoo_dir, src3_file_name, oe_str, sue_str, event1, invalid_error_str]
    yao1_row = [zoo_dir, src3_file_name, oe_str, yao_str, event1, invalid_error_str]
    yao9_row = [zoo_dir, src3_file_name, oe_str, yao_str, event9, ""]
    s5_0_row = [zoo_dir, src5_file_name, oe_str, bob_str, event3, ""]
    s5_1_row = [zoo_dir, src5_file_name, oe_str, yao_str, event9, ""]
    # el_rows = [zoo_dir, events_file_name, elog, bob_row, sue_row, yao1_row, yao9_row]
    el_rows = [bob_row, sue_row, yao1_row, yao9_row, s5_0_row, s5_1_row]
    ex_events_log_df = DataFrame(el_rows, columns=events_otx_columns)
    events_file_path = create_path(zoo_dir, "events.xlsx")
    events_log_str = "events_log"
    upsert_sheet(events_file_path, events_log_str, ex_events_log_df)

    # WHEN
    fizz_world.events_log_to_events_agg()

    # THEN
    e3_row = [bob_str, event3, ""]
    e1_sue_row = [sue_str, event1, invalid_error_str]
    e1_yao_row = [yao_str, event1, invalid_error_str]
    e9_row = [yao_str, event9, ""]
    el_rows = [e1_sue_row, e1_yao_row, e3_row, e9_row]
    events_agg_columns = [face_id_str(), event_id_str(), "note"]
    ex_events_agg_df = DataFrame(el_rows, columns=events_agg_columns)
    e_agg = "events_agg"
    gen_events_agg_df = pandas_read_excel(events_file_path, sheet_name=e_agg)
    assert len(gen_events_agg_df.columns) == len(ex_events_agg_df.columns)
    assert list(gen_events_agg_df.columns) == list(ex_events_agg_df.columns)
    assert len(gen_events_agg_df) > 0
    assert len(gen_events_agg_df) == 4
    assert len(gen_events_agg_df) == len(ex_events_agg_df)
    print(f"{gen_events_agg_df.to_csv(index=False)=}")
    print(f" {ex_events_agg_df.to_csv(index=False)=}")
    assert gen_events_agg_df.to_csv(index=False) == ex_events_agg_df.to_csv(index=False)
    assert get_sheet_names(events_file_path) == ["events_log", "events_agg"]


def test_WorldUnit_set_events_from_events_agg_file_SetsAttr_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    invalid_error_str = "invalid because of conflicting event_id"
    invalid_error_str = "invalid because of conflicting event_id"
    zoo_dir = fizz_world._zoo_dir
    e3_row = [bob_str, event3, ""]
    e1_sue_row = [sue_str, event1, invalid_error_str]
    e1_yao_row = [yao_str, event1, invalid_error_str]
    e9_row = [yao_str, event9, ""]
    el_rows = [e1_sue_row, e1_yao_row, e3_row, e9_row]
    events_agg_columns = [face_id_str(), event_id_str(), "note"]
    ex_events_agg_df = DataFrame(el_rows, columns=events_agg_columns)
    events_agg_str = "events_agg"
    events_file_path = create_path(zoo_dir, "events.xlsx")
    upsert_sheet(events_file_path, events_agg_str, ex_events_agg_df)
    assert len(fizz_world.events) != 2

    # WHEN
    fizz_world.set_events_from_events_agg_file()

    # THEN
    assert len(fizz_world.events) == 2
    assert fizz_world.events == {event3: bob_str, event9: yao_str}


def test_WorldUnit_set_events_from_events_agg_file_ClearsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    events_agg_columns = [face_id_str(), event_id_str(), "note"]
    ex_events_agg_df = DataFrame([], columns=events_agg_columns)
    events_agg_str = "events_agg"
    events_file_path = create_path(fizz_world._zoo_dir, "events.xlsx")
    upsert_sheet(events_file_path, events_agg_str, ex_events_agg_df)
    fizz_world.events = {2: "Sue", 44: "Bob"}
    assert fizz_world.events == {2: "Sue", 44: "Bob"}

    # WHEN
    fizz_world.set_events_from_events_agg_file()

    # THEN
    assert not fizz_world.events
