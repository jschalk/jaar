from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    acct_pool_str,
    addin_str,
    awardee_title_str,
    rcontext_str,
    begin_str,
    close_str,
    concept_label_str,
    credit_belief_str,
    credor_respect_str,
    credit_vote_str,
    debtit_belief_str,
    debtor_respect_str,
    debtit_vote_str,
    denom_str,
    event_int_str,
    face_name_str,
    fcontext_str,
    fstate_str,
    fnigh_str,
    fopen_str,
    fund_coin_str,
    give_force_str,
    gogo_want_str,
    group_title_str,
    healer_name_str,
    mass_str,
    morph_str,
    pledge_str,
    pstate_str,
    pnigh_str,
    numor_str,
    popen_str,
    parent_way_str,
    penny_str,
    respect_bit_str,
    rconcept_active_requisite_str,
    concept_way_str,
    stop_want_str,
    take_force_str,
    labor_title_str,
    NameStr_str,
    TitleStr_str,
    LabelStr_str,
    WayStr_str,
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_awardlink_str,
    bud_concept_reasonunit_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_laborlink_str,
    bud_concept_healerlink_str,
    bud_concept_factunit_str,
    bud_groupunit_str,
)


def test_str_functions_ReturnsObj():
    assert acct_pool_str() == "acct_pool"
    assert addin_str() == "addin"
    assert awardee_title_str() == "awardee_title"
    assert rcontext_str() == "rcontext"
    assert fcontext_str() == "fcontext"
    assert begin_str() == "begin"
    assert close_str() == "close"
    assert credit_belief_str() == "credit_belief"
    assert credor_respect_str() == "credor_respect"
    assert credit_vote_str() == "credit_vote"
    assert debtit_belief_str() == "debtit_belief"
    assert debtor_respect_str() == "debtor_respect"
    assert debtit_vote_str() == "debtit_vote"
    assert denom_str() == "denom"
    assert event_int_str() == "event_int"
    assert face_name_str() == "face_name"
    assert fstate_str() == "fstate"
    assert fnigh_str() == "fnigh"
    assert fopen_str() == "fopen"
    assert fund_coin_str() == "fund_coin"
    assert give_force_str() == "give_force"
    assert gogo_want_str() == "gogo_want"
    assert group_title_str() == "group_title"
    assert healer_name_str() == "healer_name"
    assert mass_str() == "mass"
    assert morph_str() == "morph"
    assert pledge_str() == "pledge"
    assert pstate_str() == "pstate"
    assert pnigh_str() == "pnigh"
    assert numor_str() == "numor"
    assert popen_str() == "popen"
    assert parent_way_str() == "parent_way"
    assert penny_str() == "penny"
    assert rconcept_active_requisite_str() == "rconcept_active_requisite"
    assert respect_bit_str() == "respect_bit"
    assert concept_label_str() == "concept_label"
    assert concept_way_str() == "concept_way"
    assert stop_want_str() == "stop_want"
    assert take_force_str() == "take_force"
    assert labor_title_str() == "labor_title"
    assert NameStr_str() == "NameStr"
    assert TitleStr_str() == "TitleStr"
    assert LabelStr_str() == "LabelStr"
    assert WayStr_str() == "WayStr"
    assert budunit_str() == "budunit"
    assert bud_acctunit_str() == "bud_acctunit"
    assert bud_acct_membership_str() == "bud_acct_membership"
    assert bud_groupunit_str() == "bud_groupunit"
    assert bud_conceptunit_str() == "bud_conceptunit"
    assert bud_concept_awardlink_str() == "bud_concept_awardlink"
    assert bud_concept_reasonunit_str() == "bud_concept_reasonunit"
    assert bud_concept_reason_premiseunit_str() == "bud_concept_reason_premiseunit"
    assert bud_concept_laborlink_str() == "bud_concept_laborlink"
    assert bud_concept_healerlink_str() == "bud_concept_healerlink"
    assert bud_concept_factunit_str() == "bud_concept_factunit"
