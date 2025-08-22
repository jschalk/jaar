from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_partner_debt_points_str,
    _irrational_partner_debt_points_str,
    _memberships_str,
    partner_cred_points_str,
    partner_debt_points_str,
)
from src.a05_plan_logic.plan import planunit_shop
from src.a05_plan_logic.test._util.a05_str import (
    _active_hx_str,
    _active_str,
    _all_partner_cred_str,
    _all_partner_debt_str,
    _awardheirs_str,
    _awardlines_str,
    _chore_str,
    _descendant_task_count_str,
    _factheirs_str,
    _fund_cease_str,
    _fund_onset_str,
    _fund_ratio_str,
    _gogo_calc_str,
    _healerunit_ratio_str,
    _is_expanded_str,
    _kids_str,
    _laborheir_str,
    _level_str,
    _range_evaluated_str,
    _reasonheirs_str,
    _stop_calc_str,
    _uid_str,
    addin_str,
    awardunits_str,
    begin_str,
    cases_str,
    close_str,
    denom_str,
    factunits_str,
    fund_iota_str,
    fund_share_str,
    gogo_want_str,
    healerunit_str,
    knot_str,
    laborunit_str,
    moment_label_str,
    morph_str,
    numor_str,
    plan_label_str,
    problem_bool_str,
    reason_state_str,
    reasonunits_str,
    star_str,
    stop_want_str,
    task_str,
)
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    _groupunits_str,
    parent_rope_str,
    partners_str,
    planroot_str,
)
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.a07_timeline_logic.test._util.a07_str import readable_str
from src.a22_belief_viewer.belief_viewer_tool import (
    add_small_dot,
    get_belief_view_dict,
    get_partners_view_dict,
    get_plan_view_dict,
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
        # _groupunits_str,
        partners_str(),
        planroot_str(),
    }
    sue_plan_view_dict = sue_belief_view_dict.get(planroot_str())
    expected_sue_plan_view_dict = get_plan_view_dict(sue_believer.planroot)
    assert sue_plan_view_dict == expected_sue_plan_view_dict
