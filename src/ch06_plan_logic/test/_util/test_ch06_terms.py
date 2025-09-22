from src.ch06_plan_logic._ref.ch06_terms import (
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
    fund_cease_str,
    fund_onset_str,
    fund_ratio_str,
    fund_share_str,
    gogo_calc_str,
    gogo_want_str,
    healer_name_str,
    healerunit_ratio_str,
    healerunit_str,
    is_expanded_str,
    kids_str,
    morph_str,
    numor_str,
    plan_label_str,
    plan_rope_str,
    problem_bool_str,
    range_evaluated_str,
    reasonheirs_str,
    star_str,
    stop_calc_str,
    stop_want_str,
    task_str,
    tree_level_str,
    tree_traverse_count_str,
    uid_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert active_hx_str() == "active_hx"
    assert all_voice_cred_str() == "all_voice_cred"
    assert all_voice_debt_str() == "all_voice_debt"
    assert awardheirs_str() == "awardheirs"
    assert awardlines_str() == "awardlines"
    assert descendant_task_count_str() == "descendant_task_count"
    assert fund_cease_str() == "fund_cease"
    assert fund_onset_str() == "fund_onset"
    assert fund_ratio_str() == "fund_ratio"
    assert gogo_calc_str() == "gogo_calc"
    assert healerunit_ratio_str() == "healerunit_ratio"
    assert is_expanded_str() == "is_expanded"
    assert tree_level_str() == "tree_level"
    assert kids_str() == "kids"
    assert range_evaluated_str() == "range_evaluated"
    assert reasonheirs_str() == "reasonheirs"
    assert stop_calc_str() == "stop_calc"
    assert uid_str() == "uid"
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
    assert tree_traverse_count_str() == "tree_traverse_count"
