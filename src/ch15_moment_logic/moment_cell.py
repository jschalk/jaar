from copy import copy as copy_copy
from dataclasses import dataclass
from os import sep as os_sep, walk as os_walk
from os.path import exists as os_path_exists, join as os_path_join
from src.ch01_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_json,
    save_json,
)
from src.ch03_allot_toolbox.allot import allot_nested_scale
from src.ch05_reason_logic.reason import get_dict_from_factunits
from src.ch08_epoch_logic.epoch_main import EpochPoint
from src.ch11_bud_logic._ref.ch11_semantic_types import BeliefName, LabelTerm
from src.ch11_bud_logic.bud import MomentLabel
from src.ch11_bud_logic.cell import CellUnit, cellunit_shop
from src.ch11_bud_logic.weighted_facts_tool import get_nodes_with_weighted_facts
from src.ch12_pack_file._ref.ch12_path import (
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    create_beliefevent_path,
    create_bud_dir_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_moment_json_path,
)
from src.ch12_pack_file.packfilehandler import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_belief_event_dir_sets,
    create_cell_voice_mandate_ledger_json,
    get_beliefevent_obj,
    get_beliefs_downhill_event_ints,
    open_belief_file,
)
from src.ch15_moment_logic._ref.ch15_path import BUD_MANDATE_FILENAME
from src.ch15_moment_logic._ref.ch15_semantic_types import FundNum
from src.ch15_moment_logic.moment_main import get_momentunit_from_dict


def create_moment_beliefs_cell_trees(moment_mstr_dir, moment_label):
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    for belief_name in get_level1_dirs(beliefs_dir):
        belief_dir = create_path(beliefs_dir, belief_name)
        buds_dir = create_path(belief_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            create_cell_tree(moment_mstr_dir, moment_label, belief_name, bud_time)


def create_cell_tree(moment_mstr_dir, moment_label, bud_belief_name, bud_time):
    root_cell_json_path = create_cell_json_path(
        moment_mstr_dir, moment_label, bud_belief_name, bud_time
    )
    if os_path_exists(root_cell_json_path):
        _exists_create_cell_tree(
            moment_mstr_dir, moment_label, bud_belief_name, bud_time
        )


def _exists_create_cell_tree(moment_mstr_dir, moment_label, bud_belief_name, bud_time):
    root_cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_label, bud_belief_name, bud_time, []
    )
    cells_to_evaluate = [cellunit_get_from_dir(root_cell_dir)]
    belief_events_sets = collect_belief_event_dir_sets(moment_mstr_dir, moment_label)
    while cells_to_evaluate != []:
        parent_cell = cells_to_evaluate.pop()
        cell_belief_name = parent_cell.get_cell_belief_name()
        e_int = parent_cell.event_int
        beliefevent = get_beliefevent_obj(
            moment_mstr_dir, moment_label, cell_belief_name, e_int
        )
        parent_cell.eval_beliefevent(beliefevent)
        parent_cell_dir = create_cell_dir_path(
            moment_mstr_dir,
            moment_label,
            bud_belief_name,
            bud_time,
            parent_cell.ancestors,
        )
        cellunit_save_to_dir(parent_cell_dir, parent_cell)
        parent_quota_ledger = parent_cell.get_beliefevents_quota_ledger()
        if parent_cell.celldepth > 0:
            child_celldepth = parent_cell.celldepth - 1
            parent_quota_beliefs = set(parent_quota_ledger.keys())
            beliefs_downhill_events_ints = get_beliefs_downhill_event_ints(
                belief_events_sets, parent_quota_beliefs, parent_cell.event_int
            )
            for quota_belief, quota_amount in parent_quota_ledger.items():
                if downhill_event_int := beliefs_downhill_events_ints.get(quota_belief):
                    if quota_amount > 0:
                        child_ancestors = list(copy_copy(parent_cell.ancestors))
                        child_ancestors.append(quota_belief)
                        child_cellunit = cellunit_shop(
                            ancestors=child_ancestors,
                            event_int=downhill_event_int,
                            celldepth=child_celldepth,
                            bud_belief_name=bud_belief_name,
                            money_grain=parent_cell.money_grain,
                            quota=quota_amount,
                        )
                        cells_to_evaluate.append(child_cellunit)


def load_cells_beliefevent(moment_mstr_dir: str, moment_label: LabelTerm):
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    for belief_name in get_level1_dirs(beliefs_dir):
        belief_dir = create_path(beliefs_dir, belief_name)
        buds_dir = create_path(belief_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            for dirpath, dirnames, filenames in os_walk(bud_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    _load_cell_beliefevent(moment_mstr_dir, moment_label, dirpath)


def _load_cell_beliefevent(moment_mstr_dir, moment_label, dirpath):
    x_cellunit = cellunit_get_from_dir(dirpath)
    cell_belief_name = x_cellunit.get_cell_belief_name()
    event_int = x_cellunit.event_int
    beliefevent = get_beliefevent_obj(
        moment_mstr_dir, moment_label, cell_belief_name, event_int
    )
    x_cellunit.eval_beliefevent(beliefevent)
    cellunit_save_to_dir(dirpath, x_cellunit)


def set_cell_trees_found_facts(moment_mstr_dir: str, moment_label: LabelTerm):
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    for belief_name in get_level1_dirs(beliefs_dir):
        belief_dir = create_path(beliefs_dir, belief_name)
        buds_dir = create_path(belief_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            cell_dirs = [
                dirpath
                for dirpath, dirnames, filenames in os_walk(bud_time_dir)
                if CELLNODE_FILENAME in set(filenames)
            ]
            _set_cell_found_facts(bud_time_dir, cell_dirs)


def _set_cell_found_facts(bud_time_dir: str, cell_dirs: list[str]):
    nodes_facts_dict = {}
    nodes_quotas_dict = {}
    for dirpath in cell_dirs:
        x_cell = cellunit_get_from_dir(dirpath)
        bud_path = dirpath.replace(bud_time_dir, "")
        cell_beliefs_tuple = tuple(bud_path.split(os_sep)[1:])
        nodes_facts_dict[cell_beliefs_tuple] = x_cell.beliefevent_facts
        nodes_quotas_dict[cell_beliefs_tuple] = x_cell.get_beliefevents_quota_ledger()

    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quotas_dict)
    dst_dir_facts = {
        os_path_join(bud_time_dir, *node_addr): get_dict_from_factunits(facts)
        for node_addr, facts in nodes_wgt_facts.items()
    }
    for dst_dir, dst_facts_dict in dst_dir_facts.items():
        dst_cell = cellunit_get_from_dir(dst_dir)
        dst_cell.set_found_facts_from_dict(dst_facts_dict)
        cellunit_save_to_dir(dst_dir, dst_cell)


def set_cell_trees_decrees(moment_mstr_dir: str, moment_label: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    for belief_name in get_level1_dirs(beliefs_dir):
        belief_dir = create_path(beliefs_dir, belief_name)
        buds_dir = create_path(belief_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            set_cell_tree_decrees(
                moment_mstr_dir, moment_label, belief_name, bud_time, bud_time_dir
            )


@dataclass
class DecreeUnit:
    parent_cell_dir: str = None
    cell_dir: str = None
    cell_ancestors: list[BeliefName] = None
    cell_belief_name: BeliefName = None
    cell_mandate: dict[BeliefName, FundNum] = None
    cell_celldepth: int = None
    root_cell_bool: bool = None
    event_int: int = None

    def get_child_cell_ancestors(self, child_belief_name: BeliefName):
        child_cell_ancestors = copy_copy(self.cell_ancestors)
        child_cell_ancestors.append(child_belief_name)
        return child_cell_ancestors


def set_cell_tree_decrees(
    mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: EpochPoint,
    bud_time_dir: str,
):
    # clear all current child directorys
    # create root bud tree node
    # grab boss facts from parent_cell (does not apply to root)
    # grab found facts for that cell
    # grab beliefevent for that cell
    # add all found_facts that exist in beliefevent to beliefevent
    # add all boss facts that exist in beliefevent to beliefevent
    # calculate beliefadjust
    # grab voice_agenda_fund_agenda_give ledger
    # add nodes to to_evalute_cellnodes based on voice_agenda_fund_give beliefs
    root_cell = cellunit_get_from_dir(bud_time_dir)
    root_cell_dir = create_cell_dir_path(
        mstr_dir, moment_label, belief_name, bud_time, []
    )
    root_decree = DecreeUnit(
        parent_cell_dir=None,
        cell_dir=root_cell_dir,
        cell_ancestors=[],
        cell_belief_name=belief_name,
        cell_mandate=root_cell.quota,
        cell_celldepth=root_cell.celldepth,
        root_cell_bool=True,
        event_int=root_cell.event_int,
    )
    to_evaluate_decreeunits = [root_decree]
    while to_evaluate_decreeunits != []:
        x_decree = to_evaluate_decreeunits.pop()
        if x_cell := cellunit_get_from_dir(
            x_decree.cell_dir
        ) or generate_cell_from_decree(x_decree, mstr_dir, moment_label, belief_name):
            x_cell.mandate = x_decree.cell_mandate
            parent_cell_dir = x_decree.parent_cell_dir
            _set_cell_boss_facts(x_cell, parent_cell_dir, x_decree.root_cell_bool)
            x_cell.calc_voice_mandate_ledger()
            cellunit_save_to_dir(x_decree.cell_dir, x_cell)
            if x_decree.cell_celldepth > 0:
                _add_child_decrees(
                    to_evaluate_decreeunits,
                    x_cell=x_cell,
                    x_decree=x_decree,
                    mstr_dir=mstr_dir,
                    moment_label=moment_label,
                    belief_name=belief_name,
                    bud_time=bud_time,
                )


def _add_child_decrees(
    to_evaluate_decreeunits: list[DecreeUnit],
    x_cell: CellUnit,
    x_decree: DecreeUnit,
    mstr_dir,
    moment_label: str,
    belief_name: str,
    bud_time: int,
):
    for child_belief_name, child_mandate in x_cell._voice_mandate_ledger.items():
        child_cell_ancestors = x_decree.get_child_cell_ancestors(child_belief_name)
        child_dir = create_cell_dir_path(
            mstr_dir, moment_label, belief_name, bud_time, child_cell_ancestors
        )
        child_decreeunit = DecreeUnit(
            parent_cell_dir=x_decree.cell_dir,
            cell_dir=child_dir,
            cell_ancestors=child_cell_ancestors,
            cell_belief_name=child_belief_name,
            cell_mandate=child_mandate,
            cell_celldepth=x_decree.cell_celldepth - 1,
            event_int=x_cell.event_int,
        )
        to_evaluate_decreeunits.append(child_decreeunit)


def _set_cell_boss_facts(cell: CellUnit, parent_cell_dir: str, root_cell_bool: bool):
    if root_cell_bool:
        cell.set_boss_facts_from_other_facts()
    else:
        cell.boss_facts = cellunit_get_from_dir(parent_cell_dir).boss_facts
        cell.add_other_facts_to_boss_facts()


def generate_cell_from_decree(
    x_decree: DecreeUnit, mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> CellUnit:
    cell_belief_name = x_decree.cell_belief_name
    beliefs_downhill_events_ints = get_beliefs_downhill_event_ints(
        belief_events_sets=collect_belief_event_dir_sets(mstr_dir, moment_label),
        downhill_beliefs={cell_belief_name},
        ref_event_int=x_decree.event_int,
    )
    if downhill_event_int := beliefs_downhill_events_ints.get(cell_belief_name):
        beliefevent_path = create_beliefevent_path(
            mstr_dir, moment_label, cell_belief_name, downhill_event_int
        )
        beliefevent = open_belief_file(beliefevent_path)
        x_cell = cellunit_shop(
            bud_belief_name=belief_name,
            ancestors=x_decree.get_child_cell_ancestors(cell_belief_name),
            event_int=downhill_event_int,
            celldepth=x_decree.cell_celldepth,
            money_grain=beliefevent.money_grain,
            quota=None,
            mandate=x_decree.cell_mandate,
        )
        x_cell.eval_beliefevent(beliefevent)
        return x_cell


def set_cell_tree_cell_mandates(moment_mstr_dir: str, moment_label: str):
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    for belief_name in get_level1_dirs(beliefs_dir):
        belief_dir = create_path(beliefs_dir, belief_name)
        buds_dir = create_path(belief_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            for dirpath, dirnames, filenames in os_walk(bud_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    create_cell_voice_mandate_ledger_json(dirpath)


def create_bud_mandate_ledgers(moment_mstr_dir: str, moment_label: str):
    moment_json_path = create_moment_json_path(moment_mstr_dir, moment_label)
    momentunit = get_momentunit_from_dict(open_json(moment_json_path))
    for beliefbudhistory in momentunit.beliefbudhistorys.values():
        for budunit in beliefbudhistory.buds.values():
            bud_root_dir = create_bud_dir_path(
                moment_mstr_dir,
                moment_label,
                belief_name=beliefbudhistory.belief_name,
                bud_time=budunit.bud_time,
            )
            bud_voice_mandate_ledger = allot_nested_scale(
                bud_root_dir,
                src_filename=CELL_MANDATE_FILENAME,
                scale_number=budunit.quota,
                grain_unit=momentunit.money_grain,
                depth=budunit.celldepth,
                dst_filename=BUD_MANDATE_FILENAME,
            )
            save_json(bud_root_dir, BUD_MANDATE_FILENAME, bud_voice_mandate_ledger)
            budunit._bud_voice_nets = bud_voice_mandate_ledger
    save_json(moment_json_path, None, momentunit.to_dict())
