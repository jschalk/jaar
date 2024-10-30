from src.f00_instrument.dict_tool import get_json_from_dict
from src.f00_instrument.file import save_file
from src.f02_bud.bud_tool import bud_itemunit_str
from src.f04_gift.atom_config import (
    parent_road_str,
    label_str,
    gogo_want_str,
    fiscal_id_str,
    owner_id_str,
    column_order_str,
)
from src.f09_brick.formatbuilder import create_categorys_brick_format_dict
from src.f09_brick.brick import categorys_str, attributes_str, sort_order_str
from src.f09_brick.brick_config import get_brick_formats_dir


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
    assert bud_itemunit_attributes.get(fiscal_id_str())
    assert bud_itemunit_attributes.get(owner_id_str())
    fiscal_id_dict = bud_itemunit_attributes.get(fiscal_id_str())
    owner_id_dict = bud_itemunit_attributes.get(owner_id_str())
    assert fiscal_id_dict == {column_order_str(): 0, sort_order_str(): 0}
    assert owner_id_dict == {column_order_str(): 1, sort_order_str(): 1}

    assert bud_itemunit_attributes.get(parent_road_str())
    assert bud_itemunit_attributes.get(label_str())
    assert bud_itemunit_attributes.get(gogo_want_str())
    parent_road_dict = bud_itemunit_attributes.get(parent_road_str())
    label_dict = bud_itemunit_attributes.get(label_str())
    gogo_want_dict = bud_itemunit_attributes.get(gogo_want_str())
    assert gogo_want_dict == {column_order_str(): 13}

    assert parent_road_dict == {column_order_str(): 2, sort_order_str(): 2}
    assert label_dict == {column_order_str(): 3, sort_order_str(): 3}
    rebuild_format_jsons(rebuild_bool)
    # assert 1 == 2


def rebuild_format_jsons(x_rebuild_format_jsons: bool):
    if x_rebuild_format_jsons:
        for x_filename, brick_format in create_categorys_brick_format_dict().items():
            brick_json = get_json_from_dict(brick_format)
            save_file(get_brick_formats_dir(), x_filename, brick_json)
