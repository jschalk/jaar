from ch00_py.keyword_class_builder import get_keywords_src_config
from ch97_docs_builder.keg_definitions_builder import (
    QuestionUnit,
    get_ch_sorted_keywords,
    get_exam_fixed_questions,
    get_keg_definition_questionunits,
    get_keg_definitions,
    get_keywords_by_importance,
    merge_fixed_and_floating_questions,
    rebuild_final_exam_questions,
    set_did_you_read_orders,
)
from ch99_ref.keywords import Ch97Keywords as kw
from csv import reader as csv_reader

# TODO replace how exam tier source of truth
# Having exam tier sourced in keywords_main makes it so example strings don't have exam_tiers.
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


def test_rebuild_final_exam_questions_ReturnsNone_Scenario3_CreatesCsvFile(
    tmp_path,
):
    # ESTABLISH
    output_csv_path = tmp_path / "final_exam_questions.csv"
    # WHEN
    rebuild_final_exam_questions(output_csv_path=output_csv_path)
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


# def test_get_keg_exam_ReturnsObj_ObjExists():
#     # ESTABLISH / WHEN
#     keg_exam = get_keg_exam()

#     # THEN
#     assert isinstance(keg_exam, dict), "keg_exam must be a dict"
#     assert keg_exam
#     assert len(keg_exam) > 1


# def test_get_keg_exam_ReturnsObj_KeysAreSequentialInts():
#     # ESTABLISH / WHEN
#     keg_exam = get_keg_exam()

#     # THEN
#     assert isinstance(keg_exam, dict), "keg_exam must be a dict"
#     keys = list(keg_exam.keys())
#     assert keys, "keg_exam should not be empty"

#     int_keys = []
#     for key in keys:
#         assertion_failure_str = f"Expected string keys for keg_exam, but found key of type {type(key).__name__}: {key}"
#         assert isinstance(key, str), assertion_failure_str
#         assert key.isdigit(), f"Expected numeric string keys, but found: {key}"
#         int_keys.append(int(key))

#     sorted_keys = sorted(int_keys)
#     start = sorted_keys[0]
#     for expected, actual in zip(range(start, start + len(sorted_keys)), sorted_keys):
#         assert expected == actual, (
#             f"keg_exam first-level keys are not sequential: expected {expected} but found {actual}. "
#             f"Break in sequence after {expected - 1}."
#         )


# def test_get_keg_exam_ReturnsObj_DictionariesHavekeys():
#     # sourcery skip: no-conditionals-in-tests
#     # ESTABLISH / WHEN
#     keg_exam = get_keg_exam()

#     # THEN
#     assert isinstance(keg_exam, dict), "keg_exam must be a dict"
#     required_fields = {"question_type", "question_str"}

#     for exam_level, exam_dict in keg_exam.items():
#         assert_dict_fails_str = f"Expected keg_exam[{exam_level!r}] to be a dict, but got {type(exam_dict).__name__}"
#         assert isinstance(exam_dict, dict), assert_dict_fails_str
#         missing_fields = required_fields - exam_dict.keys()
#         assertion_missing_fields_fails = f"keg_exam[{exam_level!r}] is missing required field(s): {sorted(missing_fields)}"
#         assert not missing_fields, assertion_missing_fields_fails

#         if exam_dict.get("question_type") == "Keyword Definition":
#             assert exam_dict.get("keyword")


# def test_get_keg_exam_HasAll_keywords_DefinitionQuestions():
#     # ESTABLISH / WHEN
#     keg_exam = get_keg_exam()

#     # THEN
#     keywords_with_index_key = {
#         key: value["keyword"]
#         for key, value in keg_exam.items()
#         if isinstance(value, dict)
#         and value.get("question_type") == "Keyword Definition"
#     }
#     definition_fail_str = "No Keyword Definition questions found in keg_exam"
#     assert keywords_with_index_key, definition_fail_str

#     keg_definitions = get_keg_definitions()
#     for keyword in keywords_with_index_key.values():
#         assert keg_definitions.get(keyword) != None, keyword


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
#     from ch97_docs_builder.keg_definitions_builder import (
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
#     from ch97_docs_builder.keg_definitions_builder import (
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
#     from ch97_docs_builder.keg_definitions_builder import (
#         get_kegology_exam_grade,
#     )

#     result = get_kegology_exam_grade(answers)

#     # THEN
#     # Should return -1 (no questions completed, so return before first question 0)
#     assert result == -1, f"Expected grade -1 (no questions), but got {result}"
