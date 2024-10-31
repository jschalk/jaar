from src.f01_road.finance_tran import time_id_str
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
from src.f04_gift.atom_config import (
    face_id_str,
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
    get_brickref_dict,
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
    assert brick_number_str() == "brick_number"
    assert allowed_crud_str() == "allowed_crud"
    assert attributes_str() == "attributes"
    assert categorys_str() == "categorys"
    assert get_brick_types() == {budunit_str(), fiscalunit_str(), filterunit_str()}


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
        if brick_dict.get(brick_type_str()) == fiscalunit_str():
            sub_category = fiscal_config_dict.get(brick_category)
        if brick_dict.get(brick_type_str()) == filterunit_str():
            sub_category = filter_config_dict.get(brick_category)

        if brick_category in {
            fiscal_timeline_hour_str(),
            fiscal_timeline_month_str(),
            fiscal_timeline_weekday_str(),
            fiscalunit_str(),
            bridge_explicit_label_str(),
            bridge_otx_to_inx_str(),
        }:
            assert brick_dict.get(allowed_crud_str()) == "INSERT_ONE_TIME"
        elif brick_category in {fiscal_purview_episode_str(), fiscal_cashbook_str()}:
            assert brick_dict.get(allowed_crud_str()) == "INSERT_MULITPLE"
        elif (
            sub_category.get(atom_update()) != None
            and sub_category.get(atom_insert()) != None
            and sub_category.get(atom_delete()) != None
        ):
            assert brick_dict.get(allowed_crud_str()) == "DELETE_INSERT_UPDATE"
        elif (
            sub_category.get(atom_update()) != None
            and sub_category.get(atom_insert()) != None
            and sub_category.get(atom_delete()) is None
        ):
            assert brick_dict.get(allowed_crud_str()) == "INSERT_UPDATE"
        elif (
            sub_category.get(atom_update()) is None
            and sub_category.get(atom_insert()) != None
            and sub_category.get(atom_delete()) != None
        ):
            assert brick_dict.get(allowed_crud_str()) == "DELETE_INSERT"
        elif (
            sub_category.get(atom_update()) != None
            and sub_category.get(atom_insert()) is None
            and sub_category.get(atom_delete()) != None
        ):
            assert brick_dict.get(allowed_crud_str()) == "DELETE_UPDATE"
        elif (
            sub_category.get(atom_update()) != None
            and sub_category.get(atom_insert()) is None
            and sub_category.get(atom_delete()) is None
        ):
            assert brick_dict.get(allowed_crud_str()) == "UPDATE"
        elif (
            sub_category.get(atom_update()) is None
            and sub_category.get(atom_insert()) != None
            and sub_category.get(atom_delete()) is None
        ):
            assert brick_dict.get(allowed_crud_str()) == "INSERT"
        elif (
            sub_category.get(atom_update()) is None
            and sub_category.get(atom_insert()) is None
            and sub_category.get(atom_delete()) != None
        ):
            assert brick_dict.get(allowed_crud_str()) == "DELETE"
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
