from src.a00_data_toolboxs.file_toolbox import create_path, get_level1_dirs
from src.a01_word_logic.road import OwnerName
from src.f06_listen.hub_tool import open_bud_file
from src.f08_fisc.fisc import (
    get_from_default_path as fiscunit_get_from_default_path,
)
from src.f10_idea.idea_csv_tool import (
    create_init_stance_idea_brick_csv_strs,
    add_fiscunit_to_stance_csv_strs,
    add_budunit_to_stance_csv_strs,
    add_pidginunit_to_stance_csv_strs,
)
from src.f10_idea.idea_db_tool import csv_dict_to_excel
from src.f11_etl.tran_path import create_stances_dir_path, STANCE0001_FILENAME
from os.path import exists as os_path_exists


def collect_stance_csv_strs(fisc_mstr_dir: str) -> dict[str, str]:
    x_csv_strs = create_init_stance_idea_brick_csv_strs()
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        x_fiscunit = fiscunit_get_from_default_path(fisc_mstr_dir, fisc_title)
        add_fiscunit_to_stance_csv_strs(x_fiscunit, x_csv_strs, ",")
        fisc_dir = create_path(fiscs_dir, fisc_title)
        owners_dir = create_path(fisc_dir, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            owner_dir = create_path(owners_dir, owner_name)
            gut_dir = create_path(owner_dir, "gut")
            gut_bud_path = create_path(gut_dir, f"{owner_name}.json")
            if os_path_exists(gut_bud_path):
                gut_bud = open_bud_file(gut_bud_path)
                add_budunit_to_stance_csv_strs(gut_bud, x_csv_strs, ",")
    return x_csv_strs


def create_stance0001_file(fisc_mstr_dir: str):
    stance_csv_strs = collect_stance_csv_strs(fisc_mstr_dir)
    stance_dir = create_stances_dir_path(fisc_mstr_dir)
    csv_dict_to_excel(stance_csv_strs, stance_dir, STANCE0001_FILENAME)
