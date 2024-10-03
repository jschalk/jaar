from src.f1_road.road import GroupID
from src.f2_bud.reason_team import (
    TeamUnit,
    teamunit_shop,
    TeamHeir,
    teamheir_shop,
    create_teamunit,
)
from src.f2_bud.group import membership_shop
from src.f2_bud.group import groupbox_shop
from pytest import raises as pytest_raises


def test_TeamUnit_exists():
    # ESTABLISH
    x_teamlinks = {1}

    # WHEN
    x_teamunit = TeamUnit(_teamlinks=x_teamlinks)

    # THEN
    assert x_teamunit
    assert x_teamunit._teamlinks == x_teamlinks


def test_teamunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_teamlinks = {1}

    # WHEN
    x_teamunit = teamunit_shop(_teamlinks=x_teamlinks)

    # THEN
    assert x_teamunit
    assert x_teamunit._teamlinks == x_teamlinks


def test_teamunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_teamunit = teamunit_shop()

    # THEN
    assert x_teamunit
    assert x_teamunit._teamlinks == set()


def test_create_teamunit_ReturnsCorrectObj():
    # ESTABLISH
    swim_group_id = GroupID("swimmers")

    # WHEN
    swim_teamunit = create_teamunit(swim_group_id)

    # THEN
    assert swim_teamunit
    assert len(swim_teamunit._teamlinks) == 1


def test_TeamUnit_get_dict_ReturnsCorrectDictWithSingle_teamlink():
    # ESTABLISH
    bob_group_id = GroupID("Bob")
    x_teamlinks = {bob_group_id: bob_group_id}
    x_teamunit = teamunit_shop(_teamlinks=x_teamlinks)

    # WHEN
    obj_dict = x_teamunit.get_dict()

    # THEN
    assert obj_dict is not None
    example_dict = {"_teamlinks": [bob_group_id]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_TeamUnit_set_teamlink_CorrectlySets_teamlinks_v1():
    # ESTABLISH
    x_teamunit = teamunit_shop()
    assert len(x_teamunit._teamlinks) == 0

    # WHEN
    yao_str = "Yao"
    x_teamunit.set_teamlink(group_id=yao_str)

    # THEN
    assert len(x_teamunit._teamlinks) == 1


def test_TeamUnit_teamlink_exists_ReturnsCorrectObj():
    # ESTABLISH
    x_teamunit = teamunit_shop()
    yao_str = "Yao"
    assert x_teamunit.teamlink_exists(yao_str) is False

    # WHEN
    x_teamunit.set_teamlink(group_id=yao_str)

    # THEN
    assert x_teamunit.teamlink_exists(yao_str)


def test_TeamUnit_del_teamlink_CorrectlyDeletes_teamlinks_v1():
    # ESTABLISH
    x_teamunit = teamunit_shop()
    yao_str = "Yao"
    sue_str = "Sue"
    x_teamunit.set_teamlink(group_id=yao_str)
    x_teamunit.set_teamlink(group_id=sue_str)
    assert len(x_teamunit._teamlinks) == 2

    # WHEN
    x_teamunit.del_teamlink(group_id=sue_str)

    # THEN
    assert len(x_teamunit._teamlinks) == 1


def test_TeamHeir_exists():
    # ESTABLISH
    x_teamlinks = {1}
    _owner_id_x_teamunit = True

    # WHEN
    x_teamheir = TeamHeir(_teamlinks=x_teamlinks, _owner_id_team=_owner_id_x_teamunit)

    # THEN
    assert x_teamheir
    assert x_teamheir._teamlinks == x_teamlinks
    assert x_teamheir._owner_id_team == _owner_id_x_teamunit


def test_teamheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_teamlinks = {1}
    _owner_id_x_teamunit = "example"

    # WHEN
    x_teamheir = teamheir_shop(
        _teamlinks=x_teamlinks, _owner_id_team=_owner_id_x_teamunit
    )

    # THEN
    assert x_teamheir
    assert x_teamheir._teamlinks == x_teamlinks
    assert x_teamheir._owner_id_team == _owner_id_x_teamunit


def test_TeamHeir_set_owner_id_team_CorrectlySetsAttribute_Emptyx_teamlinks():
    # ESTABLISH
    x_teamlinks = set()
    x_teamheir = teamheir_shop(_teamlinks=x_teamlinks)
    assert x_teamheir._owner_id_team is False

    # WHEN
    bud_groupboxs = {}
    x_teamheir.set_owner_id_team(bud_groupboxs, bud_owner_id="")

    # THEN
    assert x_teamheir._owner_id_team


def test_TeamHeir_set_owner_id_team_CorrectlySetsAttribute_NonEmptyx_teamlinks_v1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_groupbox = groupbox_shop(yao_str)
    sue_groupbox = groupbox_shop(sue_str)
    yao_groupbox.set_membership(membership_shop(yao_str, _acct_id=yao_str))
    sue_groupbox.set_membership(membership_shop(sue_str, _acct_id=sue_str))
    x_groupboxs = {yao_str: yao_groupbox, sue_str: sue_groupbox}
    bud_owner_id = yao_str

    x_teamlinks = {yao_str}
    x_teamheir = teamheir_shop(_teamlinks=x_teamlinks)
    assert x_teamheir._owner_id_team is False

    # WHEN
    x_teamheir.set_owner_id_team(x_groupboxs, bud_owner_id)

    # THEN
    assert x_teamheir._owner_id_team


def test_TeamHeir_set_owner_id_team_CorrectlySetsAttribute_NonEmptyx_teamlinks_v2():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_groupbox = groupbox_shop(yao_str)
    sue_groupbox = groupbox_shop(sue_str)
    yao_groupbox.set_membership(membership_shop(yao_str, _acct_id=yao_str))
    sue_groupbox.set_membership(membership_shop(sue_str, _acct_id=sue_str))
    x_groupboxs = {yao_str: yao_groupbox, sue_str: sue_groupbox}
    x_teamlinks = {sue_str}
    x_teamheir = teamheir_shop(_teamlinks=x_teamlinks)
    assert yao_groupbox.get_membership(yao_str) is not None
    assert x_teamheir._owner_id_team is False

    # WHEN
    x_teamheir.set_owner_id_team(x_groupboxs, yao_str)

    # THEN
    assert x_teamheir._owner_id_team is False


def test_TeamHeir_set_owner_id_team_CorrectlySetsAttribute_NonEmptyx_teamlinks_v3():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    yao_groupbox = groupbox_shop(yao_str)
    sue_groupbox = groupbox_shop(sue_str)
    bob_groupbox = groupbox_shop(bob_str)
    yao_groupbox.set_membership(membership_shop(yao_str, _acct_id=yao_str))
    sue_groupbox.set_membership(membership_shop(sue_str, _acct_id=sue_str))

    swim_str = ",swim"
    swim_groupbox = groupbox_shop(group_id=swim_str)
    swim_groupbox.set_membership(membership_shop(swim_str, _acct_id=yao_str))
    swim_groupbox.set_membership(membership_shop(swim_str, _acct_id=sue_str))
    x_groupboxs = {
        yao_str: yao_groupbox,
        sue_str: sue_groupbox,
        bob_str: bob_groupbox,
        swim_str: swim_groupbox,
    }

    x_teamlinks = {swim_str}
    x_teamheir = teamheir_shop(_teamlinks=x_teamlinks)
    assert x_teamheir._owner_id_team is False
    x_teamheir.set_owner_id_team(x_groupboxs, bud_owner_id=yao_str)
    assert x_teamheir._owner_id_team

    # WHEN
    swim_groupbox.del_membership(yao_str)
    x_teamheir.set_owner_id_team(x_groupboxs, yao_str)

    # THEN
    assert x_teamheir._owner_id_team is False


def test_TeamHeir_set_teamlink_TeamUnit_Empty_ParentTeamHeirEmpty():
    # ESTABLISH
    x_teamheir = teamheir_shop(_teamlinks={})
    parent_teamheir_empty = teamheir_shop()
    x_teamunit = teamunit_shop()

    # WHEN
    x_teamheir.set_teamlinks(
        parent_teamheir=parent_teamheir_empty,
        teamunit=x_teamunit,
        bud_groupboxs=None,
    )

    # THEN
    x_teamheir._teamlinks = {}


def test_TeamHeir_set_teamlink_TeamUnitNotEmpty_ParentTeamHeirIsNone():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(group_id=kent_str)
    x_teamunit.set_teamlink(group_id=swim_str)

    # WHEN
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(None, teamunit=x_teamunit, bud_groupboxs=None)

    # THEN
    assert x_teamheir._teamlinks == x_teamunit._teamlinks


def test_TeamHeir_set_teamlink_TeamUnitNotEmpty_ParentTeamHeirEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(group_id=kent_str)
    x_teamunit.set_teamlink(group_id=swim_str)

    # WHEN
    x_teamheir = teamheir_shop()
    parent_teamheir_empty = teamheir_shop()
    x_teamheir.set_teamlinks(parent_teamheir_empty, x_teamunit, bud_groupboxs=None)

    # THEN
    assert x_teamheir._teamlinks == x_teamunit._teamlinks


def test_TeamHeir_set_teamlink_TeamUnit_Empty_ParentTeamHeirNotEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    teamunit_swim = teamunit_shop()
    teamunit_swim.set_teamlink(group_id=kent_str)
    teamunit_swim.set_teamlink(group_id=swim_str)
    empty_teamheir = teamheir_shop()

    parent_teamheir = teamheir_shop()
    parent_teamheir.set_teamlinks(empty_teamheir, teamunit_swim, bud_groupboxs=None)

    teamunit_empty = teamunit_shop()

    # WHEN
    x_teamheir = teamheir_shop()
    assert x_teamheir._teamlinks == set()
    x_teamheir.set_teamlinks(parent_teamheir, teamunit_empty, bud_groupboxs=None)

    # THEN
    assert len(x_teamheir._teamlinks)
    assert x_teamheir._teamlinks == parent_teamheir._teamlinks


def test_TeamHeir_set_teamlink_TeamUnitEqualParentTeamHeir_NonEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    teamunit_swim = teamunit_shop()
    teamunit_swim.set_teamlink(group_id=kent_str)
    teamunit_swim.set_teamlink(group_id=swim_str)
    empty_teamheir = teamheir_shop()

    parent_teamheir = teamheir_shop()
    parent_teamheir.set_teamlinks(empty_teamheir, teamunit_swim, bud_groupboxs=None)

    # WHEN
    x_teamheir = teamheir_shop()
    assert x_teamheir._teamlinks == set()
    x_teamheir.set_teamlinks(parent_teamheir, teamunit_swim, bud_groupboxs=None)

    # THEN
    assert x_teamheir._teamlinks == parent_teamheir._teamlinks


def test_TeamHeir_set_teamlink_TeamUnit_NotEqual_ParentTeamHeir_NonEmpty():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_groupbox = groupbox_shop(yao_str)
    sue_groupbox = groupbox_shop(sue_str)
    bob_groupbox = groupbox_shop(bob_str)
    bob_groupbox = groupbox_shop(zia_str)
    yao_groupbox.set_membership(membership_shop(yao_str, _acct_id=yao_str))
    sue_groupbox.set_membership(membership_shop(sue_str, _acct_id=sue_str))

    swim2_str = ",swim2"
    swim2_groupbox = groupbox_shop(group_id=swim2_str)
    swim2_groupbox.set_membership(membership_shop(swim2_str, _acct_id=yao_str))
    swim2_groupbox.set_membership(membership_shop(swim2_str, _acct_id=sue_str))

    swim3_str = ",swim3"
    swim3_groupbox = groupbox_shop(group_id=swim3_str)
    swim3_groupbox.set_membership(membership_shop(swim3_str, _acct_id=yao_str))
    swim3_groupbox.set_membership(membership_shop(swim3_str, _acct_id=sue_str))
    swim3_groupbox.set_membership(membership_shop(swim3_str, _acct_id=zia_str))

    x_groupboxs = {
        yao_str: yao_groupbox,
        sue_str: sue_groupbox,
        bob_str: bob_groupbox,
        swim2_str: swim2_groupbox,
        swim3_str: swim3_groupbox,
    }

    parent_teamunit = teamunit_shop()
    parent_teamunit.set_teamlink(group_id=swim3_str)
    parent_teamheir = teamheir_shop()
    parent_teamheir.set_teamlinks(
        parent_teamheir=None, teamunit=parent_teamunit, bud_groupboxs=None
    )

    teamunit_swim2 = teamunit_shop()
    teamunit_swim2.set_teamlink(group_id=swim2_str)

    # WHEN
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(parent_teamheir, teamunit_swim2, x_groupboxs)

    # THEN
    assert x_teamheir._teamlinks == teamunit_swim2._teamlinks
    assert len(x_teamheir._teamlinks) == 1
    assert list(x_teamheir._teamlinks) == [swim2_str]


# def test_TeamHeir_set_teamlink_TeamUnit_NotEqualParentTeamHeir_RaisesError():
#     # ESTABLISH
#     yao_str = "Yao"
#     sue_str = "Sue"
#     bob_str = "Bob"
#     zia_str = "Zia"
#     yao_groupbox = groupbox_shop(yao_str)
#     sue_groupbox = groupbox_shop(sue_str)
#     bob_groupbox = groupbox_shop(bob_str)
#     bob_groupbox = groupbox_shop(zia_str)
#     yao_groupbox.set_membership(membership_shop(yao_str))
#     sue_groupbox.set_membership(membership_shop(sue_str))

#     swim2_str = ",swim2"
#     swim2_groupbox = groupbox_shop(swim2_str)
#     swim2_groupbox.set_membership(membership_shop(swim2_str, _acct_id=yao_str))
#     swim2_groupbox.set_membership(membership_shop(swim2_str, _acct_id=sue_str))

#     swim3_str = ",swim3"
#     swim3_groupbox = groupbox_shop(group_id=swim3_str)
#     swim3_groupbox.set_membership(membership_shop(swim3_str, _acct_id=yao_str))
#     swim3_groupbox.set_membership(membership_shop(swim3_str, _acct_id=sue_str))
#     swim3_groupbox.set_membership(membership_shop(swim3_str, _acct_id=zia_str))

#     x_groupboxs = {
#         yao_str: yao_groupbox,
#         sue_str: sue_groupbox,
#         bob_str: bob_groupbox,
#         swim2_str: swim2_groupbox,
#         swim3_str: swim3_groupbox,
#     }

#     parent_teamunit = teamunit_shop()
#     parent_teamunit.set_teamlink(swim2_str)
#     parent_teamheir = teamheir_shop()
#     parent_teamheir.set_teamlinks(None, parent_teamunit, x_groupboxs)

#     teamunit_swim3 = teamunit_shop()
#     teamunit_swim3.set_teamlink(group_id=swim3_str)

#     # WHEN / THEN
#     x_teamheir = teamheir_shop()
#     all_parent_teamheir_accts = {yao_str, sue_str}
#     all_teamunit_accts = {yao_str, sue_str, zia_str}
#     with pytest_raises(Exception) as excinfo:
#         x_teamheir.set_teamlinks(parent_teamheir, teamunit_swim3, x_groupboxs)
#     assert (
#         str(excinfo.value)
#         == f"parent_teamheir does not contain all accts of the idea's teamunit\n{set(all_parent_teamheir_accts)=}\n\n{set(all_teamunit_accts)=}"
#     )


def test_TeamUnit_get_teamlink_ReturnsCorrectObj():
    # ESTABLISH
    climb_str = ",climbers"
    hike_str = ",hikers"
    swim_str = ";swimmers"
    run_str = ";runners"

    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(climb_str)
    x_teamunit.set_teamlink(hike_str)
    x_teamunit.set_teamlink(swim_str)

    # WHEN / THEN
    assert x_teamunit.get_teamlink(hike_str) is not None
    assert x_teamunit.get_teamlink(swim_str) is not None
    assert x_teamunit.get_teamlink(run_str) is None


def test_TeamHeir_group_id_in_ReturnsCorrectBoolWhen_teamlinksNotEmpty():
    # ESTABLISH
    swim_str = ",swim"
    hike_str = ",hike"
    swim_dict = {swim_str}
    hike_dict = {hike_str}
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(group_id=swim_str)
    x_teamunit.set_teamlink(group_id=hike_str)
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None, teamunit=x_teamunit, bud_groupboxs=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert swim_str in x_teamheir._teamlinks
    assert hike_str in x_teamheir._teamlinks
    print(f"{hunt_str in x_teamheir._teamlinks=}")
    assert hunt_str not in x_teamheir._teamlinks
    assert play_str not in x_teamheir._teamlinks
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert x_teamheir.has_group(swim_dict)
    assert x_teamheir.has_group(hike_dict)
    assert x_teamheir.has_group(hunt_dict) is False
    assert x_teamheir.has_group(hunt_hike_dict)
    assert x_teamheir.has_group(hunt_play_dict) is False


def test_TeamHeir_has_group_ReturnsCorrectBoolWhen_teamlinksEmpty():
    # ESTABLISH
    hike_str = ",hike"
    hike_dict = {hike_str}
    x_teamunit = teamunit_shop()
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None, teamunit=x_teamunit, bud_groupboxs=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert x_teamheir._teamlinks == set()
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert x_teamheir.has_group(hike_dict)
    assert x_teamheir.has_group(hunt_dict)
    assert x_teamheir.has_group(play_dict)
    assert x_teamheir.has_group(hunt_hike_dict)
    assert x_teamheir.has_group(hunt_play_dict)
