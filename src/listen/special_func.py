from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src._world.beliefunit import BeliefID
from src._world.world import WorldUnit
from src.listen.hubunit import HubUnit
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_world: WorldUnit,
    pledge_road: RoadUnit,
    x_suffbelief: BeliefID = None,
    reason_premise: RoadUnit = None,
):
    if pledge_road is not None and get_terminus_node(pledge_road) != "":
        x_idea = x_world.get_idea_obj(pledge_road, if_missing_create=True)
        x_idea.pledge = True
        x_idea._assignedunit.set_suffbelief(x_suffbelief)

        if x_world.get_beliefunit(x_suffbelief) is None:
            x_world.add_charunit(x_suffbelief)

        if reason_premise != None:
            if x_world.idea_exists(reason_premise) is False:
                x_world.get_idea_obj(reason_premise, if_missing_create=True)
            reason_base = get_parent_road(reason_premise)
            x_world.edit_reason(pledge_road, reason_base, reason_premise)


def add_soul_pledge(
    x_hubunit: HubUnit,
    pledge_road: RoadUnit,
    x_suffbelief: BeliefID = None,
    reason_premise: RoadUnit = None,
):
    soul_world = x_hubunit.get_soul_world()
    old_soul_world = copy_deepcopy(soul_world)
    create_pledge(soul_world, pledge_road, x_suffbelief, reason_premise)
    next_giftunit = x_hubunit._default_giftunit()
    next_giftunit._changeunit.add_all_different_atomunits(old_soul_world, soul_world)
    next_giftunit.save_files()
    x_hubunit.append_gifts_to_soul_file()


def create_fact(x_world: WorldUnit, fact_pick: RoadUnit):
    if x_world.idea_exists(fact_pick) is False:
        x_world.get_idea_obj(fact_pick, if_missing_create=True)
    fact_base = get_parent_road(fact_pick)
    x_world.set_fact(fact_base, fact_pick)


def add_soul_fact(x_hubunit: HubUnit, fact_pick: RoadUnit):
    soul_world = x_hubunit.get_soul_world()
    old_soul_world = copy_deepcopy(soul_world)
    create_fact(soul_world, fact_pick)
    next_giftunit = x_hubunit._default_giftunit()
    next_giftunit._changeunit.add_all_different_atomunits(old_soul_world, soul_world)
    next_giftunit.save_files()
    x_hubunit.append_gifts_to_soul_file()
