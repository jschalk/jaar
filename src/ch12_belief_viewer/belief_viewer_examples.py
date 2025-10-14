from src.ch04_voice.group import awardunit_shop
from src.ch04_voice.labor import laborunit_shop
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch07_belief_logic.belief_tool import belief_plan_reason_caseunit_set_obj
from src.ch07_belief_logic.test._util.ch07_examples import (
    get_beliefunit_irrational_example,
)


def best_sport_str() -> str:
    return "best sport"


def best_soccer_str() -> str:
    return "The best sport is soccer"


def best_swim_str() -> str:
    return "The best sport is swimming"


def best_run_str() -> str:
    return "The best sport is running"


def play_str() -> str:
    return "playing"


def play_soccer_str() -> str:
    return "play soccer"


def play_swim_str() -> str:
    return "play swimming"


def play_run_str() -> str:
    return "play running"


def get_sue_beliefunit() -> BeliefUnit:
    sue_belief = beliefunit_shop("Sue", "accord23")
    sue_str = "Sue"
    bob_str = "Bob"
    sue_cred_lumen = 11
    sue_debt_lumen = 13
    bob_cred_lumen = 23
    bob_debt_lumen = 29
    sue_belief.add_voiceunit(sue_str, sue_cred_lumen, sue_debt_lumen)
    sue_belief.add_voiceunit(bob_str, bob_cred_lumen, bob_debt_lumen)
    sue_voice = sue_belief.get_voice(sue_str)
    swim_str = ";swimmers"
    team_str = ";Team Manager"
    sue_voice.add_membership(swim_str, 77, 51)
    bob_voice = sue_belief.get_voice(bob_str)
    bob_voice.add_membership(swim_str, 12, 37)
    bob_voice.add_membership(team_str, 51, 91)

    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, "clean")
    mop_rope = sue_belief.make_rope(clean_rope, "mop")
    mop_fancy_rope = sue_belief.make_rope(mop_rope, "use fancy mop")
    sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
    tidi_rope = sue_belief.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_belief.make_rope(tidi_rope, "dirty")
    tidy_rope = sue_belief.make_rope(tidi_rope, "tidy")
    sue_belief.add_plan(casa_rope, 3)
    sue_belief.add_plan(tidi_rope, 7)
    sue_belief.add_plan(dirty_rope, 1)
    sue_belief.add_plan(tidy_rope, 3)
    sue_belief.add_plan(clean_rope, 3)
    sue_belief.add_plan(mop_rope, 3, pledge=True)
    sue_belief.add_plan(mop_fancy_rope, 3, pledge=True)
    sue_belief.add_plan(sweep_rope, 3, pledge=True)
    sports_rope = sue_belief.make_l1_rope("sports")
    best_rope = sue_belief.make_rope(sports_rope, best_sport_str())
    best_soccer_rope = sue_belief.make_rope(best_rope, best_soccer_str())
    best_swim_rope = sue_belief.make_rope(best_rope, best_swim_str())
    best_run_rope = sue_belief.make_rope(best_rope, best_run_str())
    play_rope = sue_belief.make_rope(sports_rope, play_str())
    play_soccer_rope = sue_belief.make_rope(play_rope, play_soccer_str())
    play_swim_rope = sue_belief.make_rope(play_rope, play_swim_str())
    play_run_rope = sue_belief.make_rope(play_rope, play_run_str())
    sue_belief.add_plan(sports_rope, 5)
    sue_belief.add_plan(best_soccer_rope, 23)
    sue_belief.add_plan(best_swim_rope, 2)
    sue_belief.add_plan(best_run_rope, 23)
    sue_belief.add_plan(play_rope, 2)
    sue_belief.add_plan(play_soccer_rope, 11, pledge=True)
    sue_belief.add_plan(play_swim_rope, 55, pledge=True)
    sue_belief.add_plan(play_run_rope, 22, pledge=True)

    # Add some award links
    casa_manager_awardunit = awardunit_shop("Manager", 0.5, 0.2)
    casa_team_awardunit = awardunit_shop(team_str, 0.3, 0.1)
    casa_devloper_awardunit = awardunit_shop("Sue", 1, 0.8)
    casa_jundevloper_awardunit = awardunit_shop("Bob", 0.7, 0.9)
    root_rope = sue_belief.planroot.get_plan_rope()
    sue_belief.edit_plan_attr(root_rope, awardunit=casa_manager_awardunit)
    sue_belief.edit_plan_attr(root_rope, awardunit=casa_team_awardunit)
    sue_belief.edit_plan_attr(casa_rope, awardunit=casa_devloper_awardunit)
    sue_belief.edit_plan_attr(casa_rope, awardunit=casa_jundevloper_awardunit)
    sue_belief.cashout()
    return sue_belief


def get_sue_belief_with_facts_and_reasons() -> BeliefUnit:
    sue_belief = get_sue_beliefunit()
    sue_str = "Sue"
    bob_str = "Bob"
    casa_rope = sue_belief.make_l1_rope("casa")
    clean_rope = sue_belief.make_rope(casa_rope, "clean")
    mop_rope = sue_belief.make_rope(clean_rope, "mop")
    sweep_rope = sue_belief.make_rope(clean_rope, "sweep")
    tidi_rope = sue_belief.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_belief.make_rope(tidi_rope, "dirty")
    tidy_rope = sue_belief.make_rope(tidi_rope, "tidy")
    sports_rope = sue_belief.make_l1_rope("sports")
    best_rope = sue_belief.make_rope(sports_rope, best_sport_str())
    best_soccer_rope = sue_belief.make_rope(best_rope, best_soccer_str())
    best_swim_rope = sue_belief.make_rope(best_rope, best_swim_str())
    best_run_rope = sue_belief.make_rope(best_rope, best_run_str())
    play_rope = sue_belief.make_rope(sports_rope, play_str())
    play_soccer_rope = sue_belief.make_rope(play_rope, play_soccer_str())
    play_swim_rope = sue_belief.make_rope(play_rope, play_swim_str())
    play_run_rope = sue_belief.make_rope(play_rope, play_run_str())
    sue_belief.add_fact(tidi_rope, dirty_rope, 4, 8)
    sue_belief.add_fact(best_rope, best_soccer_rope, 1, 7)
    mop_laborunit = laborunit_shop()
    mop_laborunit.add_party(sue_str)
    mop_laborunit.add_party(bob_str, True)
    sue_belief.edit_plan_attr(mop_rope, laborunit=mop_laborunit)
    # add reasons to mop_plan, sweep_plan, play_soccer_plan, plan_swim_plan, play_run_plan
    x_plan = "plan_rope"
    x_context = "reason_context"
    x_state = "reason_state"
    tidi_dirty_jkeys = {x_plan: mop_rope, x_context: tidi_rope, x_state: dirty_rope}
    swwep_dirty_jkeys = {x_plan: sweep_rope, x_context: tidi_rope, x_state: dirty_rope}
    soccer_soccer_jkeys = {
        x_plan: play_soccer_rope,
        x_context: best_rope,
        x_state: best_soccer_rope,
    }
    soccer_run_jkeys = {
        x_plan: play_soccer_rope,
        x_context: best_rope,
        x_state: best_run_rope,
    }
    soccer_tidy_jkeys = {
        x_plan: play_soccer_rope,
        x_context: tidi_rope,
        x_state: tidy_rope,
    }
    swim_swim_jkeys = {
        x_plan: play_swim_rope,
        x_context: best_rope,
        x_state: best_swim_rope,
    }
    swim_tidy_jkeys = {x_plan: play_swim_rope, x_context: tidi_rope, x_state: tidy_rope}
    run_run_jkeys = {
        x_plan: play_run_rope,
        x_context: best_rope,
        x_state: best_run_rope,
    }
    belief_plan_reason_caseunit_set_obj(sue_belief, tidi_dirty_jkeys)
    belief_plan_reason_caseunit_set_obj(sue_belief, swwep_dirty_jkeys)
    belief_plan_reason_caseunit_set_obj(sue_belief, soccer_soccer_jkeys)
    belief_plan_reason_caseunit_set_obj(sue_belief, soccer_run_jkeys)
    belief_plan_reason_caseunit_set_obj(sue_belief, soccer_tidy_jkeys)
    belief_plan_reason_caseunit_set_obj(sue_belief, swim_swim_jkeys)
    belief_plan_reason_caseunit_set_obj(sue_belief, swim_tidy_jkeys)
    belief_plan_reason_caseunit_set_obj(sue_belief, run_run_jkeys)
    sue_belief.cashout()
    return sue_belief
