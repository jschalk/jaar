from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_plan_listen_logic._test_util.a13_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a13_plan_listen_logic._test_util.example_listen import (
    casa_way,
    clean_str,
    clean_way,
    cook_str,
    cook_way,
    eat_way,
    full_way,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
    hungry_way,
    run_str,
    run_way,
)
from src.a13_plan_listen_logic._test_util.example_listen_hub import (
    get_dakota_hubunit,
    get_dakota_way,
)
from src.a13_plan_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_duty_vision,
)


def test_listen_to_agenda_duty_vision_agenda_AddsChoresTovision_PlanWhenNo_laborlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.set_acct_respect(zia_pool)

    zia_vision = planunit_shop(zia_str, a23_str)
    zia_vision.set_concept(conceptunit_shop(clean_str(), task=True), casa_way())
    zia_vision.set_concept(conceptunit_shop(cook_str(), task=True), casa_way())
    zia_vision.add_acctunit(yao_str, debtit_belief=12)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_vision_plan(zia_vision)
    new_yao_vision = create_listen_basis(yao_duty)
    assert len(new_yao_vision.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_vision.get_concept_dict())=}")
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_AddsChoresTovision_Plan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    zia_pool = 87
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.set_acct_respect(zia_pool)

    zia_vision = planunit_shop(zia_str, a23_str)
    zia_vision.set_concept(conceptunit_shop(clean_str(), task=True), casa_way())
    zia_vision.set_concept(conceptunit_shop(cook_str(), task=True), casa_way())
    zia_vision.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_vision.get_concept_obj(clean_way())
    cook_conceptunit = zia_vision.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_vision_plan(zia_vision)

    # zia_file_path = create_path(visions_dir, zia_str}.json")
    # print(f"{os_path_exists(zia_file_path)=}")
    new_yao_vision = create_listen_basis(yao_duty)
    assert len(new_yao_vision.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_vision.get_concept_dict())=}")
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_AddsChoresTovisionPlanWithDetailsDecidedBy_debtit_belief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    zia_vision = get_example_zia_speaker()
    bob_vision = get_example_bob_speaker()
    bob_vision.edit_concept_attr(
        cook_way(),
        reason_del_premise_rcontext=eat_way(),
        reason_del_premise_pstate=hungry_way(),
    )
    bob_cook_conceptunit = bob_vision.get_concept_obj(cook_way())
    zia_cook_conceptunit = zia_vision.get_concept_obj(cook_way())
    assert bob_cook_conceptunit != zia_cook_conceptunit
    assert len(zia_cook_conceptunit.reasonunits) == 1
    assert len(bob_cook_conceptunit.reasonunits) == 0
    zia_str = zia_vision.owner_name
    bob_str = bob_vision.owner_name
    sue_dakota_hubunit = get_dakota_hubunit()
    sue_dakota_hubunit.save_vision_plan(zia_vision)
    sue_dakota_hubunit.save_vision_plan(bob_vision)

    yao_duty = get_example_yao_speaker()
    sue_dakota_hubunit.save_duty_plan(yao_duty)
    new_yao_job1 = create_listen_basis(yao_duty)
    assert new_yao_job1.concept_exists(cook_way()) is False

    # WHEN
    listen_to_agendas_duty_vision(new_yao_job1, sue_dakota_hubunit)

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
    listen_to_agendas_duty_vision(new_yao_job2, sue_dakota_hubunit)

    # THEN
    assert new_yao_job2.concept_exists(cook_way())
    new_cook_concept = new_yao_job2.get_concept_obj(cook_way())
    zia_acctunit = new_yao_job2.get_acct(zia_str)
    bob_acctunit = new_yao_job2.get_acct(bob_str)
    assert zia_acctunit.debtit_belief > bob_acctunit.debtit_belief
    zia_eat_reasonunit = zia_cook_conceptunit.get_reasonunit(eat_way())
    assert new_cook_concept.get_reasonunit(eat_way()) == zia_eat_reasonunit


def test_listen_to_agenda_duty_vision_agenda_ProcessesIrrationalPlan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str, a23_str)
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
    yao_dakota_hubunit.save_duty_plan(yao_duty)

    zia_str = "Zia"
    zia_vision = planunit_shop(zia_str, a23_str)
    zia_vision.set_concept(conceptunit_shop(clean_str(), task=True), casa_way())
    zia_vision.set_concept(conceptunit_shop(cook_str(), task=True), casa_way())
    zia_vision.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_vision.get_concept_obj(clean_way())
    cook_conceptunit = zia_vision.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_vision_plan(zia_vision)

    sue_vision = planunit_shop(sue_str)
    sue_vision.set_max_tree_traverse(5)
    zia_vision.add_acctunit(yao_str, debtit_belief=12)
    vacuum_str = "vacuum"
    vacuum_way = sue_vision.make_l1_way(vacuum_str)
    sue_vision.set_l1_concept(conceptunit_shop(vacuum_str, task=True))
    vacuum_conceptunit = sue_vision.get_concept_obj(vacuum_way)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_way = sue_vision.make_l1_way(egg_str)
    sue_vision.set_l1_concept(conceptunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_way = sue_vision.make_l1_way(chicken_str)
    sue_vision.set_l1_concept(conceptunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_vision.edit_concept_attr(
        egg_way,
        task=True,
        reason_rcontext=chicken_way,
        reason_rconcept_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_vision.edit_concept_attr(
        chicken_way,
        task=True,
        reason_rcontext=egg_way,
        reason_rconcept_active_requisite=False,
    )
    yao_dakota_hubunit.save_vision_plan(sue_vision)

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN irrational plan is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2
    zia_acctunit = new_yao_vision.get_acct(zia_str)
    sue_acctunit = new_yao_vision.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._irrational_debtit_belief=}")
    assert zia_acctunit._irrational_debtit_belief == 0
    assert sue_acctunit._irrational_debtit_belief == 51


def test_listen_to_agenda_duty_vision_agenda_ProcessesMissingDebtorvisionPlan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str, a23_str)
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
    yao_dakota_hubunit.save_duty_plan(yao_duty)

    zia_vision = planunit_shop(zia_str, a23_str)
    zia_vision.set_concept(conceptunit_shop(clean_str(), task=True), casa_way())
    zia_vision.set_concept(conceptunit_shop(cook_str(), task=True), casa_way())
    zia_vision.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_vision.get_concept_obj(clean_way())
    cook_conceptunit = zia_vision.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_vision_plan(zia_vision)

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN irrational plan is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2
    zia_acctunit = new_yao_vision.get_acct(zia_str)
    sue_acctunit = new_yao_vision.get_acct(sue_str)
    print(f"{sue_acctunit.debtit_belief=}")
    print(f"{sue_acctunit._inallocable_debtit_belief=}")
    assert zia_acctunit._inallocable_debtit_belief == 0
    assert sue_acctunit._inallocable_debtit_belief == 51


def test_listen_to_agenda_duty_vision_agenda_ListensToOwner_duty_AndNotOwner_vision(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str, a23_str)
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
    # save yao without chore to dutys
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_way())
    yao_dakota_hubunit.save_duty_plan(yao_duty)

    # Save Zia to visions
    zia_str = "Zia"
    zia_vision = planunit_shop(zia_str, a23_str)
    zia_vision.set_concept(conceptunit_shop(clean_str(), task=True), casa_way())
    zia_vision.set_concept(conceptunit_shop(cook_str(), task=True), casa_way())
    zia_vision.add_acctunit(yao_str, debtit_belief=12)
    clean_conceptunit = zia_vision.get_concept_obj(clean_way())
    cook_conceptunit = zia_vision.get_concept_obj(cook_way())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_vision_plan(zia_vision)

    # save yao with chore to visions
    yao_old_vision = planunit_shop(yao_str, a23_str)
    vacuum_str = "vacuum"
    vacuum_way = yao_old_vision.make_l1_way(vacuum_str)
    yao_old_vision.set_l1_concept(conceptunit_shop(vacuum_str, task=True))
    vacuum_conceptunit = yao_old_vision.get_concept_obj(vacuum_way)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_vision_plan(yao_old_vision)

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN irrational plan is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_GetsAgendaFromSrcPlanNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has chore run_way
    # yao_vision has chore clean_way
    # yao_new_vision fstates yao_duty chore run_way and not clean_way
    yao_duty = get_example_yao_speaker()
    assert yao_duty.concept_exists(run_way()) is False
    assert yao_duty.concept_exists(clean_way()) is False
    yao_duty.set_concept(conceptunit_shop(run_str(), task=True), casa_way())
    sue_dakota_hubunit = get_dakota_hubunit()
    sue_dakota_hubunit.save_duty_plan(yao_duty)

    yao_old_vision = get_example_yao_speaker()
    assert yao_old_vision.concept_exists(run_way()) is False
    assert yao_old_vision.concept_exists(clean_way()) is False
    yao_old_vision.set_concept(conceptunit_shop(clean_str(), task=True), casa_way())
    sue_dakota_hubunit.save_vision_plan(yao_old_vision)

    yao_new_vision = create_listen_basis(yao_duty)
    assert yao_new_vision.concept_exists(run_way()) is False
    assert yao_new_vision.concept_exists(clean_way()) is False

    # WHEN
    listen_to_agendas_duty_vision(yao_new_vision, sue_dakota_hubunit)

    # THEN
    assert yao_new_vision.concept_exists(clean_way()) is False
    assert yao_new_vision.concept_exists(run_way())
