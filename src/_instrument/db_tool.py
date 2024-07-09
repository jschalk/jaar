from sqlite3 import Connection, connect as sqlite3_connect
from dataclasses import dataclass
from contextlib import contextmanager


def sqlite_null(obj_x):
    return "NULL" if obj_x is None else obj_x


def sqlite_bool(int_x) -> bool:
    """sqlite_true_to_python_true"""
    return "NULL" if int_x is None else int_x == 1


def sqlite_text(bool_x) -> str:
    """python_bool_to_SQLITE_bool"""
    if bool_x == True:
        x_text = "TRUE"
    elif bool_x is False:
        x_text = "FALSE"
    else:
        raise TypeError("function requires boolean")
    return x_text


def sqlite_to_python(query_value) -> str:
    """SQLite string to Python None or True"""
    return None if query_value == "NULL" else query_value


def check_connection(conn: Connection) -> bool:
    try:
        conn.cursor()
        return True
    except Exception as ex:
        return False


def create_insert_sqlstr(
    x_table: str, x_columns: list[str], x_values: list[str]
) -> str:
    x_str = f"""
INSERT INTO {x_table} ("""
    columns_str = ""
    for x_column in x_columns:
        if columns_str == "":
            columns_str = f"""{columns_str}
  {x_column}"""
        else:
            columns_str = f"""{columns_str}
, {x_column}"""
    values_str = ""
    for x_value in x_values:
        if str(type(x_value)) != "<class 'int'>":
            x_value = f"'{x_value}'"

        if values_str == "":
            values_str = f"""{values_str}
  {x_value}"""
        else:
            values_str = f"""{values_str}
, {x_value}"""

    return f"""{x_str}{columns_str}
)
VALUES ({values_str}
)
;"""


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


@dataclass
class RowData:
    tablename: str = None
    row_dict: str = None


class row_dict_Exception(Exception):
    pass


def rowdata_shop(
    tablename: str,
    row_dict: str,
):
    if str(type(row_dict)) != "<class 'dict'>":
        raise row_dict_Exception("row_dict is not dictionary")
    x_dict = {x_key: x_value for x_key, x_value in row_dict.items() if x_value != None}
    return RowData(tablename, x_dict)


def get_rowdata(tablename: str, x_conn: Connection, select_sqlstr: str) -> RowData:
    x_conn.row_factory = dict_factory
    results = x_conn.execute(select_sqlstr)
    row1 = results.fetchone()
    return rowdata_shop(tablename, row1)


def get_db_tables(x_conn: Connection) -> dict[str, int]:
    sqlstr = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"
    results = x_conn.execute(sqlstr)

    return {row[0]: 1 for row in results}


def get_db_columns(x_conn: Connection) -> dict[str : dict[str, int]]:
    table_names = get_db_tables(x_conn)
    table_column_dict = {}
    for table_name in table_names.keys():
        sqlstr = f"SELECT name FROM PRAGMA_TABLE_INFO('{table_name}');"
        results = x_conn.execute(sqlstr)
        table_column_dict[table_name] = {row[0]: 1 for row in results}

    return table_column_dict


def get_single_result(db_conn: Connection, sqlstr: str) -> str:
    results = db_conn.execute(sqlstr)
    return results.fetchone()[0]


def get_row_count_sqlstr(table_name: str) -> str:
    return f"SELECT COUNT(*) FROM {table_name}"


def get_row_count(db_conn: Connection, table_name: str) -> str:
    return get_single_result(db_conn, get_row_count_sqlstr(table_name))


def check_table_column_existence(tables_dict: dict, db_conn: Connection) -> bool:
    db_tables = get_db_tables(db_conn)
    db_tables_columns = get_db_columns(db_conn)

    # for table_name, table_dict in tables_dict.items():
    for table_name in tables_dict:
        print(f"Table: {table_name}")
        if db_tables.get(table_name) is None:
            return False

        # db_columns = set(db_tables_columns.get(table_name).keys())
        # config_columns = set(table_dict.get("columns").keys())
        # diff_columns = db_columns.symmetric_difference(config_columns)
        # print(f"Table: {table_name} Column differences: {diff_columns}")

        # if diff_columns:
        #     return False

    return True


@contextmanager
def sqlite_connection(db_name):
    conn = sqlite3_connect(db_name)
    conn.row_factory = dict_factory
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
