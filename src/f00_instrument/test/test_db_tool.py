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
    db_table_exists,
    get_table_columns,
    create_table_from_columns,
    create_select_inconsistency_query,
    create_update_inconsistency_error_query,
    create_table2table_agg_insert_query,
    is_stageable,
)
from pytest import raises as pytest_raises, fixture as pytest_fixture
from os import remove as os_remove
from os.path import exists as os_path_exists
from sqlite3 import (
    connect as sqlite3_connect,
    Connection as sqlite3_Connection,
    sqlite_version as sqlite3_sqlite_version,
)


def test_sqlite_null_ReturnsObj():
    assert sqlite_null(True)
    assert sqlite_null("yea") == "yea"
    assert sqlite_null(None) == "NULL"


def test_sqlite_bool_ReturnsObj():
    assert sqlite_bool(x_int=0) is False
    assert sqlite_bool(x_int=1)
    assert sqlite_bool(x_int=None) == "NULL"


def test_sqlite_str_ReturnsObj():
    assert sqlite_str(True) == "TRUE"
    assert sqlite_str(False) == "FALSE"
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sqlite_str("Bob")
    assert str(excinfo.value) == "function requires boolean"


def test_sqlite_create_insert_sqlstr_ReturnsObj():
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


def test_get_rowdata_ReturnsObj():
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
    x_groupby_columns = set()
    x_value_columns = set()

    # WHEN
    x_select_clause = _get_grouping_select_clause(x_groupby_columns, x_value_columns)

    # THEN
    assert x_select_clause == "SELECT"


def test_get_groupby_select_clause_ReturnsObj_Scenario1():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    x_groupby_columns = [fizz_str, buzz_str]
    x_value_columns = []

    # WHEN
    x_select_clause = _get_grouping_select_clause(x_groupby_columns, x_value_columns)

    # THEN
    assert x_select_clause == f"SELECT {fizz_str}, {buzz_str}"


def test_get_groupby_select_clause_ReturnsObj_Scenario2():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    swim_str = "swim"
    run_str = "run"
    x_groupby_columns = [fizz_str, buzz_str]
    x_value_columns = [swim_str, run_str]

    # WHEN
    gen_select_clause = _get_grouping_select_clause(x_groupby_columns, x_value_columns)

    # THEN
    example_str = f"SELECT {fizz_str}, {buzz_str}, MAX({swim_str}) AS {swim_str}, MAX({run_str}) AS {run_str}"
    assert gen_select_clause == example_str


def test_get_grouping_groupby_clause_ReturnsObj_Scenario0():
    # ESTABLISH
    x_groupby_columns = set()

    # WHEN
    x_select_clause = _get_grouping_groupby_clause(x_groupby_columns)

    # THEN
    assert x_select_clause == "GROUP BY"


def test_get_grouping_groupby_clause_ReturnsObj_Scenario1():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    x_groupby_columns = [fizz_str, buzz_str]

    # WHEN
    x_select_clause = _get_grouping_groupby_clause(x_groupby_columns)

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
    x_groupby_columns = [fizz_str, buzz_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "fizzybuzzy"

    # WHEN
    gen_select_clause = get_groupby_sql_query(
        x_table_name, x_groupby_columns, x_value_columns
    )

    # THEN
    example_str = f"""{_get_grouping_select_clause(x_groupby_columns, x_value_columns)} FROM {x_table_name} GROUP BY {fizz_str}, {buzz_str}"""
    assert gen_select_clause == example_str


def test_get_grouping_with_all_values_equal_sql_query_ReturnsObj_Scenario0():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    swim_str = "swim"
    run_str = "run"
    x_groupby_columns = [fizz_str, buzz_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "fizzybuzzy"

    # WHEN
    gen_select_clause = get_grouping_with_all_values_equal_sql_query(
        x_table_name, x_groupby_columns, x_value_columns
    )

    # THEN
    example_str = f"""{get_groupby_sql_query(x_table_name, x_groupby_columns, x_value_columns)} HAVING MIN({swim_str}) = MAX({swim_str}) AND MIN({run_str}) = MAX({run_str})"""
    assert gen_select_clause == example_str


@pytest_fixture
def setup_database_and_csv() -> tuple[sqlite3_Connection, str, str]:  # type: ignore
    """
    Fixture to set up a temporary SQLite database and CSV file for testing.
    Yields the database connection, table name, and CSV file path, and cleans up after the test.
    """
    test_db = "test_database.db"
    test_table = "test_table"
    test_csv_filepath = "test_data.csv"

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
    cursor.close()
    conn.commit()

    # Create a test CSV file
    with open(test_csv_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write("id,name,age,email\n")
        csv_file.write("1,John Doe,30,john@example.com\n")
        csv_file.write("2,Jane Smith,25,jane@example.com\n")

    yield conn, test_table, test_csv_filepath

    # Clean up
    conn.close()
    if os_path_exists(test_db):
        os_remove(test_db)
    if os_path_exists(test_csv_filepath):
        os_remove(test_csv_filepath)


def test_insert_csv_ChangesDBState(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
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


def test_insert_csv_ChangesDBState_WhenPassedCursorObj(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
    """Test the insert_csv function using pytest."""
    # ESTABLISH
    conn, test_table, test_csv = setup_database_and_csv

    # WHEN
    insert_csv(test_csv, conn.cursor(), test_table)

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


def test_insert_csv_ChangesNotCommitted(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
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
    assert rows == []


def test_create_table_from_csv_ChangesDBState(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
    """Test the create_table_from_csv_with_types function."""
    conn, test_table, test_csv_filepath = setup_database_and_csv

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
    create_table_from_csv(test_csv_filepath, conn, new_table, column_types)

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


def test_create_idea_table_from_csv_DoesNothingIfTableExists(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
    # ESTABLISH
    conn, test_table, test_csv_filepath = setup_database_and_csv
    insert_csv(test_csv_filepath, conn, test_table)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {test_table}")
    before_data = [
        (1, "John Doe", 30, "john@example.com"),
        (2, "Jane Smith", 25, "jane@example.com"),
    ]
    assert cursor.fetchall() == before_data

    # WHEN
    create_table_from_csv(test_csv_filepath, conn, test_table, {})

    # THEN
    cursor.execute(f"SELECT * FROM {test_table}")
    assert cursor.fetchall() == before_data


def test_table_exists_ReturnsObjWhenPassedConnectionObj():
    # ESTABLISH
    conn = sqlite3_connect(":memory:")
    users_tablename = "users"
    assert db_table_exists(conn, users_tablename) is False

    # WHEN
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """
    )

    # THEN
    assert db_table_exists(conn, users_tablename)


def test_table_exists_ReturnsObjWhenPassedCusorObj():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        users_tablename = "users"
        assert db_table_exists(cursor, users_tablename) is False

        # WHEN
        cursor.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """
        )

        # THEN
        assert db_table_exists(cursor, users_tablename)


def test_sqlite_version():
    # Retrieve the SQLite version
    sqlite_version = sqlite3_sqlite_version

    # Log the version for debugging purposes
    print(f"SQLite version being used: {sqlite_version}")

    # Check if the version meets requirements (example: 3.30.0 or later)
    major, minor, patch = map(int, sqlite_version.split("."))
    sqlite_old_message = f"SQLite version is too old: {sqlite_version}"
    assert (major, minor, patch) >= (3, 30, 0), sqlite_old_message


def test_get_table_columns_ReturnsObj_Scenario0_TableDoesNotExist(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
    """Test the create_table_from_csv_with_types function."""
    conn, test_table, test_csv_filepath = setup_database_and_csv
    x_tablename = "something_dark_side_table"
    assert db_table_exists(conn, x_tablename) is False

    # WHEN / THEN
    assert get_table_columns(conn, x_tablename) == []


def test_get_table_columns_ReturnsObj_Scenario1_TableExists(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
    conn, test_table, test_csv_filepath = setup_database_and_csv
    x_tablename = "something_dark_side_table"
    create_table_from_csv(test_csv_filepath, conn, x_tablename, {})

    # WHEN / THEN
    assert get_table_columns(conn, x_tablename) == ["id", "name", "age", "email"]


def test_get_table_columns_ReturnsObj_Scenario2_TableExists_PassCursorObj(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
    conn, test_table, test_csv_filepath = setup_database_and_csv
    x_tablename = "something_dark_side_table"
    create_table_from_csv(test_csv_filepath, conn, x_tablename, {})
    expected_columns = ["id", "name", "age", "email"]

    # WHEN / THEN
    assert get_table_columns(conn.cursor(), x_tablename) == expected_columns


def test_create_select_inconsistency_query_ReturnsObj_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age", "email", "hair"]
        create_table_from_columns(cursor, x_tablename, x_columns, {})

        # WHEN
        gen_sqlstr = create_select_inconsistency_query(
            cursor, x_tablename, {"id"}, {"email"}
        )

        # THEN
        expected_sqlstr = """SELECT id
FROM dark_side
GROUP BY id
HAVING MIN(name) != MAX(name)
    OR MIN(age) != MAX(age)
    OR MIN(hair) != MAX(hair)
"""
        assert gen_sqlstr == expected_sqlstr


def test_create_select_inconsistency_query_ReturnsObj_Scenario1():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age", "email", "hair"]
        create_table_from_columns(cursor, x_tablename, x_columns, {})

        # WHEN
        gen_sqlstr = create_select_inconsistency_query(
            cursor, x_tablename, {"id", "name"}, {"email"}
        )

        # THEN
        expected_sqlstr = """SELECT id, name
FROM dark_side
GROUP BY id, name
HAVING MIN(age) != MAX(age)
    OR MIN(hair) != MAX(hair)
"""
        assert gen_sqlstr == expected_sqlstr


def test_create_select_inconsistency_query_ReturnsObj_Scenario2():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age", "email", "hair"]
        create_table_from_columns(cursor, x_tablename, x_columns, {})

        # WHEN
        gen_sqlstr = create_select_inconsistency_query(
            cursor, x_tablename, {"id", "name", "age", "email", "hair"}, {}
        )

        # THEN
        expected_sqlstr = """SELECT id, name, age, email, hair
FROM dark_side
GROUP BY id, name, age, email, hair

"""
        assert gen_sqlstr == expected_sqlstr


def test_create_update_inconsistency_error_query_ReturnsObj_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age", "email", "hair"]
        create_table_from_columns(cursor, x_tablename, x_columns, {})

        # WHEN
        gen_sqlstr = create_update_inconsistency_error_query(
            cursor, x_tablename, {"id"}, {"email"}
        )

        # THEN
        expected_sqlstr = """WITH inconsistency_rows AS (
SELECT id
FROM dark_side
GROUP BY id
HAVING MIN(name) != MAX(name)
    OR MIN(age) != MAX(age)
    OR MIN(hair) != MAX(hair)
)
UPDATE dark_side
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.id = dark_side.id
;
"""
        print(f"""{gen_sqlstr=}""")
        assert gen_sqlstr == expected_sqlstr


def test_create_update_inconsistency_error_queryReturnsObj_Scenario1():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age", "email", "hair"]
        create_table_from_columns(cursor, x_tablename, x_columns, {})

        # WHEN
        gen_sqlstr = create_update_inconsistency_error_query(
            cursor, x_tablename, {"id", "name"}, {"email"}
        )

        # THEN
        expected_sqlstr = """WITH inconsistency_rows AS (
SELECT id, name
FROM dark_side
GROUP BY id, name
HAVING MIN(age) != MAX(age)
    OR MIN(hair) != MAX(hair)
)
UPDATE dark_side
SET error_message = 'Inconsistent fiscal data'
FROM inconsistency_rows
WHERE inconsistency_rows.id = dark_side.id
    AND inconsistency_rows.name = dark_side.name
;
"""
        assert gen_sqlstr == expected_sqlstr


def test_create_table2table_agg_insert_query_ReturnsObj_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        hair_str = "hair"
        src_tablename = "side1"
        src_columns = ["id", "name", "age", "email", hair_str]
        create_table_from_columns(cursor, src_tablename, src_columns, {})
        dst_tablename = "side2"
        dst_columns = ["name", "age", "email", hair_str]
        create_table_from_columns(cursor, dst_tablename, dst_columns, {})

        # WHEN
        gen_sqlstr = create_table2table_agg_insert_query(
            cursor,
            dst_table=dst_tablename,
            src_table=src_tablename,
            focus_cols=["name", "age"],
            exclude_cols={hair_str},
        )

        # THEN
        expected_sqlstr = f"""INSERT INTO {dst_tablename} (name, age, email)
SELECT name, age, MAX(email)
FROM {src_tablename}
WHERE error_message IS NULL
GROUP BY name, age
;
"""
        print(f"     {gen_sqlstr=}")
        print(f"{expected_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_table2table_agg_insert_query_ReturnsObj_Scenario1():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        hair_str = "hair"
        src_tablename = "side1"
        src_columns = ["id", "name", "age", "email", hair_str]
        create_table_from_columns(cursor, src_tablename, src_columns, {})
        dst_tablename = "side2"
        dst_columns = ["name", "age", hair_str]
        create_table_from_columns(cursor, dst_tablename, dst_columns, {})

        # WHEN
        gen_sqlstr = create_table2table_agg_insert_query(
            cursor,
            dst_table=dst_tablename,
            src_table=src_tablename,
            focus_cols=["name"],
            exclude_cols={hair_str},
        )

        # THEN
        expected_sqlstr = f"""INSERT INTO {dst_tablename} (name, age)
SELECT name, MAX(age)
FROM {src_tablename}
WHERE error_message IS NULL
GROUP BY name
;
"""
        print(f"     {gen_sqlstr=}")
        print(f"{expected_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_is_stageable_ReturnsObj_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        hair_str = "hair"
        x_table1 = "side1"
        src_columns = ["id", "name", "age", "email", hair_str]
        create_table_from_columns(cursor, x_table1, src_columns, {})
        x_table2 = "side2"
        dst_columns = ["name", "age", hair_str]
        create_table_from_columns(cursor, x_table2, dst_columns, {})

        # WHEN / THEN
        assert is_stageable(cursor, x_table1, {"name", "email"})
        assert is_stageable(cursor, x_table1, {"name", "address"}) is False
        assert is_stageable(cursor, x_table2, {"name", "email"}) is False
        assert is_stageable(cursor, x_table2, {"name"})
