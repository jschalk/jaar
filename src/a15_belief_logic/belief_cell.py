from copy import copy as copy_copy
from dataclasses import dataclass
from os import sep as os_sep, walk as os_walk
from os.path import exists as os_path_exists, join as os_path_join
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_json,
    save_json,
)
from src.a01_term_logic.term import BelieverName, LabelTerm
from src.a02_finance_logic.allot import allot_nested_scale
from src.a02_finance_logic.finance_config import FundNum, TimeLinePoint
from src.a04_reason_logic.reason_plan import get_dict_from_factunits
from src.a11_bud_logic.bud import BeliefLabel
from src.a11_bud_logic.cell import CellUnit, cellunit_shop
from src.a12_hub_toolbox.a12_path import (
    BUD_MANDATE_FILENAME,
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    create_belief_json_path,
    create_believerevent_path,
    create_bud_dir_path,
    create_cell_dir_path,
    create_cell_json_path,
)
from src.a12_hub_toolbox.fact_tool import get_nodes_with_weighted_facts
from src.a12_hub_toolbox.hub_tool import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_believer_event_dir_sets,
    create_cell_person_mandate_ledger_json,
    get_believerevent_obj,
    get_believers_downhill_event_ints,
    open_believer_file,
)
from src.a15_belief_logic.belief import get_from_dict as beliefunit_get_from_dict


def create_belief_believers_cell_trees(belief_mstr_dir, belief_label):
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    for believer_name in get_level1_dirs(believers_dir):
        believer_dir = create_path(believers_dir, believer_name)
        buds_dir = create_path(believer_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            create_cell_tree(belief_mstr_dir, belief_label, believer_name, bud_time)


def create_cell_tree(belief_mstr_dir, belief_label, bud_believer_name, bud_time):
    root_cell_json_path = create_cell_json_path(
        belief_mstr_dir, belief_label, bud_believer_name, bud_time
    )
    if os_path_exists(root_cell_json_path):
        _exists_create_cell_tree(
            belief_mstr_dir, belief_label, bud_believer_name, bud_time
        )


def _exists_create_cell_tree(
    belief_mstr_dir, belief_label, bud_believer_name, bud_time
):
    root_cell_dir = create_cell_dir_path(
        belief_mstr_dir, belief_label, bud_believer_name, bud_time, []
    )
    cells_to_evaluate = [cellunit_get_from_dir(root_cell_dir)]
    believer_events_sets = collect_believer_event_dir_sets(
        belief_mstr_dir, belief_label
    )
    while cells_to_evaluate != []:
        parent_cell = cells_to_evaluate.pop()
        cell_believer_name = parent_cell.get_cell_believer_name()
        e_int = parent_cell.event_int
        believerevent = get_believerevent_obj(
            belief_mstr_dir, belief_label, cell_believer_name, e_int
        )
        parent_cell.eval_believerevent(believerevent)
        parent_cell_dir = create_cell_dir_path(
            belief_mstr_dir,
            belief_label,
            bud_believer_name,
            bud_time,
            parent_cell.ancestors,
        )
        cellunit_save_to_dir(parent_cell_dir, parent_cell)
        parent_quota_ledger = parent_cell.get_believerevents_quota_ledger()
        if parent_cell.celldepth > 0:
            child_celldepth = parent_cell.celldepth - 1
            parent_quota_believers = set(parent_quota_ledger.keys())
            believers_downhill_events_ints = get_believers_downhill_event_ints(
                believer_events_sets, parent_quota_believers, parent_cell.event_int
            )
            for quota_believer, quota_amount in parent_quota_ledger.items():
                if downhill_event_int := believers_downhill_events_ints.get(
                    quota_believer
                ):
                    if quota_amount > 0:
                        child_ancestors = list(copy_copy(parent_cell.ancestors))
                        child_ancestors.append(quota_believer)
                        child_cellunit = cellunit_shop(
                            ancestors=child_ancestors,
                            event_int=downhill_event_int,
                            celldepth=child_celldepth,
                            bud_believer_name=bud_believer_name,
                            penny=parent_cell.penny,
                            quota=quota_amount,
                        )
                        cells_to_evaluate.append(child_cellunit)


def load_cells_believerevent(belief_mstr_dir: str, belief_label: LabelTerm):
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    for believer_name in get_level1_dirs(believers_dir):
        believer_dir = create_path(believers_dir, believer_name)
        buds_dir = create_path(believer_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            for dirpath, dirnames, filenames in os_walk(bud_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    _load_cell_believerevent(belief_mstr_dir, belief_label, dirpath)


def _load_cell_believerevent(belief_mstr_dir, belief_label, dirpath):
    x_cellunit = cellunit_get_from_dir(dirpath)
    cell_believer_name = x_cellunit.get_cell_believer_name()
    event_int = x_cellunit.event_int
    believerevent = get_believerevent_obj(
        belief_mstr_dir, belief_label, cell_believer_name, event_int
    )
    x_cellunit.eval_believerevent(believerevent)
    cellunit_save_to_dir(dirpath, x_cellunit)


def set_cell_trees_found_facts(belief_mstr_dir: str, belief_label: LabelTerm):
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    for believer_name in get_level1_dirs(believers_dir):
        believer_dir = create_path(believers_dir, believer_name)
        buds_dir = create_path(believer_dir, "buds")
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
        cell_believers_tuple = tuple(bud_path.split(os_sep)[1:])
        nodes_facts_dict[cell_believers_tuple] = x_cell.believerevent_facts
        nodes_quotas_dict[cell_believers_tuple] = (
            x_cell.get_believerevents_quota_ledger()
        )

    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quotas_dict)
    dst_dir_facts = {
        os_path_join(bud_time_dir, *node_addr): get_dict_from_factunits(facts)
        for node_addr, facts in nodes_wgt_facts.items()
    }
    for dst_dir, dst_facts_dict in dst_dir_facts.items():
        dst_cell = cellunit_get_from_dir(dst_dir)
        dst_cell.set_found_facts_from_dict(dst_facts_dict)
        cellunit_save_to_dir(dst_dir, dst_cell)


def set_cell_trees_decrees(belief_mstr_dir: str, belief_label: str):
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    for believer_name in get_level1_dirs(believers_dir):
        believer_dir = create_path(believers_dir, believer_name)
        buds_dir = create_path(believer_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            set_cell_tree_decrees(
                belief_mstr_dir, belief_label, believer_name, bud_time, bud_time_dir
            )


@dataclass
class DecreeUnit:
    parent_cell_dir: str = None
    cell_dir: str = None
    cell_ancestors: list[BelieverName] = None
    cell_believer_name: BelieverName = None
    cell_mandate: dict[BelieverName, FundNum] = None
    cell_celldepth: int = None
    root_cell_bool: bool = None
    event_int: int = None

    def get_child_cell_ancestors(self, child_believer_name: BelieverName):
        child_cell_ancestors = copy_copy(self.cell_ancestors)
        child_cell_ancestors.append(child_believer_name)
        return child_cell_ancestors


def set_cell_tree_decrees(
    mstr_dir: str,
    belief_label: BeliefLabel,
    believer_name: BelieverName,
    bud_time: TimeLinePoint,
    bud_time_dir: str,
):
    # clear all current child directorys
    # create root bud tree node
    # grab boss facts from parent_cell (does not apply to root)
    # grab found facts for that cell
    # grab believerevent for that cell
    # add all found_facts that exist in believerevent to believerevent
    # add all boss facts that exist in believerevent to believerevent
    # calculate believeradjust
    # grab person_agenda_fund_agenda_give ledger
    # add nodes to to_evalute_cellnodes based on person_agenda_fund_give believers
    root_cell = cellunit_get_from_dir(bud_time_dir)
    root_cell_dir = create_cell_dir_path(
        mstr_dir, belief_label, believer_name, bud_time, []
    )
    root_decree = DecreeUnit(
        parent_cell_dir=None,
        cell_dir=root_cell_dir,
        cell_ancestors=[],
        cell_believer_name=believer_name,
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
        ) or generate_cell_from_decree(x_decree, mstr_dir, belief_label, believer_name):
            x_cell.mandate = x_decree.cell_mandate
            parent_cell_dir = x_decree.parent_cell_dir
            _set_cell_boss_facts(x_cell, parent_cell_dir, x_decree.root_cell_bool)
            x_cell.calc_person_mandate_ledger()
            cellunit_save_to_dir(x_decree.cell_dir, x_cell)
            if x_decree.cell_celldepth > 0:
                _add_child_decrees(
                    to_evaluate_decreeunits,
                    x_cell=x_cell,
                    x_decree=x_decree,
                    mstr_dir=mstr_dir,
                    belief_label=belief_label,
                    believer_name=believer_name,
                    bud_time=bud_time,
                )


def _add_child_decrees(
    to_evaluate_decreeunits: list[DecreeUnit],
    x_cell: CellUnit,
    x_decree: DecreeUnit,
    mstr_dir,
    belief_label: str,
    believer_name: str,
    bud_time: int,
):
    for child_believer_name, child_mandate in x_cell._person_mandate_ledger.items():
        child_cell_ancestors = x_decree.get_child_cell_ancestors(child_believer_name)
        child_dir = create_cell_dir_path(
            mstr_dir, belief_label, believer_name, bud_time, child_cell_ancestors
        )
        child_decreeunit = DecreeUnit(
            parent_cell_dir=x_decree.cell_dir,
            cell_dir=child_dir,
            cell_ancestors=child_cell_ancestors,
            cell_believer_name=child_believer_name,
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
    x_decree: DecreeUnit, mstr_dir: str, belief_label: str, believer_name: BelieverName
) -> CellUnit:
    cell_believer_name = x_decree.cell_believer_name
    believers_downhill_events_ints = get_believers_downhill_event_ints(
        believer_events_sets=collect_believer_event_dir_sets(mstr_dir, belief_label),
        downhill_believers={cell_believer_name},
        ref_event_int=x_decree.event_int,
    )
    if downhill_event_int := believers_downhill_events_ints.get(cell_believer_name):
        believerevent_path = create_believerevent_path(
            mstr_dir, belief_label, cell_believer_name, downhill_event_int
        )
        believerevent = open_believer_file(believerevent_path)
        x_cell = cellunit_shop(
            bud_believer_name=believer_name,
            ancestors=x_decree.get_child_cell_ancestors(cell_believer_name),
            event_int=downhill_event_int,
            celldepth=x_decree.cell_celldepth,
            penny=believerevent.penny,
            quota=None,
            mandate=x_decree.cell_mandate,
        )
        x_cell.eval_believerevent(believerevent)
        return x_cell


def set_cell_tree_cell_mandates(belief_mstr_dir: str, belief_label: str):
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    for believer_name in get_level1_dirs(believers_dir):
        believer_dir = create_path(believers_dir, believer_name)
        buds_dir = create_path(believer_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            for dirpath, dirnames, filenames in os_walk(bud_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    create_cell_person_mandate_ledger_json(dirpath)


def create_bud_mandate_ledgers(belief_mstr_dir: str, belief_label: str):
    belief_json_path = create_belief_json_path(belief_mstr_dir, belief_label)
    beliefunit = beliefunit_get_from_dict(open_json(belief_json_path))
    for brokerunit in beliefunit.brokerunits.values():
        for budunit in brokerunit.buds.values():
            bud_root_dir = create_bud_dir_path(
                belief_mstr_dir,
                belief_label,
                believer_name=brokerunit.believer_name,
                bud_time=budunit.bud_time,
            )
            bud_person_mandate_ledger = allot_nested_scale(
                bud_root_dir,
                src_filename=CELL_MANDATE_FILENAME,
                scale_number=budunit.quota,
                grain_unit=beliefunit.penny,
                depth=budunit.celldepth,
                dst_filename=BUD_MANDATE_FILENAME,
            )
            save_json(bud_root_dir, BUD_MANDATE_FILENAME, bud_person_mandate_ledger)
            budunit._bud_person_nets = bud_person_mandate_ledger
    save_json(belief_json_path, None, beliefunit.get_dict())
