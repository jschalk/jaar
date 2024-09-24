from src.s1_road.finance_outlay import (
    OutlayEvent,
    outlayevent_shop,
    OutlayLog,
    outlaylog_shop,
    get_outlayevent_from_dict,
    get_outlaylog_from_dict,
)


def test_OutlayEvent_Exists():
    # ESTABLISH / WHEN
    x_outlayevent = OutlayEvent()

    # THEN
    assert x_outlayevent
    assert not x_outlayevent.timestamp
    assert not x_outlayevent.money_magnitude
    assert not x_outlayevent._net_outlays
    assert not x_outlayevent._tender_desc


def test_outlayevent_shop_ReturnsObj():
    # ESTABLISH
    y_timestamp = 4
    y_magnitude = 55

    # WHEN
    x_outlayevent = outlayevent_shop(y_timestamp, y_magnitude)

    # THEN
    assert x_outlayevent
    assert x_outlayevent.timestamp == y_timestamp
    assert x_outlayevent.money_magnitude == y_magnitude
    assert not x_outlayevent._net_outlays
    assert not x_outlayevent._tender_desc


def test_outlayevent_shop_ReturnsObjWith_net_outlays():
    # ESTABLISH
    y_timestamp = 4
    y_magnitude = 55
    y_net_outlays = {"Sue": -4}

    # WHEN
    x_outlayevent = outlayevent_shop(y_timestamp, y_magnitude, y_net_outlays)

    # THEN
    assert x_outlayevent
    assert x_outlayevent.timestamp == y_timestamp
    assert x_outlayevent.money_magnitude == y_magnitude
    assert x_outlayevent._net_outlays == y_net_outlays
    assert not x_outlayevent._tender_desc


def test_OutlayEvent_get_array_ReturnsObj():
    # ESTABLISH
    y_timestamp = 4
    y_magnitude = 55
    x_outlayevent = outlayevent_shop(y_timestamp, y_magnitude)

    # WHEN
    x_array = x_outlayevent.get_array()

    # THEN
    assert x_array == [y_timestamp, y_magnitude]


def test_OutlayEvent_get_dict_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_outlayevent = outlayevent_shop(t4_timestamp, t4_magnitude)

    # WHEN
    t4_dict = t4_outlayevent.get_dict()

    # THEN
    assert t4_dict == {"timestamp": t4_timestamp, "money_magnitude": t4_magnitude}


def test_OutlayLog_Exists():
    # ESTABLISH / WHEN
    x_outlaylog = OutlayLog()

    # THEN
    assert x_outlaylog
    assert not x_outlaylog.owner_id
    assert not x_outlaylog.events
    assert not x_outlaylog._sum_money_magnitude
    assert not x_outlaylog._sum_acct_outlays
    assert not x_outlaylog._timestamp_min
    assert not x_outlaylog._timestamp_max


def test_outlaylog_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_outlaylog = outlaylog_shop(sue_str)

    # THEN
    assert x_outlaylog
    assert x_outlaylog.owner_id == sue_str
    assert x_outlaylog.events == {}
    assert not x_outlaylog._sum_money_magnitude
    assert x_outlaylog._sum_acct_outlays == {}
    assert not x_outlaylog._timestamp_min
    assert not x_outlaylog._timestamp_max


def test_OutlayLog_set_event_SetsAttr():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("sue")
    assert sue_outlaylog.events == {}

    # WHEN
    t1_int = 145
    t1_outlayevent = outlayevent_shop(t1_int, 0)
    sue_outlaylog.set_event(t1_outlayevent)

    # THEN
    assert sue_outlaylog.events != {}
    assert sue_outlaylog.events.get(t1_int) == t1_outlayevent


def test_OutlayLog_event_exists_ReturnsObj():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("Sue")
    t1_int = 145
    assert sue_outlaylog.event_exists(t1_int) is False

    # WHEN
    t1_outlayevent = outlayevent_shop(t1_int, 0)
    sue_outlaylog.set_event(t1_outlayevent)

    # THEN
    assert sue_outlaylog.event_exists(t1_int)


def test_OutlayLog_get_event_ReturnsObj():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("sue")
    t1_int = 145
    t1_stat_outlayevent = outlayevent_shop(t1_int, 0)
    sue_outlaylog.set_event(t1_stat_outlayevent)

    # WHEN
    t1_gen_outlayevent = sue_outlaylog.get_event(t1_int)

    # THEN
    assert t1_gen_outlayevent
    assert t1_gen_outlayevent == t1_stat_outlayevent


def test_OutlayLog_del_event_SetsAttr():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("Sue")
    t1_int = 145
    t1_stat_outlayevent = outlayevent_shop(t1_int, 0)
    sue_outlaylog.set_event(t1_stat_outlayevent)
    assert sue_outlaylog.event_exists(t1_int)

    # WHEN
    sue_outlaylog.del_event(t1_int)

    # THEN
    assert sue_outlaylog.event_exists(t1_int) is False


def test_OutlayLog_add_event_SetsAttr():
    # ESTABLISH
    sue_outlaylog = outlaylog_shop("sue")
    assert sue_outlaylog.events == {}

    # WHEN
    t1_int = 145
    t1_money_magnitude = 500
    sue_outlaylog.add_event(t1_int, t1_money_magnitude)

    # THEN
    assert sue_outlaylog.events != {}
    t1_outlayevent = outlayevent_shop(t1_int, t1_money_magnitude)
    assert sue_outlaylog.events.get(t1_int) == t1_outlayevent


def test_OutlayLog_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)

    # WHEN
    sue_events_2d_array = sue_outlaylog.get_2d_array()

    # THEN
    assert sue_events_2d_array == []


def test_OutlayLog_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_outlaylog.add_event(x4_timestamp, x4_magnitude)
    sue_outlaylog.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_events_2d_array = sue_outlaylog.get_2d_array()

    # THEN
    assert sue_events_2d_array == [
        [sue_str, x4_timestamp, x4_magnitude],
        [sue_str, x7_timestamp, x7_magnitude],
    ]


def test_OutlayLog_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_outlaylog.add_event(x4_timestamp, x4_magnitude)
    sue_outlaylog.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_headers_list = sue_outlaylog.get_headers()

    # THEN
    assert sue_headers_list == ["owner_id", "timestamp", "money_magnitude"]


def test_OutlayLog_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_outlaylog.add_event(x4_timestamp, x4_magnitude)
    sue_outlaylog.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_events_dict = sue_outlaylog.get_dict()

    # THEN
    assert sue_events_dict == {
        "owner_id": sue_str,
        "events": {
            x4_timestamp: {"money_magnitude": x4_magnitude, "timestamp": x4_timestamp},
            x7_timestamp: {"money_magnitude": x7_magnitude, "timestamp": x7_timestamp},
        },
    }


def test_get_outlayevent_from_dict_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_outlayevent = outlayevent_shop(t4_timestamp, t4_magnitude)
    t4_dict = t4_outlayevent.get_dict()
    assert t4_dict == {"timestamp": t4_timestamp, "money_magnitude": t4_magnitude}

    # WHEN
    x_outlayevent = get_outlayevent_from_dict(t4_dict)

    # THEN
    assert x_outlayevent
    assert x_outlayevent.timestamp == t4_timestamp
    assert x_outlayevent.money_magnitude == t4_magnitude
    assert x_outlayevent == t4_outlayevent


def test_OutlayLog_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_outlaylog.add_event(x4_timestamp, x4_magnitude)
    sue_outlaylog.add_event(x7_timestamp, x7_magnitude)
    sue_events_dict = sue_outlaylog.get_dict()
    assert sue_events_dict == {
        "owner_id": sue_str,
        "events": {
            x4_timestamp: {"timestamp": x4_timestamp, "money_magnitude": x4_magnitude},
            x7_timestamp: {"timestamp": x7_timestamp, "money_magnitude": x7_magnitude},
        },
    }

    # WHEN
    x_outlaylog = get_outlaylog_from_dict(sue_events_dict)

    # THEN
    assert x_outlaylog
    assert x_outlaylog.owner_id == sue_str
    assert x_outlaylog.get_event(x4_timestamp) != None
    assert x_outlaylog.get_event(x7_timestamp) != None
    assert x_outlaylog.events == sue_outlaylog.events
    assert x_outlaylog == sue_outlaylog
