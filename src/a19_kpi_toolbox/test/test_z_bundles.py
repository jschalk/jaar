from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_db_tables,
    get_row_count,
)
from src.a04_reason_logic.test._util.a04_str import belief_label_str, believer_name_str
from src.a18_etl_toolbox.test._util.a18_str import (
    belief_acct_nets_str,
    believer_net_amount_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    CREATE_BELIEF_ACCT_NETS_SQLSTR,
    CREATE_JOB_ONRPLAN_SQLSTR,
    create_prime_tablename,
)
from src.a19_kpi_toolbox.kpi_mstr import get_default_kpi_bundle, populate_kpi_bundle
from src.a19_kpi_toolbox.test._util.a19_str import belief_kpi001_acct_nets_str


def test_populate_kpi_bundle_PopulatesTable_Scenario0_GivenDefaultBundleID():
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_acct_net = -55
    bob_acct_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_ONRPLAN_SQLSTR)
        cursor.execute(CREATE_BELIEF_ACCT_NETS_SQLSTR)
        belief_acct_nets_tablename = belief_acct_nets_str()
        insert_sqlstr = f"""INSERT INTO {belief_acct_nets_tablename} ({belief_label_str()}, {believer_name_str()}, {believer_net_amount_str()})
VALUES
  ('{a23_str}', '{bob_str}', {bob_acct_net})
, ('{a23_str}', '{yao_str}', {yao_acct_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, belief_acct_nets_tablename) == 2
        belief_kpi001_acct_nets_tablename = belief_kpi001_acct_nets_str()
        assert not db_table_exists(cursor, belief_kpi001_acct_nets_tablename)

        # WHEN
        populate_kpi_bundle(cursor, get_default_kpi_bundle())

        # THEN
        assert get_row_count(cursor, belief_kpi001_acct_nets_tablename) == 2
        onrplan_job_tablename = create_prime_tablename("ONRPLAN", "job", None)
        assert set(get_db_tables(db_conn).keys()) == {
            belief_kpi001_acct_nets_str(),
            belief_acct_nets_tablename,
            onrplan_job_tablename,
        }


def test_populate_kpi_bundle_PopulatesTable_Scenario1_GivenNoBundleID():
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_acct_net = -55
    bob_acct_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_ONRPLAN_SQLSTR)
        cursor.execute(CREATE_BELIEF_ACCT_NETS_SQLSTR)
        belief_acct_nets_tablename = belief_acct_nets_str()
        insert_sqlstr = f"""INSERT INTO {belief_acct_nets_tablename} ({belief_label_str()}, {believer_name_str()}, {believer_net_amount_str()})
VALUES
  ('{a23_str}', '{bob_str}', {bob_acct_net})
, ('{a23_str}', '{yao_str}', {yao_acct_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, belief_acct_nets_tablename) == 2
        belief_kpi001_acct_nets_tablename = belief_kpi001_acct_nets_str()
        assert not db_table_exists(cursor, belief_kpi001_acct_nets_tablename)

        # WHEN
        populate_kpi_bundle(cursor)

        # THEN
        assert get_row_count(cursor, belief_kpi001_acct_nets_tablename) == 2
        onrplan_job_tablename = create_prime_tablename("ONRPLAN", "job", None)
        assert set(get_db_tables(db_conn).keys()) == {
            belief_kpi001_acct_nets_str(),
            belief_acct_nets_tablename,
            onrplan_job_tablename,
        }
