from ch41_wheel.wheel_logic import (
    FamilyUnit,
    familyunit_shop,
    PillarUnit,
    pillarunit_shop,
    FAMU_STATUSES,
    WheelUnit,
    wheelunit_shop,
)
from ch99_glossary.ch_keyword import Ch41Keywords as kw, ExampleStrs as exx
from pytest import raises as pytest_raises


def test_FamilyUnit_Exists():
    # ESTABLISH / WHEN
    x_familyunit = FamilyUnit()

    # THEN
    assert x_familyunit
    assert not x_familyunit.famu_name
    assert not x_familyunit.pillars
    assert not x_familyunit.prestige
    assert not x_familyunit.linchpin
    assert not x_familyunit.famu_status
    assert set(x_familyunit.__dict__.keys()) == {
        "famu_name",
        "pillars",
        kw.prestige,
        "linchpin",
        "famu_status",
    }


def test_FAMU_STATUSES_Exists():
    # ESTABLISH / WHEN / THEN
    assert FAMU_STATUSES == {kw.winning, kw.losing, kw.stable, None}


def test_FamilyUnit_set_famu_status_SetsAttr_Scenario0_FAMU_STATUSES():
    # ESTABLISH
    x_familyunit = FamilyUnit()
    assert x_familyunit.famu_status is None
    for x_famu_status in FAMU_STATUSES:
        # WHEN
        x_familyunit.set_famu_status(x_famu_status)
        # THEN
        assert x_familyunit.famu_status == x_famu_status


def test_FamilyUnit_set_famu_status_RaisesException_Scenario1_SetNonFamuStatus():
    # ESTABLISH
    sue_familyunit = FamilyUnit(famu_name=exx.sue)
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_familyunit.set_famu_status(exx.sweep)
    assert (
        str(excinfo.value)
        == f"FamilyUnit '{exx.sue}': '{exx.sweep}' is not acceptable famu_status."
    )


def test_FamilyUnit_set_famu_status_SetsAttr_Scenario1_Losing():
    # ESTABLISH
    x_familyunit = FamilyUnit()
    losing_str = "losing"
    assert x_familyunit.famu_status is None
    # WHEN
    x_familyunit.set_famu_status(losing_str)
    # THEN
    assert x_familyunit.famu_status == losing_str


def test_familyunit_shop_ReturnsObj_Scenario0_MinimumParameters():
    # ESTABLISH
    kennedy_str = "Kennedy"

    # WHEN
    familyunit = familyunit_shop(kennedy_str)

    # THEN
    assert familyunit
    assert familyunit.famu_name == kennedy_str
    assert familyunit.pillars == []
    assert familyunit.prestige is False
    assert familyunit.linchpin is False
    assert familyunit.famu_status is None


def test_familyunit_shop_ReturnsObj_Scenario1_MaxParameters():
    # ESTABLISH
    kennedy_str = "Kennedy"
    winning_str = "winning"

    # WHEN
    familyunit = familyunit_shop(famu_name=kennedy_str, famu_status=winning_str)

    # THEN
    assert familyunit
    assert familyunit.famu_name == kennedy_str
    assert familyunit.pillars == []
    assert familyunit.prestige is False
    assert familyunit.linchpin is False
    assert familyunit.famu_status == winning_str


def test_PillarUnit_Exists():
    # ESTABLISH / WHEN
    pillarunit = PillarUnit()

    # THEN
    assert pillarunit
    assert not pillarunit.pillar_name
    assert not pillarunit.bearers
    assert set(pillarunit.__dict__.keys()) == {"pillar_name", "bearers"}


def test_pillarunit_shop_ReturnsObj():
    # ESTABLISH
    sigma_phi_str = "sigma phi"
    # WHEN
    pillarunit = pillarunit_shop(sigma_phi_str)

    # THEN
    assert pillarunit
    assert pillarunit.pillar_name == sigma_phi_str
    assert pillarunit.bearers == {}


def test_WheelUnit_Exists():
    # ESTABLISH / WHEN
    x_wheelunit = WheelUnit()
    # THEN
    assert not x_wheelunit.wheel_name
    assert not x_wheelunit.familys
    assert set(x_wheelunit.__dict__.keys()) == {"wheel_name", "familys"}


def test_wheelunit_shop_ReturnsObj():
    # ESTABLISH
    paris_str = "Paris"
    # WHEN
    paris_wheelunit = wheelunit_shop(paris_str)
    # THEN
    assert paris_wheelunit.wheel_name == paris_str
    assert not paris_wheelunit.familys == {}


# TODO complete these tests
# def test_WheelUnit_get_stable_familys_ReturnsObj():
#     # ESTABLISH
#     paris_wheelunit =

# def test_WheelUnit_get_winning_familys_ReturnsObj():
#     # ESTABLISH
#     paris_wheelunit =

# def test_WheelUnit_get_losing_familys_ReturnsObj():
#     # ESTABLISH
#     paris_wheelunit =

# def test_WheelUnit_get_no_prestige_familys_ReturnsObj():
#     # ESTABLISH
#     paris_wheelunit =
