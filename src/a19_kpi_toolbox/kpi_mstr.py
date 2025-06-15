from sqlite3 import Cursor as sqlite3_Cursor
from src.a19_kpi_toolbox.kpi_sqlstrs import get_vow_kpi001_acct_nets_sqlstr


def create_populate_kpi001_table(cursor: sqlite3_Cursor):
    cursor.execute(get_vow_kpi001_acct_nets_sqlstr())
