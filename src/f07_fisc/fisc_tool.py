from src.f00_instrument.file import (
    create_path,
    save_json,
    get_level1_dirs,
    open_json,
    save_file,
)
from src.f01_road.allot import allot_scale, allot_nested_scale
from src.f01_road.road import TitleUnit, OwnerName, RoadUnit
from src.f02_bud.reason_item import factunits_get_from_dict, get_dict_from_factunits
from src.f02_bud.bud_tool import set_factunits_to_bud, get_acct_agenda_ledger
from src.f05_listen.hub_path import (
    DEALNODE_FILENAME,
    DEAL_ACCT_LEDGER_FILENAME,
    DEAL_BUDEVENT_FACTS_FILENAME,
    DEAL_BUDADJUST_FILENAME,
    DEAL_ADJUST_LEDGER_FILENAME,
    DEAL_FOUND_FACTS_FILENAME,
    DEAL_QUOTA_LEDGER_FILENAME,
    create_deal_node_json_path,
    create_budevent_path,
    create_deal_node_budadjust_path,
    create_deal_node_budevent_facts_path,
    create_deal_node_found_facts_path,
    create_deal_node_credit_ledger_path,
    create_deal_node_quota_ledger_path,
)
from src.f05_listen.hub_tool import (
    open_bud_file,
    get_budevent_facts,
    collect_owner_event_dir_sets,
    get_budevents_credit_ledger,
    get_owners_downhill_event_ints,
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
    root_deal_json_path = create_deal_node_json_path(
        fisc_mstr_dir, fisc_title, time_owner_name, time_int
    )
    if os_path_exists(root_deal_json_path):
        root_deal_dict = open_json(root_deal_json_path)
        deals_to_evaluate = [root_deal_dict]
        owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, fisc_title)
        while deals_to_evaluate != []:
            parent_deal = deals_to_evaluate.pop()
            parent_event_int = parent_deal.get("event_int")
            parent_dealdepth = parent_deal.get("dealdepth")
            parent_owner_name = parent_deal.get("owner_name")
            parent_quota = parent_deal.get("quota")
            parent_penny = parent_deal.get("penny")
            parent_ancestors = parent_deal.get("ancestors")
            parent_credit_ledger = get_budevents_credit_ledger(
                fisc_mstr_dir, fisc_title, parent_owner_name, parent_event_int
            )
            path_ancestors = parent_ancestors[1:]
            parent_credit_ledger_json_path = create_deal_node_credit_ledger_path(
                fisc_mstr_dir, fisc_title, time_owner_name, time_int, path_ancestors
            )
            save_json(parent_credit_ledger_json_path, None, parent_credit_ledger)
            parent_quota_ledger_path = create_deal_node_quota_ledger_path(
                fisc_mstr_dir, fisc_title, time_owner_name, time_int, path_ancestors
            )
            parent_quota_ledger = allot_scale(parent_credit_ledger, parent_quota, 1)
            save_json(parent_quota_ledger_path, None, parent_quota_ledger)
            if parent_dealdepth > 0:
                child_dealdepth = parent_dealdepth - 1
                parent_credit_owners = set(parent_credit_ledger.keys())
                owners_downhill_events_ints = get_owners_downhill_event_ints(
                    owner_events_sets, parent_credit_owners, parent_event_int
                )
                for quota_owner, quota_amount in parent_quota_ledger.items():
                    if downhill_event_int := owners_downhill_events_ints.get(
                        quota_owner
                    ):
                        if quota_amount > 0:
                            child_ancestors = list(copy_copy(parent_ancestors))
                            child_ancestors.append(quota_owner)
                            child_deal_node = {
                                "ancestors": child_ancestors,
                                "event_int": downhill_event_int,
                                "dealdepth": child_dealdepth,
                                "owner_name": quota_owner,
                                "penny": parent_penny,
                                "quota": quota_amount,
                            }
                            child_deal_json_path = create_deal_node_json_path(
                                fisc_mstr_dir,
                                fisc_title,
                                time_owner_name,
                                time_int,
                                child_ancestors[1:],
                            )
                            save_json(child_deal_json_path, None, child_deal_node)
                            deals_to_evaluate.append(child_deal_node)


def create_all_deal_node_facts_files(fisc_mstr_dir: str, fisc_title: TitleUnit):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
            for dirpath, dirnames, filenames in os_walk(deal_time_dir):
                if DEALNODE_FILENAME in set(filenames):
                    create_and_save_facts_file(
                        fisc_mstr_dir, fisc_title, owner_name, dirpath
                    )


def create_and_save_facts_file(fisc_mstr_dir, fisc_title, owner_name, dirpath):
    deal_node_json_path = create_path(dirpath, DEALNODE_FILENAME)
    deal_node_dict = open_json(deal_node_json_path)
    deal_event_int = deal_node_dict.get("event_int")
    budevent_fact_dict = get_budevent_facts(
        fisc_mstr_dir, fisc_title, owner_name, deal_event_int
    )
    deal_node_facts_path = create_path(dirpath, DEAL_BUDEVENT_FACTS_FILENAME)
    save_json(deal_node_facts_path, None, budevent_fact_dict)


def uphill_deal_node_budevent_facts(fisc_mstr_dir: str, fisc_title: TitleUnit):
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
                if DEAL_BUDEVENT_FACTS_FILENAME in set(filenames)
            ]
            quota_ledger_dirs = [
                dirpath
                for dirpath, dirnames, filenames in os_walk(deal_time_dir)
                if DEAL_QUOTA_LEDGER_FILENAME in set(filenames)
            ]
            _create_found_facts(deal_time_dir, budevent_facts_dirs, quota_ledger_dirs)


def _create_found_facts(
    deal_time_dir: str, budevent_facts_dirs: list[str], quota_ledger_dirs: list[str]
):
    nodes_facts_dict = {}
    for dirpath in budevent_facts_dirs:
        budevent_facts_path = create_path(dirpath, DEAL_BUDEVENT_FACTS_FILENAME)
        budevent_facts_dict = factunits_get_from_dict(open_json(budevent_facts_path))
        deal_path = dirpath.replace(deal_time_dir, "")
        deal_owners_tuple = tuple(deal_path.split(os_sep)[1:])
        nodes_facts_dict[deal_owners_tuple] = budevent_facts_dict

    nodes_quotas_dict = {}
    for dirpath in quota_ledger_dirs:
        quota_ledger_path = create_path(dirpath, DEAL_QUOTA_LEDGER_FILENAME)
        quota_ledger_dict = open_json(quota_ledger_path)
        deal_path = dirpath.replace(deal_time_dir, "")
        deal_owners_tuple = tuple(deal_path.split(os_sep)[1:])
        nodes_quotas_dict[deal_owners_tuple] = quota_ledger_dict

    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quotas_dict)
    output_dir_facts = {
        os_path_join(deal_time_dir, *node_addr): get_dict_from_factunits(facts)
        for node_addr, facts in nodes_wgt_facts.items()
    }
    for output_dir, output_facts_dict in output_dir_facts.items():
        save_json(output_dir, DEAL_FOUND_FACTS_FILENAME, output_facts_dict)


def create_deal_node_acct_adjust_ledgers(fisc_mstr_dir: str, fisc_title: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
            for dirpath, dirnames, filenames in os_walk(deal_time_dir):
                if DEALNODE_FILENAME in set(filenames):
                    _create_and_save_acct_adjust_ledger(
                        fisc_mstr_dir, fisc_title, owner_name, dirpath
                    )


def _create_and_save_acct_adjust_ledger(fisc_mstr_dir, fisc_title, owner_name, dirpath):
    deal_node_json_path = create_path(dirpath, DEALNODE_FILENAME)
    deal_node_dict = open_json(deal_node_json_path)
    ancestors = deal_node_dict.get("ancestors")
    deal_node_quota = deal_node_dict.get("quota")
    deal_node_owner_name = ancestors[-1] if ancestors else owner_name
    deal_node_event_int = deal_node_dict.get("event_int")
    budevent_json_path = create_budevent_path(
        fisc_mstr_dir, fisc_title, deal_node_owner_name, deal_node_event_int
    )
    budadjust_unit = open_bud_file(budevent_json_path)
    budadjust_unit.set_fund_pool(deal_node_quota)
    found_facts_path = create_path(dirpath, DEAL_FOUND_FACTS_FILENAME)
    found_facts_dict = open_json(found_facts_path)
    set_factunits_to_bud(budadjust_unit, found_facts_dict)
    adjust_acct_agenda_ledger = get_acct_agenda_ledger(budadjust_unit, settle_bud=True)
    budadjust_path = create_path(dirpath, DEAL_BUDADJUST_FILENAME)
    adjust_ledger_path = create_path(dirpath, DEAL_ADJUST_LEDGER_FILENAME)
    save_file(budadjust_path, None, budadjust_unit.get_json())
    save_json(adjust_ledger_path, None, adjust_acct_agenda_ledger)


def create_deals_net_ledgers(fisc_mstr_dir: str, fisc_title: str):
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    for owner_name in get_level1_dirs(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        deals_dir = create_path(owner_dir, "deals")
        for time_int in get_level1_dirs(deals_dir):
            deal_time_dir = create_path(deals_dir, time_int)
            deal_node_json_path = create_path(deal_time_dir, DEALNODE_FILENAME)
            deal_root_node_dict = open_json(deal_node_json_path)
            deal_root_node_quota = deal_root_node_dict.get("quota")
            allot_nested_scale(
                x_dir=deal_time_dir,
                src_filename=DEAL_ADJUST_LEDGER_FILENAME,
                scale_number=deal_root_node_quota,
                grain_unit=1,
                depth=5,
                dst_filename=DEAL_ACCT_LEDGER_FILENAME,
            )
            print(f"{deal_root_node_quota=}")
