from src.f00_instrument.dict_toolbox import create_sorted_concatenated_str
from src.f00_instrument.file import get_dir_file_strs
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_gift.atom_config import (
    face_id_str,
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
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.brick import (
    _generate_brick_dataframe,
    get_brickref_obj,
    _get_headers_list,
)
from src.f09_brick.brick_config import (
    get_brick_formats_dir,
    get_brick_format_filenames,
    get_brickref_from_file,
    brick_format_00013_itemunit_v0_0_0,
    brick_format_00019_itemunit_v0_0_0,
    brick_format_00020_bud_acct_membership_v0_0_0,
    brick_format_00021_bud_acctunit_v0_0_0,
    brick_format_00022_bud_item_awardlink_v0_0_0,
    brick_format_00023_bud_item_factunit_v0_0_0,
    brick_format_00024_bud_item_teamlink_v0_0_0,
    brick_format_00025_bud_item_healerlink_v0_0_0,
    brick_format_00026_bud_item_reason_premiseunit_v0_0_0,
    brick_format_00027_bud_item_reasonunit_v0_0_0,
    brick_format_00028_bud_itemunit_v0_0_0,
    brick_format_00029_budunit_v0_0_0,
    get_brick_format_headers,
    attributes_str,
)
from src.f09_brick.examples.brick_env import src_brick_dir


def test_config_str_functions_ReturnObjs():
    # ESTABLISH / WHEN / THEN
    assert acct_id_str() == "acct_id"
    assert acct_pool_str() == "acct_pool"
    assert debtit_belief_str() == "debtit_belief"
    assert credit_belief_str() == "credit_belief"
    assert debtit_vote_str() == "debtit_vote"
    assert credit_vote_str() == "credit_vote"
    x00021_brick = "brick_format_00021_bud_acctunit_v0_0_0"
    assert brick_format_00021_bud_acctunit_v0_0_0() == x00021_brick
    x00020_brick = "brick_format_00020_bud_acct_membership_v0_0_0"
    assert brick_format_00020_bud_acct_membership_v0_0_0() == x00020_brick
    x0003_brick = "brick_format_00013_itemunit_v0_0_0"
    assert brick_format_00013_itemunit_v0_0_0() == x0003_brick


def test_get_brick_formats_dir_ReturnsObj():
    # ESTABLISH / WHEN
    brick_dir = get_brick_formats_dir()
    # THEN
    print(f"{brick_dir=}")
    assert brick_dir == f"{(src_brick_dir())}/brick_formats"


def test_get_brickref_obj_ReturnsObj():
    # ESTABLISH
    brick_name_00021 = brick_format_00021_bud_acctunit_v0_0_0()

    # WHEN
    x_brickref = get_brickref_obj(brick_name_00021)

    # THEN
    assert x_brickref.brick_name == brick_name_00021
    assert x_brickref.categorys == [bud_acctunit_str()]
    assert x_brickref._attributes != {}
    assert len(x_brickref._attributes) == 7


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_00021_headers = _get_headers_list(brick_format_00021_bud_acctunit_v0_0_0())

    # THEN
    # print(f"{format_00001_headers=}")
    assert format_00021_headers == [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        credit_belief_str(),
        debtit_belief_str(),
    ]


def get_sorted_headers(brick_filename):
    x_brickref = get_brickref_from_file(brick_filename)
    brick_attributes = set(x_brickref.get(attributes_str()).keys())
    brick_attributes.remove(face_id_str())
    brick_attributes.remove(event_id_str())
    return create_sorted_concatenated_str(list(brick_attributes))


def test_get_sorted_headers_ReturnsObj():
    # ESTABLISH / WHEN
    headers = get_sorted_headers(brick_format_00021_bud_acctunit_v0_0_0())
    # THEN
    assert headers == "acct_id,credit_belief,debtit_belief,fiscal_id,owner_id"

    # ESTABLISH / WHEN
    headers = get_sorted_headers(brick_format_00019_itemunit_v0_0_0())
    # THEN
    item_headers_str = "addin,begin,close,denom,fiscal_id,gogo_want,label,morph,numor,owner_id,parent_road,stop_want"
    assert headers == item_headers_str


def check_sorted_headers_exist(brick_format_filename: str, x_headers: dict):
    # print(f"{brick_format_filename=}")
    sorted_headers = get_sorted_headers(brick_format_filename)
    print(f"{brick_format_filename=} {sorted_headers=}")
    assert x_headers.get(sorted_headers) == brick_format_filename


def test_get_brick_format_headers_ReturnsObj():
    # ESTABLISH / WHEN
    x_headers = get_brick_format_headers()

    # THEN
    # print(f"{set(get_brick_format_headers().values())=}")
    # sourcery skip: no-loop-in-tests
    for x_brick_filename in sorted(list(get_brick_format_filenames())):
        check_sorted_headers_exist(x_brick_filename, x_headers)

    print(f"{x_headers=}")
    assert len(x_headers) == len(get_brick_format_filenames())
    assert set(x_headers.values()) == get_brick_format_filenames()


def test__generate_brick_dataframe_ReturnsCorrectObj():
    # ESTABLISH
    empty_d2 = []
    # WHEN
    x_df = _generate_brick_dataframe(empty_d2, brick_format_00021_bud_acctunit_v0_0_0())
    # THEN
    headers_list = _get_headers_list(brick_format_00021_bud_acctunit_v0_0_0())
    assert list(x_df.columns) == headers_list


def for_all_bricks__generate_brick_dataframe():
    # Catching broad exceptions can make debugging difficult. Consider catching more specific exceptions or at least logging the exception details.
    empty_d2 = []
    for x_filename in get_brick_format_filenames():
        try:
            _generate_brick_dataframe(empty_d2, x_filename)
        except Exception:
            print(f"_generate_brick_dataframe failed for {x_filename=}")
            return False
    return True


def test__generate_brick_dataframe_ReturnsCorrectObjForEvery_brick():
    # ESTABLISH / WHEN / THEN
    assert for_all_bricks__generate_brick_dataframe()


def test_brick_FilesExist():
    # ESTABLISH
    brick_dir = get_brick_formats_dir()

    # WHEN
    brick_files = get_dir_file_strs(brick_dir, True)

    # THEN
    brick_filenames = set(brick_files.keys())
    print(f"{brick_filenames=}")
    assert brick_filenames == get_brick_format_filenames()
    assert len(brick_filenames) == len(get_brick_format_filenames())


def test_get_brickref_obj_HasCorrectAttrs_brick_format_00021_bud_acctunit_v0_0_0():
    # ESTABLISH
    brick_name = brick_format_00021_bud_acctunit_v0_0_0()

    # WHEN
    format_00001_brickref = get_brickref_obj(brick_name)

    # THEN
    assert len(format_00001_brickref._attributes) == 7
    assert format_00001_brickref._attributes == {
        "acct_id": {"otx_key": True},
        "credit_belief": {"otx_key": False},
        "debtit_belief": {"otx_key": False},
        "event_id": {"otx_key": True},
        "face_id": {"otx_key": True},
        "fiscal_id": {"otx_key": True},
        "owner_id": {"otx_key": True},
    }
    headers_list = format_00001_brickref.get_headers_list()
    assert headers_list[0] == face_id_str()
    assert headers_list[1] == event_id_str()
    assert headers_list[2] == fiscal_id_str()
    assert headers_list[3] == owner_id_str()
    assert headers_list[4] == acct_id_str()
    assert headers_list[5] == credit_belief_str()
    assert headers_list[6] == debtit_belief_str()


def test_get_brickref_obj_HasCorrectAttrs_brick_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    brick_name = brick_format_00020_bud_acct_membership_v0_0_0()

    # WHEN
    format_00021_brickref = get_brickref_obj(brick_name)

    # THEN
    assert len(format_00021_brickref._attributes) == 8
    headers_list = format_00021_brickref.get_headers_list()
    assert headers_list[0] == face_id_str()
    assert headers_list[1] == event_id_str()
    assert headers_list[2] == fiscal_id_str()
    assert headers_list[3] == owner_id_str()
    assert headers_list[4] == acct_id_str()
    assert headers_list[5] == group_id_str()
    assert headers_list[6] == credit_vote_str()
    assert headers_list[7] == debtit_vote_str()


def test_get_brickref_obj_HasCorrectAttrs_brick_format_00013_itemunit_v0_0_0():
    # ESTABLISH
    brick_name = brick_format_00013_itemunit_v0_0_0()

    # WHEN
    format_00003_brickref = get_brickref_obj(brick_name)

    # THEN
    assert len(format_00003_brickref._attributes) == 8
    headers_list = format_00003_brickref.get_headers_list()
    assert headers_list[0] == face_id_str()
    assert headers_list[1] == event_id_str()
    assert headers_list[2] == fiscal_id_str()
    assert headers_list[3] == owner_id_str()
    assert headers_list[4] == parent_road_str()
    assert headers_list[5] == label_str()
    assert headers_list[6] == mass_str()
    assert headers_list[7] == pledge_str()


def test_get_brickref_obj_HasCorrectAttrs_brick_format_00019_itemunit_v0_0_0():
    # ESTABLISH
    brick_name = brick_format_00019_itemunit_v0_0_0()

    # WHEN
    format_00019_brickref = get_brickref_obj(brick_name)

    # THEN
    assert len(format_00019_brickref._attributes) == 14
    headers_list = format_00019_brickref.get_headers_list()
    assert headers_list[0] == face_id_str()
    assert headers_list[1] == event_id_str()
    assert headers_list[2] == fiscal_id_str()
    assert headers_list[3] == owner_id_str()
    assert headers_list[4] == parent_road_str()
    assert headers_list[5] == label_str()
    assert headers_list[6] == begin_str()
    assert headers_list[7] == close_str()
    assert headers_list[8] == addin_str()
    assert headers_list[9] == numor_str()
    assert headers_list[10] == denom_str()
    assert headers_list[11] == morph_str()
    assert headers_list[12] == gogo_want_str()
    assert headers_list[13] == stop_want_str()
