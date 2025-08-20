from src.a03_group_logic.group import awardunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import BeliefUnit, beliefunit_shop


def get_sue_beliefunit() -> BeliefUnit:
    sue_belief = beliefunit_shop("Sue", "accord23")
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, "clean")
    mop_rope = sue_belief.make_rope(clean_rope, "mop")
    sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
    tidiness_rope = sue_belief.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_belief.make_rope(casa_rope, "dirty")
    tidy_rope = sue_belief.make_rope(casa_rope, "tidy")
    sue_belief.add_plan(casa_rope, 3)
    sue_belief.add_plan(tidiness_rope, 7)
    sue_belief.add_plan(dirty_rope, 1)
    sue_belief.add_plan(tidy_rope, 3)
    sue_belief.add_plan(clean_rope, 3)
    sue_belief.add_plan(mop_rope, 3, task=True)
    sue_belief.add_plan(sweep_rope, 3, task=True)
    sports_rope = sue_belief.make_l1_rope("sports")
    best_rope = sue_belief.make_rope(sports_rope, "best sport")
    best_soccer_rope = sue_belief.make_rope(best_rope, "The best sport is soccer")
    best_swim_rope = sue_belief.make_rope(best_rope, "The best sport is swimming")
    best_run_rope = sue_belief.make_rope(best_rope, "The best sport is running")
    play_rope = sue_belief.make_rope(sports_rope, "playing")
    play_soccer_rope = sue_belief.make_rope(play_rope, "play soccer")
    play_swim_rope = sue_belief.make_rope(play_rope, "play swim")
    play_run_rope = sue_belief.make_rope(play_rope, "play run")
    sue_belief.add_plan(sports_rope, 5)
    sue_belief.add_plan(best_soccer_rope, 23)
    sue_belief.add_plan(best_swim_rope, 2)
    sue_belief.add_plan(best_run_rope, 23)
    sue_belief.add_plan(play_rope, 2)
    sue_belief.add_plan(play_soccer_rope, 11)
    sue_belief.add_plan(play_swim_rope, 55)
    sue_belief.add_plan(play_run_rope, 22)

    # Add some award links
    casa_manager_awardunit = awardunit_shop("Manager", 0.5, 0.2)
    casa_team_awardunit = awardunit_shop("Team Lead", 0.3, 0.1)
    casa_devloper_awardunit = awardunit_shop("Sue", 1, 0.8)
    casa_jundevloper_awardunit = awardunit_shop("Bob", 0.7, 0.9)
    root_rope = sue_belief.planroot.get_plan_rope()
    sue_belief.edit_plan_attr(root_rope, awardunit=casa_manager_awardunit)
    sue_belief.edit_plan_attr(root_rope, awardunit=casa_team_awardunit)
    sue_belief.edit_plan_attr(casa_rope, awardunit=casa_devloper_awardunit)
    sue_belief.edit_plan_attr(casa_rope, awardunit=casa_jundevloper_awardunit)
    sue_belief.cash_out()
    return sue_belief


def get_sue_belief_with_facts_and_reasons() -> BeliefUnit:
    sue_belief = get_sue_beliefunit()
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, "clean")
    mop_rope = sue_belief.make_rope(clean_rope, "mop")
    sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
    tidiness_rope = sue_belief.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_belief.make_rope(casa_rope, "dirty")
    tidy_rope = sue_belief.make_rope(casa_rope, "tidy")
    sports_rope = sue_belief.make_l1_rope("sports")
    best_rope = sue_belief.make_rope(sports_rope, "best sport")
    best_soccer_rope = sue_belief.make_rope(best_rope, "soccer")
    best_swim_rope = sue_belief.make_rope(best_rope, "swim")
    best_run_rope = sue_belief.make_rope(best_rope, "run")
    sue_belief.add_fact(tidiness_rope, dirty_rope, 4, 8)
    sue_belief.add_fact(best_rope, best_soccer_rope, 1, 7)
    sue_belief.cash_out()
    return sue_belief


def get_beliefunit_irrational_example() -> BeliefUnit:
    # sourcery skip: extract-duplicate-method
    # this belief has no definitive agenda because 2 task plans are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active is True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active is True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_belief.cash_out these should be true:
    # 1. hatter_belief._irrational is True
    # 2. hatter_belief._tree_traverse_count = hatter_belief.max_tree_traverse

    hatter_belief = beliefunit_shop("Mad Hatter")
    hatter_belief.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_rope = hatter_belief.make_l1_rope(egg_str)
    hatter_belief.set_l1_plan(planunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_rope = hatter_belief.make_l1_rope(chicken_str)
    hatter_belief.set_l1_plan(planunit_shop(chicken_str))

    # set egg task is True when chicken first is False
    hatter_belief.edit_plan_attr(
        egg_rope,
        task=True,
        reason_context=chicken_rope,
        reason_plan_active_requisite=True,
    )

    # set chick task is True when egg first is False
    hatter_belief.edit_plan_attr(
        chicken_rope,
        task=True,
        reason_context=egg_rope,
        reason_plan_active_requisite=False,
    )

    return hatter_belief
