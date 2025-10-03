from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.ch22_belief_viewer.belief_viewer__tool import (
    add_small_dot,
    get_belief_view_dict,
    get_plan_view_dict,
    get_voices_view_dict,
)
from src.ref.ch22_keywords import Ch22Keywords as wx


def test_get_belief_view_dict_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_str = "Sue"
    sue_believer = beliefunit_shop(sue_str)
    sue_believer.cashout()

    # WHEN
    sue_belief_view_dict = get_belief_view_dict(sue_believer)

    # THEN
    assert set(sue_belief_view_dict.keys()) == {
        # wx.groupunits,
        wx.voices,
        wx.planroot,
    }
    sue_plan_view_dict = sue_belief_view_dict.get(wx.planroot)
    expected_sue_plan_view_dict = get_plan_view_dict(sue_believer.planroot)
    assert sue_plan_view_dict == expected_sue_plan_view_dict
