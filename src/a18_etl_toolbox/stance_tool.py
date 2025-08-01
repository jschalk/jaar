from os.path import exists as os_path_exists
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.a00_data_toolbox.csv_toolbox import (
    delete_column_from_csv_string,
    replace_csv_column_from_string,
)
from src.a00_data_toolbox.file_toolbox import create_path, get_level1_dirs
from src.a12_hub_toolbox.hub_tool import open_believer_file
from src.a15_belief_logic.belief_main import get_default_path_beliefunit
from src.a17_idea_logic.idea_csv_tool import (
    add_beliefunit_to_stance_csv_strs,
    add_believerunit_to_stance_csv_strs,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import csv_dict_to_excel, prettify_excel
from src.a18_etl_toolbox.a18_path import (
    create_belief_mstr_path,
    create_stance0001_path,
    create_world_db_path,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
)


def add_to_br00042_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
    pidtitl_s_vld_tablename = prime_tbl("PIDTITL", "s", "vld")
    pidcore_s_vld_tablename = prime_tbl("PIDCORE", "s", "vld")

    select_sqlstr = f"""
SELECT
  "" event_int
, pidtitl.face_name
, pidtitl.otx_title
, pidtitl.inx_title
, pidcore.otx_knot
, pidcore.inx_knot
, pidcore.unknown_str
FROM {pidtitl_s_vld_tablename} pidtitl
JOIN {pidcore_s_vld_tablename} pidcore ON pidcore.face_name = pidtitl.face_name
ORDER BY 
  pidtitl.face_name
, pidtitl.otx_title
, pidtitl.inx_title
, pidcore.otx_knot
, pidcore.inx_knot
, pidcore.unknown_str
;
"""
    cursor.execute(select_sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        x_csv += f"{csv_delimiter.join(row)}\n"
    return x_csv


def add_to_br00043_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
    pidname_s_vld_tablename = prime_tbl("PIDNAME", "s", "vld")
    pidcore_s_vld_tablename = prime_tbl("PIDCORE", "s", "vld")
    select_sqlstr = f"""
SELECT
  "" event_int
, pidname.face_name
, pidname.otx_name
, pidname.inx_name
, pidcore.otx_knot
, pidcore.inx_knot
, pidcore.unknown_str
FROM {pidname_s_vld_tablename} pidname
JOIN {pidcore_s_vld_tablename} pidcore ON pidcore.face_name = pidname.face_name
ORDER BY 
  pidname.face_name
, pidname.otx_name
, pidname.inx_name
, pidcore.otx_knot
, pidcore.inx_knot
, pidcore.unknown_str
;
"""
    cursor.execute(select_sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        x_csv += f"{csv_delimiter.join(row)}\n"
    return x_csv


def add_to_br00044_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
    pidlabe_s_vld_tablename = prime_tbl("PIDLABE", "s", "vld")
    pidcore_s_vld_tablename = prime_tbl("PIDCORE", "s", "vld")

    select_sqlstr = f"""
SELECT
  "" event_int
, pidlabe.face_name
, pidlabe.otx_label
, pidlabe.inx_label
, pidcore.otx_knot
, pidcore.inx_knot
, pidcore.unknown_str
FROM {pidlabe_s_vld_tablename} pidlabe
JOIN {pidcore_s_vld_tablename} pidcore ON pidcore.face_name = pidlabe.face_name
ORDER BY 
  pidlabe.face_name
, pidlabe.otx_label
, pidlabe.inx_label
, pidcore.otx_knot
, pidcore.inx_knot
, pidcore.unknown_str
;
"""
    cursor.execute(select_sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        x_csv += f"{csv_delimiter.join(row)}\n"
    return x_csv


def add_to_br00045_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
    pidrope_s_vld_tablename = prime_tbl("PIDROPE", "s", "vld")
    pidcore_s_vld_tablename = prime_tbl("PIDCORE", "s", "vld")

    select_sqlstr = f"""
SELECT
  "" event_int
, pidrope.face_name
, pidrope.otx_rope
, pidrope.inx_rope
, pidcore.otx_knot
, pidcore.inx_knot
, pidcore.unknown_str
FROM {pidrope_s_vld_tablename} pidrope
JOIN {pidcore_s_vld_tablename} pidcore ON pidcore.face_name = pidrope.face_name
ORDER BY 
  pidrope.face_name
, pidrope.otx_rope
, pidrope.inx_rope
, pidcore.otx_knot
, pidcore.inx_knot
, pidcore.unknown_str
;
"""
    cursor.execute(select_sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        x_csv += f"{csv_delimiter.join(row)}\n"
    return x_csv


def add_pidgin_rows_to_stance_csv_strs(
    cursor: sqlite3_Cursor, belief_csv_strs: dict[str, str], csv_delimiter: str
):
    br00042_csv = belief_csv_strs.get("br00042")
    br00043_csv = belief_csv_strs.get("br00043")
    br00044_csv = belief_csv_strs.get("br00044")
    br00045_csv = belief_csv_strs.get("br00045")
    br00042_csv = add_to_br00042_csv(br00042_csv, cursor, csv_delimiter)
    br00043_csv = add_to_br00043_csv(br00043_csv, cursor, csv_delimiter)
    br00044_csv = add_to_br00044_csv(br00044_csv, cursor, csv_delimiter)
    br00045_csv = add_to_br00045_csv(br00045_csv, cursor, csv_delimiter)
    belief_csv_strs["br00042"] = br00042_csv
    belief_csv_strs["br00043"] = br00043_csv
    belief_csv_strs["br00044"] = br00044_csv
    belief_csv_strs["br00045"] = br00045_csv


def collect_stance_csv_strs(world_dir: str) -> dict[str, str]:
    belief_mstr_dir = create_belief_mstr_path(world_dir)
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
    world_db_path = create_world_db_path(world_dir)
    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        add_pidgin_rows_to_stance_csv_strs(cursor, x_csv_strs, ",")
    db_conn.close()

    return x_csv_strs


def create_stance0001_file(
    world_dir: str,
    output_dir: str,
    world_name: str,
    prettify_excel_bool: bool = True,
):
    stance_csv_strs = collect_stance_csv_strs(world_dir)
    with_face_name_csvs = {}
    for csv_key, csv_str in stance_csv_strs.items():
        csv_str = replace_csv_column_from_string(csv_str, "face_name", world_name)
        csv_str = delete_column_from_csv_string(csv_str, "event_int")
        with_face_name_csvs[csv_key] = csv_str

    csv_dict_to_excel(with_face_name_csvs, output_dir, "stance0001.xlsx")

    # Hard to test function to prettify the excel file
    if prettify_excel_bool:
        stance0001_path = create_stance0001_path(output_dir)
        prettify_excel(stance0001_path)
