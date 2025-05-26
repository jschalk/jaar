from src.a00_data_toolbox.file_toolbox import save_file, open_file
from src.a06_bud_logic.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.a12_hub_tools.hub_path import (
    create_fisc_json_path,
    create_gut_path,
    create_job_path,
)
from src.a15_fisc_logic.fisc import fiscunit_shop
from src.a18_etl_toolbox.transformers import etl_fisc_guts_to_fisc_jobs
from src.a18_etl_toolbox._utils.env_a18 import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from os.path import exists as os_path_exists


def test_etl_fisc_guts_to_fisc_jobs_SetsFiles_Scenario0(
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
    bob_gut = budunit_shop(bob_inx, a23_str)
    bob_gut.add_acctunit(bob_inx, credit77)
    bob_gut.add_acctunit(yao_inx, credit44)
    bob_gut.add_acctunit(bob_inx, credit77)
    bob_gut.add_acctunit(sue_inx, credit88)
    bob_gut.add_acctunit(yao_inx, credit44)
    a23_bob_gut_path = create_gut_path(fisc_mstr_dir, a23_str, bob_inx)
    save_file(a23_bob_gut_path, None, bob_gut.get_json())
    a23_bob_job_path = create_job_path(fisc_mstr_dir, a23_str, bob_inx)
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(fisc_json_path, None, fiscunit_shop(a23_str, fisc_mstr_dir).get_json())
    assert os_path_exists(fisc_json_path)
    assert os_path_exists(a23_bob_gut_path)
    print(f"{a23_bob_gut_path=}")
    assert os_path_exists(a23_bob_job_path) is False

    # WHEN
    etl_fisc_guts_to_fisc_jobs(fisc_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_job_path)
    generated_job = budunit_get_from_json(open_file(a23_bob_job_path))
    expected_job = budunit_shop(bob_inx, a23_str)
    expected_job.add_acctunit(bob_inx, credit77)
    expected_job.add_acctunit(yao_inx, credit44)
    expected_job.add_acctunit(bob_inx, credit77)
    expected_job.add_acctunit(sue_inx, credit88)
    expected_job.add_acctunit(yao_inx, credit44)
    # assert generated_job.get_acct(sue_inx) == expected_job.get_acct(sue_inx)
    # assert generated_job.get_acct(bob_inx) == expected_job.get_acct(bob_inx)
    # assert generated_job.get_acct(yao_inx) == expected_job.get_acct(yao_inx)
    assert generated_job.accts.keys() == expected_job.accts.keys()
    # assert generated_job.accts == expected_job.accts
    # assert generated_job.get_concept_dict() == expected_job.get_dict()
    # assert generated_job.get_dict() == expected_job.get_dict()
    # assert generated_job == expected_job
