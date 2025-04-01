from src.f00_instrument.file import delete_dir, create_path
from src.f01_road.jaar_config import init_vow_id, get_test_fisc_title as fisc_title
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.example_listen_vows import sue_2budatoms_vowunit
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_HubUnit_default_voice_bud_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    slash_str = "/"
    x_fund_pool = 9000000
    pnine_float = 0.9
    pfour_float = 0.4
    sue_hubunit = hubunit_shop(
        env_dir(),
        fisc_title(),
        sue_str,
        keep_road=None,
        bridge=slash_str,
        fund_pool=x_fund_pool,
        fund_coin=pnine_float,
        respect_bit=pnine_float,
        penny=pfour_float,
    )

    # WHEN
    sue_default_voice = sue_hubunit.default_voice_bud()

    # THEN
    assert sue_default_voice.fisc_title == sue_hubunit.fisc_title
    assert sue_default_voice.owner_name == sue_hubunit.owner_name
    assert sue_default_voice.bridge == sue_hubunit.bridge
    assert sue_default_voice.fund_pool == sue_hubunit.fund_pool
    assert sue_default_voice.fund_coin == sue_hubunit.fund_coin
    assert sue_default_voice.respect_bit == sue_hubunit.respect_bit
    assert sue_default_voice.penny == sue_hubunit.penny
    assert sue_default_voice.last_vow_id == init_vow_id()


def test_HubUnit_delete_voice_file_DeletesvoiceFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    assert sue_hubunit.voice_file_exists()

    # WHEN
    sue_hubunit.delete_voice_file()

    # THEN
    assert sue_hubunit.voice_file_exists() is False


def test_HubUnit_create_initial_vow_files_from_default_CorrectlySavesvowUnitFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    init_vow_filename = sue_hubunit.vow_filename(init_vow_id())
    init_vow_file_path = create_path(sue_hubunit._vows_dir, init_vow_filename)
    assert os_path_exists(init_vow_file_path) is False
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_vow_files_from_default()

    # THEN
    assert os_path_exists(init_vow_file_path)
    assert sue_hubunit.voice_file_exists() is False


def test_HubUnit_create_voice_from_vows_CreatesvoiceFileFromvowFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    init_vow_filename = sue_hubunit.vow_filename(init_vow_id())
    init_vow_file_path = create_path(sue_hubunit._vows_dir, init_vow_filename)
    sue_hubunit._create_initial_vow_files_from_default()
    assert os_path_exists(init_vow_file_path)
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit._create_voice_from_vows()

    # THEN
    assert sue_hubunit.voice_file_exists()
    static_sue_voice = sue_hubunit._merge_any_vows(sue_hubunit.default_voice_bud())
    assert sue_hubunit.get_voice_bud().get_dict() == static_sue_voice.get_dict()


def test_HubUnit_create_initial_vow_and_voice_files_CreatesvowFilesAndvoiceFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    init_vow_filename = sue_hubunit.vow_filename(init_vow_id())
    init_vow_file_path = create_path(sue_hubunit._vows_dir, init_vow_filename)
    assert os_path_exists(init_vow_file_path) is False
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_vow_and_voice_files()

    # THEN
    assert os_path_exists(init_vow_file_path)
    assert sue_hubunit.voice_file_exists()
    static_sue_voice = sue_hubunit._merge_any_vows(sue_hubunit.default_voice_bud())
    assert sue_hubunit.get_voice_bud().get_dict() == static_sue_voice.get_dict()


def test_HubUnit_create_initial_vow_files_from_voice_SavesOnlyvowFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_voice_bud = sue_hubunit.default_voice_bud()
    bob_str = "Bob"
    sue_voice_bud.add_acctunit(bob_str)
    assert sue_hubunit.voice_file_exists() is False
    sue_hubunit.save_voice_bud(sue_voice_bud)
    assert sue_hubunit.voice_file_exists()
    init_vow_file_path = create_path(sue_hubunit._vows_dir, f"{init_vow_id()}.json")
    assert os_path_exists(init_vow_file_path) is False

    # WHEN
    sue_hubunit._create_initial_vow_files_from_voice()

    # THEN
    assert os_path_exists(init_vow_file_path)


def test_HubUnit_initialize_vow_voice_files_CorrectlySavesvoiceFileAndvowFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str, respect_bit=seven_int)
    assert sue_hubunit.voice_file_exists() is False
    init_vow_file_path = create_path(sue_hubunit._vows_dir, f"{init_vow_id()}.json")
    delete_dir(sue_hubunit._vows_dir)
    assert os_path_exists(init_vow_file_path) is False

    # WHEN
    sue_hubunit.initialize_vow_voice_files()

    # THEN
    voice_bud = sue_hubunit.get_voice_bud()
    assert voice_bud.fisc_title == fisc_title()
    assert voice_bud.owner_name == sue_str
    assert voice_bud.respect_bit == seven_int
    assert os_path_exists(init_vow_file_path)


def test_HubUnit_initialize_vow_voice_files_CorrectlySavesOnlyvoiceFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str, respect_bit=seven_int)
    sue_hubunit.initialize_vow_voice_files()
    assert sue_hubunit.voice_file_exists()
    sue_hubunit.delete_voice_file()
    assert sue_hubunit.voice_file_exists() is False
    init_vow_file_path = create_path(sue_hubunit._vows_dir, f"{init_vow_id()}.json")
    assert os_path_exists(init_vow_file_path)

    # WHEN
    sue_hubunit.initialize_vow_voice_files()

    # THEN
    voice_bud = sue_hubunit.get_voice_bud()
    assert voice_bud.fisc_title == fisc_title()
    assert voice_bud.owner_name == sue_str
    assert voice_bud.respect_bit == seven_int
    assert os_path_exists(init_vow_file_path)


def test_HubUnit_initialize_vow_voice_files_CorrectlySavesOnlyvowFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str, respect_bit=seven_int)
    sue_hubunit.initialize_vow_voice_files()
    sue_voice_bud = sue_hubunit.get_voice_bud()
    bob_str = "Bob"
    sue_voice_bud.add_acctunit(bob_str)
    sue_hubunit.save_voice_bud(sue_voice_bud)
    assert sue_hubunit.voice_file_exists()
    init_vow_file_path = create_path(sue_hubunit._vows_dir, f"{init_vow_id()}.json")
    delete_dir(sue_hubunit._vows_dir)
    assert os_path_exists(init_vow_file_path) is False

    # WHEN
    sue_hubunit.initialize_vow_voice_files()

    # THEN
    assert sue_voice_bud.fisc_title == fisc_title()
    assert sue_voice_bud.owner_name == sue_str
    assert sue_voice_bud.respect_bit == seven_int
    assert sue_voice_bud.acct_exists(bob_str)
    assert os_path_exists(init_vow_file_path)


def test_HubUnit_append_vows_to_voice_file_AddsvowsTovoiceFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.initialize_vow_voice_files()
    sue_hubunit.save_vow_file(sue_2budatoms_vowunit())
    voice_bud = sue_hubunit.get_voice_bud()
    print(f"{voice_bud.fisc_title=}")
    sports_str = "sports"
    sports_road = voice_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = voice_bud.make_road(sports_road, knee_str)
    assert voice_bud.item_exists(sports_road) is False
    assert voice_bud.item_exists(knee_road) is False

    # WHEN
    new_bud = sue_hubunit.append_vows_to_voice_file()

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)
    assert new_bud.item_exists(knee_road)
