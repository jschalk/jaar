from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_gift.atom_config import acct_id_str, group_id_str, road_str
from src.f09_brick.brick import BrickRef, brickref_shop


def test_BrickRef_Exists():
    # ESTABLISH / WHEN
    x_brickref = BrickRef()

    # THEN
    assert not x_brickref.brick_name
    assert not x_brickref.categorys
    assert not x_brickref._attributes


def test_brickref_shop_ReturnsObj():
    # ESTABLISH
    x1_brick_name = "0001"

    # WHEN
    x_brickref = brickref_shop(
        x_brick_name=x1_brick_name, x_categorys=[bud_acctunit_str()]
    )

    # THEN
    assert x_brickref.brick_name == x1_brick_name
    assert x_brickref.categorys == [bud_acctunit_str()]
    assert x_brickref._attributes == set()


def test_BrickColumn_set_attribute_SetsAttr():
    # ESTABLISH
    x_brickref = brickref_shop("0003", bud_acctunit_str())
    x_attribute = "1"
    assert x_brickref._attributes == set()

    # WHEN
    x_brickref.set_attribute(x_attribute)

    # THEN
    assert x_brickref._attributes != set()
    assert x_brickref._attributes == {x_attribute}


def test_BrickColumn_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH

    x_brickref = brickref_shop("0003", bud_acctunit_str())

    # WHEN
    x_headers_list = x_brickref.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_BrickColumn_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", bud_acctunit_str())
    x3_brickref.set_attribute(group_id_str())

    # WHEN
    x_headers_list = x3_brickref.get_headers_list()

    # THEN
    assert x_headers_list == [group_id_str()]


def test_BrickColumn_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", bud_acctunit_str())
    x3_brickref.set_attribute(road_str())
    x3_brickref.set_attribute(group_id_str())
    x3_brickref.set_attribute(acct_id_str())

    # WHEN
    x_headers_list = x3_brickref.get_headers_list()

    # THEN
    assert x_headers_list == [acct_id_str(), group_id_str(), road_str()]
