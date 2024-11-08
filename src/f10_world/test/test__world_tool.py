from src.f00_instrument.file import create_file_path, create_dir
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_filter.filter_config import eon_id_str
from src.f10_world.world_tool import (
    get_all_excel_bricksheets,
    get_all_brick_dataframes,
    BrickFileRef,
)
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, ExcelWriter


def test_get_all_excel_bricksheets_ReturnsObj_Scenario0_SheetNames():
    # ESTABLISH
    env_dir = get_test_worlds_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    br00000_str = "br00000"
    br00001_str = "br00001"
    br00002_str = "br00002"
    create_dir(x_dir)
    with ExcelWriter(ex_file_path) as writer:
        df1.to_excel(writer, sheet_name=br00000_str)
        df2.to_excel(writer, sheet_name=br00001_str)
        df2.to_excel(writer, sheet_name=br00002_str)

    # WHEN
    x_sheet_names = get_all_excel_bricksheets(env_dir)

    # THEN
    assert x_sheet_names
    assert (x_dir, ex_file_name, br00000_str) in x_sheet_names
    assert (x_dir, ex_file_name, br00001_str) in x_sheet_names
    assert (x_dir, ex_file_name, br00002_str) in x_sheet_names
    assert len(x_sheet_names) == 3


def test_get_all_excel_sheet_names_ReturnsObj_Scenario1_FilterSheetNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_test_worlds_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    df1 = DataFrame([["AAA", "BBB"]], columns=["spam", "egg"])
    df2 = DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
    not_br00000_str = "b00000"
    br00001_str = "example_br00001"
    br00002_str = "example_br00002_example"
    create_dir(x_dir)
    with ExcelWriter(ex_file_path) as writer:
        df1.to_excel(writer, sheet_name=not_br00000_str)
        df2.to_excel(writer, sheet_name=br00001_str)
        df2.to_excel(writer, sheet_name=br00002_str)

    # WHEN
    x_bricksheets = get_all_excel_bricksheets(env_dir)

    # THEN
    assert x_bricksheets
    assert (x_dir, ex_file_name, not_br00000_str) not in x_bricksheets
    assert (x_dir, ex_file_name, br00001_str) in x_bricksheets
    assert (x_dir, ex_file_name, br00002_str) in x_bricksheets
    assert len(x_bricksheets) == 2


def test_BrickFileRef_Exists():
    # ESTABLISH / WHEN
    x_brickfileref = BrickFileRef()

    # THEN
    assert x_brickfileref.file_dir is None
    assert x_brickfileref.file_name is None
    assert x_brickfileref.sheet_name is None
    assert x_brickfileref.brick_number is None


def test_get_all_brick_dataframes_ReturnsObj_Scenario0_FilterSheetNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_test_worlds_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    sue_str = "Sue"
    eon_1 = 1
    minute_360 = 360
    minute_420 = 420
    music23_str = "music23"
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    brick_columns = [
        face_id_str(),
        eon_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
        hour_label_str(),
    ]
    row1 = [sue_str, eon_1, minute_360, music23_str, hour6am]
    row2 = [sue_str, eon_1, minute_420, music23_str, hour7am]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    br00003_str = "example_br00003"
    br00003_str = "example_br00003"
    create_dir(x_dir)
    with ExcelWriter(ex_file_path) as writer:
        df1.to_excel(writer, sheet_name=br00003_str, index=False)

    # WHEN
    x_bricksheets = get_all_brick_dataframes(env_dir)

    # THEN
    assert x_bricksheets
    br3_brickfileref = BrickFileRef(x_dir, ex_file_name, br00003_str, "br00003")
    assert x_bricksheets == [br3_brickfileref]
    # assert (x_dir, ex_file_name, br00003_str) in x_bricksheets
    assert len(x_bricksheets) == 1


def test_get_all_brick_dataframes_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_test_worlds_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    sue_str = "Sue"
    eon_1 = 1
    minute_360 = 360
    minute_420 = 420
    music23_str = "music23"
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    brick_columns = [
        face_id_str(),
        eon_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
        hour_label_str(),
    ]
    row1 = [sue_str, eon_1, minute_360, music23_str, hour6am]
    row2 = [sue_str, eon_1, minute_420, music23_str, hour7am]
    incomplete_brick_columns = [
        face_id_str(),
        eon_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
    ]
    incom_row1 = [sue_str, eon_1, minute_360, music23_str]
    incom_row2 = [sue_str, eon_1, minute_420, music23_str]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_brick_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    create_dir(x_dir)
    with ExcelWriter(ex_file_path) as writer:
        df1.to_excel(writer, sheet_name=br00003_ex1_str, index=False)
        df2.to_excel(writer, sheet_name=br00003_ex2_str, index=False)

    # WHEN
    x_bricksheets = get_all_brick_dataframes(env_dir)

    # THEN
    assert x_bricksheets
    ex1_brickfileref = BrickFileRef(x_dir, ex_file_name, br00003_ex1_str, "br00003")
    ex2_brickfileref = BrickFileRef(x_dir, ex_file_name, br00003_ex2_str, "br00003")

    assert x_bricksheets == [ex1_brickfileref]
    assert len(x_bricksheets) == 1
