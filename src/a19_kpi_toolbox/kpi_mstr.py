from sqlite3 import Cursor as sqlite3_Cursor
from src.a00_data_toolbox.file_toolbox import create_path
from src.a19_kpi_toolbox.kpi_sqlstrs import get_vow_kpi001_acct_nets_sqlstr


def create_populate_kpi001_table(cursor: sqlite3_Cursor):
    cursor.execute(get_vow_kpi001_acct_nets_sqlstr())


def get_default_kpi_bundle() -> str:
    return "default_kpi_bundle"


def get_all_kpi_functions() -> dict[str,]:
    """
    Returns a dict of all KPI ids and their functions.
    """
    return {"vow_kpi001_acct_nets": create_populate_kpi001_table}


def get_bundles_config() -> dict[str]:
    """
    Returns a set of all KPI strings.
    """
    return {"default_kpi_bundle": {"vow_kpi001_acct_nets"}}


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
        if kpi_id == "vow_kpi001_acct_nets":
            create_populate_kpi001_table(cursor)


KPI_EXCEL_FILENAME = "kpis.xlsx"


def get_kpi_xlsx_path(vow_mstr_dir: str) -> str:
    stances_dir = create_path(vow_mstr_dir, "stances")
    return create_path(stances_dir, KPI_EXCEL_FILENAME)
