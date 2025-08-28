from src.a05_plan_logic.test._util.a05_str import (
    _healerunit_ratio_str,
    _is_expanded_str,
    _kids_str,
    _level_str,
    _range_evaluated_str,
    _reasonheirs_str,
    _stop_calc_str,
    _uid_str,
    active_hx_str,
    addin_str,
    all_voice_cred_str,
    all_voice_debt_str,
    awardheirs_str,
    awardlines_str,
    begin_str,
    close_str,
    denom_str,
    descendant_task_count_str,
    factheirs_str,
    fund_cease_str,
    fund_onset_str,
    fund_ratio_str,
    fund_share_str,
    gogo_calc_str,
    gogo_want_str,
    healer_name_str,
    healerunit_str,
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
    assert active_hx_str() == "active_hx"
    assert all_voice_cred_str() == "all_voice_cred"
    assert all_voice_debt_str() == "all_voice_debt"
    assert awardheirs_str() == "awardheirs"
    assert awardlines_str() == "awardlines"
    assert descendant_task_count_str() == "descendant_task_count"
    assert factheirs_str() == "factheirs"
    assert fund_cease_str() == "fund_cease"
    assert fund_onset_str() == "fund_onset"
    assert fund_ratio_str() == "fund_ratio"
    assert gogo_calc_str() == "gogo_calc"
    assert _healerunit_ratio_str() == "_healerunit_ratio"
    assert _is_expanded_str() == "_is_expanded"
    assert _level_str() == "_level"
    assert _kids_str() == "_kids"
    assert _range_evaluated_str() == "_range_evaluated"
    assert _reasonheirs_str() == "_reasonheirs"
    assert _stop_calc_str() == "_stop_calc"
    assert _uid_str() == "_uid"
    assert addin_str() == "addin"
    assert begin_str() == "begin"
    assert close_str() == "close"
    assert plan_label_str() == "plan_label"
    assert plan_rope_str() == "plan_rope"
    assert denom_str() == "denom"
    assert fund_share_str() == "fund_share"
    assert gogo_want_str() == "gogo_want"
    assert healerunit_str() == "healerunit"

    assert star_str() == "star"
    assert morph_str() == "morph"
    assert numor_str() == "numor"
    assert task_str() == "task"
    assert problem_bool_str() == "problem_bool"
    assert stop_want_str() == "stop_want"
    assert healer_name_str() == "healer_name"
