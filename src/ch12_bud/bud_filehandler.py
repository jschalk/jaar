from os import listdir as os_listdir
from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.ch01_py.dict_toolbox import get_empty_list_if_None
from src.ch01_py.file_toolbox import (
    create_path,
    get_dir_file_strs,
    open_json,
    save_json,
    set_dir,
)
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch09_belief_lesson._ref.ch09_path import (
    create_job_path,
    create_moment_beliefs_dir_path,
)
from src.ch09_belief_lesson.lesson_filehandler import open_belief_file, save_belief_file
from src.ch12_bud._ref.ch12_path import (
    CELLNODE_FILENAME,
    create_beliefspark_path,
    create_belieftime_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
)
from src.ch12_bud._ref.ch12_semantic_types import (
    BeliefName,
    EpochTime,
    LabelTerm,
    RopeTerm,
    SparkInt,
)
from src.ch12_bud.bud_main import BudUnit, get_budunit_from_dict
from src.ch12_bud.cell import CellUnit, cellunit_get_from_dict, cellunit_shop


def get_beliefspark_obj(
    moment_mstr_dir: str,
    moment_label: LabelTerm,
    belief_name: BeliefName,
    spark_num: int,
) -> BeliefUnit:
    beliefspark_json_path = create_beliefspark_path(
        moment_mstr_dir, moment_label, belief_name, spark_num
    )
    return open_belief_file(beliefspark_json_path)


def collect_belief_spark_dir_sets(
    moment_mstr_dir: str, moment_label: LabelTerm
) -> dict[BeliefName, set[SparkInt]]:
    x_dict = {}
    beliefs_dir = create_moment_beliefs_dir_path(moment_mstr_dir, moment_label)
    set_dir(beliefs_dir)
    for belief_name in os_listdir(beliefs_dir):
        belief_dir = create_path(beliefs_dir, belief_name)
        sparks_dir = create_path(belief_dir, "sparks")
        set_dir(sparks_dir)
        belief_sparks_dirs = {
            int(spark_num_folder)
            for spark_num_folder in os_listdir(sparks_dir)
            if os_path_isdir(create_path(sparks_dir, spark_num_folder))
        }
        x_dict[belief_name] = belief_sparks_dirs
    return x_dict


def get_beliefs_downhill_spark_nums(
    belief_sparks_sets: dict[BeliefName, set[SparkInt]],
    downhill_beliefs: set[BeliefName] = None,
    ref_spark_num: SparkInt = None,
) -> dict[BeliefName, SparkInt]:
    x_dict = {}
    if downhill_beliefs:
        for belief_name in downhill_beliefs:
            if spark_set := belief_sparks_sets.get(belief_name):
                _add_downhill_spark_num(x_dict, spark_set, ref_spark_num, belief_name)
    else:
        for belief_name, spark_set in belief_sparks_sets.items():
            _add_downhill_spark_num(x_dict, spark_set, ref_spark_num, belief_name)
    return x_dict


def _add_downhill_spark_num(
    x_dict: dict[BeliefName, SparkInt],
    spark_set: set[SparkInt],
    ref_spark_num: SparkInt,
    downhill_belief: BeliefName,
):
    if spark_set:
        if ref_spark_num:
            if downhill_spark_nums := {ei for ei in spark_set if ei <= ref_spark_num}:
                x_dict[downhill_belief] = max(downhill_spark_nums)
        else:
            x_dict[downhill_belief] = max(spark_set)


def save_arbitrary_beliefspark(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: str,
    spark_num: int,
    voices: list[list] = None,
    facts: list[tuple[RopeTerm, RopeTerm, float, float]] = None,
) -> str:
    voices = get_empty_list_if_None(voices)
    facts = get_empty_list_if_None(facts)
    x_beliefunit = beliefunit_shop(belief_name, moment_label)
    for voice_list in voices:
        try:
            voice_cred_lumen = voice_list[1]
        except Exception:
            voice_cred_lumen = None
        x_beliefunit.add_voiceunit(voice_list[0], voice_cred_lumen)
    for fact_tup in facts:
        x_reason_context = fact_tup[0]
        x_fact_state = fact_tup[1]
        x_fact_lower = fact_tup[2]
        x_fact_upper = fact_tup[3]
        x_beliefunit.add_fact(
            x_reason_context, x_fact_state, x_fact_lower, x_fact_upper, True
        )
    x_beliefspark_path = create_beliefspark_path(
        moment_mstr_dir, moment_label, belief_name, spark_num
    )
    save_json(x_beliefspark_path, None, x_beliefunit.to_dict())
    return x_beliefspark_path


def cellunit_add_json_file(
    moment_mstr_dir: str,
    moment_label: str,
    time_belief_name: str,
    bud_time: int,
    spark_num: int,
    bud_ancestors: list[BeliefName] = None,
    quota: int = None,
    celldepth: int = None,
    mana_grain: int = None,
):
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_label, time_belief_name, bud_time, bud_ancestors
    )
    x_cell = cellunit_shop(
        time_belief_name, bud_ancestors, spark_num, celldepth, mana_grain, quota
    )
    cellunit_save_to_dir(cell_dir, x_cell)


def cellunit_save_to_dir(dirpath: str, x_cell: CellUnit):
    save_json(dirpath, CELLNODE_FILENAME, x_cell.to_dict())


def cellunit_get_from_dir(dirpath: str) -> CellUnit:
    cell_json_path = create_path(dirpath, CELLNODE_FILENAME)
    if os_path_exists(cell_json_path):
        return cellunit_get_from_dict(open_json(cell_json_path))


def create_cell_voice_mandate_ledger_json(dirpath: str):
    if cell := cellunit_get_from_dir(dirpath):
        cell.calc_voice_mandate_ledger()
        save_json(dirpath, "cell_voice_mandate_ledger.json", cell._voice_mandate_ledger)


def save_bud_file(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud: BudUnit = None,
):
    x_bud.calc_magnitude()
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, belief_name, x_bud.bud_time
    )
    save_json(bud_json_path, None, x_bud.to_dict(), replace=True)


def bud_file_exists(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud_time: EpochTime = None,
) -> bool:
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, belief_name, x_bud_time
    )
    return os_path_exists(bud_json_path)


def open_bud_file(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud_time: EpochTime = None,
) -> BudUnit:
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, belief_name, x_bud_time
    )
    if bud_file_exists(moment_mstr_dir, moment_label, belief_name, x_bud_time):
        return get_budunit_from_dict(open_json(bud_json_path))


class _save_valid_belieftime_Exception(Exception):
    pass


def save_belieftime_file(
    moment_mstr_dir: str,
    x_belieftime: BeliefUnit,
    x_bud_time: EpochTime = None,
):
    x_belieftime.cashout()
    if x_belieftime.rational is False:
        raise _save_valid_belieftime_Exception(
            "BeliefTime could not be saved BeliefUnit.rational is False"
        )
    belieftime_json_path = create_belieftime_path(
        moment_mstr_dir,
        x_belieftime.moment_label,
        x_belieftime.belief_name,
        x_bud_time,
    )
    save_belief_file(belieftime_json_path, None, x_belieftime)


def belieftime_file_exists(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud_time: EpochTime = None,
) -> bool:
    belieftime_json_path = create_belieftime_path(
        moment_mstr_dir, moment_label, belief_name, x_bud_time
    )
    return os_path_exists(belieftime_json_path)


def open_belieftime_file(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud_time: EpochTime = None,
) -> bool:
    belieftime_json_path = create_belieftime_path(
        moment_mstr_dir, moment_label, belief_name, x_bud_time
    )
    # if self.belieftime_file_exists(x_bud_time):
    return open_belief_file(belieftime_json_path)


def get_epochtime_dirs(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> list[EpochTime]:
    buds_dir = create_buds_dir_path(moment_mstr_dir, moment_label, belief_name)
    x_dict = get_dir_file_strs(buds_dir, include_dirs=True, include_files=False)
    return [int(x_epochtime) for x_epochtime in sorted(list(x_dict.keys()))]
