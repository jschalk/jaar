from src.a00_data_toolbox.file_toolbox import create_path
from src.a18_etl_toolbox.a18_path import create_stances_dir_path
from src.a19_kpi_toolbox.kpi_mstr import (
    create_populate_kpi001_table,
    get_all_kpi_functions,
    get_bundles_config,
    get_default_kpi_bundle,
    get_kpi_set_from_bundle,
)
from src.a19_kpi_toolbox.test._util.a19_str import belief_kpi001_partner_nets_str


def test_get_default_kpi_bundle_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_kpi_bundle() == "default_kpi_bundle"


def test_get_all_kpi_functions_ReturnsObj():
    # ESTABLISH: Check if all_kpi_set is defined

    assert get_all_kpi_functions() is not None, "all_kpi_set should be defined"
    assert len(get_all_kpi_functions()) == 1
    assert get_all_kpi_functions() == {
        belief_kpi001_partner_nets_str(): create_populate_kpi001_table
    }


def test_get_bundles_config_ReturnsObj():
    # ESTABLISH: Check if bundles_config is defined

    assert get_bundles_config() is not None, "bundles_config should be defined"
    assert len(get_bundles_config()) == 1
    assert get_bundles_config() == {
        "default_kpi_bundle": {belief_kpi001_partner_nets_str()}
    }


def test_get_kpi_set_from_bundle_ReturnsObj_Scenario0_BundleGiven():
    # ESTABLISH / WHEN
    kpi_set = get_kpi_set_from_bundle("believer_star_kpis")

    # THEN
    assert kpi_set == set()


def test_get_kpi_set_from_bundle_ReturnsObj_Scenario1_NoBundleGiven():
    # ESTABLISH
    default_kpi_set = get_kpi_set_from_bundle("default_kpi_bundle")

    # WHEN
    kpi_set = get_kpi_set_from_bundle()

    # THEN
    assert kpi_set == {belief_kpi001_partner_nets_str()}
    assert kpi_set == default_kpi_set
