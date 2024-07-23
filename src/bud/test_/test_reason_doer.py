from src._road.road import GroupID
from src.bud.reason_doer import (
    DoerUnit,
    doerunit_shop,
    DoerHeir,
    doerheir_shop,
    create_doerunit,
)
from src.bud.group import membership_shop
from src.bud.group import groupbox_shop
from pytest import raises as pytest_raises


def test_DoerUnit_exists():
    # ESTABLISH
    x_groupholds = {1}

    # WHEN
    x_doerunit = DoerUnit(_groupholds=x_groupholds)

    # THEN
    assert x_doerunit
    assert x_doerunit._groupholds == x_groupholds


def test_doerunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_groupholds = {1}

    # WHEN
    x_doerunit = doerunit_shop(_groupholds=x_groupholds)

    # THEN
    assert x_doerunit
    assert x_doerunit._groupholds == x_groupholds


def test_doerunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_doerunit = doerunit_shop()

    # THEN
    assert x_doerunit
    assert x_doerunit._groupholds == set()


def test_create_doerunit_ReturnsCorrectObj():
    # ESTABLISH
    swim_group_id = GroupID("swimmers")

    # WHEN
    swim_doerunit = create_doerunit(swim_group_id)

    # THEN
    assert swim_doerunit
    assert len(swim_doerunit._groupholds) == 1


def test_DoerUnit_get_dict_ReturnsCorrectDictWithSingle_grouphold():
    # ESTABLISH
    bob_group_id = GroupID("Bob")
    x_groupholds = {bob_group_id: bob_group_id}
    x_doerunit = doerunit_shop(_groupholds=x_groupholds)

    # WHEN
    obj_dict = x_doerunit.get_dict()

    # THEN
    assert obj_dict is not None
    example_dict = {"_groupholds": [bob_group_id]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_DoerUnit_set_grouphold_CorrectlySets_groupholds_v1():
    # ESTABLISH
    x_doerunit = doerunit_shop()
    assert len(x_doerunit._groupholds) == 0

    # WHEN
    yao_text = "Yao"
    x_doerunit.set_grouphold(group_id=yao_text)

    # THEN
    assert len(x_doerunit._groupholds) == 1


def test_DoerUnit_grouphold_exists_ReturnsCorrectObj():
    # ESTABLISH
    x_doerunit = doerunit_shop()
    yao_text = "Yao"
    assert x_doerunit.grouphold_exists(yao_text) is False

    # WHEN
    x_doerunit.set_grouphold(group_id=yao_text)

    # THEN
    assert x_doerunit.grouphold_exists(yao_text)


def test_DoerUnit_del_grouphold_CorrectlyDeletes_groupholds_v1():
    # ESTABLISH
    x_doerunit = doerunit_shop()
    yao_text = "Yao"
    sue_text = "Sue"
    x_doerunit.set_grouphold(group_id=yao_text)
    x_doerunit.set_grouphold(group_id=sue_text)
    assert len(x_doerunit._groupholds) == 2

    # WHEN
    x_doerunit.del_grouphold(group_id=sue_text)

    # THEN
    assert len(x_doerunit._groupholds) == 1


def test_DoerHeir_exists():
    # ESTABLISH
    x_groupholds = {1}
    _owner_id_x_doerunit = True

    # WHEN
    x_doerheir = DoerHeir(_groupholds=x_groupholds, _owner_id_doer=_owner_id_x_doerunit)

    # THEN
    assert x_doerheir
    assert x_doerheir._groupholds == x_groupholds
    assert x_doerheir._owner_id_doer == _owner_id_x_doerunit


def test_doerheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_groupholds = {1}
    _owner_id_x_doerunit = "example"

    # WHEN
    x_doerheir = doerheir_shop(
        _groupholds=x_groupholds, _owner_id_doer=_owner_id_x_doerunit
    )

    # THEN
    assert x_doerheir
    assert x_doerheir._groupholds == x_groupholds
    assert x_doerheir._owner_id_doer == _owner_id_x_doerunit


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_Emptyx_groupholds():
    # ESTABLISH
    x_groupholds = set()
    x_doerheir = doerheir_shop(_groupholds=x_groupholds)
    assert x_doerheir._owner_id_doer is False

    # WHEN
    bud_groupboxs = {}
    x_doerheir.set_owner_id_doer(bud_groupboxs, bud_owner_id="")

    # THEN
    assert x_doerheir._owner_id_doer


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_groupholds_v1():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    yao_groupbox = groupbox_shop(yao_text)
    sue_groupbox = groupbox_shop(sue_text)
    yao_groupbox.set_membership(membership_shop(yao_text, _acct_id=yao_text))
    sue_groupbox.set_membership(membership_shop(sue_text, _acct_id=sue_text))
    x_groupboxs = {yao_text: yao_groupbox, sue_text: sue_groupbox}
    bud_owner_id = yao_text

    x_groupholds = {yao_text}
    x_doerheir = doerheir_shop(_groupholds=x_groupholds)
    assert x_doerheir._owner_id_doer is False

    # WHEN
    x_doerheir.set_owner_id_doer(x_groupboxs, bud_owner_id)

    # THEN
    assert x_doerheir._owner_id_doer


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_groupholds_v2():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    yao_groupbox = groupbox_shop(yao_text)
    sue_groupbox = groupbox_shop(sue_text)
    yao_groupbox.set_membership(membership_shop(yao_text, _acct_id=yao_text))
    sue_groupbox.set_membership(membership_shop(sue_text, _acct_id=sue_text))
    x_groupboxs = {yao_text: yao_groupbox, sue_text: sue_groupbox}
    x_groupholds = {sue_text}
    x_doerheir = doerheir_shop(_groupholds=x_groupholds)
    assert yao_groupbox.get_membership(yao_text) is not None
    assert x_doerheir._owner_id_doer is False

    # WHEN
    x_doerheir.set_owner_id_doer(x_groupboxs, yao_text)

    # THEN
    assert x_doerheir._owner_id_doer is False


def test_DoerHeir_set_owner_id_doer_CorrectlySetsAttribute_NonEmptyx_groupholds_v3():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    bob_text = "Bob"
    yao_groupbox = groupbox_shop(yao_text)
    sue_groupbox = groupbox_shop(sue_text)
    bob_groupbox = groupbox_shop(bob_text)
    yao_groupbox.set_membership(membership_shop(yao_text, _acct_id=yao_text))
    sue_groupbox.set_membership(membership_shop(sue_text, _acct_id=sue_text))

    swim_text = ",swim"
    swim_groupbox = groupbox_shop(group_id=swim_text)
    swim_groupbox.set_membership(membership_shop(swim_text, _acct_id=yao_text))
    swim_groupbox.set_membership(membership_shop(swim_text, _acct_id=sue_text))
    x_groupboxs = {
        yao_text: yao_groupbox,
        sue_text: sue_groupbox,
        bob_text: bob_groupbox,
        swim_text: swim_groupbox,
    }

    x_groupholds = {swim_text}
    x_doerheir = doerheir_shop(_groupholds=x_groupholds)
    assert x_doerheir._owner_id_doer is False
    x_doerheir.set_owner_id_doer(x_groupboxs, bud_owner_id=yao_text)
    assert x_doerheir._owner_id_doer

    # WHEN
    swim_groupbox.del_membership(yao_text)
    x_doerheir.set_owner_id_doer(x_groupboxs, yao_text)

    # THEN
    assert x_doerheir._owner_id_doer is False


def test_DoerHeir_set_grouphold_DoerUnitEmpty_ParentDoerHeirEmpty():
    # ESTABLISH
    x_doerheir = doerheir_shop(_groupholds={})
    parent_doerheir_empty = doerheir_shop()
    x_doerunit = doerunit_shop()

    # WHEN
    x_doerheir.set_groupholds(
        parent_doerheir=parent_doerheir_empty,
        doerunit=x_doerunit,
        bud_groupboxs=None,
    )

    # THEN
    x_doerheir._groupholds = {}


def test_DoerHeir_set_grouphold_DoerUnitNotEmpty_ParentDoerHeirIsNone():
    # ESTABLISH
    kent_text = "kent"
    swim_text = ",swim"
    x_doerunit = doerunit_shop()
    x_doerunit.set_grouphold(group_id=kent_text)
    x_doerunit.set_grouphold(group_id=swim_text)

    # WHEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_groupholds(
        parent_doerheir=None, doerunit=x_doerunit, bud_groupboxs=None
    )

    # THEN
    assert x_doerheir._groupholds == x_doerunit._groupholds


def test_DoerHeir_set_grouphold_DoerUnitNotEmpty_ParentDoerHeirEmpty():
    # ESTABLISH
    kent_text = "kent"
    swim_text = ",swim"
    x_doerunit = doerunit_shop()
    x_doerunit.set_grouphold(group_id=kent_text)
    x_doerunit.set_grouphold(group_id=swim_text)

    # WHEN
    x_doerheir = doerheir_shop()
    parent_doerheir_empty = doerheir_shop()
    x_doerheir.set_groupholds(
        parent_doerheir_empty, doerunit=x_doerunit, bud_groupboxs=None
    )

    # THEN
    assert x_doerheir._groupholds == x_doerunit._groupholds


def test_DoerHeir_set_grouphold_DoerUnitEmpty_ParentDoerHeirNotEmpty():
    # ESTABLISH
    kent_text = "kent"
    swim_text = ",swim"
    doerunit_swim = doerunit_shop()
    doerunit_swim.set_grouphold(group_id=kent_text)
    doerunit_swim.set_grouphold(group_id=swim_text)
    empty_doerheir = doerheir_shop()

    parent_doerheir = doerheir_shop()
    parent_doerheir.set_groupholds(empty_doerheir, doerunit_swim, bud_groupboxs=None)

    doerunit_empty = doerunit_shop()

    # WHEN
    x_doerheir = doerheir_shop()
    assert x_doerheir._groupholds == set()
    x_doerheir.set_groupholds(
        parent_doerheir, doerunit=doerunit_empty, bud_groupboxs=None
    )

    # THEN
    assert len(x_doerheir._groupholds)
    assert x_doerheir._groupholds == parent_doerheir._groupholds


def test_DoerHeir_set_grouphold_DoerUnitEqualParentDoerHeir_NonEmpty():
    # ESTABLISH
    kent_text = "kent"
    swim_text = ",swim"
    doerunit_swim = doerunit_shop()
    doerunit_swim.set_grouphold(group_id=kent_text)
    doerunit_swim.set_grouphold(group_id=swim_text)
    empty_doerheir = doerheir_shop()

    parent_doerheir = doerheir_shop()
    parent_doerheir.set_groupholds(empty_doerheir, doerunit_swim, bud_groupboxs=None)

    # WHEN
    x_doerheir = doerheir_shop()
    assert x_doerheir._groupholds == set()
    x_doerheir.set_groupholds(
        parent_doerheir, doerunit=doerunit_swim, bud_groupboxs=None
    )

    # THEN
    assert x_doerheir._groupholds == parent_doerheir._groupholds


def test_DoerHeir_set_grouphold_DoerUnit_NotEqual_ParentDoerHeir_NonEmpty():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_groupbox = groupbox_shop(yao_text)
    sue_groupbox = groupbox_shop(sue_text)
    bob_groupbox = groupbox_shop(bob_text)
    bob_groupbox = groupbox_shop(zia_text)
    yao_groupbox.set_membership(membership_shop(yao_text, _acct_id=yao_text))
    sue_groupbox.set_membership(membership_shop(sue_text, _acct_id=sue_text))

    swim2_text = ",swim2"
    swim2_groupbox = groupbox_shop(group_id=swim2_text)
    swim2_groupbox.set_membership(membership_shop(swim2_text, _acct_id=yao_text))
    swim2_groupbox.set_membership(membership_shop(swim2_text, _acct_id=sue_text))

    swim3_text = ",swim3"
    swim3_groupbox = groupbox_shop(group_id=swim3_text)
    swim3_groupbox.set_membership(membership_shop(swim3_text, _acct_id=yao_text))
    swim3_groupbox.set_membership(membership_shop(swim3_text, _acct_id=sue_text))
    swim3_groupbox.set_membership(membership_shop(swim3_text, _acct_id=zia_text))

    x_groupboxs = {
        yao_text: yao_groupbox,
        sue_text: sue_groupbox,
        bob_text: bob_groupbox,
        swim2_text: swim2_groupbox,
        swim3_text: swim3_groupbox,
    }

    parent_doerunit = doerunit_shop()
    parent_doerunit.set_grouphold(group_id=swim3_text)
    parent_doerheir = doerheir_shop()
    parent_doerheir.set_groupholds(
        parent_doerheir=None, doerunit=parent_doerunit, bud_groupboxs=None
    )

    doerunit_swim2 = doerunit_shop()
    doerunit_swim2.set_grouphold(group_id=swim2_text)

    # WHEN
    x_doerheir = doerheir_shop()
    x_doerheir.set_groupholds(parent_doerheir, doerunit_swim2, x_groupboxs)

    # THEN
    assert x_doerheir._groupholds == doerunit_swim2._groupholds
    assert len(x_doerheir._groupholds) == 1
    assert list(x_doerheir._groupholds) == [swim2_text]


# def test_DoerHeir_set_grouphold_DoerUnit_NotEqualParentDoerHeir_RaisesError():
#     # ESTABLISH
#     yao_text = "Yao"
#     sue_text = "Sue"
#     bob_text = "Bob"
#     zia_text = "Zia"
#     yao_groupbox = groupbox_shop(yao_text)
#     sue_groupbox = groupbox_shop(sue_text)
#     bob_groupbox = groupbox_shop(bob_text)
#     bob_groupbox = groupbox_shop(zia_text)
#     yao_groupbox.set_membership(membership_shop(yao_text))
#     sue_groupbox.set_membership(membership_shop(sue_text))

#     swim2_text = ",swim2"
#     swim2_groupbox = groupbox_shop(swim2_text)
#     swim2_groupbox.set_membership(membership_shop(swim2_text, _acct_id=yao_text))
#     swim2_groupbox.set_membership(membership_shop(swim2_text, _acct_id=sue_text))

#     swim3_text = ",swim3"
#     swim3_groupbox = groupbox_shop(group_id=swim3_text)
#     swim3_groupbox.set_membership(membership_shop(swim3_text, _acct_id=yao_text))
#     swim3_groupbox.set_membership(membership_shop(swim3_text, _acct_id=sue_text))
#     swim3_groupbox.set_membership(membership_shop(swim3_text, _acct_id=zia_text))

#     x_groupboxs = {
#         yao_text: yao_groupbox,
#         sue_text: sue_groupbox,
#         bob_text: bob_groupbox,
#         swim2_text: swim2_groupbox,
#         swim3_text: swim3_groupbox,
#     }

#     parent_doerunit = doerunit_shop()
#     parent_doerunit.set_grouphold(swim2_text)
#     parent_doerheir = doerheir_shop()
#     parent_doerheir.set_groupholds(None, parent_doerunit, x_groupboxs)

#     doerunit_swim3 = doerunit_shop()
#     doerunit_swim3.set_grouphold(group_id=swim3_text)

#     # WHEN / THEN
#     x_doerheir = doerheir_shop()
#     all_parent_doerheir_accts = {yao_text, sue_text}
#     all_doerunit_accts = {yao_text, sue_text, zia_text}
#     with pytest_raises(Exception) as excinfo:
#         x_doerheir.set_groupholds(parent_doerheir, doerunit_swim3, x_groupboxs)
#     assert (
#         str(excinfo.value)
#         == f"parent_doerheir does not contain all accts of the idea's doerunit\n{set(all_parent_doerheir_accts)=}\n\n{set(all_doerunit_accts)=}"
#     )


def test_DoerUnit_get_grouphold_ReturnsCorrectObj():
    # ESTABLISH
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_doerunit = doerunit_shop()
    x_doerunit.set_grouphold(climb_text)
    x_doerunit.set_grouphold(walk_text)
    x_doerunit.set_grouphold(swim_text)

    # WHEN / THEN
    assert x_doerunit.get_grouphold(walk_text) is not None
    assert x_doerunit.get_grouphold(swim_text) is not None
    assert x_doerunit.get_grouphold(run_text) is None


def test_DoerHeir_group_id_in_ReturnsCorrectBoolWhen_groupholdsNotEmpty():
    # ESTABLISH
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text}
    hike_dict = {hike_text}
    x_doerunit = doerunit_shop()
    x_doerunit.set_grouphold(group_id=swim_text)
    x_doerunit.set_grouphold(group_id=hike_text)
    x_doerheir = doerheir_shop()
    x_doerheir.set_groupholds(
        parent_doerheir=None, doerunit=x_doerunit, bud_groupboxs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert swim_text in x_doerheir._groupholds
    assert hike_text in x_doerheir._groupholds
    print(f"{hunt_text in x_doerheir._groupholds=}")
    assert hunt_text not in x_doerheir._groupholds
    assert play_text not in x_doerheir._groupholds
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_doerheir.has_group(swim_dict)
    assert x_doerheir.has_group(hike_dict)
    assert x_doerheir.has_group(hunt_dict) is False
    assert x_doerheir.has_group(hunt_hike_dict)
    assert x_doerheir.has_group(hunt_play_dict) is False


def test_DoerHeir_has_group_ReturnsCorrectBoolWhen_groupholdsEmpty():
    # ESTABLISH
    hike_text = ",hike"
    hike_dict = {hike_text}
    x_doerunit = doerunit_shop()
    x_doerheir = doerheir_shop()
    x_doerheir.set_groupholds(
        parent_doerheir=None, doerunit=x_doerunit, bud_groupboxs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert x_doerheir._groupholds == set()
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_doerheir.has_group(hike_dict)
    assert x_doerheir.has_group(hunt_dict)
    assert x_doerheir.has_group(play_dict)
    assert x_doerheir.has_group(hunt_hike_dict)
    assert x_doerheir.has_group(hunt_play_dict)
