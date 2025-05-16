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
from src.a02_finance_logic._utils.strs_a02 import (
    fisc_word_str,
    owner_name_str,
    deal_time_str,
    tran_time_str,
)
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_laborlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
    event_int_str,
    face_name_str,
)
from src.a07_calendar_logic._utils.str_a07 import (
    c400_number_str,
    monthday_distortion_str,
    timeline_word_str,
    yr1_jan1_offset_str,
)
from src.a08_bud_atom_logic.atom_config import get_bud_dimens, get_delete_key_name
from src.a15_fisc_logic._utils.str_a15 import (
    fiscunit_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
)
from src.a15_fisc_logic.fisc_config import get_fisc_dimens
from src.a16_pidgin_logic.pidgin_config import get_pidgin_dimens
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_label_str,
    pidgin_name_str,
    pidgin_way_str,
    pidgin_word_str,
    pidgin_core_str,
)
from src.a17_creed_logic._utils.str_a17 import creed_category_str, creed_number_str
from src.a17_creed_logic.creed_config import (
    get_creed_sqlite_types,
    get_creed_config_dict,
    get_creed_numbers,
)
from src.a17_creed_logic.creed_db_tool import (
    get_pragma_table_fetchall,
    get_default_sorted_list,
    get_creed_into_dimen_raw_query,
)
from src.a18_etl_toolbox.fisc_etl_tool import (
    FiscPrimeObjsRef,
    FiscPrimeColumnsRef,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    get_dimen_abbv7,
    create_prime_tablename,
    get_prime_create_table_sqlstrs,
    get_fisc_prime_create_table_sqlstrs,
    get_bud_prime_create_table_sqlstrs,
    create_pidgin_prime_tables,
    create_fisc_prime_tables,
    create_bud_prime_tables,
    create_all_creed_tables,
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
    FISUNIT_AGG_INSERT_SQLSTR,
    get_creed_swordeble_put_dimens,
    CREED_SWORDEBLE_DEL_DIMENS,
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
        f"{bud_idea_awardlink_str()}_put_agg": "BUDAWAR_PUT_AGG",
        f"{bud_idea_awardlink_str()}_put_raw": "BUDAWAR_PUT_RAW",
        f"{bud_idea_factunit_str()}_put_agg": "BUDFACT_PUT_AGG",
        f"{bud_idea_factunit_str()}_put_raw": "BUDFACT_PUT_RAW",
        f"{bud_idea_healerlink_str()}_put_agg": "BUDHEAL_PUT_AGG",
        f"{bud_idea_healerlink_str()}_put_raw": "BUDHEAL_PUT_RAW",
        f"{bud_idea_reason_premiseunit_str()}_put_agg": "BUDPREM_PUT_AGG",
        f"{bud_idea_reason_premiseunit_str()}_put_raw": "BUDPREM_PUT_RAW",
        f"{bud_idea_reasonunit_str()}_put_agg": "BUDREAS_PUT_AGG",
        f"{bud_idea_reasonunit_str()}_put_raw": "BUDREAS_PUT_RAW",
        f"{bud_idea_laborlink_str()}_put_agg": "BUDLABO_PUT_AGG",
        f"{bud_idea_laborlink_str()}_put_raw": "BUDLABO_PUT_RAW",
        f"{bud_ideaunit_str()}_put_agg": "BUDIDEA_PUT_AGG",
        f"{bud_ideaunit_str()}_put_raw": "BUDIDEA_PUT_RAW",
        f"{budunit_str()}_put_agg": "BUDUNIT_PUT_AGG",
        f"{budunit_str()}_put_raw": "BUDUNIT_PUT_RAW",
        f"{bud_acct_membership_str()}_del_agg": "BUDMEMB_DEL_AGG",
        f"{bud_acct_membership_str()}_del_raw": "BUDMEMB_DEL_RAW",
        f"{bud_acctunit_str()}_del_agg": "BUDACCT_DEL_AGG",
        f"{bud_acctunit_str()}_del_raw": "BUDACCT_DEL_RAW",
        f"{bud_idea_awardlink_str()}_del_agg": "BUDAWAR_DEL_AGG",
        f"{bud_idea_awardlink_str()}_del_raw": "BUDAWAR_DEL_RAW",
        f"{bud_idea_factunit_str()}_del_agg": "BUDFACT_DEL_AGG",
        f"{bud_idea_factunit_str()}_del_raw": "BUDFACT_DEL_RAW",
        f"{bud_idea_healerlink_str()}_del_agg": "BUDHEAL_DEL_AGG",
        f"{bud_idea_healerlink_str()}_del_raw": "BUDHEAL_DEL_RAW",
        f"{bud_idea_reason_premiseunit_str()}_del_agg": "BUDPREM_DEL_AGG",
        f"{bud_idea_reason_premiseunit_str()}_del_raw": "BUDPREM_DEL_RAW",
        f"{bud_idea_reasonunit_str()}_del_agg": "BUDREAS_DEL_AGG",
        f"{bud_idea_reasonunit_str()}_del_raw": "BUDREAS_DEL_RAW",
        f"{bud_idea_laborlink_str()}_del_agg": "BUDLABO_DEL_AGG",
        f"{bud_idea_laborlink_str()}_del_raw": "BUDLABO_DEL_RAW",
        f"{bud_ideaunit_str()}_del_agg": "BUDIDEA_DEL_AGG",
        f"{bud_ideaunit_str()}_del_raw": "BUDIDEA_DEL_RAW",
        f"{budunit_str()}_del_agg": "BUDUNIT_DEL_AGG",
        f"{budunit_str()}_del_raw": "BUDUNIT_DEL_RAW",
    }
    return abbrevions.get(tablename)


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH / WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(get_creed_config_dict())


def test_create_prime_tablename_ReturnsObj():
    # ESTABLISH
    budunit_dimen = budunit_str()
    budacct_dimen = bud_acctunit_str()
    budmemb_dimen = bud_acct_membership_str()
    budidea_dimen = bud_ideaunit_str()
    budawar_dimen = bud_idea_awardlink_str()
    budreas_dimen = bud_idea_reasonunit_str()
    budprem_dimen = bud_idea_reason_premiseunit_str()
    budlabor_dimen = bud_idea_laborlink_str()
    budheal_dimen = bud_idea_healerlink_str()
    budfact_dimen = bud_idea_factunit_str()
    fisunit_dimen = fiscunit_str()
    fiscash_dimen = fisc_cashbook_str()
    fisdeal_dimen = fisc_dealunit_str()
    fishour_dimen = fisc_timeline_hour_str()
    fismont_dimen = fisc_timeline_month_str()
    fisweek_dimen = fisc_timeline_weekday_str()
    fisoffi_dimen = fisc_timeoffi_str()
    pidname_dimen = pidgin_name_str()
    pidword_dimen = pidgin_word_str()
    pidwayy_dimen = pidgin_way_str()
    pidlabe_dimen = pidgin_label_str()
    pidcore_dimen = pidgin_core_str()
    raw_str = "raw"
    agg_str = "agg"
    vld_str = "vld"
    put_str = "put"
    del_str = "del"

    # WHEN
    budunit_s_agg_table = create_prime_tablename("budunit", "s", agg_str, put_str)
    budacct_s_agg_table = create_prime_tablename("budacct", "s", agg_str, put_str)
    budmemb_s_agg_table = create_prime_tablename("budmemb", "s", agg_str, put_str)
    budidea_s_agg_table = create_prime_tablename("budidea", "s", agg_str, put_str)
    budawar_s_agg_table = create_prime_tablename("budawar", "s", agg_str, put_str)
    budreas_s_agg_table = create_prime_tablename("budreas", "s", agg_str, put_str)
    budprem_s_agg_table = create_prime_tablename("budprem", "s", agg_str, put_str)
    budlabor_s_agg_table = create_prime_tablename("BUDLABO", "s", agg_str, put_str)
    budheal_s_agg_table = create_prime_tablename("budheal", "s", agg_str, put_str)
    budfact_s_agg_table = create_prime_tablename("budfact", "s", agg_str, put_str)
    budfact_s_del_table = create_prime_tablename("budfact", "s", agg_str, del_str)
    fisunit_s_agg_table = create_prime_tablename("fisunit", "s", agg_str)
    fiscash_s_agg_table = create_prime_tablename("fiscash", "s", agg_str)
    fisdeal_s_agg_table = create_prime_tablename("fisdeal", "s", agg_str)
    fishour_s_agg_table = create_prime_tablename("fishour", "s", agg_str)
    fismont_s_agg_table = create_prime_tablename("fismont", "s", agg_str)
    fisweek_s_agg_table = create_prime_tablename("fisweek", "s", agg_str)
    fisoffi_s_agg_table = create_prime_tablename("fisoffi", "s", agg_str)
    pidname_s_agg_table = create_prime_tablename("pidname", "s", agg_str)
    pidword_s_agg_table = create_prime_tablename("pidword", "s", agg_str)
    pidwayy_s_agg_table = create_prime_tablename("pidwayy", "s", agg_str)
    pidlabe_s_agg_table = create_prime_tablename("pidlabe", "s", agg_str)
    pidlabe_v_agg_table = create_prime_tablename("pidlabe", "v", agg_str)
    pidlabe_s_raw_table = create_prime_tablename("pidlabe", "s", raw_str)
    pidlabe_s_val_table = create_prime_tablename("pidlabe", "s", vld_str)
    pidcore_s_raw_table = create_prime_tablename("pidcore", "s", raw_str)
    pidcore_s_agg_table = create_prime_tablename("pidcore", "s", agg_str)

    # THEN
    assert budunit_s_agg_table == f"{budunit_dimen}_s_put_agg"
    assert budacct_s_agg_table == f"{budacct_dimen}_s_put_agg"
    assert budmemb_s_agg_table == f"{budmemb_dimen}_s_put_agg"
    assert budidea_s_agg_table == f"{budidea_dimen}_s_put_agg"
    assert budawar_s_agg_table == f"{budawar_dimen}_s_put_agg"
    assert budreas_s_agg_table == f"{budreas_dimen}_s_put_agg"
    assert budprem_s_agg_table == f"{budprem_dimen}_s_put_agg"
    assert budlabor_s_agg_table == f"{budlabor_dimen}_s_put_agg"
    assert budheal_s_agg_table == f"{budheal_dimen}_s_put_agg"
    assert budfact_s_agg_table == f"{budfact_dimen}_s_put_agg"
    assert budfact_s_del_table == f"{budfact_dimen}_s_del_agg"
    assert fisunit_s_agg_table == f"{fisunit_dimen}_s_agg"
    assert fiscash_s_agg_table == f"{fiscash_dimen}_s_agg"
    assert fisdeal_s_agg_table == f"{fisdeal_dimen}_s_agg"
    assert fishour_s_agg_table == f"{fishour_dimen}_s_agg"
    assert fismont_s_agg_table == f"{fismont_dimen}_s_agg"
    assert fisweek_s_agg_table == f"{fisweek_dimen}_s_agg"
    assert fisoffi_s_agg_table == f"{fisoffi_dimen}_s_agg"
    assert pidname_s_agg_table == f"{pidname_dimen}_s_agg"
    assert pidword_s_agg_table == f"{pidword_dimen}_s_agg"
    assert pidwayy_s_agg_table == f"{pidwayy_dimen}_s_agg"
    assert pidlabe_s_agg_table == f"{pidlabe_dimen}_s_agg"
    assert pidlabe_v_agg_table == f"{pidlabe_dimen}_v_agg"
    assert pidlabe_s_raw_table == f"{pidlabe_dimen}_s_raw"
    assert pidlabe_s_val_table == f"{pidlabe_dimen}_s_vld"
    assert pidcore_s_raw_table == f"{pidcore_dimen}_s_raw"
    assert pidcore_s_agg_table == f"{pidcore_dimen}_s_agg"


def test_get_fisc_prime_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_fisc_prime_create_table_sqlstrs()

    # THEN
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "fisc"
    }
    sqlite_types = get_creed_sqlite_types()
    for x_dimen in creed_config:
        # print(f"{x_dimen} checking...")
        abbv7 = get_dimen_abbv7(x_dimen)
        x_config = creed_config.get(x_dimen)

        ag_table = f"{x_dimen}_agg"
        ag_sqlstr = create_table_sqlstrs.get(ag_table)
        ag_cols = set(x_config.get("jkeys").keys())
        ag_cols.update(set(x_config.get("jvalues").keys()))
        ag_cols.remove(event_int_str())
        ag_cols.remove(face_name_str())
        ag_cols = get_default_sorted_list(ag_cols)
        # print(f"{ag_cols=}")
        gen_dimen_agg_sqlstr = get_create_table_sqlstr(ag_table, ag_cols, sqlite_types)
        assert ag_sqlstr == gen_dimen_agg_sqlstr

        st_table = f"{x_dimen}_raw"
        st_sqlstr = create_table_sqlstrs.get(st_table)
        st_cols = set(x_config.get("jkeys").keys())
        st_cols.update(set(x_config.get("jvalues").keys()))
        st_cols.add(creed_number_str())
        st_cols.add("error_message")
        st_cols = get_default_sorted_list(st_cols)
        gen_dimen_raw_sqlstr = get_create_table_sqlstr(st_table, st_cols, sqlite_types)
        assert st_sqlstr == gen_dimen_raw_sqlstr

        # print(f'CREATE_{abbv7.upper()}_AGG_SQLSTR= """{gen_dimen_agg_sqlstr}"""')
        # print(f'CREATE_{abbv7.upper()}_RAW_SQLSTR= """{gen_dimen_raw_sqlstr}"""')
        # print(f'"{ag_table}": {ag_table.upper()}_SQLSTR,')
        # print(f'"{st_table}": {st_table.upper()}_SQLSTR,')


def test_get_bud_prime_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_bud_prime_create_table_sqlstrs()

    # THEN
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "bud"
    }
    s_types = get_creed_sqlite_types()
    for x_dimen in creed_config:
        # print(f"{x_dimen} checking...")
        x_config = creed_config.get(x_dimen)

        ag_put_table = f"{x_dimen}_put_agg"
        ag_put_cols = set(x_config.get("jkeys").keys())
        ag_put_cols.update(set(x_config.get("jvalues").keys()))
        ag_put_cols = get_default_sorted_list(ag_put_cols)
        ex_ag_put_sqlstr = get_create_table_sqlstr(ag_put_table, ag_put_cols, s_types)
        # print(f"{ex_ag_put_sqlstr=}")
        # assert create_table_sqlstrs.get(ag_put_table) == ex_ag_put_sqlstr

        ra_put_table = f"{x_dimen}_put_raw"
        ra_put_cols = set(x_config.get("jkeys").keys())
        ra_put_cols.update(set(x_config.get("jvalues").keys()))
        ra_put_cols.add(creed_number_str())
        ra_put_cols.add("error_message")
        ra_put_cols = get_default_sorted_list(ra_put_cols)
        ex_ra_put_sqlstr = get_create_table_sqlstr(ra_put_table, ra_put_cols, s_types)
        # print(f"{ex_ra_put_sqlstr=}")
        # assert create_table_sqlstrs.get(ra_put_table) == ex_ra_put_sqlstr

        ag_del_table = f"{x_dimen}_del_agg"
        ag_del_cols = set(x_config.get("jkeys").keys())
        ag_del_cols = get_default_sorted_list(ag_del_cols)
        ag_del_cols[-1] = get_delete_key_name(ag_del_cols[-1])
        ex_ag_del_sqlstr = get_create_table_sqlstr(ag_del_table, ag_del_cols, s_types)
        # print(f" {ex_ag_del_sqlstr}")
        # assert create_table_sqlstrs.get(ag_del_table) == ex_ag_del_sqlstr

        ra_del_table = f"{x_dimen}_del_raw"
        ra_del_cols = set(x_config.get("jkeys").keys())
        ra_del_cols.add(creed_number_str())
        ra_del_cols.add("error_message")
        ra_del_cols = get_default_sorted_list(ra_del_cols)
        ra_del_cols[-2] = get_delete_key_name(ra_del_cols[-2])
        ex_ra_del_sqlstr = get_create_table_sqlstr(ra_del_table, ra_del_cols, s_types)
        # print(f" {ex_ra_del_sqlstr}")
        # assert create_table_sqlstrs.get(ra_del_table) == ex_ra_del_sqlstr

        print(f'CREATE_{abbv(ra_put_table)}_SQLSTR= """{ex_ra_put_sqlstr}"""')
        print(f'CREATE_{abbv(ag_put_table)}_SQLSTR= """{ex_ag_put_sqlstr}"""')
        print(f'CREATE_{abbv(ra_del_table)}_SQLSTR= """{ex_ra_del_sqlstr}"""')
        print(f'CREATE_{abbv(ag_del_table)}_SQLSTR= """{ex_ag_del_sqlstr}"""')
        # print(f'"{ra_put_table}": CREATE_{abbv(ra_put_table)}_SQLSTR,')
        # print(f'"{ag_put_table}": CREATE_{abbv(ag_put_table)}_SQLSTR,')
        # print(f'"{ra_del_table}": CREATE_{abbv(ra_del_table)}_SQLSTR,')
        # print(f'"{ag_del_table}": CREATE_{abbv(ag_del_table)}_SQLSTR,')
        assert create_table_sqlstrs.get(ra_put_table) == ex_ra_put_sqlstr
        assert create_table_sqlstrs.get(ag_put_table) == ex_ag_put_sqlstr
        assert create_table_sqlstrs.get(ra_del_table) == ex_ra_del_sqlstr
        assert create_table_sqlstrs.get(ag_del_table) == ex_ag_del_sqlstr


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


def test_create_all_creed_tables_CreatesFiscRawTables():
    # ESTABLISH sourcery skip: no-loop-in-tests
    creed_numbers = get_creed_numbers()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        for creed_number in creed_numbers:
            assert db_table_exists(cursor, f"{creed_number}_raw") is False

        # WHEN
        create_all_creed_tables(cursor)

        # THEN
        for creed_number in creed_numbers:
            print(f"{creed_number} checking...")
            assert db_table_exists(cursor, f"{creed_number}_raw")


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
        budawar_pud_agg_table = f"{bud_idea_awardlink_str()}_put_agg"
        budawar_pud_raw_table = f"{bud_idea_awardlink_str()}_put_raw"
        budfact_pud_agg_table = f"{bud_idea_factunit_str()}_put_agg"
        budfact_pud_raw_table = f"{bud_idea_factunit_str()}_put_raw"
        budheal_pud_agg_table = f"{bud_idea_healerlink_str()}_put_agg"
        budheal_pud_raw_table = f"{bud_idea_healerlink_str()}_put_raw"
        budprem_pud_agg_table = f"{bud_idea_reason_premiseunit_str()}_put_agg"
        budprem_pud_raw_table = f"{bud_idea_reason_premiseunit_str()}_put_raw"
        budreas_pud_agg_table = f"{bud_idea_reasonunit_str()}_put_agg"
        budreas_pud_raw_table = f"{bud_idea_reasonunit_str()}_put_raw"
        budlabor_pud_agg_table = f"{bud_idea_laborlink_str()}_put_agg"
        budlabor_pud_raw_table = f"{bud_idea_laborlink_str()}_put_raw"
        budidea_pud_agg_table = f"{bud_ideaunit_str()}_put_agg"
        budidea_pud_raw_table = f"{bud_ideaunit_str()}_put_raw"
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
        assert db_table_exists(cursor, budlabor_pud_agg_table) is False
        assert db_table_exists(cursor, budlabor_pud_raw_table) is False
        assert db_table_exists(cursor, budidea_pud_agg_table) is False
        assert db_table_exists(cursor, budidea_pud_raw_table) is False
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
        assert db_table_exists(cursor, budlabor_pud_agg_table)
        assert db_table_exists(cursor, budlabor_pud_raw_table)
        assert db_table_exists(cursor, budidea_pud_agg_table)
        assert db_table_exists(cursor, budidea_pud_raw_table)
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
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        # if dimen_config.get(creed_category_str()) != "pidgin"
        # if dimen_config.get(creed_category_str()) == "bud"
        if dimen_config.get(creed_category_str()) == "pidgin"
    }

    exclude_cols = {
        creed_number_str(),
        event_int_str(),
        face_name_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_pidgin_prime_tables(cursor)

        for x_dimen in sorted(creed_config):
            # print(f"{x_dimen} checking...")
            x_tablename = f"{x_dimen}_raw"
            dimen_config = creed_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            expected_dimen_sqlstr = create_select_inconsistency_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            print(f"{dimen_focus_columns=}")
            print(f"{get_table_columns(cursor, x_tablename)=}")
            print(
                f'{x_dimen.upper()}_INCONSISTENCY_SQLSTR ="""{expected_dimen_sqlstr}"""'
            )
            current_sqlstr = pidgin_inconsistency_sqlstrs.get(x_dimen)
            print(current_sqlstr)
            assert current_sqlstr == expected_dimen_sqlstr


def test_get_fisc_inconsistency_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    fisc_inconsistency_sqlstrs = get_fisc_inconsistency_sqlstrs()

    # THEN
    assert fisc_inconsistency_sqlstrs.keys() == get_fisc_dimens()
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        # if dimen_config.get(creed_category_str()) != "pidgin"
        # if dimen_config.get(creed_category_str()) == "bud"
        if dimen_config.get(creed_category_str()) == "fisc"
    }

    exclude_cols = {
        creed_number_str(),
        event_int_str(),
        face_name_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_prime_tables(cursor)

        for x_dimen in sorted(creed_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = fisc_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_raw"
            dimen_config = creed_config.get(x_dimen)
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
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "bud"
    }

    exclude_cols = {creed_number_str(), "error_message"}
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_prime_tables(cursor)

        for x_dimen in sorted(creed_config):
            # print(f"{x_dimen} checking...")
            x_sqlstr = bud_inconsistency_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_put_raw"
            dimen_config = creed_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_select_inconsistency_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            print(
                f'{get_dimen_abbv7(x_dimen).upper()}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""'
            )
            assert x_sqlstr == generated_dimen_sqlstr


def test_get_fisc_update_inconsist_error_message_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    fisc_update_error_sqlstrs = get_fisc_update_inconsist_error_message_sqlstrs()

    # THEN
    assert set(fisc_update_error_sqlstrs.keys()) == get_fisc_dimens()
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "fisc"
    }

    exclude_cols = {
        creed_number_str(),
        event_int_str(),
        face_name_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_fisc_prime_tables(cursor)
        create_bud_prime_tables(cursor)

        for x_dimen in creed_config:
            print(f"{x_dimen} checking...")
            x_sqlstr = fisc_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_raw"
            dimen_config = creed_config.get(x_dimen)
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
            print("")
            print(generated_dimen_sqlstr)
            assert x_sqlstr == generated_dimen_sqlstr


def test_get_pidgin_update_inconsist_error_message_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    pidgin_update_error_sqlstrs = get_pidgin_update_inconsist_error_message_sqlstrs()

    # THEN
    assert set(pidgin_update_error_sqlstrs.keys()) == get_pidgin_dimens()
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "pidgin"
    }

    exclude_cols = {
        creed_number_str(),
        event_int_str(),
        face_name_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_pidgin_prime_tables(cursor)

        for x_dimen in creed_config:
            # print(f"{x_dimen} checking...")
            x_sqlstr = pidgin_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_raw"
            dimen_config = creed_config.get(x_dimen)
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
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "bud"
    }

    exclude_cols = {creed_number_str(), "error_message"}
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_prime_tables(cursor)

        for x_dimen in creed_config:
            # print(f"{x_dimen} checking...")
            x_sqlstr = bud_update_error_sqlstrs.get(x_dimen)
            x_tablename = f"{x_dimen}_put_raw"
            dimen_config = creed_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_update_inconsistency_error_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            abbv7 = get_dimen_abbv7(x_dimen)
            print(
                f"""{abbv7.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
            )
            # print(
            #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
            # )
            # print(f"""            {x_sqlstr=}""")
            assert x_sqlstr == generated_dimen_sqlstr


def test_get_fisc_insert_agg_from_raw_sqlstrs_ReturnsObj():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH / WHEN
    fisc_insert_agg_sqlstrs = get_fisc_insert_agg_from_raw_sqlstrs()

    # THEN
    assert set(fisc_insert_agg_sqlstrs.keys()) == get_fisc_dimens()
    x_exclude_cols = {
        creed_number_str(),
        event_int_str(),
        face_name_str(),
        "error_message",
    }
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "fisc"
    }
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)

        for x_dimen in creed_config:
            print(f"{x_dimen} checking...")
            dimen_config = creed_config.get(x_dimen)
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
            focus_cols=[fisc_word_str()],
            exclude_cols=x_exclude_cols,
        )
        assert FISUNIT_AGG_INSERT_SQLSTR == generated_fiscunit_sqlstr
        columns_header = f"""{fisc_word_str()}, {timeline_word_str()}, {c400_number_str()}, {yr1_jan1_offset_str()}, {monthday_distortion_str()}, fund_coin, penny, respect_bit, bridge, job_listen_rotations"""
        tablename = "fiscunit"
        expected_fiscunit_sqlstr = f"""INSERT INTO {tablename}_agg ({columns_header})
SELECT {fisc_word_str()}, MAX({timeline_word_str()}), MAX({c400_number_str()}), MAX({yr1_jan1_offset_str()}), MAX({monthday_distortion_str()}), MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(bridge), MAX(job_listen_rotations)
FROM {tablename}_raw
WHERE error_message IS NULL
GROUP BY {fisc_word_str()}
;
"""
        assert FISUNIT_AGG_INSERT_SQLSTR == expected_fiscunit_sqlstr

    assert len(creed_config) == len(fisc_insert_agg_sqlstrs)


def test_get_pidgin_insert_agg_from_raw_sqlstrs_ReturnsObj():
    # sourcery skip: extract-method, no-loop-in-tests
    # ESTABLISH / WHEN
    pidgin_insert_agg_sqlstrs = get_pidgin_insert_agg_from_raw_sqlstrs()

    # THEN
    assert set(pidgin_insert_agg_sqlstrs.keys()) == get_pidgin_dimens()
    x_exclude_cols = {
        creed_number_str(),
        event_int_str(),
        face_name_str(),
        "error_message",
    }
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "pidgin"
    }
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_pidgin_prime_tables(cursor)

        for x_dimen in creed_config:
            # print(f"{x_dimen} checking...")
            dimen_config = creed_config.get(x_dimen)
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

    assert len(creed_config) == len(pidgin_insert_agg_sqlstrs)


def test_get_bud_insert_put_agg_from_raw_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_insert_agg_sqlstrs = get_bud_insert_put_agg_from_raw_sqlstrs()

    # THEN
    assert set(bud_insert_agg_sqlstrs.keys()) == get_bud_dimens()
    x_exclude_cols = {
        creed_number_str(),
        "error_message",
    }
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "bud"
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_prime_tables(cursor)

        for x_dimen in creed_config:
            print(f"{x_dimen} checking...")
            dimen_config = creed_config.get(x_dimen)
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
            print(
                f'{abbv(agg_tablename)}_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
            )
            assert x_sqlstr == expected_table2table_agg_insert_sqlstr


def test_get_bud_insert_del_agg_from_raw_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    bud_insert_agg_sqlstrs = get_bud_insert_del_agg_from_raw_sqlstrs()

    # THEN
    assert set(bud_insert_agg_sqlstrs.keys()) == get_bud_dimens()
    x_exclude_cols = {
        creed_number_str(),
        "error_message",
    }
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) == "bud"
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_bud_prime_tables(cursor)

        for x_dimen in creed_config:
            # print(f"{x_dimen} checking...")
            dimen_config = creed_config.get(x_dimen)
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
            print(
                f'{abbv(agg_tablename)}_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
            )
            assert x_sqlstr == expected_table2table_agg_insert_sqlstr


def test_get_creed_swordeble_put_dimens_HasAll_creed_numbersForAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) != "pidgin"
        # if dimen_config.get(creed_category_str()) == "fisc"
    }
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_all_creed_tables(cursor)
        create_fisc_prime_tables(cursor)
        create_bud_prime_tables(cursor)

        creed_raw2dimen_count = 0
        creed_dimen_combo_checked_count = 0
        sorted_creed_numbers = sorted(get_creed_numbers())
        expected_creed_swordable_dimens = {i_num: [] for i_num in sorted_creed_numbers}
        for x_dimen in sorted(creed_config):
            dimen_config = creed_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get("jkeys").keys())
            dimen_value_columns = set(dimen_config.get("jvalues").keys())
            for creed_number in sorted_creed_numbers:
                src_columns = get_table_columns(cursor, f"{creed_number}_raw")
                expected_swordable = dimen_key_columns.issubset(src_columns)
                if creed_number == "br00036":
                    print(f"{x_dimen} {creed_number} checking... {src_columns}")
                src_tablename = f"{creed_number}_raw"
                gen_stablable = required_columns_exist(
                    cursor, src_tablename, dimen_key_columns
                )
                assert expected_swordable == gen_stablable

                creed_dimen_combo_checked_count += 1
                if required_columns_exist(cursor, src_tablename, dimen_key_columns):
                    expected_creed_swordable_dimens.get(creed_number).append(x_dimen)
                    creed_raw2dimen_count += 1
                    src_cols_set = set(src_columns)
                    existing_value_col = src_cols_set.intersection(dimen_value_columns)
                    # print(
                    #     f"{x_dimen} {creed_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    # print(
                    #     f"{creed_raw2dimen_count} {creed_number} {x_dimen} keys:{dimen_key_columns}, values: {existing_value_col}"
                    # )
                    generated_sqlstr = get_creed_into_dimen_raw_query(
                        conn_or_cursor=cursor,
                        creed_number=creed_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sqlstr is correct?
                    assert generated_sqlstr != ""

    creed_swordeble_dimen_list = sorted(list(expected_creed_swordable_dimens))
    print(f"{expected_creed_swordable_dimens=}")
    assert creed_dimen_combo_checked_count == 680
    assert creed_raw2dimen_count == 109
    assert get_creed_swordeble_put_dimens() == expected_creed_swordable_dimens


def test_CREED_SWORDEBLE_DEL_DIMENS_HasAll_creed_numbersForAll_dimens():
    # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    # THEN
    creed_config = get_creed_config_dict()
    creed_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in creed_config.items()
        if dimen_config.get(creed_category_str()) != "pidgin"
        # if dimen_config.get(creed_category_str()) == "fisc"
    }
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_all_creed_tables(cursor)
        create_fisc_prime_tables(cursor)
        create_bud_prime_tables(cursor)

        creed_raw2dimen_count = 0
        creed_dimen_combo_checked_count = 0
        sorted_creed_numbers = sorted(get_creed_numbers())
        x_creed_swordable_dimens = {i_num: [] for i_num in sorted_creed_numbers}
        for x_dimen in sorted(creed_config):
            dimen_config = creed_config.get(x_dimen)
            dimen_key_columns = set(dimen_config.get("jkeys").keys())
            dimen_key_columns = get_default_sorted_list(dimen_key_columns)
            dimen_key_columns[-1] = get_delete_key_name(dimen_key_columns[-1])
            dimen_key_columns = set(dimen_key_columns)
            for creed_number in sorted_creed_numbers:
                src_columns = get_table_columns(cursor, f"{creed_number}_raw")
                expected_swordable = dimen_key_columns.issubset(src_columns)
                src_tablename = f"{creed_number}_raw"
                gen_stablable = required_columns_exist(
                    cursor, src_tablename, dimen_key_columns
                )
                assert expected_swordable == gen_stablable

                creed_dimen_combo_checked_count += 1
                if required_columns_exist(cursor, src_tablename, dimen_key_columns):
                    x_creed_swordable_dimens.get(creed_number).append(x_dimen)
                    creed_raw2dimen_count += 1
                    src_cols_set = set(src_columns)
                    # print(
                    #     f"{x_dimen} {creed_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
                    # )
                    print(
                        f"{creed_raw2dimen_count} {creed_number} {x_dimen} keys:{dimen_key_columns}"
                    )
                    generated_sqlstr = get_creed_into_dimen_raw_query(
                        conn_or_cursor=cursor,
                        creed_number=creed_number,
                        x_dimen=x_dimen,
                        x_jkeys=dimen_key_columns,
                    )
                    # check sqlstr is correct?
                    assert generated_sqlstr != ""
    expected_creed_swordable_dimens = {
        x_creed_number: swordable_dimens
        for x_creed_number, swordable_dimens in x_creed_swordable_dimens.items()
        if swordable_dimens != []
    }
    creed_swordeble_dimen_list = sorted(list(expected_creed_swordable_dimens))
    print(f"{expected_creed_swordable_dimens=}")
    assert creed_dimen_combo_checked_count == 680
    assert creed_raw2dimen_count == 10
    assert CREED_SWORDEBLE_DEL_DIMENS == expected_creed_swordable_dimens


def test_CREATE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
  {fisc_word_str()} TEXT
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
INSERT INTO fisc_event_time_agg ({fisc_word_str()}, {event_int_str()}, agg_time)
SELECT {fisc_word_str()}, {event_int_str()}, agg_time
FROM (
    SELECT {fisc_word_str()}, {event_int_str()}, {tran_time_str()} as agg_time
    FROM fisc_cashbook_raw
    GROUP BY {fisc_word_str()}, {event_int_str()}, {tran_time_str()}
    UNION 
    SELECT {fisc_word_str()}, {event_int_str()}, {deal_time_str()} as agg_time
    FROM fisc_dealunit_raw
    GROUP BY {fisc_word_str()}, {event_int_str()}, {deal_time_str()}
)
ORDER BY {fisc_word_str()}, {event_int_str()}, agg_time
;
"""
    # WHEN / THEN
    assert INSERT_FISC_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


def test_UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_UPDATE_sqlstr = f"""
WITH EventTimeOrdered AS (
    SELECT {fisc_word_str()}, {event_int_str()}, agg_time,
           LAG(agg_time) OVER (PARTITION BY {fisc_word_str()} ORDER BY {event_int_str()}) AS prev_agg_time
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
    AND EventTimeOrdered.{fisc_word_str()} = fisc_event_time_agg.{fisc_word_str()}
    AND EventTimeOrdered.agg_time = fisc_event_time_agg.agg_time
;
"""
    # WHEN / THEN
    assert UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


def test_CREATE_FISC_OTE1_AGG_SQLSTR_Exists():
    # ESTABLISH
    expected_create_table_sqlstr = f"""
CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
  {fisc_word_str()} TEXT
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
INSERT INTO fisc_ote1_agg ({fisc_word_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()})
SELECT {fisc_word_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
FROM (
    SELECT {fisc_word_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
    FROM fisc_dealunit_raw
    GROUP BY {fisc_word_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
)
ORDER BY {fisc_word_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
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
    fu1_select_sqlstrs = get_fisc_fu1_select_sqlstrs(fisc_word=a23_str)

    # THEN
    gen_fiscash_sqlstr = fu1_select_sqlstrs.get(fisc_cashbook_str())
    gen_fisdeal_sqlstr = fu1_select_sqlstrs.get(fisc_dealunit_str())
    gen_fishour_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_hour_str())
    gen_fismont_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_month_str())
    gen_fisweek_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_weekday_str())
    gen_fisoffi_sqlstr = fu1_select_sqlstrs.get(fisc_timeoffi_str())
    gen_fisunit_sqlstr = fu1_select_sqlstrs.get(fiscunit_str())
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        fiscash_agg = f"{fisc_cashbook_str()}_agg"
        fisdeal_agg = f"{fisc_dealunit_str()}_agg"
        fishour_agg = f"{fisc_timeline_hour_str()}_agg"
        fismont_agg = f"{fisc_timeline_month_str()}_agg"
        fisweek_agg = f"{fisc_timeline_weekday_str()}_agg"
        fisoffi_agg = f"{fisc_timeoffi_str()}_agg"
        fiscunit_agg = f"{fiscunit_str()}_agg"
        where_dict = {fisc_word_str(): a23_str}
        fiscash_sql = create_select_query(cursor, fiscash_agg, [], where_dict, True)
        fisdeal_sql = create_select_query(cursor, fisdeal_agg, [], where_dict, True)
        fishour_sql = create_select_query(cursor, fishour_agg, [], where_dict, True)
        fismont_sql = create_select_query(cursor, fismont_agg, [], where_dict, True)
        fisweek_sql = create_select_query(cursor, fisweek_agg, [], where_dict, True)
        fisoffi_sql = create_select_query(cursor, fisoffi_agg, [], where_dict, True)
        fisunit_sql = create_select_query(cursor, fiscunit_agg, [], where_dict, True)
        print(f"""FISUNIT_FU1_SELECT_SQLSTR = "{fisunit_sql}\"""")
        assert gen_fiscash_sqlstr == fiscash_sql
        assert gen_fisdeal_sqlstr == fisdeal_sql
        assert gen_fishour_sqlstr == fishour_sql
        assert gen_fismont_sqlstr == fismont_sql
        assert gen_fisweek_sqlstr == fisweek_sql
        assert gen_fisoffi_sqlstr == fisoffi_sql
        assert gen_fisunit_sqlstr == fisunit_sql
