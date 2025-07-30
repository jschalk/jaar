from src.a00_data_toolbox.file_toolbox import get_dir_file_strs
from src.a06_believer_logic.test._util.a06_str import (
    addin_str,
    begin_str,
    belief_label_str,
    believer_name_str,
    believer_partnerunit_str,
    believerunit_str,
    close_str,
    denom_str,
    gogo_want_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    morph_str,
    numor_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    partner_pool_str,
    plan_rope_str,
    star_str,
    stop_want_str,
    task_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a15_belief_logic.test._util.a15_str import beliefunit_str
from src.a17_idea_logic.idea_config import (
    get_default_sorted_list,
    get_idea_elements_sort_order,
    get_idea_format_filenames,
    get_idea_format_headers,
    get_idea_formats_dir,
    get_idearef_from_file,
    idea_format_00013_planunit_v0_0_0,
    idea_format_00019_planunit_v0_0_0,
    idea_format_00020_believer_partner_membership_v0_0_0,
    idea_format_00021_believer_partnerunit_v0_0_0,
)
from src.a17_idea_logic.idea_main import (
    _generate_idea_dataframe,
    _get_headers_list,
    get_idearef_obj,
)
from src.a17_idea_logic.test._util.a17_env import src_module_dir
from src.a17_idea_logic.test._util.a17_str import attributes_str


def test_config_str_functions_ReturnsObjs():
    # ESTABLISH / WHEN / THEN
    assert partner_pool_str() == "partner_pool"
    assert partner_debt_points_str() == "partner_debt_points"
    assert partner_cred_points_str() == "partner_cred_points"
    assert group_debt_points_str() == "group_debt_points"
    assert group_cred_points_str() == "group_cred_points"
    x00021_idea = "idea_format_00021_believer_partnerunit_v0_0_0"
    assert idea_format_00021_believer_partnerunit_v0_0_0() == x00021_idea
    x00020_idea = "idea_format_00020_believer_partner_membership_v0_0_0"
    assert idea_format_00020_believer_partner_membership_v0_0_0() == x00020_idea
    x0003_idea = "idea_format_00013_planunit_v0_0_0"
    assert idea_format_00013_planunit_v0_0_0() == x0003_idea


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
    idea_name_00021 = idea_format_00021_believer_partnerunit_v0_0_0()

    # WHEN
    x_idearef = get_idearef_obj(idea_name_00021)

    # THEN
    assert x_idearef.idea_name == idea_name_00021
    assert set(x_idearef.dimens) == {
        believer_partnerunit_str(),
        believerunit_str(),
        beliefunit_str(),
    }
    assert x_idearef._attributes != {}
    assert len(x_idearef._attributes) == 7


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_00021_headers = _get_headers_list(
        idea_format_00021_believer_partnerunit_v0_0_0()
    )

    # THEN
    # print(f"{format_00001_headers=}")
    assert format_00021_headers == [
        event_int_str(),
        face_name_str(),
        belief_label_str(),
        believer_name_str(),
        partner_name_str(),
        partner_cred_points_str(),
        partner_debt_points_str(),
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
    # return create_sorted_planatenated_str(list(idea_attributes))


def test_get_sorted_headers_str_ReturnsObj():
    # ESTABLISH / WHEN
    br00021_headers = get_sorted_headers_str(
        idea_format_00021_believer_partnerunit_v0_0_0()
    )
    # THEN
    assert (
        br00021_headers
        == "belief_label,believer_name,partner_name,partner_cred_points,partner_debt_points"
    )

    # ESTABLISH / WHEN
    br00019_headers = get_sorted_headers_str(idea_format_00019_planunit_v0_0_0())

    # THEN
    print(f"{br00019_headers=}")
    plan_headers_str = "belief_label,believer_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want"
    assert br00019_headers == plan_headers_str


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
    x_df = _generate_idea_dataframe(
        empty_d2, idea_format_00021_believer_partnerunit_v0_0_0()
    )
    # THEN
    headers_list = _get_headers_list(idea_format_00021_believer_partnerunit_v0_0_0())
    assert list(x_df.columns) == headers_list


def for_all_ideas__generate_idea_dataframe():
    # Catching brope exceptions can make debugging difficult. Consider catching more specific exceptions or at least logging the exception details.
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


def test_get_idearef_obj_HasCorrectAttrs_idea_format_00021_believer_partnerunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00021_believer_partnerunit_v0_0_0()

    # WHEN
    format_00001_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00001_idearef._attributes) == 7
    assert format_00001_idearef._attributes == {
        "partner_name": {"otx_key": True},
        "partner_cred_points": {"otx_key": False},
        "partner_debt_points": {"otx_key": False},
        "event_int": {"otx_key": True},
        "face_name": {"otx_key": True},
        "belief_label": {"otx_key": True},
        "believer_name": {"otx_key": True},
    }
    headers_list = format_00001_idearef.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == belief_label_str()
    assert headers_list[3] == believer_name_str()
    assert headers_list[4] == partner_name_str()
    assert headers_list[5] == partner_cred_points_str()
    assert headers_list[6] == partner_debt_points_str()


def test_get_idearef_obj_HasCorrectAttrs_idea_format_00020_believer_partner_membership_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00020_believer_partner_membership_v0_0_0()

    # WHEN
    format_00021_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00021_idearef._attributes) == 8
    headers_list = format_00021_idearef.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == belief_label_str()
    assert headers_list[3] == believer_name_str()
    assert headers_list[4] == partner_name_str()
    assert headers_list[5] == group_title_str()
    assert headers_list[6] == group_cred_points_str()
    assert headers_list[7] == group_debt_points_str()


def test_get_idearef_obj_HasCorrectAttrs_idea_format_00013_planunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00013_planunit_v0_0_0()

    # WHEN
    format_00003_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00003_idearef._attributes) == 7
    headers_list = format_00003_idearef.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == belief_label_str()
    assert headers_list[3] == believer_name_str()
    assert headers_list[4] == plan_rope_str()
    assert headers_list[5] == star_str()
    assert headers_list[6] == task_str()


def test_get_idearef_obj_HasCorrectAttrs_idea_format_00019_planunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00019_planunit_v0_0_0()

    # WHEN
    format_00019_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00019_idearef._attributes) == 13
    headers_list = format_00019_idearef.get_headers_list()
    assert headers_list[0] == event_int_str()
    assert headers_list[1] == face_name_str()
    assert headers_list[2] == belief_label_str()
    assert headers_list[3] == believer_name_str()
    assert headers_list[4] == plan_rope_str()
    assert headers_list[5] == begin_str()
    assert headers_list[6] == close_str()
    assert headers_list[7] == addin_str()
    assert headers_list[8] == numor_str()
    assert headers_list[9] == denom_str()
    assert headers_list[10] == morph_str()
    assert headers_list[11] == gogo_want_str()
    assert headers_list[12] == stop_want_str()
