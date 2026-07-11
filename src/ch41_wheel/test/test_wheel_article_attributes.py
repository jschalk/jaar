from ch40_pop_phil.article_toolbox import get_string_locations_dict
from pathlib import Path


def test_CurrentWheelMarkDownFilesHaveRequiredStrings():
    # GIVEN
    current_ch_dir = Path(__file__).resolve().parent.parent
    author_str = "**Author:**"
    date_str = "**Date:**"
    required_strings = [author_str, date_str]

    # WHEN / THEN
    for md_file_path in sorted(current_ch_dir.glob("*.md")):
        content_str = md_file_path.read_text(encoding="utf-8")
        str_loc_dict = get_string_locations_dict(content_str, required_strings)
        for required_str in required_strings:
            assertion_failure_str = f"{md_file_path} is missing {required_str!r}"
            assert str_loc_dict.get(required_str), assertion_failure_str
        author_line = str_loc_dict.get(author_str)[0][0]
        date_line = str_loc_dict.get(date_str)[0][0]
        assert author_line > date_line, md_file_path
