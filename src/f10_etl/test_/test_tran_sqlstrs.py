from src.f00_instrument.db_toolbox import (
    db_table_exists,
    create_select_inconsistency_query,
    create_update_inconsistency_error_query,
    get_create_table_sqlstr,
    create_table2table_agg_insert_query,
    get_table_columns,
    is_stageable,
)
from src.f02_bud.bud_tool import budunit_str
from src.f04_gift.atom_config import (
    face_name_str,
    fiscal_title_str,
    get_bud_dimens,
    get_delete_key_name,
)
from src.f07_fiscal.fiscal_config import fiscalunit_str, get_fiscal_dimens
from src.f08_pidgin.pidgin_config import event_int_str, pidginunit_str
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
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f10_etl.tran_sqlstrs import (
    get_fiscal_create_table_sqlstrs,
    get_bud_create_table_sqlstrs,
    create_fiscal_tables,
    create_bud_tables,
    create_all_idea_tables,
    get_bud_inconsistency_sqlstrs,
    get_fiscal_inconsistency_sqlstrs,
    get_bud_put_update_inconsist_error_message_sqlstrs,
    get_fiscal_update_inconsist_error_message_sqlstrs,
    get_bud_insert_put_agg_from_staging_sqlstrs,
    get_bud_insert_del_agg_from_staging_sqlstrs,
    get_fiscal_insert_agg_from_staging_sqlstrs,
    FISCALUNIT_AGG_INSERT_SQLSTR,
    IDEA_STAGEABLE_PUT_DIMENS,
    IDEA_STAGEABLE_DEL_DIMENS,
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


def test_get_fiscal_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_fiscal_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "fiscal"
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


def test_get_fiscal_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    fiscal_create_table_sqlstrs = get_fiscal_create_table_sqlstrs()

    # THEN
    assert fiscal_create_table_sqlstrs
    fiscal_dimens = get_fiscal_dimens()
    expected_fiscal_tablenames = {f"{x_dimen}_agg" for x_dimen in fiscal_dimens}
    expected_fiscal_tablenames.update(
        {f"{x_dimen}_staging" for x_dimen in fiscal_dimens}
    )
    print(f"{expected_fiscal_tablenames=}")
    assert set(fiscal_create_table_sqlstrs.keys()) == expected_fiscal_tablenames


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


def test_create_all_idea_tables_CreatesFiscalStagingTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    idea_numbers = get_idea_numbers()
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        for idea_number in idea_numbers:
            assert db_table_exists(cursor, f"{idea_number}_staging") is False

        # WHEN
        create_all_idea_tables(cursor)

        # THEN
        for idea_number in idea_numbers:
            print(f"{idea_number} checking...")
            assert db_table_exists(cursor, f"{idea_number}_staging")


def test_create_bud_tables_CreatesFiscalStagingTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
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


def test_create_fiscal_tables_CreatesFiscalStagingTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        fis_objs = FiscalPrimeObjsRef()
        fis_cols = FiscalPrimeColumnsRef()
        assert db_table_exists(cursor, fis_objs.unit_agg_tablename) is False
        assert db_table_exists(cursor, fis_objs.deal_agg_tablename) is False
        assert db_table_exists(cursor, fis_objs.cash_agg_tablename) is False
        assert db_table_exists(cursor, fis_objs.hour_agg_tablename) is False
        assert db_table_exists(cursor, fis_objs.mont_agg_tablename) is False
        assert db_table_exists(cursor, fis_objs.week_agg_tablename) is False
        assert db_table_exists(cursor, fis_objs.unit_stage_tablename) is False
        assert db_table_exists(cursor, fis_objs.deal_stage_tablename) is False
        assert db_table_exists(cursor, fis_objs.cash_stage_tablename) is False
        assert db_table_exists(cursor, fis_objs.hour_stage_tablename) is False
        assert db_table_exists(cursor, fis_objs.mont_stage_tablename) is False
        assert db_table_exists(cursor, fis_objs.week_stage_tablename) is False

        # WHEN
        create_fiscal_tables(cursor)

        # THEN
        assert db_table_exists(cursor, fis_objs.unit_agg_tablename)
        assert db_table_exists(cursor, fis_objs.deal_agg_tablename)
        assert db_table_exists(cursor, fis_objs.cash_agg_tablename)
        assert db_table_exists(cursor, fis_objs.hour_agg_tablename)
        assert db_table_exists(cursor, fis_objs.mont_agg_tablename)
        assert db_table_exists(cursor, fis_objs.week_agg_tablename)

        assert db_table_exists(cursor, fis_objs.unit_stage_tablename)
        assert db_table_exists(cursor, fis_objs.deal_stage_tablename)
        assert db_table_exists(cursor, fis_objs.cash_stage_tablename)
        assert db_table_exists(cursor, fis_objs.hour_stage_tablename)
        assert db_table_exists(cursor, fis_objs.mont_stage_tablename)
        assert db_table_exists(cursor, fis_objs.week_stage_tablename)

        fis_unit_agg_pragma = get_pragma_table_fetchall(fis_cols.unit_agg_columns)
        fis_deal_agg_pragma = get_pragma_table_fetchall(fis_cols.deal_agg_columns)
        fis_cash_agg_pragma = get_pragma_table_fetchall(fis_cols.cash_agg_columns)
        fis_hour_agg_pragma = get_pragma_table_fetchall(fis_cols.hour_agg_columns)
        fis_mont_agg_pragma = get_pragma_table_fetchall(fis_cols.mont_agg_columns)
        fis_week_agg_pragma = get_pragma_table_fetchall(fis_cols.week_agg_columns)
        fis_unit_stage_pragma = get_pragma_table_fetchall(fis_cols.unit_staging_columns)
        fis_deal_stage_pragma = get_pragma_table_fetchall(fis_cols.deal_staging_columns)
        fis_cash_stage_pragma = get_pragma_table_fetchall(fis_cols.cash_staging_columns)
        fis_hour_stage_pragma = get_pragma_table_fetchall(fis_cols.hour_staging_columns)
        fis_mont_stage_pragma = get_pragma_table_fetchall(fis_cols.mont_staging_columns)
        fis_week_stage_pragma = get_pragma_table_fetchall(fis_cols.week_staging_columns)
        cursor.execute(f"PRAGMA table_info({fis_objs.unit_agg_tablename})")
        assert fis_unit_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.deal_agg_tablename})")
        assert fis_deal_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.cash_agg_tablename})")
        assert fis_cash_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.hour_agg_tablename})")
        assert fis_hour_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.mont_agg_tablename})")
        assert fis_mont_agg_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.week_agg_tablename})")
        assert fis_week_agg_pragma == cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({fis_objs.unit_stage_tablename})")
        assert fis_unit_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.deal_stage_tablename})")
        assert fis_deal_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.cash_stage_tablename})")
        assert fis_cash_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.hour_stage_tablename})")
        assert fis_hour_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.mont_stage_tablename})")
        assert fis_mont_stage_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fis_objs.week_stage_tablename})")
        assert fis_week_stage_pragma == cursor.fetchall()


def test_get_fiscal_inconsistency_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    fiscal_inconsistency_sqlstrs = get_fiscal_inconsistency_sqlstrs()

    # THEN
    assert fiscal_inconsistency_sqlstrs.keys() == get_fiscal_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        # if dimen_config.get(idea_category_str()) != "pidgin"
        # if dimen_config.get(idea_category_str()) == "bud"
        if dimen_config.get(idea_category_str()) == "fiscal"
    }

    exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fiscal_tables(cursor)

        for x_dimen in sorted(idea_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = fiscal_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_staging"
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_select_inconsistency_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            print(f'{x_dimen}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""')
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


def test_get_fiscal_update_inconsist_error_message_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    fiscal_update_error_sqlstrs = get_fiscal_update_inconsist_error_message_sqlstrs()

    # THEN
    assert set(fiscal_update_error_sqlstrs.keys()) == get_fiscal_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "fiscal"
    }

    exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fiscal_tables(cursor)
        create_bud_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            x_sqlstr = fiscal_update_error_sqlstrs.get(x_dimen)
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
            # print(
            #     f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
            # )
            # print(
            #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
            # )
            # print(f"""            {x_sqlstr=}""")
            assert x_sqlstr == generated_dimen_sqlstr


def test_get_fiscal_insert_agg_from_staging_sqlstrs_ReturnsObj():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH / WHEN
    fiscal_insert_agg_sqlstrs = get_fiscal_insert_agg_from_staging_sqlstrs()

    # THEN
    assert set(fiscal_insert_agg_sqlstrs.keys()) == get_fiscal_dimens()
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
        if dimen_config.get(idea_category_str()) == "fiscal"
    }
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        create_fiscal_tables(cursor)

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
            x_sqlstr = fiscal_insert_agg_sqlstrs.get(x_dimen)
            # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
            # print(
            #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{generated_table2table_agg_insert_sqlstr}"""'
            # )
            assert x_sqlstr == generated_table2table_agg_insert_sqlstr

        generated_fiscalunit_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=f"{fiscalunit_str()}_staging",
            dst_table=f"{fiscalunit_str()}_agg",
            focus_cols=[fiscal_title_str()],
            exclude_cols=x_exclude_cols,
        )
        assert FISCALUNIT_AGG_INSERT_SQLSTR == generated_fiscalunit_sqlstr
        columns_header = """fiscal_title, fund_coin, penny, respect_bit, present_time, bridge, c400_number, yr1_jan1_offset, monthday_distortion, timeline_title"""
        tablename = "fiscalunit"
        expected_ficsalunit_sqlstr = f"""INSERT INTO {tablename}_agg ({columns_header})
SELECT fiscal_title, MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(present_time), MAX(bridge), MAX(c400_number), MAX(yr1_jan1_offset), MAX(monthday_distortion), MAX(timeline_title)
FROM {tablename}_staging
WHERE error_message IS NULL
GROUP BY fiscal_title
;
"""
        assert FISCALUNIT_AGG_INSERT_SQLSTR == expected_ficsalunit_sqlstr

    assert len(idea_config) == len(fiscal_insert_agg_sqlstrs)


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
        # if dimen_config.get(idea_category_str()) == "fiscal"
    }
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_fiscal_tables(cursor)
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
    assert idea_dimen_combo_checked_count == 624
    assert idea_stage2dimen_count == 99
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
        # if dimen_config.get(idea_category_str()) == "fiscal"
    }
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_fiscal_tables(cursor)
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
    assert idea_dimen_combo_checked_count == 624
    assert idea_stage2dimen_count == 10
    assert IDEA_STAGEABLE_DEL_DIMENS == expected_idea_stagable_dimens
