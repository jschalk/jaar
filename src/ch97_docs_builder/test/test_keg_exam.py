from ch00_py.file_toolbox import open_json, save_json
from ch00_py.keyword_class_builder import (
    get_ch_int,
    get_chapter_descs,
    get_keywords_src_config,
    parse_valid_ch_str,
)
from ch97_docs_builder._ref.ch97_path import create_term_rank_json_path
from ch97_docs_builder.glossary_ranking import (
    QuestionUnit,
    get_ch_sorted_keywords,
    get_exam_fixed_questions,
    get_keg_definition_questionunits,
    get_keg_definitions,
    get_keywords_by_importance,
    merge_fixed_and_floating_questions,
    rebuild_keg_exam_questions,
    rebuild_term_rank_json,
    set_did_you_read_orders,
)
from ch99_glossary.ch_keyword import Ch97Keywords as kw
from csv import reader as csv_reader
from os.path import exists as os_path_exists

# TODO replace how exam tier source of truth
# Having exam tier sourced in keywords_src makes it so example strings don't have exam_tiers.
# - [ ] create new json "keg_def_exam_tier.json", populate it with all terms in keg_definitions.json


def test_QuestionUnit_Exists():
    # ESTABLISH / WHEN
    questionunit = QuestionUnit()
    # THEN
    assert not QuestionUnit.keg_term
    assert not QuestionUnit.keg_definition
    assert not QuestionUnit.init_ch
    assert not QuestionUnit.exam_tier
    assert not QuestionUnit.did_you_read_order
    assert not QuestionUnit.complete_question
    assert set(questionunit.__dict__.keys()) == {
        "keg_term",
        kw.exam_tier,
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
        exam_tier=3,
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
        exam_tier=0,
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
        keg_term="alpha", exam_tier=0, init_ch=1, keg_definition="Alpha definition"
    )
    beta_questionunit = QuestionUnit(
        keg_term="beta", exam_tier=1, init_ch=10, keg_definition="Beta definition"
    )
    gamma_questionunit = QuestionUnit(
        keg_term="gamma", exam_tier=1, init_ch=5, keg_definition="Gamma definition"
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
    assert beta_questionunit.did_you_read_order == 0
    assert gamma_questionunit.did_you_read_order == 1


def test_set_did_you_read_orders_SetAttrs_Scenario3_SortsAlphabetically_WhenOtherFieldsMatch():
    # ESTABLISH
    zebra_questionunit = QuestionUnit(
        keg_term="zebra", exam_tier=1, init_ch=5, keg_definition="Zebra definition"
    )
    alpha_questionunit = QuestionUnit(
        keg_term="alpha", exam_tier=1, init_ch=5, keg_definition="Alpha definition"
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
        exam_tier=0,
        init_ch=None,
        keg_definition="Alpha definition",
    )

    numeric_init_ch_questionunit = QuestionUnit(
        keg_term="beta",
        exam_tier=0,
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


def test_rebuild_term_rank_json_SavesFile_Scenario0_NoFileExists(temp3_fs):
    # ESTABLISH
    src_dir = str(temp3_fs)
    exam_tier_path = create_term_rank_json_path(src_dir)
    assert not os_path_exists(exam_tier_path)
    # WHEN
    rebuild_term_rank_json(src_dir)
    # THEN
    assert os_path_exists(exam_tier_path)
    exam_tier_dict = open_json(exam_tier_path)

    keywords_src_config = get_keywords_src_config()
    chapter_descs = get_chapter_descs().keys()
    ch_ints = {get_ch_int(chapter_desc) for chapter_desc in chapter_descs}
    keg_questionunits = get_keg_definition_questionunits()
    set_did_you_read_orders(keg_questionunits)
    expected_keg_tiers = {}
    for keg_term, keg_qu in keg_questionunits.items():
        kw_config = keywords_src_config.get(keg_term)
        # if kw_config:
        #     ch_list = parse_valid_ch_str(ch_ints, kw_config.get("valid_ch"))
        # else:
        #     ch_list = set(ch_ints)
        valid_ch = kw_config.get("valid_ch") if kw_config else "0:"
        expected_keg_tiers[keg_qu.keg_term] = {
            "term_rank": keg_qu.did_you_read_order,
            "exam_tier": keg_qu.exam_tier,
            "chs": valid_ch,
        }
    for keg_term, exam_dict in expected_keg_tiers.items():
        print(f"{keg_term=} {exam_dict=}")
    assert exam_tier_dict == expected_keg_tiers


# def test_rebuild_term_rank_json_SavesFile_Scenario1_NoFileExists(temp3_fs):
#     # ESTABLISH
#     src_dir = str(temp3_fs)
#     exam_tier_path = create_term_rank_json_path(src_dir)
#     assert not os_path_exists(exam_tier_path)
#     # WHEN
#     rebuild_term_rank_json(src_dir)
#     # THEN
#     assert os_path_exists(exam_tier_path)
#     exam_tier_dict = open_json(exam_tier_path)

#     keywords_src_config = get_keywords_src_config()
#     chapter_descs = get_chapter_descs().keys()
#     ch_ints = {get_ch_int(chapter_desc) for chapter_desc in chapter_descs}
#     keg_questionunits = get_keg_definition_questionunits()
#     expected_keg_tiers = {}
#     for keg_term, keg_qu in keg_questionunits.items():
#         kw_config = keywords_src_config.get(keg_term)
#         # if kw_config:
#         #     ch_list = parse_valid_ch_str(ch_ints, kw_config.get("valid_ch"))
#         # else:
#         #     ch_list = set(ch_ints)
#         valid_ch = kw_config.get("valid_ch") if kw_config else "0:"
#         expected_keg_tiers[keg_qu.keg_term] = {
#             "exam_tier": keg_qu.exam_tier,
#             "chs": valid_ch,
#         }
#     for keg_term, exam_dict in expected_keg_tiers.items():
#         print(f"{keg_term=} {exam_dict=}")
#     assert exam_tier_dict == expected_keg_tiers


def test_get_exam_fixed_questions_ReturnsObj():
    # ESTABLISH / WHEN
    exam_fixed_questions = get_exam_fixed_questions()

    # THEN
    assert len(exam_fixed_questions) > 3
    for int_key in exam_fixed_questions.keys():
        assert int_key >= 0


def test_merge_fixed_and_floating_questions_ReturnsObj_Scenario0_OnlyFloatingQuestions():
    # ESTABLISH
    alpha_question = QuestionUnit(keg_term="alpha", exam_tier=0, init_ch=1)
    beta_question = QuestionUnit(keg_term="beta", exam_tier=1, init_ch=10)
    floating_questions = {"beta": beta_question, "alpha": alpha_question}
    fixed_questions = {}

    # WHEN
    result = merge_fixed_and_floating_questions(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == [beta_question, alpha_question]


def test_merge_fixed_and_floating_questions_ReturnsObj_Scenario1_FixedQuestionInsertedAtAbsoluteIndex():
    # ESTABLISH
    fixed_question = QuestionUnit(complete_question="Fixed Question")
    alpha_question = QuestionUnit(keg_term="alpha", exam_tier=0, init_ch=1)
    beta_question = QuestionUnit(keg_term="beta", exam_tier=1, init_ch=10)
    fixed_questions = {1: fixed_question}
    floating_questions = {"beta": beta_question, "alpha": alpha_question}

    # WHEN
    result = merge_fixed_and_floating_questions(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == [beta_question, fixed_question, alpha_question]


def test_merge_fixed_and_floating_questions_ReturnsObj_Scenario2_MultipleFixedIndexesRemainAbsolute():
    # ESTABLISH
    fixed_question_b = QuestionUnit(complete_question="Fixed B")
    fixed_question_d = QuestionUnit(complete_question="Fixed D")
    alpha_question = QuestionUnit(keg_term="alpha", exam_tier=0, init_ch=1)
    beta_question = QuestionUnit(keg_term="beta", exam_tier=1, init_ch=10)
    gamma_question = QuestionUnit(keg_term="gamma", exam_tier=1, init_ch=5)

    fixed_questions = {1: fixed_question_b, 3: fixed_question_d}
    floating_questions = {
        "gamma": gamma_question,
        "alpha": alpha_question,
        "beta": beta_question,
    }

    # WHEN
    result = merge_fixed_and_floating_questions(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == [
        beta_question,
        fixed_question_b,
        gamma_question,
        fixed_question_d,
        alpha_question,
    ]


def test_rebuild_keg_exam_questions_ReturnsNone_Scenario3_CreatesCsvFile(
    tmp_path,
):
    # ESTABLISH
    output_csv_path = tmp_path / "final_exam_questions.csv"
    # WHEN
    rebuild_keg_exam_questions(output_csv_path=output_csv_path)
    # THEN
    assert output_csv_path.exists()


def test_get_ch_sorted_keywords_ReturnsObj_Scenario0_basic_sorting():
    # ESTABLISH
    data = {
        "E": {kw.exam_tier: 0, kw.valid_ch: kw.ch17},
        "W": {kw.exam_tier: 0, kw.valid_ch: kw.ch02},
        "A": {kw.exam_tier: 1, kw.valid_ch: kw.ch01},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["A", "E", "W"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario1_empty_chapter_goes_first_within_tier():
    # ESTABLISH
    data = {
        "E": {kw.exam_tier: 0, kw.valid_ch: kw.ch17},
        "W": {kw.exam_tier: 0, kw.valid_ch: ""},
        "A": {kw.exam_tier: 0, kw.valid_ch: kw.ch02},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["W", "E", "A"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario2_empty_vs_other_tiers():
    # ESTABLISH
    data = {
        "A": {kw.exam_tier: 1, kw.valid_ch: ""},
        "B": {kw.exam_tier: 0, kw.valid_ch: kw.ch01},
        "C": {kw.exam_tier: 0, kw.valid_ch: ""},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    # Tier first, then chapter (empty first within same tier)
    assert result == ["A", "C", "B"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario3_malformed_chapter_treated_like_empty():
    # ESTABLISH
    data = {
        "A": {kw.exam_tier: 0, kw.valid_ch: "foo"},
        "B": {kw.exam_tier: 0, kw.valid_ch: kw.ch02},
        "C": {kw.exam_tier: 0, kw.valid_ch: ""},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
