from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_create_table_sqlstr
from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    believer_name_str,
    believer_partner_membership_str,
    believer_partnerunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_caseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
)
from src.a10_believer_calc.believer_calc_config import get_believer_calc_config_dict
from src.a10_believer_calc.test._util.a10_str import believer_groupunit_str
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
    believer_calc_config = get_believer_calc_config_dict()
    for x_dimen in believer_calc_config.keys():
        # print(f"{x_dimen} checking...")
        x_config = believer_calc_config.get(x_dimen)

        job_table = prime_table(x_dimen, job_str(), None)
        job_cols = {belief_label_str(), believer_name_str()}
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

        blrmemb_job_table = prime_table(
            believer_partner_membership_str(), job_str(), None
        )
        blrpern_job_table = prime_table(believer_partnerunit_str(), job_str(), None)
        blrgrou_job_table = prime_table(believer_groupunit_str(), job_str(), None)
        blrawar_job_table = prime_table(believer_plan_awardlink_str(), job_str(), None)
        blrfact_job_table = prime_table(believer_plan_factunit_str(), job_str(), None)
        blrheal_job_table = prime_table(believer_plan_healerlink_str(), job_str(), None)
        blrprem_job_table = prime_table(
            believer_plan_reason_caseunit_str(), job_str(), None
        )
        believerares_job_table = prime_table(
            believer_plan_reasonunit_str(), job_str(), None
        )
        blrlabo_job_table = prime_table(believer_plan_laborlink_str(), job_str(), None)
        blrplan_job_table = prime_table(believer_planunit_str(), job_str(), None)
        blrunit_job_table = prime_table(believerunit_str(), job_str(), None)
        # blrmemb_job_table = f"{believer_partner_membership_str()}_job"
        # blrpern_job_table = f"{believer_partnerunit_str()}_job"
        # blrgrou_job_table = f"{believer_groupunit_str()}_job"
        # blrawar_job_table = f"{believer_plan_awardlink_str()}_job"
        # blrfact_job_table = f"{believer_plan_factunit_str()}_job"
        # blrheal_job_table = f"{believer_plan_healerlink_str()}_job"
        # blrprem_job_table = f"{believer_plan_reason_caseunit_str()}_job"
        # believerares_job_table = f"{believer_plan_reasonunit_str()}_job"
        # blrlabo_job_table = f"{believer_plan_laborlink_str()}_job"
        # blrplan_job_table = f"{believer_planunit_str()}_job"
        # blrunit_job_table = f"{believerunit_str()}_job"

        assert db_table_exists(cursor, blrmemb_job_table) is False
        assert db_table_exists(cursor, blrpern_job_table) is False
        assert db_table_exists(cursor, blrgrou_job_table) is False
        assert db_table_exists(cursor, blrawar_job_table) is False
        assert db_table_exists(cursor, blrfact_job_table) is False
        assert db_table_exists(cursor, blrheal_job_table) is False
        assert db_table_exists(cursor, blrprem_job_table) is False
        assert db_table_exists(cursor, believerares_job_table) is False
        assert db_table_exists(cursor, blrlabo_job_table) is False
        assert db_table_exists(cursor, blrplan_job_table) is False
        assert db_table_exists(cursor, blrunit_job_table) is False

        # WHEN
        create_job_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        assert db_table_exists(cursor, blrmemb_job_table)
        assert db_table_exists(cursor, blrpern_job_table)
        assert db_table_exists(cursor, blrgrou_job_table)
        assert db_table_exists(cursor, blrawar_job_table)
        assert db_table_exists(cursor, blrfact_job_table)
        assert db_table_exists(cursor, blrheal_job_table)
        assert db_table_exists(cursor, blrprem_job_table)
        assert db_table_exists(cursor, believerares_job_table)
        assert db_table_exists(cursor, blrlabo_job_table)
        assert db_table_exists(cursor, blrplan_job_table)
        assert db_table_exists(cursor, blrunit_job_table)
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 11
