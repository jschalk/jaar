from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.a00_data_toolbox.file_toolbox import save_file
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_plan_logic.healer import healerlink_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a12_hub_toolbox.a12_path import create_belief_json_path, create_job_path
from src.a12_hub_toolbox.hub_tool import save_job_file
from src.a12_hub_toolbox.test._util.a12_str import job_str
from src.a15_belief_logic.belief_main import beliefunit_shop
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
    a23_str = "amy23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_believer = believerunit_shop(sue_str, a23_str)
    sue_believer.add_partnerunit(sue_str)
    sue_believer.add_partnerunit(bob_str)
    sue_believer.get_partner(bob_str).add_membership(run_str)
    casa_rope = sue_believer.make_l1_rope("casa")
    status_rope = sue_believer.make_l1_rope("status")
    clean_rope = sue_believer.make_rope(status_rope, "clean")
    dirty_rope = sue_believer.make_rope(status_rope, "dirty")
    sue_believer.add_plan(casa_rope)
    sue_believer.add_plan(clean_rope)
    sue_believer.add_plan(dirty_rope)
    sue_believer.edit_plan_attr(
        casa_rope, reason_context=status_rope, reason_case=dirty_rope
    )
    sue_believer.edit_plan_attr(casa_rope, awardlink=awardlink_shop(run_str))
    sue_believer.edit_plan_attr(casa_rope, healerlink=healerlink_shop({bob_str}))
    sue_believer.edit_plan_attr(casa_rope, laborunit=laborunit_shop({sue_str}))
    sue_believer.add_fact(status_rope, clean_rope)
    print(f"{sue_believer.get_plan_obj(casa_rope).laborunit=}")
    print(f"{sue_believer.get_plan_obj(casa_rope).get_dict()=}")
    save_job_file(m23_belief_mstr_dir, sue_believer)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        blrmemb_job_table = prime_table("blrmemb", job_str(), None)
        blrpern_job_table = prime_table("blrpern", job_str(), None)
        blrgrou_job_table = prime_table("blrgrou", job_str(), None)
        blrawar_job_table = prime_table("blrawar", job_str(), None)
        blrfact_job_table = prime_table("blrfact", job_str(), None)
        blrheal_job_table = prime_table("blrheal", job_str(), None)
        blrprem_job_table = prime_table("blrprem", job_str(), None)
        blrreas_job_table = prime_table("blrreas", job_str(), None)
        blrlabo_job_table = prime_table("blrlabo", job_str(), None)
        blrplan_job_table = prime_table("blrplan", job_str(), None)
        blrunit_job_table = prime_table("believerunit", job_str(), None)
        assert not db_table_exists(cursor, blrunit_job_table)
        assert not db_table_exists(cursor, blrplan_job_table)
        assert not db_table_exists(cursor, blrpern_job_table)
        assert not db_table_exists(cursor, blrmemb_job_table)
        assert not db_table_exists(cursor, blrgrou_job_table)
        assert not db_table_exists(cursor, blrawar_job_table)
        assert not db_table_exists(cursor, blrfact_job_table)
        assert not db_table_exists(cursor, blrheal_job_table)
        assert not db_table_exists(cursor, blrreas_job_table)
        assert not db_table_exists(cursor, blrprem_job_table)
        assert not db_table_exists(cursor, blrlabo_job_table)

        # WHEN
        etl_belief_job_jsons_to_job_tables(cursor, m23_belief_mstr_dir)

        # THEN
        assert get_row_count(cursor, blrunit_job_table) == 1
        assert get_row_count(cursor, blrplan_job_table) == 5
        assert get_row_count(cursor, blrpern_job_table) == 2
        assert get_row_count(cursor, blrmemb_job_table) == 3
        assert get_row_count(cursor, blrgrou_job_table) == 3
        assert get_row_count(cursor, blrawar_job_table) == 1
        assert get_row_count(cursor, blrfact_job_table) == 1
        assert get_row_count(cursor, blrheal_job_table) == 1
        assert get_row_count(cursor, blrreas_job_table) == 1
        assert get_row_count(cursor, blrprem_job_table) == 1
        assert get_row_count(cursor, blrlabo_job_table) == 1


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
    a23_str = "amy23"
    belief_mstr_dir = get_module_temp_dir()
    bob_job = believerunit_shop(bob_inx, a23_str)
    bob_job.add_partnerunit(bob_inx, credit77)
    bob_job.add_partnerunit(yao_inx, credit44)
    bob_job.add_partnerunit(bob_inx, credit77)
    bob_job.add_partnerunit(sue_inx, credit88)
    bob_job.add_partnerunit(yao_inx, credit44)
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
        blrpern_job_tablename = prime_table("blrpern", job_str(), None)
        assert not db_table_exists(cursor, blrpern_job_tablename)

        # WHEN
        etl_belief_job_jsons_to_job_tables(cursor, belief_mstr_dir)

        # THEN
        assert get_row_count(cursor, blrpern_job_tablename) == 3
        rows = cursor.execute(f"SELECT * FROM {blrpern_job_tablename}").fetchall()
        print(rows)
        assert rows == [
            (
                "amy23",
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
                "amy23",
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
                "amy23",
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
