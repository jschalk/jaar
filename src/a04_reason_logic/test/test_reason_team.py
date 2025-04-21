from src.a01_word_logic.road import GroupLabel
from src.a04_reason_logic.reason_team import (
    TeamUnit,
    teamunit_shop,
    TeamHeir,
    teamheir_shop,
    create_teamunit,
)
from src.a03_group_logic.group import membership_shop
from src.a03_group_logic.group import groupunit_shop
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


def test_create_teamunit_ReturnsObj():
    # ESTABLISH
    swim_team_title = GroupLabel("swimmers")

    # WHEN
    swim_teamunit = create_teamunit(swim_team_title)

    # THEN
    assert swim_teamunit
    assert len(swim_teamunit._teamlinks) == 1


def test_TeamUnit_get_dict_ReturnsCorrectDictWithSingle_teamlink():
    # ESTABLISH
    bob_team_title = GroupLabel("Bob")
    x_teamlinks = {bob_team_title: bob_team_title}
    x_teamunit = teamunit_shop(_teamlinks=x_teamlinks)

    # WHEN
    obj_dict = x_teamunit.get_dict()

    # THEN
    assert obj_dict is not None
    example_dict = {"_teamlinks": [bob_team_title]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_TeamUnit_set_teamlink_CorrectlySets_teamlinks_v1():
    # ESTABLISH
    x_teamunit = teamunit_shop()
    assert len(x_teamunit._teamlinks) == 0

    # WHEN
    yao_str = "Yao"
    x_teamunit.set_teamlink(team_title=yao_str)

    # THEN
    assert len(x_teamunit._teamlinks) == 1


def test_TeamUnit_teamlink_exists_ReturnsObj():
    # ESTABLISH
    x_teamunit = teamunit_shop()
    yao_str = "Yao"
    assert x_teamunit.teamlink_exists(yao_str) is False

    # WHEN
    x_teamunit.set_teamlink(team_title=yao_str)

    # THEN
    assert x_teamunit.teamlink_exists(yao_str)


def test_TeamUnit_del_teamlink_CorrectlyDeletes_teamlinks_v1():
    # ESTABLISH
    x_teamunit = teamunit_shop()
    yao_str = "Yao"
    sue_str = "Sue"
    x_teamunit.set_teamlink(team_title=yao_str)
    x_teamunit.set_teamlink(team_title=sue_str)
    assert len(x_teamunit._teamlinks) == 2

    # WHEN
    x_teamunit.del_teamlink(team_title=sue_str)

    # THEN
    assert len(x_teamunit._teamlinks) == 1


def test_TeamHeir_exists():
    # ESTABLISH
    x_teamlinks = {1}
    _owner_name_x_teamunit = True

    # WHEN
    x_teamheir = TeamHeir(
        _teamlinks=x_teamlinks, _owner_name_team=_owner_name_x_teamunit
    )

    # THEN
    assert x_teamheir
    assert x_teamheir._teamlinks == x_teamlinks
    assert x_teamheir._owner_name_team == _owner_name_x_teamunit


def test_teamheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_teamlinks = {1}
    _owner_name_x_teamunit = "example"

    # WHEN
    x_teamheir = teamheir_shop(
        _teamlinks=x_teamlinks, _owner_name_team=_owner_name_x_teamunit
    )

    # THEN
    assert x_teamheir
    assert x_teamheir._teamlinks == x_teamlinks
    assert x_teamheir._owner_name_team == _owner_name_x_teamunit


def test_TeamHeir_set_owner_name_team_CorrectlySetsAttribute_Emptyx_teamlinks():
    # ESTABLISH
    x_teamlinks = set()
    x_teamheir = teamheir_shop(_teamlinks=x_teamlinks)
    assert x_teamheir._owner_name_team is False

    # WHEN
    bud_groupunits = {}
    x_teamheir.set_owner_name_team(bud_groupunits, bud_owner_name="")

    # THEN
    assert x_teamheir._owner_name_team


def test_TeamHeir_set_owner_name_team_CorrectlySetsAttribute_NonEmptyx_teamlinks_v1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    yao_groupunit.set_membership(membership_shop(yao_str, acct_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, acct_name=sue_str))
    x_groupunits = {yao_str: yao_groupunit, sue_str: sue_groupunit}
    bud_owner_name = yao_str

    x_teamlinks = {yao_str}
    x_teamheir = teamheir_shop(_teamlinks=x_teamlinks)
    assert x_teamheir._owner_name_team is False

    # WHEN
    x_teamheir.set_owner_name_team(x_groupunits, bud_owner_name)

    # THEN
    assert x_teamheir._owner_name_team


def test_TeamHeir_set_owner_name_team_CorrectlySetsAttribute_NonEmptyx_teamlinks_v2():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    yao_groupunit.set_membership(membership_shop(yao_str, acct_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, acct_name=sue_str))
    x_groupunits = {yao_str: yao_groupunit, sue_str: sue_groupunit}
    x_teamlinks = {sue_str}
    x_teamheir = teamheir_shop(_teamlinks=x_teamlinks)
    assert yao_groupunit.get_membership(yao_str) is not None
    assert x_teamheir._owner_name_team is False

    # WHEN
    x_teamheir.set_owner_name_team(x_groupunits, yao_str)

    # THEN
    assert x_teamheir._owner_name_team is False


def test_TeamHeir_set_owner_name_team_CorrectlySetsAttribute_NonEmptyx_teamlinks_v3():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    bob_groupunit = groupunit_shop(bob_str)
    yao_groupunit.set_membership(membership_shop(yao_str, acct_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, acct_name=sue_str))

    swim_str = ",swim"
    swim_groupunit = groupunit_shop(group_label=swim_str)
    swim_groupunit.set_membership(membership_shop(swim_str, acct_name=yao_str))
    swim_groupunit.set_membership(membership_shop(swim_str, acct_name=sue_str))
    x_groupunits = {
        yao_str: yao_groupunit,
        sue_str: sue_groupunit,
        bob_str: bob_groupunit,
        swim_str: swim_groupunit,
    }

    x_teamlinks = {swim_str}
    x_teamheir = teamheir_shop(_teamlinks=x_teamlinks)
    assert x_teamheir._owner_name_team is False
    x_teamheir.set_owner_name_team(x_groupunits, bud_owner_name=yao_str)
    assert x_teamheir._owner_name_team

    # WHEN
    swim_groupunit.del_membership(yao_str)
    x_teamheir.set_owner_name_team(x_groupunits, yao_str)

    # THEN
    assert x_teamheir._owner_name_team is False


def test_TeamHeir_set_teamlink_TeamUnit_Empty_ParentTeamHeirEmpty():
    # ESTABLISH
    x_teamheir = teamheir_shop(_teamlinks={})
    parent_teamheir_empty = teamheir_shop()
    x_teamunit = teamunit_shop()

    # WHEN
    x_teamheir.set_teamlinks(
        parent_teamheir=parent_teamheir_empty,
        teamunit=x_teamunit,
        bud_groupunits=None,
    )

    # THEN
    x_teamheir._teamlinks = {}


def test_TeamHeir_set_teamlink_TeamUnitNotEmpty_ParentTeamHeirIsNone():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(team_title=kent_str)
    x_teamunit.set_teamlink(team_title=swim_str)

    # WHEN
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(None, teamunit=x_teamunit, bud_groupunits=None)

    # THEN
    assert x_teamheir._teamlinks == x_teamunit._teamlinks


def test_TeamHeir_set_teamlink_TeamUnitNotEmpty_ParentTeamHeirEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(team_title=kent_str)
    x_teamunit.set_teamlink(team_title=swim_str)

    # WHEN
    x_teamheir = teamheir_shop()
    parent_teamheir_empty = teamheir_shop()
    x_teamheir.set_teamlinks(parent_teamheir_empty, x_teamunit, bud_groupunits=None)

    # THEN
    assert x_teamheir._teamlinks == x_teamunit._teamlinks


def test_TeamHeir_set_teamlink_TeamUnit_Empty_ParentTeamHeirNotEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    teamunit_swim = teamunit_shop()
    teamunit_swim.set_teamlink(team_title=kent_str)
    teamunit_swim.set_teamlink(team_title=swim_str)
    empty_teamheir = teamheir_shop()

    parent_teamheir = teamheir_shop()
    parent_teamheir.set_teamlinks(empty_teamheir, teamunit_swim, bud_groupunits=None)

    teamunit_empty = teamunit_shop()

    # WHEN
    x_teamheir = teamheir_shop()
    assert x_teamheir._teamlinks == set()
    x_teamheir.set_teamlinks(parent_teamheir, teamunit_empty, bud_groupunits=None)

    # THEN
    assert len(x_teamheir._teamlinks)
    assert x_teamheir._teamlinks == parent_teamheir._teamlinks


def test_TeamHeir_set_teamlink_TeamUnitEqualParentTeamHeir_NonEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    teamunit_swim = teamunit_shop()
    teamunit_swim.set_teamlink(team_title=kent_str)
    teamunit_swim.set_teamlink(team_title=swim_str)
    empty_teamheir = teamheir_shop()

    parent_teamheir = teamheir_shop()
    parent_teamheir.set_teamlinks(empty_teamheir, teamunit_swim, bud_groupunits=None)

    # WHEN
    x_teamheir = teamheir_shop()
    assert x_teamheir._teamlinks == set()
    x_teamheir.set_teamlinks(parent_teamheir, teamunit_swim, bud_groupunits=None)

    # THEN
    assert x_teamheir._teamlinks == parent_teamheir._teamlinks


def test_TeamHeir_set_teamlink_TeamUnit_NotEqual_ParentTeamHeir_NonEmpty():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    bob_groupunit = groupunit_shop(bob_str)
    bob_groupunit = groupunit_shop(zia_str)
    yao_groupunit.set_membership(membership_shop(yao_str, acct_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, acct_name=sue_str))

    swim2_str = ",swim2"
    swim2_groupunit = groupunit_shop(group_label=swim2_str)
    swim2_groupunit.set_membership(membership_shop(swim2_str, acct_name=yao_str))
    swim2_groupunit.set_membership(membership_shop(swim2_str, acct_name=sue_str))

    swim3_str = ",swim3"
    swim3_groupunit = groupunit_shop(group_label=swim3_str)
    swim3_groupunit.set_membership(membership_shop(swim3_str, acct_name=yao_str))
    swim3_groupunit.set_membership(membership_shop(swim3_str, acct_name=sue_str))
    swim3_groupunit.set_membership(membership_shop(swim3_str, acct_name=zia_str))

    x_groupunits = {
        yao_str: yao_groupunit,
        sue_str: sue_groupunit,
        bob_str: bob_groupunit,
        swim2_str: swim2_groupunit,
        swim3_str: swim3_groupunit,
    }

    parent_teamunit = teamunit_shop()
    parent_teamunit.set_teamlink(team_title=swim3_str)
    parent_teamheir = teamheir_shop()
    parent_teamheir.set_teamlinks(
        parent_teamheir=None, teamunit=parent_teamunit, bud_groupunits=None
    )

    teamunit_swim2 = teamunit_shop()
    teamunit_swim2.set_teamlink(team_title=swim2_str)

    # WHEN
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(parent_teamheir, teamunit_swim2, x_groupunits)

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
#     yao_groupunit = groupunit_shop(yao_str)
#     sue_groupunit = groupunit_shop(sue_str)
#     bob_groupunit = groupunit_shop(bob_str)
#     bob_groupunit = groupunit_shop(zia_str)
#     yao_groupunit.set_membership(membership_shop(yao_str))
#     sue_groupunit.set_membership(membership_shop(sue_str))

#     swim2_str = ",swim2"
#     swim2_groupunit = groupunit_shop(swim2_str)
#     swim2_groupunit.set_membership(membership_shop(swim2_str, acct_name=yao_str))
#     swim2_groupunit.set_membership(membership_shop(swim2_str, acct_name=sue_str))

#     swim3_str = ",swim3"
#     swim3_groupunit = groupunit_shop(team_title=swim3_str)
#     swim3_groupunit.set_membership(membership_shop(swim3_str, acct_name=yao_str))
#     swim3_groupunit.set_membership(membership_shop(swim3_str, acct_name=sue_str))
#     swim3_groupunit.set_membership(membership_shop(swim3_str, acct_name=zia_str))

#     x_groupunits = {
#         yao_str: yao_groupunit,
#         sue_str: sue_groupunit,
#         bob_str: bob_groupunit,
#         swim2_str: swim2_groupunit,
#         swim3_str: swim3_groupunit,
#     }

#     parent_teamunit = teamunit_shop()
#     parent_teamunit.set_teamlink(swim2_str)
#     parent_teamheir = teamheir_shop()
#     parent_teamheir.set_teamlinks(None, parent_teamunit, x_groupunits)

#     teamunit_swim3 = teamunit_shop()
#     teamunit_swim3.set_teamlink(team_title=swim3_str)

#     # WHEN / THEN
#     x_teamheir = teamheir_shop()
#     all_parent_teamheir_accts = {yao_str, sue_str}
#     all_teamunit_accts = {yao_str, sue_str, zia_str}
#     with pytest_raises(Exception) as excinfo:
#         x_teamheir.set_teamlinks(parent_teamheir, teamunit_swim3, x_groupunits)
#     assert (
#         str(excinfo.value)
#         == f"parent_teamheir does not contain all accts of the item's teamunit\n{set(all_parent_teamheir_accts)=}\n\n{set(all_teamunit_accts)=}"
#     )


def test_TeamUnit_get_teamlink_ReturnsObj():
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


def test_TeamHeir_team_title_in_ReturnsCorrectBoolWhen_teamlinksNotEmpty():
    # ESTABLISH
    swim_str = ",swim"
    hike_str = ",hike"
    swim_dict = {swim_str}
    hike_dict = {hike_str}
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(team_title=swim_str)
    x_teamunit.set_teamlink(team_title=hike_str)
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None, teamunit=x_teamunit, bud_groupunits=None
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
    assert x_teamheir.has_team(swim_dict)
    assert x_teamheir.has_team(hike_dict)
    assert x_teamheir.has_team(hunt_dict) is False
    assert x_teamheir.has_team(hunt_hike_dict)
    assert x_teamheir.has_team(hunt_play_dict) is False


def test_TeamHeir_has_team_ReturnsCorrectBoolWhen_teamlinksEmpty():
    # ESTABLISH
    hike_str = ",hike"
    hike_dict = {hike_str}
    x_teamunit = teamunit_shop()
    x_teamheir = teamheir_shop()
    x_teamheir.set_teamlinks(
        parent_teamheir=None, teamunit=x_teamunit, bud_groupunits=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert x_teamheir._teamlinks == set()
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert x_teamheir.has_team(hike_dict)
    assert x_teamheir.has_team(hunt_dict)
    assert x_teamheir.has_team(play_dict)
    assert x_teamheir.has_team(hunt_hike_dict)
    assert x_teamheir.has_team(hunt_play_dict)
