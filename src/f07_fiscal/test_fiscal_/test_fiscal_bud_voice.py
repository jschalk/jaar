from src.f00_instrument.file import create_path
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import budunit_shop
from src.f05_listen.hubunit import hubunit_shop
from src.f07_fiscal.fiscal import fiscalunit_shop
from src.f07_fiscal.examples.fiscal_env import (
    get_test_fiscals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_FiscalUnit_generate_voice_bud_Sets_voice_BudFile(env_dir_setup_cleanup):
    # ESTABLISH
    accord45_str = "accord45"
    x_fiscals_dir = get_test_fiscals_dir()
    accord_fiscal = fiscalunit_shop(accord45_str, x_fiscals_dir, True)
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(x_fiscals_dir, accord45_str, sue_str, None)

    x_sue_owner_dir = create_path(accord_fiscal._owners_dir, sue_str)
    x_voice_dir = create_path(x_sue_owner_dir, "voice")
    x_sue_voice_path = create_path(x_voice_dir, f"{sue_str}.json")
    print(f"        {x_sue_voice_path=}")
    print(f"{sue_hubunit._voice_path=}")
    assert os_path_exists(x_sue_voice_path) is False
    accord_fiscal.init_owner_keeps(sue_str)
    assert sue_hubunit._voice_path == x_sue_voice_path
    assert os_path_exists(x_sue_voice_path)

    # WHEN
    sue_voice = accord_fiscal.generate_voice_bud(sue_str)

    # THEN
    example_bud = budunit_shop(sue_str, accord45_str)
    assert sue_voice.fiscal_title == example_bud.fiscal_title
    assert sue_voice.owner_name == example_bud.owner_name


def test_FiscalUnit_generate_voice_bud_ReturnsRegeneratedObj(env_dir_setup_cleanup):
    # ESTABLISH
    accord_fiscal = fiscalunit_shop("accord45", get_test_fiscals_dir(), True)
    sue_str = "Sue"
    accord_fiscal.init_owner_keeps(sue_str)
    sue_hubunit = hubunit_shop(
        accord_fiscal.fiscals_dir, accord_fiscal.fiscal_title, sue_str, None
    )
    before_sue_bud = sue_hubunit.get_voice_bud()
    bob_str = "Bob"
    before_sue_bud.add_acctunit(bob_str)
    sue_hubunit.save_voice_bud(before_sue_bud)
    assert sue_hubunit.get_voice_bud().acct_exists(bob_str)

    # WHEN
    after_sue_bud = accord_fiscal.generate_voice_bud(sue_str)

    # THEN method should wipe over voice bud
    assert after_sue_bud.acct_exists(bob_str) is False


def test_FiscalUnit_generate_voice_bud_SetsCorrectFileWithout_healerlink(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord_fiscal = fiscalunit_shop("accord45", get_test_fiscals_dir(), True)
    bob_str = "Bob"
    accord_fiscal.init_owner_keeps(bob_str)
    bob_hubunit = hubunit_shop(
        accord_fiscal.fiscals_dir, accord_fiscal.fiscal_title, bob_str, None
    )
    before_bob_voice_bud = accord_fiscal.generate_voice_bud(bob_str)
    sue_str = "Sue"
    assert before_bob_voice_bud.acct_exists(sue_str) is False

    # WHEN
    bob_soul_bud = bob_hubunit.get_soul_bud()
    bob_soul_bud.add_acctunit(sue_str)
    bob_hubunit.save_soul_bud(bob_soul_bud)

    # WHEN
    after_bob_voice_bud = accord_fiscal.generate_voice_bud(bob_str)

    # THEN
    assert after_bob_voice_bud.acct_exists(sue_str)


def test_FiscalUnit_generate_voice_bud_SetsFileWith_healerlink(env_dir_setup_cleanup):
    # ESTABLISH
    accord_fiscal = fiscalunit_shop("accord45", get_test_fiscals_dir(), True)

    bob_str = "Bob"
    accord_fiscal.init_owner_keeps(bob_str)
    bob_hubunit = hubunit_shop(
        accord_fiscal.fiscals_dir, accord_fiscal.fiscal_title, bob_str, None
    )
    after_bob_voice_bud = accord_fiscal.generate_voice_bud(bob_str)
    assert after_bob_voice_bud.acct_exists(bob_str) is False

    # WHEN
    bob_soul_bud = bob_hubunit.get_soul_bud()
    bob_soul_bud.add_acctunit(bob_str)
    bob_soul_bud.set_acct_respect(100)
    texas_str = "Texas"
    texas_road = bob_soul_bud.make_l1_road(texas_str)
    elpaso_str = "el paso"
    elpaso_road = bob_soul_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))
    bob_soul_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    bob_soul_bud.set_item(elpaso_item, texas_road)
    bob_hubunit.save_soul_bud(bob_soul_bud)
    after_bob_voice_bud = accord_fiscal.generate_voice_bud(bob_str)

    # THEN
    assert after_bob_voice_bud.acct_exists(bob_str)


def test_FiscalUnit_generate_all_voice_buds_SetsCorrectFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord_fiscal = fiscalunit_shop("accord45", get_test_fiscals_dir(), True)

    bob_str = "Bob"
    sue_str = "Sue"
    accord_fiscal.init_owner_keeps(bob_str)
    fiscals_dir = accord_fiscal.fiscals_dir
    bob_hubunit = hubunit_shop(fiscals_dir, accord_fiscal.fiscal_title, bob_str, None)
    accord_fiscal.init_owner_keeps(sue_str)
    sue_hubunit = hubunit_shop(fiscals_dir, accord_fiscal.fiscal_title, sue_str, None)
    bob_soul_bud = accord_fiscal.generate_voice_bud(bob_str)
    sue_soul_bud = accord_fiscal.generate_voice_bud(sue_str)

    texas_str = "Texas"
    texas_road = bob_soul_bud.make_l1_road(texas_str)
    elpaso_str = "el paso"
    elpaso_road = bob_soul_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))

    bob_soul_bud = bob_hubunit.get_soul_bud()
    bob_soul_bud.add_acctunit(bob_str)
    bob_soul_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    bob_soul_bud.set_item(elpaso_item, texas_road)
    bob_hubunit.save_soul_bud(bob_soul_bud)

    sue_soul_bud = sue_hubunit.get_soul_bud()
    sue_soul_bud.add_acctunit(sue_str)
    sue_soul_bud.add_acctunit(bob_str)
    sue_soul_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    sue_soul_bud.set_item(elpaso_item, texas_road)
    sue_hubunit.save_soul_bud(sue_soul_bud)

    before_bob_voice_bud = accord_fiscal.get_voice_file_bud(bob_str)
    before_sue_voice_bud = accord_fiscal.get_voice_file_bud(sue_str)
    assert before_bob_voice_bud.acct_exists(bob_str) is False
    assert before_sue_voice_bud.acct_exists(sue_str) is False

    # WHEN
    accord_fiscal.generate_all_voice_buds()

    # THEN
    after_bob_voice_bud = accord_fiscal.get_voice_file_bud(bob_str)
    after_sue_voice_bud = accord_fiscal.get_voice_file_bud(sue_str)
    assert after_bob_voice_bud.acct_exists(bob_str)
    assert after_sue_voice_bud.acct_exists(sue_str)
