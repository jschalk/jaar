from src._instrument.python_tool import get_json_from_dict
from src._instrument.file import save_file
from src.bud.bud_tool import bud_ideaunit_str
from src.change.atom_config import (
    parent_road_str,
    label_str,
    gogo_want_str,
    real_id_str,
    owner_id_str,
    column_order_str,
)
from src.stone.formatbuilder import create_categorys_stone_format_dict
from src.stone.stone import (
    atom_categorys_str,
    attributes_str,
    sort_order_str,
    get_stone_formats_dir,
)


def test_create_categorys_stone_format_dicts_ReturnObj(rebuild_bool):
    # ESTABLISH / WHEN
    categorys_stone_format_dict = create_categorys_stone_format_dict()
    # print(f"{categorys_stone_format_dict=}")

    # THEN
    assert len(categorys_stone_format_dict) == 10
    bud_ideaunit_filename = f"stone_format_00028_{bud_ideaunit_str()}_v0_0_0.json"
    assert categorys_stone_format_dict.get(bud_ideaunit_filename)
    bud_ideaunit_dict = categorys_stone_format_dict.get(bud_ideaunit_filename)
    assert bud_ideaunit_dict.get(atom_categorys_str()) == [bud_ideaunit_str()]
    assert bud_ideaunit_dict.get(attributes_str())
    bud_ideaunit_attributes = bud_ideaunit_dict.get(attributes_str())
    assert bud_ideaunit_attributes.get(real_id_str())
    assert bud_ideaunit_attributes.get(owner_id_str())
    real_id_dict = bud_ideaunit_attributes.get(real_id_str())
    owner_id_dict = bud_ideaunit_attributes.get(owner_id_str())
    assert real_id_dict == {column_order_str(): 0, sort_order_str(): 0}
    assert owner_id_dict == {column_order_str(): 1, sort_order_str(): 1}

    assert bud_ideaunit_attributes.get(parent_road_str())
    assert bud_ideaunit_attributes.get(label_str())
    assert bud_ideaunit_attributes.get(gogo_want_str())
    parent_road_dict = bud_ideaunit_attributes.get(parent_road_str())
    label_dict = bud_ideaunit_attributes.get(label_str())
    gogo_want_dict = bud_ideaunit_attributes.get(gogo_want_str())
    assert gogo_want_dict == {column_order_str(): 13}

    assert parent_road_dict == {column_order_str(): 2, sort_order_str(): 2}
    assert label_dict == {column_order_str(): 3, sort_order_str(): 3}
    rebuild_format_jsons(rebuild_bool)


def rebuild_format_jsons(x_rebuild_format_jsons: bool):
    if x_rebuild_format_jsons:
        for x_filename, stone_format in create_categorys_stone_format_dict().items():
            stone_json = get_json_from_dict(stone_format)
            save_file(get_stone_formats_dir(), x_filename, stone_json)
