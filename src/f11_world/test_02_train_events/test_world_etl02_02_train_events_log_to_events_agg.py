from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_name_str, event_int_str
from src.f09_idea.idea_db_tool import get_sheet_names, upsert_sheet
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_train_events_log_to_events_agg_CreatesSheets_Scenario0(
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
        "filename",
        "sheet_name",
        face_name_str(),
        event_int_str(),
        "error_message",
    ]
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
    train_dir = fizz_world._train_dir
    src3_filename = "br00003.xlsx"
    src5_filename = "br00005.xlsx"
    oe_str = "train_events"
    bob_row = [train_dir, src3_filename, oe_str, bob_str, event3, ""]
    sue_row = [train_dir, src3_filename, oe_str, sue_str, event1, invalid_error_str]
    yao1_row = [train_dir, src3_filename, oe_str, yao_str, event1, invalid_error_str]
    yao9_row = [train_dir, src3_filename, oe_str, yao_str, event9, ""]
    s5_0_row = [train_dir, src5_filename, oe_str, bob_str, event3, ""]
    s5_1_row = [train_dir, src5_filename, oe_str, yao_str, event9, ""]
    # el_rows = [train_dir, events_filename, elog, bob_row, sue_row, yao1_row, yao9_row]
    el_rows = [bob_row, sue_row, yao1_row, yao9_row, s5_0_row, s5_1_row]
    ex_events_log_df = DataFrame(el_rows, columns=events_otx_columns)
    events_file_path = create_path(train_dir, "events.xlsx")
    events_log_str = "events_log"
    upsert_sheet(events_file_path, events_log_str, ex_events_log_df)

    # WHEN
    fizz_world.train_events_log_to_events_agg()

    # THEN
    e3_row = [bob_str, event3, ""]
    e1_sue_row = [sue_str, event1, invalid_error_str]
    e1_yao_row = [yao_str, event1, invalid_error_str]
    e9_row = [yao_str, event9, ""]
    el_rows = [e1_sue_row, e1_yao_row, e3_row, e9_row]
    events_agg_columns = [face_name_str(), event_int_str(), "error_message"]
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
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
    train_dir = fizz_world._train_dir
    e3_row = [bob_str, event3, ""]
    e1_sue_row = [sue_str, event1, invalid_error_str]
    e1_yao_row = [yao_str, event1, invalid_error_str]
    e9_row = [yao_str, event9, ""]
    el_rows = [e1_sue_row, e1_yao_row, e3_row, e9_row]
    events_agg_columns = [face_name_str(), event_int_str(), "error_message"]
    ex_events_agg_df = DataFrame(el_rows, columns=events_agg_columns)
    events_agg_str = "events_agg"
    events_file_path = create_path(train_dir, "events.xlsx")
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
    events_agg_columns = [face_name_str(), event_int_str(), "error_message"]
    ex_events_agg_df = DataFrame([], columns=events_agg_columns)
    events_agg_str = "events_agg"
    events_file_path = create_path(fizz_world._train_dir, "events.xlsx")
    upsert_sheet(events_file_path, events_agg_str, ex_events_agg_df)
    fizz_world.events = {2: "Sue", 44: "Bob"}
    assert fizz_world.events == {2: "Sue", 44: "Bob"}

    # WHEN
    fizz_world.set_events_from_events_agg_file()

    # THEN
    assert not fizz_world.events
