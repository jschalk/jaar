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


def test_FiscalUnit_generate_final_bud_Sets_final_BudFile(env_dir_setup_cleanup):
    # ESTABLISH
    music_str = "Music"
    music_fiscal = fiscalunit_shop(music_str, get_test_fiscals_dir(), True)
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(None, music_str, sue_str, None)

    x_sue_owner_dir = create_path(music_fiscal._owners_dir, sue_str)
    x_final_dir = create_path(x_sue_owner_dir, "final")
    x_sue_final_path = create_path(x_final_dir, f"{sue_str}.json")
    print(f"        {x_sue_final_path=}")
    print(f"{sue_hubunit.final_path()=}")
    assert os_path_exists(x_sue_final_path) is False
    music_fiscal.init_owner_keeps(sue_str)
    assert sue_hubunit.final_path() == x_sue_final_path
    assert os_path_exists(x_sue_final_path)

    # WHEN
    sue_final = music_fiscal.generate_final_bud(sue_str)

    # THEN
    example_bud = budunit_shop(sue_str, music_str)
    assert sue_final._fiscal_id == example_bud._fiscal_id
    assert sue_final._owner_id == example_bud._owner_id


def test_FiscalUnit_generate_final_bud_ReturnsRegeneratedObj(env_dir_setup_cleanup):
    # ESTABLISH
    music_fiscal = fiscalunit_shop("music", get_test_fiscals_dir(), True)
    sue_str = "Sue"
    music_fiscal.init_owner_keeps(sue_str)
    sue_hubunit = hubunit_shop(
        music_fiscal.fiscals_dir, music_fiscal.fiscal_id, sue_str, None
    )
    before_sue_bud = sue_hubunit.get_final_bud()
    bob_str = "Bob"
    before_sue_bud.add_acctunit(bob_str)
    sue_hubunit.save_final_bud(before_sue_bud)
    assert sue_hubunit.get_final_bud().acct_exists(bob_str)

    # WHEN
    after_sue_bud = music_fiscal.generate_final_bud(sue_str)

    # THEN method should wipe over final bud
    assert after_sue_bud.acct_exists(bob_str) is False


def test_FiscalUnit_generate_final_bud_SetsCorrectFileWithout_healerlink(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_fiscal = fiscalunit_shop("music", get_test_fiscals_dir(), True)
    bob_str = "Bob"
    music_fiscal.init_owner_keeps(bob_str)
    bob_hubunit = hubunit_shop(
        music_fiscal.fiscals_dir, music_fiscal.fiscal_id, bob_str, None
    )
    before_bob_final_bud = music_fiscal.generate_final_bud(bob_str)
    sue_str = "Sue"
    assert before_bob_final_bud.acct_exists(sue_str) is False

    # WHEN
    bob_voice_bud = bob_hubunit.get_voice_bud()
    bob_voice_bud.add_acctunit(sue_str)
    bob_hubunit.save_voice_bud(bob_voice_bud)

    # WHEN
    after_bob_final_bud = music_fiscal.generate_final_bud(bob_str)

    # THEN
    assert after_bob_final_bud.acct_exists(sue_str)


def test_FiscalUnit_generate_final_bud_SetsFileWith_healerlink(env_dir_setup_cleanup):
    # ESTABLISH
    music_fiscal = fiscalunit_shop("music", get_test_fiscals_dir(), True)

    bob_str = "Bob"
    music_fiscal.init_owner_keeps(bob_str)
    bob_hubunit = hubunit_shop(
        music_fiscal.fiscals_dir, music_fiscal.fiscal_id, bob_str, None
    )
    after_bob_final_bud = music_fiscal.generate_final_bud(bob_str)
    assert after_bob_final_bud.acct_exists(bob_str) is False

    # WHEN
    bob_voice_bud = bob_hubunit.get_voice_bud()
    bob_voice_bud.add_acctunit(bob_str)
    bob_voice_bud.set_acct_respect(100)
    texas_str = "Texas"
    texas_road = bob_voice_bud.make_l1_road(texas_str)
    elpaso_str = "el paso"
    elpaso_road = bob_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))
    bob_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    bob_voice_bud.set_item(elpaso_item, texas_road)
    bob_hubunit.save_voice_bud(bob_voice_bud)
    after_bob_final_bud = music_fiscal.generate_final_bud(bob_str)

    # THEN
    assert after_bob_final_bud.acct_exists(bob_str)


def test_FiscalUnit_generate_all_final_buds_SetsCorrectFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    music_fiscal = fiscalunit_shop("music", get_test_fiscals_dir(), True)

    bob_str = "Bob"
    sue_str = "Sue"
    music_fiscal.init_owner_keeps(bob_str)
    fiscals_dir = music_fiscal.fiscals_dir
    bob_hubunit = hubunit_shop(fiscals_dir, music_fiscal.fiscal_id, bob_str, None)
    music_fiscal.init_owner_keeps(sue_str)
    sue_hubunit = hubunit_shop(fiscals_dir, music_fiscal.fiscal_id, sue_str, None)
    bob_voice_bud = music_fiscal.generate_final_bud(bob_str)
    sue_voice_bud = music_fiscal.generate_final_bud(sue_str)

    texas_str = "Texas"
    texas_road = bob_voice_bud.make_l1_road(texas_str)
    elpaso_str = "el paso"
    elpaso_road = bob_voice_bud.make_road(texas_road, elpaso_str)
    elpaso_item = itemunit_shop(elpaso_str, healerlink=healerlink_shop({bob_str}))

    bob_voice_bud = bob_hubunit.get_voice_bud()
    bob_voice_bud.add_acctunit(bob_str)
    bob_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    bob_voice_bud.set_item(elpaso_item, texas_road)
    bob_hubunit.save_voice_bud(bob_voice_bud)

    sue_voice_bud = sue_hubunit.get_voice_bud()
    sue_voice_bud.add_acctunit(sue_str)
    sue_voice_bud.add_acctunit(bob_str)
    sue_voice_bud.set_l1_item(itemunit_shop(texas_str, problem_bool=True))
    sue_voice_bud.set_item(elpaso_item, texas_road)
    sue_hubunit.save_voice_bud(sue_voice_bud)

    before_bob_final_bud = music_fiscal.get_final_file_bud(bob_str)
    before_sue_final_bud = music_fiscal.get_final_file_bud(sue_str)
    assert before_bob_final_bud.acct_exists(bob_str) is False
    assert before_sue_final_bud.acct_exists(sue_str) is False

    # WHEN
    music_fiscal.generate_all_final_buds()

    # THEN
    after_bob_final_bud = music_fiscal.get_final_file_bud(bob_str)
    after_sue_final_bud = music_fiscal.get_final_file_bud(sue_str)
    assert after_bob_final_bud.acct_exists(bob_str)
    assert after_sue_final_bud.acct_exists(sue_str)
