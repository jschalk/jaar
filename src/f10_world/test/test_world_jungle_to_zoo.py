from src.f00_instrument.file import create_path, create_dir
from src.f04_gift.atom_config import (
    face_id_str,
    fiscal_id_str,
    jaar_type_str,
    acct_id_str,
    owner_id_str,
)
from src.f07_fiscal.fiscal_config import (
    cumlative_minute_str,
    hour_label_str,
    weekday_label_str,
    weekday_order_str,
)
from src.f08_pidgin.pidgin_config import (
    event_id_str,
    inx_road_delimiter_str,
    otx_road_delimiter_str,
    inx_word_str,
    otx_word_str,
    unknown_word_str,
    inx_label_str,
    otx_label_str,
)
from src.f09_brick.pandas_tool import (
    _get_pidgen_brick_format_filenames,
    get_sheet_names,
)
from src.f10_world.world import worldunit_shop, _create_events_agg_df
from src.f10_world.world_tool import get_all_brick_dataframes
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, ExcelWriter, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_jungle_to_zoo_staging_CreatesZooFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    event_1 = 1
    event_2 = 2
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
        cumlative_minute_str(),
        fiscal_id_str(),
        hour_label_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event_1, minute_360, music23_str, hour6am]
    row2 = [sue_str, event_1, minute_420, music23_str, hour7am]
    row3 = [sue_str, event_2, minute_420, music23_str, hour7am]
    incomplete_brick_columns = [
        face_id_str(),
        event_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
    ]
    incom_row1 = [sue_str, event_1, minute_360, music23_str]
    incom_row2 = [sue_str, event_1, minute_420, music23_str]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_brick_columns)
    df3 = DataFrame([row2, row1, row3], columns=brick_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name=br00003_ex1_str, index=False)
        df2.to_excel(writer, sheet_name=br00003_ex2_str, index=False)
        df3.to_excel(writer, sheet_name=br00003_ex3_str, index=False)
    assert os_path_exists(zoo_file_path) is False

    # WHEN
    fizz_world.jungle_to_zoo_staging()

    # THEN
    print(f"{zoo_file_path=}")
    assert os_path_exists(zoo_file_path)
    x_df = pandas_read_excel(zoo_file_path, sheet_name="zoo_staging")
    assert set(brick_columns).issubset(set(x_df.columns))
    file_dir_str = "file_dir"
    file_name_str = "file_name"
    sheet_name_str = "sheet_name"
    assert file_dir_str in set(x_df.columns)
    assert file_name_str in set(x_df.columns)
    assert sheet_name_str in set(x_df.columns)
    assert len(x_df) == 5
    assert get_sheet_names(zoo_file_path) == ["zoo_staging"]


def test_WorldUnit_zoo_staging_to_zoo_agg_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    event_1 = 1
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
    row1 = [sue_str, event_1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event_1, music23_str, hour7am, minute_420]
    row3 = [sue_str, event_1, music23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3], columns=brick_columns)
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name="example1_br00003")
    fizz_world.jungle_to_zoo_staging()
    zoo__staging_df = pandas_read_excel(zoo_file_path, sheet_name="zoo_staging")
    assert len(zoo__staging_df) == 3

    # WHEN
    fizz_world.zoo_staging_to_zoo_agg()

    # THEN
    gen_otx_df = pandas_read_excel(zoo_file_path, sheet_name="zoo_agg")
    ex_otx_df = DataFrame([row1, row2], columns=brick_columns)
    print(f"{gen_otx_df.columns=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 2
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(zoo_file_path) == ["zoo_staging", "zoo_agg"]


def test_WorldUnit_zoo_staging_to_zoo_agg_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    sue_str = "Sue"
    event_1 = 1
    minute_360 = 360
    minute_420 = 420
    minute_480 = 480
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
    row1 = [sue_str, event_1, music23_str, hour6am, minute_360]
    row2 = [sue_str, event_1, music23_str, hour7am, minute_420]
    row3 = [sue_str, event_1, music23_str, hour7am, minute_480]
    df1 = DataFrame([row1, row2, row3], columns=brick_columns)
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name="example1_br00003")
    fizz_world.jungle_to_zoo_staging()
    zoo_df = pandas_read_excel(zoo_file_path, sheet_name="zoo_staging")
    assert len(zoo_df) == 3

    # WHEN
    fizz_world.zoo_staging_to_zoo_agg()

    # THEN
    gen_otx_df = pandas_read_excel(zoo_file_path, sheet_name="zoo_agg")
    ex_otx_df = DataFrame([row1], columns=brick_columns)
    # print(f"{gen_otx_df.columns=}")
    print(f"{gen_otx_df=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 1
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()
    assert get_sheet_names(zoo_file_path) == ["zoo_staging", "zoo_agg"]


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
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name="example1_br00003")
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
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name="example1_br00003")
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
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name="example1_br00003")
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
    with ExcelWriter(jungle_file_path) as writer:
        b3_df.to_excel(writer, sheet_name="example1_br00003")
        b5_df.to_excel(writer, sheet_name="example2_br00005")
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


def test_WorldUnit_create_events_agg_df_ReturnsObj(
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

    # WHEN
    gen_events_agg_df = _create_events_agg_df(ex_events_log_df)

    # THEN
    e3_row = [bob_str, event3, ""]
    e1_sue_row = [sue_str, event1, invalid_error_str]
    e1_yao_row = [yao_str, event1, invalid_error_str]
    e9_row = [yao_str, event9, ""]
    el_rows = [e1_sue_row, e1_yao_row, e3_row, e9_row]
    events_agg_columns = [face_id_str(), event_id_str(), "note"]
    ex_events_agg_df = DataFrame(el_rows, columns=events_agg_columns)
    assert len(gen_events_agg_df.columns) == len(ex_events_agg_df.columns)
    assert list(gen_events_agg_df.columns) == list(ex_events_agg_df.columns)
    assert len(gen_events_agg_df) > 0
    assert len(gen_events_agg_df) == 4
    assert len(gen_events_agg_df) == len(ex_events_agg_df)
    print(f"{gen_events_agg_df.to_csv(index=False)=}")
    print(f" {ex_events_agg_df.to_csv(index=False)=}")
    assert gen_events_agg_df.to_csv(index=False) == ex_events_agg_df.to_csv(index=False)


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
    with ExcelWriter(events_file_path) as writer:
        ex_events_log_df.to_excel(writer, sheet_name=events_log_str, index=False)

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


def test_WorldUnit_set_events_from_events_agg_SetsAttr_Scenario0(env_dir_setup_cleanup):
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
    with ExcelWriter(events_file_path) as writer:
        ex_events_agg_df.to_excel(writer, sheet_name=events_agg_str, index=False)
    assert len(fizz_world.events) != 2

    # WHEN
    fizz_world.set_events_from_events_agg()

    # THEN
    assert len(fizz_world.events) == 2
    assert fizz_world.events == {event3: bob_str, event9: yao_str}


def test_WorldUnit_set_events_from_events_agg_ClearsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    events_agg_columns = [face_id_str(), event_id_str(), "note"]
    ex_events_agg_df = DataFrame([], columns=events_agg_columns)
    events_agg_str = "events_agg"
    events_file_path = create_path(fizz_world._zoo_dir, "events.xlsx")
    with ExcelWriter(events_file_path) as writer:
        ex_events_agg_df.to_excel(writer, sheet_name=events_agg_str, index=False)
    fizz_world.events = {2: "Sue", 44: "Bob"}
    assert fizz_world.events == {2: "Sue", 44: "Bob"}

    # WHEN
    fizz_world.set_events_from_events_agg()

    # THEN
    assert not fizz_world.events


def test_get_pidgen_brick_format_filenames_ReturnsObj():
    # ESTABLISH / WHEN
    pidgen_brick_filenames = _get_pidgen_brick_format_filenames()

    # THEN
    print(f"need examples for {pidgen_brick_filenames=}")
    assert pidgen_brick_filenames == {"br00040.xlsx", "br00041.xlsx", "br00113.xlsx"}


def test_WorldUnit_zoo_agg_to_otxinx_staging_CreatesFile_Scenario0_SingleBrick(
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
    acctid_str = "AcctID"
    br00113_file_path = create_path(fizz_world._zoo_dir, "br00113.xlsx")
    br00113_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        jaar_type_str(),
        otx_word_str(),
        inx_word_str(),
    ]
    sue0 = [sue_str, event7, m_str, bob_str, yao_str, acctid_str, yao_str, yao_inx]
    sue1 = [sue_str, event7, m_str, bob_str, bob_str, acctid_str, bob_str, bob_inx]
    b113_rows = [sue0, sue1]
    br00113_df = DataFrame(b113_rows, columns=br00113_columns)
    with ExcelWriter(br00113_file_path) as writer:
        br00113_df.to_excel(writer, sheet_name="zoo_agg", index=False)
    pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
    fizz_world.zoo_agg_to_zoo_events()
    fizz_world.zoo_events_to_events_log()
    fizz_world.events_log_to_events_agg()
    fizz_world.set_events_from_events_agg()
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.zoo_agg_to_otxinx_staging()

    # THEN
    assert os_path_exists(pidgin_path)
    otxinx_staging_str = "otx2inx_staging"
    gen_otx2inx_df = pandas_read_excel(pidgin_path, sheet_name=otxinx_staging_str)
    otx2inx_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        jaar_type_str(),
        otx_word_str(),
        inx_word_str(),
        otx_road_delimiter_str(),
        inx_road_delimiter_str(),
        unknown_word_str(),
    ]
    assert list(gen_otx2inx_df.columns) == otx2inx_file_columns
    assert len(gen_otx2inx_df) == 2
    bx = "br00113"
    e1_otx2inx0 = [bx, sue_str, event7, acctid_str, yao_str, yao_inx, None, None, None]
    e1_otx2inx1 = [bx, sue_str, event7, acctid_str, bob_str, bob_inx, None, None, None]
    e1_otx2inx_rows = [e1_otx2inx0, e1_otx2inx1]
    e1_otx2inx_df = DataFrame(e1_otx2inx_rows, columns=otx2inx_file_columns)
    assert len(gen_otx2inx_df) == len(e1_otx2inx_df)
    print(f"{gen_otx2inx_df.to_csv()=}")
    print(f" {e1_otx2inx_df.to_csv()=}")
    assert gen_otx2inx_df.to_csv(index=False) == e1_otx2inx_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [otxinx_staging_str]


def test_WorldUnit_zoo_agg_to_otxinx_staging_CreatesFile_Scenario1_MultipleBricksFiles(
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
    acctid_str = "AcctID"
    br00113_file_path = create_path(fizz_world._zoo_dir, "br00113.xlsx")
    br00113_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        jaar_type_str(),
        otx_word_str(),
        inx_word_str(),
    ]
    br00040_file_path = create_path(fizz_world._zoo_dir, "br00040.xlsx")
    br00040_columns = [
        face_id_str(),
        event_id_str(),
        jaar_type_str(),
        otx_word_str(),
        inx_word_str(),
        otx_road_delimiter_str(),
        inx_road_delimiter_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, acctid_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, acctid_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, acctid_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, acctid_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event7, acctid_str, yao_str, yao_inx, rdx, rdx, ukx]
    b113_rows = [sue0, sue1]
    br00113_df = DataFrame(b113_rows, columns=br00113_columns)
    with ExcelWriter(br00113_file_path) as writer:
        br00113_df.to_excel(writer, sheet_name="zoo_agg", index=False)
    b40_rows = [sue2, sue3, yao1]
    br00040_df = DataFrame(b40_rows, columns=br00040_columns)
    with ExcelWriter(br00040_file_path) as writer:
        br00040_df.to_excel(writer, sheet_name="zoo_agg", index=False)
    pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
    fizz_world.zoo_agg_to_zoo_events()
    fizz_world.zoo_events_to_events_log()
    fizz_world.events_log_to_events_agg()
    fizz_world.set_events_from_events_agg()
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.zoo_agg_to_otxinx_staging()

    # THEN
    assert os_path_exists(pidgin_path)
    otxinx_staging_str = "otx2inx_staging"
    gen_otx2inx_df = pandas_read_excel(pidgin_path, sheet_name=otxinx_staging_str)
    otx2inx_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        jaar_type_str(),
        otx_word_str(),
        inx_word_str(),
        otx_road_delimiter_str(),
        inx_road_delimiter_str(),
        unknown_word_str(),
    ]
    assert list(gen_otx2inx_df.columns) == otx2inx_file_columns
    assert len(gen_otx2inx_df) == 5
    b3 = "br00113"
    b4 = "br00040"
    e1_otx2inx3 = [b4, sue_str, event2, acctid_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_otx2inx4 = [b4, sue_str, event5, acctid_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_otx2inx5 = [b4, yao_str, event7, acctid_str, yao_str, yao_inx, rdx, rdx, ukx]
    e1_otx2inx0 = [b3, sue_str, event1, acctid_str, yao_str, yao_inx, None, None, None]
    e1_otx2inx1 = [b3, sue_str, event1, acctid_str, bob_str, bob_inx, None, None, None]

    e1_otx2inx_rows = [e1_otx2inx3, e1_otx2inx4, e1_otx2inx5, e1_otx2inx0, e1_otx2inx1]
    e1_otx2inx_df = DataFrame(e1_otx2inx_rows, columns=otx2inx_file_columns)
    assert len(gen_otx2inx_df) == len(e1_otx2inx_df)
    print(f"{gen_otx2inx_df.to_csv()=}")
    print(f" {e1_otx2inx_df.to_csv()=}")
    assert gen_otx2inx_df.to_csv(index=False) == e1_otx2inx_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [otxinx_staging_str]


def test_WorldUnit_zoo_agg_to_otxinx_staging_CreatesFile_Scenario2_WorldUnit_events_Filters(
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
    acctid_str = "AcctID"
    br00113_file_path = create_path(fizz_world._zoo_dir, "br00113.xlsx")
    br00113_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        jaar_type_str(),
        otx_word_str(),
        inx_word_str(),
    ]
    br00040_file_path = create_path(fizz_world._zoo_dir, "br00040.xlsx")
    br00040_columns = [
        face_id_str(),
        event_id_str(),
        jaar_type_str(),
        otx_word_str(),
        inx_word_str(),
        otx_road_delimiter_str(),
        inx_road_delimiter_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, acctid_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, acctid_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, acctid_str, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, acctid_str, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, acctid_str, yao_str, yao_inx, rdx, rdx, ukx]
    b113_rows = [sue0, sue1]
    br00113_df = DataFrame(b113_rows, columns=br00113_columns)
    with ExcelWriter(br00113_file_path) as writer:
        br00113_df.to_excel(writer, sheet_name="zoo_agg", index=False)
    b40_rows = [sue2, sue3, yao1]
    br00040_df = DataFrame(b40_rows, columns=br00040_columns)
    with ExcelWriter(br00040_file_path) as writer:
        br00040_df.to_excel(writer, sheet_name="zoo_agg", index=False)
    pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
    assert fizz_world.events == {}
    fizz_world.zoo_agg_to_zoo_events()
    fizz_world.zoo_events_to_events_log()
    fizz_world.events_log_to_events_agg()
    fizz_world.set_events_from_events_agg()
    assert fizz_world.events == {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.zoo_agg_to_otxinx_staging()

    # THEN
    assert os_path_exists(pidgin_path)
    otxinx_staging_str = "otx2inx_staging"
    gen_otx2inx_df = pandas_read_excel(pidgin_path, sheet_name=otxinx_staging_str)
    otx2inx_file_columns = [
        "src_brick",
        face_id_str(),
        event_id_str(),
        jaar_type_str(),
        otx_word_str(),
        inx_word_str(),
        otx_road_delimiter_str(),
        inx_road_delimiter_str(),
        unknown_word_str(),
    ]
    assert list(gen_otx2inx_df.columns) == otx2inx_file_columns
    assert len(gen_otx2inx_df) == 2
    b3 = "br00113"
    b4 = "br00040"
    e1_otx2inx3 = [b4, sue_str, event2, acctid_str, sue_str, sue_str, rdx, rdx, ukx]
    e1_otx2inx4 = [b4, sue_str, event5, acctid_str, bob_str, bob_inx, rdx, rdx, ukx]
    e1_otx2inx_rows = [e1_otx2inx3, e1_otx2inx4]
    e1_otx2inx_df = DataFrame(e1_otx2inx_rows, columns=otx2inx_file_columns)
    assert len(gen_otx2inx_df) == len(e1_otx2inx_df)
    print(f"{gen_otx2inx_df.to_csv()=}")
    print(f" {e1_otx2inx_df.to_csv()=}")
    assert gen_otx2inx_df.to_csv(index=False) == e1_otx2inx_df.to_csv(index=False)
    assert get_sheet_names(pidgin_path) == [otxinx_staging_str]


# def test_WorldUnit_zoo_agg_to_otxinx_staging_CreatesFile(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     yao_inx = "Yaoito"
#     bob_inx = "Bobito"
#     m_str = "music23"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     acctid_str = "AcctID"
#     br00113_file_path = create_path(fizz_world._zoo_dir, "br00113.xlsx")
#     br00113_columns = [
#         face_id_str(),
#         event_id_str(),
#         fiscal_id_str(),
#         owner_id_str(),
#         acct_id_str(),
#         jaar_type_str(),
#         otx_word_str(),
#         inx_word_str(),
#     ]
#     sue0 = [sue_str, event1, m_str, bob_str, yao_str, acctid_str, yao_str, yao_inx]
#     sue1 = [sue_str, event1, m_str, bob_str, bob_str, acctid_str, bob_str, bob_inx]
#     # sue2 = [sue_str, event2, m_str, sue_str, yao_str, acctid_str, yao_str]
#     # sue3 = [sue_str, event5, m_str, bob_str, yao_str, acctid_str, yao_str]
#     # yao1 = [yao_str, event7, m_str, bob_str, yao_str, acctid_str, yao_str]
#     b113_rows = [sue0, sue1]
#     br00113_df = DataFrame(b113_rows, columns=br00113_columns)
#     with ExcelWriter(br00113_file_path) as writer:
#         br00113_df.to_excel(writer, sheet_name="zoo_agg", index=False)
#     pidgin_path = create_path(fizz_world._zoo_dir, "pidgin.xlsx")
#     assert fizz_world.events == {}
#     fizz_world.zoo_agg_to_zoo_events()
#     fizz_world.zoo_events_to_events_log()
#     fizz_world.events_log_to_events_agg()
#     fizz_world.set_events_from_events_agg()
#     assert fizz_world.events == {event1: sue_str}
#     assert os_path_exists(pidgin_path) is False

#     # WHEN
#     fizz_world.zoo_agg_to_otxinx_staging()

#     # THEN
#     assert os_path_exists(pidgin_path)
#     assert 1 == 2
#     otxinx_sheet_name = "otx2inx"
#     gen_otx2inx_df = pandas_read_excel(pidgin_path, sheet_name=otxinx_sheet_name)
#     pidgin_file_columns = {
#         "event_id",
#         "face_id",
#         "jaar_type",
#         "otx_word",
#         "otx_road_delimiter",
#         "inx_word",
#         "inx_road_delimiter",
#         "unknown_word",
#     }
#     assert set(gen_otx2inx_df.columns) == pidgin_file_columns
#     assert len(gen_otx2inx_df) == 2
#     e1_otx2inx0 = [event1, sue_str, acctid_str, yao_str, None, yao_inx, None, None]
#     e1_otx2inx1 = [event1, sue_str, acctid_str, bob_str, None, bob_inx, None, None]
#     e1_otx2inx_rows = [e1_otx2inx0, e1_otx2inx1]
#     e1_otx2inx_df = DataFrame(e1_otx2inx_rows, columns=pidgin_file_columns)
#     assert len(gen_otx2inx_df) == len(e1_otx2inx_df)
#     assert gen_otx2inx_df.to_csv() == e1_otx2inx_df.to_csv()
#     assert get_sheet_names(pidgin_path) == ["otxinx_staging"]
#     assert 1 == 2


# def test_WorldUnit_otx_to_faces_event_CreatesPidgenSheets_Scenario0(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     sue_str = "Sue"
#     yao_str = "Yao"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     event8 = 8
#     event9 = 9
#     hr6am = "6am"
#     hr7am = "7am"
#     vetday = "veterns day"
#     armday = "armistice day"
#     slash_str = "/"
#     colon_str = ":"
#     x_uk = "unknownSue"
#     roadnode_str = "RoadNode"
#     groupid_str = "GroupID"
#     br00040_file_path = create_path(fizz_world._zoo_dir, br00040_xlsx_file)
#     br00041_file_path = create_path(fizz_world._zoo_dir, br00041_xlsx_file)
#     br00040_columns = [
#         face_id_str(),
#         event_id_str(),
#         inx_road_delimiter_str(),
#         inx_word_str(),
#         jaar_type_str(),
#         otx_road_delimiter_str(),
#         otx_word_str(),
#         unknown_word_str(),
#     ]
#     br00041_columns = [
#         face_id_str(),
#         event_id_str(),
#         inx_label_str(),
#         inx_road_delimiter_str(),
#         jaar_type_str(),
#         otx_label_str(),
#         otx_road_delimiter_str(),
#         unknown_word_str(),
#     ]
#     sue_oi0 = [sue_str, event1, slash_str, hr6am, groupid_str, colon_str, hr6am, x_uk]
#     sue_oi1 = [sue_str, event1, slash_str, hr6am, roadnode_str, colon_str, hr6am, x_uk]
#     sue_oi2 = [sue_str, event2, slash_str, hr7am, roadnode_str, colon_str, hr7am, x_uk]
#     sue_oi3 = [sue_str, event5, slash_str, hr7am, roadnode_str, colon_str, hr7am, x_uk]
#     yao_1 = [yao_str, event7, slash_str, hr7am, roadnode_str, colon_str, hr7am, x_uk]
#     sue_el = [sue_str, event8, armday, slash_str, roadnode_str, vetday, colon_str, x_uk]
#     yao_el = [yao_str, event9, vetday, slash_str, roadnode_str, vetday, colon_str, x_uk]
#     b40_rows = [sue_oi0, sue_oi1, sue_oi2, sue_oi3, yao_1]
#     br00040_df = DataFrame(b40_rows, columns=br00040_columns)
#     br00041_df = DataFrame([yao_el, sue_el], columns=br00041_columns)
#     with ExcelWriter(br00040_file_path) as writer:
#         br00040_df.to_excel(writer, sheet_name="zoo_agg", index=False)
#     with ExcelWriter(br00041_file_path) as writer:
#         br00041_df.to_excel(writer, sheet_name="zoo_agg", index=False)
#     sue_face_dir = create_path(fizz_world._events_dir, f"/{sue_str}")
#     yao_face_dir = create_path(fizz_world._events_dir, f"/{yao_str}")
#     sue_road_to_inx_path = create_path(sue_face_dir, "road_otx2inx_csv")
#     sue_road_nub_path = create_path(sue_face_dir, "road_nub_label.csv")
#     yao_road_to_inx_path = create_path(yao_face_dir, "road_otx2inx_csv")
#     yao_road_nub_path = create_path(yao_face_dir, "road_nub_label.csv")
#     assert os_path_exists(sue_face_dir) is False
#     assert os_path_exists(yao_face_dir) is False
#     assert os_path_exists(sue_road_to_inx_path) is False
#     assert os_path_exists(sue_road_nub_path) is False
#     assert os_path_exists(yao_road_to_inx_path) is False
#     assert os_path_exists(yao_road_nub_path) is False

#     # WHEN
#     fizz_world.otx_to_faces_event()

#     # THEN
#     assert os_path_exists(sue_face_dir)
#     assert os_path_exists(yao_face_dir)
#     assert os_path_exists(sue_road_to_inx_path)
#     assert os_path_exists(sue_road_nub_path)
#     assert os_path_exists(yao_road_to_inx_path)
#     assert os_path_exists(yao_road_nub_path)
#     # gen_sue_otx2inx_df = open_csv(sue_otx2inx_path)
#     # gen_sue_otx_nub_df = open_csv(sue_otx_nub_path)
#     # gen_yao_otx2inx_df = open_csv(yao_otx2inx_path)
#     # gen_yao_otx_nub_df = open_csv(yao_otx_nub_path)

#     otx2inx_columns = [
#         face_id_str(),
#         jaar_type_str(),
#         otx_road_delimiter_str(),
#         inx_road_delimiter_str(),
#         unknown_word_str(),
#         otx_word_str(),
#         inx_word_str(),
#     ]
#     nub_label_columns = [
#         face_id_str(),
#         jaar_type_str(),
#         otx_road_delimiter_str(),
#         inx_road_delimiter_str(),
#         unknown_word_str(),
#         otx_label_str(),
#         inx_label_str(),
#     ]
#     sue_oi1 = [sue_str, event_1, hr6am, slash_str, roadnode_str, hr6am, colon_str, x_uk]
#     sue_oi2 = [sue_str, event_1, hr7am, slash_str, roadnode_str, hr7am, colon_str, x_uk]
#     sue_oi3 = [sue_str, event_1, hr7am, slash_str, roadnode_str, hr7am, colon_str, x_uk]
#     yao_el1 = [yao_str, event_1, hr7am, slash_str, roadnode_str, hr7am, colon_str, x_uk]
#     sue_el1 = [
#         sue_str,
#         event_1,
#         armday,
#         slash_str,
#         roadnode_str,
#         vetday,
#         colon_str,
#         x_uk,
#     ]
#     ex1_sue_otx2inx_df = DataFrame([sue_oi1, sue_oi2, sue_oi3], otx2inx_columns)
#     ex1_sue_otx_nub_df = DataFrame([sue_el1], nub_label_columns)
#     ex1_yao_otx2inx_df = DataFrame([], otx2inx_columns)
#     ex1_yao_otx_nub_df = DataFrame([yao_el1], nub_label_columns)

#     # print(f"{gen_otx_df.columns=}")
#     # assert list(gen_sue_otx2inx_df.columns) == otx2inx_columns
#     # assert list(gen_sue_otx_nub_df.columns) == nub_label_columns
#     # assert len(gen_yao_otx2inx_df) > 0
#     # assert len(gen_yao_otx2inx_df) == len(gen_sue_otx_nub_df)
#     # assert len(gen_sue_otx_nub_df) == 1
#     # assert gen_sue_otx_nub_df.to_csv() == gen_sue_otx_nub_df.to_csv()

#     assert ex1_sue_otx2inx_df == open_csv(sue_otx2inx_path)
#     assert ex1_sue_otx_nub_df == open_csv(sue_otx_nub_path)
#     assert ex1_yao_otx2inx_df == open_csv(yao_otx2inx_path)
#     assert ex1_yao_otx_nub_df == open_csv(yao_otx_nub_path)

#     assert 1 == 2
