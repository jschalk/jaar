from src.ch01_py.file_toolbox import get_dir_file_strs
from src.ch17_idea.idea_config import (
    get_default_sorted_list,
    get_idea_elements_sort_order,
    get_idea_format_filenames,
    get_idea_format_headers,
    get_idea_formats_dir,
    get_idearef_from_file,
    idea_format_00013_planunit_v0_0_0,
    idea_format_00019_planunit_v0_0_0,
    idea_format_00020_belief_voice_membership_v0_0_0,
    idea_format_00021_belief_voiceunit_v0_0_0,
)
from src.ch17_idea.idea_main import (
    _generate_idea_dataframe,
    _get_headers_list,
    get_idearef_obj,
)
from src.ch17_idea.test._util.ch17_env import src_chapter_dir
from src.ref.ch17_keywords import Ch17Keywords as wx


def test_config_str_functions_ReturnsObjs():
    # ESTABLISH / WHEN / THEN
    x00021_idea = "idea_format_00021_belief_voiceunit_v0_0_0"
    assert idea_format_00021_belief_voiceunit_v0_0_0() == x00021_idea
    x00020_idea = "idea_format_00020_belief_voice_membership_v0_0_0"
    assert idea_format_00020_belief_voice_membership_v0_0_0() == x00020_idea
    x0003_idea = "idea_format_00013_planunit_v0_0_0"
    assert idea_format_00013_planunit_v0_0_0() == x0003_idea


def test_get_idea_formats_dir_ReturnsObj():
    # ESTABLISH / WHEN
    idea_dir = get_idea_formats_dir()
    # THEN
    print(f"{idea_dir=}")
    print(f"{src_chapter_dir()=}")
    # assert idea_dir == create_path(src_chapter_dir(), "idea_formats")
    assert idea_dir == f"{src_chapter_dir()}/idea_formats"


def test_get_idearef_obj_ReturnsObj():
    # ESTABLISH
    idea_name_00021 = idea_format_00021_belief_voiceunit_v0_0_0()

    # WHEN
    x_idearef = get_idearef_obj(idea_name_00021)

    # THEN
    assert x_idearef.idea_name == idea_name_00021
    assert set(x_idearef.dimens) == {
        wx.belief_voiceunit,
        wx.beliefunit,
        wx.momentunit,
    }
    assert x_idearef._attributes != {}
    assert len(x_idearef._attributes) == 7


def test_get_headers_list_ReturnsObj():
    # ESTABLISH / WHEN
    format_00021_headers = _get_headers_list(
        idea_format_00021_belief_voiceunit_v0_0_0()
    )

    # THEN
    # print(f"{format_00001_headers=}")
    assert format_00021_headers == [
        wx.event_int,
        wx.face_name,
        wx.moment_label,
        wx.belief_name,
        wx.voice_name,
        wx.voice_cred_lumen,
        wx.voice_debt_lumen,
    ]


def get_sorted_headers_str(idea_filename):
    x_idearef = get_idearef_from_file(idea_filename)
    idea_attributes = set(x_idearef.get(wx.attributes).keys())
    idea_attributes.remove(wx.face_name)
    idea_attributes.remove(wx.event_int)
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
        idea_format_00021_belief_voiceunit_v0_0_0()
    )
    # THEN
    expected_br00021_headers_str = (
        "moment_label,belief_name,voice_name,voice_cred_lumen,voice_debt_lumen"
    )
    assert br00021_headers == expected_br00021_headers_str

    # ESTABLISH / WHEN
    br00019_headers = get_sorted_headers_str(idea_format_00019_planunit_v0_0_0())

    # THEN
    print(f"{br00019_headers=}")
    expected_plan_headers_str = "moment_label,belief_name,plan_rope,begin,close,addin,numor,denom,morph,gogo_want,stop_want"
    assert br00019_headers == expected_plan_headers_str


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
        empty_d2, idea_format_00021_belief_voiceunit_v0_0_0()
    )
    # THEN
    headers_list = _get_headers_list(idea_format_00021_belief_voiceunit_v0_0_0())
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


def test_get_idearef_obj_HasAttrs_idea_format_00021_belief_voiceunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00021_belief_voiceunit_v0_0_0()

    # WHEN
    format_00001_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00001_idearef._attributes) == 7
    assert format_00001_idearef._attributes == {
        wx.voice_name: {wx.otx_key: True},
        wx.voice_cred_lumen: {wx.otx_key: False},
        wx.voice_debt_lumen: {wx.otx_key: False},
        wx.event_int: {wx.otx_key: True},
        wx.face_name: {wx.otx_key: True},
        wx.moment_label: {wx.otx_key: True},
        wx.belief_name: {wx.otx_key: True},
    }
    headers_list = format_00001_idearef.get_headers_list()
    assert headers_list[0] == wx.event_int
    assert headers_list[1] == wx.face_name
    assert headers_list[2] == wx.moment_label
    assert headers_list[3] == wx.belief_name
    assert headers_list[4] == wx.voice_name
    assert headers_list[5] == wx.voice_cred_lumen
    assert headers_list[6] == wx.voice_debt_lumen


def test_get_idearef_obj_HasAttrs_idea_format_00020_belief_voice_membership_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00020_belief_voice_membership_v0_0_0()

    # WHEN
    format_00021_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00021_idearef._attributes) == 8
    headers_list = format_00021_idearef.get_headers_list()
    assert headers_list[0] == wx.event_int
    assert headers_list[1] == wx.face_name
    assert headers_list[2] == wx.moment_label
    assert headers_list[3] == wx.belief_name
    assert headers_list[4] == wx.voice_name
    assert headers_list[5] == wx.group_title
    assert headers_list[6] == wx.group_cred_lumen
    assert headers_list[7] == wx.group_debt_lumen


def test_get_idearef_obj_HasAttrs_idea_format_00013_planunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00013_planunit_v0_0_0()

    # WHEN
    format_00003_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00003_idearef._attributes) == 7
    headers_list = format_00003_idearef.get_headers_list()
    assert headers_list[0] == wx.event_int
    assert headers_list[1] == wx.face_name
    assert headers_list[2] == wx.moment_label
    assert headers_list[3] == wx.belief_name
    assert headers_list[4] == wx.plan_rope
    assert headers_list[5] == wx.star
    assert headers_list[6] == wx.pledge


def test_get_idearef_obj_HasAttrs_idea_format_00019_planunit_v0_0_0():
    # ESTABLISH
    idea_name = idea_format_00019_planunit_v0_0_0()

    # WHEN
    format_00019_idearef = get_idearef_obj(idea_name)

    # THEN
    assert len(format_00019_idearef._attributes) == 13
    headers_list = format_00019_idearef.get_headers_list()
    assert headers_list[0] == wx.event_int
    assert headers_list[1] == wx.face_name
    assert headers_list[2] == wx.moment_label
    assert headers_list[3] == wx.belief_name
    assert headers_list[4] == wx.plan_rope
    assert headers_list[5] == wx.begin
    assert headers_list[6] == wx.close
    assert headers_list[7] == wx.addin
    assert headers_list[8] == wx.numor
    assert headers_list[9] == wx.denom
    assert headers_list[10] == wx.morph
    assert headers_list[11] == wx.gogo_want
    assert headers_list[12] == wx.stop_want
