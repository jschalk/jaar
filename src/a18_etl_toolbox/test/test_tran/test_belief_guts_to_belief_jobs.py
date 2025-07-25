from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import open_file, save_file
from src.a06_believer_logic.believer import (
    believerunit_shop,
    get_from_json as believerunit_get_from_json,
)
from src.a12_hub_toolbox.a12_path import (
    create_belief_json_path,
    create_gut_path,
    create_job_path,
)
from src.a15_belief_logic.belief import beliefunit_shop
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import etl_belief_guts_to_belief_jobs


def test_etl_belief_guts_to_belief_jobs_SetsFiles_Scenario0(
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
    bob_gut = believerunit_shop(bob_inx, a23_str)
    bob_gut.add_partnerunit(bob_inx, credit77)
    bob_gut.add_partnerunit(yao_inx, credit44)
    bob_gut.add_partnerunit(bob_inx, credit77)
    bob_gut.add_partnerunit(sue_inx, credit88)
    bob_gut.add_partnerunit(yao_inx, credit44)
    a23_bob_gut_path = create_gut_path(belief_mstr_dir, a23_str, bob_inx)
    save_file(a23_bob_gut_path, None, bob_gut.get_json())
    a23_bob_job_path = create_job_path(belief_mstr_dir, a23_str, bob_inx)
    belief_json_path = create_belief_json_path(belief_mstr_dir, a23_str)
    save_file(
        belief_json_path, None, beliefunit_shop(a23_str, belief_mstr_dir).get_json()
    )
    assert os_path_exists(belief_json_path)
    assert os_path_exists(a23_bob_gut_path)
    print(f"{a23_bob_gut_path=}")
    assert os_path_exists(a23_bob_job_path) is False

    # WHEN
    etl_belief_guts_to_belief_jobs(belief_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_job_path)
    generated_job = believerunit_get_from_json(open_file(a23_bob_job_path))
    expected_job = believerunit_shop(bob_inx, a23_str)
    expected_job.add_partnerunit(bob_inx, credit77)
    expected_job.add_partnerunit(yao_inx, credit44)
    expected_job.add_partnerunit(bob_inx, credit77)
    expected_job.add_partnerunit(sue_inx, credit88)
    expected_job.add_partnerunit(yao_inx, credit44)
    # assert generated_job.get_partner(sue_inx) == expected_job.get_partner(sue_inx)
    # assert generated_job.get_partner(bob_inx) == expected_job.get_partner(bob_inx)
    # assert generated_job.get_partner(yao_inx) == expected_job.get_partner(yao_inx)
    assert generated_job.partners.keys() == expected_job.partners.keys()
    # assert generated_job.partners == expected_job.partners
    # assert generated_job.get_plan_dict() == expected_job.get_dict()
    # assert generated_job.get_dict() == expected_job.get_dict()
    # assert generated_job == expected_job
