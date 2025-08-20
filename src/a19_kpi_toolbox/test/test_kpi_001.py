from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a01_term_logic.rope import create_rope
from src.a04_reason_logic.test._util.a04_str import belief_name_str, coin_label_str
from src.a05_plan_logic.test._util.a05_str import plan_rope_str, task_str
from src.a18_etl_toolbox.test._util.a18_str import (
    belief_net_amount_str,
    coin_partner_nets_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    CREATE_COIN_PARTNER_NETS_SQLSTR,
    CREATE_JOB_BLRPLAN_SQLSTR,
    create_prime_tablename,
)
from src.a19_kpi_toolbox.kpi_mstr import create_populate_kpi001_table
from src.a19_kpi_toolbox.test._util.a19_str import coin_kpi001_partner_nets_str


def test_create_populate_kpi001_table_PopulatesTable_Scenario0_NoTasks():
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_partner_net = -55
    bob_partner_net = 600

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_JOB_BLRPLAN_SQLSTR)
        cursor.execute(CREATE_COIN_PARTNER_NETS_SQLSTR)
        coin_partner_nets_tablename = coin_partner_nets_str()
        insert_sqlstr = f"""INSERT INTO {coin_partner_nets_tablename} ({coin_label_str()}, {belief_name_str()}, {belief_net_amount_str()}) 
VALUES 
  ('{a23_str}', '{bob_str}', {bob_partner_net})
, ('{a23_str}', '{yao_str}', {yao_partner_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, coin_partner_nets_tablename) == 2
        coin_kpi001_partner_nets_tablename = coin_kpi001_partner_nets_str()
        assert not db_table_exists(cursor, coin_kpi001_partner_nets_tablename)

        # WHEN
        create_populate_kpi001_table(cursor)

        # THEN
        assert get_table_columns(cursor, coin_kpi001_partner_nets_tablename) == [
            coin_label_str(),
            belief_name_str(),
            "funds",
            "fund_rank",
            "tasks_count",
        ]
        assert get_row_count(cursor, coin_kpi001_partner_nets_tablename)
        select_sqlstr = f"""
        SELECT 
  {coin_label_str()}
, {belief_name_str()}
, funds
, fund_rank
, tasks_count
FROM {coin_kpi001_partner_nets_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (a23_str, bob_str, 600.0, 1, 0),
            (a23_str, yao_str, -55.0, 2, 0),
        ]


def test_create_populate_kpi001_table_PopulatesTable_Scenario1_1task():
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    bob_str = "Bob"
    yao_partner_net = -55
    bob_partner_net = 600
    casa_rope = create_rope(a23_str, "casa")

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_COIN_PARTNER_NETS_SQLSTR)
        coin_partner_nets_tablename = coin_partner_nets_str()
        insert_sqlstr = f"""INSERT INTO {coin_partner_nets_tablename} ({coin_label_str()}, {belief_name_str()}, {belief_net_amount_str()})
VALUES
  ('{a23_str}', '{bob_str}', {bob_partner_net})
, ('{a23_str}', '{yao_str}', {yao_partner_net})
"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, coin_partner_nets_tablename) == 2

        cursor.execute(CREATE_JOB_BLRPLAN_SQLSTR)
        job_blrplan_tablename = create_prime_tablename("blrplan", "job", None)
        insert_sqlstr = f"""
INSERT INTO {job_blrplan_tablename} ({coin_label_str()}, {belief_name_str()}, {plan_rope_str()}, {task_str()})
VALUES ('{a23_str}', '{bob_str}', '{casa_rope}', 1)
"""
        cursor.execute(insert_sqlstr)
        coin_kpi001_partner_nets_tablename = coin_kpi001_partner_nets_str()
        assert not db_table_exists(cursor, coin_kpi001_partner_nets_tablename)

        # WHEN
        create_populate_kpi001_table(cursor)

        # THEN
        assert get_row_count(cursor, coin_kpi001_partner_nets_tablename)
        select_sqlstr = f"""SELECT {coin_label_str()}, {belief_name_str()}, funds, fund_rank, tasks_count FROM {coin_kpi001_partner_nets_tablename}"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (a23_str, bob_str, bob_partner_net, 1, 1),
            (a23_str, yao_str, yao_partner_net, 2, 0),
        ]
