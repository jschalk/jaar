from src.a01_way_logic.way import (
    WayUnit,
    get_terminus_tag,
    get_parent_way,
    LabelUnit,
)
from src.a06_bud_logic.bud import BudUnit
from src.a12_hub_tools.hub_tool import open_gut_file
from src.a12_hub_tools.hubunit import HubUnit
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_bud: BudUnit,
    pledge_way: WayUnit,
    x_teamlink: LabelUnit = None,
    reason_premise: WayUnit = None,
):
    if pledge_way is not None and get_terminus_tag(pledge_way) != "":
        x_idea = x_bud.get_idea_obj(pledge_way, if_missing_create=True)
        x_idea.pledge = True
        x_idea.teamunit.set_teamlink(x_teamlink)

        if x_teamlink is not None and x_bud.acct_exists(x_teamlink) is False:
            x_bud.add_acctunit(x_teamlink)

        if reason_premise is not None:
            if x_bud.idea_exists(reason_premise) is False:
                x_bud.get_idea_obj(reason_premise, if_missing_create=True)
            reason_base = get_parent_way(reason_premise)
            x_bud.edit_reason(pledge_way, reason_base, reason_premise)


def add_gut_pledge(
    x_hubunit: HubUnit,
    pledge_way: WayUnit,
    x_teamlink: LabelUnit = None,
    reason_premise: WayUnit = None,
):
    gut_bud = open_gut_file(
        x_hubunit.fisc_mstr_dir,
        x_hubunit.fisc_tag,
        x_hubunit.owner_name,
    )
    old_gut_bud = copy_deepcopy(gut_bud)
    create_pledge(gut_bud, pledge_way, x_teamlink, reason_premise)
    next_packunit = x_hubunit._default_packunit()
    next_packunit._buddelta.add_all_different_budatoms(old_gut_bud, gut_bud)
    next_packunit.save_files()
    x_hubunit.append_packs_to_gut_file()


def create_fact(x_bud: BudUnit, fact_fneed: WayUnit):
    if x_bud.idea_exists(fact_fneed) is False:
        x_bud.get_idea_obj(fact_fneed, if_missing_create=True)
    fact_base = get_parent_way(fact_fneed)
    x_bud.add_fact(fact_base, fact_fneed)


def add_gut_fact(x_hubunit: HubUnit, fact_fneed: WayUnit):
    gut_bud = open_gut_file(
        x_hubunit.fisc_mstr_dir,
        x_hubunit.fisc_tag,
        x_hubunit.owner_name,
    )
    old_gut_bud = copy_deepcopy(gut_bud)
    create_fact(gut_bud, fact_fneed)
    next_packunit = x_hubunit._default_packunit()
    next_packunit._buddelta.add_all_different_budatoms(old_gut_bud, gut_bud)
    next_packunit.save_files()
    x_hubunit.append_packs_to_gut_file()
