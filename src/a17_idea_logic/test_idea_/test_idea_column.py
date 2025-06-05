from src.a06_plan_logic._test_util.a06_str import (
    acct_name_str,
    concept_way_str,
    group_title_str,
    plan_acctunit_str,
    rcontext_str,
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
    x_idearef = idearef_shop(x_idea_name=x1_idea_name, x_dimens=[plan_acctunit_str()])

    # THEN
    assert x_idearef.idea_name == x1_idea_name
    assert x_idearef.dimens == [plan_acctunit_str()]
    assert x_idearef._attributes == {}


def test_IdeaRef_set_attribute_SetsAttr():
    # ESTABLISH
    x_idearef = idearef_shop("0003", plan_acctunit_str())
    x_attribute = "1"
    assert x_idearef._attributes == {}

    # WHEN
    x_idearef.set_attribute(x_attribute, True)

    # THEN
    assert x_idearef._attributes != {}
    assert x_idearef._attributes == {x_attribute: {"otx_key": True}}


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH

    x_idearef = idearef_shop("0003", plan_acctunit_str())

    # WHEN
    x_headers_list = x_idearef.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", plan_acctunit_str())
    x3_idearef.set_attribute(group_title_str(), True)

    # WHEN
    x_headers_list = x3_idearef.get_headers_list()

    # THEN
    assert x_headers_list == [group_title_str()]


def test_IdeaRef_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", plan_acctunit_str())
    x3_idearef.set_attribute(concept_way_str(), True)
    x3_idearef.set_attribute(group_title_str(), False)
    x3_idearef.set_attribute(acct_name_str(), True)

    # WHEN
    x_headers_list = x3_idearef.get_headers_list()

    # THEN
    assert x_headers_list == [acct_name_str(), group_title_str(), concept_way_str()]


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_idearef = idearef_shop("0003", plan_acctunit_str())

    # WHEN
    x_otx_keys_list = x_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == []


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", plan_acctunit_str())
    x3_idearef.set_attribute(group_title_str(), True)

    # WHEN
    x_otx_keys_list = x3_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [group_title_str()]


def test_IdeaRef_get_otx_keys_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", plan_acctunit_str())
    x3_idearef.set_attribute(concept_way_str(), True)
    x3_idearef.set_attribute(group_title_str(), False)
    x3_idearef.set_attribute(acct_name_str(), True)

    # WHEN
    x_otx_keys_list = x3_idearef.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [acct_name_str(), concept_way_str()]


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_idearef = idearef_shop("0003", plan_acctunit_str())

    # WHEN
    x_otx_values_list = x_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", plan_acctunit_str())
    x3_idearef.set_attribute(group_title_str(), True)

    # WHEN
    x_otx_values_list = x3_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_IdeaRef_get_otx_values_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_idearef = idearef_shop("0003", plan_acctunit_str())
    x3_idearef.set_attribute(concept_way_str(), True)
    x3_idearef.set_attribute(group_title_str(), False)
    x3_idearef.set_attribute(rcontext_str(), False)
    x3_idearef.set_attribute(acct_name_str(), False)

    # WHEN
    x_otx_values_list = x3_idearef.get_otx_values_list()

    # THEN
    assert x_otx_values_list == [acct_name_str(), group_title_str(), rcontext_str()]
