from src.f00_instrument.db_toolbox import (
    sqlite_bool,
    sqlite_str,
    sqlite_null,
    create_insert_sqlstr,
    RowData,
    rowdata_shop,
    get_rowdata,
    dict_factory,
    sqlite_connection,
    _get_grouping_select_clause,
    _get_grouping_groupby_clause,
    _get_having_equal_value_clause,
    get_grouping_with_all_values_equal_sql_query,
    get_groupby_sql_query,
    insert_csv,
    create_table_from_csv,
)
from pytest import raises as pytest_raises, fixture as pytest_fixture
from os import remove as os_remove
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_sqlite_null_ReturnsCorrectObj():
    assert sqlite_null(True)
    assert sqlite_null("yea") == "yea"
    assert sqlite_null(None) == "NULL"


def test_sqlite_bool_ReturnsCorrectObj():
    assert sqlite_bool(x_int=0) is False
    assert sqlite_bool(x_int=1)
    assert sqlite_bool(x_int=None) == "NULL"


def test_sqlite_str_ReturnsCorrectObj():
    assert sqlite_str(True) == "TRUE"
    assert sqlite_str(False) == "FALSE"
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sqlite_str("Bob")
    assert str(excinfo.value) == "function requires boolean"


def test_sqlite_create_insert_sqlstr_ReturnsCorrectObj():
    # ESTABLISH
    x_table = "kubo_trains"
    eagle_id_str = "eagle_id"
    train_id_str = "train_id"
    train_color_str = "train_color"
    x_columns = [eagle_id_str, train_id_str, train_color_str]
    eagle_id_value = 47
    train_id_value = "TR34"
    train_color_value = "red"
    x_values = [eagle_id_value, train_id_value, train_color_value]

    # WHEN
    gen_sqlstr = create_insert_sqlstr(x_table, x_columns, x_values)

    # THEN
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {eagle_id_str}
, {train_id_str}
, {train_color_str}
)
VALUES (
  {eagle_id_value}
, '{train_id_value}'
, '{train_color_value}'
)
;"""
    print(example_sqlstr)
    assert example_sqlstr == gen_sqlstr


def test_RowData_Exists():
    # WHEN
    x_rowdata = RowData()

    # THEN
    assert x_rowdata
    assert x_rowdata.tablename is None
    assert x_rowdata.row_dict is None


def test_rowdata_shop_ReturnsObj():
    # ESTABLISH
    x_tablename = "earth"
    with sqlite_connection(":memory:") as conn:
        res = conn.execute("SELECT 'Earth' AS name, 6378 AS radius")
        row = res.fetchone()
        print(f"{row=}")
        print(f"{type(row)=}")

        conn.row_factory = dict_factory
        res2 = conn.execute("SELECT 'Earth' AS name, 6378 AS radius")
        row2 = res2.fetchone()
        print(f"{row2=}")
        print(f"{type(row2)=}")

    # WHEN
    x_rowdata = rowdata_shop(x_tablename, row2)

    # THEN
    assert x_rowdata
    assert x_rowdata.tablename == "earth"
    assert x_rowdata.row_dict == {"name": "Earth", "radius": 6378}


def test_rowdata_shop_RaiseErrorIf_row_dict_IsNotDict():
    # ESTABLISH
    x_tablename = "earth"

    # WHEN / THEN
    with sqlite_connection(":memory:") as conn:
        conn.row_factory = None
        res = conn.execute("SELECT 'Earth' AS name, 6378 AS radius")
        row = res.fetchone()
        print(f"{row=}")
        print(f"{type(row)=}")

    with pytest_raises(Exception) as excinfo:
        rowdata_shop(x_tablename, row)
    assert str(excinfo.value) == "row_dict is not dictionary"


def test_rowdata_shop_ReturnsObjWithoutNone():
    # ESTABLISH
    x_tablename = "earth"
    with sqlite_connection(":memory:") as conn:
        # conn.row_factory = dict_factory
        res2 = conn.execute("SELECT 'Earth' AS name, 6378 AS radius, NULL as color")
        row2 = res2.fetchone()
        print(f"{row2=}")
        print(f"{type(row2)=}")
        print(f"{type(res2)=}")

    # WHEN
    x_rowdata = rowdata_shop(x_tablename, row2)

    # THEN
    assert x_rowdata
    assert x_rowdata.tablename == "earth"
    assert x_rowdata.row_dict == {"name": "Earth", "radius": 6378}


def test_get_rowdata_ReturnsCorrectObj():
    # ESTABLISH
    x_tablename = "earth"

    # WHEN
    with sqlite_connection(":memory:") as conn:
        select_sqlstr = "SELECT 'Earth' AS name, 6378 AS radius, NULL as color"
        x_rowdata = get_rowdata(x_tablename, conn, select_sqlstr)

    # THEN
    assert x_rowdata
    assert x_rowdata.tablename == "earth"
    assert x_rowdata.row_dict == {"name": "Earth", "radius": 6378}


def test_get_groupby_select_clause_ReturnsObj_Scenario0():
    # ESTABLISH
    x_group_by_columns = set()
    x_value_columns = set()

    # WHEN
    x_select_clause = _get_grouping_select_clause(x_group_by_columns, x_value_columns)

    # THEN
    assert x_select_clause == "SELECT"


def test_get_groupby_select_clause_ReturnsObj_Scenario1():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    x_group_by_columns = [fizz_str, buzz_str]
    x_value_columns = []

    # WHEN
    x_select_clause = _get_grouping_select_clause(x_group_by_columns, x_value_columns)

    # THEN
    assert x_select_clause == f"SELECT {fizz_str}, {buzz_str}"


def test_get_groupby_select_clause_ReturnsObj_Scenario2():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    swim_str = "swim"
    run_str = "run"
    x_group_by_columns = [fizz_str, buzz_str]
    x_value_columns = [swim_str, run_str]

    # WHEN
    gen_select_clause = _get_grouping_select_clause(x_group_by_columns, x_value_columns)

    # THEN
    example_str = f"SELECT {fizz_str}, {buzz_str}, MAX({swim_str}) AS {swim_str}, MAX({run_str}) AS {run_str}"
    assert gen_select_clause == example_str


def test_get_grouping_groupby_clause_ReturnsObj_Scenario0():
    # ESTABLISH
    x_group_by_columns = set()

    # WHEN
    x_select_clause = _get_grouping_groupby_clause(x_group_by_columns)

    # THEN
    assert x_select_clause == "GROUP BY"


def test_get_grouping_groupby_clause_ReturnsObj_Scenario1():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    x_group_by_columns = [fizz_str, buzz_str]

    # WHEN
    x_select_clause = _get_grouping_groupby_clause(x_group_by_columns)

    # THEN
    assert x_select_clause == f"GROUP BY {fizz_str}, {buzz_str}"


def test_get_having_equal_value_clause_ReturnsObj_Scenario0():
    # ESTABLISH
    x_value_columns = []

    # WHEN
    gen_having_clause = _get_having_equal_value_clause(x_value_columns)

    # THEN
    assert gen_having_clause == ""


def test_get_having_equal_value_clause_ReturnsObj_Scenario1():
    # ESTABLISH
    swim_str = "swim"
    run_str = "run"
    x_value_columns = [swim_str, run_str]

    # WHEN
    gen_having_clause = _get_having_equal_value_clause(x_value_columns)

    # THEN
    static_having_clause = (
        f"HAVING MIN({swim_str}) = MAX({swim_str}) AND MIN({run_str}) = MAX({run_str})"
    )
    assert gen_having_clause == static_having_clause


def test_get_groupby_sql_query_ReturnsObj_Scenario0():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    swim_str = "swim"
    run_str = "run"
    x_group_by_columns = [fizz_str, buzz_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "fizzybuzzy"

    # WHEN
    gen_select_clause = get_groupby_sql_query(
        x_table_name, x_group_by_columns, x_value_columns
    )

    # THEN
    example_str = f"""{_get_grouping_select_clause(x_group_by_columns, x_value_columns)} FROM {x_table_name} GROUP BY {fizz_str}, {buzz_str}"""
    assert gen_select_clause == example_str


def test_get_grouping_with_all_values_equal_sql_query_ReturnsObj_Scenario0():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    swim_str = "swim"
    run_str = "run"
    x_group_by_columns = [fizz_str, buzz_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "fizzybuzzy"

    # WHEN
    gen_select_clause = get_grouping_with_all_values_equal_sql_query(
        x_table_name, x_group_by_columns, x_value_columns
    )

    # THEN
    example_str = f"""{get_groupby_sql_query(x_table_name, x_group_by_columns, x_value_columns)} HAVING MIN({swim_str}) = MAX({swim_str}) AND MIN({run_str}) = MAX({run_str})"""
    assert gen_select_clause == example_str


# @pytest_fixture
# def setup_database_and_csv():
#     """
#     Fixture to set up a temporary SQLite database and CSV file for testing.
#     Yields the database path, table name, and CSV file path, and cleans up after the test.
#     """
#     test_db = "test_database.db"
#     test_table = "test_table"
#     test_csv = "test_data.csv"

#     # Create a test SQLite database
#     conn = sqlite3_connect(test_db)
#     cursor = conn.cursor()

#     # Create a test table
#     cursor.execute(
#         f"""
#         CREATE TABLE {test_table} (
#             id INTEGER PRIMARY KEY,
#             name TEXT,
#             age INTEGER,
#             email TEXT
#         )
#     """
#     )
#     conn.commit()
#     conn.close()

#     # Create a test CSV file
#     with open(test_csv, "w", newline="", encoding="utf-8") as csv_file:
#         csv_file.write("id,name,age,email\n")
#         csv_file.write("1,John Doe,30,john@example.com\n")
#         csv_file.write("2,Jane Smith,25,jane@example.com\n")

#     yield test_db, test_table, test_csv

#     # Clean up
#     if os_path_exists(test_db):
#         os_remove(test_db)
#     if os_path_exists(test_csv):
#         os_remove(test_csv)


# def test_insert_csv(setup_database_and_csv):
#     """Test the insert_csv function using pytest."""
#     test_db, test_table, test_csv = setup_database_and_csv

#     # Call the function to insert data from the CSV file into the database
#     insert_csv(test_csv, test_db, test_table)

#     # Verify the data was inserted correctly
#     conn = sqlite3_connect(test_db)
#     cursor = conn.cursor()
#     cursor.execute(f"SELECT * FROM {test_table}")
#     rows = cursor.fetchall()
#     conn.close()

#     # Expected data
#     expected_data = [
#         (1, "John Doe", 30, "john@example.com"),
#         (2, "Jane Smith", 25, "jane@example.com"),
#     ]

#     assert rows == expected_data


@pytest_fixture
def setup_database_and_csv():
    """
    Fixture to set up a temporary SQLite database and CSV file for testing.
    Yields the database connection, table name, and CSV file path, and cleans up after the test.
    """
    test_db = "test_database.db"
    test_table = "test_table"
    test_csv = "test_data.csv"

    # Create a test SQLite database
    conn = sqlite3_connect(test_db)
    cursor = conn.cursor()

    # Create a test table
    cursor.execute(
        f"""
        CREATE TABLE {test_table} (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        )
    """
    )
    conn.commit()

    # Create a test CSV file
    with open(test_csv, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write("id,name,age,email\n")
        csv_file.write("1,John Doe,30,john@example.com\n")
        csv_file.write("2,Jane Smith,25,jane@example.com\n")

    yield conn, test_table, test_csv

    # Clean up
    conn.close()
    if os_path_exists(test_db):
        os_remove(test_db)
    if os_path_exists(test_csv):
        os_remove(test_csv)


def test_insert_csv(setup_database_and_csv):
    """Test the insert_csv function using pytest."""
    # ESTABLISH
    conn, test_table, test_csv = setup_database_and_csv

    # WHEN
    # Call the function to insert data from the CSV file into the database
    insert_csv(test_csv, conn, test_table)

    # THEN
    # Verify the data was inserted correctly
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {test_table}")
    rows = cursor.fetchall()

    # Expected data
    expected_data = [
        (1, "John Doe", 30, "john@example.com"),
        (2, "Jane Smith", 25, "jane@example.com"),
    ]

    assert rows == expected_data


def test_changes_committed(setup_database_and_csv):
    """Test that changes are committed to the database."""
    conn, test_table, test_csv = setup_database_and_csv

    # Insert data
    insert_csv(test_csv, conn, test_table)

    # Close and reopen the connection to verify persistence
    conn.close()
    conn = sqlite3_connect("test_database.db")

    # Verify the data is still present
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {test_table}")
    rows = cursor.fetchall()
    conn.close()

    # Expected data
    expected_data = [
        (1, "John Doe", 30, "john@example.com"),
        (2, "Jane Smith", 25, "jane@example.com"),
    ]

    assert rows == expected_data


def test_create_table_from_csv_ChangesDBState(setup_database_and_csv):
    """Test the create_table_from_csv_with_types function."""
    conn, test_table, test_csv = setup_database_and_csv

    # Define column types
    column_types = {
        "id": "INTEGER",
        "name": "TEXT",
        "age": "INTEGER",
        "email": "TEXT",
        "city": "TEXT",
    }

    # Call the function to create a table based on the CSV header and column types
    new_table = "new_test_table"
    create_table_from_csv(test_csv, conn, new_table, column_types)

    # Verify the table was created correctly
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({new_table})")
    columns = cursor.fetchall()

    # Expected column definitions
    expected_columns = [
        (0, "id", "INTEGER", 0, None, 0),
        (1, "name", "TEXT", 0, None, 0),
        (2, "age", "INTEGER", 0, None, 0),
        (3, "email", "TEXT", 0, None, 0),
    ]

    assert columns == expected_columns
