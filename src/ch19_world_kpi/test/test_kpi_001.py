from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count, get_table_columns
from src.ch02_rope.rope import create_rope
from src.ch18_world_etl.tran_sqlstrs import (
    CREATE_JOB_BLRPLAN_SQLSTR,
    CREATE_MOMENT_VOICE_NETS_SQLSTR,
    create_prime_tablename,
)
from src.ch19_world_kpi.kpi_mstr import create_populate_kpi001_table
from src.ref.keywords import Ch19Keywords as wx


def test_create_populate_kpi001_table_PopulatesTable_Scenario0_NoPledges():
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_voice_net = -55
    bob_voice_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_BLRPLAN_SQLSTR)
        cursor.execute(CREATE_MOMENT_VOICE_NETS_SQLSTR)
        moment_voice_nets_tablename = wx.moment_voice_nets
        insert_sqlstr = f"""INSERT INTO {moment_voice_nets_tablename} ({wx.moment_label}, {wx.belief_name}, {wx.belief_net_amount}) 
VALUES 
  ('{a23_str}', '{bob_str}', {bob_voice_net})
, ('{a23_str}', '{yao_str}', {yao_voice_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2
        moment_kpi001_voice_nets_tablename = wx.moment_kpi001_voice_nets
        assert not db_table_exists(cursor, moment_kpi001_voice_nets_tablename)

        # WHEN
        create_populate_kpi001_table(cursor)

        # THEN
        assert get_table_columns(cursor, moment_kpi001_voice_nets_tablename) == [
            wx.moment_label,
            wx.belief_name,
            "funds",
            "fund_rank",
            "pledges_count",
        ]
        assert get_row_count(cursor, moment_kpi001_voice_nets_tablename)
        select_sqlstr = f"""
        SELECT 
  {wx.moment_label}
, {wx.belief_name}
, funds
, fund_rank
, pledges_count
FROM {moment_kpi001_voice_nets_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (a23_str, bob_str, 600.0, 1, 0),
            (a23_str, yao_str, -55.0, 2, 0),
        ]


def test_create_populate_kpi001_table_PopulatesTable_Scenario1_1pledge():
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_voice_net = -55
    bob_voice_net = 600
    casa_rope = create_rope(a23_str, "casa")

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_MOMENT_VOICE_NETS_SQLSTR)
        moment_voice_nets_tablename = wx.moment_voice_nets
        insert_sqlstr = f"""INSERT INTO {moment_voice_nets_tablename} ({wx.moment_label}, {wx.belief_name}, {wx.belief_net_amount})
VALUES
  ('{a23_str}', '{bob_str}', {bob_voice_net})
, ('{a23_str}', '{yao_str}', {yao_voice_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2

        cursor.execute(CREATE_JOB_BLRPLAN_SQLSTR)
        job_blrplan_tablename = create_prime_tablename("blrplan", "job", None)
        insert_sqlstr = f"""
INSERT INTO {job_blrplan_tablename} ({wx.moment_label}, {wx.belief_name}, {wx.plan_rope}, {wx.pledge})
VALUES ('{a23_str}', '{bob_str}', '{casa_rope}', 1)
"""
        cursor.execute(insert_sqlstr)
        moment_kpi001_voice_nets_tablename = wx.moment_kpi001_voice_nets
        assert not db_table_exists(cursor, moment_kpi001_voice_nets_tablename)

        # WHEN
        create_populate_kpi001_table(cursor)

        # THEN
        assert get_row_count(cursor, moment_kpi001_voice_nets_tablename)
        select_sqlstr = f"""SELECT {wx.moment_label}, {wx.belief_name}, funds, fund_rank, pledges_count FROM {moment_kpi001_voice_nets_tablename}"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (a23_str, bob_str, bob_voice_net, 1, 1),
            (a23_str, yao_str, yao_voice_net, 2, 0),
        ]
