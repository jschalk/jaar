from pytest import raises as pytest_raises
from src.a02_finance_logic._test_util.a02_str import acct_name_str, vow_label_str
from src.a02_finance_logic.deal import (
    TranBook,
    TranUnit,
    get_tranbook_from_dict,
    tranbook_shop,
    tranunit_shop,
)


def test_TranUnit_Exists():
    # ESTABLISH / WHEN
    x_tranunit = TranUnit()

    # THEN
    assert x_tranunit
    assert not x_tranunit.src
    assert not x_tranunit.dst
    assert not x_tranunit.tran_time
    assert not x_tranunit.amount


def test_tranunit_shop_WithParametersReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    t55_tran_time = 5505
    t55_fundnum = -45
    sue_str = "Sue"
    yao_str = "Yao"

    # WHEN
    x_tranunit = tranunit_shop(sue_str, yao_str, t55_tran_time, t55_fundnum)

    # THEN
    assert x_tranunit
    assert x_tranunit.src == sue_str
    assert x_tranunit.dst == yao_str
    assert x_tranunit.tran_time == t55_tran_time
    assert x_tranunit.amount == t55_fundnum


def test_TranBook_Exists():
    # ESTABLISH / WHEN
    x_tranbook = TranBook()

    # THEN
    assert x_tranbook
    assert not x_tranbook.vow_label
    assert not x_tranbook.tranunits
    assert not x_tranbook._accts_net


def test_tranbook_shop_WithParametersReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    x_TimeLinePoint = 5505
    x_fundnum = -45
    sue_str = "Sue"
    yao_str = "Yao"
    x_tranunits = {sue_str: {yao_str: {x_TimeLinePoint: x_fundnum}}}

    # WHEN
    x_tranbook = tranbook_shop(accord23_str, x_tranunits)

    # THEN
    assert x_tranbook
    assert x_tranbook.vow_label == accord23_str
    assert x_tranbook.tranunits == x_tranunits
    assert x_tranbook._accts_net == {}


def test_tranbook_shop_WithoutParametersReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"

    # WHEN
    x_tranbook = tranbook_shop(accord23_str)

    # THEN
    assert x_tranbook
    assert x_tranbook.vow_label == accord23_str
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


def test_TranBook_set_tranunit_SetsAttrWithBlocktran_time():
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
    x_blocked_tran_times = {44}
    x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_blocked_tran_times)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_t: t55_yao_amount}}}


def test_TranBook_set_tranunit_SetsAttrWithBlocktran_time_RaisesError():
    # ESTABLISH
    accord23_str = "accord23"
    x_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    x_blocked_tran_times = {t55_t}
    sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
    assert x_tranbook.tranunits == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_blocked_tran_times)
    exception_str = (
        f"Cannot set tranunit for tran_time={t55_t}, TimeLinePoint is blocked"
    )
    assert str(excinfo.value) == exception_str


def test_TranBook_set_tranunit_SetsAttrWithCurrenttran_time():
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
    x_offi_time_max = 8808
    x_tranbook.set_tranunit(sue_yao_t55_tranunit, _offi_time_max=x_offi_time_max)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_t: t55_yao_amount}}}


def test_TranBook_set_tranunit_SetsAttrWithCurrenttran_time_RaisesError():
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
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, _offi_time_max=t55_t)
    exception_str = f"Cannot set tranunit for tran_time={t55_t}, TimeLinePoint is greater than current time={t55_t}"
    assert str(excinfo.value) == exception_str

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_tranbook.set_tranunit(sue_yao_t55_tranunit, _offi_time_max=33)
    exception_str = f"Cannot set tranunit for tran_time={t55_t}, TimeLinePoint is greater than current time=33"
    assert str(excinfo.value) == exception_str


def test_TranBook_add_tranunit_SetsAttr():
    # ESTABLISH
    accord23_str = "accord23"
    x_tranbook = tranbook_shop(accord23_str)
    assert x_tranbook.tranunits == {}

    # WHEN
    sue_str = "Sue"
    yao_str = "Yao"
    t55_tran_time = 5505
    t55_yao_amount = -55
    x_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_tran_time: t55_yao_amount}}}

    # WHEN
    bob_str = "Bob"
    t55_bob_amount = 600
    x_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_tran_time: t55_yao_amount},
            bob_str: {t55_tran_time: t55_bob_amount},
        }
    }

    # WHEN
    t66_tran_time = 6606
    t66_yao_amount = -66
    x_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)

    # THEN
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            bob_str: {t55_tran_time: t55_bob_amount},
        }
    }

    # WHEN
    t77_tran_time = 7707
    t77_yao_amount = -77
    x_tranbook.add_tranunit(yao_str, yao_str, t77_tran_time, t77_yao_amount)

    # THEN
    print(f"{x_tranbook.tranunits=}")
    assert x_tranbook.tranunits != {}
    assert x_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            bob_str: {t55_tran_time: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_tran_time: t77_yao_amount}},
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
    assert sue_yao_t55_tranunit.tran_time == t55_t
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


def test_TranBook_get_tran_times_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_bob_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t77_tran_time, t77_bob_amount)

    # WHEN
    accord23_tran_times = accord23_tranbook.get_tran_times()

    # THEN
    assert accord23_tran_times
    assert len(accord23_tran_times)
    assert accord23_tran_times == {t55_tran_time, t66_tran_time, t77_tran_time}


def test_TranBook_get_owners_accts_net_ReturnsObj_Scenario0():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_bob_amount = 600
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {bob_str: {t55_tran_time: t55_bob_amount}}
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
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            bob_str: {t55_tran_time: t55_bob_amount},
        }
    }

    # WHEN
    accord23_accts_net_dict = accord23_tranbook.get_owners_accts_net()

    # THEN
    assert accord23_accts_net_dict
    assert accord23_accts_net_dict == {
        sue_str: {yao_str: t55_yao_amount + t66_yao_amount, bob_str: t55_bob_amount}
    }


def test_TranBook_get_accts_net_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_bob_amount = 600
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {bob_str: {t55_tran_time: t55_bob_amount}}
    }

    # WHEN
    accord23_accts_net_dict = accord23_tranbook.get_accts_net_dict()

    # THEN
    assert accord23_accts_net_dict
    assert accord23_accts_net_dict == {bob_str: t55_bob_amount}


def test_TranBook_get_accts_net_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)

    accord23_tranbook.add_tranunit(yao_str, yao_str, t77_tran_time, t77_yao_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            bob_str: {t55_tran_time: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_tran_time: t77_yao_amount}},
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
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)

    accord23_tranbook.add_tranunit(yao_str, yao_str, t77_tran_time, t77_yao_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            bob_str: {t55_tran_time: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_tran_time: t77_yao_amount}},
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
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)

    accord23_tranbook.add_tranunit(yao_str, yao_str, t77_tran_time, t77_yao_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            bob_str: {t55_tran_time: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_tran_time: t77_yao_amount}},
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


def test_TranBook_get_dict_ReturnsObj():
    # ESTABLISH
    accord23_str = "accord23"
    x_TimeLinePoint = 5505
    x_fundnum = -45
    sue_str = "Sue"
    yao_str = "Yao"
    all_tranunits = {sue_str: {yao_str: {x_TimeLinePoint: x_fundnum}}}
    x_tranbook = tranbook_shop(accord23_str, all_tranunits)

    # WHEN
    x_dict = x_tranbook.get_dict()

    # THEN
    tranunits_str = "tranunits"
    assert x_dict
    assert vow_label_str() in x_dict.keys()
    assert x_dict.get(vow_label_str()) == accord23_str
    assert tranunits_str in x_dict.keys()
    tranunits_dict = x_dict.get(tranunits_str)
    assert tranunits_dict.get(sue_str)
    sue_trans_dict = tranunits_dict.get(sue_str)
    assert sue_trans_dict.get(yao_str)
    assert sue_trans_dict.get(yao_str) == {x_TimeLinePoint: x_fundnum}
    assert tranunits_dict == all_tranunits


def test_get_tranbook_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)
    accord23_tranbook.add_tranunit(yao_str, yao_str, t77_tran_time, t77_yao_amount)
    assert accord23_tranbook.tranunits == {
        sue_str: {
            yao_str: {t55_tran_time: t55_yao_amount, t66_tran_time: t66_yao_amount},
            bob_str: {t55_tran_time: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_tran_time: t77_yao_amount}},
    }
    accord23_dict = accord23_tranbook.get_dict()

    # WHEN
    generated_tranbook = get_tranbook_from_dict(accord23_dict)

    # THEN
    assert generated_tranbook
    assert generated_tranbook.vow_label == accord23_str
    assert generated_tranbook.tranunits == accord23_tranbook.tranunits
    assert generated_tranbook == accord23_tranbook


def test_get_tranbook_from_dict_ReturnsObj_Sccenario1():
    # ESTABLISH
    accord23_str = "accord23"
    accord23_tranbook = tranbook_shop(accord23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    accord23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    accord23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)
    accord23_tranbook.add_tranunit(yao_str, yao_str, t77_tran_time, t77_yao_amount)

    str_tran_time_accord23_dict = {
        "vow_label": accord23_str,
        "tranunits": {
            sue_str: {
                yao_str: {
                    str(t55_tran_time): t55_yao_amount,
                    str(t66_tran_time): t66_yao_amount,
                },
                bob_str: {str(t55_tran_time): t55_bob_amount},
            },
            yao_str: {yao_str: {str(t77_tran_time): t77_yao_amount}},
        },
    }

    # WHEN
    generated_tranbook = get_tranbook_from_dict(str_tran_time_accord23_dict)

    # THEN
    assert generated_tranbook
    assert generated_tranbook.vow_label == accord23_str
    assert generated_tranbook.tranunits == accord23_tranbook.tranunits
    assert generated_tranbook == accord23_tranbook


# def test_get_tranbook_from_json_ReturnsObj():
#     # ESTABLISH
#     x_tran_time = 4
#     x_amount = 55
#     x_deal_nets = {"Sue": -57}
#     x_tranbook = tranbook_shop(x_tran_time, x_amount, x_deal_nets)
#     x_json = x_tranbook.get_json()

#     # WHEN
#     x_tranbook = get_tranbook_from_json(x_json)

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.tran_time == x_tran_time
#     assert x_tranbook.amount == x_amount
#     assert x_tranbook._deal_nets == x_deal_nets
#     assert x_tranbook == x_tranbook
