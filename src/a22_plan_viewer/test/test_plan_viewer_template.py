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
    _healerlink_ratio_str,
    _is_expanded_str,
    _kids_str,
    _level_str,
    _range_evaluated_str,
    _reasonheirs_str,
    _stop_calc_str,
    _uid_str,
    addin_str,
    begin_str,
    belief_label_str,
    close_str,
    denom_str,
    fund_iota_str,
    fund_share_str,
    gogo_want_str,
    healerlink_str,
    knot_str,
    morph_str,
    numor_str,
    plan_label_str,
    problem_bool_str,
    star_str,
    stop_want_str,
    task_str,
)
from src.a06_believer_logic.believer_tool import believer_plan_factunit_get_obj
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.a22_plan_viewer.app import get_plan_viewer_template
from src.a22_plan_viewer.plan_viewer import add_small_dot, get_plan_view_dict
from src.a22_plan_viewer.test._util.example22_believers import get_sue_casa_believerunit


def test_get_plan_viewer_template_ReturnsObj():
    # ESTABLISH / WHEN
    template_str = get_plan_viewer_template()

    # THEN
    assert template_str
    expected_strs_in_template = {
        # _active_hx_str(),
        _active_str(),
        _all_partner_cred_str(),
        _all_partner_debt_str(),
        _awardheirs_str(),
        _awardlines_str(),
        _chore_str(),
        _descendant_task_count_str(),
        _factheirs_str(),
        _fund_cease_str(),
        _fund_onset_str(),
        _fund_ratio_str(),
        # _gogo_calc_str(),
        # _healerlink_ratio_str(),
        # _is_expanded_str(),
        # "_laborheir",
        _level_str(),
        # _range_evaluated_str(),
        # _reasonheirs_str(),
        # _stop_calc_str(),
        _uid_str(),
        # addin_str(),
        "awardlinks",
        # begin_str(),
        belief_label_str(),
        # close_str(),
        # denom_str(),
        "factunits",
        fund_iota_str(),
        "fund_share",
        # gogo_want_str(),
        # healerlink_str(),
        # knot_str(),
        # "laborunit",
        # morph_str(),
        # numor_str(),
        "parent_rope",
        # plan_label_str(),
        # problem_bool_str(),
        # "reasonunits",
        "root",
        star_str(),
        # stop_want_str(),
        task_str(),
    }

    for expected_str in sorted(list(expected_strs_in_template)):
        print(f"{expected_str=}")
        assert template_str.find(expected_str) > 0
