from src._world.reason_culture import (
    CultureUnit,
    cultureunit_shop,
    CultureHeir,
    cultureheir_shop,
    create_cultureunit,
)
from src._world.beliefunit import BeliefID, beliefunit_shop
from src._world.char import charlink_shop
from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_CultureUnit_exists():
    # GIVEN
    x_belieflinks = {1}

    # WHEN
    x_cultureunit = CultureUnit(_belieflinks=x_belieflinks)

    # THEN
    assert x_cultureunit
    assert x_cultureunit._belieflinks == x_belieflinks


def test_cultureunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    x_belieflinks = {1}

    # WHEN
    x_cultureunit = cultureunit_shop(_belieflinks=x_belieflinks)

    # THEN
    assert x_cultureunit
    assert x_cultureunit._belieflinks == x_belieflinks


def test_cultureunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    x_cultureunit = cultureunit_shop()

    # THEN
    assert x_cultureunit
    assert x_cultureunit._belieflinks == set()


def test_create_cultureunit_ReturnsCorrectObj():
    # GIVEN
    swim_belief_id = BeliefID("swimmers")

    # WHEN
    swim_cultureunit = create_cultureunit(swim_belief_id)

    # THEN
    assert swim_cultureunit
    assert len(swim_cultureunit._belieflinks) == 1


def test_CultureUnit_get_dict_ReturnsCorrectDictWithSingle_belieflink():
    # GIVEN
    bob_belief_id = BeliefID("Bob")
    x_belieflinks = {bob_belief_id: bob_belief_id}
    x_cultureunit = cultureunit_shop(_belieflinks=x_belieflinks)

    # WHEN
    obj_dict = x_cultureunit.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_belieflinks": [bob_belief_id]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_CultureUnit_set_belieflink_CorrectlySets_belieflinks_v1():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    assert len(x_cultureunit._belieflinks) == 0

    # WHEN
    jim_text = "Jim"
    x_cultureunit.set_belieflink(belief_id=jim_text)

    # THEN
    assert len(x_cultureunit._belieflinks) == 1


def test_CultureUnit_belieflink_exists_ReturnsCorrectObj():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    jim_text = "Jim"
    assert x_cultureunit.belieflink_exists(jim_text) is False

    # WHEN
    x_cultureunit.set_belieflink(belief_id=jim_text)

    # THEN
    assert x_cultureunit.belieflink_exists(jim_text)


def test_CultureUnit_del_belieflink_CorrectlyDeletes_belieflinks_v1():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    x_cultureunit.set_belieflink(belief_id=jim_text)
    x_cultureunit.set_belieflink(belief_id=sue_text)
    assert len(x_cultureunit._belieflinks) == 2

    # WHEN
    x_cultureunit.del_belieflink(belief_id=sue_text)

    # THEN
    assert len(x_cultureunit._belieflinks) == 1


def test_CultureHeir_exists():
    # GIVEN
    x_belieflinks = {1}
    _owner_id_x_cultureunit = True

    # WHEN
    x_cultureheir = CultureHeir(
        _belieflinks=x_belieflinks, _owner_id_culture=_owner_id_x_cultureunit
    )

    # THEN
    assert x_cultureheir
    assert x_cultureheir._belieflinks == x_belieflinks
    assert x_cultureheir._owner_id_culture == _owner_id_x_cultureunit


def test_cultureheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    x_belieflinks = {1}
    _owner_id_x_cultureunit = "example"

    # WHEN
    x_cultureheir = cultureheir_shop(
        _belieflinks=x_belieflinks, _owner_id_culture=_owner_id_x_cultureunit
    )

    # THEN
    assert x_cultureheir
    assert x_cultureheir._belieflinks == x_belieflinks
    assert x_cultureheir._owner_id_culture == _owner_id_x_cultureunit


def test_CultureHeir_get_all_suff_chars_ReturnsSingleDictWithAllChars_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)

    x_belieflinks = {jim_text}
    x_cultureheir = cultureheir_shop(_belieflinks=x_belieflinks)

    # WHEN
    all_chars = x_cultureheir._get_all_suff_chars(world_beliefs=x_world._beliefs)

    # THEN
    assert len(all_chars) == 1


def test_CultureHeir_get_all_suff_chars_ReturnsSingleDictWithAllChars_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    x_belieflinks = {swim_text}
    x_cultureheir = cultureheir_shop(_belieflinks=x_belieflinks)

    # WHEN
    all_chars = x_cultureheir._get_all_suff_chars(world_beliefs=x_world._beliefs)

    # THEN
    assert len(all_chars) == 2


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_Emptyx_belieflinks():
    # GIVEN
    x_belieflinks = set()
    x_cultureheir = cultureheir_shop(_belieflinks=x_belieflinks)
    assert x_cultureheir._owner_id_culture is False

    # WHEN
    world_beliefs = set()
    x_cultureheir.set_owner_id_culture(world_beliefs=world_beliefs, world_owner_id="")

    # THEN
    assert x_cultureheir._owner_id_culture


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_belieflinks_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    world_owner_id = x_world._owner_id
    world_beliefs = x_world._beliefs
    print(f"{len(world_beliefs)=}")
    # print(f"{world_beliefs.get(jim_text)=}")
    # print(f"{world_beliefs.get(sue_text)=}")

    x_belieflinks = {jim_text}
    x_cultureheir = cultureheir_shop(_belieflinks=x_belieflinks)
    assert x_cultureheir._owner_id_culture is False

    # WHEN
    x_cultureheir.set_owner_id_culture(world_beliefs, world_owner_id)

    # THEN
    assert x_cultureheir._owner_id_culture


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_belieflinks_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    world_owner_id = x_world._owner_id
    world_beliefs = x_world._beliefs
    print(f"{len(world_beliefs)=}")
    # print(f"{world_beliefs.get(jim_text)=}")
    # print(f"{world_beliefs.get(sue_text)=}")

    x_belieflinks = {sue_text}
    x_cultureheir = cultureheir_shop(_belieflinks=x_belieflinks)
    assert x_cultureheir._owner_id_culture is False

    # WHEN
    x_cultureheir.set_owner_id_culture(world_beliefs, world_owner_id)

    # THEN
    assert x_cultureheir._owner_id_culture is False


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_belieflinks_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    x_belieflinks = {swim_text}
    x_cultureheir = cultureheir_shop(_belieflinks=x_belieflinks)
    assert x_cultureheir._owner_id_culture is False
    x_cultureheir.set_owner_id_culture(x_world._beliefs, x_world._owner_id)
    assert x_cultureheir._owner_id_culture

    # WHEN
    swim_belief.del_charlink(char_id=jim_text)
    x_world.set_beliefunit(y_beliefunit=swim_belief)
    x_cultureheir.set_owner_id_culture(x_world._beliefs, x_world._owner_id)

    # THEN
    assert x_cultureheir._owner_id_culture is False


def test_CultureHeir_set__CorrectlySetsAttribute_NonEmptyx_belieflinks_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    x_belieflinks = {swim_text}
    x_cultureheir = cultureheir_shop(_belieflinks=x_belieflinks)
    assert x_cultureheir._owner_id_culture is False
    x_cultureheir.set_owner_id_culture(x_world._beliefs, x_world._owner_id)
    assert x_cultureheir._owner_id_culture

    # WHEN
    swim_belief.del_charlink(char_id=jim_text)
    x_world.set_beliefunit(y_beliefunit=swim_belief)
    x_cultureheir.set_owner_id_culture(x_world._beliefs, x_world._owner_id)

    # THEN
    assert x_cultureheir._owner_id_culture is False


def test_CultureHeir_set_belieflink_CultureUnitEmpty_ParentCultureHeirEmpty():
    # GIVEN
    x_cultureheir = cultureheir_shop(_belieflinks={})
    parent_cultureheir_empty = cultureheir_shop()
    x_cultureunit = cultureunit_shop()

    # WHEN
    x_cultureheir.set_belieflinks(
        parent_cultureheir=parent_cultureheir_empty,
        cultureunit=x_cultureunit,
        world_beliefs=None,
    )

    # THEN
    x_cultureheir._belieflinks = {}


def test_CultureHeir_set_belieflink_CultureUnitNotEmpty_ParentCultureHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_belieflink(belief_id=kent_text)
    x_cultureunit.set_belieflink(belief_id=swim_text)

    # WHEN
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_belieflinks(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )

    # THEN
    assert x_cultureheir._belieflinks == x_cultureunit._belieflinks


def test_CultureHeir_set_belieflink_CultureUnitNotEmpty_ParentCultureHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_belieflink(belief_id=kent_text)
    x_cultureunit.set_belieflink(belief_id=swim_text)

    # WHEN
    x_cultureheir = cultureheir_shop()
    parent_cultureheir_empty = cultureheir_shop()
    x_cultureheir.set_belieflinks(
        parent_cultureheir_empty, cultureunit=x_cultureunit, world_beliefs=None
    )

    # THEN
    assert x_cultureheir._belieflinks == x_cultureunit._belieflinks


def test_CultureHeir_set_belieflink_CultureUnitEmpty_ParentCultureHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    cultureunit_swim = cultureunit_shop()
    cultureunit_swim.set_belieflink(belief_id=kent_text)
    cultureunit_swim.set_belieflink(belief_id=swim_text)
    empty_cultureheir = cultureheir_shop()

    parent_cultureheir = cultureheir_shop()
    parent_cultureheir.set_belieflinks(
        empty_cultureheir, cultureunit_swim, world_beliefs=None
    )

    cultureunit_empty = cultureunit_shop()

    # WHEN
    x_cultureheir = cultureheir_shop()
    assert x_cultureheir._belieflinks == set()
    x_cultureheir.set_belieflinks(
        parent_cultureheir, cultureunit=cultureunit_empty, world_beliefs=None
    )

    # THEN
    assert len(x_cultureheir._belieflinks)
    assert x_cultureheir._belieflinks == parent_cultureheir._belieflinks


def test_CultureHeir_set_belieflink_CultureUnitEqualParentCultureHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    cultureunit_swim = cultureunit_shop()
    cultureunit_swim.set_belieflink(belief_id=kent_text)
    cultureunit_swim.set_belieflink(belief_id=swim_text)
    empty_cultureheir = cultureheir_shop()

    parent_cultureheir = cultureheir_shop()
    parent_cultureheir.set_belieflinks(
        empty_cultureheir, cultureunit_swim, world_beliefs=None
    )

    # WHEN
    x_cultureheir = cultureheir_shop()
    assert x_cultureheir._belieflinks == set()
    x_cultureheir.set_belieflinks(
        parent_cultureheir, cultureunit=cultureunit_swim, world_beliefs=None
    )

    # THEN
    assert x_cultureheir._belieflinks == parent_cultureheir._belieflinks


def test_CultureHeir_set_belieflink_CultureUnit_NotEqual_ParentCultureHeir_NonEmpty():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    tom_text = "Tom"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)
    x_world.add_charunit(char_id=tom_text)

    swim2_text = ",swim2"
    swim2_belief = beliefunit_shop(belief_id=swim2_text)
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim2_belief)

    swim3_text = ",swim3"
    swim3_belief = beliefunit_shop(belief_id=swim3_text)
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=tom_text))
    x_world.set_beliefunit(y_beliefunit=swim3_belief)

    parent_cultureunit = cultureunit_shop()
    parent_cultureunit.set_belieflink(belief_id=swim3_text)
    parent_cultureheir = cultureheir_shop()
    parent_cultureheir.set_belieflinks(
        parent_cultureheir=None, cultureunit=parent_cultureunit, world_beliefs=None
    )

    cultureunit_swim2 = cultureunit_shop()
    cultureunit_swim2.set_belieflink(belief_id=swim2_text)

    # WHEN
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_belieflinks(
        parent_cultureheir, cultureunit_swim2, world_beliefs=x_world._beliefs
    )

    # THEN
    assert x_cultureheir._belieflinks == cultureunit_swim2._belieflinks
    assert len(x_cultureheir._belieflinks) == 1
    assert list(x_cultureheir._belieflinks) == [swim2_text]


def test_CultureHeir_set_belieflink_CultureUnit_NotEqualParentCultureHeir_RaisesError():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    tom_text = "Tom"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)
    x_world.add_charunit(char_id=tom_text)

    swim2_text = ",swim2"
    swim2_belief = beliefunit_shop(belief_id=swim2_text)
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim2_belief)

    swim3_text = ",swim3"
    swim3_belief = beliefunit_shop(belief_id=swim3_text)
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=tom_text))
    x_world.set_beliefunit(y_beliefunit=swim3_belief)

    parent_cultureunit = cultureunit_shop()
    parent_cultureunit.set_belieflink(belief_id=swim2_text)
    parent_cultureheir = cultureheir_shop()
    parent_cultureheir.set_belieflinks(
        parent_cultureheir=None, cultureunit=parent_cultureunit, world_beliefs=None
    )

    cultureunit_swim3 = cultureunit_shop()
    cultureunit_swim3.set_belieflink(belief_id=swim3_text)

    # WHEN / THEN
    x_cultureheir = cultureheir_shop()
    all_parent_cultureheir_chars = {jim_text, sue_text}
    all_cultureunit_chars = {jim_text, sue_text, tom_text}
    with pytest_raises(Exception) as excinfo:
        x_cultureheir.set_belieflinks(
            parent_cultureheir, cultureunit_swim3, world_beliefs=x_world._beliefs
        )
    assert (
        str(excinfo.value)
        == f"parent_cultureheir does not contain all chars of the idea's cultureunit\n{set(all_parent_cultureheir_chars)=}\n\n{set(all_cultureunit_chars)=}"
    )


def test_CultureUnit_get_belieflink_ReturnsCorrectObj():
    # GIVEN
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_belieflink(climb_text)
    x_cultureunit.set_belieflink(walk_text)
    x_cultureunit.set_belieflink(swim_text)

    # WHEN / THEN
    assert x_cultureunit.get_belieflink(walk_text) != None
    assert x_cultureunit.get_belieflink(swim_text) != None
    assert x_cultureunit.get_belieflink(run_text) is None


def test_CultureHeir_belief_id_in_ReturnsCorrectBoolWhen_belieflinksNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text}
    hike_dict = {hike_text}
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_belieflink(belief_id=swim_text)
    x_cultureunit.set_belieflink(belief_id=hike_text)
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_belieflinks(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert swim_text in x_cultureheir._belieflinks
    assert hike_text in x_cultureheir._belieflinks
    print(f"{hunt_text in x_cultureheir._belieflinks=}")
    assert hunt_text not in x_cultureheir._belieflinks
    assert play_text not in x_cultureheir._belieflinks
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_cultureheir.has_belief(swim_dict)
    assert x_cultureheir.has_belief(hike_dict)
    assert x_cultureheir.has_belief(hunt_dict) is False
    assert x_cultureheir.has_belief(hunt_hike_dict)
    assert x_cultureheir.has_belief(hunt_play_dict) is False


def test_CultureHeir_has_belief_ReturnsCorrectBoolWhen_belieflinksEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text}
    x_cultureunit = cultureunit_shop()
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_belieflinks(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert x_cultureheir._belieflinks == set()
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_cultureheir.has_belief(hike_dict)
    assert x_cultureheir.has_belief(hunt_dict)
    assert x_cultureheir.has_belief(play_dict)
    assert x_cultureheir.has_belief(hunt_hike_dict)
    assert x_cultureheir.has_belief(hunt_play_dict)
