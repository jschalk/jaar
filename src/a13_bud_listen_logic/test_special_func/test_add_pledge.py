from src.a01_road_logic.road import get_default_fisc_tag as root_tag
from src.a12_hub_tools.hub_tool import open_gut_file
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a12_hub_tools.special_func import add_gut_pledge, add_gut_fact
from src.a13_bud_listen_logic._utils.env_a13 import (
    get_module_temp_dir as env_dir,
    env_dir_setup_cleanup,
)


def test_add_gut_pledge_Addspledgepack(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_tag(), sue_str)
    sue_hubunit.initialize_pack_gut_files()
    old_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    clean_str = "clean"
    clean_road = old_sue_gut.make_l1_road(clean_str)
    one_int = 1
    print(f"{sue_hubunit.pack_file_path(one_int)=}")
    assert sue_hubunit.pack_file_exists(one_int) is False
    old_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    assert old_sue_gut.item_exists(clean_road) is False

    # WHEN
    add_gut_pledge(sue_hubunit, clean_road)

    # THEN
    assert sue_hubunit.pack_file_exists(one_int)
    new_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    assert new_sue_gut.item_exists(clean_road)


def test_add_gut_pledge_SetsgutBudpledgeItem_teamlink(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_tag(), sue_str)
    sue_hubunit.initialize_pack_gut_files()
    old_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    clean_str = "clean"
    clean_road = old_sue_gut.make_l1_road(clean_str)
    assert old_sue_gut.item_exists(clean_road) is False

    # WHEN
    bob_str = "Bob"
    add_gut_pledge(sue_hubunit, clean_road, x_teamlink=bob_str)

    # THEN
    new_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    assert new_sue_gut.item_exists(clean_road)
    clean_item = new_sue_gut.get_item_obj(clean_road)
    print(f"{clean_item.teamunit._teamlinks=}")
    assert clean_item.teamunit.teamlink_exists(bob_str)


def test_add_gut_pledge_CanAdd_reasonunit(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_tag(), sue_str)
    sue_hubunit.initialize_pack_gut_files()
    old_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    clean_str = "clean"
    clean_road = old_sue_gut.make_l1_road(clean_str)
    house_estimation_str = "house_estimation"
    house_estimation_road = old_sue_gut.make_l1_road(house_estimation_str)
    dirty_str = "dirty"
    dirty_road = old_sue_gut.make_road(house_estimation_road, dirty_str)
    assert old_sue_gut.item_exists(dirty_road) is False

    # WHEN
    add_gut_pledge(sue_hubunit, clean_road, reason_premise=dirty_road)

    # THEN
    new_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    clean_item = new_sue_gut.get_item_obj(clean_road)
    print(f"{clean_item.reasonunits.keys()=}")
    assert clean_item.get_reasonunit(house_estimation_road) is not None
    house_reasonunit = clean_item.get_reasonunit(house_estimation_road)
    assert house_reasonunit.get_premise(dirty_road) is not None


def test_add_gut_fact_CanAdd_factunit(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_tag(), sue_str)
    sue_hubunit.initialize_pack_gut_files()
    old_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    house_estimation_str = "house_estimation"
    house_estimation_road = old_sue_gut.make_l1_road(house_estimation_str)
    dirty_str = "dirty"
    dirty_road = old_sue_gut.make_road(house_estimation_road, dirty_str)
    assert old_sue_gut.item_exists(dirty_road) is False
    assert old_sue_gut.get_fact(dirty_road) is None

    # WHEN
    add_gut_fact(sue_hubunit, dirty_road)

    # THEN
    new_sue_gut = open_gut_file(env_dir(), root_tag(), sue_str)
    assert new_sue_gut.item_exists(dirty_road)
    assert new_sue_gut.get_fact(house_estimation_road) is not None
    assert new_sue_gut.get_fact(house_estimation_road).fneed == dirty_road
