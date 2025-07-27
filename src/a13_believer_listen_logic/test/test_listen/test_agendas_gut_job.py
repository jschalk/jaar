from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import delete_dir
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a12_hub_toolbox.a12_path import create_gut_path
from src.a12_hub_toolbox.hub_tool import save_gut_file, save_job_file
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a13_believer_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_jobs_into_job,
)
from src.a13_believer_listen_logic.test._util.a13_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a13_believer_listen_logic.test._util.example_listen import (
    casa_rope,
    clean_rope,
    clean_str,
    cook_rope,
    cook_str,
    eat_rope,
    full_rope,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
    hungry_rope,
    run_rope,
    run_str,
)


def test_listen_to_agendas_jobs_into_job_AddsChoresToBelieverWhenNo_laborlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = believerunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    zia_pool = 87
    yao_gut.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    yao_gut.set_partner_respect(zia_pool)
    save_gut_file(belief_mstr_dir, yao_gut)

    zia_job = believerunit_shop(zia_str, a23_str)
    zia_job.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_partnerunit(yao_str, partner_debt_points=12)
    save_job_file(belief_mstr_dir, zia_job)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_plan_dict())=}")
    listen_to_agendas_jobs_into_job(belief_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_AddsChoresToBeliever(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = believerunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    zia_pool = 87
    yao_gut.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    yao_gut.set_partner_respect(zia_pool)
    a23_str = "amy23"
    save_job_file(belief_mstr_dir, yao_gut)

    zia_job = believerunit_shop(zia_str, a23_str)
    zia_job.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_partnerunit(yao_str, partner_debt_points=12)
    clean_planunit = zia_job.get_plan_obj(clean_rope())
    cook_planunit = zia_job.get_plan_obj(cook_rope())
    clean_planunit.laborunit.set_laborlink(yao_str)
    cook_planunit.laborunit.set_laborlink(yao_str)
    save_job_file(belief_mstr_dir, zia_job)
    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_plan_dict())=}")
    listen_to_agendas_jobs_into_job(belief_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_AddsChoresToBelieverWithDetailsDecidedBy_partner_debt_points(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    zia_job = get_example_zia_speaker()
    bob_job = get_example_bob_speaker()
    bob_job.edit_plan_attr(
        cook_rope(),
        reason_del_case_r_context=eat_rope(),
        reason_del_case_r_state=hungry_rope(),
    )
    bob_cook_planunit = bob_job.get_plan_obj(cook_rope())
    zia_cook_planunit = zia_job.get_plan_obj(cook_rope())
    assert bob_cook_planunit != zia_cook_planunit
    assert len(zia_cook_planunit.reasonunits) == 1
    assert len(bob_cook_planunit.reasonunits) == 0
    zia_str = zia_job.believer_name
    bob_str = bob_job.believer_name
    a23_str = "amy23"
    save_job_file(belief_mstr_dir, zia_job)
    save_job_file(belief_mstr_dir, bob_job)

    yao_gut = get_example_yao_speaker()
    yao_str = yao_gut.believer_name
    save_gut_file(belief_mstr_dir, yao_gut)

    new_yao_job1 = create_listen_basis(yao_gut)
    assert new_yao_job1.plan_exists(cook_rope()) is False

    # WHEN
    yao_hubunit = hubunit_shop(belief_mstr_dir, a23_str, yao_str)
    listen_to_agendas_jobs_into_job(belief_mstr_dir, new_yao_job1)

    # THEN
    assert new_yao_job1.plan_exists(cook_rope())
    new_cook_plan = new_yao_job1.get_plan_obj(cook_rope())
    zia_partnerunit = new_yao_job1.get_partner(zia_str)
    bob_partnerunit = new_yao_job1.get_partner(bob_str)
    assert zia_partnerunit.partner_debt_points < bob_partnerunit.partner_debt_points
    assert new_cook_plan.get_reasonunit(eat_rope()) is None

    yao_zia_partner_debt_points = 15
    yao_bob_partner_debt_points = 5
    yao_gut.add_partnerunit(zia_str, None, yao_zia_partner_debt_points)
    yao_gut.add_partnerunit(bob_str, None, yao_bob_partner_debt_points)
    yao_gut.set_partner_respect(100)
    new_yao_job2 = create_listen_basis(yao_gut)
    assert new_yao_job2.plan_exists(cook_rope()) is False

    # WHEN
    listen_to_agendas_jobs_into_job(belief_mstr_dir, new_yao_job2)

    # THEN
    assert new_yao_job2.plan_exists(cook_rope())
    new_cook_plan = new_yao_job2.get_plan_obj(cook_rope())
    zia_partnerunit = new_yao_job2.get_partner(zia_str)
    bob_partnerunit = new_yao_job2.get_partner(bob_str)
    assert zia_partnerunit.partner_debt_points > bob_partnerunit.partner_debt_points
    zia_eat_reasonunit = zia_cook_planunit.get_reasonunit(eat_rope())
    assert new_cook_plan.get_reasonunit(eat_rope()) == zia_eat_reasonunit


def test_listen_to_agendas_jobs_into_job_ProcessesIrrationalBeliever(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = believerunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    sue_str = "Sue"
    sue_partner_cred_points = 57
    sue_partner_debt_points = 51
    yao_gut.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    yao_gut.add_partnerunit(sue_str, sue_partner_cred_points, sue_partner_debt_points)
    yao_pool = 92
    yao_gut.set_partner_respect(yao_pool)
    a23_str = "amy23"
    save_gut_file(belief_mstr_dir, yao_gut)

    zia_str = "Zia"
    zia_job = believerunit_shop(zia_str, a23_str)
    zia_job.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_partnerunit(yao_str, partner_debt_points=12)
    clean_planunit = zia_job.get_plan_obj(clean_rope())
    cook_planunit = zia_job.get_plan_obj(cook_rope())
    clean_planunit.laborunit.set_laborlink(yao_str)
    cook_planunit.laborunit.set_laborlink(yao_str)
    save_job_file(belief_mstr_dir, zia_job)

    sue_job = believerunit_shop(sue_str, a23_str)
    sue_job.set_max_tree_traverse(5)
    zia_job.add_partnerunit(yao_str, partner_debt_points=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_job.make_l1_rope(vacuum_str)
    sue_job.set_l1_plan(planunit_shop(vacuum_str, task=True))
    vacuum_planunit = sue_job.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_rope = sue_job.make_l1_rope(egg_str)
    sue_job.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_job.make_l1_rope(chicken_str)
    sue_job.set_l1_plan(planunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_job.edit_plan_attr(
        egg_rope,
        task=True,
        reason_r_context=chicken_rope,
        reason_r_plan_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_job.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_r_context=egg_rope,
        reason_r_plan_active_requisite=False,
    )
    save_job_file(belief_mstr_dir, sue_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(belief_mstr_dir, new_yao_job)

    # THEN irrational believer is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_partnerunit = new_yao_job.get_partner(zia_str)
    sue_partnerunit = new_yao_job.get_partner(sue_str)
    print(f"{sue_partnerunit.partner_debt_points=}")
    print(f"{sue_partnerunit._irrational_partner_debt_points=}")
    assert zia_partnerunit._irrational_partner_debt_points == 0
    assert sue_partnerunit._irrational_partner_debt_points == 51


def test_listen_to_agendas_jobs_into_job_ProcessesMissingDebtorBeliever(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    yao_str = "Yao"
    a23_str = "amy23"
    yao_gut_path = create_gut_path(belief_mstr_dir, a23_str, yao_str)
    delete_dir(yao_gut_path)  # don't know why I have to do this...
    print(f"{os_path_exists(yao_gut_path)=}")
    yao_gut = believerunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_partner_cred_points = 47
    sue_partner_cred_points = 57
    zia_partner_debt_points = 41
    sue_partner_debt_points = 51
    yao_gut.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    yao_gut.add_partnerunit(sue_str, sue_partner_cred_points, sue_partner_debt_points)
    yao_pool = 92
    yao_gut.set_partner_respect(yao_pool)
    save_gut_file(belief_mstr_dir, yao_gut)

    zia_job = believerunit_shop(zia_str, a23_str)
    zia_job.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_partnerunit(yao_str, partner_debt_points=12)
    clean_planunit = zia_job.get_plan_obj(clean_rope())
    cook_planunit = zia_job.get_plan_obj(cook_rope())
    clean_planunit.laborunit.set_laborlink(yao_str)
    cook_planunit.laborunit.set_laborlink(yao_str)
    save_job_file(belief_mstr_dir, zia_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(belief_mstr_dir, new_yao_job)

    # THEN irrational believer is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_partnerunit = new_yao_job.get_partner(zia_str)
    sue_partnerunit = new_yao_job.get_partner(sue_str)
    print(f"{sue_partnerunit.partner_debt_points=}")
    print(f"{sue_partnerunit._inallocable_partner_debt_points=}")
    assert zia_partnerunit._inallocable_partner_debt_points == 0
    assert sue_partnerunit._inallocable_partner_debt_points == 51


def test_listen_to_agendas_jobs_into_job_ListensToBeliever_gut_AndNotBeliever_job(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = believerunit_shop(yao_str, a23_str)
    yao_str = "Yao"
    yao_partner_cred_points = 57
    yao_partner_debt_points = 51
    yao_gut.add_partnerunit(yao_str, yao_partner_cred_points, yao_partner_debt_points)
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    yao_gut.add_partnerunit(zia_str, zia_partner_cred_points, zia_partner_debt_points)
    yao_pool = 87
    yao_gut.set_partner_respect(yao_pool)
    # save yao without chore to dutys
    save_gut_file(belief_mstr_dir, yao_gut)

    # Save Zia to job
    zia_str = "Zia"
    zia_job = believerunit_shop(zia_str, a23_str)
    zia_job.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_partnerunit(yao_str, partner_debt_points=12)
    clean_planunit = zia_job.get_plan_obj(clean_rope())
    cook_planunit = zia_job.get_plan_obj(cook_rope())
    clean_planunit.laborunit.set_laborlink(yao_str)
    cook_planunit.laborunit.set_laborlink(yao_str)
    save_job_file(belief_mstr_dir, zia_job)

    # save yao with chore to dutys
    yao_old_job = believerunit_shop(yao_str, a23_str)
    vacuum_str = "vacuum"
    vacuum_rope = yao_old_job.make_l1_rope(vacuum_str)
    yao_old_job.set_l1_plan(planunit_shop(vacuum_str, task=True))
    vacuum_planunit = yao_old_job.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.set_laborlink(yao_str)
    save_job_file(belief_mstr_dir, yao_old_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(belief_mstr_dir, new_yao_job)

    # THEN irrational believer is ignored
    assert len(new_yao_job.get_agenda_dict()) != 2
    assert len(new_yao_job.get_agenda_dict()) == 3
