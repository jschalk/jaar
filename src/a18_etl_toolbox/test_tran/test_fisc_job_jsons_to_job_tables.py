from src.a00_data_toolbox.file_toolbox import save_file
from src.a00_data_toolbox.db_toolbox import get_row_count, db_table_exists

from src.a01_way_logic.way import OwnerName, WayStr, AcctName, GroupTitle
from src.a02_finance_logic.deal import FiscLabel, OwnerName
from src.a03_group_logic.acct import AcctUnit
from src.a03_group_logic.group import awardlink_shop, GroupUnit, AwardHeir
from src.a04_reason_logic.reason_concept import FactHeir, PremiseUnit, ReasonHeir
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_bud_logic.bud import BudUnit

from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hub_path import create_fisc_json_path, create_job_path
from src.a12_hub_tools.hub_tool import save_job_file
from src.a15_fisc_logic.fisc import fiscunit_shop
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename as prime_table
from src.a18_etl_toolbox.transformers import etl_fisc_job_jsons_to_job_tables
from src.a18_etl_toolbox._test_util.env_a18 import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_etl_fisc_job_jsons_to_job_tables_PopulatesTables_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    m23_fisc_mstr_dir = get_module_temp_dir()
    m23_str = "music23"
    a23_str = "accord23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_bud = budunit_shop(sue_str, a23_str)
    sue_bud.add_acctunit(sue_str)
    sue_bud.add_acctunit(bob_str)
    sue_bud.get_acct(bob_str).add_membership(run_str)
    casa_way = sue_bud.make_l1_way("casa")
    status_way = sue_bud.make_l1_way("status")
    clean_way = sue_bud.make_way(status_way, "clean")
    dirty_way = sue_bud.make_way(status_way, "dirty")
    sue_bud.add_concept(casa_way)
    sue_bud.add_concept(clean_way)
    sue_bud.add_concept(dirty_way)
    sue_bud.edit_concept_attr(
        casa_way, reason_rcontext=status_way, reason_premise=dirty_way
    )
    sue_bud.edit_concept_attr(casa_way, awardlink=awardlink_shop(run_str))
    sue_bud.edit_concept_attr(casa_way, healerlink=healerlink_shop({bob_str}))
    sue_bud.edit_concept_attr(casa_way, laborunit=laborunit_shop({sue_str}))
    sue_bud.add_fact(status_way, clean_way)
    print(f"{sue_bud.get_concept_obj(casa_way).laborunit=}")
    print(f"{sue_bud.get_concept_obj(casa_way).get_dict()=}")
    save_job_file(m23_fisc_mstr_dir, sue_bud)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        budmemb_job_table = prime_table("budmemb", "job", None)
        budacct_job_table = prime_table("budacct", "job", None)
        budgrou_job_table = prime_table("budgrou", "job", None)
        budawar_job_table = prime_table("budawar", "job", None)
        budfact_job_table = prime_table("budfact", "job", None)
        budheal_job_table = prime_table("budheal", "job", None)
        budprem_job_table = prime_table("budprem", "job", None)
        budreas_job_table = prime_table("budreas", "job", None)
        budlabo_job_table = prime_table("budlabo", "job", None)
        budconc_job_table = prime_table("budconc", "job", None)
        budunit_job_table = prime_table("budunit", "job", None)
        assert not db_table_exists(cursor, budunit_job_table)
        assert not db_table_exists(cursor, budconc_job_table)
        assert not db_table_exists(cursor, budacct_job_table)
        assert not db_table_exists(cursor, budmemb_job_table)
        assert not db_table_exists(cursor, budgrou_job_table)
        assert not db_table_exists(cursor, budawar_job_table)
        assert not db_table_exists(cursor, budfact_job_table)
        assert not db_table_exists(cursor, budheal_job_table)
        assert not db_table_exists(cursor, budreas_job_table)
        assert not db_table_exists(cursor, budprem_job_table)
        assert not db_table_exists(cursor, budlabo_job_table)

        # WHEN
        etl_fisc_job_jsons_to_job_tables(cursor, m23_fisc_mstr_dir)

        # THEN
        assert get_row_count(cursor, budunit_job_table) == 1
        assert get_row_count(cursor, budconc_job_table) == 5
        assert get_row_count(cursor, budacct_job_table) == 2
        assert get_row_count(cursor, budmemb_job_table) == 3
        assert get_row_count(cursor, budgrou_job_table) == 3
        assert get_row_count(cursor, budawar_job_table) == 1
        assert get_row_count(cursor, budfact_job_table) == 1
        assert get_row_count(cursor, budheal_job_table) == 1
        assert get_row_count(cursor, budreas_job_table) == 1
        assert get_row_count(cursor, budprem_job_table) == 1
        assert get_row_count(cursor, budlabo_job_table) == 1


def test_etl_fisc_job_jsons_to_job_tables_PopulatesTables_Scenario1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "accord23"
    fisc_mstr_dir = get_module_temp_dir()
    bob_job = budunit_shop(bob_inx, a23_str)
    bob_job.add_acctunit(bob_inx, credit77)
    bob_job.add_acctunit(yao_inx, credit44)
    bob_job.add_acctunit(bob_inx, credit77)
    bob_job.add_acctunit(sue_inx, credit88)
    bob_job.add_acctunit(yao_inx, credit44)
    save_job_file(fisc_mstr_dir, bob_job)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, fiscunit_shop(a23_str, fisc_mstr_dir).get_json())
    a23_bob_job_path = create_job_path(fisc_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(fisc_json_path)
    assert os_path_exists(a23_bob_job_path)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        budacct_job_tablename = prime_table("budacct", "job", None)
        assert not db_table_exists(cursor, budacct_job_tablename)

        # WHEN
        etl_fisc_job_jsons_to_job_tables(cursor, fisc_mstr_dir)

        # THEN
        assert get_row_count(cursor, budacct_job_tablename) == 3
        rows = cursor.execute(f"SELECT * FROM {budacct_job_tablename}").fetchall()
        print(rows)
        assert rows == [
            (
                "accord23",
                "Bobby",
                "Bobby",
                77.0,
                1.0,
                368421053.0,
                333333334.0,
                368421053.0,
                333333334.0,
                368421053.0,
                333333334.0,
                0.368421053,
                0.333333334,
                0.0,
                0.0,
            ),
            (
                "accord23",
                "Bobby",
                "Suzy",
                88.0,
                1.0,
                421052631.0,
                333333333.0,
                421052631.0,
                333333333.0,
                421052631.0,
                333333333.0,
                0.421052631,
                0.333333333,
                0.0,
                0.0,
            ),
            (
                "accord23",
                "Bobby",
                "Yaoe",
                44.0,
                1.0,
                210526316.0,
                333333333.0,
                210526316.0,
                333333333.0,
                210526316.0,
                333333333.0,
                0.210526316,
                0.333333333,
                0.0,
                0.0,
            ),
        ]
