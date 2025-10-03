from src.ch17_idea_logic.idea_main import IdeaRef, idearef_shop
from src.ref.ch17_keywords import Ch17Keywords as wx


def test_IdeaRef_Exists():
    # ESTABLISH / WHEN
    x_idearef = IdeaRef()

    # THEN
    assert not x_idearef.idea_name
    assert not x_idearef.dimens
    assert not x_idearef._attributes


def test_idearef_shop_ReturnsObj():
    # ESTABLISH
    x1_idea_name = "0001"

    # WHEN
    x_idearef = idearef_shop(x_idea_name=x1_idea_name, x_dimens=[wx.belief_voiceunit])

    # THEN
    assert x_idearef.idea_name == x1_idea_name
    assert x_idearef.dimens == [wx.belief_voiceunit]
    assert x_idearef._attributes == {}


def test_IdeaRef_set_attribute_SetsAttr():
    # ESTABLISH
    x_idearef = idearef_shop("0003", wx.belief_voiceunit)
    x_attribute = "1"
    assert x_idearef._attributes == {}

    # WHEN
    x_idearef.set_attribute(x_attribute, True)

    # THEN
    assert x_idearef._attributes != {}
    assert x_idearef._attributes == {x_attribute: {"otx_key": True}}


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH

    x_idearef = idearef_shop("0003", wx.belief_voiceunit)

    # WHEN
    x_headers_list = x_idearef.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", wx.belief_voiceunit)
    x3_idearef.set_attribute(wx.group_title, True)

    # WHEN
    x_headers_list = x3_idearef.get_headers_list()

    # THEN
    assert x_headers_list == [wx.group_title]


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", wx.belief_voiceunit)
    x3_idearef.set_attribute(wx.plan_rope, True)
    x3_idearef.set_attribute(wx.group_title, False)
    x3_idearef.set_attribute(wx.voice_name, True)

    # WHEN
    x_headers_list = x3_idearef.get_headers_list()

    # THEN
    assert x_headers_list == [wx.voice_name, wx.group_title, wx.plan_rope]


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_idearef = idearef_shop("0003", wx.belief_voiceunit)

    # WHEN
    x_otx_keys_list = x_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == []


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", wx.belief_voiceunit)
    x3_idearef.set_attribute(wx.group_title, True)

    # WHEN
    x_otx_keys_list = x3_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [wx.group_title]


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", wx.belief_voiceunit)
    x3_idearef.set_attribute(wx.plan_rope, True)
    x3_idearef.set_attribute(wx.group_title, False)
    x3_idearef.set_attribute(wx.voice_name, True)

    # WHEN
    x_otx_keys_list = x3_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [wx.voice_name, wx.plan_rope]


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_idearef = idearef_shop("0003", wx.belief_voiceunit)

    # WHEN
    x_otx_values_list = x_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", wx.belief_voiceunit)
    x3_idearef.set_attribute(wx.group_title, True)

    # WHEN
    x_otx_values_list = x3_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", wx.belief_voiceunit)
    x3_idearef.set_attribute(wx.plan_rope, True)
    x3_idearef.set_attribute(wx.group_title, False)
    x3_idearef.set_attribute(wx.reason_context, False)
    x3_idearef.set_attribute(wx.voice_name, False)

    # WHEN
    x_otx_values_list = x3_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == [
        wx.voice_name,
        wx.group_title,
        wx.reason_context,
    ]
