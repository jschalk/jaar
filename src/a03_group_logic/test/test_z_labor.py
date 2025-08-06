from src.a01_term_logic.term import GroupTitle
from src.a03_group_logic.group import groupunit_shop, membership_shop
from src.a03_group_logic.labor import (
    LaborHeir,
    LaborUnit,
    create_laborunit,
    laborheir_shop,
    laborunit_shop,
)
from src.a04_reason_logic.test._util.a04_str import knot_str


def test_LaborUnit_exists():
    # ESTABLISH
    x_laborlinks = {1}

    # WHEN
    x_laborunit = LaborUnit(_laborlinks=x_laborlinks)

    # THEN
    assert x_laborunit
    assert x_laborunit._laborlinks == x_laborlinks
    obj_attrs = set(x_laborunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {"_laborlinks"}


def test_laborunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_laborlinks = {1}

    # WHEN
    x_laborunit = laborunit_shop(_laborlinks=x_laborlinks)

    # THEN
    assert x_laborunit
    assert x_laborunit._laborlinks == x_laborlinks


def test_laborunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_laborunit = laborunit_shop()

    # THEN
    assert x_laborunit
    assert x_laborunit._laborlinks == set()


def test_create_laborunit_ReturnsObj():
    # ESTABLISH
    swim_labor_title = GroupTitle("swimmers")

    # WHEN
    swim_laborunit = create_laborunit(swim_labor_title)

    # THEN
    assert swim_laborunit
    assert len(swim_laborunit._laborlinks) == 1


def test_LaborUnit_get_dict_ReturnsCorrectDictWithSingle_laborlink():
    # ESTABLISH
    bob_labor_title = GroupTitle("Bob")
    x_laborlinks = {bob_labor_title: bob_labor_title}
    x_laborunit = laborunit_shop(_laborlinks=x_laborlinks)

    # WHEN
    obj_dict = x_laborunit.to_dict()

    # THEN
    assert obj_dict is not None
    example_dict = {"_laborlinks": [bob_labor_title]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_LaborUnit_set_laborlink_CorrectlySets_laborlinks_v1():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    assert len(x_laborunit._laborlinks) == 0

    # WHEN
    yao_str = "Yao"
    x_laborunit.set_laborlink(labor_title=yao_str)

    # THEN
    assert len(x_laborunit._laborlinks) == 1


def test_LaborUnit_laborlink_exists_ReturnsObj():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    yao_str = "Yao"
    assert x_laborunit.laborlink_exists(yao_str) is False

    # WHEN
    x_laborunit.set_laborlink(labor_title=yao_str)

    # THEN
    assert x_laborunit.laborlink_exists(yao_str)


def test_LaborUnit_del_laborlink_CorrectlyDeletes_laborlinks_v1():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    yao_str = "Yao"
    sue_str = "Sue"
    x_laborunit.set_laborlink(labor_title=yao_str)
    x_laborunit.set_laborlink(labor_title=sue_str)
    assert len(x_laborunit._laborlinks) == 2

    # WHEN
    x_laborunit.del_laborlink(labor_title=sue_str)

    # THEN
    assert len(x_laborunit._laborlinks) == 1


def test_LaborHeir_exists():
    # ESTABLISH
    x_laborlinks = {1}
    _believer_name_x_laborunit = True

    # WHEN
    x_laborheir = LaborHeir(
        _laborlinks=x_laborlinks, _believer_name_is_labor=_believer_name_x_laborunit
    )

    # THEN
    assert x_laborheir
    assert x_laborheir._laborlinks == x_laborlinks
    assert x_laborheir._believer_name_is_labor == _believer_name_x_laborunit
    obj_attrs = set(x_laborheir.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {"_laborlinks", "_believer_name_is_labor"}


def test_laborheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # ESTABLISH
    x_laborlinks = {1}
    _believer_name_x_laborunit = "example"

    # WHEN
    x_laborheir = laborheir_shop(
        _laborlinks=x_laborlinks, _believer_name_is_labor=_believer_name_x_laborunit
    )

    # THEN
    assert x_laborheir
    assert x_laborheir._laborlinks == x_laborlinks
    assert x_laborheir._believer_name_is_labor == _believer_name_x_laborunit


def test_LaborHeir_set_believer_name_is_labor_CorrectlySetsAttribute_Emptyx_laborlinks():
    # ESTABLISH
    x_laborlinks = set()
    x_laborheir = laborheir_shop(_laborlinks=x_laborlinks)
    assert x_laborheir._believer_name_is_labor is False

    # WHEN
    groupunits = {}
    x_laborheir.set_believer_name_is_labor(groupunits, believer_believer_name="")

    # THEN
    assert x_laborheir._believer_name_is_labor


def test_LaborHeir_set_believer_name_is_labor_CorrectlySetsAttribute_NonEmptyx_laborlinks_v1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    yao_groupunit.set_membership(membership_shop(yao_str, partner_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, partner_name=sue_str))
    x_groupunits = {yao_str: yao_groupunit, sue_str: sue_groupunit}
    believer_believer_name = yao_str

    x_laborlinks = {yao_str}
    x_laborheir = laborheir_shop(_laborlinks=x_laborlinks)
    assert x_laborheir._believer_name_is_labor is False

    # WHEN
    x_laborheir.set_believer_name_is_labor(x_groupunits, believer_believer_name)

    # THEN
    assert x_laborheir._believer_name_is_labor


def test_LaborHeir_set_believer_name_is_labor_CorrectlySetsAttribute_NonEmptyx_laborlinks_v2():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    yao_groupunit.set_membership(membership_shop(yao_str, partner_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, partner_name=sue_str))
    x_groupunits = {yao_str: yao_groupunit, sue_str: sue_groupunit}
    x_laborlinks = {sue_str}
    x_laborheir = laborheir_shop(_laborlinks=x_laborlinks)
    assert yao_groupunit.get_membership(yao_str) is not None
    assert x_laborheir._believer_name_is_labor is False

    # WHEN
    x_laborheir.set_believer_name_is_labor(x_groupunits, yao_str)

    # THEN
    assert x_laborheir._believer_name_is_labor is False


def test_LaborHeir_set_believer_name_is_labor_CorrectlySetsAttribute_NonEmptyx_laborlinks_v3():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    bob_groupunit = groupunit_shop(bob_str)
    yao_groupunit.set_membership(membership_shop(yao_str, partner_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, partner_name=sue_str))

    swim_str = ",swim"
    swim_groupunit = groupunit_shop(group_title=swim_str)
    swim_groupunit.set_membership(membership_shop(swim_str, partner_name=yao_str))
    swim_groupunit.set_membership(membership_shop(swim_str, partner_name=sue_str))
    x_groupunits = {
        yao_str: yao_groupunit,
        sue_str: sue_groupunit,
        bob_str: bob_groupunit,
        swim_str: swim_groupunit,
    }

    x_laborlinks = {swim_str}
    x_laborheir = laborheir_shop(_laborlinks=x_laborlinks)
    assert x_laborheir._believer_name_is_labor is False
    x_laborheir.set_believer_name_is_labor(x_groupunits, believer_believer_name=yao_str)
    assert x_laborheir._believer_name_is_labor

    # WHEN
    swim_groupunit.del_membership(yao_str)
    x_laborheir.set_believer_name_is_labor(x_groupunits, yao_str)

    # THEN
    assert x_laborheir._believer_name_is_labor is False


def test_LaborHeir_set_laborlink_LaborUnit_Empty_ParentLaborHeirEmpty():
    # ESTABLISH
    x_laborheir = laborheir_shop(_laborlinks={})
    parent_laborheir_empty = laborheir_shop()
    x_laborunit = laborunit_shop()

    # WHEN
    x_laborheir.set_laborlinks(
        parent_laborheir=parent_laborheir_empty,
        laborunit=x_laborunit,
        groupunits=None,
    )

    # THEN
    x_laborheir._laborlinks = {}


def test_LaborHeir_set_laborlink_LaborUnitNotEmpty_ParentLaborHeirIsNone():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=kent_str)
    x_laborunit.set_laborlink(labor_title=swim_str)

    # WHEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(None, laborunit=x_laborunit, groupunits=None)

    # THEN
    assert x_laborheir._laborlinks == x_laborunit._laborlinks


def test_LaborHeir_set_laborlink_LaborUnitNotEmpty_ParentLaborHeirEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=kent_str)
    x_laborunit.set_laborlink(labor_title=swim_str)

    # WHEN
    x_laborheir = laborheir_shop()
    parent_laborheir_empty = laborheir_shop()
    x_laborheir.set_laborlinks(parent_laborheir_empty, x_laborunit, groupunits=None)

    # THEN
    assert x_laborheir._laborlinks == x_laborunit._laborlinks


def test_LaborHeir_set_laborlink_LaborUnit_Empty_ParentLaborHeirNotEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    laborunit_swim = laborunit_shop()
    laborunit_swim.set_laborlink(labor_title=kent_str)
    laborunit_swim.set_laborlink(labor_title=swim_str)
    empty_laborheir = laborheir_shop()

    parent_laborheir = laborheir_shop()
    parent_laborheir.set_laborlinks(empty_laborheir, laborunit_swim, groupunits=None)

    laborunit_empty = laborunit_shop()

    # WHEN
    x_laborheir = laborheir_shop()
    assert x_laborheir._laborlinks == set()
    x_laborheir.set_laborlinks(parent_laborheir, laborunit_empty, groupunits=None)

    # THEN
    assert len(x_laborheir._laborlinks)
    assert x_laborheir._laborlinks == parent_laborheir._laborlinks


def test_LaborHeir_set_laborlink_LaborUnitEqualParentLaborHeir_NonEmpty():
    # ESTABLISH
    kent_str = "kent"
    swim_str = ",swim"
    laborunit_swim = laborunit_shop()
    laborunit_swim.set_laborlink(labor_title=kent_str)
    laborunit_swim.set_laborlink(labor_title=swim_str)
    empty_laborheir = laborheir_shop()

    parent_laborheir = laborheir_shop()
    parent_laborheir.set_laborlinks(empty_laborheir, laborunit_swim, groupunits=None)

    # WHEN
    x_laborheir = laborheir_shop()
    assert x_laborheir._laborlinks == set()
    x_laborheir.set_laborlinks(parent_laborheir, laborunit_swim, groupunits=None)

    # THEN
    assert x_laborheir._laborlinks == parent_laborheir._laborlinks


def test_LaborHeir_set_laborlink_LaborUnit_NotEqual_ParentLaborHeir_NonEmpty():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    bob_str = "Bob"
    zia_str = "Zia"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    bob_groupunit = groupunit_shop(bob_str)
    bob_groupunit = groupunit_shop(zia_str)
    yao_groupunit.set_membership(membership_shop(yao_str, partner_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, partner_name=sue_str))

    swim2_str = ",swim2"
    swim2_groupunit = groupunit_shop(group_title=swim2_str)
    swim2_groupunit.set_membership(membership_shop(swim2_str, partner_name=yao_str))
    swim2_groupunit.set_membership(membership_shop(swim2_str, partner_name=sue_str))

    swim3_str = ",swim3"
    swim3_groupunit = groupunit_shop(group_title=swim3_str)
    swim3_groupunit.set_membership(membership_shop(swim3_str, partner_name=yao_str))
    swim3_groupunit.set_membership(membership_shop(swim3_str, partner_name=sue_str))
    swim3_groupunit.set_membership(membership_shop(swim3_str, partner_name=zia_str))

    x_groupunits = {
        yao_str: yao_groupunit,
        sue_str: sue_groupunit,
        bob_str: bob_groupunit,
        swim2_str: swim2_groupunit,
        swim3_str: swim3_groupunit,
    }

    parent_laborunit = laborunit_shop()
    parent_laborunit.set_laborlink(labor_title=swim3_str)
    parent_laborheir = laborheir_shop()
    parent_laborheir.set_laborlinks(
        parent_laborheir=None, laborunit=parent_laborunit, groupunits=None
    )

    laborunit_swim2 = laborunit_shop()
    laborunit_swim2.set_laborlink(labor_title=swim2_str)

    # WHEN
    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(parent_laborheir, laborunit_swim2, x_groupunits)

    # THEN
    assert x_laborheir._laborlinks == laborunit_swim2._laborlinks
    assert len(x_laborheir._laborlinks) == 1
    assert list(x_laborheir._laborlinks) == [swim2_str]


# def test_LaborHeir_set_laborlink_LaborUnit_NotEqualParentLaborHeir_RaisesError():
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
#     swim2_groupunit.set_membership(membership_shop(swim2_str, partner_name=yao_str))
#     swim2_groupunit.set_membership(membership_shop(swim2_str, partner_name=sue_str))

#     swim3_str = ",swim3"
#     swim3_groupunit = groupunit_shop(labor_title=swim3_str)
#     swim3_groupunit.set_membership(membership_shop(swim3_str, partner_name=yao_str))
#     swim3_groupunit.set_membership(membership_shop(swim3_str, partner_name=sue_str))
#     swim3_groupunit.set_membership(membership_shop(swim3_str, partner_name=zia_str))

#     x_groupunits = {
#         yao_str: yao_groupunit,
#         sue_str: sue_groupunit,
#         bob_str: bob_groupunit,
#         swim2_str: swim2_groupunit,
#         swim3_str: swim3_groupunit,
#     }

#     parent_laborunit = laborunit_shop()
#     parent_laborunit.set_laborlink(swim2_str)
#     parent_laborheir = laborheir_shop()
#     parent_laborheir.set_laborlinks(None, parent_laborunit, x_groupunits)

#     laborunit_swim3 = laborunit_shop()
#     laborunit_swim3.set_laborlink(labor_title=swim3_str)

#     # WHEN / THEN
#     x_laborheir = laborheir_shop()
#     all_parent_laborheir_partners = {yao_str, sue_str}
#     all_laborunit_partners = {yao_str, sue_str, zia_str}
#     with pytest_raises(Exception) as excinfo:
#         x_laborheir.set_laborlinks(parent_laborheir, laborunit_swim3, x_groupunits)
#     assert (
#         str(excinfo.value)
#         == f"parent_laborheir does not contain all partners of the plan's laborunit\n{set(all_parent_laborheir_partners)=}\n\n{set(all_laborunit_partners)=}"
#     )


def test_LaborUnit_get_laborlink_ReturnsObj():
    # ESTABLISH
    climb_str = ",climbers"
    hike_str = ",hikers"
    swim_str = ";swimmers"
    run_str = ";runners"

    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(climb_str)
    x_laborunit.set_laborlink(hike_str)
    x_laborunit.set_laborlink(swim_str)

    # WHEN / THEN
    assert x_laborunit.get_laborlink(hike_str) is not None
    assert x_laborunit.get_laborlink(swim_str) is not None
    assert x_laborunit.get_laborlink(run_str) is None


def test_LaborHeir_labor_title_in_ReturnsCorrectBoolWhen_laborlinksNotEmpty():
    # ESTABLISH
    swim_str = ",swim"
    hike_str = ",hike"
    swim_dict = {swim_str}
    hike_dict = {hike_str}
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=swim_str)
    x_laborunit.set_laborlink(labor_title=hike_str)
    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None, laborunit=x_laborunit, groupunits=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert swim_str in x_laborheir._laborlinks
    assert hike_str in x_laborheir._laborlinks
    print(f"{hunt_str in x_laborheir._laborlinks=}")
    assert hunt_str not in x_laborheir._laborlinks
    assert play_str not in x_laborheir._laborlinks
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert x_laborheir.has_labor(swim_dict)
    assert x_laborheir.has_labor(hike_dict)
    assert x_laborheir.has_labor(hunt_dict) is False
    assert x_laborheir.has_labor(hunt_hike_dict)
    assert x_laborheir.has_labor(hunt_play_dict) is False


def test_LaborHeir_has_labor_ReturnsCorrectBoolWhen_laborlinksEmpty():
    # ESTABLISH
    hike_str = ",hike"
    hike_dict = {hike_str}
    x_laborunit = laborunit_shop()
    x_laborheir = laborheir_shop()
    x_laborheir.set_laborlinks(
        parent_laborheir=None, laborunit=x_laborunit, groupunits=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert x_laborheir._laborlinks == set()
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert x_laborheir.has_labor(hike_dict)
    assert x_laborheir.has_labor(hunt_dict)
    assert x_laborheir.has_labor(play_dict)
    assert x_laborheir.has_labor(hunt_hike_dict)
    assert x_laborheir.has_labor(hunt_play_dict)
