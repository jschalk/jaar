from src.ch01_py.file_toolbox import create_path
from src.ch12_bud._ref.ch12_semantic_types import BeliefName, MomentLabel

MOMENT_FILENAME = "moment.json"
BUDUNIT_FILENAME = "budunit.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_voice_mandate_ledger.json"
BELIEFTIME_FILENAME = "belieftime.json"
BELIEFSPARK_FILENAME = "belief.json"
SPARK_ALL_LESSON_FILENAME = "all_lesson.json"
SPARK_EXPRESSED_LESSON_FILENAME = "expressed_lesson.json"


def create_buds_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, belief_name: BeliefName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "buds")


def create_bud_dir_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time"""
    buds_dir = create_buds_dir_path(moment_mstr_dir, moment_label, belief_name)
    return create_path(buds_dir, bud_time)


def create_budunit_json_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\budunit.json"""
    epochtime_dir = create_bud_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time
    )
    return create_path(epochtime_dir, "budunit.json")


def create_belieftime_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\belieftime.json"""
    epochtime_dir = create_bud_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time
    )
    return create_path(epochtime_dir, "belieftime.json")


def create_cell_dir_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName],
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3"""
    bud_celldepth_dir = create_bud_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time
    )
    if bud_ancestors is None:
        bud_ancestors = []
    for ledger_belief in bud_ancestors:
        bud_celldepth_dir = create_path(bud_celldepth_dir, ledger_belief)
    return bud_celldepth_dir


def create_cell_json_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName] = None,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3\\cell.json"""
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_voice_mandate_ledger_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName] = None,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3\\cell_voice_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell_voice_mandate_ledger.json")


def create_belief_spark_dir_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    spark_num: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\sparks\\spark_num"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    moment_belief_dir = create_path(beliefs_dir, belief_name)
    moment_sparks_dir = create_path(moment_belief_dir, "sparks")
    return create_path(moment_sparks_dir, spark_num)


def create_beliefspark_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    spark_num: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\sparks\\spark_num\\belief.json"""
    belief_spark_dir_path = create_belief_spark_dir_path(
        moment_mstr_dir, moment_label, belief_name, spark_num
    )
    belief_filename = "belief.json"
    return create_path(belief_spark_dir_path, belief_filename)


def create_spark_all_lesson_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    spark_num: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\sparks\\spark_num\\all_lesson.json"""
    belief_spark_dir_path = create_belief_spark_dir_path(
        moment_mstr_dir, moment_label, belief_name, spark_num
    )
    all_lesson_filename = "all_lesson.json"
    return create_path(belief_spark_dir_path, all_lesson_filename)


def create_spark_expressed_lesson_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    spark_num: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\sparks\\spark_num\\expressed_lesson.json"""
    belief_spark_dir_path = create_belief_spark_dir_path(
        moment_mstr_dir, moment_label, belief_name, spark_num
    )
    expressed_lesson_filename = "expressed_lesson.json"
    return create_path(belief_spark_dir_path, expressed_lesson_filename)
