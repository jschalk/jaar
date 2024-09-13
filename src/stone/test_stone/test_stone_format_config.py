from src._instrument.python_tool import create_sorted_concatenated_str
from src._instrument.file import dir_files
from src.bud.bud_tool import bud_acctunit_str
from src.change.atom_config import (
    fiscal_id_str,
    owner_id_str,
    acct_id_str,
    group_id_str,
    parent_road_str,
    label_str,
    mass_str,
    pledge_str,
    acct_pool_str,
    debtit_belief_str,
    credit_belief_str,
    debtit_vote_str,
    credit_vote_str,
    begin_str,
    close_str,
    addin_str,
    numor_str,
    denom_str,
    morph_str,
    gogo_want_str,
    stop_want_str,
)
from src.stone.stone import _generate_stone_dataframe, get_stoneref, _get_headers_list
from src.stone.stone_config import (
    get_stone_formats_dir,
    get_stone_filenames,
    get_stoneref_dict,
    stone_format_00003_ideaunit_v0_0_0,
    stone_format_00019_ideaunit_v0_0_0,
    stone_format_00020_bud_acct_membership_v0_0_0,
    stone_format_00021_bud_acctunit_v0_0_0,
    stone_format_00022_bud_idea_awardlink_v0_0_0,
    stone_format_00023_bud_idea_factunit_v0_0_0,
    stone_format_00024_bud_idea_teamlink_v0_0_0,
    stone_format_00025_bud_idea_healerlink_v0_0_0,
    stone_format_00026_bud_idea_reason_premiseunit_v0_0_0,
    stone_format_00027_bud_idea_reasonunit_v0_0_0,
    stone_format_00028_bud_ideaunit_v0_0_0,
    stone_format_00029_budunit_v0_0_0,
    get_stone_format_headers,
    attributes_str,
)
from src.stone.examples.stone_env import src_stone_dir


def test_config_str_functions_ReturnObjs():
    # ESTABLISH / WHEN / THEN
    assert acct_id_str() == "acct_id"
    assert acct_pool_str() == "acct_pool"
    assert debtit_belief_str() == "debtit_belief"
    assert credit_belief_str() == "credit_belief"
    assert debtit_vote_str() == "debtit_vote"
    assert credit_vote_str() == "credit_vote"
    x00021_stone = "stone_format_00021_bud_acctunit_v0_0_0"
    assert stone_format_00021_bud_acctunit_v0_0_0() == x00021_stone
    x00020_stone = "stone_format_00020_bud_acct_membership_v0_0_0"
    assert stone_format_00020_bud_acct_membership_v0_0_0() == x00020_stone
    x0003_stone = "stone_format_00003_ideaunit_v0_0_0"
    assert stone_format_00003_ideaunit_v0_0_0() == x0003_stone


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
    assert stone_format_00021_bud_acctunit_v0_0_0() in x_filenames
    assert stone_format_00020_bud_acct_membership_v0_0_0() in x_filenames
    assert stone_format_00003_ideaunit_v0_0_0() in x_filenames


def test_get_stoneref_ReturnsObj():
    # ESTABLISH
    stone_name_00021 = stone_format_00021_bud_acctunit_v0_0_0()

    # WHEN
    x_stoneref = get_stoneref(stone_name_00021)

    # THEN
    assert x_stoneref.stone_name == stone_name_00021
    assert x_stoneref.atom_categorys == [bud_acctunit_str()]
    assert x_stoneref._stonecolumns != {}
    assert len(x_stoneref._stonecolumns) == 5


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_00021_headers = _get_headers_list(stone_format_00021_bud_acctunit_v0_0_0())

    # THEN
    # print(f"{format_00001_headers=}")
    assert format_00021_headers == [
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        "debtit_belief",
        "credit_belief",
    ]


def get_sorted_headers(stone_filename):
    x_stoneref = get_stoneref_dict(stone_filename)
    stone_attributes = list(x_stoneref.get(attributes_str()).keys())
    return create_sorted_concatenated_str(stone_attributes)


def test_get_sorted_headers_ReturnsObj():
    # ESTABLISH / WHEN
    headers = get_sorted_headers(stone_format_00021_bud_acctunit_v0_0_0())
    # THEN
    assert headers == "acct_id,credit_belief,debtit_belief,fiscal_id,owner_id"

    # ESTABLISH / WHEN
    headers = get_sorted_headers(stone_format_00019_ideaunit_v0_0_0())
    # THEN
    idea_headers_str = "addin,begin,close,denom,fiscal_id,gogo_want,label,morph,numor,owner_id,parent_road,stop_want"
    assert headers == idea_headers_str


def check_sorted_headers_exist(stone_format_filename: str, x_headers: dict):
    sorted_headers = get_sorted_headers(stone_format_filename)
    print(f"{stone_format_filename=} {sorted_headers=}")
    assert x_headers.get(sorted_headers) == stone_format_filename


def test_get_stone_format_headers_ReturnsObj():
    # ESTABLISH / WHEN
    x_headers = get_stone_format_headers()

    # THEN
    # print(f"{set(get_stone_format_headers().values())=}")
    for x_stone_filename in get_stone_filenames():
        check_sorted_headers_exist(x_stone_filename, x_headers)
    assert len(x_headers) == len(get_stone_filenames())
    assert set(x_headers.values()) == get_stone_filenames()


def test__generate_stone_dataframe_ReturnsCorrectObj():
    # ESTABLISH
    empty_d2 = []
    # WHEN
    x_df = _generate_stone_dataframe(empty_d2, stone_format_00021_bud_acctunit_v0_0_0())
    # THEN
    headers_list = _get_headers_list(stone_format_00021_bud_acctunit_v0_0_0())
    assert list(x_df.columns) == headers_list


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
    print(f"{stone_filenames=}")
    assert stone_filenames == get_stone_filenames()
    assert len(stone_filenames) == len(get_stone_filenames())


def test_get_stoneref_HasCorrectAttrs_stone_format_00021_bud_acctunit_v0_0_0():
    # ESTABLISH
    stone_name = stone_format_00021_bud_acctunit_v0_0_0()

    # WHEN
    format_00001_stoneref = get_stoneref(stone_name)

    # THEN
    fiscal_id_stonecolumn = format_00001_stoneref.get_stonecolumn(fiscal_id_str())
    owner_id_stonecolumn = format_00001_stoneref.get_stonecolumn(owner_id_str())
    acct_id_stonecolumn = format_00001_stoneref.get_stonecolumn(acct_id_str())
    credit_belief_stonecolumn = format_00001_stoneref.get_stonecolumn(
        credit_belief_str()
    )
    debtit_belief_stonecolumn = format_00001_stoneref.get_stonecolumn(
        debtit_belief_str()
    )
    assert len(format_00001_stoneref._stonecolumns) == 5

    assert fiscal_id_stonecolumn.column_order == 0
    assert owner_id_stonecolumn.column_order == 1
    assert acct_id_stonecolumn.column_order == 2
    assert credit_belief_stonecolumn.column_order == 4
    assert debtit_belief_stonecolumn.column_order == 3


def test_get_stoneref_HasCorrectAttrs_stone_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    stone_name = stone_format_00020_bud_acct_membership_v0_0_0()

    # WHEN
    format_00021_stoneref = get_stoneref(stone_name)

    # THEN
    fiscal_id_stonecolumn = format_00021_stoneref.get_stonecolumn(fiscal_id_str())
    owner_id_stonecolumn = format_00021_stoneref.get_stonecolumn(owner_id_str())
    acct_id_stonecolumn = format_00021_stoneref.get_stonecolumn(acct_id_str())
    group_id_stonecolumn = format_00021_stoneref.get_stonecolumn(group_id_str())
    credit_vote_stonecolumn = format_00021_stoneref.get_stonecolumn(credit_vote_str())
    debtit_vote_stonecolumn = format_00021_stoneref.get_stonecolumn(debtit_vote_str())
    assert len(format_00021_stoneref._stonecolumns) == 6

    assert fiscal_id_stonecolumn.column_order == 0
    assert owner_id_stonecolumn.column_order == 1
    assert acct_id_stonecolumn.column_order == 2
    assert group_id_stonecolumn.column_order == 3
    assert debtit_vote_stonecolumn.column_order == 4
    assert credit_vote_stonecolumn.column_order == 5


def test_get_stoneref_HasCorrectAttrs_stone_format_00003_ideaunit_v0_0_0():
    # ESTABLISH
    stone_name = stone_format_00003_ideaunit_v0_0_0()

    # WHEN
    format_00003_stoneref = get_stoneref(stone_name)

    # THEN
    fiscal_id_stonecolumn = format_00003_stoneref.get_stonecolumn(fiscal_id_str())
    owner_id_stonecolumn = format_00003_stoneref.get_stonecolumn(owner_id_str())
    parent_road_stonecolumn = format_00003_stoneref.get_stonecolumn(parent_road_str())
    label_stonecolumn = format_00003_stoneref.get_stonecolumn(label_str())
    print(f"{format_00003_stoneref._stonecolumns.keys()=}")
    print(f"{format_00003_stoneref._stonecolumns.get(mass_str())=}")
    mass_stonecolumn = format_00003_stoneref.get_stonecolumn(mass_str())
    print(f"{mass_stonecolumn=}")
    pledge_stonecolumn = format_00003_stoneref.get_stonecolumn(pledge_str())
    assert len(format_00003_stoneref._stonecolumns) == 6

    assert fiscal_id_stonecolumn.column_order == 0
    assert owner_id_stonecolumn.column_order == 1
    assert parent_road_stonecolumn.column_order == 3
    assert label_stonecolumn.column_order == 5
    assert mass_stonecolumn.column_order == 4
    assert pledge_stonecolumn.column_order == 2


def test_get_stoneref_HasCorrectAttrs_stone_format_00019_ideaunit_v0_0_0():
    # ESTABLISH
    stone_name = stone_format_00019_ideaunit_v0_0_0()

    # WHEN
    format_00019_stoneref = get_stoneref(stone_name)

    # THEN
    fiscal_id_stonecolumn = format_00019_stoneref.get_stonecolumn(fiscal_id_str())
    owner_id_stonecolumn = format_00019_stoneref.get_stonecolumn(owner_id_str())
    parent_road_stonecolumn = format_00019_stoneref.get_stonecolumn(parent_road_str())
    label_stonecolumn = format_00019_stoneref.get_stonecolumn(label_str())
    print(f"{format_00019_stoneref._stonecolumns.keys()=}")
    begin_stonecolumn = format_00019_stoneref.get_stonecolumn(begin_str())
    close_stonecolumn = format_00019_stoneref.get_stonecolumn(close_str())
    addin_stonecolumn = format_00019_stoneref.get_stonecolumn(addin_str())
    numor_stonecolumn = format_00019_stoneref.get_stonecolumn(numor_str())
    denom_stonecolumn = format_00019_stoneref.get_stonecolumn(denom_str())
    morph_stonecolumn = format_00019_stoneref.get_stonecolumn(morph_str())
    gogo_want_stonecolumn = format_00019_stoneref.get_stonecolumn(gogo_want_str())
    stop_want_stonecolumn = format_00019_stoneref.get_stonecolumn(stop_want_str())

    assert len(format_00019_stoneref._stonecolumns) == 12

    assert fiscal_id_stonecolumn.column_order == 0
    assert owner_id_stonecolumn.column_order == 1
    assert parent_road_stonecolumn.column_order == 2
    assert label_stonecolumn.column_order == 3
    assert begin_stonecolumn.column_order == 4
    assert close_stonecolumn.column_order == 5
    assert addin_stonecolumn.column_order == 6
    assert numor_stonecolumn.column_order == 7
    assert denom_stonecolumn.column_order == 8
    assert morph_stonecolumn.column_order == 9
    assert gogo_want_stonecolumn.column_order == 10
    assert stop_want_stonecolumn.column_order == 11
