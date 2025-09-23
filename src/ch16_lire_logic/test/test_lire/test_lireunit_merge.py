from pytest import raises as pytest_raises
from src.ch16_lire_logic._ref.ch16_keywords import NameTerm_str
from src.ch16_lire_logic.lire_main import inherit_lireunit, lireunit_shop
from src.ch16_lire_logic.test._util.example_lires import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_suita_namemap,
    get_swim_titlemap,
)


def test_LireUnit_inherit_lireunit_ReturnsObj_Scenario0_EmptyLireUnits():
    # ESTABLISH
    sue_str = "Sue"
    old_lireunit = lireunit_shop(sue_str, 0)
    new_lireunit = lireunit_shop(sue_str, 1)

    # WHEN
    merged_lireunit = inherit_lireunit(old_lireunit, new_lireunit)

    # THEN
    assert merged_lireunit
    assert merged_lireunit == new_lireunit


def test_LireUnit_inherit_lireunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_knot = "/"
    old_lireunit = lireunit_shop(sue_str, 0, otx_knot=slash_otx_knot)
    new_lireunit = lireunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_lireunit(old_lireunit, new_lireunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_LireUnit_inherit_lireunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_knot():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_knot = "/"
    old_lireunit = lireunit_shop(sue_str, 0, inx_knot=slash_otx_knot)
    new_lireunit = lireunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_lireunit(old_lireunit, new_lireunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_LireUnit_inherit_lireunit_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    old_lireunit = lireunit_shop(sue_str, 0, unknown_str=x_unknown_str)
    new_lireunit = lireunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_lireunit(old_lireunit, new_lireunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_LireUnit_inherit_lireunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_lireunit = lireunit_shop(sue_str, 0)
    new_lireunit = lireunit_shop(bob_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_lireunit(old_lireunit, new_lireunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_LireUnit_inherit_lireunit_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_lireunit = lireunit_shop(sue_str, 5)
    new_lireunit = lireunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_lireunit(old_lireunit, new_lireunit)

    # THEN
    assert str(excinfo.value) == "older lireunit is not older"


def test_LireUnit_inherit_lireunit_ReturnsObj_Scenario6_namemap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_lireunit = lireunit_shop(sue_str, 0)
    old_lireunit.set_namemap(get_suita_namemap())
    old_lireunit.set_titlemap(get_swim_titlemap())
    old_lireunit.set_labelmap(get_clean_labelmap())
    old_lireunit.set_ropemap(get_clean_ropemap())
    new_lireunit = lireunit_shop(sue_str, event1)
    assert new_lireunit.namemap != get_suita_namemap()

    # WHEN
    merged_lireunit = inherit_lireunit(old_lireunit, new_lireunit)

    # THEN
    assert merged_lireunit
    merged_voicebrigde = get_suita_namemap()
    merged_voicebrigde.event_int = event1
    assert merged_lireunit.namemap == merged_voicebrigde
    merged_groupbrigde = get_swim_titlemap()
    merged_groupbrigde.event_int = event1
    assert merged_lireunit.titlemap == merged_groupbrigde
    merged_labelbrigde = get_clean_labelmap()
    merged_labelbrigde.event_int = event1
    assert merged_lireunit.labelmap == merged_labelbrigde
    merged_ropebrigde = get_clean_ropemap()
    merged_ropebrigde.event_int = event1
    merged_ropebrigde.labelmap = merged_labelbrigde
    assert merged_lireunit.ropemap == merged_ropebrigde


def test_LireUnit_inherit_lireunit_ReturnsObj_Scenario7_namemap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_lireunit = lireunit_shop(sue_str, 0)
    old_lireunit.set_namemap(get_suita_namemap())
    old_lireunit.set_titlemap(get_swim_titlemap())
    new_lireunit = lireunit_shop(sue_str, event1)
    bob_otx = "Bob"
    bob_inx = "Bobby"
    new_lireunit.set_otx2inx(NameTerm_str(), bob_otx, bob_inx)
    assert new_lireunit.namemap != get_suita_namemap()
    assert new_lireunit.nameterm_exists(bob_otx, bob_inx)

    # WHEN
    merged_lireunit = inherit_lireunit(old_lireunit, new_lireunit)

    # THEN
    assert merged_lireunit
    assert new_lireunit.nameterm_exists(bob_otx, bob_inx)
    merged_voicebrigde = get_suita_namemap()
    merged_voicebrigde.event_int = event1
    merged_voicebrigde.set_otx2inx(bob_otx, bob_inx)
    assert merged_lireunit.namemap == merged_voicebrigde
    merged_groupbrigde = get_swim_titlemap()
    merged_groupbrigde.event_int = event1
    assert merged_lireunit.titlemap == merged_groupbrigde
