from sqlite3 import (
    Connection,
    connect as sqlite3_connect,
    Error as sqlite3_Error,
    Connection as sqlite3_Connection,
)
from dataclasses import dataclass
from contextlib import contextmanager
from csv import reader as csv_reader


def sqlite_null(x_obj: any):
    return "NULL" if x_obj is None else x_obj


def sqlite_bool(x_int: int) -> bool:
    """sqlite_true_to_python_true"""
    return "NULL" if x_int is None else x_int == 1


def sqlite_str(x_bool: any) -> str:
    """python_bool_to_SQLITE_bool"""
    if x_bool is True:
        x_str = "TRUE"
    elif not x_bool:
        x_str = "FALSE"
    else:
        raise TypeError("function requires boolean")
    return x_str


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
    x_dict = {
        x_key: x_value for x_key, x_value in row_dict.items() if x_value is not None
    }
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
    print(f"{db_tables.keys()=}")
    db_tables_columns = get_db_columns(db_conn)

    # for table_name, table_dict in tables_dict.items():
    for table_name in tables_dict:
        if db_tables.get(table_name) is None:
            print(f"Table {table_name} is missing")
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


def _get_grouping_select_clause(
    group_by_columns: list[str], value_columns: list[str]
) -> str:
    select_str = "SELECT"
    for group_by_column in group_by_columns:
        select_str += f" {group_by_column},"
    for value_column in value_columns:
        select_str += f" MAX({value_column}) AS {value_column},"
    return _remove_comma_at_end(select_str)


def _remove_comma_at_end(x_str: str) -> str:
    return x_str.removesuffix(",")


def _get_grouping_groupby_clause(group_by_columns: list[str]) -> str:
    groupby_str = "GROUP BY"
    for group_by_column in group_by_columns:
        groupby_str += f" {group_by_column},"
    return _remove_comma_at_end(groupby_str)


def _get_having_equal_value_clause(value_columns: list[str]) -> str:
    if not value_columns:
        return ""
    having_clause = "HAVING"
    for value_column in value_columns:
        if having_clause != "HAVING":
            having_clause += " AND"
        having_clause += f" MIN({value_column}) = MAX({value_column})"
    return _remove_comma_at_end(having_clause)


def get_groupby_sql_query(
    x_table: str, group_by_columns: list[str], value_columns: list[str]
) -> str:
    return f"{_get_grouping_select_clause(group_by_columns, value_columns)} FROM {x_table} {_get_grouping_groupby_clause(group_by_columns)}"


def get_grouping_with_all_values_equal_sql_query(
    x_table: str, group_by_columns: list[str], value_columns: list[str]
) -> str:
    return f"{_get_grouping_select_clause(group_by_columns, value_columns)} FROM {x_table} {_get_grouping_groupby_clause(group_by_columns)} {_get_having_equal_value_clause(value_columns)}"


def insert_csv(
    csv_file_path: str, sqlite_connection: sqlite3_Connection, table_name: str
):
    """
    Inserts data from a CSV file into a specified SQLite database table.

    Args:
        csv_file_path (str): Path to the CSV file.
        sqlite_connection (sqlite3.Connection): SQLite database connection object.
        table_name (str): Name of the table to insert data into.

    Returns:
        None
    """
    try:
        # Use the provided SQLite connection
        cursor = sqlite_connection.cursor()

        # Open the CSV file
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv_reader(csv_file)

            # Extract the header row from the CSV file
            headers = next(reader)

            # Create a parameterized SQL query for inserting data
            placeholders = ", ".join(["?"] * len(headers))
            insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"

            # Insert each row into the database
            for row in reader:
                cursor.execute(insert_query, row)

        # Commit the transaction
        sqlite_connection.commit()

    except sqlite3_Error as e:
        print(f"SQLite error: {e}")

    except Exception as e:
        print(f"Error: {e}")
