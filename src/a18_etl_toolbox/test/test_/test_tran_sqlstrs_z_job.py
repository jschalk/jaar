from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_create_table_sqlstr
from src.a06_belief_logic.belief_config import get_belief_config_dict
from src.a17_idea_logic.idea_config import get_idea_sqlite_types
from src.a17_idea_logic.idea_db_tool import get_default_sorted_list
from src.a18_etl_toolbox.test._util.a18_str import (
    belief_groupunit_str,
    belief_name_str,
    belief_plan_awardunit_str,
    belief_plan_factunit_str,
    belief_plan_healerunit_str,
    belief_plan_partyunit_str,
    belief_plan_reason_caseunit_str,
    belief_plan_reasonunit_str,
    belief_planunit_str,
    belief_voice_membership_str,
    belief_voiceunit_str,
    beliefunit_str,
    job_str,
    moment_label_str,
)
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
    belief_config = get_belief_config_dict()
    for x_dimen in belief_config.keys():
        # print(f"{x_dimen} checking...")
        x_config = belief_config.get(x_dimen)

        job_table = prime_table(x_dimen, job_str(), None)
        job_cols = {moment_label_str(), belief_name_str()}
        job_cols.update(set(x_config.get("jkeys").keys()))
        job_cols.update(set(x_config.get("jvalues").keys()))
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
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0

        blrmemb_job_table = prime_table(belief_voice_membership_str(), job_str(), None)
        blrpern_job_table = prime_table(belief_voiceunit_str(), job_str(), None)
        blrgrou_job_table = prime_table(belief_groupunit_str(), job_str(), None)
        blrawar_job_table = prime_table(belief_plan_awardunit_str(), job_str(), None)
        blrfact_job_table = prime_table(belief_plan_factunit_str(), job_str(), None)
        blrheal_job_table = prime_table(belief_plan_healerunit_str(), job_str(), None)
        blrprem_job_table = prime_table(
            belief_plan_reason_caseunit_str(), job_str(), None
        )
        beliefares_job_table = prime_table(
            belief_plan_reasonunit_str(), job_str(), None
        )
        blrlabo_job_table = prime_table(belief_plan_partyunit_str(), job_str(), None)
        blrplan_job_table = prime_table(belief_planunit_str(), job_str(), None)
        blrunit_job_table = prime_table(beliefunit_str(), job_str(), None)
        # blrmemb_job_table = f"{belief_voice_membership_str()}_job"
        # blrpern_job_table = f"{belief_voiceunit_str()}_job"
        # blrgrou_job_table = f"{belief_groupunit_str()}_job"
        # blrawar_job_table = f"{belief_plan_awardunit_str()}_job"
        # blrfact_job_table = f"{belief_plan_factunit_str()}_job"
        # blrheal_job_table = f"{belief_plan_healerunit_str()}_job"
        # blrprem_job_table = f"{belief_plan_reason_caseunit_str()}_job"
        # beliefares_job_table = f"{belief_plan_reasonunit_str()}_job"
        # blrlabo_job_table = f"{belief_plan_partyunit_str()}_job"
        # blrplan_job_table = f"{belief_planunit_str()}_job"
        # blrunit_job_table = f"{beliefunit_str()}_job"

        assert db_table_exists(cursor, blrmemb_job_table) is False
        assert db_table_exists(cursor, blrpern_job_table) is False
        assert db_table_exists(cursor, blrgrou_job_table) is False
        assert db_table_exists(cursor, blrawar_job_table) is False
        assert db_table_exists(cursor, blrfact_job_table) is False
        assert db_table_exists(cursor, blrheal_job_table) is False
        assert db_table_exists(cursor, blrprem_job_table) is False
        assert db_table_exists(cursor, beliefares_job_table) is False
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
        assert db_table_exists(cursor, beliefares_job_table)
        assert db_table_exists(cursor, blrlabo_job_table)
        assert db_table_exists(cursor, blrplan_job_table)
        assert db_table_exists(cursor, blrunit_job_table)
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 11
