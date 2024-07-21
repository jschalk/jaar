from src._instrument.file import dir_files
from src.gift.atom_config import config_file_dir
from src.gift.span import (
    real_id_str,
    owner_id_str,
    acct_id_str,
    lobby_id_str,
    parent_road_str,
    label_str,
    weight_str,
    pledge_str,
    acct_pool_str,
    debtor_weight_str,
    credor_weight_str,
    column_order_str,
    # must_be_str,
    # must_be_roadnode_str,
    # must_be_roadunit_str,
    # must_be_number_str,
    # must_be_bool_str,
    get_span_formats_dir,
    get_span_filenames,
    get_span_attribute_dict,
    get_column_ordered_span_attributes,
    jaar_format_0001_acct_v0_0_0,
    jaar_format_0002_lobbyship_v0_0_0,
    jaar_format_0003_ideaunit_v0_0_0,
    _get_headers_list,
    create_span_dataframe,
)


def test_config_str_functions_ReturnObjs():
    # ESTABLISH / WHEN / THEN
    assert real_id_str() == "real_id"
    assert owner_id_str() == "owner_id"
    assert acct_id_str() == "acct_id"
    assert acct_pool_str() == "acct_pool"
    assert debtor_weight_str() == "debtor_weight"
    assert credor_weight_str() == "credor_weight"
    assert jaar_format_0001_acct_v0_0_0() == "jaar_format_0001_acct_v0_0_0"
    x0002_span = "jaar_format_0002_lobbyship_v0_0_0"
    assert jaar_format_0002_lobbyship_v0_0_0() == x0002_span
    x0003_span = "jaar_format_0003_ideaunit_v0_0_0"
    assert jaar_format_0003_ideaunit_v0_0_0() == x0003_span


def test_get_span_formats_dir_ReturnsObj():
    # ESTABLISH / WHEN
    span_dir = get_span_formats_dir()
    # THEN
    print(f"{span_dir=}")
    assert span_dir == f"{config_file_dir()}/span_formats"


def test_get_span_filenames_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    x_filenames = get_span_filenames()
    # THEN
    print(f"{x_filenames=}")
    assert jaar_format_0001_acct_v0_0_0() in x_filenames
    assert jaar_format_0002_lobbyship_v0_0_0() in x_filenames
    assert jaar_format_0003_ideaunit_v0_0_0() in x_filenames


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_0001_headers = _get_headers_list(jaar_format_0001_acct_v0_0_0())

    # THEN
    # print(f"{format_0001_headers=}")
    assert format_0001_headers == [
        "acct_id",
        "credor_weight",
        "debtor_weight",
        "owner_id",
        "real_id",
    ]


def test_create_span_dataframe_ReturnsCorrectObj():
    # ESTABLISH
    empty_d2 = []
    # WHEN
    x_df = create_span_dataframe(empty_d2, jaar_format_0001_acct_v0_0_0())
    # THEN
    assert list(x_df.columns) == _get_headers_list(jaar_format_0001_acct_v0_0_0())


def for_all_spans_create_span_dataframe():
    # TODO Catching broad exceptions can make debugging difficult. Consider catching more specific exceptions or at least logging the exception details.
    empty_d2 = []
    for x_filename in get_span_filenames():
        try:
            create_span_dataframe(empty_d2, x_filename)
        except Exception:
            print(f"create_span_dataframe failed for {x_filename=}")
            return False
    return True


def test_create_span_dataframe_ReturnsCorrectObjForEvery_span():
    # ESTABLISH / WHEN / THEN
    assert for_all_spans_create_span_dataframe()


def test_span_FilesExist():
    # ESTABLISH
    span_dir = get_span_formats_dir()

    # WHEN
    span_files = dir_files(span_dir, True)

    # THEN
    span_filenames = set(span_files.keys())
    assert span_filenames == get_span_filenames()
    assert len(span_filenames) == len(get_span_filenames())


def test_get_span_attribute_dict_HasCorrectAttrs_jaar_format_0001_acct_v0_0_0():
    # ESTABLISH
    span_name = jaar_format_0001_acct_v0_0_0()

    # WHEN
    span_dict = get_span_attribute_dict(span_name)

    # THEN
    real_id_dict = span_dict.get(real_id_str())
    owner_id_dict = span_dict.get(owner_id_str())
    acct_id_dict = span_dict.get(acct_id_str())
    credor_weight_dict = span_dict.get(credor_weight_str())
    debtor_weight_dict = span_dict.get(debtor_weight_str())
    assert real_id_dict is not None
    assert owner_id_dict is not None
    assert acct_id_dict is not None
    assert credor_weight_dict is not None
    assert debtor_weight_dict is not None
    assert len(span_dict) == 5

    real_id_column_order = real_id_dict.get(column_order_str())
    owner_id_column_order = owner_id_dict.get(column_order_str())
    acct_id_column_order = acct_id_dict.get(column_order_str())
    credor_weight_column_order = credor_weight_dict.get(column_order_str())
    debtor_weight_column_order = debtor_weight_dict.get(column_order_str())
    assert real_id_column_order == 0
    assert owner_id_column_order == 1
    assert acct_id_column_order == 2
    assert credor_weight_column_order == 3
    assert debtor_weight_column_order == 4


def test_get_span_attribute_dict_HasCorrectAttrs_jaar_format_0002_lobbyship_v0_0_0():
    # ESTABLISH
    span_name = jaar_format_0002_lobbyship_v0_0_0()

    # WHEN
    span_dict = get_span_attribute_dict(span_name)

    # THEN
    real_id_dict = span_dict.get(real_id_str())
    owner_id_dict = span_dict.get(owner_id_str())
    acct_id_dict = span_dict.get(acct_id_str())
    lobby_id_dict = span_dict.get(lobby_id_str())
    debtor_weight_dict = span_dict.get(debtor_weight_str())
    credor_weight_dict = span_dict.get(credor_weight_str())
    assert real_id_dict is not None
    assert owner_id_dict is not None
    assert acct_id_dict is not None
    assert lobby_id_dict is not None
    assert debtor_weight_dict is not None
    assert credor_weight_dict is not None
    assert len(span_dict) == 6

    assert real_id_dict.get(column_order_str()) == 0
    assert owner_id_dict.get(column_order_str()) == 1
    assert acct_id_dict.get(column_order_str()) == 2
    assert lobby_id_dict.get(column_order_str()) == 3
    assert debtor_weight_dict.get(column_order_str()) == 5
    assert credor_weight_dict.get(column_order_str()) == 4


def test_get_span_attribute_dict_HasCorrectAttrs_jaar_format_0003_ideaunit_v0_0_0():
    # ESTABLISH
    span_name = jaar_format_0003_ideaunit_v0_0_0()

    # WHEN
    span_dict = get_span_attribute_dict(span_name)

    # THEN
    real_id_dict = span_dict.get(real_id_str())
    owner_id_dict = span_dict.get(owner_id_str())
    parent_road_dict = span_dict.get(parent_road_str())
    label_dict = span_dict.get(label_str())
    weight_dict = span_dict.get(weight_str())
    pledge_dict = span_dict.get(pledge_str())
    assert real_id_dict is not None
    assert owner_id_dict is not None
    assert parent_road_dict is not None
    assert label_dict is not None
    assert weight_dict is not None
    assert pledge_dict is not None
    assert len(span_dict) == 6

    assert real_id_dict.get(column_order_str()) == 0
    assert owner_id_dict.get(column_order_str()) == 1
    assert parent_road_dict.get(column_order_str()) == 3
    assert label_dict.get(column_order_str()) == 5
    assert weight_dict.get(column_order_str()) == 4
    assert pledge_dict.get(column_order_str()) == 2


def test_get_column_ordered_span_attributes_ReturnsCorrectObj_scenario1():
    # ESTABLISH
    span_name = jaar_format_0001_acct_v0_0_0()
    # WHEN
    sorted_span_attributes = get_column_ordered_span_attributes(span_name)

    # THEN
    assert sorted_span_attributes == [
        real_id_str(),
        owner_id_str(),
        acct_id_str(),
        credor_weight_str(),
        debtor_weight_str(),
    ]


def test_get_column_ordered_span_attributes_ReturnsCorrectObj_scenario2():
    # ESTABLISH
    span_name = jaar_format_0003_ideaunit_v0_0_0()
    # WHEN
    sorted_span_attributes = get_column_ordered_span_attributes(span_name)

    # THEN
    print(f"{sorted_span_attributes=}")
    assert sorted_span_attributes == [
        real_id_str(),
        owner_id_str(),
        pledge_str(),
        parent_road_str(),
        weight_str(),
        label_str(),
    ]
