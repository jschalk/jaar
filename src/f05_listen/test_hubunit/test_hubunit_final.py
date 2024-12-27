from src.f00_instrument.file import open_file, save_file, delete_dir
from src.f01_road.road import get_default_deal_id_ideaunit as root_lx
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_HubUnit_final_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_lx(), sue_str, None)
    assert os_path_exists(sue_hubunit.final_path()) is False
    assert sue_hubunit.final_file_exists() is False

    # WHEN
    save_file(
        dest_dir=sue_hubunit.final_dir(),
        file_name=sue_hubunit.final_file_name(),
        file_str=budunit_shop(sue_str).get_json(),
    )

    # THEN
    assert os_path_exists(sue_hubunit.final_path())
    assert sue_hubunit.final_file_exists()


def test_HubUnit_save_final_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_lx(), sue_str, None)
    assert sue_hubunit.final_file_exists() is False

    # WHEN
    sue_bud = budunit_shop(sue_str)
    bob_str = "Bob"
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.save_final_bud(sue_bud)

    # THEN
    assert sue_hubunit.final_file_exists()

    final_file_str = open_file(sue_hubunit.final_dir(), sue_hubunit.final_file_name())
    print(f"{final_file_str=}")
    final_bud = budunit_get_from_json(final_file_str)
    assert final_bud.acct_exists(bob_str)

    # # WHEN
    sue2_bud = budunit_shop(sue_str)
    zia_str = "Zia"
    sue2_bud.add_acctunit(zia_str)
    sue_hubunit.save_final_bud(sue2_bud)

    # THEN
    final_file_str = open_file(sue_hubunit.final_dir(), sue_hubunit.final_file_name())
    print(f"{final_file_str=}")
    final_bud = budunit_get_from_json(final_file_str)
    assert final_bud.acct_exists(zia_str)


def test_HubUnit_save_final_file_RaisesErrorWhenBud_final_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_lx(), sue_str, None)

    # WHEN / THEN
    yao_str = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_final_bud(budunit_shop(yao_str))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_id '{yao_str}' cannot be saved as owner_id '{sue_str}''s final bud."
    )


def test_HubUnit_initialize_final_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_lx(), sue_str, None)
    sue_bud = budunit_shop(sue_str, root_lx())
    assert sue_hubunit.final_file_exists() is False

    # WHEN
    sue_hubunit.initialize_final_file(sue_bud)

    # THEN
    final_bud = sue_hubunit.get_final_bud()
    assert final_bud._deal_id == root_lx()
    assert final_bud._owner_id == sue_str
    bob_str = "Bob"
    assert final_bud.acct_exists(bob_str) is False

    # ESTABLISH
    sue_bud = budunit_shop(sue_str)
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.save_final_bud(sue_bud)
    final_bud = sue_hubunit.get_final_bud()
    assert final_bud.get_acct(bob_str)

    # WHEN
    sue_hubunit.initialize_final_file(sue_bud)

    # THEN
    final_bud = sue_hubunit.get_final_bud()
    assert final_bud.get_acct(bob_str)


def test_HubUnit_initialize_final_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_deal_dir = f"{env_dir()}/{root_lx()}"
    sue_fund_pool = 50000
    sue_fund_coin = 5
    sue_bit = 25
    sue_hubunit = hubunit_shop(
        env_dir(),
        root_lx(),
        sue_str,
        None,
        fund_pool=sue_fund_pool,
        fund_coin=sue_fund_coin,
        respect_bit=sue_bit,
    )
    sue_bud = budunit_shop(
        sue_str,
        root_lx(),
        fund_pool=sue_fund_pool,
        fund_coin=sue_fund_coin,
        respect_bit=sue_bit,
    )
    sue_hubunit.initialize_final_file(sue_bud)
    assert sue_hubunit.final_file_exists()
    delete_dir(sue_hubunit.final_path())
    assert sue_hubunit.final_file_exists() is False

    # WHEN
    bob_str = "Bob"
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.initialize_final_file(sue_bud)

    # THEN
    assert sue_hubunit.final_file_exists()

    sue_deal_dir = f"{env_dir()}/{root_lx()}"
    sue_owners_dir = f"{sue_deal_dir}/owners"
    sue_owner_dir = f"{sue_owners_dir}/{sue_str}"
    sue_final_dir = f"{sue_owner_dir}/final"
    sue_final_file_name = f"{sue_str}.json"
    final_file_str = open_file(dest_dir=sue_final_dir, file_name=sue_final_file_name)
    print(f"{final_file_str=}")
    final_bud = budunit_get_from_json(final_file_str)
    assert final_bud._deal_id == root_lx()
    assert final_bud._owner_id == sue_str
    assert final_bud.fund_pool == sue_fund_pool
    assert final_bud.fund_coin == sue_fund_coin
    assert final_bud.respect_bit == sue_bit


def test_HubUnit_initialize_final_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_lx(), sue_str, None)
    delete_dir(sue_hubunit.deal_dir())
    assert os_path_exists(sue_hubunit.final_path()) is False

    # WHEN
    sue_bud = budunit_shop(sue_str, root_lx())
    sue_hubunit.initialize_final_file(sue_bud)

    # THEN
    assert os_path_exists(sue_hubunit.final_path())
