from ch97_docs_builder.glossary_ranking import (
    QuestionUnit,
    get_keg_definition_questionunits,
    get_keg_definitions,
    set_did_you_read_orders,
)
from ch99_glossary.ch_keyword import Ch97Keywords as kw


def test_QuestionUnit_Exists():
    # ESTABLISH / WHEN
    questionunit = QuestionUnit()
    # THEN
    assert not QuestionUnit.keg_term
    assert not QuestionUnit.keg_definition
    assert not QuestionUnit.init_ch
    assert not QuestionUnit.rank_tier
    assert not QuestionUnit.did_you_read_order
    assert not QuestionUnit.complete_question
    assert set(questionunit.__dict__.keys()) == {
        "keg_term",
        kw.rank_tier,
        "keg_definition",
        "init_ch",
        "did_you_read_order",
        "complete_question",
    }


def test_QuestionUnit_get_question_ReturnsObj_Scenario0():
    # ESTABLISH
    star_definition = f"{kw.star} is an attribute that represents A."
    star_questionunit = QuestionUnit(kw.star, star_definition)
    # WHEN
    did_you_read_question_str = star_questionunit.get_question()
    # THEN
    assert did_you_read_question_str
    expected_did_you_read_question_str = (
        f"Did you read that the keg_definition of '{kw.star}' is '{star_definition}'."
    )
    assert did_you_read_question_str == expected_did_you_read_question_str


def test_QuestionUnit_get_question_ReturnsObj_Scenario1_complete_question_Exists():
    # ESTABLISH
    expected_question_str = "Have you heard of Kegology?"
    a_questionunit = QuestionUnit(complete_question=expected_question_str)
    # WHEN
    a_question_str = a_questionunit.get_question()
    # THEN
    assert a_question_str
    assert a_question_str == expected_question_str


def test_get_keg_definition_questionunits_ReturnsObj():
    # ESTABLISH / WHEN
    keg_questions1 = get_keg_definition_questionunits()
    # THEN
    keg_definitions = get_keg_definitions()
    assert set(keg_definitions.keys()) == set(keg_questions1.keys())
    expected_year_length_questionunit = QuestionUnit(
        keg_term=kw.year_length,
        keg_definition=keg_definitions.get(kw.year_length),
        init_ch=13,
        rank_tier=0,
    )
    assert keg_questions1.get(kw.year_length) == expected_year_length_questionunit


def test_set_did_you_read_orders_SetAttrs_Scenario0_EmptyList_WhenNoTermsExist():
    # ESTABLISH
    keg_questions = {}

    # WHEN
    set_did_you_read_orders(keg_questions)

    # THEN
    assert not keg_questions


def test_set_did_you_read_orders_SetAttrs_Scenario1_SingleQuestion_WhenSingleTermProvided():
    # ESTABLISH
    star_questionunit = QuestionUnit(
        keg_term=kw.star,
        rank_tier=0,
        init_ch=4,
        keg_definition="Used to measure weight of plan",
    )
    keg_questions = {kw.star: star_questionunit}
    assert star_questionunit.did_you_read_order is None

    # WHEN
    set_did_you_read_orders(keg_questions)

    # THEN
    assert star_questionunit.did_you_read_order == 0


def test_set_did_you_read_orders_SetAttrs_Scenario2_AssignsSequentialOrder():
    # ESTABLISH
    alpha_questionunit = QuestionUnit(
        keg_term="alpha", rank_tier=0, init_ch=1, keg_definition="Alpha definition"
    )
    beta_questionunit = QuestionUnit(
        keg_term="beta", rank_tier=1, init_ch=10, keg_definition="Beta definition"
    )
    gamma_questionunit = QuestionUnit(
        keg_term="gamma", rank_tier=1, init_ch=5, keg_definition="Gamma definition"
    )
    keg_questions = {
        "gamma": gamma_questionunit,
        "alpha": alpha_questionunit,
        "beta": beta_questionunit,
    }

    # WHEN
    set_did_you_read_orders(keg_questions)

    # THEN
    assert alpha_questionunit.did_you_read_order == 2
    assert beta_questionunit.did_you_read_order == 1
    assert gamma_questionunit.did_you_read_order == 0


def test_set_did_you_read_orders_SetAttrs_Scenario3_SortsAlphabetically_WhenOtherFieldsMatch():
    # ESTABLISH
    zebra_questionunit = QuestionUnit(
        keg_term="zebra", rank_tier=1, init_ch=5, keg_definition="Zebra definition"
    )
    alpha_questionunit = QuestionUnit(
        keg_term="alpha", rank_tier=1, init_ch=5, keg_definition="Alpha definition"
    )
    keg_questions = {"zebra": zebra_questionunit, "alpha": alpha_questionunit}

    # WHEN
    set_did_you_read_orders(keg_questions)

    # THEN
    assert alpha_questionunit.did_you_read_order == 0
    assert zebra_questionunit.did_you_read_order == 1


def test_set_did_you_read_orders_SetAttrs_Scenario4_SortsNoneInitChAheadOfNumericInitCh():
    # ESTABLISH
    none_init_ch_questionunit = QuestionUnit(
        keg_term="alpha",
        rank_tier=0,
        init_ch=None,
        keg_definition="Alpha definition",
    )

    numeric_init_ch_questionunit = QuestionUnit(
        keg_term="beta",
        rank_tier=0,
        init_ch=99,
        keg_definition="Beta definition",
    )

    keg_questions = {
        "beta": numeric_init_ch_questionunit,
        "alpha": none_init_ch_questionunit,
    }

    # WHEN
    set_did_you_read_orders(keg_questions)

    # THEN
    assert none_init_ch_questionunit.did_you_read_order == 0
    assert numeric_init_ch_questionunit.did_you_read_order == 1
