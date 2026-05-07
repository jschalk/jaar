from ch00_py.keyword_class_builder import get_keywords_src_config
from ch98_docs_builder.keg_definitions_builder import (
    create_did_you_read_questions,
    create_final_exam_question_list,
    export_final_exam_questions_to_csv,
    get_ch_sorted_keywords,
    get_exam_middle1,
    get_keg_definitions,
    get_keg_exam,
    get_keywords_by_importance,
)
from csv import reader as csv_reader
from ref.keywords import Ch98Keywords as kw


# TODO change this it returns a obj like KegQTerm, there will be more to change
def test_get_exam_middle1_dict_ReturnsObj():
    # ESTABLISH / WHEN
    exam_middle1 = get_exam_middle1()
    # THEN
    keg_definitions = get_keg_definitions()
    assert set(keg_definitions.keys()) == set(exam_middle1.keys())
    expected_keys = {"keg_definition", "init_ch", "exam_tier"}
    for keg_term, exam_dict in exam_middle1.items():
        assert set(exam_dict.keys()) == expected_keys, keg_term


def test_create_did_you_read_questions_ReturnsEmptyList_WhenNoTermsExist():
    # ESTABLISH
    keg_terms = {}

    # WHEN
    result = create_did_you_read_questions(keg_terms)

    # THEN
    assert result == []


def test_create_did_you_read_questions_ReturnsSingleQuestion_WhenSingleTermProvided():
    # ESTABLISH
    keg_terms = {
        "star": {
            "exam_tier": 0,
            "keg_definition": "Used to measure weight of plan",
            "init_ch": 4,
        },
    }

    # WHEN
    result = create_did_you_read_questions(keg_terms)

    # THEN
    assert result == [
        (
            "Did you read about 'star'?",
            "Used to measure weight of plan",
        ),
    ]


def test_create_did_you_read_questions_ReturnsQuestionsSortedByExamTier():
    # ESTABLISH
    keg_terms = {
        "high": {
            "exam_tier": 5,
            "keg_definition": "High tier",
            "init_ch": 1,
        },
        "low": {
            "exam_tier": 0,
            "keg_definition": "Low tier",
            "init_ch": 1,
        },
    }

    # WHEN
    result = create_did_you_read_questions(keg_terms)

    # THEN
    assert result == [
        ("Did you read about 'low'?", "Low tier"),
        ("Did you read about 'high'?", "High tier"),
    ]


def test_create_did_you_read_questions_ReturnsQuestionsSortedByInitChDescending_WhenExamTierMatches():
    # ESTABLISH
    keg_terms = {
        "small_ch": {
            "exam_tier": 1,
            "keg_definition": "Small chapter",
            "init_ch": 2,
        },
        "large_ch": {
            "exam_tier": 1,
            "keg_definition": "Large chapter",
            "init_ch": 10,
        },
    }

    # WHEN
    result = create_did_you_read_questions(keg_terms)

    # THEN
    assert result == [
        ("Did you read about 'large_ch'?", "Large chapter"),
        ("Did you read about 'small_ch'?", "Small chapter"),
    ]


def test_create_did_you_read_questions_ReturnsAlphabeticalOrder_WhenExamTierAndInitChMatch():
    # ESTABLISH
    keg_terms = {
        "zebra": {
            "exam_tier": 2,
            "keg_definition": "Zebra definition",
            "init_ch": 5,
        },
        "alpha": {
            "exam_tier": 2,
            "keg_definition": "Alpha definition",
            "init_ch": 5,
        },
    }

    # WHEN
    result = create_did_you_read_questions(keg_terms)

    # THEN
    assert result == [
        ("Did you read about 'alpha'?", "Alpha definition"),
        ("Did you read about 'zebra'?", "Zebra definition"),
    ]


# TODO change this it handles a obj like KegQTerm, there will be more to change
def test_create_did_you_read_questions_ReturnsCorrectMultiFieldOrdering():
    # ESTABLISH
    keg_terms = {
        "gamma": {
            "exam_tier": 1,
            "keg_definition": "Gamma definition",
            "init_ch": 5,
        },
        "alpha": {
            "exam_tier": 0,
            "keg_definition": "Alpha definition",
            "init_ch": 1,
        },
        "beta": {
            "exam_tier": 1,
            "keg_definition": "Beta definition",
            "init_ch": 10,
        },
        "delta": {
            "exam_tier": 1,
            "keg_definition": "Delta definition",
            "init_ch": 5,
        },
    }

    # WHEN
    result = create_did_you_read_questions(keg_terms)

    # THEN
    assert result == [
        ("Did you read about 'alpha'?", "Alpha definition"),
        ("Did you read about 'beta'?", "Beta definition"),
        ("Did you read about 'delta'?", "Delta definition"),
        ("Did you read about 'gamma'?", "Gamma definition"),
    ]


# TODO change this it handles a obj like QuestionUnit, there will be more to change
def test_create_final_exam_question_list_ReturnsList_Scenario0_EmptyInputs():
    # ESTABLISH
    fixed_questions = {}
    floating_questions = []

    # WHEN
    result = create_final_exam_question_list(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == []


def test_create_final_exam_question_list_ReturnsList_Scenario0_OnlyFloatingQuestions():
    # ESTABLISH
    fixed_questions = {}
    floating_questions = ["Question A", "Question B"]

    # WHEN
    result = create_final_exam_question_list(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == ["Question A", "Question B"]


def test_create_final_exam_question_list_ReturnsList_Scenario0_FixedQuestionInsertedAtBeginning():
    # ESTABLISH
    fixed_questions = {0: "Fixed Question"}
    floating_questions = ["Question A", "Question B"]

    # WHEN
    result = create_final_exam_question_list(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == ["Fixed Question", "Question A", "Question B"]


def test_create_final_exam_question_list_ReturnsList_Scenario0_FixedQuestionInsertedInMiddle():
    # ESTABLISH
    fixed_questions = {1: "Fixed Question"}
    floating_questions = ["Question A", "Question B"]

    # WHEN
    result = create_final_exam_question_list(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == ["Question A", "Fixed Question", "Question B"]


def test_create_final_exam_question_list_ReturnsList_Scenario0_MultipleFixedIndexes():
    # ESTABLISH
    fixed_questions = {1: "Fixed B", 3: "Fixed D"}
    floating_questions = ["Question A", "Question C", "Question E"]

    # WHEN
    result = create_final_exam_question_list(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == ["Question A", "Fixed B", "Question C", "Fixed D", "Question E"]


# TODO change this it handes create_did_you_read_questions result
def test_create_final_exam_question_list_ReturnsList_Scenario0_FixedIndexesRemainAbsolute():
    # ESTABLISH
    fixed_questions = {2: "Fixed C", 5: "Fixed F"}
    floating_questions = ["Question A", "Question B", "Question D", "Question E"]

    # WHEN
    result = create_final_exam_question_list(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
    )

    # THEN
    assert result == [
        "Question A",
        "Question B",
        "Fixed C",
        "Question D",
        "Question E",
        "Fixed F",
    ]


def test_export_final_exam_questions_to_csv_ReturnsNone_Scenario0_WritesCsvFile(
    tmp_path,
):
    # ESTABLISH
    output_csv_path = tmp_path / "questions.csv"
    fixed_questions = {1: "Fixed Question"}
    floating_questions = ["Question A", "Question B"]

    # WHEN
    export_final_exam_questions_to_csv(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
        output_csv_path=output_csv_path,
    )

    # THEN
    with open(output_csv_path, newline="", encoding="utf-8") as csv_file:
        rows = list(csv_reader(csv_file))
    assert rows == [
        ["row_number", "question"],
        ["0", "Question A"],
        ["1", "Fixed Question"],
        ["2", "Question B"],
    ]


# TODO change this so exported csv has question number, keg_term, question_str
def test_export_final_exam_questions_to_csv_ReturnsNone_Scenario0_WritesEmptyCsvWithHeaderOnly(
    tmp_path,
):
    # ESTABLISH
    output_csv_path = tmp_path / "questions.csv"

    fixed_questions = {}
    floating_questions = []

    # WHEN
    export_final_exam_questions_to_csv(
        fixed_questions=fixed_questions,
        floating_questions=floating_questions,
        output_csv_path=output_csv_path,
    )

    # THEN
    with open(output_csv_path, newline="", encoding="utf-8") as csv_file:
        rows = list(csv_reader(csv_file))

    assert rows == [["row_number", "question"]]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario0_basic_sorting():
    # ESTABLISH
    data = {
        "Excel": {kw.exam_tier: 0, kw.valid_ch: kw.ch17},
        "Word": {kw.exam_tier: 0, kw.valid_ch: kw.ch02},
        "Access": {kw.exam_tier: 1, kw.valid_ch: kw.ch01},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["Access", "Excel", "Word"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario1_empty_chapter_goes_first_within_tier():
    # ESTABLISH
    data = {
        "Excel": {kw.exam_tier: 0, kw.valid_ch: kw.ch17},
        "Word": {kw.exam_tier: 0, kw.valid_ch: ""},
        "Access": {kw.exam_tier: 0, kw.valid_ch: kw.ch02},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["Word", "Excel", "Access"]


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
