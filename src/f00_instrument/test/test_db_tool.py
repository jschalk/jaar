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
    get_consistent_values_sql_query,
    get_groupby_sql_query,
)
from pytest import raises as pytest_raises


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


def test_get_consistent_values_sql_query_ReturnsObj_Scenario0():
    # ESTABLISH
    fizz_str = "fizz"
    buzz_str = "buzz"
    swim_str = "swim"
    run_str = "run"
    x_group_by_columns = [fizz_str, buzz_str]
    x_value_columns = [swim_str, run_str]
    x_table_name = "fizzybuzzy"

    # WHEN
    gen_select_clause = get_consistent_values_sql_query(
        x_table_name, x_group_by_columns, x_value_columns
    )

    # THEN
    example_str = f"""{get_groupby_sql_query(x_table_name, x_group_by_columns, x_value_columns)} HAVING MIN({swim_str}) = MAX({swim_str}) AND MIN({run_str}) = MAX({run_str})"""
    assert gen_select_clause == example_str
