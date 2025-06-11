from sqlite3 import Cursor
from src.a02_finance_logic.deal import TranBook


def insert_tranunit_accts_net(cursor: Cursor, tranbook: TranBook, dst_tablename: str):
    """
    Insert the net amounts for each account in the tranbook into the specified table.

    :param cursor: SQLite cursor object
    :param tranbook: TranBook object containing transaction units
    :param dst_tablename: Name of the destination table
    """
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {dst_tablename} (
        owner_name TEXT NOT NULL,
        net_amount REAL NOT NULL
    );
    """
    cursor.execute(create_table_sql)
    accts_net_array = tranbook._get_accts_net_array()
    cursor.executemany(
        f"INSERT INTO {dst_tablename} (owner_name, net_amount) VALUES (?, ?)",
        accts_net_array,
    )
