from copy import copy as copy_copy
from dataclasses import dataclass
from os import sep as os_sep
from os import walk as os_walk
from os.path import exists as os_path_exists
from os.path import join as os_path_join
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_json,
    save_json,
)
from src.a01_term_logic.way import LabelTerm, OwnerName
from src.a02_finance_logic.allot import allot_nested_scale
from src.a02_finance_logic.deal import FiscLabel
from src.a02_finance_logic.finance_config import FundNum, TimeLinePoint
from src.a04_reason_logic.reason_concept import get_dict_from_factunits
from src.a11_deal_cell_logic.cell import CellUnit, cellunit_shop
from src.a12_hub_tools.fact_tool import get_nodes_with_weighted_facts
from src.a12_hub_tools.hub_path import (
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    DEAL_MANDATE_FILENAME,
    create_budevent_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_deal_dir_path,
    create_fisc_json_path,
)
from src.a12_hub_tools.hub_tool import (
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    collect_owner_event_dir_sets,
    create_cell_acct_mandate_ledger_json,
    get_budevent_obj,
    get_owners_downhill_event_ints,
    open_bud_file,
)
from src.a15_fisc_logic.fisc import get_from_dict as fiscunit_get_from_dict


def create_fisc_owners_cell_trees(fisc_mstr_dir, fisc_label):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_label)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for deal_time in get_level1_dirs(deals_dir):
            create_cell_tree(fisc_mstr_dir, fisc_label, owner_name, deal_time)


def create_cell_tree(fisc_mstr_dir, fisc_label, deal_owner_name, deal_time):
    root_cell_json_path = create_cell_json_path(
        fisc_mstr_dir, fisc_label, deal_owner_name, deal_time
    )
    if os_path_exists(root_cell_json_path):
        _exists_create_cell_tree(fisc_mstr_dir, fisc_label, deal_owner_name, deal_time)


def _exists_create_cell_tree(fisc_mstr_dir, fisc_label, deal_owner_name, deal_time):
    root_cell_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_label, deal_owner_name, deal_time, []
    )
    cells_to_evaluate = [cellunit_get_from_dir(root_cell_dir)]
    owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, fisc_label)
    while cells_to_evaluate != []:
        parent_cell = cells_to_evaluate.pop()
        cell_owner_name = parent_cell.get_cell_owner_name()
        e_int = parent_cell.event_int
        budevent = get_budevent_obj(fisc_mstr_dir, fisc_label, cell_owner_name, e_int)
        parent_cell.eval_budevent(budevent)
        parent_cell_dir = create_cell_dir_path(
            fisc_mstr_dir,
            fisc_label,
            deal_owner_name,
            deal_time,
            parent_cell.ancestors,
        )
        cellunit_save_to_dir(parent_cell_dir, parent_cell)
        parent_quota_ledger = parent_cell.get_budevents_quota_ledger()
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
                            deal_owner_name=deal_owner_name,
                            penny=parent_cell.penny,
                            quota=quota_amount,
                        )
                        cells_to_evaluate.append(child_cellunit)


def load_cells_budevent(fisc_mstr_dir: str, fisc_label: LabelTerm):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_label)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for deal_time in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, deal_time)
            for dirpath, dirnames, filenames in os_walk(deal_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    _load_cell_budevent(fisc_mstr_dir, fisc_label, dirpath)


def _load_cell_budevent(fisc_mstr_dir, fisc_label, dirpath):
    x_cellunit = cellunit_get_from_dir(dirpath)
    cell_owner_name = x_cellunit.get_cell_owner_name()
    event_int = x_cellunit.event_int
    budevent = get_budevent_obj(fisc_mstr_dir, fisc_label, cell_owner_name, event_int)
    x_cellunit.eval_budevent(budevent)
    cellunit_save_to_dir(dirpath, x_cellunit)


def set_cell_trees_found_facts(fisc_mstr_dir: str, fisc_label: LabelTerm):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_label)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for deal_time in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, deal_time)
            cell_dirs = [
                dirpath
                for dirpath, dirnames, filenames in os_walk(deal_time_dir)
                if CELLNODE_FILENAME in set(filenames)
            ]
            _set_cell_found_facts(deal_time_dir, cell_dirs)


def _set_cell_found_facts(deal_time_dir: str, cell_dirs: list[str]):
    nodes_facts_dict = {}
    nodes_quotas_dict = {}
    for dirpath in cell_dirs:
        x_cell = cellunit_get_from_dir(dirpath)
        deal_path = dirpath.replace(deal_time_dir, "")
        cell_owners_tuple = tuple(deal_path.split(os_sep)[1:])
        nodes_facts_dict[cell_owners_tuple] = x_cell.budevent_facts
        nodes_quotas_dict[cell_owners_tuple] = x_cell.get_budevents_quota_ledger()

    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quotas_dict)
    output_dir_facts = {
        os_path_join(deal_time_dir, *node_addr): get_dict_from_factunits(facts)
        for node_addr, facts in nodes_wgt_facts.items()
    }
    for output_dir, output_facts_dict in output_dir_facts.items():
        output_cell = cellunit_get_from_dir(output_dir)
        output_cell.set_found_facts_from_dict(output_facts_dict)
        cellunit_save_to_dir(output_dir, output_cell)


def set_cell_trees_decrees(fisc_mstr_dir: str, fisc_label: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_label)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for deal_time in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, deal_time)
            set_cell_tree_decrees(
                fisc_mstr_dir, fisc_label, owner_name, deal_time, deal_time_dir
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
    fisc_label: FiscLabel,
    owner_name: OwnerName,
    deal_time: TimeLinePoint,
    deal_time_dir: str,
):
    # clear all current child directorys
    # create root deal tree node
    # grab boss facts from parent_cell (does not apply to root)
    # grab found facts for that cell
    # grab budevent for that cell
    # add all found_facts that exist in budevent to budevent
    # add all boss facts that exist in budevent to budevent
    # calculate budadjust
    # grab acct_agenda_fund_agenda_give ledger
    # add nodes to to_evalute_cellnodes based on acct_agenda_fund_give owners
    root_cell = cellunit_get_from_dir(deal_time_dir)
    root_cell_dir = create_cell_dir_path(
        mstr_dir, fisc_label, owner_name, deal_time, []
    )
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
        ) or generate_cell_from_decree(x_decree, mstr_dir, fisc_label, owner_name):
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
                    fisc_label=fisc_label,
                    owner_name=owner_name,
                    deal_time=deal_time,
                )


def _add_child_decrees(
    to_evaluate_decreeunits: list[DecreeUnit],
    x_cell: CellUnit,
    x_decree: DecreeUnit,
    mstr_dir,
    fisc_label: str,
    owner_name: str,
    deal_time: int,
):
    for child_owner_name, child_mandate in x_cell._acct_mandate_ledger.items():
        child_cell_ancestors = x_decree.get_child_cell_ancestors(child_owner_name)
        child_dir = create_cell_dir_path(
            mstr_dir, fisc_label, owner_name, deal_time, child_cell_ancestors
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
    x_decree: DecreeUnit, mstr_dir: str, fisc_label: str, owner_name: OwnerName
) -> CellUnit:
    cell_owner_name = x_decree.cell_owner_name
    owners_downhill_events_ints = get_owners_downhill_event_ints(
        owner_events_sets=collect_owner_event_dir_sets(mstr_dir, fisc_label),
        downhill_owners={cell_owner_name},
        ref_event_int=x_decree.event_int,
    )
    if downhill_event_int := owners_downhill_events_ints.get(cell_owner_name):
        budevent_path = create_budevent_path(
            mstr_dir, fisc_label, cell_owner_name, downhill_event_int
        )
        budevent = open_bud_file(budevent_path)
        x_cell = cellunit_shop(
            deal_owner_name=owner_name,
            ancestors=x_decree.get_child_cell_ancestors(cell_owner_name),
            event_int=downhill_event_int,
            celldepth=x_decree.cell_celldepth,
            penny=budevent.penny,
            quota=None,
            mandate=x_decree.cell_mandate,
        )
        x_cell.eval_budevent(budevent)
        return x_cell


def set_cell_tree_cell_mandates(fisc_mstr_dir: str, fisc_label: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_label)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for deal_time in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, deal_time)
            for dirpath, dirnames, filenames in os_walk(deal_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    create_cell_acct_mandate_ledger_json(dirpath)


def create_deal_mandate_ledgers(fisc_mstr_dir: str, fisc_label: str):
    fisc_json_path = create_fisc_json_path(fisc_mstr_dir, fisc_label)
    fiscunit = fiscunit_get_from_dict(open_json(fisc_json_path))
    for brokerunit in fiscunit.brokerunits.values():
        for dealunit in brokerunit.deals.values():
            deal_root_dir = create_deal_dir_path(
                fisc_mstr_dir,
                fisc_label,
                owner_name=brokerunit.owner_name,
                deal_time=dealunit.deal_time,
            )
            deal_acct_mandate_ledger = allot_nested_scale(
                deal_root_dir,
                src_filename=CELL_MANDATE_FILENAME,
                scale_number=dealunit.quota,
                grain_unit=fiscunit.penny,
                depth=dealunit.celldepth,
                dst_filename=DEAL_MANDATE_FILENAME,
            )
            save_json(deal_root_dir, DEAL_MANDATE_FILENAME, deal_acct_mandate_ledger)
            dealunit._deal_acct_nets = deal_acct_mandate_ledger
    save_json(fisc_json_path, None, fiscunit.get_dict())
