from src.f00_instrument.file import create_path, save_json, get_level1_dirs, open_json
from src.f01_road.road import TitleUnit
from src.f05_listen.hub_path import (
    create_deal_node_json_path,
    create_deal_node_facts_path,
)
from src.f05_listen.hub_tool import get_budevent_facts
from os import walk as os_walk
from os.path import exists as os_path_exists


def create_all_deal_node_facts_files(fisc_mstr_dir: str, fisc_title: str):
    deal_node_filename = "deal_node.json"
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    for fisc_title in get_level1_dirs(fiscs_dir):
        fisc_dir = create_path(fiscs_dir, fisc_title)
        owners_dir = create_path(fisc_dir, "owners")
        for owner_name in get_level1_dirs(owners_dir):
            owner_dir = create_path(owners_dir, owner_name)
            deals_dir = create_path(owner_dir, "deals")
            for time_int in get_level1_dirs(deals_dir):
                deal_time_dir = create_path(deals_dir, time_int)
                for dirpath, dirnames, filenames in os_walk(deal_time_dir):
                    if deal_node_filename in set(filenames):
                        deal_node_json_path = create_path(dirpath, deal_node_filename)
                        deal_node_dict = open_json(deal_node_json_path)
                        deal_event_int = deal_node_dict.get("event_int")
                        budevent_fact_dict = get_budevent_facts(
                            fisc_mstr_dir, fisc_title, owner_name, deal_event_int
                        )
                        deal_node_facts_path = create_path(dirpath, "facts.json")
                        save_json(deal_node_facts_path, None, budevent_fact_dict)


# def inherit_all_deal_node_face_files(fisc_mstr_dir: str, fiscal_title: TitleUnit):
#     pass
