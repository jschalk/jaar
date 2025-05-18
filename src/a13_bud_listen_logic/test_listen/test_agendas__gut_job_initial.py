from src.a00_data_toolbox.file_toolbox import delete_dir, save_file
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hub_path import create_gut_path
from src.a12_hub_tools.hub_tool import save_gut_file, save_gut_file
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_bud_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_create_init_job_from_guts,
)
from src.a13_bud_listen_logic._utils.env_a13 import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)
from src.a13_bud_listen_logic._utils.example_listen import (
    cook_str,
    clean_str,
    run_str,
    casa_way,
    cook_way,
    eat_way,
    hungry_way,
    full_way,
    clean_way,
    run_way,
    get_example_yao_speaker,
    get_example_zia_speaker,
    get_example_bob_speaker,
)
from os.path import exists as os_path_exists


def test_listen_to_agendas_create_init_job_from_guts_AddsTasksToBudWhenNo_laborlinkIsSet(
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

    zia_gut = budunit_shop(zia_str, a23_str)
    zia_gut.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_gut.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_gut.add_acctunit(yao_str, debtit_belief=12)
    save_gut_file(fisc_mstr_dir, zia_gut)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_concept_dict())=}")
    listen_to_agendas_create_init_job_from_guts(fisc_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_create_init_job_from_guts_AddsTasksToBud(
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
    a23_str = "accord23"
    save_gut_file(fisc_mstr_dir, yao_gut)
    zia_gut = budunit_shop(zia_str, a23_str)
    zia_gut.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_gut.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_gut.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_gut.get_concept_obj(clean_way())
    cook_conceptunit = zia_gut.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_gut_file(fisc_mstr_dir, zia_gut)
    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_concept_dict())=}")
    listen_to_agendas_create_init_job_from_guts(fisc_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_create_init_job_from_guts_AddsTasksToBudWithDetailsDecidedBy_debtit_belief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = env_dir()
    zia_gut = get_example_zia_speaker()
    bob_gut = get_example_bob_speaker()
    bob_gut.edit_concept_attr(
        cook_way(),
        reason_del_premise_rcontext=eat_way(),
        reason_del_premise_pbranch=hungry_way(),
    )
    bob_cook_conceptunit = bob_gut.get_concept_obj(cook_way())
    zia_cook_conceptunit = zia_gut.get_concept_obj(cook_way())
    assert bob_cook_conceptunit != zia_cook_conceptunit
    assert len(zia_cook_conceptunit.reasonunits) == 1
    assert len(bob_cook_conceptunit.reasonunits) == 0
    zia_str = zia_gut.owner_name
    bob_str = bob_gut.owner_name
    a23_str = "accord23"
    save_gut_file(fisc_mstr_dir, zia_gut)
    save_gut_file(fisc_mstr_dir, bob_gut)

    yao_gut = get_example_yao_speaker()
    yao_str = yao_gut.owner_name
    save_gut_file(fisc_mstr_dir, yao_gut)

    new_yao_gut1 = create_listen_basis(yao_gut)
    assert new_yao_gut1.concept_exists(cook_way()) is False

    # WHEN
    yao_hubunit = hubunit_shop(fisc_mstr_dir, a23_str, yao_str)
    listen_to_agendas_create_init_job_from_guts(fisc_mstr_dir, new_yao_gut1)

    # THEN
    assert new_yao_gut1.concept_exists(cook_way())
    new_cook_concept = new_yao_gut1.get_concept_obj(cook_way())
    zia_acctunit = new_yao_gut1.get_acct(zia_str)
    bob_acctunit = new_yao_gut1.get_acct(bob_str)
    assert zia_acctunit.debtit_belief < bob_acctunit.debtit_belief
    assert new_cook_concept.get_reasonunit(eat_way()) is None

    yao_zia_debtit_belief = 15
    yao_bob_debtit_belief = 5
    yao_gut.add_acctunit(zia_str, None, yao_zia_debtit_belief)
    yao_gut.add_acctunit(bob_str, None, yao_bob_debtit_belief)
    yao_gut.set_acct_respect(100)
    new_yao_gut2 = create_listen_basis(yao_gut)
    assert new_yao_gut2.concept_exists(cook_way()) is False

    # WHEN
    listen_to_agendas_create_init_job_from_guts(fisc_mstr_dir, new_yao_gut2)

    # THEN
    assert new_yao_gut2.concept_exists(cook_way())
    new_cook_concept = new_yao_gut2.get_concept_obj(cook_way())
    zia_acctunit = new_yao_gut2.get_acct(zia_str)
    bob_acctunit = new_yao_gut2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    zia_eat_reasonunit = zia_cook_conceptunit.get_reasonunit(eat_way())
    assert new_cook_concept.get_reasonunit(eat_way()) == zia_eat_reasonunit


def test_listen_to_agendas_create_init_job_from_guts_ProcessesIrrationalBud(
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
    zia_gut = budunit_shop(zia_str, a23_str)
    zia_gut.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_gut.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_gut.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_gut.get_concept_obj(clean_way())
    cook_conceptunit = zia_gut.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_gut_file(fisc_mstr_dir, zia_gut)

    sue_gut = budunit_shop(sue_str, a23_str)
    sue_gut.set_max_tree_traverse(5)
    zia_gut.add_acctunit(yao_str, debtit_belief=12)
    vacuum_str = "vacuum"
    vacuum_way = sue_gut.make_l1_way(vacuum_str)
    sue_gut.set_l1_concept(conceptunit_shop(vacuum_str, pledge=True))
    vacuum_conceptunit = sue_gut.get_concept_obj(vacuum_way)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_way = sue_gut.make_l1_way(egg_str)
    sue_gut.set_l1_concept(conceptunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_way = sue_gut.make_l1_way(chicken_str)
    sue_gut.set_l1_concept(conceptunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_gut.edit_concept_attr(
        egg_way,
        pledge=True,
        reason_rcontext=chicken_way,
        reason_rcontext_concept_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_gut.edit_concept_attr(
        chicken_way,
        pledge=True,
        reason_rcontext=egg_way,
        reason_rcontext_concept_active_requisite=False,
    )
    save_gut_file(fisc_mstr_dir, sue_gut)

    # WHEN
    new_yao_gut = create_listen_basis(yao_gut)
    listen_to_agendas_create_init_job_from_guts(fisc_mstr_dir, new_yao_gut)

    # THEN irrational bud is ignored
    assert len(new_yao_gut.get_agenda_dict()) != 3
    assert len(new_yao_gut.get_agenda_dict()) == 2
    zia_acctunit = new_yao_gut.get_acct(zia_str)
    sue_acctunit = new_yao_gut.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 51


def test_listen_to_agendas_create_init_job_from_guts_ProcessesMissingDebtorBud(
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

    zia_gut = budunit_shop(zia_str, a23_str)
    zia_gut.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_gut.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_gut.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_gut.get_concept_obj(clean_way())
    cook_conceptunit = zia_gut.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_gut_file(fisc_mstr_dir, zia_gut)

    # WHEN
    new_yao_gut = create_listen_basis(yao_gut)
    listen_to_agendas_create_init_job_from_guts(fisc_mstr_dir, new_yao_gut)

    # THEN irrational bud is ignored
    assert len(new_yao_gut.get_agenda_dict()) != 3
    assert len(new_yao_gut.get_agenda_dict()) == 2
    zia_acctunit = new_yao_gut.get_acct(zia_str)
    sue_acctunit = new_yao_gut.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._inallocable_debtit_belief=}")
    assert zia_acctunit._inallocable_debtit_belief == 0
    assert sue_acctunit._inallocable_debtit_belief == 51
