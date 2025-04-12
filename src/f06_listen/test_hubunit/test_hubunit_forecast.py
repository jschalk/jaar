from src.f00_instrument.file import delete_dir, create_path
from src.f01_road.road import get_default_fisc_title as root_title
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f06_listen.hub_path import create_forecast_path
from src.f06_listen.hub_tool import (
    save_forecast_file,
    open_forecast_file,
    forecast_file_exists,
)
from src.f06_listen.hubunit import hubunit_shop
from src.f06_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_HubUnit_initialize_forecast_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str, None)
    sue_bud = budunit_shop(sue_str, root_title())
    assert forecast_file_exists(env_dir(), root_title(), sue_str) is False

    # WHEN
    sue_hubunit.initialize_forecast_file(sue_bud)

    # THEN
    forecast = open_forecast_file(env_dir(), root_title(), sue_str)
    assert forecast.fisc_title == root_title()
    assert forecast.owner_name == sue_str
    bob_str = "Bob"
    assert forecast.acct_exists(bob_str) is False

    # ESTABLISH
    sue_bud = budunit_shop(sue_str)
    sue_bud.add_acctunit(bob_str)
    save_forecast_file(env_dir(), sue_bud)
    forecast = open_forecast_file(env_dir(), root_title(), sue_str)
    assert forecast.get_acct(bob_str)

    # WHEN
    sue_hubunit.initialize_forecast_file(sue_bud)

    # THEN
    forecast = open_forecast_file(env_dir(), root_title(), sue_str)
    assert forecast.get_acct(bob_str)


def test_HubUnit_initialize_forecast_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    fisc_mstr_dir = env_dir()
    sue_fisc_dir = create_path(fisc_mstr_dir, root_title())
    sue_fund_pool = 50000
    sue_fund_coin = 5
    sue_bit = 25
    sue_hubunit = hubunit_shop(
        fisc_mstr_dir,
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
    sue_hubunit.initialize_forecast_file(sue_bud)
    assert forecast_file_exists(env_dir(), root_title(), sue_str)
    sue_forecast_path = create_forecast_path(env_dir(), root_title(), sue_str)
    delete_dir(sue_forecast_path)
    assert forecast_file_exists(env_dir(), root_title(), sue_str) is False

    # WHEN
    bob_str = "Bob"
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.initialize_forecast_file(sue_bud)

    # THEN
    assert forecast_file_exists(env_dir(), root_title(), sue_str)
    forecast = open_forecast_file(env_dir(), root_title(), sue_str)
    assert forecast.fisc_title == root_title()
    assert forecast.owner_name == sue_str
    assert forecast.fund_pool == sue_fund_pool
    assert forecast.fund_coin == sue_fund_coin
    assert forecast.respect_bit == sue_bit


def test_HubUnit_initialize_forecast_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str, None)
    delete_dir(sue_hubunit._fisc_dir)
    assert forecast_file_exists(env_dir(), root_title(), sue_str) is False

    # WHEN
    sue_bud = budunit_shop(sue_str, root_title())
    sue_hubunit.initialize_forecast_file(sue_bud)

    # THEN
    assert forecast_file_exists(env_dir(), root_title(), sue_str)
