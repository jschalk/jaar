from src._road.road import RoadUnit, get_terminus_node, get_parent_road, LobbyID
from src.bud.bud import BudUnit
from src.listen.hubunit import HubUnit
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_bud: BudUnit,
    pledge_road: RoadUnit,
    x_lobbyhold: LobbyID = None,
    reason_premise: RoadUnit = None,
):
    if pledge_road is not None and get_terminus_node(pledge_road) != "":
        x_idea = x_bud.get_idea_obj(pledge_road, if_missing_create=True)
        x_idea.pledge = True
        x_idea._doerunit.set_lobbyhold(x_lobbyhold)

        if x_lobbyhold != None and x_bud.char_exists(x_lobbyhold) is False:
            x_bud.add_charunit(x_lobbyhold)

        if reason_premise != None:
            if x_bud.idea_exists(reason_premise) is False:
                x_bud.get_idea_obj(reason_premise, if_missing_create=True)
            reason_base = get_parent_road(reason_premise)
            x_bud.edit_reason(pledge_road, reason_base, reason_premise)


def add_voice_pledge(
    x_hubunit: HubUnit,
    pledge_road: RoadUnit,
    x_lobbyhold: LobbyID = None,
    reason_premise: RoadUnit = None,
):
    voice_bud = x_hubunit.get_voice_bud()
    old_voice_bud = copy_deepcopy(voice_bud)
    create_pledge(voice_bud, pledge_road, x_lobbyhold, reason_premise)
    next_giftunit = x_hubunit._default_giftunit()
    next_giftunit._changeunit.add_all_different_atomunits(old_voice_bud, voice_bud)
    next_giftunit.save_files()
    x_hubunit.append_gifts_to_voice_file()


def create_fact(x_bud: BudUnit, fact_pick: RoadUnit):
    if x_bud.idea_exists(fact_pick) is False:
        x_bud.get_idea_obj(fact_pick, if_missing_create=True)
    fact_base = get_parent_road(fact_pick)
    x_bud.set_fact(fact_base, fact_pick)


def add_voice_fact(x_hubunit: HubUnit, fact_pick: RoadUnit):
    voice_bud = x_hubunit.get_voice_bud()
    old_voice_bud = copy_deepcopy(voice_bud)
    create_fact(voice_bud, fact_pick)
    next_giftunit = x_hubunit._default_giftunit()
    next_giftunit._changeunit.add_all_different_atomunits(old_voice_bud, voice_bud)
    next_giftunit.save_files()
    x_hubunit.append_gifts_to_voice_file()
