from src.a00_data_toolbox.file_toolbox import set_dir
from src.a06_believer_logic.believer import BelieverUnit, believerunit_shop
from src.a12_hub_toolbox.a12_path import create_believer_dir_path
from src.a12_hub_toolbox.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a15_belief_logic.belief import beliefunit_shop
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_BeliefUnit_rotate_job_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    belief_mstr_dir = get_module_temp_dir()
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    sue_str = "Sue"
    assert not job_file_exists(belief_mstr_dir, a23_str, sue_str)
    a23_belief.create_init_job_from_guts(sue_str)
    assert job_file_exists(belief_mstr_dir, a23_str, sue_str)

    # WHEN
    sue_job = a23_belief.rotate_job(sue_str)

    # THEN
    example_believer = believerunit_shop(sue_str, a23_str)
    assert sue_job.belief_label == example_believer.belief_label
    assert sue_job.believer_name == example_believer.believer_name


def test_BeliefUnit_rotate_job_ReturnsObj_Scenario2_EmptyPersonsCause_inallocable_person_debt_points(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    init_sue_job = believerunit_shop(sue_str, a23_str)
    init_sue_job.add_personunit(yao_str)
    init_sue_job.add_personunit(bob_str)
    init_sue_job.add_personunit(zia_str)
    save_job_file(belief_mstr_dir, init_sue_job)
    assert job_file_exists(belief_mstr_dir, a23_str, sue_str)
    assert job_file_exists(belief_mstr_dir, a23_str, yao_str) is False
    assert job_file_exists(belief_mstr_dir, a23_str, bob_str) is False
    assert job_file_exists(belief_mstr_dir, a23_str, zia_str) is False

    # WHEN
    rotated_sue_job = a23_belief.rotate_job(sue_str)

    # THEN method should wipe over job believer
    assert rotated_sue_job.person_exists(bob_str)
    assert rotated_sue_job.get_dict() != init_sue_job.get_dict()
    assert init_sue_job.get_person(bob_str)._inallocable_person_debt_points == 0
    assert rotated_sue_job.get_person(bob_str)._inallocable_person_debt_points == 1


def a23_job(believer_name: str) -> BelieverUnit:
    belief_mstr_dir = get_module_temp_dir()
    return open_job_file(belief_mstr_dir, "amy23", believer_name)


def test_BeliefUnit_rotate_job_ReturnsObj_Scenario3_job_ChangesFromRotation(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    init_sue_job = believerunit_shop(sue_str, a23_str)
    init_sue_job.add_personunit(yao_str)
    init_yao_job = believerunit_shop(yao_str, a23_str)
    init_yao_job.add_personunit(bob_str)
    init_bob_job = believerunit_shop(bob_str, a23_str)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_plan(clean_rope, task=True)
    save_job_file(belief_mstr_dir, init_sue_job)
    save_job_file(belief_mstr_dir, init_yao_job)
    save_job_file(belief_mstr_dir, init_bob_job)
    assert len(a23_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_job(yao_str).get_agenda_dict()) == 0
    assert len(a23_job(bob_str).get_agenda_dict()) == 1

    # WHEN / THEN
    assert len(a23_belief.rotate_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_belief.rotate_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_belief.rotate_job(bob_str).get_agenda_dict()) == 0


def test_BeliefUnit_rotate_job_ReturnsObj_Scenario4_job_SelfReferenceWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    init_bob_job = believerunit_shop(bob_str, a23_str)
    init_bob_job.add_personunit(bob_str)
    init_sue_job = believerunit_shop(sue_str, a23_str)
    init_sue_job.add_personunit(yao_str)
    init_yao_job = believerunit_shop(yao_str, a23_str)
    init_yao_job.add_personunit(bob_str)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_plan(clean_rope, task=True)
    save_job_file(belief_mstr_dir, init_sue_job)
    save_job_file(belief_mstr_dir, init_yao_job)
    save_job_file(belief_mstr_dir, init_bob_job)
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_job(yao_str).get_agenda_dict()) == 0

    # WHEN / THEN
    assert len(a23_belief.rotate_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_belief.rotate_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_belief.rotate_job(yao_str).get_agenda_dict()) == 1


def test_BeliefUnit_generate_all_jobs_Scenario0_init_job_IsCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    belief_mstr_dir = get_module_temp_dir()
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    bob_gut = believerunit_shop(bob_str, a23_str)
    save_gut_file(belief_mstr_dir, bob_gut)
    sue_dir = create_believer_dir_path(belief_mstr_dir, a23_str, sue_str)
    set_dir(sue_dir)
    assert gut_file_exists(belief_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(belief_mstr_dir, a23_str, sue_str) is False
    assert job_file_exists(belief_mstr_dir, a23_str, bob_str) is False
    assert job_file_exists(belief_mstr_dir, a23_str, sue_str) is False

    # WHEN
    a23_belief.generate_all_jobs()

    # THEN
    assert gut_file_exists(belief_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(belief_mstr_dir, a23_str, sue_str)
    assert job_file_exists(belief_mstr_dir, a23_str, bob_str)
    assert job_file_exists(belief_mstr_dir, a23_str, sue_str)


def test_BeliefUnit_generate_all_jobs_Scenario1_jobs_rotated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    bob_gut = believerunit_shop(bob_str, a23_str)
    bob_gut.add_personunit(bob_str)
    bob_gut.add_personunit(sue_str)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_plan(clean_rope, task=True)

    sue_gut = believerunit_shop(sue_str, a23_str)
    sue_gut.add_personunit(sue_str)
    sue_gut.add_personunit(bob_str)
    yao_gut = believerunit_shop(yao_str, a23_str)
    yao_gut.add_personunit(sue_str)
    save_gut_file(belief_mstr_dir, bob_gut)
    save_gut_file(belief_mstr_dir, sue_gut)
    save_gut_file(belief_mstr_dir, yao_gut)
    assert not job_file_exists(belief_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(belief_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(belief_mstr_dir, a23_str, yao_str)

    # WHEN
    a23_belief.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1


def test_BeliefUnit_generate_all_jobs_Scenario2_jobs_rotated_InSortedOrder(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_gut = believerunit_shop(bob_str, a23_str)
    bob_gut.add_personunit(bob_str)
    bob_gut.add_personunit(sue_str)

    sue_gut = believerunit_shop(sue_str, a23_str)
    sue_gut.add_personunit(sue_str)
    sue_gut.add_personunit(bob_str)
    sue_gut.add_personunit(yao_str)

    yao_gut = believerunit_shop(yao_str, a23_str)
    yao_gut.add_personunit(sue_str)
    yao_gut.add_personunit(yao_str)
    yao_gut.add_personunit(zia_str)

    zia_gut = believerunit_shop(zia_str, a23_str)
    zia_gut.add_personunit(zia_str)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_plan(clean_rope, task=True)
    save_gut_file(belief_mstr_dir, bob_gut)
    save_gut_file(belief_mstr_dir, sue_gut)
    save_gut_file(belief_mstr_dir, yao_gut)
    save_gut_file(belief_mstr_dir, zia_gut)
    assert not job_file_exists(belief_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(belief_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(belief_mstr_dir, a23_str, yao_str)
    assert not job_file_exists(belief_mstr_dir, a23_str, zia_str)

    # WHEN
    a23_belief.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 0
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1


def test_BeliefUnit_generate_all_jobs_Scenario3_job_listen_rotation_AffectsJobs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_gut = believerunit_shop(bob_str, a23_str)
    bob_gut.add_personunit(bob_str)
    bob_gut.add_personunit(sue_str)

    sue_gut = believerunit_shop(sue_str, a23_str)
    sue_gut.add_personunit(sue_str)
    sue_gut.add_personunit(bob_str)
    sue_gut.add_personunit(yao_str)

    yao_gut = believerunit_shop(yao_str, a23_str)
    yao_gut.add_personunit(sue_str)
    yao_gut.add_personunit(yao_str)
    yao_gut.add_personunit(zia_str)

    zia_gut = believerunit_shop(zia_str, a23_str)
    zia_gut.add_personunit(zia_str)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_plan(clean_rope, task=True)
    save_gut_file(belief_mstr_dir, bob_gut)
    save_gut_file(belief_mstr_dir, sue_gut)
    save_gut_file(belief_mstr_dir, yao_gut)
    save_gut_file(belief_mstr_dir, zia_gut)
    assert not job_file_exists(belief_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(belief_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(belief_mstr_dir, a23_str, yao_str)
    assert not job_file_exists(belief_mstr_dir, a23_str, zia_str)
    assert a23_belief.job_listen_rotations == 1

    # WHEN
    a23_belief.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 0
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1

    # WHEN
    a23_belief.job_listen_rotations = 2
    a23_belief.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1
