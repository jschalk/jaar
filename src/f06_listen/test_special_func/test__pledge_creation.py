from src.a01_word_logic.road import create_road
from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.f06_listen.special_func import create_pledge
from copy import deepcopy as copy_deepcopy


def test_create_pledge_EqualBudWithEmptyParameters():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    old_sue_bud = copy_deepcopy(sue_bud)

    # WHEN
    empty_road = create_road("")
    create_pledge(x_bud=sue_bud, pledge_road=empty_road)

    # THEN
    assert sue_bud == old_sue_bud

    # WHEN
    create_pledge(x_bud=sue_bud, pledge_road=None)

    # THEN
    assert sue_bud == old_sue_bud


def test_create_pledge_CorrectlyAddspledgeToBud():
    # ESTABLISH
    sue_str = "Sue"
    new_sue_bud = budunit_shop(sue_str)
    old_sue_bud = copy_deepcopy(new_sue_bud)

    # WHEN
    clean_road = new_sue_bud.make_l1_road("clean")
    create_pledge(new_sue_bud, clean_road)

    # THEN
    assert new_sue_bud != old_sue_bud
    assert old_sue_bud.item_exists(clean_road) is False
    assert new_sue_bud.item_exists(clean_road)
    clean_item = new_sue_bud.get_item_obj(clean_road)
    assert clean_item.pledge


def test_create_pledge_CorrectlyModifiesBudNonpledgeItemTopledgeItem():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    clean_str = "clean"
    clean_item = itemunit_shop(clean_str)
    clean_road = sue_bud.make_l1_road(clean_str)
    floor_str = "floor"
    floor_road = sue_bud.make_road(clean_road, floor_str)
    floor_item = itemunit_shop(floor_str, pledge=True)

    sue_bud.set_l1_item(clean_item)
    sue_bud.set_item(floor_item, clean_road)
    old_clean_item = sue_bud.get_item_obj(clean_road)
    old_floor_item = sue_bud.get_item_obj(floor_road)
    assert old_clean_item.pledge is False
    assert old_floor_item.pledge

    # WHEN
    create_pledge(sue_bud, clean_road)

    # THEN
    assert sue_bud.item_exists(clean_road)
    assert sue_bud.item_exists(floor_road)
    new_clean_item = sue_bud.get_item_obj(clean_road)
    new_floor_item = sue_bud.get_item_obj(floor_road)
    assert new_clean_item.pledge
    assert new_floor_item.pledge


def test_create_pledge_CorrectlySets_teamlink():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    clean_str = "clean"
    clean_road = sue_bud.make_l1_road(clean_str)
    floor_str = "floor"
    floor_road = sue_bud.make_road(clean_road, floor_str)
    bob_str = "Bob"
    floor_item = itemunit_shop(floor_str, pledge=True)
    floor_item.teamunit.set_teamlink(bob_str)
    sue_bud.set_item(floor_item, clean_road)
    floor_item = sue_bud.get_item_obj(floor_road)
    assert floor_item.teamunit.teamlink_exists(bob_str) is False

    # WHEN
    create_pledge(sue_bud, floor_road, bob_str)

    # THEN
    assert floor_item.teamunit.teamlink_exists(bob_str)
    yao_str = "Yao"
    assert sue_bud.acct_exists(yao_str) is False
    assert floor_item.teamunit.teamlink_exists(yao_str) is False

    # WHEN
    create_pledge(sue_bud, floor_road, yao_str)

    # THEN
    assert sue_bud.acct_exists(yao_str)
    assert floor_item.teamunit.teamlink_exists(yao_str)
