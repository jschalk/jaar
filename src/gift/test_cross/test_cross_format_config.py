from src._instrument.file import dir_files
from src.gift.atom_config import config_file_dir
from src.gift.cross import (
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
    # must_be_str,
    # must_be_roadnode_str,
    # must_be_roadunit_str,
    # must_be_number_str,
    # must_be_bool_str,
    get_cross_formats_dir,
    get_cross_filenames,
    get_cross_attribute_dict,
    get_column_ordered_cross_attributes,
    jaar_format_0001_char_v0_0_0,
    jaar_format_0002_belieflink_v0_0_0,
    jaar_format_0003_ideaunit_v0_0_0,
    _get_headers_list,
    create_cross_dataframe,
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
    x0002_cross = "jaar_format_0002_belieflink_v0_0_0"
    assert jaar_format_0002_belieflink_v0_0_0() == x0002_cross
    x0003_cross = "jaar_format_0003_ideaunit_v0_0_0"
    assert jaar_format_0003_ideaunit_v0_0_0() == x0003_cross


def test_get_cross_formats_dir_ReturnsObj():
    # GIVEN / WHEN
    cross_dir = get_cross_formats_dir()
    # THEN
    print(f"{cross_dir=}")
    assert cross_dir == f"{config_file_dir()}/cross_formats"


def test_get_cross_filenames_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_filenames = get_cross_filenames()
    # THEN
    print(f"{x_filenames=}")
    assert jaar_format_0001_char_v0_0_0() in x_filenames
    assert jaar_format_0002_belieflink_v0_0_0() in x_filenames
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


def test_create_cross_dataframe_ReturnsCorrectObj():
    # GIVEN
    empty_d2 = []
    # WHEN
    x_df = create_cross_dataframe(empty_d2, jaar_format_0001_char_v0_0_0())
    # THEN
    assert list(x_df.columns) == _get_headers_list(jaar_format_0001_char_v0_0_0())


def for_all_crosss_create_cross_dataframe():
    empty_d2 = []
    for x_filename in get_cross_filenames():
        try:
            create_cross_dataframe(empty_d2, x_filename)
        except Exception:
            print(f"create_cross_dataframe failed for {x_filename=}")
            return False
    return True


def test_create_cross_dataframe_ReturnsCorrectObjForEvery_cross():
    # GIVEN / WHEN / THEN
    assert for_all_crosss_create_cross_dataframe()


def test_cross_FilesExist():
    # GIVEN
    cross_dir = get_cross_formats_dir()

    # WHEN
    cross_files = dir_files(cross_dir, True)

    # THEN
    cross_filenames = set(cross_files.keys())
    assert cross_filenames == get_cross_filenames()
    assert len(cross_filenames) == len(get_cross_filenames())


def test_get_cross_attribute_dict_HasCorrectAttrs_jaar_format_0001_char_v0_0_0():
    # GIVEN
    cross_name = jaar_format_0001_char_v0_0_0()

    # WHEN
    cross_dict = get_cross_attribute_dict(cross_name)

    # THEN
    real_id_dict = cross_dict.get(real_id_str())
    owner_id_dict = cross_dict.get(owner_id_str())
    char_id_dict = cross_dict.get(char_id_str())
    char_pool_dict = cross_dict.get(char_pool_str())
    debtor_weight_dict = cross_dict.get(debtor_weight_str())
    credor_weight_dict = cross_dict.get(credor_weight_str())
    assert real_id_dict != None
    assert owner_id_dict != None
    assert char_id_dict != None
    assert char_pool_dict != None
    assert debtor_weight_dict != None
    assert credor_weight_dict != None
    assert len(cross_dict) == 6

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


def test_get_cross_attribute_dict_HasCorrectAttrs_jaar_format_0002_belieflink_v0_0_0():
    # GIVEN
    cross_name = jaar_format_0002_belieflink_v0_0_0()

    # WHEN
    cross_dict = get_cross_attribute_dict(cross_name)

    # THEN
    real_id_dict = cross_dict.get(real_id_str())
    owner_id_dict = cross_dict.get(owner_id_str())
    char_id_dict = cross_dict.get(char_id_str())
    belief_id_dict = cross_dict.get(belief_id_str())
    debtor_weight_dict = cross_dict.get(debtor_weight_str())
    credor_weight_dict = cross_dict.get(credor_weight_str())
    assert real_id_dict != None
    assert owner_id_dict != None
    assert char_id_dict != None
    assert belief_id_dict != None
    assert debtor_weight_dict != None
    assert credor_weight_dict != None
    assert len(cross_dict) == 6

    assert real_id_dict.get(column_order_str()) == 0
    assert owner_id_dict.get(column_order_str()) == 1
    assert char_id_dict.get(column_order_str()) == 2
    assert belief_id_dict.get(column_order_str()) == 3
    assert debtor_weight_dict.get(column_order_str()) == 5
    assert credor_weight_dict.get(column_order_str()) == 4


def test_get_cross_attribute_dict_HasCorrectAttrs_jaar_format_0003_ideaunit_v0_0_0():
    # GIVEN
    cross_name = jaar_format_0003_ideaunit_v0_0_0()

    # WHEN
    cross_dict = get_cross_attribute_dict(cross_name)

    # THEN
    real_id_dict = cross_dict.get(real_id_str())
    owner_id_dict = cross_dict.get(owner_id_str())
    parent_road_dict = cross_dict.get(parent_road_str())
    label_dict = cross_dict.get(label_str())
    weight_dict = cross_dict.get(weight_str())
    pledge_dict = cross_dict.get(pledge_str())
    assert real_id_dict != None
    assert owner_id_dict != None
    assert parent_road_dict != None
    assert label_dict != None
    assert weight_dict != None
    assert pledge_dict != None
    assert len(cross_dict) == 6

    assert real_id_dict.get(column_order_str()) == 0
    assert owner_id_dict.get(column_order_str()) == 1
    assert parent_road_dict.get(column_order_str()) == 3
    assert label_dict.get(column_order_str()) == 5
    assert weight_dict.get(column_order_str()) == 4
    assert pledge_dict.get(column_order_str()) == 2


def test_get_column_ordered_cross_attributes_ReturnsCorrectObj_scenario1():
    # GIVEN
    cross_name = jaar_format_0001_char_v0_0_0()
    # WHEN
    sorted_cross_attributes = get_column_ordered_cross_attributes(cross_name)

    # THEN
    assert sorted_cross_attributes == [
        real_id_str(),
        owner_id_str(),
        char_pool_str(),
        char_id_str(),
        credor_weight_str(),
        debtor_weight_str(),
    ]


def test_get_column_ordered_cross_attributes_ReturnsCorrectObj_scenario2():
    # GIVEN
    cross_name = jaar_format_0003_ideaunit_v0_0_0()
    # WHEN
    sorted_cross_attributes = get_column_ordered_cross_attributes(cross_name)

    # THEN
    print(f"{sorted_cross_attributes=}")
    assert sorted_cross_attributes == [
        real_id_str(),
        owner_id_str(),
        pledge_str(),
        parent_road_str(),
        weight_str(),
        label_str(),
    ]