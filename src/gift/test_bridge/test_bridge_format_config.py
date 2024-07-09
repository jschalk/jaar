from src._instrument.file import dir_files
from src.gift.atom_config import (
    config_file_dir,
    atom_insert,
    atom_delete,
    atom_update,
    category_ref,
    is_category_ref,
    get_atom_config_dict,
    get_atom_order as q_order,
    set_mog,
    get_flattened_atom_table_build,
    get_normalized_world_table_build,
    required_args_text,
    optional_args_text,
    normal_table_name_text,
    normal_specs_text,
    sqlite_datatype_text,
    python_type_text,
    worldunit_text,
    world_charunit_text,
    world_char_beliefhold_text,
    world_ideaunit_text,
    world_idea_fiscallink_text,
    world_idea_reasonunit_text,
    world_idea_reason_premiseunit_text,
    world_idea_belieflink_text,
    world_idea_healerhold_text,
    world_idea_factunit_text,
)
from src.gift.bridge import (
    real_id_str,
    owner_id_str,
    char_id_str,
    belief_id_str,
    parent_road_str,
    label_str,
    weight_str,
    pledge_str,
    char_pool_str,
    debtor_weight_str,
    credor_weight_str,
    column_order_str,
    must_be_str,
    must_be_roadnode_str,
    must_be_roadunit_str,
    must_be_number_str,
    must_be_bool_str,
    get_bridge_formats_dir,
    get_bridge_filenames,
    get_bridge_attribute_dict,
    get_column_ordered_bridge_attributes,
    jaar_format_0001_char_v0_0_0,
    jaar_format_0002_beliefhold_v0_0_0,
    jaar_format_0003_ideaunit_v0_0_0,
    _get_headers_list,
    create_bridge_dataframe,
)


def test_str_functions_ReturnCorrectObjs():
    # GIVEN / WHEN / THEN
    assert real_id_str() == "real_id"
    assert owner_id_str() == "owner_id"
    assert char_id_str() == "char_id"
    assert char_pool_str() == "char_pool"
    assert debtor_weight_str() == "debtor_weight"
    assert credor_weight_str() == "credor_weight"
    assert jaar_format_0001_char_v0_0_0() == "jaar_format_0001_char_v0_0_0"
    x0002_bridge = "jaar_format_0002_beliefhold_v0_0_0"
    assert jaar_format_0002_beliefhold_v0_0_0() == x0002_bridge
    x0003_bridge = "jaar_format_0003_ideaunit_v0_0_0"
    assert jaar_format_0003_ideaunit_v0_0_0() == x0003_bridge


def test_get_bridge_formats_dir_ReturnsObj():
    # GIVEN / WHEN
    bridge_dir = get_bridge_formats_dir()
    # THEN
    print(f"{bridge_dir=}")
    assert bridge_dir == f"{config_file_dir()}/bridge_formats"


def test_get_bridge_filenames_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_filenames = get_bridge_filenames()
    # THEN
    print(f"{x_filenames=}")
    assert jaar_format_0001_char_v0_0_0() in x_filenames
    assert jaar_format_0002_beliefhold_v0_0_0() in x_filenames
    assert jaar_format_0003_ideaunit_v0_0_0() in x_filenames


def test_get_headers_list_ReturnsObj():
    # GIVEN / WHEN
    format_0001_headers = _get_headers_list(jaar_format_0001_char_v0_0_0())

    # THEN
    # print(f"{format_0001_headers=}")
    assert format_0001_headers == [
        "char_id",
        "char_pool",
        "credor_weight",
        "debtor_weight",
        "owner_id",
        "real_id",
    ]


def test_create_bridge_dataframe_ReturnsCorrectObj():
    # GIVEN
    empty_d2 = []
    # WHEN
    x_df = create_bridge_dataframe(empty_d2, jaar_format_0001_char_v0_0_0())
    # THEN
    assert list(x_df.columns) == _get_headers_list(jaar_format_0001_char_v0_0_0())


def for_all_bridges_create_bridge_dataframe():
    empty_d2 = []
    for x_filename in get_bridge_filenames():
        try:
            create_bridge_dataframe(empty_d2, x_filename)
        except Exception:
            print(f"create_bridge_dataframe failed for {x_filename=}")
            return False
    return True


def test_create_bridge_dataframe_ReturnsCorrectObjForEvery_bridge():
    # GIVEN / WHEN / THEN
    assert for_all_bridges_create_bridge_dataframe()


def test_bridge_FilesExist():
    # GIVEN
    bridge_dir = get_bridge_formats_dir()

    # WHEN
    bridge_files = dir_files(bridge_dir, True)

    # THEN
    bridge_filenames = set(bridge_files.keys())
    assert bridge_filenames == get_bridge_filenames()
    assert len(bridge_filenames) == len(get_bridge_filenames())


def test_get_bridge_attribute_dict_HasCorrectAttrs_jaar_format_0001_char_v0_0_0():
    # GIVEN
    bridge_name = jaar_format_0001_char_v0_0_0()

    # WHEN
    bridge_dict = get_bridge_attribute_dict(bridge_name)

    # THEN
    real_id_dict = bridge_dict.get(real_id_str())
    owner_id_dict = bridge_dict.get(owner_id_str())
    char_id_dict = bridge_dict.get(char_id_str())
    char_pool_dict = bridge_dict.get(char_pool_str())
    debtor_weight_dict = bridge_dict.get(debtor_weight_str())
    credor_weight_dict = bridge_dict.get(credor_weight_str())
    assert real_id_dict != None
    assert owner_id_dict != None
    assert char_id_dict != None
    assert char_pool_dict != None
    assert debtor_weight_dict != None
    assert credor_weight_dict != None
    assert len(bridge_dict) == 6

    real_id_column_order = real_id_dict.get(column_order_str())
    owner_id_column_order = owner_id_dict.get(column_order_str())
    char_id_column_order = char_id_dict.get(column_order_str())
    char_pool_column_order = char_pool_dict.get(column_order_str())
    debtor_weight_column_order = debtor_weight_dict.get(column_order_str())
    credor_weight_column_order = credor_weight_dict.get(column_order_str())
    assert real_id_column_order == 0
    assert owner_id_column_order == 1
    assert char_pool_column_order == 2
    assert char_id_column_order == 3
    assert debtor_weight_column_order == 5
    assert credor_weight_column_order == 4


def test_get_bridge_attribute_dict_HasCorrectAttrs_jaar_format_0002_beliefhold_v0_0_0():
    # GIVEN
    bridge_name = jaar_format_0002_beliefhold_v0_0_0()

    # WHEN
    bridge_dict = get_bridge_attribute_dict(bridge_name)

    # THEN
    real_id_dict = bridge_dict.get(real_id_str())
    owner_id_dict = bridge_dict.get(owner_id_str())
    char_id_dict = bridge_dict.get(char_id_str())
    belief_id_dict = bridge_dict.get(belief_id_str())
    debtor_weight_dict = bridge_dict.get(debtor_weight_str())
    credor_weight_dict = bridge_dict.get(credor_weight_str())
    assert real_id_dict != None
    assert owner_id_dict != None
    assert char_id_dict != None
    assert belief_id_dict != None
    assert debtor_weight_dict != None
    assert credor_weight_dict != None
    assert len(bridge_dict) == 6

    assert real_id_dict.get(column_order_str()) == 0
    assert owner_id_dict.get(column_order_str()) == 1
    assert char_id_dict.get(column_order_str()) == 2
    assert belief_id_dict.get(column_order_str()) == 3
    assert debtor_weight_dict.get(column_order_str()) == 5
    assert credor_weight_dict.get(column_order_str()) == 4


def test_get_bridge_attribute_dict_HasCorrectAttrs_jaar_format_0003_ideaunit_v0_0_0():
    # GIVEN
    bridge_name = jaar_format_0003_ideaunit_v0_0_0()

    # WHEN
    bridge_dict = get_bridge_attribute_dict(bridge_name)

    # THEN
    real_id_dict = bridge_dict.get(real_id_str())
    owner_id_dict = bridge_dict.get(owner_id_str())
    parent_road_dict = bridge_dict.get(parent_road_str())
    label_dict = bridge_dict.get(label_str())
    weight_dict = bridge_dict.get(weight_str())
    pledge_dict = bridge_dict.get(pledge_str())
    assert real_id_dict != None
    assert owner_id_dict != None
    assert parent_road_dict != None
    assert label_dict != None
    assert weight_dict != None
    assert pledge_dict != None
    assert len(bridge_dict) == 6

    assert real_id_dict.get(column_order_str()) == 0
    assert owner_id_dict.get(column_order_str()) == 1
    assert parent_road_dict.get(column_order_str()) == 3
    assert label_dict.get(column_order_str()) == 5
    assert weight_dict.get(column_order_str()) == 4
    assert pledge_dict.get(column_order_str()) == 2


def test_get_column_ordered_bridge_attributes_ReturnsCorrectObj_scenario1():
    # GIVEN
    bridge_name = jaar_format_0001_char_v0_0_0()
    # WHEN
    sorted_bridge_attributes = get_column_ordered_bridge_attributes(bridge_name)

    # THEN
    assert sorted_bridge_attributes == [
        real_id_str(),
        owner_id_str(),
        char_pool_str(),
        char_id_str(),
        credor_weight_str(),
        debtor_weight_str(),
    ]


def test_get_column_ordered_bridge_attributes_ReturnsCorrectObj_scenario2():
    # GIVEN
    bridge_name = jaar_format_0003_ideaunit_v0_0_0()
    # WHEN
    sorted_bridge_attributes = get_column_ordered_bridge_attributes(bridge_name)

    # THEN
    print(f"{sorted_bridge_attributes=}")
    assert sorted_bridge_attributes == [
        real_id_str(),
        owner_id_str(),
        pledge_str(),
        parent_road_str(),
        weight_str(),
        label_str(),
    ]
