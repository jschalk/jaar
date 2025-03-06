from src.f00_instrument.file import create_path, get_level1_dirs
from src.f01_road.finance import TimeLinePoint
from src.f01_road.deal import FiscTitle
from src.f01_road.road import TitleUnit, OwnerName
from src.f01_road.finance import FundNum
from src.f02_bud.reason_item import get_dict_from_factunits
from src.f05_listen.cell import CellUnit, cellunit_shop
from src.f05_listen.hub_path import (
    CELLNODE_FILENAME,
    create_cell_dir_path,
    create_cell_json_path,
    create_budevent_path,
)
from src.f05_listen.hub_tool import (
    get_budevent_obj,
    open_bud_file,
    collect_owner_event_dir_sets,
    get_owners_downhill_event_ints,
    cellunit_get_from_dir,
    cellunit_save_to_dir,
    create_acct_mandate_ledger_json,
)
from src.f05_listen.fact_tool import get_nodes_with_weighted_facts
from os import walk as os_walk, sep as os_sep
from os.path import exists as os_path_exists, join as os_path_join
from copy import copy as copy_copy
from dataclasses import dataclass


def create_fisc_owners_deal_trees(fisc_mstr_dir, fisc_title):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            create_deal_tree(fisc_mstr_dir, fisc_title, owner_name, time_int)


def create_deal_tree(fisc_mstr_dir, fisc_title, deal_owner_name, time_int):
    root_cell_json_path = create_cell_json_path(
        fisc_mstr_dir, fisc_title, deal_owner_name, time_int
    )
    if os_path_exists(root_cell_json_path):
        _exists_create_deal_tree(fisc_mstr_dir, fisc_title, deal_owner_name, time_int)


def _exists_create_deal_tree(fisc_mstr_dir, fisc_title, deal_owner_name, time_int):
    root_cell_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_title, deal_owner_name, time_int, []
    )
    cells_to_evaluate = [cellunit_get_from_dir(root_cell_dir)]
    owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, fisc_title)
    while cells_to_evaluate != []:
        parent_cell = cells_to_evaluate.pop()
        cell_owner_name = parent_cell.get_cell_owner_name()
        e_int = parent_cell.event_int
        budevent = get_budevent_obj(fisc_mstr_dir, fisc_title, cell_owner_name, e_int)
        parent_cell.load_budevent(budevent)
        parent_cell_dir = create_cell_dir_path(
            fisc_mstr_dir,
            fisc_title,
            deal_owner_name,
            time_int,
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


def load_cells_budevent(fisc_mstr_dir: str, fisc_title: TitleUnit):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
            for dirpath, dirnames, filenames in os_walk(deal_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    _load_cell_budevent(fisc_mstr_dir, fisc_title, dirpath)


def _load_cell_budevent(fisc_mstr_dir, fisc_title, dirpath):
    x_cellunit = cellunit_get_from_dir(dirpath)
    cell_owner_name = x_cellunit.get_cell_owner_name()
    event_int = x_cellunit.event_int
    budevent = get_budevent_obj(fisc_mstr_dir, fisc_title, cell_owner_name, event_int)
    x_cellunit.load_budevent(budevent)
    cellunit_save_to_dir(dirpath, x_cellunit)


def set_deal_trees_found_facts(fisc_mstr_dir: str, fisc_title: TitleUnit):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
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


def set_deal_trees_decrees(fisc_mstr_dir: str, fisc_title: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
            set_deal_tree_decrees(
                fisc_mstr_dir, fisc_title, owner_name, time_int, deal_time_dir
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


def set_deal_tree_decrees(
    mstr_dir: str,
    fisc_title: FiscTitle,
    owner_name: OwnerName,
    time_int: TimeLinePoint,
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
    root_cell_dir = create_cell_dir_path(mstr_dir, fisc_title, owner_name, time_int, [])
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
        ) or generate_cell_from_decree(x_decree, mstr_dir, fisc_title, owner_name):
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
                    fisc_title=fisc_title,
                    owner_name=owner_name,
                    time_int=time_int,
                )


def _add_child_decrees(
    to_evaluate_decreeunits: list[DecreeUnit],
    x_cell: CellUnit,
    x_decree: DecreeUnit,
    mstr_dir,
    fisc_title: str,
    owner_name: str,
    time_int: int,
):
    for child_owner_name, child_mandate in x_cell._acct_mandate_ledger.items():
        child_cell_ancestors = x_decree.get_child_cell_ancestors(child_owner_name)
        child_dir = create_cell_dir_path(
            mstr_dir, fisc_title, owner_name, time_int, child_cell_ancestors
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
    x_decree: DecreeUnit, mstr_dir: str, fisc_title: str, owner_name: OwnerName
) -> CellUnit:
    cell_owner_name = x_decree.cell_owner_name
    owners_downhill_events_ints = get_owners_downhill_event_ints(
        owner_events_sets=collect_owner_event_dir_sets(mstr_dir, fisc_title),
        downhill_owners={cell_owner_name},
        ref_event_int=x_decree.event_int,
    )
    if downhill_event_int := owners_downhill_events_ints.get(cell_owner_name):
        budevent_path = create_budevent_path(
            mstr_dir, fisc_title, cell_owner_name, downhill_event_int
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
        x_cell.load_budevent(budevent)
        return x_cell


def set_deal_tree_mandates(fisc_mstr_dir: str, fisc_title: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
            for dirpath, dirnames, filenames in os_walk(deal_time_dir):
                if CELLNODE_FILENAME in set(filenames):
                    create_acct_mandate_ledger_json(dirpath)
