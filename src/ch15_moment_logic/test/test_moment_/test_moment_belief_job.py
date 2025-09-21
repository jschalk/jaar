from src.ch00_data_toolbox.file_toolbox import set_dir
from src.ch06_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch12_hub_toolbox.ch12_path import create_belief_dir_path
from src.ch12_hub_toolbox.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch15_moment_logic.test._util.ch15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_MomentUnit_rotate_job_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_module_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    sue_str = "Sue"
    assert not job_file_exists(moment_mstr_dir, a23_str, sue_str)
    a23_moment.create_init_job_from_guts(sue_str)
    assert job_file_exists(moment_mstr_dir, a23_str, sue_str)

    # WHEN
    sue_job = a23_moment.rotate_job(sue_str)

    # THEN
    example_belief = beliefunit_shop(sue_str, a23_str)
    assert sue_job.moment_label == example_belief.moment_label
    assert sue_job.belief_name == example_belief.belief_name


def test_MomentUnit_rotate_job_ReturnsObj_Scenario2_EmptyVoicesCause_inallocable_voice_debt_points(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    init_sue_job = beliefunit_shop(sue_str, a23_str)
    init_sue_job.add_voiceunit(yao_str)
    init_sue_job.add_voiceunit(bob_str)
    init_sue_job.add_voiceunit(zia_str)
    save_job_file(moment_mstr_dir, init_sue_job)
    assert job_file_exists(moment_mstr_dir, a23_str, sue_str)
    assert job_file_exists(moment_mstr_dir, a23_str, yao_str) is False
    assert job_file_exists(moment_mstr_dir, a23_str, bob_str) is False
    assert job_file_exists(moment_mstr_dir, a23_str, zia_str) is False

    # WHEN
    rotated_sue_job = a23_moment.rotate_job(sue_str)

    # THEN method should wipe over job belief
    assert rotated_sue_job.voice_exists(bob_str)
    assert rotated_sue_job.to_dict() != init_sue_job.to_dict()
    assert init_sue_job.get_voice(bob_str).inallocable_voice_debt_points == 0
    assert rotated_sue_job.get_voice(bob_str).inallocable_voice_debt_points == 1


def a23_job(belief_name: str) -> BeliefUnit:
    moment_mstr_dir = get_module_temp_dir()
    return open_job_file(moment_mstr_dir, "amy23", belief_name)


def test_MomentUnit_rotate_job_ReturnsObj_Scenario3_job_ChangesFromRotation(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    init_sue_job = beliefunit_shop(sue_str, a23_str)
    init_sue_job.add_voiceunit(yao_str)
    init_yao_job = beliefunit_shop(yao_str, a23_str)
    init_yao_job.add_voiceunit(bob_str)
    init_bob_job = beliefunit_shop(bob_str, a23_str)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_plan(clean_rope, task=True)
    save_job_file(moment_mstr_dir, init_sue_job)
    save_job_file(moment_mstr_dir, init_yao_job)
    save_job_file(moment_mstr_dir, init_bob_job)
    assert len(a23_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_job(yao_str).get_agenda_dict()) == 0
    assert len(a23_job(bob_str).get_agenda_dict()) == 1

    # WHEN / THEN
    assert len(a23_moment.rotate_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_moment.rotate_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_moment.rotate_job(bob_str).get_agenda_dict()) == 0


def test_MomentUnit_rotate_job_ReturnsObj_Scenario4_job_SelfReferenceWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    init_bob_job = beliefunit_shop(bob_str, a23_str)
    init_bob_job.add_voiceunit(bob_str)
    init_sue_job = beliefunit_shop(sue_str, a23_str)
    init_sue_job.add_voiceunit(yao_str)
    init_yao_job = beliefunit_shop(yao_str, a23_str)
    init_yao_job.add_voiceunit(bob_str)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_plan(clean_rope, task=True)
    save_job_file(moment_mstr_dir, init_sue_job)
    save_job_file(moment_mstr_dir, init_yao_job)
    save_job_file(moment_mstr_dir, init_bob_job)
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_job(yao_str).get_agenda_dict()) == 0

    # WHEN / THEN
    assert len(a23_moment.rotate_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_moment.rotate_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_moment.rotate_job(yao_str).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario0_init_job_IsCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_module_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    bob_gut = beliefunit_shop(bob_str, a23_str)
    save_gut_file(moment_mstr_dir, bob_gut)
    sue_dir = create_belief_dir_path(moment_mstr_dir, a23_str, sue_str)
    set_dir(sue_dir)
    assert gut_file_exists(moment_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(moment_mstr_dir, a23_str, sue_str) is False
    assert job_file_exists(moment_mstr_dir, a23_str, bob_str) is False
    assert job_file_exists(moment_mstr_dir, a23_str, sue_str) is False

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert gut_file_exists(moment_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(moment_mstr_dir, a23_str, sue_str)
    assert job_file_exists(moment_mstr_dir, a23_str, bob_str)
    assert job_file_exists(moment_mstr_dir, a23_str, sue_str)


def test_MomentUnit_generate_all_jobs_Scenario1_jobs_rotated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    bob_gut = beliefunit_shop(bob_str, a23_str)
    bob_gut.add_voiceunit(bob_str)
    bob_gut.add_voiceunit(sue_str)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_plan(clean_rope, task=True)

    sue_gut = beliefunit_shop(sue_str, a23_str)
    sue_gut.add_voiceunit(sue_str)
    sue_gut.add_voiceunit(bob_str)
    yao_gut = beliefunit_shop(yao_str, a23_str)
    yao_gut.add_voiceunit(sue_str)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    assert not job_file_exists(moment_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(moment_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(moment_mstr_dir, a23_str, yao_str)

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario2_jobs_rotated_InSortedOrder(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_gut = beliefunit_shop(bob_str, a23_str)
    bob_gut.add_voiceunit(bob_str)
    bob_gut.add_voiceunit(sue_str)

    sue_gut = beliefunit_shop(sue_str, a23_str)
    sue_gut.add_voiceunit(sue_str)
    sue_gut.add_voiceunit(bob_str)
    sue_gut.add_voiceunit(yao_str)

    yao_gut = beliefunit_shop(yao_str, a23_str)
    yao_gut.add_voiceunit(sue_str)
    yao_gut.add_voiceunit(yao_str)
    yao_gut.add_voiceunit(zia_str)

    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.add_voiceunit(zia_str)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_plan(clean_rope, task=True)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    save_gut_file(moment_mstr_dir, zia_gut)
    assert not job_file_exists(moment_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(moment_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(moment_mstr_dir, a23_str, yao_str)
    assert not job_file_exists(moment_mstr_dir, a23_str, zia_str)

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 0
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1


def test_MomentUnit_generate_all_jobs_Scenario3_job_listen_rotation_AffectsJobs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_gut = beliefunit_shop(bob_str, a23_str)
    bob_gut.add_voiceunit(bob_str)
    bob_gut.add_voiceunit(sue_str)

    sue_gut = beliefunit_shop(sue_str, a23_str)
    sue_gut.add_voiceunit(sue_str)
    sue_gut.add_voiceunit(bob_str)
    sue_gut.add_voiceunit(yao_str)

    yao_gut = beliefunit_shop(yao_str, a23_str)
    yao_gut.add_voiceunit(sue_str)
    yao_gut.add_voiceunit(yao_str)
    yao_gut.add_voiceunit(zia_str)

    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.add_voiceunit(zia_str)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_plan(clean_rope, task=True)
    save_gut_file(moment_mstr_dir, bob_gut)
    save_gut_file(moment_mstr_dir, sue_gut)
    save_gut_file(moment_mstr_dir, yao_gut)
    save_gut_file(moment_mstr_dir, zia_gut)
    assert not job_file_exists(moment_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(moment_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(moment_mstr_dir, a23_str, yao_str)
    assert not job_file_exists(moment_mstr_dir, a23_str, zia_str)
    assert a23_moment.job_listen_rotations == 1

    # WHEN
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 0
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1

    # WHEN
    a23_moment.job_listen_rotations = 2
    a23_moment.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1
