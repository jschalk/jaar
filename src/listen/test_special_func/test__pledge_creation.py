from src._road.road import create_road
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.listen.special_func import create_pledge
from copy import deepcopy as copy_deepcopy


def test_create_pledge_EqualWorldWithEmptyParameters():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    old_sue_world = copy_deepcopy(sue_world)

    # WHEN
    empty_road = create_road("")
    create_pledge(x_world=sue_world, pledge_road=empty_road)

    # THEN
    assert sue_world == old_sue_world

    # WHEN
    create_pledge(x_world=sue_world, pledge_road=None)

    # THEN
    assert sue_world == old_sue_world


def test_create_pledge_CorrectlyAddspledgeToWorld():
    # GIVEN
    sue_text = "Sue"
    new_sue_world = worldunit_shop(sue_text)
    old_sue_world = copy_deepcopy(new_sue_world)

    # WHEN
    clean_road = new_sue_world.make_l1_road("clean")
    create_pledge(new_sue_world, clean_road)

    # THEN
    assert new_sue_world != old_sue_world
    assert old_sue_world.idea_exists(clean_road) is False
    assert new_sue_world.idea_exists(clean_road)
    clean_idea = new_sue_world.get_idea_obj(clean_road)
    assert clean_idea.pledge


def test_create_pledge_CorrectlyModifiesWorldNonpledgeIdeaTopledgeIdea():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    clean_road = sue_world.make_l1_road(clean_text)
    floor_text = "floor"
    floor_road = sue_world.make_road(clean_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, pledge=True)

    sue_world.add_l1_idea(clean_idea)
    sue_world.add_idea(floor_idea, clean_road)
    old_clean_idea = sue_world.get_idea_obj(clean_road)
    old_floor_idea = sue_world.get_idea_obj(floor_road)
    assert old_clean_idea.pledge is False
    assert old_floor_idea.pledge

    # WHEN
    create_pledge(sue_world, clean_road)

    # THEN
    assert sue_world.idea_exists(clean_road)
    assert sue_world.idea_exists(floor_road)
    new_clean_idea = sue_world.get_idea_obj(clean_road)
    new_floor_idea = sue_world.get_idea_obj(floor_road)
    assert new_clean_idea.pledge
    assert new_floor_idea.pledge


def test_create_pledge_CorrectlySets_belieflink():
    # GIVEN
    sue_text = "Sue"
    sue_world = worldunit_shop(sue_text)
    clean_text = "clean"
    clean_road = sue_world.make_l1_road(clean_text)
    floor_text = "floor"
    floor_road = sue_world.make_road(clean_road, floor_text)
    bob_text = "Bob"
    floor_idea = ideaunit_shop(floor_text, pledge=True)
    floor_idea._cultureunit.set_belieflink(bob_text)
    sue_world.add_idea(floor_idea, clean_road)
    floor_idea = sue_world.get_idea_obj(floor_road)
    assert floor_idea._cultureunit.belieflink_exists(bob_text) is False

    # WHEN
    create_pledge(sue_world, floor_road, bob_text)

    # THEN
    assert floor_idea._cultureunit.belieflink_exists(bob_text)
    yao_text = "Yao"
    assert sue_world.char_exists(yao_text) is False
    assert floor_idea._cultureunit.belieflink_exists(yao_text) is False

    # WHEN
    create_pledge(sue_world, floor_road, yao_text)

    # THEN
    assert sue_world.char_exists(yao_text)
    assert floor_idea._cultureunit.belieflink_exists(yao_text)
