from src.ch19_world_kpi.kpi_mstr import (
    create_populate_kpi001_table,
    create_populate_kpi002_table,
    get_all_kpi_functions,
    get_bundles_config,
    get_kpi_set_from_bundle,
)
from src.ref.keywords import Ch19Keywords as wx


def test_get_all_kpi_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN: Check if all_kpi_set is defined
    assert get_all_kpi_functions() is not None, "all_kpi_set should be defined"
    assert len(get_all_kpi_functions()) == 2
    assert get_all_kpi_functions() == {
        wx.moment_kpi001_voice_nets: create_populate_kpi001_table,
        wx.moment_kpi002_belief_pledges: create_populate_kpi002_table,
    }


def test_get_bundles_config_ReturnsObj():
    # ESTABLISH / WHEN / THEN: Check if bundles_config is defined
    assert get_bundles_config() is not None, "bundles_config should be defined"
    assert len(get_bundles_config()) == 1
    assert get_bundles_config() == {
        wx.default_kpi_bundle: {
            wx.moment_kpi001_voice_nets,
            wx.moment_kpi002_belief_pledges,
        }
    }


def test_get_kpi_set_from_bundle_ReturnsObj_Scenario0_WithBundle():
    # ESTABLISH / WHEN
    kpi_set = get_kpi_set_from_bundle("belief_no_reference_kpis")

    # THEN
    assert kpi_set == set()


def test_get_kpi_set_from_bundle_ReturnsObj_Scenario1_WithNoBundle():
    # ESTABLISH
    default_kpi_set = get_kpi_set_from_bundle(wx.default_kpi_bundle)

    # WHEN
    kpi_set = get_kpi_set_from_bundle()

    # THEN
    assert kpi_set == default_kpi_set
