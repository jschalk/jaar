from src.f00_instrument.dict_toolbox import get_json_from_dict
from src.f00_instrument.file import save_file
from src.f02_bud.bud_tool import bud_itemunit_str
from src.f04_gift.atom_config import (
    parent_road_str,
    label_str,
    gogo_want_str,
    deal_id_str,
    owner_id_str,
    get_atom_config_args,
)
from src.f09_brick.brick_config import (
    get_brick_formats_dir,
    get_brick_config_dict,
    categorys_str,
    attributes_str,
)


def create_categorys_brick_format_dict() -> dict:
    brick_format_files_dict = {}
    x_count = 20
    for brick_category, category_dict in get_brick_config_dict().items():
        if category_dict.get("brick_type") == "budunit":
            brick_filename = f"brick_format_{x_count:05}_{brick_category}_v0_0_0.json"
            attributes_set = {deal_id_str(), owner_id_str()}
            args_dict = get_atom_config_args(brick_category)
            attributes_set.update(set(args_dict.keys()))

            brick_format = {"categorys": [brick_category], "attributes": attributes_set}
            brick_format_files_dict[brick_filename] = brick_format
            x_count += 1
    return brick_format_files_dict


def test_create_categorys_brick_format_dict_ReturnObj(rebuild_bool):
    # ESTABLISH / WHEN
    categorys_brick_format_dict = create_categorys_brick_format_dict()
    print(f"{categorys_brick_format_dict.keys()=}")

    # THEN
    assert len(categorys_brick_format_dict) == 10
    bud_itemunit_filename = f"brick_format_00028_{bud_itemunit_str()}_v0_0_0.json"
    assert categorys_brick_format_dict.get(bud_itemunit_filename)
    bud_itemunit_dict = categorys_brick_format_dict.get(bud_itemunit_filename)
    assert bud_itemunit_dict.get(categorys_str()) == [bud_itemunit_str()]
    assert bud_itemunit_dict.get(attributes_str())
    bud_itemunit_attributes = bud_itemunit_dict.get(attributes_str())
    assert deal_id_str() in bud_itemunit_attributes
    assert owner_id_str() in bud_itemunit_attributes
    assert parent_road_str() in bud_itemunit_attributes
    assert label_str() in bud_itemunit_attributes
    assert gogo_want_str() in bud_itemunit_attributes

    rebuild_format_jsons(rebuild_bool)


def rebuild_format_jsons(x_rebuild_format_jsons: bool):
    if x_rebuild_format_jsons:
        for x_filename, brick_format in create_categorys_brick_format_dict().items():
            brick_json = get_json_from_dict(brick_format)
            save_file(get_brick_formats_dir(), x_filename, brick_json)
