from src._instrument.file import delete_dir
from src._road.jaar_config import init_gift_id, get_test_real_id as real_id
from src.listen.hubunit import hubunit_shop
from src.listen.examples.example_listen_gifts import sue_2atomunits_giftunit
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_HubUnit_default_voice_world_ReturnsCorrectObj():
    # ESTABLISH
    sue_text = "Sue"
    slash_text = "/"
    x_bud_pool = 9000000
    point_nine_float = 0.9
    point_five_float = 0.5
    point_four_float = 0.4
    sue_hubunit = hubunit_shop(
        env_dir(),
        real_id(),
        sue_text,
        econ_road=None,
        road_delimiter=slash_text,
        bud_pool=x_bud_pool,
        bud_coin=point_five_float,
        bit=point_five_float,
        penny=point_four_float,
    )

    # WHEN
    sue_default_voice = sue_hubunit.default_voice_world()

    # THEN
    assert sue_default_voice._real_id == sue_hubunit.real_id
    assert sue_default_voice._owner_id == sue_hubunit.owner_id
    assert sue_default_voice._road_delimiter == sue_hubunit.road_delimiter
    assert sue_default_voice._bud_pool == sue_hubunit.bud_pool
    assert sue_default_voice._bud_coin == sue_hubunit.bud_coin
    assert sue_default_voice._bit == sue_hubunit.bit
    assert sue_default_voice._penny == sue_hubunit.penny


def test_HubUnit_delete_voice_file_DeletesvoiceFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    sue_hubunit.save_voice_world(sue_hubunit.default_voice_world())
    assert sue_hubunit.voice_file_exists()

    # WHEN
    sue_hubunit.delete_voice_file()

    # THEN
    assert sue_hubunit.voice_file_exists() is False


def test_HubUnit_create_initial_gift_files_from_default_CorrectlySavesGiftUnitFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_gift_files_from_default()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.voice_file_exists() is False


def test_HubUnit_create_voice_from_gifts_CreatesvoiceFileFromGiftFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    sue_hubunit._create_initial_gift_files_from_default()
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit._create_voice_from_gifts()

    # THEN
    assert sue_hubunit.voice_file_exists()
    static_sue_voice = sue_hubunit._merge_any_gifts(sue_hubunit.default_voice_world())
    assert sue_hubunit.get_voice_world().get_dict() == static_sue_voice.get_dict()


def test_HubUnit_create_initial_gift_and_voice_files_CreatesGiftFilesAndvoiceFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_gift_and_voice_files()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.voice_file_exists()
    static_sue_voice = sue_hubunit._merge_any_gifts(sue_hubunit.default_voice_world())
    assert sue_hubunit.get_voice_world().get_dict() == static_sue_voice.get_dict()


def test_HubUnit_create_initial_gift_files_from_voice_SavesOnlyGiftFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    sue_voice_world = sue_hubunit.default_voice_world()
    bob_text = "Bob"
    sue_voice_world.add_charunit(bob_text)
    assert sue_hubunit.voice_file_exists() is False
    sue_hubunit.save_voice_world(sue_voice_world)
    assert sue_hubunit.voice_file_exists()
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit._create_initial_gift_files_from_voice()

    # THEN
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_voice_files_CorrectlySavesvoiceFileAndGiftFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, bit=seven_int)
    assert sue_hubunit.voice_file_exists() is False
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_hubunit.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit.initialize_gift_voice_files()

    # THEN
    voice_world = sue_hubunit.get_voice_world()
    assert voice_world._real_id == real_id()
    assert voice_world._owner_id == sue_text
    assert voice_world._bit == seven_int
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_voice_files_CorrectlySavesOnlyvoiceFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, bit=seven_int)
    sue_hubunit.initialize_gift_voice_files()
    assert sue_hubunit.voice_file_exists()
    sue_hubunit.delete_voice_file()
    assert sue_hubunit.voice_file_exists() is False
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path)

    # WHEN
    sue_hubunit.initialize_gift_voice_files()

    # THEN
    voice_world = sue_hubunit.get_voice_world()
    assert voice_world._real_id == real_id()
    assert voice_world._owner_id == sue_text
    assert voice_world._bit == seven_int
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_voice_files_CorrectlySavesOnlygiftFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, bit=seven_int)
    sue_hubunit.initialize_gift_voice_files()
    sue_voice_world = sue_hubunit.get_voice_world()
    bob_text = "Bob"
    sue_voice_world.add_charunit(bob_text)
    sue_hubunit.save_voice_world(sue_voice_world)
    assert sue_hubunit.voice_file_exists()
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_hubunit.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit.initialize_gift_voice_files()

    # THEN
    assert sue_voice_world._real_id == real_id()
    assert sue_voice_world._owner_id == sue_text
    assert sue_voice_world._bit == seven_int
    assert sue_voice_world.char_exists(bob_text)
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_append_gifts_to_voice_file_AddsgiftsTovoiceFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    sue_hubunit.initialize_gift_voice_files()
    sue_hubunit.save_gift_file(sue_2atomunits_giftunit())
    voice_world = sue_hubunit.get_voice_world()
    print(f"{voice_world._real_id=}")
    sports_text = "sports"
    sports_road = voice_world.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = voice_world.make_road(sports_road, knee_text)
    assert voice_world.idea_exists(sports_road) is False
    assert voice_world.idea_exists(knee_road) is False

    # WHEN
    new_world = sue_hubunit.append_gifts_to_voice_file()

    # THEN
    assert new_world != voice_world
    assert new_world.idea_exists(sports_road)
    assert new_world.idea_exists(knee_road)
