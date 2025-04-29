from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    acct_name_str,
    group_label_str,
    road_str,
    base_str,
)
from src.a17_idea_logic.idea import IdeaRef, idearef_shop


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
    x_idearef = idearef_shop(x_idea_name=x1_idea_name, x_dimens=[bud_acctunit_str()])

    # THEN
    assert x_idearef.idea_name == x1_idea_name
    assert x_idearef.dimens == [bud_acctunit_str()]
    assert x_idearef._attributes == {}


def test_IdeaRef_set_attribute_SetsAttr():
    # ESTABLISH
    x_idearef = idearef_shop("0003", bud_acctunit_str())
    x_attribute = "1"
    assert x_idearef._attributes == {}

    # WHEN
    x_idearef.set_attribute(x_attribute, True)

    # THEN
    assert x_idearef._attributes != {}
    assert x_idearef._attributes == {x_attribute: {"otx_key": True}}


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH

    x_idearef = idearef_shop("0003", bud_acctunit_str())

    # WHEN
    x_headers_list = x_idearef.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", bud_acctunit_str())
    x3_idearef.set_attribute(group_label_str(), True)

    # WHEN
    x_headers_list = x3_idearef.get_headers_list()

    # THEN
    assert x_headers_list == [group_label_str()]


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", bud_acctunit_str())
    x3_idearef.set_attribute(road_str(), True)
    x3_idearef.set_attribute(group_label_str(), False)
    x3_idearef.set_attribute(acct_name_str(), True)

    # WHEN
    x_headers_list = x3_idearef.get_headers_list()

    # THEN
    assert x_headers_list == [acct_name_str(), group_label_str(), road_str()]


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_idearef = idearef_shop("0003", bud_acctunit_str())

    # WHEN
    x_otx_keys_list = x_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == []


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", bud_acctunit_str())
    x3_idearef.set_attribute(group_label_str(), True)

    # WHEN
    x_otx_keys_list = x3_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [group_label_str()]


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", bud_acctunit_str())
    x3_idearef.set_attribute(road_str(), True)
    x3_idearef.set_attribute(group_label_str(), False)
    x3_idearef.set_attribute(acct_name_str(), True)

    # WHEN
    x_otx_keys_list = x3_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [acct_name_str(), road_str()]


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_idearef = idearef_shop("0003", bud_acctunit_str())

    # WHEN
    x_otx_values_list = x_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", bud_acctunit_str())
    x3_idearef.set_attribute(group_label_str(), True)

    # WHEN
    x_otx_values_list = x3_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", bud_acctunit_str())
    x3_idearef.set_attribute(road_str(), True)
    x3_idearef.set_attribute(group_label_str(), False)
    x3_idearef.set_attribute(base_str(), False)
    x3_idearef.set_attribute(acct_name_str(), False)

    # WHEN
    x_otx_values_list = x3_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == [acct_name_str(), group_label_str(), base_str()]
