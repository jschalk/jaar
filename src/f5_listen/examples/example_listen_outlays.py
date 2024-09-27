from src.f1_road.finance_tran import outlayevent_shop, OutlayEvent


def get_outlayevent_55_example() -> OutlayEvent:
    x_timestamp = 55
    return outlayevent_shop(x_timestamp)


def get_outlayevent_66_example() -> OutlayEvent:
    t66_timestamp = 66
    t66_outlayevent = outlayevent_shop(t66_timestamp)
    t66_outlayevent.set_net_outlay("Sue", -5)
    t66_outlayevent.set_net_outlay("Bob", 5)
    return t66_outlayevent


def get_outlayevent_88_example() -> OutlayEvent:
    t88_timestamp = 88
    t88_outlayevent = outlayevent_shop(t88_timestamp)
    t88_outlayevent.purview = 800
    return t88_outlayevent


def get_outlayevent_invalid_example() -> OutlayEvent:
    t55_timestamp = 55
    t55_outlayevent = outlayevent_shop(t55_timestamp)
    t55_outlayevent.set_net_outlay("Sue", -5)
    t55_outlayevent.set_net_outlay("Bob", 3)
    return t55_outlayevent
