from src.f00_instrument.file import create_path
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f06_listen.hub_tool import (
    save_voice_file,
    open_voice_file,
    open_plan_file,
    save_plan_file,
)
from src.f06_listen.hubunit import hubunit_shop
from src.f08_fisc.fisc import fiscunit_shop
from src.f08_fisc.examples.fisc_env import (
    get_test_fisc_mstr_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_FiscUnit_generate_plan_Sets_planFile(env_dir_setup_cleanup):
    # ESTABLISH
    accord23_str = "accord23"
    x_fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(accord23_str, x_fisc_mstr_dir, True)
    sue_str = "Sue"
    x_sue_owner_dir = create_path(a23_fisc._owners_dir, sue_str)
    x_plan_dir = create_path(x_sue_owner_dir, "plan")
    x_sue_plan_path = create_path(x_plan_dir, f"{sue_str}.json")
    print(f"        {x_sue_plan_path=}")
    assert os_path_exists(x_sue_plan_path) is False
    a23_fisc.init_owner_keeps(sue_str)
    assert os_path_exists(x_sue_plan_path)

    # WHEN
    sue_plan = a23_fisc.generate_plan(sue_str)

    # THEN
    example_bud = budunit_shop(sue_str, accord23_str)
    assert sue_plan.fisc_title == example_bud.fisc_title
    assert sue_plan.owner_name == example_bud.owner_name


def test_FiscUnit_generate_plan_ReturnsRegeneratedObj(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "accord23"
    a23_fisc = fiscunit_shop(a23_str, get_test_fisc_mstr_dir(), True)
    sue_str = "Sue"
    a23_fisc.init_owner_keeps(sue_str)
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


def test_FiscUnit_generate_plan_SetsCorrectFileWithout_healerlink(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir, True)
    bob_str = "Bob"
    a23_fisc.init_owner_keeps(bob_str)
    before_bob_plan = a23_fisc.generate_plan(bob_str)
    sue_str = "Sue"
    assert before_bob_plan.acct_exists(sue_str) is False

    # WHEN
    bob_voice_bud = open_voice_file(fisc_mstr_dir, a23_str, bob_str)
    bob_voice_bud.add_acctunit(sue_str)
    save_voice_file(a23_fisc.fisc_mstr_dir, bob_voice_bud)

    # WHEN
    after_bob_plan = a23_fisc.generate_plan(bob_str)

    # THEN
    assert after_bob_plan.acct_exists(sue_str)


def test_FiscUnit_generate_plan_SetsFileWith_healerlink(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir, True)

    bob_str = "Bob"
    a23_fisc.init_owner_keeps(bob_str)
    after_bob_plan = a23_fisc.generate_plan(bob_str)
    assert after_bob_plan.acct_exists(bob_str) is False

    # WHEN
    bob_voice_bud = open_voice_file(fisc_mstr_dir, a23_str, bob_str)
    bob_voice_bud.add_acctunit(bob_str)
    bob_voice_bud.set_acct_respect(100)
    texas_str = "Texas"
    texas_road = bob_voice_bud.make_l1_road(texas_str)
    elpaso_str = "el paso"
    elpaso_road = bob_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))
    bob_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    bob_voice_bud.set_item(elpaso_item, texas_road)
    save_voice_file(a23_fisc.fisc_mstr_dir, bob_voice_bud)

    after_bob_plan = a23_fisc.generate_plan(bob_str)

    # THEN
    assert after_bob_plan.acct_exists(bob_str)


def test_FiscUnit_generate_all_plans_SetsCorrectFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    a23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir, True)

    bob_str = "Bob"
    sue_str = "Sue"
    a23_fisc.init_owner_keeps(bob_str)
    fisc_mstr_dir = a23_fisc.fisc_mstr_dir
    a23_fisc.init_owner_keeps(sue_str)
    bob_voice_bud = a23_fisc.generate_plan(bob_str)
    sue_voice_bud = a23_fisc.generate_plan(sue_str)

    texas_str = "Texas"
    texas_road = bob_voice_bud.make_l1_road(texas_str)
    elpaso_str = "el paso"
    elpaso_road = bob_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))

    bob_voice_bud = open_voice_file(fisc_mstr_dir, a23_str, bob_str)
    bob_voice_bud.add_acctunit(bob_str)
    bob_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    bob_voice_bud.set_item(elpaso_item, texas_road)
    save_voice_file(a23_fisc.fisc_mstr_dir, bob_voice_bud)

    sue_voice_bud = open_voice_file(fisc_mstr_dir, a23_str, sue_str)
    sue_voice_bud.add_acctunit(sue_str)
    sue_voice_bud.add_acctunit(bob_str)
    sue_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    sue_voice_bud.set_item(elpaso_item, texas_road)
    save_voice_file(a23_fisc.fisc_mstr_dir, sue_voice_bud)

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
