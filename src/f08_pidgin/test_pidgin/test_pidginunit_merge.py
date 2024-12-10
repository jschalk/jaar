from src.f04_gift.atom_config import type_AcctID_str
from src.f08_pidgin.pidgin import pidginunit_shop, inherit_pidginunit
from src.f08_pidgin.examples.example_pidgins import (
    get_clean_roadbridge,
    get_clean_ideabridge,
    get_swim_groupbridge,
    get_suita_acctbridge,
)
from pytest import raises as pytest_raises


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario0_EmptyPidginUnits():
    # ESTABLISH
    sue_str = "Sue"
    old_pidginunit = pidginunit_shop(sue_str, 0)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    assert merged_pidginunit == new_pidginunit


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_wall():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_wall = "/"
    old_pidginunit = pidginunit_shop(sue_str, 0, x_otx_wall=slash_otx_wall)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_wall():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_wall = "/"
    old_pidginunit = pidginunit_shop(sue_str, 0, x_inx_wall=slash_otx_wall)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_word():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    old_pidginunit = pidginunit_shop(sue_str, 0, x_unknown_word=x_unknown_word)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_id():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_pidginunit = pidginunit_shop(sue_str, 0)
    new_pidginunit = pidginunit_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario5_RaiseErrorWhenEventIDsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_pidginunit = pidginunit_shop(sue_str, 5)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "older pidginunit is not older"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario6_acctbridge_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_pidginunit = pidginunit_shop(sue_str, 0)
    old_pidginunit.set_acctbridge(get_suita_acctbridge())
    old_pidginunit.set_groupbridge(get_swim_groupbridge())
    old_pidginunit.set_ideabridge(get_clean_ideabridge())
    old_pidginunit.set_roadbridge(get_clean_roadbridge())
    new_pidginunit = pidginunit_shop(sue_str, event1)
    assert new_pidginunit.acctbridge != get_suita_acctbridge()

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    merged_acctbrigde = get_suita_acctbridge()
    merged_acctbrigde.event_id = event1
    assert merged_pidginunit.acctbridge == merged_acctbrigde
    merged_groupbrigde = get_swim_groupbridge()
    merged_groupbrigde.event_id = event1
    assert merged_pidginunit.groupbridge == merged_groupbrigde
    merged_ideabrigde = get_clean_ideabridge()
    merged_ideabrigde.event_id = event1
    assert merged_pidginunit.ideabridge == merged_ideabrigde
    merged_roadbrigde = get_clean_roadbridge()
    merged_roadbrigde.event_id = event1
    merged_roadbrigde.ideabridge = merged_ideabrigde
    assert merged_pidginunit.roadbridge == merged_roadbrigde


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario7_acctbridge_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_pidginunit = pidginunit_shop(sue_str, 0)
    old_pidginunit.set_acctbridge(get_suita_acctbridge())
    old_pidginunit.set_groupbridge(get_swim_groupbridge())
    new_pidginunit = pidginunit_shop(sue_str, event1)
    bob_otx = "Bob"
    bob_inx = "Bobby"
    new_pidginunit.set_otx2inx(type_AcctID_str(), bob_otx, bob_inx)
    assert new_pidginunit.acctbridge != get_suita_acctbridge()
    assert new_pidginunit.acct_id_exists(bob_otx, bob_inx)

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    assert new_pidginunit.acct_id_exists(bob_otx, bob_inx)
    merged_acctbrigde = get_suita_acctbridge()
    merged_acctbrigde.event_id = event1
    merged_acctbrigde.set_otx2inx(bob_otx, bob_inx)
    assert merged_pidginunit.acctbridge == merged_acctbrigde
    merged_groupbrigde = get_swim_groupbridge()
    merged_groupbrigde.event_id = event1
    assert merged_pidginunit.groupbridge == merged_groupbrigde
