from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import delete_dir
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_toolbox.hub_path import create_gut_path
from src.a12_hub_toolbox.hub_tool import save_gut_file, save_job_file
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a13_plan_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_jobs_into_job,
)
from src.a13_plan_listen_logic.test._util.a13_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a13_plan_listen_logic.test._util.example_listen import (
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


def test_listen_to_agendas_jobs_into_job_AddsChoresToPlanWhenNo_laborlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = env_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    yao_gut = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_score = 47
    zia_debt_score = 41
    zia_pool = 87
    yao_gut.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    yao_gut.set_acct_respect(zia_pool)
    save_gut_file(bank_mstr_dir, yao_gut)

    zia_job = planunit_shop(zia_str, a23_str)
    zia_job.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_acctunit(yao_str, debt_score=12)
    save_job_file(bank_mstr_dir, zia_job)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_concept_dict())=}")
    listen_to_agendas_jobs_into_job(bank_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_AddsChoresToPlan(env_dir_setup_cleanup):
    # ESTABLISH
    bank_mstr_dir = env_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    yao_gut = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_score = 47
    zia_debt_score = 41
    zia_pool = 87
    yao_gut.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    yao_gut.set_acct_respect(zia_pool)
    a23_str = "accord23"
    save_job_file(bank_mstr_dir, yao_gut)

    zia_job = planunit_shop(zia_str, a23_str)
    zia_job.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_acctunit(yao_str, debt_score=12)
    clean_conceptunit = zia_job.get_concept_obj(clean_rope())
    cook_conceptunit = zia_job.get_concept_obj(cook_rope())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_job_file(bank_mstr_dir, zia_job)
    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_concept_dict())=}")
    listen_to_agendas_jobs_into_job(bank_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_AddsChoresToPlanWithDetailsDecidedBy_debt_score(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = env_dir()
    zia_job = get_example_zia_speaker()
    bob_job = get_example_bob_speaker()
    bob_job.edit_concept_attr(
        cook_rope(),
        reason_del_premise_rcontext=eat_rope(),
        reason_del_premise_pstate=hungry_rope(),
    )
    bob_cook_conceptunit = bob_job.get_concept_obj(cook_rope())
    zia_cook_conceptunit = zia_job.get_concept_obj(cook_rope())
    assert bob_cook_conceptunit != zia_cook_conceptunit
    assert len(zia_cook_conceptunit.reasonunits) == 1
    assert len(bob_cook_conceptunit.reasonunits) == 0
    zia_str = zia_job.owner_name
    bob_str = bob_job.owner_name
    a23_str = "accord23"
    save_job_file(bank_mstr_dir, zia_job)
    save_job_file(bank_mstr_dir, bob_job)

    yao_gut = get_example_yao_speaker()
    yao_str = yao_gut.owner_name
    save_gut_file(bank_mstr_dir, yao_gut)

    new_yao_job1 = create_listen_basis(yao_gut)
    assert new_yao_job1.concept_exists(cook_rope()) is False

    # WHEN
    yao_hubunit = hubunit_shop(bank_mstr_dir, a23_str, yao_str)
    listen_to_agendas_jobs_into_job(bank_mstr_dir, new_yao_job1)

    # THEN
    assert new_yao_job1.concept_exists(cook_rope())
    new_cook_concept = new_yao_job1.get_concept_obj(cook_rope())
    zia_acctunit = new_yao_job1.get_acct(zia_str)
    bob_acctunit = new_yao_job1.get_acct(bob_str)
    assert zia_acctunit.debt_score < bob_acctunit.debt_score
    assert new_cook_concept.get_reasonunit(eat_rope()) is None

    yao_zia_debt_score = 15
    yao_bob_debt_score = 5
    yao_gut.add_acctunit(zia_str, None, yao_zia_debt_score)
    yao_gut.add_acctunit(bob_str, None, yao_bob_debt_score)
    yao_gut.set_acct_respect(100)
    new_yao_job2 = create_listen_basis(yao_gut)
    assert new_yao_job2.concept_exists(cook_rope()) is False

    # WHEN
    listen_to_agendas_jobs_into_job(bank_mstr_dir, new_yao_job2)

    # THEN
    assert new_yao_job2.concept_exists(cook_rope())
    new_cook_concept = new_yao_job2.get_concept_obj(cook_rope())
    zia_acctunit = new_yao_job2.get_acct(zia_str)
    bob_acctunit = new_yao_job2.get_acct(bob_str)
    assert zia_acctunit.debt_score > bob_acctunit.debt_score
    zia_eat_reasonunit = zia_cook_conceptunit.get_reasonunit(eat_rope())
    assert new_cook_concept.get_reasonunit(eat_rope()) == zia_eat_reasonunit


def test_listen_to_agendas_jobs_into_job_ProcessesIrrationalPlan(env_dir_setup_cleanup):
    # ESTABLISH
    bank_mstr_dir = env_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    yao_gut = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_score = 47
    zia_debt_score = 41
    sue_str = "Sue"
    sue_credit_score = 57
    sue_debt_score = 51
    yao_gut.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    yao_gut.add_acctunit(sue_str, sue_credit_score, sue_debt_score)
    yao_pool = 92
    yao_gut.set_acct_respect(yao_pool)
    a23_str = "accord23"
    save_gut_file(bank_mstr_dir, yao_gut)

    zia_str = "Zia"
    zia_job = planunit_shop(zia_str, a23_str)
    zia_job.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_acctunit(yao_str, debt_score=12)
    clean_conceptunit = zia_job.get_concept_obj(clean_rope())
    cook_conceptunit = zia_job.get_concept_obj(cook_rope())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_job_file(bank_mstr_dir, zia_job)

    sue_job = planunit_shop(sue_str, a23_str)
    sue_job.set_max_tree_traverse(5)
    zia_job.add_acctunit(yao_str, debt_score=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_job.make_l1_rope(vacuum_str)
    sue_job.set_l1_concept(conceptunit_shop(vacuum_str, task=True))
    vacuum_conceptunit = sue_job.get_concept_obj(vacuum_rope)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_rope = sue_job.make_l1_rope(egg_str)
    sue_job.set_l1_concept(conceptunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_job.make_l1_rope(chicken_str)
    sue_job.set_l1_concept(conceptunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_job.edit_concept_attr(
        egg_rope,
        task=True,
        reason_rcontext=chicken_rope,
        reason_rconcept_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_job.edit_concept_attr(
        chicken_rope,
        task=True,
        reason_rcontext=egg_rope,
        reason_rconcept_active_requisite=False,
    )
    save_job_file(bank_mstr_dir, sue_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(bank_mstr_dir, new_yao_job)

    # THEN irrational plan is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_acctunit = new_yao_job.get_acct(zia_str)
    sue_acctunit = new_yao_job.get_acct(sue_str)
    print(f"{sue_acctunit.debt_score=}")
    print(f"{sue_acctunit._irrational_debt_score=}")
    assert zia_acctunit._irrational_debt_score == 0
    assert sue_acctunit._irrational_debt_score == 51


def test_listen_to_agendas_jobs_into_job_ProcessesMissingDebtorPlan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = env_dir()
    yao_str = "Yao"
    a23_str = "accord23"
    yao_gut_path = create_gut_path(bank_mstr_dir, a23_str, yao_str)
    delete_dir(yao_gut_path)  # don't know why I have to do this...
    print(f"{os_path_exists(yao_gut_path)=}")
    yao_gut = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_credit_score = 47
    sue_credit_score = 57
    zia_debt_score = 41
    sue_debt_score = 51
    yao_gut.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    yao_gut.add_acctunit(sue_str, sue_credit_score, sue_debt_score)
    yao_pool = 92
    yao_gut.set_acct_respect(yao_pool)
    save_gut_file(bank_mstr_dir, yao_gut)

    zia_job = planunit_shop(zia_str, a23_str)
    zia_job.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_acctunit(yao_str, debt_score=12)
    clean_conceptunit = zia_job.get_concept_obj(clean_rope())
    cook_conceptunit = zia_job.get_concept_obj(cook_rope())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_job_file(bank_mstr_dir, zia_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(bank_mstr_dir, new_yao_job)

    # THEN irrational plan is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_acctunit = new_yao_job.get_acct(zia_str)
    sue_acctunit = new_yao_job.get_acct(sue_str)
    print(f"{sue_acctunit.debt_score=}")
    print(f"{sue_acctunit._inallocable_debt_score=}")
    assert zia_acctunit._inallocable_debt_score == 0
    assert sue_acctunit._inallocable_debt_score == 51


def test_listen_to_agendas_jobs_into_job_ListensToOwner_gut_AndNotOwner_job(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bank_mstr_dir = env_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    yao_gut = planunit_shop(yao_str, a23_str)
    yao_str = "Yao"
    yao_credit_score = 57
    yao_debt_score = 51
    yao_gut.add_acctunit(yao_str, yao_credit_score, yao_debt_score)
    zia_str = "Zia"
    zia_credit_score = 47
    zia_debt_score = 41
    yao_gut.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    yao_pool = 87
    yao_gut.set_acct_respect(yao_pool)
    # save yao without chore to dutys
    save_gut_file(bank_mstr_dir, yao_gut)

    # Save Zia to job
    zia_str = "Zia"
    zia_job = planunit_shop(zia_str, a23_str)
    zia_job.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_job.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_job.add_acctunit(yao_str, debt_score=12)
    clean_conceptunit = zia_job.get_concept_obj(clean_rope())
    cook_conceptunit = zia_job.get_concept_obj(cook_rope())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_job_file(bank_mstr_dir, zia_job)

    # save yao with chore to dutys
    yao_old_job = planunit_shop(yao_str, a23_str)
    vacuum_str = "vacuum"
    vacuum_rope = yao_old_job.make_l1_rope(vacuum_str)
    yao_old_job.set_l1_concept(conceptunit_shop(vacuum_str, task=True))
    vacuum_conceptunit = yao_old_job.get_concept_obj(vacuum_rope)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)
    save_job_file(bank_mstr_dir, yao_old_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(bank_mstr_dir, new_yao_job)

    # THEN irrational plan is ignored
    assert len(new_yao_job.get_agenda_dict()) != 2
    assert len(new_yao_job.get_agenda_dict()) == 3
