from src.a00_data_toolboxs.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
    is_stageable,
    create_select_query,
)
from src.a02_finance_toolboxs.deal import fisc_title_str, owner_name_str
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
from src.a10_fund_metric.fund_metric_config import get_fund_metric_config_dict
from src.a17_idea_logic.idea_config import get_idea_sqlite_types
from src.a17_idea_logic.idea_db_tool import get_default_sorted_list
from src.a20_lobby_db_toolbox.lobby_sqlstrs import (
    get_job_create_table_sqlstrs,
    create_job_tables,
)
from sqlite3 import connect as sqlite3_connect


def test_get_job_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_job_create_table_sqlstrs()

    # THEN
    s_types = get_idea_sqlite_types()
    fund_metric_config = get_fund_metric_config_dict()
    for x_dimen in fund_metric_config.keys():
        # print(f"{x_dimen} checking...")
        x_config = fund_metric_config.get(x_dimen)

        job_table = f"{x_dimen}_job"
        job_cols = {fisc_title_str(), owner_name_str()}
        job_cols.update(set(x_config.get("jkeys").keys()))
        job_cols.update(set(x_config.get("jvalues").keys()))
        job_cols.update(set(x_config.get("jmetrics").keys()))
        job_cols = get_default_sorted_list(job_cols)
        expected_create_sqlstr = get_create_table_sqlstr(job_table, job_cols, s_types)
        job_dimen_abbr = x_config.get("abbreviation").upper()
        print(f'CREATE_job_{job_dimen_abbr}_SQLSTR= """{expected_create_sqlstr}"""')
        # print(f'"{job_table}": CREATE_job_{job_dimen_abbr}_SQLSTR,')
        assert create_table_sqlstrs.get(job_table) == expected_create_sqlstr


def test_create_job_tables_CreatesTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0

        budmemb_job_table = f"{bud_acct_membership_str()}_job"
        budacct_job_table = f"{bud_acctunit_str()}_job"
        budgrou_job_table = f"{bud_groupunit_str()}_job"
        budawar_job_table = f"{bud_item_awardlink_str()}_job"
        budfact_job_table = f"{bud_item_factunit_str()}_job"
        budheal_job_table = f"{bud_item_healerlink_str()}_job"
        budprem_job_table = f"{bud_item_reason_premiseunit_str()}_job"
        budares_job_table = f"{bud_item_reasonunit_str()}_job"
        budteam_job_table = f"{bud_item_teamlink_str()}_job"
        buditem_job_table = f"{bud_itemunit_str()}_job"
        budunit_job_table = f"{budunit_str()}_job"

        assert db_table_exists(cursor, budmemb_job_table) is False
        assert db_table_exists(cursor, budacct_job_table) is False
        assert db_table_exists(cursor, budgrou_job_table) is False
        assert db_table_exists(cursor, budawar_job_table) is False
        assert db_table_exists(cursor, budfact_job_table) is False
        assert db_table_exists(cursor, budheal_job_table) is False
        assert db_table_exists(cursor, budprem_job_table) is False
        assert db_table_exists(cursor, budares_job_table) is False
        assert db_table_exists(cursor, budteam_job_table) is False
        assert db_table_exists(cursor, buditem_job_table) is False
        assert db_table_exists(cursor, budunit_job_table) is False

        # WHEN
        create_job_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        assert db_table_exists(cursor, budmemb_job_table)
        assert db_table_exists(cursor, budacct_job_table)
        assert db_table_exists(cursor, budgrou_job_table)
        assert db_table_exists(cursor, budawar_job_table)
        assert db_table_exists(cursor, budfact_job_table)
        assert db_table_exists(cursor, budheal_job_table)
        assert db_table_exists(cursor, budprem_job_table)
        assert db_table_exists(cursor, budares_job_table)
        assert db_table_exists(cursor, budteam_job_table)
        assert db_table_exists(cursor, buditem_job_table)
        assert db_table_exists(cursor, budunit_job_table)
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 11


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

#     expected_budunit_unit_select_SQLSTR = """CREATE TABLE IF NOT EXISTS budunit_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, credor_respect REAL, debtor_respect REAL, fund_pool REAL, max_tree_traverse INTEGER, tally REAL, fund_coin REAL, penny REAL, respect_bit REAL)"""
#     expected_budACCT_acct_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acctunit_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, acct_name TEXT, credit_belief REAL, debtit_belief REAL)"""
#     expected_budMEMB_memb_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_acct_membership_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, acct_name TEXT, group_label TEXT, credit_vote REAL, debtit_vote REAL)"""
#     expected_budITEM_item_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_itemunit_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, parent_road TEXT, item_title TEXT, begin REAL, close REAL, addin REAL, numor REAL, denom REAL, morph INTEGER, gogo_want REAL, stop_want REAL, mass REAL, pledge INTEGER, problem_bool INTEGER)"""
#     expected_budAWAR_awar_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_awardlink_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, road TEXT, awardee_tag TEXT, give_force REAL, take_force REAL)"""
#     expected_budPREM_reas_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reason_premiseunit_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, road TEXT, base TEXT, need TEXT, nigh REAL, open REAL, divisor REAL)"""
#     expected_budREAS_prem_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_reasonunit_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, road TEXT, base TEXT, base_item_active_requisite TEXT)"""
#     expected_budTEAM_team_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_teamlink_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, road TEXT, team_tag TEXT)"""
#     expected_budHEAL_heal_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_healerlink_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, road TEXT, healer_name TEXT)"""
#     expected_budFACT_fact_select_SQLSTR = """CREATE TABLE IF NOT EXISTS bud_item_factunit_put_agg (face_name TEXT, {event_int_str()} INTEGER, {fisc_title_str()} TEXT, {owner_name_str()} TEXT, road TEXT, base TEXT, pick TEXT, fopen REAL, fnigh REAL)"""

#     assert gen_budcash_sqlstr == expected_budcash_sqlstr
#     assert gen_buddeal_sqlstr == expected_buddeal_sqlstr
#     assert gen_budhour_sqlstr == expected_budhour_sqlstr
#     assert gen_budmont_sqlstr == expected_budmont_sqlstr
#     assert gen_budweek_sqlstr == expected_budweek_sqlstr
#     assert gen_budoffi_sqlstr == expected_budoffi_sqlstr
#     assert gen_budunit_sqlstr == expected_budunit_sqlstr
