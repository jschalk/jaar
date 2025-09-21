from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.ch00_data_toolbox.db_toolbox import db_table_exists, get_db_tables
from src.ch00_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    save_file,
    set_dir,
)
from src.ch07_timeline_logic.calendar_markdown import get_calendarmarkdown_str
from src.ch15_moment_logic.moment_main import get_default_path_momentunit
from src.ch15_moment_logic.moment_timeline import get_moment_belieftimelinepoint
from src.ch17_idea_logic.idea_db_tool import save_table_to_csv
from src.ch19_kpi_toolbox.kpi_sqlstrs import get_moment_kpi001_voice_nets_sqlstr


def create_populate_kpi001_table(cursor: sqlite3_Cursor):
    cursor.execute("DROP TABLE IF EXISTS moment_kpi001_voice_nets")
    cursor.execute(get_moment_kpi001_voice_nets_sqlstr())


def get_default_kpi_bundle() -> str:
    return "default_kpi_bundle"


def get_all_kpi_functions() -> dict[str,]:
    """
    Returns a dict of all KPI ids and their functions.
    """
    return {"moment_kpi001_voice_nets": create_populate_kpi001_table}


def get_bundles_config() -> dict[str]:
    """
    Returns a set of all KPI strings.
    """
    return {"default_kpi_bundle": {"moment_kpi001_voice_nets"}}


def get_kpi_set_from_bundle(bundle_id: str = None) -> set[str]:
    """
    Returns a set of KPI strings from the specified bundle.
    """
    bundles_config = get_bundles_config()
    if bundle_id is None:
        bundle_id = "default_kpi_bundle"

    return bundles_config.get(bundle_id, set())


def populate_kpi_bundle(cursor: sqlite3_Cursor, bundle_id: str = None):
    """If bundle_id is None, create default kpis"""

    bundle_kpi_ids = get_kpi_set_from_bundle(bundle_id)
    kpi_functions = get_all_kpi_functions()
    for kpi_id in bundle_kpi_ids:
        if kpi_id == "moment_kpi001_voice_nets":
            create_populate_kpi001_table(cursor)


def create_kpi_csvs(db_path: str, dst_dir: str):
    with sqlite3_connect(db_path) as db_conn:
        cursor = db_conn.cursor()
        kpi_tables = get_db_tables(db_conn, "kpi")
        for kpi_table in kpi_tables:
            save_table_to_csv(cursor, dst_dir, kpi_table)
    db_conn.close()


def create_calendar_markdown_files(moment_mstr_dir: str, output_dir: str):
    set_dir(output_dir)
    moments_dir = create_path(moment_mstr_dir, "moments")
    for moment_label in get_level1_dirs(moments_dir):
        moment_calendar_md_path = create_path(output_dir, f"{moment_label}_calendar.md")
        x_momentunit = get_default_path_momentunit(moment_mstr_dir, moment_label)
        moment_belieftimelinepoint = get_moment_belieftimelinepoint(x_momentunit)
        moment_year_num = moment_belieftimelinepoint._year_num
        moment_timeline_config = x_momentunit.timeline.to_dict()
        x_calendarmarkdown = get_calendarmarkdown_str(
            moment_timeline_config, moment_year_num
        )
        save_file(moment_calendar_md_path, None, x_calendarmarkdown)

    # a23_calendar_md_path = create_path(output_dir, f"{a23_str}_calendar.md")
