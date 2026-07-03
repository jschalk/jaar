from csv import DictReader as csv_DictReader


def get_keg_yes_mapping_level(given_csv_path: str, static_csv_path: str) -> int:
    with open(static_csv_path, newline="", encoding="utf-8") as static_csv_x:
        static_questions_x = [
            row_x["question"].strip()
            for row_x in csv_DictReader(static_csv_x)
            if row_x["question"].strip() != ""
        ]

    with open(given_csv_path, newline="", encoding="utf-8") as given_csv_x:
        given_reader_x = csv_DictReader(given_csv_x)
        given_reader_x.fieldnames = [
            fieldname_x.strip() for fieldname_x in given_reader_x.fieldnames
        ]
        given_yes_questions_x = {
            row_x["question"].strip()
            for row_x in given_reader_x
            if row_x["question"].strip() != ""
            and row_x["yes/no"].strip().lower() == "yes"
        }

    level_complete_x = 0
    for question_x in static_questions_x:
        if question_x not in given_yes_questions_x:
            break
        level_complete_x += 1

    return level_complete_x
