from src.f01_road.road import RoadUnit, get_terminus_title, get_parent_road, LabelUnit
from src.f02_bud.bud import BudUnit
from src.f05_listen.hubunit import HubUnit
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


def add_voice_pledge(
    x_hubunit: HubUnit,
    pledge_road: RoadUnit,
    x_teamlink: LabelUnit = None,
    reason_premise: RoadUnit = None,
):
    voice_bud = x_hubunit.get_voice_bud()
    old_voice_bud = copy_deepcopy(voice_bud)
    create_pledge(voice_bud, pledge_road, x_teamlink, reason_premise)
    next_standunit = x_hubunit._default_standunit()
    next_standunit._buddelta.add_all_different_budatoms(old_voice_bud, voice_bud)
    next_standunit.save_files()
    x_hubunit.append_stands_to_voice_file()


def create_fact(x_bud: BudUnit, fact_pick: RoadUnit):
    if x_bud.item_exists(fact_pick) is False:
        x_bud.get_item_obj(fact_pick, if_missing_create=True)
    fact_base = get_parent_road(fact_pick)
    x_bud.add_fact(fact_base, fact_pick)


def add_voice_fact(x_hubunit: HubUnit, fact_pick: RoadUnit):
    voice_bud = x_hubunit.get_voice_bud()
    old_voice_bud = copy_deepcopy(voice_bud)
    create_fact(voice_bud, fact_pick)
    next_standunit = x_hubunit._default_standunit()
    next_standunit._buddelta.add_all_different_budatoms(old_voice_bud, voice_bud)
    next_standunit.save_files()
    x_hubunit.append_stands_to_voice_file()
