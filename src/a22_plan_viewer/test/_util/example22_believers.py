from src.a03_group_logic.group import awardlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import BelieverUnit, believerunit_shop


def get_sue_casa_believerunit() -> BelieverUnit:
    sue_believer = believerunit_shop("Sue", "accord23")
    casa_rope = sue_believer.make_l1_rope("casa")
    clean_rope = sue_believer.make_rope(casa_rope, "clean")
    mop_rope = sue_believer.make_rope(clean_rope, "mop")
    sweep_rope = sue_believer.make_rope(clean_rope, "sweep")
    tidiness_rope = sue_believer.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_believer.make_rope(casa_rope, "dirty")
    tidy_rope = sue_believer.make_rope(casa_rope, "tidy")
    sue_believer.add_plan(casa_rope, 3)
    sue_believer.add_plan(tidiness_rope, 7)
    sue_believer.add_plan(dirty_rope, 1)
    sue_believer.add_plan(tidy_rope, 3)
    sue_believer.add_plan(clean_rope, 3)
    sue_believer.add_plan(mop_rope, 3, task=True)
    sue_believer.add_plan(sweep_rope, 3, task=True)
    sports_rope = sue_believer.make_l1_rope("sports")
    sue_believer.add_plan(sports_rope, 5)

    # Add some award links
    casa_manager_awardlink = awardlink_shop("Manager", 0.5, 0.2)
    casa_team_awardlink = awardlink_shop("Team Lead", 0.3, 0.1)
    casa_devloper_awardlink = awardlink_shop("Sue", 1, 0.8)
    casa_jundevloper_awardlink = awardlink_shop("Bob", 0.7, 0.9)
    root_rope = sue_believer.planroot.get_plan_rope()
    sue_believer.edit_plan_attr(root_rope, awardlink=casa_manager_awardlink)
    sue_believer.edit_plan_attr(root_rope, awardlink=casa_team_awardlink)
    sue_believer.edit_plan_attr(casa_rope, awardlink=casa_devloper_awardlink)
    sue_believer.edit_plan_attr(casa_rope, awardlink=casa_jundevloper_awardlink)
    sue_believer.settle_believer()
    return sue_believer
