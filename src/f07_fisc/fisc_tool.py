from src.f00_instrument.file import create_path, save_json, get_level1_dirs, open_json
from src.f01_road.road import TitleUnit, OwnerName, RoadUnit
from src.f02_bud.reason_item import factunits_get_from_dict, get_dict_from_factunits
from src.f05_listen.hub_path import (
    DEALNODE_FILENAME,
    DEAL_BUDEVENT_FACTS_FILENAME,
    DEAL_FOUND_FACTS_FILENAME,
    DEAL_QUOTA_LEDGER_FILENAME,
    create_deal_node_json_path,
    create_deal_node_budevent_facts_path,
)
from src.f05_listen.hub_tool import get_budevent_facts
from src.f05_listen.fact_tool import get_nodes_with_weighted_facts
from os import walk as os_walk, sep as os_sep
from os.path import exists as os_path_exists, join as os_path_join
from copy import copy as copy_copy


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
