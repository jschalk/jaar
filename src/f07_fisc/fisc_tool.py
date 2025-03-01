from src.f00_instrument.file import create_path, save_json, get_level1_dirs, open_json
from src.f01_road.allot import allot_scale
from src.f01_road.road import TitleUnit
from src.f02_bud.reason_item import factunits_get_from_dict, get_dict_from_factunits
from src.f05_listen.cell import (
    create_child_cellunits,
    cellunit_shop,
    cellunit_get_from_dict,
)
from src.f05_listen.hub_path import (
    CELLNODE_FILENAME,
    CELL_QUOTA_LEDGER_FILENAME,
    create_cell_node_json_path,
    create_budevent_path,
    create_cell_quota_ledger_path,
)
from src.f05_listen.hub_tool import (
    get_budevent_obj,
    collect_owner_event_dir_sets,
    get_owners_downhill_event_ints,
    cellunit_get_from_dir,
    cellunit_save_to_dir,
)
from src.f05_listen.fact_tool import get_nodes_with_weighted_facts
from os import walk as os_walk, sep as os_sep
from os.path import exists as os_path_exists, join as os_path_join
from copy import copy as copy_copy


def create_fisc_owners_deal_trees(fisc_mstr_dir, fisc_title):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            create_deal_tree(fisc_mstr_dir, fisc_title, owner_name, time_int)


def create_deal_tree(fisc_mstr_dir, fisc_title, time_owner_name, time_int):
    root_cell_json_path = create_cell_node_json_path(
        fisc_mstr_dir, fisc_title, time_owner_name, time_int
    )
    if os_path_exists(root_cell_json_path):
        root_cell_dict = open_json(root_cell_json_path)
        root_cellunit = cellunit_get_from_dict(root_cell_dict)
        cells_to_evaluate = [root_cellunit]
        owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, fisc_title)
        while cells_to_evaluate != []:
            parent_cell = cells_to_evaluate.pop()
            budevent = get_budevent_obj(
                fisc_mstr_dir,
                fisc_title,
                parent_cell.get_cell_owner_name(),
                parent_cell.event_int,
            )
            parent_cell.load_budevent(budevent)
            path_ancestors = copy_copy(parent_cell.ancestors)[1:]
            parent_quota_ledger_path = create_cell_quota_ledger_path(
                fisc_mstr_dir, fisc_title, time_owner_name, time_int, path_ancestors
            )
            parent_quota_ledger = parent_cell.get_budevents_quota_ledger()
            save_json(parent_quota_ledger_path, None, parent_quota_ledger)
            if parent_cell.celldepth > 0:
                child_celldepth = parent_cell.celldepth - 1
                parent_quota_owners = set(parent_quota_ledger.keys())
                owners_downhill_events_ints = get_owners_downhill_event_ints(
                    owner_events_sets, parent_quota_owners, parent_cell.event_int
                )
                for quota_owner, quota_amount in parent_quota_ledger.items():
                    if downhill_event_int := owners_downhill_events_ints.get(
                        quota_owner
                    ):
                        if quota_amount > 0:
                            child_ancestors = list(copy_copy(parent_cell.ancestors))
                            child_ancestors.append(quota_owner)
                            child_cellunit = cellunit_shop(
                                ancestors=child_ancestors,
                                event_int=downhill_event_int,
                                celldepth=child_celldepth,
                                deal_owner_name=time_owner_name,
                                penny=parent_cell.penny,
                                quota=quota_amount,
                            )
                            child_cell_json_path = create_cell_node_json_path(
                                fisc_mstr_dir,
                                fisc_title,
                                time_owner_name,
                                time_int,
                                child_ancestors[1:],
                            )
                            save_json(
                                child_cell_json_path, None, child_cellunit.get_dict()
                            )
                            cells_to_evaluate.append(child_cellunit)


def create_all_cell_node_facts_files(fisc_mstr_dir: str, fisc_title: TitleUnit):
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
                    create_and_save_facts_file(
                        fisc_mstr_dir, fisc_title, owner_name, dirpath
                    )


def create_and_save_facts_file(fisc_mstr_dir, fisc_title, owner_name, dirpath):
    x_cellunit = cellunit_get_from_dir(dirpath)
    cell_owner_name = x_cellunit.get_cell_owner_name()
    event_int = x_cellunit.event_int
    budevent = get_budevent_obj(fisc_mstr_dir, fisc_title, cell_owner_name, event_int)
    x_cellunit.load_budevent(budevent)
    cellunit_save_to_dir(dirpath, x_cellunit)


def uphill_cell_node_budevent_facts(fisc_mstr_dir: str, fisc_title: TitleUnit):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
            budevent_facts_dirs = [
                dirpath
                for dirpath, dirnames, filenames in os_walk(deal_time_dir)
                if CELLNODE_FILENAME in set(filenames)
            ]
            quota_ledger_dirs = [
                dirpath
                for dirpath, dirnames, filenames in os_walk(deal_time_dir)
                if CELL_QUOTA_LEDGER_FILENAME in set(filenames)
            ]
            _create_found_facts(deal_time_dir, budevent_facts_dirs, quota_ledger_dirs)


def _create_found_facts(
    deal_time_dir: str, budevent_facts_dirs: list[str], quota_ledger_dirs: list[str]
):
    nodes_facts_dict = {}
    for dirpath in budevent_facts_dirs:
        x_cell = cellunit_get_from_dir(dirpath)
        deal_path = dirpath.replace(deal_time_dir, "")
        cell_owners_tuple = tuple(deal_path.split(os_sep)[1:])
        nodes_facts_dict[cell_owners_tuple] = x_cell.budevent_facts

    nodes_quotas_dict = {}
    for dirpath in quota_ledger_dirs:
        quota_ledger_path = create_path(dirpath, CELL_QUOTA_LEDGER_FILENAME)
        quota_ledger_dict = open_json(quota_ledger_path)
        deal_path = dirpath.replace(deal_time_dir, "")
        cell_owners_tuple = tuple(deal_path.split(os_sep)[1:])
        nodes_quotas_dict[cell_owners_tuple] = quota_ledger_dict

    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quotas_dict)
    output_dir_facts = {
        os_path_join(deal_time_dir, *node_addr): get_dict_from_factunits(facts)
        for node_addr, facts in nodes_wgt_facts.items()
    }
    for output_dir, output_facts_dict in output_dir_facts.items():
        output_cell = cellunit_get_from_dir(output_dir)
        output_cell.set_found_facts_from_dict(output_facts_dict)
        cellunit_save_to_dir(output_dir, output_cell)


def modify_deal_trees_create_boss_facts(fisc_mstr_dir: str, fisc_title: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
            modify_deal_tree_create_boss_facts(
                fisc_mstr_dir, fisc_title, owner_name, deal_time_dir
            )


def modify_deal_tree_create_boss_facts(
    fisc_mstr_dir, fisc_title, owner_name, deal_time_dir
):
    root_cell = cellunit_get_from_dir(deal_time_dir)
    cell_event_int = root_cell.event_int
    budevent = get_budevent_obj(fisc_mstr_dir, fisc_title, owner_name, cell_event_int)
    root_cell.load_budevent(budevent)
    root_cell.set_boss_facts_from_other_facts()
    to_evaluate_cells = [root_cell]
    while to_evaluate_cells != []:
        curr_cell = to_evaluate_cells.pop()
        to_evaluate_cells.extend(create_child_cellunits(curr_cell))

    print(f"{root_cell=}")

    # get_deal_root budevent
    # if exists as budevent.reason_base add found_facts to budevent
    # set boss_facts to budadjust.root facts
    # save boss_facts
    # 0 set found facts to deal tree root
    # evaluate every deal tree node, start with root

    # while not every deal tree node has been evaluated
    # pick a closest to root deal tree node
    # grab boss facts from parent_cell_node
    # grab found facts for that cell_node
    # grab budevent for that cell_node
    # add all found_facts that exist in budevent to budevent
    # add all boss facts that exist in budevent to budevent
    # calculate budadjust
    # grab acct_agenda_fund_agenda_give ledger
    # add nodes to to_evalute_cellnodes based on acct_agenda_fund_give owners
