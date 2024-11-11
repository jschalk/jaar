from src.f00_instrument.dict_toolbox import get_json_from_dict
from src.f00_instrument.file import save_file
from src.f01_road.finance_tran import quota_str, time_id_str, road_delimiter_str
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
    get_atom_args_category_mapping,
    get_atom_config_dict,
    get_atom_categorys,
    required_args_str,
    optional_args_str,
    normal_specs_str,
    column_order_str,
    atom_delete,
    atom_insert,
    atom_update,
    face_id_str,
    obj_class_str,
    fiscal_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    parent_road_str,
    label_str,
    road_str,
    base_str,
    team_id_str,
    awardee_id_str,
    healer_id_str,
    numor_str,
    denom_str,
    addin_str,
    base_item_active_requisite_str,
    begin_str,
    close_str,
    credit_belief_str,
    debtit_belief_str,
    credit_vote_str,
    debtit_vote_str,
    credor_respect_str,
    debtor_respect_str,
    fopen_str,
    fnigh_str,
    gogo_want_str,
    mass_str,
    morph_str,
    pledge_str,
    stop_want_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
    give_force_str,
    take_force_str,
)

from src.f07_fiscal.fiscal_config import (
    get_fiscal_args_category_mapping,
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
    amount_str,
    month_label_str,
    hour_label_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_label_str,
    weekday_order_str,
)
from src.f08_pidgin.pidgin_config import (
    eon_id_str,
    pidginunit_str,
    otx_road_delimiter_str,
    inx_road_delimiter_str,
    unknown_word_str,
    otx_word_str,
    inx_word_str,
    otx_label_str,
    inx_label_str,
    bridge_explicit_label_str,
    bridge_otx_to_inx_str,
    get_pidgin_categorys,
    get_pidgin_config_dict,
    get_pidgin_args_category_mapping,
)
from src.f09_brick.brick_config import (
    brick_type_str,
    get_brick_types,
    get_brick_elements_sort_order,
    get_brick_sqlite_type,
    brick_number_str,
    allowed_crud_str,
    attributes_str,
    categorys_str,
    otx_key_str,
    insert_one_time_str,
    insert_mulitple_str,
    delete_insert_update_str,
    insert_update_str,
    delete_insert_str,
    delete_update_str,
    build_order_str,
    get_allowed_curds,
    get_brickref_from_file,
    get_quick_bricks_column_ref,
    config_file_dir,
    get_brick_config_file_name,
    get_brick_config_dict,
    get_brick_format_filenames,
    get_brick_format_filename,
    get_brick_numbers,
    brick_format_00021_bud_acctunit_v0_0_0,
    brick_format_00020_bud_acct_membership_v0_0_0,
    brick_format_00013_itemunit_v0_0_0,
)
from os import getcwd as os_getcwd


def test_str_functions_ReturnObj():
    # ESTABLISH / WHEN / THEN
    assert brick_type_str() == "brick_type"
    assert build_order_str() == "build_order"
    assert brick_number_str() == "brick_number"
    assert allowed_crud_str() == "allowed_crud"
    assert attributes_str() == "attributes"
    assert categorys_str() == "categorys"
    assert otx_key_str() == "otx_key"
    assert insert_one_time_str() == "INSERT_ONE_TIME"
    assert insert_mulitple_str() == "INSERT_MULITPLE"
    assert delete_insert_update_str() == "DELETE_INSERT_UPDATE"
    assert insert_update_str() == "INSERT_UPDATE"
    assert delete_insert_str() == "DELETE_INSERT"
    assert delete_update_str() == "DELETE_UPDATE"

    assert get_brick_types() == {budunit_str(), fiscalunit_str(), pidginunit_str()}


def test_get_brick_elements_sort_order_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_brick_elements_sort_order()

    # THEN
    assert table_sorting_priority[0] == face_id_str()
    assert table_sorting_priority[1] == eon_id_str()
    assert table_sorting_priority[2] == fiscal_id_str()
    assert table_sorting_priority[3] == obj_class_str()
    assert table_sorting_priority[4] == owner_id_str()
    assert table_sorting_priority[5] == acct_id_str()
    assert table_sorting_priority[6] == group_id_str()
    assert table_sorting_priority[7] == parent_road_str()
    assert table_sorting_priority[8] == label_str()
    assert table_sorting_priority[9] == road_str()
    assert table_sorting_priority[10] == base_str()
    assert table_sorting_priority[11] == "need"
    assert table_sorting_priority[12] == "pick"
    assert table_sorting_priority[13] == team_id_str()
    assert table_sorting_priority[14] == awardee_id_str()
    assert table_sorting_priority[15] == healer_id_str()
    assert table_sorting_priority[16] == time_id_str()
    assert table_sorting_priority[17] == begin_str()
    assert table_sorting_priority[18] == close_str()
    assert table_sorting_priority[19] == addin_str()
    assert table_sorting_priority[20] == numor_str()
    assert table_sorting_priority[21] == denom_str()
    assert table_sorting_priority[22] == morph_str()
    assert table_sorting_priority[23] == gogo_want_str()
    assert table_sorting_priority[24] == stop_want_str()
    assert table_sorting_priority[25] == base_item_active_requisite_str()
    assert table_sorting_priority[26] == credit_belief_str()
    assert table_sorting_priority[27] == debtit_belief_str()
    assert table_sorting_priority[28] == credit_vote_str()
    assert table_sorting_priority[29] == debtit_vote_str()
    assert table_sorting_priority[30] == credor_respect_str()
    assert table_sorting_priority[31] == debtor_respect_str()
    assert table_sorting_priority[32] == fopen_str()
    assert table_sorting_priority[33] == fnigh_str()
    assert table_sorting_priority[34] == "fund_pool"
    assert table_sorting_priority[35] == give_force_str()
    assert table_sorting_priority[36] == mass_str()
    assert table_sorting_priority[37] == "max_tree_traverse"
    assert table_sorting_priority[38] == "nigh"
    assert table_sorting_priority[39] == "open"
    assert table_sorting_priority[40] == "divisor"
    assert table_sorting_priority[41] == pledge_str()
    assert table_sorting_priority[42] == "problem_bool"
    assert table_sorting_priority[43] == "purview_time_id"
    assert table_sorting_priority[44] == take_force_str()
    assert table_sorting_priority[45] == "tally"
    assert table_sorting_priority[46] == fund_coin_str()
    assert table_sorting_priority[47] == penny_str()
    assert table_sorting_priority[48] == respect_bit_str()
    assert table_sorting_priority[49] == current_time_str()
    assert table_sorting_priority[50] == amount_str()
    assert table_sorting_priority[51] == month_label_str()
    assert table_sorting_priority[52] == hour_label_str()
    assert table_sorting_priority[53] == cumlative_minute_str()
    assert table_sorting_priority[54] == cumlative_day_str()
    assert table_sorting_priority[55] == weekday_label_str()
    assert table_sorting_priority[56] == weekday_order_str()
    assert table_sorting_priority[57] == otx_road_delimiter_str()
    assert table_sorting_priority[58] == inx_road_delimiter_str()
    assert table_sorting_priority[59] == unknown_word_str()
    assert table_sorting_priority[60] == otx_word_str()
    assert table_sorting_priority[61] == inx_word_str()
    assert table_sorting_priority[62] == otx_label_str()
    assert table_sorting_priority[63] == inx_label_str()
    assert table_sorting_priority[64] == road_delimiter_str()
    assert table_sorting_priority[65] == c400_number_str()
    assert table_sorting_priority[66] == yr1_jan1_offset_str()
    assert table_sorting_priority[67] == quota_str()
    assert table_sorting_priority[68] == monthday_distortion_str()
    assert table_sorting_priority[69] == timeline_label_str()
    assert len(table_sorting_priority) == 70
    atom_args = set(get_atom_args_category_mapping().keys())
    assert atom_args.issubset(set(table_sorting_priority))
    fiscal_args = set(get_fiscal_args_category_mapping().keys())
    print(f"{fiscal_args=}")
    print(f"{fiscal_args.difference(set(table_sorting_priority))=}")
    assert fiscal_args.issubset(set(table_sorting_priority))
    pidgin_args = set(get_pidgin_args_category_mapping().keys())
    assert pidgin_args.issubset(set(table_sorting_priority))
    atom_fiscal_pidgin_args = atom_args
    atom_fiscal_pidgin_args.update(fiscal_args)
    atom_fiscal_pidgin_args.update(pidgin_args)
    table_sorting_priority.remove(eon_id_str())
    table_sorting_priority.remove(face_id_str())
    table_sorting_priority.remove(obj_class_str())
    assert atom_fiscal_pidgin_args == set(table_sorting_priority)


def test_get_brick_sqlite_type_ReturnsObj():
    # ESTABLISH / WHEN
    sqlite_types = get_brick_sqlite_type()

    # THEN
    assert set(sqlite_types.keys()) == set(get_brick_elements_sort_order())
    assert sqlite_types.get(face_id_str()) == "TEXT"
    assert sqlite_types.get(eon_id_str()) == "INTEGER"
    assert sqlite_types.get(fiscal_id_str()) == "TEXT"
    assert sqlite_types.get(obj_class_str()) == "TEXT"
    assert sqlite_types.get(owner_id_str()) == "TEXT"
    assert sqlite_types.get(acct_id_str()) == "TEXT"
    assert sqlite_types.get(group_id_str()) == "TEXT"
    assert sqlite_types.get(parent_road_str()) == "TEXT"
    assert sqlite_types.get(label_str()) == "TEXT"
    assert sqlite_types.get(road_str()) == "TEXT"
    assert sqlite_types.get(base_str()) == "TEXT"
    assert sqlite_types.get("need") == "TEXT"
    assert sqlite_types.get("pick") == "TEXT"
    assert sqlite_types.get(team_id_str()) == "TEXT"
    assert sqlite_types.get(awardee_id_str()) == "TEXT"
    assert sqlite_types.get(healer_id_str()) == "TEXT"
    assert sqlite_types.get(time_id_str()) == "INTEGER"
    assert sqlite_types.get(begin_str()) == "REAL"
    assert sqlite_types.get(close_str()) == "REAL"
    assert sqlite_types.get(addin_str()) == "REAL"
    assert sqlite_types.get(numor_str()) == "REAL"
    assert sqlite_types.get(denom_str()) == "REAL"
    assert sqlite_types.get(morph_str()) == "INTEGER"
    assert sqlite_types.get(gogo_want_str()) == "REAL"
    assert sqlite_types.get(stop_want_str()) == "REAL"
    assert sqlite_types.get(base_item_active_requisite_str()) == "TEXT"
    assert sqlite_types.get(credit_belief_str()) == "REAL"
    assert sqlite_types.get(debtit_belief_str()) == "REAL"
    assert sqlite_types.get(credit_vote_str()) == "REAL"
    assert sqlite_types.get(debtit_vote_str()) == "REAL"
    assert sqlite_types.get(credor_respect_str()) == "REAL"
    assert sqlite_types.get(debtor_respect_str()) == "REAL"
    assert sqlite_types.get(fopen_str()) == "REAL"
    assert sqlite_types.get(fnigh_str()) == "REAL"
    assert sqlite_types.get("fund_pool") == "REAL"
    assert sqlite_types.get(give_force_str()) == "REAL"
    assert sqlite_types.get(mass_str()) == "REAL"
    assert sqlite_types.get("max_tree_traverse") == "INTEGER"
    assert sqlite_types.get("nigh") == "REAL"
    assert sqlite_types.get("open") == "REAL"
    assert sqlite_types.get("divisor") == "REAL"
    assert sqlite_types.get(pledge_str()) == "INTEGER"
    assert sqlite_types.get("problem_bool") == "INTEGER"
    assert sqlite_types.get("purview_time_id") == "INTEGER"
    assert sqlite_types.get(take_force_str()) == "REAL"
    assert sqlite_types.get("tally") == "REAL"
    assert sqlite_types.get(fund_coin_str()) == "REAL"
    assert sqlite_types.get(penny_str()) == "REAL"
    assert sqlite_types.get(respect_bit_str()) == "REAL"
    assert sqlite_types.get(current_time_str()) == "INTEGER"
    assert sqlite_types.get(amount_str()) == "REAL"
    assert sqlite_types.get(month_label_str()) == "TEXT"
    assert sqlite_types.get(hour_label_str()) == "TEXT"
    assert sqlite_types.get(cumlative_minute_str()) == "INTEGER"
    assert sqlite_types.get(cumlative_day_str()) == "INTEGER"
    assert sqlite_types.get(weekday_label_str()) == "TEXT"
    assert sqlite_types.get(weekday_order_str()) == "INTEGER"
    assert sqlite_types.get(otx_road_delimiter_str()) == "TEXT"
    assert sqlite_types.get(inx_road_delimiter_str()) == "TEXT"
    assert sqlite_types.get(unknown_word_str()) == "TEXT"
    assert sqlite_types.get(otx_word_str()) == "TEXT"
    assert sqlite_types.get(inx_word_str()) == "TEXT"
    assert sqlite_types.get(otx_label_str()) == "TEXT"
    assert sqlite_types.get(inx_label_str()) == "TEXT"
    assert sqlite_types.get(road_delimiter_str()) == "TEXT"
    assert sqlite_types.get(c400_number_str()) == "INTEGER"
    assert sqlite_types.get(yr1_jan1_offset_str()) == "INTEGER"
    assert sqlite_types.get(quota_str()) == "REAL"
    assert sqlite_types.get(monthday_distortion_str()) == "INTEGER"
    assert sqlite_types.get(timeline_label_str()) == "TEXT"


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
    assert get_pidgin_categorys().issubset(brick_config_categorys)
    assert len(x_brick_config) == 18
    _validate_brick_config(x_brick_config)


def _validate_brick_config(x_brick_config: dict):
    atom_config_dict = get_atom_config_dict()
    fiscal_config_dict = get_fiscal_config_dict()
    pidgin_config_dict = get_pidgin_config_dict()
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
        elif brick_dict.get(brick_type_str()) == pidginunit_str():
            sub_category = pidgin_config_dict.get(brick_category)

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

        brick_optional_args_dict = brick_dict.get(optional_args_str())
        brick_optional_args_keys = set(brick_optional_args_dict.keys())
        # print(f"  {sub_optional_args_keys=}")
        # print(f"{brick_optional_args_keys=}")
        assert sub_optional_args_keys.issubset(brick_optional_args_keys)

        assert face_id_str() in brick_required_args_keys
        assert eon_id_str() in brick_required_args_keys
        assert fiscal_id_str() not in brick_optional_args_keys
        if brick_dict.get(brick_type_str()) != pidginunit_str():
            assert fiscal_id_str() in brick_required_args_keys
            assert time_id_str() in brick_required_args_keys

        # sort_list = get_brick_elements_sort_order()
        # x_count = 0
        # sort_dict1 = {}
        # sort_dict2 = {}
        # for brick_arg in sort_list:
        #     sort_dict1[x_count] = brick_arg
        #     sort_dict1[brick_arg] = x_count

        # for optional_arg in brick_optional_args_keys:
        #     print(f"{optional_arg=} {brick_optional_args_dict=}")
        #     optional_arg_dict = brick_optional_args_dict.get(optional_arg)
        #     optional_arg_column_order = optional_arg_dict.get(column_order_str())
        #     assert optional_arg_column_order != None
        #     list_ref_arg = sort_list[optional_arg_column_order]
        #     assert list_ref_arg != None
        #     assert optional_arg == list_ref_arg

        # # for required_arg in brick_required_args_keys:
        #     print(f"{required_arg=} {brick_required_args_dict=}")
        #     required_arg_dict = brick_required_args_dict.get(required_arg)
        #     required_arg_column_order = required_arg_dict.get(column_order_str())
        #     assert required_arg_column_order != None
        #     list_ref_arg = sort_list[required_arg_column_order]
        #     assert list_ref_arg != None
        #     assert required_arg == list_ref_arg


def test_get_brick_format_filenames_ReturnsObj():
    # ESTABLISH
    brick_filenames_set = get_brick_format_filenames()
    brick_filenames_sorted = list(brick_filenames_set)
    brick_filenames_sorted.sort(key=lambda x: x)
    print(brick_filenames_sorted)

    # THEN
    assert brick_format_00021_bud_acctunit_v0_0_0() in brick_filenames_set
    assert brick_format_00020_bud_acct_membership_v0_0_0() in brick_filenames_set
    assert brick_format_00013_itemunit_v0_0_0() in brick_filenames_set

    # WHEN / THEN
    assert _validate_brick_format_files(brick_filenames_sorted)


def _validate_brick_format_files(brick_filenames: set[str]):
    valid_brick_categorys = set()
    valid_brick_categorys.update(get_atom_categorys())
    valid_brick_categorys.update(get_fiscal_categorys())
    valid_brick_categorys.update(get_pidgin_categorys())
    config_dict = get_brick_config_dict()

    # for every brick_format file there exists a unique brick_number always with leading zeros to make 5 digits
    brick_numbers_set = set()
    for brick_filename in brick_filenames:
        ref_dict = get_brickref_from_file(brick_filename)
        print(f"{brick_filename=} {ref_dict.get(brick_number_str())=}")
        brick_number_value = ref_dict.get(brick_number_str())
        assert brick_number_value
        assert brick_number_value[2:8] == brick_filename[13:18]
        brick_numbers_set.add(brick_number_value)

        format_cats = ref_dict.get(categorys_str())
        assert format_cats is not None
        assert len(format_cats) > 0
        for brick_format_category in format_cats:
            assert brick_format_category in valid_brick_categorys

        assert ref_dict.get(attributes_str()) is not None
        brick_format_attributes = ref_dict.get(attributes_str())
        for brick_attribute, attr_dict in brick_format_attributes.items():
            assert otx_key_str() in set(attr_dict.keys())
            otx_key_value = attr_dict.get(otx_key_str())
            for brick_format_category in format_cats:
                format_config = config_dict.get(brick_format_category)
                cat_required_keys = set(format_config.get(required_args_str()).keys())
                cat_optional_keys = set(format_config.get(optional_args_str()).keys())
                attr_in_required = brick_attribute in cat_required_keys
                attr_in_optional = brick_attribute in cat_optional_keys
                attr_in_keys = attr_in_required or attr_in_optional
                assert_fail_str = (
                    f"{brick_format_category=} {brick_attribute=} {otx_key_value=}"
                )
                if attr_in_keys and otx_key_value:
                    assert attr_in_required, assert_fail_str
                elif attr_in_keys:
                    assert attr_in_optional, assert_fail_str

    # assert face_id_str() in brick_format_attributes
    # assert eon_id_str() in brick_format_attributes

    # confirm every bricknumber is unique
    assert len(brick_numbers_set) == len(brick_filenames)
    assert brick_numbers_set == get_brick_numbers()

    return True


def test_get_brick_format_filename_ReturnsObj():
    # ESTABLISH
    br00021_str = "br00021"
    br00020_str = "br00020"
    br00013_str = "br00013"

    # WHEN
    br00021_filename = get_brick_format_filename(br00021_str)
    br00020_filename = get_brick_format_filename(br00020_str)
    br00013_filename = get_brick_format_filename(br00013_str)

    # THEN
    assert br00021_filename == brick_format_00021_bud_acctunit_v0_0_0()
    assert br00020_filename == brick_format_00020_bud_acct_membership_v0_0_0()
    assert br00013_filename == brick_format_00013_itemunit_v0_0_0()

    all_set = {get_brick_format_filename(br) for br in get_brick_numbers()}
    assert all_set == get_brick_format_filenames()


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
