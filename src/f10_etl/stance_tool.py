from src.f00_instrument.file import create_path, get_level1_dirs
from src.f01_road.road import OwnerName
from src.f05_listen.hub_path import create_stances_owner_dir_path, STANCE0001_FILENAME
from src.f05_listen.hub_tool import open_bud_file
from src.f07_fisc.fisc import (
    get_from_standard as fiscunit_get_from_standard,
)
from src.f09_idea.idea_csv_tool import (
    create_init_stance_idea_brick_csv_strs,
    add_fiscunit_to_stance_csv_strs,
    add_budunit_to_stance_csv_strs,
    add_pidginunit_to_stance_csv_strs,
)
from src.f09_idea.idea_db_tool import csv_dict_to_excel
from os.path import exists as os_path_exists


def collect_stance_csv_strs(
    fisc_mstr_dir: str, owner_name: OwnerName
) -> dict[str, str]:
    x_csv_strs = create_init_stance_idea_brick_csv_strs()
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        x_fiscunit = fiscunit_get_from_standard(fisc_mstr_dir, fisc_title)
        add_fiscunit_to_stance_csv_strs(x_fiscunit, x_csv_strs, ",")
        fisc_dir = create_path(fiscs_dir, fisc_title)
        owners_dir = create_path(fisc_dir, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            owner_dir = create_path(owners_dir, owner_name)
            voice_dir = create_path(owner_dir, "voice")
            voice_bud_path = create_path(voice_dir, f"{owner_name}.json")
            if os_path_exists(voice_bud_path):
                voice_bud = open_bud_file(voice_bud_path)
                add_budunit_to_stance_csv_strs(voice_bud, x_csv_strs, ",")
    return x_csv_strs


def create_stance0001_file(fisc_mstr_dir: str, owner_name: OwnerName):
    stance_csv_strs = collect_stance_csv_strs(fisc_mstr_dir, owner_name)
    owner_stance_dir = create_stances_owner_dir_path(fisc_mstr_dir, owner_name)
    csv_dict_to_excel(stance_csv_strs, owner_stance_dir, STANCE0001_FILENAME)
