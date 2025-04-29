from src.a00_data_toolbox.file_toolbox import delete_dir
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hub_path import create_gut_path
from src.a12_hub_tools.hub_tool import save_gut_file, save_job_file
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_bud_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_jobs_into_job,
)
from src.a13_bud_listen_logic._utils.example_listen import (
    cook_str,
    clean_str,
    run_str,
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
from src.a13_bud_listen_logic._utils.env_utils import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_listen_to_agendas_jobs_into_job_AddsTasksToBudWhenNo_teamlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = env_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    yao_gut = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_gut.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_gut.set_acct_respect(zia_pool)
    save_gut_file(fisc_mstr_dir, yao_gut)

    zia_job = budunit_shop(zia_str, a23_str)
    zia_job.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_job.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_str, debtit_belief=12)
    save_job_file(fisc_mstr_dir, zia_job)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_item_dict())=}")
    listen_to_agendas_jobs_into_job(fisc_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_AddsTasksToBud(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = env_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    yao_gut = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_gut.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_gut.set_acct_respect(zia_pool)
    a23_str = "accord23"
    save_job_file(fisc_mstr_dir, yao_gut)

    zia_job = budunit_shop(zia_str, a23_str)
    zia_job.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_job.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_str, debtit_belief=12)
    clean_itemunit = zia_job.get_item_obj(clean_road())
    cook_itemunit = zia_job.get_item_obj(cook_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    cook_itemunit.teamunit.set_teamlink(yao_str)
    save_job_file(fisc_mstr_dir, zia_job)
    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_item_dict())=}")
    listen_to_agendas_jobs_into_job(fisc_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_jobs_into_job_AddsTasksToBudWithDetailsDecidedBy_debtit_belief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = env_dir()
    zia_job = get_example_zia_speaker()
    bob_job = get_example_bob_speaker()
    bob_job.edit_item_attr(
        road=cook_road(),
        reason_del_premise_base=eat_road(),
        reason_del_premise_need=hungry_road(),
    )
    bob_cook_itemunit = bob_job.get_item_obj(cook_road())
    zia_cook_itemunit = zia_job.get_item_obj(cook_road())
    assert bob_cook_itemunit != zia_cook_itemunit
    assert len(zia_cook_itemunit.reasonunits) == 1
    assert len(bob_cook_itemunit.reasonunits) == 0
    zia_str = zia_job.owner_name
    bob_str = bob_job.owner_name
    a23_str = "accord23"
    save_job_file(fisc_mstr_dir, zia_job)
    save_job_file(fisc_mstr_dir, bob_job)

    yao_gut = get_example_yao_speaker()
    yao_str = yao_gut.owner_name
    save_gut_file(fisc_mstr_dir, yao_gut)

    new_yao_job1 = create_listen_basis(yao_gut)
    assert new_yao_job1.item_exists(cook_road()) is False

    # WHEN
    yao_hubunit = hubunit_shop(fisc_mstr_dir, a23_str, yao_str)
    listen_to_agendas_jobs_into_job(fisc_mstr_dir, new_yao_job1)

    # THEN
    assert new_yao_job1.item_exists(cook_road())
    new_cook_item = new_yao_job1.get_item_obj(cook_road())
    zia_acctunit = new_yao_job1.get_acct(zia_str)
    bob_acctunit = new_yao_job1.get_acct(bob_str)
    assert zia_acctunit.debtit_belief < bob_acctunit.debtit_belief
    assert new_cook_item.get_reasonunit(eat_road()) is None

    yao_zia_debtit_belief = 15
    yao_bob_debtit_belief = 5
    yao_gut.add_acctunit(zia_str, None, yao_zia_debtit_belief)
    yao_gut.add_acctunit(bob_str, None, yao_bob_debtit_belief)
    yao_gut.set_acct_respect(100)
    new_yao_job2 = create_listen_basis(yao_gut)
    assert new_yao_job2.item_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_jobs_into_job(fisc_mstr_dir, new_yao_job2)

    # THEN
    assert new_yao_job2.item_exists(cook_road())
    new_cook_item = new_yao_job2.get_item_obj(cook_road())
    zia_acctunit = new_yao_job2.get_acct(zia_str)
    bob_acctunit = new_yao_job2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    zia_eat_reasonunit = zia_cook_itemunit.get_reasonunit(eat_road())
    assert new_cook_item.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_agendas_jobs_into_job_ProcessesIrrationalBud(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = env_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    yao_gut = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    sue_str = "Sue"
    sue_credit_belief = 57
    sue_debtit_belief = 51
    yao_gut.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_gut.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_gut.set_acct_respect(yao_pool)
    a23_str = "accord23"
    save_gut_file(fisc_mstr_dir, yao_gut)

    zia_str = "Zia"
    zia_job = budunit_shop(zia_str, a23_str)
    zia_job.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_job.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_str, debtit_belief=12)
    clean_itemunit = zia_job.get_item_obj(clean_road())
    cook_itemunit = zia_job.get_item_obj(cook_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    cook_itemunit.teamunit.set_teamlink(yao_str)
    save_job_file(fisc_mstr_dir, zia_job)

    sue_job = budunit_shop(sue_str, a23_str)
    sue_job.set_max_tree_traverse(5)
    zia_job.add_acctunit(yao_str, debtit_belief=12)
    vacuum_str = "vacuum"
    vacuum_road = sue_job.make_l1_road(vacuum_str)
    sue_job.set_l1_item(itemunit_shop(vacuum_str, pledge=True))
    vacuum_itemunit = sue_job.get_item_obj(vacuum_road)
    vacuum_itemunit.teamunit.set_teamlink(yao_str)

    egg_str = "egg first"
    egg_road = sue_job.make_l1_road(egg_str)
    sue_job.set_l1_item(itemunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_road = sue_job.make_l1_road(chicken_str)
    sue_job.set_l1_item(itemunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_job.edit_item_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_base_item_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_job.edit_item_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_base_item_active_requisite=False,
    )
    save_job_file(fisc_mstr_dir, sue_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(fisc_mstr_dir, new_yao_job)

    # THEN irrational bud is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_acctunit = new_yao_job.get_acct(zia_str)
    sue_acctunit = new_yao_job.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 51


def test_listen_to_agendas_jobs_into_job_ProcessesMissingDebtorBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = env_dir()
    yao_str = "Yao"
    a23_str = "accord23"
    yao_gut_path = create_gut_path(fisc_mstr_dir, a23_str, yao_str)
    delete_dir(yao_gut_path)  # don't know why I have to do this...
    print(f"{os_path_exists(yao_gut_path)=}")
    yao_gut = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_credit_belief = 47
    sue_credit_belief = 57
    zia_debtit_belief = 41
    sue_debtit_belief = 51
    yao_gut.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_gut.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_gut.set_acct_respect(yao_pool)
    save_gut_file(fisc_mstr_dir, yao_gut)

    zia_job = budunit_shop(zia_str, a23_str)
    zia_job.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_job.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_str, debtit_belief=12)
    clean_itemunit = zia_job.get_item_obj(clean_road())
    cook_itemunit = zia_job.get_item_obj(cook_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    cook_itemunit.teamunit.set_teamlink(yao_str)
    save_job_file(fisc_mstr_dir, zia_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(fisc_mstr_dir, new_yao_job)

    # THEN irrational bud is ignored
    assert len(new_yao_job.get_agenda_dict()) != 3
    assert len(new_yao_job.get_agenda_dict()) == 2
    zia_acctunit = new_yao_job.get_acct(zia_str)
    sue_acctunit = new_yao_job.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._inallocable_debtit_belief=}")
    assert zia_acctunit._inallocable_debtit_belief == 0
    assert sue_acctunit._inallocable_debtit_belief == 51


def test_listen_to_agendas_jobs_into_job_ListensToOwner_gut_AndNotOwner_job(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = env_dir()
    a23_str = "accord23"
    yao_str = "Yao"
    yao_gut = budunit_shop(yao_str, a23_str)
    yao_str = "Yao"
    yao_credit_belief = 57
    yao_debtit_belief = 51
    yao_gut.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    yao_gut.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_pool = 87
    yao_gut.set_acct_respect(yao_pool)
    # save yao without task to dutys
    save_gut_file(fisc_mstr_dir, yao_gut)

    # Save Zia to job
    zia_str = "Zia"
    zia_job = budunit_shop(zia_str, a23_str)
    zia_job.set_item(itemunit_shop(clean_str(), pledge=True), casa_road())
    zia_job.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    zia_job.add_acctunit(yao_str, debtit_belief=12)
    clean_itemunit = zia_job.get_item_obj(clean_road())
    cook_itemunit = zia_job.get_item_obj(cook_road())
    clean_itemunit.teamunit.set_teamlink(yao_str)
    cook_itemunit.teamunit.set_teamlink(yao_str)
    save_job_file(fisc_mstr_dir, zia_job)

    # save yao with task to dutys
    yao_old_job = budunit_shop(yao_str, a23_str)
    vacuum_str = "vacuum"
    vacuum_road = yao_old_job.make_l1_road(vacuum_str)
    yao_old_job.set_l1_item(itemunit_shop(vacuum_str, pledge=True))
    vacuum_itemunit = yao_old_job.get_item_obj(vacuum_road)
    vacuum_itemunit.teamunit.set_teamlink(yao_str)
    save_job_file(fisc_mstr_dir, yao_old_job)

    # WHEN
    new_yao_job = create_listen_basis(yao_gut)
    listen_to_agendas_jobs_into_job(fisc_mstr_dir, new_yao_job)

    # THEN irrational bud is ignored
    assert len(new_yao_job.get_agenda_dict()) != 2
    assert len(new_yao_job.get_agenda_dict()) == 3
