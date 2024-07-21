from src.gift.span import SpanColumn, SpanRef, spanref_shop


def test_SpanColumn_Exists():
    # ESTABLISH
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3

    # WHEN
    x_spancolumn = SpanColumn(x_attribute_key, x_column_order, x_sort_order)

    # THEN
    assert x_spancolumn.attribute_key == x_attribute_key
    assert x_spancolumn.column_order == x_column_order
    assert x_spancolumn.sort_order == x_sort_order


def test_SpanRef_Exists():
    # ESTABLISH / WHEN
    x_spanref = SpanRef()

    # THEN
    assert not x_spanref.span_name
    assert not x_spanref.atom_category
    assert not x_spanref._spancolumns


def test_spanref_shop_ReturnsObj():
    # ESTABLISH
    x1_span_name = "0001"
    bud_acctunit_text = "bud_acctunit"

    # WHEN
    x_spanref = spanref_shop(
        x_span_name=x1_span_name, x_atom_category=bud_acctunit_text
    )

    # THEN
    assert x_spanref.span_name == x1_span_name
    assert x_spanref.atom_category == bud_acctunit_text
    assert x_spanref._spancolumns == {}


def test_SpanColumn_set_spancolumn_SetsAttr():
    # ESTABLISH
    bud_acctunit_text = "bud_acctunit"
    x_spanref = spanref_shop("0003", bud_acctunit_text)
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_spancolumn = SpanColumn(x_attribute_key, x_column_order, x_sort_order)
    assert x_spanref._spancolumns == {}

    # WHEN
    x_spanref.set_spancolumn(x_spancolumn)

    # THEN
    assert x_spanref._spancolumns != {}
    assert x_spanref._spancolumns.get(x_attribute_key) == x_spancolumn


def test_SpanColumn_get_spancolumn_ReturnsObj():
    # ESTABLISH
    bud_acctunit_text = "bud_acctunit"
    x_spanref = spanref_shop("0003", bud_acctunit_text)
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_spancolumn = SpanColumn(x_attribute_key, x_column_order, x_sort_order)
    x_spanref.set_spancolumn(x_spancolumn)

    # WHEN / THEN
    assert x_spanref.get_spancolumn(x_attribute_key) == x_spancolumn


def test_SpanColumn_get_headers_list_ReturnsObj_Scenario0():
    # ESTABLISH
    bud_acctunit_text = "bud_acctunit"
    x_spanref = spanref_shop("0003", bud_acctunit_text)

    # WHEN
    x_headers_list = x_spanref.get_headers_list()

    # THEN
    assert x_headers_list == []


def test_SpanColumn_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH
    bud_acctunit_text = "bud_acctunit"
    x3_spanref = spanref_shop("0003", bud_acctunit_text)
    x_attribute_key = "1"
    x_column_order = 2
    x_sort_order = 3
    x_spancolumn = SpanColumn(x_attribute_key, x_column_order, x_sort_order)
    x3_spanref.set_spancolumn(x_spancolumn)

    # WHEN
    x_headers_list = x3_spanref.get_headers_list()

    # THEN
    assert x_headers_list == [x_attribute_key]


def test_SpanColumn_get_headers_list_ReturnsObj_Scenario1():
    # ESTABLISH
    bud_acctunit_text = "bud_acctunit"
    x3_spanref = spanref_shop("0003", bud_acctunit_text)
    third_column_str = "third column"
    second_column_str = "second column"
    first_column_str = "first column"
    x3_spanref.set_spancolumn(SpanColumn(third_column_str, column_order=2))
    x3_spanref.set_spancolumn(SpanColumn(second_column_str, column_order=1))
    x3_spanref.set_spancolumn(SpanColumn(first_column_str, column_order=0))

    # WHEN
    x_headers_list = x3_spanref.get_headers_list()

    # THEN
    assert x_headers_list == [first_column_str, second_column_str, third_column_str]


def test_SpanColumn_get_headers_list_ReturnsObj_Scenario2():
    # ESTABLISH
    bud_acctunit_text = "bud_acctunit"
    x3_spanref = spanref_shop("0003", bud_acctunit_text)
    third_column_str = "third column"
    second_column_str = "second column"
    first_column_str = "first column"
    fouth_column_str = "fourth column"
    x3_spanref.set_spancolumn(SpanColumn(third_column_str, column_order=2))
    x3_spanref.set_spancolumn(SpanColumn(second_column_str, column_order=1))
    x3_spanref.set_spancolumn(SpanColumn(first_column_str, column_order=0))
    x3_spanref.set_spancolumn(SpanColumn(fouth_column_str, column_order=3))

    # WHEN
    x_headers_list = x3_spanref.get_headers_list()

    # THEN
    assert x_headers_list == [
        first_column_str,
        second_column_str,
        third_column_str,
        fouth_column_str,
    ]
