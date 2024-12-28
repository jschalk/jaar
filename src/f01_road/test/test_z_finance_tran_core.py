from src.f01_road.finance_tran import (
    TranUnit,
    tranunit_shop,
    TranBook,
    tranbook_shop,
    get_tranbook_from_dict,
    get_tranbook_from_json,
)
from pytest import raises as pytest_raises


def test_TranUnit_Exists():
    # ESTABLISH / WHEN
    x_tranunit = TranUnit()

    # THEN
    assert x_tranunit
    assert not x_tranunit.src
    assert not x_tranunit.dst
    assert not x_tranunit.time_int
    assert not x_tranunit.amount


def test_tranunit_shop_WithParametersReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    t55_time_int = 5505
    t55_fundnum = -45
    sue_str = "Sue"
    yao_str = "Yao"

    # WHEN
    x_tranunit = tranunit_shop(sue_str, yao_str, t55_time_int, t55_fundnum)

    # THEN
    assert x_tranunit
    assert x_tranunit.src == sue_str
    assert x_tranunit.dst == yao_str
    assert x_tranunit.time_int == t55_time_int
    assert x_tranunit.amount == t55_fundnum


def test_TranBook_Exists():
    # ESTABLISH / WHEN
    x_tranbook = TranBook()

    # THEN
    assert x_tranbook
    assert not x_tranbook.deal_id
    assert not x_tranbook.tranunits
    assert not x_tranbook._accts_net


def test_tranbook_shop_WithParametersReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    x_timelinepoint = 5505
    x_fundnum = -45
    sue_str = "Sue"
    yao_str = "Yao"
    x_tranunits = {sue_str: {yao_str: {x_timelinepoint: x_fundnum}}}

    # WHEN
    x_tranbook = tranbook_shop(accord23_str, x_tranunits)

    # THEN
    assert x_tranbook
    assert x_tranbook.deal_id == accord23_str
    assert x_tranbook.tranunits == x_tranunits
    assert x_tranbook._accts_net == {}


def test_tranbook_shop_WithoutParametersReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"

    # WHEN
    x_tranbook = tranbook_shop(accord23_str)

    # THEN
    assert x_tranbook
    assert x_tranbook.deal_id == accord23_str
    assert x_tranbook.tranunits == {}
    assert x_tranbook._accts_net == {}


def test_TranBook_set_tranunit_SetsAttr():
    # ESTABLISH
    accord23_str = "accord23"
    x_tranbook = tranbook_shop(accord23_str)
    assert x_tranbook.tranunits == {}

    # WHEN
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
    x_tranbook.set_tranunit(sue_yao_t55_tranunit)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_t: t55_yao_amount}}}

    # WHEN
    bob_str = "Bob"
    t55_bob_amount = 600
    sue_bob_t55_tranunit = tranunit_shop(sue_str, bob_str, t55_t, t55_bob_amount)
    x_tranbook.set_tranunit(sue_bob_t55_tranunit)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_t: t55_yao_amount},
            bob_str: {t55_t: t55_bob_amount},
        }
    }

    # WHEN
    t66_t = 6606
    t66_yao_amount = -66
    sue_yao_t66_tranunit = tranunit_shop(sue_str, yao_str, t66_t, t66_yao_amount)
    x_tranbook.set_tranunit(sue_yao_t66_tranunit)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_t: t55_yao_amount, t66_t: t66_yao_amount},
            bob_str: {t55_t: t55_bob_amount},
        }
    }

    # WHEN
    t77_t = 7707
    t77_yao_amount = -77
    yao_yao_77_tranunit = tranunit_shop(yao_str, yao_str, t77_t, t77_yao_amount)
    x_tranbook.set_tranunit(yao_yao_77_tranunit)

    # THEN
    print(f"{x_tranbook.tranunits=}")
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_t: t55_yao_amount, t66_t: t66_yao_amount},
            bob_str: {t55_t: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_t: t77_yao_amount}},
    }


def test_TranBook_set_tranunit_SetsAttrWithBlocktime_int():
    # ESTABLISH
    accord23_str = "accord23"
    x_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN
    x_blocked_time_ints = {44}
    x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_blocked_time_ints)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_t: t55_yao_amount}}}


def test_TranBook_set_tranunit_SetsAttrWithBlocktime_int_RaisesError():
    # ESTABLISH
    accord23_str = "accord23"
    x_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    x_blocked_time_ints = {t55_t}
    sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_blocked_time_ints)
    exception_str = (
        f"Cannot set tranunit for time_int={t55_t}, timelinepoint is blocked"
    )
    assert str(excinfo.value) == exception_str


def test_TranBook_set_tranunit_SetsAttrWithCurrenttime_int():
    # ESTABLISH
    accord23_str = "accord23"
    x_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN
    x_current_time = 8808
    x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_current_time=x_current_time)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_t: t55_yao_amount}}}


def test_TranBook_set_tranunit_SetsAttrWithCurrenttime_int_RaisesError():
    # ESTABLISH
    accord23_str = "accord23"
    x_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_current_time=t55_t)
    exception_str = f"Cannot set tranunit for time_int={t55_t}, timelinepoint is greater than current time={t55_t}"
    assert str(excinfo.value) == exception_str

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_current_time=33)
    exception_str = f"Cannot set tranunit for time_int={t55_t}, timelinepoint is greater than current time=33"
    assert str(excinfo.value) == exception_str


def test_TranBook_add_tranunit_SetsAttr():
    # ESTABLISH
    accord23_str = "accord23"
    x_tranbook = tranbook_shop(accord23_str)
    assert x_tranbook.tranunits == {}

    # WHEN
    sue_str = "Sue"
    yao_str = "Yao"
    t55_time_int = 5505
    t55_yao_amount = -55
    x_tranbook.add_tranunit(sue_str, yao_str, t55_time_int, t55_yao_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_time_int: t55_yao_amount}}}

    # WHEN
    bob_str = "Bob"
    t55_bob_amount = 600
    x_tranbook.add_tranunit(sue_str, bob_str, t55_time_int, t55_bob_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_time_int: t55_yao_amount},
            bob_str: {t55_time_int: t55_bob_amount},
        }
    }

    # WHEN
    t66_time_int = 6606
    t66_yao_amount = -66
    x_tranbook.add_tranunit(sue_str, yao_str, t66_time_int, t66_yao_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_time_int: t55_yao_amount, t66_time_int: t66_yao_amount},
            bob_str: {t55_time_int: t55_bob_amount},
        }
    }

    # WHEN
    t77_time_int = 7707
    t77_yao_amount = -77
    x_tranbook.add_tranunit(yao_str, yao_str, t77_time_int, t77_yao_amount)

    # THEN
    print(f"{x_tranbook.tranunits=}")
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_time_int: t55_yao_amount, t66_time_int: t66_yao_amount},
            bob_str: {t55_time_int: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_time_int: t77_yao_amount}},
    }


def test_TranBook_tranunit_exists_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
    assert accord23_tranbook.tranunit_exists(sue_str, yao_str, t55_t) is False

    # WHEN
    accord23_tranbook.set_tranunit(sue_yao_t55_tranunit)

    # THEN
    assert accord23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)


def test_TranBook_get_tranunit_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_t, t55_yao_amount)
    assert accord23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)

    # WHEN
    sue_yao_t55_tranunit = accord23_tranbook.get_tranunit(sue_str, yao_str, t55_t)

    # THEN
    assert sue_yao_t55_tranunit
    assert sue_yao_t55_tranunit.src == sue_str
    assert sue_yao_t55_tranunit.dst == yao_str
    assert sue_yao_t55_tranunit.time_int == t55_t
    assert sue_yao_t55_tranunit.amount == t55_yao_amount

    # WHEN / THEN
    assert not accord23_tranbook.get_tranunit(sue_str, "Bob", t55_t)
    assert not accord23_tranbook.get_tranunit("Bob", yao_str, t55_t)
    assert not accord23_tranbook.get_tranunit(sue_str, yao_str, 44)


def test_TranBook_get_amount_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_t, t55_yao_amount)
    assert accord23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)

    # WHEN
    assert accord23_tranbook.get_amount(sue_str, yao_str, t55_t) == t55_yao_amount
    assert not accord23_tranbook.get_amount(sue_str, "Bob", t55_t)
    assert not accord23_tranbook.get_amount("Bob", yao_str, t55_t)
    assert not accord23_tranbook.get_amount(sue_str, yao_str, 44)


def test_TranBook_del_tranunit_SetsAttr():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_t, t55_yao_amount)
    assert accord23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)

    # WHEN
    accord23_tranbook.del_tranunit(sue_str, yao_str, t55_t)

    # THEN
    assert accord23_tranbook.tranunit_exists(sue_str, yao_str, t55_t) is False


def test_TranBook_get_time_ints_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_time_int = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_time_int = 6606
    t66_yao_amount = -66
    t77_time_int = 7707
    t77_bob_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_time_int, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_time_int, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t77_time_int, t77_bob_amount)

    # WHEN
    accord23_time_ints = accord23_tranbook.get_time_ints()

    # THEN
    assert accord23_time_ints
    assert len(accord23_time_ints)
    assert accord23_time_ints == {t55_time_int, t66_time_int, t77_time_int}


def test_TranBook_get_owners_accts_net_ReturnObj_Scenario0():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_time_int = 5505
    t55_bob_amount = 600
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_time_int, t55_bob_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {bob_str: {t55_time_int: t55_bob_amount}}
    }

    # WHEN
    accord23_accts_net_dict = accord23_tranbook.get_owners_accts_net()

    # THEN
    assert accord23_accts_net_dict
    assert accord23_accts_net_dict == {sue_str: {bob_str: t55_bob_amount}}


def test_TranBook_get_owners_accts_net_ReturnsObj_Scenario1():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_time_int = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_time_int = 6606
    t66_yao_amount = -66
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_time_int, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_time_int, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_time_int, t55_bob_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_time_int: t55_yao_amount, t66_time_int: t66_yao_amount},
            bob_str: {t55_time_int: t55_bob_amount},
        }
    }

    # WHEN
    accord23_accts_net_dict = accord23_tranbook.get_owners_accts_net()

    # THEN
    assert accord23_accts_net_dict
    assert accord23_accts_net_dict == {
        sue_str: {yao_str: t55_yao_amount + t66_yao_amount, bob_str: t55_bob_amount}
    }


def test_TranBook_get_accts_net_dict_ReturnObj_Scenario0():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_time_int = 5505
    t55_bob_amount = 600
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_time_int, t55_bob_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {bob_str: {t55_time_int: t55_bob_amount}}
    }

    # WHEN
    accord23_accts_net_dict = accord23_tranbook.get_accts_net_dict()

    # THEN
    assert accord23_accts_net_dict
    assert accord23_accts_net_dict == {bob_str: t55_bob_amount}


def test_TranBook_get_accts_net_dict_ReturnObj_Scenario1():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_time_int = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_time_int = 6606
    t66_yao_amount = -66
    t77_time_int = 7707
    t77_yao_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_time_int, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_time_int, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_time_int, t55_bob_amount)

    accord23_tranbook.add_tranunit(yao_str, yao_str, t77_time_int, t77_yao_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_time_int: t55_yao_amount, t66_time_int: t66_yao_amount},
            bob_str: {t55_time_int: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_time_int: t77_yao_amount}},
    }

    # WHEN
    accord23_accts_net_dict = accord23_tranbook.get_accts_net_dict()

    # THEN
    assert accord23_accts_net_dict
    assert accord23_accts_net_dict == {
        yao_str: t55_yao_amount + t66_yao_amount + t77_yao_amount,
        bob_str: t55_bob_amount,
    }


def test_TranBook_get_accts_net_array_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_time_int = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_time_int = 6606
    t66_yao_amount = -66
    t77_time_int = 7707
    t77_yao_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_time_int, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_time_int, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_time_int, t55_bob_amount)

    accord23_tranbook.add_tranunit(yao_str, yao_str, t77_time_int, t77_yao_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_time_int: t55_yao_amount, t66_time_int: t66_yao_amount},
            bob_str: {t55_time_int: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_time_int: t77_yao_amount}},
    }

    # WHEN
    accord23_accts_net_array = accord23_tranbook._get_accts_net_array()

    # THEN
    assert accord23_accts_net_array
    assert accord23_accts_net_array == [
        [bob_str, t55_bob_amount],
        [yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount],
    ]


def test_TranBook_get_accts_headers_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)

    # WHEN / THEN
    assert accord23_tranbook._get_accts_headers() == ["acct_name", "net_amount"]


def test_TranBook_get_accts_csv_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_time_int = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_time_int = 6606
    t66_yao_amount = -66
    t77_time_int = 7707
    t77_yao_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_time_int, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_time_int, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_time_int, t55_bob_amount)

    accord23_tranbook.add_tranunit(yao_str, yao_str, t77_time_int, t77_yao_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_time_int: t55_yao_amount, t66_time_int: t66_yao_amount},
            bob_str: {t55_time_int: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_time_int: t77_yao_amount}},
    }

    # WHEN
    accord23_accts_net_csv = accord23_tranbook.get_accts_net_csv()

    # THEN
    assert accord23_accts_net_csv
    example_csv = f"""acct_name,net_amount
{bob_str},{t55_bob_amount}
{yao_str},{t55_yao_amount + t66_yao_amount + t77_yao_amount}
"""
    assert accord23_accts_net_csv == example_csv


# def test_TranBook_get_dict_ReturnsObj():
#     # ESTABLISH
#     accord23_str = "accord23"
#     x_timelinepoint = 5505
#     x_fundnum = -45
#     sue_str = "Sue"
#     yao_str = "Yao"
#     x_tranunits = {sue_str: {yao_str: {x_timelinepoint: x_fundnum}}}
#     x_tranbook = tranbook_shop(accord23_str, x_tranunits)

#     # WHEN
#     x_dict = x_tranbook.get_dict()

#     # THEN
#     assert x_dict
#     assert "accord23_str" in x_dict.keys()
#     accord23_dict = x_dict.get(accord23_str)
#     assert accord23_dict
#     assert accord23_dict == x_tranunits


# def test_tranbook_shop_ReturnsObjWith_net_purviews():
#     # ESTABLISH
#     x_time_int = 4
#     x_amount = 55
#     x_net_purviews = {"Sue": -4}
#     x_magnitude = 677

#     # WHEN
#     x_tranbook = tranbook_shop(
#         x_time_int=x_time_int,
#         x_amount=x_amount,
#         net_purviews=x_net_purviews,
#         x_magnitude=x_magnitude,
#     )

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.time_int == x_time_int
#     assert x_tranbook.amount == x_amount
#     assert x_tranbook._magnitude == 677
#     assert x_tranbook._net_purviews == x_net_purviews


# def test_TranBook_set_net_purview_SetsAttr():
#     # ESTABLISH
#     yao_tranbook = tranbook_shop("yao", 33)
#     assert yao_tranbook._net_purviews == {}

#     # WHEN
#     sue_str = "Sue"
#     sue_purview = -44
#     yao_tranbook.set_net_purview(sue_str, sue_purview)

#     # THEN
#     assert yao_tranbook._net_purviews != {}
#     assert yao_tranbook._net_purviews.get(sue_str) == sue_purview


# def test_TranBook_net_purview_exists_ReturnsObj():
#     # ESTABLISH
#     yao_tranbook = tranbook_shop("yao", 33)
#     sue_str = "Sue"
#     sue_purview = -44
#     assert yao_tranbook.net_purview_exists(sue_str) is False

#     # WHEN
#     yao_tranbook.set_net_purview(sue_str, sue_purview)

#     # THEN
#     assert yao_tranbook.net_purview_exists(sue_str)


# def test_TranBook_get_net_purview_ReturnsObj():
#     # ESTABLISH
#     yao_tranbook = tranbook_shop("yao", 33)
#     sue_str = "Sue"
#     sue_purview = -44
#     yao_tranbook.set_net_purview(sue_str, sue_purview)

#     # WHEN / THEN
#     assert yao_tranbook.get_net_purview(sue_str)
#     assert yao_tranbook.get_net_purview(sue_str) == sue_purview


# def test_TranBook_del_net_purview_SetsAttr():
#     # ESTABLISH
#     yao_tranbook = tranbook_shop("yao", 33)
#     sue_str = "Sue"
#     sue_purview = -44
#     yao_tranbook.set_net_purview(sue_str, sue_purview)
#     assert yao_tranbook.net_purview_exists(sue_str)

#     # WHEN
#     yao_tranbook.del_net_purview(sue_str)

#     # THEN
#     assert yao_tranbook.net_purview_exists(sue_str) is False


# def test_TranBook_get_dict_ReturnsObj():
#     # ESTABLISH
#     x_time_int = 4
#     x_amount = 55
#     x_tranbook = tranbook_shop(x_time_int, x_amount)

#     # WHEN
#     x_dict = x_tranbook.get_dict()

#     # THEN
#     assert x_dict == {"time_int": x_time_int, "amount": x_amount}


# def test_TranBook_calc_magnitude_SetsAttr_Scenario0():
#     # ESTABLISH
#     x_time_int = 4
#     x_tranbook = tranbook_shop(x_time_int)
#     assert x_tranbook._magnitude == 0

#     # WHEN
#     x_tranbook.calc_magnitude()

#     # THEN
#     assert x_tranbook._magnitude == 0


# def test_TranBook_calc_magnitude_SetsAttr_Scenario1():
#     # ESTABLISH
#     x_time_int = 4
#     x_net_purviews = {"Sue": -4, "Yao": 2, "Zia": 2}

#     x_tranbook = tranbook_shop(x_time_int, net_purviews=x_net_purviews)
#     assert x_tranbook._magnitude == 0

#     # WHEN
#     x_tranbook.calc_magnitude()

#     # THEN
#     assert x_tranbook._magnitude == 4


# def test_TranBook_calc_magnitude_SetsAttr_Scenario2():
#     # ESTABLISH
#     x_time_int = 4
#     x_net_purviews = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

#     x_tranbook = tranbook_shop(x_time_int, net_purviews=x_net_purviews)
#     assert x_tranbook._magnitude == 0

#     # WHEN
#     x_tranbook.calc_magnitude()

#     # THEN
#     assert x_tranbook._magnitude == 20


# def test_TranBook_calc_magnitude_SetsAttr_Scenario3_RaisesError():
#     # ESTABLISH
#     x_time_int = 4
#     bob_purview = -13
#     sue_purview = -3
#     yao_purview = 100
#     x_net_purviews = {"Bob": bob_purview, "Sue": sue_purview, "Yao": yao_purview}
#     x_tranbook = tranbook_shop(x_time_int, net_purviews=x_net_purviews)

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         x_tranbook.calc_magnitude()
#     exception_str = f"magnitude cannot be calculated: debt_purview={bob_purview+sue_purview}, cred_purview={yao_purview}"
#     assert str(excinfo.value) == exception_str


# def test_TranBook_get_dict_ReturnsObjWith_net_purviews():
#     # ESTABLISH
#     x_time_int = 4
#     x_amount = 55
#     x_net_purviews = {"Sue": -4}
#     x_magnitude = 67
#     x_tranbook = tranbook_shop(x_time_int, x_amount, x_net_purviews)
#     x_tranbook._magnitude = 67

#     # WHEN
#     x_dict = x_tranbook.get_dict()

#     # THEN
#     assert x_dict == {
#         "time_int": x_time_int,
#         "amount": x_amount,
#         "magnitude": x_magnitude,
#         "net_purviews": x_net_purviews,
#     }


# def test_TranBook_get_json_ReturnsObj():
#     # ESTABLISH
#     x_time_int = 4
#     x_amount = 55
#     x_net_purviews = {"Sue": -77}
#     x_tranbook = tranbook_shop(x_time_int, x_amount, x_net_purviews)
#     x_tranbook._magnitude = 67

#     # WHEN
#     x_json = x_tranbook.get_json()

#     # THEN
#     static_x_json = """{
#   "magnitude": 67,
#   "net_purviews": {
#     "Sue": -77
#   },
#   "amount": 55,
#   "time_int": 4
# }"""
#     print(f"{x_json=}")
#     assert x_json == static_x_json


# def test_get_tranbook_from_dict_ReturnsObj_Sccenario0():
#     # ESTABLISH
#     x_time_int = 4
#     x_amount = 55
#     x_tranbook = tranbook_shop(x_time_int, x_amount)
#     x_dict = x_tranbook.get_dict()
#     assert x_dict == {"time_int": x_time_int, "amount": x_amount}

#     # WHEN
#     x_tranbook = get_tranbook_from_dict(x_dict)

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.time_int == x_time_int
#     assert x_tranbook.amount == x_amount
#     assert x_tranbook._magnitude == 0
#     assert x_tranbook == x_tranbook


# def test_get_tranbook_from_dict_ReturnsObj_Scenario1():
#     # ESTABLISH
#     x_time_int = 4
#     x_amount = 55
#     x_magnitude = 65
#     x_net_purviews = {"Sue": -77}
#     x_tranbook = tranbook_shop(x_time_int, x_amount, x_net_purviews)
#     x_tranbook._magnitude = x_magnitude
#     x_dict = x_tranbook.get_dict()

#     # WHEN
#     x_tranbook = get_tranbook_from_dict(x_dict)

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.time_int == x_time_int
#     assert x_tranbook.amount == x_amount
#     assert x_tranbook._magnitude == x_magnitude
#     assert x_tranbook._net_purviews == x_net_purviews
#     assert x_tranbook == x_tranbook


# def test_get_tranbook_from_json_ReturnsObj():
#     # ESTABLISH
#     x_time_int = 4
#     x_amount = 55
#     x_net_purviews = {"Sue": -57}
#     x_tranbook = tranbook_shop(x_time_int, x_amount, x_net_purviews)
#     x_json = x_tranbook.get_json()

#     # WHEN
#     x_tranbook = get_tranbook_from_json(x_json)

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.time_int == x_time_int
#     assert x_tranbook.amount == x_amount
#     assert x_tranbook._net_purviews == x_net_purviews
#     assert x_tranbook == x_tranbook
