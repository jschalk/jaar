from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a01_term_logic.rope import create_rope
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a04_reason_logic._test_util.a04_str import _active_str, _chore_str
from src.a05_concept_logic._test_util.a05_str import concept_rope_str, task_str
from src.a06_plan_logic._test_util.a06_str import plan_conceptunit_str
from src.a18_etl_toolbox._test_util.a18_str import (
    owner_net_amount_str,
    vow_acct_nets_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    CREATE_JOB_PLNCONC_SQLSTR,
    CREATE_VOW_ACCT_NETS_SQLSTR,
    create_prime_tablename,
)
from src.a19_kpi_toolbox._test_util.a19_str import vow_kpi001_acct_nets_str
from src.a19_kpi_toolbox.kpi_mstr import create_kpi001_table


def test_create_kpi001_table_PopulatesTable_Scenario0_NoTasks():
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
        create_kpi001_table(cursor)

        # THEN
        assert get_table_columns(cursor, vow_kpi001_acct_nets_tablename) == [
            vow_label_str(),
            owner_name_str(),
            "funds",
            "fund_rank",
            "tasks_count",
        ]
        assert get_row_count(cursor, vow_kpi001_acct_nets_tablename)
        select_sqlstr = f"""
        SELECT 
  {vow_label_str()}
, {owner_name_str()}
, funds
, fund_rank
, tasks_count
FROM {vow_kpi001_acct_nets_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (a23_str, bob_str, 600.0, 1, 0),
            (a23_str, yao_str, -55.0, 2, 0),
        ]


def test_create_kpi001_table_PopulatesTable_Scenario1_1task():
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_acct_net = -55
    bob_acct_net = 600
    casa_rope = create_rope(a23_str, "casa")

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_VOW_ACCT_NETS_SQLSTR)
        vow_acct_nets_tablename = vow_acct_nets_str()
        insert_sqlstr = f"""INSERT INTO {vow_acct_nets_tablename} ({vow_label_str()}, {owner_name_str()}, {owner_net_amount_str()})
VALUES
  ('{a23_str}', '{bob_str}', {bob_acct_net})
, ('{a23_str}', '{yao_str}', {yao_acct_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, vow_acct_nets_tablename) == 2

        cursor.execute(CREATE_JOB_PLNCONC_SQLSTR)
        job_plnconc_tablename = create_prime_tablename("plnconc", "job", None)
        insert_sqlstr = f"""
INSERT INTO {job_plnconc_tablename} ({vow_label_str()}, {owner_name_str()}, {concept_rope_str()}, {task_str()})
VALUES ('{a23_str}', '{bob_str}', '{casa_rope}', 1)
"""
        cursor.execute(insert_sqlstr)
        vow_kpi001_acct_nets_tablename = vow_kpi001_acct_nets_str()
        assert not db_table_exists(cursor, vow_kpi001_acct_nets_tablename)

        # WHEN
        create_kpi001_table(cursor)

        # THEN
        assert get_row_count(cursor, vow_kpi001_acct_nets_tablename)
        select_sqlstr = f"""SELECT {vow_label_str()}, {owner_name_str()}, funds, fund_rank, tasks_count FROM {vow_kpi001_acct_nets_tablename}"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (a23_str, bob_str, bob_acct_net, 1, 1),
            (a23_str, yao_str, yao_acct_net, 2, 0),
        ]
