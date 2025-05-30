from src.a01_term_logic.way import (
    WayTerm,
    get_tail_label,
    get_parent_way,
    TitleTerm,
)
from src.a06_bud_logic.bud import BudUnit
from src.a12_hub_tools.hub_tool import open_gut_file
from src.a12_hub_tools.hubunit import HubUnit
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_bud: BudUnit,
    pledge_way: WayTerm,
    x_laborlink: TitleTerm = None,
    reason_premise: WayTerm = None,
):
    if pledge_way is not None and pledge_way != "" and get_tail_label(pledge_way) != "":
        x_concept = x_bud.get_concept_obj(pledge_way, if_missing_create=True)
        x_concept.pledge = True
        x_concept.laborunit.set_laborlink(x_laborlink)

        if x_laborlink is not None and x_bud.acct_exists(x_laborlink) is False:
            x_bud.add_acctunit(x_laborlink)

        if reason_premise is not None:
            if x_bud.concept_exists(reason_premise) is False:
                x_bud.get_concept_obj(reason_premise, if_missing_create=True)
            reason_rcontext = get_parent_way(reason_premise)
            x_bud.edit_reason(pledge_way, reason_rcontext, reason_premise)


def add_gut_pledge(
    x_hubunit: HubUnit,
    pledge_way: WayTerm,
    x_laborlink: TitleTerm = None,
    reason_premise: WayTerm = None,
):
    gut_bud = open_gut_file(
        x_hubunit.fisc_mstr_dir,
        x_hubunit.fisc_label,
        x_hubunit.owner_name,
    )
    old_gut_bud = copy_deepcopy(gut_bud)
    create_pledge(gut_bud, pledge_way, x_laborlink, reason_premise)
    next_packunit = x_hubunit._default_packunit()
    next_packunit._buddelta.add_all_different_budatoms(old_gut_bud, gut_bud)
    next_packunit.save_files()
    x_hubunit.append_packs_to_gut_file()


def create_fact(x_bud: BudUnit, fact_fstate: WayTerm):
    if x_bud.concept_exists(fact_fstate) is False:
        x_bud.get_concept_obj(fact_fstate, if_missing_create=True)
    fact_rcontext = get_parent_way(fact_fstate)
    x_bud.add_fact(fact_rcontext, fact_fstate)


def add_gut_fact(x_hubunit: HubUnit, fact_fstate: WayTerm):
    gut_bud = open_gut_file(
        x_hubunit.fisc_mstr_dir,
        x_hubunit.fisc_label,
        x_hubunit.owner_name,
    )
    old_gut_bud = copy_deepcopy(gut_bud)
    create_fact(gut_bud, fact_fstate)
    next_packunit = x_hubunit._default_packunit()
    next_packunit._buddelta.add_all_different_budatoms(old_gut_bud, gut_bud)
    next_packunit.save_files()
    x_hubunit.append_packs_to_gut_file()
