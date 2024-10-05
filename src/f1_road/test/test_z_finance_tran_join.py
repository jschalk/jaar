from src.f1_road.finance_tran import (
    TranUnit,
    tranunit_shop,
    TranBook,
    tranbook_shop,
)
from pytest import raises as pytest_raises


def test_TranBook_join_SetsAttr():
    # ESTABLISH
    m23_tranbook = tranbook_shop("music23")
    sue_str = "Sue"
    yao_str = "Yao"
    t55_t = 5505
    t55_yao_amount = -55
    t66_t = 6606
    t66_yao_amount = -66
    m23_tranbook.set_tranunit(tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount))
    m23_tranbook.set_tranunit(tranunit_shop(sue_str, yao_str, t66_t, t66_yao_amount))
    bob_str = "Bob"

    t55_bob_amount = 600
    m24_tranbook = tranbook_shop("music24")
    m24_tranbook.set_tranunit(tranunit_shop(sue_str, bob_str, t55_t, t55_bob_amount))

    assert m23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)
    assert m23_tranbook.tranunit_exists(sue_str, yao_str, t66_t)
    assert m23_tranbook.tranunit_exists(sue_str, bob_str, t55_t) is False
    assert m24_tranbook.tranunit_exists(sue_str, bob_str, t55_t)

    # WHEN
    m23_tranbook.join(m24_tranbook)

    # THEN
    assert m23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)
    assert m23_tranbook.tranunit_exists(sue_str, yao_str, t66_t)
    assert m23_tranbook.tranunit_exists(sue_str, bob_str, t55_t)
    assert m24_tranbook.tranunit_exists(sue_str, bob_str, t55_t)


# def test_TranBook_set_tranunit_SetsAttrWithBlockTimeStamp():
#     # ESTABLISH
#     music23_str = "music23"
#     x_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_t = 5505
#     t55_yao_amount = -55
#     sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
#     assert x_tranbook.tranunits == {}

#     # WHEN
#     x_blocked_timestamps = {44}
#     x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_blocked_timestamps)

#     # THEN
#     assert x_tranbook.tranunits != {}
#     assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_t: t55_yao_amount}}}


# def test_TranBook_set_tranunit_SetsAttrWithBlockTimeStamp_RaisesError():
#     # ESTABLISH
#     music23_str = "music23"
#     x_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_t = 5505
#     t55_yao_amount = -55
#     x_blocked_timestamps = {t55_t}
#     sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
#     assert x_tranbook.tranunits == {}

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_blocked_timestamps)
#     exception_str = (
#         f"Cannot set tranunit for timestamp={t55_t}, timelinepoint is blocked"
#     )
#     assert str(excinfo.value) == exception_str


# def test_TranBook_set_tranunit_SetsAttrWithCurrentTimeStamp():
#     # ESTABLISH
#     music23_str = "music23"
#     x_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_t = 5505
#     t55_yao_amount = -55
#     sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
#     assert x_tranbook.tranunits == {}

#     # WHEN
#     x_current_time = 8808
#     x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_current_time=x_current_time)

#     # THEN
#     assert x_tranbook.tranunits != {}
#     assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_t: t55_yao_amount}}}


# def test_TranBook_set_tranunit_SetsAttrWithCurrentTimeStamp_RaisesError():
#     # ESTABLISH
#     music23_str = "music23"
#     x_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_t = 5505
#     t55_yao_amount = -55
#     sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
#     assert x_tranbook.tranunits == {}

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_current_time=t55_t)
#     exception_str = f"Cannot set tranunit for timestamp={t55_t}, timelinepoint is greater than current time={t55_t}"
#     assert str(excinfo.value) == exception_str

#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         x_tranbook.set_tranunit(sue_yao_t55_tranunit, x_current_time=33)
#     exception_str = f"Cannot set tranunit for timestamp={t55_t}, timelinepoint is greater than current time=33"
#     assert str(excinfo.value) == exception_str


# def test_TranBook_add_tranunit_SetsAttr():
#     # ESTABLISH
#     music23_str = "music23"
#     x_tranbook = tranbook_shop(music23_str)
#     assert x_tranbook.tranunits == {}

#     # WHEN
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_timestamp = 5505
#     t55_yao_amount = -55
#     x_tranbook.add_tranunit(sue_str, yao_str, t55_timestamp, t55_yao_amount)

#     # THEN
#     assert x_tranbook.tranunits != {}
#     assert x_tranbook.tranunits == {sue_str: {yao_str: {t55_timestamp: t55_yao_amount}}}

#     # WHEN
#     bob_str = "Bob"
#     t55_bob_amount = 600
#     x_tranbook.add_tranunit(sue_str, bob_str, t55_timestamp, t55_bob_amount)

#     # THEN
#     assert x_tranbook.tranunits != {}
#     assert x_tranbook.tranunits == {
#         sue_str: {
#             yao_str: {t55_timestamp: t55_yao_amount},
#             bob_str: {t55_timestamp: t55_bob_amount},
#         }
#     }

#     # WHEN
#     t66_timestamp = 6606
#     t66_yao_amount = -66
#     x_tranbook.add_tranunit(sue_str, yao_str, t66_timestamp, t66_yao_amount)

#     # THEN
#     assert x_tranbook.tranunits != {}
#     assert x_tranbook.tranunits == {
#         sue_str: {
#             yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
#             bob_str: {t55_timestamp: t55_bob_amount},
#         }
#     }

#     # WHEN
#     t77_timestamp = 7707
#     t77_yao_amount = -77
#     x_tranbook.add_tranunit(yao_str, yao_str, t77_timestamp, t77_yao_amount)

#     # THEN
#     print(f"{x_tranbook.tranunits=}")
#     assert x_tranbook.tranunits != {}
#     assert x_tranbook.tranunits == {
#         sue_str: {
#             yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
#             bob_str: {t55_timestamp: t55_bob_amount},
#         },
#         yao_str: {yao_str: {t77_timestamp: t77_yao_amount}},
#     }


# def test_TranBook_tranunit_exists_ReturnsObj():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_t = 5505
#     t55_yao_amount = -55
#     sue_yao_t55_tranunit = tranunit_shop(sue_str, yao_str, t55_t, t55_yao_amount)
#     assert music23_tranbook.tranunit_exists(sue_str, yao_str, t55_t) is False

#     # WHEN
#     music23_tranbook.set_tranunit(sue_yao_t55_tranunit)

#     # THEN
#     assert music23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)


# def test_TranBook_get_tranunit_ReturnsObj():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_t = 5505
#     t55_yao_amount = -55
#     music23_tranbook.add_tranunit(sue_str, yao_str, t55_t, t55_yao_amount)
#     assert music23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)

#     # WHEN
#     sue_yao_t55_tranunit = music23_tranbook.get_tranunit(sue_str, yao_str, t55_t)

#     # THEN
#     assert sue_yao_t55_tranunit
#     assert sue_yao_t55_tranunit.src == sue_str
#     assert sue_yao_t55_tranunit.dst == yao_str
#     assert sue_yao_t55_tranunit.timestamp == t55_t
#     assert sue_yao_t55_tranunit.amount == t55_yao_amount

#     # WHEN / THEN
#     assert not music23_tranbook.get_tranunit(sue_str, "Bob", t55_t)
#     assert not music23_tranbook.get_tranunit("Bob", yao_str, t55_t)
#     assert not music23_tranbook.get_tranunit(sue_str, yao_str, 44)


# def test_TranBook_get_amount_ReturnsObj():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_t = 5505
#     t55_yao_amount = -55
#     music23_tranbook.add_tranunit(sue_str, yao_str, t55_t, t55_yao_amount)
#     assert music23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)

#     # WHEN
#     assert music23_tranbook.get_amount(sue_str, yao_str, t55_t) == t55_yao_amount
#     assert not music23_tranbook.get_amount(sue_str, "Bob", t55_t)
#     assert not music23_tranbook.get_amount("Bob", yao_str, t55_t)
#     assert not music23_tranbook.get_amount(sue_str, yao_str, 44)


# def test_TranBook_del_tranunit_SetsAttr():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     t55_t = 5505
#     t55_yao_amount = -55
#     music23_tranbook.add_tranunit(sue_str, yao_str, t55_t, t55_yao_amount)
#     assert music23_tranbook.tranunit_exists(sue_str, yao_str, t55_t)

#     # WHEN
#     music23_tranbook.del_tranunit(sue_str, yao_str, t55_t)

#     # THEN
#     assert music23_tranbook.tranunit_exists(sue_str, yao_str, t55_t) is False


# def test_TranBook_get_timestamps_ReturnsObj():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     bob_str = "Bob"
#     t55_timestamp = 5505
#     t55_yao_amount = -55
#     t55_bob_amount = 600
#     t66_timestamp = 6606
#     t66_yao_amount = -66
#     t77_timestamp = 7707
#     t77_bob_amount = -77
#     music23_tranbook.add_tranunit(sue_str, yao_str, t55_timestamp, t55_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, yao_str, t66_timestamp, t66_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, bob_str, t77_timestamp, t77_bob_amount)

#     # WHEN
#     music23_timestamps = music23_tranbook.get_timestamps()

#     # THEN
#     assert music23_timestamps
#     assert len(music23_timestamps)
#     assert music23_timestamps == {t55_timestamp, t66_timestamp, t77_timestamp}


# def test_TranBook_get_owners_accts_net_ReturnObj_Scenario0():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     bob_str = "Bob"
#     t55_timestamp = 5505
#     t55_bob_amount = 600
#     music23_tranbook.add_tranunit(sue_str, bob_str, t55_timestamp, t55_bob_amount)
#     assert music23_tranbook.tranunits == {
#         sue_str: {bob_str: {t55_timestamp: t55_bob_amount}}
#     }

#     # WHEN
#     music23_accts_net_dict = music23_tranbook.get_owners_accts_net()

#     # THEN
#     assert music23_accts_net_dict
#     assert music23_accts_net_dict == {sue_str: {bob_str: t55_bob_amount}}


# def test_TranBook_get_owners_accts_net_ReturnsObj_Scenario1():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     bob_str = "Bob"
#     t55_timestamp = 5505
#     t55_yao_amount = -55
#     t55_bob_amount = 600
#     t66_timestamp = 6606
#     t66_yao_amount = -66
#     music23_tranbook.add_tranunit(sue_str, yao_str, t55_timestamp, t55_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, yao_str, t66_timestamp, t66_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, bob_str, t55_timestamp, t55_bob_amount)
#     assert music23_tranbook.tranunits == {
#         sue_str: {
#             yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
#             bob_str: {t55_timestamp: t55_bob_amount},
#         }
#     }

#     # WHEN
#     music23_accts_net_dict = music23_tranbook.get_owners_accts_net()

#     # THEN
#     assert music23_accts_net_dict
#     assert music23_accts_net_dict == {
#         sue_str: {yao_str: t55_yao_amount + t66_yao_amount, bob_str: t55_bob_amount}
#     }


# def test_TranBook_get_accts_net_dict_ReturnObj_Scenario0():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     bob_str = "Bob"
#     t55_timestamp = 5505
#     t55_bob_amount = 600
#     music23_tranbook.add_tranunit(sue_str, bob_str, t55_timestamp, t55_bob_amount)
#     assert music23_tranbook.tranunits == {
#         sue_str: {bob_str: {t55_timestamp: t55_bob_amount}}
#     }

#     # WHEN
#     music23_accts_net_dict = music23_tranbook.get_accts_net_dict()

#     # THEN
#     assert music23_accts_net_dict
#     assert music23_accts_net_dict == {bob_str: t55_bob_amount}


# def test_TranBook_get_accts_net_dict_ReturnObj_Scenario1():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     bob_str = "Bob"
#     t55_timestamp = 5505
#     t55_yao_amount = -55
#     t55_bob_amount = 600
#     t66_timestamp = 6606
#     t66_yao_amount = -66
#     t77_timestamp = 7707
#     t77_yao_amount = -77
#     music23_tranbook.add_tranunit(sue_str, yao_str, t55_timestamp, t55_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, yao_str, t66_timestamp, t66_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, bob_str, t55_timestamp, t55_bob_amount)

#     music23_tranbook.add_tranunit(yao_str, yao_str, t77_timestamp, t77_yao_amount)
#     assert music23_tranbook.tranunits == {
#         sue_str: {
#             yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
#             bob_str: {t55_timestamp: t55_bob_amount},
#         },
#         yao_str: {yao_str: {t77_timestamp: t77_yao_amount}},
#     }

#     # WHEN
#     music23_accts_net_dict = music23_tranbook.get_accts_net_dict()

#     # THEN
#     assert music23_accts_net_dict
#     assert music23_accts_net_dict == {
#         yao_str: t55_yao_amount + t66_yao_amount + t77_yao_amount,
#         bob_str: t55_bob_amount,
#     }


# def test_TranBook_get_accts_net_array_ReturnsObj():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     bob_str = "Bob"
#     t55_timestamp = 5505
#     t55_yao_amount = -55
#     t55_bob_amount = 600
#     t66_timestamp = 6606
#     t66_yao_amount = -66
#     t77_timestamp = 7707
#     t77_yao_amount = -77
#     music23_tranbook.add_tranunit(sue_str, yao_str, t55_timestamp, t55_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, yao_str, t66_timestamp, t66_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, bob_str, t55_timestamp, t55_bob_amount)

#     music23_tranbook.add_tranunit(yao_str, yao_str, t77_timestamp, t77_yao_amount)
#     assert music23_tranbook.tranunits == {
#         sue_str: {
#             yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
#             bob_str: {t55_timestamp: t55_bob_amount},
#         },
#         yao_str: {yao_str: {t77_timestamp: t77_yao_amount}},
#     }

#     # WHEN
#     music23_accts_net_array = music23_tranbook._get_accts_net_array()

#     # THEN
#     assert music23_accts_net_array
#     assert music23_accts_net_array == [
#         [bob_str, t55_bob_amount],
#         [yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount],
#     ]


# def test_TranBook_get_accts_headers_ReturnsObj():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)

#     # WHEN / THEN
#     assert music23_tranbook._get_accts_headers() == ["acct_id", "net_amount"]


# def test_TranBook_get_accts_csv_ReturnsObj():
#     # ESTABLISH
#     music23_str = "music23"
#     music23_tranbook = tranbook_shop(music23_str)
#     sue_str = "Sue"
#     yao_str = "Yao"
#     bob_str = "Bob"
#     t55_timestamp = 5505
#     t55_yao_amount = -55
#     t55_bob_amount = 600
#     t66_timestamp = 6606
#     t66_yao_amount = -66
#     t77_timestamp = 7707
#     t77_yao_amount = -77
#     music23_tranbook.add_tranunit(sue_str, yao_str, t55_timestamp, t55_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, yao_str, t66_timestamp, t66_yao_amount)
#     music23_tranbook.add_tranunit(sue_str, bob_str, t55_timestamp, t55_bob_amount)

#     music23_tranbook.add_tranunit(yao_str, yao_str, t77_timestamp, t77_yao_amount)
#     assert music23_tranbook.tranunits == {
#         sue_str: {
#             yao_str: {t55_timestamp: t55_yao_amount, t66_timestamp: t66_yao_amount},
#             bob_str: {t55_timestamp: t55_bob_amount},
#         },
#         yao_str: {yao_str: {t77_timestamp: t77_yao_amount}},
#     }

#     # WHEN
#     music23_accts_net_csv = music23_tranbook.get_accts_net_csv()

#     # THEN
#     assert music23_accts_net_csv
#     example_csv = f"""acct_id,net_amount
# {bob_str},{t55_bob_amount}
# {yao_str},{t55_yao_amount + t66_yao_amount + t77_yao_amount}
# """
#     assert music23_accts_net_csv == example_csv
