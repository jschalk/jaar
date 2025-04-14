from src.a00_data_toolboxs.file_toolbox import set_dir
from src.a05_item_logic.healer import healerlink_shop
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hub_path import (
    create_fisc_owners_dir_path,
    create_owner_dir_path,
)
from src.a12_hub_tools.hub_tool import (
    save_gut_file,
    open_gut_file,
    open_plan_file,
    save_plan_file,
    gut_file_exists,
    plan_file_exists,
)
from src.a15_fisc_logic.fisc import fiscunit_shop
from src.a15_fisc_logic.examples.fisc_env import (
    get_test_fisc_mstr_dir,
    env_dir_setup_cleanup,
)


def test_FiscUnit_generate_plan_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    sue_str = "Sue"
    assert not plan_file_exists(fisc_mstr_dir, a23_str, sue_str)
    a23_fisc.set_init_pack_and_plan(sue_str)
    assert plan_file_exists(fisc_mstr_dir, a23_str, sue_str)

    # WHEN
    sue_plan = a23_fisc.generate_plan(sue_str)

    # THEN
    example_bud = budunit_shop(sue_str, a23_str)
    assert sue_plan.fisc_title == example_bud.fisc_title
    assert sue_plan.owner_name == example_bud.owner_name


def test_FiscUnit_generate_plan_ReturnsObj_Scenario2_plan_changed(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, get_test_fisc_mstr_dir(), True)
    sue_str = "Sue"
    a23_fisc.set_init_pack_and_plan(sue_str)
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    before_sue_bud = open_plan_file(fisc_mstr_dir, a23_str, sue_str)
    bob_str = "Bob"
    before_sue_bud.add_acctunit(bob_str)
    save_plan_file(fisc_mstr_dir, before_sue_bud)
    assert open_plan_file(fisc_mstr_dir, a23_str, sue_str).acct_exists(bob_str)

    # WHEN
    after_sue_bud = a23_fisc.generate_plan(sue_str)

    # THEN method should wipe over plan bud
    assert after_sue_bud.acct_exists(bob_str) is False


def test_FiscUnit_generate_plan_ReturnsObj_Scenario3_Without_healerlink(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    bob_str = "Bob"
    a23_fisc.set_init_pack_and_plan(bob_str)
    before_bob_plan = a23_fisc.generate_plan(bob_str)
    sue_str = "Sue"
    assert before_bob_plan.acct_exists(sue_str) is False

    # WHEN
    bob_gut_bud = open_gut_file(fisc_mstr_dir, a23_str, bob_str)
    bob_gut_bud.add_acctunit(sue_str)
    save_gut_file(a23_fisc.fisc_mstr_dir, bob_gut_bud)

    # WHEN
    after_bob_plan = a23_fisc.generate_plan(bob_str)

    # THEN
    assert after_bob_plan.acct_exists(sue_str)


def test_FiscUnit_generate_plan_ReturnsObj_Scenario4_With_healerlink(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)

    bob_str = "Bob"
    a23_fisc.set_init_pack_and_plan(bob_str)
    after_bob_plan = a23_fisc.generate_plan(bob_str)
    assert after_bob_plan.acct_exists(bob_str) is False

    # WHEN
    bob_gut_bud = open_gut_file(fisc_mstr_dir, a23_str, bob_str)
    bob_gut_bud.add_acctunit(bob_str)
    bob_gut_bud.set_acct_respect(100)
    texas_str = "Texas"
    texas_road = bob_gut_bud.make_l1_road(texas_str)
    elpaso_str = "el paso"
    elpaso_road = bob_gut_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))
    bob_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    bob_gut_bud.set_item(elpaso_item, texas_road)
    save_gut_file(a23_fisc.fisc_mstr_dir, bob_gut_bud)

    after_bob_plan = a23_fisc.generate_plan(bob_str)

    # THEN
    assert after_bob_plan.acct_exists(bob_str)


def test_FiscUnit_generate_all_plans_Scenario0_Initial_plan_IsCreated(
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
    assert plan_file_exists(fisc_mstr_dir, a23_str, bob_str) is False
    assert plan_file_exists(fisc_mstr_dir, a23_str, sue_str) is False

    # WHEN
    a23_fisc.generate_all_plans()

    # THEN
    assert gut_file_exists(fisc_mstr_dir, a23_str, bob_str)
    assert gut_file_exists(fisc_mstr_dir, a23_str, sue_str)
    assert plan_file_exists(fisc_mstr_dir, a23_str, bob_str)
    assert plan_file_exists(fisc_mstr_dir, a23_str, sue_str)


def test_FiscUnit_generate_all_plans_Scenario1_SetsCorrectFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)

    bob_str = "Bob"
    sue_str = "Sue"
    a23_fisc.set_init_pack_and_plan(bob_str)
    fisc_mstr_dir = a23_fisc.fisc_mstr_dir
    a23_fisc.set_init_pack_and_plan(sue_str)
    bob_gut_bud = a23_fisc.generate_plan(bob_str)
    sue_gut_bud = a23_fisc.generate_plan(sue_str)

    texas_str = "Texas"
    texas_road = bob_gut_bud.make_l1_road(texas_str)
    elpaso_str = "el paso"
    elpaso_road = bob_gut_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))

    bob_gut_bud = open_gut_file(fisc_mstr_dir, a23_str, bob_str)
    bob_gut_bud.add_acctunit(bob_str)
    bob_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    bob_gut_bud.set_item(elpaso_item, texas_road)
    save_gut_file(a23_fisc.fisc_mstr_dir, bob_gut_bud)

    sue_gut_bud = open_gut_file(fisc_mstr_dir, a23_str, sue_str)
    sue_gut_bud.add_acctunit(sue_str)
    sue_gut_bud.add_acctunit(bob_str)
    sue_gut_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    sue_gut_bud.set_item(elpaso_item, texas_road)
    save_gut_file(a23_fisc.fisc_mstr_dir, sue_gut_bud)

    before_bob_plan = a23_fisc.get_plan_file_bud(bob_str)
    before_sue_plan = a23_fisc.get_plan_file_bud(sue_str)
    assert before_bob_plan.acct_exists(bob_str) is False
    assert before_sue_plan.acct_exists(sue_str) is False

    # WHEN
    a23_fisc.generate_all_plans()

    # THEN
    after_bob_plan = a23_fisc.get_plan_file_bud(bob_str)
    after_sue_plan = a23_fisc.get_plan_file_bud(sue_str)
    assert after_bob_plan.acct_exists(bob_str)
    assert after_sue_plan.acct_exists(sue_str)


# def test_FiscUnit_generate_all_plans_Scenario2_plan_limit_rotation_Changes_plan(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     a23_str = "accord23"
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     x_plan_listen_rotations = 2
#     a23_fisc = fiscunit_shop(
#         a23_str, fisc_mstr_dir, plan_listen_rotations=x_plan_listen_rotations
#     )

#     bob_str = "Bob"
#     sue_str = "Sue"
#     sue_str = "Sue"
#     a23_fisc.set_init_pack_and_plan(bob_str)
#     fisc_mstr_dir = a23_fisc.fisc_mstr_dir
#     a23_fisc.set_init_pack_and_plan(sue_str)
#     bob_gut_bud = a23_fisc.generate_plan(bob_str)
#     sue_gut_bud = a23_fisc.generate_plan(sue_str)

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

#     before_bob_plan = a23_fisc.get_plan_file_bud(bob_str)
#     before_sue_plan = a23_fisc.get_plan_file_bud(sue_str)
#     assert a23_fisc.plan_listen_rotations == 9
#     assert before_bob_plan.acct_exists(bob_str) is False
#     assert before_sue_plan.acct_exists(sue_str) is False

#     # WHEN
#     a23_fisc.generate_all_plans()

#     # THEN
#     after_bob_plan = a23_fisc.get_plan_file_bud(bob_str)
#     after_sue_plan = a23_fisc.get_plan_file_bud(sue_str)
#     assert after_bob_plan.acct_exists(bob_str)
#     assert after_sue_plan.acct_exists(sue_str)

#     assert 1 == 2
