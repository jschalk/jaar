from pandas import DataFrame
from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._util.a02_str import vow_label_str
from src.a09_pack_logic._util.a09_str import event_int_str, face_name_str
from src.a15_vow_logic._util.a15_str import cumlative_minute_str, hour_label_str
from src.a17_idea_logic.idea_db_tool import upsert_sheet
from src.a18_etl_toolbox._util.a18_env import env_dir_setup_cleanup, get_module_temp_dir
from src.a18_etl_toolbox.idea_collector import (
    IdeaFileRef,
    get_all_excel_ideasheets,
    get_all_idea_dataframes,
)


def test_get_all_excel_ideasheets_ReturnsObj_Scenario0_SheetNames(
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
    x_sheet_names = get_all_excel_ideasheets(env_dir)

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
    x_ideasheets = get_all_excel_ideasheets(env_dir)

    # THEN
    assert x_ideasheets
    assert (x_dir, ex_filename, not_br00000_str) not in x_ideasheets
    assert (x_dir, ex_filename, br00001_str) in x_ideasheets
    assert (x_dir, ex_filename, br00002_str) in x_ideasheets
    assert len(x_ideasheets) == 2


def test_IdeaFileRef_Exists():
    # ESTABLISH / WHEN
    x_ideafileref = IdeaFileRef()

    # THEN
    assert x_ideafileref.file_dir is None
    assert x_ideafileref.filename is None
    assert x_ideafileref.sheet_name is None
    assert x_ideafileref.idea_number is None


def test_IdeaFileRef_get_csv_filename_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN
    x_ideafileref = IdeaFileRef()

    # THEN
    assert x_ideafileref.get_csv_filename() == ""


def test_IdeaFileRef_get_csv_filename_ReturnsObj_Scenario1():
    # ESTABLISH
    br00003_str = "br00003"

    # WHEN
    x_ideafileref = IdeaFileRef(idea_number=br00003_str)

    # THEN
    assert x_ideafileref.get_csv_filename() == f"{br00003_str}.csv"


def test_get_all_idea_dataframes_ReturnsObj_Scenario0_PidginSheetNames(
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
    idea_columns = [
        event_int_str(),
        face_name_str(),
        cumlative_minute_str(),
        vow_label_str(),
        hour_label_str(),
    ]
    row1 = [event1, sue_str, minute_360, accord23_str, hour6am]
    row2 = [event1, sue_str, minute_420, accord23_str, hour7am]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    br00003_str = "example_br00003"
    br00003_str = "example_br00003"
    upsert_sheet(ex_file_path, br00003_str, df1)

    # WHEN
    x_ideasheets = get_all_idea_dataframes(env_dir)

    # THEN
    assert x_ideasheets
    br3_ideafileref = IdeaFileRef(x_dir, ex_filename, br00003_str, "br00003")
    assert x_ideasheets == [br3_ideafileref]
    # assert (x_dir, ex_filename, br00003_str) in x_ideasheets
    assert len(x_ideasheets) == 1


def test_get_all_idea_dataframes_ReturnsObj_Scenario1(env_dir_setup_cleanup):
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
    idea_columns = [
        event_int_str(),
        face_name_str(),
        cumlative_minute_str(),
        vow_label_str(),
        hour_label_str(),
    ]
    row1 = [event1, sue_str, minute_360, accord23_str, hour6am]
    row2 = [event1, sue_str, minute_420, accord23_str, hour7am]
    incomplete_idea_columns = [
        event_int_str(),
        face_name_str(),
        cumlative_minute_str(),
        vow_label_str(),
    ]
    incom_row1 = [event1, sue_str, minute_360, accord23_str]
    incom_row2 = [event1, sue_str, minute_420, accord23_str]

    df1 = DataFrame([row1, row2], columns=idea_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_idea_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    upsert_sheet(ex_file_path, br00003_ex1_str, df1)
    upsert_sheet(ex_file_path, br00003_ex2_str, df2)

    # WHEN
    x_ideasheets = get_all_idea_dataframes(env_dir)

    # THEN
    assert x_ideasheets
    ex1_ideafileref = IdeaFileRef(x_dir, ex_filename, br00003_ex1_str, "br00003")
    ex2_ideafileref = IdeaFileRef(x_dir, ex_filename, br00003_ex2_str, "br00003")

    assert x_ideasheets == [ex1_ideafileref]
    assert len(x_ideasheets) == 1
