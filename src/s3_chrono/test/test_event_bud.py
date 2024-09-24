from src.s3_chrono.bud_event import (
    BudEvent,
    budevent_shop,
    BudLog,
    budlog_shop,
    get_budevent_from_dict,
    get_budlog_from_dict,
)


def test_BudEvent_Exists():
    # ESTABLISH / WHEN
    x_budevent = BudEvent()

    # THEN
    assert x_budevent
    assert not x_budevent.timestamp
    assert not x_budevent.money_magnitude
    assert not x_budevent._bud
    assert not x_budevent._money_desc


def test_budevent_shop_ReturnsObj():
    # ESTABLISH
    y_timestamp = 4
    y_magnitude = 55

    # WHEN
    x_budevent = budevent_shop(y_timestamp, y_magnitude)

    # THEN
    assert x_budevent
    assert x_budevent.timestamp == y_timestamp
    assert x_budevent.money_magnitude == y_magnitude
    assert not x_budevent._bud
    assert not x_budevent._money_desc


def test_BudEvent_get_array_ReturnsObj():
    # ESTABLISH
    y_timestamp = 4
    y_magnitude = 55
    x_budevent = budevent_shop(y_timestamp, y_magnitude)

    # WHEN
    x_array = x_budevent.get_array()

    # THEN
    assert x_array == [y_timestamp, y_magnitude]


def test_BudEvent_get_dict_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_budevent = budevent_shop(t4_timestamp, t4_magnitude)

    # WHEN
    t4_dict = t4_budevent.get_dict()

    # THEN
    assert t4_dict == {"timestamp": t4_timestamp, "money_magnitude": t4_magnitude}


def test_BudLog_Exists():
    # ESTABLISH / WHEN
    x_budlog = BudLog()

    # THEN
    assert x_budlog
    assert not x_budlog.owner_id
    assert not x_budlog.events
    assert not x_budlog._sum_money_magnitude
    assert not x_budlog._sum_acct_outlays
    assert not x_budlog._timestamp_min
    assert not x_budlog._timestamp_max


def test_budlog_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_budlog = budlog_shop(sue_str)

    # THEN
    assert x_budlog
    assert x_budlog.owner_id == sue_str
    assert x_budlog.events == {}
    assert not x_budlog._sum_money_magnitude
    assert x_budlog._sum_acct_outlays == {}
    assert not x_budlog._timestamp_min
    assert not x_budlog._timestamp_max


def test_BudLog_set_event_SetsAttr():
    # ESTABLISH
    sue_budlog = budlog_shop("sue")
    assert sue_budlog.events == {}

    # WHEN
    t1_int = 145
    t1_budevent = budevent_shop(t1_int, 0)
    sue_budlog.set_event(t1_budevent)

    # THEN
    assert sue_budlog.events != {}
    assert sue_budlog.events.get(t1_int) == t1_budevent


def test_BudLog_event_exists_ReturnsObj():
    # ESTABLISH
    sue_budlog = budlog_shop("Sue")
    t1_int = 145
    assert sue_budlog.event_exists(t1_int) is False

    # WHEN
    t1_budevent = budevent_shop(t1_int, 0)
    sue_budlog.set_event(t1_budevent)

    # THEN
    assert sue_budlog.event_exists(t1_int)


def test_BudLog_get_event_ReturnsObj():
    # ESTABLISH
    sue_budlog = budlog_shop("sue")
    t1_int = 145
    t1_stat_budevent = budevent_shop(t1_int, 0)
    sue_budlog.set_event(t1_stat_budevent)

    # WHEN
    t1_gen_budevent = sue_budlog.get_event(t1_int)

    # THEN
    assert t1_gen_budevent
    assert t1_gen_budevent == t1_stat_budevent


def test_BudLog_del_event_SetsAttr():
    # ESTABLISH
    sue_budlog = budlog_shop("Sue")
    t1_int = 145
    t1_stat_budevent = budevent_shop(t1_int, 0)
    sue_budlog.set_event(t1_stat_budevent)
    assert sue_budlog.event_exists(t1_int)

    # WHEN
    sue_budlog.del_event(t1_int)

    # THEN
    assert sue_budlog.event_exists(t1_int) is False


def test_BudLog_add_event_SetsAttr():
    # ESTABLISH
    sue_budlog = budlog_shop("sue")
    assert sue_budlog.events == {}

    # WHEN
    t1_int = 145
    t1_money_magnitude = 500
    sue_budlog.add_event(t1_int, t1_money_magnitude)

    # THEN
    assert sue_budlog.events != {}
    t1_budevent = budevent_shop(t1_int, t1_money_magnitude)
    assert sue_budlog.events.get(t1_int) == t1_budevent


def test_BudLog_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_budlog = budlog_shop(sue_str)

    # WHEN
    sue_events_2d_array = sue_budlog.get_2d_array()

    # THEN
    assert sue_events_2d_array == []


def test_BudLog_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_budlog = budlog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_budlog.add_event(x4_timestamp, x4_magnitude)
    sue_budlog.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_events_2d_array = sue_budlog.get_2d_array()

    # THEN
    assert sue_events_2d_array == [
        [sue_str, x4_timestamp, x4_magnitude],
        [sue_str, x7_timestamp, x7_magnitude],
    ]


def test_BudLog_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_budlog = budlog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_budlog.add_event(x4_timestamp, x4_magnitude)
    sue_budlog.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_headers_list = sue_budlog.get_headers()

    # THEN
    assert sue_headers_list == ["owner_id", "timestamp", "money_magnitude"]


def test_BudLog_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_budlog = budlog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_budlog.add_event(x4_timestamp, x4_magnitude)
    sue_budlog.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_events_dict = sue_budlog.get_dict()

    # THEN
    assert sue_events_dict == {
        "owner_id": sue_str,
        "events": {
            x4_timestamp: {"money_magnitude": x4_magnitude},
            x7_timestamp: {"money_magnitude": x7_magnitude},
        },
    }


def test_get_budevent_from_dict_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_budevent = budevent_shop(t4_timestamp, t4_magnitude)
    t4_dict = t4_budevent.get_dict()
    assert t4_dict == {"timestamp": t4_timestamp, "money_magnitude": t4_magnitude}

    # WHEN
    x_budevent = get_budevent_from_dict(t4_dict)

    # THEN
    assert x_budevent
    assert x_budevent.timestamp == t4_timestamp
    assert x_budevent.money_magnitude == t4_magnitude
    assert x_budevent == t4_budevent


def test_BudLog_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_budlog = budlog_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_budlog.add_event(x4_timestamp, x4_magnitude)
    sue_budlog.add_event(x7_timestamp, x7_magnitude)
    sue_events_dict = sue_budlog.get_dict()
    assert sue_events_dict == {
        "owner_id": sue_str,
        "events": {
            x4_timestamp: {"timestamp": x4_timestamp, "money_magnitude": x4_magnitude},
            x7_timestamp: {"timestamp": x7_timestamp, "money_magnitude": x7_magnitude},
        },
    }

    # WHEN
    x_budlog = get_budlog_from_dict(sue_events_dict)

    # THEN
    assert x_budlog
    assert x_budlog.owner_id == sue_str
    assert x_budlog.get_event(x4_timestamp) != None
    assert x_budlog.get_event(x7_timestamp) != None
    assert x_budlog.events == sue_budlog.events
    assert x_budlog == sue_budlog
