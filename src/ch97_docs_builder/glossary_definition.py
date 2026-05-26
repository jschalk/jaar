from ch00_py.chapter_desc_main import get_chapter_desc_prefix, get_chapter_descs
from ch00_py.file_toolbox import open_json, save_json
from ch00_py.keyword_class_builder import (
    get_chapter_descs,
    get_keywords_src_config,
    parse_valid_ch_str,
)
from ch08_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_config_dict,
)
from ch97_docs_builder._ref.ch97_path import (
    create_chapter_ref_path,
    create_src_keg_definitions_path,
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
