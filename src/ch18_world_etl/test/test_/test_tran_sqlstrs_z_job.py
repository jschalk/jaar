from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_create_table_sqlstr
from src.ch07_belief_logic.belief_config import get_belief_config_dict
from src.ch17_idea.idea_config import get_idea_sqlite_types
from src.ch17_idea.idea_db_tool import get_default_sorted_list
from src.ch18_world_etl.tran_sqlstrs import (
    create_job_tables,
    create_prime_tablename as prime_table,
    get_job_create_table_sqlstrs,
)
from src.ref.keywords import Ch18Keywords as kw


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

        job_table = prime_table(x_dimen, kw.job, None)
        job_cols = {kw.moment_label, kw.belief_name}
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

        blrmemb_job_table = prime_table(kw.belief_voice_membership, kw.job, None)
        blfvoce_job_table = prime_table(kw.belief_voiceunit, kw.job, None)
        blrgrou_job_table = prime_table(kw.belief_groupunit, kw.job, None)
        blrawar_job_table = prime_table(kw.belief_plan_awardunit, kw.job, None)
        blrfact_job_table = prime_table(kw.belief_plan_factunit, kw.job, None)
        blrheal_job_table = prime_table(kw.belief_plan_healerunit, kw.job, None)
        blrcase_job_table = prime_table(kw.belief_plan_reason_caseunit, kw.job, None)
        beliefares_job_table = prime_table(kw.belief_plan_reasonunit, kw.job, None)
        blrlabo_job_table = prime_table(kw.belief_plan_partyunit, kw.job, None)
        blrplan_job_table = prime_table(kw.belief_planunit, kw.job, None)
        blrunit_job_table = prime_table(kw.beliefunit, kw.job, None)
        # blrmemb_job_table = f"{kw.belief_voice_membership}_job"
        # blfvoce_job_table = f"{kw.belief_voiceunit}_job"
        # blrgrou_job_table = f"{kw.belief_groupunit}_job"
        # blrawar_job_table = f"{kw.belief_plan_awardunit}_job"
        # blrfact_job_table = f"{kw.belief_plan_factunit}_job"
        # blrheal_job_table = f"{kw.belief_plan_healerunit}_job"
        # blrcase_job_table = f"{kw.belief_plan_reason_caseunit}_job"
        # beliefares_job_table = f"{kw.belief_plan_reasonunit}_job"
        # blrlabo_job_table = f"{kw.belief_plan_partyunit}_job"
        # blrplan_job_table = f"{kw.belief_planunit}_job"
        # blrunit_job_table = f"{kw.beliefunit}_job"

        assert db_table_exists(cursor, blrmemb_job_table) is False
        assert db_table_exists(cursor, blfvoce_job_table) is False
        assert db_table_exists(cursor, blrgrou_job_table) is False
        assert db_table_exists(cursor, blrawar_job_table) is False
        assert db_table_exists(cursor, blrfact_job_table) is False
        assert db_table_exists(cursor, blrheal_job_table) is False
        assert db_table_exists(cursor, blrcase_job_table) is False
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
        assert db_table_exists(cursor, blfvoce_job_table)
        assert db_table_exists(cursor, blrgrou_job_table)
        assert db_table_exists(cursor, blrawar_job_table)
        assert db_table_exists(cursor, blrfact_job_table)
        assert db_table_exists(cursor, blrheal_job_table)
        assert db_table_exists(cursor, blrcase_job_table)
        assert db_table_exists(cursor, beliefares_job_table)
        assert db_table_exists(cursor, blrlabo_job_table)
        assert db_table_exists(cursor, blrplan_job_table)
        assert db_table_exists(cursor, blrunit_job_table)
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 11
