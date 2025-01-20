from src.f00_instrument.db_toolbox import (
    db_table_exists,
    create_inconsistency_query,
    get_create_table_sqlstr,
    create_agg_insert_query,
)
from src.f01_road.finance_tran import time_int_str
from src.f02_bud.bud_tool import budunit_str
from src.f04_gift.atom_config import (
    face_name_str,
    fiscal_title_str,
    owner_name_str,
    acct_name_str,
)
from src.f07_fiscal.fiscal_config import (
    fiscalunit_str,
    hour_title_str,
    month_title_str,
    weekday_title_str,
)
from src.f08_pidgin.pidgin_config import event_int_str, pidginunit_str
from src.f09_idea.idea_config import (
    idea_number_str,
    get_idea_sqlite_types,
    get_idea_config_dict,
    idea_type_str,
)
from src.f09_idea.pandas_tool import get_pragma_table_fetchall, get_custom_sorted_list
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f10_etl.tran_sqlstrs import (
    get_all_idea_create_table_sqlstrs,
    get_fiscal_create_table_sqlstrs,
    get_bud_create_table_sqlstrs,
    create_fiscal_tables,
    create_bud_tables,
    get_all_inconsistency_sqlstrs,
    get_fiscal_inconsistency_sqlstrs,
    FISCALUNIT_AGG_INSERT_SQLSTR,
    FISCALDEAL_AGG_INSERT_SQLSTR,
    FISCALCASH_AGG_INSERT_SQLSTR,
    FISCALHOUR_AGG_INSERT_SQLSTR,
    FISCALMONT_AGG_INSERT_SQLSTR,
    FISCALWEEK_AGG_INSERT_SQLSTR,
)
from sqlite3 import connect as sqlite3_connect


def test_get_all_idea_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_all_idea_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_category: category_config
        for x_category, category_config in idea_config.items()
        if category_config.get(idea_type_str()) != pidginunit_str()
    }
    sqlite_types = get_idea_sqlite_types()
    for x_category in idea_config:
        # print(f"{x_category} checking...")
        x_config = idea_config.get(x_category)

        ag_table = f"{x_category}_agg"
        ag_sqlstr = create_table_sqlstrs.get(ag_table)
        ag_cols = set(x_config.get("jkeys").keys())
        ag_cols.update(set(x_config.get("jvalues").keys()))
        ag_cols.remove(event_int_str())
        ag_cols.remove(face_name_str())
        ag_cols = get_custom_sorted_list(ag_cols)
        gen_cat_agg_sqlstr = get_create_table_sqlstr(ag_table, ag_cols, sqlite_types)
        assert ag_sqlstr == gen_cat_agg_sqlstr

        st_table = f"{x_category}_staging"
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


def test_get_fiscal_create_table_sqlstrs_ReturnsObj():
    # ESTABLISH / WHEN
    fiscal_create_table_sqlstrs = get_fiscal_create_table_sqlstrs()

    # THEN
    assert fiscal_create_table_sqlstrs
    idea_config = get_idea_config_dict()
    expected_fiscal_tablenames = {
        f"{x_category}_agg"
        for x_category, category_config in idea_config.items()
        if category_config.get(idea_type_str()) == fiscalunit_str()
    }
    expected_fiscal_tablenames.update(
        {
            f"{x_category}_staging"
            for x_category, category_config in idea_config.items()
            if category_config.get(idea_type_str()) == fiscalunit_str()
        }
    )
    print(f"{expected_fiscal_tablenames=}")
    assert set(fiscal_create_table_sqlstrs.keys()) == expected_fiscal_tablenames


def test_get_bud_create_table_sqlstrs_ReturnsObj():
    # ESTABLISH / WHEN
    bud_create_table_sqlstrs = get_bud_create_table_sqlstrs()

    # THEN
    assert bud_create_table_sqlstrs
    idea_config = get_idea_config_dict()
    expected_bud_tablenames = {
        f"{x_category}_agg"
        for x_category, category_config in idea_config.items()
        if category_config.get(idea_type_str()) == budunit_str()
    }
    expected_bud_tablenames.update(
        {
            f"{x_category}_staging"
            for x_category, category_config in idea_config.items()
            if category_config.get(idea_type_str()) == budunit_str()
        }
    )
    print(f"{expected_bud_tablenames=}")
    assert set(bud_create_table_sqlstrs.keys()) == expected_bud_tablenames


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
    # ESTABLISH / WHEN
    fiscal_inconsistency_sqlstrs = get_fiscal_inconsistency_sqlstrs()

    # THEN
    assert fiscal_inconsistency_sqlstrs
    idea_config = get_idea_config_dict()
    fiscal_config = {
        x_category: category_config
        for x_category, category_config in idea_config.items()
        if category_config.get(idea_type_str()) == fiscalunit_str()
    }
    expected_fiscal_cateogrys = fiscal_config.keys()
    assert fiscal_inconsistency_sqlstrs.keys() == expected_fiscal_cateogrys


def test_get_all_inconsistency_sqlstrs_ReturnsObj():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH / WHEN
    all_inconsistency_sqlstrs = get_all_inconsistency_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    idea_config = {
        x_category: category_config
        for x_category, category_config in idea_config.items()
        # if category_config.get(idea_type_str()) != pidginunit_str()
        if category_config.get(idea_type_str()) == budunit_str()
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

        for x_category in idea_config:
            print(f"{x_category} checking...")
            x_sqlstr = all_inconsistency_sqlstrs.get(x_category)
            x_tablename = f"{x_category}_staging"
            cat_config = idea_config.get(x_category)
            cat_focus_columns = set(cat_config.get("jkeys").keys())
            cat_focus_columns.remove(event_int_str())
            cat_focus_columns.remove(face_name_str())
            generated_cat_sqlstr = create_inconsistency_query(
                cursor, x_tablename, cat_focus_columns, exclude_cols
            )
            # print(f"{generated_cat_sqlstr=}")
            assert x_sqlstr == generated_cat_sqlstr


def test_GlobalVairableAGG_INSERT_SQLSTR_ReturnsObj():
    # sourcery skip: extract-method
    # ESTABLISH
    x_objs = FiscalPrimeObjsRef()
    x_cols = FiscalPrimeColumnsRef()
    x_exclude_cols = {
        idea_number_str(),
        face_name_str(),
        event_int_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)

        # WHEN
        generated_fiscalunit_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.unit_stage_tablename,
            dst_table=x_objs.unit_agg_tablename,
            focus_cols=[fiscal_title_str()],
            exclude_cols=x_exclude_cols,
        )

        # THEN
        print(f" {generated_fiscalunit_sqlstr=}")
        print(f"{FISCALUNIT_AGG_INSERT_SQLSTR=}")
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

        # WHEN / THEN
        generated_fiscaldeal_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.deal_stage_tablename,
            dst_table=x_objs.deal_agg_tablename,
            focus_cols=[fiscal_title_str(), owner_name_str(), time_int_str()],
            exclude_cols=x_exclude_cols,
        )
        assert FISCALDEAL_AGG_INSERT_SQLSTR == generated_fiscaldeal_sqlstr

        # WHEN / THEN
        cash_focus_cols = [
            fiscal_title_str(),
            owner_name_str(),
            acct_name_str(),
            time_int_str(),
        ]
        generated_fiscalcash_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.cash_stage_tablename,
            dst_table=x_objs.cash_agg_tablename,
            focus_cols=cash_focus_cols,
            exclude_cols=x_exclude_cols,
        )
        assert FISCALCASH_AGG_INSERT_SQLSTR == generated_fiscalcash_sqlstr

        # WHEN / THEN
        generated_fiscalhour_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.hour_stage_tablename,
            dst_table=x_objs.hour_agg_tablename,
            focus_cols=[fiscal_title_str(), hour_title_str()],
            exclude_cols=x_exclude_cols,
        )
        assert FISCALHOUR_AGG_INSERT_SQLSTR == generated_fiscalhour_sqlstr

        # WHEN / THEN
        generated_fiscalmont_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.mont_stage_tablename,
            dst_table=x_objs.mont_agg_tablename,
            focus_cols=[fiscal_title_str(), month_title_str()],
            exclude_cols=x_exclude_cols,
        )
        assert FISCALMONT_AGG_INSERT_SQLSTR == generated_fiscalmont_sqlstr

        # WHEN / THEN
        generated_fiscalweek_sqlstr = create_agg_insert_query(
            fiscal_db_conn,
            src_table=x_objs.week_stage_tablename,
            dst_table=x_objs.week_agg_tablename,
            focus_cols=[fiscal_title_str(), weekday_title_str()],
            exclude_cols=x_exclude_cols,
        )
        assert FISCALWEEK_AGG_INSERT_SQLSTR == generated_fiscalweek_sqlstr
