from src.a00_data_toolbox.file_toolbox import save_json
from src.a02_finance_logic._test_util.a02_str import owner_name_str, fisc_label_str
from src.a06_bud_logic._test_util.a06_str import bud_conceptunit_str
from src.a06_bud_logic._test_util.a06_str import (
    bud_conceptunit_str,
    concept_way_str,
    gogo_want_str,
)
from src.a08_bud_atom_logic.atom_config import get_atom_config_args
from src.a17_idea_logic._test_util.a17_str import attributes_str, dimens_str
from src.a17_idea_logic.idea_config import (
    get_idea_formats_dir,
    get_idea_config_dict,
)


def create_dimens_idea_format_dict() -> dict:
    idea_format_files_dict = {}
    x_count = 20
    for idea_dimen, dimen_dict in get_idea_config_dict().items():
        if dimen_dict.get("idea_category") == "bud":
            idea_filename = f"idea_format_{x_count:05}_{idea_dimen}_v0_0_0.json"
            attributes_set = {fisc_label_str(), owner_name_str()}
            args_dict = get_atom_config_args(idea_dimen)
            attributes_set.update(set(args_dict.keys()))

            idea_format = {"dimens": [idea_dimen], "attributes": attributes_set}
            idea_format_files_dict[idea_filename] = idea_format
            x_count += 1
    return idea_format_files_dict


def test_create_dimens_idea_format_dict_ReturnObj(rebuild_bool):
    # ESTABLISH / WHEN
    dimens_idea_format_dict = create_dimens_idea_format_dict()
    print(f"{dimens_idea_format_dict.keys()=}")

    # THEN
    assert len(dimens_idea_format_dict) == 10
    bud_conceptunit_filename = f"idea_format_00028_{bud_conceptunit_str()}_v0_0_0.json"
    assert dimens_idea_format_dict.get(bud_conceptunit_filename)
    bud_conceptunit_dict = dimens_idea_format_dict.get(bud_conceptunit_filename)
    assert bud_conceptunit_dict.get(dimens_str()) == [bud_conceptunit_str()]
    assert bud_conceptunit_dict.get(attributes_str())
    bud_conceptunit_attributes = bud_conceptunit_dict.get(attributes_str())
    assert fisc_label_str() in bud_conceptunit_attributes
    assert owner_name_str() in bud_conceptunit_attributes
    assert concept_way_str() in bud_conceptunit_attributes
    assert gogo_want_str() in bud_conceptunit_attributes

    rebuild_format_jsons(rebuild_bool)


def rebuild_format_jsons(x_rebuild_format_jsons: bool):
    if x_rebuild_format_jsons:
        for x_filename, idea_format in create_dimens_idea_format_dict().items():
            save_json(get_idea_formats_dir(), x_filename, idea_format)
