from src.a01_way_logic.way import get_default_fisc_word as root_word
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
    sue_hubunit = hubunit_shop(env_dir(), root_word(), sue_str)
    sue_hubunit.initialize_pack_gut_files()
    old_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    clean_str = "clean"
    clean_way = old_sue_gut.make_l1_way(clean_str)
    one_int = 1
    print(f"{sue_hubunit.pack_file_path(one_int)=}")
    assert sue_hubunit.pack_file_exists(one_int) is False
    old_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    assert old_sue_gut.idea_exists(clean_way) is False

    # WHEN
    add_gut_pledge(sue_hubunit, clean_way)

    # THEN
    assert sue_hubunit.pack_file_exists(one_int)
    new_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    assert new_sue_gut.idea_exists(clean_way)


def test_add_gut_pledge_SetsgutBudpledgeIdea_laborlink(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_word(), sue_str)
    sue_hubunit.initialize_pack_gut_files()
    old_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    clean_str = "clean"
    clean_way = old_sue_gut.make_l1_way(clean_str)
    assert old_sue_gut.idea_exists(clean_way) is False

    # WHEN
    bob_str = "Bob"
    add_gut_pledge(sue_hubunit, clean_way, x_laborlink=bob_str)

    # THEN
    new_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    assert new_sue_gut.idea_exists(clean_way)
    clean_idea = new_sue_gut.get_idea_obj(clean_way)
    print(f"{clean_idea.laborunit._laborlinks=}")
    assert clean_idea.laborunit.laborlink_exists(bob_str)


def test_add_gut_pledge_CanAdd_reasonunit(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_word(), sue_str)
    sue_hubunit.initialize_pack_gut_files()
    old_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    clean_str = "clean"
    clean_way = old_sue_gut.make_l1_way(clean_str)
    house_estimation_str = "house_estimation"
    house_estimation_way = old_sue_gut.make_l1_way(house_estimation_str)
    dirty_str = "dirty"
    dirty_way = old_sue_gut.make_way(house_estimation_way, dirty_str)
    assert old_sue_gut.idea_exists(dirty_way) is False

    # WHEN
    add_gut_pledge(sue_hubunit, clean_way, reason_premise=dirty_way)

    # THEN
    new_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    clean_idea = new_sue_gut.get_idea_obj(clean_way)
    print(f"{clean_idea.reasonunits.keys()=}")
    assert clean_idea.get_reasonunit(house_estimation_way) is not None
    house_reasonunit = clean_idea.get_reasonunit(house_estimation_way)
    assert house_reasonunit.get_premise(dirty_way) is not None


def test_add_gut_fact_CanAdd_factunit(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_word(), sue_str)
    sue_hubunit.initialize_pack_gut_files()
    old_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    house_estimation_str = "house_estimation"
    house_estimation_way = old_sue_gut.make_l1_way(house_estimation_str)
    dirty_str = "dirty"
    dirty_way = old_sue_gut.make_way(house_estimation_way, dirty_str)
    assert old_sue_gut.idea_exists(dirty_way) is False
    assert old_sue_gut.get_fact(dirty_way) is None

    # WHEN
    add_gut_fact(sue_hubunit, dirty_way)

    # THEN
    new_sue_gut = open_gut_file(env_dir(), root_word(), sue_str)
    assert new_sue_gut.idea_exists(dirty_way)
    assert new_sue_gut.get_fact(house_estimation_way) is not None
    assert new_sue_gut.get_fact(house_estimation_way).fbranch == dirty_way
