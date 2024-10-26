from src.f00_instrument.file import create_file_path, create_dir
from src.f10_world.world_tool import get_all_excel_bricksheets
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, ExcelWriter


def test_get_all_excel_bricksheets_ReturnsObj_Scenario0_SheetNames():
    # ESTABLISH
    env_dir = get_test_worlds_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    df1 = DataFrame([["AAA", "BBB"]], columns=["Spam", "Egg"])
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
    x_sheetnames = get_all_excel_bricksheets(env_dir)

    # THEN
    assert x_sheetnames
    assert (x_dir, ex_file_name, br00000_str) in x_sheetnames
    assert (x_dir, ex_file_name, br00001_str) in x_sheetnames
    assert (x_dir, ex_file_name, br00002_str) in x_sheetnames
    assert len(x_sheetnames) == 3


def test_get_all_excel_sheetnames_ReturnsObj_Scenario1_FilterSheetNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    env_dir = get_test_worlds_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    df1 = DataFrame([["AAA", "BBB"]], columns=["Spam", "Egg"])
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
