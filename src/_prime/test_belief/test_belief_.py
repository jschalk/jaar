from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._prime.belief import (
    BeliefUnit,
    beliefunit_shop,
    create_beliefunit,
    opinionunit_shop,
)
from pytest import raises as pytest_raises


def test_BeliefUnit_exists():
    # GIVEN / WHEN
    x_belief = BeliefUnit()

    # THEN
    assert x_belief != None
    assert x_belief.base is None
    assert x_belief.action is None
    assert x_belief.opinionunits is None
    assert x_belief.delimiter is None
    assert x_belief.actors is None
    assert x_belief._calc_is_meaningful is None
    assert x_belief._calc_is_tribal is None
    assert x_belief._calc_is_dialectic is None


def test_beliefunit_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    cook_belief = beliefunit_shop(base=cook_road)

    # THEN
    assert cook_belief.base == cook_road
    assert cook_belief.action == False
    assert cook_belief.opinionunits == {}
    assert cook_belief.delimiter == default_road_delimiter_if_none()
    assert cook_belief.actors == {}
    assert cook_belief._calc_is_meaningful == False
    assert cook_belief._calc_is_tribal == False
    assert cook_belief._calc_is_dialectic == False


def test_BeliefUnit_set_action_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    assert cook_belief.action == False

    # WHEN / THEN
    cook_belief.set_action(True)
    assert cook_belief.action

    # WHEN / THEN
    cook_belief.set_action(False)
    assert cook_belief.action == False


def test_BeliefUnit_set_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    assert cook_belief.actors == {}

    # WHEN
    bob_text = "Bob"
    cook_belief.set_actor(x_actor=bob_text)

    # THEN
    assert cook_belief.actors != {}
    assert cook_belief.actors.get(bob_text) != None
    assert cook_belief.actors.get(bob_text) == bob_text


def test_BeliefUnit_del_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_belief.set_actor(bob_text)
    cook_belief.set_actor(yao_text)
    assert len(cook_belief.actors) == 2
    assert cook_belief.actors.get(bob_text) != None
    assert cook_belief.actors.get(yao_text) != None

    # WHEN
    cook_belief.del_actor(bob_text)

    # THEN
    assert len(cook_belief.actors) == 1
    assert cook_belief.actors.get(bob_text) is None
    assert cook_belief.actors.get(yao_text) != None


def test_BeliefUnit_get_actor_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_belief.set_actor(bob_text)
    cook_belief.set_actor(yao_text)

    # WHEN
    bob_actor = cook_belief.get_actor(bob_text)

    # THEN
    assert bob_actor != None
    assert bob_actor == bob_text


def test_BeliefUnit_actor_exists_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    assert cook_belief.actor_exists(bob_text) == False
    assert cook_belief.actor_exists(yao_text) == False

    # WHEN / THEN
    cook_belief.set_actor(bob_text)
    cook_belief.set_actor(yao_text)
    assert cook_belief.actor_exists(bob_text)
    assert cook_belief.actor_exists(yao_text)

    # WHEN / THEN
    cook_belief.del_actor(yao_text)
    assert cook_belief.actor_exists(bob_text)
    assert cook_belief.actor_exists(yao_text) == False


def test_BeliefUnit_set_opinionunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    assert cook_belief.opinionunits == {}

    # WHEN
    cheap_road = create_road(cook_road, "cheap food")
    x_affect = -2
    cheap_opinionunit = opinionunit_shop(cheap_road, affect=x_affect)
    cook_belief.set_opinionunit(x_opinionunit=cheap_opinionunit)

    # THEN
    assert cook_belief.opinionunits != {}
    assert cook_belief.opinionunits.get(cheap_road) != None
    assert cook_belief.opinionunits.get(cheap_road) == cheap_opinionunit


def test_BeliefUnit_del_opinionunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    metal_road = create_road(cook_road, "metal pots")
    cheap_opinionunit = opinionunit_shop(cheap_road, affect=-2)
    metal_opinionunit = opinionunit_shop(metal_road, affect=3)
    cook_belief.set_opinionunit(cheap_opinionunit)
    cook_belief.set_opinionunit(metal_opinionunit)
    assert len(cook_belief.opinionunits) == 2
    assert cook_belief.opinionunits.get(cheap_road) != None
    assert cook_belief.opinionunits.get(metal_road) != None

    # WHEN
    cook_belief.del_opinionunit(cheap_road)

    # THEN
    assert len(cook_belief.opinionunits) == 1
    assert cook_belief.opinionunits.get(cheap_road) is None
    assert cook_belief.opinionunits.get(metal_road) != None


def test_BeliefUnit_get_opinionunits_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_opinionunit = opinionunit_shop(farm_road, farm_affect)
    cook_belief.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_good_opinionunits = cook_belief.get_opinionunits(good=True)

    # THEN
    assert x_good_opinionunits != {}
    assert len(x_good_opinionunits) == 1
    assert x_good_opinionunits.get(farm_road) == farm_opinionunit


def test_BeliefUnit_get_opinionunits_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_opinionunit = opinionunit_shop(farm_road, farm_affect)
    cook_belief.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cheap_opinionunit = opinionunit_shop(cheap_road, cheap_affect)
    cook_belief.set_opinionunit(cheap_opinionunit)

    # WHEN
    x_bad_opinionunits = cook_belief.get_opinionunits(bad=True)

    # THEN
    assert x_bad_opinionunits != {}
    assert len(x_bad_opinionunits) == 1
    assert x_bad_opinionunits.get(cheap_road) == cheap_opinionunit


def test_BeliefUnit_get_1_opinionunit_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_belief.set_opinionunit(opinionunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_opinionunit = cook_belief.get_1_opinionunit(good=True)

    # THEN
    assert x_bad_opinionunit == farm_road


def test_BeliefUnit_get_1_opinionunit_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_belief.set_opinionunit(opinionunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_opinionunit = cook_belief.get_1_opinionunit(bad=True)

    # THEN
    assert x_bad_opinionunit == cheap_road


def test_BeliefUnit_get_opinionunits_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=farm_love)
    cook_belief.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_in_tribe_opinionunits = cook_belief.get_opinionunits(in_tribe=True)

    # THEN
    assert x_in_tribe_opinionunits != {}
    assert len(x_in_tribe_opinionunits) == 1
    assert x_in_tribe_opinionunits.get(farm_road) == farm_opinionunit


def test_BeliefUnit_get_opinionunits_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=farm_love)
    cook_belief.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cheap_opinionunit = opinionunit_shop(cheap_road, -2, love=cheap_love)
    cook_belief.set_opinionunit(cheap_opinionunit)

    # WHEN
    x_out_tribe_opinionunits = cook_belief.get_opinionunits(out_tribe=True)

    # THEN.
    assert x_out_tribe_opinionunits != {}
    assert len(x_out_tribe_opinionunits) == 1
    assert x_out_tribe_opinionunits.get(cheap_road) == cheap_opinionunit


def test_BeliefUnit_get_1_opinionunit_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_belief.set_opinionunit(opinionunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_opinionunit = cook_belief.get_1_opinionunit(in_tribe=True)

    # THEN
    assert x_out_tribe_opinionunit == farm_road


def test_BeliefUnit_get_1_opinionunit_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_belief.set_opinionunit(opinionunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_opinionunit = cook_belief.get_1_opinionunit(out_tribe=True)

    # THEN
    assert x_out_tribe_opinionunit == cheap_road


def test_BeliefUnit_set_opinionunits_CorrectlyRaisesBeliefSubRoadUnitException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    go_road = "going out"
    go_cheap_road = create_road(go_road, "cheap food")
    go_cheap_opinionunit = opinionunit_shop(go_cheap_road, affect=-3)

    # WHEN
    x_affect = -2
    with pytest_raises(Exception) as excinfo:
        cook_belief.set_opinionunit(go_cheap_opinionunit)
    assert (
        str(excinfo.value)
        == f"BeliefUnit cannot set opinionunit '{go_cheap_road}' because base road is '{cook_road}'."
    )


def test_BeliefUnit_get_all_roads_ReturnsCorrectObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    cheap_text = "cheap food"
    farm_text = "farm fresh"
    plastic_text = "plastic pots"
    metal_text = "metal pots"
    cook_belief.set_opinionunit(
        opinionunit_shop(create_road(cook_road, cheap_text), -2)
    )
    cook_belief.set_opinionunit(opinionunit_shop(create_road(cook_road, farm_text), 3))
    cook_belief.set_opinionunit(
        opinionunit_shop(create_road(cook_road, plastic_text), -5)
    )
    cook_belief.set_opinionunit(opinionunit_shop(create_road(cook_road, metal_text), 7))
    assert len(cook_belief.opinionunits) == 4

    # WHEN
    all_roads_dict = cook_belief.get_all_roads()

    # THEN
    assert len(all_roads_dict) == 5
    assert all_roads_dict.get(cook_road) != None
    cheap_road = create_road(cook_road, cheap_text)
    farm_road = create_road(cook_road, farm_text)
    plastic_road = create_road(cook_road, plastic_text)
    metal_road = create_road(cook_road, metal_text)
    assert all_roads_dict.get(cheap_road) != None
    assert all_roads_dict.get(farm_road) != None
    assert all_roads_dict.get(plastic_road) != None
    assert all_roads_dict.get(metal_road) != None
    assert len(cook_belief.opinionunits) == 4


def test_create_beliefunit_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_belief = create_beliefunit(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_belief.base == cook_road
    assert cook_belief.opinionunits != {}
    farm_road = create_road(cook_road, farm_text)
    cheap_road = create_road(cook_road, cheap_text)
    assert cook_belief.opinionunits.get(farm_road) == opinionunit_shop(farm_road, 1)
    assert cook_belief.opinionunits.get(cheap_road) == opinionunit_shop(cheap_road, -1)
