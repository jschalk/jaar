from src.f01_road.deal import dealepisode_shop, DealEpisode


def get_dealepisode_55_example() -> DealEpisode:
    x_time_int = 55
    return dealepisode_shop(x_time_int)


def get_dealepisode_66_example() -> DealEpisode:
    t66_time_int = 66
    t66_dealepisode = dealepisode_shop(t66_time_int)
    t66_dealepisode.set_net_deal("Sue", -5)
    t66_dealepisode.set_net_deal("Bob", 5)
    return t66_dealepisode


def get_dealepisode_88_example() -> DealEpisode:
    t88_time_int = 88
    t88_dealepisode = dealepisode_shop(t88_time_int)
    t88_dealepisode.quota = 800
    return t88_dealepisode


def get_dealepisode_invalid_example() -> DealEpisode:
    t55_time_int = 55
    t55_dealepisode = dealepisode_shop(t55_time_int)
    t55_dealepisode.set_net_deal("Sue", -5)
    t55_dealepisode.set_net_deal("Bob", 3)
    return t55_dealepisode
