from src.f00_instrument.file_toolbox import delete_dir, create_path
from src.f04_pack.pack import init_pack_id
from src.f06_listen.hub_tool import create_gut_path
from src.f06_listen.hub_tool import save_gut_file, open_gut_file, gut_file_exists
from src.f06_listen.hubunit import hubunit_shop
from src.f06_listen.examples.example_listen_packs import sue_2budatoms_packunit
from src.f06_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_HubUnit_default_gut_bud_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    slash_str = "/"
    x_fund_pool = 9000000
    pnine_float = 0.9
    pfour_float = 0.4
    sue_hubunit = hubunit_shop(
        env_dir(),
        "accord23",
        sue_str,
        keep_road=None,
        bridge=slash_str,
        fund_pool=x_fund_pool,
        fund_coin=pnine_float,
        respect_bit=pnine_float,
        penny=pfour_float,
    )

    # WHEN
    sue_default_gut = sue_hubunit.default_gut_bud()

    # THEN
    assert sue_default_gut.fisc_title == sue_hubunit.fisc_title
    assert sue_default_gut.owner_name == sue_hubunit.owner_name
    assert sue_default_gut.bridge == sue_hubunit.bridge
    assert sue_default_gut.fund_pool == sue_hubunit.fund_pool
    assert sue_default_gut.fund_coin == sue_hubunit.fund_coin
    assert sue_default_gut.respect_bit == sue_hubunit.respect_bit
    assert sue_default_gut.penny == sue_hubunit.penny
    assert sue_default_gut.last_pack_id == init_pack_id()


def test_HubUnit_create_initial_pack_files_from_default_CorrectlySavesPackUnitFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    init_pack_filename = sue_hubunit.pack_filename(init_pack_id())
    init_pack_file_path = create_path(sue_hubunit._packs_dir, init_pack_filename)
    assert os_path_exists(init_pack_file_path) is False
    assert gut_file_exists(env_dir(), "accord23", sue_str) is False

    # WHEN
    sue_hubunit._create_initial_pack_files_from_default()

    # THEN
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "accord23", sue_str) is False


def test_HubUnit_create_gut_from_packs_CreatesgutFileFrompackFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    init_pack_filename = sue_hubunit.pack_filename(init_pack_id())
    init_pack_file_path = create_path(sue_hubunit._packs_dir, init_pack_filename)
    sue_hubunit._create_initial_pack_files_from_default()
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "accord23", sue_str) is False

    # WHEN
    sue_hubunit._create_gut_from_packs()

    # THEN
    assert gut_file_exists(env_dir(), "accord23", sue_str)
    static_sue_gut = sue_hubunit._merge_any_packs(sue_hubunit.default_gut_bud())
    gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    assert gut_bud.get_dict() == static_sue_gut.get_dict()


def test_HubUnit_create_initial_pack_and_gut_files_CreatespackFilesAndgutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    init_pack_filename = sue_hubunit.pack_filename(init_pack_id())
    init_pack_file_path = create_path(sue_hubunit._packs_dir, init_pack_filename)
    assert os_path_exists(init_pack_file_path) is False
    assert gut_file_exists(env_dir(), "accord23", sue_str) is False

    # WHEN
    sue_hubunit._create_initial_pack_and_gut_files()

    # THEN
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "accord23", sue_str)
    static_sue_gut = sue_hubunit._merge_any_packs(sue_hubunit.default_gut_bud())
    gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    assert gut_bud.get_dict() == static_sue_gut.get_dict()


def test_HubUnit_create_initial_pack_files_from_gut_SavesOnlypackFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    sue_gut_bud = sue_hubunit.default_gut_bud()
    bob_str = "Bob"
    sue_gut_bud.add_acctunit(bob_str)
    assert gut_file_exists(env_dir(), "accord23", sue_str) is False
    save_gut_file(env_dir(), sue_gut_bud)
    assert gut_file_exists(env_dir(), "accord23", sue_str)
    init_pack_file_path = create_path(sue_hubunit._packs_dir, f"{init_pack_id()}.json")
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_hubunit._create_initial_pack_files_from_gut()

    # THEN
    assert os_path_exists(init_pack_file_path)


def test_HubUnit_initialize_pack_gut_files_CorrectlySavesgutFileAndpackFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str, respect_bit=seven_int)
    assert gut_file_exists(env_dir(), "accord23", sue_str) is False
    init_pack_file_path = create_path(sue_hubunit._packs_dir, f"{init_pack_id()}.json")
    delete_dir(sue_hubunit._packs_dir)
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_hubunit.initialize_pack_gut_files()

    # THEN
    gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    assert gut_bud.fisc_title == "accord23"
    assert gut_bud.owner_name == sue_str
    assert gut_bud.respect_bit == seven_int
    assert os_path_exists(init_pack_file_path)


def test_HubUnit_initialize_pack_gut_files_CorrectlySavesOnlygutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str, respect_bit=seven_int)
    sue_hubunit.initialize_pack_gut_files()
    assert gut_file_exists(env_dir(), "accord23", sue_str)
    gut_path = create_gut_path(env_dir(), "accord23", sue_str)
    delete_dir(gut_path)
    assert gut_file_exists(env_dir(), "accord23", sue_str) is False
    init_pack_file_path = create_path(sue_hubunit._packs_dir, f"{init_pack_id()}.json")
    assert os_path_exists(init_pack_file_path)

    # WHEN
    sue_hubunit.initialize_pack_gut_files()

    # THEN
    gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    assert gut_bud.fisc_title == "accord23"
    assert gut_bud.owner_name == sue_str
    assert gut_bud.respect_bit == seven_int
    assert os_path_exists(init_pack_file_path)


def test_HubUnit_initialize_pack_gut_files_CorrectlySavesOnlypackFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str, respect_bit=seven_int)
    sue_hubunit.initialize_pack_gut_files()
    sue_gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    bob_str = "Bob"
    sue_gut_bud.add_acctunit(bob_str)
    save_gut_file(env_dir(), sue_gut_bud)
    assert gut_file_exists(env_dir(), "accord23", sue_str)
    init_pack_file_path = create_path(sue_hubunit._packs_dir, f"{init_pack_id()}.json")
    delete_dir(sue_hubunit._packs_dir)
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_hubunit.initialize_pack_gut_files()

    # THEN
    assert sue_gut_bud.fisc_title == "accord23"
    assert sue_gut_bud.owner_name == sue_str
    assert sue_gut_bud.respect_bit == seven_int
    assert sue_gut_bud.acct_exists(bob_str)
    assert os_path_exists(init_pack_file_path)


def test_HubUnit_append_packs_to_gut_file_AddspacksTogutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    sue_hubunit.initialize_pack_gut_files()
    sue_hubunit.save_pack_file(sue_2budatoms_packunit())
    gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    print(f"{gut_bud.fisc_title=}")
    sports_str = "sports"
    sports_road = gut_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = gut_bud.make_road(sports_road, knee_str)
    assert gut_bud.item_exists(sports_road) is False
    assert gut_bud.item_exists(knee_road) is False

    # WHEN
    new_bud = sue_hubunit.append_packs_to_gut_file()

    # THEN
    assert new_bud != gut_bud
    assert new_bud.item_exists(sports_road)
    assert new_bud.item_exists(knee_road)
