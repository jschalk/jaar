from src.f00_instrument.file import delete_dir
from src.f01_road.jaar_config import init_gift_id, get_test_fiscal_title as fiscal_title
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.example_listen_gifts import sue_2atomunits_giftunit
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_HubUnit_default_soul_bud_ReturnsCorrectObj():
    # ESTABLISH
    sue_str = "Sue"
    slash_str = "/"
    x_fund_pool = 9000000
    pnine_float = 0.9
    pfour_float = 0.4
    sue_hubunit = hubunit_shop(
        env_dir(),
        fiscal_title(),
        sue_str,
        keep_road=None,
        bridge=slash_str,
        fund_pool=x_fund_pool,
        fund_coin=pnine_float,
        respect_bit=pnine_float,
        penny=pfour_float,
    )

    # WHEN
    sue_default_soul = sue_hubunit.default_soul_bud()

    # THEN
    assert sue_default_soul.fiscal_title == sue_hubunit.fiscal_title
    assert sue_default_soul.owner_name == sue_hubunit.owner_name
    assert sue_default_soul.bridge == sue_hubunit.bridge
    assert sue_default_soul.fund_pool == sue_hubunit.fund_pool
    assert sue_default_soul.fund_coin == sue_hubunit.fund_coin
    assert sue_default_soul.respect_bit == sue_hubunit.respect_bit
    assert sue_default_soul.penny == sue_hubunit.penny


def test_HubUnit_delete_soul_file_DeletessoulFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title(), sue_str)
    sue_hubunit.save_soul_bud(sue_hubunit.default_soul_bud())
    assert sue_hubunit.soul_file_exists()

    # WHEN
    sue_hubunit.delete_soul_file()

    # THEN
    assert sue_hubunit.soul_file_exists() is False


def test_HubUnit_create_initial_gift_files_from_default_CorrectlySavesGiftUnitFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title(), sue_str)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_hubunit.soul_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_gift_files_from_default()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.soul_file_exists() is False


def test_HubUnit_create_soul_from_gifts_CreatessoulFileFromGiftFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title(), sue_str)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    sue_hubunit._create_initial_gift_files_from_default()
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.soul_file_exists() is False

    # WHEN
    sue_hubunit._create_soul_from_gifts()

    # THEN
    assert sue_hubunit.soul_file_exists()
    static_sue_soul = sue_hubunit._merge_any_gifts(sue_hubunit.default_soul_bud())
    assert sue_hubunit.get_soul_bud().get_dict() == static_sue_soul.get_dict()


def test_HubUnit_create_initial_gift_and_soul_files_CreatesGiftFilesAndsoulFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title(), sue_str)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_hubunit.soul_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_gift_and_soul_files()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.soul_file_exists()
    static_sue_soul = sue_hubunit._merge_any_gifts(sue_hubunit.default_soul_bud())
    assert sue_hubunit.get_soul_bud().get_dict() == static_sue_soul.get_dict()


def test_HubUnit_create_initial_gift_files_from_soul_SavesOnlyGiftFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title(), sue_str)
    sue_soul_bud = sue_hubunit.default_soul_bud()
    bob_str = "Bob"
    sue_soul_bud.add_acctunit(bob_str)
    assert sue_hubunit.soul_file_exists() is False
    sue_hubunit.save_soul_bud(sue_soul_bud)
    assert sue_hubunit.soul_file_exists()
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit._create_initial_gift_files_from_soul()

    # THEN
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_soul_files_CorrectlySavessoulFileAndGiftFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(
        env_dir(), fiscal_title(), sue_str, respect_bit=seven_int
    )
    assert sue_hubunit.soul_file_exists() is False
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_hubunit.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit.initialize_gift_soul_files()

    # THEN
    soul_bud = sue_hubunit.get_soul_bud()
    assert soul_bud.fiscal_title == fiscal_title()
    assert soul_bud.owner_name == sue_str
    assert soul_bud.respect_bit == seven_int
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_soul_files_CorrectlySavesOnlysoulFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(
        env_dir(), fiscal_title(), sue_str, respect_bit=seven_int
    )
    sue_hubunit.initialize_gift_soul_files()
    assert sue_hubunit.soul_file_exists()
    sue_hubunit.delete_soul_file()
    assert sue_hubunit.soul_file_exists() is False
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path)

    # WHEN
    sue_hubunit.initialize_gift_soul_files()

    # THEN
    soul_bud = sue_hubunit.get_soul_bud()
    assert soul_bud.fiscal_title == fiscal_title()
    assert soul_bud.owner_name == sue_str
    assert soul_bud.respect_bit == seven_int
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_soul_files_CorrectlySavesOnlygiftFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(
        env_dir(), fiscal_title(), sue_str, respect_bit=seven_int
    )
    sue_hubunit.initialize_gift_soul_files()
    sue_soul_bud = sue_hubunit.get_soul_bud()
    bob_str = "Bob"
    sue_soul_bud.add_acctunit(bob_str)
    sue_hubunit.save_soul_bud(sue_soul_bud)
    assert sue_hubunit.soul_file_exists()
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_hubunit.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit.initialize_gift_soul_files()

    # THEN
    assert sue_soul_bud.fiscal_title == fiscal_title()
    assert sue_soul_bud.owner_name == sue_str
    assert sue_soul_bud.respect_bit == seven_int
    assert sue_soul_bud.acct_exists(bob_str)
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_append_gifts_to_soul_file_AddsgiftsTosoulFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fiscal_title(), sue_str)
    sue_hubunit.initialize_gift_soul_files()
    sue_hubunit.save_gift_file(sue_2atomunits_giftunit())
    soul_bud = sue_hubunit.get_soul_bud()
    print(f"{soul_bud.fiscal_title=}")
    sports_str = "sports"
    sports_road = soul_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = soul_bud.make_road(sports_road, knee_str)
    assert soul_bud.item_exists(sports_road) is False
    assert soul_bud.item_exists(knee_road) is False

    # WHEN
    new_bud = sue_hubunit.append_gifts_to_soul_file()

    # THEN
    assert new_bud != soul_bud
    assert new_bud.item_exists(sports_road)
    assert new_bud.item_exists(knee_road)
