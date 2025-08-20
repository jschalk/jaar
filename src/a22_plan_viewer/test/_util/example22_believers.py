from src.a03_group_logic.group import awardunit_shop
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
    best_rope = sue_believer.make_rope(sports_rope, "best sport")
    best_soccer_rope = sue_believer.make_rope(best_rope, "soccer")
    best_swim_rope = sue_believer.make_rope(best_rope, "swim")
    best_run_rope = sue_believer.make_rope(best_rope, "run")
    sue_believer.add_plan(sports_rope, 5)
    sue_believer.add_plan(best_soccer_rope, 5)
    sue_believer.add_plan(best_swim_rope, 5)
    sue_believer.add_plan(best_run_rope, 5)
    sue_believer.add_fact(tidiness_rope, dirty_rope, 4, 8)
    sue_believer.add_fact(best_rope, best_soccer_rope, 1, 7)

    # Add some award links
    casa_manager_awardunit = awardunit_shop("Manager", 0.5, 0.2)
    casa_team_awardunit = awardunit_shop("Team Lead", 0.3, 0.1)
    casa_devloper_awardunit = awardunit_shop("Sue", 1, 0.8)
    casa_jundevloper_awardunit = awardunit_shop("Bob", 0.7, 0.9)
    root_rope = sue_believer.planroot.get_plan_rope()
    sue_believer.edit_plan_attr(root_rope, awardunit=casa_manager_awardunit)
    sue_believer.edit_plan_attr(root_rope, awardunit=casa_team_awardunit)
    sue_believer.edit_plan_attr(casa_rope, awardunit=casa_devloper_awardunit)
    sue_believer.edit_plan_attr(casa_rope, awardunit=casa_jundevloper_awardunit)
    sue_believer.settle_believer()
    return sue_believer


def get_believerunit_irrational_example() -> BelieverUnit:
    # sourcery skip: extract-duplicate-method
    # this believer has no definitive agenda because 2 task plans are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active is True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active is True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_believer.settle_believer these should be true:
    # 1. hatter_believer._irrational is True
    # 2. hatter_believer._tree_traverse_count = hatter_believer.max_tree_traverse

    hatter_believer = believerunit_shop("Mad Hatter")
    hatter_believer.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_rope = hatter_believer.make_l1_rope(egg_str)
    hatter_believer.set_l1_plan(planunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_rope = hatter_believer.make_l1_rope(chicken_str)
    hatter_believer.set_l1_plan(planunit_shop(chicken_str))

    # set egg task is True when chicken first is False
    hatter_believer.edit_plan_attr(
        egg_rope,
        task=True,
        reason_context=chicken_rope,
        reason_plan_active_requisite=True,
    )

    # set chick task is True when egg first is False
    hatter_believer.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_context=egg_rope,
        reason_plan_active_requisite=False,
    )

    return hatter_believer
