from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_bud_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_duty_plan,
)
from src.a13_bud_listen_logic._test_util.example_listen_hub import (
    get_dakota_hubunit,
    get_dakota_way,
)
from src.a13_bud_listen_logic._test_util.a13_env import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)
from src.a13_bud_listen_logic._test_util.example_listen import (
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


def test_listen_to_agenda_duty_plan_agenda_AddsTasksToplan_BudWhenNo_laborlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.set_acct_respect(zia_pool)

    zia_plan = budunit_shop(zia_str, a23_str)
    zia_plan.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_plan.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_plan.add_acctunit(yao_str, debtit_belief=12)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_plan_bud(zia_plan)
    new_yao_plan = create_listen_basis(yao_duty)
    assert len(new_yao_plan.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_plan.get_concept_dict())=}")
    listen_to_agendas_duty_plan(new_yao_plan, yao_dakota_hubunit)

    # THEN
    assert len(new_yao_plan.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_plan_agenda_AddsTasksToplan_Bud(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.set_acct_respect(zia_pool)

    zia_plan = budunit_shop(zia_str, a23_str)
    zia_plan.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_plan.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_plan.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_plan.get_concept_obj(clean_way())
    cook_conceptunit = zia_plan.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_plan_bud(zia_plan)

    # zia_file_path = create_path(plans_dir, zia_str}.json")
    # print(f"{os_path_exists(zia_file_path)=}")
    new_yao_plan = create_listen_basis(yao_duty)
    assert len(new_yao_plan.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_plan.get_concept_dict())=}")
    listen_to_agendas_duty_plan(new_yao_plan, yao_dakota_hubunit)

    # THEN
    assert len(new_yao_plan.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_plan_agenda_AddsTasksToplanBudWithDetailsDecidedBy_debtit_belief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    zia_plan = get_example_zia_speaker()
    bob_plan = get_example_bob_speaker()
    bob_plan.edit_concept_attr(
        cook_way(),
        reason_del_premise_rcontext=eat_way(),
        reason_del_premise_pstate=hungry_way(),
    )
    bob_cook_conceptunit = bob_plan.get_concept_obj(cook_way())
    zia_cook_conceptunit = zia_plan.get_concept_obj(cook_way())
    assert bob_cook_conceptunit != zia_cook_conceptunit
    assert len(zia_cook_conceptunit.reasonunits) == 1
    assert len(bob_cook_conceptunit.reasonunits) == 0
    zia_str = zia_plan.owner_name
    bob_str = bob_plan.owner_name
    sue_dakota_hubunit = get_dakota_hubunit()
    sue_dakota_hubunit.save_plan_bud(zia_plan)
    sue_dakota_hubunit.save_plan_bud(bob_plan)

    yao_duty = get_example_yao_speaker()
    sue_dakota_hubunit.save_duty_bud(yao_duty)
    new_yao_job1 = create_listen_basis(yao_duty)
    assert new_yao_job1.concept_exists(cook_way()) is False

    # WHEN
    listen_to_agendas_duty_plan(new_yao_job1, sue_dakota_hubunit)

    # THEN
    assert new_yao_job1.concept_exists(cook_way())
    new_cook_concept = new_yao_job1.get_concept_obj(cook_way())
    zia_acctunit = new_yao_job1.get_acct(zia_str)
    bob_acctunit = new_yao_job1.get_acct(bob_str)
    assert zia_acctunit.debtit_belief < bob_acctunit.debtit_belief
    assert new_cook_concept.get_reasonunit(eat_way()) is None

    yao_zia_debtit_belief = 15
    yao_bob_debtit_belief = 5
    yao_duty.add_acctunit(zia_str, None, yao_zia_debtit_belief)
    yao_duty.add_acctunit(bob_str, None, yao_bob_debtit_belief)
    yao_duty.set_acct_respect(100)
    new_yao_job2 = create_listen_basis(yao_duty)
    assert new_yao_job2.concept_exists(cook_way()) is False

    # WHEN
    listen_to_agendas_duty_plan(new_yao_job2, sue_dakota_hubunit)

    # THEN
    assert new_yao_job2.concept_exists(cook_way())
    new_cook_concept = new_yao_job2.get_concept_obj(cook_way())
    zia_acctunit = new_yao_job2.get_acct(zia_str)
    bob_acctunit = new_yao_job2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    zia_eat_reasonunit = zia_cook_conceptunit.get_reasonunit(eat_way())
    assert new_cook_concept.get_reasonunit(eat_way()) == zia_eat_reasonunit


def test_listen_to_agenda_duty_plan_agenda_ProcessesIrrationalBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    sue_str = "Sue"
    sue_credit_belief = 57
    sue_debtit_belief = 51
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_duty_bud(yao_duty)

    zia_str = "Zia"
    zia_plan = budunit_shop(zia_str, a23_str)
    zia_plan.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_plan.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_plan.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_plan.get_concept_obj(clean_way())
    cook_conceptunit = zia_plan.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_plan_bud(zia_plan)

    sue_plan = budunit_shop(sue_str)
    sue_plan.set_max_tree_traverse(5)
    zia_plan.add_acctunit(yao_str, debtit_belief=12)
    vacuum_str = "vacuum"
    vacuum_way = sue_plan.make_l1_way(vacuum_str)
    sue_plan.set_l1_concept(conceptunit_shop(vacuum_str, pledge=True))
    vacuum_conceptunit = sue_plan.get_concept_obj(vacuum_way)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_way = sue_plan.make_l1_way(egg_str)
    sue_plan.set_l1_concept(conceptunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_way = sue_plan.make_l1_way(chicken_str)
    sue_plan.set_l1_concept(conceptunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_plan.edit_concept_attr(
        egg_way,
        pledge=True,
        reason_rcontext=chicken_way,
        reason_rcontext_concept_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_plan.edit_concept_attr(
        chicken_way,
        pledge=True,
        reason_rcontext=egg_way,
        reason_rcontext_concept_active_requisite=False,
    )
    yao_dakota_hubunit.save_plan_bud(sue_plan)

    # WHEN
    new_yao_plan = create_listen_basis(yao_duty)
    listen_to_agendas_duty_plan(new_yao_plan, yao_dakota_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_plan.get_agenda_dict()) != 3
    assert len(new_yao_plan.get_agenda_dict()) == 2
    zia_acctunit = new_yao_plan.get_acct(zia_str)
    sue_acctunit = new_yao_plan.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 51


def test_listen_to_agenda_duty_plan_agenda_ProcessesMissingDebtorplanBud(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_credit_belief = 47
    sue_credit_belief = 57
    zia_debtit_belief = 41
    sue_debtit_belief = 51
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_duty.set_acct_respect(yao_pool)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_duty_bud(yao_duty)

    zia_plan = budunit_shop(zia_str, a23_str)
    zia_plan.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_plan.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_plan.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_plan.get_concept_obj(clean_way())
    cook_conceptunit = zia_plan.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_plan_bud(zia_plan)

    # WHEN
    new_yao_plan = create_listen_basis(yao_duty)
    listen_to_agendas_duty_plan(new_yao_plan, yao_dakota_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_plan.get_agenda_dict()) != 3
    assert len(new_yao_plan.get_agenda_dict()) == 2
    zia_acctunit = new_yao_plan.get_acct(zia_str)
    sue_acctunit = new_yao_plan.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._inallocable_debtit_belief=}")
    assert zia_acctunit._inallocable_debtit_belief == 0
    assert sue_acctunit._inallocable_debtit_belief == 51


def test_listen_to_agenda_duty_plan_agenda_ListensToOwner_duty_AndNotOwner_plan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str, a23_str)
    yao_str = "Yao"
    yao_credit_belief = 57
    yao_debtit_belief = 51
    yao_duty.add_acctunit(yao_str, yao_credit_belief, yao_debtit_belief)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_pool = 87
    yao_duty.set_acct_respect(yao_pool)
    # save yao without task to dutys
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_duty_bud(yao_duty)

    # Save Zia to plans
    zia_str = "Zia"
    zia_plan = budunit_shop(zia_str, a23_str)
    zia_plan.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    zia_plan.set_concept(conceptunit_shop(cook_str(), pledge=True), casa_way())
    zia_plan.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_plan.get_concept_obj(clean_way())
    cook_conceptunit = zia_plan.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_plan_bud(zia_plan)

    # save yao with task to plans
    yao_old_plan = budunit_shop(yao_str, a23_str)
    vacuum_str = "vacuum"
    vacuum_way = yao_old_plan.make_l1_way(vacuum_str)
    yao_old_plan.set_l1_concept(conceptunit_shop(vacuum_str, pledge=True))
    vacuum_conceptunit = yao_old_plan.get_concept_obj(vacuum_way)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_plan_bud(yao_old_plan)

    # WHEN
    new_yao_plan = create_listen_basis(yao_duty)
    listen_to_agendas_duty_plan(new_yao_plan, yao_dakota_hubunit)

    # THEN irrational bud is ignored
    assert len(new_yao_plan.get_agenda_dict()) != 3
    assert len(new_yao_plan.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_plan_agenda_GetsAgendaFromSrcBudNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has task run_way
    # yao_plan has task clean_way
    # yao_new_plan fstates yao_duty task run_way and not clean_way
    yao_duty = get_example_yao_speaker()
    assert yao_duty.concept_exists(run_way()) is False
    assert yao_duty.concept_exists(clean_way()) is False
    yao_duty.set_concept(conceptunit_shop(run_str(), pledge=True), casa_way())
    sue_dakota_hubunit = get_dakota_hubunit()
    sue_dakota_hubunit.save_duty_bud(yao_duty)

    yao_old_plan = get_example_yao_speaker()
    assert yao_old_plan.concept_exists(run_way()) is False
    assert yao_old_plan.concept_exists(clean_way()) is False
    yao_old_plan.set_concept(conceptunit_shop(clean_str(), pledge=True), casa_way())
    sue_dakota_hubunit.save_plan_bud(yao_old_plan)

    yao_new_plan = create_listen_basis(yao_duty)
    assert yao_new_plan.concept_exists(run_way()) is False
    assert yao_new_plan.concept_exists(clean_way()) is False

    # WHEN
    listen_to_agendas_duty_plan(yao_new_plan, sue_dakota_hubunit)

    # THEN
    assert yao_new_plan.concept_exists(clean_way()) is False
    assert yao_new_plan.concept_exists(run_way())
