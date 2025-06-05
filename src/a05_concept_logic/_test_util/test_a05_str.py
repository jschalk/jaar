from src.a05_concept_logic._test_util.a05_str import (
    _active_hx_str,
    _all_acct_cred_str,
    _all_acct_debt_str,
    _awardheirs_str,
    _awardlines_str,
    _descendant_pledge_count_str,
    _factheirs_str,
    _fund_cease_str,
    _fund_onset_str,
    _fund_ratio_str,
    _gogo_calc_str,
    _healerlink_ratio_str,
    _is_expanded_str,
    _kids_str,
    _range_evaluated_str,
    _reasonheirs_str,
    _stop_calc_str,
    _uid_str,
    addin_str,
    begin_str,
    close_str,
    concept_label_str,
    concept_way_str,
    denom_str,
    gogo_want_str,
    healer_name_str,
    healerlink_str,
    mass_str,
    morph_str,
    numor_str,
    pledge_str,
    problem_bool_str,
    stop_want_str,
)


def test_str_functions_ReturnsObj():
    assert _active_hx_str() == "_active_hx"
    assert _all_acct_cred_str() == "_all_acct_cred"
    assert _all_acct_debt_str() == "_all_acct_debt"
    assert _awardheirs_str() == "_awardheirs"
    assert _awardlines_str() == "_awardlines"
    assert _descendant_pledge_count_str() == "_descendant_pledge_count"
    assert _factheirs_str() == "_factheirs"
    assert _fund_cease_str() == "_fund_cease"
    assert _fund_onset_str() == "_fund_onset"
    assert _fund_ratio_str() == "_fund_ratio"
    assert _gogo_calc_str() == "_gogo_calc"
    assert _healerlink_ratio_str() == "_healerlink_ratio"
    assert _is_expanded_str() == "_is_expanded"
    assert _kids_str() == "_kids"
    assert _range_evaluated_str() == "_range_evaluated"
    assert _reasonheirs_str() == "_reasonheirs"
    assert _stop_calc_str() == "_stop_calc"
    assert _uid_str() == "_uid"
    assert addin_str() == "addin"
    assert begin_str() == "begin"
    assert close_str() == "close"
    assert concept_label_str() == "concept_label"
    assert concept_way_str() == "concept_way"
    assert denom_str() == "denom"
    assert gogo_want_str() == "gogo_want"
    assert healerlink_str() == "healerlink"
    assert mass_str() == "mass"
    assert morph_str() == "morph"
    assert numor_str() == "numor"
    assert pledge_str() == "pledge"
    assert problem_bool_str() == "problem_bool"
    assert stop_want_str() == "stop_want"
    assert healer_name_str() == "healer_name"
