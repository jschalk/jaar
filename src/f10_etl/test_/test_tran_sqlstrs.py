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
from src.f04_gift.atom_config import face_name_str, fiscal_title_str, get_bud_dimens
from src.f07_fiscal.fiscal_config import fiscalunit_str, get_fiscal_dimens
from src.f08_pidgin.pidgin_config import event_int_str, pidginunit_str
from src.f09_idea.idea_config import (
    idea_number_str,
    get_idea_sqlite_types,
    get_idea_config_dict,
    idea_type_str,
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
    get_bud_update_inconsist_error_message_sqlstrs,
    get_fiscal_update_inconsist_error_message_sqlstrs,
    get_bud_insert_agg_from_staging_sqlstrs,
    get_fiscal_insert_agg_from_staging_sqlstrs,
    FISCALUNIT_AGG_INSERT_SQLSTR,
    IDEA_STAGEABLE_DIMENS,
)
from sqlite3 import connect as sqlite3_connect


def test_get_fiscal_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_fiscal_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_type_str()) == fiscalunit_str()
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
        gen_cat_agg_sqlstr = get_create_table_sqlstr(ag_table, ag_cols, sqlite_types)
        assert ag_sqlstr == gen_cat_agg_sqlstr

        st_table = f"{x_dimen}_staging"
        st_sqlstr = create_table_sqlstrs.get(st_table)
        st_cols = set(x_config.get("jkeys").keys())
        st_cols.update(set(x_config.get("jvalues").keys()))
        st_cols.add(idea_number_str())
        st_cols.add("error_message")
        st_cols = get_custom_sorted_list(st_cols)
        gen_cat_stage_sqlstr = get_create_table_sqlstr(st_table, st_cols, sqlite_types)
        assert st_sqlstr == gen_cat_stage_sqlstr

        # print(f'{ag_table.upper()}_SQLSTR= """{gen_cat_agg_sqlstr}"""')
        # print(f'{st_table.upper()}_SQLSTR= """{gen_cat_stage_sqlstr}"""')
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
        if dimen_config.get(idea_type_str()) == budunit_str()
    }
    sqlite_types = get_idea_sqlite_types()
    for x_dimen in idea_config:
        print(f"{x_dimen} checking...")
        x_config = idea_config.get(x_dimen)

        ag_table = f"{x_dimen}_agg"
        ag_sqlstr = create_table_sqlstrs.get(ag_table)
        ag_cols = set(x_config.get("jkeys").keys())
        ag_cols.update(set(x_config.get("jvalues").keys()))
        ag_cols = get_custom_sorted_list(ag_cols)
        gen_cat_agg_sqlstr = get_create_table_sqlstr(ag_table, ag_cols, sqlite_types)
        assert ag_sqlstr == gen_cat_agg_sqlstr

        st_table = f"{x_dimen}_staging"
        st_sqlstr = create_table_sqlstrs.get(st_table)
        st_cols = set(x_config.get("jkeys").keys())
        st_cols.update(set(x_config.get("jvalues").keys()))
        st_cols.add(idea_number_str())
        st_cols.add("error_message")
        st_cols = get_custom_sorted_list(st_cols)
        gen_cat_stage_sqlstr = get_create_table_sqlstr(st_table, st_cols, sqlite_types)
        assert st_sqlstr == gen_cat_stage_sqlstr

        # print(f'CREATE_{ag_table.upper()}_SQLSTR= """{gen_cat_agg_sqlstr}"""')
        # print(f'CREATE_{st_table.upper()}_SQLSTR= """{gen_cat_stage_sqlstr}"""')
        # print(f'"{ag_table}": {ag_table.upper()}_SQLSTR,')
        # print(f'"{st_table}": {st_table.upper()}_SQLSTR,')


def test_get_fiscal_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    fiscal_create_table_sqlstrs = get_fiscal_create_table_sqlstrs()

    # THEN
    assert fiscal_create_table_sqlstrs
    fiscal_dimens = get_fiscal_dimens()
    expected_fiscal_tablenames = {f"{x_cat}_agg" for x_cat in fiscal_dimens}
    expected_fiscal_tablenames.update({f"{x_cat}_staging" for x_cat in fiscal_dimens})
    print(f"{expected_fiscal_tablenames=}")
    assert set(fiscal_create_table_sqlstrs.keys()) == expected_fiscal_tablenames


def test_get_bud_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    bud_create_table_sqlstrs = get_bud_create_table_sqlstrs()

    # THEN
    assert bud_create_table_sqlstrs
    bud_dimens = get_bud_dimens()
    expected_bud_tablenames = {f"{x_cat}_agg" for x_cat in bud_dimens}
    expected_bud_tablenames.update({f"{x_cat}_staging" for x_cat in bud_dimens})
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
        assert db_table_exists(cursor, "bud_acct_membership_agg") is False
        assert db_table_exists(cursor, "bud_acct_membership_staging") is False
        assert db_table_exists(cursor, "bud_acctunit_agg") is False
        assert db_table_exists(cursor, "bud_acctunit_staging") is False
        assert db_table_exists(cursor, "bud_item_awardlink_agg") is False
        assert db_table_exists(cursor, "bud_item_awardlink_staging") is False
        assert db_table_exists(cursor, "bud_item_factunit_agg") is False
        assert db_table_exists(cursor, "bud_item_factunit_staging") is False
        assert db_table_exists(cursor, "bud_item_healerlink_agg") is False
        assert db_table_exists(cursor, "bud_item_healerlink_staging") is False
        assert db_table_exists(cursor, "bud_item_reason_premiseunit_agg") is False
        assert db_table_exists(cursor, "bud_item_reason_premiseunit_staging") is False
        assert db_table_exists(cursor, "bud_item_reasonunit_agg") is False
        assert db_table_exists(cursor, "bud_item_reasonunit_staging") is False
        assert db_table_exists(cursor, "bud_item_teamlink_agg") is False
        assert db_table_exists(cursor, "bud_item_teamlink_staging") is False
        assert db_table_exists(cursor, "bud_itemunit_agg") is False
        assert db_table_exists(cursor, "bud_itemunit_staging") is False
        assert db_table_exists(cursor, "budunit_agg") is False
        assert db_table_exists(cursor, "budunit_staging") is False

        # WHEN
        create_bud_tables(cursor)

        # THEN
        assert db_table_exists(cursor, "bud_acct_membership_agg")
        assert db_table_exists(cursor, "bud_acct_membership_staging")
        assert db_table_exists(cursor, "bud_acctunit_agg")
        assert db_table_exists(cursor, "bud_acctunit_staging")
        assert db_table_exists(cursor, "bud_item_awardlink_agg")
        assert db_table_exists(cursor, "bud_item_awardlink_staging")
        assert db_table_exists(cursor, "bud_item_factunit_agg")
        assert db_table_exists(cursor, "bud_item_factunit_staging")
        assert db_table_exists(cursor, "bud_item_healerlink_agg")
        assert db_table_exists(cursor, "bud_item_healerlink_staging")
        assert db_table_exists(cursor, "bud_item_reason_premiseunit_agg")
        assert db_table_exists(cursor, "bud_item_reason_premiseunit_staging")
        assert db_table_exists(cursor, "bud_item_reasonunit_agg")
        assert db_table_exists(cursor, "bud_item_reasonunit_staging")
        assert db_table_exists(cursor, "bud_item_teamlink_agg")
        assert db_table_exists(cursor, "bud_item_teamlink_staging")
        assert db_table_exists(cursor, "bud_itemunit_agg")
        assert db_table_exists(cursor, "bud_itemunit_staging")
        assert db_table_exists(cursor, "budunit_agg")
        assert db_table_exists(cursor, "budunit_staging")


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
        # if dimen_config.get(idea_type_str()) != pidginunit_str()
        # if dimen_config.get(idea_type_str()) == budunit_str()
        if dimen_config.get(idea_type_str()) == fiscalunit_str()
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
            cat_config = idea_config.get(x_dimen)
            cat_focus_columns = set(cat_config.get("jkeys").keys())
            generated_cat_sqlstr = create_select_inconsistency_query(
                cursor, x_tablename, cat_focus_columns, exclude_cols
            )
            print(f'{x_dimen}_INCONSISTENCY_SQLSTR ="""{generated_cat_sqlstr}"""')
            assert x_sqlstr == generated_cat_sqlstr


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
        if dimen_config.get(idea_type_str()) == budunit_str()
    }

    exclude_cols = {idea_number_str(), "error_message"}
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_tables(cursor)

        for x_dimen in sorted(idea_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = bud_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_staging"
            cat_config = idea_config.get(x_dimen)
            cat_focus_columns = set(cat_config.get("jkeys").keys())
            generated_cat_sqlstr = create_select_inconsistency_query(
                cursor, x_tablename, cat_focus_columns, exclude_cols
            )
            print(
                f'{x_dimen.upper()}_INCONSISTENCY_SQLSTR ="""{generated_cat_sqlstr}"""'
            )
            assert x_sqlstr == generated_cat_sqlstr


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
        if dimen_config.get(idea_type_str()) == fiscalunit_str()
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
            cat_config = idea_config.get(x_dimen)
            cat_focus_columns = set(cat_config.get("jkeys").keys())
            generated_cat_sqlstr = create_update_inconsistency_error_query(
                cursor, x_tablename, cat_focus_columns, exclude_cols
            )
            # print(
            #     f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_cat_sqlstr}\"\"\""""
            # )
            # print(
            #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
            # )
            # print(f"""            {x_sqlstr=}""")
            assert x_sqlstr == generated_cat_sqlstr


def test_get_bud_update_inconsist_error_message_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_update_error_sqlstrs = get_bud_update_inconsist_error_message_sqlstrs()

    # THEN
    assert set(bud_update_error_sqlstrs.keys()) == get_bud_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_type_str()) == budunit_str()
    }

    exclude_cols = {idea_number_str(), "error_message"}
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_tables(cursor)

        for x_dimen in idea_config:
            # print(f"{x_dimen} checking...")
            x_sqlstr = bud_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_staging"
            cat_config = idea_config.get(x_dimen)
            cat_focus_columns = set(cat_config.get("jkeys").keys())
            generated_cat_sqlstr = create_update_inconsistency_error_query(
                cursor, x_tablename, cat_focus_columns, exclude_cols
            )
            # print(
            #     f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_cat_sqlstr}\"\"\""""
            # )
            # print(
            #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
            # )
            # print(f"""            {x_sqlstr=}""")
            assert x_sqlstr == generated_cat_sqlstr


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
        if dimen_config.get(idea_type_str()) == fiscalunit_str()
    }
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        create_fiscal_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            cat_config = idea_config.get(x_dimen)
            cat_focus_columns = set(cat_config.get("jkeys").keys())
            cat_focus_columns.remove(event_int_str())
            cat_focus_columns.remove(face_name_str())
            cat_focus_columns = get_custom_sorted_list(cat_focus_columns)
            stage_tablename = f"{x_dimen}_staging"
            agg_tablename = f"{x_dimen}_agg"

            generated_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=stage_tablename,
                    dst_table=agg_tablename,
                    focus_cols=cat_focus_columns,
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


def test_get_bud_insert_agg_from_staging_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_insert_agg_sqlstrs = get_bud_insert_agg_from_staging_sqlstrs()

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
        if dimen_config.get(idea_type_str()) == budunit_str()
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_tables(cursor)

        for x_dimen in idea_config:
            print(f"{x_dimen} checking...")
            cat_config = idea_config.get(x_dimen)
            cat_focus_columns = set(cat_config.get("jkeys").keys())
            cat_focus_columns = get_custom_sorted_list(cat_focus_columns)
            stage_tablename = f"{x_dimen}_staging"
            agg_tablename = f"{x_dimen}_agg"

            generated_table2table_agg_insert_sqlstr = (
                create_table2table_agg_insert_query(
                    cursor,
                    src_table=stage_tablename,
                    dst_table=agg_tablename,
                    focus_cols=cat_focus_columns,
                    exclude_cols=x_exclude_cols,
                )
            )
            x_sqlstr = bud_insert_agg_sqlstrs.get(x_dimen)
            # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
            # print(
            #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{generated_table2table_agg_insert_sqlstr}"""'
            # )
            assert x_sqlstr == generated_table2table_agg_insert_sqlstr


def test_idea_into_dimen_ReturnsObj_ForAll_idea_numbersAndAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_type_str()) != pidginunit_str()
        # if dimen_config.get(idea_type_str()) == fiscalunit_str()
    }
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        create_all_idea_tables(cursor)
        create_fiscal_tables(cursor)
        create_bud_tables(cursor)

        idea_stage2dimen_count = 0
        idea_cat_combo_checked_count = 0
        sorted_idea_numbers = sorted(get_idea_numbers())
        idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
        for x_dimen in sorted(idea_config):
            cat_config = idea_config.get(x_dimen)
            cat_key_columns = set(cat_config.get("jkeys").keys())
            cat_value_columns = set(cat_config.get("jvalues").keys())
            for idea_number in sorted_idea_numbers:
                # print(f"{x_dimen} {idea_number} checking...")
                src_columns = get_table_columns(cursor, f"{idea_number}_staging")
                expected_stagable = cat_key_columns.issubset(src_columns)
                src_tablename = f"{idea_number}_staging"
                gen_stablable = is_stageable(cursor, src_tablename, cat_key_columns)
                assert expected_stagable == gen_stablable

                idea_cat_combo_checked_count += 1
                if is_stageable(cursor, src_tablename, cat_key_columns):
                    idea_stagable_dimens.get(idea_number).append(x_dimen)
                    idea_stage2dimen_count += 1
                    src_cols_set = set(src_columns)
                    existing_value_col = src_cols_set.intersection(cat_value_columns)
                    # print(
                    #     f"{x_dimen} {idea_number} checking... {cat_key_columns=} {cat_value_columns=} {src_cols_set=}"
                    # )
                    print(
                        f"{idea_stage2dimen_count} {idea_number} {x_dimen} keys:{cat_key_columns}, values: {existing_value_col}"
                    )
                    generated_sqlstr = get_idea_into_dimen_staging_query(
                        conn_or_cursor=cursor,
                        idea_number=idea_number,
                        x_dimen=x_dimen,
                        x_jkeys=cat_key_columns,
                    )
                    # check sql syntax is correct?
                    assert generated_sqlstr != ""

    idea_stageable_dimen_list = sorted(list(idea_stagable_dimens))
    # print(f"{idea_stagable_dimens=}")
    assert idea_cat_combo_checked_count == 464
    assert idea_stage2dimen_count == 77
    assert IDEA_STAGEABLE_DIMENS == idea_stagable_dimens
