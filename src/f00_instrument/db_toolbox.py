from src.f00_instrument.file import set_dir, create_path
from sqlite3 import (
    Connection,
    connect as sqlite3_connect,
    Error as sqlite3_Error,
    Connection as sqlite3_Connection,
)
from dataclasses import dataclass
from contextlib import contextmanager
from csv import reader as csv_reader, writer as csv_writer
from os.path import join as os_path_join
from copy import copy as copy_copy


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
    db_tables_columns = get_db_columns(db_conn)

    # # for table_name, table_dict in tables_dict.items():
    # for table_name in tables_dict:
    #     if db_tables.get(table_name) is None:
    #         # print(f"Table {table_name} is missing")
    #         return False

    #     # db_columns = set(db_tables_columns.get(table_name).keys())
    #     # config_columns = set(table_dict.get("columns").keys())
    #     # diff_columns = db_columns.symmetric_difference(config_columns)
    #     # print(f"Table: {table_name} Column differences: {diff_columns}")

    #     # if diff_columns:
    #     #     return False
    return all(db_tables.get(table_name) is not None for table_name in tables_dict)


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
    groupby_columns: list[str], value_columns: list[str]
) -> str:
    select_str = "SELECT"
    for groupby_column in groupby_columns:
        select_str += f" {groupby_column},"
    for value_column in value_columns:
        select_str += f" MAX({value_column}) AS {value_column},"
    return _remove_comma_at_end(select_str)


def _remove_comma_at_end(x_str: str) -> str:
    return x_str.removesuffix(",")


def _get_grouping_groupby_clause(groupby_columns: list[str]) -> str:
    groupby_str = "GROUP BY"
    for groupby_column in groupby_columns:
        groupby_str += f" {groupby_column},"
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
    x_table: str, groupby_columns: list[str], value_columns: list[str]
) -> str:
    return f"{_get_grouping_select_clause(groupby_columns, value_columns)} FROM {x_table} {_get_grouping_groupby_clause(groupby_columns)}"


def get_grouping_with_all_values_equal_sql_query(
    x_table: str, groupby_columns: list[str], value_columns: list[str]
) -> str:
    return f"{_get_grouping_select_clause(groupby_columns, value_columns)} FROM {x_table} {_get_grouping_groupby_clause(groupby_columns)} {_get_having_equal_value_clause(value_columns)}"


def insert_csv(csv_file_path: str, conn_or_cursor: sqlite3_Connection, table_name: str):
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
                conn_or_cursor.execute(insert_query, row)

    except sqlite3_Error as e:
        print(f"SQLite error: {e}")

    except Exception as e:
        print(f"Error: {e}")


class sqlite3_Error_Exception(Exception):
    pass


def get_create_table_sqlstr(
    tablename: str,
    columns_list: list[str],
    column_types: dict[str, str],
) -> str:
    # Dynamically create a table schema based on the provided column types
    columns = []
    for column in columns_list:
        data_type = column_types.get(column, "TEXT")  # Default to TEXT
        columns.append(f"{column} {data_type}")
    columns_definition = ", ".join(columns)
    return f"CREATE TABLE IF NOT EXISTS {tablename} ({columns_definition})"


def create_table_from_columns(
    conn_or_cursor: sqlite3_Connection,
    tablename: str,
    columns_list: list[str],
    column_types: dict[str, str],
):
    x_sqlstr = get_create_table_sqlstr(tablename, columns_list, column_types)
    conn_or_cursor.execute(x_sqlstr)


def create_table_from_csv(
    csv_file_path: str,
    conn_or_cursor: sqlite3_Connection,
    table_name: str,
    column_types: dict[str, str],
):
    """
    Creates a SQLite table based on the header of a CSV file and a dictionary of column names and their data types.

    Args:
        csv_file_path (str): Path to the CSV file.
        sqlite_connection (sqlite3.Connection): SQLite database connection object.
        table_name (str): Name of the table to create.
        column_types (dict): Dictionary mapping column names to their SQLite data types.

    Returns:
        None
    """
    try:
        # Open the CSV file to read the header
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
            headers = csv_file.readline().strip().split(",")
        create_table_from_columns(conn_or_cursor, table_name, headers, column_types)

    except sqlite3_Error as e:
        raise sqlite3_Error_Exception(f"SQLite error: {e}") from e

    # except Exception as e:
    #     raise Exception(f"Error: {e}")


def db_table_exists(conn_or_cursor: sqlite3_Connection, tablename: str) -> bool:
    table_master_sqlstr = (
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename}';"
    )
    result = conn_or_cursor.execute(table_master_sqlstr).fetchone()
    return bool(result)


def get_table_columns(conn_or_cursor: sqlite3_Connection, tablename: str) -> list[str]:
    db_columns = conn_or_cursor.execute(f"PRAGMA table_info({tablename})").fetchall()
    return [db_column[1] for db_column in db_columns]


def create_select_inconsistency_query(
    conn_or_cursor: sqlite3_Connection,
    x_tablename: str,
    focus_columns: set[str],
    exclude_columns: set[str],
) -> str:
    table_columns = get_table_columns(conn_or_cursor, x_tablename)
    having_str = None
    for x_column in table_columns:
        if x_column not in exclude_columns and x_column not in focus_columns:
            if having_str:
                having_str += f"\n    OR MIN({x_column}) != MAX({x_column})"
            else:
                having_str = f"HAVING MIN({x_column}) != MAX({x_column})"
    if not having_str:
        having_str = ""
    focus_columns_list = []
    focus_columns_list.extend(
        t_column
        for t_column in table_columns
        if t_column not in exclude_columns and t_column in focus_columns
    )
    focus_columns_str = ", ".join(focus_columns_list)
    return f"""SELECT {focus_columns_str}
FROM {x_tablename}
GROUP BY {focus_columns_str}
{having_str}
"""


def create_update_inconsistency_error_query(
    conn_or_cursor: sqlite3_Connection,
    x_tablename: str,
    focus_columns: set[str],
    exclude_columns: set[str],
):
    select_inconsistency_query = create_select_inconsistency_query(
        conn_or_cursor, x_tablename, focus_columns, exclude_columns
    )
    table_columns = get_table_columns(conn_or_cursor, x_tablename)
    where_str = None
    for x_column in table_columns:
        if x_column not in exclude_columns and x_column in focus_columns:
            if where_str:
                where_str += f"\n    AND inconsistency_rows.{x_column} = {x_tablename}.{x_column}"
            else:
                where_str = (
                    f"WHERE inconsistency_rows.{x_column} = {x_tablename}.{x_column}"
                )

    return f"""WITH inconsistency_rows AS (
{select_inconsistency_query})
UPDATE {x_tablename}
SET error_message = 'Inconsistent fisc data'
FROM inconsistency_rows
{where_str}
;
"""


def create_table2table_agg_insert_query(
    conn_or_cursor: sqlite3_Connection,
    src_table: str,
    dst_table: str,
    focus_cols: list[str],
    exclude_cols: set[str],
) -> str:
    focus_cols_set = set(focus_cols)
    dst_columns = get_table_columns(conn_or_cursor, dst_table)
    dst_columns = [dst_col for dst_col in dst_columns if dst_col not in exclude_cols]
    dst_columns_str = ", ".join(list(dst_columns))
    select_columns_str = None
    for dst_column in dst_columns:
        if select_columns_str is None and dst_column in focus_cols_set:
            select_columns_str = f"{dst_column}"
        elif dst_column in focus_cols_set:
            select_columns_str += f", {dst_column}"
        else:
            select_columns_str += f", MAX({dst_column})"
    groupby_columns_str = ", ".join(focus_cols)

    return f"""INSERT INTO {dst_table} ({dst_columns_str})
SELECT {select_columns_str}
FROM {src_table}
WHERE error_message IS NULL
GROUP BY {groupby_columns_str}
;
"""


def is_stageable(
    conn_or_cursor: sqlite3_Connection,
    src_table: str,
    required_columns: set[str],
):
    src_columns = set(get_table_columns(conn_or_cursor, src_table))
    return required_columns.issubset(src_columns)


def save_to_split_csvs(
    conn_or_cursor: sqlite3_Connection,
    tablename,
    key_columns,
    output_dir,
    col1_prefix=None,
    col2_prefix=None,
):
    """
    Select a single table from a SQLite DB, filter rows into CSVs by key columns, and save them.

    :param db_path: Path to the SQLite database file.
    :param tablename: Name of the table to query.
    :param key_columns: List of columns to use as keys for filtering rows.
    :param output_dir: Directory to save the resulting CSVs.
    """
    # Fetch all rows from the table
    column_names = get_table_columns(conn_or_cursor, tablename)
    query = f"SELECT * FROM {tablename}"
    rows = conn_or_cursor.execute(query).fetchall()

    # Find the indices of key columns
    key_indices = [column_names.index(key) for key in key_columns]

    # Organize rows by key values
    collectioned_rows = {}
    for row in rows:
        # Create a tuple of key values
        key_values = tuple(row[index] for index in key_indices)

        if key_values not in collectioned_rows:
            collectioned_rows[key_values] = []
        collectioned_rows[key_values].append(row)

    # Write collectioned rows to separate CSV files
    for key_values, collection in collectioned_rows.items():
        if col1_prefix:
            new_key_values = [key_values[0], col1_prefix]
            new_key_values.extend(key_values[1:])
            key_values = new_key_values
        if col2_prefix:
            new_key_values = key_values[:3]
            new_key_values.append(col2_prefix)
            new_key_values.extend(key_values[3:])
            key_values = new_key_values

        key_path_part = get_key_part(key_values)
        csv_path = create_path(output_dir, key_path_part)
        set_dir(csv_path)
        output_file = os_path_join(csv_path, f"{tablename}.csv")
        print(f"{csv_path=}")
        # Write to CSV
        with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv_writer(csv_file)
            writer.writerow(column_names)
            writer.writerows(collection)


def get_key_part(key_values: list[str]) -> str:
    return "/".join(str(value) for value in key_values)
    # x_key_path = ""
    # for value in key_values:
    #     header_name = key_columns.pop()
    #     if x_key_path == "":
    #         x_key_path = f"{header_name}s/{value}"
    #     else:
    #         x_key_path += f"/{header_name}s/{value}"
    # return x_key_path
