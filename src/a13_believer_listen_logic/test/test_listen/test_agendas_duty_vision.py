from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer import believerunit_shop
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.keep_tool import save_duty_believer
from src.a13_believer_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_duty_vision,
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
from src.a13_believer_listen_logic.test._util.example_listen_hub import (
    get_dakota_hubunit,
    get_dakota_rope,
)


def test_listen_to_agenda_duty_vision_agenda_AddsChoresTovision_BelieverWhenNo_laborlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    yao_duty = believerunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_person_cred_points = 47
    zia_person_debt_points = 41
    zia_pool = 87
    yao_duty.add_personunit(zia_str, zia_person_cred_points, zia_person_debt_points)
    yao_duty.set_person_respect(zia_pool)

    zia_vision = believerunit_shop(zia_str, a23_str)
    zia_vision.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_vision.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_vision.add_personunit(yao_str, person_debt_points=12)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_rope())
    yao_dakota_hubunit.save_vision_believer(zia_vision)
    new_yao_vision = create_listen_basis(yao_duty)
    assert len(new_yao_vision.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_vision.get_plan_dict())=}")
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_AddsChoresTovision_Believer(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    yao_duty = believerunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_person_cred_points = 47
    zia_person_debt_points = 41
    zia_pool = 87
    yao_duty.add_personunit(zia_str, zia_person_cred_points, zia_person_debt_points)
    yao_duty.set_person_respect(zia_pool)

    zia_vision = believerunit_shop(zia_str, a23_str)
    zia_vision.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_vision.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_vision.add_personunit(yao_str, person_debt_points=12)
    clean_planunit = zia_vision.get_plan_obj(clean_rope())
    cook_planunit = zia_vision.get_plan_obj(cook_rope())
    clean_planunit.laborunit.set_laborlink(yao_str)
    cook_planunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_rope())
    yao_dakota_hubunit.save_vision_believer(zia_vision)

    # zia_file_path = create_path(visions_path, zia_str}.json")
    # print(f"{os_path_exists(zia_file_path)=}")
    new_yao_vision = create_listen_basis(yao_duty)
    assert len(new_yao_vision.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_vision.get_plan_dict())=}")
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_AddsChoresTovisionBelieverWithDetailsDecidedBy_person_debt_points(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    zia_vision = get_example_zia_speaker()
    bob_vision = get_example_bob_speaker()
    bob_vision.edit_plan_attr(
        cook_rope(),
        reason_del_premise_rcontext=eat_rope(),
        reason_del_premise_pstate=hungry_rope(),
    )
    bob_cook_planunit = bob_vision.get_plan_obj(cook_rope())
    zia_cook_planunit = zia_vision.get_plan_obj(cook_rope())
    assert bob_cook_planunit != zia_cook_planunit
    assert len(zia_cook_planunit.reasonunits) == 1
    assert len(bob_cook_planunit.reasonunits) == 0
    zia_str = zia_vision.believer_name
    bob_str = bob_vision.believer_name
    sue_dakota_hubunit = get_dakota_hubunit()
    sue_dakota_hubunit.save_vision_believer(zia_vision)
    sue_dakota_hubunit.save_vision_believer(bob_vision)

    yao_duty = get_example_yao_speaker()
    save_duty_believer(
        belief_mstr_dir=sue_dakota_hubunit.belief_mstr_dir,
        believer_name=sue_dakota_hubunit.believer_name,
        belief_label=sue_dakota_hubunit.belief_label,
        keep_rope=sue_dakota_hubunit.keep_rope,
        knot=None,
        duty_believer=yao_duty,
    )
    new_yao_job1 = create_listen_basis(yao_duty)
    assert new_yao_job1.plan_exists(cook_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(new_yao_job1, sue_dakota_hubunit)

    # THEN
    assert new_yao_job1.plan_exists(cook_rope())
    new_cook_plan = new_yao_job1.get_plan_obj(cook_rope())
    zia_personunit = new_yao_job1.get_person(zia_str)
    bob_personunit = new_yao_job1.get_person(bob_str)
    assert zia_personunit.person_debt_points < bob_personunit.person_debt_points
    assert new_cook_plan.get_reasonunit(eat_rope()) is None

    yao_zia_person_debt_points = 15
    yao_bob_person_debt_points = 5
    yao_duty.add_personunit(zia_str, None, yao_zia_person_debt_points)
    yao_duty.add_personunit(bob_str, None, yao_bob_person_debt_points)
    yao_duty.set_person_respect(100)
    new_yao_job2 = create_listen_basis(yao_duty)
    assert new_yao_job2.plan_exists(cook_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(new_yao_job2, sue_dakota_hubunit)

    # THEN
    assert new_yao_job2.plan_exists(cook_rope())
    new_cook_plan = new_yao_job2.get_plan_obj(cook_rope())
    zia_personunit = new_yao_job2.get_person(zia_str)
    bob_personunit = new_yao_job2.get_person(bob_str)
    assert zia_personunit.person_debt_points > bob_personunit.person_debt_points
    zia_eat_reasonunit = zia_cook_planunit.get_reasonunit(eat_rope())
    assert new_cook_plan.get_reasonunit(eat_rope()) == zia_eat_reasonunit


def test_listen_to_agenda_duty_vision_agenda_ProcessesIrrationalBeliever(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    yao_duty = believerunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_person_cred_points = 47
    zia_person_debt_points = 41
    sue_str = "Sue"
    sue_person_cred_points = 57
    sue_person_debt_points = 51
    yao_duty.add_personunit(zia_str, zia_person_cred_points, zia_person_debt_points)
    yao_duty.add_personunit(sue_str, sue_person_cred_points, sue_person_debt_points)
    yao_pool = 92
    yao_duty.set_person_respect(yao_pool)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_rope())
    save_duty_believer(
        belief_mstr_dir=yao_dakota_hubunit.belief_mstr_dir,
        believer_name=yao_dakota_hubunit.believer_name,
        belief_label=yao_dakota_hubunit.belief_label,
        keep_rope=yao_dakota_hubunit.keep_rope,
        knot=None,
        duty_believer=yao_duty,
    )

    zia_str = "Zia"
    zia_vision = believerunit_shop(zia_str, a23_str)
    zia_vision.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_vision.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_vision.add_personunit(yao_str, person_debt_points=12)
    clean_planunit = zia_vision.get_plan_obj(clean_rope())
    cook_planunit = zia_vision.get_plan_obj(cook_rope())
    clean_planunit.laborunit.set_laborlink(yao_str)
    cook_planunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_vision_believer(zia_vision)

    sue_vision = believerunit_shop(sue_str)
    sue_vision.set_max_tree_traverse(5)
    zia_vision.add_personunit(yao_str, person_debt_points=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_vision.make_l1_rope(vacuum_str)
    sue_vision.set_l1_plan(planunit_shop(vacuum_str, task=True))
    vacuum_planunit = sue_vision.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_rope = sue_vision.make_l1_rope(egg_str)
    sue_vision.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_vision.make_l1_rope(chicken_str)
    sue_vision.set_l1_plan(planunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_vision.edit_plan_attr(
        egg_rope,
        task=True,
        reason_rcontext=chicken_rope,
        reason_rplan_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_vision.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_rcontext=egg_rope,
        reason_rplan_active_requisite=False,
    )
    yao_dakota_hubunit.save_vision_believer(sue_vision)

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN irrational believer is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2
    zia_personunit = new_yao_vision.get_person(zia_str)
    sue_personunit = new_yao_vision.get_person(sue_str)
    print(f"{sue_personunit.person_debt_points=}")
    print(f"{sue_personunit._irrational_person_debt_points=}")
    assert zia_personunit._irrational_person_debt_points == 0
    assert sue_personunit._irrational_person_debt_points == 51


def test_listen_to_agenda_duty_vision_agenda_ProcessesMissingDebtorvisionBeliever(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    yao_duty = believerunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_person_cred_points = 47
    sue_person_cred_points = 57
    zia_person_debt_points = 41
    sue_person_debt_points = 51
    yao_duty.add_personunit(zia_str, zia_person_cred_points, zia_person_debt_points)
    yao_duty.add_personunit(sue_str, sue_person_cred_points, sue_person_debt_points)
    yao_pool = 92
    yao_duty.set_person_respect(yao_pool)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_rope())
    save_duty_believer(
        belief_mstr_dir=yao_dakota_hubunit.belief_mstr_dir,
        believer_name=yao_dakota_hubunit.believer_name,
        belief_label=yao_dakota_hubunit.belief_label,
        keep_rope=yao_dakota_hubunit.keep_rope,
        knot=None,
        duty_believer=yao_duty,
    )

    zia_vision = believerunit_shop(zia_str, a23_str)
    zia_vision.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_vision.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_vision.add_personunit(yao_str, person_debt_points=12)
    clean_planunit = zia_vision.get_plan_obj(clean_rope())
    cook_planunit = zia_vision.get_plan_obj(cook_rope())
    clean_planunit.laborunit.set_laborlink(yao_str)
    cook_planunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_rope())
    yao_dakota_hubunit.save_vision_believer(zia_vision)

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN irrational believer is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2
    zia_personunit = new_yao_vision.get_person(zia_str)
    sue_personunit = new_yao_vision.get_person(sue_str)
    print(f"{sue_personunit.person_debt_points=}")
    print(f"{sue_personunit._inallocable_person_debt_points=}")
    assert zia_personunit._inallocable_person_debt_points == 0
    assert sue_personunit._inallocable_person_debt_points == 51


def test_listen_to_agenda_duty_vision_agenda_ListensToBeliever_duty_AndNotBeliever_vision(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    yao_str = "Yao"
    yao_duty = believerunit_shop(yao_str, a23_str)
    yao_str = "Yao"
    yao_person_cred_points = 57
    yao_person_debt_points = 51
    yao_duty.add_personunit(yao_str, yao_person_cred_points, yao_person_debt_points)
    zia_str = "Zia"
    zia_person_cred_points = 47
    zia_person_debt_points = 41
    yao_duty.add_personunit(zia_str, zia_person_cred_points, zia_person_debt_points)
    yao_pool = 87
    yao_duty.set_person_respect(yao_pool)
    # save yao without chore to dutys
    yao_dakota_hubunit = hubunit_shop(env_dir(), a23_str, yao_str, get_dakota_rope())
    save_duty_believer(
        belief_mstr_dir=yao_dakota_hubunit.belief_mstr_dir,
        believer_name=yao_dakota_hubunit.believer_name,
        belief_label=yao_dakota_hubunit.belief_label,
        keep_rope=yao_dakota_hubunit.keep_rope,
        knot=None,
        duty_believer=yao_duty,
    )

    # Save Zia to visions
    zia_str = "Zia"
    zia_vision = believerunit_shop(zia_str, a23_str)
    zia_vision.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_vision.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_vision.add_personunit(yao_str, person_debt_points=12)
    clean_planunit = zia_vision.get_plan_obj(clean_rope())
    cook_planunit = zia_vision.get_plan_obj(cook_rope())
    clean_planunit.laborunit.set_laborlink(yao_str)
    cook_planunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_vision_believer(zia_vision)

    # save yao with chore to visions
    yao_old_vision = believerunit_shop(yao_str, a23_str)
    vacuum_str = "vacuum"
    vacuum_rope = yao_old_vision.make_l1_rope(vacuum_str)
    yao_old_vision.set_l1_plan(planunit_shop(vacuum_str, task=True))
    vacuum_planunit = yao_old_vision.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.set_laborlink(yao_str)
    yao_dakota_hubunit.save_vision_believer(yao_old_vision)

    # WHEN
    new_yao_vision = create_listen_basis(yao_duty)
    listen_to_agendas_duty_vision(new_yao_vision, yao_dakota_hubunit)

    # THEN irrational believer is ignored
    assert len(new_yao_vision.get_agenda_dict()) != 3
    assert len(new_yao_vision.get_agenda_dict()) == 2


def test_listen_to_agenda_duty_vision_agenda_GetsAgendaFromSrcBelieverNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao_duty has chore run_rope
    # yao_vision has chore clean_rope
    # yao_new_vision fstates yao_duty chore run_rope and not clean_rope
    yao_duty = get_example_yao_speaker()
    assert yao_duty.plan_exists(run_rope()) is False
    assert yao_duty.plan_exists(clean_rope()) is False
    yao_duty.set_plan(planunit_shop(run_str(), task=True), casa_rope())
    sue_dakota_hubunit = get_dakota_hubunit()
    save_duty_believer(
        belief_mstr_dir=sue_dakota_hubunit.belief_mstr_dir,
        believer_name=sue_dakota_hubunit.believer_name,
        belief_label=sue_dakota_hubunit.belief_label,
        keep_rope=sue_dakota_hubunit.keep_rope,
        knot=None,
        duty_believer=yao_duty,
    )
    yao_old_vision = get_example_yao_speaker()
    assert yao_old_vision.plan_exists(run_rope()) is False
    assert yao_old_vision.plan_exists(clean_rope()) is False
    yao_old_vision.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    sue_dakota_hubunit.save_vision_believer(yao_old_vision)

    yao_new_vision = create_listen_basis(yao_duty)
    assert yao_new_vision.plan_exists(run_rope()) is False
    assert yao_new_vision.plan_exists(clean_rope()) is False

    # WHEN
    listen_to_agendas_duty_vision(yao_new_vision, sue_dakota_hubunit)

    # THEN
    assert yao_new_vision.plan_exists(clean_rope()) is False
    assert yao_new_vision.plan_exists(run_rope())
