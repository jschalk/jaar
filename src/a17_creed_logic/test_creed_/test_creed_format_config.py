from src.a00_data_toolbox.file_toolbox import get_dir_file_strs
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_word_str
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    face_name_str,
    event_int_str,
    acct_name_str,
    group_label_str,
    mass_str,
    idea_way_str,
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
from src.a15_fisc_logic._utils.str_a15 import fiscunit_str
from src.a17_creed_logic.creed import (
    _generate_creed_dataframe,
    get_creedref_obj,
    _get_headers_list,
)
from src.a17_creed_logic._utils.str_a17 import attributes_str
from src.a17_creed_logic.creed_config import (
    get_creed_formats_dir,
    get_creed_format_filenames,
    get_creedref_from_file,
    creed_format_00013_ideaunit_v0_0_0,
    creed_format_00019_ideaunit_v0_0_0,
    creed_format_00020_bud_acct_membership_v0_0_0,
    creed_format_00021_bud_acctunit_v0_0_0,
    creed_format_00022_bud_idea_awardlink_v0_0_0,
    creed_format_00023_bud_idea_factunit_v0_0_0,
    creed_format_00024_bud_idea_laborlink_v0_0_0,
    creed_format_00025_bud_idea_healerlink_v0_0_0,
    creed_format_00026_bud_idea_reason_premiseunit_v0_0_0,
    creed_format_00027_bud_idea_reasonunit_v0_0_0,
    creed_format_00028_bud_ideaunit_v0_0_0,
    creed_format_00029_budunit_v0_0_0,
    get_creed_format_headers,
    get_creed_elements_sort_order,
    get_default_sorted_list,
)
from src.a17_creed_logic._utils.env_a17 import src_module_dir


def test_config_str_functions_ReturnObjs():
    # ESTABLISH / WHEN / THEN
    assert acct_name_str() == "acct_name"
    assert acct_pool_str() == "acct_pool"
    assert debtit_belief_str() == "debtit_belief"
    assert credit_belief_str() == "credit_belief"
    assert debtit_vote_str() == "debtit_vote"
    assert credit_vote_str() == "credit_vote"
    x00021_creed = "creed_format_00021_bud_acctunit_v0_0_0"
    assert creed_format_00021_bud_acctunit_v0_0_0() == x00021_creed
    x00020_creed = "creed_format_00020_bud_acct_membership_v0_0_0"
    assert creed_format_00020_bud_acct_membership_v0_0_0() == x00020_creed
    x0003_creed = "creed_format_00013_ideaunit_v0_0_0"
    assert creed_format_00013_ideaunit_v0_0_0() == x0003_creed


def test_get_creed_formats_dir_ReturnsObj():
    # ESTABLISH / WHEN
    creed_dir = get_creed_formats_dir()
    # THEN
    print(f"{creed_dir=}")
    print(f"{src_module_dir()=}")
    # assert creed_dir == create_path(src_module_dir(), "creed_formats")
    assert creed_dir == f"{src_module_dir()}/creed_formats"


def test_get_creedref_obj_ReturnsObj():
    # ESTABLISH
    creed_name_00021 = creed_format_00021_bud_acctunit_v0_0_0()

    # WHEN
    x_creedref = get_creedref_obj(creed_name_00021)

    # THEN
    assert x_creedref.creed_name == creed_name_00021
    assert set(x_creedref.dimens) == {bud_acctunit_str(), budunit_str(), fiscunit_str()}
    assert x_creedref._attributes != {}
    assert len(x_creedref._attributes) == 7


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_00021_headers = _get_headers_list(creed_format_00021_bud_acctunit_v0_0_0())

    # THEN
    # print(f"{format_00001_headers=}")
    assert format_00021_headers == [
        event_int_str(),
        face_name_str(),
        fisc_word_str(),
        owner_name_str(),
        acct_name_str(),
        credit_belief_str(),
        debtit_belief_str(),
    ]


def get_sorted_headers_str(creed_filename):
    x_creedref = get_creedref_from_file(creed_filename)
    creed_attributes = set(x_creedref.get(attributes_str()).keys())
    creed_attributes.remove(face_name_str())
    creed_attributes.remove(event_int_str())
    print(f"{creed_attributes=}")
    attr_sort = get_creed_elements_sort_order()
    creed_attributes = get_default_sorted_list(creed_attributes, attr_sort)
    print(f"{creed_attributes=}")
    header_str = "".join(f",{x_header}" for x_header in creed_attributes)
    return header_str[1:]
    # return create_sorted_concatenated_str(list(creed_attributes))


def test_get_sorted_headers_str_ReturnsObj():
    # ESTABLISH / WHEN
    br00021_headers = get_sorted_headers_str(creed_format_00021_bud_acctunit_v0_0_0())
    # THEN
    assert (
        br00021_headers == "fisc_word,owner_name,acct_name,credit_belief,debtit_belief"
    )

    # ESTABLISH / WHEN
    br00019_headers = get_sorted_headers_str(creed_format_00019_ideaunit_v0_0_0())

    # THEN
    print(f"{br00019_headers=}")
    idea_headers_str = "fisc_word,owner_name,idea_way,begin,close,addin,numor,denom,morph,gogo_want,stop_want"
    assert br00019_headers == idea_headers_str


def check_sorted_headers_exist(creed_format_filename: str, x_headers: dict):
    # print(f"{creed_format_filename=}")
    sorted_headers = get_sorted_headers_str(creed_format_filename)
    print(f"{creed_format_filename=} {sorted_headers=}")
    assert x_headers.get(sorted_headers) == creed_format_filename


def test_get_creed_format_headers_ReturnsObj():
    # ESTABLISH / WHEN
    x_headers = get_creed_format_headers()

    # THEN
    # print(f"{set(get_creed_format_headers().values())=}")
    # sourcery skip: no-loop-in-tests
    for x_creed_filename in sorted(list(get_creed_format_filenames())):
        check_sorted_headers_exist(x_creed_filename, x_headers)

    print(f"{x_headers=}")
    assert len(x_headers) == len(get_creed_format_filenames())
    assert set(x_headers.values()) == get_creed_format_filenames()


def test__generate_creed_dataframe_ReturnsObj():
    # ESTABLISH
    empty_d2 = []
    # WHEN
    x_df = _generate_creed_dataframe(empty_d2, creed_format_00021_bud_acctunit_v0_0_0())
    # THEN
    headers_list = _get_headers_list(creed_format_00021_bud_acctunit_v0_0_0())
    assert list(x_df.columns) == headers_list


def for_all_creeds__generate_creed_dataframe():
    # Catching bway exceptions can make debugging difficult. Consider catching more specific exceptions or at least logging the exception details.
    empty_d2 = []
    for x_filename in get_creed_format_filenames():
        try:
            _generate_creed_dataframe(empty_d2, x_filename)
        except Exception:
            print(f"_generate_creed_dataframe failed for {x_filename=}")
            return False
    return True


def test__generate_creed_dataframe_ReturnsObjForEvery_creed():
    # ESTABLISH / WHEN / THEN
    assert for_all_creeds__generate_creed_dataframe()


def test_creed_FilesExist():
    # ESTABLISH
    creed_dir = get_creed_formats_dir()

    # WHEN
    creed_files = get_dir_file_strs(creed_dir, True)

    # THEN
    creed_filenames = set(creed_files.keys())
    print(f"{creed_filenames=}")
    assert creed_filenames == get_creed_format_filenames()
    assert len(creed_filenames) == len(get_creed_format_filenames())


def test_get_creedref_obj_HasCorrectAttrs_creed_format_00021_bud_acctunit_v0_0_0():
    # ESTABLISH
    creed_name = creed_format_00021_bud_acctunit_v0_0_0()

    # WHEN
    format_00001_creedref = get_creedref_obj(creed_name)

    # THEN
    assert len(format_00001_creedref._attributes) == 7
    assert format_00001_creedref._attributes == {
        "acct_name": {"otx_key": True},
        "credit_belief": {"otx_key": False},
        "debtit_belief": {"otx_key": False},
        "event_int": {"otx_key": True},
        "face_name": {"otx_key": True},
        "fisc_word": {"otx_key": True},
        "owner_name": {"otx_key": True},
    }
    headers_list = format_00001_creedref.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == fisc_word_str()
    assert headers_list[3] == owner_name_str()
    assert headers_list[4] == acct_name_str()
    assert headers_list[5] == credit_belief_str()
    assert headers_list[6] == debtit_belief_str()


def test_get_creedref_obj_HasCorrectAttrs_creed_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    creed_name = creed_format_00020_bud_acct_membership_v0_0_0()

    # WHEN
    format_00021_creedref = get_creedref_obj(creed_name)

    # THEN
    assert len(format_00021_creedref._attributes) == 8
    headers_list = format_00021_creedref.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == fisc_word_str()
    assert headers_list[3] == owner_name_str()
    assert headers_list[4] == acct_name_str()
    assert headers_list[5] == group_label_str()
    assert headers_list[6] == credit_vote_str()
    assert headers_list[7] == debtit_vote_str()


def test_get_creedref_obj_HasCorrectAttrs_creed_format_00013_ideaunit_v0_0_0():
    # ESTABLISH
    creed_name = creed_format_00013_ideaunit_v0_0_0()

    # WHEN
    format_00003_creedref = get_creedref_obj(creed_name)

    # THEN
    assert len(format_00003_creedref._attributes) == 7
    headers_list = format_00003_creedref.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == fisc_word_str()
    assert headers_list[3] == owner_name_str()
    assert headers_list[4] == idea_way_str()
    assert headers_list[5] == mass_str()
    assert headers_list[6] == pledge_str()


def test_get_creedref_obj_HasCorrectAttrs_creed_format_00019_ideaunit_v0_0_0():
    # ESTABLISH
    creed_name = creed_format_00019_ideaunit_v0_0_0()

    # WHEN
    format_00019_creedref = get_creedref_obj(creed_name)

    # THEN
    assert len(format_00019_creedref._attributes) == 13
    headers_list = format_00019_creedref.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == fisc_word_str()
    assert headers_list[3] == owner_name_str()
    assert headers_list[4] == idea_way_str()
    assert headers_list[5] == begin_str()
    assert headers_list[6] == close_str()
    assert headers_list[7] == addin_str()
    assert headers_list[8] == numor_str()
    assert headers_list[9] == denom_str()
    assert headers_list[10] == morph_str()
    assert headers_list[11] == gogo_want_str()
    assert headers_list[12] == stop_want_str()
