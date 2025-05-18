from src.a01_way_logic.way import create_way
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.special_func import create_pledge
from copy import deepcopy as copy_deepcopy


def test_create_pledge_EqualBudWithEmptyParameters():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    old_sue_bud = copy_deepcopy(sue_bud)

    # WHEN
    empty_way = create_way("")
    create_pledge(x_bud=sue_bud, pledge_way=empty_way)

    # THEN
    assert sue_bud == old_sue_bud

    # WHEN
    create_pledge(x_bud=sue_bud, pledge_way=None)

    # THEN
    assert sue_bud == old_sue_bud


def test_create_pledge_CorrectlyAddspledgeToBud():
    # ESTABLISH
    sue_str = "Sue"
    new_sue_bud = budunit_shop(sue_str)
    old_sue_bud = copy_deepcopy(new_sue_bud)

    # WHEN
    clean_way = new_sue_bud.make_l1_way("clean")
    create_pledge(new_sue_bud, clean_way)

    # THEN
    assert new_sue_bud != old_sue_bud
    assert old_sue_bud.concept_exists(clean_way) is False
    assert new_sue_bud.concept_exists(clean_way)
    clean_concept = new_sue_bud.get_concept_obj(clean_way)
    assert clean_concept.pledge


def test_create_pledge_CorrectlyModifiesBudNonpledgeConceptTopledgeConcept():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    clean_str = "clean"
    clean_concept = conceptunit_shop(clean_str)
    clean_way = sue_bud.make_l1_way(clean_str)
    floor_str = "floor"
    floor_way = sue_bud.make_way(clean_way, floor_str)
    floor_concept = conceptunit_shop(floor_str, pledge=True)

    sue_bud.set_l1_concept(clean_concept)
    sue_bud.set_concept(floor_concept, clean_way)
    old_clean_concept = sue_bud.get_concept_obj(clean_way)
    old_floor_concept = sue_bud.get_concept_obj(floor_way)
    assert old_clean_concept.pledge is False
    assert old_floor_concept.pledge

    # WHEN
    create_pledge(sue_bud, clean_way)

    # THEN
    assert sue_bud.concept_exists(clean_way)
    assert sue_bud.concept_exists(floor_way)
    new_clean_concept = sue_bud.get_concept_obj(clean_way)
    new_floor_concept = sue_bud.get_concept_obj(floor_way)
    assert new_clean_concept.pledge
    assert new_floor_concept.pledge


def test_create_pledge_CorrectlySets_laborlink():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    clean_str = "clean"
    clean_way = sue_bud.make_l1_way(clean_str)
    floor_str = "floor"
    floor_way = sue_bud.make_way(clean_way, floor_str)
    bob_str = "Bob"
    floor_concept = conceptunit_shop(floor_str, pledge=True)
    floor_concept.laborunit.set_laborlink(bob_str)
    sue_bud.set_concept(floor_concept, clean_way)
    floor_concept = sue_bud.get_concept_obj(floor_way)
    assert floor_concept.laborunit.laborlink_exists(bob_str) is False

    # WHEN
    create_pledge(sue_bud, floor_way, bob_str)

    # THEN
    assert floor_concept.laborunit.laborlink_exists(bob_str)
    yao_str = "Yao"
    assert sue_bud.acct_exists(yao_str) is False
    assert floor_concept.laborunit.laborlink_exists(yao_str) is False

    # WHEN
    create_pledge(sue_bud, floor_way, yao_str)

    # THEN
    assert sue_bud.acct_exists(yao_str)
    assert floor_concept.laborunit.laborlink_exists(yao_str)
