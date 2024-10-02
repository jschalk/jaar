from src.f1_road.finance_tran import outlayepisode_shop, OutlayEpisode


def get_outlayepisode_55_example() -> OutlayEpisode:
    x_timestamp = 55
    return outlayepisode_shop(x_timestamp)


def get_outlayepisode_66_example() -> OutlayEpisode:
    t66_timestamp = 66
    t66_outlayepisode = outlayepisode_shop(t66_timestamp)
    t66_outlayepisode.set_net_outlay("Sue", -5)
    t66_outlayepisode.set_net_outlay("Bob", 5)
    return t66_outlayepisode


def get_outlayepisode_88_example() -> OutlayEpisode:
    t88_timestamp = 88
    t88_outlayepisode = outlayepisode_shop(t88_timestamp)
    t88_outlayepisode.purview = 800
    return t88_outlayepisode


def get_outlayepisode_invalid_example() -> OutlayEpisode:
    t55_timestamp = 55
    t55_outlayepisode = outlayepisode_shop(t55_timestamp)
    t55_outlayepisode.set_net_outlay("Sue", -5)
    t55_outlayepisode.set_net_outlay("Bob", 3)
    return t55_outlayepisode
