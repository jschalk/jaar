from src._instrument.file import delete_dir, save_file
from src._road.jaar_config import get_json_filename
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.userhub import userhub_shop
from src.listen.listen import create_listen_basis, listen_to_intents_role_job
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
    get_dakota_userhub,
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


def test_listen_to_intent_role_job_intent_AddsTasksToJobAgendaWhenNo_suffgroupIsSet(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.set_party_pool(zia_pool)

    zia_job = agendaunit_shop(zia_text)
    zia_job.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_partyunit(yao_text, debtor_weight=12)
    yao_dakota_userhub = userhub_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_userhub.save_job_agenda(zia_job)
    new_yao_job = create_listen_basis(yao_role)
    assert len(new_yao_job.get_intent_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_idea_dict())=}")
    listen_to_intents_role_job(new_yao_job, yao_dakota_userhub)

    # THEN
    assert len(new_yao_job.get_intent_dict()) == 2


def test_listen_to_intent_role_job_intent_AddsTasksToJobAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.set_party_pool(zia_pool)

    zia_job = agendaunit_shop(zia_text)
    zia_job.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    cook_ideaunit = zia_job.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_dakota_userhub = userhub_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_userhub.save_job_agenda(zia_job)

    # zia_file_path = f"{jobs_dir}/{zia_text}.json"
    # print(f"{os_path_exists(zia_file_path)=}")
    new_yao_job = create_listen_basis(yao_role)
    assert len(new_yao_job.get_intent_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_idea_dict())=}")
    listen_to_intents_role_job(new_yao_job, yao_dakota_userhub)

    # THEN
    assert len(new_yao_job.get_intent_dict()) == 2


def test_listen_to_intent_role_job_intent_AddsTasksToJobAgendaWithDetailsDecidedBy_debtor_weight(
    env_dir_setup_cleanup,
):
    # GIVEN
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
    sue_dakota_userhub = get_dakota_userhub()
    sue_dakota_userhub.save_job_agenda(zia_job)
    sue_dakota_userhub.save_job_agenda(bob_job)

    yao_role = get_example_yao_speaker()
    sue_dakota_userhub.save_role_agenda(yao_role)
    new_yao_work1 = create_listen_basis(yao_role)
    assert new_yao_work1.idea_exists(cook_road()) is False

    # WHEN
    listen_to_intents_role_job(new_yao_work1, sue_dakota_userhub)

    # THEN
    assert new_yao_work1.idea_exists(cook_road())
    new_cook_idea = new_yao_work1.get_idea_obj(cook_road())
    zia_partyunit = new_yao_work1.get_party(zia_text)
    bob_partyunit = new_yao_work1.get_party(bob_text)
    assert zia_partyunit.debtor_weight < bob_partyunit.debtor_weight
    assert new_cook_idea.get_reasonunit(eat_road()) is None

    yao_zia_debtor_weight = 15
    yao_bob_debtor_weight = 5
    yao_role.add_partyunit(zia_text, None, yao_zia_debtor_weight)
    yao_role.add_partyunit(bob_text, None, yao_bob_debtor_weight)
    yao_role.set_party_pool(100)
    new_yao_work2 = create_listen_basis(yao_role)
    assert new_yao_work2.idea_exists(cook_road()) is False

    # WHEN
    listen_to_intents_role_job(new_yao_work2, sue_dakota_userhub)

    # THEN
    assert new_yao_work2.idea_exists(cook_road())
    new_cook_idea = new_yao_work2.get_idea_obj(cook_road())
    zia_partyunit = new_yao_work2.get_party(zia_text)
    bob_partyunit = new_yao_work2.get_party(bob_text)
    assert zia_partyunit.debtor_weight > bob_partyunit.debtor_weight
    zia_eat_reasonunit = zia_cook_ideaunit.get_reasonunit(eat_road())
    assert new_cook_idea.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_intent_role_job_intent_ProcessesIrrationalAgenda(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_creditor_weight = 57
    sue_debtor_weight = 51
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_role.set_party_pool(yao_pool)
    yao_dakota_userhub = userhub_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_userhub.save_role_agenda(yao_role)

    zia_text = "Zia"
    zia_job = agendaunit_shop(zia_text)
    zia_job.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    cook_ideaunit = zia_job.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_dakota_userhub.save_job_agenda(zia_job)

    sue_job = agendaunit_shop(sue_text)
    sue_job.set_max_tree_traverse(5)
    zia_job.add_partyunit(yao_text, debtor_weight=12)
    vacuum_text = "vacuum"
    vacuum_road = sue_job.make_l1_road(vacuum_text)
    sue_job.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = sue_job.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffgroup(yao_text)

    egg_text = "egg first"
    egg_road = sue_job.make_l1_road(egg_text)
    sue_job.add_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_job.make_l1_road(chicken_text)
    sue_job.add_l1_idea(ideaunit_shop(chicken_text))
    # set egg pledge is True when chicken first is False
    sue_job.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_suff_idea_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_job.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_suff_idea_active=False,
    )
    yao_dakota_userhub.save_job_agenda(sue_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_role)
    listen_to_intents_role_job(new_yao_job, yao_dakota_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_job.get_intent_dict()) != 3
    assert len(new_yao_job.get_intent_dict()) == 2
    zia_partyunit = new_yao_job.get_party(zia_text)
    sue_partyunit = new_yao_job.get_party(sue_text)
    print(f"{sue_partyunit.debtor_weight=}")
    print(f"{sue_partyunit._irrational_debtor_weight=}")
    assert zia_partyunit._irrational_debtor_weight == 0
    assert sue_partyunit._irrational_debtor_weight == 51


def test_listen_to_intent_role_job_intent_ProcessesMissingDebtorJobAgenda(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    sue_text = "Sue"
    zia_creditor_weight = 47
    sue_creditor_weight = 57
    zia_debtor_weight = 41
    sue_debtor_weight = 51
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_role.set_party_pool(yao_pool)
    yao_dakota_userhub = userhub_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_userhub.save_role_agenda(yao_role)

    zia_job = agendaunit_shop(zia_text)
    zia_job.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    cook_ideaunit = zia_job.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_dakota_userhub = userhub_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_userhub.save_job_agenda(zia_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_role)
    listen_to_intents_role_job(new_yao_job, yao_dakota_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_job.get_intent_dict()) != 3
    assert len(new_yao_job.get_intent_dict()) == 2
    zia_partyunit = new_yao_job.get_party(zia_text)
    sue_partyunit = new_yao_job.get_party(sue_text)
    print(f"{sue_partyunit.debtor_weight=}")
    print(f"{sue_partyunit._missing_debtor_weight=}")
    assert zia_partyunit._missing_debtor_weight == 0
    assert sue_partyunit._missing_debtor_weight == 51


def test_listen_to_intent_role_job_intent_ListensToOwner_role_AndNotOwner_job(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    yao_text = "Yao"
    yao_creditor_weight = 57
    yao_debtor_weight = 51
    yao_role.add_partyunit(yao_text, yao_creditor_weight, yao_debtor_weight)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_pool = 87
    yao_role.set_party_pool(yao_pool)
    # save yao without task to roles
    yao_dakota_userhub = userhub_shop(env_dir(), None, yao_text, get_dakota_road())
    yao_dakota_userhub.save_role_agenda(yao_role)

    # Save Zia to jobs
    zia_text = "Zia"
    zia_job = agendaunit_shop(zia_text)
    zia_job.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_job.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_job.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_job.get_idea_obj(clean_road())
    cook_ideaunit = zia_job.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_dakota_userhub.save_job_agenda(zia_job)

    # save yao with task to jobs
    yao_old_job = agendaunit_shop(yao_text)
    vacuum_text = "vacuum"
    vacuum_road = yao_old_job.make_l1_road(vacuum_text)
    yao_old_job.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = yao_old_job.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_dakota_userhub.save_job_agenda(yao_old_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_role)
    listen_to_intents_role_job(new_yao_job, yao_dakota_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_job.get_intent_dict()) != 3
    assert len(new_yao_job.get_intent_dict()) == 2


def test_listen_to_intent_role_job_intent_GetsIntentFromSrcAgendaNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao_role has task run_road
    # yao_job has task clean_road
    # yao_new_job picks yao_role task run_road and not clean_road
    yao_role = get_example_yao_speaker()
    assert yao_role.idea_exists(run_road()) is False
    assert yao_role.idea_exists(clean_road()) is False
    yao_role.add_idea(ideaunit_shop(run_text(), pledge=True), casa_road())
    sue_dakota_userhub = get_dakota_userhub()
    sue_dakota_userhub.save_role_agenda(yao_role)

    yao_old_job = get_example_yao_speaker()
    assert yao_old_job.idea_exists(run_road()) is False
    assert yao_old_job.idea_exists(clean_road()) is False
    yao_old_job.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    sue_dakota_userhub.save_job_agenda(yao_old_job)

    yao_new_job = create_listen_basis(yao_role)
    assert yao_new_job.idea_exists(run_road()) is False
    assert yao_new_job.idea_exists(clean_road()) is False

    # WHEN
    listen_to_intents_role_job(yao_new_job, sue_dakota_userhub)

    # THEN
    assert yao_new_job.idea_exists(clean_road()) is False
    assert yao_new_job.idea_exists(run_road())