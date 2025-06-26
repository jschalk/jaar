from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import delete_dir, save_file
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a12_hub_toolbox.hub_path import create_gut_path
from src.a12_hub_toolbox.hub_tool import save_gut_file
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a13_plan_listen_logic.listen import (
    create_listen_basis,
    listen_to_agendas_create_init_job_from_guts,
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


def test_listen_to_agendas_create_init_job_from_guts_AddsChoresToPlanWhenNo_laborlinkIsSet(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_acct_cred_points = 47
    zia_acct_debt_points = 41
    zia_pool = 87
    yao_gut.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_gut.set_acct_respect(zia_pool)
    save_gut_file(belief_mstr_dir, yao_gut)

    zia_gut = planunit_shop(zia_str, a23_str)
    zia_gut.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_gut.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_gut.add_acctunit(yao_str, acct_debt_points=12)
    save_gut_file(belief_mstr_dir, zia_gut)

    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_concept_dict())=}")
    listen_to_agendas_create_init_job_from_guts(belief_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_create_init_job_from_guts_AddsChoresToPlan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_acct_cred_points = 47
    zia_acct_debt_points = 41
    zia_pool = 87
    yao_gut.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_gut.set_acct_respect(zia_pool)
    a23_str = "amy23"
    save_gut_file(belief_mstr_dir, yao_gut)
    zia_gut = planunit_shop(zia_str, a23_str)
    zia_gut.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_gut.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_gut.add_acctunit(yao_str, acct_debt_points=12)
    clean_conceptunit = zia_gut.get_concept_obj(clean_rope())
    cook_conceptunit = zia_gut.get_concept_obj(cook_rope())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_gut_file(belief_mstr_dir, zia_gut)
    new_yao_job = create_listen_basis(yao_gut)
    assert len(new_yao_job.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_job.get_concept_dict())=}")
    listen_to_agendas_create_init_job_from_guts(belief_mstr_dir, new_yao_job)

    # THEN
    assert len(new_yao_job.get_agenda_dict()) == 2


def test_listen_to_agendas_create_init_job_from_guts_AddsChoresToPlanWithDetailsDecidedBy_acct_debt_points(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    zia_gut = get_example_zia_speaker()
    bob_gut = get_example_bob_speaker()
    bob_gut.edit_concept_attr(
        cook_rope(),
        reason_del_premise_rcontext=eat_rope(),
        reason_del_premise_pstate=hungry_rope(),
    )
    bob_cook_conceptunit = bob_gut.get_concept_obj(cook_rope())
    zia_cook_conceptunit = zia_gut.get_concept_obj(cook_rope())
    assert bob_cook_conceptunit != zia_cook_conceptunit
    assert len(zia_cook_conceptunit.reasonunits) == 1
    assert len(bob_cook_conceptunit.reasonunits) == 0
    zia_str = zia_gut.owner_name
    bob_str = bob_gut.owner_name
    a23_str = "amy23"
    save_gut_file(belief_mstr_dir, zia_gut)
    save_gut_file(belief_mstr_dir, bob_gut)

    yao_gut = get_example_yao_speaker()
    yao_str = yao_gut.owner_name
    save_gut_file(belief_mstr_dir, yao_gut)

    new_yao_gut1 = create_listen_basis(yao_gut)
    assert new_yao_gut1.concept_exists(cook_rope()) is False

    # WHEN
    yao_hubunit = hubunit_shop(belief_mstr_dir, a23_str, yao_str)
    listen_to_agendas_create_init_job_from_guts(belief_mstr_dir, new_yao_gut1)

    # THEN
    assert new_yao_gut1.concept_exists(cook_rope())
    new_cook_concept = new_yao_gut1.get_concept_obj(cook_rope())
    zia_acctunit = new_yao_gut1.get_acct(zia_str)
    bob_acctunit = new_yao_gut1.get_acct(bob_str)
    assert zia_acctunit.acct_debt_points < bob_acctunit.acct_debt_points
    assert new_cook_concept.get_reasonunit(eat_rope()) is None

    yao_zia_acct_debt_points = 15
    yao_bob_acct_debt_points = 5
    yao_gut.add_acctunit(zia_str, None, yao_zia_acct_debt_points)
    yao_gut.add_acctunit(bob_str, None, yao_bob_acct_debt_points)
    yao_gut.set_acct_respect(100)
    new_yao_gut2 = create_listen_basis(yao_gut)
    assert new_yao_gut2.concept_exists(cook_rope()) is False

    # WHEN
    listen_to_agendas_create_init_job_from_guts(belief_mstr_dir, new_yao_gut2)

    # THEN
    assert new_yao_gut2.concept_exists(cook_rope())
    new_cook_concept = new_yao_gut2.get_concept_obj(cook_rope())
    zia_acctunit = new_yao_gut2.get_acct(zia_str)
    bob_acctunit = new_yao_gut2.get_acct(bob_str)
    assert zia_acctunit.acct_debt_points > bob_acctunit.acct_debt_points
    zia_eat_reasonunit = zia_cook_conceptunit.get_reasonunit(eat_rope())
    assert new_cook_concept.get_reasonunit(eat_rope()) == zia_eat_reasonunit


def test_listen_to_agendas_create_init_job_from_guts_ProcessesIrrationalPlan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    a23_str = "amy23"
    yao_str = "Yao"
    yao_gut = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    zia_acct_cred_points = 47
    zia_acct_debt_points = 41
    sue_str = "Sue"
    sue_acct_cred_points = 57
    sue_acct_debt_points = 51
    yao_gut.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_gut.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_pool = 92
    yao_gut.set_acct_respect(yao_pool)
    a23_str = "amy23"
    save_gut_file(belief_mstr_dir, yao_gut)

    zia_str = "Zia"
    zia_gut = planunit_shop(zia_str, a23_str)
    zia_gut.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_gut.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_gut.add_acctunit(yao_str, acct_debt_points=12)
    clean_conceptunit = zia_gut.get_concept_obj(clean_rope())
    cook_conceptunit = zia_gut.get_concept_obj(cook_rope())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_gut_file(belief_mstr_dir, zia_gut)

    sue_gut = planunit_shop(sue_str, a23_str)
    sue_gut.set_max_tree_traverse(5)
    zia_gut.add_acctunit(yao_str, acct_debt_points=12)
    vacuum_str = "vacuum"
    vacuum_rope = sue_gut.make_l1_rope(vacuum_str)
    sue_gut.set_l1_concept(conceptunit_shop(vacuum_str, task=True))
    vacuum_conceptunit = sue_gut.get_concept_obj(vacuum_rope)
    vacuum_conceptunit.laborunit.set_laborlink(yao_str)

    egg_str = "egg first"
    egg_rope = sue_gut.make_l1_rope(egg_str)
    sue_gut.set_l1_concept(conceptunit_shop(egg_str))
    chicken_str = "chicken first"
    chicken_rope = sue_gut.make_l1_rope(chicken_str)
    sue_gut.set_l1_concept(conceptunit_shop(chicken_str))
    # set egg task is True when chicken first is False
    sue_gut.edit_concept_attr(
        egg_rope,
        task=True,
        reason_rcontext=chicken_rope,
        reason_rconcept_active_requisite=True,
    )
    # set chick task is True when egg first is False
    sue_gut.edit_concept_attr(
        chicken_rope,
        task=True,
        reason_rcontext=egg_rope,
        reason_rconcept_active_requisite=False,
    )
    save_gut_file(belief_mstr_dir, sue_gut)

    # WHEN
    new_yao_gut = create_listen_basis(yao_gut)
    listen_to_agendas_create_init_job_from_guts(belief_mstr_dir, new_yao_gut)

    # THEN irrational plan is ignored
    assert len(new_yao_gut.get_agenda_dict()) != 3
    assert len(new_yao_gut.get_agenda_dict()) == 2
    zia_acctunit = new_yao_gut.get_acct(zia_str)
    sue_acctunit = new_yao_gut.get_acct(sue_str)
    print(f"{sue_acctunit.acct_debt_points=}")
    print(f"{sue_acctunit._irrational_acct_debt_points=}")
    assert zia_acctunit._irrational_acct_debt_points == 0
    assert sue_acctunit._irrational_acct_debt_points == 51


def test_listen_to_agendas_create_init_job_from_guts_ProcessesMissingDebtorPlan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    yao_str = "Yao"
    a23_str = "amy23"
    yao_gut_path = create_gut_path(belief_mstr_dir, a23_str, yao_str)
    delete_dir(yao_gut_path)  # don't know why I have to do this...
    print(f"{os_path_exists(yao_gut_path)=}")
    yao_gut = planunit_shop(yao_str, a23_str)
    zia_str = "Zia"
    sue_str = "Sue"
    zia_acct_cred_points = 47
    sue_acct_cred_points = 57
    zia_acct_debt_points = 41
    sue_acct_debt_points = 51
    yao_gut.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_gut.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_pool = 92
    yao_gut.set_acct_respect(yao_pool)
    save_gut_file(belief_mstr_dir, yao_gut)

    zia_gut = planunit_shop(zia_str, a23_str)
    zia_gut.set_concept(conceptunit_shop(clean_str(), task=True), casa_rope())
    zia_gut.set_concept(conceptunit_shop(cook_str(), task=True), casa_rope())
    zia_gut.add_acctunit(yao_str, acct_debt_points=12)
    clean_conceptunit = zia_gut.get_concept_obj(clean_rope())
    cook_conceptunit = zia_gut.get_concept_obj(cook_rope())
    clean_conceptunit.laborunit.set_laborlink(yao_str)
    cook_conceptunit.laborunit.set_laborlink(yao_str)
    save_gut_file(belief_mstr_dir, zia_gut)

    # WHEN
    new_yao_gut = create_listen_basis(yao_gut)
    listen_to_agendas_create_init_job_from_guts(belief_mstr_dir, new_yao_gut)

    # THEN irrational plan is ignored
    assert len(new_yao_gut.get_agenda_dict()) != 3
    assert len(new_yao_gut.get_agenda_dict()) == 2
    zia_acctunit = new_yao_gut.get_acct(zia_str)
    sue_acctunit = new_yao_gut.get_acct(sue_str)
    print(f"{sue_acctunit.acct_debt_points=}")
    print(f"{sue_acctunit._inallocable_acct_debt_points=}")
    assert zia_acctunit._inallocable_acct_debt_points == 0
    assert sue_acctunit._inallocable_acct_debt_points == 51
