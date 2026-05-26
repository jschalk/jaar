from ch00_py.file_toolbox import open_json, save_json
from ch01_keyword.keyword_class_builder import (
    get_ch_int,
    get_chapter_descs,
    get_keywords_src_config,
    parse_valid_ch_str,
)
from ch97_docs_builder._ref.ch97_path import create_keg_rank_json_path
from ch97_docs_builder.glossary_ranking import (
    QuestionUnit,
    get_ch_sorted_keywords,
    get_exam_fixed_questions,
    get_keg_definition_questionunits,
    get_keg_definitions,
    get_keywords_by_importance,
    get_tiered_questionunits,
    merge_fixed_and_floating_questions,
    rebuild_keg_exam_questions,
    rebuild_keg_rank_json,
    set_did_you_read_orders,
)
from ch99_glossary.ch_keyword import Ch97Keywords as kw
from os.path import exists as os_path_exists


# CUT / EXAM2
def test_tiered_questionunits_ReturnsObj():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    tiered_questionunits = get_tiered_questionunits()
    # THEN
    keywords_src_config = get_keywords_src_config()
    keywords_set = set(keywords_src_config.keys())
    for keg_term, keg_qu in tiered_questionunits.items():
        # check chxx terms
        if len(keg_term) == 4 and keg_term.startswith("ch"):
            assert keg_qu.question_tier == 6
        # check non ch terms
        if keg_qu.init_ch is None and keg_term in keywords_set:
            print(f"{keg_term=} {keg_qu.init_ch=} {keg_qu.question_tier=}")
            assert keg_qu.question_tier == 10
    # assert 1 == 2
