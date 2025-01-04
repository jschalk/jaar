from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_name_str, cmty_title_str
from src.f07_cmty.cmty_config import (
    cumlative_minute_str,
    hour_title_str,
    weekday_title_str,
    weekday_order_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.pandas_tool import get_sheet_names, upsert_sheet
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_boat_events_to_events_log_CreatesSheets_Scenario0(
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
    ocean_file_path = create_path(fizz_world._ocean_dir, ex_file_name)
    idea_columns = [
        face_name_str(),
        event_int_str(),
        cmty_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event1, accord23_str, hour7am, minute_420]
    row3 = [yao_str, event1, accord23_str, hour7am, minute_420]
    row4 = [yao_str, event9, accord23_str, hour7am, minute_420]
    row5 = [bob_str, event3, accord23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4, row5], columns=idea_columns)
    upsert_sheet(ocean_file_path, "example1_br00003", df1)
    fizz_world.ocean_to_boat_staging()
    fizz_world.boat_staging_to_boat_agg()
    fizz_world.boat_agg_to_boat_events()
    events_file_name = "events.xlsx"
    events_file_path = create_path(fizz_world._boat_dir, events_file_name)
    assert os_path_exists(events_file_path) is False

    # WHEN
    fizz_world.boat_events_to_events_log()

    # THEN
    assert os_path_exists(events_file_path)
    elog = "events_log"
    gen_events_log_df = pandas_read_excel(events_file_path, sheet_name=elog)
    print(f"{gen_events_log_df.columns=}")
    events_otx_columns = [
        "file_dir",
        "file_name",
        "sheet_name",
        face_name_str(),
        event_int_str(),
        "note",
    ]
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
    boat_dir = fizz_world._boat_dir
    src_file_name = "br00003.xlsx"
    oe_str = "boat_events"
    bob_row = [boat_dir, src_file_name, oe_str, bob_str, event3, ""]
    sue_row = [boat_dir, src_file_name, oe_str, sue_str, event1, invalid_error_str]
    yao1_row = [boat_dir, src_file_name, oe_str, yao_str, event1, invalid_error_str]
    yao9_row = [boat_dir, src_file_name, oe_str, yao_str, event9, ""]
    # el_rows = [boat_dir, events_file_name, elog, bob_row, sue_row, yao1_row, yao9_row]
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


def test_WorldUnit_boat_events_to_events_log_CreatesSheets_Scenario1_MultipleIdeas(
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
    ocean_file_path = create_path(fizz_world._ocean_dir, ex_file_name)
    idea3_columns = [
        face_name_str(),
        event_int_str(),
        cmty_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    idea5_columns = [
        event_int_str(),
        face_name_str(),
        cmty_title_str(),
        weekday_title_str(),
        weekday_order_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event1, accord23_str, hour7am, minute_420]
    row3 = [yao_str, event1, accord23_str, hour7am, minute_420]
    row4 = [yao_str, event9, accord23_str, hour7am, minute_420]
    row5 = [bob_str, event3, accord23_str, hour7am, minute_420]
    b3_df = DataFrame([row1, row2, row3, row4, row5], columns=idea3_columns)
    b5_0_row = [event3, bob_str, accord23_str, "thu", 1]
    b5_1_row = [event9, yao_str, accord23_str, "wed", 0]
    b5_df = DataFrame([b5_0_row, b5_1_row], columns=idea5_columns)
    upsert_sheet(ocean_file_path, "example1_br00003", b3_df)
    upsert_sheet(ocean_file_path, "example1_br00005", b5_df)
    fizz_world.ocean_to_boat_staging()
    fizz_world.boat_staging_to_boat_agg()
    fizz_world.boat_agg_to_boat_events()
    events_file_name = "events.xlsx"
    events_file_path = create_path(fizz_world._boat_dir, events_file_name)
    assert os_path_exists(events_file_path) is False

    # WHEN
    fizz_world.boat_events_to_events_log()

    # THEN
    assert os_path_exists(events_file_path)
    elog = "events_log"
    gen_events_log_df = pandas_read_excel(events_file_path, sheet_name=elog)
    print(f"{gen_events_log_df.columns=}")
    events_otx_columns = [
        "file_dir",
        "file_name",
        "sheet_name",
        face_name_str(),
        event_int_str(),
        "note",
    ]
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
    boat_dir = fizz_world._boat_dir
    src3_file_name = "br00003.xlsx"
    src5_file_name = "br00005.xlsx"
    oe_str = "boat_events"
    bob_row = [boat_dir, src3_file_name, oe_str, bob_str, event3, ""]
    sue_row = [boat_dir, src3_file_name, oe_str, sue_str, event1, invalid_error_str]
    yao1_row = [boat_dir, src3_file_name, oe_str, yao_str, event1, invalid_error_str]
    yao9_row = [boat_dir, src3_file_name, oe_str, yao_str, event9, ""]
    s5_0_row = [boat_dir, src5_file_name, oe_str, bob_str, event3, ""]
    s5_1_row = [boat_dir, src5_file_name, oe_str, yao_str, event9, ""]
    # el_rows = [boat_dir, events_file_name, elog, bob_row, sue_row, yao1_row, yao9_row]
    el_rows = [bob_row, sue_row, yao1_row, yao9_row, s5_0_row, s5_1_row]
    ex_events_log_df = DataFrame(el_rows, columns=events_otx_columns)
    assert len(gen_events_log_df.columns) == len(ex_events_log_df.columns)
    assert list(gen_events_log_df.columns) == list(ex_events_log_df.columns)
    print(f"{gen_events_log_df=}\n")
    print(f" {ex_events_log_df=}\n\n")
    print(f"{gen_events_log_df.to_csv(index=False)=}")
    print(f" {ex_events_log_df.to_csv(index=False)=}")
    assert len(gen_events_log_df) > 0
    assert len(gen_events_log_df) == 6
    assert len(gen_events_log_df) == len(ex_events_log_df)
    print(f"{gen_events_log_df.to_csv(index=False)=}")
    print(f" {ex_events_log_df.to_csv(index=False)=}")
    assert gen_events_log_df.to_csv(index=False) == ex_events_log_df.to_csv(index=False)
    assert get_sheet_names(events_file_path) == ["events_log"]
