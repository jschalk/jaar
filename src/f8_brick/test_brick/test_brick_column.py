from src.f2_bud.bud_tool import bud_acctunit_str
from src.f8_brick.brick import BrickColumn, BrickRef, brickref_shop


def test_BrickColumn_Exists():
    # ESTABLISH
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3

    # WHEN
    x_brickcolumn = BrickColumn(x_attribute_key, x_column_order, x_sort_order)

    # THEN
    assert x_brickcolumn.attribute_key == x_attribute_key
    assert x_brickcolumn.column_order == x_column_order
    assert x_brickcolumn.sort_order == x_sort_order


def test_BrickRef_Exists():
    # ESTABLISH / WHEN
    x_brickref = BrickRef()

    # THEN
    assert not x_brickref.brick_name
    assert not x_brickref.atom_categorys
    assert not x_brickref._brickcolumns


def test_brickref_shop_ReturnsObj():
    # ESTABLISH
    x1_brick_name = "0001"

    # WHEN
    x_brickref = brickref_shop(
        x_brick_name=x1_brick_name, x_atom_categorys=[bud_acctunit_str()]
    )

    # THEN
    assert x_brickref.brick_name == x1_brick_name
    assert x_brickref.atom_categorys == [bud_acctunit_str()]
    assert x_brickref._brickcolumns == {}


def test_BrickColumn_set_brickcolumn_SetsAttr():
    # ESTABLISH
    x_brickref = brickref_shop("0003", bud_acctunit_str())
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_brickcolumn = BrickColumn(x_attribute_key, x_column_order, x_sort_order)
    assert x_brickref._brickcolumns == {}

    # WHEN
    x_brickref.set_brickcolumn(x_brickcolumn)

    # THEN
    assert x_brickref._brickcolumns != {}
    assert x_brickref._brickcolumns.get(x_attribute_key) == x_brickcolumn


def test_BrickColumn_get_brickcolumn_ReturnsObj():
    # ESTABLISH

    x_brickref = brickref_shop("0003", bud_acctunit_str())
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_brickcolumn = BrickColumn(x_attribute_key, x_column_order, x_sort_order)
    x_brickref.set_brickcolumn(x_brickcolumn)

    # WHEN / THEN
    assert x_brickref.get_brickcolumn(x_attribute_key) == x_brickcolumn


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
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_brickcolumn = BrickColumn(x_attribute_key, x_column_order, x_sort_order)
    x3_brickref.set_brickcolumn(x_brickcolumn)

    # WHEN
    x_headers_list = x3_brickref.get_headers_list()

    # THEN
    assert x_headers_list == [x_attribute_key]


def test_BrickColumn_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", bud_acctunit_str())
    third_column_str = "third column"
    skeepd_column_str = "skeepd column"
    first_column_str = "first column"
    x3_brickref.set_brickcolumn(BrickColumn(third_column_str, column_order=2))
    x3_brickref.set_brickcolumn(BrickColumn(skeepd_column_str, column_order=1))
    x3_brickref.set_brickcolumn(BrickColumn(first_column_str, column_order=0))

    # WHEN
    x_headers_list = x3_brickref.get_headers_list()

    # THEN
    assert x_headers_list == [first_column_str, skeepd_column_str, third_column_str]


def test_BrickColumn_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_brickref = brickref_shop("0003", bud_acctunit_str())
    third_column_str = "third column"
    skeepd_column_str = "skeepd column"
    first_column_str = "first column"
    fouth_column_str = "fourth column"
    x3_brickref.set_brickcolumn(BrickColumn(third_column_str, column_order=2))
    x3_brickref.set_brickcolumn(BrickColumn(skeepd_column_str, column_order=1))
    x3_brickref.set_brickcolumn(BrickColumn(first_column_str, column_order=0))
    x3_brickref.set_brickcolumn(BrickColumn(fouth_column_str, column_order=3))

    # WHEN
    x_headers_list = x3_brickref.get_headers_list()

    # THEN
    assert x_headers_list == [
        first_column_str,
        skeepd_column_str,
        third_column_str,
        fouth_column_str,
    ]
