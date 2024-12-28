from src.f04_gift.atom_config import type_AcctName_str
from src.f08_pidgin.pidgin import pidginunit_shop, inherit_pidginunit
from src.f08_pidgin.examples.example_pidgins import (
    get_clean_roadmap,
    get_clean_ideamap,
    get_swim_groupmap,
    get_suita_acctmap,
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


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_pidginunit = pidginunit_shop(sue_str, 0, otx_bridge=slash_otx_bridge)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_bridge():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_bridge = "/"
    old_pidginunit = pidginunit_shop(sue_str, 0, inx_bridge=slash_otx_bridge)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_word():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    old_pidginunit = pidginunit_shop(sue_str, 0, unknown_word=x_unknown_word)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_pidginunit = pidginunit_shop(sue_str, 0)
    new_pidginunit = pidginunit_shop(bob_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_pidginunit = pidginunit_shop(sue_str, 5)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)
    assert str(excinfo.value) == "older pidginunit is not older"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario6_acctmap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_pidginunit = pidginunit_shop(sue_str, 0)
    old_pidginunit.set_acctmap(get_suita_acctmap())
    old_pidginunit.set_groupmap(get_swim_groupmap())
    old_pidginunit.set_ideamap(get_clean_ideamap())
    old_pidginunit.set_roadmap(get_clean_roadmap())
    new_pidginunit = pidginunit_shop(sue_str, event1)
    assert new_pidginunit.acctmap != get_suita_acctmap()

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    merged_acctbrigde = get_suita_acctmap()
    merged_acctbrigde.event_int = event1
    assert merged_pidginunit.acctmap == merged_acctbrigde
    merged_groupbrigde = get_swim_groupmap()
    merged_groupbrigde.event_int = event1
    assert merged_pidginunit.groupmap == merged_groupbrigde
    merged_ideabrigde = get_clean_ideamap()
    merged_ideabrigde.event_int = event1
    assert merged_pidginunit.ideamap == merged_ideabrigde
    merged_roadbrigde = get_clean_roadmap()
    merged_roadbrigde.event_int = event1
    merged_roadbrigde.ideamap = merged_ideabrigde
    assert merged_pidginunit.roadmap == merged_roadbrigde


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario7_acctmap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_pidginunit = pidginunit_shop(sue_str, 0)
    old_pidginunit.set_acctmap(get_suita_acctmap())
    old_pidginunit.set_groupmap(get_swim_groupmap())
    new_pidginunit = pidginunit_shop(sue_str, event1)
    bob_otx = "Bob"
    bob_inx = "Bobby"
    new_pidginunit.set_otx2inx(type_AcctName_str(), bob_otx, bob_inx)
    assert new_pidginunit.acctmap != get_suita_acctmap()
    assert new_pidginunit.acct_name_exists(bob_otx, bob_inx)

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    assert new_pidginunit.acct_name_exists(bob_otx, bob_inx)
    merged_acctbrigde = get_suita_acctmap()
    merged_acctbrigde.event_int = event1
    merged_acctbrigde.set_otx2inx(bob_otx, bob_inx)
    assert merged_pidginunit.acctmap == merged_acctbrigde
    merged_groupbrigde = get_swim_groupmap()
    merged_groupbrigde.event_int = event1
    assert merged_pidginunit.groupmap == merged_groupbrigde
