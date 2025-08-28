from src.a03_group_logic.test._util.a03_str import (
    credor_pool_str,
    debtor_pool_str,
    fund_agenda_give_str,
    fund_agenda_ratio_give_str,
    fund_agenda_ratio_take_str,
    fund_agenda_take_str,
    fund_give_str,
    fund_take_str,
    inallocable_voice_debt_points_str,
    irrational_voice_debt_points_str,
    memberships_str,
    voice_cred_points_str,
    voice_debt_points_str,
)
from src.a05_plan_logic.plan import planunit_shop
from src.a05_plan_logic.test._util.a05_str import (
    active_hx_str,
    active_str,
    addin_str,
    all_voice_cred_str,
    all_voice_debt_str,
    awardheirs_str,
    awardlines_str,
    awardunits_str,
    begin_str,
    cases_str,
    chore_str,
    close_str,
    denom_str,
    descendant_task_count_str,
    factheirs_str,
    factunits_str,
    fund_cease_str,
    fund_iota_str,
    fund_onset_str,
    fund_ratio_str,
    fund_share_str,
    gogo_calc_str,
    gogo_want_str,
    healerunit_ratio_str,
    healerunit_str,
    is_expanded_str,
    kids_str,
    knot_str,
    laborheir_str,
    laborunit_str,
    level_str,
    moment_label_str,
    morph_str,
    numor_str,
    plan_label_str,
    problem_bool_str,
    range_evaluated_str,
    reason_state_str,
    reasonheirs_str,
    reasonunits_str,
    star_str,
    stop_calc_str,
    stop_want_str,
    task_str,
    uid_str,
)
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    groupunits_str,
    parent_rope_str,
    planroot_str,
    voices_str,
)
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.a07_timeline_logic.test._util.a07_str import readable_str
from src.a22_belief_viewer.belief_viewer_tool import (
    add_small_dot,
    get_belief_view_dict,
    get_plan_view_dict,
    get_voices_view_dict,
)
from src.a22_belief_viewer.example22_beliefs import (
    best_run_str,
    best_soccer_str,
    best_sport_str,
    best_swim_str,
    get_beliefunit_irrational_example,
    get_sue_belief_with_facts_and_reasons,
    get_sue_beliefunit,
    play_run_str,
    play_soccer_str,
    play_str,
    play_swim_str,
)


def test_get_belief_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    sue_believer.cash_out()

    # WHEN
    sue_belief_view_dict = get_belief_view_dict(sue_believer)

    # THEN
    assert set(sue_belief_view_dict.keys()) == {
        # groupunits_str,
        voices_str(),
        planroot_str(),
    }
    sue_plan_view_dict = sue_belief_view_dict.get(planroot_str())
    expected_sue_plan_view_dict = get_plan_view_dict(sue_believer.planroot)
    assert sue_plan_view_dict == expected_sue_plan_view_dict
