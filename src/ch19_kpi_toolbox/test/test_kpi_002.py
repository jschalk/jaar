from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.ch02_rope_logic.rope import create_rope
from src.ch18_etl_toolbox.tran_sqlstrs import (
    CREATE_JOB_BLRPLAN_SQLSTR,
    create_prime_tablename,
)
from src.ch19_kpi_toolbox._ref.ch19_keywords import Ch19Keywords as wx
from src.ch19_kpi_toolbox.kpi_mstr import create_populate_kpi002_table


def test_create_populate_kpi002_table_PopulatesTable_Scenario0_NoPledges():
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    bob_str = "Bob"
    casa_rope = create_rope(a23_str, "casa")
    casa_pledge = 0
    casa_active = 0
    casa_task = 0

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_BLRPLAN_SQLSTR)
        job_blrplan_tablename = create_prime_tablename("BLRPLAN", "job", None)
        insert_sqlstr = f"""INSERT INTO {job_blrplan_tablename} (
  {wx.moment_label}
, {wx.belief_name}
, {wx.plan_rope}
, {wx.pledge}
, {wx.active}
, {wx.task}
)
VALUES 
  ('{a23_str}', '{bob_str}', '{casa_rope}', {casa_pledge}, {casa_active}, {casa_task})
, ('{a23_str}', '{yao_str}', '{casa_rope}', {casa_pledge}, {casa_active}, {casa_task})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, job_blrplan_tablename) == 2
        moment_kpi002_belief_pledges_tablename = wx.moment_kpi002_belief_pledges
        assert not db_table_exists(cursor, moment_kpi002_belief_pledges_tablename)

        # WHEN
        create_populate_kpi002_table(cursor)

        # THEN
        assert db_table_exists(cursor, moment_kpi002_belief_pledges_tablename)
        assert get_table_columns(cursor, moment_kpi002_belief_pledges_tablename) == [
            wx.moment_label,
            wx.belief_name,
            wx.plan_rope,
            wx.pledge,
            wx.active,
            wx.task,
        ]
        assert get_row_count(cursor, moment_kpi002_belief_pledges_tablename) == 0


def test_create_populate_kpi002_table_PopulatesTable_Scenario1_TwoPledges():
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    bob_str = "Bob"
    casa_rope = create_rope(a23_str, "casa")
    casa_pledge = 0
    casa_active = 0
    casa_task = 0
    clean_rope = create_rope(casa_rope, "clean")
    clean_pledge = 1
    clean_active = 1
    clean_task = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_BLRPLAN_SQLSTR)
        job_blrplan_tablename = create_prime_tablename("BLRPLAN", "job", None)
        insert_sqlstr = f"""INSERT INTO {job_blrplan_tablename} (
  {wx.moment_label}
, {wx.belief_name}
, {wx.plan_rope}
, {wx.pledge}
, {wx.active}
, {wx.task}
)
VALUES 
  ('{a23_str}', '{bob_str}', '{casa_rope}', {casa_pledge}, {casa_active}, {casa_task})
, ('{a23_str}', '{yao_str}', '{casa_rope}', {casa_pledge}, {casa_active}, {casa_task})
, ('{a23_str}', '{bob_str}', '{clean_rope}', {clean_pledge}, {clean_active}, {clean_task})
, ('{a23_str}', '{yao_str}', '{clean_rope}', {clean_pledge}, {clean_active}, {clean_task})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, job_blrplan_tablename) == 4
        moment_kpi002_belief_pledges_tablename = wx.moment_kpi002_belief_pledges
        assert not db_table_exists(cursor, moment_kpi002_belief_pledges_tablename)

        # WHEN
        create_populate_kpi002_table(cursor)

        # THEN
        assert db_table_exists(cursor, moment_kpi002_belief_pledges_tablename)
        assert get_table_columns(cursor, moment_kpi002_belief_pledges_tablename) == [
            wx.moment_label,
            wx.belief_name,
            wx.plan_rope,
            wx.pledge,
            wx.active,
            wx.task,
        ]
        assert get_row_count(cursor, moment_kpi002_belief_pledges_tablename) == 2
