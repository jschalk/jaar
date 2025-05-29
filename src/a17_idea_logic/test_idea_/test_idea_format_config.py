from src.a00_data_toolbox.file_toolbox import get_dir_file_strs
from src.a02_finance_logic._test_util.a02_str import owner_name_str, fisc_label_str
from src.a06_bud_logic._test_util.a06_str import (
    budunit_str,
    bud_acctunit_str,
    face_name_str,
    event_int_str,
    acct_name_str,
    group_title_str,
    mass_str,
    concept_way_str,
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
from src.a15_fisc_logic._test_util.a15_str import fiscunit_str
from src.a17_idea_logic.idea import (
    _generate_idea_dataframe,
    get_idearef_obj,
    _get_headers_list,
)
from src.a17_idea_logic._test_util.a17_str import attributes_str
from src.a17_idea_logic.idea_config import (
    get_idea_formats_dir,
    get_idea_format_filenames,
    get_idearef_from_file,
    idea_format_00013_conceptunit_v0_0_0,
    idea_format_00019_conceptunit_v0_0_0,
    idea_format_00020_bud_acct_membership_v0_0_0,
    idea_format_00021_bud_acctunit_v0_0_0,
    get_idea_format_headers,
    get_idea_elements_sort_order,
    get_default_sorted_list,
)
from src.a17_idea_logic._test_util.a17_env import src_module_dir


def test_config_str_functions_ReturnsObjs():
    # ESTABLISH / WHEN / THEN
    assert acct_pool_str() == "acct_pool"
    assert debtit_belief_str() == "debtit_belief"
    assert credit_belief_str() == "credit_belief"
    assert debtit_vote_str() == "debtit_vote"
    assert credit_vote_str() == "credit_vote"
    x00021_idea = "idea_format_00021_bud_acctunit_v0_0_0"
    assert idea_format_00021_bud_acctunit_v0_0_0() == x00021_idea
    x00020_idea = "idea_format_00020_bud_acct_membership_v0_0_0"
    assert idea_format_00020_bud_acct_membership_v0_0_0() == x00020_idea
    x0003_idea = "idea_format_00013_conceptunit_v0_0_0"
    assert idea_format_00013_conceptunit_v0_0_0() == x0003_idea


def test_get_idea_formats_dir_ReturnsObj():
    # ESTABLISH / WHEN
    idea_dir = get_idea_formats_dir()
    # THEN
    print(f"{idea_dir=}")
    print(f"{src_module_dir()=}")
    # assert idea_dir == create_path(src_module_dir(), "idea_formats")
    assert idea_dir == f"{src_module_dir()}/idea_formats"


def test_get_idearef_obj_ReturnsObj():
    # ESTABLISH
    idea_name_00021 = idea_format_00021_bud_acctunit_v0_0_0()

    # WHEN
    x_idearef = get_idearef_obj(idea_name_00021)

    # THEN
    assert x_idearef.idea_name == idea_name_00021
    assert set(x_idearef.dimens) == {bud_acctunit_str(), budunit_str(), fiscunit_str()}
    assert x_idearef._attributes != {}
    assert len(x_idearef._attributes) == 7


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_00021_headers = _get_headers_list(idea_format_00021_bud_acctunit_v0_0_0())

    # THEN
    # print(f"{format_00001_headers=}")
    assert format_00021_headers == [
        event_int_str(),
        face_name_str(),
        fisc_label_str(),
        owner_name_str(),
        acct_name_str(),
        credit_belief_str(),
        debtit_belief_str(),
    ]


def get_sorted_headers_str(idea_filename):
    x_idearef = get_idearef_from_file(idea_filename)
    idea_attributes = set(x_idearef.get(attributes_str()).keys())
    idea_attributes.remove(face_name_str())
    idea_attributes.remove(event_int_str())
    print(f"{idea_attributes=}")
    attr_sort = get_idea_elements_sort_order()
    idea_attributes = get_default_sorted_list(idea_attributes, attr_sort)
    print(f"{idea_attributes=}")
    header_str = "".join(f",{x_header}" for x_header in idea_attributes)
    return header_str[1:]
    # return create_sorted_concatenated_str(list(idea_attributes))


def test_get_sorted_headers_str_ReturnsObj():
    # ESTABLISH / WHEN
    br00021_headers = get_sorted_headers_str(idea_format_00021_bud_acctunit_v0_0_0())
    # THEN
    assert (
        br00021_headers == "fisc_label,owner_name,acct_name,credit_belief,debtit_belief"
    )

    # ESTABLISH / WHEN
    br00019_headers = get_sorted_headers_str(idea_format_00019_conceptunit_v0_0_0())

    # THEN
    print(f"{br00019_headers=}")
    concept_headers_str = "fisc_label,owner_name,concept_way,begin,close,addin,numor,denom,morph,gogo_want,stop_want"
    assert br00019_headers == concept_headers_str


def check_sorted_headers_exist(idea_format_filename: str, x_headers: dict):
    # print(f"{idea_format_filename=}")
    sorted_headers = get_sorted_headers_str(idea_format_filename)
    print(f"{idea_format_filename=} {sorted_headers=}")
    assert x_headers.get(sorted_headers) == idea_format_filename


def test_get_idea_format_headers_ReturnsObj():
    # ESTABLISH / WHEN
    x_headers = get_idea_format_headers()

    # THEN
    # print(f"{set(get_idea_format_headers().values())=}")
    # sourcery skip: no-loop-in-tests
    for x_idea_filename in sorted(list(get_idea_format_filenames())):
        check_sorted_headers_exist(x_idea_filename, x_headers)

    print(f"{x_headers=}")
    assert len(x_headers) == len(get_idea_format_filenames())
    assert set(x_headers.values()) == get_idea_format_filenames()


def test__generate_idea_dataframe_ReturnsObj():
    # ESTABLISH
    empty_d2 = []
    # WHEN
    x_df = _generate_idea_dataframe(empty_d2, idea_format_00021_bud_acctunit_v0_0_0())
    # THEN
    headers_list = _get_headers_list(idea_format_00021_bud_acctunit_v0_0_0())
    assert list(x_df.columns) == headers_list


def for_all_ideas__generate_idea_dataframe():
    # Catching bway exceptions can make debugging difficult. Consider catching more specific exceptions or at least logging the exception details.
    empty_d2 = []
    for x_filename in get_idea_format_filenames():
        try:
            _generate_idea_dataframe(empty_d2, x_filename)
        except Exception:
            print(f"_generate_idea_dataframe failed for {x_filename=}")
            return False
    return True


def test__generate_idea_dataframe_ReturnsObjForEvery_idea():
    # ESTABLISH / WHEN / THEN
    assert for_all_ideas__generate_idea_dataframe()


def test_idea_FilesExist():
    # ESTABLISH
    idea_dir = get_idea_formats_dir()

    # WHEN
    idea_files = get_dir_file_strs(idea_dir, True)

    # THEN
    idea_filenames = set(idea_files.keys())
    print(f"{idea_filenames=}")
    assert idea_filenames == get_idea_format_filenames()
    assert len(idea_filenames) == len(get_idea_format_filenames())


def test_get_idearef_obj_HasCorrectAttrs_idea_format_00021_bud_acctunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00021_bud_acctunit_v0_0_0()

    # WHEN
    format_00001_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00001_idearef._attributes) == 7
    assert format_00001_idearef._attributes == {
        "acct_name": {"otx_key": True},
        "credit_belief": {"otx_key": False},
        "debtit_belief": {"otx_key": False},
        "event_int": {"otx_key": True},
        "face_name": {"otx_key": True},
        "fisc_label": {"otx_key": True},
        "owner_name": {"otx_key": True},
    }
    headers_list = format_00001_idearef.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == fisc_label_str()
    assert headers_list[3] == owner_name_str()
    assert headers_list[4] == acct_name_str()
    assert headers_list[5] == credit_belief_str()
    assert headers_list[6] == debtit_belief_str()


def test_get_idearef_obj_HasCorrectAttrs_idea_format_00020_bud_acct_membership_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00020_bud_acct_membership_v0_0_0()

    # WHEN
    format_00021_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00021_idearef._attributes) == 8
    headers_list = format_00021_idearef.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == fisc_label_str()
    assert headers_list[3] == owner_name_str()
    assert headers_list[4] == acct_name_str()
    assert headers_list[5] == group_title_str()
    assert headers_list[6] == credit_vote_str()
    assert headers_list[7] == debtit_vote_str()


def test_get_idearef_obj_HasCorrectAttrs_idea_format_00013_conceptunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00013_conceptunit_v0_0_0()

    # WHEN
    format_00003_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00003_idearef._attributes) == 7
    headers_list = format_00003_idearef.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == fisc_label_str()
    assert headers_list[3] == owner_name_str()
    assert headers_list[4] == concept_way_str()
    assert headers_list[5] == mass_str()
    assert headers_list[6] == pledge_str()


def test_get_idearef_obj_HasCorrectAttrs_idea_format_00019_conceptunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00019_conceptunit_v0_0_0()

    # WHEN
    format_00019_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00019_idearef._attributes) == 13
    headers_list = format_00019_idearef.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == fisc_label_str()
    assert headers_list[3] == owner_name_str()
    assert headers_list[4] == concept_way_str()
    assert headers_list[5] == begin_str()
    assert headers_list[6] == close_str()
    assert headers_list[7] == addin_str()
    assert headers_list[8] == numor_str()
    assert headers_list[9] == denom_str()
    assert headers_list[10] == morph_str()
    assert headers_list[11] == gogo_want_str()
    assert headers_list[12] == stop_want_str()
