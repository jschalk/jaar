from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
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
from src.a19_kpi_toolbox.kpi_mstr import create_populate_kpi001_table


def test_etl_vow_json_acct_nets_to_vow_acct_nets_table_PopulatesTable_Scenario0_NoTasks():
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_acct_net = -55
    bob_acct_net = 600

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
        vow_kpi001_acct_nets_tablename = vow_kpi001_acct_nets_str()
        assert not db_table_exists(cursor, vow_kpi001_acct_nets_tablename)

        # WHEN
        create_populate_kpi001_table(cursor)

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
            (a23_str, bob_str, 600.0, None, None),
            (a23_str, yao_str, -55.0, None, None),
        ]


# def test_etl_vow_json_acct_nets_to_vow_acct_nets_table_PopulatesTable_Scenario1_1task():
#     # ESTABLISH
#     a23_str = "accord23"
#     yao_str = "Yao"
#     bob_str = "Bob"
#     yao_acct_net = -55
#     bob_acct_net = 600

#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         cursor.execute(CREATE_VOW_ACCT_NETS_SQLSTR)
#         vow_acct_nets_tablename = vow_acct_nets_str()
#         insert_sqlstr = f"""INSERT INTO {vow_acct_nets_tablename} ({vow_label_str()}, {owner_name_str()}, {owner_net_amount_str()})
# VALUES
#   ('{a23_str}', '{bob_str}', {bob_acct_net})
# , ('{a23_str}', '{yao_str}', {yao_acct_net})
# """
#         cursor.execute(insert_sqlstr)
#         assert get_row_count(cursor, vow_acct_nets_tablename) == 2

#         cursor.execute(CREATE_JOB_PLNCONC_SQLSTR)
#         job_plnconc_tablename = create_prime_tablename(plan_conceptunit_str(), "job")
#         insert_sqlstr = f"""INSERT INTO {job_plnconc_tablename} ({vow_label_str()}, {owner_name_str()}, {owner_net_amount_str()})
# VALUES
#   ('{a23_str}', '{bob_str}', {bob_acct_net})
# , ('{a23_str}', '{yao_str}', {yao_acct_net})
# """
#         cursor.execute(insert_sqlstr)
# vow_label, owner_name, concept_way, task, _active INTEGER, _chore INTEGER

#         vow_kpi001_acct_nets_tablename = vow_kpi001_acct_nets_str()
#         assert not db_table_exists(cursor, vow_kpi001_acct_nets_tablename)

#         # WHEN
#         create_populate_kpi001_table(cursor)

#         # THEN
#         assert get_table_columns(cursor, vow_kpi001_acct_nets_tablename) == [
#             vow_label_str(),
#             owner_name_str(),
#             "funds",
#             "fund_rank",
#             "tasks_count",
#         ]
#         assert get_row_count(cursor, vow_kpi001_acct_nets_tablename)
#         select_sqlstr = f"""
#         SELECT
#   {vow_label_str()}
# , {owner_name_str()}
# , funds
# , fund_rank
# , tasks_count
# FROM {vow_kpi001_acct_nets_tablename}
# """
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         print(rows)
#         assert rows == [
#             (a23_str, bob_str, 600.0, None, None),
#             (a23_str, yao_str, -55.0, None, None),
#         ]
