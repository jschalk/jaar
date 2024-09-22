from src.s3_chrono.bud_event import (
    OwnerBudEvent,
    ownerbudevent_shop,
    OwnerBudEvents,
    ownerbudevents_shop,
    get_ownerbudevent_from_dict,
    get_ownerbudevents_from_dict,
)


def test_OwnerBudEvent_Exists():
    # ESTABLISH / WHEN
    x_ownerbudevent = OwnerBudEvent()

    # THEN
    assert x_ownerbudevent
    assert not x_ownerbudevent.timestamp
    assert not x_ownerbudevent.money_magnitude
    assert not x_ownerbudevent._bud
    assert not x_ownerbudevent._money_desc


def test_ownerbudevent_shop_ReturnsObj():
    # ESTABLISH
    y_timestamp = 4
    y_magnitude = 55

    # WHEN
    x_ownerbudevent = ownerbudevent_shop(y_timestamp, y_magnitude)

    # THEN
    assert x_ownerbudevent
    assert x_ownerbudevent.timestamp == y_timestamp
    assert x_ownerbudevent.money_magnitude == y_magnitude
    assert not x_ownerbudevent._bud
    assert not x_ownerbudevent._money_desc


def test_OwnerBudEvent_get_array_ReturnsObj():
    # ESTABLISH
    y_timestamp = 4
    y_magnitude = 55
    x_ownerbudevent = ownerbudevent_shop(y_timestamp, y_magnitude)

    # WHEN
    x_array = x_ownerbudevent.get_array()

    # THEN
    assert x_array == [y_timestamp, y_magnitude]


def test_OwnerBudEvent_get_dict_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_ownerbudevent = ownerbudevent_shop(t4_timestamp, t4_magnitude)

    # WHEN
    t4_dict = t4_ownerbudevent.get_dict()

    # THEN
    assert t4_dict == {"timestamp": t4_timestamp, "money_magnitude": t4_magnitude}


def test_OwnerBudEvents_Exists():
    # ESTABLISH / WHEN
    x_ownerbudevents = OwnerBudEvents()

    # THEN
    assert x_ownerbudevents
    assert not x_ownerbudevents.owner_id
    assert not x_ownerbudevents.events
    assert not x_ownerbudevents._sum_money_magnitude
    assert not x_ownerbudevents._sum_acct_outlays
    assert not x_ownerbudevents._timestamp_min
    assert not x_ownerbudevents._timestamp_max


def test_ownerbudevents_shop_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"

    # WHEN
    x_ownerbudevents = ownerbudevents_shop(sue_str)

    # THEN
    assert x_ownerbudevents
    assert x_ownerbudevents.owner_id == sue_str
    assert x_ownerbudevents.events == {}
    assert not x_ownerbudevents._sum_money_magnitude
    assert x_ownerbudevents._sum_acct_outlays == {}
    assert not x_ownerbudevents._timestamp_min
    assert not x_ownerbudevents._timestamp_max


def test_OwnerBudEvents_set_event_SetsAttr():
    # ESTABLISH
    sue_ownerbudevents = ownerbudevents_shop("sue")
    assert sue_ownerbudevents.events == {}

    # WHEN
    t1_int = 145
    t1_ownerbudevent = ownerbudevent_shop(t1_int, 0)
    sue_ownerbudevents.set_event(t1_ownerbudevent)

    # THEN
    assert sue_ownerbudevents.events != {}
    assert sue_ownerbudevents.events.get(t1_int) == t1_ownerbudevent


def test_OwnerBudEvents_event_exists_ReturnsObj():
    # ESTABLISH
    sue_ownerbudevents = ownerbudevents_shop("Sue")
    t1_int = 145
    assert sue_ownerbudevents.event_exists(t1_int) is False

    # WHEN
    t1_ownerbudevent = ownerbudevent_shop(t1_int, 0)
    sue_ownerbudevents.set_event(t1_ownerbudevent)

    # THEN
    assert sue_ownerbudevents.event_exists(t1_int)


def test_OwnerBudEvents_get_event_ReturnsObj():
    # ESTABLISH
    sue_ownerbudevents = ownerbudevents_shop("sue")
    t1_int = 145
    t1_stat_ownerbudevent = ownerbudevent_shop(t1_int, 0)
    sue_ownerbudevents.set_event(t1_stat_ownerbudevent)

    # WHEN
    t1_gen_ownerbudevent = sue_ownerbudevents.get_event(t1_int)

    # THEN
    assert t1_gen_ownerbudevent
    assert t1_gen_ownerbudevent == t1_stat_ownerbudevent


def test_OwnerBudEvents_del_event_SetsAttr():
    # ESTABLISH
    sue_ownerbudevents = ownerbudevents_shop("Sue")
    t1_int = 145
    t1_stat_ownerbudevent = ownerbudevent_shop(t1_int, 0)
    sue_ownerbudevents.set_event(t1_stat_ownerbudevent)
    assert sue_ownerbudevents.event_exists(t1_int)

    # WHEN
    sue_ownerbudevents.del_event(t1_int)

    # THEN
    assert sue_ownerbudevents.event_exists(t1_int) is False


def test_OwnerBudEvents_add_event_SetsAttr():
    # ESTABLISH
    sue_ownerbudevents = ownerbudevents_shop("sue")
    assert sue_ownerbudevents.events == {}

    # WHEN
    t1_int = 145
    t1_money_magnitude = 500
    sue_ownerbudevents.add_event(t1_int, t1_money_magnitude)

    # THEN
    assert sue_ownerbudevents.events != {}
    t1_ownerbudevent = ownerbudevent_shop(t1_int, t1_money_magnitude)
    assert sue_ownerbudevents.events.get(t1_int) == t1_ownerbudevent


def test_OwnerBudEvents_get_2d_array_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_ownerbudevents = ownerbudevents_shop(sue_str)

    # WHEN
    sue_events_2d_array = sue_ownerbudevents.get_2d_array()

    # THEN
    assert sue_events_2d_array == []


def test_OwnerBudEvents_get_2d_array_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_ownerbudevents.add_event(x4_timestamp, x4_magnitude)
    sue_ownerbudevents.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_events_2d_array = sue_ownerbudevents.get_2d_array()

    # THEN
    assert sue_events_2d_array == [
        [sue_str, x4_timestamp, x4_magnitude],
        [sue_str, x7_timestamp, x7_magnitude],
    ]


def test_OwnerBudEvents_get_headers_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_ownerbudevents.add_event(x4_timestamp, x4_magnitude)
    sue_ownerbudevents.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_headers_list = sue_ownerbudevents.get_headers()

    # THEN
    assert sue_headers_list == ["owner_id", "timestamp", "money_magnitude"]


def test_OwnerBudEvents_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_ownerbudevents.add_event(x4_timestamp, x4_magnitude)
    sue_ownerbudevents.add_event(x7_timestamp, x7_magnitude)

    # WHEN
    sue_events_dict = sue_ownerbudevents.get_dict()

    # THEN
    assert sue_events_dict == {
        "owner_id": sue_str,
        "events": {
            x4_timestamp: {"money_magnitude": x4_magnitude},
            x7_timestamp: {"money_magnitude": x7_magnitude},
        },
    }


def test_get_ownerbudevent_from_dict_ReturnsObj():
    # ESTABLISH
    t4_timestamp = 4
    t4_magnitude = 55
    t4_ownerbudevent = ownerbudevent_shop(t4_timestamp, t4_magnitude)
    t4_dict = t4_ownerbudevent.get_dict()
    assert t4_dict == {"timestamp": t4_timestamp, "money_magnitude": t4_magnitude}

    # WHEN
    x_ownerbudevent = get_ownerbudevent_from_dict(t4_dict)

    # THEN
    assert x_ownerbudevent
    assert x_ownerbudevent.timestamp == t4_timestamp
    assert x_ownerbudevent.money_magnitude == t4_magnitude
    assert x_ownerbudevent == t4_ownerbudevent


def test_OwnerBudEvents_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_ownerbudevents = ownerbudevents_shop(sue_str)
    x4_timestamp = 4
    x4_magnitude = 55
    x7_timestamp = 7
    x7_magnitude = 66
    sue_ownerbudevents.add_event(x4_timestamp, x4_magnitude)
    sue_ownerbudevents.add_event(x7_timestamp, x7_magnitude)
    sue_events_dict = sue_ownerbudevents.get_dict()
    assert sue_events_dict == {
        "owner_id": sue_str,
        "events": {
            x4_timestamp: {"timestamp": x4_timestamp, "money_magnitude": x4_magnitude},
            x7_timestamp: {"timestamp": x7_timestamp, "money_magnitude": x7_magnitude},
        },
    }

    # WHEN
    x_ownerbudevents = get_ownerbudevents_from_dict(sue_events_dict)

    # THEN
    assert x_ownerbudevents
    assert x_ownerbudevents.owner_id == sue_str
    assert x_ownerbudevents.get_event(x4_timestamp) != None
    assert x_ownerbudevents.get_event(x7_timestamp) != None
    assert x_ownerbudevents.events == sue_ownerbudevents.events
    assert x_ownerbudevents == sue_ownerbudevents
