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
    # THEN
    # A and C both treated as -1 → alphabetical between them
    assert result == ["C", "B", "A"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario4_alphabetical_tiebreaker():
    # ESTABLISH
    data = {
        "beta": {kw.exam_tier: 0, kw.valid_ch: kw.ch01},
        "Alpha": {kw.exam_tier: 0, kw.valid_ch: kw.ch01},
        "gamma": {kw.exam_tier: 0, kw.valid_ch: kw.ch01},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    assert result == ["Alpha", "beta", "gamma"]


def test_get_ch_sorted_keywords_ReturnsObj_Scenario5_missing_fields():
    # ESTABLISH
    data = {
        "A": {},  # missing both fields
        "B": {kw.exam_tier: 0},
        "C": {kw.valid_ch: kw.ch01},
    }
    # WHEN
    result = get_ch_sorted_keywords(data)
    # THEN
    # A: tier=inf, ch=-1 → last tier but first within that tier
    # C: tier=inf, ch=1
    # B: tier=0, ch=-1 → comes first overall
    assert result == ["A", "C", "B"]


def test_get_keywords_by_importance_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN
    kws_by_importance = get_keywords_by_importance()

    # THEN
    ch_sorted_keywords = get_ch_sorted_keywords(get_keywords_src_config())
    assert len(ch_sorted_keywords) == len(kws_by_importance)
    for sorted_count, sorted_keyword in enumerate(ch_sorted_keywords):
        assert kws_by_importance.get(sorted_count) == sorted_keyword

    keywords_src_config = get_keywords_src_config()
    for kw_index, kw_with_i in kws_by_importance.items():
        kw_src_config = keywords_src_config.get(kw_with_i)
        tier_str = kw_src_config.get(kw.exam_tier)
        valid_ch_str = kw_src_config.get(kw.valid_ch)
        # if kw_index < 30:
        #     print(f"{kw_index} {tier_str} {valid_ch_str} {kw_with_i=}")


def test_get_keg_exam_ReturnsObj_ObjExists():
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    assert isinstance(keg_exam, dict), "keg_exam must be a dict"
    assert keg_exam
    assert len(keg_exam) > 1


def test_get_keg_exam_ReturnsObj_KeysAreSequentialInts():
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    assert isinstance(keg_exam, dict), "keg_exam must be a dict"
    keys = list(keg_exam.keys())
    assert keys, "keg_exam should not be empty"

    int_keys = []
    for key in keys:
        assertion_failure_str = f"Expected string keys for keg_exam, but found key of type {type(key).__name__}: {key}"
        assert isinstance(key, str), assertion_failure_str
        assert key.isdigit(), f"Expected numeric string keys, but found: {key}"
        int_keys.append(int(key))

    sorted_keys = sorted(int_keys)
    start = sorted_keys[0]
    for expected, actual in zip(range(start, start + len(sorted_keys)), sorted_keys):
        assert expected == actual, (
            f"keg_exam first-level keys are not sequential: expected {expected} but found {actual}. "
            f"Break in sequence after {expected - 1}."
        )


def test_get_keg_exam_ReturnsObj_DictionariesHavekeys():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    assert isinstance(keg_exam, dict), "keg_exam must be a dict"
    required_fields = {"question_type", "question_str"}

    for exam_level, exam_dict in keg_exam.items():
        assert_dict_fails_str = f"Expected keg_exam[{exam_level!r}] to be a dict, but got {type(exam_dict).__name__}"
        assert isinstance(exam_dict, dict), assert_dict_fails_str
        missing_fields = required_fields - exam_dict.keys()
        assertion_missing_fields_fails = f"keg_exam[{exam_level!r}] is missing required field(s): {sorted(missing_fields)}"
        assert not missing_fields, assertion_missing_fields_fails

        if exam_dict.get("question_type") == "Keyword Definition":
            assert exam_dict.get("keyword")


def test_get_keg_exam_HasAll_keywords_DefinitionQuestions():
    # ESTABLISH / WHEN
    keg_exam = get_keg_exam()

    # THEN
    keywords_with_index_key = {
        key: value["keyword"]
        for key, value in keg_exam.items()
        if isinstance(value, dict)
        and value.get("question_type") == "Keyword Definition"
    }
    definition_fail_str = "No Keyword Definition questions found in keg_exam"
    assert keywords_with_index_key, definition_fail_str

    keg_definitions = get_keg_definitions()
    for keyword in keywords_with_index_key.values():
        assert keg_definitions.get(keyword) != None, keyword


# def first_out_of_order(
#     sorting_order: dict[int, str], exam_order: dict[int, str]
# ) -> str | None:
#     # Step 1: build expected ranking
#     expected_sequence = [keyword for _, keyword in sorted(sorting_order.items())]
#     rank = {keyword: i for i, keyword in enumerate(expected_sequence)}

#     # Step 2: iterate through exam order
#     last_rank = -1
#     for _, keyword in sorted(exam_order.items()):
#         if keyword not in rank:
#             # skip or raise depending on your use case
#             continue

#         current_rank = rank[keyword]

#         # Step 3: detect violation
#         if current_rank < last_rank:
#             print(f"{keyword} {current_rank=} {last_rank=}")
#             return keyword

#         last_rank = current_rank

#     return None


# TODO write keg_exam_doc_builder that passes this test
# follow keywords_main model: On every test run rewrite key_exam.json. Then run
# the tests so that it's clear it satisfies requirements.
# def test_get_keg_exam_DefinitionQuestionsAreInOrder():
#     # ESTABLISH / WHEN
#     keg_exam = get_keg_exam()
#     # THEN
#     definition_exam_keywords = {
#         key: value["keyword"]
#         for key, value in keg_exam.items()
#         if isinstance(value, dict)
#         and value.get("question_type") == "Keyword Definition"
#     }

#     sorted_keywords = dict(enumerate(get_ch_sorted_keywords(get_keywords_src_config())))
#     # print(f"{sorted_keywords=}")
#     assert not first_out_of_order(sorted_keywords, definition_exam_keywords)
#     # for keyword_term in sorted_keywords:
#     #     x_question_str = f"Have you read the Kegology definition of '{keyword_term}'?"
#     #     question_dict = {
#     #         "question_type": "Keyword Definition",
#     #         "question_str": x_question_str,
#     #         "keyword": keyword_term,
#     #     }
#     #     expected_keyword_definition_questions[str(x_count)] = question_dict
#     #     x_count += 1

#     # for exam_level, question_dict2 in expected_keyword_definition_questions.items():
#     #     print(f""""{exam_level}": {question_dict2},""")
#     # need to create new asserts that all keyword_terms have exam question


# The concept is that a set of statements like "I have read about the keg definition of 'plan'
# and the function will return the highest completed keg exam level.
# if new terms are introduced that could change a keg exam level measurement.
# Thus each exam measurement is associated with a keg version.
# def test_get_kegology_exam_grade_ReturnsHighestCompletedQuestionNum():
#     # ESTABLISH
#     # Simulating answers dict with question_str as key, answer as value
#     answers = {
#         "Have you heard of 'Kegology'?": "yes",
#         "Have you heard of 'Philosophy'?": "no",
#         # Question 2 is not answered
#     }

#     # WHEN
#     from ch98_docs_builder.keg_definitions_builder import (
#         get_kegology_exam_grade,
#     )

#     result = get_kegology_exam_grade(answers)

#     # THEN
#     # Should return 1 (the highest question number that is complete, which is before 2)
#     assert result == 1, f"Expected grade 1, but got {result}"

# # TODO get these tests working
# def test_get_kegology_exam_grade_AllQuestionsAnswered():
#     # ESTABLISH
#     keg_exam = get_keg_exam()
#     answers = {
#         value["question_str"]: "yes"
#         for value in keg_exam.values()
#         if isinstance(value, dict)
#     }

#     # WHEN
#     from ch98_docs_builder.keg_definitions_builder import (
#         get_kegology_exam_grade,
#     )

#     result = get_kegology_exam_grade(answers)

#     # THEN
#     # Should return the highest question number (len - 1 since we start from 0)
#     expected = len(keg_exam) - 1
#     assert (
#         result == expected
#     ), f"Expected grade {expected} (all questions), but got {result}"


# # TODO get these tests working
# def test_get_kegology_exam_grade_NoQuestionsAnswered():
#     # ESTABLISH
#     answers = {}

#     # WHEN
#     from ch98_docs_builder.keg_definitions_builder import (
#         get_kegology_exam_grade,
#     )

#     result = get_kegology_exam_grade(answers)

#     # THEN
#     # Should return -1 (no questions completed, so return before first question 0)
#     assert result == -1, f"Expected grade -1 (no questions), but got {result}"
