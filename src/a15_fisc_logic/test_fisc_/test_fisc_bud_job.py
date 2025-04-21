from src.a00_data_toolboxs.file_toolbox import set_dir
from src.a05_item_logic.healer import healerlink_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop, BudUnit
from src.a12_hub_tools.hub_path import create_owner_dir_path
from src.a12_hub_tools.hub_tool import (
    save_gut_file,
    open_gut_file,
    open_job_file,
    save_job_file,
    gut_file_exists,
    job_file_exists,
)
from src.a15_fisc_logic.fisc import fiscunit_shop
from src.a15_fisc_logic.examples.fisc_env import (
    get_test_fisc_mstr_dir,
    env_dir_setup_cleanup,
)


def test_FiscUnit_rotate_job_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    sue_str = "Sue"
    assert not job_file_exists(fisc_mstr_dir, a23_str, sue_str)
    a23_fisc.create_init_job_from_guts(sue_str)
    assert job_file_exists(fisc_mstr_dir, a23_str, sue_str)

    # WHEN
    sue_job = a23_fisc.rotate_job(sue_str)

    # THEN
    example_bud = budunit_shop(sue_str, a23_str)
    assert sue_job.fisc_tag == example_bud.fisc_tag
    assert sue_job.owner_name == example_bud.owner_name


def test_FiscUnit_rotate_job_ReturnsObj_Scenario2_EmptyAcctsCause_inallocable_debtit_belief(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    init_sue_job = budunit_shop(sue_str, a23_str)
    init_sue_job.add_acctunit(yao_str)
    init_sue_job.add_acctunit(bob_str)
    init_sue_job.add_acctunit(zia_str)
    save_job_file(fisc_mstr_dir, init_sue_job)
    assert job_file_exists(fisc_mstr_dir, a23_str, sue_str)
    assert job_file_exists(fisc_mstr_dir, a23_str, yao_str) is False
    assert job_file_exists(fisc_mstr_dir, a23_str, bob_str) is False
    assert job_file_exists(fisc_mstr_dir, a23_str, zia_str) is False

    # WHEN
    rotated_sue_job = a23_fisc.rotate_job(sue_str)

    # THEN method should wipe over job bud
    assert rotated_sue_job.acct_exists(bob_str)
    assert rotated_sue_job.get_dict() != init_sue_job.get_dict()
    assert init_sue_job.get_acct(bob_str)._inallocable_debtit_belief == 0
    assert rotated_sue_job.get_acct(bob_str)._inallocable_debtit_belief == 1


def a23_job(owner_name: str) -> BudUnit:
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    return open_job_file(fisc_mstr_dir, "accord23", owner_name)


def test_FiscUnit_rotate_job_ReturnsObj_Scenario3_job_ChangesFromRotation(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    init_sue_job = budunit_shop(sue_str, a23_str)
    init_sue_job.add_acctunit(yao_str)
    init_yao_job = budunit_shop(yao_str, a23_str)
    init_yao_job.add_acctunit(bob_str)
    init_bob_job = budunit_shop(bob_str, a23_str)
    casa_road = init_bob_job.make_l1_road("casa")
    clean_road = init_bob_job.make_road(casa_road, "clean")
    init_bob_job.add_item(clean_road, pledge=True)
    save_job_file(fisc_mstr_dir, init_sue_job)
    save_job_file(fisc_mstr_dir, init_yao_job)
    save_job_file(fisc_mstr_dir, init_bob_job)
    assert len(a23_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_job(yao_str).get_agenda_dict()) == 0
    assert len(a23_job(bob_str).get_agenda_dict()) == 1

    # WHEN / THEN
    assert len(a23_fisc.rotate_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_fisc.rotate_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_fisc.rotate_job(bob_str).get_agenda_dict()) == 0


def test_FiscUnit_rotate_job_ReturnsObj_Scenario4_job_SelfReferenceWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    init_bob_job = budunit_shop(bob_str, a23_str)
    init_bob_job.add_acctunit(bob_str)
    init_sue_job = budunit_shop(sue_str, a23_str)
    init_sue_job.add_acctunit(yao_str)
    init_yao_job = budunit_shop(yao_str, a23_str)
    init_yao_job.add_acctunit(bob_str)
    casa_road = init_bob_job.make_l1_road("casa")
    clean_road = init_bob_job.make_road(casa_road, "clean")
    init_bob_job.add_item(clean_road, pledge=True)
    save_job_file(fisc_mstr_dir, init_sue_job)
    save_job_file(fisc_mstr_dir, init_yao_job)
    save_job_file(fisc_mstr_dir, init_bob_job)
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_job(yao_str).get_agenda_dict()) == 0

    # WHEN / THEN
    assert len(a23_fisc.rotate_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_fisc.rotate_job(sue_str).get_agenda_dict()) == 0
    assert len(a23_fisc.rotate_job(yao_str).get_agenda_dict()) == 1


# def test_FiscUnit_rotate_job_ReturnsObj_Scenario3_Without_healerlink(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     a23_str = "accord23"
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
#     bob_str = "Bob"
#     a23_fisc.create_init_job_from_guts(bob_str)
#     before_bob_job = a23_fisc.rotate_job(bob_str)
#     sue_str = "Sue"
#     assert before_bob_job.acct_exists(sue_str) is False

#     # WHEN
#     bob_gut_bud = open_gut_file(fisc_mstr_dir, a23_str, bob_str)
#     bob_gut_bud.add_acctunit(sue_str)
#     save_gut_file(a23_fisc.fisc_mstr_dir, bob_gut_bud)

#     # WHEN
#     after_bob_job = a23_fisc.rotate_job(bob_str)

#     # THEN
#     assert after_bob_job.acct_exists(sue_str)


# def test_FiscUnit_rotate_job_ReturnsObj_Scenario4_With_healerlink(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     a23_str = "accord23"
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)

#     bob_str = "Bob"
#     a23_fisc.create_init_job_from_guts(bob_str)
#     after_bob_job = a23_fisc.rotate_job(bob_str)
#     assert after_bob_job.acct_exists(bob_str) is False

#     # WHEN
#     bob_gut_bud = open_gut_file(fisc_mstr_dir, a23_str, bob_str)
#     bob_gut_bud.add_acctunit(bob_str)
#     bob_gut_bud.set_acct_respect(100)
#     texas_str = "Texas"
#     texas_road = bob_gut_bud.make_l1_road(texas_str)
#     elpaso_str = "el paso"
#     elpaso_road = bob_gut_bud.make_road(texas_road, elpaso_str)
#     elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))
#     bob_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
#     bob_gut_bud.set_item(elpaso_item, texas_road)
#     save_gut_file(a23_fisc.fisc_mstr_dir, bob_gut_bud)

#     after_bob_job = a23_fisc.rotate_job(bob_str)

#     # THEN
#     assert after_bob_job.acct_exists(bob_str)


# def test_FiscUnit_rotate_job_ReturnsObj_Scenario0_Empty_gut(env_dir_setup_cleanup):
#     # ESTABLISH
#     a23_str = "accord23"
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
#     sue_str = "Sue"
#     a23_fisc.set_gut_if_none(sue_str)
#     sue_gut = open_gut_file(fisc_mstr_dir, a23_str, sue_str)
#     assert len(sue_gut.get_acctunits_dict()) == 0

#     # WHEN / THEN
#     assert not a23_fisc.rotate_job(sue_str)


# def test_FiscUnit_rotate_job_ReturnsObj_Scenario1_gut_accts_Equal_job_accts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
#     sue_str = "Sue"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     sue_gut = budunit_shop(sue_str, a23_str)
#     sue_gut.add_acctunit(sue_str)
#     sue_gut.add_acctunit(bob_str)
#     sue_gut.add_acctunit(yao_str)
#     save_gut_file(fisc_mstr_dir, sue_gut)
#     sue_gut = open_gut_file(fisc_mstr_dir, a23_str, sue_str)
#     assert len(sue_gut.get_acctunits_dict()) == 3

#     # WHEN
#     sue_job = a23_fisc.rotate_job(sue_str)

#     # THEN
#     expected_job = budunit_shop(sue_str, a23_str)
#     expected_job.add_acctunit(sue_str)
#     expected_job.add_acctunit(bob_str)
#     expected_job.add_acctunit(yao_str)
#     expected_job.settle_bud()
#     sue_job.settle_bud()
#     assert sue_job.accts.keys() == expected_job.accts.keys()
#     expected_sue_acct = sue_job.get_acct(sue_str)
#     expected_bob_acct = sue_job.get_acct(bob_str)
#     assert sue_job.get_acct(sue_str) == expected_sue_acct
#     assert sue_job.get_acct(bob_str) == expected_bob_acct
#     print(f"{sue_job.get_acctunits_dict().get(bob_str)=}")
#     print(f"{expected_job.get_acctunits_dict().get(bob_str)=}")
#     assert sue_job.get_acctunits_dict() == expected_job.get_acctunits_dict()
#     assert sue_job.get_dict() == expected_job.get_dict()
#     assert 1 == 5


# def test_FiscUnit_rotate_job_ReturnsObj_Scenario1_gut_with_Agenda(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
#     sue_str = "Sue"
#     sue_bud = budunit_shop(sue_str, a23_str)
#     casa_road = sue_bud.make_l1_road("casa")
#     dirty_road = sue_bud.make_road(casa_road, "dirty")
#     mop_road = sue_bud.make_road(casa_road, "mop")
#     sue_bud.add_item(mop_road, pledge=True)
#     sue_bud.add_item(dirty_road)
#     sue_bud.edit_reason(mop_road, casa_road, dirty_road)
#     sue_bud.add_fact(casa_road, dirty_road)
#     save_gut_file(fisc_mstr_dir, sue_bud)
#     sue_gut = open_gut_file(fisc_mstr_dir, a23_str, sue_str)
#     assert len(sue_gut.get_acctunits_dict()) == 0

#     # WHEN
#     sue_job = a23_fisc.rotate_job(sue_str)

#     # THEN
#     expected_job = budunit_shop(sue_str, a23_str)
#     expected_job.add_item(mop_road, pledge=True)
#     expected_job.add_item(dirty_road)
#     expected_job.edit_reason(mop_road, casa_road, dirty_road)
#     expected_job.add_fact(casa_road, dirty_road)
#     assert sue_job.fisc_tag == expected_job.fisc_tag
#     assert sue_job.owner_name == expected_job.owner_name
#     assert sue_job.get_agenda_dict() == expected_job.get_agenda_dict()
#     assert sue_job.get_dict() == expected_job.get_dict()
#     assert 1 == 2


# def test_FiscUnit_rotate_job_ReturnsObj_Scenario2_gut_with_FactUnit(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord23"
#     a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
#     sue_str = "Sue"
#     sue_bud = budunit_shop(sue_str, a23_str)
#     casa_road = sue_bud.make_l1_road("casa")
#     clean_road = sue_bud.make_road(casa_road, "clean")
#     dirty_road = sue_bud.make_road(casa_road, "dirty")
#     mop_road = sue_bud.make_road(casa_road, "mop")
#     sue_bud.add_item(mop_road, pledge=True)
#     sue_bud.add_item(dirty_road)
#     sue_bud.edit_reason(mop_road, casa_road, dirty_road)
#     sue_bud.add_fact(casa_road, clean_road, create_missing_items=True)
#     save_gut_file(fisc_mstr_dir, sue_bud)
#     sue_gut = open_gut_file(fisc_mstr_dir, a23_str, sue_str)
#     assert len(sue_gut.get_acctunits_dict()) == 0

#     # WHEN
#     sue_job = a23_fisc.rotate_job(sue_str)

#     # THEN
#     expected_job = budunit_shop(sue_str, a23_str)
#     expected_job.add_fact(casa_road, clean_road, create_missing_items=True)
#     assert sue_job.fisc_tag == expected_job.fisc_tag
#     assert sue_job.owner_name == expected_job.owner_name
#     assert sue_job.get_factunits_dict() == expected_job.get_factunits_dict()
#     assert sue_job.get_dict() == expected_job.get_dict()
#     assert 1 == 2


def test_FiscUnit_generate_all_jobs_Scenario0_init_job_IsCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    bob_str = "Bob"
    sue_str = "Sue"
    bob_gut = budunit_shop(bob_str, a23_str)
    save_gut_file(fisc_mstr_dir, bob_gut)
    sue_dir = create_owner_dir_path(fisc_mstr_dir, a23_str, sue_str)
    set_dir(sue_dir)
    assert gut_file_exists(fisc_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(fisc_mstr_dir, a23_str, sue_str) is False
    assert job_file_exists(fisc_mstr_dir, a23_str, bob_str) is False
    assert job_file_exists(fisc_mstr_dir, a23_str, sue_str) is False

    # WHEN
    a23_fisc.generate_all_jobs()

    # THEN
    assert gut_file_exists(fisc_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(fisc_mstr_dir, a23_str, sue_str)
    assert job_file_exists(fisc_mstr_dir, a23_str, bob_str)
    assert job_file_exists(fisc_mstr_dir, a23_str, sue_str)


def test_FiscUnit_generate_all_jobs_Scenario1_jobs_rotated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    bob_gut = budunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit(bob_str)
    bob_gut.add_acctunit(sue_str)
    casa_road = bob_gut.make_l1_road("casa")
    clean_road = bob_gut.make_road(casa_road, "clean")
    bob_gut.add_item(clean_road, pledge=True)

    sue_gut = budunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(sue_str)
    sue_gut.add_acctunit(bob_str)
    yao_gut = budunit_shop(yao_str, a23_str)
    yao_gut.add_acctunit(sue_str)
    save_gut_file(fisc_mstr_dir, bob_gut)
    save_gut_file(fisc_mstr_dir, sue_gut)
    save_gut_file(fisc_mstr_dir, yao_gut)
    assert not job_file_exists(fisc_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(fisc_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(fisc_mstr_dir, a23_str, yao_str)

    # WHEN
    a23_fisc.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1


def test_FiscUnit_generate_all_jobs_Scenario2_jobs_rotated_InSortedOrder(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_gut = budunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit(bob_str)
    bob_gut.add_acctunit(sue_str)

    sue_gut = budunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(sue_str)
    sue_gut.add_acctunit(bob_str)
    sue_gut.add_acctunit(yao_str)

    yao_gut = budunit_shop(yao_str, a23_str)
    yao_gut.add_acctunit(sue_str)
    yao_gut.add_acctunit(yao_str)
    yao_gut.add_acctunit(zia_str)

    zia_gut = budunit_shop(zia_str, a23_str)
    zia_gut.add_acctunit(zia_str)
    casa_road = zia_gut.make_l1_road("casa")
    clean_road = zia_gut.make_road(casa_road, "clean")
    zia_gut.add_item(clean_road, pledge=True)
    save_gut_file(fisc_mstr_dir, bob_gut)
    save_gut_file(fisc_mstr_dir, sue_gut)
    save_gut_file(fisc_mstr_dir, yao_gut)
    save_gut_file(fisc_mstr_dir, zia_gut)
    assert not job_file_exists(fisc_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(fisc_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(fisc_mstr_dir, a23_str, yao_str)
    assert not job_file_exists(fisc_mstr_dir, a23_str, zia_str)

    # WHEN
    a23_fisc.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 0
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1


def test_FiscUnit_generate_all_jobs_Scenario3_job_listen_rotation_AffectsJobs(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir, job_listen_rotations=1)
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_gut = budunit_shop(bob_str, a23_str)
    bob_gut.add_acctunit(bob_str)
    bob_gut.add_acctunit(sue_str)

    sue_gut = budunit_shop(sue_str, a23_str)
    sue_gut.add_acctunit(sue_str)
    sue_gut.add_acctunit(bob_str)
    sue_gut.add_acctunit(yao_str)

    yao_gut = budunit_shop(yao_str, a23_str)
    yao_gut.add_acctunit(sue_str)
    yao_gut.add_acctunit(yao_str)
    yao_gut.add_acctunit(zia_str)

    zia_gut = budunit_shop(zia_str, a23_str)
    zia_gut.add_acctunit(zia_str)
    casa_road = zia_gut.make_l1_road("casa")
    clean_road = zia_gut.make_road(casa_road, "clean")
    zia_gut.add_item(clean_road, pledge=True)
    save_gut_file(fisc_mstr_dir, bob_gut)
    save_gut_file(fisc_mstr_dir, sue_gut)
    save_gut_file(fisc_mstr_dir, yao_gut)
    save_gut_file(fisc_mstr_dir, zia_gut)
    assert not job_file_exists(fisc_mstr_dir, a23_str, bob_str)
    assert not job_file_exists(fisc_mstr_dir, a23_str, sue_str)
    assert not job_file_exists(fisc_mstr_dir, a23_str, yao_str)
    assert not job_file_exists(fisc_mstr_dir, a23_str, zia_str)
    assert a23_fisc.job_listen_rotations == 1

    # WHEN
    a23_fisc.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 0
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1

    # WHEN
    a23_fisc.job_listen_rotations = 2
    a23_fisc.generate_all_jobs()

    # THEN
    assert len(a23_job(bob_str).get_agenda_dict()) == 1
    assert len(a23_job(sue_str).get_agenda_dict()) == 1
    assert len(a23_job(yao_str).get_agenda_dict()) == 1
    assert len(a23_job(zia_str).get_agenda_dict()) == 1


# def test_FiscUnit_generate_all_jobs_Scenario2_job_limit_rotation_Changes_job(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     a23_str = "accord23"
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     x_job_listen_rotations = 2
#     a23_fisc = fiscunit_shop(
#         a23_str, fisc_mstr_dir, job_listen_rotations=x_job_listen_rotations
#     )

#     bob_str = "Bob"
#     sue_str = "Sue"
#     sue_str = "Sue"
#     a23_fisc.create_init_job_from_guts(bob_str)
#     fisc_mstr_dir = a23_fisc.fisc_mstr_dir
#     a23_fisc.create_init_job_from_guts(sue_str)
#     bob_gut_bud = a23_fisc.rotate_job(bob_str)
#     sue_gut_bud = a23_fisc.rotate_job(sue_str)

#     texas_str = "Texas"
#     texas_road = bob_gut_bud.make_l1_road(texas_str)
#     elpaso_str = "el paso"
#     elpaso_road = bob_gut_bud.make_road(texas_road, elpaso_str)
#     elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))

#     bob_gut_bud = open_gut_file(fisc_mstr_dir, a23_str, bob_str)
#     bob_gut_bud.add_acctunit(bob_str)
#     bob_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
#     bob_gut_bud.set_item(elpaso_item, texas_road)
#     save_gut_file(a23_fisc.fisc_mstr_dir, bob_gut_bud)

#     sue_gut_bud = open_gut_file(fisc_mstr_dir, a23_str, sue_str)
#     sue_gut_bud.add_acctunit(sue_str)
#     sue_gut_bud.add_acctunit(bob_str)
#     sue_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
#     sue_gut_bud.set_item(elpaso_item, texas_road)
#     save_gut_file(a23_fisc.fisc_mstr_dir, sue_gut_bud)

#     before_bob_job = a23_fisc.get_job_file_bud(bob_str)
#     before_sue_job = a23_fisc.get_job_file_bud(sue_str)
#     assert a23_fisc.job_listen_rotations == 9
#     assert before_bob_job.acct_exists(bob_str) is False
#     assert before_sue_job.acct_exists(sue_str) is False

#     # WHEN
#     a23_fisc.generate_all_jobs()

#     # THEN
#     after_bob_job = a23_fisc.get_job_file_bud(bob_str)
#     after_sue_job = a23_fisc.get_job_file_bud(sue_str)
#     assert after_bob_job.acct_exists(bob_str)
#     assert after_sue_job.acct_exists(sue_str)

#     assert 1 == 2
