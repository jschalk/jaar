from src.f00_instrument.dict_toolbox import get_json_from_dict
from src.f00_instrument.file import save_file, create_path
from src.f01_road.finance_tran import quota_str, time_int_str, bridge_str
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
    timeline_idea_str,
    yr1_jan1_offset_str,
)
from src.f04_gift.atom_config import (
    get_atom_args_category_mapping,
    get_atom_config_dict,
    get_atom_categorys,
    jkeys_str,
    jvalues_str,
    normal_specs_str,
    column_order_str,
    atom_delete,
    atom_insert,
    atom_update,
    face_name_str,
    gov_idea_str,
    owner_name_str,
    acct_name_str,
    group_label_str,
    parent_road_str,
    idee_str,
    road_str,
    base_str,
    team_label_str,
    awardee_label_str,
    healer_name_str,
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

from src.f07_gov.gov_config import (
    get_gov_args_category_mapping,
    get_gov_config_dict,
    get_gov_categorys,
    govunit_str,
    gov_pactlog_str,
    gov_pact_episode_str,
    gov_cashbook_str,
    gov_timeline_hour_str,
    gov_timeline_month_str,
    gov_timeline_weekday_str,
    current_time_str,
    amount_str,
    month_idea_str,
    hour_idea_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_idea_str,
    weekday_order_str,
)
from src.f08_pidgin.pidgin_config import (
    event_int_str,
    pidginunit_str,
    otx_bridge_str,
    inx_bridge_str,
    unknown_word_str,
    otx_idea_str,
    inx_idea_str,
    otx_road_str,
    inx_road_str,
    otx_name_str,
    inx_name_str,
    otx_label_str,
    inx_label_str,
    map_otx2inx_str,
    map_name_str,
    map_label_str,
    map_idea_str,
    map_road_str,
    get_pidgin_categorys,
    get_pidgin_config_dict,
    get_pidgin_args_category_mapping,
)
from src.f09_brick.brick_config import (
    brick_type_str,
    get_brick_types,
    get_brick_elements_sort_order,
    get_brick_sqlite_type,
    get_brick_category_ref,
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

    assert get_brick_types() == {budunit_str(), govunit_str(), pidginunit_str()}


def test_get_brick_elements_sort_order_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_brick_elements_sort_order()

    # THEN
    assert table_sorting_priority[0] == face_name_str()
    assert table_sorting_priority[1] == event_int_str()
    assert table_sorting_priority[2] == gov_idea_str()
    assert table_sorting_priority[3] == owner_name_str()
    assert table_sorting_priority[4] == acct_name_str()
    assert table_sorting_priority[5] == group_label_str()
    assert table_sorting_priority[6] == parent_road_str()
    assert table_sorting_priority[7] == idee_str()
    assert table_sorting_priority[8] == road_str()
    assert table_sorting_priority[9] == base_str()
    assert table_sorting_priority[10] == "need"
    assert table_sorting_priority[11] == "pick"
    assert table_sorting_priority[12] == team_label_str()
    assert table_sorting_priority[13] == awardee_label_str()
    assert table_sorting_priority[14] == healer_name_str()
    assert table_sorting_priority[15] == time_int_str()
    assert table_sorting_priority[16] == begin_str()
    assert table_sorting_priority[17] == close_str()
    assert table_sorting_priority[18] == addin_str()
    assert table_sorting_priority[19] == numor_str()
    assert table_sorting_priority[20] == denom_str()
    assert table_sorting_priority[21] == morph_str()
    assert table_sorting_priority[22] == gogo_want_str()
    assert table_sorting_priority[23] == stop_want_str()
    assert table_sorting_priority[24] == base_item_active_requisite_str()
    assert table_sorting_priority[25] == credit_belief_str()
    assert table_sorting_priority[26] == debtit_belief_str()
    assert table_sorting_priority[27] == credit_vote_str()
    assert table_sorting_priority[28] == debtit_vote_str()
    assert table_sorting_priority[29] == credor_respect_str()
    assert table_sorting_priority[30] == debtor_respect_str()
    assert table_sorting_priority[31] == fopen_str()
    assert table_sorting_priority[32] == fnigh_str()
    assert table_sorting_priority[33] == "fund_pool"
    assert table_sorting_priority[34] == give_force_str()
    assert table_sorting_priority[35] == mass_str()
    assert table_sorting_priority[36] == "max_tree_traverse"
    assert table_sorting_priority[37] == "nigh"
    assert table_sorting_priority[38] == "open"
    assert table_sorting_priority[39] == "divisor"
    assert table_sorting_priority[40] == pledge_str()
    assert table_sorting_priority[41] == "problem_bool"
    assert table_sorting_priority[42] == "pact_time_int"
    assert table_sorting_priority[43] == take_force_str()
    assert table_sorting_priority[44] == "tally"
    assert table_sorting_priority[45] == fund_coin_str()
    assert table_sorting_priority[46] == penny_str()
    assert table_sorting_priority[47] == respect_bit_str()
    assert table_sorting_priority[48] == current_time_str()
    assert table_sorting_priority[49] == amount_str()
    assert table_sorting_priority[50] == month_idea_str()
    assert table_sorting_priority[51] == hour_idea_str()
    assert table_sorting_priority[52] == cumlative_minute_str()
    assert table_sorting_priority[53] == cumlative_day_str()
    assert table_sorting_priority[54] == weekday_idea_str()
    assert table_sorting_priority[55] == weekday_order_str()
    assert table_sorting_priority[56] == otx_idea_str()
    assert table_sorting_priority[57] == inx_idea_str()
    assert table_sorting_priority[58] == otx_road_str()
    assert table_sorting_priority[59] == inx_road_str()
    assert table_sorting_priority[60] == otx_name_str()
    assert table_sorting_priority[61] == inx_name_str()
    assert table_sorting_priority[62] == otx_label_str()
    assert table_sorting_priority[63] == inx_label_str()
    assert table_sorting_priority[64] == otx_bridge_str()
    assert table_sorting_priority[65] == inx_bridge_str()
    assert table_sorting_priority[66] == bridge_str()
    assert table_sorting_priority[67] == unknown_word_str()
    assert table_sorting_priority[68] == c400_number_str()
    assert table_sorting_priority[69] == yr1_jan1_offset_str()
    assert table_sorting_priority[70] == quota_str()
    assert table_sorting_priority[71] == monthday_distortion_str()
    assert table_sorting_priority[72] == timeline_idea_str()
    assert len(table_sorting_priority) == 73
    atom_args = set(get_atom_args_category_mapping().keys())
    assert atom_args.issubset(set(table_sorting_priority))
    gov_args = set(get_gov_args_category_mapping().keys())
    print(f"{gov_args=}")
    print(f"{gov_args.difference(set(table_sorting_priority))=}")
    assert gov_args.issubset(set(table_sorting_priority))
    pidgin_args = set(get_pidgin_args_category_mapping().keys())
    assert pidgin_args.issubset(set(table_sorting_priority))
    atom_gov_pidgin_args = atom_args
    atom_gov_pidgin_args.update(gov_args)
    atom_gov_pidgin_args.update(pidgin_args)
    table_sorting_priority.remove(event_int_str())
    table_sorting_priority.remove(face_name_str())
    assert atom_gov_pidgin_args == set(table_sorting_priority)


def test_get_brick_sqlite_type_ReturnsObj():
    # ESTABLISH / WHEN
    sqlite_types = get_brick_sqlite_type()

    # THEN
    assert set(sqlite_types.keys()) == set(get_brick_elements_sort_order())
    assert sqlite_types.get(face_name_str()) == "TEXT"
    assert sqlite_types.get(event_int_str()) == "INTEGER"
    assert sqlite_types.get(gov_idea_str()) == "TEXT"
    assert sqlite_types.get(owner_name_str()) == "TEXT"
    assert sqlite_types.get(acct_name_str()) == "TEXT"
    assert sqlite_types.get(group_label_str()) == "TEXT"
    assert sqlite_types.get(parent_road_str()) == "TEXT"
    assert sqlite_types.get(idee_str()) == "TEXT"
    assert sqlite_types.get(road_str()) == "TEXT"
    assert sqlite_types.get(base_str()) == "TEXT"
    assert sqlite_types.get("need") == "TEXT"
    assert sqlite_types.get("pick") == "TEXT"
    assert sqlite_types.get(team_label_str()) == "TEXT"
    assert sqlite_types.get(awardee_label_str()) == "TEXT"
    assert sqlite_types.get(healer_name_str()) == "TEXT"
    assert sqlite_types.get(time_int_str()) == "INTEGER"
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
    assert sqlite_types.get("pact_time_int") == "INTEGER"
    assert sqlite_types.get(take_force_str()) == "REAL"
    assert sqlite_types.get("tally") == "REAL"
    assert sqlite_types.get(fund_coin_str()) == "REAL"
    assert sqlite_types.get(penny_str()) == "REAL"
    assert sqlite_types.get(respect_bit_str()) == "REAL"
    assert sqlite_types.get(current_time_str()) == "INTEGER"
    assert sqlite_types.get(amount_str()) == "REAL"
    assert sqlite_types.get(month_idea_str()) == "TEXT"
    assert sqlite_types.get(hour_idea_str()) == "TEXT"
    assert sqlite_types.get(cumlative_minute_str()) == "INTEGER"
    assert sqlite_types.get(cumlative_day_str()) == "INTEGER"
    assert sqlite_types.get(weekday_idea_str()) == "TEXT"
    assert sqlite_types.get(weekday_order_str()) == "INTEGER"
    assert sqlite_types.get(otx_bridge_str()) == "TEXT"
    assert sqlite_types.get(inx_bridge_str()) == "TEXT"
    assert sqlite_types.get(unknown_word_str()) == "TEXT"
    assert sqlite_types.get(bridge_str()) == "TEXT"
    assert sqlite_types.get(c400_number_str()) == "INTEGER"
    assert sqlite_types.get(yr1_jan1_offset_str()) == "INTEGER"
    assert sqlite_types.get(quota_str()) == "REAL"
    assert sqlite_types.get(monthday_distortion_str()) == "INTEGER"
    assert sqlite_types.get(timeline_idea_str()) == "TEXT"


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
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f09_brick")


def test_get_brick_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    x_brick_config = get_brick_config_dict()

    # THEN
    assert x_brick_config
    brick_config_categorys = set(x_brick_config.keys())
    assert govunit_str() in brick_config_categorys
    assert gov_pactlog_str() not in brick_config_categorys
    assert gov_pact_episode_str() in brick_config_categorys
    assert gov_cashbook_str() in brick_config_categorys
    assert gov_timeline_hour_str() in brick_config_categorys
    assert gov_timeline_month_str() in brick_config_categorys
    assert gov_timeline_weekday_str() in brick_config_categorys
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
    assert map_name_str() in brick_config_categorys
    assert map_label_str() in brick_config_categorys
    assert map_idea_str() in brick_config_categorys
    assert map_road_str() in brick_config_categorys
    assert get_atom_categorys().issubset(brick_config_categorys)
    assert get_gov_categorys().issubset(brick_config_categorys)
    assert get_pidgin_categorys().issubset(brick_config_categorys)
    assert len(x_brick_config) == 20
    _validate_brick_config(x_brick_config)


def _validate_brick_config(x_brick_config: dict):
    atom_config_dict = get_atom_config_dict()
    gov_config_dict = get_gov_config_dict()
    pidgin_config_dict = get_pidgin_config_dict()
    # for every brick_format file there exists a unique brick_number always with leading zeros to make 5 digits
    for brick_category, brick_dict in x_brick_config.items():
        print(f"{brick_category=}")
        assert brick_dict.get(brick_type_str()) in get_brick_types()
        assert brick_dict.get(jkeys_str()) is not None
        assert brick_dict.get(jvalues_str()) is not None
        assert brick_dict.get(allowed_crud_str()) is not None
        assert brick_dict.get(atom_update()) is None
        assert brick_dict.get(atom_insert()) is None
        assert brick_dict.get(atom_delete()) is None
        assert brick_dict.get(normal_specs_str()) is None
        if brick_dict.get(brick_type_str()) == budunit_str():
            sub_category = atom_config_dict.get(brick_category)
        elif brick_dict.get(brick_type_str()) == govunit_str():
            sub_category = gov_config_dict.get(brick_category)
        elif brick_dict.get(brick_type_str()) == pidginunit_str():
            sub_category = pidgin_config_dict.get(brick_category)

        assert brick_dict.get(allowed_crud_str()) in get_allowed_curds()

        if brick_category in {
            gov_timeline_hour_str(),
            gov_timeline_month_str(),
            gov_timeline_weekday_str(),
            govunit_str(),
            map_otx2inx_str(),
            map_label_str(),
            map_name_str(),
            map_idea_str(),
            map_road_str(),
        }:
            assert brick_dict.get(allowed_crud_str()) == insert_one_time_str()
        elif brick_category in {gov_pact_episode_str(), gov_cashbook_str()}:
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

        sub_jkeys_keys = set(sub_category.get(jkeys_str()).keys())
        brick_jkeys_keys = set(brick_dict.get(jkeys_str()).keys())
        print(f"    {sub_jkeys_keys=}")
        print(f"  {brick_jkeys_keys=}")
        assert face_name_str() in brick_jkeys_keys
        assert event_int_str() in brick_jkeys_keys
        if brick_dict.get(brick_type_str()) != pidginunit_str():
            assert gov_idea_str() in brick_jkeys_keys
        if brick_dict.get(brick_type_str()) == budunit_str():
            brick_jkeys_keys.remove(gov_idea_str())
        brick_jkeys_keys.remove(face_name_str())
        brick_jkeys_keys.remove(event_int_str())
        assert sub_jkeys_keys == brick_jkeys_keys

        sub_jvalues_keys = set(sub_category.get(jvalues_str()).keys())
        print(f"  {sub_jvalues_keys=}")
        if gov_idea_str() in sub_jvalues_keys:
            sub_jvalues_keys.remove(gov_idea_str())

        brick_jvalues_dict = brick_dict.get(jvalues_str())
        brick_jvalues_keys = set(brick_jvalues_dict.keys())
        # print(f"  {sub_jvalues_keys=}")
        # print(f"{brick_jvalues_keys=}")
        assert sub_jvalues_keys == brick_jvalues_keys

        assert gov_idea_str() not in brick_jvalues_keys

        # sort_list = get_brick_elements_sort_order()
        # x_count = 0
        # sort_dict1 = {}
        # sort_dict2 = {}
        # for brick_arg in sort_list:
        #     sort_dict1[x_count] = brick_arg
        #     sort_dict1[brick_arg] = x_count

        # for jvalue in brick_jvalues_keys:
        #     print(f"{jvalue=} {brick_jvalues_dict=}")
        #     jvalue_dict = brick_jvalues_dict.get(jvalue)
        #     jvalue_column_order = jvalue_dict.get(column_order_str())
        #     assert jvalue_column_order != None
        #     list_ref_arg = sort_list[jvalue_column_order]
        #     assert list_ref_arg != None
        #     assert jvalue == list_ref_arg

        # # for jkey in brick_jkeys_keys:
        #     print(f"{jkey=} {brick_jkeys_dict=}")
        #     jkey_dict = brick_jkeys_dict.get(jkey)
        #     jkey_column_order = jkey_dict.get(column_order_str())
        #     assert jkey_column_order != None
        #     list_ref_arg = sort_list[jkey_column_order]
        #     assert list_ref_arg != None
        #     assert jkey == list_ref_arg


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
    valid_brick_categorys.update(get_gov_categorys())
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
                cat_required_keys = set(format_config.get(jkeys_str()).keys())
                cat_optional_keys = set(format_config.get(jvalues_str()).keys())
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

    # assert face_name_str() in brick_format_attributes
    # assert event_int_str() in brick_format_attributes

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
    # set_brick_config_json(map_name_str(), 0)
    # set_brick_config_json(map_label_str(), 1)
    # set_brick_config_json(map_idea_str(), 2)
    # set_brick_config_json(map_road_str(), 3)
    # set_brick_config_json(govunit_str(), 5)
    # set_brick_config_json(gov_timeline_hour_str(), 6)
    # set_brick_config_json(gov_timeline_month_str(), 7)
    # set_brick_config_json(gov_timeline_weekday_str(), 8)
    # set_brick_config_json(bud_acct_membership_str(), 9)
    # set_brick_config_json(bud_acctunit_str(), 10)
    # set_brick_config_json(bud_item_awardlink_str(), 11)
    # set_brick_config_json(bud_item_factunit_str(), 12)
    # set_brick_config_json(bud_item_teamlink_str(), 14)
    # set_brick_config_json(bud_item_healerlink_str(), 15)
    # set_brick_config_json(bud_item_reason_premiseunit_str(), 16)
    # set_brick_config_json(bud_item_reasonunit_str(), 17)
    # set_brick_config_json(bud_itemunit_str(), 18)
    # set_brick_config_json(budunit_str(), 19)
    # set_brick_config_json(gov_pact_episode_str(), 20)
    # set_brick_config_json(gov_cashbook_str(), 21)

    x_brick_config = get_brick_config_dict()

    # THEN
    assert x_brick_config.get(map_name_str()).get(bo) == 0
    assert x_brick_config.get(map_label_str()).get(bo) == 1
    assert x_brick_config.get(map_idea_str()).get(bo) == 2
    assert x_brick_config.get(map_road_str()).get(bo) == 3
    assert x_brick_config.get(govunit_str()).get(bo) == 5
    assert x_brick_config.get(gov_timeline_hour_str()).get(bo) == 6
    assert x_brick_config.get(gov_timeline_month_str()).get(bo) == 7
    assert x_brick_config.get(gov_timeline_weekday_str()).get(bo) == 8
    assert x_brick_config.get(bud_acct_membership_str()).get(bo) == 9
    assert x_brick_config.get(bud_acctunit_str()).get(bo) == 10
    assert x_brick_config.get(bud_item_awardlink_str()).get(bo) == 11
    assert x_brick_config.get(bud_item_factunit_str()).get(bo) == 12
    assert x_brick_config.get(bud_item_teamlink_str()).get(bo) == 14
    assert x_brick_config.get(bud_item_healerlink_str()).get(bo) == 15
    assert x_brick_config.get(bud_item_reason_premiseunit_str()).get(bo) == 16
    assert x_brick_config.get(bud_item_reasonunit_str()).get(bo) == 17
    assert x_brick_config.get(bud_itemunit_str()).get(bo) == 18
    assert x_brick_config.get(budunit_str()).get(bo) == 19
    assert x_brick_config.get(gov_pact_episode_str()).get(bo) == 20
    assert x_brick_config.get(gov_cashbook_str()).get(bo) == 21


def test_get_quick_bricks_column_ref_ReturnsObj():
    # ESTABLISH / WHEN
    x_brick_quick_column_ref = get_quick_bricks_column_ref()

    # THEN
    assert len(x_brick_quick_column_ref) == len(get_brick_numbers())
    assert x_brick_quick_column_ref.get("br00000") == {
        face_name_str(),
        event_int_str(),
        c400_number_str(),
        current_time_str(),
        gov_idea_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        timeline_idea_str(),
        yr1_jan1_offset_str(),
    }


def test_get_brick_category_ref_ReturnsObj():
    # ESTABLISH / WHEN
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    brick_numbers_sorted = list(get_brick_numbers())
    brick_numbers_sorted.sort(key=lambda x: x)

    example_ref = {}
    for brick_number in brick_numbers_sorted:
        brick_format_file_name = get_brick_format_filename(brick_number)
        x_brickref = get_brickref_from_file(brick_format_file_name)
        categorys_list = x_brickref.get(categorys_str())
        for x_category in categorys_list:
            if example_ref.get(x_category) is None:
                example_ref[x_category] = [brick_number]
            else:
                example_ref.get(x_category).append(brick_number)
    print(f"{example_ref=}")

    # WHEN / THEN
    assert get_brick_category_ref() == example_ref
