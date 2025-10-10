from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import delete_dir
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch12_pack_file._ref.ch12_path import create_gut_path
from src.ch12_pack_file.packfilehandler import packfilehandler_shop, save_gut_file
from src.ch13_belief_listen_logic.listen_main import (
    create_listen_basis,
    listen_to_agendas_create_init_job_from_guts,
)
from src.ch13_belief_listen_logic.test._util.ch13_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as env_dir,
)
from src.ch13_belief_listen_logic.test._util.ch13_examples import (
    a23_casa_rope,
    a23_clean_rope,
    a23_cook_rope,
    a23_eat_rope,
    a23_hungry_rope,
    clean_str,
    cook_str,
    get_example_bob_speaker,
    get_example_yao_speaker,
    get_example_zia_speaker,
)


def test_listen_to_agendas_create_init_job_from_guts_AddstasksToBeliefWhenNo_partyunitIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = beliefunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    zia_pool = 87
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_gut.set_voice_respect(zia_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.set_plan(planunit_shop(clean_str(), pledge=True), a23_casa_rope())
    zia_gut.set_plan(planunit_shop(cook_str(), pledge=True), a23_casa_rope())
    zia_gut.add_voiceunit(yao_str, voice_debt_lumen=12)
    save_gut_file(moment_mstr_dir, zia_gut)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_plan_dict())=}")
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_create_init_job_from_guts_AddstasksToBelief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = beliefunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    zia_pool = 87
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_gut.set_voice_respect(zia_pool)
    a23_str = "amy23"
    save_gut_file(moment_mstr_dir, yao_gut)
    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.set_plan(planunit_shop(clean_str(), pledge=True), a23_casa_rope())
    zia_gut.set_plan(planunit_shop(cook_str(), pledge=True), a23_casa_rope())
    zia_gut.add_voiceunit(yao_str, voice_debt_lumen=12)
    clean_planunit = zia_gut.get_plan_obj(a23_clean_rope())
    cook_planunit = zia_gut.get_plan_obj(a23_cook_rope())
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


def test_listen_to_agendas_create_init_job_from_guts_AddstasksToBeliefWithDetailsDecidedBy_voice_debt_lumen(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = env_dir()
    zia_gut = get_example_zia_speaker()
    bob_gut = get_example_bob_speaker()
    bob_gut.edit_plan_attr(
        a23_cook_rope(),
        reason_del_case_reason_context=a23_eat_rope(),
        reason_del_case_reason_state=a23_hungry_rope(),
    )
    bob_cook_planunit = bob_gut.get_plan_obj(a23_cook_rope())
    zia_cook_planunit = zia_gut.get_plan_obj(a23_cook_rope())
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
    assert new_yao_gut1.plan_exists(a23_cook_rope()) is False

    # WHEN
    yao_packfilehandler = packfilehandler_shop(moment_mstr_dir, a23_str, yao_str)
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_gut1)

    # THEN
    assert new_yao_gut1.plan_exists(a23_cook_rope())
    new_cook_plan = new_yao_gut1.get_plan_obj(a23_cook_rope())
    zia_voiceunit = new_yao_gut1.get_voice(zia_str)
    bob_voiceunit = new_yao_gut1.get_voice(bob_str)
    assert zia_voiceunit.voice_debt_lumen < bob_voiceunit.voice_debt_lumen
    assert new_cook_plan.get_reasonunit(a23_eat_rope()) is None

    yao_zia_voice_debt_lumen = 15
    yao_bob_voice_debt_lumen = 5
    yao_gut.add_voiceunit(zia_str, None, yao_zia_voice_debt_lumen)
    yao_gut.add_voiceunit(bob_str, None, yao_bob_voice_debt_lumen)
    yao_gut.set_voice_respect(100)
    new_yao_gut2 = create_listen_basis(yao_gut)
    assert new_yao_gut2.plan_exists(a23_cook_rope()) is False

    # WHEN
    listen_to_agendas_create_init_job_from_guts(moment_mstr_dir, new_yao_gut2)

    # THEN
    assert new_yao_gut2.plan_exists(a23_cook_rope())
    new_cook_plan = new_yao_gut2.get_plan_obj(a23_cook_rope())
    zia_voiceunit = new_yao_gut2.get_voice(zia_str)
    bob_voiceunit = new_yao_gut2.get_voice(bob_str)
    assert zia_voiceunit.voice_debt_lumen > bob_voiceunit.voice_debt_lumen
    zia_eat_reasonunit = zia_cook_planunit.get_reasonunit(a23_eat_rope())
    assert new_cook_plan.get_reasonunit(a23_eat_rope()) == zia_eat_reasonunit


def test_listen_to_agendas_create_init_job_from_guts_ProcessesIrrationalBelief(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-duplicate-method
    # ESTABLISH
    moment_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = beliefunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_voice_cred_lumen = 47
    zia_voice_debt_lumen = 41
    sue_str = "Sue"
    sue_voice_cred_lumen = 57
    sue_voice_debt_lumen = 51
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_gut.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_pool = 92
    yao_gut.set_voice_respect(yao_pool)
    a23_str = "amy23"
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_str = "Zia"
    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.set_plan(planunit_shop(clean_str(), pledge=True), a23_casa_rope())
    zia_gut.set_plan(planunit_shop(cook_str(), pledge=True), a23_casa_rope())
    zia_gut.add_voiceunit(yao_str, voice_debt_lumen=12)
    clean_planunit = zia_gut.get_plan_obj(a23_clean_rope())
    cook_planunit = zia_gut.get_plan_obj(a23_cook_rope())
    clean_planunit.laborunit.add_party(yao_str)
    cook_planunit.laborunit.add_party(yao_str)
    save_gut_file(moment_mstr_dir, zia_gut)

    sue_gut = beliefunit_shop(sue_str, a23_str)
    sue_gut.set_max_tree_traverse(5)
    zia_gut.add_voiceunit(yao_str, voice_debt_lumen=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_gut.make_l1_rope(vacuum_str)
    sue_gut.set_l1_plan(planunit_shop(vacuum_str, pledge=True))
    vacuum_planunit = sue_gut.get_plan_obj(vacuum_rope)
    vacuum_planunit.laborunit.add_party(yao_str)

    egg_str = "egg first"
    egg_rope = sue_gut.make_l1_rope(egg_str)
    sue_gut.set_l1_plan(planunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_gut.make_l1_rope(chicken_str)
    sue_gut.set_l1_plan(planunit_shop(chicken_str))
    # set egg pledge is True when chicken first is False
    sue_gut.edit_plan_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_plan_active_requisite=True,
    )
    # set chick pledge is True when egg first is False
    sue_gut.edit_plan_attr(
        chicken_rope,
        pledge=True,
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
    print(f"{sue_voiceunit.voice_debt_lumen=}")
    print(f"{sue_voiceunit.irrational_voice_debt_lumen=}")
    assert zia_voiceunit.irrational_voice_debt_lumen == 0
    assert sue_voiceunit.irrational_voice_debt_lumen == 51


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
    zia_voice_cred_lumen = 47
    sue_voice_cred_lumen = 57
    zia_voice_debt_lumen = 41
    sue_voice_debt_lumen = 51
    yao_gut.add_voiceunit(zia_str, zia_voice_cred_lumen, zia_voice_debt_lumen)
    yao_gut.add_voiceunit(sue_str, sue_voice_cred_lumen, sue_voice_debt_lumen)
    yao_pool = 92
    yao_gut.set_voice_respect(yao_pool)
    save_gut_file(moment_mstr_dir, yao_gut)

    zia_gut = beliefunit_shop(zia_str, a23_str)
    zia_gut.set_plan(planunit_shop(clean_str(), pledge=True), a23_casa_rope())
    zia_gut.set_plan(planunit_shop(cook_str(), pledge=True), a23_casa_rope())
    zia_gut.add_voiceunit(yao_str, voice_debt_lumen=12)
    clean_planunit = zia_gut.get_plan_obj(a23_clean_rope())
    cook_planunit = zia_gut.get_plan_obj(a23_cook_rope())
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
    print(f"{sue_voiceunit.voice_debt_lumen=}")
    print(f"{sue_voiceunit.inallocable_voice_debt_lumen=}")
    assert zia_voiceunit.inallocable_voice_debt_lumen == 0
    assert sue_voiceunit.inallocable_voice_debt_lumen == 51
