from src.bud.bud_tool import bud_acctunit_str
from src.stone.stone import StoneColumn, StoneRef, stoneref_shop


def test_StoneColumn_Exists():
    # ESTABLISH
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3

    # WHEN
    x_stonecolumn = StoneColumn(x_attribute_key, x_column_order, x_sort_order)

    # THEN
    assert x_stonecolumn.attribute_key == x_attribute_key
    assert x_stonecolumn.column_order == x_column_order
    assert x_stonecolumn.sort_order == x_sort_order


def test_StoneRef_Exists():
    # ESTABLISH / WHEN
    x_stoneref = StoneRef()

    # THEN
    assert not x_stoneref.stone_name
    assert not x_stoneref.atom_categorys
    assert not x_stoneref._stonecolumns


def test_stoneref_shop_ReturnsObj():
    # ESTABLISH
    x1_stone_name = "0001"

    # WHEN
    x_stoneref = stoneref_shop(
        x_stone_name=x1_stone_name, x_atom_categorys=[bud_acctunit_str()]
    )

    # THEN
    assert x_stoneref.stone_name == x1_stone_name
    assert x_stoneref.atom_categorys == [bud_acctunit_str()]
    assert x_stoneref._stonecolumns == {}


def test_StoneColumn_set_stonecolumn_SetsAttr():
    # ESTABLISH
    x_stoneref = stoneref_shop("0003", bud_acctunit_str())
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_stonecolumn = StoneColumn(x_attribute_key, x_column_order, x_sort_order)
    assert x_stoneref._stonecolumns == {}

    # WHEN
    x_stoneref.set_stonecolumn(x_stonecolumn)

    # THEN
    assert x_stoneref._stonecolumns != {}
    assert x_stoneref._stonecolumns.get(x_attribute_key) == x_stonecolumn


def test_StoneColumn_get_stonecolumn_ReturnsObj():
    # ESTABLISH

    x_stoneref = stoneref_shop("0003", bud_acctunit_str())
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_stonecolumn = StoneColumn(x_attribute_key, x_column_order, x_sort_order)
    x_stoneref.set_stonecolumn(x_stonecolumn)

    # WHEN / THEN
    assert x_stoneref.get_stonecolumn(x_attribute_key) == x_stonecolumn


def test_StoneColumn_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH

    x_stoneref = stoneref_shop("0003", bud_acctunit_str())

    # WHEN
    x_headers_list = x_stoneref.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_StoneColumn_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_stoneref = stoneref_shop("0003", bud_acctunit_str())
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_stonecolumn = StoneColumn(x_attribute_key, x_column_order, x_sort_order)
    x3_stoneref.set_stonecolumn(x_stonecolumn)

    # WHEN
    x_headers_list = x3_stoneref.get_headers_list()

    # THEN
    assert x_headers_list == [x_attribute_key]


def test_StoneColumn_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH

    x3_stoneref = stoneref_shop("0003", bud_acctunit_str())
    third_column_str = "third column"
    skeepd_column_str = "skeepd column"
    first_column_str = "first column"
    x3_stoneref.set_stonecolumn(StoneColumn(third_column_str, column_order=2))
    x3_stoneref.set_stonecolumn(StoneColumn(skeepd_column_str, column_order=1))
    x3_stoneref.set_stonecolumn(StoneColumn(first_column_str, column_order=0))

    # WHEN
    x_headers_list = x3_stoneref.get_headers_list()

    # THEN
    assert x_headers_list == [first_column_str, skeepd_column_str, third_column_str]


def test_StoneColumn_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH

    x3_stoneref = stoneref_shop("0003", bud_acctunit_str())
    third_column_str = "third column"
    skeepd_column_str = "skeepd column"
    first_column_str = "first column"
    fouth_column_str = "fourth column"
    x3_stoneref.set_stonecolumn(StoneColumn(third_column_str, column_order=2))
    x3_stoneref.set_stonecolumn(StoneColumn(skeepd_column_str, column_order=1))
    x3_stoneref.set_stonecolumn(StoneColumn(first_column_str, column_order=0))
    x3_stoneref.set_stonecolumn(StoneColumn(fouth_column_str, column_order=3))

    # WHEN
    x_headers_list = x3_stoneref.get_headers_list()

    # THEN
    assert x_headers_list == [
        first_column_str,
        skeepd_column_str,
        third_column_str,
        fouth_column_str,
    ]
