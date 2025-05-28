from src.a00_data_toolbox.file_toolbox import save_file
from src.a00_data_toolbox.db_toolbox import get_row_count, db_table_exists
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hub_path import create_fisc_json_path, create_job_path
from src.a12_hub_tools.hub_tool import save_job_file
from src.a15_fisc_logic.fisc import fiscunit_shop
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a18_etl_toolbox.transformers import etl_fisc_job_jsons_to_job_tables
from src.a18_etl_toolbox._utils.env_a18 import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_etl_fisc_job_jsons_to_job_tables_SetsFiles_Scenario0(
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
        budacct_job_tablename = create_prime_tablename("budacct", "job", None)
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
