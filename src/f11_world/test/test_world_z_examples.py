from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import cmty_title_str, acct_name_str
from src.f09_idea.pandas_tool import upsert_sheet
from src.f10_etl.idea_collector import get_all_excel_ideasheets
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame


def test_ocean_to_boat_staging_PidginsAll(env_dir_setup_cleanup):
    # ESTABLISH
    env_dir = get_test_worlds_dir()
    x_dir = create_path(env_dir, "examples_folder")
    ex_file_name = "fizzbuzz.xlsx"
    ex_file_path = create_path(x_dir, ex_file_name)
    accord23_str = "accord23"
    sue_str = "Sue"
    event_int = 55
    df1 = DataFrame(
        [[accord23_str, sue_str]], columns=[cmty_title_str(), acct_name_str()]
    )
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
    assert (x_dir, ex_file_name, br00000_str) in x_sheet_names
    assert (x_dir, ex_file_name, br00001_str) in x_sheet_names
    assert (x_dir, ex_file_name, br00002_str) in x_sheet_names
    assert len(x_sheet_names) == 3
