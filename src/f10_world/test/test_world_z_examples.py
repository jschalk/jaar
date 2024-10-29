from src.f00_instrument.file import create_file_path, create_dir
from src.f04_gift.atom_config import fiscal_id_str, acct_id_str
from src.f10_world.world_tool import get_all_excel_bricksheets
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, ExcelWriter


def test_jungle_to_zoo_FiltersAll(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_test_worlds_dir()
    x_dir = create_file_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_file_path(x_dir, ex_file_name)
    music_str = "music23"
    sue_str = "Sue"
    time_wid = 55
    df1 = DataFrame([[music_str, sue_str]], columns=[fiscal_id_str(), acct_id_str()])
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
