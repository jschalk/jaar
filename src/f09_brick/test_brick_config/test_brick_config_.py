from src.f00_instrument.dict_tool import get_json_from_dict
from src.f00_instrument.file import save_file
from src.f01_road.finance_tran import time_id_str, road_delimiter_str
from src.f02_bud.bud_tool import (
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_item_awardlink_str,
    bud_item_factunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_reason_premiseunit_str,
    bud_item_reasonunit_str,
    bud_itemunit_str,
    budunit_str,
)
from src.f03_chrono.chrono import (
    c400_number_str,
    monthday_distortion_str,
    timeline_label_str,
    yr1_jan1_offset_str,
)
from src.f04_gift.atom_config import (
    face_id_str,
    penny_str,
    respect_bit_str,
    fund_coin_str,
    get_atom_config_dict,
    atom_delete,
    atom_insert,
    atom_update,
    normal_specs_str,
    required_args_str,
    optional_args_str,
    face_id_str,
    fiscal_id_str,
    get_atom_categorys,
)
from src.f07_fiscal.fiscal_config import (
    get_fiscal_config_dict,
    get_fiscal_categorys,
    fiscalunit_str,
    fiscal_purviewlog_str,
    fiscal_purview_episode_str,
    fiscal_cashbook_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
    current_time_str,
)
from src.f08_filter.filter_config import (
    eon_id_str,
    filterunit_str,
    bridge_explicit_label_str,
    bridge_otx_to_inx_str,
    get_filter_categorys,
    get_filter_config_dict,
)
from src.f09_brick.brick_config import (
    brick_type_str,
    get_brick_types,
    brick_number_str,
    allowed_crud_str,
    attributes_str,
    categorys_str,
    insert_one_time_str,
    insert_mulitple_str,
    delete_insert_update_str,
    insert_update_str,
    delete_insert_str,
    delete_update_str,
    build_order_str,
    get_allowed_curds,
    get_brickref_dict,
    get_quick_bricks_column_ref,
    config_file_dir,
    get_brick_config_file_name,
    get_brick_config_dict,
    get_brick_format_filenames,
    get_brick_numbers,
    brick_format_00021_bud_acctunit_v0_0_0,
    brick_format_00020_bud_acct_membership_v0_0_0,
    brick_format_00013_itemunit_v0_0_0,
)
from src.f08_filter.filter_config import get_filter_categorys
from os import getcwd as os_getcwd


def test_str_functions_ReturnObj():
    # ESTABLISH / WHEN / THEN
    assert brick_type_str() == "brick_type"
    assert build_order_str() == "build_order"
    assert brick_number_str() == "brick_number"
    assert allowed_crud_str() == "allowed_crud"
    assert attributes_str() == "attributes"
    assert categorys_str() == "categorys"
    assert insert_one_time_str() == "INSERT_ONE_TIME"
    assert insert_mulitple_str() == "INSERT_MULITPLE"
    assert delete_insert_update_str() == "DELETE_INSERT_UPDATE"
    assert insert_update_str() == "INSERT_UPDATE"
    assert delete_insert_str() == "DELETE_INSERT"
    assert delete_update_str() == "DELETE_UPDATE"

    assert get_brick_types() == {budunit_str(), fiscalunit_str(), filterunit_str()}


def test_get_allowed_curds_ReturnObj():
    # ESTABLISH / WHEN / THEN
    assert get_allowed_curds() == {
        insert_one_time_str(),
        insert_mulitple_str(),
        delete_insert_update_str(),
        insert_update_str(),
        delete_insert_str(),
        delete_update_str(),
        atom_insert(),
        atom_delete(),
        atom_update(),
    }


def test_get_brick_config_file_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_brick_config_file_name() == "brick_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    assert config_file_dir() == f"{os_getcwd()}/src/f09_brick"


def test_get_brick_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    x_brick_config = get_brick_config_dict()

    # THEN
    assert x_brick_config
    brick_config_categorys = set(x_brick_config.keys())
    assert fiscalunit_str() in brick_config_categorys
    assert fiscal_purviewlog_str() not in brick_config_categorys
    assert fiscal_purview_episode_str() in brick_config_categorys
    assert fiscal_cashbook_str() in brick_config_categorys
    assert fiscal_timeline_hour_str() in brick_config_categorys
    assert fiscal_timeline_month_str() in brick_config_categorys
    assert fiscal_timeline_weekday_str() in brick_config_categorys
    assert bud_acct_membership_str() in brick_config_categorys
    assert bud_acctunit_str() in brick_config_categorys
    assert bud_item_awardlink_str() in brick_config_categorys
    assert bud_item_factunit_str() in brick_config_categorys
    assert bud_item_teamlink_str() in brick_config_categorys
    assert bud_item_healerlink_str() in brick_config_categorys
    assert bud_item_reason_premiseunit_str() in brick_config_categorys
    assert bud_item_reasonunit_str() in brick_config_categorys
    assert bud_itemunit_str() in brick_config_categorys
    assert budunit_str() in brick_config_categorys
    assert bridge_explicit_label_str() in brick_config_categorys
    assert bridge_otx_to_inx_str() in brick_config_categorys
    assert get_atom_categorys().issubset(brick_config_categorys)
    assert get_fiscal_categorys().issubset(brick_config_categorys)
    assert get_filter_categorys().issubset(brick_config_categorys)
    assert len(x_brick_config) == 18
    _validate_brick_config(x_brick_config)


def _validate_brick_config(x_brick_config: dict):
    atom_config_dict = get_atom_config_dict()
    fiscal_config_dict = get_fiscal_config_dict()
    filter_config_dict = get_filter_config_dict()
    # for every brick_format file there exists a unique brick_number always with leading zeros to make 5 digits
    for brick_category, brick_dict in x_brick_config.items():
        print(f"{brick_category=}")
        assert brick_dict.get(brick_type_str()) in get_brick_types()
        assert brick_dict.get(required_args_str()) is not None
        assert brick_dict.get(optional_args_str()) is not None
        assert brick_dict.get(allowed_crud_str()) is not None
        assert brick_dict.get(atom_update()) is None
        assert brick_dict.get(atom_insert()) is None
        assert brick_dict.get(atom_delete()) is None
        assert brick_dict.get(normal_specs_str()) is None
        if brick_dict.get(brick_type_str()) == budunit_str():
            sub_category = atom_config_dict.get(brick_category)
        elif brick_dict.get(brick_type_str()) == fiscalunit_str():
            sub_category = fiscal_config_dict.get(brick_category)
        elif brick_dict.get(brick_type_str()) == filterunit_str():
            sub_category = filter_config_dict.get(brick_category)

        assert brick_dict.get(allowed_crud_str()) in get_allowed_curds()

        if brick_category in {
            fiscal_timeline_hour_str(),
            fiscal_timeline_month_str(),
            fiscal_timeline_weekday_str(),
            fiscalunit_str(),
            bridge_explicit_label_str(),
            bridge_otx_to_inx_str(),
        }:
            assert brick_dict.get(allowed_crud_str()) == insert_one_time_str()
        elif brick_category in {fiscal_purview_episode_str(), fiscal_cashbook_str()}:
            assert brick_dict.get(allowed_crud_str()) == insert_mulitple_str()
        elif (
            sub_category.get(atom_update()) != None
            and sub_category.get(atom_insert()) != None
            and sub_category.get(atom_delete()) != None
        ):
            assert brick_dict.get(allowed_crud_str()) == delete_insert_update_str()
        elif (
            sub_category.get(atom_update()) != None
            and sub_category.get(atom_insert()) != None
            and sub_category.get(atom_delete()) is None
        ):
            assert brick_dict.get(allowed_crud_str()) == insert_update_str()
        elif (
            sub_category.get(atom_update()) is None
            and sub_category.get(atom_insert()) != None
            and sub_category.get(atom_delete()) != None
        ):
            assert brick_dict.get(allowed_crud_str()) == delete_insert_str()
        elif (
            sub_category.get(atom_update()) != None
            and sub_category.get(atom_insert()) is None
            and sub_category.get(atom_delete()) != None
        ):
            assert brick_dict.get(allowed_crud_str()) == delete_update_str()
        elif (
            sub_category.get(atom_update()) != None
            and sub_category.get(atom_insert()) is None
            and sub_category.get(atom_delete()) is None
        ):
            assert brick_dict.get(allowed_crud_str()) == atom_update()
        elif (
            sub_category.get(atom_update()) is None
            and sub_category.get(atom_insert()) != None
            and sub_category.get(atom_delete()) is None
        ):
            assert brick_dict.get(allowed_crud_str()) == atom_insert()
        elif (
            sub_category.get(atom_update()) is None
            and sub_category.get(atom_insert()) is None
            and sub_category.get(atom_delete()) != None
        ):
            assert brick_dict.get(allowed_crud_str()) == atom_delete()
        else:
            test_str = f"{allowed_crud_str()} not checked by test"
            assert brick_dict.get(allowed_crud_str()) == test_str

        sub_required_args_keys = set(sub_category.get(required_args_str()).keys())
        brick_required_args_keys = set(brick_dict.get(required_args_str()).keys())
        # print(f"  {sub_required_args_keys=}")
        # print(f"{brick_required_args_keys=}")
        assert sub_required_args_keys.issubset(brick_required_args_keys)

        sub_optional_args_keys = set(sub_category.get(optional_args_str()).keys())
        if fiscal_id_str() in sub_optional_args_keys:
            sub_optional_args_keys.remove(fiscal_id_str())

        brick_optional_args_keys = set(brick_dict.get(optional_args_str()).keys())
        # print(f"  {sub_optional_args_keys=}")
        # print(f"{brick_optional_args_keys=}")
        assert sub_optional_args_keys.issubset(brick_optional_args_keys)

        assert face_id_str() in brick_required_args_keys
        assert eon_id_str() in brick_required_args_keys
        assert fiscal_id_str() not in brick_optional_args_keys
        if brick_dict.get(brick_type_str()) != filterunit_str():
            assert fiscal_id_str() in brick_required_args_keys
            assert time_id_str() in brick_required_args_keys


def test_get_brick_format_filenames_ReturnsObj():
    # ESTABLISH
    brick_filenames = get_brick_format_filenames()

    # THEN
    print(f"{brick_filenames=}")
    print("")
    assert brick_format_00021_bud_acctunit_v0_0_0() in brick_filenames
    assert brick_format_00020_bud_acct_membership_v0_0_0() in brick_filenames
    assert brick_format_00013_itemunit_v0_0_0() in brick_filenames

    # WHEN / THEN
    assert _validate_brick_format_files(brick_filenames)
    # assert 1 == 2


def _validate_brick_format_files(brick_filenames: set[str]):
    valid_brick_categorys = set()
    valid_brick_categorys.update(get_atom_categorys())
    valid_brick_categorys.update(get_fiscal_categorys())
    valid_brick_categorys.update(get_filter_categorys())

    # for every brick_format file there exists a unique brick_number always with leading zeros to make 5 digits
    brick_numbers_set = set()
    for brick_filename in brick_filenames:
        brickref_dict = get_brickref_dict(brick_filename)
        print(f"{brick_filename=} {brickref_dict.get(brick_number_str())=}")
        brick_number_value = brickref_dict.get(brick_number_str())
        assert brick_number_value
        assert brick_number_value[2:8] == brick_filename[13:18]
        brick_numbers_set.add(brick_number_value)

        brick_format_categorys = brickref_dict.get(categorys_str())
        assert brick_format_categorys is not None
        assert len(brick_format_categorys) > 0
        for brick_format_category in brick_format_categorys:
            assert brick_format_category in valid_brick_categorys
            print(f"{brick_format_category=}")

        assert brickref_dict.get(attributes_str()) is not None
        brick_format_attributes = brickref_dict.get(attributes_str()).keys()
        # assert fiscal_id_str() in brick_format_attributes
        # assert face_id_str() in brick_format_attributes
        # assert eon_id_str() in brick_format_attributes
        # for brick_format_attribute in brick_format_attributes:
        #     print(f"{brick_format_attribute=}")

    # confirm every bricknumber is unique
    assert len(brick_numbers_set) == len(brick_filenames)
    assert brick_numbers_set == get_brick_numbers()

    return True


def set_brick_config_json(category: str, build_order: int):
    x_brick_config = get_brick_config_dict()
    category_dict = x_brick_config.get(category)
    category_dict[build_order_str()] = build_order
    x_brick_config[category] = category_dict
    x_file_str = get_json_from_dict(x_brick_config)
    save_file(config_file_dir(), get_brick_config_file_name(), x_file_str)


def test_get_brick_config_dict_ReturnsObj_build_order():
    # ESTABLISH / WHEN
    bo = build_order_str()
    # set_brick_config_json(bridge_otx_to_inx_str(), 0)
    # set_brick_config_json(bridge_explicit_label_str(), 1)
    # set_brick_config_json(fiscalunit_str(), 2)
    # set_brick_config_json(fiscal_timeline_hour_str(), 3)
    # set_brick_config_json(fiscal_timeline_month_str(), 4)
    # set_brick_config_json(fiscal_timeline_weekday_str(), 5)
    # set_brick_config_json(bud_acct_membership_str(), 6)
    # set_brick_config_json(bud_acctunit_str(), 7)
    # set_brick_config_json(bud_item_awardlink_str(), 8)
    # set_brick_config_json(bud_item_factunit_str(), 9)
    # set_brick_config_json(bud_item_teamlink_str(), 10)
    # set_brick_config_json(bud_item_healerlink_str(), 11)
    # set_brick_config_json(bud_item_reason_premiseunit_str(), 12)
    # set_brick_config_json(bud_item_reasonunit_str(), 14)
    # set_brick_config_json(bud_itemunit_str(), 15)
    # set_brick_config_json(budunit_str(), 16)
    # set_brick_config_json(fiscal_purview_episode_str(), 17)
    # set_brick_config_json(fiscal_cashbook_str(), 18)
    x_brick_config = get_brick_config_dict()

    # THEN
    assert x_brick_config.get(bridge_otx_to_inx_str()).get(bo) == 0
    assert x_brick_config.get(bridge_explicit_label_str()).get(bo) == 1
    assert x_brick_config.get(fiscalunit_str()).get(bo) == 2
    assert x_brick_config.get(fiscal_timeline_hour_str()).get(bo) == 3
    assert x_brick_config.get(fiscal_timeline_month_str()).get(bo) == 4
    assert x_brick_config.get(fiscal_timeline_weekday_str()).get(bo) == 5
    assert x_brick_config.get(bud_acct_membership_str()).get(bo) == 6
    assert x_brick_config.get(bud_acctunit_str()).get(bo) == 7
    assert x_brick_config.get(bud_item_awardlink_str()).get(bo) == 8
    assert x_brick_config.get(bud_item_factunit_str()).get(bo) == 9
    assert x_brick_config.get(bud_item_teamlink_str()).get(bo) == 10
    assert x_brick_config.get(bud_item_healerlink_str()).get(bo) == 11
    assert x_brick_config.get(bud_item_reason_premiseunit_str()).get(bo) == 12
    assert x_brick_config.get(bud_item_reasonunit_str()).get(bo) == 14
    assert x_brick_config.get(bud_itemunit_str()).get(bo) == 15
    assert x_brick_config.get(budunit_str()).get(bo) == 16
    assert x_brick_config.get(fiscal_purview_episode_str()).get(bo) == 17
    assert x_brick_config.get(fiscal_cashbook_str()).get(bo) == 18


def test_get_quick_bricks_column_ref_ReturnsObj():
    # ESTABLISH / WHEN
    x_brick_quick_column_ref = get_quick_bricks_column_ref()

    # THEN
    assert len(x_brick_quick_column_ref) == len(get_brick_numbers())
    assert x_brick_quick_column_ref.get("br00000") == {
        face_id_str(),
        eon_id_str(),
        c400_number_str(),
        current_time_str(),
        fiscal_id_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        road_delimiter_str(),
        timeline_label_str(),
        yr1_jan1_offset_str(),
    }
