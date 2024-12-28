from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_brick.pandas_tool import get_sheet_names, upsert_sheet
from src.f10_etl.transformers import (
    _create_events_agg_df,
    etl_boat_events_log_to_events_agg,
    get_events_dict_from_events_agg_file,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel


def test_create_events_agg_df_ReturnsObj(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    boat_dir = "fizzyz"
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
        event_int_str(),
        "note",
    ]
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
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

    # WHEN
    gen_events_agg_df = _create_events_agg_df(ex_events_log_df)

    # THEN
    e3_row = [bob_str, event3, ""]
    e1_sue_row = [sue_str, event1, invalid_error_str]
    e1_yao_row = [yao_str, event1, invalid_error_str]
    e9_row = [yao_str, event9, ""]
    el_rows = [e1_sue_row, e1_yao_row, e3_row, e9_row]
    events_agg_columns = [face_id_str(), event_int_str(), "note"]
    ex_events_agg_df = DataFrame(el_rows, columns=events_agg_columns)
    assert len(gen_events_agg_df.columns) == len(ex_events_agg_df.columns)
    assert list(gen_events_agg_df.columns) == list(ex_events_agg_df.columns)
    assert len(gen_events_agg_df) > 0
    assert len(gen_events_agg_df) == 4
    assert len(gen_events_agg_df) == len(ex_events_agg_df)
    print(f"{gen_events_agg_df.to_csv(index=False)=}")
    print(f" {ex_events_agg_df.to_csv(index=False)=}")
    assert gen_events_agg_df.to_csv(index=False) == ex_events_agg_df.to_csv(index=False)


def test_WorldUnit_boat_events_log_to_events_agg_CreatesSheets_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
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
        event_int_str(),
        "note",
    ]
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
    boat_dir = get_test_etl_dir()
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
    events_file_path = create_path(boat_dir, "events.xlsx")
    events_log_str = "events_log"
    upsert_sheet(events_file_path, events_log_str, ex_events_log_df)

    # WHEN
    etl_boat_events_log_to_events_agg(boat_dir)

    # THEN
    e3_row = [bob_str, event3, ""]
    e1_sue_row = [sue_str, event1, invalid_error_str]
    e1_yao_row = [yao_str, event1, invalid_error_str]
    e9_row = [yao_str, event9, ""]
    el_rows = [e1_sue_row, e1_yao_row, e3_row, e9_row]
    events_agg_columns = [face_id_str(), event_int_str(), "note"]
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
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    event1 = 1
    event3 = 3
    event9 = 9
    invalid_error_str = "invalid because of conflicting event_int"
    invalid_error_str = "invalid because of conflicting event_int"
    boat_dir = get_test_etl_dir()
    e3_row = [bob_str, event3, ""]
    e1_sue_row = [sue_str, event1, invalid_error_str]
    e1_yao_row = [yao_str, event1, invalid_error_str]
    e9_row = [yao_str, event9, ""]
    el_rows = [e1_sue_row, e1_yao_row, e3_row, e9_row]
    events_agg_columns = [face_id_str(), event_int_str(), "note"]
    ex_events_agg_df = DataFrame(el_rows, columns=events_agg_columns)
    events_agg_str = "events_agg"
    events_file_path = create_path(boat_dir, "events.xlsx")
    upsert_sheet(events_file_path, events_agg_str, ex_events_agg_df)

    # WHEN
    events_dict = get_events_dict_from_events_agg_file(boat_dir)

    # THEN
    assert len(events_dict) == 2
    assert events_dict == {event3: bob_str, event9: yao_str}
