from src.a00_data_toolboxs.file_toolbox import create_path
from src.a02_finance_toolboxs.deal import fisc_tag_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import (
    cumlative_minute_str,
    hour_tag_str,
    weekday_tag_str,
    weekday_order_str,
)
from src.a17_idea_logic.idea_db_tool import get_sheet_names, upsert_sheet
from src.a18_etl_toolbox.tran_path import create_cochlea_events_path
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic.examples.world_env import (
    get_test_worlds_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_cochlea_events_to_events_log_CreatesSheets_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
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
    ex_filename = "fizzbuzz.xlsx"
    sound_file_path = create_path(fizz_world._sound_dir, ex_filename)
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        hour_tag_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event1, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event1, accord23_str, hour7am, minute_420]
    row3 = [yao_str, event1, accord23_str, hour7am, minute_420]
    row4 = [yao_str, event9, accord23_str, hour7am, minute_420]
    row5 = [bob_str, event3, accord23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3, row4, row5], columns=idea_columns)
    upsert_sheet(sound_file_path, "example1_br00003", df1)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        fizz_world.sound_df_to_cochlea_raw_df(db_conn)
        fizz_world.cochlea_raw_df_to_cochlea_agg_df(db_conn, cursor)
    fizz_world.cochlea_agg_to_cochlea_events()
    events_file_path = create_cochlea_events_path(fizz_world._cochlea_dir)
    assert os_path_exists(events_file_path) is False

    # WHEN
    fizz_world.cochlea_events_to_events_log()

    # THEN
    assert os_path_exists(events_file_path)
    elog = "events_log"
    gen_events_log_df = pandas_read_excel(events_file_path, sheet_name=elog)
    print(f"{gen_events_log_df.columns=}")
    events_otx_columns = [
        "file_dir",
        "filename",
        "sheet_name",
        face_name_str(),
        event_int_str(),
        "error_message",
    ]
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
    cochlea_dir = fizz_world._cochlea_dir
    src_filename = "br00003.xlsx"
    oe_str = "cochlea_events"
    bob_row = [cochlea_dir, src_filename, oe_str, bob_str, event3, ""]
    sue_row = [cochlea_dir, src_filename, oe_str, sue_str, event1, invalid_error_str]
    yao1_row = [cochlea_dir, src_filename, oe_str, yao_str, event1, invalid_error_str]
    yao9_row = [cochlea_dir, src_filename, oe_str, yao_str, event9, ""]
    # el_rows = [cochlea_dir, events_filename, elog, bob_row, sue_row, yao1_row, yao9_row]
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


def test_WorldUnit_cochlea_events_to_events_log_CreatesSheets_Scenario1_MultipleIdeas(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
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
    ex_filename = "fizzbuzz.xlsx"
    sound_file_path = create_path(fizz_world._sound_dir, ex_filename)
    idea3_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        hour_tag_str(),
        cumlative_minute_str(),
    ]
    idea5_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        weekday_tag_str(),
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
    upsert_sheet(sound_file_path, "example1_br00003", b3_df)
    upsert_sheet(sound_file_path, "example1_br00005", b5_df)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        fizz_world.sound_df_to_cochlea_raw_df(db_conn)
        fizz_world.cochlea_raw_df_to_cochlea_agg_df(db_conn, cursor)
    fizz_world.cochlea_agg_to_cochlea_events()
    events_file_path = create_cochlea_events_path(fizz_world._cochlea_dir)
    assert os_path_exists(events_file_path) is False

    # WHEN
    fizz_world.cochlea_events_to_events_log()

    # THEN
    assert os_path_exists(events_file_path)
    elog = "events_log"
    gen_events_log_df = pandas_read_excel(events_file_path, sheet_name=elog)
    print(f"{gen_events_log_df.columns=}")
    events_otx_columns = [
        "file_dir",
        "filename",
        "sheet_name",
        face_name_str(),
        event_int_str(),
        "error_message",
    ]
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
    cochlea_dir = fizz_world._cochlea_dir
    src3_filename = "br00003.xlsx"
    src5_filename = "br00005.xlsx"
    oe_str = "cochlea_events"
    bob_row = [cochlea_dir, src3_filename, oe_str, bob_str, event3, ""]
    sue_row = [cochlea_dir, src3_filename, oe_str, sue_str, event1, invalid_error_str]
    yao1_row = [cochlea_dir, src3_filename, oe_str, yao_str, event1, invalid_error_str]
    yao9_row = [cochlea_dir, src3_filename, oe_str, yao_str, event9, ""]
    s5_0_row = [cochlea_dir, src5_filename, oe_str, bob_str, event3, ""]
    s5_1_row = [cochlea_dir, src5_filename, oe_str, yao_str, event9, ""]
    # el_rows = [cochlea_dir, events_filename, elog, bob_row, sue_row, yao1_row, yao9_row]
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
