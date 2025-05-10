from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
)
from src.a16_pidgin_logic.pidgin_config import get_pidgin_dimens
from src.a17_idea_logic._utils.str_a17 import idea_category_str, idea_number_str
from src.a17_idea_logic.idea_config import get_idea_sqlite_types, get_idea_config_dict
from src.a17_idea_logic.idea_db_tool import get_default_sorted_list
from src.a18_etl_toolbox.tran_sqlstrs import (
    get_dimen_abbv7,
    get_pidgin_prime_create_table_sqlstrs,
    create_pidgin_prime_tables,
)
from sqlite3 import connect as sqlite3_connect


def test_get_pidgin_prime_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_pidgin_prime_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "pidgin"
    }
    sqlite_types = get_idea_sqlite_types()
    for x_dimen in idea_config:
        # print(f"{x_dimen} checking...")
        x_config = idea_config.get(x_dimen)

        raw_table = f"{x_dimen}_raw"
        raw_cols = set(x_config.get("jkeys").keys())
        raw_cols.update(set(x_config.get("jvalues").keys()))
        raw_cols.add("idea_number")
        raw_cols.add("error_message")
        raw_cols = get_default_sorted_list(raw_cols)
        ex_raw_sqlstr = get_create_table_sqlstr(raw_table, raw_cols, sqlite_types)
        raw_create_sqlstr = create_table_sqlstrs.get(raw_table)
        assert raw_create_sqlstr == ex_raw_sqlstr

        agg_table = f"{x_dimen}_agg"
        agg_cols = set(x_config.get("jkeys").keys())
        agg_cols.update(set(x_config.get("jvalues").keys()))
        agg_cols = get_default_sorted_list(agg_cols)
        ex_agg_sqlstr = get_create_table_sqlstr(agg_table, agg_cols, sqlite_types)
        agg_create_sqlstr = create_table_sqlstrs.get(agg_table)
        assert agg_create_sqlstr == ex_agg_sqlstr

        # abbv7 = get_dimen_abbv7(x_dimen)
        # print(f'CREATE_{abbv7.upper()}_RAW_SQLSTR= """{ex_raw_sqlstr}"""')
        # print(f'CREATE_{abbv7.upper()}_AGG_SQLSTR= """{ex_agg_sqlstr}"""')
        # print(f'"{raw_table}": CREATE_{raw_table.upper()}_SQLSTR,')
        # print(f'"{agg_table}": CREATE_{agg_table.upper()}_SQLSTR,')


def test_get_pidgin_prime_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    pidgin_create_table_sqlstrs = get_pidgin_prime_create_table_sqlstrs()

    # THEN
    assert pidgin_create_table_sqlstrs
    bud_dimens = get_pidgin_dimens()
    expected_bud_tablenames = {f"{x_dimen}_agg" for x_dimen in bud_dimens}
    expected_bud_tablenames.update({f"{x_dimen}_raw" for x_dimen in bud_dimens})
    print(f"{expected_bud_tablenames=}")
    assert set(pidgin_create_table_sqlstrs.keys()) == expected_bud_tablenames


def test_create_pidgin_prime_tables_CreatesPidginPrimeTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fisc_db_conn:
        pidname_raw_table = "pidgin_label_raw"
        pidname_agg_table = "pidgin_label_agg"
        pidtagg_raw_table = "pidgin_name_raw"
        pidtagg_agg_table = "pidgin_name_agg"
        pidroad_raw_table = "pidgin_road_raw"
        pidroad_agg_table = "pidgin_road_agg"
        pidlabe_raw_table = "pidgin_tag_raw"
        pidlabe_agg_table = "pidgin_tag_agg"
        cursor = fisc_db_conn.cursor()
        assert not db_table_exists(cursor, pidname_raw_table)
        assert not db_table_exists(cursor, pidname_agg_table)
        assert not db_table_exists(cursor, pidtagg_raw_table)
        assert not db_table_exists(cursor, pidtagg_agg_table)
        assert not db_table_exists(cursor, pidroad_raw_table)
        assert not db_table_exists(cursor, pidroad_agg_table)
        assert not db_table_exists(cursor, pidlabe_raw_table)
        assert not db_table_exists(cursor, pidlabe_agg_table)

        # WHEN
        create_pidgin_prime_tables(cursor)

        # THEN
        assert db_table_exists(cursor, pidname_raw_table)
        assert db_table_exists(cursor, pidname_agg_table)
        assert db_table_exists(cursor, pidtagg_raw_table)
        assert db_table_exists(cursor, pidtagg_agg_table)
        assert db_table_exists(cursor, pidroad_raw_table)
        assert db_table_exists(cursor, pidroad_agg_table)
        assert db_table_exists(cursor, pidlabe_raw_table)
        assert db_table_exists(cursor, pidlabe_agg_table)

        pidname_raw_columns = get_table_columns(cursor, pidname_raw_table)
        pidname_agg_columns = get_table_columns(cursor, pidname_agg_table)
        pidtagg_raw_columns = get_table_columns(cursor, pidtagg_raw_table)
        pidtagg_agg_columns = get_table_columns(cursor, pidtagg_agg_table)
        pidroad_raw_columns = get_table_columns(cursor, pidroad_raw_table)
        pidroad_agg_columns = get_table_columns(cursor, pidroad_agg_table)
        pidlabe_raw_columns = get_table_columns(cursor, pidlabe_raw_table)
        pidlabe_agg_columns = get_table_columns(cursor, pidlabe_agg_table)

        print(f"{pidname_raw_columns=}")
        print(f"{pidname_agg_columns=}")
        assert "error_message" in pidname_raw_columns
        assert "error_message" not in pidname_agg_columns
        assert "error_message" in pidtagg_raw_columns
        assert "error_message" not in pidtagg_agg_columns
        assert "error_message" in pidroad_raw_columns
        assert "error_message" not in pidroad_agg_columns
        assert "error_message" in pidlabe_raw_columns
        assert "error_message" not in pidlabe_agg_columns
        assert idea_number_str() in pidname_raw_columns
        assert idea_number_str() not in pidname_agg_columns
        assert idea_number_str() in pidtagg_raw_columns
        assert idea_number_str() not in pidtagg_agg_columns
        assert idea_number_str() in pidroad_raw_columns
        assert idea_number_str() not in pidroad_agg_columns
        assert idea_number_str() in pidlabe_raw_columns
        assert idea_number_str() not in pidlabe_agg_columns
        assert len(pidname_raw_columns) == 9
        assert len(pidname_agg_columns) == 7
        assert len(pidtagg_raw_columns) == 9
        assert len(pidtagg_agg_columns) == 7
        assert len(pidroad_raw_columns) == 9
        assert len(pidroad_agg_columns) == 7
        assert len(pidlabe_raw_columns) == 9
        assert len(pidlabe_agg_columns) == 7
