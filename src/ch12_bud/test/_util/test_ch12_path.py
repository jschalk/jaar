from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch01_py.file_toolbox import create_path
from src.ch12_bud._ref.ch12_path import (
    BELIEFSPARK_FILENAME,
    BELIEFTIME_FILENAME,
    BUDUNIT_FILENAME,
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    MOMENT_FILENAME,
    SPARK_ALL_LESSON_FILENAME,
    SPARK_EXPRESSED_LESSON_FILENAME,
    create_belief_spark_dir_path,
    create_beliefspark_path,
    create_belieftime_path,
    create_bud_dir_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_cell_voice_mandate_ledger_path,
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path,
)
from src.ch12_bud.test._util.ch12_env import get_temp_dir
from src.ref.keywords import Ch12Keywords as kw


def test_create_buds_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"

    # WHEN
    buds_dir = create_buds_dir_path(x_moment_mstr_dir, amy23_str, sue_str)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, amy23_str)
    beliefs_dir = create_path(amy23_dir, "beliefs")
    sue_dir = create_path(beliefs_dir, sue_str)
    expected_buds_dir = create_path(sue_dir, "buds")
    assert buds_dir == expected_buds_dir


def test_create_bud_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    amy23_str = "amy23"
    sue_str = "Sue"
    epochtime7 = 7

    # WHEN
    generated_epochtime_dir = create_bud_dir_path(
        x_moment_mstr_dir, amy23_str, sue_str, epochtime7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, amy23_str)
    beliefs_dir = create_path(amy23_dir, "beliefs")
    sue_dir = create_path(beliefs_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    expected_epochtime_dir = create_path(buds_dir, epochtime7)
    assert generated_epochtime_dir == expected_epochtime_dir


def test_create_budunit_json_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    epochtime7 = 7

    # WHEN
    gen_bud_path = create_budunit_json_path(
        x_moment_mstr_dir, a23_str, sue_str, epochtime7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, a23_str)
    beliefs_dir = create_path(amy23_dir, "beliefs")
    sue_dir = create_path(beliefs_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    epochtime_dir = create_path(buds_dir, epochtime7)
    expected_bud_path_dir = create_path(epochtime_dir, BUDUNIT_FILENAME)
    assert gen_bud_path == expected_bud_path_dir


def test_create_belieftime_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    epochtime7 = 7

    # WHEN
    gen_belieftime_path = create_belieftime_path(
        x_moment_mstr_dir, a23_str, sue_str, epochtime7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, a23_str)
    beliefs_dir = create_path(amy23_dir, "beliefs")
    sue_dir = create_path(beliefs_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    epochtime_dir = create_path(buds_dir, epochtime7)
    expected_belieftime_path_dir = create_path(epochtime_dir, BELIEFTIME_FILENAME)
    assert gen_belieftime_path == expected_belieftime_path_dir


def test_create_cell_dir_path_ReturnsObj_Scenario0_No_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7

    # WHEN
    gen_cell_dir = create_cell_dir_path(x_moment_mstr_dir, a23_str, sue_str, tp7, [])

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, a23_str, sue_str, tp7)
    assert gen_cell_dir == epochtime_dir


def test_create_cell_dir_path_ReturnsObj_Scenario1_One_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    x_bud_ancestors = [yao_str]

    # WHEN
    gen_cell_dir = create_cell_dir_path(
        x_moment_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(epochtime_dir, yao_str)
    assert gen_cell_dir == tp_yao_dir


def test_create_cell_dir_path_ReturnsObj_Scenario2_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bud_ancestors = [yao_str, bob_str, zia_str]

    # WHEN
    gen_bud_celldepth_dir_path = create_cell_dir_path(
        x_moment_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(epochtime_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_tp_yao_bob_zia_dir = create_path(tp_yao_bob_dir, zia_str)
    assert gen_bud_celldepth_dir_path == expected_tp_yao_bob_zia_dir


def test_create_cell_json_path_ReturnsObj_Scenario0_Empty_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    epochtime7 = 7

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_moment_mstr_dir, a23_str, sue_str, epochtime7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, a23_str)
    beliefs_dir = create_path(amy23_dir, "beliefs")
    sue_dir = create_path(beliefs_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    epochtime_dir = create_path(buds_dir, epochtime7)
    expected_cell_json_path = create_path(epochtime_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_json_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    bud_ancestors = [yao_str, bob_str]

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_moment_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(epochtime_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_voice_mandate_ledger_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_str = "amy23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    bud_ancestors = [yao_str, bob_str]

    # WHEN
    gen_cell_json_path = create_cell_voice_mandate_ledger_path(
        x_moment_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    epochtime_dir = create_bud_dir_path(x_moment_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(epochtime_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELL_MANDATE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_belief_spark_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    amy23_str = "amy23"
    bob_str = "Bob"
    spark3 = 3

    # WHEN
    gen_a23_e3_dir_path = create_belief_spark_dir_path(
        x_moment_mstr_dir, amy23_str, bob_str, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, amy23_str)
    a23_beliefs_dir = create_path(a23_dir, "beliefs")
    a23_bob_dir = create_path(a23_beliefs_dir, bob_str)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    expected_a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    assert gen_a23_e3_dir_path == expected_a23_bob_e3_dir


def test_create_beliefspark_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    amy23_str = "amy23"
    bob_str = "Bob"
    spark3 = 3

    # WHEN
    gen_a23_e3_belief_path = create_beliefspark_path(
        x_moment_mstr_dir, amy23_str, bob_str, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, amy23_str)
    a23_beliefs_dir = create_path(a23_dir, "beliefs")
    a23_bob_dir = create_path(a23_beliefs_dir, bob_str)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_belief_path = create_path(a23_bob_e3_dir, BELIEFSPARK_FILENAME)
    assert gen_a23_e3_belief_path == expected_a23_bob_e3_belief_path


def test_create_spark_all_lesson_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    amy23_str = "amy23"
    bob_str = "Bob"
    spark3 = 3

    # WHEN
    gen_a23_e3_belief_path = create_spark_all_lesson_path(
        x_moment_mstr_dir, amy23_str, bob_str, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, amy23_str)
    a23_beliefs_dir = create_path(a23_dir, "beliefs")
    a23_bob_dir = create_path(a23_beliefs_dir, bob_str)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_all_lesson_path = create_path(
        a23_bob_e3_dir, SPARK_ALL_LESSON_FILENAME
    )
    assert gen_a23_e3_belief_path == expected_a23_bob_e3_all_lesson_path


def test_create_spark_expressed_lesson_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    amy23_str = "amy23"
    bob_str = "Bob"
    spark3 = 3

    # WHEN
    gen_a23_e3_belief_path = create_spark_expressed_lesson_path(
        x_moment_mstr_dir, amy23_str, bob_str, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, amy23_str)
    a23_beliefs_dir = create_path(a23_dir, "beliefs")
    a23_bob_dir = create_path(a23_beliefs_dir, bob_str)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_expressed_lesson_path = create_path(
        a23_bob_e3_dir, SPARK_EXPRESSED_LESSON_FILENAME
    )
    assert gen_a23_e3_belief_path == expected_a23_bob_e3_expressed_lesson_path


LINUX_OS = platform_system() == "Linux"


def test_create_buds_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_buds_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_buds_dir_path) == doc_str


def test_create_bud_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_dir_path) == doc_str


def test_create_cell_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_belief1", "ledger_belief2", "ledger_belief3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_dir_path) == doc_str


def test_create_cell_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_json_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_belief1", "ledger_belief2", "ledger_belief3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_json_path) == doc_str


def test_create_cell_voice_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_voice_mandate_ledger_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_belief1", "ledger_belief2", "ledger_belief3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_voice_mandate_ledger_path) == doc_str


def test_create_budunit_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_budunit_json_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budunit_json_path) == doc_str


def test_create_belieftime_path_HasDocString():
    # ESTABLISH
    doc_str = create_belieftime_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belieftime_path) == doc_str


def test_create_belief_spark_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_spark_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_spark_dir_path) == doc_str


def test_create_beliefspark_path_HasDocString():
    # ESTABLISH
    doc_str = create_beliefspark_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_beliefspark_path) == doc_str


def test_create_spark_all_lesson_path_HasDocString():
    # ESTABLISH
    doc_str = create_spark_all_lesson_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_spark_all_lesson_path) == doc_str


def test_create_spark_expressed_lesson_path_HasDocString():
    # ESTABLISH
    doc_str = create_spark_expressed_lesson_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_label=kw.moment_label,
        belief_name=kw.belief_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_spark_expressed_lesson_path) == doc_str
