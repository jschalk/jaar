from ch40_pop_phil.article_toolbox import get_string_locations_dict
from pathlib import Path


def test_get_string_locations_dict_ReturnsDict_Scenario01_SingleMatchSingleLine():
    # ESTABLISH
    x_markdown_str = "Hello keg world"
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": [(1, 7)]}


def test_get_string_locations_dict_ReturnsDict_Scenario02_MultipleMatchesSameLine():
    # ESTABLISH
    x_markdown_str = "keg keg keg"
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": [(1, 1), (1, 5), (1, 9)]}


def test_get_string_locations_dict_ReturnsDict_Scenario03_MatchesAcrossMultipleLines():
    # ESTABLISH
    x_markdown_str = "# Title\nkeg intro\nsecond keg line\n"
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": [(2, 1), (3, 8)]}


def test_get_string_locations_dict_ReturnsDict_Scenario04_NoMatchFound():
    # ESTABLISH
    x_markdown_str = "This document does not have required word."
    x_search_list = ["missing"]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"missing": []}


def test_get_string_locations_dict_ReturnsDict_Scenario05_EmptySearchStringYieldsNoMatches():
    # ESTABLISH
    x_markdown_str = "Any content here"
    x_search_list = [""]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"": []}


def test_get_string_locations_dict_ReturnsDict_Scenario06_EmptyMarkdownTextYieldsNoMatches():
    # ESTABLISH
    x_markdown_str = ""
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": []}


def test_get_string_locations_dict_ReturnsDict_Scenario07_OverlappingMatchesAreAllCaptured():
    # ESTABLISH
    x_markdown_str = "aaaa"
    x_search_list = ["aa"]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"aa": [(1, 1), (1, 2), (1, 3)]}


def test_get_string_locations_dict_ReturnsDict_Scenario08_SearchIsCaseSensitive():
    # ESTABLISH
    x_markdown_str = "Keg keg KEG"
    x_search_list = ["keg"]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg": [(1, 5)]}


def test_get_string_locations_dict_ReturnsDict_Scenario09_MultipleSearchStringsEachGetOwnEntry():
    # ESTABLISH
    x_markdown_str = "# keg2 Title\nBody text about keg2 and knot.\n"
    x_search_list = ["keg2", "knot", "rope"]

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {
        "keg2": [(1, 3), (2, 17)],
        "knot": [(2, 26)],
        "rope": [],
    }


def test_get_string_locations_dict_ReturnsDict_Scenario10_EmptySearchListYieldsEmptyDict():
    # ESTABLISH
    x_markdown_str = "keg content"
    x_search_list = []

    # WHEN
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {}


def test_get_string_locations_dict_ReturnsDict_Scenario11_MarkdownFileReadFromDisk(
    tmp_path,
):
    # ESTABLISH
    x_markdown_file_path = tmp_path / "sample.md"
    x_markdown_file_path.write_text("# keg2\n\nSee the keg2 docs.\n")
    x_search_list = ["keg2"]

    # WHEN
    x_markdown_str = x_markdown_file_path.read_text()
    x_result_dict = get_string_locations_dict(x_markdown_str, x_search_list)

    # THEN
    assert x_result_dict == {"keg2": [(1, 3), (3, 9)]}


def test_CurrentMarkDownFilesHaveRequiredStrings():
    # GIVEN
    current_ch_dir = Path(__file__).resolve().parent.parent
    author_str = "**Author:**"
    date_str = "**Date:**"
    source_str = "**Source:**"
    copied_str = "**Copied to Keg:**"
    required_strings = [author_str, date_str, source_str, copied_str]

    # WHEN / THEN
    for md_file_path in sorted(current_ch_dir.glob("*.md")):
        content_str = md_file_path.read_text(encoding="utf-8")
        str_loc_dict = get_string_locations_dict(content_str, required_strings)
        for required_str in required_strings:
            assertion_failure_str = f"{md_file_path} is missing {required_str!r}"
            assert str_loc_dict.get(required_str), assertion_failure_str
        author_line = str_loc_dict.get(author_str)[0][0]
        date_line = str_loc_dict.get(date_str)[0][0]
        source_line = str_loc_dict.get(source_str)[0][0]
        copied_line = str_loc_dict.get(copied_str)[0][0]
        assert author_line > date_line, md_file_path
        assert source_line > author_line, md_file_path
        assert copied_line > source_line, md_file_path
