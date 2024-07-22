from src._instrument.file import dir_files
from src.gift.atom_config import config_file_dir, bud_acctunit_text
from src.gift.span import (
    real_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    parent_road_str,
    label_str,
    mass_str,
    pledge_str,
    acct_pool_str,
    debtit_score_str,
    credit_score_str,
    column_order_str,
    # must_be_str,
    # must_be_roadnode_str,
    # must_be_roadunit_str,
    # must_be_number_str,
    # must_be_bool_str,
    get_span_formats_dir,
    get_span_filenames,
    jaar_format_0001_acct_v0_0_0,
    jaar_format_0002_membership_v0_0_0,
    jaar_format_0003_ideaunit_v0_0_0,
    _get_headers_list,
    create_span_dataframe,
    get_spanref,
)


def test_config_str_functions_ReturnObjs():
    # ESTABLISH / WHEN / THEN
    assert real_id_str() == "real_id"
    assert owner_id_str() == "owner_id"
    assert acct_id_str() == "acct_id"
    assert acct_pool_str() == "acct_pool"
    assert debtit_score_str() == "debtit_score"
    assert credit_score_str() == "credit_score"
    assert jaar_format_0001_acct_v0_0_0() == "jaar_format_0001_acct_v0_0_0"
    x0002_span = "jaar_format_0002_membership_v0_0_0"
    assert jaar_format_0002_membership_v0_0_0() == x0002_span
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
    assert jaar_format_0002_membership_v0_0_0() in x_filenames
    assert jaar_format_0003_ideaunit_v0_0_0() in x_filenames


def test_get_spanref_ReturnsObj():
    # ESTABLISH
    span_name_0001 = jaar_format_0001_acct_v0_0_0()

    # WHEN
    x_spanref = get_spanref(span_name_0001)

    # THEN
    assert x_spanref.span_name == span_name_0001
    assert x_spanref.atom_category == bud_acctunit_text()
    assert x_spanref._spancolumns != {}
    assert len(x_spanref._spancolumns) == 5


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_0001_headers = _get_headers_list(jaar_format_0001_acct_v0_0_0())

    # THEN
    # print(f"{format_0001_headers=}")
    assert format_0001_headers == [
        "real_id",
        "owner_id",
        "acct_id",
        "credit_score",
        "debtit_score",
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


def test_get_spanref_HasCorrectAttrs_jaar_format_0001_acct_v0_0_0():
    # ESTABLISH
    span_name = jaar_format_0001_acct_v0_0_0()

    # WHEN
    format_0001_spanref = get_spanref(span_name)

    # THEN
    real_id_spancolumn = format_0001_spanref.get_spancolumn(real_id_str())
    owner_id_spancolumn = format_0001_spanref.get_spancolumn(owner_id_str())
    acct_id_spancolumn = format_0001_spanref.get_spancolumn(acct_id_str())
    credit_score_spancolumn = format_0001_spanref.get_spancolumn(credit_score_str())
    debtit_score_spancolumn = format_0001_spanref.get_spancolumn(debtit_score_str())
    assert len(format_0001_spanref._spancolumns) == 5

    assert real_id_spancolumn.column_order == 0
    assert owner_id_spancolumn.column_order == 1
    assert acct_id_spancolumn.column_order == 2
    assert credit_score_spancolumn.column_order == 3
    assert debtit_score_spancolumn.column_order == 4


def test_get_spanref_HasCorrectAttrs_jaar_format_0002_membership_v0_0_0():
    # ESTABLISH
    span_name = jaar_format_0002_membership_v0_0_0()

    # WHEN
    format_0002_spanref = get_spanref(span_name)

    # THEN
    real_id_spancolumn = format_0002_spanref.get_spancolumn(real_id_str())
    owner_id_spancolumn = format_0002_spanref.get_spancolumn(owner_id_str())
    acct_id_spancolumn = format_0002_spanref.get_spancolumn(acct_id_str())
    group_id_spancolumn = format_0002_spanref.get_spancolumn(group_id_str())
    credit_score_spancolumn = format_0002_spanref.get_spancolumn(credit_score_str())
    debtit_score_spancolumn = format_0002_spanref.get_spancolumn(debtit_score_str())
    assert len(format_0002_spanref._spancolumns) == 6

    assert real_id_spancolumn.column_order == 0
    assert owner_id_spancolumn.column_order == 1
    assert acct_id_spancolumn.column_order == 2
    assert group_id_spancolumn.column_order == 3
    assert debtit_score_spancolumn.column_order == 5
    assert credit_score_spancolumn.column_order == 4


def test_get_spanref_HasCorrectAttrs_jaar_format_0003_ideaunit_v0_0_0():
    # ESTABLISH
    span_name = jaar_format_0003_ideaunit_v0_0_0()

    # WHEN
    format_0003_spanref = get_spanref(span_name)

    # THEN
    real_id_spancolumn = format_0003_spanref.get_spancolumn(real_id_str())
    owner_id_spancolumn = format_0003_spanref.get_spancolumn(owner_id_str())
    parent_road_spancolumn = format_0003_spanref.get_spancolumn(parent_road_str())
    label_spancolumn = format_0003_spanref.get_spancolumn(label_str())
    mass_spancolumn = format_0003_spanref.get_spancolumn(mass_str())
    pledge_spancolumn = format_0003_spanref.get_spancolumn(pledge_str())
    assert len(format_0003_spanref._spancolumns) == 6

    assert real_id_spancolumn.column_order == 0
    assert owner_id_spancolumn.column_order == 1
    assert parent_road_spancolumn.column_order == 3
    assert label_spancolumn.column_order == 5
    assert mass_spancolumn.column_order == 4
    assert pledge_spancolumn.column_order == 2
