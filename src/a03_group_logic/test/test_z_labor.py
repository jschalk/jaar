from src.a01_term_logic.term import GroupTitle, default_knot_if_None
from src.a03_group_logic.group import groupunit_shop, membership_shop
from src.a03_group_logic.labor import (
    LaborHeir,
    LaborUnit,
    PartyHeir,
    PartyUnit,
    create_laborunit,
    laborheir_shop,
    laborunit_shop,
    partyheir_shop,
    partyunit_shop,
)
from src.a03_group_logic.test._util.a03_str import (
    _parent_solo_str,
    party_title_str,
    solo_str,
)


def test_PartyUnit_Exists():
    # ESTABLISH / WHEN
    x_partyunit = PartyUnit()

    # THEN
    assert not x_partyunit.party_title
    assert not x_partyunit.solo
    obj_attrs = set(x_partyunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {party_title_str(), solo_str()}


def test_partyunit_shop_ReturnsObj_Scenario0_WithParameters():
    # ESTABLISH
    bob_str = "Bob"
    bob_solo_bool = True

    # WHEN
    x_partyunit = partyunit_shop(bob_str, solo=bob_solo_bool)

    # THEN
    assert x_partyunit.party_title == bob_str
    assert x_partyunit.solo == bob_solo_bool


def test_PartyUnit_get_dict_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_solo_bool = True
    x_partyunit = partyunit_shop(bob_str, solo=bob_solo_bool)

    # WHEN
    party_dict = x_partyunit.get_dict()

    # THEN
    assert party_dict
    assert party_dict.get(party_title_str()) == bob_str
    assert party_dict.get(solo_str()) == bob_solo_bool


def test_partyunit_shop_ReturnsObj_Scenario1_WithParametersNot():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    x_partyunit = partyunit_shop(bob_str)

    # THEN
    assert x_partyunit.party_title == bob_str
    assert x_partyunit.solo is False


def test_PartyHeir_Exists():
    # ESTABLISH / WHEN
    x_partyheir = PartyHeir()

    # THEN
    assert not x_partyheir.party_title
    assert not x_partyheir.solo
    assert not x_partyheir._parent_solo
    obj_attrs = set(x_partyheir.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {party_title_str(), solo_str(), _parent_solo_str()}


def test_partyheir_shop_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_solo_bool = True

    # WHEN
    x_partyheir = partyheir_shop(bob_str, bob_solo_bool)

    # THEN
    assert x_partyheir.party_title == bob_str
    assert x_partyheir.solo == bob_solo_bool


def test_LaborUnit_Exists():
    # ESTABLISH / WHEN
    x_laborunit = LaborUnit()

    # THEN
    assert x_laborunit
    assert not x_laborunit._partys
    obj_attrs = set(x_laborunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {"_partys"}


def test_laborunit_shop_ReturnsWithCorrectAttributes_v1():
    # ESTABLISH
    x_partys = {1}

    # WHEN
    x_laborunit = laborunit_shop(_partys=x_partys)

    # THEN
    assert x_laborunit
    assert x_laborunit._partys == x_partys


def test_laborunit_shop_ifEmptyReturnsWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_laborunit = laborunit_shop()

    # THEN
    assert x_laborunit
    assert x_laborunit._partys == {}


def test_LaborUnit_add_partyunit_SetsAttr_Secnario0():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    assert len(x_laborunit._partys) == 0

    # WHEN
    yao_str = "Yao"
    x_laborunit.add_partyunit(party_title=yao_str)

    # THEN
    assert len(x_laborunit._partys) == 1
    expected_partys = {yao_str: partyunit_shop(yao_str)}
    assert x_laborunit._partys == expected_partys


def test_LaborUnit_add_partyunit_SetsAttr_Secnario1():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    yao_str = "Yao"
    yao_solo_bool = True
    assert len(x_laborunit._partys) == 0

    # WHEN
    x_laborunit.add_partyunit(party_title=yao_str, solo=yao_solo_bool)

    # THEN
    assert len(x_laborunit._partys) == 1
    expected_partys = {yao_str: partyunit_shop(yao_str, solo=yao_solo_bool)}
    assert x_laborunit._partys == expected_partys


def test_create_laborunit_ReturnsObj():
    # ESTABLISH
    swim_party_title = GroupTitle("swimmers")

    # WHEN
    swim_laborunit = create_laborunit(swim_party_title)

    # THEN
    assert swim_laborunit
    assert len(swim_laborunit._partys) == 1
    expected_partys = {swim_party_title: partyunit_shop(swim_party_title)}
    assert swim_laborunit._partys == expected_partys


def test_LaborUnit_get_dict_ReturnsDictWithSingle_partyunit():
    # ESTABLISH
    bob_party_title = GroupTitle("Bob")
    x_partys = {bob_party_title: bob_party_title}
    x_laborunit = laborunit_shop(_partys=x_partys)

    # WHEN
    obj_dict = x_laborunit.to_dict()

    # THEN
    assert obj_dict is not None
    example_dict = {"_partys": [bob_party_title]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_LaborUnit_partyunit_exists_ReturnsObj():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    yao_str = "Yao"
    assert x_laborunit.partyunit_exists(yao_str) is False

    # WHEN
    x_laborunit.add_partyunit(party_title=yao_str)

    # THEN
    assert x_laborunit.partyunit_exists(yao_str)


def test_LaborUnit_del_partyunit_Deletes_partys_v1():
    # ESTABLISH
    x_laborunit = laborunit_shop()
    yao_str = "Yao"
    sue_str = "Sue"
    x_laborunit.add_partyunit(party_title=yao_str)
    x_laborunit.add_partyunit(party_title=sue_str)
    assert len(x_laborunit._partys) == 2

    # WHEN
    x_laborunit.del_partyunit(party_title=sue_str)

    # THEN
    assert len(x_laborunit._partys) == 1


def test_LaborHeir_Exists():
    # ESTABLISH / WHEN
    x_laborheir = LaborHeir()

    # THEN
    assert x_laborheir
    assert not x_laborheir._partys
    assert not x_laborheir._believer_name_is_labor
    obj_attrs = set(x_laborheir.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {"_partys", "_believer_name_is_labor"}


def test_laborheir_shop_ReturnsObj_Scenario1_WithAttributes():
    # ESTABLISH
    swim_party_title = GroupTitle("swimmers")
    _believer_name_x_laborunit = "example"
    x_partys = {swim_party_title: partyunit_shop(swim_party_title)}

    # WHEN
    x_laborheir = laborheir_shop(
        _partys=x_partys, _believer_name_is_labor=_believer_name_x_laborunit
    )

    # THEN
    assert x_laborheir
    assert x_laborheir._partys == x_partys
    assert x_laborheir._believer_name_is_labor == _believer_name_x_laborunit


def test_LaborHeir_set_believer_name_is_labor_SetsAttribute_Emptyx_partys():
    # ESTABLISH
    x_partys = {}
    x_laborheir = laborheir_shop(_partys=x_partys)
    assert x_laborheir._believer_name_is_labor is False

    # WHEN
    groupunits = {}
    x_laborheir.set_believer_name_is_labor(groupunits, believer_name="")

    # THEN
    assert x_laborheir._believer_name_is_labor


def test_LaborHeir_set_believer_name_is_labor_SetsAttribute_NonEmptyx_partys_v1():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    yao_groupunit.set_membership(membership_shop(yao_str, partner_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, partner_name=sue_str))
    x_groupunits = {yao_str: yao_groupunit, sue_str: sue_groupunit}
    believer_name = yao_str

    x_partys = {yao_str}
    x_laborheir = laborheir_shop(_partys=x_partys)
    assert x_laborheir._believer_name_is_labor is False

    # WHEN
    x_laborheir.set_believer_name_is_labor(x_groupunits, believer_name)

    # THEN
    assert x_laborheir._believer_name_is_labor


def test_LaborHeir_set_believer_name_is_labor_SetsAttribute_NonEmptyx_partys_v2():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    yao_groupunit = groupunit_shop(yao_str)
    sue_groupunit = groupunit_shop(sue_str)
    yao_groupunit.set_membership(membership_shop(yao_str, partner_name=yao_str))
    sue_groupunit.set_membership(membership_shop(sue_str, partner_name=sue_str))
    x_groupunits = {yao_str: yao_groupunit, sue_str: sue_groupunit}
    x_partys = {sue_str}
    x_laborheir = laborheir_shop(_partys=x_partys)
    assert yao_groupunit.get_membership(yao_str) is not None
    assert x_laborheir._believer_name_is_labor is False

    # WHEN
    x_laborheir.set_believer_name_is_labor(x_groupunits, yao_str)

    # THEN
    assert x_laborheir._believer_name_is_labor is False


def test_LaborHeir_set_believer_name_is_labor_SetsAttribute_NonEmptyx_partys_v3():
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

    x_partys = {swim_str}
    x_laborheir = laborheir_shop(_partys=x_partys)
    assert x_laborheir._believer_name_is_labor is False
    x_laborheir.set_believer_name_is_labor(x_groupunits, believer_name=yao_str)
    assert x_laborheir._believer_name_is_labor

    # WHEN
    swim_groupunit.del_membership(yao_str)
    x_laborheir.set_believer_name_is_labor(x_groupunits, yao_str)

    # THEN
    assert x_laborheir._believer_name_is_labor is False


def test_LaborHeir_set_partys_Scenario0_LaborUnitIsEmptyAndParentLaborHeirIsEmpty():
    # ESTABLISH
    x_laborheir = laborheir_shop(_partys={})
    parent_laborheir_empty = laborheir_shop()
    x_laborunit = laborunit_shop()

    # WHEN
    x_laborheir.set_partys(
        parent_laborheir=parent_laborheir_empty,
        laborunit=x_laborunit,
        groupunits=None,
    )

    # THEN
    x_laborheir._partys = {}


def test_LaborHeir_set_partys_Scenario1_LaborUnitNotEmpty_ParentLaborHeirIsNone():
    # ESTABLISH
    xio_str = "xio"
    xio_solo_bool = True
    swim_str = ",swim"
    x_laborunit = laborunit_shop()
    x_laborunit.add_partyunit(xio_str, xio_solo_bool)
    x_laborunit.add_partyunit(swim_str)
    x_laborheir = laborheir_shop()
    assert x_laborheir._partys == {}

    # WHEN
    x_laborheir.set_partys(None, laborunit=x_laborunit, groupunits=None)

    # THEN
    assert x_laborheir._partys.keys() == x_laborunit._partys.keys()
    expected_partys = {
        xio_str: partyheir_shop(xio_str, xio_solo_bool),
        swim_str: partyheir_shop(swim_str, False),
    }
    print(f"{x_laborheir._partys=}")
    print(f"    {expected_partys=}")
    assert x_laborheir._partys == expected_partys


def test_LaborHeir_set_partys_Scenario2_LaborUnitNotEmpty_ParentLaborHeirEmpty():
    # ESTABLISH
    xio_str = "xio"
    xio_solo_bool = True
    swim_str = ",swim"
    x_laborunit = laborunit_shop()
    x_laborunit.add_partyunit(xio_str, xio_solo_bool)
    x_laborunit.add_partyunit(swim_str)
    x_laborheir = laborheir_shop()
    parent_laborheir_empty = laborheir_shop()
    assert x_laborheir._partys == {}

    # WHEN
    x_laborheir.set_partys(parent_laborheir_empty, x_laborunit, groupunits=None)

    # THEN
    assert x_laborheir._partys.keys() == x_laborunit._partys.keys()
    expected_partys = {
        xio_str: partyheir_shop(xio_str, xio_solo_bool),
        swim_str: partyheir_shop(swim_str, False),
    }
    print(f"{x_laborheir._partys=}")
    print(f"    {expected_partys=}")
    assert x_laborheir._partys == expected_partys


def test_LaborHeir_set_partys_Scenario3_LaborUnit_Empty_ParentLaborHeirNotEmpty():
    # ESTABLISH
    xio_str = "xio"
    xio_solo_bool = True
    swim_str = ",swim"
    laborunit_swim = laborunit_shop()
    laborunit_swim.add_partyunit(xio_str, xio_solo_bool)
    laborunit_swim.add_partyunit(swim_str, False)
    empty_laborheir = laborheir_shop()
    parent_laborheir = laborheir_shop()
    parent_laborheir.set_partys(empty_laborheir, laborunit_swim, groupunits=None)

    laborunit_empty = laborunit_shop()
    x_laborheir = laborheir_shop()
    assert x_laborheir._partys == {}
    assert laborunit_empty._partys == {}

    # WHEN
    x_laborheir.set_partys(parent_laborheir, laborunit_empty, groupunits=None)

    # THEN
    assert x_laborheir._partys.keys() == parent_laborheir._partys.keys()
    expected_partys = {
        xio_str: partyheir_shop(xio_str, xio_solo_bool),
        swim_str: partyheir_shop(swim_str, False),
    }
    print(f"{x_laborheir._partys=}")
    print(f"    {expected_partys=}")
    assert x_laborheir._partys == expected_partys


def test_LaborHeir_set_partys_Scenario4_LaborUnitEqualParentLaborHeir_NonEmpty():
    # ESTABLISH
    xio_str = "xio"
    xio_solo_bool = True
    xio_laborunit = laborunit_shop()
    xio_laborunit.add_partyunit(xio_str, xio_solo_bool)
    empty_laborheir = laborheir_shop()
    parent_laborheir = laborheir_shop()
    parent_laborheir.set_partys(empty_laborheir, xio_laborunit, groupunits=None)

    swim_str = ",swim"
    swim_laborunit = laborunit_shop()
    swim_laborunit.add_partyunit(swim_str)

    x_laborheir = laborheir_shop()
    assert x_laborheir._partys == {}

    # WHEN
    x_laborheir.set_partys(parent_laborheir, swim_laborunit, groupunits=None)

    # THEN
    assert x_laborheir._partys.keys() != parent_laborheir._partys.keys()
    assert x_laborheir._partys.keys() != swim_laborunit._partys.keys()
    expected_partys = {
        xio_str: partyheir_shop(xio_str, xio_solo_bool),
        swim_str: partyheir_shop(swim_str, False),
    }
    print(f"{x_laborheir._partys=}")
    print(f"    {expected_partys=}")
    assert x_laborheir._partys == expected_partys


# def test_LaborHeir_set_partys_Scenario5_LaborUnit_NotEqual_ParentLaborHeir_NonEmpty():
#     # ESTABLISH
#     yao_str = "Yao"
#     sue_str = "Sue"
#     bob_str = "Bob"
#     zia_str = "Zia"
#     yao_groupunit = groupunit_shop(yao_str)
#     sue_groupunit = groupunit_shop(sue_str)
#     bob_groupunit = groupunit_shop(bob_str)
#     bob_groupunit = groupunit_shop(zia_str)
#     yao_groupunit.set_membership(membership_shop(yao_str, partner_name=yao_str))
#     sue_groupunit.set_membership(membership_shop(sue_str, partner_name=sue_str))

#     swim2_str = ",swim2"
#     swim2_groupunit = groupunit_shop(group_title=swim2_str)
#     swim2_groupunit.set_membership(membership_shop(swim2_str, partner_name=yao_str))
#     swim2_groupunit.set_membership(membership_shop(swim2_str, partner_name=sue_str))

#     swim3_str = ",swim3"
#     swim3_groupunit = groupunit_shop(group_title=swim3_str)
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
#     parent_laborunit.add_partyunit(party_title=swim3_str)
#     parent_laborheir = laborheir_shop()
#     parent_laborheir.set_partys(
#         parent_laborheir=None, laborunit=parent_laborunit, groupunits=None
#     )

#     laborunit_swim2 = laborunit_shop()
#     laborunit_swim2.add_partyunit(party_title=swim2_str)
#     x_laborheir = laborheir_shop()
#     assert x_laborheir._partys == {}

#     # WHEN
#     x_laborheir.set_partys(parent_laborheir, laborunit_swim2, x_groupunits)

#     # THEN
#     assert x_laborheir._partys.keys() == laborunit_swim2._partys.keys()
#     assert len(x_laborheir._partys) == 1
#     assert list(x_laborheir._partys) == [swim2_str]


def test_LaborUnit_get_partyunit_ReturnsObj():
    # ESTABLISH
    climb_str = ",climbers"
    hike_str = ",hikers"
    swim_str = ";swimmers"
    run_str = ";runners"

    x_laborunit = laborunit_shop()
    x_laborunit.add_partyunit(climb_str)
    x_laborunit.add_partyunit(hike_str)
    x_laborunit.add_partyunit(swim_str)

    # WHEN / THEN
    assert x_laborunit.get_partyunit(hike_str) is not None
    assert x_laborunit.get_partyunit(swim_str) is not None
    assert x_laborunit.get_partyunit(run_str) is None


def test_LaborHeir_party_title_in_ReturnsBoolWhen_partysNotEmpty():
    # ESTABLISH
    swim_str = ",swim"
    hike_str = ",hike"
    swim_dict = {swim_str}
    hike_dict = {hike_str}
    x_laborunit = laborunit_shop()
    x_laborunit.add_partyunit(party_title=swim_str)
    x_laborunit.add_partyunit(party_title=hike_str)
    x_laborheir = laborheir_shop()
    x_laborheir.set_partys(
        parent_laborheir=None, laborunit=x_laborunit, groupunits=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert swim_str in x_laborheir._partys
    assert hike_str in x_laborheir._partys
    print(f"{hunt_str in x_laborheir._partys=}")
    assert hunt_str not in x_laborheir._partys
    assert play_str not in x_laborheir._partys
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert x_laborheir.has_party(swim_dict)
    assert x_laborheir.has_party(hike_dict)
    assert x_laborheir.has_party(hunt_dict) is False
    assert x_laborheir.has_party(hunt_hike_dict)
    assert x_laborheir.has_party(hunt_play_dict) is False


def test_LaborHeir_has_party_ReturnsObj():
    # ESTABLISH
    hike_str = ",hike"
    hike_dict = {hike_str}
    hike_partyunit = partyunit_shop(hike_str)
    hike_laborunit = laborunit_shop({hike_str: hike_partyunit})
    hike_laborheir = laborheir_shop()
    hike_laborheir.set_partys(
        parent_laborheir=None, laborunit=hike_laborunit, groupunits=None
    )
    hunt_str = ",hunt"
    hunt_dict = {hunt_str}
    play_str = ",play"
    play_dict = {play_str}
    assert len(hike_laborheir._partys) == 1
    hunt_hike_dict = {hunt_str, hike_str}
    hunt_play_dict = {hunt_str, play_str}

    # WHEN / THEN
    assert hike_laborheir.has_party(hike_dict)
    assert not hike_laborheir.has_party(hunt_dict)
    assert not hike_laborheir.has_party(play_dict)
    assert hike_laborheir.has_party(hunt_hike_dict)
    assert not hike_laborheir.has_party(hunt_play_dict)
