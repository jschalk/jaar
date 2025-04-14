from src.a01_word_logic.road import (
    RoadUnit,
    get_terminus_title,
    get_parent_road,
    LabelUnit,
)
from src.f02_bud.bud import BudUnit
from src.f06_listen.hub_tool import open_gut_file
from src.f06_listen.hubunit import HubUnit
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_bud: BudUnit,
    pledge_road: RoadUnit,
    x_teamlink: LabelUnit = None,
    reason_premise: RoadUnit = None,
):
    if pledge_road is not None and get_terminus_title(pledge_road) != "":
        x_item = x_bud.get_item_obj(pledge_road, if_missing_create=True)
        x_item.pledge = True
        x_item.teamunit.set_teamlink(x_teamlink)

        if x_teamlink is not None and x_bud.acct_exists(x_teamlink) is False:
            x_bud.add_acctunit(x_teamlink)

        if reason_premise is not None:
            if x_bud.item_exists(reason_premise) is False:
                x_bud.get_item_obj(reason_premise, if_missing_create=True)
            reason_base = get_parent_road(reason_premise)
            x_bud.edit_reason(pledge_road, reason_base, reason_premise)


def add_gut_pledge(
    x_hubunit: HubUnit,
    pledge_road: RoadUnit,
    x_teamlink: LabelUnit = None,
    reason_premise: RoadUnit = None,
):
    gut_bud = open_gut_file(
        x_hubunit.fisc_mstr_dir,
        x_hubunit.fisc_title,
        x_hubunit.owner_name,
    )
    old_gut_bud = copy_deepcopy(gut_bud)
    create_pledge(gut_bud, pledge_road, x_teamlink, reason_premise)
    next_packunit = x_hubunit._default_packunit()
    next_packunit._buddelta.add_all_different_budatoms(old_gut_bud, gut_bud)
    next_packunit.save_files()
    x_hubunit.append_packs_to_gut_file()


def create_fact(x_bud: BudUnit, fact_pick: RoadUnit):
    if x_bud.item_exists(fact_pick) is False:
        x_bud.get_item_obj(fact_pick, if_missing_create=True)
    fact_base = get_parent_road(fact_pick)
    x_bud.add_fact(fact_base, fact_pick)


def add_gut_fact(x_hubunit: HubUnit, fact_pick: RoadUnit):
    gut_bud = open_gut_file(
        x_hubunit.fisc_mstr_dir,
        x_hubunit.fisc_title,
        x_hubunit.owner_name,
    )
    old_gut_bud = copy_deepcopy(gut_bud)
    create_fact(gut_bud, fact_pick)
    next_packunit = x_hubunit._default_packunit()
    next_packunit._buddelta.add_all_different_budatoms(old_gut_bud, gut_bud)
    next_packunit.save_files()
    x_hubunit.append_packs_to_gut_file()
