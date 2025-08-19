from src.a05_plan_logic.test._util.a05_str import (
    _active_hx_str,
    _all_partner_cred_str,
    _all_partner_debt_str,
    _awardheirs_str,
    _awardlines_str,
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
    awardlinks_str,
    begin_str,
    close_str,
    denom_str,
    fund_share_str,
    gogo_want_str,
    healer_name_str,
    healerlink_str,
    morph_str,
    numor_str,
    plan_label_str,
    plan_rope_str,
    problem_bool_str,
    star_str,
    stop_want_str,
    task_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert _active_hx_str() == "_active_hx"
    assert _all_partner_cred_str() == "_all_partner_cred"
    assert _all_partner_debt_str() == "_all_partner_debt"
    assert _awardheirs_str() == "_awardheirs"
    assert _awardlines_str() == "_awardlines"
    assert _descendant_task_count_str() == "_descendant_task_count"
    assert _factheirs_str() == "_factheirs"
    assert _fund_cease_str() == "_fund_cease"
    assert _fund_onset_str() == "_fund_onset"
    assert _fund_ratio_str() == "_fund_ratio"
    assert _gogo_calc_str() == "_gogo_calc"
    assert _healerlink_ratio_str() == "_healerlink_ratio"
    assert _is_expanded_str() == "_is_expanded"
    assert _level_str() == "_level"
    assert _kids_str() == "_kids"
    assert _range_evaluated_str() == "_range_evaluated"
    assert _reasonheirs_str() == "_reasonheirs"
    assert _stop_calc_str() == "_stop_calc"
    assert _uid_str() == "_uid"
    assert addin_str() == "addin"
    assert awardlinks_str() == "awardlinks"
    assert begin_str() == "begin"
    assert close_str() == "close"
    assert plan_label_str() == "plan_label"
    assert plan_rope_str() == "plan_rope"
    assert denom_str() == "denom"
    assert fund_share_str() == "fund_share"
    assert gogo_want_str() == "gogo_want"
    assert healerlink_str() == "healerlink"
    assert star_str() == "star"
    assert morph_str() == "morph"
    assert numor_str() == "numor"
    assert task_str() == "task"
    assert problem_bool_str() == "problem_bool"
    assert stop_want_str() == "stop_want"
    assert healer_name_str() == "healer_name"
