from src._instrument.python_tool import get_json_from_dict
from src._instrument.file import save_file
from src.gift.atom_config import (
    bud_ideaunit_text,
    parent_road_str,
    label_str,
    gogo_want_str,
    real_id_str,
    owner_id_str,
    column_order_str,
    bud_idea_healerhold_text,
)
from src.stone.formatbuilder import create_categorys_stone_format_dict
from src.stone.stone import (
    atom_categorys_str,
    attributes_str,
    sort_order_str,
    get_stone_formats_dir,
)


def test_create_categorys_stone_format_dicts_ReturnObj():
    # ESTABLISH / WHEN
    categorys_stone_format_dict = create_categorys_stone_format_dict()
    # print(f"{categorys_stone_format_dict=}")

    # THEN
    assert len(categorys_stone_format_dict) == 10
    bud_ideaunit_filename = f"stone_format_00028_{bud_ideaunit_text()}_v0_0_0.json"
    assert categorys_stone_format_dict.get(bud_ideaunit_filename)
    bud_ideaunit_dict = categorys_stone_format_dict.get(bud_ideaunit_filename)
    assert bud_ideaunit_dict.get(atom_categorys_str()) == [bud_ideaunit_text()]
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

    # healer_filename = "stone_format_00025_bud_idea_healerhold_v0_0_0.json"
    # healer_hold_dict = create_categorys_stone_format_dict().get(healer_filename)
    # print(f"{healer_hold_dict=}")
    # stone_json = get_json_from_dict(healer_hold_dict)
    # save_file(get_stone_formats_dir(), healer_filename, stone_json)

    # for x_filename, stone_format_dict in create_categorys_stone_format_dict().items():
    #     stone_json = get_json_from_dict(stone_format_dict)
    #     save_file(get_stone_formats_dir(), x_filename, stone_json)
