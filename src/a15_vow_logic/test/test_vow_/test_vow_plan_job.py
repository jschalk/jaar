from src.a00_data_toolbox.file_toolbox import set_dir
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic.plan import PlanUnit, planunit_shop
from src.a12_hub_toolbox.hub_path import create_owner_dir_path
from src.a12_hub_toolbox.hub_tool import (
    gut_file_exists,
    job_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a15_vow_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_vow_logic.vow import vowunit_shop


def test_VowUnit_rotate_job_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    vow_mstr_dir = get_module_temp_dir()
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    sue_str = "Sue"
    assert not job_file_exists(vow_mstr_dir, a23_str, sue_str)
    a23_vow.create_init_job_from_guts(sue_str)
    assert job_file_exists(vow_mstr_dir, a23_str, sue_str)

    # WHEN
    sue_job = a23_vow.rotate_job(sue_str)

    # THEN
    example_plan = planunit_shop(sue_str, a23_str)
    assert sue_job.vow_label == example_plan.vow_label
    assert sue_job.owner_name == example_plan.owner_name


def test_VowUnit_rotate_job_ReturnsObj_Scenario2_EmptyAcctsCause_inallocable_debt_score(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    init_sue_job = planunit_shop(sue_str, a23_str)
    init_sue_job.add_acctunit(yao_str)
    init_sue_job.add_acctunit(bob_str)
    init_sue_job.add_acctunit(zia_str)
    save_job_file(vow_mstr_dir, init_sue_job)
    assert job_file_exists(vow_mstr_dir, a23_str, sue_str)
    assert job_file_exists(vow_mstr_dir, a23_str, yao_str) is False
    assert job_file_exists(vow_mstr_dir, a23_str, bob_str) is False
    assert job_file_exists(vow_mstr_dir, a23_str, zia_str) is False

    # WHEN
    rotated_sue_job = a23_vow.rotate_job(sue_str)

    # THEN method should wipe over job plan
    assert rotated_sue_job.acct_exists(bob_str)
    assert rotated_sue_job.get_dict() != init_sue_job.get_dict()
    assert init_sue_job.get_acct(bob_str)._inallocable_debt_score == 0
    assert rotated_sue_job.get_acct(bob_str)._inallocable_debt_score == 1


def a23_job(owner_name: str) -> PlanUnit:
    vow_mstr_dir = get_module_temp_dir()
    return open_job_file(vow_mstr_dir, "accord23", owner_name)


def test_VowUnit_rotate_job_ReturnsObj_Scenario3_job_ChangesFromRotation(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    init_sue_job = planunit_shop(sue_str, a23_str)
    init_sue_job.add_acctunit(yao_str)
    init_yao_job = planunit_shop(yao_str, a23_str)
    init_yao_job.add_acctunit(bob_str)
    init_bob_job = planunit_shop(bob_str, a23_str)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_concept(clean_rope, task=True)
    save_job_file(vow_mstr_dir, init_sue_job)
    save_job_file(vow_mstr_dir, init_yao_job)
    save_job_file(vow_mstr_dir, init_bob_job)
    assert len(a23_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_job(yao_str).get_agenda_dict()) == 0
    assert len(a23_job(bob_str).get_agenda_dict()) == 1

    # WHEN / THEN
    assert len(a23_vow.rotate_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_vow.rotate_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_vow.rotate_job(bob_str).get_agenda_dict()) == 0


def test_VowUnit_rotate_job_ReturnsObj_Scenario4_job_SelfReferenceWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    init_bob_job = planunit_shop(bob_str, a23_str)
    init_bob_job.add_acctunit(bob_str)
    init_sue_job = planunit_shop(sue_str, a23_str)
    init_sue_job.add_acctunit(yao_str)
    init_yao_job = planunit_shop(yao_str, a23_str)
    init_yao_job.add_acctunit(bob_str)
    casa_rope = init_bob_job.make_l1_rope("casa")
    clean_rope = init_bob_job.make_rope(casa_rope, "clean")
    init_bob_job.add_concept(clean_rope, task=True)
    save_job_file(vow_mstr_dir, init_sue_job)
    save_job_file(vow_mstr_dir, init_yao_job)
    save_job_file(vow_mstr_dir, init_bob_job)
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_job(yao_str).get_agenda_dict()) == 0

    # WHEN / THEN
    assert len(a23_vow.rotate_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_vow.rotate_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_vow.rotate_job(yao_str).get_agenda_dict()) == 1


# def test_VowUnit_rotate_job_ReturnsObj_Scenario3_Without_healerlink(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     a23_str = "accord23"
#     vow_mstr_dir = get_module_temp_dir()
#     a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
#     bob_str = "Bob"
#     a23_vow.create_init_job_from_guts(bob_str)
#     before_bob_job = a23_vow.rotate_job(bob_str)
#     sue_str = "Sue"
#     assert before_bob_job.acct_exists(sue_str) is False

#     # WHEN
#     bob_gut_plan = open_gut_file(vow_mstr_dir, a23_str, bob_str)
#     bob_gut_plan.add_acctunit(sue_str)
#     save_gut_file(a23_vow.vow_mstr_dir, bob_gut_plan)

#     # WHEN
#     after_bob_job = a23_vow.rotate_job(bob_str)

#     # THEN
#     assert after_bob_job.acct_exists(sue_str)


# def test_VowUnit_rotate_job_ReturnsObj_Scenario4_With_healerlink(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     a23_str = "accord23"
#     vow_mstr_dir = get_module_temp_dir()
#     a23_vow = vowunit_shop(a23_str, vow_mstr_dir)

#     bob_str = "Bob"
#     a23_vow.create_init_job_from_guts(bob_str)
#     after_bob_job = a23_vow.rotate_job(bob_str)
#     assert after_bob_job.acct_exists(bob_str) is False

#     # WHEN
#     bob_gut_plan = open_gut_file(vow_mstr_dir, a23_str, bob_str)
#     bob_gut_plan.add_acctunit(bob_str)
#     bob_gut_plan.set_acct_respect(100)
#     texas_str = "Texas"
#     texas_rope = bob_gut_plan.make_l1_rope(texas_str)
#     elpaso_str = "el paso"
#     elpaso_rope = bob_gut_plan.make_rope(texas_rope, elpaso_str)
#     elpaso_concept = conceptunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))
#     bob_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
#     bob_gut_plan.set_concept(elpaso_concept, texas_rope)
#     save_gut_file(a23_vow.vow_mstr_dir, bob_gut_plan)

#     after_bob_job = a23_vow.rotate_job(bob_str)

#     # THEN
#     assert after_bob_job.acct_exists(bob_str)


# def test_VowUnit_rotate_job_ReturnsObj_Scenario0_Empty_gut(env_dir_setup_cleanup):
#     # ESTABLISH
#     a23_str = "accord23"
#     vow_mstr_dir = get_module_temp_dir()
#     a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
#     sue_str = "Sue"
#     a23_vow.set_gut_if_none(sue_str)
#     sue_gut = open_gut_file(vow_mstr_dir, a23_str, sue_str)
#     assert len(sue_gut.get_acctunits_dict()) == 0

#     # WHEN / THEN
#     assert not a23_vow.rotate_job(sue_str)


# def test_VowUnit_rotate_job_ReturnsObj_Scenario1_gut_accts_Equal_job_accts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     vow_mstr_dir = get_module_temp_dir()
#     a23_str = "accord23"
#     a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
#     sue_str = "Sue"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     sue_gut = planunit_shop(sue_str, a23_str)
#     sue_gut.add_acctunit(sue_str)
#     sue_gut.add_acctunit(bob_str)
#     sue_gut.add_acctunit(yao_str)
#     save_gut_file(vow_mstr_dir, sue_gut)
#     sue_gut = open_gut_file(vow_mstr_dir, a23_str, sue_str)
#     assert len(sue_gut.get_acctunits_dict()) == 3

#     # WHEN
#     sue_job = a23_vow.rotate_job(sue_str)

#     # THEN
#     expected_job = planunit_shop(sue_str, a23_str)
#     expected_job.add_acctunit(sue_str)
#     expected_job.add_acctunit(bob_str)
#     expected_job.add_acctunit(yao_str)
#     expected_job.settle_plan()
#     sue_job.settle_plan()
#     assert sue_job.accts.keys() == expected_job.accts.keys()
#     expected_sue_acct = sue_job.get_acct(sue_str)
#     expected_bob_acct = sue_job.get_acct(bob_str)
#     assert sue_job.get_acct(sue_str) == expected_sue_acct
#     assert sue_job.get_acct(bob_str) == expected_bob_acct
#     print(f"{sue_job.get_acctunits_dict().get(bob_str)=}")
#     print(f"{expected_job.get_acctunits_dict().get(bob_str)=}")
#     assert sue_job.get_acctunits_dict() == expected_job.get_acctunits_dict()
#     assert sue_job.get_dict() == expected_job.get_dict()
#     assert 1 == 5


# def test_VowUnit_rotate_job_ReturnsObj_Scenario1_gut_with_Agenda(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     vow_mstr_dir = get_module_temp_dir()
#     a23_str = "accord23"
#     a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
#     sue_str = "Sue"
#     sue_plan = planunit_shop(sue_str, a23_str)
#     casa_rope = sue_plan.make_l1_rope("casa")
#     dirty_rope = sue_plan.make_rope(casa_rope, "dirty")
#     mop_rope = sue_plan.make_rope(casa_rope, "mop")
#     sue_plan.add_concept(mop_rope, task=True)
#     sue_plan.add_concept(dirty_rope)
#     sue_plan.edit_reason(mop_rope, casa_rope, dirty_rope)
#     sue_plan.add_fact(casa_rope, dirty_rope)
#     save_gut_file(vow_mstr_dir, sue_plan)
#     sue_gut = open_gut_file(vow_mstr_dir, a23_str, sue_str)
#     assert len(sue_gut.get_acctunits_dict()) == 0

#     # WHEN
#     sue_job = a23_vow.rotate_job(sue_str)

#     # THEN
#     expected_job = planunit_shop(sue_str, a23_str)
#     expected_job.add_concept(mop_rope, task=True)
#     expected_job.add_concept(dirty_rope)
#     expected_job.edit_reason(mop_rope, casa_rope, dirty_rope)
#     expected_job.add_fact(casa_rope, dirty_rope)
#     assert sue_job.vow_label == expected_job.vow_label
#     assert sue_job.owner_name == expected_job.owner_name
#     assert sue_job.get_agenda_dict() == expected_job.get_agenda_dict()
#     assert sue_job.get_dict() == expected_job.get_dict()


# def test_VowUnit_rotate_job_ReturnsObj_Scenario2_gut_with_FactUnit(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     vow_mstr_dir = get_module_temp_dir()
#     a23_str = "accord23"
#     a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
#     sue_str = "Sue"
#     sue_plan = planunit_shop(sue_str, a23_str)
#     casa_rope = sue_plan.make_l1_rope("casa")
#     clean_rope = sue_plan.make_rope(casa_rope, "clean")
#     dirty_rope = sue_plan.make_rope(casa_rope, "dirty")
#     mop_rope = sue_plan.make_rope(casa_rope, "mop")
#     sue_plan.add_concept(mop_rope, task=True)
#     sue_plan.add_concept(dirty_rope)
#     sue_plan.edit_reason(mop_rope, casa_rope, dirty_rope)
#     sue_plan.add_fact(casa_rope, clean_rope, create_missing_concepts=True)
#     save_gut_file(vow_mstr_dir, sue_plan)
#     sue_gut = open_gut_file(vow_mstr_dir, a23_str, sue_str)
#     assert len(sue_gut.get_acctunits_dict()) == 0

#     # WHEN
#     sue_job = a23_vow.rotate_job(sue_str)

#     # THEN
#     expected_job = planunit_shop(sue_str, a23_str)
#     expected_job.add_fact(casa_rope, clean_rope, create_missing_concepts=True)
#     assert sue_job.vow_label == expected_job.vow_label
#     assert sue_job.owner_name == expected_job.owner_name
#     assert sue_job.get_factunits_dict() == expected_job.get_factunits_dict()
#     assert sue_job.get_dict() == expected_job.get_dict()


def test_VowUnit_generate_all_jobs_Scenario0_init_job_IsCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    vow_mstr_dir = get_module_temp_dir()
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    bob_gut = planunit_shop(bob_str, a23_str)
    save_gut_file(vow_mstr_dir, bob_gut)
    sue_dir = create_owner_dir_path(vow_mstr_dir, a23_str, sue_str)
    set_dir(sue_dir)
    assert gut_file_exists(vow_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(vow_mstr_dir, a23_str, sue_str) is False
    assert job_file_exists(vow_mstr_dir, a23_str, bob_str) is False
    assert job_file_exists(vow_mstr_dir, a23_str, sue_str) is False

    # WHEN
    a23_vow.generate_all_jobs()

    # THEN
    assert gut_file_exists(vow_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(vow_mstr_dir, a23_str, sue_str)
    assert job_file_exists(vow_mstr_dir, a23_str, bob_str)
    assert job_file_exists(vow_mstr_dir, a23_str, sue_str)


def test_VowUnit_generate_all_jobs_Scenario1_jobs_rotated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    bob_gut = planunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit(bob_str)
    bob_gut.add_acctunit(sue_str)
    casa_rope = bob_gut.make_l1_rope("casa")
    clean_rope = bob_gut.make_rope(casa_rope, "clean")
    bob_gut.add_concept(clean_rope, task=True)

    sue_gut = planunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(sue_str)
    sue_gut.add_acctunit(bob_str)
    yao_gut = planunit_shop(yao_str, a23_str)
    yao_gut.add_acctunit(sue_str)
    save_gut_file(vow_mstr_dir, bob_gut)
    save_gut_file(vow_mstr_dir, sue_gut)
    save_gut_file(vow_mstr_dir, yao_gut)
    assert not job_file_exists(vow_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(vow_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(vow_mstr_dir, a23_str, yao_str)

    # WHEN
    a23_vow.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1


def test_VowUnit_generate_all_jobs_Scenario2_jobs_rotated_InSortedOrder(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_gut = planunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit(bob_str)
    bob_gut.add_acctunit(sue_str)

    sue_gut = planunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(sue_str)
    sue_gut.add_acctunit(bob_str)
    sue_gut.add_acctunit(yao_str)

    yao_gut = planunit_shop(yao_str, a23_str)
    yao_gut.add_acctunit(sue_str)
    yao_gut.add_acctunit(yao_str)
    yao_gut.add_acctunit(zia_str)

    zia_gut = planunit_shop(zia_str, a23_str)
    zia_gut.add_acctunit(zia_str)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_concept(clean_rope, task=True)
    save_gut_file(vow_mstr_dir, bob_gut)
    save_gut_file(vow_mstr_dir, sue_gut)
    save_gut_file(vow_mstr_dir, yao_gut)
    save_gut_file(vow_mstr_dir, zia_gut)
    assert not job_file_exists(vow_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(vow_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(vow_mstr_dir, a23_str, yao_str)
    assert not job_file_exists(vow_mstr_dir, a23_str, zia_str)

    # WHEN
    a23_vow.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 0
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1


def test_VowUnit_generate_all_jobs_Scenario3_job_listen_rotation_AffectsJobs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_vow = vowunit_shop(a23_str, vow_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_gut = planunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit(bob_str)
    bob_gut.add_acctunit(sue_str)

    sue_gut = planunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(sue_str)
    sue_gut.add_acctunit(bob_str)
    sue_gut.add_acctunit(yao_str)

    yao_gut = planunit_shop(yao_str, a23_str)
    yao_gut.add_acctunit(sue_str)
    yao_gut.add_acctunit(yao_str)
    yao_gut.add_acctunit(zia_str)

    zia_gut = planunit_shop(zia_str, a23_str)
    zia_gut.add_acctunit(zia_str)
    casa_rope = zia_gut.make_l1_rope("casa")
    clean_rope = zia_gut.make_rope(casa_rope, "clean")
    zia_gut.add_concept(clean_rope, task=True)
    save_gut_file(vow_mstr_dir, bob_gut)
    save_gut_file(vow_mstr_dir, sue_gut)
    save_gut_file(vow_mstr_dir, yao_gut)
    save_gut_file(vow_mstr_dir, zia_gut)
    assert not job_file_exists(vow_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(vow_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(vow_mstr_dir, a23_str, yao_str)
    assert not job_file_exists(vow_mstr_dir, a23_str, zia_str)
    assert a23_vow.job_listen_rotations == 1

    # WHEN
    a23_vow.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 0
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1

    # WHEN
    a23_vow.job_listen_rotations = 2
    a23_vow.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1


# def test_VowUnit_generate_all_jobs_Scenario2_job_limit_rotation_Changes_job(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     a23_str = "accord23"
#     vow_mstr_dir = get_module_temp_dir()
#     x_job_listen_rotations = 2
#     a23_vow = vowunit_shop(
#         a23_str, vow_mstr_dir, job_listen_rotations=x_job_listen_rotations
#     )

#     bob_str = "Bob"
#     sue_str = "Sue"
#     sue_str = "Sue"
#     a23_vow.create_init_job_from_guts(bob_str)
#     vow_mstr_dir = a23_vow.vow_mstr_dir
#     a23_vow.create_init_job_from_guts(sue_str)
#     bob_gut_plan = a23_vow.rotate_job(bob_str)
#     sue_gut_plan = a23_vow.rotate_job(sue_str)

#     texas_str = "Texas"
#     texas_rope = bob_gut_plan.make_l1_rope(texas_str)
#     elpaso_str = "el paso"
#     elpaso_rope = bob_gut_plan.make_rope(texas_rope, elpaso_str)
#     elpaso_concept = conceptunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))

#     bob_gut_plan = open_gut_file(vow_mstr_dir, a23_str, bob_str)
#     bob_gut_plan.add_acctunit(bob_str)
#     bob_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
#     bob_gut_plan.set_concept(elpaso_concept, texas_rope)
#     save_gut_file(a23_vow.vow_mstr_dir, bob_gut_plan)

#     sue_gut_plan = open_gut_file(vow_mstr_dir, a23_str, sue_str)
#     sue_gut_plan.add_acctunit(sue_str)
#     sue_gut_plan.add_acctunit(bob_str)
#     sue_gut_plan.set_l1_concept(conceptunit_shop(texas_str, problem_bool=True))
#     sue_gut_plan.set_concept(elpaso_concept, texas_rope)
#     save_gut_file(a23_vow.vow_mstr_dir, sue_gut_plan)

#     before_bob_job = a23_vow.get_job_file_plan(bob_str)
#     before_sue_job = a23_vow.get_job_file_plan(sue_str)
#     assert a23_vow.job_listen_rotations == 9
#     assert before_bob_job.acct_exists(bob_str) is False
#     assert before_sue_job.acct_exists(sue_str) is False

#     # WHEN
#     a23_vow.generate_all_jobs()

#     # THEN
#     after_bob_job = a23_vow.get_job_file_plan(bob_str)
#     after_sue_job = a23_vow.get_job_file_plan(sue_str)
#     assert after_bob_job.acct_exists(bob_str)
#     assert after_sue_job.acct_exists(sue_str)
