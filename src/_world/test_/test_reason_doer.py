from src._road.road import BeliefID
from src._world.reason_doer import (
    DoerUnit,
    doerunit_shop,
    DoerHeir,
    doerheir_shop,
    create_doerunit,
)
from src._world.belieflink import belieflink_shop
from src._world.beliefstory import beliefstory_shop
from pytest import raises as pytest_raises


def test_DoerUnit_exists():
    # GIVEN
    x_beliefholds = {1}

    # WHEN
    x_doerunit = DoerUnit(_beliefholds=x_beliefholds)

    # THEN
    assert x_doerunit
    assert x_doerunit._beliefholds == x_beliefholds


def test_doerunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    x_beliefholds = {1}

    # WHEN
    x_doerunit = doerunit_shop(_beliefholds=x_beliefholds)

    # THEN
    assert x_doerunit
    assert x_doerunit._beliefholds == x_beliefholds


def test_doerunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    x_doerunit = doerunit_shop()

    # THEN
    assert x_doerunit
    assert x_doerunit._beliefholds == set()


def test_create_doerunit_ReturnsCorrectObj():
    # GIVEN
    swim_belief_id = BeliefID("swimmers")

    # WHEN
    swim_doerunit = create_doerunit(swim_belief_id)

    # THEN
    assert swim_doerunit
    assert len(swim_doerunit._beliefholds) == 1


def test_DoerUnit_get_dict_ReturnsCorrectDictWithSingle_beliefhold():
    # GIVEN
    bob_belief_id = BeliefID("Bob")
    x_beliefholds = {bob_belief_id: bob_belief_id}
    x_doerunit = doerunit_shop(_beliefholds=x_beliefholds)

    # WHEN
    obj_dict = x_doerunit.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_beliefholds": [bob_belief_id]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_DoerUnit_set_beliefhold_CorrectlySets_beliefholds_v1():
    # GIVEN
    x_doerunit = doerunit_shop()
    assert len(x_doerunit._beliefholds) == 0

    # WHEN
    yao_text = "Yao"
    x_doerunit.set_beliefhold(belief_id=yao_text)

    # THEN
    assert len(x_doerunit._beliefholds) == 1


def test_DoerUnit_beliefhold_exists_ReturnsCorrectObj():
    # GIVEN
    x_doerunit = doerunit_shop()
    yao_text = "Yao"
    assert x_doerunit.beliefhold_exists(yao_text) is False

    # WHEN
    x_doerunit.set_beliefhold(belief_id=yao_text)

    # THEN
    assert x_doerunit.beliefhold_exists(yao_text)


def test_DoerUnit_del_beliefhold_CorrectlyDeletes_beliefholds_v1():
    # GIVEN
    x_doerunit = doerunit_shop()
    yao_text = "Yao"
    sue_text = "Sue"
    x_doerunit.set_beliefhold(belief_id=yao_text)
    x_doerunit.set_beliefhold(belief_id=sue_text)
    assert len(x_doerunit._beliefholds) == 2

    # WHEN
    x_doerunit.del_beliefhold(belief_id=sue_text)

    # THEN
    assert len(x_doerunit._beliefholds) == 1


def test_DoerHeir_exists():
    # GIVEN
    x_beliefholds = {1}
    _owner_id_x_doerunit = True

    # WHEN
    x_doerheir = DoerHeir(
        _beliefholds=x_beliefholds, _owner_id_doer=_owner_id_x_doerunit
    )

    # THEN
    assert x_doerheir
    assert x_doerheir._beliefholds == x_beliefholds
    assert x_doerheir._owner_id_doer == _owner_id_x_doerunit


def test_doerheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    x_beliefholds = {1}
    _owner_id_x_doerunit = "example"

    # WHEN
    x_doerheir = doerheir_shop(
        _beliefholds=x_beliefholds, _owner_id_doer=_owner_id_x_doerunit
    )

    # THEN
    assert x_doerheir
    assert x_doerheir._beliefholds == x_beliefholds
    assert x_doerheir._owner_id_doer == _owner_id_x_doerunit


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_Emptyx_beliefholds():
    # GIVEN
    x_beliefholds = set()
    x_doerheir = doerheir_shop(_beliefholds=x_beliefholds)
    assert x_doerheir._owner_id_doer is False

    # WHEN
    world_beliefstorys = {}
    x_doerheir.set_owner_id_doer(world_beliefstorys, world_owner_id="")

    # THEN
    assert x_doerheir._owner_id_doer


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_beliefholds_v1():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_beliefstory = beliefstory_shop(yao_text)
    sue_beliefstory = beliefstory_shop(sue_text)
    yao_beliefstory.set_belieflink(belieflink_shop(yao_text, _char_id=yao_text))
    sue_beliefstory.set_belieflink(belieflink_shop(sue_text, _char_id=sue_text))
    x_beliefstorys = {yao_text: yao_beliefstory, sue_text: sue_beliefstory}
    world_owner_id = yao_text

    x_beliefholds = {yao_text}
    x_doerheir = doerheir_shop(_beliefholds=x_beliefholds)
    assert x_doerheir._owner_id_doer is False

    # WHEN
    x_doerheir.set_owner_id_doer(x_beliefstorys, world_owner_id)

    # THEN
    assert x_doerheir._owner_id_doer


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_beliefholds_v2():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_beliefstory = beliefstory_shop(yao_text)
    sue_beliefstory = beliefstory_shop(sue_text)
    yao_beliefstory.set_belieflink(belieflink_shop(yao_text, _char_id=yao_text))
    sue_beliefstory.set_belieflink(belieflink_shop(sue_text, _char_id=sue_text))
    x_beliefstorys = {yao_text: yao_beliefstory, sue_text: sue_beliefstory}
    x_beliefholds = {sue_text}
    x_doerheir = doerheir_shop(_beliefholds=x_beliefholds)
    assert yao_beliefstory.get_belieflink(yao_text) != None
    assert x_doerheir._owner_id_doer is False

    # WHEN
    x_doerheir.set_owner_id_doer(x_beliefstorys, yao_text)

    # THEN
    assert x_doerheir._owner_id_doer is False


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_beliefholds_v3():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    bob_text = "Bob"
    yao_beliefstory = beliefstory_shop(yao_text)
    sue_beliefstory = beliefstory_shop(sue_text)
    bob_beliefstory = beliefstory_shop(bob_text)
    yao_beliefstory.set_belieflink(belieflink_shop(yao_text, _char_id=yao_text))
    sue_beliefstory.set_belieflink(belieflink_shop(sue_text, _char_id=sue_text))

    swim_text = ",swim"
    swim_beliefstory = beliefstory_shop(belief_id=swim_text)
    swim_beliefstory.set_belieflink(belieflink_shop(swim_text, _char_id=yao_text))
    swim_beliefstory.set_belieflink(belieflink_shop(swim_text, _char_id=sue_text))
    x_beliefstorys = {
        yao_text: yao_beliefstory,
        sue_text: sue_beliefstory,
        bob_text: bob_beliefstory,
        swim_text: swim_beliefstory,
    }

    x_beliefholds = {swim_text}
    x_doerheir = doerheir_shop(_beliefholds=x_beliefholds)
    assert x_doerheir._owner_id_doer is False
    x_doerheir.set_owner_id_doer(x_beliefstorys, world_owner_id=yao_text)
    assert x_doerheir._owner_id_doer

    # WHEN
    swim_beliefstory.del_belieflink(yao_text)
    x_doerheir.set_owner_id_doer(x_beliefstorys, yao_text)

    # THEN
    assert x_doerheir._owner_id_doer is False


def test_DoerHeir_set_beliefhold_DoerUnitEmpty_ParentDoerHeirEmpty():
    # GIVEN
    x_doerheir = doerheir_shop(_beliefholds={})
    parent_doerheir_empty = doerheir_shop()
    x_doerunit = doerunit_shop()

    # WHEN
    x_doerheir.set_beliefholds(
        parent_doerheir=parent_doerheir_empty,
        doerunit=x_doerunit,
        world_beliefstorys=None,
    )

    # THEN
    x_doerheir._beliefholds = {}


def test_DoerHeir_set_beliefhold_DoerUnitNotEmpty_ParentDoerHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    x_doerunit = doerunit_shop()
    x_doerunit.set_beliefhold(belief_id=kent_text)
    x_doerunit.set_beliefhold(belief_id=swim_text)

    # WHEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_beliefholds(
        parent_doerheir=None, doerunit=x_doerunit, world_beliefstorys=None
    )

    # THEN
    assert x_doerheir._beliefholds == x_doerunit._beliefholds


def test_DoerHeir_set_beliefhold_DoerUnitNotEmpty_ParentDoerHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    x_doerunit = doerunit_shop()
    x_doerunit.set_beliefhold(belief_id=kent_text)
    x_doerunit.set_beliefhold(belief_id=swim_text)

    # WHEN
    x_doerheir = doerheir_shop()
    parent_doerheir_empty = doerheir_shop()
    x_doerheir.set_beliefholds(
        parent_doerheir_empty, doerunit=x_doerunit, world_beliefstorys=None
    )

    # THEN
    assert x_doerheir._beliefholds == x_doerunit._beliefholds


def test_DoerHeir_set_beliefhold_DoerUnitEmpty_ParentDoerHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    doerunit_swim = doerunit_shop()
    doerunit_swim.set_beliefhold(belief_id=kent_text)
    doerunit_swim.set_beliefhold(belief_id=swim_text)
    empty_doerheir = doerheir_shop()

    parent_doerheir = doerheir_shop()
    parent_doerheir.set_beliefholds(
        empty_doerheir, doerunit_swim, world_beliefstorys=None
    )

    doerunit_empty = doerunit_shop()

    # WHEN
    x_doerheir = doerheir_shop()
    assert x_doerheir._beliefholds == set()
    x_doerheir.set_beliefholds(
        parent_doerheir, doerunit=doerunit_empty, world_beliefstorys=None
    )

    # THEN
    assert len(x_doerheir._beliefholds)
    assert x_doerheir._beliefholds == parent_doerheir._beliefholds


def test_DoerHeir_set_beliefhold_DoerUnitEqualParentDoerHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    doerunit_swim = doerunit_shop()
    doerunit_swim.set_beliefhold(belief_id=kent_text)
    doerunit_swim.set_beliefhold(belief_id=swim_text)
    empty_doerheir = doerheir_shop()

    parent_doerheir = doerheir_shop()
    parent_doerheir.set_beliefholds(
        empty_doerheir, doerunit_swim, world_beliefstorys=None
    )

    # WHEN
    x_doerheir = doerheir_shop()
    assert x_doerheir._beliefholds == set()
    x_doerheir.set_beliefholds(
        parent_doerheir, doerunit=doerunit_swim, world_beliefstorys=None
    )

    # THEN
    assert x_doerheir._beliefholds == parent_doerheir._beliefholds


def test_DoerHeir_set_beliefhold_DoerUnit_NotEqual_ParentDoerHeir_NonEmpty():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_beliefstory = beliefstory_shop(yao_text)
    sue_beliefstory = beliefstory_shop(sue_text)
    bob_beliefstory = beliefstory_shop(bob_text)
    bob_beliefstory = beliefstory_shop(zia_text)
    yao_beliefstory.set_belieflink(belieflink_shop(yao_text, _char_id=yao_text))
    sue_beliefstory.set_belieflink(belieflink_shop(sue_text, _char_id=sue_text))

    swim2_text = ",swim2"
    swim2_beliefstory = beliefstory_shop(belief_id=swim2_text)
    swim2_beliefstory.set_belieflink(belieflink_shop(swim2_text, _char_id=yao_text))
    swim2_beliefstory.set_belieflink(belieflink_shop(swim2_text, _char_id=sue_text))

    swim3_text = ",swim3"
    swim3_beliefstory = beliefstory_shop(belief_id=swim3_text)
    swim3_beliefstory.set_belieflink(belieflink_shop(swim3_text, _char_id=yao_text))
    swim3_beliefstory.set_belieflink(belieflink_shop(swim3_text, _char_id=sue_text))
    swim3_beliefstory.set_belieflink(belieflink_shop(swim3_text, _char_id=zia_text))

    x_beliefstorys = {
        yao_text: yao_beliefstory,
        sue_text: sue_beliefstory,
        bob_text: bob_beliefstory,
        swim2_text: swim2_beliefstory,
        swim3_text: swim3_beliefstory,
    }

    parent_doerunit = doerunit_shop()
    parent_doerunit.set_beliefhold(belief_id=swim3_text)
    parent_doerheir = doerheir_shop()
    parent_doerheir.set_beliefholds(
        parent_doerheir=None, doerunit=parent_doerunit, world_beliefstorys=None
    )

    doerunit_swim2 = doerunit_shop()
    doerunit_swim2.set_beliefhold(belief_id=swim2_text)

    # WHEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_beliefholds(parent_doerheir, doerunit_swim2, x_beliefstorys)

    # THEN
    assert x_doerheir._beliefholds == doerunit_swim2._beliefholds
    assert len(x_doerheir._beliefholds) == 1
    assert list(x_doerheir._beliefholds) == [swim2_text]


# def test_DoerHeir_set_beliefhold_DoerUnit_NotEqualParentDoerHeir_RaisesError():
#     # GIVEN
#     yao_text = "Yao"
#     sue_text = "Sue"
#     bob_text = "Bob"
#     zia_text = "Zia"
#     yao_beliefstory = beliefstory_shop(yao_text)
#     sue_beliefstory = beliefstory_shop(sue_text)
#     bob_beliefstory = beliefstory_shop(bob_text)
#     bob_beliefstory = beliefstory_shop(zia_text)
#     yao_beliefstory.set_belieflink(belieflink_shop(yao_text))
#     sue_beliefstory.set_belieflink(belieflink_shop(sue_text))

#     swim2_text = ",swim2"
#     swim2_beliefstory = beliefstory_shop(swim2_text)
#     swim2_beliefstory.set_belieflink(belieflink_shop(swim2_text, _char_id=yao_text))
#     swim2_beliefstory.set_belieflink(belieflink_shop(swim2_text, _char_id=sue_text))

#     swim3_text = ",swim3"
#     swim3_beliefstory = beliefstory_shop(belief_id=swim3_text)
#     swim3_beliefstory.set_belieflink(belieflink_shop(swim3_text, _char_id=yao_text))
#     swim3_beliefstory.set_belieflink(belieflink_shop(swim3_text, _char_id=sue_text))
#     swim3_beliefstory.set_belieflink(belieflink_shop(swim3_text, _char_id=zia_text))

#     x_beliefstorys = {
#         yao_text: yao_beliefstory,
#         sue_text: sue_beliefstory,
#         bob_text: bob_beliefstory,
#         swim2_text: swim2_beliefstory,
#         swim3_text: swim3_beliefstory,
#     }

#     parent_doerunit = doerunit_shop()
#     parent_doerunit.set_beliefhold(swim2_text)
#     parent_doerheir = doerheir_shop()
#     parent_doerheir.set_beliefholds(None, parent_doerunit, x_beliefstorys)

#     doerunit_swim3 = doerunit_shop()
#     doerunit_swim3.set_beliefhold(belief_id=swim3_text)

#     # WHEN / THEN
#     x_doerheir = doerheir_shop()
#     all_parent_doerheir_chars = {yao_text, sue_text}
#     all_doerunit_chars = {yao_text, sue_text, zia_text}
#     with pytest_raises(Exception) as excinfo:
#         x_doerheir.set_beliefholds(parent_doerheir, doerunit_swim3, x_beliefstorys)
#     assert (
#         str(excinfo.value)
#         == f"parent_doerheir does not contain all chars of the idea's doerunit\n{set(all_parent_doerheir_chars)=}\n\n{set(all_doerunit_chars)=}"
#     )


def test_DoerUnit_get_beliefhold_ReturnsCorrectObj():
    # GIVEN
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_doerunit = doerunit_shop()
    x_doerunit.set_beliefhold(climb_text)
    x_doerunit.set_beliefhold(walk_text)
    x_doerunit.set_beliefhold(swim_text)

    # WHEN / THEN
    assert x_doerunit.get_beliefhold(walk_text) != None
    assert x_doerunit.get_beliefhold(swim_text) != None
    assert x_doerunit.get_beliefhold(run_text) is None


def test_DoerHeir_belief_id_in_ReturnsCorrectBoolWhen_beliefholdsNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text}
    hike_dict = {hike_text}
    x_doerunit = doerunit_shop()
    x_doerunit.set_beliefhold(belief_id=swim_text)
    x_doerunit.set_beliefhold(belief_id=hike_text)
    x_doerheir = doerheir_shop()
    x_doerheir.set_beliefholds(
        parent_doerheir=None, doerunit=x_doerunit, world_beliefstorys=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert swim_text in x_doerheir._beliefholds
    assert hike_text in x_doerheir._beliefholds
    print(f"{hunt_text in x_doerheir._beliefholds=}")
    assert hunt_text not in x_doerheir._beliefholds
    assert play_text not in x_doerheir._beliefholds
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_doerheir.has_belief(swim_dict)
    assert x_doerheir.has_belief(hike_dict)
    assert x_doerheir.has_belief(hunt_dict) is False
    assert x_doerheir.has_belief(hunt_hike_dict)
    assert x_doerheir.has_belief(hunt_play_dict) is False


def test_DoerHeir_has_belief_ReturnsCorrectBoolWhen_beliefholdsEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text}
    x_doerunit = doerunit_shop()
    x_doerheir = doerheir_shop()
    x_doerheir.set_beliefholds(
        parent_doerheir=None, doerunit=x_doerunit, world_beliefstorys=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert x_doerheir._beliefholds == set()
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_doerheir.has_belief(hike_dict)
    assert x_doerheir.has_belief(hunt_dict)
    assert x_doerheir.has_belief(play_dict)
    assert x_doerheir.has_belief(hunt_hike_dict)
    assert x_doerheir.has_belief(hunt_play_dict)
