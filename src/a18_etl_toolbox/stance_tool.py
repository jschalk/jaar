from os.path import exists as os_path_exists
from src.a00_data_toolbox.csv_toolbox import (
    delete_column_from_csv_string,
    replace_csv_column_from_string,
)
from src.a00_data_toolbox.file_toolbox import create_path, get_level1_dirs
from src.a12_hub_toolbox.hub_tool import open_plan_file
from src.a15_belief_logic.belief import get_default_path_beliefunit
from src.a17_idea_logic.idea_csv_tool import (
    add_beliefunit_to_stance_csv_strs,
    add_planunit_to_stance_csv_strs,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import csv_dict_to_excel, prettify_excel
from src.a18_etl_toolbox.tran_path import STANCE0001_FILENAME, create_stance0001_path


def collect_stance_csv_strs(belief_mstr_dir: str) -> dict[str, str]:
    x_csv_strs = create_init_stance_idea_csv_strs()
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    for belief_label in get_level1_dirs(beliefs_dir):
        x_beliefunit = get_default_path_beliefunit(belief_mstr_dir, belief_label)
        add_beliefunit_to_stance_csv_strs(x_beliefunit, x_csv_strs, ",")
        belief_dir = create_path(beliefs_dir, belief_label)
        owners_dir = create_path(belief_dir, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            owner_dir = create_path(owners_dir, owner_name)
            gut_dir = create_path(owner_dir, "gut")
            gut_plan_path = create_path(gut_dir, f"{owner_name}.json")
            if os_path_exists(gut_plan_path):
                gut_plan = open_plan_file(gut_plan_path)
                add_planunit_to_stance_csv_strs(gut_plan, x_csv_strs, ",")
    return x_csv_strs


def create_stance0001_file(
    belief_mstr_dir: str,
    output_dir: str,
    world_name: str,
    prettify_excel_bool: bool = True,
):
    stance_csv_strs = collect_stance_csv_strs(belief_mstr_dir)
    with_face_name_csvs = {}
    for csv_key, csv_str in stance_csv_strs.items():
        csv_str = replace_csv_column_from_string(csv_str, "face_name", world_name)
        csv_str = delete_column_from_csv_string(csv_str, "event_int")
        with_face_name_csvs[csv_key] = csv_str
    csv_dict_to_excel(with_face_name_csvs, output_dir, STANCE0001_FILENAME)

    # Hard to test function to prettify the excel file
    if prettify_excel_bool:
        stance0001_path = create_stance0001_path(output_dir)
        prettify_excel(stance0001_path)
