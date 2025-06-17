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
from src.a01_term_logic.term import LabelTerm, OwnerName
from src.a02_finance_logic.allot import allot_nested_scale
from src.a02_finance_logic.bud import VowLabel
from src.a02_finance_logic.finance_config import FundNum, TimeLinePoint
from src.a04_reason_logic.reason_concept import get_dict_from_factunits
from src.a11_bud_cell_logic.cell import CellUnit, cellunit_shop
from src.a12_hub_toolbox.fact_tool import get_nodes_with_weighted_facts
from src.a12_hub_toolbox.hub_path import (
    BUD_MANDATE_FILENAME,
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    create_bud_dir_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_planevent_path,
    create_vow_json_path,
)
from src.a12_hub_toolbox.hub_tool import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_owner_event_dir_sets,
    create_cell_acct_mandate_ledger_json,
    get_owners_downhill_event_ints,
    get_planevent_obj,
    open_plan_file,
)
from src.a15_vow_logic.vow import get_from_dict as vowunit_get_from_dict


def create_vow_owners_cell_trees(vow_mstr_dir, vow_label):
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        buds_dir = create_path(owner_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            create_cell_tree(vow_mstr_dir, vow_label, owner_name, bud_time)


def create_cell_tree(vow_mstr_dir, vow_label, bud_owner_name, bud_time):
    root_cell_json_path = create_cell_json_path(
        vow_mstr_dir, vow_label, bud_owner_name, bud_time
    )
    if os_path_exists(root_cell_json_path):
        _exists_create_cell_tree(vow_mstr_dir, vow_label, bud_owner_name, bud_time)


def _exists_create_cell_tree(vow_mstr_dir, vow_label, bud_owner_name, bud_time):
    root_cell_dir = create_cell_dir_path(
        vow_mstr_dir, vow_label, bud_owner_name, bud_time, []
    )
    cells_to_evaluate = [cellunit_get_from_dir(root_cell_dir)]
    owner_events_sets = collect_owner_event_dir_sets(vow_mstr_dir, vow_label)
    while cells_to_evaluate != []:
        parent_cell = cells_to_evaluate.pop()
        cell_owner_name = parent_cell.get_cell_owner_name()
        e_int = parent_cell.event_int
        planevent = get_planevent_obj(vow_mstr_dir, vow_label, cell_owner_name, e_int)
        parent_cell.eval_planevent(planevent)
        parent_cell_dir = create_cell_dir_path(
            vow_mstr_dir,
            vow_label,
            bud_owner_name,
            bud_time,
            parent_cell.ancestors,
        )
        cellunit_save_to_dir(parent_cell_dir, parent_cell)
        parent_quota_ledger = parent_cell.get_planevents_quota_ledger()
        if parent_cell.celldepth > 0:
            child_celldepth = parent_cell.celldepth - 1
            parent_quota_owners = set(parent_quota_ledger.keys())
            owners_downhill_events_ints = get_owners_downhill_event_ints(
                owner_events_sets, parent_quota_owners, parent_cell.event_int
            )
            for quota_owner, quota_amount in parent_quota_ledger.items():
                if downhill_event_int := owners_downhill_events_ints.get(quota_owner):
                    if quota_amount > 0:
                        child_ancestors = list(copy_copy(parent_cell.ancestors))
                        child_ancestors.append(quota_owner)
                        child_cellunit = cellunit_shop(
                            ancestors=child_ancestors,
                            event_int=downhill_event_int,
                            celldepth=child_celldepth,
                            bud_owner_name=bud_owner_name,
                            penny=parent_cell.penny,
                            quota=quota_amount,
                        )
                        cells_to_evaluate.append(child_cellunit)


def load_cells_planevent(vow_mstr_dir: str, vow_label: LabelTerm):
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        buds_dir = create_path(owner_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            for dirpath, dirnames, filenames in os_walk(bud_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    _load_cell_planevent(vow_mstr_dir, vow_label, dirpath)


def _load_cell_planevent(vow_mstr_dir, vow_label, dirpath):
    x_cellunit = cellunit_get_from_dir(dirpath)
    cell_owner_name = x_cellunit.get_cell_owner_name()
    event_int = x_cellunit.event_int
    planevent = get_planevent_obj(vow_mstr_dir, vow_label, cell_owner_name, event_int)
    x_cellunit.eval_planevent(planevent)
    cellunit_save_to_dir(dirpath, x_cellunit)


def set_cell_trees_found_facts(vow_mstr_dir: str, vow_label: LabelTerm):
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        buds_dir = create_path(owner_dir, "buds")
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
        cell_owners_tuple = tuple(bud_path.split(os_sep)[1:])
        nodes_facts_dict[cell_owners_tuple] = x_cell.planevent_facts
        nodes_quotas_dict[cell_owners_tuple] = x_cell.get_planevents_quota_ledger()

    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quotas_dict)
    dst_dir_facts = {
        os_path_join(bud_time_dir, *node_addr): get_dict_from_factunits(facts)
        for node_addr, facts in nodes_wgt_facts.items()
    }
    for dst_dir, dst_facts_dict in dst_dir_facts.items():
        dst_cell = cellunit_get_from_dir(dst_dir)
        dst_cell.set_found_facts_from_dict(dst_facts_dict)
        cellunit_save_to_dir(dst_dir, dst_cell)


def set_cell_trees_decrees(vow_mstr_dir: str, vow_label: str):
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        buds_dir = create_path(owner_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            set_cell_tree_decrees(
                vow_mstr_dir, vow_label, owner_name, bud_time, bud_time_dir
            )


@dataclass
class DecreeUnit:
    parent_cell_dir: str = None
    cell_dir: str = None
    cell_ancestors: list[OwnerName] = None
    cell_owner_name: OwnerName = None
    cell_mandate: dict[OwnerName, FundNum] = None
    cell_celldepth: int = None
    root_cell_bool: bool = None
    event_int: int = None

    def get_child_cell_ancestors(self, child_owner_name: OwnerName):
        child_cell_ancestors = copy_copy(self.cell_ancestors)
        child_cell_ancestors.append(child_owner_name)
        return child_cell_ancestors


def set_cell_tree_decrees(
    mstr_dir: str,
    vow_label: VowLabel,
    owner_name: OwnerName,
    bud_time: TimeLinePoint,
    bud_time_dir: str,
):
    # clear all current child directorys
    # create root bud tree node
    # grab boss facts from parent_cell (does not apply to root)
    # grab found facts for that cell
    # grab planevent for that cell
    # add all found_facts that exist in planevent to planevent
    # add all boss facts that exist in planevent to planevent
    # calculate planadjust
    # grab acct_agenda_fund_agenda_give ledger
    # add nodes to to_evalute_cellnodes based on acct_agenda_fund_give owners
    root_cell = cellunit_get_from_dir(bud_time_dir)
    root_cell_dir = create_cell_dir_path(mstr_dir, vow_label, owner_name, bud_time, [])
    root_decree = DecreeUnit(
        parent_cell_dir=None,
        cell_dir=root_cell_dir,
        cell_ancestors=[],
        cell_owner_name=owner_name,
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
        ) or generate_cell_from_decree(x_decree, mstr_dir, vow_label, owner_name):
            x_cell.mandate = x_decree.cell_mandate
            parent_cell_dir = x_decree.parent_cell_dir
            _set_cell_boss_facts(x_cell, parent_cell_dir, x_decree.root_cell_bool)
            x_cell.calc_acct_mandate_ledger()
            cellunit_save_to_dir(x_decree.cell_dir, x_cell)
            if x_decree.cell_celldepth > 0:
                _add_child_decrees(
                    to_evaluate_decreeunits,
                    x_cell=x_cell,
                    x_decree=x_decree,
                    mstr_dir=mstr_dir,
                    vow_label=vow_label,
                    owner_name=owner_name,
                    bud_time=bud_time,
                )


def _add_child_decrees(
    to_evaluate_decreeunits: list[DecreeUnit],
    x_cell: CellUnit,
    x_decree: DecreeUnit,
    mstr_dir,
    vow_label: str,
    owner_name: str,
    bud_time: int,
):
    for child_owner_name, child_mandate in x_cell._acct_mandate_ledger.items():
        child_cell_ancestors = x_decree.get_child_cell_ancestors(child_owner_name)
        child_dir = create_cell_dir_path(
            mstr_dir, vow_label, owner_name, bud_time, child_cell_ancestors
        )
        child_decreeunit = DecreeUnit(
            parent_cell_dir=x_decree.cell_dir,
            cell_dir=child_dir,
            cell_ancestors=child_cell_ancestors,
            cell_owner_name=child_owner_name,
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
    x_decree: DecreeUnit, mstr_dir: str, vow_label: str, owner_name: OwnerName
) -> CellUnit:
    cell_owner_name = x_decree.cell_owner_name
    owners_downhill_events_ints = get_owners_downhill_event_ints(
        owner_events_sets=collect_owner_event_dir_sets(mstr_dir, vow_label),
        downhill_owners={cell_owner_name},
        ref_event_int=x_decree.event_int,
    )
    if downhill_event_int := owners_downhill_events_ints.get(cell_owner_name):
        planevent_path = create_planevent_path(
            mstr_dir, vow_label, cell_owner_name, downhill_event_int
        )
        planevent = open_plan_file(planevent_path)
        x_cell = cellunit_shop(
            bud_owner_name=owner_name,
            ancestors=x_decree.get_child_cell_ancestors(cell_owner_name),
            event_int=downhill_event_int,
            celldepth=x_decree.cell_celldepth,
            penny=planevent.penny,
            quota=None,
            mandate=x_decree.cell_mandate,
        )
        x_cell.eval_planevent(planevent)
        return x_cell


def set_cell_tree_cell_mandates(vow_mstr_dir: str, vow_label: str):
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        buds_dir = create_path(owner_dir, "buds")
        for bud_time in get_level1_dirs(buds_dir):
            bud_time_dir = create_path(buds_dir, bud_time)
            for dirpath, dirnames, filenames in os_walk(bud_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    create_cell_acct_mandate_ledger_json(dirpath)


def create_bud_mandate_ledgers(vow_mstr_dir: str, vow_label: str):
    vow_json_path = create_vow_json_path(vow_mstr_dir, vow_label)
    vowunit = vowunit_get_from_dict(open_json(vow_json_path))
    for brokerunit in vowunit.brokerunits.values():
        for budunit in brokerunit.buds.values():
            bud_root_dir = create_bud_dir_path(
                vow_mstr_dir,
                vow_label,
                owner_name=brokerunit.owner_name,
                bud_time=budunit.bud_time,
            )
            bud_acct_mandate_ledger = allot_nested_scale(
                bud_root_dir,
                src_filename=CELL_MANDATE_FILENAME,
                scale_number=budunit.quota,
                grain_unit=vowunit.penny,
                depth=budunit.celldepth,
                dst_filename=BUD_MANDATE_FILENAME,
            )
            save_json(bud_root_dir, BUD_MANDATE_FILENAME, bud_acct_mandate_ledger)
            budunit._bud_acct_nets = bud_acct_mandate_ledger
    save_json(vow_json_path, None, vowunit.get_dict())
