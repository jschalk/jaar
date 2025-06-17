from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_db_tables,
    get_row_count,
)
from src.a02_finance_logic._util.a02_str import owner_name_str, vow_label_str
from src.a18_etl_toolbox._util.a18_str import owner_net_amount_str, vow_acct_nets_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    CREATE_JOB_PLNCONC_SQLSTR,
    CREATE_VOW_ACCT_NETS_SQLSTR,
    create_prime_tablename,
)
from src.a19_kpi_toolbox._util.a19_str import vow_kpi001_acct_nets_str
from src.a19_kpi_toolbox.kpi_mstr import get_default_kpi_bundle, populate_kpi_bundle


def test_populate_kpi_bundle_PopulatesTable_Scenario0_GivenDefaultBundleID():
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_acct_net = -55
    bob_acct_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_PLNCONC_SQLSTR)
        cursor.execute(CREATE_VOW_ACCT_NETS_SQLSTR)
        vow_acct_nets_tablename = vow_acct_nets_str()
        insert_sqlstr = f"""INSERT INTO {vow_acct_nets_tablename} ({vow_label_str()}, {owner_name_str()}, {owner_net_amount_str()})
VALUES
  ('{a23_str}', '{bob_str}', {bob_acct_net})
, ('{a23_str}', '{yao_str}', {yao_acct_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, vow_acct_nets_tablename) == 2
        vow_kpi001_acct_nets_tablename = vow_kpi001_acct_nets_str()
        assert not db_table_exists(cursor, vow_kpi001_acct_nets_tablename)

        # WHEN
        populate_kpi_bundle(cursor, get_default_kpi_bundle())

        # THEN
        assert get_row_count(cursor, vow_kpi001_acct_nets_tablename) == 2
        plnconc_job_tablename = create_prime_tablename("PLNCONC", "job", None)
        assert set(get_db_tables(db_conn).keys()) == {
            vow_kpi001_acct_nets_str(),
            vow_acct_nets_tablename,
            plnconc_job_tablename,
        }


def test_populate_kpi_bundle_PopulatesTable_Scenario1_GivenNoBundleID():
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_acct_net = -55
    bob_acct_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_PLNCONC_SQLSTR)
        cursor.execute(CREATE_VOW_ACCT_NETS_SQLSTR)
        vow_acct_nets_tablename = vow_acct_nets_str()
        insert_sqlstr = f"""INSERT INTO {vow_acct_nets_tablename} ({vow_label_str()}, {owner_name_str()}, {owner_net_amount_str()})
VALUES
  ('{a23_str}', '{bob_str}', {bob_acct_net})
, ('{a23_str}', '{yao_str}', {yao_acct_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, vow_acct_nets_tablename) == 2
        vow_kpi001_acct_nets_tablename = vow_kpi001_acct_nets_str()
        assert not db_table_exists(cursor, vow_kpi001_acct_nets_tablename)

        # WHEN
        populate_kpi_bundle(cursor)

        # THEN
        assert get_row_count(cursor, vow_kpi001_acct_nets_tablename) == 2
        plnconc_job_tablename = create_prime_tablename("PLNCONC", "job", None)
        assert set(get_db_tables(db_conn).keys()) == {
            vow_kpi001_acct_nets_str(),
            vow_acct_nets_tablename,
            plnconc_job_tablename,
        }
