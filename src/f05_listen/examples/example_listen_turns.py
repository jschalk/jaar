from src.f01_road.finance_tran import turnepisode_shop, TurnEpisode


def get_turnepisode_55_example() -> TurnEpisode:
    x_time_int = 55
    return turnepisode_shop(x_time_int)


def get_turnepisode_66_example() -> TurnEpisode:
    t66_time_int = 66
    t66_turnepisode = turnepisode_shop(t66_time_int)
    t66_turnepisode.set_net_turn("Sue", -5)
    t66_turnepisode.set_net_turn("Bob", 5)
    return t66_turnepisode


def get_turnepisode_88_example() -> TurnEpisode:
    t88_time_int = 88
    t88_turnepisode = turnepisode_shop(t88_time_int)
    t88_turnepisode.quota = 800
    return t88_turnepisode


def get_turnepisode_invalid_example() -> TurnEpisode:
    t55_time_int = 55
    t55_turnepisode = turnepisode_shop(t55_time_int)
    t55_turnepisode.set_net_turn("Sue", -5)
    t55_turnepisode.set_net_turn("Bob", 3)
    return t55_turnepisode
