from src.f01_road.finance_tran import pactepisode_shop, PactEpisode


def get_pactepisode_55_example() -> PactEpisode:
    x_time_int = 55
    return pactepisode_shop(x_time_int)


def get_pactepisode_66_example() -> PactEpisode:
    t66_time_int = 66
    t66_pactepisode = pactepisode_shop(t66_time_int)
    t66_pactepisode.set_net_pact("Sue", -5)
    t66_pactepisode.set_net_pact("Bob", 5)
    return t66_pactepisode


def get_pactepisode_88_example() -> PactEpisode:
    t88_time_int = 88
    t88_pactepisode = pactepisode_shop(t88_time_int)
    t88_pactepisode.quota = 800
    return t88_pactepisode


def get_pactepisode_invalid_example() -> PactEpisode:
    t55_time_int = 55
    t55_pactepisode = pactepisode_shop(t55_time_int)
    t55_pactepisode.set_net_pact("Sue", -5)
    t55_pactepisode.set_net_pact("Bob", 3)
    return t55_pactepisode
