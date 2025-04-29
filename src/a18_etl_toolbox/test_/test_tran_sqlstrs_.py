from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    create_select_inconsistency_query,
    create_update_inconsistency_error_query,
    get_create_table_sqlstr,
    create_table2table_agg_insert_query,
    get_table_columns,
    required_columns_exist,
    create_select_query,
)
from src.a02_finance_logic._utils.str_helpers import (
    fisc_tag_str,
    owner_name_str,
    deal_time_str,
    tran_time_str,
)
from src.a06_bud_logic.bud_tool import (
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_item_awardlink_str,
    bud_item_factunit_str,
    bud_item_healerlink_str,
    bud_item_reason_premiseunit_str,
    bud_item_reasonunit_str,
    bud_item_teamlink_str,
    bud_itemunit_str,
    budunit_str,
    bud_groupunit_str,
)
from src.a07_calendar_logic.chrono import (
    timeline_tag_str,
    c400_number_str,
    monthday_distortion_str,
    yr1_jan1_offset_str,
)
from src.a08_bud_atom_logic.atom_config import (
    event_int_str,
    face_name_str,
    get_bud_dimens,
    get_delete_key_name,
)
from src.a15_fisc_logic.fisc_config import (
    get_fisc_dimens,
    fiscunit_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
)
from src.a16_pidgin_logic.pidgin_config import get_pidgin_dimens
from src.a17_idea_logic.idea_config import (
    idea_number_str,
    get_idea_sqlite_types,
    get_idea_config_dict,
    idea_category_str,
    get_idea_numbers,
)
from src.a17_idea_logic.idea_db_tool import (
    get_pragma_table_fetchall,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.a18_etl_toolbox.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    get_fisc_prime_create_table_sqlstrs,
    get_bud_prime_create_table_sqlstrs,
    create_pidgin_prime_tables,
    create_fisc_prime_tables,
    create_bud_prime_tables,
    create_all_idea_tables,
    get_pidgin_inconsistency_sqlstrs,
    get_bud_inconsistency_sqlstrs,
    get_fisc_inconsistency_sqlstrs,
    get_pidgin_update_inconsist_error_message_sqlstrs,
    get_bud_put_update_inconsist_error_message_sqlstrs,
    get_fisc_update_inconsist_error_message_sqlstrs,
    get_bud_insert_put_agg_from_raw_sqlstrs,
    get_bud_insert_del_agg_from_raw_sqlstrs,
    get_fisc_insert_agg_from_raw_sqlstrs,
    get_pidgin_insert_agg_from_raw_sqlstrs,
    FISCUNIT_AGG_INSERT_SQLSTR,
    IDEA_STAGEBLE_PUT_DIMENS,
    IDEA_STAGEBLE_DEL_DIMENS,
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
        f"{bud_acct_membership_str()}_put_agg": "BUDMEMB_PUT_AGG",
        f"{bud_acct_membership_str()}_put_raw": "BUDMEMB_PUT_RAW",
        f"{bud_acctunit_str()}_put_agg": "BUDACCT_PUT_AGG",
        f"{bud_acctunit_str()}_put_raw": "BUDACCT_PUT_RAW",
        f"{bud_item_awardlink_str()}_put_agg": "BUDAWAR_PUT_AGG",
        f"{bud_item_awardlink_str()}_put_raw": "BUDAWAR_PUT_RAW",
        f"{bud_item_factunit_str()}_put_agg": "BUDFACT_PUT_AGG",
        f"{bud_item_factunit_str()}_put_raw": "BUDFACT_PUT_RAW",
        f"{bud_item_healerlink_str()}_put_agg": "BUDHEAL_PUT_AGG",
        f"{bud_item_healerlink_str()}_put_raw": "BUDHEAL_PUT_RAW",
        f"{bud_item_reason_premiseunit_str()}_put_agg": "BUDPREM_PUT_AGG",
        f"{bud_item_reason_premiseunit_str()}_put_raw": "BUDPREM_PUT_RAW",
        f"{bud_item_reasonunit_str()}_put_agg": "BUDREAS_PUT_AGG",
        f"{bud_item_reasonunit_str()}_put_raw": "BUDREAS_PUT_RAW",
        f"{bud_item_teamlink_str()}_put_agg": "BUDTEAM_PUT_AGG",
        f"{bud_item_teamlink_str()}_put_raw": "BUDTEAM_PUT_RAW",
        f"{bud_itemunit_str()}_put_agg": "BUDITEM_PUT_AGG",
        f"{bud_itemunit_str()}_put_raw": "BUDITEM_PUT_RAW",
        f"{budunit_str()}_put_agg": "BUDUNIT_PUT_AGG",
        f"{budunit_str()}_put_raw": "BUDUNIT_PUT_RAW",
        f"{bud_acct_membership_str()}_del_agg": "BUDMEMB_DEL_AGG",
        f"{bud_acct_membership_str()}_del_raw": "BUDMEMB_DEL_RAW",
        f"{bud_acctunit_str()}_del_agg": "BUDACCT_DEL_AGG",
        f"{bud_acctunit_str()}_del_raw": "BUDACCT_DEL_RAW",
        f"{bud_item_awardlink_str()}_del_agg": "BUDAWAR_DEL_AGG",
        f"{bud_item_awardlink_str()}_del_raw": "BUDAWAR_DEL_RAW",
        f"{bud_item_factunit_str()}_del_agg": "BUDFACT_DEL_AGG",
        f"{bud_item_factunit_str()}_del_raw": "BUDFACT_DEL_RAW",
        f"{bud_item_healerlink_str()}_del_agg": "BUDHEAL_DEL_AGG",
        f"{bud_item_healerlink_str()}_del_raw": "BUDHEAL_DEL_RAW",
        f"{bud_item_reason_premiseunit_str()}_del_agg": "BUDPREM_DEL_AGG",
        f"{bud_item_reason_premiseunit_str()}_del_raw": "BUDPREM_DEL_RAW",
        f"{bud_item_reasonunit_str()}_del_agg": "BUDREAS_DEL_AGG",
        f"{bud_item_reasonunit_str()}_del_raw": "BUDREAS_DEL_RAW",
        f"{bud_item_teamlink_str()}_del_agg": "BUDTEAM_DEL_AGG",
        f"{bud_item_teamlink_str()}_del_raw": "BUDTEAM_DEL_RAW",
        f"{bud_itemunit_str()}_del_agg": "BUDITEM_DEL_AGG",
        f"{bud_itemunit_str()}_del_raw": "BUDITEM_DEL_RAW",
        f"{budunit_str()}_del_agg": "BUDUNIT_DEL_AGG",
        f"{budunit_str()}_del_raw": "BUDUNIT_DEL_RAW",
    }
    return abbrevions.get(tablename)


def test_get_fisc_prime_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_fisc_prime_create_table_sqlstrs()

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
        ag_cols = get_default_sorted_list(ag_cols)
        print(f"{ag_cols=}")
        gen_dimen_agg_sqlstr = get_create_table_sqlstr(ag_table, ag_cols, sqlite_types)
        assert ag_sqlstr == gen_dimen_agg_sqlstr

        st_table = f"{x_dimen}_raw"
        st_sqlstr = create_table_sqlstrs.get(st_table)
        st_cols = set(x_config.get("jkeys").keys())
        st_cols.update(set(x_config.get("jvalues").keys()))
        st_cols.add(idea_number_str())
        st_cols.add("error_message")
        st_cols = get_default_sorted_list(st_cols)
        gen_dimen_raw_sqlstr = get_create_table_sqlstr(st_table, st_cols, sqlite_types)
        assert st_sqlstr == gen_dimen_raw_sqlstr

        # print(f'CREATE_{ag_table.upper()}_SQLSTR= """{gen_dimen_agg_sqlstr}"""')
        # print(f'CREATE_{st_table.upper()}_SQLSTR= """{gen_dimen_raw_sqlstr}"""')
        # print(f'"{ag_table}": {ag_table.upper()}_SQLSTR,')
        # print(f'"{st_table}": {st_table.upper()}_SQLSTR,')


def test_get_bud_prime_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_bud_prime_create_table_sqlstrs()

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
        ag_put_cols = get_default_sorted_list(ag_put_cols)
        ex_ag_put_sqlstr = get_create_table_sqlstr(ag_put_table, ag_put_cols, s_types)
        print(f"{ex_ag_put_sqlstr=}")
        assert create_table_sqlstrs.get(ag_put_table) == ex_ag_put_sqlstr

        st_put_table = f"{x_dimen}_put_raw"
        st_put_cols = set(x_config.get("jkeys").keys())
        st_put_cols.update(set(x_config.get("jvalues").keys()))
        st_put_cols.add(idea_number_str())
        st_put_cols.add("error_message")
        st_put_cols = get_default_sorted_list(st_put_cols)
        ex_st_put_sqlstr = get_create_table_sqlstr(st_put_table, st_put_cols, s_types)
        print(f"{ex_st_put_sqlstr=}")
        assert create_table_sqlstrs.get(st_put_table) == ex_st_put_sqlstr

        ag_del_table = f"{x_dimen}_del_agg"
        ag_del_cols = set(x_config.get("jkeys").keys())
        ag_del_cols = get_default_sorted_list(ag_del_cols)
        ag_del_cols[-1] = get_delete_key_name(ag_del_cols[-1])
        ex_ag_del_sqlstr = get_create_table_sqlstr(ag_del_table, ag_del_cols, s_types)
        # print(f" {ex_ag_del_sqlstr}")
        assert create_table_sqlstrs.get(ag_del_table) == ex_ag_del_sqlstr

        st_del_table = f"{x_dimen}_del_raw"
        st_del_cols = set(x_config.get("jkeys").keys())
        st_del_cols.add(idea_number_str())
        st_del_cols.add("error_message")
        st_del_cols = get_default_sorted_list(st_del_cols)
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


def test_get_fisc_prime_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    fisc_create_table_sqlstrs = get_fisc_prime_create_table_sqlstrs()

    # THEN
    assert fisc_create_table_sqlstrs
    fisc_dimens = get_fisc_dimens()
    expected_fisc_tablenames = {f"{x_dimen}_agg" for x_dimen in fisc_dimens}
    expected_fisc_tablenames.update({f"{x_dimen}_raw" for x_dimen in fisc_dimens})
    print(f"{expected_fisc_tablenames=}")
    assert set(fisc_create_table_sqlstrs.keys()) == expected_fisc_tablenames


def test_get_bud_prime_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    bud_create_table_sqlstrs = get_bud_prime_create_table_sqlstrs()

    # THEN
    assert bud_create_table_sqlstrs
    bud_dimens = get_bud_dimens()
    expected_bud_tablenames = {f"{x_dimen}_put_agg" for x_dimen in bud_dimens}
    expected_bud_tablenames.update({f"{x_dimen}_put_raw" for x_dimen in bud_dimens})
    expected_bud_tablenames.update({f"{x_dimen}_del_agg" for x_dimen in bud_dimens})
    expected_bud_tablenames.update({f"{x_dimen}_del_raw" for x_dimen in bud_dimens})
    print(f"{expected_bud_tablenames=}")
    assert set(bud_create_table_sqlstrs.keys()) == expected_bud_tablenames


def test_create_all_idea_tables_CreatesFiscRawTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    idea_numbers = get_idea_numbers()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        for idea_number in idea_numbers:
            assert db_table_exists(cursor, f"{idea_number}_raw") is False

        # WHEN
        create_all_idea_tables(cursor)

        # THEN
        for idea_number in idea_numbers:
            print(f"{idea_number} checking...")
            assert db_table_exists(cursor, f"{idea_number}_raw")


def test_create_bud_prime_tables_CreatesFiscRawTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0
        budmemb_pud_agg_table = f"{bud_acct_membership_str()}_put_agg"
        budmemb_pud_raw_table = f"{bud_acct_membership_str()}_put_raw"
        budacct_pud_agg_table = f"{bud_acctunit_str()}_put_agg"
        budacct_pud_raw_table = f"{bud_acctunit_str()}_put_raw"
        budawar_pud_agg_table = f"{bud_item_awardlink_str()}_put_agg"
        budawar_pud_raw_table = f"{bud_item_awardlink_str()}_put_raw"
        budfact_pud_agg_table = f"{bud_item_factunit_str()}_put_agg"
        budfact_pud_raw_table = f"{bud_item_factunit_str()}_put_raw"
        budheal_pud_agg_table = f"{bud_item_healerlink_str()}_put_agg"
        budheal_pud_raw_table = f"{bud_item_healerlink_str()}_put_raw"
        budprem_pud_agg_table = f"{bud_item_reason_premiseunit_str()}_put_agg"
        budprem_pud_raw_table = f"{bud_item_reason_premiseunit_str()}_put_raw"
        budreas_pud_agg_table = f"{bud_item_reasonunit_str()}_put_agg"
        budreas_pud_raw_table = f"{bud_item_reasonunit_str()}_put_raw"
        budteam_pud_agg_table = f"{bud_item_teamlink_str()}_put_agg"
        budteam_pud_raw_table = f"{bud_item_teamlink_str()}_put_raw"
        buditem_pud_agg_table = f"{bud_itemunit_str()}_put_agg"
        buditem_pud_raw_table = f"{bud_itemunit_str()}_put_raw"
        budunit_pud_agg_table = f"{budunit_str()}_put_agg"
        budunit_pud_raw_table = f"{budunit_str()}_put_raw"

        assert db_table_exists(cursor, budmemb_pud_agg_table) is False
        assert db_table_exists(cursor, budmemb_pud_raw_table) is False
        assert db_table_exists(cursor, budacct_pud_agg_table) is False
        assert db_table_exists(cursor, budacct_pud_raw_table) is False
        assert db_table_exists(cursor, budawar_pud_agg_table) is False
        assert db_table_exists(cursor, budawar_pud_raw_table) is False
        assert db_table_exists(cursor, budfact_pud_agg_table) is False
        assert db_table_exists(cursor, budfact_pud_raw_table) is False
        assert db_table_exists(cursor, budheal_pud_agg_table) is False
        assert db_table_exists(cursor, budheal_pud_raw_table) is False
        assert db_table_exists(cursor, budprem_pud_agg_table) is False
        assert db_table_exists(cursor, budprem_pud_raw_table) is False
        assert db_table_exists(cursor, budreas_pud_agg_table) is False
        assert db_table_exists(cursor, budreas_pud_raw_table) is False
        assert db_table_exists(cursor, budteam_pud_agg_table) is False
        assert db_table_exists(cursor, budteam_pud_raw_table) is False
        assert db_table_exists(cursor, buditem_pud_agg_table) is False
        assert db_table_exists(cursor, buditem_pud_raw_table) is False
        assert db_table_exists(cursor, budunit_pud_agg_table) is False
        assert db_table_exists(cursor, budunit_pud_raw_table) is False

        # WHEN
        create_bud_prime_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 40
        assert db_table_exists(cursor, budmemb_pud_agg_table)
        assert db_table_exists(cursor, budmemb_pud_raw_table)
        assert db_table_exists(cursor, budacct_pud_agg_table)
        assert db_table_exists(cursor, budacct_pud_raw_table)
        assert db_table_exists(cursor, budawar_pud_agg_table)
        assert db_table_exists(cursor, budawar_pud_raw_table)
        assert db_table_exists(cursor, budfact_pud_agg_table)
        assert db_table_exists(cursor, budfact_pud_raw_table)
        assert db_table_exists(cursor, budheal_pud_agg_table)
        assert db_table_exists(cursor, budheal_pud_raw_table)
        assert db_table_exists(cursor, budprem_pud_agg_table)
        assert db_table_exists(cursor, budprem_pud_raw_table)
        assert db_table_exists(cursor, budreas_pud_agg_table)
        assert db_table_exists(cursor, budreas_pud_raw_table)
        assert db_table_exists(cursor, budteam_pud_agg_table)
        assert db_table_exists(cursor, budteam_pud_raw_table)
        assert db_table_exists(cursor, buditem_pud_agg_table)
        assert db_table_exists(cursor, buditem_pud_raw_table)
        assert db_table_exists(cursor, budunit_pud_agg_table)
        assert db_table_exists(cursor, budunit_pud_raw_table)


def test_create_fisc_prime_tables_CreatesFiscRawTables():
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
        assert db_table_exists(cursor, fisc_objs.unit_raw_tablename) is False
        assert db_table_exists(cursor, fisc_objs.deal_raw_tablename) is False
        assert db_table_exists(cursor, fisc_objs.cash_raw_tablename) is False
        assert db_table_exists(cursor, fisc_objs.hour_raw_tablename) is False
        assert db_table_exists(cursor, fisc_objs.mont_raw_tablename) is False
        assert db_table_exists(cursor, fisc_objs.week_raw_tablename) is False

        # WHEN
        create_fisc_prime_tables(cursor)

        # THEN
        assert db_table_exists(cursor, fisc_objs.unit_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.deal_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.cash_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.hour_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.mont_agg_tablename)
        assert db_table_exists(cursor, fisc_objs.week_agg_tablename)

        assert db_table_exists(cursor, fisc_objs.unit_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.deal_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.cash_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.hour_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.mont_raw_tablename)
        assert db_table_exists(cursor, fisc_objs.week_raw_tablename)

        fisc_unit_agg_pragma = get_pragma_table_fetchall(fisc_cols.unit_agg_columns)
        fisc_deal_agg_pragma = get_pragma_table_fetchall(fisc_cols.deal_agg_columns)
        fisc_cash_agg_pragma = get_pragma_table_fetchall(fisc_cols.cash_agg_columns)
        fisc_hour_agg_pragma = get_pragma_table_fetchall(fisc_cols.hour_agg_columns)
        fisc_mont_agg_pragma = get_pragma_table_fetchall(fisc_cols.mont_agg_columns)
        fisc_week_agg_pragma = get_pragma_table_fetchall(fisc_cols.week_agg_columns)
        fisc_unit_raw_pragma = get_pragma_table_fetchall(fisc_cols.unit_raw_columns)
        fisc_deal_raw_pragma = get_pragma_table_fetchall(fisc_cols.deal_raw_columns)
        fisc_cash_raw_pragma = get_pragma_table_fetchall(fisc_cols.cash_raw_columns)
        fisc_hour_raw_pragma = get_pragma_table_fetchall(fisc_cols.hour_raw_columns)
        fisc_mont_raw_pragma = get_pragma_table_fetchall(fisc_cols.mont_raw_columns)
        fisc_week_raw_pragma = get_pragma_table_fetchall(fisc_cols.week_raw_columns)
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

        cursor.execute(f"PRAGMA table_info({fisc_objs.unit_raw_tablename})")
        assert fisc_unit_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.deal_raw_tablename})")
        assert fisc_deal_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.cash_raw_tablename})")
        assert fisc_cash_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.hour_raw_tablename})")
        assert fisc_hour_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.mont_raw_tablename})")
        assert fisc_mont_raw_pragma == cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({fisc_objs.week_raw_tablename})")
        assert fisc_week_raw_pragma == cursor.fetchall()


def test_get_pidgin_inconsistency_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    pidgin_inconsistency_sqlstrs = get_pidgin_inconsistency_sqlstrs()

    # THEN
    assert pidgin_inconsistency_sqlstrs.keys() == get_pidgin_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        # if dimen_config.get(idea_category_str()) != "pidgin"
        # if dimen_config.get(idea_category_str()) == "bud"
        if dimen_config.get(idea_category_str()) == "pidgin"
    }

    exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_pidgin_prime_tables(cursor)

        for x_dimen in sorted(idea_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = pidgin_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_raw"
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_select_inconsistency_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            print(
                f'{x_dimen.upper()}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""'
            )
            print(f'{x_sqlstr=}"""')
            assert x_sqlstr == generated_dimen_sqlstr


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
        create_fisc_prime_tables(cursor)

        for x_dimen in sorted(idea_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = fisc_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_raw"
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
        create_bud_prime_tables(cursor)

        for x_dimen in sorted(idea_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = bud_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_put_raw"
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
        create_fisc_prime_tables(cursor)
        create_bud_prime_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            x_sqlstr = fisc_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_raw"
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


def test_get_pidgin_update_inconsist_error_message_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    pidgin_update_error_sqlstrs = get_pidgin_update_inconsist_error_message_sqlstrs()

    # THEN
    assert set(pidgin_update_error_sqlstrs.keys()) == get_pidgin_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "pidgin"
    }

    exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_pidgin_prime_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            x_sqlstr = pidgin_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_raw"
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
        create_bud_prime_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            x_sqlstr = bud_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_put_raw"
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


def test_get_fisc_insert_agg_from_raw_sqlstrs_ReturnsObj():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH / WHEN
    fisc_insert_agg_sqlstrs = get_fisc_insert_agg_from_raw_sqlstrs()

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
        create_fisc_prime_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns.remove(event_int_str())
            dimen_focus_columns.remove(face_name_str())
            dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
            raw_tablename = f"{x_dimen}_raw"
            agg_tablename = f"{x_dimen}_agg"

            expected_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=raw_tablename,
                    dst_table=agg_tablename,
                    focus_cols=dimen_focus_columns,
                    exclude_cols=x_exclude_cols,
                )
            )
            x_sqlstr = fisc_insert_agg_sqlstrs.get(x_dimen)
            # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
            # print(
            #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
            # )
            assert x_sqlstr == expected_table2table_agg_insert_sqlstr

        generated_fiscunit_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=f"{fiscunit_str()}_raw",
            dst_table=f"{fiscunit_str()}_agg",
            focus_cols=[fisc_tag_str()],
            exclude_cols=x_exclude_cols,
        )
        assert FISCUNIT_AGG_INSERT_SQLSTR == generated_fiscunit_sqlstr
        columns_header = f"""{fisc_tag_str()}, {timeline_tag_str()}, {c400_number_str()}, {yr1_jan1_offset_str()}, {monthday_distortion_str()}, fund_coin, penny, respect_bit, bridge, job_listen_rotations"""
        tablename = "fiscunit"
        expected_fiscunit_sqlstr = f"""INSERT INTO {tablename}_agg ({columns_header})
SELECT {fisc_tag_str()}, MAX({timeline_tag_str()}), MAX({c400_number_str()}), MAX({yr1_jan1_offset_str()}), MAX({monthday_distortion_str()}), MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(bridge), MAX(job_listen_rotations)
FROM {tablename}_raw
WHERE error_message IS NULL
GROUP BY {fisc_tag_str()}
;
"""
        assert FISCUNIT_AGG_INSERT_SQLSTR == expected_fiscunit_sqlstr

    assert len(idea_config) == len(fisc_insert_agg_sqlstrs)


def test_get_pidgin_insert_agg_from_raw_sqlstrs_ReturnsObj():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH / WHEN
    pidgin_insert_agg_sqlstrs = get_pidgin_insert_agg_from_raw_sqlstrs()

    # THEN
    assert set(pidgin_insert_agg_sqlstrs.keys()) == get_pidgin_dimens()
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
        if dimen_config.get(idea_category_str()) == "pidgin"
    }
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_pidgin_prime_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns.remove(event_int_str())
            dimen_focus_columns.remove(face_name_str())
            dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
            raw_tablename = f"{x_dimen}_raw"
            agg_tablename = f"{x_dimen}_agg"

            expected_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=raw_tablename,
                    dst_table=agg_tablename,
                    focus_cols=dimen_focus_columns,
                    exclude_cols=x_exclude_cols,
                )
            )
            x_sqlstr = pidgin_insert_agg_sqlstrs.get(x_dimen)
            # print(f'"{x_dimen}": {x_dimen.upper()}_AGG_INSERT_SQLSTR,')
            # print(
            #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
            # )
            assert x_sqlstr == expected_table2table_agg_insert_sqlstr

    assert len(idea_config) == len(pidgin_insert_agg_sqlstrs)


def test_get_bud_insert_put_agg_from_raw_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_insert_agg_sqlstrs = get_bud_insert_put_agg_from_raw_sqlstrs()

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
        create_bud_prime_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
            raw_tablename = f"{x_dimen}_put_raw"
            agg_tablename = f"{x_dimen}_put_agg"

            expected_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=raw_tablename,
                    dst_table=agg_tablename,
                    focus_cols=dimen_focus_columns,
                    exclude_cols=x_exclude_cols,
                )
            )
            x_sqlstr = bud_insert_agg_sqlstrs.get(x_dimen)
            # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
            # print(
            #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
            # )
            assert x_sqlstr == expected_table2table_agg_insert_sqlstr


def test_get_bud_insert_del_agg_from_raw_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_insert_agg_sqlstrs = get_bud_insert_del_agg_from_raw_sqlstrs()

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
        create_bud_prime_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
            dimen_focus_columns[-1] = get_delete_key_name(dimen_focus_columns[-1])
            raw_tablename = f"{x_dimen}_del_raw"
            agg_tablename = f"{x_dimen}_del_agg"

            expected_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=raw_tablename,
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


def test_IDEA_STAGEBLE_PUT_DIMENS_HasAll_idea_numbersForAll_dimens():
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
        create_fisc_prime_tables(cursor)
        create_bud_prime_tables(cursor)

        idea_raw2dimen_count = 0
        idea_dimen_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        expected_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            dimen_config = idea_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get("jkeys").keys())
            dimen_value_columns = set(dimen_config.get("jvalues").keys())
            for idea_number in sorted_idea_numbers:
                src_columns = get_table_columns(cursor, f"{idea_number}_raw")
                expected_stagable = dimen_key_columns.issubset(src_columns)
                if idea_number == "br00050":
                    print(f"{x_dimen} {idea_number} checking... {src_columns}")
                src_tablename = f"{idea_number}_raw"
                gen_stablable = required_columns_exist(
                    cursor, src_tablename, dimen_key_columns
                )
                assert expected_stagable == gen_stablable

                idea_dimen_combo_checked_count += 1
                if required_columns_exist(cursor, src_tablename, dimen_key_columns):
                    expected_idea_stagable_dimens.get(idea_number).append(x_dimen)
                    idea_raw2dimen_count += 1
                    src_cols_set = set(src_columns)
                    existing_value_col = src_cols_set.intersection(dimen_value_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    # print(
                    #     f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}, values: {existing_value_col}"
                    # )
                    generated_sqlstr = get_idea_into_dimen_raw_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sqlstr is correct?
                    assert generated_sqlstr != ""

    idea_stageble_dimen_list = sorted(list(expected_idea_stagable_dimens))
    print(f"{expected_idea_stagable_dimens=}")
    assert idea_dimen_combo_checked_count == 680
    assert idea_raw2dimen_count == 100
    assert IDEA_STAGEBLE_PUT_DIMENS == expected_idea_stagable_dimens


def test_IDEA_STAGEBLE_DEL_DIMENS_HasAll_idea_numbersForAll_dimens():
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
        create_fisc_prime_tables(cursor)
        create_bud_prime_tables(cursor)

        idea_raw2dimen_count = 0
        idea_dimen_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        x_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            dimen_config = idea_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get("jkeys").keys())
            dimen_key_columns = get_default_sorted_list(dimen_key_columns)
            dimen_key_columns[-1] = get_delete_key_name(dimen_key_columns[-1])
            dimen_key_columns = set(dimen_key_columns)
            for idea_number in sorted_idea_numbers:
                src_columns = get_table_columns(cursor, f"{idea_number}_raw")
                expected_stagable = dimen_key_columns.issubset(src_columns)
                src_tablename = f"{idea_number}_raw"
                gen_stablable = required_columns_exist(
                    cursor, src_tablename, dimen_key_columns
                )
                assert expected_stagable == gen_stablable

                idea_dimen_combo_checked_count += 1
                if required_columns_exist(cursor, src_tablename, dimen_key_columns):
                    x_idea_stagable_dimens.get(idea_number).append(x_dimen)
                    idea_raw2dimen_count += 1
                    src_cols_set = set(src_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    print(
                        f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}"
                    )
                    generated_sqlstr = get_idea_into_dimen_raw_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sqlstr is correct?
                    assert generated_sqlstr != ""
    expected_idea_stagable_dimens = {
        x_idea_number: stagable_dimens
        for x_idea_number, stagable_dimens in x_idea_stagable_dimens.items()
        if stagable_dimens != []
    }
    idea_stageble_dimen_list = sorted(list(expected_idea_stagable_dimens))
    print(f"{expected_idea_stagable_dimens=}")
    assert idea_dimen_combo_checked_count == 680
    assert idea_raw2dimen_count == 10
    assert IDEA_STAGEBLE_DEL_DIMENS == expected_idea_stagable_dimens


def test_CREATE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
  {fisc_tag_str()} TEXT
, {event_int_str()} INTEGER
, agg_time INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_FISC_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = f"""
INSERT INTO fisc_event_time_agg ({fisc_tag_str()}, {event_int_str()}, agg_time)
SELECT {fisc_tag_str()}, {event_int_str()}, agg_time
FROM (
    SELECT {fisc_tag_str()}, {event_int_str()}, {tran_time_str()} as agg_time
    FROM fisc_cashbook_raw
    GROUP BY {fisc_tag_str()}, {event_int_str()}, {tran_time_str()}
    UNION 
    SELECT {fisc_tag_str()}, {event_int_str()}, {deal_time_str()} as agg_time
    FROM fisc_dealunit_raw
    GROUP BY {fisc_tag_str()}, {event_int_str()}, {deal_time_str()}
)
ORDER BY {fisc_tag_str()}, {event_int_str()}, agg_time
;
"""
    # WHEN / THEN
    assert INSERT_FISC_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


def test_UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_UPDATE_sqlstr = f"""
WITH EventTimeOrdered AS (
    SELECT {fisc_tag_str()}, {event_int_str()}, agg_time,
           LAG(agg_time) OVER (PARTITION BY {fisc_tag_str()} ORDER BY {event_int_str()}) AS prev_agg_time
    FROM fisc_event_time_agg
)
UPDATE fisc_event_time_agg
SET error_message = CASE 
         WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
         THEN 'not sorted'
         ELSE 'sorted'
       END 
FROM EventTimeOrdered
WHERE EventTimeOrdered.{event_int_str()} = fisc_event_time_agg.{event_int_str()}
    AND EventTimeOrdered.{fisc_tag_str()} = fisc_event_time_agg.{fisc_tag_str()}
    AND EventTimeOrdered.agg_time = fisc_event_time_agg.agg_time
;
"""
    # WHEN / THEN
    assert UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


def test_CREATE_FISC_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
  {fisc_tag_str()} TEXT
, {owner_name_str()} TEXT
, {event_int_str()} INTEGER
, {deal_time_str()} INTEGER
, error_message TEXT
)
;
"""
    # WHEN / THEN
    assert CREATE_FISC_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


def test_INSERT_FISC_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_INSERT_sqlstr = f"""
INSERT INTO fisc_ote1_agg ({fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()})
SELECT {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
FROM (
    SELECT {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
    FROM fisc_dealunit_raw
    GROUP BY {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
)
ORDER BY {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
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
    fu1_select_sqlstrs = get_fisc_fu1_select_sqlstrs(fisc_tag=a23_str)

    # THEN
    gen_fisccash_sqlstr = fu1_select_sqlstrs.get(fisc_cashbook_str())
    gen_fiscdeal_sqlstr = fu1_select_sqlstrs.get(fisc_dealunit_str())
    gen_fischour_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_hour_str())
    gen_fiscmont_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_month_str())
    gen_fiscweek_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_weekday_str())
    gen_fiscoffi_sqlstr = fu1_select_sqlstrs.get(fisc_timeoffi_str())
    gen_fiscunit_sqlstr = fu1_select_sqlstrs.get(fiscunit_str())
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        fisccash_agg = f"{fisc_cashbook_str()}_agg"
        fiscdeal_agg = f"{fisc_dealunit_str()}_agg"
        fischour_agg = f"{fisc_timeline_hour_str()}_agg"
        fiscmont_agg = f"{fisc_timeline_month_str()}_agg"
        fiscweek_agg = f"{fisc_timeline_weekday_str()}_agg"
        fiscoffi_agg = f"{fisc_timeoffi_str()}_agg"
        fiscunit_agg = f"{fiscunit_str()}_agg"
        where_dict = {fisc_tag_str(): a23_str}
        fisccash_sql = create_select_query(cursor, fisccash_agg, [], where_dict, True)
        fiscdeal_sql = create_select_query(cursor, fiscdeal_agg, [], where_dict, True)
        fischour_sql = create_select_query(cursor, fischour_agg, [], where_dict, True)
        fiscmont_sql = create_select_query(cursor, fiscmont_agg, [], where_dict, True)
        fiscweek_sql = create_select_query(cursor, fiscweek_agg, [], where_dict, True)
        fiscoffi_sql = create_select_query(cursor, fiscoffi_agg, [], where_dict, True)
        fiscunit_sql = create_select_query(cursor, fiscunit_agg, [], where_dict, True)
        print(f"""FISCUNIT_FU1_SELECT_SQLSTR = "{fiscunit_sql}\"""")
        assert gen_fisccash_sqlstr == fisccash_sql
        assert gen_fiscdeal_sqlstr == fiscdeal_sql
        assert gen_fischour_sqlstr == fischour_sql
        assert gen_fiscmont_sqlstr == fiscmont_sql
        assert gen_fiscweek_sqlstr == fiscweek_sql
        assert gen_fiscoffi_sqlstr == fiscoffi_sql
        assert gen_fiscunit_sqlstr == fiscunit_sql
