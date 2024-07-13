from src._world.reason_culture import (
    CultureUnit,
    cultureunit_shop,
    CultureHeir,
    cultureheir_shop,
    create_cultureunit,
)
from src._world.beliefbox import BeliefID, beliefbox_shop
from src._world.char import charlink_shop
from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_CultureUnit_exists():
    # GIVEN
    x_allyholds = {1}

    # WHEN
    x_cultureunit = CultureUnit(_allyholds=x_allyholds)

    # THEN
    assert x_cultureunit
    assert x_cultureunit._allyholds == x_allyholds


def test_cultureunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    x_allyholds = {1}

    # WHEN
    x_cultureunit = cultureunit_shop(_allyholds=x_allyholds)

    # THEN
    assert x_cultureunit
    assert x_cultureunit._allyholds == x_allyholds


def test_cultureunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    x_cultureunit = cultureunit_shop()

    # THEN
    assert x_cultureunit
    assert x_cultureunit._allyholds == set()


def test_create_cultureunit_ReturnsCorrectObj():
    # GIVEN
    swim_belief_id = BeliefID("swimmers")

    # WHEN
    swim_cultureunit = create_cultureunit(swim_belief_id)

    # THEN
    assert swim_cultureunit
    assert len(swim_cultureunit._allyholds) == 1


def test_CultureUnit_get_dict_ReturnsCorrectDictWithSingle_allyhold():
    # GIVEN
    bob_belief_id = BeliefID("Bob")
    x_allyholds = {bob_belief_id: bob_belief_id}
    x_cultureunit = cultureunit_shop(_allyholds=x_allyholds)

    # WHEN
    obj_dict = x_cultureunit.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_allyholds": [bob_belief_id]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_CultureUnit_set_allyhold_CorrectlySets_allyholds_v1():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    assert len(x_cultureunit._allyholds) == 0

    # WHEN
    jim_text = "Jim"
    x_cultureunit.set_allyhold(belief_id=jim_text)

    # THEN
    assert len(x_cultureunit._allyholds) == 1


def test_CultureUnit_allyhold_exists_ReturnsCorrectObj():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    jim_text = "Jim"
    assert x_cultureunit.allyhold_exists(jim_text) is False

    # WHEN
    x_cultureunit.set_allyhold(belief_id=jim_text)

    # THEN
    assert x_cultureunit.allyhold_exists(jim_text)


def test_CultureUnit_del_allyhold_CorrectlyDeletes_allyholds_v1():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    x_cultureunit.set_allyhold(belief_id=jim_text)
    x_cultureunit.set_allyhold(belief_id=sue_text)
    assert len(x_cultureunit._allyholds) == 2

    # WHEN
    x_cultureunit.del_allyhold(belief_id=sue_text)

    # THEN
    assert len(x_cultureunit._allyholds) == 1


def test_CultureHeir_exists():
    # GIVEN
    x_allyholds = {1}
    _owner_id_x_cultureunit = True

    # WHEN
    x_cultureheir = CultureHeir(
        _allyholds=x_allyholds, _owner_id_culture=_owner_id_x_cultureunit
    )

    # THEN
    assert x_cultureheir
    assert x_cultureheir._allyholds == x_allyholds
    assert x_cultureheir._owner_id_culture == _owner_id_x_cultureunit


def test_cultureheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    x_allyholds = {1}
    _owner_id_x_cultureunit = "example"

    # WHEN
    x_cultureheir = cultureheir_shop(
        _allyholds=x_allyholds, _owner_id_culture=_owner_id_x_cultureunit
    )

    # THEN
    assert x_cultureheir
    assert x_cultureheir._allyholds == x_allyholds
    assert x_cultureheir._owner_id_culture == _owner_id_x_cultureunit


def test_CultureHeir_get_all_suff_chars_ReturnsSingleDictWithAllChars_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)

    x_allyholds = {jim_text}
    x_cultureheir = cultureheir_shop(_allyholds=x_allyholds)

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
    swim_belief = beliefbox_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefbox(y_beliefbox=swim_belief)

    x_allyholds = {swim_text}
    x_cultureheir = cultureheir_shop(_allyholds=x_allyholds)

    # WHEN
    all_chars = x_cultureheir._get_all_suff_chars(world_beliefs=x_world._beliefs)

    # THEN
    assert len(all_chars) == 2


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_Emptyx_allyholds():
    # GIVEN
    x_allyholds = set()
    x_cultureheir = cultureheir_shop(_allyholds=x_allyholds)
    assert x_cultureheir._owner_id_culture is False

    # WHEN
    world_beliefs = set()
    x_cultureheir.set_owner_id_culture(world_beliefs=world_beliefs, world_owner_id="")

    # THEN
    assert x_cultureheir._owner_id_culture


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_allyholds_v1():
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

    x_allyholds = {jim_text}
    x_cultureheir = cultureheir_shop(_allyholds=x_allyholds)
    assert x_cultureheir._owner_id_culture is False

    # WHEN
    x_cultureheir.set_owner_id_culture(world_beliefs, world_owner_id)

    # THEN
    assert x_cultureheir._owner_id_culture


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_allyholds_v2():
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

    x_allyholds = {sue_text}
    x_cultureheir = cultureheir_shop(_allyholds=x_allyholds)
    assert x_cultureheir._owner_id_culture is False

    # WHEN
    x_cultureheir.set_owner_id_culture(world_beliefs, world_owner_id)

    # THEN
    assert x_cultureheir._owner_id_culture is False


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_allyholds_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefbox_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefbox(y_beliefbox=swim_belief)

    x_allyholds = {swim_text}
    x_cultureheir = cultureheir_shop(_allyholds=x_allyholds)
    assert x_cultureheir._owner_id_culture is False
    x_cultureheir.set_owner_id_culture(x_world._beliefs, x_world._owner_id)
    assert x_cultureheir._owner_id_culture

    # WHEN
    swim_belief.del_charlink(char_id=jim_text)
    x_world.set_beliefbox(y_beliefbox=swim_belief)
    x_cultureheir.set_owner_id_culture(x_world._beliefs, x_world._owner_id)

    # THEN
    assert x_cultureheir._owner_id_culture is False


def test_CultureHeir_set__CorrectlySetsAttribute_NonEmptyx_allyholds_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefbox_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefbox(y_beliefbox=swim_belief)

    x_allyholds = {swim_text}
    x_cultureheir = cultureheir_shop(_allyholds=x_allyholds)
    assert x_cultureheir._owner_id_culture is False
    x_cultureheir.set_owner_id_culture(x_world._beliefs, x_world._owner_id)
    assert x_cultureheir._owner_id_culture

    # WHEN
    swim_belief.del_charlink(char_id=jim_text)
    x_world.set_beliefbox(y_beliefbox=swim_belief)
    x_cultureheir.set_owner_id_culture(x_world._beliefs, x_world._owner_id)

    # THEN
    assert x_cultureheir._owner_id_culture is False


def test_CultureHeir_set_allyhold_CultureUnitEmpty_ParentCultureHeirEmpty():
    # GIVEN
    x_cultureheir = cultureheir_shop(_allyholds={})
    parent_cultureheir_empty = cultureheir_shop()
    x_cultureunit = cultureunit_shop()

    # WHEN
    x_cultureheir.set_allyholds(
        parent_cultureheir=parent_cultureheir_empty,
        cultureunit=x_cultureunit,
        world_beliefs=None,
    )

    # THEN
    x_cultureheir._allyholds = {}


def test_CultureHeir_set_allyhold_CultureUnitNotEmpty_ParentCultureHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_allyhold(belief_id=kent_text)
    x_cultureunit.set_allyhold(belief_id=swim_text)

    # WHEN
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )

    # THEN
    assert x_cultureheir._allyholds == x_cultureunit._allyholds


def test_CultureHeir_set_allyhold_CultureUnitNotEmpty_ParentCultureHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_allyhold(belief_id=kent_text)
    x_cultureunit.set_allyhold(belief_id=swim_text)

    # WHEN
    x_cultureheir = cultureheir_shop()
    parent_cultureheir_empty = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir_empty, cultureunit=x_cultureunit, world_beliefs=None
    )

    # THEN
    assert x_cultureheir._allyholds == x_cultureunit._allyholds


def test_CultureHeir_set_allyhold_CultureUnitEmpty_ParentCultureHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    cultureunit_swim = cultureunit_shop()
    cultureunit_swim.set_allyhold(belief_id=kent_text)
    cultureunit_swim.set_allyhold(belief_id=swim_text)
    empty_cultureheir = cultureheir_shop()

    parent_cultureheir = cultureheir_shop()
    parent_cultureheir.set_allyholds(
        empty_cultureheir, cultureunit_swim, world_beliefs=None
    )

    cultureunit_empty = cultureunit_shop()

    # WHEN
    x_cultureheir = cultureheir_shop()
    assert x_cultureheir._allyholds == set()
    x_cultureheir.set_allyholds(
        parent_cultureheir, cultureunit=cultureunit_empty, world_beliefs=None
    )

    # THEN
    assert len(x_cultureheir._allyholds)
    assert x_cultureheir._allyholds == parent_cultureheir._allyholds


def test_CultureHeir_set_allyhold_CultureUnitEqualParentCultureHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    cultureunit_swim = cultureunit_shop()
    cultureunit_swim.set_allyhold(belief_id=kent_text)
    cultureunit_swim.set_allyhold(belief_id=swim_text)
    empty_cultureheir = cultureheir_shop()

    parent_cultureheir = cultureheir_shop()
    parent_cultureheir.set_allyholds(
        empty_cultureheir, cultureunit_swim, world_beliefs=None
    )

    # WHEN
    x_cultureheir = cultureheir_shop()
    assert x_cultureheir._allyholds == set()
    x_cultureheir.set_allyholds(
        parent_cultureheir, cultureunit=cultureunit_swim, world_beliefs=None
    )

    # THEN
    assert x_cultureheir._allyholds == parent_cultureheir._allyholds


def test_CultureHeir_set_allyhold_CultureUnit_NotEqual_ParentCultureHeir_NonEmpty():
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
    swim2_belief = beliefbox_shop(belief_id=swim2_text)
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefbox(y_beliefbox=swim2_belief)

    swim3_text = ",swim3"
    swim3_belief = beliefbox_shop(belief_id=swim3_text)
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=tom_text))
    x_world.set_beliefbox(y_beliefbox=swim3_belief)

    parent_cultureunit = cultureunit_shop()
    parent_cultureunit.set_allyhold(belief_id=swim3_text)
    parent_cultureheir = cultureheir_shop()
    parent_cultureheir.set_allyholds(
        parent_cultureheir=None, cultureunit=parent_cultureunit, world_beliefs=None
    )

    cultureunit_swim2 = cultureunit_shop()
    cultureunit_swim2.set_allyhold(belief_id=swim2_text)

    # WHEN
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir, cultureunit_swim2, world_beliefs=x_world._beliefs
    )

    # THEN
    assert x_cultureheir._allyholds == cultureunit_swim2._allyholds
    assert len(x_cultureheir._allyholds) == 1
    assert list(x_cultureheir._allyholds) == [swim2_text]


def test_CultureHeir_set_allyhold_CultureUnit_NotEqualParentCultureHeir_RaisesError():
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
    swim2_belief = beliefbox_shop(belief_id=swim2_text)
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefbox(y_beliefbox=swim2_belief)

    swim3_text = ",swim3"
    swim3_belief = beliefbox_shop(belief_id=swim3_text)
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=tom_text))
    x_world.set_beliefbox(y_beliefbox=swim3_belief)

    parent_cultureunit = cultureunit_shop()
    parent_cultureunit.set_allyhold(belief_id=swim2_text)
    parent_cultureheir = cultureheir_shop()
    parent_cultureheir.set_allyholds(
        parent_cultureheir=None, cultureunit=parent_cultureunit, world_beliefs=None
    )

    cultureunit_swim3 = cultureunit_shop()
    cultureunit_swim3.set_allyhold(belief_id=swim3_text)

    # WHEN / THEN
    x_cultureheir = cultureheir_shop()
    all_parent_cultureheir_chars = {jim_text, sue_text}
    all_cultureunit_chars = {jim_text, sue_text, tom_text}
    with pytest_raises(Exception) as excinfo:
        x_cultureheir.set_allyholds(
            parent_cultureheir, cultureunit_swim3, world_beliefs=x_world._beliefs
        )
    assert (
        str(excinfo.value)
        == f"parent_cultureheir does not contain all chars of the idea's cultureunit\n{set(all_parent_cultureheir_chars)=}\n\n{set(all_cultureunit_chars)=}"
    )


def test_CultureUnit_get_allyhold_ReturnsCorrectObj():
    # GIVEN
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_allyhold(climb_text)
    x_cultureunit.set_allyhold(walk_text)
    x_cultureunit.set_allyhold(swim_text)

    # WHEN / THEN
    assert x_cultureunit.get_allyhold(walk_text) != None
    assert x_cultureunit.get_allyhold(swim_text) != None
    assert x_cultureunit.get_allyhold(run_text) is None


def test_CultureHeir_belief_id_in_ReturnsCorrectBoolWhen_allyholdsNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text}
    hike_dict = {hike_text}
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_allyhold(belief_id=swim_text)
    x_cultureunit.set_allyhold(belief_id=hike_text)
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert swim_text in x_cultureheir._allyholds
    assert hike_text in x_cultureheir._allyholds
    print(f"{hunt_text in x_cultureheir._allyholds=}")
    assert hunt_text not in x_cultureheir._allyholds
    assert play_text not in x_cultureheir._allyholds
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_cultureheir.has_belief(swim_dict)
    assert x_cultureheir.has_belief(hike_dict)
    assert x_cultureheir.has_belief(hunt_dict) is False
    assert x_cultureheir.has_belief(hunt_hike_dict)
    assert x_cultureheir.has_belief(hunt_play_dict) is False


def test_CultureHeir_has_belief_ReturnsCorrectBoolWhen_allyholdsEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text}
    x_cultureunit = cultureunit_shop()
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_allyholds(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert x_cultureheir._allyholds == set()
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_cultureheir.has_belief(hike_dict)
    assert x_cultureheir.has_belief(hunt_dict)
    assert x_cultureheir.has_belief(play_dict)
    assert x_cultureheir.has_belief(hunt_hike_dict)
    assert x_cultureheir.has_belief(hunt_play_dict)
