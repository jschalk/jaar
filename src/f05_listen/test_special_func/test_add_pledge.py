from src.f01_road.road import get_default_fisc_title as root_title
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.special_func import add_voice_pledge, add_voice_fact
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_add_voice_pledge_Addspledgevow(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str)
    sue_hubunit.initialize_vow_voice_files()
    old_sue_voice = sue_hubunit.get_voice_bud()
    clean_str = "clean"
    clean_road = old_sue_voice.make_l1_road(clean_str)
    one_int = 1
    print(f"{sue_hubunit.vow_file_path(one_int)=}")
    assert sue_hubunit.vow_file_exists(one_int) is False
    old_sue_voice = sue_hubunit.get_voice_bud()
    assert old_sue_voice.item_exists(clean_road) is False

    # WHEN
    add_voice_pledge(sue_hubunit, clean_road)

    # THEN
    assert sue_hubunit.vow_file_exists(one_int)
    new_sue_voice = sue_hubunit.get_voice_bud()
    assert new_sue_voice.item_exists(clean_road)


def test_add_voice_pledge_SetsvoiceBudpledgeItem_teamlink(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str)
    sue_hubunit.initialize_vow_voice_files()
    old_sue_voice = sue_hubunit.get_voice_bud()
    clean_str = "clean"
    clean_road = old_sue_voice.make_l1_road(clean_str)
    assert old_sue_voice.item_exists(clean_road) is False

    # WHEN
    bob_str = "Bob"
    add_voice_pledge(sue_hubunit, clean_road, x_teamlink=bob_str)

    # THEN
    new_sue_voice = sue_hubunit.get_voice_bud()
    assert new_sue_voice.item_exists(clean_road)
    clean_item = new_sue_voice.get_item_obj(clean_road)
    print(f"{clean_item.teamunit._teamlinks=}")
    assert clean_item.teamunit.teamlink_exists(bob_str)


def test_add_voice_pledge_CanAdd_reasonunit(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str)
    sue_hubunit.initialize_vow_voice_files()
    old_sue_voice = sue_hubunit.get_voice_bud()
    clean_str = "clean"
    clean_road = old_sue_voice.make_l1_road(clean_str)
    house_estimation_str = "house_estimation"
    house_estimation_road = old_sue_voice.make_l1_road(house_estimation_str)
    dirty_str = "dirty"
    dirty_road = old_sue_voice.make_road(house_estimation_road, dirty_str)
    assert old_sue_voice.item_exists(dirty_road) is False

    # WHEN
    add_voice_pledge(sue_hubunit, clean_road, reason_premise=dirty_road)

    # THEN
    new_sue_voice = sue_hubunit.get_voice_bud()
    clean_item = new_sue_voice.get_item_obj(clean_road)
    print(f"{clean_item.reasonunits.keys()=}")
    assert clean_item.get_reasonunit(house_estimation_road) is not None
    house_reasonunit = clean_item.get_reasonunit(house_estimation_road)
    assert house_reasonunit.get_premise(dirty_road) is not None


def test_add_voice_fact_CanAdd_factunit(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_title(), sue_str)
    sue_hubunit.initialize_vow_voice_files()
    old_sue_voice = sue_hubunit.get_voice_bud()
    house_estimation_str = "house_estimation"
    house_estimation_road = old_sue_voice.make_l1_road(house_estimation_str)
    dirty_str = "dirty"
    dirty_road = old_sue_voice.make_road(house_estimation_road, dirty_str)
    assert old_sue_voice.item_exists(dirty_road) is False
    assert old_sue_voice.get_fact(dirty_road) is None

    # WHEN
    add_voice_fact(sue_hubunit, dirty_road)

    # THEN
    new_sue_voice = sue_hubunit.get_voice_bud()
    assert new_sue_voice.item_exists(dirty_road)
    assert new_sue_voice.get_fact(house_estimation_road) is not None
    assert new_sue_voice.get_fact(house_estimation_road).pick == dirty_road
