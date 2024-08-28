from src._instrument.file import dir_files
from src.gift.atom_config import config_file_dir, bud_acctunit_text
from src.stone.stone import (
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
    debtit_vote_str,
    credit_vote_str,
    column_order_str,
    # must_be_str,
    # must_be_roadnode_str,
    # must_be_roadunit_str,
    # must_be_number_str,
    # must_be_bool_str,
    get_stone_formats_dir,
    get_stone_filenames,
    jaar_format_00001_acct_v0_0_0,
    jaar_format_00002_membership_v0_0_0,
    jaar_format_00003_ideaunit_v0_0_0,
    _get_headers_list,
    _generate_stone_dataframe,
    get_stoneref,
)
from src.stone.examples.stone_env import src_stone_dir


def test_config_str_functions_ReturnObjs():
    # ESTABLISH / WHEN / THEN
    assert real_id_str() == "real_id"
    assert owner_id_str() == "owner_id"
    assert acct_id_str() == "acct_id"
    assert acct_pool_str() == "acct_pool"
    assert debtit_score_str() == "debtit_score"
    assert credit_score_str() == "credit_score"
    assert debtit_vote_str() == "debtit_vote"
    assert credit_vote_str() == "credit_vote"
    assert jaar_format_00001_acct_v0_0_0() == "jaar_format_00001_acct_v0_0_0"
    x0002_stone = "jaar_format_00002_membership_v0_0_0"
    assert jaar_format_00002_membership_v0_0_0() == x0002_stone
    x0003_stone = "jaar_format_00003_ideaunit_v0_0_0"
    assert jaar_format_00003_ideaunit_v0_0_0() == x0003_stone


def test_get_stone_formats_dir_ReturnsObj():
    # ESTABLISH / WHEN
    stone_dir = get_stone_formats_dir()
    # THEN
    print(f"{stone_dir=}")
    assert stone_dir == f"{(src_stone_dir())}/stone_formats"


def test_get_stone_filenames_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    x_filenames = get_stone_filenames()
    # THEN
    print(f"{x_filenames=}")
    assert jaar_format_00001_acct_v0_0_0() in x_filenames
    assert jaar_format_00002_membership_v0_0_0() in x_filenames
    assert jaar_format_00003_ideaunit_v0_0_0() in x_filenames


def test_get_stoneref_ReturnsObj():
    # ESTABLISH
    stone_name_00001 = jaar_format_00001_acct_v0_0_0()

    # WHEN
    x_stoneref = get_stoneref(stone_name_00001)

    # THEN
    assert x_stoneref.stone_name == stone_name_00001
    assert x_stoneref.atom_category == bud_acctunit_text()
    assert x_stoneref._stonecolumns != {}
    assert len(x_stoneref._stonecolumns) == 5


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_00001_headers = _get_headers_list(jaar_format_00001_acct_v0_0_0())

    # THEN
    # print(f"{format_00001_headers=}")
    assert format_00001_headers == [
        "real_id",
        "owner_id",
        "acct_id",
        "credit_score",
        "debtit_score",
    ]


def test__generate_stone_dataframe_ReturnsCorrectObj():
    # ESTABLISH
    empty_d2 = []
    # WHEN
    x_df = _generate_stone_dataframe(empty_d2, jaar_format_00001_acct_v0_0_0())
    # THEN
    assert list(x_df.columns) == _get_headers_list(jaar_format_00001_acct_v0_0_0())


def for_all_stones__generate_stone_dataframe():
    # Catching broad exceptions can make debugging difficult. Consider catching more specific exceptions or at least logging the exception details.
    empty_d2 = []
    for x_filename in get_stone_filenames():
        try:
            _generate_stone_dataframe(empty_d2, x_filename)
        except Exception:
            print(f"_generate_stone_dataframe failed for {x_filename=}")
            return False
    return True


def test__generate_stone_dataframe_ReturnsCorrectObjForEvery_stone():
    # ESTABLISH / WHEN / THEN
    assert for_all_stones__generate_stone_dataframe()


def test_stone_FilesExist():
    # ESTABLISH
    stone_dir = get_stone_formats_dir()

    # WHEN
    stone_files = dir_files(stone_dir, True)

    # THEN
    stone_filenames = set(stone_files.keys())
    assert stone_filenames == get_stone_filenames()
    assert len(stone_filenames) == len(get_stone_filenames())


def test_get_stoneref_HasCorrectAttrs_jaar_format_00001_acct_v0_0_0():
    # ESTABLISH
    stone_name = jaar_format_00001_acct_v0_0_0()

    # WHEN
    format_00001_stoneref = get_stoneref(stone_name)

    # THEN
    real_id_stonecolumn = format_00001_stoneref.get_stonecolumn(real_id_str())
    owner_id_stonecolumn = format_00001_stoneref.get_stonecolumn(owner_id_str())
    acct_id_stonecolumn = format_00001_stoneref.get_stonecolumn(acct_id_str())
    credit_score_stonecolumn = format_00001_stoneref.get_stonecolumn(credit_score_str())
    debtit_score_stonecolumn = format_00001_stoneref.get_stonecolumn(debtit_score_str())
    assert len(format_00001_stoneref._stonecolumns) == 5

    assert real_id_stonecolumn.column_order == 0
    assert owner_id_stonecolumn.column_order == 1
    assert acct_id_stonecolumn.column_order == 2
    assert credit_score_stonecolumn.column_order == 3
    assert debtit_score_stonecolumn.column_order == 4


def test_get_stoneref_HasCorrectAttrs_jaar_format_00002_membership_v0_0_0():
    # ESTABLISH
    stone_name = jaar_format_00002_membership_v0_0_0()

    # WHEN
    format_00002_stoneref = get_stoneref(stone_name)

    # THEN
    real_id_stonecolumn = format_00002_stoneref.get_stonecolumn(real_id_str())
    owner_id_stonecolumn = format_00002_stoneref.get_stonecolumn(owner_id_str())
    acct_id_stonecolumn = format_00002_stoneref.get_stonecolumn(acct_id_str())
    group_id_stonecolumn = format_00002_stoneref.get_stonecolumn(group_id_str())
    credit_vote_stonecolumn = format_00002_stoneref.get_stonecolumn(credit_vote_str())
    debtit_vote_stonecolumn = format_00002_stoneref.get_stonecolumn(debtit_vote_str())
    assert len(format_00002_stoneref._stonecolumns) == 6

    assert real_id_stonecolumn.column_order == 0
    assert owner_id_stonecolumn.column_order == 1
    assert acct_id_stonecolumn.column_order == 2
    assert group_id_stonecolumn.column_order == 3
    assert debtit_vote_stonecolumn.column_order == 5
    assert credit_vote_stonecolumn.column_order == 4


def test_get_stoneref_HasCorrectAttrs_jaar_format_00003_ideaunit_v0_0_0():
    # ESTABLISH
    stone_name = jaar_format_00003_ideaunit_v0_0_0()

    # WHEN
    format_00003_stoneref = get_stoneref(stone_name)

    # THEN
    real_id_stonecolumn = format_00003_stoneref.get_stonecolumn(real_id_str())
    owner_id_stonecolumn = format_00003_stoneref.get_stonecolumn(owner_id_str())
    parent_road_stonecolumn = format_00003_stoneref.get_stonecolumn(parent_road_str())
    label_stonecolumn = format_00003_stoneref.get_stonecolumn(label_str())
    print(f"{format_00003_stoneref._stonecolumns.keys()=}")
    print(f"{format_00003_stoneref._stonecolumns.get(mass_str())=}")
    mass_stonecolumn = format_00003_stoneref.get_stonecolumn(mass_str())
    print(f"{mass_stonecolumn=}")
    pledge_stonecolumn = format_00003_stoneref.get_stonecolumn(pledge_str())
    assert len(format_00003_stoneref._stonecolumns) == 6

    assert real_id_stonecolumn.column_order == 0
    assert owner_id_stonecolumn.column_order == 1
    assert parent_road_stonecolumn.column_order == 3
    assert label_stonecolumn.column_order == 5
    assert mass_stonecolumn.column_order == 4
    assert pledge_stonecolumn.column_order == 2