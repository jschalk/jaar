from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_create_table_sqlstr
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a06_bud_logic._test_util.a06_str import (
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_concept_awardlink_str,
    bud_concept_factunit_str,
    bud_concept_healerlink_str,
    bud_concept_laborlink_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_reasonunit_str,
    bud_conceptunit_str,
    budunit_str,
)
from src.a10_bud_calc._test_util.a10_str import bud_groupunit_str
from src.a10_bud_calc.bud_calc_config import get_bud_calc_config_dict
from src.a12_hub_tools._test_util.a12_str import job_str
from src.a17_idea_logic.idea_config import get_idea_sqlite_types
from src.a17_idea_logic.idea_db_tool import get_default_sorted_list
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_job_tables,
    create_prime_tablename as prime_table,
    get_job_create_table_sqlstrs,
)


def test_get_job_create_table_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_job_create_table_sqlstrs()

    # THEN
    s_types = get_idea_sqlite_types()
    bud_calc_config = get_bud_calc_config_dict()
    for x_dimen in bud_calc_config.keys():
        # print(f"{x_dimen} checking...")
        x_config = bud_calc_config.get(x_dimen)

        job_table = prime_table(x_dimen, job_str(), None)
        job_cols = {vow_label_str(), owner_name_str()}
        job_cols.update(set(x_config.get("jkeys").keys()))
        job_cols.update(set(x_config.get("jvalues").keys()))
        job_cols.update(set(x_config.get("jmetrics").keys()))
        job_cols = get_default_sorted_list(job_cols)
        expected_create_sqlstr = get_create_table_sqlstr(job_table, job_cols, s_types)
        job_dimen_abbr = x_config.get("abbreviation").upper()
        print(
            f'CREATE_JOB_{job_dimen_abbr.upper()}_SQLSTR= """{expected_create_sqlstr}"""'
        )
        # print(f'"{job_table}": CREATE_JOB_{job_dimen_abbr}_SQLSTR,')
        assert create_table_sqlstrs.get(job_table) == expected_create_sqlstr


def test_create_job_tables_CreatesTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0

        budmemb_job_table = prime_table(bud_acct_membership_str(), job_str(), None)
        budacct_job_table = prime_table(bud_acctunit_str(), job_str(), None)
        budgrou_job_table = prime_table(bud_groupunit_str(), job_str(), None)
        budawar_job_table = prime_table(bud_concept_awardlink_str(), job_str(), None)
        budfact_job_table = prime_table(bud_concept_factunit_str(), job_str(), None)
        budheal_job_table = prime_table(bud_concept_healerlink_str(), job_str(), None)
        budprem_job_table = prime_table(
            bud_concept_reason_premiseunit_str(), job_str(), None
        )
        budares_job_table = prime_table(bud_concept_reasonunit_str(), job_str(), None)
        budlabo_job_table = prime_table(bud_concept_laborlink_str(), job_str(), None)
        budconc_job_table = prime_table(bud_conceptunit_str(), job_str(), None)
        budunit_job_table = prime_table(budunit_str(), job_str(), None)
        # budmemb_job_table = f"{bud_acct_membership_str()}_job"
        # budacct_job_table = f"{bud_acctunit_str()}_job"
        # budgrou_job_table = f"{bud_groupunit_str()}_job"
        # budawar_job_table = f"{bud_concept_awardlink_str()}_job"
        # budfact_job_table = f"{bud_concept_factunit_str()}_job"
        # budheal_job_table = f"{bud_concept_healerlink_str()}_job"
        # budprem_job_table = f"{bud_concept_reason_premiseunit_str()}_job"
        # budares_job_table = f"{bud_concept_reasonunit_str()}_job"
        # budlabo_job_table = f"{bud_concept_laborlink_str()}_job"
        # budconc_job_table = f"{bud_conceptunit_str()}_job"
        # budunit_job_table = f"{budunit_str()}_job"

        assert db_table_exists(cursor, budmemb_job_table) is False
        assert db_table_exists(cursor, budacct_job_table) is False
        assert db_table_exists(cursor, budgrou_job_table) is False
        assert db_table_exists(cursor, budawar_job_table) is False
        assert db_table_exists(cursor, budfact_job_table) is False
        assert db_table_exists(cursor, budheal_job_table) is False
        assert db_table_exists(cursor, budprem_job_table) is False
        assert db_table_exists(cursor, budares_job_table) is False
        assert db_table_exists(cursor, budlabo_job_table) is False
        assert db_table_exists(cursor, budconc_job_table) is False
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
        assert db_table_exists(cursor, budlabo_job_table)
        assert db_table_exists(cursor, budconc_job_table)
        assert db_table_exists(cursor, budunit_job_table)
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 11
