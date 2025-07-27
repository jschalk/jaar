from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_db_tables
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    save_file,
    set_dir,
)
from src.a07_timeline_logic.calendar_markdown import get_calendarmarkdown_str
from src.a15_belief_logic.belief_main import get_default_path_beliefunit
from src.a15_belief_logic.belief_timeline import get_belief_believertimelinepoint
from src.a17_idea_logic.idea_db_tool import save_table_to_csv
from src.a19_kpi_toolbox.kpi_sqlstrs import get_belief_kpi001_partner_nets_sqlstr


def create_populate_kpi001_table(cursor: sqlite3_Cursor):
    cursor.execute("DROP TABLE IF EXISTS belief_kpi001_partner_nets")
    cursor.execute(get_belief_kpi001_partner_nets_sqlstr())


def get_default_kpi_bundle() -> str:
    return "default_kpi_bundle"


def get_all_kpi_functions() -> dict[str,]:
    """
    Returns a dict of all KPI ids and their functions.
    """
    return {"belief_kpi001_partner_nets": create_populate_kpi001_table}


def get_bundles_config() -> dict[str]:
    """
    Returns a set of all KPI strings.
    """
    return {"default_kpi_bundle": {"belief_kpi001_partner_nets"}}


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
        if kpi_id == "belief_kpi001_partner_nets":
            create_populate_kpi001_table(cursor)


def create_kpi_csvs(db_path: str, dst_dir: str):
    with sqlite3_connect(db_path) as db_conn:
        cursor = db_conn.cursor()
        kpi_tables = get_db_tables(db_conn, "kpi")
        for kpi_table in kpi_tables:
            save_table_to_csv(cursor, dst_dir, kpi_table)
    db_conn.close()


def create_calendar_markdown_files(belief_mstr_dir: str, output_dir: str):
    set_dir(output_dir)
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    for belief_label in get_level1_dirs(beliefs_dir):
        belief_calendar_md_path = create_path(output_dir, f"{belief_label}_calendar.md")
        x_beliefunit = get_default_path_beliefunit(belief_mstr_dir, belief_label)
        belief_believertimelinepoint = get_belief_believertimelinepoint(x_beliefunit)
        belief_year_num = belief_believertimelinepoint._year_num
        belief_timeline_config = x_beliefunit.timeline.get_dict()
        x_calendarmarkdown = get_calendarmarkdown_str(
            belief_timeline_config, belief_year_num
        )
        save_file(belief_calendar_md_path, None, x_calendarmarkdown)

    # a23_calendar_md_path = create_path(output_dir, f"{a23_str}_calendar.md")
