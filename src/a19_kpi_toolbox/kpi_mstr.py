from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_db_tables
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    save_file,
    set_dir,
)
from src.a07_timeline_logic.calendar_markdown import get_calendarmarkdown_str
from src.a15_bank_logic.bank import (
    get_from_default_path as bankunit_get_from_default_path,
)
from src.a15_bank_logic.bank_timeline import get_bank_plantimelinepoint
from src.a17_idea_logic.idea_db_tool import save_table_to_csv
from src.a19_kpi_toolbox.kpi_sqlstrs import get_bank_kpi001_acct_nets_sqlstr


def create_populate_kpi001_table(cursor: sqlite3_Cursor):
    cursor.execute(get_bank_kpi001_acct_nets_sqlstr())


def get_default_kpi_bundle() -> str:
    return "default_kpi_bundle"


def get_all_kpi_functions() -> dict[str,]:
    """
    Returns a dict of all KPI ids and their functions.
    """
    return {"bank_kpi001_acct_nets": create_populate_kpi001_table}


def get_bundles_config() -> dict[str]:
    """
    Returns a set of all KPI strings.
    """
    return {"default_kpi_bundle": {"bank_kpi001_acct_nets"}}


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
        if kpi_id == "bank_kpi001_acct_nets":
            create_populate_kpi001_table(cursor)


def create_kpi_csvs(db_path: str, dst_dir: str):
    with sqlite3_connect(db_path) as db_conn:
        cursor = db_conn.cursor()
        kpi_tables = get_db_tables(db_conn, "kpi")
        for kpi_table in kpi_tables:
            save_table_to_csv(cursor, dst_dir, kpi_table)


def create_calendar_markdown_files(bank_mstr_dir: str, output_dir: str):
    set_dir(output_dir)
    banks_dir = create_path(bank_mstr_dir, "banks")
    for bank_label in get_level1_dirs(banks_dir):
        bank_calendar_md_path = create_path(output_dir, f"{bank_label}_calendar.md")
        x_bankunit = bankunit_get_from_default_path(bank_mstr_dir, bank_label)
        bank_plantimelinepoint = get_bank_plantimelinepoint(x_bankunit)
        bank_year_num = bank_plantimelinepoint._year_num
        bank_timeline_config = x_bankunit.timeline.get_dict()
        x_calendarmarkdown = get_calendarmarkdown_str(
            bank_timeline_config, bank_year_num
        )
        save_file(bank_calendar_md_path, None, x_calendarmarkdown)

    # a23_calendar_md_path = create_path(output_dir, f"{a23_str}_calendar.md")
