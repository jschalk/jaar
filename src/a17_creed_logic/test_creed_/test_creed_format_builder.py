from src.a00_data_toolbox.file_toolbox import save_json
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import (
    bud_itemunit_str,
    item_way_str,
    gogo_want_str,
)
from src.a08_bud_atom_logic.atom_config import get_atom_config_args
from src.a17_creed_logic._utils.str_a17 import attributes_str, dimens_str
from src.a17_creed_logic.creed_config import (
    get_creed_formats_dir,
    get_creed_config_dict,
)
from src.a06_bud_logic._utils.str_a06 import bud_itemunit_str


def create_dimens_creed_format_dict() -> dict:
    creed_format_files_dict = {}
    x_count = 20
    for creed_dimen, dimen_dict in get_creed_config_dict().items():
        if dimen_dict.get("creed_category") == "bud":
            creed_filename = f"creed_format_{x_count:05}_{creed_dimen}_v0_0_0.json"
            attributes_set = {fisc_tag_str(), owner_name_str()}
            args_dict = get_atom_config_args(creed_dimen)
            attributes_set.update(set(args_dict.keys()))

            creed_format = {"dimens": [creed_dimen], "attributes": attributes_set}
            creed_format_files_dict[creed_filename] = creed_format
            x_count += 1
    return creed_format_files_dict


def test_create_dimens_creed_format_dict_ReturnObj(rebuild_bool):
    # ESTABLISH / WHEN
    dimens_creed_format_dict = create_dimens_creed_format_dict()
    print(f"{dimens_creed_format_dict.keys()=}")

    # THEN
    assert len(dimens_creed_format_dict) == 10
    bud_itemunit_filename = f"creed_format_00028_{bud_itemunit_str()}_v0_0_0.json"
    assert dimens_creed_format_dict.get(bud_itemunit_filename)
    bud_itemunit_dict = dimens_creed_format_dict.get(bud_itemunit_filename)
    assert bud_itemunit_dict.get(dimens_str()) == [bud_itemunit_str()]
    assert bud_itemunit_dict.get(attributes_str())
    bud_itemunit_attributes = bud_itemunit_dict.get(attributes_str())
    assert fisc_tag_str() in bud_itemunit_attributes
    assert owner_name_str() in bud_itemunit_attributes
    assert item_way_str() in bud_itemunit_attributes
    assert gogo_want_str() in bud_itemunit_attributes

    rebuild_format_jsons(rebuild_bool)


def rebuild_format_jsons(x_rebuild_format_jsons: bool):
    if x_rebuild_format_jsons:
        for x_filename, creed_format in create_dimens_creed_format_dict().items():
            save_json(get_creed_formats_dir(), x_filename, creed_format)
