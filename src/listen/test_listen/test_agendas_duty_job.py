from src._instrument.file import delete_dir, save_file
from src._road.jaar_config import get_json_filename
from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.listen.hubunit import hubunit_shop
from src.listen.listen import create_listen_basis, listen_to_agendas_duty_job
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
    get_dakota_hubunit,
    get_dakota_road,
)
from src.listen.examples.example_listen import (
    cook_text,
    clean_text,
    run_text,
    casa_road,
    cook_road,
    eat_road,
    hungry_road,
    full_road,
    clean_road,
    run_road,
    get_example_yao_speaker,
    get_example_zia_speaker,
    get_example_bob_speaker,
)
from os.path import exists as os_path_exists


def test_listen_to_agenda_duty_job_agenda_AddsTasksToJob_BudWhenNo_teamlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    yao_duty.set_acct_respect(zia_pool)

    zia_job = budunit_shop(zia_text)
    zia_job.set_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.set_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_text, debtit_score=12)
    yao_dakota_hubunit = hubunit_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_hubunit.save_job_bud(zia_job)
    new_yao_job = create_listen_basis(yao_duty)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_idea_dict())=}")
    listen_to_agendas_duty_job(new_yao_job, yao_dakota_hubunit)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_job_agenda_AddsTasksToJob_Bud(env_dir_setup_cleanup):
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    yao_duty.set_acct_respect(zia_pool)

    zia_job = budunit_shop(zia_text)
    zia_job.set_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.set_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_text, debtit_score=12)
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    cook_ideaunit = zia_job.get_idea_obj(cook_road())
    clean_ideaunit._teamunit.set_teamlink(yao_text)
    cook_ideaunit._teamunit.set_teamlink(yao_text)
    yao_dakota_hubunit = hubunit_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_hubunit.save_job_bud(zia_job)

    # zia_file_path = f"{jobs_dir}/{zia_text}.json"
    # print(f"{os_path_exists(zia_file_path)=}")
    new_yao_job = create_listen_basis(yao_duty)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_idea_dict())=}")
    listen_to_agendas_duty_job(new_yao_job, yao_dakota_hubunit)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_job_agenda_AddsTasksToJobBudWithDetailsDecidedBy_debtit_score(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    zia_job = get_example_zia_speaker()
    bob_job = get_example_bob_speaker()
    bob_job.edit_idea_attr(
        road=cook_road(),
        reason_del_premise_base=eat_road(),
        reason_del_premise_need=hungry_road(),
    )
    bob_cook_ideaunit = bob_job.get_idea_obj(cook_road())
    zia_cook_ideaunit = zia_job.get_idea_obj(cook_road())
    assert bob_cook_ideaunit != zia_cook_ideaunit
    assert len(zia_cook_ideaunit._reasonunits) == 1
    assert len(bob_cook_ideaunit._reasonunits) == 0
    zia_text = zia_job._owner_id
    bob_text = bob_job._owner_id
    sue_dakota_hubunit = get_dakota_hubunit()
    sue_dakota_hubunit.save_job_bud(zia_job)
    sue_dakota_hubunit.save_job_bud(bob_job)

    yao_duty = get_example_yao_speaker()
    sue_dakota_hubunit.save_duty_bud(yao_duty)
    new_yao_action1 = create_listen_basis(yao_duty)
    assert new_yao_action1.idea_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_duty_job(new_yao_action1, sue_dakota_hubunit)

    # THEN
    assert new_yao_action1.idea_exists(cook_road())
    new_cook_idea = new_yao_action1.get_idea_obj(cook_road())
    zia_acctunit = new_yao_action1.get_acct(zia_text)
    bob_acctunit = new_yao_action1.get_acct(bob_text)
    assert zia_acctunit.debtit_score < bob_acctunit.debtit_score
    assert new_cook_idea.get_reasonunit(eat_road()) is None

    yao_zia_debtit_score = 15
    yao_bob_debtit_score = 5
    yao_duty.add_acctunit(zia_text, None, yao_zia_debtit_score)
    yao_duty.add_acctunit(bob_text, None, yao_bob_debtit_score)
    yao_duty.set_acct_respect(100)
    new_yao_action2 = create_listen_basis(yao_duty)
    assert new_yao_action2.idea_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_duty_job(new_yao_action2, sue_dakota_hubunit)

    # THEN
    assert new_yao_action2.idea_exists(cook_road())
    new_cook_idea = new_yao_action2.get_idea_obj(cook_road())
    zia_acctunit = new_yao_action2.get_acct(zia_text)
    bob_acctunit = new_yao_action2.get_acct(bob_text)
    assert zia_acctunit.debtit_score > bob_acctunit.debtit_score
    zia_eat_reasonunit = zia_cook_ideaunit.get_reasonunit(eat_road())
    assert new_cook_idea.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_agenda_duty_job_agenda_ProcessesIrrationalBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    sue_text = "Sue"
    sue_credit_score = 57
    sue_debtit_score = 51
    yao_duty.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    yao_duty.add_acctunit(sue_text, sue_credit_score, sue_debtit_score)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)
    yao_dakota_hubunit = hubunit_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_hubunit.save_duty_bud(yao_duty)

    zia_text = "Zia"
    zia_job = budunit_shop(zia_text)
    zia_job.set_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.set_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_text, debtit_score=12)
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    cook_ideaunit = zia_job.get_idea_obj(cook_road())
    clean_ideaunit._teamunit.set_teamlink(yao_text)
    cook_ideaunit._teamunit.set_teamlink(yao_text)
    yao_dakota_hubunit.save_job_bud(zia_job)

    sue_job = budunit_shop(sue_text)
    sue_job.set_max_tree_traverse(5)
    zia_job.add_acctunit(yao_text, debtit_score=12)
    vacuum_text = "vacuum"
    vacuum_road = sue_job.make_l1_road(vacuum_text)
    sue_job.set_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = sue_job.get_idea_obj(vacuum_road)
    vacuum_ideaunit._teamunit.set_teamlink(yao_text)

    egg_text = "egg first"
    egg_road = sue_job.make_l1_road(egg_text)
    sue_job.set_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_job.make_l1_road(chicken_text)
    sue_job.set_l1_idea(ideaunit_shop(chicken_text))
    # set egg pledge is True when chicken first is False
    sue_job.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_idea_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_job.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_idea_active_requisite=False,
    )
    yao_dakota_hubunit.save_job_bud(sue_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_duty)
    listen_to_agendas_duty_job(new_yao_job, yao_dakota_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_acctunit = new_yao_job.get_acct(zia_text)
    sue_acctunit = new_yao_job.get_acct(sue_text)
    print(f"{sue_acctunit.debtit_score=}")
    print(f"{sue_acctunit._irrational_debtit_score=}")
    assert zia_acctunit._irrational_debtit_score == 0
    assert sue_acctunit._irrational_debtit_score == 51


def test_listen_to_agenda_duty_job_agenda_ProcessesMissingDebtorJobBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    zia_text = "Zia"
    sue_text = "Sue"
    zia_credit_score = 47
    sue_credit_score = 57
    zia_debtit_score = 41
    sue_debtit_score = 51
    yao_duty.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    yao_duty.add_acctunit(sue_text, sue_credit_score, sue_debtit_score)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)
    yao_dakota_hubunit = hubunit_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_hubunit.save_duty_bud(yao_duty)

    zia_job = budunit_shop(zia_text)
    zia_job.set_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.set_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_text, debtit_score=12)
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    cook_ideaunit = zia_job.get_idea_obj(cook_road())
    clean_ideaunit._teamunit.set_teamlink(yao_text)
    cook_ideaunit._teamunit.set_teamlink(yao_text)
    yao_dakota_hubunit = hubunit_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_hubunit.save_job_bud(zia_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_duty)
    listen_to_agendas_duty_job(new_yao_job, yao_dakota_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_acctunit = new_yao_job.get_acct(zia_text)
    sue_acctunit = new_yao_job.get_acct(sue_text)
    print(f"{sue_acctunit.debtit_score=}")
    print(f"{sue_acctunit._inallocable_debtit_score=}")
    assert zia_acctunit._inallocable_debtit_score == 0
    assert sue_acctunit._inallocable_debtit_score == 51


def test_listen_to_agenda_duty_job_agenda_ListensToOwner_duty_AndNotOwner_job(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    yao_text = "Yao"
    yao_credit_score = 57
    yao_debtit_score = 51
    yao_duty.add_acctunit(yao_text, yao_credit_score, yao_debtit_score)
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    yao_duty.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    yao_pool = 87
    yao_duty.set_acct_respect(yao_pool)
    # save yao without task to dutys
    yao_dakota_hubunit = hubunit_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_hubunit.save_duty_bud(yao_duty)

    # Save Zia to jobs
    zia_text = "Zia"
    zia_job = budunit_shop(zia_text)
    zia_job.set_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.set_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_text, debtit_score=12)
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    cook_ideaunit = zia_job.get_idea_obj(cook_road())
    clean_ideaunit._teamunit.set_teamlink(yao_text)
    cook_ideaunit._teamunit.set_teamlink(yao_text)
    yao_dakota_hubunit.save_job_bud(zia_job)

    # save yao with task to jobs
    yao_old_job = budunit_shop(yao_text)
    vacuum_text = "vacuum"
    vacuum_road = yao_old_job.make_l1_road(vacuum_text)
    yao_old_job.set_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = yao_old_job.get_idea_obj(vacuum_road)
    vacuum_ideaunit._teamunit.set_teamlink(yao_text)
    yao_dakota_hubunit.save_job_bud(yao_old_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_duty)
    listen_to_agendas_duty_job(new_yao_job, yao_dakota_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_job_agenda_GetsAgendaFromSrcBudNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has task run_road
    # yao_job has task clean_road
    # yao_new_job picks yao_duty task run_road and not clean_road
    yao_duty = get_example_yao_speaker()
    assert yao_duty.idea_exists(run_road()) is False
    assert yao_duty.idea_exists(clean_road()) is False
    yao_duty.set_idea(ideaunit_shop(run_text(), pledge=True), casa_road())
    sue_dakota_hubunit = get_dakota_hubunit()
    sue_dakota_hubunit.save_duty_bud(yao_duty)

    yao_old_job = get_example_yao_speaker()
    assert yao_old_job.idea_exists(run_road()) is False
    assert yao_old_job.idea_exists(clean_road()) is False
    yao_old_job.set_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    sue_dakota_hubunit.save_job_bud(yao_old_job)

    yao_new_job = create_listen_basis(yao_duty)
    assert yao_new_job.idea_exists(run_road()) is False
    assert yao_new_job.idea_exists(clean_road()) is False

    # WHEN
    listen_to_agendas_duty_job(yao_new_job, sue_dakota_hubunit)

    # THEN
    assert yao_new_job.idea_exists(clean_road()) is False
    assert yao_new_job.idea_exists(run_road())
