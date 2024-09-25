from src.s1_road.finance_outlay import (
    OutlayEvent,
    outlayevent_shop,
    OutlayLog,
    outlaylog_shop,
    get_outlayevent_from_dict,
    get_outlaylog_from_dict,
)
from pytest import raises as pytest_raises


def test_OutlayEvent_Exists():
    # ESTABLISH / WHEN
    x_outlayevent = OutlayEvent()

    # THEN
    assert x_outlayevent
    assert not x_outlayevent.timestamp
    assert not x_outlayevent._magnitude
    assert not x_outlayevent._net_outlays
    assert not x_outlayevent._tender_desc


def test_outlayevent_shop_ReturnsObj():
    # ESTABLISH
    y_timestamp = 4

    # WHEN
    x_outlayevent = outlayevent_shop(y_timestamp)

    # THEN
    assert x_outlayevent
    assert x_outlayevent.timestamp == y_timestamp
    assert x_outlayevent._magnitude == 0
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
    assert x_outlayevent._magnitude == y_magnitude
    assert x_outlayevent._net_outlays == y_net_outlays
    assert not x_outlayevent._tender_desc


def test_OutlayEvent_set_net_outlay_SetsAttr():
    # ESTABLISH
    yao_outlayevent = outlayevent_shop("yao", 33)
    assert yao_outlayevent._net_outlays == {}

    # WHEN
    sue_text = "Sue"
    sue_outlay = -44
    yao_outlayevent.set_net_outlay(sue_text, sue_outlay)

    # THEN
    assert yao_outlayevent._net_outlays != {}
    assert yao_outlayevent._net_outlays.get(sue_text) == sue_outlay


def test_OutlayEvent_net_outlay_exists_ReturnsObj():
    # ESTABLISH
    yao_outlayevent = outlayevent_shop("yao", 33)
    sue_text = "Sue"
    sue_outlay = -44
    assert yao_outlayevent.net_outlay_exists(sue_text) is False

    # WHEN
    yao_outlayevent.set_net_outlay(sue_text, sue_outlay)

    # THEN
    assert yao_outlayevent.net_outlay_exists(sue_text)


def test_OutlayEvent_get_net_outlay_ReturnsObj():
    # ESTABLISH
    yao_outlayevent = outlayevent_shop("yao", 33)
    sue_text = "Sue"
    sue_outlay = -44
    yao_outlayevent.set_net_outlay(sue_text, sue_outlay)

    # WHEN / THEN
    assert yao_outlayevent.get_net_outlay(sue_text)
    assert yao_outlayevent.get_net_outlay(sue_text) == sue_outlay


def test_OutlayEvent_del_net_outlay_SetsAttr():
    # ESTABLISH
    yao_outlayevent = outlayevent_shop("yao", 33)
    sue_text = "Sue"
    sue_outlay = -44
    yao_outlayevent.set_net_outlay(sue_text, sue_outlay)
    assert yao_outlayevent.net_outlay_exists(sue_text)

    # WHEN
    yao_outlayevent.del_net_outlay(sue_text)

    # THEN
    assert yao_outlayevent.net_outlay_exists(sue_text) is False


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
    assert t4_dict == {"timestamp": t4_timestamp, "magnitude": t4_magnitude}


def test_OutlayEvent_calc_magnitude_SetsAttr_Scenario0():
    # ESTABLISH
    t4_timestamp = 4
    t4_outlayevent = outlayevent_shop(t4_timestamp)
    assert t4_outlayevent._magnitude == 0

    # WHEN
    t4_outlayevent.calc_magnitude()

    # THEN
    assert t4_outlayevent._magnitude == 0


def test_OutlayEvent_calc_magnitude_SetsAttr_Scenario1():
    # ESTABLISH
    t4_timestamp = 4
    t4_net_outlays = {"Sue": -4, "Yao": 2, "Zia": 2}

    t4_outlayevent = outlayevent_shop(t4_timestamp, net_outlays=t4_net_outlays)
    assert t4_outlayevent._magnitude == 0

    # WHEN
    t4_outlayevent.calc_magnitude()

    # THEN
    assert t4_outlayevent._magnitude == 4


def test_OutlayEvent_calc_magnitude_SetsAttr_Scenario2():
    # ESTABLISH
    t4_timestamp = 4
    t4_net_outlays = {"Bob": -13, "Sue": -7, "Yao": 18, "Zia": 2}

    t4_outlayevent = outlayevent_shop(t4_timestamp, net_outlays=t4_net_outlays)
    assert t4_outlayevent._magnitude == 0

    # WHEN
    t4_outlayevent.calc_magnitude()

    # THEN
    assert t4_outlayevent._magnitude == 20


def test_OutlayEvent_calc_magnitude_SetsAttr_Scenario3_RaisesError():
    # ESTABLISH
    t4_timestamp = 4
    bob_outlay = -13
    sue_outlay = -3
    yao_outlay = 100
    t4_net_outlays = {"Bob": bob_outlay, "Sue": sue_outlay, "Yao": yao_outlay}
    t4_outlayevent = outlayevent_shop(t4_timestamp, net_outlays=t4_net_outlays)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        t4_outlayevent.calc_magnitude()
    exception_str = f"magnitude cannot be calculated: debt_outlay={bob_outlay+sue_outlay}, cred_outlay={yao_outlay}"
    assert str(excinfo.value) == exception_str


def test_OutlayEvent_get_dict_ReturnsObjWith_net_outlays():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_net_outlays = {"Sue": -4}
    t4_outlayevent = outlayevent_shop(t4_timestamp, t4_magnitude, t4_net_outlays)

    # WHEN
    t4_dict = t4_outlayevent.get_dict()

    # THEN
    assert t4_dict == {
        "timestamp": t4_timestamp,
        "magnitude": t4_magnitude,
        "net_outlays": t4_net_outlays,
    }


def test_get_outlayevent_from_dict_ReturnsObj_Sccenario0():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_outlayevent = outlayevent_shop(t4_timestamp, t4_magnitude)
    t4_dict = t4_outlayevent.get_dict()
    assert t4_dict == {"timestamp": t4_timestamp, "magnitude": t4_magnitude}

    # WHEN
    x_outlayevent = get_outlayevent_from_dict(t4_dict)

    # THEN
    assert x_outlayevent
    assert x_outlayevent.timestamp == t4_timestamp
    assert x_outlayevent._magnitude == t4_magnitude
    assert x_outlayevent == t4_outlayevent


def test_get_outlayevent_from_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_net_outlays = {"Sue": -4}
    t4_outlayevent = outlayevent_shop(t4_timestamp, t4_magnitude, t4_net_outlays)
    t4_dict = t4_outlayevent.get_dict()

    # WHEN
    x_outlayevent = get_outlayevent_from_dict(t4_dict)

    # THEN
    assert x_outlayevent
    assert x_outlayevent.timestamp == t4_timestamp
    assert x_outlayevent._magnitude == t4_magnitude
    assert x_outlayevent._net_outlays == t4_net_outlays
    assert x_outlayevent == t4_outlayevent


def test_OutlayLog_Exists():
    # ESTABLISH / WHEN
    x_outlaylog = OutlayLog()

    # THEN
    assert x_outlaylog
    assert not x_outlaylog.owner_id
    assert not x_outlaylog.events
    assert not x_outlaylog._sum_outlayevent_magnitude
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
    assert not x_outlaylog._sum_outlayevent_magnitude
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
    t1__magnitude = 500
    sue_outlaylog.add_event(t1_int, t1__magnitude)

    # THEN
    assert sue_outlaylog.events != {}
    t1_outlayevent = outlayevent_shop(t1_int, t1__magnitude)
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
    assert sue_headers_list == ["owner_id", "timestamp", "magnitude"]


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
            x4_timestamp: {"magnitude": x4_magnitude, "timestamp": x4_timestamp},
            x7_timestamp: {"magnitude": x7_magnitude, "timestamp": x7_timestamp},
        },
    }


def test_get_outlaylog_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    sue_events_dict = sue_outlaylog.get_dict()
    assert sue_events_dict == {"owner_id": sue_str, "events": {}}

    # WHEN
    x_outlaylog = get_outlaylog_from_dict(sue_events_dict)

    # THEN
    assert x_outlaylog
    assert x_outlaylog.owner_id == sue_str
    assert x_outlaylog.events == {}
    assert x_outlaylog.events == sue_outlaylog.events
    assert x_outlaylog == sue_outlaylog


def test_get_outlaylog_from_dict_ReturnsObj_Scenario1():
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
            x4_timestamp: {"timestamp": x4_timestamp, "magnitude": x4_magnitude},
            x7_timestamp: {"timestamp": x7_timestamp, "magnitude": x7_magnitude},
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


def test_get_outlaylog_from_dict_ReturnsObj_Scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_outlaylog = outlaylog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_outlaylog.add_event(x4_timestamp, x4_magnitude)
    sue_outlaylog.add_event(x7_timestamp, x7_magnitude)
    zia_str = "Zia"
    zia_net_outlay = 887
    sue_net_outlay = 445
    sue_outlaylog.get_event(x7_timestamp).set_net_outlay(sue_str, sue_net_outlay)
    sue_outlaylog.get_event(x7_timestamp).set_net_outlay(zia_str, zia_net_outlay)
    sue_events_dict = sue_outlaylog.get_dict()
    assert sue_events_dict == {
        "owner_id": sue_str,
        "events": {
            x4_timestamp: {"timestamp": x4_timestamp, "magnitude": x4_magnitude},
            x7_timestamp: {
                "timestamp": x7_timestamp,
                "magnitude": x7_magnitude,
                "net_outlays": {sue_str: sue_net_outlay, zia_str: zia_net_outlay},
            },
        },
    }

    # WHEN
    x_outlaylog = get_outlaylog_from_dict(sue_events_dict)

    # THEN
    assert x_outlaylog
    assert x_outlaylog.owner_id == sue_str
    assert x_outlaylog.get_event(x4_timestamp) != None
    assert x_outlaylog.get_event(x7_timestamp) != None
    assert x_outlaylog.get_event(x7_timestamp)._net_outlays != {}
    assert len(x_outlaylog.get_event(x7_timestamp)._net_outlays) == 2
    assert x_outlaylog.events == sue_outlaylog.events
    assert x_outlaylog == sue_outlaylog
