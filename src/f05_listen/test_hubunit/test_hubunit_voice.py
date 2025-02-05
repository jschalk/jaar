from src.f00_instrument.file import open_file, save_file, delete_dir
from src.f01_road.road import get_default_fiscal_title as root_title
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_HubUnit_voice_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str, None)
    assert os_path_exists(sue_hubunit._voice_path) is False
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    save_file(
        dest_dir=sue_hubunit._voice_dir,
        file_name=sue_hubunit._voice_file_name,
        file_str=budunit_shop(sue_str).get_json(),
    )

    # THEN
    assert os_path_exists(sue_hubunit._voice_path)
    assert sue_hubunit.voice_file_exists()


def test_HubUnit_save_voice_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str, None)
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_bud = budunit_shop(sue_str)
    bob_str = "Bob"
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.save_voice_bud(sue_bud)

    # THEN
    assert sue_hubunit.voice_file_exists()

    voice_file_str = open_file(sue_hubunit._voice_dir, sue_hubunit._voice_file_name)
    print(f"{voice_file_str=}")
    voice_bud = budunit_get_from_json(voice_file_str)
    assert voice_bud.acct_exists(bob_str)

    # # WHEN
    sue2_bud = budunit_shop(sue_str)
    zia_str = "Zia"
    sue2_bud.add_acctunit(zia_str)
    sue_hubunit.save_voice_bud(sue2_bud)

    # THEN
    voice_file_str = open_file(sue_hubunit._voice_dir, sue_hubunit._voice_file_name)
    print(f"{voice_file_str=}")
    voice_bud = budunit_get_from_json(voice_file_str)
    assert voice_bud.acct_exists(zia_str)


def test_HubUnit_save_voice_file_RaisesErrorWhenBud_voice_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str, None)

    # WHEN / THEN
    yao_str = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_voice_bud(budunit_shop(yao_str))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_name '{yao_str}' cannot be saved as owner_name '{sue_str}''s voice bud."
    )


def test_HubUnit_initialize_voice_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str, None)
    sue_bud = budunit_shop(sue_str, root_title())
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit.initialize_voice_file(sue_bud)

    # THEN
    voice_bud = sue_hubunit.get_voice_bud()
    assert voice_bud.fiscal_title == root_title()
    assert voice_bud.owner_name == sue_str
    bob_str = "Bob"
    assert voice_bud.acct_exists(bob_str) is False

    # ESTABLISH
    sue_bud = budunit_shop(sue_str)
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.save_voice_bud(sue_bud)
    voice_bud = sue_hubunit.get_voice_bud()
    assert voice_bud.get_acct(bob_str)

    # WHEN
    sue_hubunit.initialize_voice_file(sue_bud)

    # THEN
    voice_bud = sue_hubunit.get_voice_bud()
    assert voice_bud.get_acct(bob_str)


def test_HubUnit_initialize_voice_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_fiscal_dir = f"{env_dir()}/{root_title()}"
    sue_fund_pool = 50000
    sue_fund_coin = 5
    sue_bit = 25
    sue_hubunit = hubunit_shop(
        env_dir(),
        root_title(),
        sue_str,
        None,
        fund_pool=sue_fund_pool,
        fund_coin=sue_fund_coin,
        respect_bit=sue_bit,
    )
    sue_bud = budunit_shop(
        sue_str,
        root_title(),
        fund_pool=sue_fund_pool,
        fund_coin=sue_fund_coin,
        respect_bit=sue_bit,
    )
    sue_hubunit.initialize_voice_file(sue_bud)
    assert sue_hubunit.voice_file_exists()
    delete_dir(sue_hubunit._voice_path)
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    bob_str = "Bob"
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.initialize_voice_file(sue_bud)

    # THEN
    assert sue_hubunit.voice_file_exists()

    sue_fiscal_dir = f"{env_dir()}/{root_title()}"
    sue_owners_dir = f"{sue_fiscal_dir}/owners"
    sue_owner_dir = f"{sue_owners_dir}/{sue_str}"
    sue_voice_dir = f"{sue_owner_dir}/voice"
    sue_voice_file_name = f"{sue_str}.json"
    voice_file_str = open_file(dest_dir=sue_voice_dir, file_name=sue_voice_file_name)
    print(f"{voice_file_str=}")
    voice_bud = budunit_get_from_json(voice_file_str)
    assert voice_bud.fiscal_title == root_title()
    assert voice_bud.owner_name == sue_str
    assert voice_bud.fund_pool == sue_fund_pool
    assert voice_bud.fund_coin == sue_fund_coin
    assert voice_bud.respect_bit == sue_bit


def test_HubUnit_initialize_voice_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str, None)
    delete_dir(sue_hubunit._fiscal_dir)
    assert os_path_exists(sue_hubunit._voice_path) is False

    # WHEN
    sue_bud = budunit_shop(sue_str, root_title())
    sue_hubunit.initialize_voice_file(sue_bud)

    # THEN
    assert os_path_exists(sue_hubunit._voice_path)
