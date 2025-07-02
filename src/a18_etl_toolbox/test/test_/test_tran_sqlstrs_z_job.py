from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_create_table_sqlstr
from src.a06_owner_logic.test._util.a06_str import (
    belief_label_str,
    owner_acct_membership_str,
    owner_acctunit_str,
    owner_name_str,
    owner_plan_awardlink_str,
    owner_plan_factunit_str,
    owner_plan_healerlink_str,
    owner_plan_laborlink_str,
    owner_plan_reason_premiseunit_str,
    owner_plan_reasonunit_str,
    owner_planunit_str,
    ownerunit_str,
)
from src.a10_owner_calc.owner_calc_config import get_owner_calc_config_dict
from src.a10_owner_calc.test._util.a10_str import owner_groupunit_str
from src.a12_hub_toolbox.test._util.a12_str import job_str
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
    owner_calc_config = get_owner_calc_config_dict()
    for x_dimen in owner_calc_config.keys():
        # print(f"{x_dimen} checking...")
        x_config = owner_calc_config.get(x_dimen)

        job_table = prime_table(x_dimen, job_str(), None)
        job_cols = {belief_label_str(), owner_name_str()}
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
    with sqlite3_connect(":memory:") as belief_db_conn:
        cursor = belief_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0

        plnmemb_job_table = prime_table(owner_acct_membership_str(), job_str(), None)
        plnacct_job_table = prime_table(owner_acctunit_str(), job_str(), None)
        plngrou_job_table = prime_table(owner_groupunit_str(), job_str(), None)
        plnawar_job_table = prime_table(owner_plan_awardlink_str(), job_str(), None)
        plnfact_job_table = prime_table(owner_plan_factunit_str(), job_str(), None)
        plnheal_job_table = prime_table(owner_plan_healerlink_str(), job_str(), None)
        plnprem_job_table = prime_table(
            owner_plan_reason_premiseunit_str(), job_str(), None
        )
        ownerares_job_table = prime_table(owner_plan_reasonunit_str(), job_str(), None)
        plnlabo_job_table = prime_table(owner_plan_laborlink_str(), job_str(), None)
        plnconc_job_table = prime_table(owner_planunit_str(), job_str(), None)
        plnunit_job_table = prime_table(ownerunit_str(), job_str(), None)
        # plnmemb_job_table = f"{owner_acct_membership_str()}_job"
        # plnacct_job_table = f"{owner_acctunit_str()}_job"
        # plngrou_job_table = f"{owner_groupunit_str()}_job"
        # plnawar_job_table = f"{owner_plan_awardlink_str()}_job"
        # plnfact_job_table = f"{owner_plan_factunit_str()}_job"
        # plnheal_job_table = f"{owner_plan_healerlink_str()}_job"
        # plnprem_job_table = f"{owner_plan_reason_premiseunit_str()}_job"
        # ownerares_job_table = f"{owner_plan_reasonunit_str()}_job"
        # plnlabo_job_table = f"{owner_plan_laborlink_str()}_job"
        # plnconc_job_table = f"{owner_planunit_str()}_job"
        # plnunit_job_table = f"{ownerunit_str()}_job"

        assert db_table_exists(cursor, plnmemb_job_table) is False
        assert db_table_exists(cursor, plnacct_job_table) is False
        assert db_table_exists(cursor, plngrou_job_table) is False
        assert db_table_exists(cursor, plnawar_job_table) is False
        assert db_table_exists(cursor, plnfact_job_table) is False
        assert db_table_exists(cursor, plnheal_job_table) is False
        assert db_table_exists(cursor, plnprem_job_table) is False
        assert db_table_exists(cursor, ownerares_job_table) is False
        assert db_table_exists(cursor, plnlabo_job_table) is False
        assert db_table_exists(cursor, plnconc_job_table) is False
        assert db_table_exists(cursor, plnunit_job_table) is False

        # WHEN
        create_job_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        assert db_table_exists(cursor, plnmemb_job_table)
        assert db_table_exists(cursor, plnacct_job_table)
        assert db_table_exists(cursor, plngrou_job_table)
        assert db_table_exists(cursor, plnawar_job_table)
        assert db_table_exists(cursor, plnfact_job_table)
        assert db_table_exists(cursor, plnheal_job_table)
        assert db_table_exists(cursor, plnprem_job_table)
        assert db_table_exists(cursor, ownerares_job_table)
        assert db_table_exists(cursor, plnlabo_job_table)
        assert db_table_exists(cursor, plnconc_job_table)
        assert db_table_exists(cursor, plnunit_job_table)
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 11
