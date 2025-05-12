from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    acct_name_str,
    group_label_str,
    idea_way_str,
    context_str,
)
from src.a17_creed_logic.creed import CreedRef, creedref_shop


def test_CreedRef_Exists():
    # ESTABLISH / WHEN
    x_creedref = CreedRef()

    # THEN
    assert not x_creedref.creed_name
    assert not x_creedref.dimens
    assert not x_creedref._attributes


def test_creedref_shop_ReturnsObj():
    # ESTABLISH
    x1_creed_name = "0001"

    # WHEN
    x_creedref = creedref_shop(
        x_creed_name=x1_creed_name, x_dimens=[bud_acctunit_str()]
    )

    # THEN
    assert x_creedref.creed_name == x1_creed_name
    assert x_creedref.dimens == [bud_acctunit_str()]
    assert x_creedref._attributes == {}


def test_CreedRef_set_attribute_SetsAttr():
    # ESTABLISH
    x_creedref = creedref_shop("0003", bud_acctunit_str())
    x_attribute = "1"
    assert x_creedref._attributes == {}

    # WHEN
    x_creedref.set_attribute(x_attribute, True)

    # THEN
    assert x_creedref._attributes != {}
    assert x_creedref._attributes == {x_attribute: {"otx_key": True}}


def test_CreedRef_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH

    x_creedref = creedref_shop("0003", bud_acctunit_str())

    # WHEN
    x_headers_list = x_creedref.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_CreedRef_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_creedref = creedref_shop("0003", bud_acctunit_str())
    x3_creedref.set_attribute(group_label_str(), True)

    # WHEN
    x_headers_list = x3_creedref.get_headers_list()

    # THEN
    assert x_headers_list == [group_label_str()]


def test_CreedRef_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_creedref = creedref_shop("0003", bud_acctunit_str())
    x3_creedref.set_attribute(idea_way_str(), True)
    x3_creedref.set_attribute(group_label_str(), False)
    x3_creedref.set_attribute(acct_name_str(), True)

    # WHEN
    x_headers_list = x3_creedref.get_headers_list()

    # THEN
    assert x_headers_list == [acct_name_str(), group_label_str(), idea_way_str()]


def test_CreedRef_get_otx_keys_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_creedref = creedref_shop("0003", bud_acctunit_str())

    # WHEN
    x_otx_keys_list = x_creedref.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == []


def test_CreedRef_get_otx_keys_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_creedref = creedref_shop("0003", bud_acctunit_str())
    x3_creedref.set_attribute(group_label_str(), True)

    # WHEN
    x_otx_keys_list = x3_creedref.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [group_label_str()]


def test_CreedRef_get_otx_keys_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_creedref = creedref_shop("0003", bud_acctunit_str())
    x3_creedref.set_attribute(idea_way_str(), True)
    x3_creedref.set_attribute(group_label_str(), False)
    x3_creedref.set_attribute(acct_name_str(), True)

    # WHEN
    x_otx_keys_list = x3_creedref.get_otx_keys_list()

    # THEN
    assert x_otx_keys_list == [acct_name_str(), idea_way_str()]


def test_CreedRef_get_otx_values_list_ReturnsObj_Scenario0():
    # ESTABLISH
    x_creedref = creedref_shop("0003", bud_acctunit_str())

    # WHEN
    x_otx_values_list = x_creedref.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_CreedRef_get_otx_values_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_creedref = creedref_shop("0003", bud_acctunit_str())
    x3_creedref.set_attribute(group_label_str(), True)

    # WHEN
    x_otx_values_list = x3_creedref.get_otx_values_list()

    # THEN
    assert x_otx_values_list == []


def test_CreedRef_get_otx_values_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_creedref = creedref_shop("0003", bud_acctunit_str())
    x3_creedref.set_attribute(idea_way_str(), True)
    x3_creedref.set_attribute(group_label_str(), False)
    x3_creedref.set_attribute(context_str(), False)
    x3_creedref.set_attribute(acct_name_str(), False)

    # WHEN
    x_otx_values_list = x3_creedref.get_otx_values_list()

    # THEN
    assert x_otx_values_list == [acct_name_str(), group_label_str(), context_str()]
