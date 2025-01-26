from src.f00_instrument.dict_toolbox import get_json_from_dict
from src.f00_instrument.file import save_file
from src.f02_bud.bud_tool import bud_itemunit_str
from src.f04_gift.atom_config import (
    parent_road_str,
    item_title_str,
    gogo_want_str,
    fiscal_title_str,
    owner_name_str,
    get_atom_config_args,
)
from src.f09_idea.idea_config import (
    get_idea_formats_dir,
    get_idea_config_dict,
    dimens_str,
    attributes_str,
)


def create_dimens_idea_format_dict() -> dict:
    idea_format_files_dict = {}
    x_count = 20
    for idea_dimen, dimen_dict in get_idea_config_dict().items():
        if dimen_dict.get("idea_type") == "budunit":
            idea_filename = f"idea_format_{x_count:05}_{idea_dimen}_v0_0_0.json"
            attributes_set = {fiscal_title_str(), owner_name_str()}
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
    bud_itemunit_filename = f"idea_format_00028_{bud_itemunit_str()}_v0_0_0.json"
    assert dimens_idea_format_dict.get(bud_itemunit_filename)
    bud_itemunit_dict = dimens_idea_format_dict.get(bud_itemunit_filename)
    assert bud_itemunit_dict.get(dimens_str()) == [bud_itemunit_str()]
    assert bud_itemunit_dict.get(attributes_str())
    bud_itemunit_attributes = bud_itemunit_dict.get(attributes_str())
    assert fiscal_title_str() in bud_itemunit_attributes
    assert owner_name_str() in bud_itemunit_attributes
    assert parent_road_str() in bud_itemunit_attributes
    assert item_title_str() in bud_itemunit_attributes
    assert gogo_want_str() in bud_itemunit_attributes

    rebuild_format_jsons(rebuild_bool)


def rebuild_format_jsons(x_rebuild_format_jsons: bool):
    if x_rebuild_format_jsons:
        for x_filename, idea_format in create_dimens_idea_format_dict().items():
            idea_json = get_json_from_dict(idea_format)
            save_file(get_idea_formats_dir(), x_filename, idea_json)
