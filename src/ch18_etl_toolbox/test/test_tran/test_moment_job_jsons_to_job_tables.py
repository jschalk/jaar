from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.ch01_data_toolbox.file_toolbox import save_file
from src.ch04_voice_logic.group import awardunit_shop
from src.ch04_voice_logic.labor import laborunit_shop
from src.ch06_plan_logic.healer import healerunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch12_hub_toolbox.ch12_path import create_job_path, create_moment_json_path
from src.ch12_hub_toolbox.hub_tool import save_job_file
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch18_etl_toolbox._ref.ch18_keywords import Ch18Keywords as wx
from src.ch18_etl_toolbox.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_etl_toolbox.tran_sqlstrs import create_prime_tablename as prime_table
from src.ch18_etl_toolbox.transformers import etl_moment_job_jsons_to_job_tables


def test_etl_moment_job_jsons_to_job_tables_PopulatesTables_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    m23_moment_mstr_dir = get_chapter_temp_dir()
    m23_str = "music23"
    a23_str = "amy23"
    sue_str = "Sue"
    bob_str = "Bob"
    run_str = ";run"
    sue_belief = beliefunit_shop(sue_str, a23_str)
    sue_belief.add_voiceunit(sue_str)
    sue_belief.add_voiceunit(bob_str)
    sue_belief.get_voice(bob_str).add_membership(run_str)
    casa_rope = sue_belief.make_l1_rope("casa")
    status_rope = sue_belief.make_l1_rope("status")
    clean_rope = sue_belief.make_rope(status_rope, "clean")
    dirty_rope = sue_belief.make_rope(status_rope, "dirty")
    sue_belief.add_plan(casa_rope)
    sue_belief.add_plan(clean_rope)
    sue_belief.add_plan(dirty_rope)
    sue_belief.edit_plan_attr(
        casa_rope, reason_context=status_rope, reason_case=dirty_rope
    )
    sue_belief.edit_plan_attr(casa_rope, awardunit=awardunit_shop(run_str))
    sue_belief.edit_plan_attr(casa_rope, healerunit=healerunit_shop({bob_str}))
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(sue_str)
    sue_belief.edit_plan_attr(casa_rope, laborunit=sue_laborunit)
    sue_belief.add_fact(status_rope, clean_rope)
    print(f"{sue_belief.get_plan_obj(casa_rope).laborunit=}")
    print(f"{sue_belief.get_plan_obj(casa_rope).to_dict()=}")
    save_job_file(m23_moment_mstr_dir, sue_belief)

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        blrmemb_job_table = prime_table("blrmemb", wx.job, None)
        blrpern_job_table = prime_table("blrpern", wx.job, None)
        blrgrou_job_table = prime_table("blrgrou", wx.job, None)
        blrawar_job_table = prime_table("blrawar", wx.job, None)
        blrfact_job_table = prime_table("blrfact", wx.job, None)
        blrheal_job_table = prime_table("blrheal", wx.job, None)
        blrprem_job_table = prime_table("blrprem", wx.job, None)
        blrreas_job_table = prime_table("blrreas", wx.job, None)
        blrlabo_job_table = prime_table("blrlabo", wx.job, None)
        blrplan_job_table = prime_table("blrplan", wx.job, None)
        blrunit_job_table = prime_table("beliefunit", wx.job, None)
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
        etl_moment_job_jsons_to_job_tables(cursor, m23_moment_mstr_dir)

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


def test_etl_moment_job_jsons_to_job_tables_PopulatesTables_Scenario1(
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
    moment_mstr_dir = get_chapter_temp_dir()
    bob_job = beliefunit_shop(bob_inx, a23_str)
    bob_job.add_voiceunit(bob_inx, credit77)
    bob_job.add_voiceunit(yao_inx, credit44)
    bob_job.add_voiceunit(bob_inx, credit77)
    bob_job.add_voiceunit(sue_inx, credit88)
    bob_job.add_voiceunit(yao_inx, credit44)
    save_job_file(moment_mstr_dir, bob_job)
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_str)
    save_file(
        moment_json_path, None, momentunit_shop(a23_str, moment_mstr_dir).get_json()
    )
    a23_bob_job_path = create_job_path(moment_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(moment_json_path)
    assert os_path_exists(a23_bob_job_path)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        blrpern_job_tablename = prime_table("blrpern", wx.job, None)
        assert not db_table_exists(cursor, blrpern_job_tablename)

        # WHEN
        etl_moment_job_jsons_to_job_tables(cursor, moment_mstr_dir)

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
