from src.a08_bud_atom_logic.atom_config import type_NameUnit_str
from src.f09_pidgin.pidgin import pidginunit_shop, inherit_pidginunit
from src.f09_pidgin.examples.example_pidgins import (
    get_clean_roadmap,
    get_clean_titlemap,
    get_swim_labelmap,
    get_suita_namemap,
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


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario6_namemap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_pidginunit = pidginunit_shop(sue_str, 0)
    old_pidginunit.set_namemap(get_suita_namemap())
    old_pidginunit.set_labelmap(get_swim_labelmap())
    old_pidginunit.set_titlemap(get_clean_titlemap())
    old_pidginunit.set_roadmap(get_clean_roadmap())
    new_pidginunit = pidginunit_shop(sue_str, event1)
    assert new_pidginunit.namemap != get_suita_namemap()

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    merged_acctbrigde = get_suita_namemap()
    merged_acctbrigde.event_int = event1
    assert merged_pidginunit.namemap == merged_acctbrigde
    merged_groupbrigde = get_swim_labelmap()
    merged_groupbrigde.event_int = event1
    assert merged_pidginunit.labelmap == merged_groupbrigde
    merged_titlebrigde = get_clean_titlemap()
    merged_titlebrigde.event_int = event1
    assert merged_pidginunit.titlemap == merged_titlebrigde
    merged_roadbrigde = get_clean_roadmap()
    merged_roadbrigde.event_int = event1
    merged_roadbrigde.titlemap = merged_titlebrigde
    assert merged_pidginunit.roadmap == merged_roadbrigde


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario7_namemap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_pidginunit = pidginunit_shop(sue_str, 0)
    old_pidginunit.set_namemap(get_suita_namemap())
    old_pidginunit.set_labelmap(get_swim_labelmap())
    new_pidginunit = pidginunit_shop(sue_str, event1)
    bob_otx = "Bob"
    bob_inx = "Bobby"
    new_pidginunit.set_otx2inx(type_NameUnit_str(), bob_otx, bob_inx)
    assert new_pidginunit.namemap != get_suita_namemap()
    assert new_pidginunit.nameunit_exists(bob_otx, bob_inx)

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    assert new_pidginunit.nameunit_exists(bob_otx, bob_inx)
    merged_acctbrigde = get_suita_namemap()
    merged_acctbrigde.event_int = event1
    merged_acctbrigde.set_otx2inx(bob_otx, bob_inx)
    assert merged_pidginunit.namemap == merged_acctbrigde
    merged_groupbrigde = get_swim_labelmap()
    merged_groupbrigde.event_int = event1
    assert merged_pidginunit.labelmap == merged_groupbrigde
