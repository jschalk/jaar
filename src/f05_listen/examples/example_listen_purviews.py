from src.f01_road.finance_tran import purviewepisode_shop, PurviewEpisode


def get_purviewepisode_55_example() -> PurviewEpisode:
    x_time_id = 55
    return purviewepisode_shop(x_time_id)


def get_purviewepisode_66_example() -> PurviewEpisode:
    t66_time_id = 66
    t66_purviewepisode = purviewepisode_shop(t66_time_id)
    t66_purviewepisode.set_net_purview("Sue", -5)
    t66_purviewepisode.set_net_purview("Bob", 5)
    return t66_purviewepisode


def get_purviewepisode_88_example() -> PurviewEpisode:
    t88_time_id = 88
    t88_purviewepisode = purviewepisode_shop(t88_time_id)
    t88_purviewepisode.quota = 800
    return t88_purviewepisode


def get_purviewepisode_invalid_example() -> PurviewEpisode:
    t55_time_id = 55
    t55_purviewepisode = purviewepisode_shop(t55_time_id)
    t55_purviewepisode.set_net_purview("Sue", -5)
    t55_purviewepisode.set_net_purview("Bob", 3)
    return t55_purviewepisode
