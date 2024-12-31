from src.f01_road.finance_tran import bankepisode_shop, BankEpisode


def get_bankepisode_55_example() -> BankEpisode:
    x_time_int = 55
    return bankepisode_shop(x_time_int)


def get_bankepisode_66_example() -> BankEpisode:
    t66_time_int = 66
    t66_bankepisode = bankepisode_shop(t66_time_int)
    t66_bankepisode.set_net_bank("Sue", -5)
    t66_bankepisode.set_net_bank("Bob", 5)
    return t66_bankepisode


def get_bankepisode_88_example() -> BankEpisode:
    t88_time_int = 88
    t88_bankepisode = bankepisode_shop(t88_time_int)
    t88_bankepisode.quota = 800
    return t88_bankepisode


def get_bankepisode_invalid_example() -> BankEpisode:
    t55_time_int = 55
    t55_bankepisode = bankepisode_shop(t55_time_int)
    t55_bankepisode.set_net_bank("Sue", -5)
    t55_bankepisode.set_net_bank("Bob", 3)
    return t55_bankepisode
