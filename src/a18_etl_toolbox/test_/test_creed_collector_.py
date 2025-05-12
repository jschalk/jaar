from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_tag_str
from src.a17_creed_logic.creed_db_tool import upsert_sheet
from src.a18_etl_toolbox.creed_collector import (
    get_all_excel_creedsheets,
    get_all_creed_dataframes,
    CreedFileRef,
)
from src.a18_etl_toolbox._utils.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame


def test_get_all_excel_creedsheets_ReturnsObj_Scenario0_SheetNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x_dir = create_path(env_dir, "examples_folder")
    ex_filename = "fizzbuzz.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    br00000_str = "br00000"
    br00001_str = "br00001"
    br00002_str = "br00002"
    upsert_sheet(ex_file_path, br00000_str, df1)
    upsert_sheet(ex_file_path, br00001_str, df2)
    upsert_sheet(ex_file_path, br00002_str, df2)

    # WHEN
    x_sheet_names = get_all_excel_creedsheets(env_dir)

    # THEN
    assert x_sheet_names
    assert (x_dir, ex_filename, br00000_str) in x_sheet_names
    assert (x_dir, ex_filename, br00001_str) in x_sheet_names
    assert (x_dir, ex_filename, br00002_str) in x_sheet_names
    assert len(x_sheet_names) == 3


def test_get_all_excel_sheet_names_ReturnsObj_Scenario1_PidginSheetNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x_dir = create_path(env_dir, "examples_folder")
    ex_filename = "fizzbuzz.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    not_br00000_str = "b00000"
    br00001_str = "example_br00001"
    br00002_str = "example_br00002_example"
    upsert_sheet(ex_file_path, not_br00000_str, df1)
    upsert_sheet(ex_file_path, br00001_str, df2)
    upsert_sheet(ex_file_path, br00002_str, df2)

    # WHEN
    x_creedsheets = get_all_excel_creedsheets(env_dir)

    # THEN
    assert x_creedsheets
    assert (x_dir, ex_filename, not_br00000_str) not in x_creedsheets
    assert (x_dir, ex_filename, br00001_str) in x_creedsheets
    assert (x_dir, ex_filename, br00002_str) in x_creedsheets
    assert len(x_creedsheets) == 2


def test_CreedFileRef_Exists():
    # ESTABLISH / WHEN
    x_creedfileref = CreedFileRef()

    # THEN
    assert x_creedfileref.file_dir is None
    assert x_creedfileref.filename is None
    assert x_creedfileref.sheet_name is None
    assert x_creedfileref.creed_number is None


def test_CreedFileRef_get_csv_filename_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN
    x_creedfileref = CreedFileRef()

    # THEN
    assert x_creedfileref.get_csv_filename() == ""


def test_CreedFileRef_get_csv_filename_ReturnsObj_Scenario1():
    # ESTABLISH
    br00003_str = "br00003"

    # WHEN
    x_creedfileref = CreedFileRef(creed_number=br00003_str)

    # THEN
    assert x_creedfileref.get_csv_filename() == f"{br00003_str}.csv"


def test_get_all_creed_dataframes_ReturnsObj_Scenario0_PidginSheetNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x_dir = create_path(env_dir, "examples_folder")
    sue_str = "Sue"
    event1 = 1
    minute_360 = 360
    minute_420 = 420
    accord23_str = "accord23"
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    creed_columns = [
        event_int_str(),
        face_name_str(),
        cumlative_minute_str(),
        fisc_tag_str(),
        hour_tag_str(),
    ]
    row1 = [event1, sue_str, minute_360, accord23_str, hour6am]
    row2 = [event1, sue_str, minute_420, accord23_str, hour7am]

    df1 = DataFrame([row1, row2], columns=creed_columns)
    br00003_str = "example_br00003"
    br00003_str = "example_br00003"
    upsert_sheet(ex_file_path, br00003_str, df1)

    # WHEN
    x_creedsheets = get_all_creed_dataframes(env_dir)

    # THEN
    assert x_creedsheets
    br3_creedfileref = CreedFileRef(x_dir, ex_filename, br00003_str, "br00003")
    assert x_creedsheets == [br3_creedfileref]
    # assert (x_dir, ex_filename, br00003_str) in x_creedsheets
    assert len(x_creedsheets) == 1


def test_get_all_creed_dataframes_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_module_temp_dir()
    x_dir = create_path(env_dir, "examples_folder")
    sue_str = "Sue"
    event1 = 1
    minute_360 = 360
    minute_420 = 420
    accord23_str = "accord23"
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    ex_file_path = create_path(x_dir, ex_filename)
    creed_columns = [
        event_int_str(),
        face_name_str(),
        cumlative_minute_str(),
        fisc_tag_str(),
        hour_tag_str(),
    ]
    row1 = [event1, sue_str, minute_360, accord23_str, hour6am]
    row2 = [event1, sue_str, minute_420, accord23_str, hour7am]
    incomplete_creed_columns = [
        event_int_str(),
        face_name_str(),
        cumlative_minute_str(),
        fisc_tag_str(),
    ]
    incom_row1 = [event1, sue_str, minute_360, accord23_str]
    incom_row2 = [event1, sue_str, minute_420, accord23_str]

    df1 = DataFrame([row1, row2], columns=creed_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_creed_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    upsert_sheet(ex_file_path, br00003_ex1_str, df1)
    upsert_sheet(ex_file_path, br00003_ex2_str, df2)

    # WHEN
    x_creedsheets = get_all_creed_dataframes(env_dir)

    # THEN
    assert x_creedsheets
    ex1_creedfileref = CreedFileRef(x_dir, ex_filename, br00003_ex1_str, "br00003")
    ex2_creedfileref = CreedFileRef(x_dir, ex_filename, br00003_ex2_str, "br00003")

    assert x_creedsheets == [ex1_creedfileref]
    assert len(x_creedsheets) == 1
