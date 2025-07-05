from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.a00_data_toolbox.file_toolbox import create_path
from src.a04_reason_logic.test._util.a04_str import belief_label_str
from src.a09_pack_logic.test._util.a09_str import believer_name_str
from src.a18_etl_toolbox.a18_path import (
    create_belief_ote1_csv_path,
    create_belief_ote1_json_path,
    create_last_run_metrics_path,
    create_stance0001_path,
    create_stances_believer_dir_path,
    create_stances_dir_path,
    create_world_db_path,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)

STANCE0001_FILENAME = "stance0001.xlsx"
BELIEF_OTE1_AGG_CSV_FILENAME = "belief_ote1_agg.csv"
BELIEF_OTE1_AGG_JSON_FILENAME = "belief_ote1_agg.json"
LAST_RUN_METRICS_JSON_FILENAME = "last_run_metrics.json"
WORLD_DB_FILENAME = "world.db"


def test_a18_path_constants_are_values():
    # ESTABLISH / WHEN / THEN
    assert BELIEF_OTE1_AGG_CSV_FILENAME == "belief_ote1_agg.csv"
    assert BELIEF_OTE1_AGG_JSON_FILENAME == "belief_ote1_agg.json"
    assert LAST_RUN_METRICS_JSON_FILENAME == "last_run_metrics.json"
    assert STANCE0001_FILENAME == "stance0001.xlsx"
    assert WORLD_DB_FILENAME == "world.db"


def test_create_last_run_metrics_path_ReturnsObj():
    # ESTABLISH
    x_world_dir = get_module_temp_dir()

    # WHEN
    gen_last_run_metrics_path = create_last_run_metrics_path(x_world_dir)

    # THEN
    expected_path = create_path(x_world_dir, LAST_RUN_METRICS_JSON_FILENAME)
    assert gen_last_run_metrics_path == expected_path


def test_create_stances_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()

    # WHEN
    gen_bob_stance_dir = create_stances_dir_path(x_belief_mstr_dir)

    # THEN
    expected_stances_dir = create_path(x_belief_mstr_dir, "stances")
    assert gen_bob_stance_dir == expected_stances_dir


def test_create_stances_believer_dir_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"

    # WHEN
    gen_bob_stance_dir = create_stances_believer_dir_path(x_belief_mstr_dir, bob_str)

    # THEN
    stances_dir = create_stances_dir_path(x_belief_mstr_dir)
    expected_bob_stance_dir = create_path(stances_dir, bob_str)
    assert gen_bob_stance_dir == expected_bob_stance_dir


def test_create_stance0001_path_ReturnsObj():
    # ESTABLISH
    output_dir = get_module_temp_dir()

    # WHEN
    gen_stance0001_xlsx_path = create_stance0001_path(output_dir)

    # THEN
    expected_stance000001_path = create_path(output_dir, STANCE0001_FILENAME)
    assert gen_stance0001_xlsx_path == expected_stance000001_path


LINUX_OS = platform_system() == "Linux"


def test_create_last_run_metrics_path_HasDocString():
    # ESTABLISH
    doc_str = create_last_run_metrics_path("world_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_last_run_metrics_path) == doc_str


def test_create_stances_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_stances_dir_path(belief_mstr_dir="belief_mstr_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stances_dir_path) == doc_str


def test_create_stances_believer_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_stances_believer_dir_path(
        belief_mstr_dir="belief_mstr_dir", believer_name=believer_name_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stances_believer_dir_path) == doc_str


def test_create_stance0001_path_HasDocString():
    # ESTABLISH
    doc_str = create_stance0001_path(output_dir="output_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_stance0001_path) == doc_str


def test_create_belief_ote1_csv_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"

    # WHEN
    gen_a23_te_csv_path = create_belief_ote1_csv_path(x_belief_mstr_dir, a23_str)

    # THEN
    beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_path = create_path(beliefs_dir, a23_str)
    expected_a23_te_path = create_path(a23_path, BELIEF_OTE1_AGG_CSV_FILENAME)
    assert gen_a23_te_csv_path == expected_a23_te_path


def test_create_belief_ote1_json_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"

    # WHEN
    gen_a23_te_csv_path = create_belief_ote1_json_path(x_belief_mstr_dir, a23_str)

    # THEN
    beliefs_dir = create_path(x_belief_mstr_dir, "beliefs")
    a23_path = create_path(beliefs_dir, a23_str)
    expected_a23_te_path = create_path(a23_path, BELIEF_OTE1_AGG_JSON_FILENAME)
    assert gen_a23_te_csv_path == expected_a23_te_path


def test_create_world_db_path_ReturnsObj():
    # ESTABLISH
    x_belief_mstr_dir = get_module_temp_dir()
    a23_str = "amy23"

    # WHEN
    gen_world_db_path = create_world_db_path(x_belief_mstr_dir)

    # THEN
    expected_path = create_path(x_belief_mstr_dir, WORLD_DB_FILENAME)
    assert gen_world_db_path == expected_path


def test_create_belief_ote1_csv_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_ote1_csv_path("belief_mstr_dir", belief_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_ote1_csv_path) == doc_str


def test_create_belief_ote1_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_ote1_json_path("belief_mstr_dir", belief_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_ote1_json_path) == doc_str


def test_create_world_db_path_HasDocString():
    # ESTABLISH
    doc_str = create_world_db_path("belief_mstr_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_world_db_path) == doc_str
