from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch18_etl_toolbox.ch18_path import create_stances_dir_path
from src.ch19_kpi_toolbox._ref.ch19_terms import moment_kpi001_voice_nets_str
from src.ch19_kpi_toolbox.kpi_mstr import (
    create_populate_kpi001_table,
    get_all_kpi_functions,
    get_bundles_config,
    get_default_kpi_bundle,
    get_kpi_set_from_bundle,
)


def test_get_default_kpi_bundle_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_kpi_bundle() == "default_kpi_bundle"


def test_get_all_kpi_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN: Check if all_kpi_set is defined
    assert get_all_kpi_functions() is not None, "all_kpi_set should be defined"
    assert len(get_all_kpi_functions()) == 1
    assert get_all_kpi_functions() == {
        moment_kpi001_voice_nets_str(): create_populate_kpi001_table
    }


def test_get_bundles_config_ReturnsObj():
    # ESTABLISH / WHEN / THEN: Check if bundles_config is defined
    assert get_bundles_config() is not None, "bundles_config should be defined"
    assert len(get_bundles_config()) == 1
    assert get_bundles_config() == {
        "default_kpi_bundle": {moment_kpi001_voice_nets_str()}
    }


def test_get_kpi_set_from_bundle_ReturnsObj_Scenario0_WithBundle():
    # ESTABLISH / WHEN
    kpi_set = get_kpi_set_from_bundle("belief_no_reference_kpis")

    # THEN
    assert kpi_set == set()


def test_get_kpi_set_from_bundle_ReturnsObj_Scenario1_WithNoBundle():
    # ESTABLISH
    default_kpi_set = get_kpi_set_from_bundle("default_kpi_bundle")

    # WHEN
    kpi_set = get_kpi_set_from_bundle()

    # THEN
    assert kpi_set == {moment_kpi001_voice_nets_str()}
    assert kpi_set == default_kpi_set
