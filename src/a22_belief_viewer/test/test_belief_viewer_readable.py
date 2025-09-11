from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.a22_belief_viewer.belief_viewer_tool import (
    add_small_dot,
    get_belief_view_dict,
    get_plan_view_dict,
    get_voices_view_dict,
)
from src.a22_belief_viewer.test._util.a22_str import planroot_str, voices_str


def test_get_belief_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    sue_believer.cashout()

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
