def set_str_index(
    x_search_str: str, x_lines_list: list, x_matches_list: list, x_locations_dict: dict
) -> None:
    if x_search_str:
        for x_line_num, x_line_str in enumerate(x_lines_list, start=1):
            x_start_index = 0
            while True:
                x_col_index = x_line_str.find(x_search_str, x_start_index)
                if x_col_index == -1:
                    break
                x_matches_list.append((x_line_num, x_col_index + 1))
                x_start_index = x_col_index + 1

    x_locations_dict[x_search_str] = x_matches_list


def get_string_locations_dict(
    markdown_text: str, search_strings: list[str]
) -> dict[str, list[tuple[int, int]]]:
    """
    Locate each search string within a markdown document.

    Args:
        markdown_text: The full contents of the markdown file as a string.
        search_strings: The list of substrings to search for.

    Returns:
        A dict mapping each search string to a list of (line_number, column_number)
        tuples, both 1-indexed, for every occurrence found. A string with no
        occurrences maps to an empty list. Overlapping occurrences on the same
        line are all captured (search advances by 1 character, not by match length).
    """
    x_locations_dict: dict[str, list[tuple[int, int]]] = {}
    x_lines_list = markdown_text.splitlines()

    for x_search_str in search_strings:
        x_matches_list: list[tuple[int, int]] = []
        set_str_index(x_search_str, x_lines_list, x_matches_list, x_locations_dict)
    return x_locations_dict
