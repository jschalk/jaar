from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_row_count,
    get_table_columns,
)
from src.a01_term_logic.rope import create_rope
from src.a02_finance_logic._util.a02_str import owner_name_str, vow_label_str
from src.a04_reason_logic._util.a04_str import _active_str, _chore_str
from src.a05_concept_logic._util.a05_str import concept_rope_str, task_str
from src.a06_plan_logic._util.a06_str import plan_conceptunit_str
from src.a18_etl_toolbox._util.a18_str import owner_net_amount_str, vow_acct_nets_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    CREATE_JOB_PLNCONC_SQLSTR,
    CREATE_VOW_ACCT_NETS_SQLSTR,
    create_prime_tablename,
)
from src.a19_kpi_toolbox._util.a19_str import vow_kpi001_acct_nets_str
from src.a19_kpi_toolbox.kpi_mstr import (
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
    # ESTABLISH: Check if all_kpi_set is defined

    assert get_all_kpi_functions() is not None, "all_kpi_set should be defined"
    assert len(get_all_kpi_functions()) == 1
    assert get_all_kpi_functions() == {
        vow_kpi001_acct_nets_str(): create_populate_kpi001_table
    }


def test_get_bundles_config_ReturnsObj():
    # ESTABLISH: Check if bundles_config is defined

    assert get_bundles_config() is not None, "bundles_config should be defined"
    assert len(get_bundles_config()) == 1
    assert get_bundles_config() == {"default_kpi_bundle": {vow_kpi001_acct_nets_str()}}


def test_get_kpi_set_from_bundle_ReturnsObj_Scenario0_BundleGiven():
    # ESTABLISH / WHEN
    kpi_set = get_kpi_set_from_bundle("plan_star_kpis")

    # THEN
    assert kpi_set == set()


def test_get_kpi_set_from_bundle_ReturnsObj_Scenario1_NoBundleGiven():
    # ESTABLISH
    default_kpi_set = get_kpi_set_from_bundle("default_kpi_bundle")

    # WHEN
    kpi_set = get_kpi_set_from_bundle()

    # THEN
    assert kpi_set == {vow_kpi001_acct_nets_str()}
    assert kpi_set == default_kpi_set
