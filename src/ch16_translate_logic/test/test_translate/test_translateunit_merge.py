from pytest import raises as pytest_raises
from src.ch16_translate_logic._ref.ch16_keywords import Ch16Keywords as wx
from src.ch16_translate_logic.test._util.ch16_examples import (
    get_clean_labelmap,
    get_clean_ropemap,
    get_suita_namemap,
    get_swim_titlemap,
)
from src.ch16_translate_logic.translate_main import (
    inherit_translateunit,
    translateunit_shop,
)


def test_TranslateUnit_inherit_translateunit_ReturnsObj_Scenario0_EmptyTranslateUnits():
    # ESTABLISH
    sue_str = "Sue"
    old_translateunit = translateunit_shop(sue_str, 0)
    new_translateunit = translateunit_shop(sue_str, 1)

    # WHEN
    merged_translateunit = inherit_translateunit(old_translateunit, new_translateunit)

    # THEN
    assert merged_translateunit
    assert merged_translateunit == new_translateunit


def test_TranslateUnit_inherit_translateunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_otx_knot():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_knot = "/"
    old_translateunit = translateunit_shop(sue_str, 0, otx_knot=slash_otx_knot)
    new_translateunit = translateunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_translateunit(old_translateunit, new_translateunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_TranslateUnit_inherit_translateunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_inx_knot():
    # ESTABLISH
    sue_str = "Sue"
    slash_otx_knot = "/"
    old_translateunit = translateunit_shop(sue_str, 0, inx_knot=slash_otx_knot)
    new_translateunit = translateunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_translateunit(old_translateunit, new_translateunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_TranslateUnit_inherit_translateunit_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    old_translateunit = translateunit_shop(sue_str, 0, unknown_str=x_unknown_str)
    new_translateunit = translateunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_translateunit(old_translateunit, new_translateunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_TranslateUnit_inherit_translateunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_face_name():
    # ESTABLISH
    sue_str = "Sue"
    bob_str = "Bob"
    old_translateunit = translateunit_shop(sue_str, 0)
    new_translateunit = translateunit_shop(bob_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_translateunit(old_translateunit, new_translateunit)

    # THEN
    assert str(excinfo.value) == "Core attributes in conflict"


def test_TranslateUnit_inherit_translateunit_ReturnsObj_Scenario5_RaiseErrorWhenEventIntsOutOfOrder():
    # ESTABLISH
    sue_str = "Sue"
    old_translateunit = translateunit_shop(sue_str, 5)
    new_translateunit = translateunit_shop(sue_str, 1)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        inherit_translateunit(old_translateunit, new_translateunit)

    # THEN
    assert str(excinfo.value) == "older translateunit is not older"


def test_TranslateUnit_inherit_translateunit_ReturnsObj_Scenario6_namemap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_translateunit = translateunit_shop(sue_str, 0)
    old_translateunit.set_namemap(get_suita_namemap())
    old_translateunit.set_titlemap(get_swim_titlemap())
    old_translateunit.set_labelmap(get_clean_labelmap())
    old_translateunit.set_ropemap(get_clean_ropemap())
    new_translateunit = translateunit_shop(sue_str, event1)
    assert new_translateunit.namemap != get_suita_namemap()

    # WHEN
    merged_translateunit = inherit_translateunit(old_translateunit, new_translateunit)

    # THEN
    assert merged_translateunit
    merged_voicebrigde = get_suita_namemap()
    merged_voicebrigde.event_int = event1
    assert merged_translateunit.namemap == merged_voicebrigde
    merged_groupbrigde = get_swim_titlemap()
    merged_groupbrigde.event_int = event1
    assert merged_translateunit.titlemap == merged_groupbrigde
    merged_labelbrigde = get_clean_labelmap()
    merged_labelbrigde.event_int = event1
    assert merged_translateunit.labelmap == merged_labelbrigde
    merged_ropebrigde = get_clean_ropemap()
    merged_ropebrigde.event_int = event1
    merged_ropebrigde.labelmap = merged_labelbrigde
    assert merged_translateunit.ropemap == merged_ropebrigde


def test_TranslateUnit_inherit_translateunit_ReturnsObj_Scenario7_namemap_Inherited():
    # ESTABLISH
    sue_str = "Sue"
    event1 = 1
    old_translateunit = translateunit_shop(sue_str, 0)
    old_translateunit.set_namemap(get_suita_namemap())
    old_translateunit.set_titlemap(get_swim_titlemap())
    new_translateunit = translateunit_shop(sue_str, event1)
    bob_otx = "Bob"
    bob_inx = "Bobby"
    new_translateunit.set_otx2inx(wx.NameTerm, bob_otx, bob_inx)
    assert new_translateunit.namemap != get_suita_namemap()
    assert new_translateunit.nameterm_exists(bob_otx, bob_inx)

    # WHEN
    merged_translateunit = inherit_translateunit(old_translateunit, new_translateunit)

    # THEN
    assert merged_translateunit
    assert new_translateunit.nameterm_exists(bob_otx, bob_inx)
    merged_voicebrigde = get_suita_namemap()
    merged_voicebrigde.event_int = event1
    merged_voicebrigde.set_otx2inx(bob_otx, bob_inx)
    assert merged_translateunit.namemap == merged_voicebrigde
    merged_groupbrigde = get_swim_titlemap()
    merged_groupbrigde.event_int = event1
    assert merged_translateunit.titlemap == merged_groupbrigde
