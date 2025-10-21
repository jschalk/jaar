from pytest import raises as pytest_raises
from sqlite3 import (
    Connection as sqlite3_Connection,
    connect as sqlite3_connect,
    sqlite_version as sqlite3_sqlite_version,
)
from src.ch01_py.db_toolbox import (
    RowData,
    _get_grouping_groupby_clause,
    _get_grouping_select_clause,
    _get_having_equal_value_clause,
    create_insert_query,
    create_select_inconsistency_query,
    create_select_query,
    create_table2table_agg_insert_query,
    create_table_from_columns,
    create_table_from_csv,
    create_type_reference_insert_sqlstr,
    create_update_inconsistency_error_query,
    db_table_exists,
    dict_factory,
    get_db_tables,
    get_groupby_sql_query,
    get_grouping_with_all_values_equal_sql_query,
    get_rowdata,
    get_table_columns,
    insert_csv,
    required_columns_exist,
    rowdata_shop,
    sqlite_obj_str,
)
from src.ch01_py.file_toolbox import create_path, delete_dir, set_dir
from src.ch01_py.test._util.ch01_env import get_temp_dir, temp_dir_setup


def test_sqlite_obj_str_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert sqlite_obj_str(True, sqlite_datatype="TEXT") == "'TRUE'"
    assert sqlite_obj_str(False, sqlite_datatype="TEXT") == "'FALSE'"
    assert sqlite_obj_str(True, sqlite_datatype="INTEGER") == "1"
    assert sqlite_obj_str(False, sqlite_datatype="INTEGER") == "0"
    assert sqlite_obj_str("yea", sqlite_datatype="TEXT") == "'yea'"
    assert sqlite_obj_str(2, sqlite_datatype="TEXT") == "'2'"
    assert sqlite_obj_str(1, sqlite_datatype="TEXT") == "'1'"
    assert sqlite_obj_str(0, sqlite_datatype="TEXT") == "'0'"
    assert sqlite_obj_str(None, sqlite_datatype="TEXT") == "NULL"
    assert sqlite_obj_str(12.5, sqlite_datatype="INTEGER") == "12"
    assert sqlite_obj_str(12.5, sqlite_datatype="REAL") == "12.5"
    assert sqlite_obj_str(None, sqlite_datatype="REAL") == "NULL"


def test_sqlite_create_type_reference_insert_sqlstr_ReturnsObj_Scenario0_WithoutNones():
    # ESTABLISH
    x_table = "kubo_casas"
    eagle_id_str = "eagle_id"
    casa_id_str = "casa_id"
    casa_color_str = "casa_color"
    x_columns = [eagle_id_str, casa_id_str, casa_color_str]
    eagle_id_value = 47
    casa_id_value = "TR34"
    casa_color_value = "red"
    x_values = [eagle_id_value, casa_id_value, casa_color_value]

    # WHEN
    gen_sqlstr = create_type_reference_insert_sqlstr(x_table, x_columns, x_values)

    # THEN
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {eagle_id_str}
, {casa_id_str}
, {casa_color_str}
)
VALUES (
  {eagle_id_value}
, '{casa_id_value}'
, '{casa_color_value}'
)
;"""
    print(example_sqlstr)
    assert example_sqlstr == gen_sqlstr


def test_sqlite_create_type_reference_insert_sqlstr_ReturnsObj_Scenario1_WithNones():
    # ESTABLISH
    x_table = "kubo_casas"
    eagle_id_str = "eagle_id"
    casa_id_str = "casa_id"
    casa_color_str = "casa_color"
    x_columns = [eagle_id_str, casa_id_str, casa_color_str]
    eagle_id_value = 47.0
    casa_id_value = 34
    x_values = [eagle_id_value, casa_id_value, None]

    # WHEN
    gen_sqlstr = create_type_reference_insert_sqlstr(x_table, x_columns, x_values)

    # THEN
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {eagle_id_str}
, {casa_id_str}
, {casa_color_str}
)
VALUES (
  {eagle_id_value}
, {casa_id_value}
, NULL
)
;"""
    print(example_sqlstr)
    assert example_sqlstr == gen_sqlstr


def test_RowData_Exists():
    # ESTABLISH / WHEN
    x_rowdata = RowData()

    # THEN
    assert x_rowdata
    assert x_rowdata.tablename is None
    assert x_rowdata.row_dict is None


def test_rowdata_shop_ReturnsObj():  # sourcery skip: extract-duplicate-method
    # ESTABLISH
    x_tablename = "earth"
    with sqlite3_connect(":memory:") as conn:
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
    with sqlite3_connect(":memory:") as conn:
        conn.row_factory = None
        res = conn.execute("SELECT 'Earth' AS name, 6378 AS radius")
        row = res.fetchone()
        print(f"{row=}")
        print(f"{type(row)=}")

    with pytest_raises(Exception) as excinfo:
        rowdata_shop(x_tablename, row)
    assert str(excinfo.value) == "row_dict is not dictionary"


def test_rowdata_shop_ReturnsObjWithoutNone():  # sourcery skip: extract-method
    # ESTABLISH
    x_tablename = "earth"
    with sqlite3_connect(":memory:") as conn:
        conn.row_factory = dict_factory
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
    with sqlite3_connect(":memory:") as conn:
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
    fay_str = "Fay"
    bob_str = "Bob"
    x_groupby_columns = [fay_str, bob_str]
    x_value_columns = []

    # WHEN
    x_select_clause = _get_grouping_select_clause(x_groupby_columns, x_value_columns)

    # THEN
    assert x_select_clause == f"SELECT {fay_str}, {bob_str}"


def test_get_groupby_select_clause_ReturnsObj_Scenario2():
    # ESTABLISH
    fay_str = "Fay"
    bob_str = "Bob"
    swim_str = "swim"
    run_str = "run"
    x_groupby_columns = [fay_str, bob_str]
    x_value_columns = [swim_str, run_str]

    # WHEN
    gen_select_clause = _get_grouping_select_clause(x_groupby_columns, x_value_columns)

    # THEN
    example_str = f"SELECT {fay_str}, {bob_str}, MAX({swim_str}) AS {swim_str}, MAX({run_str}) AS {run_str}"
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
    fay_str = "Fay"
    bob_str = "Bob"
    x_groupby_columns = [fay_str, bob_str]

    # WHEN
    x_select_clause = _get_grouping_groupby_clause(x_groupby_columns)

    # THEN
    assert x_select_clause == f"GROUP BY {fay_str}, {bob_str}"


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
    fay_str = "Fay"
    bob_str = "Bob"
    swim_str = "swim"
    run_str = "run"
    x_groupby_columns = [fay_str, bob_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "Fayyboby"

    # WHEN
    gen_select_clause = get_groupby_sql_query(
        x_table_name, x_groupby_columns, x_value_columns
    )

    # THEN
    example_str = f"""{_get_grouping_select_clause(x_groupby_columns, x_value_columns)} FROM {x_table_name} GROUP BY {fay_str}, {bob_str}"""
    assert gen_select_clause == example_str


def test_get_groupby_sql_query_ReturnsObj_Scenario1_IncludeWhereClause():
    # ESTABLISH
    fay_str = "Fay"
    bob_str = "Bob"
    swim_str = "swim"
    run_str = "run"
    x_groupby_columns = [fay_str, bob_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "Fayyboby"
    where_clause_str = "WHERE error_holder_col IS NULL"

    # WHEN
    gen_select_clause = get_groupby_sql_query(
        x_table_name, x_groupby_columns, x_value_columns, where_clause_str
    )

    # THEN
    example_str = f"""{_get_grouping_select_clause(x_groupby_columns, x_value_columns)} FROM {x_table_name} WHERE error_holder_col IS NULL GROUP BY {fay_str}, {bob_str}"""
    assert gen_select_clause == example_str


def test_get_grouping_with_all_values_equal_sql_query_ReturnsObj_Scenario0():
    # ESTABLISH
    fay_str = "Fay"
    bob_str = "Bob"
    swim_str = "swim"
    run_str = "run"
    x_groupby_columns = [fay_str, bob_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "Fayyboby"

    # WHEN
    gen_select_clause = get_grouping_with_all_values_equal_sql_query(
        x_table_name, x_groupby_columns, x_value_columns
    )

    # THEN
    example_str = f"""{get_groupby_sql_query(x_table_name, x_groupby_columns, x_value_columns)} HAVING MIN({swim_str}) = MAX({swim_str}) AND MIN({run_str}) = MAX({run_str})"""
    assert gen_select_clause == example_str


def test_get_grouping_with_all_values_equal_sql_query_ReturnsObj_Scenario1_IncludeWhereClause():
    # ESTABLISH
    fay_str = "Fay"
    bob_str = "Bob"
    swim_str = "swim"
    run_str = "run"
    x_groupby_columns = [fay_str, bob_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "Fayyboby"
    where_clause_str = "WHERE error_holder_col IS NULL"

    # WHEN
    gen_select_clause = get_grouping_with_all_values_equal_sql_query(
        x_table_name, x_groupby_columns, x_value_columns, where_clause_str
    )

    # THEN
    example_str = f"""{get_groupby_sql_query(x_table_name, x_groupby_columns, x_value_columns, where_clause_str)} HAVING MIN({swim_str}) = MAX({swim_str}) AND MIN({run_str}) = MAX({run_str})"""
    assert gen_select_clause == example_str


def get_example_test_database11_path_literal() -> str:
    """get_temp_dir/test_database11.db"""
    return create_path(get_temp_dir(), "test_database11.db")


def get_example_test_tablename() -> str:
    return "test_table"


def save_test_csv_file():
    set_dir(get_temp_dir())
    test_csv_filepath = create_path(get_temp_dir(), "test_data.csv")
    with open(test_csv_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write("id,name,age,email\n")
        csv_file.write("1,John Doe,30,john@example.com\n")
        csv_file.write("2,Jane Smith,25,jane@example.com\n")
    return test_csv_filepath


def get_create_test_table_sqlstr():
    test_table = "test_table"
    return f"""CREATE TABLE {test_table} (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT);"""


def test_insert_csv_ChangesDBState(temp_dir_setup):
    # sourcery skip: extract-method
    """Test the insert_csv function using pytest."""
    # ESTABLISH
    test_tablename = get_example_test_tablename()
    csv_path = save_test_csv_file()
    print(f"{csv_path=}")
    with sqlite3_connect(get_example_test_database11_path_literal()) as conn:
        cursor = conn.cursor()
        cursor.execute(get_create_test_table_sqlstr())

        # WHEN Call the function to insert data from the CSV file into the database
        insert_csv(csv_path, conn, test_tablename)

        # THEN Verify the data was inserted
        cursor.execute(f"SELECT * FROM {test_tablename}")
        rows = cursor.fetchall()
        expected_data = [
            (1, "John Doe", 30, "john@example.com"),
            (2, "Jane Smith", 25, "jane@example.com"),
        ]
        assert rows == expected_data
    conn.close()


def test_insert_csv_ChangesDBState_WhenPassedCursorObj(
    temp_dir_setup,
):  # sourcery skip: extract-method
    """Test the insert_csv function using pytest."""
    # ESTABLISH
    test_tablename = get_example_test_tablename()
    csv_path = save_test_csv_file()
    with sqlite3_connect(get_example_test_database11_path_literal()) as conn:
        cursor = conn.cursor()
        cursor.execute(get_create_test_table_sqlstr())

        # WHEN
        insert_csv(csv_path, cursor, test_tablename)

        # THEN Verify the data was inserted
        cursor.execute(f"SELECT * FROM {test_tablename}")
        rows = cursor.fetchall()
        expected_data = [
            (1, "John Doe", 30, "john@example.com"),
            (2, "Jane Smith", 25, "jane@example.com"),
        ]
        assert rows == expected_data
    conn.close()


def test_insert_csv_ChangesNotCommitted(
    temp_dir_setup: tuple[sqlite3_Connection, str, str],
):
    """Test that changes are committed to the database."""
    # ESTABLISH
    test_tablename = get_example_test_tablename()
    csv_path = save_test_csv_file()

    # WHEN
    with sqlite3_connect(get_example_test_database11_path_literal()) as conn:
        cursor = conn.cursor()
        cursor.execute(get_create_test_table_sqlstr())

        insert_csv(csv_path, cursor, test_tablename)

    # THEN
    # reopen the connection to verify persistence
    test_database7_path = create_path(get_temp_dir(), "test_database7.db")
    with sqlite3_connect(test_database7_path) as conn2:
        cursor2 = conn2.cursor()
        cursor2.execute(get_create_test_table_sqlstr())

        # Verify no data committed
        cursor2.execute(f"SELECT * FROM {test_tablename}")
        rows = cursor2.fetchall()
        assert rows == []

    conn.close()
    conn2.close()


def test_create_table_from_csv_ChangesDBState(temp_dir_setup):
    # sourcery skip: extract-method
    """Test the create_table_from_csv_with_types function."""
    # ESTABLISH
    column_types = {
        "id": "INTEGER",
        "name": "TEXT",
        "age": "INTEGER",
        "email": "TEXT",
        "city": "TEXT",
    }
    new_table = "new_test_table"
    test_csv_filepath = save_test_csv_file()
    with sqlite3_connect(get_example_test_database11_path_literal()) as conn:
        cursor = conn.cursor()
        assert not db_table_exists(cursor, new_table)

        # WHEN
        create_table_from_csv(test_csv_filepath, conn, new_table, column_types)

        # THEN Verify the table was created
        cursor.execute(f"PRAGMA table_info({new_table})")
        columns = cursor.fetchall()
        expected_columns = [
            (0, "id", "INTEGER", 0, None, 0),
            (1, "name", "TEXT", 0, None, 0),
            (2, "age", "INTEGER", 0, None, 0),
            (3, "email", "TEXT", 0, None, 0),
        ]
        assert columns == expected_columns

    conn.close()


def test_create_table_from_csv_DoesNotEmptyTable(
    temp_dir_setup: tuple[sqlite3_Connection, str, str],
):  # sourcery skip: extract-method
    # ESTABLISH
    test_csv_filepath = save_test_csv_file()
    test_table = get_example_test_tablename()
    set_dir(get_temp_dir())
    with sqlite3_connect(get_example_test_database11_path_literal()) as conn:
        cursor = conn.cursor()
        cursor.execute(get_create_test_table_sqlstr())

        insert_csv(test_csv_filepath, conn, test_table)
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
    delete_dir(test_csv_filepath)

    conn.close()


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
    # ESTABLISH
    # Retrieve the SQLite version
    sqlite_version = sqlite3_sqlite_version

    # Log the version for debugging
    print(f"SQLite version being used: {sqlite_version}")

    # Check if the version meets requirements (example: 3.30.0 or later)
    # WHEN
    major, minor, patch = map(int, sqlite_version.split("."))
    sqlite_old_message = f"SQLite version is too old: {sqlite_version}"

    # THEN
    assert (major, minor, patch) >= (3, 30, 0), sqlite_old_message


def test_get_table_columns_ReturnsObj_Scenario0_TableDoesNotExist():
    # ESTABLISH
    x_tablename = "some_dark_side_table"
    with sqlite3_connect(":memory:") as conn:
        assert db_table_exists(conn, x_tablename) is False

        # WHEN / THEN
        assert get_table_columns(conn, x_tablename) == []


def test_get_table_columns_ReturnsObj_Scenario1_TableExists():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_table_sqlstr = get_create_test_table_sqlstr()
        x_tablename = get_example_test_tablename()
        print(create_table_sqlstr)
        print(x_tablename)
        cursor.execute(create_table_sqlstr)

        # WHEN / THEN
        assert get_table_columns(conn, x_tablename) == ["id", "name", "age", "email"]
        assert get_table_columns(cursor, x_tablename) == ["id", "name", "age", "email"]


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
HAVING 1=2
"""
        assert gen_sqlstr == expected_sqlstr


def test_create_select_query_ReturnsObj_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age"]
        create_table_from_columns(cursor, x_tablename, x_columns, {})
        x_select_columns = set()

        # WHEN
        gen_sqlstr = create_select_query(cursor, x_tablename, x_select_columns)

        # THEN
        expected_sqlstr = f"""SELECT id, name, age
FROM {x_tablename}

"""
        assert gen_sqlstr == expected_sqlstr


def test_create_select_query_ReturnsObj_Scenario1_WhereClauseExists():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age"]
        create_table_from_columns(cursor, x_tablename, x_columns, {})
        x_select_columns = set()
        x_where = {"name": "bob"}

        # WHEN
        gen_sqlstr = create_select_query(cursor, x_tablename, x_select_columns, x_where)

        # THEN
        expected_sqlstr = f"""SELECT id, name, age
FROM {x_tablename}
WHERE name = 'bob'
"""
        assert gen_sqlstr == expected_sqlstr


def test_create_select_query_ReturnsObj_Scenario2_WhereClauseHasAllElements():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        id_str = "id"
        name_str = "name"
        age_str = "age"
        x_columns = [id_str, name_str, age_str]
        column_types = {id_str: "INTEGER", name_str: "TEXT", age_str: "REAL"}
        create_table_from_columns(cursor, x_tablename, x_columns, column_types)
        x_select_columns = set()
        x_where = {id_str: 3, name_str: "bob", age_str: 23.5}

        # WHEN
        gen_sqlstr = create_select_query(cursor, x_tablename, x_select_columns, x_where)

        # THEN
        expected_sqlstr = f"""SELECT {id_str}, {name_str}, {age_str}
FROM {x_tablename}
WHERE {id_str} = 3
  AND {name_str} = 'bob'
  AND {age_str} = 23.5
"""
        print(f"{gen_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_select_query_ReturnsObj_Scenario3_StringIsFlat():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        id_str = "id"
        name_str = "name"
        age_str = "age"
        x_columns = [id_str, name_str, age_str]
        column_types = {id_str: "INTEGER", name_str: "TEXT", age_str: "REAL"}
        create_table_from_columns(cursor, x_tablename, x_columns, column_types)
        x_select_columns = set()
        x_where = {id_str: 3, name_str: "bob", age_str: 23.5}

        # WHEN
        gen_sqlstr = create_select_query(
            cursor, x_tablename, x_select_columns, x_where, flat_bool=True
        )

        # THEN
        expected_sqlstr = f"""SELECT {id_str}, {name_str}, {age_str} FROM {x_tablename} WHERE {id_str} = 3 AND {name_str} = 'bob' AND {age_str} = 23.5"""
        print(f"{gen_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_select_query_ReturnsObj_Scenario4_ColumnOrdering():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        id_str = "id"
        name_str = "name"
        age_str = "age"
        x_columns = [id_str, name_str, age_str]
        column_types = {id_str: "INTEGER", name_str: "TEXT", age_str: "REAL"}
        create_table_from_columns(cursor, x_tablename, x_columns, column_types)
        x_select_columns = {age_str, id_str}
        x_where = {id_str: 3, name_str: "bob", age_str: 23.5}

        # WHEN
        gen_sqlstr = create_select_query(
            cursor, x_tablename, x_select_columns, x_where, flat_bool=True
        )

        # THEN
        expected_sqlstr = f"""SELECT {id_str}, {age_str} FROM {x_tablename} WHERE {id_str} = 3 AND {name_str} = 'bob' AND {age_str} = 23.5"""
        print(f"{gen_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_select_query_ReturnsObj_Scenario4():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        id_str = "id"
        name_str = "name"
        age_str = "age"
        x_columns = [id_str, name_str, age_str]
        column_types = {id_str: "INTEGER", name_str: "TEXT", age_str: "REAL"}
        create_table_from_columns(cursor, x_tablename, x_columns, column_types)
        x_select_columns = {age_str, id_str}
        x_where = {id_str: 3, name_str: "bob", age_str: 23.5}

        # WHEN
        gen_sqlstr = create_select_query(
            cursor, x_tablename, x_select_columns, x_where, flat_bool=True
        )

        # THEN
        expected_sqlstr = f"""SELECT {id_str}, {age_str} FROM {x_tablename} WHERE {id_str} = 3 AND {name_str} = 'bob' AND {age_str} = 23.5"""
        print(f"{gen_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_insert_query_ReturnsObj_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        id_str = "id"
        name_str = "name"
        age_str = "age"
        x_columns = [id_str, name_str, age_str]
        column_types = {id_str: "INTEGER", name_str: "TEXT", age_str: "REAL"}
        create_table_from_columns(cursor, x_tablename, x_columns, column_types)
        x_insert_values = {id_str: 3, name_str: "bob", age_str: 23.5}

        # WHEN
        gen_sqlstr = create_insert_query(cursor, x_tablename, x_insert_values)

        # THEN
        expected_sqlstr = f"""INSERT INTO {x_tablename} ({id_str}, {name_str}, {age_str})
VALUES (
  3
, 'bob'
, 23.5
)
;
"""
        print(f"{gen_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_insert_query_ReturnsObj_Scenario1():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        id_str = "id"
        name_str = "name"
        age_str = "age"
        x_columns = [id_str, name_str, age_str]
        column_types = {id_str: "INTEGER", name_str: "TEXT", age_str: "REAL"}
        create_table_from_columns(cursor, x_tablename, x_columns, column_types)
        x_insert_values = {id_str: 3, name_str: "bob", age_str: 23.5}

        # WHEN
        gen_sqlstr = create_insert_query(cursor, x_tablename, x_insert_values, True)

        # THEN
        expected_sqlstr = f"""INSERT INTO {x_tablename} ({id_str}, {name_str}, {age_str})
VALUES (3, 'bob', 23.5);"""
        print(f"{gen_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_update_inconsistency_error_query_ReturnsObj_Scenario0():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age", "email", "hair"]
        x_error_holder_column = "error_holder2"
        x_error_str = "error_str2"
        create_table_from_columns(cursor, x_tablename, x_columns, {})

        # WHEN
        gen_sqlstr = create_update_inconsistency_error_query(
            cursor,
            x_tablename,
            {"id"},
            {"email"},
            x_error_holder_column,
            x_error_str,
        )

        # THEN
        expected_sqlstr = f"""WITH inconsistency_rows AS (
SELECT id
FROM dark_side
GROUP BY id
HAVING MIN(name) != MAX(name)
    OR MIN(age) != MAX(age)
    OR MIN(hair) != MAX(hair)
)
UPDATE dark_side
SET {x_error_holder_column} = '{x_error_str}'
FROM inconsistency_rows
WHERE inconsistency_rows.id = dark_side.id
;
"""
        print(f"""{gen_sqlstr=}""")
        assert gen_sqlstr == expected_sqlstr


def test_create_update_inconsistency_error_query_ReturnsObj_Scenario1():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_tablename = "dark_side"
        x_columns = ["id", "name", "age", "email", "hair"]
        x_error_holder_column = "error_holder2"
        x_error_str = "error_relevant_elements"
        create_table_from_columns(cursor, x_tablename, x_columns, {})

        # WHEN
        gen_sqlstr = create_update_inconsistency_error_query(
            cursor,
            x_tablename,
            {"id", "name"},
            {"email"},
            x_error_holder_column,
            x_error_str,
        )

        # THEN
        expected_sqlstr = f"""WITH inconsistency_rows AS (
SELECT id, name
FROM dark_side
GROUP BY id, name
HAVING MIN(age) != MAX(age)
    OR MIN(hair) != MAX(hair)
)
UPDATE dark_side
SET {x_error_holder_column} = '{x_error_str}'
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
            focus_cols={"name", "age"},
            exclude_cols={hair_str},
            where_block="WHERE error_holder IS NULL",
        )

        # THEN
        expected_sqlstr = f"""INSERT INTO {dst_tablename} (name, age, email)
SELECT name, age, MAX(email)
FROM {src_tablename}
WHERE error_holder IS NULL
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
            focus_cols={"name"},
            exclude_cols={hair_str},
            where_block="WHERE error_holder IS NULL",
        )

        # THEN
        expected_sqlstr = f"""INSERT INTO {dst_tablename} (name, age)
SELECT name, MAX(age)
FROM {src_tablename}
WHERE error_holder IS NULL
GROUP BY name
;
"""
        print(f"     {gen_sqlstr=}")
        print(f"{expected_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_table2table_agg_insert_query_ReturnsObj_Scenario3():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        hair_str = "hair"
        email_str = "email"
        age_str = "age"
        style_str = "style"
        src_tablename = "side1"
        src_columns = ["id", "name", age_str, style_str, email_str, hair_str]
        create_table_from_columns(cursor, src_tablename, src_columns, {})
        dst_tablename = "side2"
        dst_columns = ["name", age_str, style_str, hair_str]
        create_table_from_columns(cursor, dst_tablename, dst_columns, {})

        # WHEN
        gen_sqlstr = create_table2table_agg_insert_query(
            cursor,
            dst_table=dst_tablename,
            src_table=src_tablename,
            focus_cols={style_str, "name"},
            exclude_cols={age_str},
            where_block="WHERE error_holder IS NULL",
        )

        # THEN
        expected_sqlstr = f"""INSERT INTO {dst_tablename} (name, style, hair)
SELECT name, style, MAX(hair)
FROM {src_tablename}
WHERE error_holder IS NULL
GROUP BY name, style
;
"""
        print(f"     {gen_sqlstr=}")
        print(f"{expected_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_table2table_agg_insert_query_ReturnsObj_Scenario4():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        hair_str = "hair"
        email_str = "email"
        age_str = "age"
        style_str = "style"
        src_tablename = "side1"
        src_columns = ["id", "name", age_str, style_str, email_str, hair_str]
        create_table_from_columns(cursor, src_tablename, src_columns, {})
        dst_tablename = "side2"
        dst_columns = ["name", age_str, style_str, hair_str]
        create_table_from_columns(cursor, dst_tablename, dst_columns, {})

        # WHEN
        gen_sqlstr = create_table2table_agg_insert_query(
            cursor,
            dst_table=dst_tablename,
            src_table=src_tablename,
            focus_cols={style_str, "name"},
            exclude_cols={age_str},
            where_block="",
        )

        # THEN
        expected_sqlstr = f"""INSERT INTO {dst_tablename} (name, style, hair)
SELECT name, style, MAX(hair)
FROM {src_tablename}
GROUP BY name, style
;
"""
        print(f"     {gen_sqlstr=}")
        print(f"{expected_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_create_table2table_agg_insert_query_ReturnsObj_Scenario5():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        hair_str = "hair"
        email_str = "email"
        age_str = "age"
        style_str = "style"
        src_tablename = "side1"
        src_columns = ["id", "name", age_str, style_str, email_str, hair_str]
        create_table_from_columns(cursor, src_tablename, src_columns, {})
        dst_tablename = "side2"
        dst_columns = ["name", age_str, style_str, hair_str]
        create_table_from_columns(cursor, dst_tablename, dst_columns, {})

        # WHEN
        gen_sqlstr = create_table2table_agg_insert_query(
            cursor,
            dst_table=dst_tablename,
            src_table=src_tablename,
            focus_cols=None,
            exclude_cols={"id"},
            where_block="",
        )

        # THEN
        expected_sqlstr = f"""INSERT INTO {dst_tablename} (name, age, style, hair)
SELECT name, age, style, hair
FROM {src_tablename}
GROUP BY name, age, style, hair
;
"""
        print(f"     {gen_sqlstr=}")
        print(f"{expected_sqlstr=}")
        assert gen_sqlstr == expected_sqlstr


def test_required_columns_exist_ReturnsObj_Scenario0():
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
        assert required_columns_exist(cursor, x_table1, {"name", "email"})
        assert required_columns_exist(cursor, x_table1, {"name", "address"}) is False
        assert required_columns_exist(cursor, x_table2, {"name", "email"}) is False
        assert required_columns_exist(cursor, x_table2, {"name"})


def test_get_db_tables_ReturnsObj_Scenario0_AllTablenames():
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
        assert get_db_tables(cursor) == {x_table1: 1, x_table2: 1}


def test_get_db_tables_ReturnsObj_Scenario1_TablenamesContainsString():
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
        assert get_db_tables(cursor, "2") == {x_table2: 1}


def test_get_db_tables_ReturnsObj_Scenario1_TablenamesStartWithString():
    # ESTABLISH
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        x_table1 = "side1"
        x_table2 = "side2"
        x_table3 = "run2"
        create_table_from_columns(cursor, x_table1, ["id", "age"], {})
        create_table_from_columns(cursor, x_table2, ["id", "age"], {})
        create_table_from_columns(cursor, x_table3, ["id", "age"], {})

        # WHEN / THEN
        assert get_db_tables(cursor, "2") == {x_table2: 1, x_table3: 1}
        assert get_db_tables(cursor, "2", "side") == {x_table2: 1}
