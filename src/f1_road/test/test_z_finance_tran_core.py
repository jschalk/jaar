from src.f1_road.finance import default_fund_pool
from src.f1_road.finance_tran import (
    TranBook,
    tranbook_shop,
    get_tranbook_from_dict,
    get_tranbook_from_json,
    get_outlaylog_from_dict,
)
from pytest import raises as pytest_raises


def test_TranBook_Exists():
    # ESTABLISH / WHEN
    x_tranbook = TranBook()

    # THEN
    assert x_tranbook
    assert not x_tranbook.fiscal_id
    assert not x_tranbook.tranlogs
    assert not x_tranbook.tender_desc
    assert not x_tranbook._accts_net


def test_tranbook_shop_WithParametersReturnsObj():
    # ESTABLISH
    music23_str = "music23"
    ducet_str = "ducet"
    x_timelinepoint = 5505
    x_fundnum = -45
    sue_str = "Sue"
    yao_str = "Yao"
    x_tranlogs = {sue_str: {yao_str: {x_timelinepoint: x_fundnum}}}

    # WHEN
    x_tranbook = tranbook_shop(music23_str, x_tranlogs, ducet_str)

    # THEN
    assert x_tranbook
    assert x_tranbook.fiscal_id == music23_str
    assert x_tranbook.tranlogs == x_tranlogs
    assert x_tranbook.tender_desc == ducet_str
    assert x_tranbook._accts_net == {}


def test_tranbook_shop_WithoutParametersReturnsObj():
    # ESTABLISH
    music23_str = "music23"

    # WHEN
    x_tranbook = tranbook_shop(music23_str)

    # THEN
    assert x_tranbook
    assert x_tranbook.fiscal_id == music23_str
    assert x_tranbook.tranlogs == {}
    assert x_tranbook.tender_desc is None
    assert x_tranbook._accts_net == {}


def test_TranBook_set_tranlog_SetsAttr():
    # ESTABLISH
    music23_str = "music23"
    x_tranbook = tranbook_shop(music23_str)
    assert x_tranbook.tranlogs == {}

    # WHEN
    sue_str = "Sue"
    yao_str = "Yao"
    t55_timestamp = 5505
    t55_yao_amount = -55
    x_tranbook.set_tranlog(sue_str, yao_str, t55_timestamp, t55_yao_amount)

    # THEN
    assert x_tranbook.tranlogs != {}
    assert x_tranbook.tranlogs == {sue_str: {yao_str: {t55_timestamp: t55_yao_amount}}}

    # WHEN
    bob_str = "Bob"
    t55_bob_amount = 600
    x_tranbook.set_tranlog(sue_str, bob_str, t55_timestamp, t55_bob_amount)

    # THEN
    assert x_tranbook.tranlogs != {}
    assert x_tranbook.tranlogs == {
        sue_str: {
            yao_str: {t55_timestamp: t55_yao_amount},
            bob_str: {t55_timestamp: t55_bob_amount},
        }
    }

    # WHEN
    t66_timestamp = 6606
    t66_yao_amount = -66
    x_tranbook.set_tranlog(sue_str, yao_str, t66_timestamp, t66_yao_amount)

    # THEN
    assert x_tranbook.tranlogs != {}
    assert x_tranbook.tranlogs == {
        sue_str: {
            yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
            bob_str: {t55_timestamp: t55_bob_amount},
        }
    }

    # WHEN
    t77_timestamp = 7707
    t77_yao_amount = -77
    x_tranbook.set_tranlog(yao_str, yao_str, t77_timestamp, t77_yao_amount)

    # THEN
    print(f"{x_tranbook.tranlogs=}")
    assert x_tranbook.tranlogs != {}
    assert x_tranbook.tranlogs == {
        sue_str: {
            yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
            bob_str: {t55_timestamp: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_timestamp: t77_yao_amount}},
    }


def test_TranBook_get_owners_accts_net_ReturnObj_Scenario0():
    # ESTABLISH
    music23_str = "music23"
    music23_tranbook = tranbook_shop(music23_str)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_timestamp = 5505
    t55_bob_amount = 600
    music23_tranbook.set_tranlog(sue_str, bob_str, t55_timestamp, t55_bob_amount)
    assert music23_tranbook.tranlogs == {
        sue_str: {bob_str: {t55_timestamp: t55_bob_amount}}
    }

    # WHEN
    music23_accts_net_dict = music23_tranbook.get_owners_accts_net()

    # THEN
    assert music23_accts_net_dict
    assert music23_accts_net_dict == {sue_str: {bob_str: t55_bob_amount}}


def test_TranBook_get_owners_accts_net_ReturnsObj_Scenario1():
    # ESTABLISH
    music23_str = "music23"
    music23_tranbook = tranbook_shop(music23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_timestamp = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_timestamp = 6606
    t66_yao_amount = -66
    music23_tranbook.set_tranlog(sue_str, yao_str, t55_timestamp, t55_yao_amount)
    music23_tranbook.set_tranlog(sue_str, yao_str, t66_timestamp, t66_yao_amount)
    music23_tranbook.set_tranlog(sue_str, bob_str, t55_timestamp, t55_bob_amount)
    assert music23_tranbook.tranlogs == {
        sue_str: {
            yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
            bob_str: {t55_timestamp: t55_bob_amount},
        }
    }

    # WHEN
    music23_accts_net_dict = music23_tranbook.get_owners_accts_net()

    # THEN
    assert music23_accts_net_dict
    assert music23_accts_net_dict == {
        sue_str: {yao_str: t55_yao_amount + t66_yao_amount, bob_str: t55_bob_amount}
    }


def test_TranBook_get_accts_net_dict_ReturnObj_Scenario0():
    # ESTABLISH
    music23_str = "music23"
    music23_tranbook = tranbook_shop(music23_str)
    sue_str = "Sue"
    bob_str = "Bob"
    t55_timestamp = 5505
    t55_bob_amount = 600
    music23_tranbook.set_tranlog(sue_str, bob_str, t55_timestamp, t55_bob_amount)
    assert music23_tranbook.tranlogs == {
        sue_str: {bob_str: {t55_timestamp: t55_bob_amount}}
    }

    # WHEN
    music23_accts_net_dict = music23_tranbook.get_accts_net_dict()

    # THEN
    assert music23_accts_net_dict
    assert music23_accts_net_dict == {bob_str: t55_bob_amount}


def test_TranBook_get_accts_net_dict_ReturnObj_Scenario1():
    # ESTABLISH
    music23_str = "music23"
    music23_tranbook = tranbook_shop(music23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_timestamp = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_timestamp = 6606
    t66_yao_amount = -66
    t77_timestamp = 7707
    t77_yao_amount = -77
    music23_tranbook.set_tranlog(sue_str, yao_str, t55_timestamp, t55_yao_amount)
    music23_tranbook.set_tranlog(sue_str, yao_str, t66_timestamp, t66_yao_amount)
    music23_tranbook.set_tranlog(sue_str, bob_str, t55_timestamp, t55_bob_amount)

    music23_tranbook.set_tranlog(yao_str, yao_str, t77_timestamp, t77_yao_amount)
    assert music23_tranbook.tranlogs == {
        sue_str: {
            yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
            bob_str: {t55_timestamp: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_timestamp: t77_yao_amount}},
    }

    # WHEN
    music23_accts_net_dict = music23_tranbook.get_accts_net_dict()

    # THEN
    assert music23_accts_net_dict
    assert music23_accts_net_dict == {
        yao_str: t55_yao_amount + t66_yao_amount + t77_yao_amount,
        bob_str: t55_bob_amount,
    }


def test_TranBook_get_accts_net_array_ReturnsObj():
    # ESTABLISH
    music23_str = "music23"
    music23_tranbook = tranbook_shop(music23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_timestamp = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_timestamp = 6606
    t66_yao_amount = -66
    t77_timestamp = 7707
    t77_yao_amount = -77
    music23_tranbook.set_tranlog(sue_str, yao_str, t55_timestamp, t55_yao_amount)
    music23_tranbook.set_tranlog(sue_str, yao_str, t66_timestamp, t66_yao_amount)
    music23_tranbook.set_tranlog(sue_str, bob_str, t55_timestamp, t55_bob_amount)

    music23_tranbook.set_tranlog(yao_str, yao_str, t77_timestamp, t77_yao_amount)
    assert music23_tranbook.tranlogs == {
        sue_str: {
            yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
            bob_str: {t55_timestamp: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_timestamp: t77_yao_amount}},
    }

    # WHEN
    music23_accts_net_array = music23_tranbook._get_accts_net_array()

    # THEN
    assert music23_accts_net_array
    assert music23_accts_net_array == [
        [bob_str, t55_bob_amount],
        [yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount],
    ]


def test_TranBook_get_accts_headers_ReturnsObj():
    # ESTABLISH
    music23_str = "music23"
    music23_tranbook = tranbook_shop(music23_str)

    # WHEN / THEN
    assert music23_tranbook._get_accts_headers() == ["acct_id", "net_amount"]


def test_TranBook_get_accts_csv_ReturnsObj():
    # ESTABLISH
    music23_str = "music23"
    music23_tranbook = tranbook_shop(music23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_timestamp = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_timestamp = 6606
    t66_yao_amount = -66
    t77_timestamp = 7707
    t77_yao_amount = -77
    music23_tranbook.set_tranlog(sue_str, yao_str, t55_timestamp, t55_yao_amount)
    music23_tranbook.set_tranlog(sue_str, yao_str, t66_timestamp, t66_yao_amount)
    music23_tranbook.set_tranlog(sue_str, bob_str, t55_timestamp, t55_bob_amount)

    music23_tranbook.set_tranlog(yao_str, yao_str, t77_timestamp, t77_yao_amount)
    assert music23_tranbook.tranlogs == {
        sue_str: {
            yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
            bob_str: {t55_timestamp: t55_bob_amount},
        },
        yao_str: {yao_str: {t77_timestamp: t77_yao_amount}},
    }

    # WHEN
    music23_accts_net_csv = music23_tranbook.get_accts_net_csv()

    # THEN
    assert music23_accts_net_csv
    example_csv = f"""acct_id,net_amount
{bob_str},{t55_bob_amount}
{yao_str},{t55_yao_amount + t66_yao_amount + t77_yao_amount}
"""
    assert music23_accts_net_csv == example_csv


# def test_TranBook_get_dict_ReturnsObj():
#     # ESTABLISH
#     music23_str = "music23"
#     ducet_str = "ducet"
#     x_timelinepoint = 5505
#     x_fundnum = -45
#     sue_str = "Sue"
#     yao_str = "Yao"
#     x_tranlogs = {sue_str: {yao_str: {x_timelinepoint: x_fundnum}}}
#     x_tranbook = tranbook_shop(music23_str, x_tranlogs, ducet_str)

#     # WHEN
#     x_dict = x_tranbook.get_dict()

#     # THEN
#     assert x_dict
#     assert "music23_str" in x_dict.keys()
#     music23_dict = x_dict.get(music23_str)
#     assert music23_dict
#     assert music23_dict == x_tranlogs


# def test_tranbook_shop_ReturnsObjWith_net_outlays():
#     # ESTABLISH
#     x_timestamp = 4
#     x_purview = 55
#     x_net_outlays = {"Sue": -4}
#     x_magnitude = 677

#     # WHEN
#     x_tranbook = tranbook_shop(
#         x_timestamp=x_timestamp,
#         x_purview=x_purview,
#         net_outlays=x_net_outlays,
#         x_magnitude=x_magnitude,
#     )

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.timestamp == x_timestamp
#     assert x_tranbook.purview == x_purview
#     assert x_tranbook._magnitude == 677
#     assert x_tranbook._net_outlays == x_net_outlays
#     assert not x_tranbook._tender_desc


# def test_TranBook_set_net_outlay_SetsAttr():
#     # ESTABLISH
#     yao_tranbook = tranbook_shop("yao", 33)
#     assert yao_tranbook._net_outlays == {}

#     # WHEN
#     sue_text = "Sue"
#     sue_outlay = -44
#     yao_tranbook.set_net_outlay(sue_text, sue_outlay)

#     # THEN
#     assert yao_tranbook._net_outlays != {}
#     assert yao_tranbook._net_outlays.get(sue_text) == sue_outlay


# def test_TranBook_net_outlay_exists_ReturnsObj():
#     # ESTABLISH
#     yao_tranbook = tranbook_shop("yao", 33)
#     sue_text = "Sue"
#     sue_outlay = -44
#     assert yao_tranbook.net_outlay_exists(sue_text) is False

#     # WHEN
#     yao_tranbook.set_net_outlay(sue_text, sue_outlay)

#     # THEN
#     assert yao_tranbook.net_outlay_exists(sue_text)


# def test_TranBook_get_net_outlay_ReturnsObj():
#     # ESTABLISH
#     yao_tranbook = tranbook_shop("yao", 33)
#     sue_text = "Sue"
#     sue_outlay = -44
#     yao_tranbook.set_net_outlay(sue_text, sue_outlay)

#     # WHEN / THEN
#     assert yao_tranbook.get_net_outlay(sue_text)
#     assert yao_tranbook.get_net_outlay(sue_text) == sue_outlay


# def test_TranBook_del_net_outlay_SetsAttr():
#     # ESTABLISH
#     yao_tranbook = tranbook_shop("yao", 33)
#     sue_text = "Sue"
#     sue_outlay = -44
#     yao_tranbook.set_net_outlay(sue_text, sue_outlay)
#     assert yao_tranbook.net_outlay_exists(sue_text)

#     # WHEN
#     yao_tranbook.del_net_outlay(sue_text)

#     # THEN
#     assert yao_tranbook.net_outlay_exists(sue_text) is False


# def test_TranBook_get_dict_ReturnsObj():
#     # ESTABLISH
#     x_timestamp = 4
#     x_purview = 55
#     x_tranbook = tranbook_shop(x_timestamp, x_purview)

#     # WHEN
#     x_dict = x_tranbook.get_dict()

#     # THEN
#     assert x_dict == {"timestamp": x_timestamp, "purview": x_purview}


# def test_TranBook_calc_magnitude_SetsAttr_Scenario0():
#     # ESTABLISH
#     x_timestamp = 4
#     x_tranbook = tranbook_shop(x_timestamp)
#     assert x_tranbook._magnitude == 0

#     # WHEN
#     x_tranbook.calc_magnitude()

#     # THEN
#     assert x_tranbook._magnitude == 0


# def test_TranBook_calc_magnitude_SetsAttr_Scenario1():
#     # ESTABLISH
#     x_timestamp = 4
#     x_net_outlays = {"Sue": -4, "Yao": 2, "Zia": 2}

#     x_tranbook = tranbook_shop(x_timestamp, net_outlays=x_net_outlays)
#     assert x_tranbook._magnitude == 0

#     # WHEN
#     x_tranbook.calc_magnitude()

#     # THEN
#     assert x_tranbook._magnitude == 4


# def test_TranBook_calc_magnitude_SetsAttr_Scenario2():
#     # ESTABLISH
#     x_timestamp = 4
#     x_net_outlays = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

#     x_tranbook = tranbook_shop(x_timestamp, net_outlays=x_net_outlays)
#     assert x_tranbook._magnitude == 0

#     # WHEN
#     x_tranbook.calc_magnitude()

#     # THEN
#     assert x_tranbook._magnitude == 20


# def test_TranBook_calc_magnitude_SetsAttr_Scenario3_RaisesError():
#     # ESTABLISH
#     x_timestamp = 4
#     bob_outlay = -13
#     sue_outlay = -3
#     yao_outlay = 100
#     x_net_outlays = {"Bob": bob_outlay, "Sue": sue_outlay, "Yao": yao_outlay}
#     x_tranbook = tranbook_shop(x_timestamp, net_outlays=x_net_outlays)

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         x_tranbook.calc_magnitude()
#     exception_str = f"magnitude cannot be calculated: debt_outlay={bob_outlay+sue_outlay}, cred_outlay={yao_outlay}"
#     assert str(excinfo.value) == exception_str


# def test_TranBook_get_dict_ReturnsObjWith_net_outlays():
#     # ESTABLISH
#     x_timestamp = 4
#     x_purview = 55
#     x_net_outlays = {"Sue": -4}
#     x_magnitude = 67
#     x_tranbook = tranbook_shop(x_timestamp, x_purview, x_net_outlays)
#     x_tranbook._magnitude = 67

#     # WHEN
#     x_dict = x_tranbook.get_dict()

#     # THEN
#     assert x_dict == {
#         "timestamp": x_timestamp,
#         "purview": x_purview,
#         "magnitude": x_magnitude,
#         "net_outlays": x_net_outlays,
#     }


# def test_TranBook_get_json_ReturnsObj():
#     # ESTABLISH
#     x_timestamp = 4
#     x_purview = 55
#     x_net_outlays = {"Sue": -77}
#     x_tranbook = tranbook_shop(x_timestamp, x_purview, x_net_outlays)
#     x_tranbook._magnitude = 67

#     # WHEN
#     x_json = x_tranbook.get_json()

#     # THEN
#     static_x_json = """{
#   "magnitude": 67,
#   "net_outlays": {
#     "Sue": -77
#   },
#   "purview": 55,
#   "timestamp": 4
# }"""
#     print(f"{x_json=}")
#     assert x_json == static_x_json


# def test_get_tranbook_from_dict_ReturnsObj_Sccenario0():
#     # ESTABLISH
#     x_timestamp = 4
#     x_purview = 55
#     x_tranbook = tranbook_shop(x_timestamp, x_purview)
#     x_dict = x_tranbook.get_dict()
#     assert x_dict == {"timestamp": x_timestamp, "purview": x_purview}

#     # WHEN
#     x_tranbook = get_tranbook_from_dict(x_dict)

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.timestamp == x_timestamp
#     assert x_tranbook.purview == x_purview
#     assert x_tranbook._magnitude == 0
#     assert x_tranbook == x_tranbook


# def test_get_tranbook_from_dict_ReturnsObj_Scenario1():
#     # ESTABLISH
#     x_timestamp = 4
#     x_purview = 55
#     x_magnitude = 65
#     x_net_outlays = {"Sue": -77}
#     x_tranbook = tranbook_shop(x_timestamp, x_purview, x_net_outlays)
#     x_tranbook._magnitude = x_magnitude
#     x_dict = x_tranbook.get_dict()

#     # WHEN
#     x_tranbook = get_tranbook_from_dict(x_dict)

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.timestamp == x_timestamp
#     assert x_tranbook.purview == x_purview
#     assert x_tranbook._magnitude == x_magnitude
#     assert x_tranbook._net_outlays == x_net_outlays
#     assert x_tranbook == x_tranbook


# def test_get_tranbook_from_json_ReturnsObj():
#     # ESTABLISH
#     x_timestamp = 4
#     x_purview = 55
#     x_net_outlays = {"Sue": -57}
#     x_tranbook = tranbook_shop(x_timestamp, x_purview, x_net_outlays)
#     x_json = x_tranbook.get_json()

#     # WHEN
#     x_tranbook = get_tranbook_from_json(x_json)

#     # THEN
#     assert x_tranbook
#     assert x_tranbook.timestamp == x_timestamp
#     assert x_tranbook.purview == x_purview
#     assert x_tranbook._net_outlays == x_net_outlays
#     assert x_tranbook == x_tranbook
