from pytest import raises as pytest_raises
from src.a16_pidgin_logic.pidgin_main import inherit_pidginunit, pidginunit_shop
from src.a16_pidgin_logic.test._util.a16_terms import NameTerm_str
from src.a16_pidgin_logic.test._util.example_pidgins import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_suita_namemap,
    get_swim_titlemap,
)


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


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_knot = "/"
    old_pidginunit = pidginunit_shop(sue_str, 0, otx_knot=slash_otx_knot)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_knot():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_knot = "/"
    old_pidginunit = pidginunit_shop(sue_str, 0, inx_knot=slash_otx_knot)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    old_pidginunit = pidginunit_shop(sue_str, 0, unknown_str=x_unknown_str)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_pidginunit = pidginunit_shop(sue_str, 0)
    new_pidginunit = pidginunit_shop(bob_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_pidginunit = pidginunit_shop(sue_str, 5)
    new_pidginunit = pidginunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert str(excinfo.value) == "older pidginunit is not older"


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario6_namemap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_pidginunit = pidginunit_shop(sue_str, 0)
    old_pidginunit.set_namemap(get_suita_namemap())
    old_pidginunit.set_titlemap(get_swim_titlemap())
    old_pidginunit.set_labelmap(get_clean_labelmap())
    old_pidginunit.set_ropemap(get_clean_ropemap())
    new_pidginunit = pidginunit_shop(sue_str, event1)
    assert new_pidginunit.namemap != get_suita_namemap()

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    merged_voicebrigde = get_suita_namemap()
    merged_voicebrigde.event_int = event1
    assert merged_pidginunit.namemap == merged_voicebrigde
    merged_groupbrigde = get_swim_titlemap()
    merged_groupbrigde.event_int = event1
    assert merged_pidginunit.titlemap == merged_groupbrigde
    merged_labelbrigde = get_clean_labelmap()
    merged_labelbrigde.event_int = event1
    assert merged_pidginunit.labelmap == merged_labelbrigde
    merged_ropebrigde = get_clean_ropemap()
    merged_ropebrigde.event_int = event1
    merged_ropebrigde.labelmap = merged_labelbrigde
    assert merged_pidginunit.ropemap == merged_ropebrigde


def test_PidginUnit_inherit_pidginunit_ReturnsObj_Scenario7_namemap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_pidginunit = pidginunit_shop(sue_str, 0)
    old_pidginunit.set_namemap(get_suita_namemap())
    old_pidginunit.set_titlemap(get_swim_titlemap())
    new_pidginunit = pidginunit_shop(sue_str, event1)
    bob_otx = "Bob"
    bob_inx = "Bobby"
    new_pidginunit.set_otx2inx(NameTerm_str(), bob_otx, bob_inx)
    assert new_pidginunit.namemap != get_suita_namemap()
    assert new_pidginunit.nameterm_exists(bob_otx, bob_inx)

    # WHEN
    merged_pidginunit = inherit_pidginunit(old_pidginunit, new_pidginunit)

    # THEN
    assert merged_pidginunit
    assert new_pidginunit.nameterm_exists(bob_otx, bob_inx)
    merged_voicebrigde = get_suita_namemap()
    merged_voicebrigde.event_int = event1
    merged_voicebrigde.set_otx2inx(bob_otx, bob_inx)
    assert merged_pidginunit.namemap == merged_voicebrigde
    merged_groupbrigde = get_swim_titlemap()
    merged_groupbrigde.event_int = event1
    assert merged_pidginunit.titlemap == merged_groupbrigde
