from ch01_keyword.keyword_class_builder import (
    get_keywords_src_config,
    parse_valid_ch_str,
    get_chapter_descs,
    get_ch_int,
)
from ch97_docs_builder.glossary_definition import (
    get_count_keg_terms_by_chapters,
    get_count_strs_by_dirs,
    get_keg_definitions,
)
from ch99_glossary.ch_keyword import Ch97Keywords as kw


def test_get_count_strs_by_dirs_CountsTerms_Scenario0_SingleFile(tmp_path):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "file1.txt").write_text(
        "ContactName BreakTerm ContactName", encoding="utf-8"
    )
    ch_dirs = {1: ch01_dir}
    keg_terms = {"ContactName", "BreakTerm"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 2}, "BreakTerm": {1: 1}}


def test_get_count_strs_by_dirs_CountsAcrossFiles_Scenario1_MultipleFiles(tmp_path):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "file1.txt").write_text("ContactName", encoding="utf-8")
    (ch01_dir / "file2.txt").write_text("ContactName BreakTerm", encoding="utf-8")
    ch_dirs = {1: ch01_dir}
    keg_terms = {"ContactName", "BreakTerm"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 2}, "BreakTerm": {1: 1}}


def test_get_count_strs_by_dirs_CountsByChapter_Scenario2_MultipleChapters(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch02_dir = tmp_path / "ch02"
    ch01_dir.mkdir()
    ch02_dir.mkdir()
    (ch01_dir / "file.txt").write_text("ContactName ContactName", encoding="utf-8")
    (ch02_dir / "file.txt").write_text("ContactName BreakTerm", encoding="utf-8")
    ch_dirs = {1: ch01_dir, 2: ch02_dir}
    keg_terms = {"ContactName", "BreakTerm"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 2, 2: 1}, "BreakTerm": {1: 0, 2: 1}}


def test_get_count_strs_by_dirs_ReturnsZero_Scenario3_TermMissing(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "file.txt").write_text("SomethingElse", encoding="utf-8")
    ch_dirs = {1: ch01_dir}
    keg_terms = {"ContactName"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 0}}


def test_get_count_strs_by_dirs_HandlesNestedFiles_Scenario4_Subdirectories(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    nested_dir = ch01_dir / "nested"

    nested_dir.mkdir(parents=True)
    (nested_dir / "file.txt").write_text("BreakTerm BreakTerm", encoding="utf-8")
    ch_dirs = {1: ch01_dir}
    keg_terms = {"BreakTerm"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"BreakTerm": {1: 2}}


def test_get_count_strs_by_dirs_SkipsBinaryFiles_Scenario5_UnicodeDecodeError(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "valid.txt").write_text("ContactName", encoding="utf-8")
    (ch01_dir / "binary.bin").write_bytes(b"\x80\x81\x82\x83")
    ch_dirs = {1: ch01_dir}
    keg_terms = {"ContactName"}

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {"ContactName": {1: 1}}


def test_get_count_strs_by_dirs_ReturnsEmpty_Scenario6_EmptyKegTerms(
    tmp_path,
):
    # GIVEN
    ch01_dir = tmp_path / "ch01"
    ch01_dir.mkdir()
    (ch01_dir / "file.txt").write_text("ContactName", encoding="utf-8")
    ch_dirs = {1: ch01_dir}
    keg_terms = set()

    # WHEN
    result = get_count_strs_by_dirs(ch_dirs, keg_terms)

    # THEN
    assert result == {}


def test_get_count_keg_terms_by_chapters_CountsTerms_Scenario0_SrcDir():
    # sourcery skip: no-conditionals-in-tests
    # GIVEN / WHEN
    keg_terms_by_chapters = get_count_keg_terms_by_chapters()

    # THEN
    keg_terms = set(get_keg_definitions().keys())
    assert set(keg_terms_by_chapters.keys()) == keg_terms
    # TODO move this to function in glossary_definition.py
    # This part finds all keg_terms used only in one chapter and changes
    # valid_ch from range to single chapter
    chapter_descs = get_chapter_descs().keys()
    ch_ints = {get_ch_int(chapter_desc) for chapter_desc in chapter_descs}
    keywords_src_config = get_keywords_src_config()
    for keg_term in sorted(keg_terms_by_chapters.keys()):
        ch_dir_dict = keg_terms_by_chapters.get(keg_term)
        # if len(ch_dir_dict) == 2:
        if keyword_config := keywords_src_config.get(keg_term):
            if len(ch_dir_dict) > 0:
                lone_ch = list(ch_dir_dict.keys())[0]
                x_valid_ch = keyword_config.get(kw.valid_ch)
                valid_chapters = sorted(parse_valid_ch_str(ch_ints, x_valid_ch))
                if str(lone_ch) != x_valid_ch:
                    # print(f"{set(ch_dir_dict.keys())=}")
                    # print(f"{keg_term} {ch_dir_dict=} {lone_ch=} {x_valid_ch=}")
                    # if len(valid_chapters) - len(ch_dir_dict) > 20:
                    if keg_term == "idea":
                        print(
                            f"{keg_term:<20} {str(sorted(set(ch_dir_dict.keys()))):<40} {valid_chapters[:20]=}"
                        )
                    # print(f"{x_valid_ch=}")
                    keyword_config[kw.valid_ch] = str(lone_ch)
    # src_keywords_src_path = create_src_keywords_src_path(kw.src)
    # save_json(src_keywords_src_path, None, keywords_src_config)
    # assert 1 == 2
    # TODO consider adapting this to ch01
    # TODO consider finding all terms used twice and change keyword src.
    # TODO consider replacing all range with individual listed
    # TODO consider removing 'Only referenced in ch if not single entry
