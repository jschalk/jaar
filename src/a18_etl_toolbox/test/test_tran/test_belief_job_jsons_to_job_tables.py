from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.a00_data_toolbox.file_toolbox import save_file
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_toolbox.hub_path import create_belief_json_path, create_job_path
from src.a12_hub_toolbox.hub_tool import save_job_file
from src.a12_hub_toolbox.test._util.a12_str import job_str
from src.a15_belief_logic.belief import beliefunit_shop
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename as prime_table
from src.a18_etl_toolbox.transformers import etl_belief_job_jsons_to_job_tables


def test_etl_belief_job_jsons_to_job_tables_PopulatesTables_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    m23_belief_mstr_dir = get_module_temp_dir()
    m23_str = "music23"
    a23_str = "accord23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_plan = planunit_shop(sue_str, a23_str)
    sue_plan.add_acctunit(sue_str)
    sue_plan.add_acctunit(bob_str)
    sue_plan.get_acct(bob_str).add_membership(run_str)
    casa_rope = sue_plan.make_l1_rope("casa")
    status_rope = sue_plan.make_l1_rope("status")
    clean_rope = sue_plan.make_rope(status_rope, "clean")
    dirty_rope = sue_plan.make_rope(status_rope, "dirty")
    sue_plan.add_concept(casa_rope)
    sue_plan.add_concept(clean_rope)
    sue_plan.add_concept(dirty_rope)
    sue_plan.edit_concept_attr(
        casa_rope, reason_rcontext=status_rope, reason_premise=dirty_rope
    )
    sue_plan.edit_concept_attr(casa_rope, awardlink=awardlink_shop(run_str))
    sue_plan.edit_concept_attr(casa_rope, healerlink=healerlink_shop({bob_str}))
    sue_plan.edit_concept_attr(casa_rope, laborunit=laborunit_shop({sue_str}))
    sue_plan.add_fact(status_rope, clean_rope)
    print(f"{sue_plan.get_concept_obj(casa_rope).laborunit=}")
    print(f"{sue_plan.get_concept_obj(casa_rope).get_dict()=}")
    save_job_file(m23_belief_mstr_dir, sue_plan)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        plnmemb_job_table = prime_table("plnmemb", job_str(), None)
        plnacct_job_table = prime_table("plnacct", job_str(), None)
        plngrou_job_table = prime_table("plngrou", job_str(), None)
        plnawar_job_table = prime_table("plnawar", job_str(), None)
        plnfact_job_table = prime_table("plnfact", job_str(), None)
        plnheal_job_table = prime_table("plnheal", job_str(), None)
        plnprem_job_table = prime_table("plnprem", job_str(), None)
        plnreas_job_table = prime_table("plnreas", job_str(), None)
        plnlabo_job_table = prime_table("plnlabo", job_str(), None)
        plnconc_job_table = prime_table("plnconc", job_str(), None)
        plnunit_job_table = prime_table("planunit", job_str(), None)
        assert not db_table_exists(cursor, plnunit_job_table)
        assert not db_table_exists(cursor, plnconc_job_table)
        assert not db_table_exists(cursor, plnacct_job_table)
        assert not db_table_exists(cursor, plnmemb_job_table)
        assert not db_table_exists(cursor, plngrou_job_table)
        assert not db_table_exists(cursor, plnawar_job_table)
        assert not db_table_exists(cursor, plnfact_job_table)
        assert not db_table_exists(cursor, plnheal_job_table)
        assert not db_table_exists(cursor, plnreas_job_table)
        assert not db_table_exists(cursor, plnprem_job_table)
        assert not db_table_exists(cursor, plnlabo_job_table)

        # WHEN
        etl_belief_job_jsons_to_job_tables(cursor, m23_belief_mstr_dir)

        # THEN
        assert get_row_count(cursor, plnunit_job_table) == 1
        assert get_row_count(cursor, plnconc_job_table) == 5
        assert get_row_count(cursor, plnacct_job_table) == 2
        assert get_row_count(cursor, plnmemb_job_table) == 3
        assert get_row_count(cursor, plngrou_job_table) == 3
        assert get_row_count(cursor, plnawar_job_table) == 1
        assert get_row_count(cursor, plnfact_job_table) == 1
        assert get_row_count(cursor, plnheal_job_table) == 1
        assert get_row_count(cursor, plnreas_job_table) == 1
        assert get_row_count(cursor, plnprem_job_table) == 1
        assert get_row_count(cursor, plnlabo_job_table) == 1


def test_etl_belief_job_jsons_to_job_tables_PopulatesTables_Scenario1(
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
    belief_mstr_dir = get_module_temp_dir()
    bob_job = planunit_shop(bob_inx, a23_str)
    bob_job.add_acctunit(bob_inx, credit77)
    bob_job.add_acctunit(yao_inx, credit44)
    bob_job.add_acctunit(bob_inx, credit77)
    bob_job.add_acctunit(sue_inx, credit88)
    bob_job.add_acctunit(yao_inx, credit44)
    save_job_file(belief_mstr_dir, bob_job)
    belief_json_path = create_belief_json_path(belief_mstr_dir, a23_str)
    save_file(
        belief_json_path, None, beliefunit_shop(a23_str, belief_mstr_dir).get_json()
    )
    a23_bob_job_path = create_job_path(belief_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(belief_json_path)
    assert os_path_exists(a23_bob_job_path)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        plnacct_job_tablename = prime_table("plnacct", job_str(), None)
        assert not db_table_exists(cursor, plnacct_job_tablename)

        # WHEN
        etl_belief_job_jsons_to_job_tables(cursor, belief_mstr_dir)

        # THEN
        assert get_row_count(cursor, plnacct_job_tablename) == 3
        rows = cursor.execute(f"SELECT * FROM {plnacct_job_tablename}").fetchall()
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
