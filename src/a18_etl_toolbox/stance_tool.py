from os.path import exists as os_path_exists
from src.a00_data_toolbox.csv_toolbox import (
    delete_column_from_csv_string,
    replace_csv_column_from_string,
)
from src.a00_data_toolbox.file_toolbox import create_path, get_level1_dirs
from src.a12_hub_toolbox.hub_tool import open_believer_file
from src.a15_belief_logic.belief import get_default_path_beliefunit
from src.a17_idea_logic.idea_csv_tool import (
    add_beliefunit_to_stance_csv_strs,
    add_believerunit_to_stance_csv_strs,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import csv_dict_to_excel, prettify_excel
from src.a18_etl_toolbox.tran_path import STANCE0001_FILENAME, create_stance0001_path

# TODO #842
# def add_to_br00042_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
#     for x_otx, x_inx in x_pidginunit.titlemap.otx2inx.items():
#         x_row = [
#             x_pidginunit.face_name,
#             str(x_pidginunit.event_int),
#             x_otx,
#             x_pidginunit.otx_knot,
#             x_inx,
#             x_pidginunit.inx_knot,
#             x_pidginunit.unknown_str,
#         ]
#         x_csv += csv_delimiter.join(x_row)
#         x_csv += "\n"
#     return x_csv


# def add_to_br00043_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
#     for x_otx, x_inx in x_pidginunit.namemap.otx2inx.items():
#         x_row = [
#             x_pidginunit.face_name,
#             str(x_pidginunit.event_int),
#             x_otx,
#             x_pidginunit.otx_knot,
#             x_inx,
#             x_pidginunit.inx_knot,
#             x_pidginunit.unknown_str,
#         ]
#         x_csv += csv_delimiter.join(x_row)
#         x_csv += "\n"
#     return x_csv


# def add_to_br00044_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
#     for x_otx, x_inx in x_pidginunit.labelmap.otx2inx.items():
#         x_row = [
#             x_pidginunit.face_name,
#             str(x_pidginunit.event_int),
#             x_otx,
#             x_pidginunit.otx_knot,
#             x_inx,
#             x_pidginunit.inx_knot,
#             x_pidginunit.unknown_str,
#         ]
#         x_csv += csv_delimiter.join(x_row)
#         x_csv += "\n"
#     return x_csv


# def add_to_br00045_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
#     for x_otx, x_inx in x_pidginunit.ropemap.otx2inx.items():
#         x_row = [
#             x_pidginunit.face_name,
#             str(x_pidginunit.event_int),
#             x_otx,
#             x_pidginunit.otx_knot,
#             x_inx,
#             x_pidginunit.inx_knot,
#             x_pidginunit.unknown_str,
#         ]
#         x_csv += csv_delimiter.join(x_row)
#         x_csv += "\n"
#     return x_csv


# def add_pidginunit_to_stance_csv_strs(
#     x_pidgin: PidginUnit, belief_csv_strs: dict[str, str], csv_delimiter: str
# ) -> str:
#     br00042_csv = belief_csv_strs.get("br00042")
#     br00043_csv = belief_csv_strs.get("br00043")
#     br00044_csv = belief_csv_strs.get("br00044")
#     br00045_csv = belief_csv_strs.get("br00045")
#     br00042_csv = add_to_br00042_csv(br00042_csv, x_pidgin, csv_delimiter)
#     br00043_csv = add_to_br00043_csv(br00043_csv, x_pidgin, csv_delimiter)
#     br00044_csv = add_to_br00044_csv(br00044_csv, x_pidgin, csv_delimiter)
#     br00045_csv = add_to_br00045_csv(br00045_csv, x_pidgin, csv_delimiter)
#     belief_csv_strs["br00042"] = br00042_csv
#     belief_csv_strs["br00043"] = br00043_csv
#     belief_csv_strs["br00044"] = br00044_csv
#     belief_csv_strs["br00045"] = br00045_csv


def collect_stance_csv_strs(belief_mstr_dir: str) -> dict[str, str]:
    x_csv_strs = create_init_stance_idea_csv_strs()
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    for belief_label in get_level1_dirs(beliefs_dir):
        x_beliefunit = get_default_path_beliefunit(belief_mstr_dir, belief_label)
        add_beliefunit_to_stance_csv_strs(x_beliefunit, x_csv_strs, ",")
        belief_dir = create_path(beliefs_dir, belief_label)
        believers_dir = create_path(belief_dir, "believers")
        for believer_name in get_level1_dirs(believers_dir):
            believer_dir = create_path(believers_dir, believer_name)
            gut_dir = create_path(believer_dir, "gut")
            gut_believer_path = create_path(gut_dir, f"{believer_name}.json")
            if os_path_exists(gut_believer_path):
                gut_believer = open_believer_file(gut_believer_path)
                add_believerunit_to_stance_csv_strs(gut_believer, x_csv_strs, ",")
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
