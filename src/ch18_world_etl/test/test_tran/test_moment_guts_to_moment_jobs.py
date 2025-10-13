from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import open_json, save_json
from src.ch07_belief_logic.belief_main import beliefunit_shop, get_beliefunit_from_dict
from src.ch10_pack._ref.ch10_path import (
    create_gut_path,
    create_job_path,
    create_moment_json_path,
)
from src.ch15_moment.moment_main import momentunit_shop
from src.ch18_world_etl.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_world_etl.transformers import etl_moment_guts_to_moment_jobs


def test_etl_moment_guts_to_moment_jobs_SetsFiles_Scenario0(
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
    bob_gut = beliefunit_shop(bob_inx, a23_str)
    bob_gut.add_voiceunit(bob_inx, credit77)
    bob_gut.add_voiceunit(yao_inx, credit44)
    bob_gut.add_voiceunit(bob_inx, credit77)
    bob_gut.add_voiceunit(sue_inx, credit88)
    bob_gut.add_voiceunit(yao_inx, credit44)
    a23_bob_gut_path = create_gut_path(moment_mstr_dir, a23_str, bob_inx)
    save_json(a23_bob_gut_path, None, bob_gut.to_dict())
    a23_bob_job_path = create_job_path(moment_mstr_dir, a23_str, bob_inx)
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_str)
    save_json(
        moment_json_path, None, momentunit_shop(a23_str, moment_mstr_dir).to_dict()
    )
    assert os_path_exists(moment_json_path)
    assert os_path_exists(a23_bob_gut_path)
    print(f"{a23_bob_gut_path=}")
    assert os_path_exists(a23_bob_job_path) is False

    # WHEN
    etl_moment_guts_to_moment_jobs(moment_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_job_path)
    generated_job = get_beliefunit_from_dict(open_json(a23_bob_job_path))
    expected_job = beliefunit_shop(bob_inx, a23_str)
    expected_job.add_voiceunit(bob_inx, credit77)
    expected_job.add_voiceunit(yao_inx, credit44)
    expected_job.add_voiceunit(bob_inx, credit77)
    expected_job.add_voiceunit(sue_inx, credit88)
    expected_job.add_voiceunit(yao_inx, credit44)
    # assert generated_job.get_voice(sue_inx) == expected_job.get_voice(sue_inx)
    # assert generated_job.get_voice(bob_inx) == expected_job.get_voice(bob_inx)
    # assert generated_job.get_voice(yao_inx) == expected_job.get_voice(yao_inx)
    assert generated_job.voices.keys() == expected_job.voices.keys()
    # assert generated_job.voices == expected_job.voices
    # assert generated_job.get_plan_dict() == expected_job.to_dict()
    # assert generated_job.to_dict() == expected_job.to_dict()
    # assert generated_job == expected_job
