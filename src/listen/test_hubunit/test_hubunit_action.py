from src._instrument.file import open_file, save_file, delete_dir
from src._road.road import get_default_real_id_roadnode as root_label
from src.bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.listen.hubunit import hubunit_shop
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_HubUnit_action_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text, None)
    assert os_path_exists(sue_hubunit.action_path()) is False
    assert sue_hubunit.action_file_exists() is False

    # WHEN
    save_file(
        dest_dir=sue_hubunit.action_dir(),
        file_name=sue_hubunit.action_file_name(),
        file_text=budunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_hubunit.action_path())
    assert sue_hubunit.action_file_exists()


def test_HubUnit_save_action_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text, None)
    assert sue_hubunit.action_file_exists() is False

    # WHEN
    sue_bud = budunit_shop(sue_text)
    bob_text = "Bob"
    sue_bud.add_charunit(bob_text)
    sue_hubunit.save_action_bud(sue_bud)

    # THEN
    assert sue_hubunit.action_file_exists()

    action_file_text = open_file(
        sue_hubunit.action_dir(), sue_hubunit.action_file_name()
    )
    print(f"{action_file_text=}")
    action_bud = budunit_get_from_json(action_file_text)
    assert action_bud.char_exists(bob_text)

    # # WHEN
    sue2_bud = budunit_shop(sue_text)
    zia_text = "Zia"
    sue2_bud.add_charunit(zia_text)
    sue_hubunit.save_action_bud(sue2_bud)

    # THEN
    action_file_text = open_file(
        sue_hubunit.action_dir(), sue_hubunit.action_file_name()
    )
    print(f"{action_file_text=}")
    action_bud = budunit_get_from_json(action_file_text)
    assert action_bud.char_exists(zia_text)


def test_HubUnit_save_action_file_RaisesErrorWhenBud_action_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text, None)

    # WHEN / THEN
    yao_text = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_action_bud(budunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_id '{yao_text}' cannot be saved as owner_id '{sue_text}''s action bud."
    )


def test_HubUnit_initialize_action_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text, None)
    sue_bud = budunit_shop(sue_text, root_label())
    assert sue_hubunit.action_file_exists() is False

    # WHEN
    sue_hubunit.initialize_action_file(sue_bud)

    # THEN
    action_bud = sue_hubunit.get_action_bud()
    assert action_bud._real_id == root_label()
    assert action_bud._owner_id == sue_text
    bob_text = "Bob"
    assert action_bud.char_exists(bob_text) is False

    # ESTABLISH
    sue_bud = budunit_shop(sue_text)
    sue_bud.add_charunit(bob_text)
    sue_hubunit.save_action_bud(sue_bud)
    action_bud = sue_hubunit.get_action_bud()
    assert action_bud.get_char(bob_text)

    # WHEN
    sue_hubunit.initialize_action_file(sue_bud)

    # THEN
    action_bud = sue_hubunit.get_action_bud()
    assert action_bud.get_char(bob_text)


def test_HubUnit_initialize_action_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_fund_pool = 50000
    sue_fund_coin = 5
    sue_bit = 25
    sue_hubunit = hubunit_shop(
        env_dir(),
        root_label(),
        sue_text,
        None,
        fund_pool=sue_fund_pool,
        fund_coin=sue_fund_coin,
        bit=sue_bit,
    )
    sue_bud = budunit_shop(
        sue_text,
        root_label(),
        _fund_pool=sue_fund_pool,
        _fund_coin=sue_fund_coin,
        _bit=sue_bit,
    )
    sue_hubunit.initialize_action_file(sue_bud)
    assert sue_hubunit.action_file_exists()
    delete_dir(sue_hubunit.action_path())
    assert sue_hubunit.action_file_exists() is False

    # WHEN
    bob_text = "Bob"
    sue_bud.add_charunit(bob_text)
    sue_hubunit.initialize_action_file(sue_bud)

    # THEN
    assert sue_hubunit.action_file_exists()

    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_owners_dir = f"{sue_real_dir}/owners"
    sue_owner_dir = f"{sue_owners_dir}/{sue_text}"
    sue_action_dir = f"{sue_owner_dir}/action"
    sue_action_file_name = f"{sue_text}.json"
    action_file_text = open_file(
        dest_dir=sue_action_dir, file_name=sue_action_file_name
    )
    print(f"{action_file_text=}")
    action_bud = budunit_get_from_json(action_file_text)
    assert action_bud._real_id == root_label()
    assert action_bud._owner_id == sue_text
    assert action_bud._fund_pool == sue_fund_pool
    assert action_bud._fund_coin == sue_fund_coin
    assert action_bud._bit == sue_bit


def test_HubUnit_initialize_action_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text, None)
    delete_dir(sue_hubunit.real_dir())
    assert os_path_exists(sue_hubunit.action_path()) is False

    # WHEN
    sue_bud = budunit_shop(sue_text, root_label())
    sue_hubunit.initialize_action_file(sue_bud)

    # THEN
    assert os_path_exists(sue_hubunit.action_path())
