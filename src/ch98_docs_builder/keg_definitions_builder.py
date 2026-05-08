from ch00_py.chapter_desc_main import get_chapter_desc_prefix, get_chapter_descs
from ch00_py.dict_toolbox import get_0_if_None
from ch00_py.file_toolbox import create_path, open_json, save_json
from ch00_py.keyword_class_builder import (
    get_chapter_descs,
    get_keywords_src_config,
    parse_valid_ch_str,
)
from ch07_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_calc_dimen_args,
    get_person_config_dict,
)
from ch18_etl_config.etl_config import get_etl_stage_types_config_dict
from ch98_docs_builder._ref.ch98_path import (
    create_chapter_ref_path,
    create_src_keg_definitions_path,
    create_src_keg_exam_path,
)
from csv import writer as csv_writer
from dataclasses import dataclass
from pathlib import Path
from re import search as re_search


def get_keg_definitions() -> dict[str, dict]:
    return open_json(create_src_keg_definitions_path("src"))


def save_keg_descriptions_json(src_dir: str, x_dict: dict[str, dict]):
    file_path = create_src_keg_definitions_path(src_dir)
    save_json(file_path, None, x_dict, keys_case_insensitive=True)


def get_person_dimen_config(dimen: str) -> dict:
    x_dimen_config = get_person_config_dict().get(dimen)
    x_config_args = x_dimen_config.get("jkeys")
    for v_keyword, v_config in x_dimen_config.get("jvalues").items():
        x_config_args[v_keyword] = v_config
    return x_config_args


def rebuild_keg_definitions_contents():
    ch_dict = get_chxx_prefix_path_dict()
    person_config_args = get_person_dimen_config("personunit")
    plan_config_args = get_person_dimen_config("person_planunit")
    all_person_calc_args = get_all_person_calc_args()

    rebuilt_kw_desc = {}
    for keyword, description in get_keg_definitions().items():
        rebuilt_kw_desc[keyword] = description
        if keyword in ch_dict:
            rebuilt_kw_desc[keyword] = get_chxx_ref_blurb(ch_dict, keyword)
        if keyword in person_config_args:
            keyword_config = person_config_args.get(keyword)
            if keyword_config.get("calc_by_thinkout"):
                # rebuilt_kw_desc[keyword] = f"Person thinkout"
                pass
            # else:
            #     # rebuilt_kw_desc[keyword] = f"Set by seed part of the Person bluep"
            #     pass
        # if keyword in plan_config_args:
        #     keyword_config = plan_config_args.get(keyword)
        #     if keyword_config.get("calc_by_thinkout"):
        #         rebuilt_kw_desc[keyword] = f"Set by Person thinkout process"
        #     else:
        #         rebuilt_kw_desc[keyword] = f"Plan seed data"

    save_keg_descriptions_json("src", rebuilt_kw_desc)


def get_chxx_prefix_path_dict() -> dict[str, str]:
    ch_dict = {}
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
        ch_ref_path = create_chapter_ref_path(chapter_dir, chapter_desc_prefix)
        ch_dict[chapter_desc_prefix] = ch_ref_path
    return ch_dict


def get_chxx_ref_blurb(ch_dict, keyword) -> str:
    ch_ref_dict = open_json(ch_dict[keyword])
    return ch_ref_dict.get("chapter_blurb")


@dataclass
class QuestionUnit:
    keg_term: str = None
    keg_definition: str = None
    init_ch: int = None
    exam_tier: int = None
    did_you_read_order: int = None
    complete_question: str = None

    def get_question(self) -> str:
        if self.complete_question:
            return self.complete_question
        return f"Did you read that the keg_definition of '{self.keg_term}' is '{self.keg_definition}'."


def get_keg_definition_questionunits() -> dict[str, QuestionUnit]:
    chapter_descs = get_chapter_descs().keys()
    ch_ints = {int(chapter_desc[2:4]) for chapter_desc in chapter_descs}
    keywords_src_config = get_keywords_src_config()

    keg_definitions = get_keg_definitions()
    keg_questions = {}
    for keg_term, keg_definition in keg_definitions.items():
        kw_config = keywords_src_config.get(keg_term)
        questionunit = QuestionUnit(keg_term, keg_definition)
        if kw_config:
            valid_chs = parse_valid_ch_str(ch_ints, kw_config.get("valid_ch"))
            init_ch = sorted(valid_chs)[0] if valid_chs else None
            questionunit.init_ch = init_ch
            questionunit.exam_tier = kw_config.get("exam_tier")
        else:
            questionunit.exam_tier = 0
        keg_questions[keg_term] = questionunit
    return keg_questions


def set_did_you_read_orders(keg_questions: dict[str, QuestionUnit]) -> None:
    """
    Assign did_you_read_order values in-place.

    Ordering rules:
        1. exam_tier ascending
        2. init_ch descending
        3. keg_term alphabetical
    """
    sorted_questunits = sorted(
        keg_questions.values(),
        key=lambda q: (
            -q.exam_tier,
            q.init_ch is not None,  # None last or first depending on your preference
            -(q.init_ch or 0),  # descending for ints
            q.keg_term,
        ),
    )
    for did_you_read_order, questionunit in enumerate(sorted_questunits):
        questionunit.did_you_read_order = did_you_read_order


def get_exam_fixed_questions() -> dict[int, QuestionUnit]:
    question000 = "Have you heard of 'Kegology'?"
    question010 = "Have you heard of Excel spreadsheet application?"
    return {
        0: QuestionUnit(complete_question=question000),
        1: QuestionUnit(complete_question="Have you heard the word 'Philosophy'?"),
        2: QuestionUnit(complete_question="Do you believe listening is important?"),
        10: QuestionUnit(complete_question=question010),
    }


def merge_fixed_and_floating_questions(
    fixed_questions: dict[int, QuestionUnit],
    floating_questions: dict[str, QuestionUnit],
) -> list[QuestionUnit]:
    """
    Merge fixed-position QuestionUnits with floating QuestionUnits.

    Fixed indexes are absolute.
    Floating questions are inserted into all remaining positions.
    """

    set_did_you_read_orders(floating_questions)

    sorted_floating_questions: list[QuestionUnit] = sorted(
        floating_questions.values(),
        key=lambda questionunit: questionunit.did_you_read_order,
    )

    result_questionunits: list[QuestionUnit] = []

    floating_index = 0
    total_length = len(fixed_questions) + len(sorted_floating_questions)

    for index in range(total_length):
        if index in fixed_questions:
            result_questionunits.append(fixed_questions[index])
        else:
            result_questionunits.append(sorted_floating_questions[floating_index])
            floating_index += 1

    for question in result_questionunits:
        print(f"{question.keg_term} {question.did_you_read_order=}")

    return result_questionunits


def rebuild_final_exam_questions(
    output_csv_path: str | Path,
) -> None:
    """
    Create the final exam question list and export it to a CSV file.

    CSV columns:
        - row_number
        - question
    """
    final_questions = merge_fixed_and_floating_questions(
        fixed_questions=get_exam_fixed_questions(),
        floating_questions=get_keg_definition_questionunits(),
    )

    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv_writer(csv_file)
        writer.writerow(["row_number", "question"])
        for row_number, questionunit in enumerate(final_questions):
            writer.writerow([row_number, questionunit.get_question()])


def get_ch_sorted_keywords(keywords_src_config: dict) -> list[str]:
    def parse_chapter(ch):
        if not ch:
            return float("inf")  # push empty to front
        match = re_search(r"\d+", ch)
        return int(match.group()) if match else -1

    return sorted(
        keywords_src_config.keys(),
        key=lambda k: (
            -keywords_src_config[k].get("exam_tier", float("inf")),
            -parse_chapter(keywords_src_config[k].get("valid_ch", "")),
            k.lower(),
        ),
    )


def get_keywords_by_importance() -> dict:
    x_list = get_ch_sorted_keywords(get_keywords_src_config())
    return dict(enumerate(x_list))


def get_kegology_exam_grade(answers: dict[str, str]) -> int:
    """Return the highest completed exam question index.

    A question is complete only when its question_str maps to "yes" in answers.
    If a question is missing or not answered "yes", the grade is the previous
    question index. If the first question is incomplete, return -1.
    """
    return 0
    # keg_exam = get_keg_exam()

    # question_numbers = []
    # question_map = {}
    # for key, value in keg_exam.items():
    #     question_str = value.get("question_str")
    #     question_number = int(key)
    #     question_numbers.append(question_number)
    #     question_map[question_number] = question_str

    # if not question_numbers:
    #     return -1

    # for question_number in sorted(question_numbers):
    #     question_str = question_map[question_number]
    #     answer = answers.get(question_str)
    #     if not isinstance(answer, str) or answer.strip().lower() != "yes":
    #         return question_number - 1

    # return max(question_numbers)
