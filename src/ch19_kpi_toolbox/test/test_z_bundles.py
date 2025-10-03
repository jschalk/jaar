from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import (
    db_table_exists,
    get_db_tables,
    get_row_count,
)
from src.ch18_etl_toolbox.tran_sqlstrs import (
    CREATE_JOB_BLRPLAN_SQLSTR,
    CREATE_MOMENT_VOICE_NETS_SQLSTR,
    create_prime_tablename,
)
from src.ch19_kpi_toolbox.kpi_mstr import populate_kpi_bundle
from src.ref.ch19_keywords import Ch19Keywords as wx


def test_populate_kpi_bundle_PopulatesTable_Scenario0_WithDefaultBundleID():
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
        blrplan_job_tablename = create_prime_tablename("BLRPLAN", "job", None)
        insert_sqlstr = f"""INSERT INTO {moment_voice_nets_tablename} ({wx.moment_label}, {wx.belief_name}, {wx.belief_net_amount})
VALUES
  ('{a23_str}', '{bob_str}', {bob_voice_net})
, ('{a23_str}', '{yao_str}', {yao_voice_net})
"""
        cursor.execute(insert_sqlstr)
        assert db_table_exists(cursor, blrplan_job_tablename)
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2
        moment_kpi001_tablename = wx.moment_kpi001_voice_nets
        moment_kpi002_tablename = wx.moment_kpi002_belief_pledges
        assert not db_table_exists(cursor, moment_kpi001_tablename)
        assert not db_table_exists(cursor, moment_kpi002_tablename)

        # WHEN
        populate_kpi_bundle(cursor, wx.default_kpi_bundle)

        # THEN
        assert db_table_exists(cursor, moment_kpi001_tablename)
        assert db_table_exists(cursor, moment_kpi002_tablename)
        assert get_row_count(cursor, moment_kpi001_tablename) == 2
        assert get_row_count(cursor, moment_kpi002_tablename) == 0
        assert set(get_db_tables(db_conn).keys()) == {
            wx.moment_kpi001_voice_nets,
            wx.moment_kpi002_belief_pledges,
            moment_voice_nets_tablename,
            blrplan_job_tablename,
        }


def test_populate_kpi_bundle_PopulatesTable_Scenario1_WithNoBundleID():
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
        populate_kpi_bundle(cursor)

        # THEN
        assert get_row_count(cursor, moment_kpi001_voice_nets_tablename) == 2
        blrplan_job_tablename = create_prime_tablename("BLRPLAN", "job", None)
        assert set(get_db_tables(db_conn).keys()) == {
            wx.moment_kpi001_voice_nets,
            wx.moment_kpi002_belief_pledges,
            moment_voice_nets_tablename,
            blrplan_job_tablename,
        }
