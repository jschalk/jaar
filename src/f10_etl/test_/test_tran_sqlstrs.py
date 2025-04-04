from src.f00_instrument.db_toolbox import (
    db_table_exists,
    create_select_inconsistency_query,
    create_update_inconsistency_error_query,
    get_create_table_sqlstr,
    create_table2table_agg_insert_query,
    get_table_columns,
    is_stageable,
)
from src.f01_road.deal import fisc_title_str
from src.f02_bud.bud_tool import budunit_str
from src.f04_vow.atom_config import (
    event_int_str,
    face_name_str,
    get_bud_dimens,
    get_delete_key_name,
)
from src.f07_fisc.fisc_config import fiscunit_str, get_fisc_dimens
from src.f09_idea.idea_config import (
    idea_number_str,
    get_idea_sqlite_types,
    get_idea_config_dict,
    idea_category_str,
    get_idea_numbers,
)
from src.f09_idea.idea_db_tool import (
    get_pragma_table_fetchall,
    get_custom_sorted_list,
    get_idea_into_dimen_staging_query,
)
from src.f10_etl.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
)
from src.f10_etl.tran_sqlstrs import (
    get_fisc_create_table_sqlstrs,
    get_bud_create_table_sqlstrs,
    create_fisc_tables,
    create_bud_tables,
    create_all_idea_tables,
    get_bud_inconsistency_sqlstrs,
    get_fisc_inconsistency_sqlstrs,
    get_bud_put_update_inconsist_error_message_sqlstrs,
    get_fisc_update_inconsist_error_message_sqlstrs,
    get_bud_insert_put_agg_from_staging_sqlstrs,
    get_bud_insert_del_agg_from_staging_sqlstrs,
    get_fisc_insert_agg_from_staging_sqlstrs,
    FISCUNIT_AGG_INSERT_SQLSTR,
    IDEA_STAGEABLE_PUT_DIMENS,
    IDEA_STAGEABLE_DEL_DIMENS,
    CREATE_FISC_EVENT_TIME_AGG_SQLSTR,
    INSERT_FISC_EVENT_TIME_AGG_SQLSTR,
    UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR,
    CREATE_FISC_OTE1_AGG_SQLSTR,
    INSERT_FISC_OTE1_AGG_SQLSTR,
    get_fisc_fu1_select_sqlstrs,
    # get_bud_bu1_select_sqlstrs,
)
from sqlite3 import connect as sqlite3_connect


def abbv(tablename: str) -> str:
    abbrevions = {
        "bud_acct_membership_put_agg": "BUDMEMB_PUT_AGG",
        "bud_acct_membership_put_staging": "BUDMEMB_PUT_STAGING",
        "bud_acctunit_put_agg": "BUDACCT_PUT_AGG",
        "bud_acctunit_put_staging": "BUDACCT_PUT_STAGING",
        "bud_item_awardlink_put_agg": "BUDAWAR_PUT_AGG",
        "bud_item_awardlink_put_staging": "BUDAWAR_PUT_STAGING",
        "bud_item_factunit_put_agg": "BUDFACT_PUT_AGG",
        "bud_item_factunit_put_staging": "BUDFACT_PUT_STAGING",
        "bud_item_healerlink_put_agg": "BUDHEAL_PUT_AGG",
        "bud_item_healerlink_put_staging": "BUDHEAL_PUT_STAGING",
        "bud_item_reason_premiseunit_put_agg": "BUDPREM_PUT_AGG",
        "bud_item_reason_premiseunit_put_staging": "BUDPREM_PUT_STAGING",
        "bud_item_reasonunit_put_agg": "BUDREAS_PUT_AGG",
        "bud_item_reasonunit_put_staging": "BUDREAS_PUT_STAGING",
        "bud_item_teamlink_put_agg": "BUDTEAM_PUT_AGG",
        "bud_item_teamlink_put_staging": "BUDTEAM_PUT_STAGING",
        "bud_itemunit_put_agg": "BUDITEM_PUT_AGG",
        "bud_itemunit_put_staging": "BUDITEM_PUT_STAGING",
        "budunit_put_agg": "BUDUNIT_PUT_AGG",
        "budunit_put_staging": "BUDUNIT_PUT_STAGING",
        "bud_acct_membership_del_agg": "BUDMEMB_DEL_AGG",
        "bud_acct_membership_del_staging": "BUDMEMB_DEL_STAGING",
        "bud_acctunit_del_agg": "BUDACCT_DEL_AGG",
        "bud_acctunit_del_staging": "BUDACCT_DEL_STAGING",
        "bud_item_awardlink_del_agg": "BUDAWAR_DEL_AGG",
        "bud_item_awardlink_del_staging": "BUDAWAR_DEL_STAGING",
        "bud_item_factunit_del_agg": "BUDFACT_DEL_AGG",
        "bud_item_factunit_del_staging": "BUDFACT_DEL_STAGING",
        "bud_item_healerlink_del_agg": "BUDHEAL_DEL_AGG",
        "bud_item_healerlink_del_staging": "BUDHEAL_DEL_STAGING",
        "bud_item_reason_premiseunit_del_agg": "BUDPREM_DEL_AGG",
        "bud_item_reason_premiseunit_del_staging": "BUDPREM_DEL_STAGING",
        "bud_item_reasonunit_del_agg": "BUDREAS_DEL_AGG",
        "bud_item_reasonunit_del_staging": "BUDREAS_DEL_STAGING",
        "bud_item_teamlink_del_agg": "BUDTEAM_DEL_AGG",
        "bud_item_teamlink_del_staging": "BUDTEAM_DEL_STAGING",
        "bud_itemunit_del_agg": "BUDITEM_DEL_AGG",
        "bud_itemunit_del_staging": "BUDITEM_DEL_STAGING",
        "budunit_del_agg": "BUDUNIT_DEL_AGG",
        "budunit_del_staging": "BUDUNIT_DEL_STAGING",
    }
    return abbrevions.get(tablename)


def test_get_fisc_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_fisc_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "fisc"
    }
    sqlite_types = get_idea_sqlite_types()
    for x_dimen in idea_config:
        # print(f"{x_dimen} checking...")
        x_config = idea_config.get(x_dimen)

        ag_table = f"{x_dimen}_agg"
        ag_sqlstr = create_table_sqlstrs.get(ag_table)
        ag_cols = set(x_config.get("jkeys").keys())
        ag_cols.update(set(x_config.get("jvalues").keys()))
        ag_cols.remove(event_int_str())
        ag_cols.remove(face_name_str())
        ag_cols = get_custom_sorted_list(ag_cols)
        print(f"{ag_cols=}")
        gen_dimen_agg_sqlstr = get_create_table_sqlstr(ag_table, ag_cols, sqlite_types)
        assert ag_sqlstr == gen_dimen_agg_sqlstr

        st_table = f"{x_dimen}_staging"
        st_sqlstr = create_table_sqlstrs.get(st_table)
        st_cols = set(x_config.get("jkeys").keys())
        st_cols.update(set(x_config.get("jvalues").keys()))
        st_cols.add(idea_number_str())
        st_cols.add("error_message")
        st_cols = get_custom_sorted_list(st_cols)
        gen_dimen_stage_sqlstr = get_create_table_sqlstr(
            st_table, st_cols, sqlite_types
        )
        assert st_sqlstr == gen_dimen_stage_sqlstr

        # print(f'{ag_table.upper()}_SQLSTR= """{gen_dimen_agg_sqlstr}"""')
        # print(f'{st_table.upper()}_SQLSTR= """{gen_dimen_stage_sqlstr}"""')
        # print(f'"{ag_table}": {ag_table.upper()}_SQLSTR,')
        # print(f'"{st_table}": {st_table.upper()}_SQLSTR,')


def test_get_bud_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_bud_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "bud"
    }
    s_types = get_idea_sqlite_types()
    for x_dimen in idea_config:
        print(f"{x_dimen} checking...")
        x_config = idea_config.get(x_dimen)

        ag_put_table = f"{x_dimen}_put_agg"
        ag_put_cols = set(x_config.get("jkeys").keys())
        ag_put_cols.update(set(x_config.get("jvalues").keys()))
        ag_put_cols = get_custom_sorted_list(ag_put_cols)
        ex_ag_put_sqlstr = get_create_table_sqlstr(ag_put_table, ag_put_cols, s_types)
        assert create_table_sqlstrs.get(ag_put_table) == ex_ag_put_sqlstr

        st_put_table = f"{x_dimen}_put_staging"
        st_put_cols = set(x_config.get("jkeys").keys())
        st_put_cols.update(set(x_config.get("jvalues").keys()))
        st_put_cols.add(idea_number_str())
        st_put_cols.add("error_message")
        st_put_cols = get_custom_sorted_list(st_put_cols)
        ex_st_put_sqlstr = get_create_table_sqlstr(st_put_table, st_put_cols, s_types)
        assert create_table_sqlstrs.get(st_put_table) == ex_st_put_sqlstr

        ag_del_table = f"{x_dimen}_del_agg"
        ag_del_cols = set(x_config.get("jkeys").keys())
        ag_del_cols = get_custom_sorted_list(ag_del_cols)
        ag_del_cols[-1] = get_delete_key_name(ag_del_cols[-1])
        ex_ag_del_sqlstr = get_create_table_sqlstr(ag_del_table, ag_del_cols, s_types)
        # print(f" {ex_ag_del_sqlstr}")
        assert create_table_sqlstrs.get(ag_del_table) == ex_ag_del_sqlstr

        st_del_table = f"{x_dimen}_del_staging"
        st_del_cols = set(x_config.get("jkeys").keys())
        st_del_cols.add(idea_number_str())
        st_del_cols.add("error_message")
        st_del_cols = get_custom_sorted_list(st_del_cols)
        st_del_cols[-2] = get_delete_key_name(st_del_cols[-2])
        ex_st_del_sqlstr = get_create_table_sqlstr(st_del_table, st_del_cols, s_types)
        # print(f" {ex_st_del_sqlstr}")
        assert create_table_sqlstrs.get(st_del_table) == ex_st_del_sqlstr

        # print(f'CREATE_{abbv(ag_put_table)}_SQLSTR= """{ex_ag_put_sqlstr}"""')
        # print(f'CREATE_{abbv(st_put_table)}_SQLSTR= """{ex_st_put_sqlstr}"""')
        # print(f'CREATE_{abbv(ag_del_table)}_SQLSTR= """{ex_ag_del_sqlstr}"""')
        # print(f'CREATE_{abbv(st_del_table)}_SQLSTR= """{ex_st_del_sqlstr}"""')
        # print(f'"{ag_put_table}": CREATE_{abbv(ag_put_table)}_SQLSTR,')
        # print(f'"{st_put_table}": CREATE_{abbv(st_put_table)}_SQLSTR,')
        # print(f'"{ag_del_table}": CREATE_{abbv(ag_del_table)}_SQLSTR,')
        # print(f'"{st_del_table}": CREATE_{abbv(st_del_table)}_SQLSTR,')


def test_get_fisc_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    fisc_create_table_sqlstrs = get_fisc_create_table_sqlstrs()

    # THEN
    assert fisc_create_table_sqlstrs
    fisc_dimens = get_fisc_dimens()
    expected_fisc_tablenames = {f"{x_dimen}_agg" for x_dimen in fisc_dimens}
    expected_fisc_tablenames.update({f"{x_dimen}_staging" for x_dimen in fisc_dimens})
    print(f"{expected_fisc_tablenames=}")
    assert set(fisc_create_table_sqlstrs.keys()) == expected_fisc_tablenames


def test_get_bud_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    bud_create_table_sqlstrs = get_bud_create_table_sqlstrs()

    # THEN
    assert bud_create_table_sqlstrs
    bud_dimens = get_bud_dimens()
    expected_bud_tablenames = {f"{x_dimen}_put_agg" for x_dimen in bud_dimens}
    expected_bud_tablenames.update({f"{x_dimen}_put_staging" for x_dimen in bud_dimens})
    expected_bud_tablenames.update({f"{x_dimen}_del_agg" for x_dimen in bud_dimens})
    expected_bud_tablenames.update({f"{x_dimen}_del_staging" for x_dimen in bud_dimens})
    print(f"{expected_bud_tablenames=}")
    assert set(bud_create_table_sqlstrs.keys()) == expected_bud_tablenames


def test_create_all_idea_tables_CreatesFiscStagingTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    idea_numbers = get_idea_numbers()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        for idea_number in idea_numbers:
            assert db_table_exists(cursor, f"{idea_number}_staging") is False

        # WHEN
        create_all_idea_tables(cursor)

        # THEN
        for idea_number in idea_numbers:
            print(f"{idea_number} checking...")
            assert db_table_exists(cursor, f"{idea_number}_staging")


def test_create_bud_tables_CreatesFiscStagingTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0
        assert db_table_exists(cursor, "bud_acct_membership_put_agg") is False
        assert db_table_exists(cursor, "bud_acct_membership_put_staging") is False
        assert db_table_exists(cursor, "bud_acctunit_put_agg") is False
        assert db_table_exists(cursor, "bud_acctunit_put_staging") is False
        assert db_table_exists(cursor, "bud_item_awardlink_put_agg") is False
        assert db_table_exists(cursor, "bud_item_awardlink_put_staging") is False
        assert db_table_exists(cursor, "bud_item_factunit_put_agg") is False
        assert db_table_exists(cursor, "bud_item_factunit_put_staging") is False
        assert db_table_exists(cursor, "bud_item_healerlink_put_agg") is False
        assert db_table_exists(cursor, "bud_item_healerlink_put_staging") is False
        assert db_table_exists(cursor, "bud_item_reason_premiseunit_put_agg") is False
        assert (
            db_table_exists(cursor, "bud_item_reason_premiseunit_put_staging") is False
        )
        assert db_table_exists(cursor, "bud_item_reasonunit_put_agg") is False
        assert db_table_exists(cursor, "bud_item_reasonunit_put_staging") is False
        assert db_table_exists(cursor, "bud_item_teamlink_put_agg") is False
        assert db_table_exists(cursor, "bud_item_teamlink_put_staging") is False
        assert db_table_exists(cursor, "bud_itemunit_put_agg") is False
        assert db_table_exists(cursor, "bud_itemunit_put_staging") is False
        assert db_table_exists(cursor, "budunit_put_agg") is False
        assert db_table_exists(cursor, "budunit_put_staging") is False

        # WHEN
        create_bud_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 40
        assert db_table_exists(cursor, "bud_acct_membership_put_agg")
        assert db_table_exists(cursor, "bud_acct_membership_put_staging")
        assert db_table_exists(cursor, "bud_acctunit_put_agg")
        assert db_table_exists(cursor, "bud_acctunit_put_staging")
        assert db_table_exists(cursor, "bud_item_awardlink_put_agg")
        assert db_table_exists(cursor, "bud_item_awardlink_put_staging")
        assert db_table_exists(cursor, "bud_item_factunit_put_agg")
        assert db_table_exists(cursor, "bud_item_factunit_put_staging")
        assert db_table_exists(cursor, "bud_item_healerlink_put_agg")
        assert db_table_exists(cursor, "bud_item_healerlink_put_staging")
        assert db_table_exists(cursor, "bud_item_reason_premiseunit_put_agg")
        assert db_table_exists(cursor, "bud_item_reason_premiseunit_put_staging")
        assert db_table_exists(cursor, "bud_item_reasonunit_put_agg")
        assert db_table_exists(cursor, "bud_item_reasonunit_put_staging")
        assert db_table_exists(cursor, "bud_item_teamlink_put_agg")
        assert db_table_exists(cursor, "bud_item_teamlink_put_staging")
        assert db_table_exists(cursor, "bud_itemunit_put_agg")
        assert db_table_exists(cursor, "bud_itemunit_put_staging")
        assert db_table_exists(cursor, "budunit_put_agg")
        assert db_table_exists(cursor, "budunit_put_staging")


def test_create_fisc_tables_CreatesFiscStagingTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        fisc_objs = FiscPrimeObjsRef()
        fisc_cols = FiscPrimeColumnsRef()
        assert db_table_exists(cursor, fisc_objs.unit_agg_tablename) is False
        assert db_table_exists(cursor, fisc_objs.deal_agg_tablename) is False
        assert db_table_exists(cursor, fisc_objs.cash_agg_tablename) is False
        assert db_table_exists(cursor, fisc_objs.hour_agg_tablename) is False
        assert db_table_exists(cursor, fisc_objs.mont_agg_tablename) is False
        assert db_table_exists(cursor, fisc_objs.week_agg_tablename) is False
        assert db_table_exists(cursor, fisc_objs.unit_stage_tablename) is False
        assert db_table_exists(cursor, fisc_objs.deal_stage_tablename) is False
        assert db_table_exists(cursor, fisc_objs.cash_stage_tablename) is False
        assert db_table_exists(cursor, fisc_objs.hour_stage_tablename) is False
        assert db_table_exists(cursor, fisc_objs.mont_stage_tablename) is False
        assert db_table_exists(cursor, fisc_objs.week_stage_tablename) is False

        # WHEN
        create_fisc_tables(cursor)

        # THEN
        assert db_table_exists(cursor, fisc_objs.unit_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.deal_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.cash_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.hour_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.mont_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.week_agg_tablename)

        assert db_table_exists(cursor, fisc_objs.unit_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.deal_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.cash_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.hour_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.mont_stage_tablename)
        assert db_table_exists(cursor, fisc_objs.week_stage_tablename)

        fisc_unit_agg_pragma = get_pragma_table_fetchall(fisc_cols.unit_agg_columns)
        fisc_deal_agg_pragma = get_pragma_table_fetchall(fisc_cols.deal_agg_columns)
        fisc_cash_agg_pragma = get_pragma_table_fetchall(fisc_cols.cash_agg_columns)
        fisc_hour_agg_pragma = get_pragma_table_fetchall(fisc_cols.hour_agg_columns)
        fisc_mont_agg_pragma = get_pragma_table_fetchall(fisc_cols.mont_agg_columns)
        fisc_week_agg_pragma = get_pragma_table_fetchall(fisc_cols.week_agg_columns)
        fisc_unit_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.unit_staging_columns
        )
        fisc_deal_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.deal_staging_columns
        )
        fisc_cash_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.cash_staging_columns
        )
        fisc_hour_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.hour_staging_columns
        )
        fisc_mont_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.mont_staging_columns
        )
        fisc_week_stage_pragma = get_pragma_table_fetchall(
            fisc_cols.week_staging_columns
        )
        cursor.execute(f"PRAGMA table_info({fisc_objs.unit_agg_tablename})")
        assert fisc_unit_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.deal_agg_tablename})")
        assert fisc_deal_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.cash_agg_tablename})")
        assert fisc_cash_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.hour_agg_tablename})")
        assert fisc_hour_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.mont_agg_tablename})")
        assert fisc_mont_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.week_agg_tablename})")
        assert fisc_week_agg_pragma == cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({fisc_objs.unit_stage_tablename})")
        assert fisc_unit_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.deal_stage_tablename})")
        assert fisc_deal_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.cash_stage_tablename})")
        assert fisc_cash_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.hour_stage_tablename})")
        assert fisc_hour_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.mont_stage_tablename})")
        assert fisc_mont_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.week_stage_tablename})")
        assert fisc_week_stage_pragma == cursor.fetchall()


def test_get_fisc_inconsistency_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    fisc_inconsistency_sqlstrs = get_fisc_inconsistency_sqlstrs()

    # THEN
    assert fisc_inconsistency_sqlstrs.keys() == get_fisc_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        # if dimen_config.get(idea_category_str()) != "pidgin"
        # if dimen_config.get(idea_category_str()) == "bud"
        if dimen_config.get(idea_category_str()) == "fisc"
    }

    exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)

        for x_dimen in sorted(idea_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = fisc_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_staging"
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_select_inconsistency_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            print(f'{x_dimen}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""')
            print(f'{x_sqlstr=}"""')
            assert x_sqlstr == generated_dimen_sqlstr


def test_get_bud_inconsistency_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_inconsistency_sqlstrs = get_bud_inconsistency_sqlstrs()

    # THEN
    assert bud_inconsistency_sqlstrs.keys() == get_bud_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "bud"
    }

    exclude_cols = {idea_number_str(), "error_message"}
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_tables(cursor)

        for x_dimen in sorted(idea_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = bud_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_put_staging"
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_select_inconsistency_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            print(
                f'{x_dimen.upper()}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""'
            )
            assert x_sqlstr == generated_dimen_sqlstr


def test_get_fisc_update_inconsist_error_message_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    fisc_update_error_sqlstrs = get_fisc_update_inconsist_error_message_sqlstrs()

    # THEN
    assert set(fisc_update_error_sqlstrs.keys()) == get_fisc_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "fisc"
    }

    exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_tables(cursor)
        create_bud_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            x_sqlstr = fisc_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_staging"
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_update_inconsistency_error_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            # print(
            #     f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
            # )
            # print(
            #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
            # )
            # print(f"""            {x_sqlstr=}""")
            assert x_sqlstr == generated_dimen_sqlstr


def test_get_bud_put_update_inconsist_error_message_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_update_error_sqlstrs = get_bud_put_update_inconsist_error_message_sqlstrs()

    # THEN
    assert set(bud_update_error_sqlstrs.keys()) == get_bud_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "bud"
    }

    exclude_cols = {idea_number_str(), "error_message"}
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            x_sqlstr = bud_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_put_staging"
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_update_inconsistency_error_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            print(
                f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
            )
            print(
                f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
            )
            print(f"""            {x_sqlstr=}""")
            assert x_sqlstr == generated_dimen_sqlstr


def test_get_fisc_insert_agg_from_staging_sqlstrs_ReturnsObj():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH / WHEN
    fisc_insert_agg_sqlstrs = get_fisc_insert_agg_from_staging_sqlstrs()

    # THEN
    assert set(fisc_insert_agg_sqlstrs.keys()) == get_fisc_dimens()
    x_exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "fisc"
    }
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns.remove(event_int_str())
            dimen_focus_columns.remove(face_name_str())
            dimen_focus_columns = get_custom_sorted_list(dimen_focus_columns)
            stage_tablename = f"{x_dimen}_staging"
            agg_tablename = f"{x_dimen}_agg"

            generated_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=stage_tablename,
                    dst_table=agg_tablename,
                    focus_cols=dimen_focus_columns,
                    exclude_cols=x_exclude_cols,
                )
            )
            x_sqlstr = fisc_insert_agg_sqlstrs.get(x_dimen)
            # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
            # print(
            #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{generated_table2table_agg_insert_sqlstr}"""'
            # )
            assert x_sqlstr == generated_table2table_agg_insert_sqlstr

        generated_fiscunit_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=f"{fiscunit_str()}_staging",
            dst_table=f"{fiscunit_str()}_agg",
            focus_cols=[fisc_title_str()],
            exclude_cols=x_exclude_cols,
        )
        assert FISCUNIT_AGG_INSERT_SQLSTR == generated_fiscunit_sqlstr
        columns_header = """fisc_title, timeline_title, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge"""
        tablename = "fiscunit"
        expected_fiscunit_sqlstr = f"""INSERT INTO {tablename}_agg ({columns_header})
SELECT fisc_title, MAX(timeline_title), MAX(c400_number), MAX(yr1_jan1_offset), MAX(monthday_distortion), MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(bridge)
FROM {tablename}_staging
WHERE error_message IS NULL
GROUP BY fisc_title
;
"""
        assert FISCUNIT_AGG_INSERT_SQLSTR == expected_fiscunit_sqlstr

    assert len(idea_config) == len(fisc_insert_agg_sqlstrs)


def test_get_bud_insert_put_agg_from_staging_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_insert_agg_sqlstrs = get_bud_insert_put_agg_from_staging_sqlstrs()

    # THEN
    assert set(bud_insert_agg_sqlstrs.keys()) == get_bud_dimens()
    x_exclude_cols = {
        idea_number_str(),
        "error_message",
    }
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "bud"
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns = get_custom_sorted_list(dimen_focus_columns)
            stage_tablename = f"{x_dimen}_put_staging"
            agg_tablename = f"{x_dimen}_put_agg"

            generated_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=stage_tablename,
                    dst_table=agg_tablename,
                    focus_cols=dimen_focus_columns,
                    exclude_cols=x_exclude_cols,
                )
            )
            x_sqlstr = bud_insert_agg_sqlstrs.get(x_dimen)
            # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
            # print(
            #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{generated_table2table_agg_insert_sqlstr}"""'
            # )
            assert x_sqlstr == generated_table2table_agg_insert_sqlstr


def test_get_bud_insert_del_agg_from_staging_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_insert_agg_sqlstrs = get_bud_insert_del_agg_from_staging_sqlstrs()

    # THEN
    assert set(bud_insert_agg_sqlstrs.keys()) == get_bud_dimens()
    x_exclude_cols = {
        idea_number_str(),
        "error_message",
    }
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "bud"
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns = get_custom_sorted_list(dimen_focus_columns)
            dimen_focus_columns[-1] = get_delete_key_name(dimen_focus_columns[-1])
            stage_tablename = f"{x_dimen}_del_staging"
            agg_tablename = f"{x_dimen}_del_agg"

            expected_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=stage_tablename,
                    dst_table=agg_tablename,
                    focus_cols=dimen_focus_columns,
                    exclude_cols=x_exclude_cols,
                )
            )
            x_sqlstr = bud_insert_agg_sqlstrs.get(x_dimen)
            # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
            # print(
            #     f'{abbv(agg_tablename)}_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
            # )
            assert x_sqlstr == expected_table2table_agg_insert_sqlstr


def test_IDEA_STAGEABLE_PUT_DIMENS_HasAll_idea_numbersForAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) != "pidgin"
        # if dimen_config.get(idea_category_str()) == "fisc"
    }
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_fisc_tables(cursor)
        create_bud_tables(cursor)

        idea_stage2dimen_count = 0
        idea_dimen_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        expected_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            dimen_config = idea_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get("jkeys").keys())
            dimen_value_columns = set(dimen_config.get("jvalues").keys())
            for idea_number in sorted_idea_numbers:
                src_columns = get_table_columns(cursor, f"{idea_number}_staging")
                expected_stagable = dimen_key_columns.issubset(src_columns)
                if idea_number == "br00050":
                    print(f"{x_dimen} {idea_number} checking... {src_columns}")
                src_tablename = f"{idea_number}_staging"
                gen_stablable = is_stageable(cursor, src_tablename, dimen_key_columns)
                assert expected_stagable == gen_stablable

                idea_dimen_combo_checked_count += 1
                if is_stageable(cursor, src_tablename, dimen_key_columns):
                    expected_idea_stagable_dimens.get(idea_number).append(x_dimen)
                    idea_stage2dimen_count += 1
                    src_cols_set = set(src_columns)
                    existing_value_col = src_cols_set.intersection(dimen_value_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    # print(
                    #     f"{idea_stage2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}, values: {existing_value_col}"
                    # )
                    generated_sqlstr = get_idea_into_dimen_staging_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sql syntax is correct?
                    assert generated_sqlstr != ""

    idea_stageable_dimen_list = sorted(list(expected_idea_stagable_dimens))
    print(f"{expected_idea_stagable_dimens=}")
    assert idea_dimen_combo_checked_count == 680
    assert idea_stage2dimen_count == 100
    assert IDEA_STAGEABLE_PUT_DIMENS == expected_idea_stagable_dimens


def test_IDEA_STAGEABLE_DEL_DIMENS_HasAll_idea_numbersForAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) != "pidgin"
        # if dimen_config.get(idea_category_str()) == "fisc"
    }
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_fisc_tables(cursor)
        create_bud_tables(cursor)

        idea_stage2dimen_count = 0
        idea_dimen_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        x_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            dimen_config = idea_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get("jkeys").keys())
            dimen_key_columns = get_custom_sorted_list(dimen_key_columns)
            dimen_key_columns[-1] = get_delete_key_name(dimen_key_columns[-1])
            dimen_key_columns = set(dimen_key_columns)
            for idea_number in sorted_idea_numbers:
                src_columns = get_table_columns(cursor, f"{idea_number}_staging")
                expected_stagable = dimen_key_columns.issubset(src_columns)
                src_tablename = f"{idea_number}_staging"
                gen_stablable = is_stageable(cursor, src_tablename, dimen_key_columns)
                assert expected_stagable == gen_stablable

                idea_dimen_combo_checked_count += 1
                if is_stageable(cursor, src_tablename, dimen_key_columns):
                    x_idea_stagable_dimens.get(idea_number).append(x_dimen)
                    idea_stage2dimen_count += 1
                    src_cols_set = set(src_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    print(
                        f"{idea_stage2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}"
                    )
                    generated_sqlstr = get_idea_into_dimen_staging_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sql syntax is correct?
                    assert generated_sqlstr != ""
    expected_idea_stagable_dimens = {
        x_idea_number: stagable_dimens
        for x_idea_number, stagable_dimens in x_idea_stagable_dimens.items()
        if stagable_dimens != []
    }
    idea_stageable_dimen_list = sorted(list(expected_idea_stagable_dimens))
    print(f"{expected_idea_stagable_dimens=}")
    assert idea_dimen_combo_checked_count == 680
    assert idea_stage2dimen_count == 10
    assert IDEA_STAGEABLE_DEL_DIMENS == expected_idea_stagable_dimens


def test_CREATE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = """
CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
  fisc_title TEXT
, event_int INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_FISC_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = """
INSERT INTO fisc_event_time_agg (fisc_title, event_int, agg_time)
SELECT fisc_title, event_int, agg_time
FROM (
    SELECT fisc_title, event_int, tran_time as agg_time
    FROM fisc_cashbook_staging
    GROUP BY fisc_title, event_int, tran_time
    UNION 
    SELECT fisc_title, event_int, deal_time as agg_time
    FROM fisc_dealunit_staging
    GROUP BY fisc_title, event_int, deal_time
)
ORDER BY fisc_title, event_int, agg_time
;
"""
    # WHEN / THEN
    assert INSERT_FISC_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


def test_UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_UPDATE_sqlstr = """
WITH EventTimeOrdered AS (
    SELECT fisc_title, event_int, agg_time,
           LAG(agg_time) OVER (PARTITION BY fisc_title ORDER BY event_int) AS prev_agg_time
    FROM fisc_event_time_agg
)
UPDATE fisc_event_time_agg
SET error_message = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.event_int = fisc_event_time_agg.event_int
    AND EventTimeOrdered.fisc_title = fisc_event_time_agg.fisc_title
    AND EventTimeOrdered.agg_time = fisc_event_time_agg.agg_time
;
"""
    # WHEN / THEN
    assert UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


def test_CREATE_FISC_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = """
CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
  fisc_title TEXT
, owner_name TEXT
, event_int INTEGER
, deal_time INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_FISC_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_FISC_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = """
INSERT INTO fisc_ote1_agg (fisc_title, owner_name, event_int, deal_time)
SELECT fisc_title, owner_name, event_int, deal_time
FROM (
    SELECT fisc_title, owner_name, event_int, deal_time
    FROM fisc_dealunit_staging
    GROUP BY fisc_title, owner_name, event_int, deal_time
)
ORDER BY fisc_title, owner_name, event_int, deal_time
;
"""
    # WHEN / THEN
    assert INSERT_FISC_OTE1_AGG_SQLSTR == expected_INSERT_sqlstr


def test_get_fisc_fu1_select_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    fu1_select_sqlstrs = get_fisc_fu1_select_sqlstrs(a23_str)

    # THEN
    assert fu1_select_sqlstrs
    expected_fu1_select_dimens = set(get_fisc_dimens())
    assert set(fu1_select_sqlstrs.keys()) == expected_fu1_select_dimens


def test_get_fisc_fu1_select_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    fu1_select_sqlstrs = get_fisc_fu1_select_sqlstrs(fisc_title=a23_str)

    # THEN
    fisccash_str = "fisc_cashbook"
    fiscdeal_str = "fisc_dealunit"
    fischour_str = "fisc_timeline_hour"
    fiscmont_str = "fisc_timeline_month"
    fiscweek_str = "fisc_timeline_weekday"
    fiscoffi_str = "fisc_timeoffi"
    fiscunit_str = "fiscunit"
    gen_fisccash_sqlstr = fu1_select_sqlstrs.get(fisccash_str)
    gen_fiscdeal_sqlstr = fu1_select_sqlstrs.get(fiscdeal_str)
    gen_fischour_sqlstr = fu1_select_sqlstrs.get(fischour_str)
    gen_fiscmont_sqlstr = fu1_select_sqlstrs.get(fiscmont_str)
    gen_fiscweek_sqlstr = fu1_select_sqlstrs.get(fiscweek_str)
    gen_fiscoffi_sqlstr = fu1_select_sqlstrs.get(fiscoffi_str)
    gen_fiscunit_sqlstr = fu1_select_sqlstrs.get(fiscunit_str)

    expected_fisccash_sqlstr = f"SELECT fisc_title, owner_name, acct_name, tran_time, amount FROM fisc_cashbook_agg WHERE fisc_title = '{a23_str}'"
    expected_fiscdeal_sqlstr = f"SELECT fisc_title, owner_name, deal_time, quota, celldepth FROM fisc_dealunit_agg WHERE fisc_title = '{a23_str}'"
    expected_fischour_sqlstr = f"SELECT fisc_title, cumlative_minute, hour_title FROM fisc_timeline_hour_agg WHERE fisc_title = '{a23_str}'"
    expected_fiscmont_sqlstr = f"SELECT fisc_title, cumlative_day, month_title FROM fisc_timeline_month_agg WHERE fisc_title = '{a23_str}'"
    expected_fiscweek_sqlstr = f"SELECT fisc_title, weekday_order, weekday_title FROM fisc_timeline_weekday_agg WHERE fisc_title = '{a23_str}'"
    expected_fiscoffi_sqlstr = f"SELECT fisc_title, offi_time FROM fisc_timeoffi_agg WHERE fisc_title = '{a23_str}'"
    expected_fiscunit_sqlstr = f"SELECT fisc_title, timeline_title, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge FROM fiscunit_agg WHERE fisc_title = '{a23_str}'"

    assert gen_fisccash_sqlstr == expected_fisccash_sqlstr
    assert gen_fiscdeal_sqlstr == expected_fiscdeal_sqlstr
    assert gen_fischour_sqlstr == expected_fischour_sqlstr
    assert gen_fiscmont_sqlstr == expected_fiscmont_sqlstr
    assert gen_fiscweek_sqlstr == expected_fiscweek_sqlstr
    assert gen_fiscoffi_sqlstr == expected_fiscoffi_sqlstr
    assert gen_fiscunit_sqlstr == expected_fiscunit_sqlstr


# def test_get_bud_bu1_select_sqlstrs_ReturnsObj_HasAllNeededKeys():
#     # ESTABLISH
#     a23_str = "accord23"

#     # WHEN
#     fu1_select_sqlstrs = get_bud_bu1_select_sqlstrs(a23_str)

#     # THEN
#     assert fu1_select_sqlstrs
#     expected_fu1_select_dimens = set(get_bud_dimens())
#     assert set(fu1_select_sqlstrs.keys()) == expected_fu1_select_dimens


# def test_get_bud_bu1_select_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH
#     a23_str = "accord23"

#     # WHEN
#     bu1_select_sqlstrs = get_bud_bu1_select_sqlstrs(bud_title=a23_str)

#     # THEN
#     budunit_str = "budunit"
#     budacct_str = "bud_acctunit"
#     budmemb_str = "bud_acct_membership"
#     buditem_str = "bud_itemunit"
#     budawar_str = "bud_item_awardlink"
#     budreas_str = "bud_item_reasonunit"
#     budprem_str = "bud_item_reason_premiseunit"
#     budteam_str = "bud_item_teamlink"
#     budheal_str = "bud_item_healerlink"
#     budfact_str = "bud_item_factunit"
#     gen_budunit_sqlstr = bu1_select_sqlstrs.get(budunit_str)
#     gen_budacct_sqlstr = bu1_select_sqlstrs.get(budacct_str)
#     gen_budmemb_sqlstr = bu1_select_sqlstrs.get(budmemb_str)
#     gen_buditem_sqlstr = bu1_select_sqlstrs.get(buditem_str)
#     gen_budawar_sqlstr = bu1_select_sqlstrs.get(budawar_str)
#     gen_budreas_sqlstr = bu1_select_sqlstrs.get(budreas_str)
#     gen_budprem_sqlstr = bu1_select_sqlstrs.get(budprem_str)
#     gen_budteam_sqlstr = bu1_select_sqlstrs.get(budteam_str)
#     gen_budheal_sqlstr = bu1_select_sqlstrs.get(budheal_str)
#     gen_budfact_sqlstr = bu1_select_sqlstrs.get(budfact_str)

#     expected_budunit_unit_select_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally REAL, fund_coin REAL, penny REAL, respect_bit REAL)"""
#     expected_budACCT_acct_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"""
#     expected_budMEMB_memb_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"""
#     expected_budITEM_item_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor REAL, denom REAL, morph INTEGER, gogo_want REAL, stop_want REAL, mass REAL, pledge INTEGER, problem_bool INTEGER)"""
#     expected_budAWAR_awar_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL)"""
#     expected_budPREM_reas_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor REAL)"""
#     expected_budREAS_prem_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, base_item_active_requisite TEXT)"""
#     expected_budTEAM_team_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, team_tag TEXT)"""
#     expected_budHEAL_heal_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, healer_name TEXT)"""
#     expected_budFACT_fact_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_put_agg (face_name TEXT, event_int INTEGER, fisc_title TEXT, owner_name TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL)"""

#     assert gen_budcash_sqlstr == expected_budcash_sqlstr
#     assert gen_buddeal_sqlstr == expected_buddeal_sqlstr
#     assert gen_budhour_sqlstr == expected_budhour_sqlstr
#     assert gen_budmont_sqlstr == expected_budmont_sqlstr
#     assert gen_budweek_sqlstr == expected_budweek_sqlstr
#     assert gen_budoffi_sqlstr == expected_budoffi_sqlstr
#     assert gen_budunit_sqlstr == expected_budunit_sqlstr
