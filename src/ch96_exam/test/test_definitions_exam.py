from ch96_exam.definitions_exam import get_keg_yes_mapping_level
from pathlib import Path as Path


def _write_csv(dir_x: Path, filename_x: str, content_x: str) -> str:
    filepath_x = dir_x / filename_x
    filepath_x.write_text(content_x, encoding="utf-8")
    return str(filepath_x)


def test_get_keg_yes_mapping_level_ReturnsObj_Scenario00_AllQuestionsYesInAnyOrder(
    tmp_path,
):
    # ESTABLISH
    static_csv_x = _write_csv(
        tmp_path,
        "static.csv",
        "question\n"
        "Have you heard of 'Kegology'?\n"
        "Have you heard the word 'Philosophy'?\n"
        "Do you believe listening is important?\n",
    )
    given_csv_x = _write_csv(
        tmp_path,
        "given.csv",
        "yes/no,question\n"
        "yes,Do you believe listening is important?\n"
        "yes,Have you heard of 'Kegology'?\n"
        "yes,Have you heard the word 'Philosophy'?\n",
    )

    # WHEN
    level_complete_x = get_keg_yes_mapping_level(given_csv_x, static_csv_x)

    # THEN
    assert level_complete_x == 3


def test_get_keg_yes_mapping_level_ReturnsObj_Scenario01_FirstQuestionMissing(tmp_path):
    # ESTABLISH
    static_csv_x = _write_csv(
        tmp_path,
        "static.csv",
        "question\n"
        "Have you heard of 'Kegology'?\n"
        "Have you heard the word 'Philosophy'?\n",
    )
    given_csv_x = _write_csv(
        tmp_path,
        "given.csv",
        "yes/no,question\n" "yes,Have you heard the word 'Philosophy'?\n",
    )

    # WHEN
    level_complete_x = get_keg_yes_mapping_level(given_csv_x, static_csv_x)

    # THEN
    assert level_complete_x == 0


def test_get_keg_yes_mapping_level_ReturnsObj_Scenario02_MiddleQuestionAnsweredNo(
    tmp_path,
):
    # ESTABLISH
    static_csv_x = _write_csv(
        tmp_path,
        "static.csv",
        "question\n"
        "Have you heard of 'Kegology'?\n"
        "Have you heard the word 'Philosophy'?\n"
        "Do you believe listening is important?\n",
    )
    given_csv_x = _write_csv(
        tmp_path,
        "given.csv",
        "yes/no,question\n"
        "yes,Have you heard of 'Kegology'?\n"
        "no,Have you heard the word 'Philosophy'?\n"
        "yes,Do you believe listening is important?\n",
    )

    # WHEN
    level_complete_x = get_keg_yes_mapping_level(given_csv_x, static_csv_x)

    # THEN
    assert level_complete_x == 1


def test_get_keg_yes_mapping_level_ReturnsObj_Scenario03_ExtraGivenQuestionIgnored(
    tmp_path,
):
    # ESTABLISH
    static_csv_x = _write_csv(
        tmp_path,
        "static.csv",
        "question\n"
        "Have you heard of 'Kegology'?\n"
        "Have you heard the word 'Philosophy'?\n",
    )
    given_csv_x = _write_csv(
        tmp_path,
        "given.csv",
        "yes/no,question\n"
        "yes,Have you heard of 'Kegology'?\n"
        "yes,Have you heard the word 'Philosophy'?\n"
        "yes,Some unrelated question not in static csv?\n",
    )

    # WHEN
    level_complete_x = get_keg_yes_mapping_level(given_csv_x, static_csv_x)

    # THEN
    assert level_complete_x == 2


def test_get_keg_yes_mapping_level_ReturnsObj_Scenario04_EmptyGivenCsv(tmp_path):
    # ESTABLISH
    static_csv_x = _write_csv(
        tmp_path,
        "static.csv",
        "question\n" "Have you heard of 'Kegology'?\n",
    )
    given_csv_x = _write_csv(tmp_path, "given.csv", "yes/no,question\n")

    # WHEN
    level_complete_x = get_keg_yes_mapping_level(given_csv_x, static_csv_x)

    # THEN
    assert level_complete_x == 0


def test_get_keg_yes_mapping_level_ReturnsObj_Scenario05_CaseInsensitiveYes(tmp_path):
    # ESTABLISH
    static_csv_x = _write_csv(
        tmp_path,
        "static.csv",
        "question\n" "Have you heard of 'Kegology'?\n",
    )
    given_csv_x = _write_csv(
        tmp_path,
        "given.csv",
        "yes/no,question\n" "YES,Have you heard of 'Kegology'?\n",
    )

    # WHEN
    level_complete_x = get_keg_yes_mapping_level(given_csv_x, static_csv_x)

    # THEN
    assert level_complete_x == 1
