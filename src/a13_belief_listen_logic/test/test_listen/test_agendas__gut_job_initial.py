from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import delete_dir, save_file
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a12_hub_toolbox.a12_path import create_gut_path
from src.a12_hub_toolbox.hub_tool import save_gut_file
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a13_belief_listen_logic.listen_main import (
    create_listen_basis,
    listen_to_agendas_create_init_job_from_guts,
)
from src.a13_belief_listen_logic.test._util.a13_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a13_belief_listen_logic.test._util.example_listen import (
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


def test_listen_to_agendas_create_init_job_from_guts_AddsChoresToBeliefWhenNo_partyunitIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = beliefunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    zia_pool = 87
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    yao_gut.set_voice_respect(zia_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_gut.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_gut.add_voiceunit(yao_str, voice_debt_points=12)
    save_gut_file(moment_mstr_dir, zia_gut)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_plan_dict())=}")
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_create_init_job_from_guts_AddsChoresToBelief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = beliefunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    zia_pool = 87
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    yao_gut.set_voice_respect(zia_pool)
    a23_str = "amy23"
    save_gut_file(moment_mstr_dir, yao_gut)
    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_gut.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_gut.add_voiceunit(yao_str, voice_debt_points=12)
    clean_planunit = zia_gut.get_plan_obj(clean_rope())
    cook_planunit = zia_gut.get_plan_obj(cook_rope())
    clean_planunit.laborunit.add_party(yao_str)
    cook_planunit.laborunit.add_party(yao_str)
    save_gut_file(moment_mstr_dir, zia_gut)
    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_plan_dict())=}")
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_create_init_job_from_guts_AddsChoresToBeliefWithDetailsDecidedBy_voice_debt_points(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    zia_gut = get_example_zia_speaker()
    bob_gut = get_example_bob_speaker()
    bob_gut.edit_plan_attr(
        cook_rope(),
        reason_del_case_reason_context=eat_rope(),
        reason_del_case_reason_state=hungry_rope(),
    )
    bob_cook_planunit = bob_gut.get_plan_obj(cook_rope())
    zia_cook_planunit = zia_gut.get_plan_obj(cook_rope())
    assert bob_cook_planunit != zia_cook_planunit
    assert len(zia_cook_planunit.reasonunits) == 1
    assert len(bob_cook_planunit.reasonunits) == 0
    zia_str = zia_gut.belief_name
    bob_str = bob_gut.belief_name
    a23_str = "amy23"
    save_gut_file(moment_mstr_dir, zia_gut)
    save_gut_file(moment_mstr_dir, bob_gut)

    yao_gut = get_example_yao_speaker()
    yao_str = yao_gut.belief_name
    save_gut_file(moment_mstr_dir, yao_gut)

    new_yao_gut1 = create_listen_basis(yao_gut)
    assert new_yao_gut1.plan_exists(cook_rope()) is False

    # WHEN
    yao_hubunit = hubunit_shop(moment_mstr_dir, a23_str, yao_str)
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_gut1)

    # THEN
    assert new_yao_gut1.plan_exists(cook_rope())
    new_cook_plan = new_yao_gut1.get_plan_obj(cook_rope())
    zia_voiceunit = new_yao_gut1.get_voice(zia_str)
    bob_voiceunit = new_yao_gut1.get_voice(bob_str)
    assert zia_voiceunit.voice_debt_points < bob_voiceunit.voice_debt_points
    assert new_cook_plan.get_reasonunit(eat_rope()) is None

    yao_zia_voice_debt_points = 15
    yao_bob_voice_debt_points = 5
    yao_gut.add_voiceunit(zia_str, None, yao_zia_voice_debt_points)
    yao_gut.add_voiceunit(bob_str, None, yao_bob_voice_debt_points)
    yao_gut.set_voice_respect(100)
    new_yao_gut2 = create_listen_basis(yao_gut)
    assert new_yao_gut2.plan_exists(cook_rope()) is False

    # WHEN
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_gut2)

    # THEN
    assert new_yao_gut2.plan_exists(cook_rope())
    new_cook_plan = new_yao_gut2.get_plan_obj(cook_rope())
    zia_voiceunit = new_yao_gut2.get_voice(zia_str)
    bob_voiceunit = new_yao_gut2.get_voice(bob_str)
    assert zia_voiceunit.voice_debt_points > bob_voiceunit.voice_debt_points
    zia_eat_reasonunit = zia_cook_planunit.get_reasonunit(eat_rope())
    assert new_cook_plan.get_reasonunit(eat_rope()) == zia_eat_reasonunit


def test_listen_to_agendas_create_init_job_from_guts_ProcessesIrrationalBelief(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-duplicate-method
    # ESTABLISH
    moment_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = beliefunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    sue_str = "Sue"
    sue_voice_cred_points = 57
    sue_voice_debt_points = 51
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    yao_gut.add_voiceunit(sue_str, sue_voice_cred_points, sue_voice_debt_points)
    yao_pool = 92
    yao_gut.set_voice_respect(yao_pool)
    a23_str = "amy23"
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_str = "Zia"
    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_gut.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_gut.add_voiceunit(yao_str, voice_debt_points=12)
    clean_planunit = zia_gut.get_plan_obj(clean_rope())
    cook_planunit = zia_gut.get_plan_obj(cook_rope())
    clean_planunit.laborunit.add_party(yao_str)
    cook_planunit.laborunit.add_party(yao_str)
    save_gut_file(moment_mstr_dir, zia_gut)

    sue_gut = beliefunit_shop(sue_str, a23_str)
    sue_gut.set_max_tree_traverse(5)
    zia_gut.add_voiceunit(yao_str, voice_debt_points=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_gut.make_l1_rope(vacuum_str)
    sue_gut.set_l1_plan(planunit_shop(vacuum_str, task=True))
    vacuum_planunit = sue_gut.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.add_party(yao_str)

    egg_str = "egg first"
    egg_rope = sue_gut.make_l1_rope(egg_str)
    sue_gut.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_gut.make_l1_rope(chicken_str)
    sue_gut.set_l1_plan(planunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_gut.edit_plan_attr(
        egg_rope,
        task=True,
        reason_context=chicken_rope,
        reason_plan_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_gut.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_context=egg_rope,
        reason_plan_active_requisite=False,
    )
    save_gut_file(moment_mstr_dir, sue_gut)

    # WHEN
    new_yao_gut = create_listen_basis(yao_gut)
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_gut)

    # THEN irrational belief is ignored
    assert len(new_yao_gut.get_agenda_dict()) != 3
    assert len(new_yao_gut.get_agenda_dict()) == 2
    zia_voiceunit = new_yao_gut.get_voice(zia_str)
    sue_voiceunit = new_yao_gut.get_voice(sue_str)
    print(f"{sue_voiceunit.voice_debt_points=}")
    print(f"{sue_voiceunit._irrational_voice_debt_points=}")
    assert zia_voiceunit._irrational_voice_debt_points == 0
    assert sue_voiceunit._irrational_voice_debt_points == 51


def test_listen_to_agendas_create_init_job_from_guts_ProcessesMissingDebtorBelief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    yao_str = "Yao"
    a23_str = "amy23"
    yao_gut_path = create_gut_path(moment_mstr_dir, a23_str, yao_str)
    delete_dir(yao_gut_path)  # don't know why I have to do this...
    print(f"{os_path_exists(yao_gut_path)=}")
    yao_gut = beliefunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_voice_cred_points = 47
    sue_voice_cred_points = 57
    zia_voice_debt_points = 41
    sue_voice_debt_points = 51
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    yao_gut.add_voiceunit(sue_str, sue_voice_cred_points, sue_voice_debt_points)
    yao_pool = 92
    yao_gut.set_voice_respect(yao_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.set_plan(planunit_shop(clean_str(), task=True), casa_rope())
    zia_gut.set_plan(planunit_shop(cook_str(), task=True), casa_rope())
    zia_gut.add_voiceunit(yao_str, voice_debt_points=12)
    clean_planunit = zia_gut.get_plan_obj(clean_rope())
    cook_planunit = zia_gut.get_plan_obj(cook_rope())
    clean_planunit.laborunit.add_party(yao_str)
    cook_planunit.laborunit.add_party(yao_str)
    save_gut_file(moment_mstr_dir, zia_gut)

    # WHEN
    new_yao_gut = create_listen_basis(yao_gut)
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_gut)

    # THEN irrational belief is ignored
    assert len(new_yao_gut.get_agenda_dict()) != 3
    assert len(new_yao_gut.get_agenda_dict()) == 2
    zia_voiceunit = new_yao_gut.get_voice(zia_str)
    sue_voiceunit = new_yao_gut.get_voice(sue_str)
    print(f"{sue_voiceunit.voice_debt_points=}")
    print(f"{sue_voiceunit._inallocable_voice_debt_points=}")
    assert zia_voiceunit._inallocable_voice_debt_points == 0
    assert sue_voiceunit._inallocable_voice_debt_points == 51
